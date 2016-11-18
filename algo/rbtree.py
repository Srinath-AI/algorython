from algo.basetree import BaseNode, BaseTree


def rb_color_of(node):
    """
    :type node: RBNode
    """
    if node is None:
        return RBNode.BLACK
    else:
        return node.color


def is_rbtree(root):
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
        # TODO: simplify this
        if self.root is None:
            self.root = self.node_type(data, RBNode.BLACK)
            return self.root

        def rotate_right(top):
            assert top.left is not None
            left = top.left
            top.left = left.right
            left.right = top
            return left

        def rotate_left(top):
            assert top.right is not None
            right = top.right
            top.right = right.left
            right.left = top
            return right

        def set_new_top(top, old):
            while True:
                try:
                    pp = stack.pop()
                except IndexError:
                    pp = None

                if pp is None:
                    self.root = top
                    if top.color == RBNode.RED:
                        top.color = RBNode.BLACK
                elif pp.left is old:
                    pp.left = top
                else:
                    assert pp.right is old
                    pp.right = top

                # both parent and child is RED, adjust it
                if pp is not None and top.color == pp.color == RBNode.RED:
                    ppp = stack.pop()
                    assert ppp.color == RBNode.BLACK

                    if (pp is ppp.left) == (top is pp.left):
                        #     (ppp) B
                        #          / \         R (pp)
                        #    (pp) R   *       / \
                        #        / \     ==> B   B (ppp)
                        # (top) R   *       / \  |\
                        #      / \         *   * * *
                        #     *   *

                        top.color = RBNode.BLACK
                        if pp is ppp.left:
                            top = rotate_right(ppp)
                        else:
                            top = rotate_left(ppp)

                        old = ppp
                        continue  # tail recursion
                    else:
                        #  (ppp) B             (ppp) B
                        #       / \                 / \             R (top)
                        # (pp) R   *         (top) R   *           / \
                        #     / \        ==>      / \    ==> (pp) B   B (ppp)
                        #    *   R (top)    (pp) R   *           / \  |\
                        #       / \             / \             *   * * *
                        #      *   *           *   *

                        pp.color = RBNode.BLACK
                        if pp is ppp.left:
                            assert top is pp.right
                            ppp.left = rotate_left(pp)
                            assert top is ppp.left
                            ret = rotate_right(ppp)
                            assert ret is top
                        else:
                            assert top is pp.left
                            ppp.right = rotate_right(pp)
                            assert top is ppp.right
                            ret = rotate_left(ppp)
                            assert ret is top

                        old = ppp
                        continue  # tail recursion

                return

        stack = [self.root]
        while stack[-1] is not None:
            if data < stack[-1].data:
                stack.append(stack[-1].left)
            else:
                stack.append(stack[-1].right)
        else:
            stack.pop()     # pop None

        node = self.node_type(data, color=RBNode.RED)

        cur = stack.pop()
        if cur.color == RBNode.BLACK:
            if data < cur.data:
                assert cur.right is None or cur.right.color == RBNode.RED
                cur.left = node
            else:
                assert cur.left is None or cur.left.color == RBNode.RED
                cur.right = node
        else:   # c.color == RBNode.RED
            assert cur.left is cur.right is None
            p = stack.pop()
            assert p is not None

            if cur is p.left:
                if data < cur.data:
                    #     B
                    #    / \
                    #   R   ?
                    #  /
                    # X
                    node.color = RBNode.BLACK
                    cur.left = node
                    p.left = None
                    cur.right = p

                    set_new_top(cur, p)
                else:
                    #     B
                    #    / \
                    #   R   ?
                    #    \
                    #     X
                    node.left = cur
                    cur.color = RBNode.BLACK
                    node.right = p
                    p.left = None

                    set_new_top(node, p)
            else:
                if data < cur.data:
                    #   B
                    #  / \
                    # ?   R
                    #    /
                    #   X
                    node.left = p
                    node.right = cur
                    cur.color = RBNode.BLACK
                    p.right = None

                    set_new_top(node, p)
                else:
                    #   B
                    #  / \
                    # ?   R
                    #      \
                    #       X
                    cur.left = p
                    p.right = None
                    node.color = RBNode.BLACK
                    cur.right = node

                    set_new_top(cur, p)

        return node
