import numpy as np

a = np.array([
    [0, 1, -3, 1],
    [3, 1, 3, -4],
    [-3, 1, 3, 4]
])

a[a < 0] = 0

print(a)