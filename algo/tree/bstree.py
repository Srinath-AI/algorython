from algo.tree.basetree import BaseNode, middle_iter, BaseTree


def is_bstree(tree, iterator=middle_iter):
    """
    :type tree: BaseTree
    """
    prev = None
    for node in iterator(tree.root):
        if prev is not None:
            if node.data < prev.data:
                return False
        prev = node
    else:
        return True


class BSNode(BaseNode):
    __slots__ = ()

    def insert_node(self, node):
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

    def find_first(self, data):
        cur = self
        while cur is not None and data != cur.data:
            if data < cur.data:
                cur = cur.left
            else:
                cur = cur.right

        return cur


class BSTree(BaseTree):
    __slots__ = ()
    node_type = BSNode

    def insert(self, data):
        node = self.node_type(data)
        if self.root is None:
            self.root = node
        else:
            self.root.insert_node(node)

    def find_first(self, data):
        if self.root is None:
            return None
        else:
            return self.root.find_first(data)

    def find_all(self, data):
        if self.root is None:
            raise StopIteration
        else:
            ans = self.root.find_first(data)
            while ans is not None:
                yield ans
                if ans.right is not None:
                    ans = ans.right.find_first(data)
                else:
                    raise StopIteration

    def remove(self, data):
        cur, parent, pp = self.root, None, None
        while cur is not None and cur.data != data:
            if data < cur.data:
                cur, parent, pp = cur.left, cur, parent
            else:
                cur, parent, pp = cur.right, cur, parent

        if cur is None:
            return None

        def set_top(old, new):
            return self.set_child(old, new, parent=target_parent)

        target, target_parent = cur, parent
        if target.left is None:
            set_top(target, target.right)
        elif target.right is None:
            set_top(target, target.left)
        else:
            cur, parent, pp = target.right.left, target.right, target
            while cur is not None:
                cur, parent, pp = cur.left, cur, parent
            cur, parent = parent, pp

            if cur is target.right:
                cur.left = target.left
            else:
                parent.left = cur.right
                cur.left, cur.right = target.left, target.right

            set_top(target, cur)

        target.left = target.right = None
        return target

    def min(self):
        if self.root is None:
            return None

        c = self.root
        while c.left is not None:
            c = c.left

        return c

    def max(self):
        if self.root is None:
            return None

        c = self.root
        while c.right is not None:
            c = c.right

        return c
