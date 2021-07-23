from util_library import *
import numpy as np
def square(x):
    return x * x

x = np.random.randint(1, 10)
y = square(x)
print('%d squared is %d' % (x, y))







result_array = sorted(result_array, key=lambda x: x['order'], reverse=False)
print(';##;')
print(result_array)