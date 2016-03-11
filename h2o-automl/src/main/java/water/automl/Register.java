package water.automl;

import water.H2O;
import water.api.AbstractRegister;

public class Register extends AbstractRegister{
  @Override public void register(String relativeResourcePath) throws ClassNotFoundException {
    H2O.registerPOST("/99/AutoMLBuilder", AutoMLBuilderHandler.class, "automl", "automatically build models");
    H2O.registerGET("/99/AutoML/(?<automl_id>.*)/", AutoMLHandler.class,"refersh", "refresh the model key");
  }
}
