import random

from algo.tree.basetree import BaseNode, BaseTree, rotate_left, rotate_right
from algo.tree.bstree import BSTreeMixin


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


def treap_root_from_sorted(sorted_stream):
    try:
        stack = [TreapNode(next(sorted_stream))]
    except StopIteration:
        return None

    while True:
        try:
            new_node = TreapNode(next(sorted_stream))
        except StopIteration:
            return stack[0]

        assert stack[-1].right is None
        stack[-1].right = new_node
        stack.append(new_node)
        while len(stack) >= 2 and stack[-1].priority < stack[-2].priority:
            ch, p = stack.pop(), stack.pop()
            p = rotate_left(p)
            if stack:
                stack[-1].right = p
            stack.append(p)


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


def treap_split(node, data):
    """
    :type node: TreapNode
    :rtype (TreapNode, TreapNode)
    """
    new_node = TreapNode(data)
    new_node.priority = float('-inf')
    node = treap_insert_node(node, new_node)
    assert node is new_node
    # node.left.data <= data and node.right.data > data
    return node.left, node.right


class Treap(BSTreeMixin, BaseTree):
    __slots__ = ()
    node_type = TreapNode

    @classmethod
    def from_sorted(cls, sorted_stream):
        tree = cls()
        tree.root = treap_root_from_sorted(sorted_stream)
        return tree

    def insert(self, data):
        new_node = self.node_type(data)
        self.root = treap_insert_node(self.root, new_node)
        return new_node

    def remove(self, data):
        self.root, removed = treap_remove_data(self.root, data)
        return removed

    def split(self, data):
        left, right = treap_split(self.root, data)
        self.root = None
        return Treap(left), Treap(right)
