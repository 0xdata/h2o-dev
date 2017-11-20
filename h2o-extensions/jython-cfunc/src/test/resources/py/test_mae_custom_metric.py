import water.udf.CMetricFunc as MetricFunc

class MAE(MetricFunc):
    def perRow(self, pred, act, w, o, model):
        return [abs(pred[0] - act[0]), 1]

    def combine(self, l, r):
        return [l[0] + r[0], l[1] + r[1]]

    def metric(self, l):
        return l[0]/l[1]