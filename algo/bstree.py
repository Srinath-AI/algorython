from algo.basetree import BaseNode, middle_iter, BaseTree


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
