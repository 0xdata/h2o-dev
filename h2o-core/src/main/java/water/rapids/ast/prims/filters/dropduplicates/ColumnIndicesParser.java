package water.rapids.ast.prims.filters.dropduplicates;

import water.fvec.Frame;
import water.fvec.Vec;
import water.rapids.Val;

public class ColumnIndicesParser {

  /**
   * @param deduplicatedFrame Deduplicated frame to look for vectors in
   * @param comparedColumns   A {@link Val} instance of columns to be compared during row de-duplication process.
   *                          Accepts {@link water.rapids.ast.params.AstStr}, {@link water.rapids.ast.params.AstStrList},
   *                          and {@link water.rapids.ast.params.AstNumList}.
   * @return An array if primitive integers with indices of vectorss
   * @throws IllegalArgumentException If comparedColumns field is not of given type. If any given column is not
   *                                  recognized in deduplicatedFrame or if any column compared has unsupported type.
   */
  public static int[] parseAndCheckComparedColumnIndices(final Frame deduplicatedFrame, final Val comparedColumns)
      throws IllegalArgumentException {
    final int[] columnRange;

    if (comparedColumns.isStr()) {
      final String columnName = comparedColumns.getStr();
      final int columnIndex = deduplicatedFrame.find(columnName);
      if (columnIndex == -1) {
        throw new IllegalArgumentException(String.format("Unknown column name: '%s'", columnName));
      }
      columnRange = new int[]{columnIndex};
    } else if (comparedColumns.isStrs()) {
      final String[] columnNames = comparedColumns.getStrs();
      columnRange = new int[columnNames.length];

      for (int i = 0; i < columnNames.length; i++) {
        final String columnName = columnNames[i];
        final int columnIndex = deduplicatedFrame.find(columnName);
        if (columnIndex == -1) {
          throw new IllegalArgumentException(String.format("Unknown column name: '%s'", columnName));
        } else if (isUnsupportedVecType(deduplicatedFrame.types()[columnIndex])) {
          throw new IllegalArgumentException(String.format("Column '%s' is of unsupported type %s for row de-duplication.",
              columnName, Vec.TYPE_STR[deduplicatedFrame.types()[columnIndex]]));
        }
        columnRange[i] = columnIndex;
      }

    } else if (comparedColumns.isNums()) {
      final double[] columnRangeDouble = comparedColumns.getNums();
      columnRange = new int[columnRangeDouble.length];
      for (int i = 0; i < columnRangeDouble.length; i++) {
        columnRange[i] = (int) columnRangeDouble[i];
        if (columnRange[i] < 0 || columnRange[i] > deduplicatedFrame.numCols() - 1) {
          throw new IllegalArgumentException(String.format("No such column index: '%d', frame has %d columns," +
              "maximum index is %d.", columnRange[i], deduplicatedFrame.numCols(), deduplicatedFrame.numCols() - 1));
        } else if (isUnsupportedVecType(deduplicatedFrame.types()[columnRange[i]])) {
          throw new IllegalArgumentException(String.format("Column '%s' is of unsupported type %s for row de-duplication.",
              deduplicatedFrame.name(columnRange[i]),
              Vec.TYPE_STR[deduplicatedFrame.types()[columnRange[i]]]));
        }
      }
    } else {
      throw new IllegalArgumentException(String.format("Column range for deduplication must either be a set of columns, or a " +
          "column range. Given type: %s", comparedColumns.type()));
    }

    return columnRange;
  }

  private static boolean isUnsupportedVecType(final byte vecType) {
    return vecType == Vec.T_STR || vecType == Vec.T_BAD || vecType == Vec.T_UUID;
  }
}
