from env import make_data, handle_progress
import numpy as np

data, label = make_data()
print(data)
print(label)
print("_"*100)
data_chunks = np.array_split(data, 100)
label_chunks = np.array_split(label, 100)
print(data_chunks[-1])
print(label_chunks[-1])