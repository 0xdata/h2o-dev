package ai.h2o.automl;

import org.junit.BeforeClass;
import org.junit.Test;
import water.Key;
import water.api.schemas3.ImportFilesV3;
import water.fvec.Frame;

public class AutoMLTest extends TestUtil {

  @BeforeClass public static void setup() { stall_till_cloudsize(1); }

  @Test public void AirlinesTest() {
    AutoML aml=null;
    Frame fr=null;
    try {
      AutoMLBuildSpec autoMLBuildSpec = new AutoMLBuildSpec();
      fr = parse_test_file("./smalldata/airlines/allyears2k_headers.zip");
      autoMLBuildSpec.input_spec.training_frame = fr._key;
      autoMLBuildSpec.input_spec.response_column = "IsDepDelayed";
      autoMLBuildSpec.build_control.loss = "AUTO";
      autoMLBuildSpec.build_control.stopping_criteria.set_max_runtime_secs(5);

      aml = AutoML.makeAutoML(Key.<AutoML>make(), autoMLBuildSpec);
      AutoML.startAutoML(aml);
      aml.get();

    } finally {
      // cleanup
      if(aml!=null) aml.deleteWithChildren();
    }
  }
}
