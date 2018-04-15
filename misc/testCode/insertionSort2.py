'''
Created on Sep 2, 2014

@author: George
'''

A = [31,41,59,26,41,58]

def insertionSort(list):
    for i in range(1, len(list)):
        key = list[i]
        firstNum = i -1
        print list[0:firstNum+1], "|", list[firstNum+1:]

        while firstNum >= 0 and list[firstNum] > key:
            list[firstNum + 1] = list[firstNum]
            print list[firstNum+1], "-->"
            print key, "<--"
            firstNum -= 1

        list[firstNum+1] = key



print A
insertionSort(A)
print A