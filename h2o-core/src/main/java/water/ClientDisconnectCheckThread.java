package water;

import water.util.Log;

class ClientDisconnectCheckThread extends Thread {

  public ClientDisconnectCheckThread() {
    super("ClientDisconnectCheckThread");
    setDaemon(true);
  }

  private boolean isTimeoutExceeded(H2ONode client, long timeout) {
    long lastHeardFrom = client._last_heard_from;
    boolean timedOut = (System.currentTimeMillis() - lastHeardFrom) >= timeout;
    if (timedOut) {
      System.out.println("TIMEOUT: " + lastHeardFrom + ", currenct time millis: " + System.currentTimeMillis() + " | " + client.debugInfo());
    }
    return timedOut;
  }

  /**
   * This method checks whether the client is disconnected from this node due to some problem such as client or network
   * is unreachable.
   */
  private void handleClientDisconnect(H2ONode client) {
    if(client != H2O.SELF) {
      if (H2O.isFlatfileEnabled()) {
        H2O.removeNodeFromFlatfile(client);
      }
      H2O.removeClient(client);
    }
  }

  @Override
  public void run() {
    while (true) {
      for(H2ONode client: H2O.getClients()){
        if(isTimeoutExceeded(client, H2O.ARGS.clientDisconnectTimeout)){
          handleClientDisconnect(client);
        }
      }
      try {
        Thread.sleep(H2O.ARGS.clientDisconnectTimeout);
      } catch (InterruptedException ignore) {}
    }
  }
}
