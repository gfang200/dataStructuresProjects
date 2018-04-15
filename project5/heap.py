from swap import swap

def less(x, y):
    return x < y

def less_key(x, y):
    return x.key < y.key

def left(i):
    return 2 * i + 1

def right(i):
    return 2 * (i + 1)

def parent(i):
    return (i-1) / 2

# Student code -- fill in all the methods that have pass as the only statement
class Heap:
    def __init__(self, data, less = less):
        self.data = data
        self.less = less
        self.heap_length = len(data)
        self.build_min_heap()
        
    def __repr__(self):
        ls = []
        for i in range(self.heap_length):
            ls.append(self.data[i])
        return repr(ls)
    
    def minimum(self):
        return self.data[0]

    def insert(self, obj):
        #if the heap length is the array length, for the love of all that is holy, stop
        #else, bump the heap length, add the new element to the end of the array and
        #run heapify on the parent
        self.heap_length += 1
        if self.heap_length >= len(self.data):
            self.data.append(obj)
        else:
            self.data[self.heap_length-1]=obj

        p = parent(self.heap_length - 1)
        while p >=0:
            self.min_heapify(p)
            p = parent(p)


    def extract_min(self):
        #if the heap is empty, do nothing
        if self.heap_length == 0:
            print "Empty Heap"
            pass
        
        #replace the root with the last element in the heap and heapify up the tree
        temp = self.data[0]
        self.data[0] = self.data[self.heap_length-1]
        self.heap_length -= 1
        self.min_heapify(0)

        return temp
        
    def min_heapify(self, i):
        L = left(i)
        R = right(i)
        smallest = i

        #find the smallest of the children or root
        if L < self.heap_length and self.less(self.data[L], self.data[smallest]):
            smallest = L
        if R < self.heap_length and self.less(self.data[R], self.data[smallest]):
            smallest = R


        def swap(A, i, j):
            temp = A[i]
            A[i] = A[j]
            A[j] = temp

        #swap the smallest with the root and recur    
        if smallest != i:
            swap(self.data, i, smallest)
            self.min_heapify(smallest)
        
        
    
    def build_min_heap(self):
        #all the leaves are already heaps. now heapify from the middle on up
        length = len(self.data)
        for i in range(length/2, -1, -1):
            self.min_heapify(i)
    
class PriorityQueue:
    def __init__(self, less=less_key):
        self.heap = Heap([], less)

    def __repr__(self):
        return repr(self.heap)

    def push(self, obj):
        self.heap.insert(obj)

    def pop(self):
        return self.heap.extract_min()

if __name__ == "__main__":
    def check_heap(heapArray, index = 0, parent = None):
        if index not in range(len(heapArray)):
            return True
        if less(heapArray[index], parent):
            return (check_heap(heapArray, left(index), heapArray[index])) and check_heap(heapArray, right(index), heapArray[index])
        else:
            print heapArray
            return False
        
    P=PriorityQueue(less)
    for i in range(10,0,-1):
        P.push(i)
    print P
    #assert check_heap(P.heap.data)
    
    
    
    
