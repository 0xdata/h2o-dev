package hex.pca;

import hex.DataInfo;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;
import water.DKV;
import water.Key;
import water.TestUtil;
import water.fvec.Frame;
import water.util.FrameUtils;

import java.util.concurrent.TimeUnit;

import static hex.pca.JMHConfiguration.logLevel;
import static hex.pca.PCAModel.PCAParameters;
import static hex.pca.PCAModel.PCAParameters.Method.GramSVD;
import static water.TestUtil.parseTestFile;
import static water.TestUtil.stall_till_cloudsize;

/**
 * PCA benchmark micro-benchmark based on hex.pca.PCATest.testImputeMissing()
 */
@Fork(1)
@Threads(1)
@State(Scope.Thread)
@Warmup(iterations = JMHConfiguration.WARM_UP_ITERATIONS)
@Measurement(iterations = JMHConfiguration.MEASUREMENT_ITERATIONS)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Timeout(time = JMHConfiguration.TIMEOUT_MINUTES, timeUnit = TimeUnit.MINUTES)
public class PCAImputeMissingScoringBench {

  @Param({"JAMA", "MTJ_SVD_DENSEMATRIX", "MTJ_EVD_DENSEMATRIX", "MTJ_EVD_SYMMMATRIX"})
  private PCAImplementation PCAImplementation;

  private PCAParameters paramsImputeMissing;
  private PCAModel pcaModel;
  private Frame trainingFrame;

  public static void main(String[] args) throws RunnerException {
    Options opt = new OptionsBuilder()
        .include(PCAImputeMissingScoringBench.class.getSimpleName())
        .build();

    new Runner(opt).run();
  }

  @Setup(Level.Iteration)
  public void setup() {
    water.util.Log.setLogLevel(logLevel);
    stall_till_cloudsize(1);

    trainingFrame = null;
    double missing_fraction = 0.75;
    long seed = 12345;

    try {
      trainingFrame = parseTestFile(Key.make("arrests.hex"), "smalldata/pca_test/USArrests.csv");
      // Add missing values to the training data
      Frame frame = new Frame(Key.<Frame>make(), trainingFrame.names(), trainingFrame.vecs());
      DKV.put(frame._key, frame); // Need to put the frame (to be modified) into DKV for MissingInserter to pick up
      FrameUtils.MissingInserter j = new FrameUtils.MissingInserter(frame._key, seed, missing_fraction);
      j.execImpl().get(); // MissingInserter is non-blocking, must block here explicitly
      DKV.remove(frame._key); // Delete the frame header (not the data)

      paramsImputeMissing = new PCAParameters();
      paramsImputeMissing._train = trainingFrame._key;
      paramsImputeMissing._k = 4;
      paramsImputeMissing._transform = DataInfo.TransformType.NONE;
      paramsImputeMissing._pca_method = GramSVD;
      paramsImputeMissing._pca_implementation = PCAImplementation;
      paramsImputeMissing._impute_missing = true;   // Don't skip rows with NA entries, but impute using mean of column
      paramsImputeMissing._seed = seed;

    } catch (RuntimeException e) {
      if (trainingFrame != null) {
        trainingFrame.delete();
      }
      throw e;
    }
  }

  @Setup(Level.Invocation)
  public void setupInvocation() {
    try {
      if (!train()) { // prepare the model for scoring
        throw new RuntimeException("PCA model failed to be trained.");
      }
    } catch(RuntimeException e) {
      if (trainingFrame != null) {
        trainingFrame.delete();
      }
      throw e;
    }
  }
  
  @Benchmark
  public boolean measureImputeMissingScoring() throws Exception {
    if (!score()) {
      throw new Exception("Model for PCAImputeMissing failed to be scored!");
    }
    return true;
  }

  @TearDown(Level.Iteration)
  public void tearDown() {
    if (trainingFrame != null) {
      trainingFrame.delete();
    }
  }
  
  @TearDown(Level.Invocation)
  public void tearDownInvocation() {
    if (pcaModel != null) {
      pcaModel.remove();
    }
  }

  private boolean train() {
    try {
      pcaModel = new PCA(paramsImputeMissing).trainModel().get();
    } catch (Exception exception) {
      return false;
    }
    return true;
  }

  private boolean score() {
    try {
      pcaModel.score(trainingFrame);
    } catch (Exception e) {
      return false;
    }
    return true;
  }

}
