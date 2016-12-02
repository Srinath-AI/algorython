from algo.tree.basetree import BaseNode, BaseTree, rotate_left, rotate_right


def avl_height_of(node):
    """
    :type node: AVLNode
    """
    if node is None:
        return 0
    else:
        return node.height


def is_avltree(tree):
    """
    :type tree: AVLTree
    """
    def check(node, parent):
        height = avl_height_of(node)
        if height == 0:
            return node is None

        l, r = avl_height_of(node.left), avl_height_of(node.right)
        if max(l, r) - min(l, r) > 1:
            return False

        if max(l, r) + 1 != height:
            return False

        if parent is not None:
            if node is parent.left:
                if r > l:
                    return False
            else:
                assert node is parent.right
                if l > r:
                    return False

        return check(node.left, node) and check(node.right, node)

    return check(tree.root, None)


def avl_reheight(node):
    """
    :type node: AVLNode
    """
    node.height = 1 + max(
        avl_height_of(node.right),
        avl_height_of(node.left))


def avl_rotate_left(node):
    """
    :type node: AVLNode
    """
    assert avl_height_of(node.right) > avl_height_of(node.left)
    node = rotate_left(node)
    avl_reheight(node.left)
    avl_reheight(node)
    return node


def avl_rotate_right(node):
    """
    :type node: AVLNode
    """
    assert avl_height_of(node.left) > avl_height_of(node.right)
    node = rotate_right(node)
    avl_reheight(node.right)
    avl_reheight(node)
    return node


def avl_adjust_direction(node, parent):
    if parent is None or node is None:
        return node

    left_h, right_h = avl_height_of(node.left), avl_height_of(node.right)
    if left_h > right_h:
        assert left_h == right_h + 1
        if node is parent.right:
            return avl_rotate_right(node)
        else:
            assert node is parent.left
    elif left_h < right_h:
        assert left_h + 1 == right_h
        if node is parent.left:
            return avl_rotate_left(node)
        else:
            assert node is parent.right
    return node


class AVLNode(BaseNode):
    __slots__ = ('height',)

    def __init__(self, data):
        super().__init__(data)
        self.height = 1

    def deepcopy(self):
        ret = super().deepcopy()
        ret.height = self.height
        return ret

    def _node_repr_(self):
        return '{self.data}|h={self.height}'.format_map(locals())


class AVLTree(BaseTree):
    __slots__ = ()
    node_type = AVLNode

    def insert(self, data):
        if self.root is None:
            self.root = self.node_type(data)
            return self.root

        stack = [self.root]
        while stack[-1] is not None:
            if data < stack[-1].data:
                stack.append(stack[-1].left)
            else:
                stack.append(stack[-1].right)
        stack.pop()     # pop None

        def fix(node):
            try:
                p = stack.pop()
            except IndexError:
                return

            if node is p.left:
                if avl_height_of(node.left) < avl_height_of(node.right):
                    #       p             p
                    #      / \           / \
                    # (n) *   ?     (n) *   ?
                    #    / \           / \
                    #   2   *   ==>   *   2
                    #      / \       / \
                    #     1   2     2   1
                    p.left = node = avl_rotate_left(p.left)
                assert avl_height_of(node.left) > avl_height_of(node.right)

                left_height, right_height = avl_height_of(p.left), avl_height_of(p.right)
                if left_height == right_height:
                    #     p
                    #    / \
                    #   n   3
                    #  / \
                    # 2   1
                    return
                elif left_height == right_height + 1:
                    #     p
                    #    / \
                    #   n   2
                    #  / \
                    # 2   1
                    p.height += 1
                    fix(p)
                else:
                    #     p           n
                    #    / \         / \
                    #   n   1  ==>  2   p
                    #  / \             / \
                    # 2   1           1   1
                    assert left_height == right_height + 2
                    assert avl_height_of(node.left) \
                        == avl_height_of(node.right) + 1 \
                        == avl_height_of(p.right) + 1
                    new_p = avl_rotate_right(p)
                    self.set_child(p, new_p, stack=stack)
            else:
                assert node is p.right
                if avl_height_of(node.right) < avl_height_of(node.left):
                    p.right = node = avl_rotate_right(p.right)
                assert avl_height_of(node.right) > avl_height_of(node.left)

                right_height, left_height = avl_height_of(p.right), avl_height_of(p.left)
                if right_height == left_height:
                    return
                elif right_height == left_height + 1:
                    p.height += 1
                    fix(p)
                else:
                    assert right_height == left_height + 2
                    assert avl_height_of(node.right) \
                        == avl_height_of(node.left) + 1 \
                        == avl_height_of(p.left) + 1
                    new_p = avl_rotate_left(p)
                    self.set_child(p, new_p, stack=stack)

        cur = stack.pop()
        new_node = self.node_type(data)
        if data < cur.data:
            cur.left = new_node
        else:
            cur.right = new_node

        if cur.left is None or cur.right is None:
            cur.height += 1
            fix(cur)

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
        target_idx = len(stack)
        try:
            target_parent = stack[-1]
        except IndexError:
            target_parent = None

        def fix_child(node):
            try:
                p = stack.pop()
            except IndexError:
                p = None

            left_h, right_h = avl_height_of(node.left), avl_height_of(node.right)
            delta = max(left_h, right_h) - min(left_h, right_h)
            if delta == 0:
                avl_reheight(node)  # node may be reheighted already
                if p is not None:
                    fix_child(p)
            elif delta == 1:
                self.set_child(node, avl_adjust_direction(node, p), parent=p)
            else:
                assert delta == 2
                origin_height = node.height

                if left_h < right_h:
                    top1 = avl_rotate_left(node)
                    top1.left.right = avl_adjust_direction(top1.left.right, top1.left)
                    top1.left = avl_adjust_direction(top1.left, top1)
                else:
                    top1 = avl_rotate_right(node)
                    top1.right.left = avl_adjust_direction(top1.right.left, top1.right)
                    top1.right = avl_adjust_direction(top1.right, top1)

                self.set_child(node, top1, parent=p)
                top2 = avl_adjust_direction(top1, p)
                self.set_child(top1, top2, parent=p)
                if top2.height < origin_height:
                    assert top2.height + 1 == origin_height
                    if p is not None:
                        fix_child(p)

        if target.right is None or target.right is None:
            self.set_child(target, target.left or target.right, parent=target_parent)
            if target_parent is not None:
                stack.pop()
                fix_child(target_parent)
        else:
            stack.append(None)
            cur = target.right
            while cur is not None:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            assert stack[target_idx] is None
            stack[target_idx] = cur
            p = stack.pop()

            if cur is target.right:
                cur.left = target.left
            else:
                p.left = cur.right
                cur.left, cur.right = target.left, target.right

            avl_reheight(cur)   # cur may be p
            self.set_child(target, cur, parent=target_parent)
            fix_child(p)

        target.left = target.right = None
        return target
