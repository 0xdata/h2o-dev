package water.automl;

import ai.h2o.automl.AutoML;
import ai.h2o.automl.H2OJob;
import water.DKV;
import water.Key;
import water.api.Handler;
import water.api.JobV3;
import water.fvec.Frame;


public class AutoMLBuilderHandler extends Handler {
  public AutoMLBuilderV3 automl(int version, AutoMLBuilderV3 args) {
    Frame frame = DKV.getGet(args.dataset);
    if( null==frame )
      throw new IllegalArgumentException("No such frame: " + args.dataset);
    AutoML aml = new AutoML(
            Key.<AutoML>make(),
            args.dataset,
            frame,
            args.target_name,
            args.loss,
            args.max_time,
            -1,     // min accuracy or stopping crit ... "loss threshold"
            args.ensemble,
            args.exclude,
            args.try_mutations);
    DKV.put(aml);
    args.job = new JobV3().fillFromImpl(new H2OJob(aml,aml._key).start());
    return args;
  }
}
