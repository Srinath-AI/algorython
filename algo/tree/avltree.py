from algo.tree.basetree import BaseNode, BaseTree, rotate_left, rotate_right
from algo.tree.bstree import BSTreeMixin


class AVLNode(BaseNode):
    __slots__ = ('height',)
    _extra_attr_ = BaseNode._extra_attr_ + __slots__

    def __init__(self, data):
        super().__init__(data)
        self.height = 1

    def _short_repr_(self):
        return '{self.data}|h={self.height}'.format_map(locals())


def avl_height_of(node: AVLNode):
    if node is None:
        return 0
    else:
        return node.height


def is_avltree(tree: 'AVLTree'):
    def check(node):
        height = avl_height_of(node)
        if height == 0:
            return node is None

        l, r = avl_height_of(node.left), avl_height_of(node.right)
        if max(l, r) - min(l, r) > 1:
            return False

        if max(l, r) + 1 != height:
            return False

        return check(node.left) and check(node.right)

    return check(tree.root)


def avl_reheight(node: AVLNode):
    node.height = 1 + max(
        avl_height_of(node.right),
        avl_height_of(node.left))


def avl_rotate_left(node: AVLNode):
    assert avl_height_of(node.right) > avl_height_of(node.left)
    node = rotate_left(node)
    avl_reheight(node.left)
    avl_reheight(node)
    return node


def avl_rotate_right(node: AVLNode):
    assert avl_height_of(node.left) > avl_height_of(node.right)
    node = rotate_right(node)
    avl_reheight(node.right)
    avl_reheight(node)
    return node


def avl_fix_left(node: AVLNode) -> AVLNode:
    assert avl_height_of(node.left) - avl_height_of(node.right) == 2
    if avl_height_of(node.left.left) == avl_height_of(node.right):
        # node.left.left is too short
        #       p             p
        #      / \           / \
        #     *   2         *   2
        #    / \           / \
        #   2   *   ==>   *  12
        #      / \       / \
        #     12  12    2  12
        node.left = avl_rotate_left(node.left)
    return avl_rotate_right(node)


def avl_fix_right(node: AVLNode) -> AVLNode:
    assert avl_height_of(node.right) - avl_height_of(node.left) == 2
    if avl_height_of(node.right.right) == avl_height_of(node.left):
        node.right = avl_rotate_right(node.right)
    return avl_rotate_left(node)


def avl_fix(node: AVLNode) -> AVLNode:
    if node is None:
        return node

    avl_reheight(node)
    lh, rh = avl_height_of(node.left), avl_height_of(node.right)
    if lh == rh + 2:
        return avl_fix_left(node)
    elif lh + 2 == rh:
        return avl_fix_right(node)
    else:
        return node


def avl_insert_node(node: AVLNode, new_node: AVLNode) -> AVLNode:
    if node is None:
        return new_node

    if new_node.data < node.data:
        node.left = avl_insert_node(node.left, new_node)
    else:
        node.right = avl_insert_node(node.right, new_node)

    return avl_fix(node)


def avl_remove_min(node: AVLNode) -> (AVLNode, AVLNode):
    if node.left is None:
        return node.right, node
    else:
        node.left, removed = avl_remove_min(node.left)
        return avl_fix(node), removed


def avl_remove(node: AVLNode, data) -> (AVLNode, AVLNode):
    if node is None:
        return node, None

    if data < node.data:
        node.left, removed = avl_remove(node.left, data)
    elif data > node.data:
        node.right, removed = avl_remove(node.right, data)
    else:
        if node.right is None:
            node, removed = node.left, node
        elif node.left is None:
            node, removed = node.right, node
        else:
            node.right, removed = avl_remove_min(node.right)
            removed.left, removed.right = node.left, node.right
            removed, node = node, removed

    return avl_fix(node), removed


class AVLTree(BSTreeMixin, BaseTree):
    __slots__ = ()
    node_type = AVLNode

    def insert(self, data) -> AVLNode:
        new_node = AVLNode(data)
        self.root = avl_insert_node(self.root, new_node)
        return new_node

    def remove(self, data) -> AVLNode:
        self.root, removed = avl_remove(self.root, data)
        return removed
