from util_library import *
addToChart('Time vs Voltage', 'test.png',2)
addToChart('Subplots', 'test1.png',1)  
result_array = sorted(result_array, key=lambda x: x['order'], reverse=False)
print(';##;')
print(result_array)