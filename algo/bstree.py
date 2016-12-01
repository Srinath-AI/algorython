from algo.basetree import BaseNode, middle_iter, BaseTree


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


class BSTree(BaseTree):
    __slots__ = ()
    node_type = BSNode

    def insert(self, data):
        node = self.node_type(data)
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

    def remove(self, data):
        cur, parent, pp = self.root, None, None
        while cur is not None and cur.data != data:
            if data < cur.data:
                cur, parent, pp = cur.left, cur, parent
            else:
                cur, parent, pp = cur.right, cur, parent

        if cur is None:
            return None

        def set_top(old, new, parent):
            if parent is None:
                assert old is self.root
                self.root = new
            elif old is parent.left:
                parent.left = new
            else:
                parent.right = new

        target, target_parent = cur, parent
        if target.left is None:
            set_top(target, target.right, target_parent)
        elif target.right is None:
            set_top(target, target.left, target_parent)
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

            set_top(target, cur, target_parent)

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
