from algo.basetree import BaseNode, BaseTree, rotate_left, rotate_right


def rb_color_of(node):
    """
    :type node: RBNode
    """
    if node is None:
        return RBNode.BLACK
    else:
        return node.color


def is_rbtree_root(root):
    """
    :type root: RBNode
    """
    if rb_color_of(root) == RBNode.RED:
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
        check(root)
    except NotRBTree:
        return False
    else:
        return True


class RBNode(BaseNode):
    __slots__ = ('color',)

    RED   = 0
    BLACK = 1

    def __init__(self, data, color=RED):
        super().__init__(data)
        self.color = color

    def deepcopy(self):
        ret = super().deepcopy()
        ret.color = self.color
        return ret


class RBTree(BaseTree):
    __slots__ = ()
    node_type = RBNode

    def deepcopy(self):
        return RBTree(self.root.deepcopy() if self.root is not None else None)

    def insert_data(self, data):
        if self.root is None:
            self.root = self.node_type(data, RBNode.BLACK)
            return self.root

        stack = [self.root]
        while stack[-1] is not None:
            if data < stack[-1].data:
                stack.append(stack[-1].left)
            else:
                stack.append(stack[-1].right)
        else:
            stack.pop()     # pop None

        cur = stack[-1]
        node = self.node_type(data, color=RBNode.RED)
        if data < cur.data:
            cur.left = node
        else:
            cur.right = node

        def set_top(old_top, new_top):
            try:
                p = stack[-1]
            except IndexError:
                self.root = new_top
            else:
                if old_top is p.left:
                    p.left = new_top
                else:
                    p.right = new_top

        def fix(red):
            assert red.color == RBNode.RED
            while red.color == RBNode.RED:
                p = stack.pop()

                if red.left is not None and red.left.color == RBNode.RED:
                    if red is p.left:
                        #     (p) B
                        #        / \         R (red)
                        # (red) R   *       / \
                        #      / \     ==> B   B (p)
                        #     R   *       / \  |\
                        #    / \         *   * * *
                        #   *   *
                        top = rotate_right(p)
                        top.left.color = RBNode.BLACK
                    else:
                        #   B (p)          B (p)
                        #  / \            / \                  R
                        # *   R (red)    *   R                / \
                        #    / \     ==>    / \      ==> (p) B   B (red)
                        #   R   *          *   R (red)      / \  |\
                        #  / \                / \          *   * * *
                        # *   *              *   *
                        assert red is p.right
                        p.right = rotate_right(red)
                        top = rotate_left(p)
                        top.right.color = RBNode.BLACK
                else:
                    assert red.right.color == RBNode.RED
                    if red is p.left:
                        p.left = rotate_left(red)
                        top = rotate_right(p)
                        top.left.color = RBNode.BLACK
                    else:
                        assert red is p.right
                        top = rotate_left(p)
                        top.right.color = RBNode.BLACK

                assert top.color == RBNode.RED
                set_top(p, top)

                try:
                    red = stack.pop()   # recursion
                except IndexError:
                    top.color = RBNode.BLACK
                    return

        if cur.color == RBNode.RED:
            fix(stack.pop())

        return node
