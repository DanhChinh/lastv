from env import make_data
import numpy as np

data,  label = make_data()

def split_array(arr, frac=0.7, random=False, seed=None):
    arr = np.array(arr)
    n = len(arr)

    if random:
        rng = np.random.default_rng(seed)
        indices = np.arange(n)
        rng.shuffle(indices)
        split_point = int(n * frac)
        idx1, idx2 = indices[:split_point], indices[split_point:]
        return arr[idx1], arr[idx2]
    else:
        split_point = int(n * frac)
        return arr[:split_point], arr[split_point:]

xtrain, xtest = split_array(data)
ytrain, ytest = split_array(label)
