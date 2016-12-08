from algo.tree.basetree import BaseNode, BaseTree, rotate_left, rotate_right
from algo.tree.bstree import bst_find


def rb_color_of(node):
    """
    :type node: RBNode
    """
    if node is None:
        return RBNode.BLACK
    else:
        return node.color


def is_rbtree(tree):
    """
    :type tree: RBTree
    """
    if rb_color_of(tree.root) == RBNode.RED:
        return False    # root must be black

    class NotRBTree(Exception):
        pass

    def check(node):
        if node is None:
            return 1

        if node.color == RBNode.RED:    # children of red node is black
            if not (rb_color_of(node.left) == rb_color_of(node.right) == RBNode.BLACK):
                raise NotRBTree

        lcount = check(node.left)
        rcount = check(node.right)
        if lcount != rcount:
            raise NotRBTree

        return lcount + int(node.color == RBNode.BLACK)

    try:
        check(tree.root)
    except NotRBTree:
        return False
    else:
        return True


class RBNode(BaseNode):
    __slots__ = ('color',)
    _extra_attr_ = BaseNode._extra_attr_ + __slots__

    RED   = 0
    BLACK = 1

    def __init__(self, data, color=RED):
        super().__init__(data)
        self.color = color

    def _short_repr_(self):
        dot = { RBNode.BLACK: '■', RBNode.RED: '□' }[self.color]
        return '{dot}{self.data}'.format_map(locals())

    def _add_to_graphviz(self, g, name):
        if self.color == RBNode.RED:
            opts = dict(color='red')
        else:
            opts = dict(color='black', fontcolor='white')
        g.node(name, repr(self.data), **opts)


def rb_insert_node(cur, node):
    """
    :type cur: RBNode
    :type node: RBNode
    """
    if cur is None:
        return node
    else:
        if node.data < cur.data:
            cur.left = rb_insert_node(cur.left, node)
            if cur.color == RBNode.BLACK:
                if cur.left.color == RBNode.RED:
                    if rb_color_of(cur.left.right) == RBNode.RED:
                        #     B            B
                        #    / \          /
                        #   R   *        R
                        #  / \     ==>  / \
                        # *   R        R   *
                        #    / \      / \
                        #   *   *    *   *
                        cur.left = rotate_left(cur.left)
                    if rb_color_of(cur.left.left) == RBNode.RED:
                        #       B
                        #      / \         R
                        #     R   *       / \
                        #    / \     ==> B   B
                        #   R   *       / \  |\
                        #  / \         *   * * *
                        # *   *
                        cur = rotate_right(cur)
                        assert cur.left.color == RBNode.RED
                        cur.left.color = RBNode.BLACK
        else:
            cur.right = rb_insert_node(cur.right, node)
            if cur.right.color == RBNode.RED:
                if rb_color_of(cur.right.left) == RBNode.RED:
                    cur.right = rotate_right(cur.right)
                if rb_color_of(cur.right.right) == RBNode.RED:
                    cur = rotate_left(cur)
                    assert cur.right.color == RBNode.RED
                    cur.right.color = RBNode.BLACK

        return cur


def rb_remove_fix_left(node):
    """
    :type node: RBNode
    :rtype: (RBNode, bool)
    """
    if rb_color_of(node.left) == RBNode.RED:
        node.left.color = RBNode.BLACK
        return node, False

    if node.right.color == RBNode.RED:
        #     B               B
        #    / \             / \
        # * B   R           R   B
        #  /|  / \  ==>    / \  |\
        # 1 1 B   B     * B   B 2 2
        #    /|  / \     /|  /|
        #   2 2 2   2   1 1 2 2
        node = rotate_left(node)
        node.color = RBNode.BLACK
        node.left.color = RBNode.RED
        node.left, need_fix = rb_remove_fix_left(node.left)
        if need_fix:
            node, need_fix = rb_remove_fix_left(node)
        assert not need_fix
        return node, False
    elif rb_color_of(node.right.left) == rb_color_of(node.right.right) == RBNode.BLACK:
        #     ?            * ?
        #    / \            / \
        # * B   B          B   R
        #  /|  / \  ==>   /|  / \
        # 1 1 B   B      1 1 B   B
        #    /|  / \        /|  / \
        #   1 1 1   1      1 1 1   1
        node.right.color = RBNode.RED
        return node, True
    elif rb_color_of(node.right.left) != rb_color_of(node.right.right) == RBNode.BLACK:
        #     ?              ?              ?
        #    / \            / \            / \
        # * B   B          B   R        * B   B
        #  /|  / \  ==>   /|  / \  ==>   /|  / \
        # 1 1 R   B      1 1 2   B      1 1 2   R
        #    /|  / \            / \            / \
        #   2 2 1   1          2   B          2   B
        #                         / \            / \
        #                        1   1          1   1
        node.right = rotate_right(node.right)
        node.right.color = RBNode.BLACK
        node.right.right.color = RBNode.RED
        node, need_fix = rb_remove_fix_left(node)
        assert not need_fix
        return node, False
    else:
        #     ?               B               ?
        #    / \             / \             / \
        # * B   B           ?   R           B   B
        #  /|  / \  ==>    / \  |\  ==>    / \  |\
        # 1 1 2   R       B   2 2 2       B   2 2 2
        #        / \     / \             / \
        #       2   2   1   1           1   1
        assert node.right.right.color == RBNode.RED
        node = rotate_left(node)
        node.color = node.left.color
        node.left.color = node.right.color = RBNode.BLACK
        return node, False


def rb_remove_fix_right(node):
    """
    :type node: RBNode
    :rtype: (RBNode, bool)
    """
    if rb_color_of(node.right) == RBNode.RED:
        node.right.color = RBNode.BLACK
        return node, False

    if node.left.color == RBNode.RED:
        node = rotate_right(node)
        node.color = RBNode.BLACK
        node.right.color = RBNode.RED
        node.right, need_fix = rb_remove_fix_right(node.right)
        if need_fix:
            node, need_fix = rb_remove_fix_right(node)
        assert not need_fix
        return node, False
    elif rb_color_of(node.left.right) == rb_color_of(node.left.left) == RBNode.BLACK:
        node.left.color = RBNode.RED
        return node, True
    elif rb_color_of(node.left.right) != rb_color_of(node.left.left) == RBNode.BLACK:
        node.left = rotate_left(node.left)
        node.left.color = RBNode.BLACK
        node.left.left.color = RBNode.RED
        node, need_fix = rb_remove_fix_right(node)
        assert not need_fix
        return node, False
    else:
        assert node.left.left.color == RBNode.RED
        node = rotate_right(node)
        node.color = node.right.color
        node.right.color = node.left.color = RBNode.BLACK
        return node, False


def rb_remove_min(node):
    """
    :type node: RBNode
    :rtype (RBNode, RBNode, bool)
    """
    if node.left is None:
        return node.right, node, node.color == RBNode.BLACK
    else:
        node.left, removed, need_fix = rb_remove_min(node.left)
        if need_fix:
            node, need_fix = rb_remove_fix_left(node)
        return node, removed, need_fix


def rb_remove(node, data):
    """
    :type node: RBNode
    :rtype (RBNode, RBNode, bool)
    """
    if node is None:
        return None, None, False

    if data == node.data:
        if node.right is None:
            return node.left, node, node.color == RBNode.BLACK
        elif node.left is None:
            return node.right, node, node.color == RBNode.BLACK
        else:
            node.right, removed, need_fix = rb_remove_min(node.right)
            removed.left, removed.right, removed.color = node.left, node.right, node.color
            node, removed = removed, node
            if need_fix:
                node, need_fix = rb_remove_fix_right(node)
            return node, removed, need_fix
    elif data < node.data:
        node.left, removed, need_fix = rb_remove(node.left, data)
        if need_fix:
            node, need_fix = rb_remove_fix_left(node)
        return node, removed, need_fix
    else:
        node.right, removed, need_fix = rb_remove(node.right, data)
        if need_fix:
            node, need_fix = rb_remove_fix_right(node)
        return node, removed, need_fix


class RBTree(BaseTree):
    __slots__ = ()
    node_type = RBNode

    def find(self, data):
        return bst_find(self.root, data)

    def insert(self, data):
        new_node = self.node_type(data, color=RBNode.RED)
        self.root = rb_insert_node(self.root, new_node)
        self.root.color = RBNode.BLACK

        return new_node

    def remove(self, data):
        self.root, removed, need_fix = rb_remove(self.root, data)
        if rb_color_of(self.root) == RBNode.RED:
            self.root.color = RBNode.BLACK

        return removed
