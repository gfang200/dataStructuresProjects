'''
Created on Sep 1, 2014

@author: George
'''
unSorted = [5,2,4,6,1,3]
stack = []

def insertionSort(list):
    for i in range(1, len(list)):
        element = list[i]
        j = i-1
        while j>=0 and list[j]>element:
            list[j+1]=list[j]
            j= j - 1
        list[j+1] = element
        print list

#print unSorted
#insertionSort(unSorted)
#print unSorted

class stack(object):

    def __init__(self):
        self.stack = [None for x in range(0,6)]
        self.top = 0

    def stackEmpty(self):
        if self.top==0:
            return True
        else:
            return False

    def stackPush(self,x):
        self.stack[self.top]=x
        self.top=self.top+1

    def stackPop(self):
        if self.stackEmpty():
            print "underflow"
        else:
            self.top = self.top - 1
            return self.stack[self.top + 1]

    def stackContent(self):
        print "array = ",self.stack
        print "top = ",self.top
        print "stack = ",self.stack[0:self.top]

"""
dequeTest = stack()
print "PUSH(S,4)"
dequeTest.stackPush(4)
dequeTest.stackContent()
print "\nPUSH(S,1)"
dequeTest.stackPush(1)
dequeTest.stackContent()
print "\nPUSH(S,3)"
dequeTest.stackPush(3)
dequeTest.stackContent()
print "\nPOP(S)"
dequeTest.stackPop()
dequeTest.stackContent()
print "\nPUSH(S,8)"
dequeTest.stackPush(8)
dequeTest.stackContent()
print "\nPOP(S)"
dequeTest.stackPop()
dequeTest.stackContent()
"""
class deque(object):

    def __init__(self):
        self.stack = [None for x in range(0,6)]
        self.top = 0
        self.bot = 0

    def stackEmpty(self):
        if self.top==0:
            return True
        else:
            return False

    def topPush(self,x):
        self.stack[self.top]=x
        self.top=self.top+1

    def topPop(self):
        if self.stackEmpty():
            print "underflow"
        else:
            self.top = self.top - 1
            return self.stack[self.top + 1]

    def enQueue(self,x):
        if self.top==self.bot:
            print "overflow"
        else:
            self.top = self.top - 1 + len(self.stack)
            self.stack[self.top] = x


    def deQueue(self):
        for i in range(len(self.stack)-1):
            self.stack[i]=self.stack[i+1]
            self.top=self.top-1

    def stackContent(self):
        print "array = ",self.stack
        print "top = ",self.top
        print "stack = ",self.stack[:self.top]


dequeTest = deque()
dequeTest.topPush(4)
dequeTest.stackContent()
dequeTest.topPush(1)
dequeTest.stackContent()
dequeTest.topPush(3)
dequeTest.stackContent()
dequeTest.topPop()
dequeTest.stackContent()
dequeTest.topPop()
dequeTest.stackContent()
dequeTest.enQueue(5)
dequeTest.stackContent()

10.2-1


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class ListIterator:
    def __init__(self, node):
        self.node = node

    def __next__(self):
        if self.node:
            d = self.node.data
            self.node = self.node.next
            return d
        else:
            raise StopIteration

class List:
    def __init__(self):
        self.head = None
        self.tail = None

    # Sequence interface

    def __iter__(self):
        return ListIterator(self.head)

    def begin(self):
        return ListIterator(self.head)

    def insert_after(self, iter, x):
        n = Node(x)
        n.next = iter.node.next
        iter.node.next = n
        if iter.node == self.tail or self.tail == None:
            self.tail = n

    def erase_after(self, iter):
        if self.tail == iter.node.next:
            self.tail = iter.node
        iter.node.next = iter.node.next.next

    def insert_front(self, x):
        n = Node(x)
        n.next = self.head
        self.head = n
        if self.tail == None:
            self.tail = n

    def erase_front(self):
        if self.head == self.tail:
            self.tail = None
        self.head = self.head.next

    def append(self, x):
        n = Node(x)
        if self.is_empty():
            self.insert_front(x)
        else:
            self.insert_after(ListIterator(self.tail), x)

    def __repr__(self):
        return "[" + ",".join([x.__repr__() for x in self]) + "]"

