from code_elements.Structure import Structure
import ast
from _ast import *
from inspect import getmembers
# class ForStatement(Structure):
#     def __init__(self, expression, body):
#         self.expression = expression
#         self.body = body
#     def getExpression(self):
#         return self.expression
#
#     def getBody(self):
#         if self.body:
#             return self.body
#         return None

class ForStatement(ast.For):
    def __init__(self, expression, body):
        super().__init__()
