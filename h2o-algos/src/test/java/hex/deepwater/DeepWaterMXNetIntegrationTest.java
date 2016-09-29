package hex.deepwater;

import hex.deepwater.backends.BackendFactory;
import hex.deepwater.backends.BackendParams;
import hex.deepwater.backends.BackendTrain;
import hex.deepwater.backends.RuntimeOptions;
import hex.deepwater.datasets.ImageDataSet;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import water.parser.BufferedString;
import water.util.ArrayUtils;
import water.util.StringUtils;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class DeepWaterMXNetIntegrationTest extends DeepWaterAbstractIntegrationTest {

    @Before
    public void setUp() throws Exception {
        backend = DeepWaterParameters.Backend.mxnet;
    }

    // This test has nothing to do with H2O - Pure integration test of deepwater/backends/mxnet
    // FIXME: push this to the actual deepwater.backends.mxnet.test module
    @Ignore
    @Test
    public void inceptionPredictionMX() throws IOException {
      File imgFile = find_test_file("smalldata/deepwater/imagenet/test2.jpg");
      BufferedImage img = ImageIO.read(imgFile);

      int w = 224, h = 224;

      BufferedImage scaledImg = new BufferedImage(w, h, img.getType());

      Graphics2D g2d = scaledImg.createGraphics();
      g2d.drawImage(img, 0, 0, w, h, null);
      g2d.dispose();

      float[] pixels = new float[w * h * 3];

      int r_idx = 0;
      int g_idx = r_idx + w * h;
      int b_idx = g_idx + w * h;

      for (int i = 0; i < h; i++) {
        for (int j = 0; j < w; j++) {
          Color mycolor = new Color(scaledImg.getRGB(j, i));
          int red = mycolor.getRed();
          int green = mycolor.getGreen();
          int blue = mycolor.getBlue();
          pixels[r_idx] = red-117; r_idx++; //FIXME: Hardcoded mean image RGB values
          pixels[g_idx] = green-117; g_idx++;
          pixels[b_idx] = blue-117; b_idx++;
        }
      }

      // the path to Inception model
      //ImageTrain m = new ImageTrain(224,224,3);
      //m.buildNet(1000,1,"inception_bn");
      ImageDataSet id = new ImageDataSet(224,224,3);
      BackendTrain m = BackendFactory.create(backend); //NOTE: could have used the ImagePred class too - but using ImageTrain to check more relevant logic

      RuntimeOptions opts = new RuntimeOptions();
      opts.setSeed(1234);
      opts.setUseGPU(false); //FIXME: Fails when set to true (i.e., running on the GPU) due to BatchNormalization issues?

      BackendParams bparm = new BackendParams();
      bparm.set("mini_batch_size", 1);

      //FIXME: make the path a resource of the package
      m.buildNet(id, opts, bparm, 1000, StringUtils.expandPath("~/deepwater/backends/mxnet/Inception/model-symbol.json"));
      m.loadParam(StringUtils.expandPath("~/deepwater/backends/mxnet/Inception/model.params"));

      float[] preds = m.predict(pixels);
      int which = ArrayUtils.maxIndex(preds);

      water.fvec.Frame labels = parse_test_file("~/deepwater/backends/mxnet/Inception/synset.txt");

      BufferedString str = new BufferedString();
      String answer = labels.anyVec().atStr(str, which).toString();
      System.out.println("\n\n" + answer +"\n\n");
      labels.remove();
      Assert.assertEquals("n02113023 Pembroke", answer);
    }
}
