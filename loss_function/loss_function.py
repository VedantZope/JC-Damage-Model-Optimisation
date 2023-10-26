import numpy as np

def rmse(y_true, y_pred):
    return np.sqrt(np.mean(np.square(y_pred - y_true), axis=-1))


def abs_error(y_true, y_pred):
    return abs(y_pred - y_true)