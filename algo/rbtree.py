from algo.basetree import BaseNode, BaseTree, rotate_left, rotate_right


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

    RED   = 0
    BLACK = 1

    def __init__(self, data, color=RED):
        super().__init__(data)
        self.color = color

    def deepcopy(self):
        ret = super().deepcopy()
        ret.color = self.color
        return ret

    def _extra_attr(self):
        return (self.color,)


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

    def remove_data(self, data):
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
                assert rb_color_of(node.right.left) != rb_color_of(node.right.right) ==  RBNode.BLACK
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
                assert rb_color_of(node.left.right) != rb_color_of(node.left.left) ==  RBNode.BLACK
                node.left = rotate_left(node.left)
                node.left.color = RBNode.BLACK
                node.left.left.color = RBNode.RED
                fix_right(node)

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

        if target.right is None or target.right is None:
            new_top = target.left or target.right
            set_top(target, new_top)
            if target.color == RBNode.BLACK:
                try:
                    p = stack.pop()
                except IndexError:
                    # target is root
                    if self.root is not None:
                        self.root.color = RBNode.BLACK
                else:
                    if new_top is p.left:
                        fix_left(p)
                    else:
                        assert new_top is p.right
                        fix_right(p)
        else:
            stack2 = [cur]
            cur = cur.right
            while cur is not None:
                stack2.append(cur)
                cur = cur.left
            cur = stack2.pop()
            stack2[0] = cur     # replace target
            p = stack2.pop()
            need_fix = cur.color == RBNode.BLACK

            if cur is target.right:
                cur.left = target.left
                cur.color = target.color
                set_top(target, cur)
                if need_fix:
                    stack.extend(stack2)
                    fix_right(cur)
            else:
                assert p.left is cur
                p.left = cur.right
                cur.left = target.left
                cur.right = target.right
                cur.color = target.color
                set_top(target, cur)
                if need_fix:
                    stack.extend(stack2)
                    fix_left(p)

        target.left = target.right = None
        return target
