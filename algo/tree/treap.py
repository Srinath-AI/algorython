import random

from algo.tree.basetree import BaseNode, BaseTree, rotate_left, rotate_right


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

    def __init__(self, data):
        super().__init__(data)
        self.priority = random.random()

    def deepcopy(self):
        ret = super().deepcopy()
        ret.priority = self.priority
        return ret

    def _node_repr_(self):
        return '{self.data}|p={self.priority:.3}'.format_map(locals())


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


def treap_remove_next(node):
    """
    :type node: TreapNode
    """
    cur, p = node.right, node
    while cur.left is not None:
        cur, p = cur.left, cur

    if cur is node.right:
        node.right = cur.right
    else:
        p.left = cur.right

    return cur


def treap_remove_data(node, data):
    """
    :type node: TreapNode
    """
    # no rotation needed

    if node is None:
        return None, None

    if data < node.data:
        node.left, removed = treap_remove_data(node.left, data)
    elif data > node.data:
        node.right, removed = treap_remove_data(node.right, data)
    else:
        assert data == node.data
        if node.right is None:
            return node.left, node
        elif node.left is None:
            return node.right, node
        else:
            right_min = treap_remove_next(node)
            right_min.priority = node.priority
            right_min.left, right_min.right = node.left, node.right
            return right_min, node

    return node, removed


class Treap(BaseTree):
    __slots__ = ()
    node_type = TreapNode

    def insert(self, data):
        new_node = TreapNode(data)
        self.root = treap_insert_node(self.root, new_node)
        return new_node

    def remove(self, data):
        self.root, removed = treap_remove_data(self.root, data)
        return removed
