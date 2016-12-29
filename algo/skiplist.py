import random


class SLNode:
    __slots__ = ('tower', 'data')

    def __init__(self, data, height=1):
        self.tower = [None] * height
        self.data = data


def sl_height(p=0.5):
    ans = 1
    rand = random.random()
    threshold = p
    while rand < threshold:
        ans += 1
        threshold *= p

    return ans


def sl_insert_node(node: SLNode, new_node: SLNode):
    for next_node in reversed(node.tower):
        if next_node is not None and next_node.data <= new_node.data:
            sl_insert_node(next_node, new_node)
            # link node to new_node
            for i in range(len(next_node.tower), min(len(new_node.tower), len(node.tower))):
                new_node.tower[i] = node.tower[i]
                node.tower[i] = new_node
            return

    # insert new_node here
    assert node.data <= new_node.data
    assert node.tower[0] is None or node.tower[0].data > new_node.data

    # link node to new_node
    for i in range(min(len(new_node.tower), len(node.tower))):
        new_node.tower[i] = node.tower[i]
        node.tower[i] = new_node


def sl_remove(node: SLNode, data) -> SLNode:
    for next_node in reversed(node.tower):
        if next_node is not None and next_node.data < data:
            removed = sl_remove(next_node, data)
            if removed is not None:
                assert removed is not next_node
                for i in range(len(next_node.tower), min(len(removed.tower), len(node.tower))):
                    node.tower[i] = removed.tower[i]

            return removed

    assert node.tower[0] is None or node.tower[0].data >= data

    if node.tower[0] is not None and node.tower[0].data == data:
        removed = node.tower[0]
        for i in range(min(len(node.tower), len(removed.tower))):
            node.tower[i] = removed.tower[i]
        return removed
    else:
        return None


class SkipList:
    def __init__(self):
        self.head = SLNode(float('-inf'), height=1)

    def data_iter(self):
        cur = self.head
        while cur.tower[0] is not None:
            cur = cur.tower[0]
            yield cur.data

    def find(self, data):
        node = self.head
        while True:
            for node in reversed(node.tower):
                if node is not None and node.data <= data:
                    break

            if node is None:
                return None
            elif node.data == data:
                return node

    def insert(self, data):
        new_node = SLNode(data, height=sl_height())
        sl_insert_node(self.head, new_node)
        extended = len(new_node.tower) - len(self.head.tower)
        if extended > 0:
            # increase height of head
            self.head.tower.extend([new_node] * extended)
        return new_node

    def remove(self, data):
        removed = sl_remove(self.head, data)
        while len(self.head.tower) > 1 and self.head.tower[-1] is None:
            # decrease height of head
            self.head.tower.pop()
        return removed

    def _repr_svg_(self):
        return self._to_graphviz()._repr_svg_()

    def _to_graphviz(self):
        from graphviz import Digraph

        g = Digraph()
        g.attr('node', width='0', height='0', style='filled', shape='box', fontname='Fira Code')

        node = self.head
        while node is not None:
            data_node_id = id(node)
            data_node_name = 'D_{data_node_id}'.format_map(locals())
            g.node(data_node_name, repr(node.data), color='green', fontcolor='white')

            prev_name = data_node_name
            subgraph = Digraph()
            subgraph.attr('graph', rank='same')
            subgraph.node(prev_name)

            for i, next_node in enumerate(node.tower):
                tower_node_name = 'T_{data_node_id}_{i}'.format_map(locals())
                g.node(tower_node_name, str(i))
                g.edge(prev_name, tower_node_name)
                if next_node is not None:
                    next_node_id = id(next_node)
                    next_tower_node_name = 'T_{next_node_id}_{i}'.format_map(locals())
                    g.edge(tower_node_name, next_tower_node_name)

                subgraph.node(tower_node_name)
                prev_name = tower_node_name

            g.subgraph(subgraph)

            node = node.tower[0]

        return g
