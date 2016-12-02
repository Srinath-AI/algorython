from algo.tree.basetree import BaseNode, middle_iter, BaseTree


def is_bstree(tree, iterator=middle_iter):
    """
    :type tree: BaseTree
    """
    prev = None
    for node in iterator(tree.root):
        if prev is not None:
            if node.data < prev.data:
                return False
        prev = node

    return True


class BSNode(BaseNode):
    __slots__ = ()


def bst_insert_node(node, new_node):
    """
    :type node: BaseNode
    :type new_node: BaseNode
    """
    if node is None:
        return new_node

    root = node
    while True:
        if new_node.data < node.data:
            if node.left is None:
                node.left = new_node
                return root
            else:
                node = node.left
        else:
            if node.right is None:
                node.right = new_node
                return root
            else:
                node = node.right


def bst_find(node, data):
    """
    :type node: BaseNode
    """
    while node is not None and node.data != data:
        if data < node.data:
            node = node.left
        else:
            node = node.right

    return node


def bst_find_all(node, data):
    """
    :type node: BaseNode
    """
    while node is not None:
        node = bst_find(node, data)
        if node is not None:
            if node.left is not None and node.left.data == data:
                yield from bst_find_all(node.left, data)
            yield node
            node = node.right


class BSTree(BaseTree):
    __slots__ = ()
    node_type = BSNode

    def insert(self, data):
        node = self.node_type(data)
        self.root = bst_insert_node(self.root, node)
        return node

    def find(self, data):
        return bst_find(self.root, data)

    def find_all(self, data):
        yield from bst_find_all(self.root, data)

    def remove(self, data):
        cur, parent, pp = self.root, None, None
        while cur is not None and cur.data != data:
            if data < cur.data:
                cur, parent, pp = cur.left, cur, parent
            else:
                cur, parent, pp = cur.right, cur, parent

        if cur is None:
            return None

        def set_top(old, new):
            return self.set_child(old, new, parent=target_parent)

        target, target_parent = cur, parent
        if target.left is None:
            set_top(target, target.right)
        elif target.right is None:
            set_top(target, target.left)
        else:
            cur, parent, pp = target.right.left, target.right, target
            while cur is not None:
                cur, parent, pp = cur.left, cur, parent
            cur, parent = parent, pp

            if cur is target.right:
                cur.left = target.left
            else:
                parent.left = cur.right
                cur.left, cur.right = target.left, target.right

            set_top(target, cur)

        target.left = target.right = None
        return target

    def min(self):
        if self.root is None:
            return None

        c = self.root
        while c.left is not None:
            c = c.left

        return c

    def max(self):
        if self.root is None:
            return None

        c = self.root
        while c.right is not None:
            c = c.right

        return c
