from algo.tree.basetree import BaseTree, rotate_left, rotate_right
from algo.tree.bstree import BSTreeMixin
from algo.tree.rbtree import rb_color_of, RBNode


def is_llrbtree(tree: BaseTree):
    if rb_color_of(tree.root) == RBNode.RED:
        return False    # root must be black

    class NotLLRBTree(Exception):
        pass

    def check(node):
        if node is None:
            return 1

        if node.color == RBNode.RED:    # children of red node is black
            if not (rb_color_of(node.left) == rb_color_of(node.right) == RBNode.BLACK):
                raise NotLLRBTree
        else:
            if rb_color_of(node.right) == RBNode.RED:
                # right leanning or 4-nodes
                raise NotLLRBTree

        lcount = check(node.left)
        rcount = check(node.right)
        if lcount != rcount:
            raise NotLLRBTree

        return lcount + int(node.color == RBNode.BLACK)

    try:
        check(tree.root)
    except NotLLRBTree:
        return False
    else:
        return True


def llrb_rotate_left(node: RBNode) -> RBNode:
    assert node.right.color == RBNode.RED
    node = rotate_left(node)
    node.color = node.left.color
    node.left.color = RBNode.RED
    return node


def llrb_rotate_right(node: RBNode) -> RBNode:
    assert node.left.color == RBNode.RED
    node = rotate_right(node)
    node.color = node.right.color
    node.right.color = RBNode.RED
    return node


def llrb_insert_node(node: RBNode, new_node: RBNode) -> RBNode:
    if node is None:
        assert new_node.color == RBNode.RED
        return new_node

    if new_node.data < node.data:
        node.left = llrb_insert_node(node.left, new_node)
    else:
        node.right = llrb_insert_node(node.right, new_node)

    # fix right leanning
    if rb_color_of(node.left) == RBNode.BLACK != rb_color_of(node.right):
        node = llrb_rotate_left(node)

    # 2-nodes to 3-nodes
    if rb_color_of(node.left) == RBNode.RED and rb_color_of(node.left.left) == RBNode.RED:
        assert node.color == RBNode.BLACK
        node = llrb_rotate_right(node)

    # split 4-nodes on the way up by flipping color
    if node.color == RBNode.BLACK and rb_color_of(node.right) == RBNode.RED:
        assert node.left.color == RBNode.RED
        node.color = RBNode.RED
        node.left.color = node.right.color = RBNode.BLACK

    return node


def llrb_left_red(node: RBNode) -> RBNode:
    if node.left.color == RBNode.BLACK:
        # flip
        node.color = RBNode.BLACK
        node.left.color = node.right.color = RBNode.RED

        if rb_color_of(node.right.left) == RBNode.RED:
            #   B          B           B           R
            #  / \        / \         / \   x     / \
            # R   R  =>  R   R  =>   R   R  =>   B   B
            #    / \        / \     / \  | \    / \  | \
            #   R              R   R           R
            #  / \            / \
            node.right = llrb_rotate_right(node.right)
            node = llrb_rotate_left(node)

    assert node.left.color == RBNode.RED
    return node


def llrb_right_red(node: RBNode) -> RBNode:
    assert node.right.color == RBNode.BLACK

    if rb_color_of(node.left) == RBNode.RED:
        node = llrb_rotate_right(node)
    else:
        # flip
        node.color = RBNode.BLACK
        node.left.color = node.right.color = RBNode.RED

        if rb_color_of(node.left.left) == RBNode.RED:
            #     B          B          B
            #    / \        / \        / \
            #   R   R  =>  R   R  =>  R   R
            #  / \  |\        / \        / \
            # R                  R      R
            #                   / \    / \
            node = llrb_rotate_right(node)
            node.right = llrb_rotate_left(node.right)
            if rb_color_of(node.right.left.right) == RBNode.RED:
                #   B          B
                #  / \        / \
                # R   R      R   R
                #    / \  =>    / \
                #   R          R
                #    \        /
                #     R      R
                node.right.left = llrb_rotate_left(node.right.left)

    assert node.right.color == RBNode.RED
    return node


def llrb_fixup(node: RBNode) -> RBNode:
    # fix right leanning
    if rb_color_of(node.left) == RBNode.BLACK != rb_color_of(node.right):
        node = llrb_rotate_left(node)

    # split 4-nodes on the way up by flipping color
    if node.color == RBNode.BLACK and rb_color_of(node.right) == RBNode.RED:
        assert node.left.color == RBNode.RED
        node.color = RBNode.RED
        node.left.color = node.right.color = RBNode.BLACK

    # fix continuous red
    if rb_color_of(node.left) == RBNode.RED and rb_color_of(node.left.left) == RBNode.RED:
        #     X
        #    /        X
        #   R   =>   / \
        #  /        R   R
        # R
        node = llrb_rotate_right(node)

    return node


def llrb_remove_min(node: RBNode) -> (RBNode, RBNode):
    if node.left is None:
        return node.right, node
    else:
        node = llrb_left_red(node)
        node.left, removed = llrb_remove_min(node.left)
        node = llrb_fixup(node)
        return node, removed


def llrb_remove(node: RBNode, data) -> (RBNode, RBNode):
    if node is None:
        return None, None

    origin_node = node
    if data < node.data:
        if node.left is None:
            return node.right, None
        node = llrb_left_red(node)
        node.left, removed = llrb_remove(node.left, data)
    elif data > node.data:
        if node.right is None:
            return node.left, None
        node = llrb_right_red(node)
        node.right, removed = llrb_remove(node.right, data)
    else:
        if node.right is None:
            return node.left, node
        elif node.left is None:
            return node.right, node
        else:
            node = llrb_right_red(node)
            if node is origin_node:
                node.right, removed = llrb_remove_min(node.right)
                removed.left, removed.right, removed.color = node.left, node.right, node.color
                removed, node = node, removed
            else:
                node.right, removed = llrb_remove(node.right, data,)

    node = llrb_fixup(node)
    return node, removed


class LLRBTree(BSTreeMixin, BaseTree):
    __slots__ = ()
    node_type = RBNode

    def insert(self, data):
        new_node = self.node_type(data, color=RBNode.RED)
        self.root = llrb_insert_node(self.root, new_node)
        self.root.color = RBNode.BLACK

        return new_node

    def remove(self, data):
        self.root, removed = llrb_remove(self.root, data)
        if rb_color_of(self.root) == RBNode.RED:
            self.root.color = RBNode.BLACK

        return removed
