from code_structure.Block import ForBlock,WhileBlock,IfBlock
from code_structure.Variable import Variable
from code_structure.Statement import ListComprehension,Assignment,IfStmnt,ForStmnt
from code_structure.Node import Node
import ast

class Node:
    def __init__(self, data=None):
        self._data = data
        self._children = []

    def insert(self, data):
        n = Node(data)
        self._children.append(n)
        return n
    def get_children(self):
        return self.children

class IndiscriminateFollow:
    def __init__(self):
        self.root = Node('ANY_NESTING')
        self.root.insert(Node('ASSIGNMENT'))
