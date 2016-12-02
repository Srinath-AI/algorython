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


def pretty_tree(tree):
    """
    :type tree: BaseTree
    """
    # TODO: fullwidth char?
    # TODO: colorize in ipython console

    def fmt_data(node):
        formated = repr(node.data)

        if hasattr(node, 'color'):      # for rbtree
            from algo.tree.rbtree import RBNode
            dot = {RBNode.BLACK: '■', RBNode.RED: '□'}[node.color]
            formated = dot + formated
        elif hasattr(node, 'height'):   # for avltree
            formated = '{}|h={}'.format(formated, node.height)
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

    box, _ = make_box(tree.root)
    ret = '\n'.join(box)
    return ret


def print_tree(tree):
    """
    :type tree: BaseTree
    """
    print(pretty_tree(tree))


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
                while True:
                    if not stack:       # go up
                        raise StopIteration
                    cur, c = stack.pop(), cur

                    if c is cur.left:   # go up from left
                        yield cur

                        if cur.right is not None:   # go to right
                            stack.append(cur)
                            cur = cur.right
                            break


def middle_iter_sm(root):
    """
    State machine base implementation.
    :type root: BaseNode
    """
    if root is None:
        raise StopIteration

    p1, p2 = root, root.left
    state = 1
    stack = [root]
    while True:
        if state == 1:
            # assert p1 is stack[-1]
            if p2 is None:
                p1, p2 = p2, p1
                state = 3
            else:
                p1, p2 = p2, p2.left
                stack.append(p1)
        elif state == 2:
            # assert p1 is stack[-1]
            if p2 is None:
                p1, p2 = p2, p1
                state = 4
            else:
                p1, p2 = p2, p2.left
                stack.append(p1)
                state = 1
        elif state == 3:
            # assert p2 is stack[-1]
            yield p2
            p1, p2 = p2, p2.right
            state = 2
        else:   # state = 4
            # assert p2 is stack[-1]
            stack.pop()
            try:
                p1, p2 = p2, stack[-1]
            except IndexError:
                raise StopIteration
            if p1 is p2.left:
                state = 3
            else:
                pass


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

    def deepcopy(self):
        return self.__class__(self.root.deepcopy() if self.root is not None else None)

    def node_iter(self):
        if self.root is not None:
            yield from middle_iter(self.root)

    def data_iter(self):
        for node in self.node_iter():
            yield node.data

    def count(self):
        return sum(1 for _ in self.node_iter())

    def insert(self, data):
        raise NotImplementedError

    def remove(self, data):
        raise NotImplementedError

    def set_child(self, old, new, stack=None, parent=None):
        if stack is not None:
            assert parent is None
            try:
                parent = stack[-1]
            except IndexError:
                parent = None

        if parent is None:
            assert old is self.root
            self.root = new
        elif old is parent.left:
            parent.left = new
        else:
            assert old is parent.right
            parent.right = new

    # for ipython
    def _repr_svg_(self):
        return self._to_graphviz()._repr_svg_()

    def _to_graphviz(self, graph_param=None):
        import graphviz
        import itertools

        def tree_repr_short(tree):
            return object.__repr__(tree)

        g = graphviz.Digraph()
        g.attr('node', style='filled', shape='box', fontname='fira', width='0', height='0')
        graph_attr = dict(label=tree_repr_short(self), labelloc='t')
        graph_attr.update(graph_param or dict(size='16', ratio='compress'))
        g.attr('graph', **graph_attr)

        serial_gen = map(lambda x: 'N_{}'.format(x), itertools.count())

        def get_node_option(node):
            if hasattr(node, 'color'):
                from algo.tree.rbtree import RBNode
                if node.color == RBNode.RED:
                    return dict(color='red')
                else:
                    return dict(color='black', fontcolor='white')
            elif node is None:
                return dict(color='black', fontcolor='white')
            else:
                return dict()

        def sub(node, parent=None):
            name = next(serial_gen)
            if node is not None:
                g.node(name, repr(node.data), **get_node_option(node))
                sub(node.left, name)
                sub(node.right, name)
            else:
                g.node(name, 'NIL', **get_node_option(node))
            if parent is not None:
                g.edge(parent, name)

        sub(self.root)
        return g

    try:
        __IPYTHON__
    except NameError:
        pass
    else:
        # print ascii graph
        def __repr__(self):
            return pretty_tree(self)


def rotate_right(top):
    """
    :type top: BaseNode
    """
    assert top.left is not None
    left = top.left
    top.left = left.right
    left.right = top
    return left


def rotate_left(top):
    """
    :type top: BaseNode
    """
    assert top.right is not None
    right = top.right
    top.right = right.left
    right.left = top
    return right
