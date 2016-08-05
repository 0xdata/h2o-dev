package hex.deepwater;

import hex.Model;
import static hex.deepwater.DeepWaterParameters.Network.USER;
import water.*;
import water.exceptions.H2OIllegalArgumentException;
import water.fvec.Frame;
import water.gpu.ImageTrain;
import water.util.*;

import static hex.deepwater.DeepWaterParameters.Network.AUTO;
import static hex.deepwater.DeepWaterParameters.Network.inception_bn;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;


/**
 * This class contains the state of the Deep Learning model
 * This will be shared: one per node
 */
final public class DeepWaterModelInfo extends Iced {
  // pointer and snapshot of state of native library
  transient ImageTrain _imageTrain;
  int _height;
  int _width;
  int _channels;
  byte[] _network;
  byte[] _modelparams;

  public TwoDimTable summaryTable;

  // compute model size (number of model parameters required for making predictions)
  // momenta are not counted here, but they are needed for model building
  public long size() {
    long res = 0;
    if (_network!=null) res+=_network.length;
    if (_modelparams!=null) res+=_modelparams.length;
    return res;
  }

  Key<Model> _model_id;
  public DeepWaterParameters parameters;
  public final DeepWaterParameters get_params() { return parameters; }

  private long processed_global;
  public synchronized long get_processed_global() { return processed_global; }
  public synchronized void set_processed_global(long p) { processed_global = p; }
  public synchronized void add_processed_global(long p) { processed_global += p; }
  private long processed_local;
  public synchronized long get_processed_local() { return processed_local; }
  public synchronized void set_processed_local(long p) { processed_local = p; }
  public synchronized void add_processed_local(long p) { processed_local += p; }
  public synchronized long get_processed_total() { return processed_global + processed_local; }

  final boolean _classification; // Classification cache (nclasses>1)
  final Frame _train;         // Prepared training frame
  final Frame _valid;         // Prepared validation frame

  /**
   * Dummy constructor, only to be used for deserialization from autobuffer
   */
  private DeepWaterModelInfo() {
    super(); // key is null
    _classification = false;
    _train = _valid = null;
  }

  /**
   * Main constructor
   * @param params Model parameters
   * @param nClasses number of classes (1 for regression, 0 for autoencoder)
   * @param train User-given training data frame, prepared by AdaptTestTrain
   * @param valid User-specified validation data frame, prepared by AdaptTestTrain
   */
  public DeepWaterModelInfo(final DeepWaterParameters params, Key model_id, int nClasses, Frame train, Frame valid) {
    _classification = nClasses > 1;
    _train = train;
    _valid = valid;
    parameters = (DeepWaterParameters) params.clone(); //make a copy, don't change model's parameters
    _model_id = model_id;
    DeepWaterParameters.Sanity.modifyParms(parameters, parameters, nClasses); //sanitize the model_info's parameters

    if (parameters._checkpoint!=null) {
      try {
        DeepWaterModel other = (DeepWaterModel) parameters._checkpoint.get();
        restoreFromInternalState(nClasses, parameters._mini_batch_size, other.model_info()._network, other.model_info()._modelparams);
      } catch (Throwable t) {
        throw new H2OIllegalArgumentException("_checkpoint", "Invalid checkpoint provided.");
      }
    }
    else {
      _width=parameters._width;
      _height=parameters._height;
      _channels=parameters._channels;
      if (_width==0 || _height==0) {
        switch(parameters._network) {
          case lenet:
            _width = 28;
            _height = 28;
            break;
          case AUTO:
          case alexnet:
          case inception_bn:
          case googlenet:
          case resnet:
            _width = 224;
            _height = 224;
            break;
          case vgg:
          case vgg16:
            _width = 320;
            _height = 320;
            break;
          case USER:
            throw new H2OIllegalArgumentException("_network", "Please specify width and height for user-given model definition.");
          default:
            throw H2O.unimpl("Unknown network type: " + parameters._network);
        }
      }
      try {
        _imageTrain = new ImageTrain(_width, _height, _channels);
        if (parameters._network != USER) {
          String network = parameters._network == AUTO ? inception_bn.toString() : parameters._network.toString();
          Log.info("Creating a fresh model of the following network type: " + network);
          _imageTrain.buildNet(nClasses, parameters._mini_batch_size, network); //set optimizer, batch size, nclasses, etc.
        }
        // load a network if specified
        final String networkDef = parameters._network_definition_file;
        if (networkDef != null && !networkDef.isEmpty()) {
          Log.info("Loading the network from: " + networkDef);
          _imageTrain.loadModel(networkDef);
          Log.info("Setting the optimizer.");
          _imageTrain.setOptimizer(nClasses, parameters._mini_batch_size);
        }
        final String networkParms = parameters._network_parameters_file;
        if (networkParms != null && !networkParms.isEmpty()) {
          Log.info("Loading the parameters (weights/biases) from: " + networkParms);
          _imageTrain.loadParam(networkParms);
        } else {
          Log.warn("No network parameters file specified. Starting from scratch.");
        }
//        storeInternalState();
      } catch(Throwable t) {
        Log.err("Unable to initialize the native Deep Learning backend: " + t.getMessage());
        throw t;
      }
    }
  }

  public void storeInternalState() {
    Path path = null;
    // only overwrite the network definition if it's null
    if (_network==null) {
      try {
        path = Paths.get(System.getProperty("java.io.tmpdir"), Key.make().toString());
        _imageTrain.saveModel(path.toString());
        _network = Files.readAllBytes(path);
      } catch (IOException e) {
        e.printStackTrace();
      } finally { if (path!=null) try { Files.deleteIfExists(path); } catch (IOException e) { } }
    }
    // always overwrite the parameters (weights/biases)
    try {
      path = Paths.get(System.getProperty("java.io.tmpdir"), Key.make().toString());
      _imageTrain.saveParam(path.toString());
      _modelparams = Files.readAllBytes(path);
    } catch (IOException e) {
      e.printStackTrace();
    } finally { if (path!=null) try { Files.deleteIfExists(path); } catch (IOException e) { } }
  }

  public void restoreFromInternalState(int nClasses, int miniBatchSize, byte[] network, byte[] parameters) {
    if (network==null || parameters==null) return;

    Path path = null;
    // only overwrite the network definition if it's null
    try {
      path = Paths.get(System.getProperty("java.io.tmpdir"), Key.make().toString());
      Files.write(path, network);
      _imageTrain.loadModel(path.toString());
      _imageTrain.setOptimizer(nClasses, miniBatchSize);
    } catch (IOException e) {
      e.printStackTrace();
    } finally { if (path!=null) try { Files.deleteIfExists(path); } catch (IOException e) { } }
    // always overwrite the parameters (weights/biases)
    try {
      path = Paths.get(System.getProperty("java.io.tmpdir"), Key.make().toString());
      Files.write(path, parameters);
      Log.info("Loading the parameters.");
      _imageTrain.loadParam(path.toString());
    } catch (IOException e) {
      e.printStackTrace();
    } finally { if (path!=null) try { Files.deleteIfExists(path); } catch (IOException e) { } }
  }

  DeepWaterModelInfo deep_clone() {
    AutoBuffer ab = new AutoBuffer();
    this.write(ab);
    ab.flipForReading();
    return (DeepWaterModelInfo) new DeepWaterModelInfo().read(ab);
  }

  /**
   * Create a summary table
   * @return TwoDimTable with the summary of the model
   */
  TwoDimTable createSummaryTable() {
    return null;
  }

  /**
   * Print a summary table
   * @return String containing ASCII version of summary table
   */
  @Override public String toString() {
    StringBuilder sb = new StringBuilder();
    if (!get_params()._quiet_mode) {
      createSummaryTable();
      if (summaryTable!=null) sb.append(summaryTable.toString(1));
    }
    return sb.toString();
  }

  /**
   * Debugging printout
   * @return String with useful info
   */
  public String toStringAll() {
    StringBuilder sb = new StringBuilder();
    sb.append(toString());
    sb.append("\nprocessed global: ").append(get_processed_global());
    sb.append("\nprocessed local:  ").append(get_processed_local());
    sb.append("\nprocessed total:  ").append(get_processed_total());
    sb.append("\n");
    return sb.toString();
  }
  public void add(DeepWaterModelInfo other) {
    throw H2O.unimpl();
  }
  public void mult(double N) {
    throw H2O.unimpl();
  }
  public void div(double N) {
    throw H2O.unimpl();
  }
}
