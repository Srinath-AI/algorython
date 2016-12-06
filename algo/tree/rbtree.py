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


class RBTree(BaseTree):
    __slots__ = ()
    node_type = RBNode

    def find(self, data):
        return bst_find(self.root, data)

    def insert(self, data):
        new_node = RBNode(data, color=RBNode.RED)
        self.root = rb_insert_node(self.root, new_node)
        self.root.color = RBNode.BLACK

        return new_node

    def remove(self, data):
        cur = self.root
        stack = [cur]
        while cur is not None and cur.data != data:
            if data < cur.data:
                cur = cur.left
            else:
                cur = cur.right
            stack.append(cur)
        stack.pop()     # pop cur

        if cur is None:
            return None
        target = cur

        def fix_left(node):
            if rb_color_of(node.left) == RBNode.RED:
                node.left.color = RBNode.BLACK
                return

            if node.right.color == RBNode.RED:
                #     B               B
                #    / \             / \
                # * B   R           R   B
                #  /|  / \  ==>    / \  |\
                # 1 1 B   B     * B   B 2 2
                #    /|  / \     /|  /|
                #   2 2 2   2   1 1 2 2
                top = rotate_left(node)
                set_top(node, top)
                top.left.color = RBNode.RED
                top.color = RBNode.BLACK
                stack.append(top)
                fix_left(top.left)
            elif rb_color_of(node.right.left) == rb_color_of(node.right.right) == RBNode.BLACK:
                #     ?            * ?
                #    / \            / \
                # * B   B          B   R
                #  /|  / \  ==>   /|  / \
                # 1 1 B   B      1 1 B   B
                #    /|  / \        /|  / \
                #   1 1 1   1      1 1 1   1
                node.right.color = RBNode.RED
                try:
                    p = stack.pop()
                except IndexError:
                    node.color = RBNode.BLACK
                else:
                    if node is p.left:
                        fix_left(p)
                    else:
                        fix_right(p)
            elif rb_color_of(node.right.right) == RBNode.RED:
                #     ?               B               ?
                #    / \             / \             / \
                # * B   B           ?   R           B   B
                #  /|  / \  ==>    / \  |\  ==>    / \  |\
                # 1 1 2   R       B   2 2 2       B   2 2 2
                #        / \     / \             / \
                #       2   2   1   1           1   1
                top = rotate_left(node)
                set_top(node, top)
                top.color = top.left.color
                top.left.color = top.right.color = RBNode.BLACK
            else:
                #     ?              ?              ?
                #    / \            / \            / \
                # * B   B          B   R        * B   B
                #  /|  / \  ==>   /|  / \  ==>   /|  / \
                # 1 1 R   B      1 1 2   B      1 1 2   R
                #    /|  / \            / \            / \
                #   2 2 1   1          2   B          2   B
                #                         / \            / \
                #                        1   1          1   1
                assert rb_color_of(node.right.left) != rb_color_of(node.right.right) == RBNode.BLACK
                node.right = rotate_right(node.right)
                node.right.color = RBNode.BLACK
                node.right.right.color = RBNode.RED
                fix_left(node)

        def fix_right(node):
            if rb_color_of(node.right) == RBNode.RED:
                node.right.color = RBNode.BLACK
                return

            if node.left.color == RBNode.RED:
                top = rotate_right(node)
                set_top(node, top)
                top.right.color = RBNode.RED
                top.color = RBNode.BLACK
                stack.append(top)
                fix_right(top.right)
            elif rb_color_of(node.left.right) == rb_color_of(node.left.left) == RBNode.BLACK:
                node.left.color = RBNode.RED
                try:
                    p = stack.pop()
                except IndexError:
                    node.color = RBNode.BLACK
                else:
                    if node is p.right:
                        fix_right(p)
                    else:
                        fix_left(p)
            elif rb_color_of(node.left.left) == RBNode.RED:
                top = rotate_right(node)
                set_top(node, top)
                top.color = top.right.color
                top.right.color = top.left.color = RBNode.BLACK
            else:
                assert rb_color_of(node.left.right) != rb_color_of(node.left.left) == RBNode.BLACK
                node.left = rotate_left(node.left)
                node.left.color = RBNode.BLACK
                node.left.left.color = RBNode.RED
                fix_right(node)

        def set_top(old, new):
            return self.set_child(old, new, stack=stack)

        if target.right is None or target.right is None:
            child = target.left or target.right
            set_top(target, child)
            if target.color == RBNode.BLACK:
                try:
                    parent = stack.pop()
                except IndexError:
                    # target is root
                    if self.root is not None:
                        self.root.color = RBNode.BLACK
                else:
                    if child is parent.left:
                        fix_left(parent)
                    else:
                        assert child is parent.right
                        fix_right(parent)
        else:
            stack2 = [cur]
            cur = cur.right
            while cur is not None:
                stack2.append(cur)
                cur = cur.left
            cur = stack2.pop()
            stack2[0] = cur     # replace target
            parent = stack2.pop()
            need_fix = cur.color == RBNode.BLACK

            if cur is target.right:
                cur.left = target.left
                cur.color = target.color
                set_top(target, cur)
                if need_fix:
                    stack.extend(stack2)
                    fix_right(cur)
            else:
                assert parent.left is cur
                parent.left = cur.right
                cur.left = target.left
                cur.right = target.right
                cur.color = target.color
                set_top(target, cur)
                if need_fix:
                    stack.extend(stack2)
                    fix_left(parent)

        target.left = target.right = None
        return target
