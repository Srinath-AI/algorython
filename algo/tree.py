from algo.heap import heap_left, heap_right


class BaseNode:
    __slots__ = ('data', 'left', 'right')

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def __repr__(self):
        return '<{cls_name} at {id:#x} data={data}>'.format(
            cls_name=self.__class__.__name__,
            id=id(self),
            data=self.data,
        )

    @classmethod
    def from_heap(cls, heap, heap_root=0):
        data = heap[heap_root]
        if data is None:
            return None

        root = cls(data)

        left_index = heap_left(heap_root)
        if left_index < len(heap):
            root.left = cls.from_heap(heap, heap_root=left_index)

        right_index = heap_right(heap_root)
        if right_index < len(heap):
            root.right = cls.from_heap(heap, heap_root=right_index)

        return root

    def deepcopy(self):
        node = self.__class__(self.data)
        if self.left is not None:
            node.left = self.left.deepcopy()
        if self.right is not None:
            node.right = self.right.deepcopy()

        return node

    # def to_list(self):
    #     ret = [self.data]
    #     for child in (self.left, self.right):
    #         if child is not None:
    #             ret.append(child.to_list())
    #         else:
    #             ret.append(None)
    #
    #     return ret


def pretty_tree_vetical(root, pad1='', pad2='', pad3='', html=False, is_root=True):
    """
    :type root: BaseNode
    """
    from html import escape

    if root is None:
        return '{pad2}None'.format(pad2=pad2)

    data = repr(root.data)
    if html:
        data = escape(data)

    ret = '\n'.join([
        pretty_tree_vetical(root.left,
                    pad1 + '    ', pad1 + '┌───', pad1 + '│   ',
                    html=html, is_root=False),
        '{pad2}[{data}]'.format(pad2=pad2, data=data),
        pretty_tree_vetical(root.right,
                    pad3 + '│   ', pad3 + '└───', pad3 + '    ',
                    html=html, is_root=False),
    ])

    if html and is_root:
        ret = '<pre>\n' + ret + '</pev>\n'
    return ret


def pretty_tree(root, html=False):
    """
    :type root: BaseNode
    """

    # TODO: fullwidth char?
    # TODO: colorize rbtree with html
    from html import escape

    def fmt_data(node):
        formated = repr(node.data)
        if html:
            formated = escape(formated)

        if hasattr(node, 'color'):
            dot = {RBNode.BLACK: '■', RBNode.RED: '□'}[node.color]
            formated = dot + formated
        else:
            formated = '[{}]'.format(formated)
        return formated

    def make_box(node):
        if node is None:
            return ['NIL'], 1

        lbox, lpos = make_box(node.left)
        rbox, rpos = make_box(node.right)

        # lines that connecting parent and children
        conn_line = ' ' * lpos + '┌' + '─' * (len(lbox[0]) - lpos - 1)
        conn_line += '┴'
        conn_line += '─' * rpos + '┐'
        conn_line = conn_line.ljust(len(lbox[0]) + 1 + len(rbox[0]))
        # postion of the center of parent
        conn_pos = len(lbox[0])

        # join 2 boxes
        jbox = [conn_line]
        for i in range(max(len(lbox), len(rbox))):
            if i < len(lbox):
                line1 = lbox[i]
            else:
                line1 = ' ' * len(lbox[0])
            if i < len(rbox):
                line2 = rbox[i]
            else:
                line2 = ' ' * len(rbox[0])

            assert len(line1) + 1 + len(line2) == len(conn_line)
            jbox.append(line1 + ' ' + line2)

        # data of parent node
        data_line = fmt_data(node)
        assert len(data_line) >= 1
        center = (len(data_line) + 1) // 2 - 1

        # adjust left padding between data_line and jbox
        if center < conn_pos:
            data_line = ' ' * (conn_pos - center) + data_line
        elif conn_pos < center:
            pad = ' ' * (center - conn_pos)
            for i, line in enumerate(jbox):
                line = pad + line
                jbox[i] = line
            conn_pos = center

        jbox.insert(0, data_line)

        # adjust right padding between data_line and jbox
        box_width = max(len(line) for line in jbox)
        for i, line in enumerate(jbox):
            jbox[i] = line.ljust(box_width)

        return jbox, conn_pos

    box, _ = make_box(root)
    ret = '\n'.join(box)
    if html:
        ret = '<pre>\n' + ret + '\n</pre>\n'
    return ret


def print_tree(root):
    """
    :type root: BaseNode
    """
    print(pretty_tree(root))


def middle_iter(root):
    """
    :type root: BaseNode
    """
    if root is None:
        raise StopIteration

    if root.left is not None:
        yield from middle_iter(root.left)
    yield root
    if root.right is not None:
        yield from middle_iter(root.right)


def middle_iter_bystack(root):
    """
    :type root: BaseNode
    """
    if root is None:
        raise StopIteration

    stack = []
    cur = root
    while True:
        if cur.left is not None:        # go to left
            stack.append(cur)
            cur = cur.left
        else:
            yield cur                   # no left child

            if cur.right is not None:   # go to right
                stack.append(cur)
                cur = cur.right
            else:
                if not stack:           # go up
                    raise StopIteration
                cur, c = stack.pop(), cur

                while True:
                    if c is cur.left:   # go up from left
                        yield cur

                        if cur.right is not None:   # go to right
                            stack.append(cur)
                            cur = cur.right
                            break

                    if not stack:       # go up
                        raise StopIteration
                    cur, c = stack.pop(), cur


def is_bstree(root, iterator=middle_iter):
    """
    :type root: BaseNode
    """
    prev = None
    for node in iterator(root):
        if prev is not None:
            if node.data < prev.data:
                return False
        prev = node
    else:
        return True


def remove_from_parent(parent, child):
    if child is parent.left:
        parent.left = child.remove_self()
    else:
        parent.right = child.remove_self()


class BSNode(BaseNode):
    __slots__ = ()

    def insert(self, node):
        """
        :type node: BSNode
        """
        cur = self
        while True:
            if node.data < cur.data:
                if cur.left is None:
                    cur.left = node
                    return
                else:
                    cur = cur.left
            else:
                if cur.right is None:
                    cur.right = node
                    return
                else:
                    cur = cur.right

    def find_first_with_parent(self, value):
        cur, parent = self, None
        while cur is not None and value != cur.data:
            if value < cur.data:
                cur, parent = cur.left, cur
            else:
                cur, parent = cur.right, cur
        else:
            return cur, parent

    def find_first(self, value):
        cur, parent = self.find_first_with_parent(value)
        return cur

    def remove_self(self):
        if self.left is self.right is None:
            return None

        if self.left is not None and self.right is not None:
            removed, right = self.right.remove_left_most()
            removed.right = right
            removed.left = self.left

            return removed
        else:   # just one child
            if self.left is not None:
                return self.left
            else:
                return self.right

    def remove_self_alt(self):
        # alternate implementation of remove_self()

        if self.left is self.right is None:
            return None

        if self.left is not None:
            removed, left = self.left.remove_right_most()
            removed.left = left
            removed.right = self.right

            return removed
        else:
            removed, right = self.right.remove_left_most()
            removed.right = right
            removed.left = self.left

            return removed

    def remove_right_most(self):
        if self.right is None:
            return self, self.remove_self()

        p, c = self, self.right
        while c.right is not None:
            p, c = c, c.right

        p.right = c.remove_self()
        return c, self

    def remove_left_most(self):
        if self.left is None:
            return self, self.remove_self()

        p, c = self, self.left
        while c.left is not None:
            p, c = c, c.left

        p.left = c.remove_self()    # no recursion here since c has only one child
        return c, self


class BaseTree:
    __slots__ = ('root',)
    node_type = BaseNode

    def __init__(self, root=None):
        """
        :type root: BaseNode
        """
        self.root = root

    @classmethod
    def from_heap(cls, heap):
        tree = cls()
        tree.root = cls.node_type.from_heap(heap)
        return tree

    def node_iter(self):
        if self.root is not None:
            yield from middle_iter(self.root)

    def data_iter(self):
        for node in self.node_iter():
            yield node.data

    def count(self):
        return sum(1 for _ in self.node_iter())

    def _repr_html_(self):
        return pretty_tree(self.root, html=True)


class BSTree(BaseTree):
    __slots__ = ()
    node_type = BSNode

    def insert(self, node):
        """
        :type node: BSNode
        """
        if self.root is None:
            self.root = node
        else:
            self.root.insert(node)

    def find_first(self, value):
        if self.root is None:
            return None
        else:
            return self.root.find_first(value)

    def find_all(self, value):
        if self.root is None:
            raise StopIteration
        else:
            ans = self.root.find_first(value)
            while ans is not None:
                yield ans
                if ans.right is not None:
                    ans = ans.right.find_first(value)
                else:
                    raise StopIteration

    def remove_first(self, value):
        if self.root is None:
            return False

        child, parent = self.root.find_first_with_parent(value)
        if child is None:
            return False
        else:
            if parent is None:
                self.root = child.remove_self()
            else:
                remove_from_parent(parent, child)

            return True

    # def remove_at(self, node):
    #     pass

    def min(self):
        if self.root is None:
            return None

        c, p = self.root, None
        while c.left is not None:
            c, p = c.left, c

        return c

    def max(self):
        if self.root is None:
            return None

        c, p = self.root, None
        while c.right is not None:
            c, p = c.right, c

        return c


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

    def __init__(self, data, color=None):
        super().__init__(data)
        if color is None:
            color = self.BLACK
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
        else:
            stack = [self.root]
            while stack[-1] is not None:
                if data < stack[-1].data:
                    stack.append(stack[-1].left)
                else:
                    stack.append(stack[-1].right)
            else:
                stack.pop()     # pop None

            cur = stack.pop()
            if cur.color == RBNode.BLACK:
                node = self.node_type(data, color=RBNode.RED)
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
                                #          / \          R (pp)
                                #    (pp) R   *        / \
                                #        / \     ===> B   B (ppp)
                                # (top) R   *        / \  |\
                                #      / \          *   * * *
                                #     *   *

                                top.color = RBNode.BLACK
                                if pp is ppp.left:
                                    top = rotate_right(ppp)
                                else:
                                    top = rotate_left(ppp)

                                old = ppp
                                continue    # tail recursion
                            else:
                                #  (ppp) B              (ppp) B
                                #       / \                  / \              R (top)
                                # (pp) R   *          (top) R   *            / \
                                #     / \        ===>      / \    ===> (pp) B   B (ppp)
                                #    *   R (top)     (pp) R   *            / \  |\
                                #       / \              / \              *   * * *
                                #      *   *            *   *

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
                                continue    # tail recursion

                        return

                node = self.node_type(data, color=RBNode.BLACK)
                if cur is p.left:
                    if data < cur.data:
                        #     B
                        #    / \
                        #   R   ?
                        #  /
                        # X
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
                        node.color = RBNode.RED
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
                        node.color = RBNode.RED
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
                        cur.right = node

                        set_new_top(cur, p)

            return node
