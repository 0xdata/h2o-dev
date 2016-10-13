package hex.deepwater.backends;

import hex.deepwater.datasets.DataSet;

public interface BackendTrain {

    void delete();

    void setOptimizer(int var1, int var2);

    void loadModel(String model_path);

    void buildNet(DataSet dataset, RuntimeOptions opts, BackendParams backend_params, int num_classes, String name);

    void saveModel(String model_path);

    void loadParam(String param_path);

    void saveParam(String param_path);

    String toJson();

    // learning_rate
    // weight_decay
    // momentum
    // clip_gradient: bool
    void setParameter(String name, float value);

//    public void setLR(float var1) {
//        deepwaterJNI.ImageTrain_setLR(this.swigCPtr, this, var1);
//    }
//
//    public void setWD(float var1) {
//        deepwaterJNI.ImageTrain_setWD(this.swigCPtr, this, var1);
//    }
//
//    public void setMomentum(float var1) {
//        deepwaterJNI.ImageTrain_setMomentum(this.swigCPtr, this, var1);
//    }
//
//    public void setClipGradient(float var1) {
//        deepwaterJNI.ImageTrain_setClipGradient(this.swigCPtr, this, var1);
//    }

    float[] train(float[] data, float[] label);

    float[] predict(float[] data, float[] label);

    float[] predict(float[] data);

    void setupSession(RuntimeOptions opts, int classes, int mini_batch_size, String network);
}