import random

from algo.tree.basetree import BaseNode, BaseTree, rotate_left, rotate_right
from algo.tree.bstree import bst_find


# treap = minimum heap + binary search tree


def is_treap(tree):
    """
    :type tree: Treap
    """
    def check(node):
        if node is None:
            return True

        for child in (node.left, node.right):
            if child is not None and child.priority < node.priority:
                return False

        return check(node.left) and check(node.right)

    return check(tree.root)


class TreapNode(BaseNode):
    __slots__ = ('priority',)
    _extra_attr_ = BaseNode._extra_attr_ + __slots__

    def __init__(self, data):
        super().__init__(data)
        self.priority = random.random()

    def _short_repr_(self):
        return '{self.data}|p={self.priority:.3f}'.format_map(locals())


def treap_insert_node(node, new_node):
    """
    :type node: TreapNode
    :type new_node: TreapNode
    """
    if node is None:
        return new_node

    if new_node.data < node.data:
        node.left = treap_insert_node(node.left, new_node)
        if node.left.priority < node.priority:
            node = rotate_right(node)
    else:
        node.right = treap_insert_node(node.right, new_node)
        if node.right.priority < node.priority:
            node = rotate_left(node)

    return node


def treap_remove_data(node, data):
    """
    :type node: TreapNode
    """
    if node is None:
        return None, None
    elif data < node.data:
        node.left, removed = treap_remove_data(node.left, data)
        return node, removed
    elif data > node.data:
        node.right, removed = treap_remove_data(node.right, data)
        return node, removed
    else:
        assert data == node.data
        if node.right is None:
            return node.left, node
        elif node.left is None:
            return node.right, node
        else:
            # move node down until it can be removed directly
            if node.left.priority < node.right.priority:
                # node.left is potentially larger
                node = rotate_right(node)
                node.right, removed = treap_remove_data(node.right, data)
            else:
                node = rotate_left(node)
                node.left, removed = treap_remove_data(node.left, data)
            return node, removed


class Treap(BaseTree):
    __slots__ = ()
    node_type = TreapNode

    def find(self, data):
        return bst_find(self.root, data)

    def insert(self, data):
        new_node = self.node_type(data)
        self.root = treap_insert_node(self.root, new_node)
        return new_node

    def remove(self, data):
        self.root, removed = treap_remove_data(self.root, data)
        return removed
