import ast
from inspect import getmembers
# from code_structure.IndiscriminateFollow import IndiscriminateFollow
import queue

class MyVisitor(ast.NodeVisitor):
    def visit(self, node):
        return node.body
controller_file = open('test_file.py','r').read()
car_controller = ast.parse(controller_file)
#MyTransformer().visit(car_controller)
# pattern = IndiscriminateFollow()
# pattern_root = pattern.root
MyVisitor().visit(car_controller)
