package hex;

import water.H2O;
import water.Job;
import water.util.Log;

/**
 * Runs given model builders in bulk.
 */
public class BulkModelBuilder {

    private final String modelType;
    private final Job job;
    private final ModelBuilder<?, ?, ?>[] modelBuilders;
    private final int parallelization;
    private final int updateInc;

    /**
     * @param modelType       text description of group of models being built (for logging purposes)
     * @param job             parent job (processing will be stopped if stop of a parent job was requested)
     * @param modelBuilders   list of model builders to run in bulk
     * @param parallelization level of parallelization (how many models can be built at the same time)
     * @param updateInc       update increment (0 = disable updates)
     */
    public BulkModelBuilder(
        String modelType, Job job, ModelBuilder<?, ?, ?>[] modelBuilders,
        int parallelization, int updateInc
    ) {
        this.modelType = modelType;
        this.job = job;
        this.modelBuilders = modelBuilders;
        this.parallelization = parallelization;
        this.updateInc = updateInc;
    }
    
    protected void prepare(ModelBuilder m) {}
    
    protected void finished(ModelBuilder m) {}

    public void bulkBuildModels() {
        final int N = modelBuilders.length;
        H2O.H2OCountedCompleter[] submodel_tasks = new H2O.H2OCountedCompleter[N];
        int nRunning = 0;
        RuntimeException rt = null;
        for (int i = 0; i < N; ++i) {
            if (job.stop_requested()) {
                Log.info("Skipping build of last " + (N - i) + " out of " + N + " " + modelType + " CV models");
                stopAll(submodel_tasks);
                throw new Job.JobCancelledException();
            }
            Log.info("Building " + modelType + " model " + (i + 1) + " / " + N + ".");
            prepare(modelBuilders[i]);
            submodel_tasks[i] = H2O.submitTask(modelBuilders[i].trainModelImpl());
            if (++nRunning == parallelization) { //piece-wise advance in training the models
                while (nRunning > 0) try {
                    int waitForTaskIndex = i + 1 - nRunning;
                    submodel_tasks[waitForTaskIndex].join();
                    finished(modelBuilders[waitForTaskIndex]);
                    nRunning--;
                    if (updateInc > 0) job.update(updateInc); // One job finished
                } catch (RuntimeException t) {
                    if (rt == null) rt = t;
                }
                if (rt != null) throw rt;
            }
        }
        for (int i = 0; i < N; ++i) //all sub-models must be completed before the main model can be built
            try {
                final H2O.H2OCountedCompleter task = submodel_tasks[i];
                assert task != null;
                task.join();
            } catch (RuntimeException t) {
                if (rt == null) rt = t;
            }
        if (rt != null) throw rt;
    }

    private void stopAll(H2O.H2OCountedCompleter[] tasks) {
        for (H2O.H2OCountedCompleter task : tasks) {
            if (task != null) {
                task.cancel(true);
            }
        }
    }

}
