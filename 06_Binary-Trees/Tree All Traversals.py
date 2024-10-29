class BinaryTreeNode :
    def __init__(self, data) :
        self.data = data
        self.left = None
        self.right = None

def getTreeTraversal(root):
    res = []
    
    tmp = []
    def inorder(root):
        if not root: return
        inorder(root.left)
        tmp.append(root.data)
        inorder(root.right)
    inorder(root)
    res.append(tmp)
    
    tmp = []
    def preorder(root):
        if not root: return
        tmp.append(root.data)
        preorder(root.left)
        preorder(root.right)
    preorder(root)
    res.append(tmp)
    
    tmp = []
    def postorder(root):
        if not root: return
        postorder(root.left)
        postorder(root.right)
        tmp.append(root.data)
    postorder(root)
    res.append(tmp)
    
    return res

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def preorder(self, root):
        if root is None:
            return
        print(root.value, end=" ")
        self.preorder(root.left)
        self.preorder(root.right)

    def inorder(self, root):
        if root is None:
            return
        self.inorder(root.left)
        print(root.value, end=" ")
        self.inorder(root.right)

    def postorder(self, root):
        if root is None:
            return
        self.postorder(root.left)
        self.postorder(root.right)
        print(root.value, end=" ")
        

# Test case
if __name__ == "__main__":
    # Create a sample binary tree:
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5

    # Create root and nodes
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    # Test all traversals
    print("Preorder traversal:")
    root.preorder(root)    # Expected output: 1 2 4 5 3
    
    print("\nInorder traversal:")
    root.inorder(root)     # Expected output: 4 2 5 1 3
    
    print("\nPostorder traversal:")
    root.postorder(root)   # Expected output: 4 5 2 3 1




