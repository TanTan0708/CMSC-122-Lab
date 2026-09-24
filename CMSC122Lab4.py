# Each node is like a single box that holds a value and points to left and right boxes
class Node:
    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    # --- INSERTION ---
    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_helper(self.root, key)

    def _insert_helper(self, current, key):
        # Smaller values go left
        if key < current.val:
            if current.left is None:
                current.left = Node(key)
            else:
                self._insert_helper(current.left, key)
        # Bigger values go right
        elif key > current.val:
            if current.right is None:
                current.right = Node(key)
            else:
                self._insert_helper(current.right, key)

    # --- DELETION ---
    def delete(self, key):
        self.root = self._delete_helper(self.root, key)

    def _delete_helper(self, current, key):
        if current is None:
            return current

        # Search for the node to delete
        if key < current.val:
            current.left = self._delete_helper(current.left, key)
        elif key > current.val:
            current.right = self._delete_helper(current.right, key)
        else:
            # Case 1 & 2: Node has no left child or no right child
            if current.left is None:
                return current.right
            elif current.right is None:
                return current.left

            # Case 3: Node has two children
            # Find the smallest value in the right branch
            temp = current.right
            while temp.left is not None:
                temp = temp.left
            
            # Replace current value with that smallest value
            current.val = temp.val
            # Remove that duplicate from the right branch
            current.right = self._delete_helper(current.right, temp.val)

        return current

    # --- 4 TRAVERSAL FUNCTIONS ---

    # 1. In-order Traversal (Left -> Root -> Right)
    def inorder(self, node):
        if node:
            self.inorder(node.left)
            print(node.val, end=" ")
            self.inorder(node.right)

    # 2. Pre-order Traversal (Root -> Left -> Right)
    def preorder(self, node):
        if node:
            print(node.val, end=" ")
            self.preorder(node.left)
            self.preorder(node.right)

    # 3. Post-order Traversal (Left -> Right -> Root)
    def postorder(self, node):
        if node:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.val, end=" ")

    # 4. Level-order Traversal (Row by Row from top to bottom)
    def levelorder(self):
        if self.root is None:
            return
        
        queue = [self.root]
        while len(queue) > 0:
            node = queue.pop(0)
            print(node.val, end=" ")
            
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)


# --- TEST PROGRAM ---
if __name__ == "__main__":
    bst = BinarySearchTree()

    # Insert items
    values = [50, 30, 70, 20, 40, 60, 80]
    for v in values:
        bst.insert(v)

    print("In-order (Sorted Order):")
    bst.inorder(bst.root)
    print("\n")

    #Pre-order Traversal Function
    
    print("Pre-order:")
    bst.preorder(bst.root)
    print("\n")

    print("Post-order:")
    bst.postorder(bst.root)
    print("\n")

    print("Level-order:")
    bst.levelorder()
    print("\n")

    print("Deleting 20 (Leaf node)...")
    bst.delete(20)
    bst.inorder(bst.root)
    print("\n")

    print("Deleting 30 (Node with children)...")
    bst.delete(30)
    bst.inorder(bst.root)
    print()

    