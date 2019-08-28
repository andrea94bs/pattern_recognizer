class Node:
    def __init__(self, data=None):
        self._data = data
        self._children = []

    def insert(self, data):
        n = Node(data)
        self._children.append(n)
        return n

    def print_node(self):
        print(self.data)

