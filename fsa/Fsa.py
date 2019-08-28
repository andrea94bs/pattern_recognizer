from abc import ABC, abstractmethod
import ast
import parser


class MyVisitor(ast.NodeVisitor):
    def visit(self, node):
        return node.body

class Node():
    def __init__(self):
        pass

    def compare(self, to_compare):
        for x in dict(ast.iter_fields(self)):
            attr = self.__getattribute__(x)
            attr_to_compare = to_compare.__getattribute__(x)
            if attr is None:
                if attr_to_compare is not None:
                    return False
            elif isinstance(attr, list):
                if not(isinstance(attr_to_compare, list)):
                    return False
                for y,z in zip((attr, attr_to_compare)):
                    if not y.compare(z):
                        return False
            elif isinstance(x, ast.AST) and isinstance(x, Node):
                return attr.compare(attr_to_compare)
            elif isinstance(x.AST):
                return isinstance(attr_to_compare, attr.__class__)
            else:
                return attr == attr_to_compare


class Num(ast.Num, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Num)):
            raise TypeError
        else:
            return self.n == to_compare.n


class GenericNum(Num):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Num)):
            raise TypeError
        else:
            return True

class Str(ast.Str, Node):
    def compare(self, to_compare):
        if (not isinstance(to_compare, Str)):
            raise TypeError
        else:
            return self.s and to_compare.s


class GenericStr(Str):
    def compare(self, to_compare):
        if (not isinstance(to_compare, Str)):
            raise TypeError
        else:
            return True


class FormattedValue(ast.FormattedValue, Node):
    def compare(self, to_compare):
        if(not isinstance(to_compare, FormattedValue)):
            raise TypeError
        else:
            return self.value.compare(to_compare.value) and self.conversion == to_compare.conversion \
                   and self.format_spec.compare(to_compare.format_spec)


class GenericFormattedValue(FormattedValue):
    def compare(self, to_compare):
        if(not isinstance(to_compare, FormattedValue)):
            raise TypeError
        else:
            return True

class JoinedStr(ast.JoinedStr, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, JoinedStr)):
            raise TypeError
        else:
            if len(self.values) != len(to_compare.values):
                return False
            else:
                for x,y in zip((self.values, to_compare.values)):
                    if not x.compare(y):
                        return False
                return True


class GenericJoinedStr(JoinedStr):
    def compare(self, to_compare):
        if not(isinstance(to_compare, JoinedStr)):
            raise TypeError
        else:
            return True


class Bytes(ast.Bytes, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Bytes)):
            raise TypeError
        else:
            return self.s == to_compare.s


class GenericBytes(Bytes):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Bytes)):
            raise TypeError
        else:
            return True

class List(ast.List, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, List)):
            raise TypeError
        else:
            for x, y in zip((self.elts, to_compare.elts)):
                if not x.compare(y):
                    return False
            if not(isinstance(to_compare.ctx, self.ctx.__class__)):
                return False
            return True

class GenericList(List):
    def compare(self, to_compare):
        if not(isinstance(to_compare, List)):
            raise TypeError
        else:
            return True


class Tuple(ast.Tuple, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Tuple)):
            raise TypeError
        else:
            for x, y in zip((self.elts, to_compare.elts)):
                if not x.compare(y):
                    return False
            if not(isinstance(to_compare.ctx, self.ctx.__class__)):
                return False
            return True

class GenericTuple(Tuple):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Tuple)):
            raise TypeError
        else:
            return True


class Set(ast.Set, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Set)):
            raise TypeError
        else:
            for x, y in zip((self.elts, to_compare.elts)):
                if not x.compare(y):
                    return False
            return True

class GenericSet(Set):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Set)):
            raise TypeError
        else:
            return True

class Dict(ast.Dict, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Dict)):
            raise TypeError
        else:
            for x,y in zip((self.keys, to_compare.keys)):
                if not x.compare(y):
                    return False
            for x,y in zip((self.values, to_compare.values)):
                if not x.compare(y):
                    return False
            return True


class Ellipsis(ast.Ellipsis, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Ellipsis)):
            raise TypeError
        else:
            return True


class NameConstant(ast.NameConstant, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, NameConstant)):
            raise TypeError
        else:
            return self.value == to_compare.value


class Name(ast.Name, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Name)):
            raise TypeError
        else:
            return self.id == to_compare.id and isinstance(to_compare.ctx, self.ctx.__class__)


class GenericName(Name):
    def __init__(self, id, ctx):
        super().__init__(id=id, ctx=ctx)

    def compare(self, to_compare):
        if not(isinstance(to_compare, Name)):
            raise TypeError
        else:
            return True


class Starred(ast.Starred, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Starred)):
            raise TypeError
        else:
            return self.value.compare(to_compare.value) \
                   and isinstance(to_compare.ctx, self.ctx.__class__)


class GenericStarred(Starred):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Starred)):
            raise TypeError
        else:
            return True


class UnaryOp(ast.UnaryOp, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, UnaryOp)):
            raise TypeError
        else:
            return self.operand.compare(to_compare.operand) \
                   and isinstance(to_compare.op, self.op.__class__)


class GenericUnaryOp(UnaryOp):
    def compare(self, to_compare):
        if not(isinstance(to_compare, UnaryOp)):
            raise TypeError
        else:
            return True


class BinOp(ast.BinOp, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, BinOp)):
            raise TypeError
        else:
            return self.left.compare(to_compare.left) and self.right.compare(to_compare.right) \
                   and isinstance(to_compare.op, self.op.__class__)


class GenericBinOp(BinOp):
    def compare(self, to_compare):
        if not(isinstance(to_compare, BinOp)):
            raise TypeError
        else:
            return True


class BoolOp(ast.BoolOp, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, BoolOp)):
            raise TypeError
        else:
            if not(isinstance(to_compare.op, self.op.__class__)):
                return False
            if len(self.values) != len(to_compare.values):
                return False
            for x,y in zip((self.values, to_compare.values)):
                if not(x.compare(y)):
                    return False
            return True


class GenericBoolOp(BoolOp):
    def compare(self, to_compare):
        if not(isinstance(to_compare, BoolOp)):
            raise TypeError
        else:
            return True


class Compare(ast.Compare, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Compare)):
            raise TypeError
        else:
            if len(self.ops) != len(to_compare.ops):
                return False
            if len(self.comparators) != len(to_compare.comparators):
                return False
            if not self.left.compare(to_compare.left):
                return False
            for x,y in zip((self.ops, to_compare.ops)):
                if not(isinstance(y, x.__class__)):
                    return False
            for x,y in zip((self.comparators, to_compare.comparators)):
                if not(x.compare(y)):
                    return False
            return True


class GenericCompare(Compare):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Compare)):
            raise TypeError
        else:
            return True


class Call(ast.Call, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Call)):
            raise TypeError
        else:
            if len(self.args) != len(to_compare.args):
                return False
            if len(self.keywords) != len(to_compare.args):
                return False
            for x,y in zip((self.args, to_compare.args)):
                if not x.compare(y):
                    return False
            for x,y in zip((self.keywords, to_compare.keywords)):
                if not x.compare(y):
                    return False
            if 'starargs' in dict(ast.iter_fields(self)):
                if 'starargs' not in dict(ast.iter_fields(to_compare)):
                    return False
                elif not self.starargs.compare(to_compare.starargs):
                    return False
            if 'kwargs' in dict(ast.iter_fields(self)):
                if 'kwargs' not in dict(ast.iter_fields(to_compare)):
                    return False
                elif not self.starargs.compare(to_compare.starargs):
                    return False
            return self.func.compare(to_compare.func)

class GenericCall(Call):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Call)):
            raise TypeError
        else:
            return True

class keyword(ast.keyword, Node):
    def compare(self, to_compare):
        if not isinstance(to_compare, keyword):
            raise TypeError
        else:
            return self.arg == to_compare.arg and self.value.compare(to_compare.value)

class generic_keyword(keyword):
    def compare(self, to_compare):
        if not isinstance(to_compare, keyword):
            raise TypeError
        else:
            return True

class IfExp(ast.IfExp, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, IfExp)):
            raise TypeError
        else:
            return self.test.compare(to_compare.test) and self.body.compare(to_compare.body) \
                   and self.orelse.compare(to_compare.orelse)

class GenericIfExp(IfExp):
    def compare(self, to_compare):
        if not(isinstance(to_compare, IfExp)):
            raise TypeError
        else:
            return True


class Attribute(ast.Attribute, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Attribute)):
            raise TypeError
        else:
            return self.value.compare(to_compare.value) and self.attr==to_compare.attr \
                   and isinstance(to_compare.ctx, self.ctx.__class__)


class GenericAttribute(Attribute):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Attribute)):
            raise TypeError
        else:
            return True


class Subscript(ast.Subscript, Node):
    def compare(self, to_compare):
        if not (isinstance(to_compare, Subscript)):
            raise TypeError
        else:
            return self.value.compare(to_compare.value) and self.value.compare(to_compare.value)\
                   and isinstance(to_compare.ctx, self.ctx.__class__)


class GenericSubscript(Subscript):
    def compare(self, to_compare):
        if not (isinstance(to_compare, Subscript)):
            raise TypeError
        else:
            return True

class Index(ast.Index, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Index)):
            raise TypeError
        else:
            return self.value.compare(to_compare.value)

class GenericIndex(Index):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Index)):
            raise TypeError
        else:
            return True


class Slice(ast.Slice, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Slice)):
            raise TypeError
        else:
            if self.step is None:
                x = to_compare is None
            elif to_compare.step is None:
                return False
            else:
                x = self.step.compare(to_compare.step)
            return x and self.lower.compare(to_compare.lower) and self.upper.compare(to_compare.upper)

class GenericSlice(Slice):
    def compare(self, to_compare):
        if not (isinstance(to_compare, Slice)):
            raise TypeError
        else:
            return True


class ExtSlice(ast.ExtSlice, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, ExtSlice)):
            raise TypeError
        else:
            for x,y in zip((self.dims, to_compare.dims)):
                if not x.compare(y):
                    return False
            return True

class GenericExtSlice(ExtSlice):
    def compare(self, to_compare):
        if not (isinstance(to_compare, ExtSlice)):
            raise TypeError
        else:
            return True


class ListComp(ast.ListComp, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, ListComp)):
            raise TypeError
        else:
            for x,y in zip((self.generators, to_compare.generators)):
                if x.compare(y):
                    return False
            return self.elt.compare(to_compare.elt)


class GenericListComp(ListComp):
    def compare(self, to_compare):
        if not (isinstance(to_compare, ListComp)):
            raise TypeError
        else:
            return True


class SetComp(ast.SetComp, Node):
    def compare(self, to_compare):
        if not (isinstance(to_compare, SetComp)):
            raise TypeError
        else:
            for x, y in zip((self.generators, to_compare.generators)):
                if x.compare(y):
                    return False
            return self.elt.compare(to_compare.elt)


class GenericSetComp(SetComp):
    def compare(self, to_compare):
        if not (isinstance(to_compare, SetComp)):
            raise TypeError
        else:
            return True


class GeneratorExp(ast.GeneratorExp, Node):
    def compare(self, to_compare):
        if not (isinstance(to_compare, GeneratorExp)):
            raise TypeError
        else:
            for x, y in zip((self.generators, to_compare.generators)):
                if x.compare(y):
                    return False
            return self.elt.compare(to_compare.elt)


class GenericGeneratorExp(GeneratorExp):
    def compare(self, to_compare):
        if not (isinstance(to_compare, GeneratorExp)):
            raise TypeError
        else:
            return True


class DictComp(ast.DictComp, Node):
    def compare(self, to_compare):
        if not (isinstance(to_compare, DictComp)):
            raise TypeError
        else:
            for x, y in zip((self.generators, to_compare.generators)):
                if x.compare(y):
                    return False
            return self.key.compare(to_compare.key) and self.value.compare(to_compare.value)


class GenericDictComp(DictComp):
    def compare(self, to_compare):
        if not (isinstance(to_compare, DictComp)):
            raise TypeError
        else:
            return True


class comprehension(ast.comprehension, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, comprehension)):
            raise TypeError
        else:
            for x,y in zip((self.ifs, to_compare.ifs)):
                if not x.compare(y):
                    return False
            return self.target.compare(to_compare.target) and self.iter.compare(to_compare.iter) \
                   and self.is_async == to_compare.is_async


class generic_comprehension(comprehension):
    def compare(self, to_compare):
        if not (isinstance(to_compare, comprehension)):
            raise TypeError
        else:
            return True




class generic_arg(ast.arg):
    def __init__(self, arg, annotation):
        super().__init__(arg=arg, annotation=annotation)


class Assign(ast.Assign, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Assign)):
            raise TypeError
        else:
            if len(self.targets) != len(to_compare.targets):
                return False
            for x,y in zip((self.targets, to_compare.targets)):
                if not x.compare(y):
                    return False
            return self.value.compare(to_compare.value)


class GenericAssign(Assign):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Assign)):
            raise TypeError
        else:
            return True


class AnnAssign(ast.AnnAssign, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, AnnAssign)):
            raise TypeError
        else:
            if ('value' in ast.iter_fields(self)):
                if not('value' in ast.iter_fields(to_compare)):
                    return False
                if not self.value.compare(to_compare.value):
                    return False
            else:
                if ('value' in ast.iter_fields()):
                    return False
            return self.target.compare(to_compare.target) and self.annotation.compare(to_compare.annotation) \
                   and self.simple == to_compare.simple


class GenericAnnAssign(AnnAssign):
    def compare(self, to_compare):
        if not(isinstance(to_compare, AnnAssign)):
            raise TypeError
        else:
            return True


class AugAssign(ast.AugAssign, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, AugAssign)):
            raise TypeError
        else:
            return self.target.compare(to_compare.target) and self.value.compare(to_compare.value) \
                   and isinstance(to_compare.op, self.op.__class__)


class GenericAnnAssign(AnnAssign):
    def compare(self, to_compare):
        if not(isinstance(to_compare, AugAssign)):
            raise TypeError
        else:
            return True


class Raise(ast.Raise, Node):
    def compare(self, to_compare):
        if not(isinstance(to_compare, Raise)):
            raise TypeError
        else:
            if self.exc is not None:
                if to_compare.exc is None:
                    return False
                return self.exc.compare(to_compare.exc) and self.cause.compare(to_compare.cause)
            else:
                if to_compare.exc is not None:
                    return False
                return self.cause.compare(to_compare.cause)


class Assert(ast.Assert, Node):
    def compare(self, to_compare):
        pass

class GenericFunctionDef(ast.FunctionDef):
    def __init__(self, name, args, body, decorator_list, returns):
        super().__init__(name=name, args=args, body=body, decorator_list=decorator_list,
                         returns=returns)


class GenericClassDef(ast.ClassDef):
    def __init__(self, name, bases, keywords, body, decorator_list):
        super().__init__(name=name, bases=bases, keywords=keywords,
                         body=body, decorator_list=decorator_list)



class State():

    def __init__(self, name, isfinal, indentation):
        self.name = name
        self.isfinal = isfinal
        self.indentation = indentation
        self.next = None

    @abstractmethod
    def run(input):
        pass

    @abstractmethod
    def get_class(self):
        pass

    @abstractmethod
    def compare(self, node):
        pass

    def attach(self, state):
        self.next = state
        return self.next


class ModuleState(State):
    def __init__(self, name, isfinal, indentation, body):
        super().__init__(name, isfinal, indentation)
        self.body = body

    def run(input, program, pattern):
        pass

    def get_class(self):
        return ModuleState



class AssignState(ast.Assign, Node, State):
    def __init__(self, name, isfinal, indentation, targets, value):
        super().__init__(name, isfinal, indentation)
        self.targets = targets
        self.value = value

    def run(input):
        pass

    def get_class(self):
        return AssignState

    def compare(self, to_compare):
        pass

class GenericAssignState(AssignState):
    def compare(self, to_compare):
        pass
class AnnAssignState(State):
    def __init__(self, name, isfinal, indentation, targets, annotation, value, simple):
        super().__init__(name, isfinal, indentation)
        self.targets = targets
        self.value = value
        self.annotation = annotation
        self.simple = simple

    def run(input):
        pass

    def get_class(self):
        return AnnAssignState


class AugAssignState(State):
    def __init__(self, name, isfinal, indentation, target, value, op):
        super().__init__(name, isfinal, indentation)
        self.target = target
        self.value = value
        self.op = op

    def run(input):
        pass

    def get_class(self):
        return AugAssignState


class ExprState(State):
    def __init__(self, name, isfinal, indentation, value):
        super().__init__(name, isfinal, indentation)
        self.value = value

    def run(input):
        pass

    def get_class(self):
        return ExprState


class GenericStatementState(State):
    def __init__(self, name, isfinal, indentation):
        super().__init__(name, isfinal, indentation)

    def run(input):
        pass

    def get_class(self):
        return GenericStatementState


class GenericAssignmentState(State):
    def __init__(self, name, isfinal, indentation):
        super().__init__(name, isfinal, indentation)

    def run(input):
        pass

    def get_class(self):
        return GenericAssignmentState


class RaiseState(State):
    def __init__(self, name, isfinal, indentation, exc, cause):
        super().__init__(name, isfinal, indentation)
        self.exc = exc
        self.cause = cause

    def run(input):
        pass

    def get_class(self):
        return RaiseState


class AssertState(State):
    def __init__(self, name, isfinal, indentation, test, msg):
        super().__init__(name, isfinal, indentation)
        self.test = test
        self.msg = msg

    def run(input):
        pass

    def get_class(self):
        return AssertState


class ImportState(State):
    def __init__(self, name, isfinal, indentation, names):
        super().__init__(name, isfinal, indentation)
        self.names = names

    def run(input):
        pass

    def get_class(self):
        return ImportState


class ImportFromState(State):
    def __init__(self, name, isfinal, indentation, module, names):
        super().__init__(name, isfinal, indentation)
        self.names = names
        self.module = module

    def run(input):
        pass

    def get_class(self):
        return ImportFromState


class GenericClassDefState(State):
    def __init__(self, name, isfinal, indentation, body,
                 class_name, bases, keywords, decorator_list):
        super().__init__(name, isfinal, indentation)
        self.bases = bases
        self.keywords = keywords
        self.decorator_list = decorator_list
        self.class_name = class_name
        self.body = body

    def run(input):
        pass

    def get_class(self):
        return GenericClassDefState


class ClassDefState(State):
    def __init__(self, name, isfinal, body, indentation, class_name, bases, keywords, decorator_list):
        super().__init__(name, isfinal, indentation)
        self.bases = bases
        self.keywords = keywords
        self.decorator_list = decorator_list
        self.class_name = class_name
        self.body = body

    def run(input):
        pass

    def get_class(self):
        return ClassDefState


class LambdaState(State):
    def __init__(self, name, isfinal, indentation, body, args):
        super().__init__(name, isfinal, indentation)
        self.args = args
        self.body = body

    def run(input):
        pass

    def get_class(self):
        return LambdaState


class GenericFunctionDefState(State):
    def __init__(self, name, isfinal, indentation, body, function_name, args, decorator_list, returns):
        super().__init__(name, isfinal, indentation)
        self.function_name = function_name
        self.args = args
        self.decorator_list = decorator_list
        self.returns = returns
        self.body = body

    def run(input):
        pass

    def get_class(self):
        return GenericFunctionDefState


class FunctionDefState(State):
    def __init__(self, name, isfinal, indentation, body, function_name, args, decorator_list, returns):
        super().__init__(name, isfinal, indentation)
        self.function_name = function_name
        self.args = args
        self.decorator_list = decorator_list
        self.returns = returns
        self.body = body

    def run(input):
        pass

    def get_class(self):
        return FunctionDefState


class IfState(State):
    def __init__(self, name, isfinal, indentation, test, body, orelse):
        super().__init__(name, isfinal, indentation)
        self.test = test
        self.body = body
        self.orelse = orelse

    def run(input):
        pass

    def get_class(self):
        return IfState


class ForState(State):
    def __init__(self, name, isfinal, indentation, target, iter, body, orelse):
        super().__init__(name, isfinal, indentation)
        self.target = target
        self.iter = iter
        self.body = body
        self.orelse = orelse

    def run(input):
        pass

    def get_class(self):
        return ForState


class WhileState(State):
    def __init__(self, name, isfinal, indentation, test, body, orelse):
        super().__init__(name, isfinal, indentation)
        self.test = test
        self.body = body
        self.orelse = orelse

    def run(input):
        pass

    def get_class(self):
        return WhileState


class TryState(State):
    def __init__(self, name, isfinal, indentation, body, handlers, orelse, finalbody):
        super().__init__(name, isfinal, indentation)
        self.body = body
        self.handlers = handlers
        self.orelse = orelse
        self.finalbody = finalbody

    def run(input):
        pass

    def get_class(self):
        return TryState


class WithState(State):
    def __init__(self, name, isfinal, indentation, items, body):
        super().__init__(name, isfinal, indentation)
        self.items = items
        self.body = body

    def run(input):
        pass

    def get_class(self):
        return WithState


class ExceptHandlerState(State):
    def __init__(self, name, isfinal, indentation, type, handler_name, body):
        super().__init__(name, isfinal, indentation)
        self.type = type
        self.handler_name = handler_name
        self.body = body

    def run(input):
        pass

    def get_class(self):
        return ExceptHandlerState


class ReturnState(State):
    def __init__(self, name, isfinal, indentation, value):
        super().__init__(name, isfinal, indentation)
        self.value = value

    def run(input):
        pass

    def get_class(self):
        return ReturnState


correspondence = {
        ModuleState: ast.Module,
        IfState: ast.If,
        ForState: ast.For,
        WhileState: ast.While,
        ExprState: ast.Expr,
        AssignState: ast.Assign,
        AnnAssignState: ast.AnnAssign,
        AugAssignState: ast.AugAssign,
        GenericAssignmentState: ast.Assign,
        GenericClassDefState: ast.ClassDef,
        GenericFunctionDefState: ast.FunctionDef,
        GenericStatementState: ast.AST,
        ClassDefState: ast.ClassDef,
        FunctionDefState: ast.FunctionDef,
        RaiseState: ast.Raise,
        AssertState: ast.Assert,
        ImportState: ast.Import,
        ImportFromState: ast.ImportFrom,
        LambdaState: ast.Lambda,
        TryState: ast.Try,
        WithState: ast.With,
        ExceptHandlerState: ast.ExceptHandler,
        ReturnState: ast.Return
    }

class Fsa:
    def __init__(self):
        self.initial = None
        self.final = None

    def run(self, program, pattern_fsa):
        current_state = pattern_fsa
        stack = []
        for x in program.body:
            stack.append(x)
        while stack:
            current_node = stack.pop()
            if 'body' in dict(ast.iter_fields(current_node)):
                for x in current_node.body:
                    stack.append(x)
            if isinstance(current_node, correspondence.get(current_state.get_class())):
                current_state.compare(current_node)


# file = open('test_file.py','r').read()
# tree = ast.parse(file)
# #MyTransformer().visit(car_controller)
# # pattern = IndiscriminateFollow()
# # pattern_root = pattern.root
# MyVisitor().visit(tree)
# statements = [GenericAssignment, GenericStatement]
# x=None
# print(any(isinstance(x, y) for y in statements))

x = Str(s='s')
print(x.__getattribute__('s'))

### DA SISTEMARE IL PARSING DI keyword in Call(b=c)