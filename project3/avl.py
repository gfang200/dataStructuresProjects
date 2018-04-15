# AVL Trees, by Elizabeth Feicke

class AVLNode:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = None

    def __str__(self):
        return 'Node(%s)' % self.key

    def __repr__(self):
        return self.__str__()
        
def less_than(x,y):
    return x < y

class AVLTree:
    def __init__(self, root = None, less=less_than):
        self.root = root
        self.less = less

    def __str__(self):
        # recursive function that creates a list of nodes
        # for each level, None if node doesn't exist at that slot
        from itertools import chain

        # recursively accumulates nodes at each level of tree
        def drill_down(node_list, accumulated):
            if any(isinstance(n, AVLNode) for n in node_list):
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
        self.balance(self.BSTinsert(k))
        return self.search(k)

    
    def BSTinsert(self, k):
        #Helper function to insert when given a node
        def node_insert(node, key, less):
            if less(key, node.key):
                if node.left:
                    return node_insert(node.left, key, less)
                else:
                    node.left = AVLNode(key)
                    node.left.parent = node
                    return node.left
            else:
                if node.right:
                    return node_insert(node.right, key, less)
                else:
                    node.right = AVLNode(key)
                    node.right.parent = node
                    return node.right
                
        #if root exists, start inserting into tree   
        if self.root:
            return node_insert(self.root, k, self.less)
        #if not, simply insert node as root
        else:
            self.root = AVLNode(k)
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
            
    # takes node, returns node
    def delete_node(self, n):
        #helper which assumes n is not the root
        def delete(n):
            if not(n.right or n.left):
                if n.parent.left and n.parent.left.key == n.key:
                    n.parent.left = None
                else:
                    n.parent.right = None
                return n.parent
                

            elif not n.left:
                n.right.parent = n.parent
                if n.parent.left and n.parent.left.key == n.key:
                    n.parent.left = n.right
                else:
                    n.parent.right = n.right
                return n.parent
            
            elif not n.right:
                n.left.parent = n.parent
                if n.parent.left and n.parent.left.key == n.key:
                    n.parent.left = n.left
                else:
                    n.parent.right = n.left
                return n.parent
            
            else:
                s = self.successor(n)
                n.key = s.key
                return delete(s)

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
            self.balance(delete(n))
            




    def right_rotation(self, n):
        if not n.left:
            pass
        
        if n.parent:
            if n.parent.left and n.parent.left.key == n.key:
                n.parent.left = n.left
            else:
                n.parent.right = n.left
            n.left.parent = n.parent
            n.parent = n.left
        else:
            self.root = n.left
            n.left.parent = None

        carry_over = n.left.right
        if carry_over and carry_over.parent:
            carry_over.parent = n
        n.left.right = n
        n.left = carry_over

    def left_rotation(self, n):
        if not n.right:
            pass

        if n.parent:
            if n.parent.left and n.parent.left.key == n.key:
                n.parent.left = n.right
            else:
                n.parent.right = n.right
            n.right.parent = n.parent
            n.parent = n.right
        else:
            self.root = n.right
            n.right.parent = None

        carry_over = n.right.left
        if carry_over and carry_over.parent:
            carry_over.parent = n
        n.right.left = n
        n.right = carry_over

    def height(self, n):
        if n == None:
            return -1
        else:
            return 1 + max(self.height(n.left), self.height(n.right))

    def balanced(self, n):
        return (abs(self.height(n.right) - self.height(n.left)) <= 1)
          

    def right_heavy(self, n):
        return (self.height(n.right) > self.height(n.left))

    def left_heavy(self, n):
        return (self.height(n.left) > self.height(n.right))

    def balance(self, n):
        #print n.key
        if not self.balanced(n):
            if self.right_heavy(n):
                if self.left_heavy(n.right):
                    self.right_rotation(n.right)
                    #print 'right rotation on:'
                    #print n.right.key
                self.left_rotation(n)
                #print 'left rotation on:'
                #print n.key

            elif self.left_heavy(n):
                if self.right_heavy(n.left):
                    self.left_rotation(n.left)
                    #print 'left rotation on:'
                    #print n.left.key
                self.right_rotation(n)
                #print 'right rotation on:'
                #print n.key
        #print self
        if n.parent:
            self.balance(n.parent)

