\
from stack import ArrayStack

class BSTNode:
    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        return 'Node(%s)' % self.key

    def __repr__(self):
        return self.__str__()

def less_than(x,y):
    return x < y

class BinarySearchTree:
    def __init__(self, root = None, less=less_than):
        #I AM ROOT
        self.root = root
        self.parents = True
        self.less = less

    def __str__(self):
        # recursive function that creates a list of nodes
        # for each level, None if node doesn't exist at that slot
        from itertools import chain

        # recursively accumulates nodes at each level of tree
        def drill_down(node_list, accumulated):
            if any(isinstance(n, BSTNode) for n in node_list):
            # there are leaves left to explore
                this_layer = [(n.left, n.right) if n else (None,) for n in node_list]
                this_layer = tuple(chain(*this_layer))
                accumulated.append(this_layer)
                return drill_down(this_layer, accumulated)
            else:
                # last level was all leaves, remove it and return
                accumulated.pop()
                return accumulated

        if not self.root:
            return '<NullTree>'

        levels = drill_down([self.root], [(self.root,)])
        
        WIDTH = 10
        bottom_width = int(pow(2, len(levels)-1)) * WIDTH

        # center all the nodes
        stringified_layers = []
        for level in levels:
            level_str = ' '.join(map(lambda n: str(n).center(WIDTH) if n else '<Null> ', level))
            stringified_layers.append(level_str.center(bottom_width))

        return '\n'.join(stringified_layers) + '\n'


    # takes value, returns node with key value
    def insert(self, k):
        #Helper function to insert when given a node
        def node_insert(node, key, less):
            if less(key, node.key):
                if node.left:
                    return node_insert(node.left, key, less)
                else:
                    node.left = BSTNode(key)
                    node.left.parent = node
                    return node.left
            else:
                if node.right:
                    return node_insert(node.right, key, less)
                else:
                    node.right = BSTNode(key)
                    node.right.parent = node
                    return node.right
                
        #if root exists, start inserting into tree   
        if self.root:
            return node_insert(self.root, k, self.less)
        #if not, simply insert node as root
        else:
            self.root = BSTNode(k)
            return self.root
       

    # takes node, returns node
    # return the node with the smallest key greater than n.key
    def successor(self, n):
        #heler to move up parent chain
        def greatest_parent(n):
            parent = n.parent
            if parent and parent.right and n.key == parent.right.key:
                return greatest_parent(parent)
            else:
                return parent

        
        if n.right:
            temp = n.right
            while temp.left:
                temp = temp.left
            return temp
        else:
            return greatest_parent(n)

    # return the node with the largest key smaller than n.key
    def predecessor(self, n):
        #helper to move up the parent chain
        def least_parent(n):
            parent = n.parent
            if parent and parent.left and n.key == parent.left.key:
                return least_parent(parent)
            else:
                return parent
            
        if n.left:
            temp = n.left
            while temp.right:
                temp = temp.right
            return temp

        else:
            return least_parent(n)

    # takes key returns node
    # can return None
    def search(self, k):
        #Helper function to search on node
        def node_search(node, key, less):
            if less(key, node.key):
                if node.left:
                    return node_search(node.left, key, self.less)
                else:
                    return None
            elif less(node.key, key):
                if node.right:
                    return node_search(node.right, key, self.less)
                else:
                    return None
            else:
                return node

        if self.root:
            return node_search(self.root, k, self.less)
        else:
            return None
            
    # takes node
    def delete_node(self, n):
        #helper which assumes n is not the root
        def delete(n):
            if not(n.right or n.left):
                if n.parent.left and n.parent.left.key == n.key:
                    n.parent.left = None
                else:
                    n.parent.right = None

            elif not n.left:
                n.right.parent = n.parent
                if n.parent.left and n.parent.left.key == n.key:
                    n.parent.left = n.right
                else:
                    n.parent.right = n.right

            elif not n.right:
                n.left.parent = n.parent
                if n.parent.left and n.parent.left.key == n.key:
                    n.parent.left = n.left
                else:
                    n.parent.right = n.left

            else:
                s = self.successor(n)
                n.key = s.key
                delete(s)

        #Special care taken with root as it has no parents
        if n.key == self.root.key:
            if not (n.right or n.left):
                self.root = None 
            elif not n.right:
                self.root = n.left
                self.root.parent = None
            elif not n.left:
                self.root = n.right
                self.root.parent = None
            else:
                s = self.successor(n)
                self.root.key = s.key
                if s.right:
                    s.right.parent = s.parent
                if s.parent:
                    s.parent.left = s.right
            
        else:
            delete(n)

