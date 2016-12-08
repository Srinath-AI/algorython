import random

from algo.tree.basetree import BaseNode, BaseTree, rotate_left, rotate_right
from algo.tree.bstree import bst_find


def rst_size_of(node):
    """
    :type node: RSNode
    """
    return node.size if node is not None else 0


def is_rstree(tree):
    """
    :type tree: RSTree
    """
    for node in tree.node_iter():
        if node.size != 1 + rst_size_of(node.left) + rst_size_of(node.right):
            return False

    return True


def rst_fix_size(node):
    """
    :type node: RSNode
    """
    node.size = 1 + rst_size_of(node.left) + rst_size_of(node.right)


def rst_rotate_left(node):
    """
    :type node: RSNode
    """
    node = rotate_left(node)
    rst_fix_size(node.left)
    rst_fix_size(node)
    return node


def rst_rotate_right(node):
    """
    :type node: RSNode
    """
    node = rotate_right(node)
    rst_fix_size(node.right)
    rst_fix_size(node)
    return node


class RSNode(BaseNode):
    __slots__ = ('size',)
    _extra_attr_ = BaseNode._extra_attr_ + __slots__

    def __init__(self, data):
        super().__init__(data)
        self.size = 1

    def _short_repr_(self):
        return '{self.data}|s={self.size}'.format_map(locals())


def rst_insert_data_here(node, new_node):
    """
    :type node: RSNode
    :type new_node: RSNode
    """
    if node is None:
        node = new_node
    elif new_node.data < node.data:
        node.left = rst_insert_data_here(node.left, new_node)
        # node.left.size will be fixed in rotation
        node = rst_rotate_right(node)
    else:
        node.right = rst_insert_data_here(node.right, new_node)
        node = rst_rotate_left(node)

    return node


def rst_insert_node(node, new_node):
    """
    :type node: RSNode
    :type new_node: RSNode
    """
    if node is None:
        return new_node
    elif random.randrange(node.size + 1) == 0:
        return rst_insert_data_here(node, new_node)
    else:
        if new_node.data < node.data:
            node.left = rst_insert_node(node.left, new_node)
        else:
            node.right = rst_insert_node(node.right, new_node)

        node.size += 1
        return node


class RSTree(BaseTree):
    __slots__ = ()
    node_type = RSNode

    def find(self, data):
        return bst_find(self.root, data)

    def insert(self, data):
        new_node = self.node_type(data)
        self.root = rst_insert_node(self.root, new_node)
        return new_node
