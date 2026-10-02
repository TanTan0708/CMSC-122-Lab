# Each node is like a single box that holds a value and points to left and right boxes
# NEW: every box also remembers its height (how many levels are under it, counting itself)
class Node:
    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None
        self.height = 1  # a brand new node is a leaf, so height is 1


class AVLTree:
    def __init__(self):
        self.root = None

    # --- HEIGHT AND BALANCE HELPERS ---
    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def update_height(self, node):
        # Height = 1 + the taller child
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance(self, node):
        # Balance factor = left height - right height
        # 0 or 1 or -1 is fine. Anything else means the tree is leaning too much.
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # --- ROTATIONS (this is how the tree fixes itself) ---
    def rotate_right(self, y):
        # y is too heavy on the left, so its left child x moves up
        #       y            x
        #      /            / \
        #     x     -->    a   y
        #    / \              /
        #   a   b            b
        x = y.left
        b = x.right

        x.right = y
        y.left = b

        self.update_height(y)
        self.update_height(x)
        return x  # x is the new top of this branch

    def rotate_left(self, x):
        # x is too heavy on the right, so its right child y moves up
        #     x                y
        #      \              / \
        #       y    -->     x   c
        #      / \            \
        #     b   c            b
        y = x.right
        b = y.left

        y.left = x
        x.right = b

        self.update_height(x)
        self.update_height(y)
        return y  # y is the new top of this branch

    def rebalance(self, node):
        # Called on the way back up after an insert or delete
        self.update_height(node)
        balance = self.get_balance(node)

        # Left side is too heavy
        if balance > 1:
            # Left-Right case: the left child leans right, so fix it first
            if self.get_balance(node.left) < 0:
                print("  >> Left-Right case at", node.val, "(rotate left, then rotate right)")
                node.left = self.rotate_left(node.left)
            else:
                print("  >> Left-Left case at", node.val, "(rotate right)")
            return self.rotate_right(node)

        # Right side is too heavy
        if balance < -1:
            # Right-Left case: the right child leans left, so fix it first
            if self.get_balance(node.right) > 0:
                print("  >> Right-Left case at", node.val, "(rotate right, then rotate left)")
                node.right = self.rotate_right(node.right)
            else:
                print("  >> Right-Right case at", node.val, "(rotate left)")
            return self.rotate_left(node)

        # Already balanced, nothing to do
        return node

    # --- INSERTION ---
    def insert(self, key):
        self.root = self._insert_helper(self.root, key)

    def _insert_helper(self, current, key):
        # Same as a normal BST insert...
        if current is None:
            return Node(key)

        if key < current.val:
            current.left = self._insert_helper(current.left, key)
        elif key > current.val:
            current.right = self._insert_helper(current.right, key)
        else:
            return current  # no duplicates

        # ...but we rebalance on the way back up
        return self.rebalance(current)

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

        # Rebalance on the way back up
        return self.rebalance(current)

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

    # --- EXTRA: draw the tree sideways so it's easy to show on video ---
    # The root is on the left, right children are on top, left children are on the bottom
    def print_tree(self, node, level=0):
        if node is not None:
            self.print_tree(node.right, level + 1)
            print("      " * level + str(node.val) + " (h=" + str(node.height) + ")")
            self.print_tree(node.left, level + 1)


# --- DEMO HELPERS ---
def show(tree):
    print("Tree (sideways, root on the left):")
    tree.print_tree(tree.root)
    print()


def demo_title(text):
    print("=" * 55)
    print(text)
    print("=" * 55)


# --- TEST PROGRAM ---
if __name__ == "__main__":

    # DEMO 1: Right-Right case (a straight line going right)
    demo_title("DEMO 1: Insert 10, 20, 30 (leans RIGHT)")
    t1 = AVLTree()
    for v in [10, 20, 30]:
        print("Inserting", v)
        t1.insert(v)
    show(t1)

    # DEMO 2: Left-Left case (a straight line going left)
    demo_title("DEMO 2: Insert 30, 20, 10 (leans LEFT)")
    t2 = AVLTree()
    for v in [30, 20, 10]:
        print("Inserting", v)
        t2.insert(v)
    show(t2)

    # DEMO 3: Left-Right case (a zigzag)
    demo_title("DEMO 3: Insert 30, 10, 20 (zigzag: left then right)")
    t3 = AVLTree()
    for v in [30, 10, 20]:
        print("Inserting", v)
        t3.insert(v)
    show(t3)

    # DEMO 4: Right-Left case (a zigzag the other way)
    demo_title("DEMO 4: Insert 10, 30, 20 (zigzag: right then left)")
    t4 = AVLTree()
    for v in [10, 30, 20]:
        print("Inserting", v)
        t4.insert(v)
    show(t4)

    # DEMO 5: Why AVL is useful. Sorted input would ruin a normal BST.
    demo_title("DEMO 5: Insert 1 to 7 in order")
    t5 = AVLTree()
    for v in [1, 2, 3, 4, 5, 6, 7]:
        t5.insert(v)
    show(t5)
    print("AVL height:", t5.get_height(t5.root))
    print("A normal BST would have a height of 7 here (a long chain)!")
    print()

    # DEMO 6: The 4 traversals
    demo_title("DEMO 6: Traversals on the tree from Demo 5")
    print("In-order (Sorted Order):")
    t5.inorder(t5.root)
    print("\n")

    print("Pre-order:")
    t5.preorder(t5.root)
    print("\n")

    print("Post-order:")
    t5.postorder(t5.root)
    print("\n")

    print("Level-order:")
    t5.levelorder()
    print("\n")

    # DEMO 7: Deleting can also unbalance the tree
    demo_title("DEMO 7: Deletion that triggers a rotation")
    t6 = AVLTree()
    for v in [20, 10, 30, 5]:
        t6.insert(v)
    print("Before deleting:")
    show(t6)

    print("Deleting 30 (now the left side is too heavy)...")
    t6.delete(30)
    show(t6)

    print("In-order after delete:")
    t6.inorder(t6.root)
    print()