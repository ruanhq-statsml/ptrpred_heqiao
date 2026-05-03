#PCA local average:

from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

#Input is the loading data
#
def local_average(X, col, start_ind, window_size, step_size):
    n = X.shape[0]
    if step_size > window_size:
        raise ValueError("The step size should be smaller than the window size")
    loading_mat_MA = np.random.random(len(np.arange(start_ind, n - window_size, step_size)))
    loading_subs = X.iloc[start_ind:(start_ind + window_size), :]
    loading_mat = loading_subs.mean(axis = 1)
    for i in range(start_ind, n_window_size, step_size):
        loading_sub = X.iloc[start_ind:(start_ind + window_size), :]
        loading_dim_avg = loading_subs.mean(axis = 1)
        loading_mat_MA[i, :] = loading_dim_avgs
    return loading_mat_MA



    