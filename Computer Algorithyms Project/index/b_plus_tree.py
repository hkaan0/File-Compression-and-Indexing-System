import bisect

class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf
        self.next_leaf = None  # Only for leaf nodes
        self.parent = None  # For easier traversal (optional)

class BPlusTree:
    def __init__(self, degree=3):
        self.root = BPlusTreeNode(is_leaf=True)
        self.degree = degree
        self.min_keys = degree - 1
        self.max_keys = 2 * degree - 1

    def insert(self, key, value):
        if len(self.root.keys) == self.max_keys:
            new_root = BPlusTreeNode()
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        if node.is_leaf:
            idx = bisect.bisect_left(node.keys, key)
            node.keys.insert(idx, key)
            node.children.insert(idx, value)
        else:
            idx = bisect.bisect_left(node.keys, key)
            child = node.children[idx]
            if len(child.keys) == self.max_keys:
                self._split_child(node, idx)
                if key > node.keys[idx]:
                    child = node.children[idx + 1]
            self._insert_non_full(child, key, value)

    def _split_child(self, parent, index):
        old_node = parent.children[index]
        new_node = BPlusTreeNode(is_leaf=old_node.is_leaf)
        
        split_pos = len(old_node.keys) // 2
        split_key = old_node.keys[split_pos]
        
        # Right half goes to new node
        new_node.keys = old_node.keys[split_pos + (1 if old_node.is_leaf else 0):]
        new_node.children = old_node.children[split_pos + (1 if old_node.is_leaf else 0):]
        
        # Left half remains
        old_node.keys = old_node.keys[:split_pos]
        old_node.children = old_node.children[:split_pos + (0 if old_node.is_leaf else 1)]
        
        # Update parent
        parent.keys.insert(index, split_key)
        parent.children.insert(index + 1, new_node)
        
        # Link leaves
        if old_node.is_leaf:
            new_node.next_leaf = old_node.next_leaf
            old_node.next_leaf = new_node

    def search(self, key):
        node = self.root
        while not node.is_leaf:
            idx = bisect.bisect_left(node.keys, key)
            node = node.children[idx]
        idx = bisect.bisect_left(node.keys, key)
        return node.children[idx] if idx < len(node.keys) and node.keys[idx] == key else None

    def range_query(self, start, end):
        results = []
        leaf = self._find_leaf(start)
        while leaf:
            for i, key in enumerate(leaf.keys):
                if start <= key <= end:
                    results.append((key, leaf.children[i]))
                elif key > end:
                    return results
            leaf = leaf.next_leaf
        return results

    def _find_leaf(self, key):
        node = self.root
        while not node.is_leaf:
            idx = bisect.bisect_left(node.keys, key)
            node = node.children[idx]
        return node

    def delete(self, key):
        self._delete_recursive(self.root, key)
        if not self.root.is_leaf and len(self.root.children) == 1:
            self.root = self.root.children[0]

    def _delete_recursive(self, node, key):
        if node.is_leaf:
            idx = bisect.bisect_left(node.keys, key)
            if idx < len(node.keys) and node.keys[idx] == key:
                node.keys.pop(idx)
                node.children.pop(idx)
            return
        
        idx = bisect.bisect_left(node.keys, key)
        child = node.children[idx]
        self._delete_recursive(child, key)
        
        # Handle underflow
        if len(child.keys) < self.min_keys:
            self._fix_underflow(node, idx)

    def _fix_underflow(self, parent, index):
        # Try to borrow from left sibling
        if index > 0 and len(parent.children[index-1].keys) > self.min_keys:
            self._borrow_from_left(parent, index)
        # Try to borrow from right sibling
        elif index < len(parent.children)-1 and len(parent.children[index+1].keys) > self.min_keys:
            self._borrow_from_right(parent, index)
        # Merge with sibling
        else:
            if index > 0:
                self._merge_nodes(parent, index-1)
            else:
                self._merge_nodes(parent, index)

    def _borrow_from_left(self, parent, index):
        child = parent.children[index]
        left_sibling = parent.children[index-1]
        
        if child.is_leaf:
            # Borrow key-value pair
            borrowed_key = left_sibling.keys.pop()
            borrowed_value = left_sibling.children.pop()
            child.keys.insert(0, borrowed_key)
            child.children.insert(0, borrowed_value)
            parent.keys[index-1] = child.keys[0]
        else:
            # Borrow key and child
            borrowed_key = parent.keys[index-1]
            borrowed_child = left_sibling.children.pop()
            child.keys.insert(0, borrowed_key)
            child.children.insert(0, borrowed_child)
            parent.keys[index-1] = left_sibling.keys.pop()

    def _borrow_from_right(self, parent, index):
        child = parent.children[index]
        right_sibling = parent.children[index+1]
        
        if child.is_leaf:
            # Borrow key-value pair
            borrowed_key = right_sibling.keys.pop(0)
            borrowed_value = right_sibling.children.pop(0)
            child.keys.append(borrowed_key)
            child.children.append(borrowed_value)
            parent.keys[index] = right_sibling.keys[0]
        else:
            # Borrow key and child
            borrowed_key = parent.keys[index]
            borrowed_child = right_sibling.children.pop(0)
            child.keys.append(borrowed_key)
            child.children.append(borrowed_child)
            parent.keys[index] = right_sibling.keys.pop(0)

    def _merge_nodes(self, parent, index):
        left = parent.children[index]
        right = parent.children[index+1]
        
        if left.is_leaf:
            # Merge leaves
            left.keys += right.keys
            left.children += right.children
            left.next_leaf = right.next_leaf
        else:
            # Merge internal nodes
            left.keys.append(parent.keys.pop(index))
            left.keys += right.keys
            left.children += right.children
        
        parent.children.pop(index+1)

    def display(self, node=None, level=0):
        if node is None:
            node = self.root
        print(f"{'  '*level}{node.keys} {'(leaf)' if node.is_leaf else ''}")
        if not node.is_leaf:
            for child in node.children:
                self.display(child, level+1)




