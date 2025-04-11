
RED = 'RED'
BLACK = 'BLACK'

class RBNode:
    """Red-Black Tree Node class"""
    def __init__(self, filename, filepath, color=RED):
        self.filename = filename  
        self.filepath = filepath  
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    """Red-Black Tree implementation for filename indexing"""
    def __init__(self):
        self.NIL = RBNode(None, None, BLACK)  
        self.root = self.NIL
    
    def insert(self, filename, filepath):
        """Insert a new file into the index"""
        new_node = RBNode(filename, filepath)
        new_node.left = self.NIL
        new_node.right = self.NIL
        
        parent = None
        current = self.root
        
        
        while current != self.NIL:
            parent = current
            if filename < current.filename:
                current = current.left
            else:
                current = current.right
        
        new_node.parent = parent
        
        if parent is None:
            self.root = new_node
        elif filename < parent.filename:
            parent.left = new_node
        else:
            parent.right = new_node
        
        
        self._fix_insert(new_node)
    
    def _fix_insert(self, node):
        """Maintain Red-Black Tree properties after insertion"""
        while node != self.root and node.parent.color == RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == RED:
                    
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._right_rotate(node.parent.parent)
            else:
                
                uncle = node.parent.parent.left
                if uncle.color == RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._left_rotate(node.parent.parent)
        
        self.root.color = BLACK
    
    def _left_rotate(self, x):
        """Left rotation operation"""
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y
    
    def _right_rotate(self, y):
        """Right rotation operation"""
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        
        x.right = y
        y.parent = x
    
    def search(self, filename):
        """Search for a file by name"""
        return self._search_helper(self.root, filename)
    
    def _search_helper(self, node, filename):
        """Recursive search helper"""
        if node == self.NIL:
            return None
        
        if filename == node.filename:
            return node.filepath
        elif filename < node.filename:
            return self._search_helper(node.left, filename)
        else:
            return self._search_helper(node.right, filename)
    
    def list_files(self):
        """List all files in alphabetical order"""
        files = []
        self._inorder_traversal(self.root, files)
        return files
    
    def _inorder_traversal(self, node, result):
        """In-order traversal helper"""
        if node != self.NIL:
            self._inorder_traversal(node.left, result)
            result.append((node.filename, node.filepath))
            self._inorder_traversal(node.right, result)
    
    def delete(self, filename):
        """Delete a file from the index"""
        node = self._find_node(filename)
        if node == self.NIL:
            return
        
        original_color = node.color
        if node.left == self.NIL:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL:
            x = node.left
            self._transplant(node, node.left)
        else:
            successor = self._minimum(node.right)
            original_color = successor.color
            x = successor.right
            if successor.parent == node:
                x.parent = successor
            else:
                self._transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor
            
            self._transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor
            successor.color = node.color
        
        if original_color == BLACK:
            self._fix_delete(x)
    
    def _find_node(self, filename):
        """Find a node by filename"""
        current = self.root
        while current != self.NIL:
            if filename == current.filename:
                return current
            elif filename < current.filename:
                current = current.left
            else:
                current = current.right
        return self.NIL
    
    def _minimum(self, node):
        """Find minimum node in subtree"""
        while node.left != self.NIL:
            node = node.left
        return node
    
    def _transplant(self, u, v):
        """Replace subtree u with subtree v"""
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
    def _fix_delete(self, x):
        """Maintain Red-Black Tree properties after deletion"""
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                sibling = x.parent.right
                if sibling.color == RED:
                    
                    sibling.color = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    sibling = x.parent.right
                
                if sibling.left.color == BLACK and sibling.right.color == BLACK:
                    
                    sibling.color = RED
                    x = x.parent
                else:
                    if sibling.right.color == BLACK:
                        
                        sibling.left.color = BLACK
                        sibling.color = RED
                        self._right_rotate(sibling)
                        sibling = x.parent.right
                    
                    
                    sibling.color = x.parent.color
                    x.parent.color = BLACK
                    sibling.right.color = BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                
                sibling = x.parent.left
                if sibling.color == RED:
                    sibling.color = BLACK
                    x.parent.color = RED
                    self._right_rotate(x.parent)
                    sibling = x.parent.left
                
                if sibling.right.color == BLACK and sibling.left.color == BLACK:
                    sibling.color = RED
                    x = x.parent
                else:
                    if sibling.left.color == BLACK:
                        sibling.right.color = BLACK
                        sibling.color = RED
                        self._left_rotate(sibling)
                        sibling = x.parent.left
                    
                    sibling.color = x.parent.color
                    x.parent.color = BLACK
                    sibling.left.color = BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        
        x.color = BLACK




