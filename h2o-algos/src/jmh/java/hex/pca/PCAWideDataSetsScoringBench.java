package hex.pca;

import hex.svd.SVDImplementation;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

import java.util.concurrent.TimeUnit;

import static water.TestUtil.stall_till_cloudsize;

/**
 * PCA benchmark
 */
@Fork(1)
@Threads(1)
@State(Scope.Thread)
@Warmup(iterations = JMHConfiguration.WARM_UP_ITERATIONS)
@Measurement(iterations = JMHConfiguration.MEASUREMENT_ITERATIONS)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
public class PCAWideDataSetsScoringBench {
	
	private PCAWideDataSetsBenchModel pcaWideDataSetsBench;
	@Param({"1", "2", "3", "4", "5", "6"})
	private int dataSetCase;
	@Param({"JAMA", "MTJ", "EVD_MTJ_DENSEMATRIX", "EVD_MTJ_SYMM"})
	private SVDImplementation svdImplementation;

	public static void main(String[] args) throws RunnerException {
		Options opt = new OptionsBuilder()
			.include(PCAWideDataSetsScoringBench.class.getSimpleName())
			.build();
		
		new Runner(opt).run();
	}
	
	@Setup(Level.Invocation)
	public void setup() {
		water.util.Log.setLogLevel("ERRR");
		stall_till_cloudsize(1);
		
		pcaWideDataSetsBench = new PCAWideDataSetsBenchModel(dataSetCase);
		pcaWideDataSetsBench.setSvdImplementation(svdImplementation);
		// train model to prepare for score()
		pcaWideDataSetsBench.train();
	}
	
	@Benchmark
	public boolean measureWideDataSetsBenchScoringCase() throws Exception {
		if (!pcaWideDataSetsBench.score()) {
			throw new Exception("Model for PCAWideDataSetsBench failed to be scored!");
		}
		return true;
	}
	
	@TearDown(Level.Invocation)
	public void tearDown() {
		pcaWideDataSetsBench.tearDown();
	}
	
}
