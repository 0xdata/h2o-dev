package water.hive;

import water.util.JSONUtils;

import java.sql.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

@SuppressWarnings({"rawtypes", "unchecked"})
public class JdbcHiveMetadata implements HiveMetaData {

    private static final String SQL_SET_JSON_OUTPUT = "set hive.ddl.output.format=json";
    private static final String SQL_DESCRIBE_TABLE = "DESCRIBE EXTENDED %s";
    private static final String SQL_DESCRIBE_PARTITION = "DESCRIBE EXTENDED %s PARTITION (%s)";
    private static final String SQL_SHOW_PARTS = "SHOW PARTITIONS %s";

    private final String url;

    public JdbcHiveMetadata(String url) {
        this.url = url;
    }

    static class StorableMetadata {
        String location;
        String serializationLib;
        String inputFormat;
        Map<String, String> serDeParams = Collections.emptyMap();
    }

    static class JdbcStorable implements Storable {

        private final String location;
        private final String serializationLib;
        private final String inputFormat;
        private final Map<String, String> serDeParams;

        JdbcStorable(StorableMetadata data) {
            this.location = data.location;
            this.serializationLib = data.serializationLib;
            this.inputFormat = data.inputFormat;
            this.serDeParams = data.serDeParams;
        }

        @Override
        public Map<String, String> getSerDeParams() {
            return serDeParams;
        }

        @Override
        public String getLocation() {
            return location;
        }

        @Override
        public String getSerializationLib() {
            return serializationLib;
        }

        @Override
        public String getInputFormat() {
            return inputFormat;
        }
    }

    static class JdbcPartition extends JdbcStorable implements Partition {

        private final List<String> values;

        JdbcPartition(StorableMetadata meta, List<String> values) {
            super(meta);
            this.values = values;
        }

        @Override
        public List<String> getValues() {
            return values;
        }
    }

    static class JdbcColumn implements Column {

        private final String name;
        private final String type;

        JdbcColumn(String name, String type) {
            this.name = name;
            this.type = type;
        }

        @Override
        public String getName() {
            return name;
        }

        @Override
        public String getType() {
            return type;
        }
    }

    static class JdbcTable extends JdbcStorable implements Table {

        private final String name;
        private final List<Partition> partitions;
        private final List<Column> columns;
        private final List<Column> partitionKeys;

        public JdbcTable(
            String name,
            StorableMetadata meta,
            List<Column> columns,
            List<Partition> partitions,
            List<Column> partitionKeys
        ) {
            super(meta);
            this.name = name;
            this.partitions = partitions;
            this.columns = columns;
            this.partitionKeys = partitionKeys;
        }

        @Override
        public String getName() {
            return name;
        }

        @Override
        public boolean hasPartitions() {
            return !partitionKeys.isEmpty();
        }

        @Override
        public List<Partition> getPartitions() {
            return partitions;
        }

        @Override
        public List<Column> getColumns() {
            return columns;
        }

        @Override
        public List<Column> getPartitionKeys() {
            return partitionKeys;
        }
    }

    private Map<String, Object> executeAndParseJsonResultSet(Connection conn, String query) throws SQLException {
        try (Statement stmt = conn.createStatement()) {
            try (ResultSet rs = stmt.executeQuery(query)) {
                rs.next();
                String json = rs.getString(1);
                return JSONUtils.parse(json);
            }
        }
    }

    @Override
    public Table getTable(String tableName) throws SQLException {
        try (Connection conn = DriverManager.getConnection(url)) {
            try (Statement stmt = conn.createStatement()) {
                stmt.execute(SQL_SET_JSON_OUTPUT);
            }
            return getTable(conn, tableName);
        }
    }

    private Table getTable(Connection conn, String name) throws SQLException {
        String query = String.format(SQL_DESCRIBE_TABLE, name);
        Map<String, Object> tableData = executeAndParseJsonResultSet(conn, query);
        List<Column> columns = readColumns((List<Map<String, Object>>) tableData.get("columns"));
        Map<String, Object> tableInfo = (Map<String, Object>) tableData.get("tableInfo");
        List<Column> partitionKeys = readPartitionKeys(tableInfo);
        columns = columns.subList(0, columns.size() - partitionKeys.size()); // remove partition keys from the end
        List<Partition> partitions = readPartitions(conn, name, partitionKeys);
        StorableMetadata storableData = readStorableMetadata(tableInfo);
        return new JdbcTable(name, storableData, columns, partitions, partitionKeys);
    }

    private StorableMetadata readStorableMetadata(Map<String, Object> tableInfo) {
        StorableMetadata res = new StorableMetadata();
        Map<String, Object> sd = (Map<String, Object>) tableInfo.get("sd");
        res.location = (String) sd.get("location");
        res.inputFormat = (String) sd.get("inputFormat");
        Map serDeInfo = (Map) sd.get("serdeInfo");
        res.serializationLib = (String) serDeInfo.get("serializationLib");
        res.serDeParams = (Map<String, String>) serDeInfo.get("parameters");
        return res;
    }

    private List<Partition> readPartitions(
        Connection conn,
        String tableName,
        List<Column> partitionKeys
    ) throws SQLException {
        if (partitionKeys.isEmpty()) {
            return Collections.emptyList();
        }
        String query = String.format(SQL_SHOW_PARTS, tableName);
        Map<String, Object> partitionsResult = executeAndParseJsonResultSet(conn, query);
        List<Partition> partitions = new ArrayList<>();
        List<Map<String, Object>> partitionsData = (List<Map<String, Object>>) partitionsResult.get("partitions");
        for (Map<String, Object> partition : partitionsData) {
            List<String> values = parsePartitionValues(partition);
            StorableMetadata data = readPartitionMetadata(conn, tableName, partitionKeys, values);
            partitions.add(new JdbcPartition(data, values));
        }
        return partitions;
    }

    private StorableMetadata readPartitionMetadata(
        Connection conn,
        String tableName,
        List<Column> partitionKeys,
        List<String> values
    ) throws SQLException {
        String query = String.format(SQL_DESCRIBE_PARTITION, tableName, toPartitionIdentifier(partitionKeys, values));
        Map<String, Object> data = executeAndParseJsonResultSet(conn, query);
        Map<String, Object> info = (Map<String, Object>) data.get("partitionInfo");
        return readStorableMetadata(info);
    }

    private String toPartitionIdentifier(List<Column> partitionKeys, List<String> values) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < partitionKeys.size(); i++) {
            if (i > 0) sb.append(",");
            sb.append(partitionKeys.get(i).getName()).append(("=")).append(values.get(i));
        }
        return sb.toString();
    }

    private List<String> parsePartitionValues(Map<String, Object> partition) {
        List<String> values = new ArrayList<>();
        List<Map<String, Object>> valuesData = (List<Map<String, Object>>) partition.get("values");
        for (Map<String, Object> value : valuesData) {
            values.add((String) value.get("columnValue"));
        }
        return values;
    }

    private List<Column> readPartitionKeys(Map<String, Object> tableInfo) {
        if (!tableInfo.containsKey("partitionKeys")) {
            return Collections.emptyList();
        } else {
            List<Map<String, Object>> partitionColumns = (List<Map<String, Object>>) tableInfo.get("partitionKeys");
            return readColumns(partitionColumns);
        }
    }

    private List<Column> readColumns(List<Map<String, Object>> columnDataList) {
        List<Column> columns = new ArrayList<>();
        for (Map column : columnDataList) {
            columns.add(new JdbcColumn((String) column.get("name"), (String) column.get("type")));
        }
        return columns;
    }

}
