package water.jdbc;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.contrib.java.lang.system.ProvideSystemProperty;
import org.junit.contrib.java.lang.system.RestoreSystemProperties;
import org.mockito.Mockito;
import org.powermock.api.mockito.PowerMockito;
import water.H2O;
import water.H2ONode;
import water.Paxos;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;

public class SQLManagerTest {

  @Rule
  public final ProvideSystemProperty provideSystemProperty =
      new ProvideSystemProperty(H2O.OptArgs.SYSTEM_PROP_PREFIX + "sql.connections.max", "7");


  @Rule
  public final RestoreSystemProperties restoreSystemProperties = new RestoreSystemProperties();

  private Field cloudSizeField;
  private Field currentRuntimeField;

  @Before
  public void setUp() throws Exception {
    Paxos._commonKnowledge = true;
    cloudSizeField = H2O.class.getField("_memary");
    cloudSizeField.setAccessible(true);

    Field modifiersField = Field.class.getDeclaredField("modifiers");
    modifiersField.setAccessible(true);
    modifiersField.setInt(cloudSizeField, cloudSizeField.getModifiers() & ~Modifier.FINAL);

    currentRuntimeField = Runtime.class.getDeclaredField("currentRuntime");
    currentRuntimeField.setAccessible(true);
    modifiersField.setInt(currentRuntimeField, currentRuntimeField.getModifiers() & ~Modifier.FINAL);

  }

  @Test
  public void testConnectionPoolSize() throws Exception {
    // Cloud size 1
    cloudSizeField.set(H2O.CLOUD, new H2ONode[1]);
    Runtime runtime = PowerMockito.spy(Runtime.getRuntime());
    // This ensures unified behavior of such test across various environments
    Mockito.when(runtime.availableProcessors()).thenReturn(100);
    currentRuntimeField.set(null, runtime);
    // Verify there are truly 100 processors returned available
    Assert.assertEquals(100, Runtime.getRuntime().availableProcessors());

    SQLManager.SqlTableToH2OFrame frame = new SQLManager.SqlTableToH2OFrame("", "", false,
        "", "", "", 1, 10, null);

    Integer maxConnectionsPerNode = frame.getMaxConnectionsPerNode();
    //Even if there are 100 available processors on a single node, there should be only limited number of connections
    // in the pool.
    Assert.assertEquals(Integer.valueOf(System.getProperty(H2O.OptArgs.SYSTEM_PROP_PREFIX + "sql.connections.max")),
        maxConnectionsPerNode);
  }

  @Test
  public void testConnectionPoolSizeOneProcessor() throws Exception {
    // Cloud size 1
    cloudSizeField.set(H2O.CLOUD, new H2ONode[1]);
    Runtime runtime = PowerMockito.spy(Runtime.getRuntime());
    // This ensures unified behavior of such test across various environments
    Mockito.when(runtime.availableProcessors()).thenReturn(1);
    currentRuntimeField.set(null, runtime);
    Assert.assertEquals(1, Runtime.getRuntime().availableProcessors());

    SQLManager.SqlTableToH2OFrame frame = new SQLManager.SqlTableToH2OFrame("", "", false,
        "", "", "", 1, 10, null);

    int maxConnectionsPerNode = frame.getMaxConnectionsPerNode();
    //The user-defined limit for number of connections in the pool is 7, however there is only one processor.
    Assert.assertEquals(Runtime.getRuntime().availableProcessors(),
        maxConnectionsPerNode);
  }

  /**
   * Tests if there is at least one connection in the pool instantiated for each node, even if number of available
   * processors is a number lower than 1.
   */
  @Test
  public void testConnectionPoolSizeZeroProcessors() throws Exception {
    // Cloud size 1
    cloudSizeField.set(H2O.CLOUD, new H2ONode[1]);
    Runtime runtime = PowerMockito.spy(Runtime.getRuntime());
    // This ensures unified behavior of such test across various environments
    Mockito.when(runtime.availableProcessors()).thenReturn(-1);
    currentRuntimeField.set(null, runtime);
    Assert.assertEquals(-1, Runtime.getRuntime().availableProcessors());

    SQLManager.SqlTableToH2OFrame frame = new SQLManager.SqlTableToH2OFrame("", "", false,
        "", "", "", 1, 10, null);

    int maxConnectionsPerNode = frame.getMaxConnectionsPerNode();
    Assert.assertEquals(1,
        maxConnectionsPerNode);
  }

  @Test
  public void testConnectionPoolSizeTwoNodes() throws Exception {
    cloudSizeField.set(H2O.CLOUD, new H2ONode[2]);
    Runtime runtime = PowerMockito.spy(Runtime.getRuntime());
    Mockito.when(runtime.availableProcessors()).thenReturn(10);
    currentRuntimeField.set(null, runtime);
    Assert.assertEquals(10, Runtime.getRuntime().availableProcessors());

    SQLManager.SqlTableToH2OFrame frame = new SQLManager.SqlTableToH2OFrame("", "", false,
        "", "", "", 1, 10, null);

    int maxConnectionsPerNode = frame.getMaxConnectionsPerNode();
    int expectedConnectionsPerNode = Integer.valueOf(
        System.getProperty(H2O.OptArgs.SYSTEM_PROP_PREFIX + "sql.connections.max")
    ).intValue() / 2;
    Assert.assertEquals(expectedConnectionsPerNode, maxConnectionsPerNode);
  }

}