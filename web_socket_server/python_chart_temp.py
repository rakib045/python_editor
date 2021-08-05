from util_library import *
def bubbleSort(in_array):
    array_size = len(in_array)

    for i in range(array_size):
        not_swap = True
        for j in range(0, array_size-i-1):
            #print("i: " + str(i) + ", j: " + str(j))
            if in_array[j] > in_array[j+1]:
                not_swap = False
                in_array[j], in_array[j+1] = in_array[j+1], in_array[j]

        if not_swap:
            break

if __name__ == '__main__':
    print("Code is starting ...")
    input_array = [4, 3, 2, 8, 9, 5]
    #print("Input Array: " + str(input_array))

    #Call Bubble Sort Array
    bubbleSort(input_array)

    print("Output Array: " + str(input_array))
    #print("Code finished !")
result_array = sorted(result_array, key=lambda x: x['order'], reverse=False)
print(';##;')
print(result_array)