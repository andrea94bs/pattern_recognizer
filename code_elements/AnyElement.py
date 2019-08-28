from code_elements.Structure import Structure
from ast import *


class GenericStatement(AST):
    def __init__(self):
        pass


class GenericAssignment(AST):
    def __init__(self):
        pass


class GenericExpression(AST):
    def __init__(self):
        pass


class GenericVariable(Name):
    def __init__(self, id, ctx):
        super().__init__(id=id, ctx=ctx)


class GenericAttribute(Attribute):
    def __init__(self, value, attr, ctx):
        super().__init__(value=value, attr=attr, ctx=ctx)


class GenericCall(Call):
    def __init__(self, func, args, keywords):
        super().__init__(func=func, args=args, keywords=keywords)


class GenericName(Name):
    def __init__(self, id, ctx):
        super().__init__(id=id, ctx=ctx)


class generic_arg(arg):
    def __init__(self, arg, annotation):
        super().__init__(arg=arg, annotation=annotation)


class GenericFunctionDef(FunctionDef):
    def __init__(self, name, args, body, decorator_list, returns):
        super().__init__(name=name, args=args, body=body, decorator_list=decorator_list,
                         returns=returns)


class GenericClassDef(ClassDef):
    def __init__(self, name, bases, keywords, body, decorator_list):
        super().__init__(name=name, bases=bases, keywords=keywords,
                         body=body, decorator_list=decorator_list)


x = GenericVariable(id = "v1", ctx=None)
print(x.__class__)