package hex.tree.gbm;

import hex.genmodel.utils.DistributionFamily;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.Test;
import water.DKV;
import water.Scope;
import water.TestUtil;
import water.exceptions.H2OModelBuilderIllegalArgumentException;
import water.fvec.Frame;
import water.udf.CFuncRef;
import water.udf.TestBernoulliCustomDistribution;
import water.util.FrameUtils;

import java.io.IOException;

import static water.udf.JFuncUtils.loadTestFunc;

public class GBMCustomDistributionTest extends TestUtil {

    @BeforeClass
    static public void setup() { stall_till_cloudsize(1); }

    @Test
    public void testCustomDistribution() throws Exception {
        final CFuncRef func = bernoulliCustomDistribution();
        Frame fr = null; GBMModel gbm_default = null; GBMModel gbm_custom = null;
        try {
            Scope.enter();
            fr = parse_test_file("./smalldata/gbm_test/alphabet_cattest.csv");
            int idx = fr.find("y");
            if (!fr.vecs()[idx].isCategorical()) {
                Scope.track(fr.replace(idx, fr.vecs()[idx].toCategoricalVec()));
            }

            System.out.println("Creating default model GBM...");
            GBMModel.GBMParameters parms = new GBMModel.GBMParameters();
            parms._train = fr._key;
            parms._response_column = "y"; // Train on the outcome
            parms._distribution = DistributionFamily.bernoulli;
            gbm_default = (GBMModel) Scope.track_generic(new GBM(parms).trainModel().get());

            System.out.println("Creating custom distribution model GBM...");
            parms = new GBMModel.GBMParameters();
            parms._train = fr._key;
            parms._response_column = "y"; // Train on the outcome
            parms._distribution = DistributionFamily.custom;
            parms._custom_distribution_func = func.toRef();
            gbm_custom = (GBMModel) Scope.track_generic(new GBM(parms).trainModel().get());

            Assert.assertEquals(gbm_default._output._training_metrics.mse(), gbm_custom._output._training_metrics.mse(), 1e-4);
            Assert.assertEquals(gbm_default._output._training_metrics.auc_obj()._auc, gbm_custom._output._training_metrics.auc_obj()._auc, 1e-4);

            try {
                System.out.println("Creating custom distribution model GBM wrong setting...");
                parms = new GBMModel.GBMParameters();
                parms._train = fr._key;
                parms._response_column = "y"; // Train on the outcome
                parms._distribution = DistributionFamily.custom;
                parms._custom_distribution_func = null;
                gbm_custom = (GBMModel) Scope.track_generic(new GBM(parms).trainModel().get());
            } catch (H2OModelBuilderIllegalArgumentException ex){
                System.out.println("Catch illegal argument exception.");
            }
            
            
        }  finally {
            FrameUtils.delete(fr, gbm_default, gbm_custom);
            DKV.remove(func.getKey());
            Scope.exit();
        }
    }
    
    private CFuncRef bernoulliCustomDistribution() throws IOException {
        return loadTestFunc("customDistribution.key", TestBernoulliCustomDistribution.class);
    }
}
