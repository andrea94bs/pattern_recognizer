from abc import ABC, abstractmethod
import ast
import parser
import copy

from spyder.utils.programs import ProgramError
from win32comext.axscript.server.error import Exception

from code_elements.Function import Function

global program_memory
program_memory = {}

class MyVisitor(ast.NodeVisitor):
    def visit(self, node):
        return node.body


class Node():
    def __init__(self, father=None, binding_id=None):
        self.next = None
        self.father = father
        self.binding_id = binding_id

    def compare(self, to_compare, memory=None):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not (isinstance(to_compare, self.__class__)):
            program_memory = backup_memory
            return False
        for x in dict(ast.iter_fields(self)):
            if x not in ['body', 'orelse', 'handlers', 'finalbody']:
                attr = self.__getattribute__(x)
                attr_to_compare = to_compare.__getattribute__(x)
                if attr is None:
                    if attr_to_compare is not None:
                        program_memory = backup_memory
                        return False
                elif isinstance(attr, list):
                    if not(isinstance(attr_to_compare, list)):
                        program_memory = backup_memory
                        return False
                    if len(attr) != len(attr_to_compare):
                        program_memory = backup_memory
                        return False
                    for y,z in zip(attr, attr_to_compare):
                        if not(y.compare(z)):
                            program_memory = backup_memory
                            return False
                elif isinstance(attr, EmptyClass):
                    if not (attr.compare(attr_to_compare)):
                        program_memory = backup_memory
                        return False
                elif isinstance(attr, Node):
                    if not attr.compare(attr_to_compare):
                        program_memory = backup_memory
                        return False
                else:
                    if not (attr == attr_to_compare):
                        program_memory = backup_memory
                        return False
        return True

    def attach(self, to_attach):
        self.next = to_attach
        return to_attach

    def __deepcopy__(self, memo={}):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result


class GenericNode(Node):

    def __init__(self=None, multi=False, binding_id=None):
        self.multi=multi
        Node.__init__(self)
        self.binding_id = binding_id

    @abstractmethod
    def compare(self, to_compare):
        pass


class EmptyClass(Node):
    def __init__(self, binding_id=None):
        Node.__init__(self, binding_id=binding_id)
        self.binding_id = binding_id

    @abstractmethod
    def compare(self, to_compare):
        pass


class Num(ast.Num, Node):
    def __init__(self, n, binding_id=None):
        super().__init__(n=n)
        Node.__init__(self, binding_id=binding_id)


class GenericNum(GenericNode):
    def __init__(self, binding_id=None, gt=None, lt=None):
        self.gt = gt
        self.lt = lt
        super().__init__(binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Num)):
            program_memory = backup_memory
            return False
        if (self.gt and self.lt):
            return to_compare.n > self.gt and to_compare.n < self.lt
        if (self.gt):
            return to_compare.n > self.gt
        if (self.lt):
            return to_compare.n < self.lt
        return True




class Str(ast.Str, Node):
    def __init__(self, s, binding_id=None):
        super().__init__(s=s)
        Node.__init__(self, binding_id=binding_id)



class GenericStr(GenericNode):
    def __init__(self, binding_id=None, name=None):
        self.name = name
        super().__init__(binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, (Str, str))):
            program_memory = backup_memory
            return False
        return True




class FormattedValue(ast.FormattedValue, Node):
    def __init__(self, value, conversion, format_spec, binding_id=None):
        super().__init__(value=value, conversion=conversion, format_spec=format_spec)
        Node.__init__(self, binding_id=binding_id)


class GenericFormattedValue(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, FormattedValue)):
            program_memory = backup_memory
            return False
        return True





class JoinedStr(ast.JoinedStr, Node):
    def __init__(self, values, binding_id=None):
        super().__init__(values=values)
        Node.__init__(self, binding_id=binding_id)


class GenericJoinedStr(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, JoinedStr)):
            program_memory = backup_memory
            return False
        return True




class Bytes(ast.Bytes, Node):
    def __init__(self, s, binding_id=None):
        super().__init__(s=s)
        Node.__init__(self, binding_id=binding_id)


class GenericBytes(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Bytes)):
            program_memory = backup_memory
            return False
        return True




class List(ast.List, Node):
    def __init__(self, elts, ctx, binding_id=None):
        super().__init__(elts=elts, ctx=ctx)
        Node.__init__(self, binding_id=binding_id)

class GenericList(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, List)):
            program_memory = backup_memory
            return False
        return True




class Tuple(ast.Tuple, Node):
    def __init__(self, elts, ctx, binding_id=None):
        super().__init__(elts=elts, ctx=ctx)
        Node.__init__(self, binding_id=binding_id)

class GenericTuple(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Tuple)):
            program_memory = backup_memory
            return False
        return True




class Set(ast.Set, Node):
    def __init__(self, elts, binding_id=None):
        super().__init__(elts=elts)
        Node.__init__(self, binding_id=binding_id)


class GenericSet(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Set)):
            program_memory = backup_memory
            return False
        return True




class Dict(ast.Dict, Node):
    def __init__(self, keys, values, binding_id=None):
        super().__init__(keys=keys, values=values)
        Node.__init__(self, binding_id=binding_id)


class GenericDict(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Dict)):
            program_memory = backup_memory
            return False
        return True





class Ellipsis(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Ellipsis):
            program_memory = backup_memory
            return False
        return True


class NameConstant(ast.NameConstant, Node):
    def __init__(self, value, binding_id=None):
        super().__init__(value=value)
        Node.__init__(self, binding_id=binding_id)


class GenericNameConstant(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, NameConstant)):
            program_memory = backup_memory
            return False
        return True





class Name(ast.Name, Node):
    def __init__(self, id, ctx, binding_id=None):
        super().__init__(id=id, ctx=ctx)
        Node.__init__(self, binding_id=binding_id)


class GenericName(GenericNode):
    def __init__(self, name, multi=False, binding_id=None):
        self.name = name
        super().__init__(multi=multi, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if '_MULTI_' in self.name:
            if not (isinstance(to_compare, (Name, Attribute, Subscript, Call))):
                program_memory = backup_memory
                return False
        else:
            if not(isinstance(to_compare, Name)):
                program_memory = backup_memory
                return False
            if program_memory:
                for e in program_memory:
                    if to_compare.id == e:
                        program_memory.get(e).append(self.binding_id)
                        break
                else:
                    program_memory[to_compare.id] = [self.binding_id]
            else:
                program_memory[to_compare.id] = [self.binding_id]
        return True





class Load(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Load):
            program_memory = backup_memory
            return False
        return True


class Store(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Store):
            program_memory = backup_memory
            return False
        return True


class Del(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Del):
            program_memory = backup_memory
            return False
        return True


class Starred(ast.Starred, Node):
    def __init__(self, value, ctx, binding_id=None):
        super().__init__(value=value, ctx=ctx)
        Node.__init__(self, binding_id=binding_id)

class GenericStarred(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Starred)):
            program_memory = backup_memory
            return False
        return True




class Expr(ast.Expr, Node):
    def __init__(self, value, binding_id=None):
        super().__init__(value=value)
        Node.__init__(self, binding_id=binding_id)


class GenericExpr(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Expr)):
            program_memory = backup_memory
            return False
        return True






class GenericExpression(GenericNode):
    def __init__(self, multi=False, binding_id=None):
        super().__init__(multi=multi)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        # if (not isinstance(to_compare, Name)) and (not isinstance(to_compare, Attribute)) and (not isinstance(to_compare, Compare)) \
        #         and (not isinstance(to_compare, NameConstant)):
        #     program_memory = backup_memory
        #     return False
        return True


class UnaryOp(ast.UnaryOp, Node):
    def __init__(self, op, operand, binding_id=None):
        super().__init__(op=op, operand=operand)
        Node.__init__(self, binding_id=binding_id)


class GenericUnaryOp(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, UnaryOp)):
            program_memory = backup_memory
            return False
        return True




class UAdd(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, UAdd):
            program_memory = backup_memory
            return False
        return True


class USub(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, USub):
            program_memory = backup_memory
            return False
        return True


class Not(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Not):
            program_memory = backup_memory
            return False
        return True


class Invert(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Invert):
            program_memory = backup_memory
            return False
        return True


class BinOp(ast.BinOp, Node):
    def __init__(self, left, op, right, binding_id=None):
        super().__init__(left=left, op=op, right=right)
        Node.__init__(self, binding_id=binding_id)


class GenericBinOp(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, BinOp)):
            program_memory = backup_memory
            return False
        return True






class Add(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Add):
            program_memory = backup_memory
            return False
        return True


class Sub(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Sub):
            program_memory = backup_memory
            return False
        return True


class Mult(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Mult):
            program_memory = backup_memory
            return False
        return True


class Div(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Div):
            program_memory = backup_memory
            return False
        return True


class FloorDiv(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, FloorDiv):
            program_memory = backup_memory
            return False
        return True


class Mod(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Mod):
            program_memory = backup_memory
            return False
        return True


class Pow(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Pow):
            program_memory = backup_memory
            return False
        return True


class LShift(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, LShift):
            program_memory = backup_memory
            return False
        return True


class RShift(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, RShift):
            program_memory = backup_memory
            return False
        return True


class BitOr(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, BitOr):
            program_memory = backup_memory
            return False
        return True


class BitXor(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, BitXor):
            program_memory = backup_memory
            return False
        return True


class BitAnd(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, BitAnd):
            program_memory = backup_memory
            return False
        return True


class MatMult(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, MatMult):
            program_memory = backup_memory
            return False
        return True


class BoolOp(ast.BoolOp, Node):
    def __init__(self, op, values, binding_id=None):
        super().__init__(op=op, values=values)
        Node.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        if not isinstance(to_compare, Node):
            raise TypeError
        if isinstance(self.op, And):
            if len(self.values) > 1:
                if isinstance(self.values[1], GenericExpression):
                    if isinstance(to_compare, BoolOp):
                        for value in to_compare.values:
                            res = Node.compare(self.values[0], value)
                            if res :
                                return res
                        return res
                    return Node.compare(self.values[0], to_compare)
        return Node.compare(self, to_compare)


class GenericBoolOp(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)


    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, BoolOp)):
            program_memory = backup_memory
            return False
        return True






class And(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, And):
            program_memory = backup_memory
            return False
        return True


class Or(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Or):
            program_memory = backup_memory
            return False
        return True


class Compare(ast.Compare, Node):
    def __init__(self, left, ops, comparators, binding_id=None):
        super().__init__(left=left, ops=ops, comparators=comparators)
        Node.__init__(self, binding_id=binding_id)


class GenericCompare(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Compare)):
            program_memory = backup_memory
            return False
        return True






class Eq(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Eq):
            program_memory = backup_memory
            return False
        return True


class NotEq(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, NotEq):
            program_memory = backup_memory
            return False
        return True


class Lt(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Lt):
            program_memory = backup_memory
            return False
        return True


class LtE(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, LtE):
            program_memory = backup_memory
            return False
        return True


class Gt(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Gt):
            program_memory = backup_memory
            return False
        return True


class GtE(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, GtE):
            program_memory = backup_memory
            return False
        return True


class Is(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Is):
            program_memory = backup_memory
            return False
        return True


class IsNot(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, IsNot):
            program_memory = backup_memory
            return False
        return True


class In(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, In):
            program_memory = backup_memory
            return False
        return True


class NotIn(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, NotIn):
            program_memory = backup_memory
            return False
        return True


class Call(ast.Call, Node):
    def __init__(self, func=None, args=None, keywords=None, binding_id=None):
        super().__init__(func=func, args=args, keywords=keywords)
        Node.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        if not isinstance(to_compare, Node):
            raise TypeError
        if not isinstance(to_compare, Call):
            return False
        if self.args:
            for i in range(0, len(self.args)):
                if isinstance(self.args[i], Name) and self.args[i].id == '_ARGS_':
                    break
            else:
                return Node.compare(self, to_compare)
            return Node.compare(Call(func=self.func, args=self.args[0:i], keywords=None, binding_id=self.binding_id),
                                Call(func=to_compare.func, args=to_compare.args[0:i], keywords=None,
                                     binding_id=to_compare.binding_id))

class GenericCall(GenericNode):
    def __init__(self, multi=False, binding_id=None, name=None, args=None, keywords=None, func=None):
        self.multi = multi
        self.func = func
        self.name = name
        self.args = args
        self.keywords = keywords
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Call)):
            program_memory = backup_memory
            return False
        else:
            name = to_compare.func.id if isinstance(to_compare.func, Name) else to_compare.func.attr
            if program_memory:
                for e in program_memory:
                    if name == e:
                        program_memory.get(e).append(self.binding_id)
                        break
                else:
                    program_memory[name] = [self.binding_id]
            else:
                program_memory[name] = [self.binding_id]
            if self.args or self.keywords:
                return Node.compare(Call(args=self.args, keywords=self.keywords),
                                    Call(args=to_compare.args, keywords=to_compare.keywords))
        return True





class keyword(ast.keyword, Node):
    def __init__(self, arg, value, binding_id=None):
        super().__init__(arg=arg, value=value)
        Node.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        if not isinstance(to_compare, keyword):
            raise TypeError
        if not isinstance(to_compare, keyword):
            return False
        if '_KEY_' in self.arg:
            return Node.compare(self, keyword(arg='_KEY_', value=to_compare.value))
        else:
            return Node.compare(self, to_compare)

class generic_keyword(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)


    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not (isinstance(to_compare, Node)):
            raise TypeError
        if not (isinstance(to_compare, keyword)):
            program_memory = backup_memory
            return False
        if program_memory:
            for e in program_memory:
                if to_compare.id == e:
                    program_memory.get(e).append(self.binding_id)
                    break
            else:
                program_memory[to_compare.id] = [self.binding_id]
        else:
            program_memory[to_compare.id] = [self.binding_id]
        return True


class IfExp(ast.IfExp, Node):
    def __init__(self, test, body, orelse, binding_id=None):
        super().__init__(test=test, body=body, orelse=orelse)
        Node.__init__(self, binding_id=binding_id)


class GenericIfExp(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, IfExp)):
            program_memory = backup_memory
            return False
        return True





class Attribute(ast.Attribute, Node):
    def __init__(self, value, attr, ctx, binding_id=None):
        super().__init__(value=value, attr=attr, ctx=ctx)
        Node.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        if not isinstance(to_compare, Node):
            raise TypeError
        if not isinstance(to_compare, Attribute):
            if isinstance(self.value, GenericName):
                if isinstance(to_compare, Name):
                    return self.attr == to_compare.id
                elif isinstance(to_compare, Call):
                    return Node.compare(self, to_compare.func)
                elif isinstance(to_compare, Subscript):
                    return Node.compare(self, to_compare.value)
            else:
                return False
        return Node.compare(self, to_compare)

class GenericAttribute(GenericNode):
    def __init__(self, attr, value,  multi=False, binding_id=None):
        self.attr = attr
        self.value = value
        super().__init__(multi=multi, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if '_MULTI_' in self.attr:
            if not(isinstance(to_compare, (Attribute, Call, Subscript, Name))):
                program_memory = backup_memory
                return False
            if isinstance(self.value, GenericNode):
                result1 = self.value.compare(to_compare)
                result2 = self.value.compare(to_compare.value)
            else:
                result1 = Node.compare(self.value, to_compare)
                result2 = Node.compare(self.value, to_compare.value)
            if result1 or result2:
                return True
            else:
                if 'value' in dir(to_compare):
                    return self.compare(to_compare.value)
                else:
                    return self.compare(to_compare.func)
        else:
            if not isinstance(to_compare, Attribute):
                return False
            if isinstance(self.value, GenericNode):
                return self.value.compare(to_compare.value)
            else:
                return Node.compare(self.value, to_compare.value)
        if '_MULTI_' not in self.attr:
            if program_memory:
                for e in program_memory:
                    if to_compare.attr == e:
                        program_memory.get(e).append(self.binding_id)
                        break
                else:
                    program_memory[to_compare.attr] = [self.binding_id]
            else:
                program_memory[to_compare.attr] = [self.binding_id]






class Subscript(ast.Subscript, Node):
    def __init__(self, value, slice, ctx, binding_id=None):
        super().__init__(value=value, slice=slice, ctx=ctx)
        Node.__init__(self)


class GenericSubscript(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Subscript)):
            program_memory = backup_memory
            return False
        return True





class Index(ast.Index, Node):
    def __init__(self, value, binding_id=None):
        super().__init__(value=value)
        Node.__init__(self, binding_id=binding_id)


class GenericIndex(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Index)):
            program_memory = backup_memory
            return False
        return True





class Slice(ast.Slice, Node):
    def __init__(self, lower, upper, step, binding_id=None):
        super().__init__(lower=lower, upper=upper, step=step)
        Node.__init__(self, binding_id=binding_id)


class GenericSlice(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Slice)):
            program_memory = backup_memory
            return False
        return True





class ExtSlice(ast.ExtSlice, Node):
    def __init__(self, dims, binding_id=None):
        super().__init__(dims=dims)
        Node.__init__(self, binding_id=binding_id)


class GenericExtSlice(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, ExtSlice)):
            program_memory = backup_memory
            return False
        return True





class ListComp(ast.ListComp, Node):
    def __init__(self, elt, generators, binding_id=None):
        super().__init__(elt=elt, generators=generators)
        Node.__init__(self, binding_id=binding_id)


class GenericListComp(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, ListComp)):
            program_memory = backup_memory
            return False
        return True





class SetComp(ast.SetComp, Node):
    def __init__(self, elt, generators, binding_id=None):
        super().__init__(elt=elt, generators=generators)
        Node.__init__(self, binding_id=binding_id)


class GenericSetComp(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, SetComp)):
            program_memory = backup_memory
            return False
        return True





class GeneratorExp(ast.GeneratorExp, Node):
    def __init__(self, elt, generators, binding_id=None):
        super().__init__(elt=elt, generators=generators)
        Node.__init__(self, binding_id=binding_id)


class GenericGeneratorExp(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, GeneratorExp)):
            program_memory = backup_memory
            return False
        return True





class DictComp(ast.DictComp, Node):
    def __init__(self, key, value, generators, binding_id=None):
        super().__init__(key=key, value=value, generators=generators)
        Node.__init__(self, binding_id=binding_id)


class GenericDictComp(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, DictComp)):
            program_memory = backup_memory
            return False
        return True





class comprehension(ast.comprehension, Node):
    def __init__(self, target, iter, ifs, is_async, binding_id=None):
        super().__init__(target=target, iter=iter, ifs=ifs, is_async=is_async)
        Node.__init__(self, binding_id=binding_id)


class generic_comprehension(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, comprehension)):
            program_memory = backup_memory
            return False
        return True





class Assign(ast.Assign, Node):
    def __init__(self, targets, value, binding_id=None):
        super().__init__(targets=targets, value=value)
        Node.__init__(self, binding_id=binding_id)


class GenericAssign(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Assign)):
            program_memory = backup_memory
            return False
        return True





class AnnAssign(ast.AnnAssign, Node):
    def __init__(self, target, annotation, simple, value=None, binding_id=None):
        super().__init__(target=target, annotation=annotation,
                         value=value, simple=simple)
        Node.__init__(self, binding_id=binding_id)


class GenericAnnAssign(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, AnnAssign)):
            program_memory = backup_memory
            return False
        return True





class AugAssign(ast.AugAssign, Node):
    def __init__(self, target, op, value, binding_id=None):
        super().__init__(target=target, op=op, value=value)
        Node.__init__(self, binding_id=binding_id)


class GenericAugAssign(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, AugAssign)):
            program_memory = backup_memory
            return False
        return True





class Raise(ast.Raise, Node):
    def __init__(self, exc=None, cause=None, binding_id=None):
        super().__init__(exc=exc, cause=cause)
        Node.__init__(self, binding_id=binding_id)


class GenericRaise(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Raise)):
            program_memory = backup_memory
            return False
        return True





class Assert(ast.Assert, Node):
    def __init__(self, test, msg, binding_id=None):
        super().__init__(test=test, msg=msg)
        Node.__init__(self, binding_id=binding_id)


class GenericAssert(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Assert)):
            program_memory = backup_memory
            return False
        return True





class Delete(ast.Delete, Node):
    def __init__(self, targets, binding_id=None):
        super().__init__(targets=targets)
        Node.__init__(self, binding_id=binding_id)


class GenericDelete(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Delete)):
            program_memory = backup_memory
            return False
        return True





class Pass(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Pass):
            program_memory = backup_memory
            return False
        return True


class Import(ast.Import, Node):
    def __init__(self, names, binding_id=None):
        super().__init__(names=names)
        Node.__init__(self, binding_id=binding_id)


class GenericImport(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Import)):
            program_memory = backup_memory
            return False
        return True





class ImportFrom(ast.ImportFrom, Node):
    def __init__(self, module, names, level, binding_id=None):
        super().__init__(module=module, names=names, level=level)
        Node.__init__(self, binding_id=binding_id)


class GenericImportFrom(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, ImportFrom)):
            program_memory = backup_memory
            return False
        return True





class alias(ast.alias, Node):
    def __init__(self, name, asname, binding_id=None):
        super().__init__(name=name, asname=asname)
        Node.__init__(self, binding_id=binding_id)


class generic_alias(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, alias)):
            program_memory = backup_memory
            return False
        return True



class If(ast.If, Node):
    def __init__(self, test, body, orelse, binding_id=None):
        super().__init__(test=test, body=body, orelse=orelse)
        Node.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        if not  isinstance(to_compare, Node):
            raise TypeError
        if not isinstance(to_compare, If):
            return False
        if not isinstance(self.test, BoolOp):
            if isinstance(to_compare.test, BoolOp):
                for val in to_compare.test.values:
                    result = self.test.compare(val)
                    if result:
                        return Node.compare(If(test="OK", body=self.body, orelse=self.orelse),
                                            If(test="OK", body=to_compare.body, orelse=to_compare.orelse))
                return False
        else:
            return Node.compare(self, to_compare)

class GenericIf(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, If)):
            program_memory = backup_memory
            return False
        return True



class For(ast.For, Node):
    def __init__(self, target, iter, body, orelse, binding_id=None):
        super().__init__(target=target, iter=iter, body=body, orelse=orelse)
        Node.__init__(self, binding_id=binding_id)


class GenericFor(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, For)):
            program_memory = backup_memory
            return False
        return True


class While(ast.While, Node):
    def __init__(self, test, body, orelse, binding_id=None):
        super().__init__(test=test, body=body, orelse=orelse)
        Node.__init__(self, binding_id=binding_id)


class GenericWhile(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, While)):
            program_memory = backup_memory
            return False
        return True


class Break(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Break):
            program_memory = backup_memory
            return False
        return True


class Continue(EmptyClass):
    def __init__(self, binding_id=None):
        EmptyClass.__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Continue):
            program_memory = backup_memory
            return False
        return True


class Try(ast.Try, Node):
    def __init__(self, body, handlers, orelse, finalbody, binding_id=None):
        super().__init__(body=body, handlers=handlers, orelse=orelse,
                         finalbody=finalbody)
        Node.__init__(self, binding_id=binding_id)


class GenericTry(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Try)):
            program_memory = backup_memory
            return False
        return True


class ExceptHandler(ast.ExceptHandler, Node):
    def __init__(self, type, name, body, binding_id=None):
        super().__init__(name=name, type=type, body=body)
        Node.__init__(self, binding_id=binding_id)


class GenericExceptHandler(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, ExceptHandler)):
            program_memory = backup_memory
            return False
        return True


class With(ast.With, Node):
    def __init__(self, items, body, binding_id=None):
        super().__init__(items=items, body=body)
        Node.__init__(self, binding_id=binding_id)


class GenericWith(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, With)):
            program_memory = backup_memory
            return False
        return True


class withitem(ast.withitem, Node):
    def __init__(self, context_expr, optional_vars, binding_id=None):
        super().__init__(context_expr=context_expr, optional_vars=optional_vars)
        Node.__init__(self, binding_id=binding_id)


class generic_withitem(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, withitem)):
            program_memory = backup_memory
            return False
        return True


class FunctionDef(ast.FunctionDef, Node):
    def __init__(self, name, args, decorator_list=None, returns=None, body=None, binding_id=None):
        super().__init__(name=name, args=args, body=body,
                         decorator_list=decorator_list, returns=returns)
        Node.__init__(self, binding_id=binding_id)



class GenericFunctionDef(GenericNode):
    def __init__(self, name=None, multi=False, body=None, fun_node=None, args=None, binding_id=None):
        self.args = args
        self.body = body
        self.fun_node = fun_node
        self.name = name
        super().__init__(multi=multi, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if program_memory:
            for e in program_memory:
                if to_compare.name == e:
                    program_memory.get(e).append(self.binding_id)
                    break
            else:
                program_memory[to_compare.name] = [self.binding_id]
        else:
            program_memory[to_compare.name] = [self.binding_id]
        if self.args.args:
            return Node.compare(FunctionDef(name=None, args=self.args), FunctionDef(name=None, args=to_compare.args))
        else:
            if not(isinstance(to_compare, FunctionDef)):
                program_memory = backup_memory
                return False
            return True


class ClassDef(ast.ClassDef, Node):
    def __init__(self, bases, name=None, keywords=None, body=None, decorator_list=None,
                 starargs=None, kwargs=None, binding_id=None):
        super().__init__(name=name, bases=bases, keywords=keywords,
                         starargs=starargs, kwargs=kwargs, body=body,
                         decorator_list=decorator_list)
        Node.__init__(self, binding_id=binding_id)


class GenericClassDef(GenericNode):
    def __init__(self, name=None, bases=None, multi=False, body=None, binding_id=None):
        self.body = body
        self.bases = bases
        self.name = name
        super().__init__(multi=multi, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if program_memory:
            for e in program_memory:
                if to_compare.name == e:
                    program_memory.get(e).append(self.binding_id)
                    break
            else:
                program_memory[to_compare.name] = [self.binding_id]
        else:
            program_memory[to_compare.name] = [self.binding_id]
        if self.bases:
            return Node.compare(ClassDef(name=None, bases=self.bases), ClassDef(name=None, bases=to_compare.bases))
        else:
            if not(isinstance(to_compare, ClassDef)):
                program_memory = backup_memory
                return False
            return True



class Lambda(ast.Lambda, Node):
    def __init__(self, args, body, binding_id=None):
        super().__init__(args=args, body=body)
        Node.__init__(self, binding_id=binding_id)


class GenericLambda(GenericNode):
    def __init__(self, multi=False, binding_id=None):
        super().__init__(multi=multi, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Lambda)):
            program_memory = backup_memory
            return False
        return True


class arguments(ast.arguments, Node):
    def __init__(self, args, kwonlyargs, kwarg, defaults, kw_defaults,
                 vararg=None, binding_id=None):
        super().__init__(args=args, kwonlyargs=kwonlyargs, kwarg=kwarg,
                         defaults=defaults, kw_defaults=kw_defaults,
                         vararg=vararg)
        Node.__init__(self, binding_id=binding_id)


class generic_arguments(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, arguments)):
            program_memory = backup_memory
            return False
        return True


class arg(ast.arg, Node):
    def __init__(self, arg, annotation, binding_id=None):
        super().__init__(arg=arg, annotation=annotation)
        Node.__init__(self, binding_id=binding_id)


class generic_arg(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, arg)):
            program_memory = backup_memory
            return False
        return True


class Return(ast.Return, Node):
    def __init__(self, value, binding_id=None):
        super().__init__(value=value)
        Node.__init__(self, binding_id=binding_id)


class GenericReturn(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Return)):
            program_memory = backup_memory
            return False
        return True


class Yield(ast.Yield, Node):
    def __init__(self, value, binding_id=None):
        super().__init__(value=value)
        Node.__init__(self, binding_id=binding_id)


class GenericYield(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Yield)):
            program_memory = backup_memory
            return False
        return True


class YieldFrom(ast.YieldFrom, Node):
    def __init__(self, value, binding_id=None):
        super().__init__(value=value)
        Node.__init__(self, binding_id=binding_id)


class GenericYieldFrom(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, YieldFrom)):
            program_memory = backup_memory
            return False
        return True


class Global(ast.Global, Node):
    def __init__(self, names, binding_id=None):
        super().__init__(names=names)
        Node.__init__(self, binding_id=binding_id)


class GenericGlobal(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Global)):
            program_memory = backup_memory
            return False
        return True


class Nonlocal(ast.Nonlocal, Node):
    def __init__(self, names, binding_id=None):
        super().__init__(names=names)
        Node.__init__(self, binding_id=binding_id)


class GenericNonlocal(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Nonlocal)):
            program_memory = backup_memory
            return False
        return True

class AsyncFunctionDef(ast.AsyncFunctionDef, Node):
    def __init__(self, args, body, decorator_list, returns, binding_id=None):
        super().__init__(args=args, body=body,
                         decorator_list=decorator_list, returns=returns)
        Node.__init__(self, binding_id=binding_id)


class GenericAsyncFunctionDef(GenericNode):
    def __init__(self, binding_id=None, name=None):
        self.name = name
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, AsyncFunctionDef)):
            program_memory = backup_memory
            return False
        return True


class Await(ast.Await, Node):
    def __init__(self, value, binding_id=None):
        super().__init__(value=value)
        Node.__init__(self, binding_id=binding_id)


class GenericAwait(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, Await)):
            program_memory = backup_memory
            return False
        return True


class AsyncFor(ast.AsyncFor, Node):
    def __init__(self, target, iter, body, orelse, binding_id=None):
        super().__init__(target=target, iter=iter, body=body,
                         orelse=orelse)
        Node.__init__(self, binding_id=binding_id)


class GenericAsyncFor(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, AsyncFor)):
            program_memory = backup_memory
            return False
        return True


class AsyncWith(ast.AsyncWith, Node):
    def __init__(self, items, body, binding_id=None):
        super().__init__(items=items, body=body)
        Node.__init__(self, binding_id=binding_id)


class GenericAsyncWith(GenericNode):
    def __init__(self, binding_id=None):
        super().__init__(self, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not(isinstance(to_compare, Node)):
            raise TypeError
        if not(isinstance(to_compare, AsyncWith)):
            program_memory = backup_memory
            return False
        return True


class Module(ast.Module, Node):
    def __init__(self, body, binding_id=None):
        super().__init__(body=body)
        Node.__init__(self, binding_id=binding_id)

# ############################################################## #
# ############################################################## #
# ############################################################## #
# ############################################################## #
# ############################################################## #
# ############################################################## #
# ############################################################## #
# ############################################################## #
# ############################################################## #

class State():

    def __init__(self, node=None, multi=None):
        self.name = None
        self.node = node
        self.next = None
        self.multi = multi

    @abstractmethod
    def run(self, program_piece, father):
        pass

    def attach(self, state):
        last = self.next

        if last:
            while True:
                if last.next is None:
                    break
                last = last.next
            last.next = state
        else:
            self.next = state
        return self.next


    def node_class(self):
        return self.node.__class__


class GenericState(State):
    def __init__(self, multi=None):
        super().__init__(multi=multi)


class ModuleState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Module):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                return self.next.run(program_piece=program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False


class AsyncFunctionDefState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, AsyncFunctionDef) or not self.node.compare(program_piece, memory=memory):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece=program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False


class GenericAsyncFunctionDefState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, AsyncFunctionDef):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False

    def node_class(self):
        return AsyncFunctionDef


class FunctionDefState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, FunctionDef) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            for n in father:
                n.next = None
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False


class GenericFunctionDefState(GenericState):
    def __init__(self, multi=None, node=None):
        super().__init__(multi=multi)
        self.node = node

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if self.node:
            backup_memory = copy.deepcopy(program_memory)
            if not isinstance(program_piece, FunctionDef) or not self.node.compare(program_piece):
                program_memory = backup_memory
                return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            for n in father:
                n.next = None
        else:
            if not isinstance(program_piece, FunctionDef):
                program_memory = backup_memory
                return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False

    def node_class(self):
        return FunctionDef


class ClassDefState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, ClassDef) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            for n in father:
                n.next = None
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False


class GenericClassDefState(GenericState):
    def __init__(self, node=None):
        super().__init__(self)
        self.node = node

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, ClassDef) or not self.node.compare(program_piece, memory=program_memory):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False

    def node_class(self):
        return ClassDef


class IfState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, If) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            program_piece.orelse = None
            for n in father:
                n.next = None
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False


class GenericIfState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, If) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            program_piece.orelse = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False

    def node_class(self):
        return If


class WhileState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, While) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            program_piece.orelse = None
            for n in father:
                n.next = None
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False


class GenericWhileState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, While):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.orelse = None
            program_piece.body = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False

    def node_class(self):
        return While


class ForState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, For) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            program_piece.orelse = None
            for n in father:
                n.next = None
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False


class GenericForState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, For):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.orelse = None
            program_piece.body = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False

    def node_class(self):
        return For


class AsyncForState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, AsyncFor) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            program_piece.orelse = None
            for n in father:
                n.next = None
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False


class GenericAsyncForState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, AsyncFor):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            program_piece.orelse = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False

    def node_class(self):
        return AsyncFor


class TryState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Try) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            program_piece.orelse = None
            program_piece.handlers = None
            program_piece.finalbody = None
            for n in father:
                n.next = None
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False


class GenericTryState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Try):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            program_piece.orelse = None
            program_piece.handlers = None
            program_piece.finalbody = None
            for n in father:
                n.next = None
                program_piece.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False

    def node_class(self):
        return Try


class WithState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, With) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            for n in father:
                n.next = None
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False


class GenericWithState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, While):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False

    def node_class(self):
        return With


class LambdaState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Lambda) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False


class GenericLambdaState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Lambda):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False

    def node_class(self):
        return Lambda


class AsyncWithState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, AsyncWith) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            for n in father:
                n.next = None
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False


class GenericAsyncWithState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, AsyncWith):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            program_piece.body = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False

    def node_class(self):
        return AsyncWith


class ReturnState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Return) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False


class GenericReturnState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Return):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Return


class YieldState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Yield) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False


class GenericYieldState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Yield):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Yield


class YieldFromState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, YieldFrom) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False



class GenericYieldFromState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, YieldFrom):
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return YieldFrom


class GenericStatementState(GenericState):
    def __init__(self, multi=False):
        self.multi = multi
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Node):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if 'body' in dir(program_piece):
                father.append(program_piece)
                if self.multi:
                    result = self.next.run(program_piece.body, father=father, memory=memory)
                    if result:
                        return True
                    else:
                        return self.run(program_piece.body, father=father, memory=memory)
                return self.next.run(program_piece.next, father=father, memory=memory)
            elif program_piece.next:
                if self.multi:
                    result = self.next.run(program_piece.next, father=father, memory=memory)
                    if result:
                        return True
                    else:
                        return self.run(program_piece.next, father=father, memory=memory)
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father) - 1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            if self.multi:
                                result = self.next.run(father[i], father=father, memory=memory)
                                if result:
                                   return True
                                else:
                                    return self.run(father[i], father=father, memory=memory)
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            if self.multi:
                                result = self.next.run(father[i], father=father, memory=memory)
                                if result:
                                    return True
                                else:
                                    return self.run(father[i], father=father, memory=memory)
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            if self.multi:
                                result = self.next.run(father[i], father=father, memory=memory)
                                if result:
                                    return True
                                else:
                                    return self.run(father[i], father=father, memory=memory)
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        if self.multi:
                            result = self.next.run(to_run, father=father, memory=memory)
                            if result:
                                return True
                            else:
                                if not isinstance(to_run, (FunctionDef, ClassDef)):
                                    return self.run(to_run, father=father, memory=memory)
                                else:
                                    return False
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Node


class AssignState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Assign) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False


class GenericAssignState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Assign):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Assign


class DeleteState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Delete) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False


class GenericDeleteState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Delete):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Delete


class AnnAssignState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, AnnAssign) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False



class GenericAnnAssignState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, AnnAssign):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return AnnAssign


class AugAssignState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, AugAssign) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False


class GenericAugAssignState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, AugAssign):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return AugAssign


class RaiseState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Raise) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False


class GenericRaiseState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Raise):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Raise


class AssertState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Assert) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False


class GenericAssertState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Assert):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Assert


class ImportState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Import) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False


class GenericImportState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Import):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Import


class ImportFromState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, ImportFrom) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False


class GenericImportFromState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, ImportFrom):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return ImportFrom


class GlobalState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Global) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False


class GenericGlobalState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Global):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Global


class NonLocalState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Nonlocal) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False


class GenericNonLocalState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Nonlocal):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Nonlocal


class AwaitState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Await) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False


class GenericAwaitState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Await):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Await


class ExceptHandlerState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, ExceptHandler) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.body:
                father.append(program_piece)
                return self.next.run(program_piece.body, father=father, memory=memory)
            program_memory = backup_memory
            return False



class GenericExceptHanlderState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, ExceptHandler):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return ExceptHandler


class ExprState(State):
    def __init__(self, node):
        super().__init__(node=node)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Expr) or not self.node.compare(program_piece):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False


class GenericExprState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Expr):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Expr


class GenericStatement(GenericNode):
    def __init__(self=None, multi=None, binding_id=None):
        super().__init__(multi=multi, binding_id=binding_id)

    def compare(self, to_compare):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(to_compare, Node):
            program_memory = backup_memory
            return False
        return True


class PassState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Pass):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Pass


class BreakState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Break):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Break


class OrelseState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not program_piece.orelse:
            program_memory = backup_memory
            return False
        return self.next.run(program_piece.orelse, father=father, memory=memory)


class HandlerState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not program_piece.handlers:
            program_memory = backup_memory
            return False
        return self.next.run(program_piece.handlers, father=father, memory=memory)


class FinalBodyState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not program_piece.finalbody:
            program_memory = backup_memory
            return False
        return self.next.run(program_piece.finalbody, father=father)


class EllipsisState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Ellipsis):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Ellipsis

class ContinueState(GenericState):
    def __init__(self):
        super().__init__(self)

    def run(self, program_piece, father, memory):
        global program_memory
        backup_memory = copy.deepcopy(program_memory)
        if not isinstance(program_piece, Continue):
            program_memory = backup_memory
            return False
        if self.next is None:
            program_piece.next = None
            for n in father:
                n.next = None
            return True
        else:
            if program_piece.next:
                return self.next.run(program_piece.next, father=father, memory=memory)
            else:
                for i in range(len(father)-1, -1, -1):
                    if isinstance(self.next, OrelseState):
                        if father[i].orelse:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, HandlerState):
                        if father[i].handlers:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif isinstance(self.next, FinalBodyState):
                        if father[i].finalbody:
                            return self.next.run(father[i], father=father, memory=memory)
                    elif father[i].next:
                        to_run = father[i].next
                        father.remove(father[i])
                        return self.next.run(to_run, father=father, memory=memory)
                program_memory = backup_memory
                return False

    def node_class(self):
        return Continue

class Fsa:
    def __init__(self, pattern_program):
        global program_memory
        if isinstance(pattern_program, tuple):
            body = pattern_program[0].body
        else:
            body = pattern_program.body
        self.is_if = True if isinstance(body, If) else False
        self.is_for = True if isinstance(body, For) else False
        self.is_while = True if isinstance(body, While) else False
        self.is_try = True if isinstance(body, Try) else False
        self.count_else = 0
        self.count_handlers = 0
        self.has_finalbody = False
        if isinstance(body, (If,
                                        For,
                                        While,
                                        Try)):
            if body.orelse:
                to_iterate = body.orelse
                while to_iterate is not None:
                    self.count_else += 1
                    to_iterate = to_iterate.next
            if isinstance(body, Try):
                if body.handlers:
                    to_iterate = body.handlers
                    while to_iterate is not None:
                        self.count_handlers += 1
                        to_iterate = to_iterate.next
                if body.finalbody:
                    self.has_finalbody = True
        self.initial, self.memory_pattern = self.create_fsa(pattern_program)
        state_index = 0
        node = self.initial
        program_memory = {}
        while node:
            node.name = "q_" + str(state_index)
            state_index += 1
            node = node.next

    def run(self, program):
        global program_memory
        temp_program = program.__deepcopy__()
        first_result = self.initial.run(temp_program, father=[temp_program], memory=program_memory)
        result_nodes = []
        if first_result:
            ok = True
            exit_ = False
            for el in self.memory_pattern.values():
                for le in program_memory.values():
                    if set(el) == set(le):
                        break
                else:
                    ok = False
                if not ok:
                    break
            if ok and not isinstance(program, Module):
                result_nodes.append(program)
        go_on = True
        father = [program]
        v = father[0].body
        to_visit=[]
        while v is not None:
            temp_v = v.__deepcopy__()
            to_visit.append(temp_v)
            v = v.next
        while True:
            backup=[]
            for x in to_visit:
                backup.append(x.__deepcopy__())
                program_memory = {}
                first_result = self.initial.run(Module(body=x), father=[Module(body=x)],
                                                memory=program_memory)
                if first_result :
                    ok = True
                    exit_ = False
                    for el in self.memory_pattern.values():
                        for le in program_memory.values():
                            if set(el) == set(le):
                                break
                        else:
                            ok = False
                        if not ok:
                            break
                    if ok:
                        result_nodes.append(x)
            temp=[]
            for x in backup:
                if 'body' in dir(x):
                    b = x.body
                    while b is not None:
                        temp_b = b.__deepcopy__()
                        temp.append(temp_b)
                        b = b.next
                if 'orelse' in dir(x):
                    o = x.orelse
                    while o is not None:
                        temp_o = o.__deepcopy__()
                        temp.append(temp_o)
                        o = o.next
                if 'finalbody' in dir(x):
                    f = x.finalbody
                    while f is not None:
                        temp_f = f.__deepcopy__()
                        temp.append(temp_f)
                        f = f.next
                if 'handlers' in dir(x):
                    handlers_list = []
                    h = x.handlers
                    while h is not None:
                        handlers_list.append(h)
                        h = h.next
                    for j in handlers_list:
                        k = j
                        while k is not None:
                            temp_k = k.__deepcopy__()
                            temp.append(temp_k)
                            k = k.next
            if not temp:
                break
            to_visit = temp
        return result_nodes

    def create_fsa(self, node):

        global state_index
        state_index = 0

        node_body = None
        node_orelse = None
        node_handler = None
        node_finalbody = None

        if isinstance(node, tuple):
            node, memory_pattern = node

        if isinstance(node, Module) or isinstance(node, ClassDef) or isinstance(node, FunctionDef) \
             or isinstance(node, If) or isinstance(node, For) or isinstance(node, While) \
             or isinstance(node, Try) or isinstance(node, ExceptHandler) or isinstance(node, With) or isinstance(node, AsyncFunctionDef)\
                or isinstance(node, AsyncWith) or isinstance(node, GenericClassDef) or isinstance(node, GenericFunctionDef):
            if node.body:
                to_attach = self.create_fsa(node.body)
                if node.body.next:
                    node_body = node.body.next
                    state_body = to_attach.attach(self.create_fsa(node_body))
                    while node_body.next:
                        state_body = state_body.attach(self.create_fsa(node_body.next))
                        node_body = node_body.next
                else:
                    state_body = to_attach
            else:
                state_body = None
            if isinstance(node, Module):
                to_return = ModuleState(node=node)
                state_index += 1
                to_return.attach(to_attach)
                return to_return, memory_pattern
            elif isinstance(node, ClassDef):
                to_return = ClassDefState(node=node)
                state_index += 1
                to_return.attach(to_attach)
                return to_return
            elif isinstance(node, GenericClassDef):
                to_return = GenericClassDefState(node=node)
                state_index += 1
                to_return.attach(to_attach)
                return to_return
            elif isinstance(node, FunctionDef):
                to_return = FunctionDefState(node=node)
                state_index += 1
                to_return.attach(to_attach)
                return to_return
            elif isinstance(node, GenericFunctionDef):
                to_return = GenericFunctionDefState(node=node)
                state_index += 1
                to_return.attach(to_attach)
                return to_return
            elif isinstance(node, AsyncFunctionDefState):
                to_return = AsyncFunctionDefState(node=node)
                state_index += 1
                to_return.attach(to_attach)
                return to_return
            elif isinstance(node, With):
                to_return = WithState(node=node)
                state_index += 1
                to_return.attach(to_attach)
                return to_return
            elif isinstance(node, AsyncWith):
                to_return = AsyncWithState(node=node)
                state_index += 1
                to_return.attach(to_attach)
                return to_return
            elif isinstance(node, If) or isinstance(node, For) or isinstance(node, While) or isinstance(node, AsyncFor):
                if node.orelse:
                    node_orelse = node.orelse
                    state_orelse = state_body.attach(OrelseState())
                    state_orelse = state_orelse.attach(self.create_fsa(node_orelse))
                    state_index += 1
                    while node_orelse.next:
                        state_orelse = state_orelse.attach(self.create_fsa(node_orelse.next))
                        node_orelse = node_orelse.next
                else:
                    state_orelse = state_body
                if isinstance(node, If):
                    to_return = IfState(node=node)
                    state_index += 1
                    to_return.attach(to_attach)
                    return to_return
                elif isinstance(node, While):
                    to_return = WhileState(node=node)
                    state_index += 1
                    to_return.attach(to_attach)
                    return to_return
                elif isinstance(node, For):
                    to_return = ForState(node=node)
                    state_index += 1
                    to_return.attach(to_attach)
                    return to_return
                else:
                    to_return = AsyncForState(node=node)
                    state_index += 1
                    to_return.attach(to_attach)
                    return to_return
            elif isinstance(node, Try):
                if node.handlers:
                    node_handler = node.handlers
                    state_handler = state_body.attach(HandlerState())
                    state_handler = state_handler.attach(self.create_fsa(node_handler))
                    while node_handler.next:
                        state_handler = state_handler.attach(self.create_fsa(node_handler.next))
                        node_handler = node_handler.next
                else:
                    state_handler = state_body
                if node.orelse:
                    node_orelse = node.orelse
                    if node_handler:
                        state_orelse = state_handler.attach(OrelseState())
                        state_orelse = state_orelse.attach(self.create_fsa(node_orelse))
                    else:
                        state_orelse = state_body.attach(OrelseState())
                        state_orelse = state_orelse.attach(self.create_fsa(node_orelse))
                    while node_orelse.next:
                        state_orelse = state_orelse.attach(self.create_fsa(node_orelse.next))
                        node_orelse = node_orelse.next
                else:
                    if state_handler:
                        state_orelse = state_handler
                    else:
                        state_orelse = state_body
                if node.finalbody:
                    node_finalbody = node.finalbody
                    if state_orelse:
                        state_finalbody = state_orelse.attach(FinalBodyState())
                        state_finalbody = state_finalbody.attach(self.create_fsa(node_finalbody))
                    else:
                        if state_handler:
                            state_finalbody = state_handler.attach(FinalBodyState())
                            state_finalbody = state_finalbody.attach(self.create_fsa(node_finalbody))
                        else:
                            state_finalbody = state_body.attach(FinalBodyState())
                            state_finalbody = state_finalbody.attach(self.create_fsa(node_finalbody))
                    while node_finalbody.next:
                        state_finalbody = state_finalbody.attach(self.create_fsa(node_finalbody.next))
                        node_finalbody = node_finalbody.next
                to_return = TryState(node=node)
                state_index += 1
                to_return.attach(to_attach)
                return to_return
            elif isinstance(node, ExceptHandler):
                to_return = ExceptHandlerState(node=node)
                state_index += 1
                to_return.attach(to_attach)
                return to_return
        elif isinstance(node, Return):
            to_return = ReturnState(node=node)
            state_index += 1
            return to_return
        elif isinstance(node, Yield):
            to_return = YieldState(node=node)
            state_index += 1
            return to_return
        elif isinstance(node, YieldFrom):
            to_return = YieldFromState(node=node)
            state_index += 1
            return to_return
        elif isinstance(node, Expr):
            to_return = ExprState(node=node)
            state_index += 1
            return to_return
        elif isinstance(node, Assign):
            to_return = AssignState(node=node)
            state_index += 1
            return to_return
        elif isinstance(node, AnnAssign):
            to_return = AnnAssignState(node=node)
            state_index += 1
            return to_return
        elif isinstance(node, AugAssign):
            to_return = AugAssignState(node=node)
            state_index += 1
            return to_return
        elif isinstance(node, Delete):
            to_return = DeleteState(node=node)
            state_index += 1
            return to_return
        elif isinstance(node, Raise):
            to_return = RaiseState(node=node)
            state_index += 1
            return to_return
        elif isinstance(node, Assert):
            to_return = AssertState(node=node)
            state_index += 1
            return to_return
        elif isinstance(node, Import):
            to_return = ImportState(node=node)
            state_index += 1
            return to_return
        elif isinstance(node, ImportFrom):
            to_return = ImportFromState(node=node)
            state_index += 1
            return to_return
        elif isinstance(node, Nonlocal):
            to_return = NonLocalState(node=node)
            state_index += 1
            return to_return
        elif isinstance(node, Pass):
            to_return = PassState()
            state_index += 1
            return to_return
        elif isinstance(node, Break):
            to_return = BreakState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericAsyncFunctionDef):
            to_return = GenericAsyncFunctionDefState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericAnnAssign):
            to_return = GenericAnnAssignState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericAssert):
            to_return = GenericAssertState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericAssign):
            to_return = GenericAssignState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericAsyncWith):
            to_return = GenericAsyncWithState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericAsyncFor):
            to_return = GenericAsyncForState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericAugAssign):
            to_return = GenericAugAssignState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericDelete):
            to_return = GenericDeleteState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericExceptHandler):
            to_return = GenericExceptHanlderState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericExpr):
            to_return = GenericExprState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericFor):
            to_return = GenericForState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericGlobal):
            to_return = GenericGlobalState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericIf):
            to_return = GenericIfState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericImport):
            to_return = GenericImportState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericImportFrom):
            to_return = GenericImportFromState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericNonlocal):
            to_return = GenericNonLocalState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericRaise):
            to_return = GenericRaiseState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericReturn):
            to_return = GenericReturnState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericStatement):
            to_return = GenericStatementState(multi = node.multi)
            state_index += 1
            return to_return
        elif isinstance(node, GenericTry):
            to_return = GenericTryState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericWhile):
            to_return = GenericWhileState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericWith):
            to_return = GenericWithState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericYield):
            to_return = GenericYieldState()
            state_index += 1
            return to_return
        elif isinstance(node, GenericYieldFrom):
            to_return = GenericYieldFromState()
            state_index += 1
            return to_return
        elif isinstance(node, Ellipsis):
            to_return = EllipsisState()
            state_index += 1
            return to_return
        elif isinstance(node, Continue):
            to_return = ContinueState()
            state_index += 1
            return to_return
        elif isinstance(node, Global):
            to_return = GlobalState(node=node)
            state_index +=1
            return to_return

def print_program(tree, tab=""):
    if isinstance(tree, Module):
        body = tree.body
        while body:
            print("\n")
            print_program(body)
            body = body.next
    elif isinstance(tree, Num):
        print(tree.n, end='')
    elif isinstance(tree, Str):
        print('"'+tree.s+'"', end='')
    elif isinstance(tree, FormattedValue):
        print("{", end='')
        print_program(tree.value)
        print("}", end='')
    elif isinstance(tree, JoinedStr):
        print('f"', end='')
        for v in tree.values:
            print_program(v)
        print('"')
    elif isinstance(tree, Bytes):
        print('b"'+tree.b+ '"', end='')
    elif isinstance(tree, List):
        print("[", end='')
        for el in tree.elts:
            print_program(el)
        print("]", end='')
    elif isinstance(tree, Tuple):
        print("(", end='')
        for el in tree.elts:
            print_program(el)
        print(")", end='')
    elif isinstance(tree, Set):
        print("{", end='')
        for el in tree:
            print_program(el)
        print("}", end='')
    elif isinstance(tree, Dict):
        print("{", end='')
        for key, value in zip(tree.keys, tree.values):
            print_program(key)
            print(":", end='')
            print_program(value)
            print(",", end='')
        print("}", end='')
    elif isinstance(tree, Ellipsis):
        print("...", end='')
    elif isinstance(tree, NameConstant):
        print(tree.value, end='')
    elif isinstance(tree, Name):
        print(tree.id, end='')
    elif isinstance(tree, Starred):
        print("*", end='')
        print_program(tree.value)
    elif isinstance(tree, Expr):
        print(tab, end='')
        print_program(tree.value)
    elif isinstance(tree, UnaryOp):
        print_program(tree.op)
        print_program(tree.operand)
    elif isinstance(tree, UAdd):
        print("++", end='')
    elif isinstance(tree, USub):
        print("--", end='')
    elif isinstance(tree, Not):
        print("not ", end='')
    elif isinstance(tree, Invert):
        print("~", end='')
    elif isinstance(tree, BinOp):
        print_program(tree.left)
        print_program(tree.op)
        print_program(tree.right)
    elif isinstance(tree, Add):
        print("+", end='')
    elif isinstance(tree, Sub):
        print("-", end='')
    elif isinstance(tree, Mult):
        print("*", end='')
    elif isinstance(tree, Div):
        print("/", end='')
    elif isinstance(tree, FloorDiv):
        print("//", end='')
    elif isinstance(tree, Mod):
        print("%", end='')
    elif isinstance(tree, Pow):
        print("**", end='')
    elif isinstance(tree, LShift):
        print("<<", end='')
    elif isinstance(tree, RShift):
        print(">>", end='')
    elif isinstance(tree, BitOr):
        print("|", end='')
    elif isinstance(tree, BitAnd):
        print("&", end='')
    elif isinstance(tree, BitXor):
        print("^", end='')
    elif isinstance(tree, MatMult):
        print("@", end='')
    elif isinstance(tree, BoolOp):
        for v in tree.values:
            print_program(v)
            print(" ", end='')
            print_program(tree.op)
            print(" ", end='')
    elif isinstance(tree, And):
        print("and", end='')
    elif isinstance(tree, Or):
        print("or", end='')
    elif isinstance(tree, Compare):
        print_program(tree.left)
        print(" ", end='')
        for op, comp in zip(tree.ops, tree.comparators):
            print_program(op)
            print(" ", end='')
            print_program(comp)
            print(" ", end='')
    elif isinstance(tree, Eq):
        print("==", end='')
    elif isinstance(tree, NotEq):
        print("!=", end='')
    elif isinstance(tree, Lt):
        print("<", end='')
    elif isinstance(tree, LtE):
        print("<=", end='')
    elif isinstance(tree, Gt):
        print(">", end='')
    elif isinstance(tree, GtE):
        print(">=", end='')
    elif isinstance(tree, Is):
        print("is", end='')
    elif isinstance(tree, IsNot):
        print("is not", end='')
    elif isinstance(tree, In):
        print("in", end='')
    elif isinstance(tree, NotIn):
        print("not in", end='')
    elif isinstance(tree, Call):
        print(tab, end='')
        print_program(tree.func)
        print("(", end='')
        for arg_ in tree.args:
            print_program(arg_)
            print(", ", end='')
        for keyword_ in tree.keywords:
            print_program(keyword_)
            print(", ", end='')
        print(")", end='')
    elif isinstance(tree, keyword):
        print_program(tree.arg)
        print(" = ", end='')
        print_program(tree.value)
    elif isinstance(tree, IfExp):
        print_program(tree.body)
        print(" if ", end='')
        print_program(tree.test)
        print(" else ", end='')
        print_program(tree.orelse)
    elif isinstance(tree, Attribute):
        print_program(tree.value)
        print(".", end='')
        print_program(tree.attr)
    elif isinstance(tree, Subscript):
        print_program(tree.value)
        print_program(tree.slice)
    elif isinstance(tree, Index):
        print("[", end='')
        print_program(tree.value)
        print("]", end='')
    elif isinstance(tree, Slice):
        print("[", end='')
        print_program(tree.lower)
        print(":", end='')
        print_program(tree.upper)
        print("]", end='')
    elif isinstance(tree, ExtSlice):
        print("[", end='')
        for dim in tree.dims:
            print_program(dim)
            print(", ", end='')
    elif isinstance(tree, ListComp):
        print("[", end='')
        print_program(tree.elt)
        print(" ", end='')
        for gen in tree.generators:
            print_program(gen)
            print(" ", end='')
        print("]", end='')
    elif isinstance(tree, SetComp):
        print("{", end='')
        print_program(tree.elt)
        print(" ", end='')
        for gen in tree.generators:
            print_program(gen)
            print(" ", end='')
        print("}", end='')
    elif isinstance(tree, GeneratorExp):
        print("(", end='')
        print_program(tree.elt)
        print(" ", end='')
        for gen in tree.generators:
            print_program(gen)
            print(" ", end='')
        print(")", end='')
    elif isinstance(tree, DictComp):
        print("{", end='')
        print_program(tree.key)
        print(":", end='')
        print_program(tree.value)
        print(" ", end='')
        for gen in tree.generators:
            print_program(gen)
            print(" ", end='')
        print("}", end='')
    elif isinstance(tree, comprehension):
        print("for ", end='')
        print_program(tree.target)
        print(" in ", end='')
        print_program(tree.iter)
        for i in tree.ifs:
            print(" if ", end='')
            print_program(i)
    elif isinstance(tree, Assign):
        print(tab, end='')
        for targ in tree.targets:
            print_program(targ)
            print("=", end='')
        print("=", end='')
        print_program(tree.value)
    elif isinstance(tree, AnnAssign):
        print(tab, end='')
        print_program(tree.target)
        print("=", end='')
        print_program(tree.value)
    elif isinstance(tree, AugAssign):
        print(tab, end='')
        print_program(tree.target)
        print_program(tree.op)
        print("=", end='')
    elif isinstance(tree, Raise):
        print(tab, end='')
        print("raise ", end='')
        if tree.exc:
            print_program(tree.exc)
        if tree.cause:
            print(" from ", end='')
            print_program(tree.cause)
    elif isinstance(tree, Assert):
        print(tab, end='')
        print("assert ", end='')
        print_program(tree.test)
        print('"', end='')
        print_program(tree.msg)
        print('"', end='')
    elif isinstance(tree, Delete):
        print(tab, end='')
        print("del ", end='')
        for el in tree.targets:
            print_program(el)
            print(", ", end='')
    elif isinstance(tree, Pass):
        print(tab, end='')
        print("pass", end='')
    elif isinstance(tree, Import):
        print("import ", end='')
        for n in tree.names:
            print_program(n)
            print(", ", end='')
    elif isinstance(tree, ImportFrom):
        print("from ", end='')
        for n in tree.names:
            print_program(n)
            print(", ", end='')
    elif isinstance(tree, alias):
        print_program(tree.name)
        print(" as ", end='')
        print_program(tree.asname)
    elif isinstance(tree, If):
        print(tab, end='')
        print("if ", end='')
        print_program(tree.test)
        print(":", end='')
        body = tree.body
        while body:
            print("\n", end='')
            print_program(body, tab=tab+"\t")
            print("\n", end='')
            body = body.next
        if tree.orelse:
            orelse = tree.orelse
            while orelse:
                print("\n", end='')
                print("else ", end='')
                if isinstance(orelse, If):
                    print_program(orelse, tab=tab)
                else:
                    print("\n", end='')
                    print_program(orelse, tab=tab+"\t")
                orelse = orelse.next
                print("\n", end='')
    elif isinstance(tree, For):
        print(tab, end='')
        print("for ", end='')
        print_program(tree.target)
        print(" in ", end='')
        print_program(tree.iter)
        print(":", end='')
        body = tree.body
        while body:
            print("\n", end='')
            print_program(body, tab=tab+"\t")
            print("\n", end='')
            body = body.next
        if tree.orelse:
            print("\n", end='')
            print("else ", end='')
            print_program(tree.orelse, tab=tab + "\t")
            print("\n", end='')
    elif isinstance(tree, While):
        print(tab, end='')
        print("while ", end='')
        print_program(tree.test)
        print(":", end='')
        body = tree.body
        while body:
            print("\n", end='')
            print_program(body, tab=tab+"\t")
            print("\n", end='')
            body = body.next
        if tree.orelse:
            print("\n", end='')
            print("else ", end='')
            print_program(tree.orelse, tab=tab + "\t")
            print("\n", end='')
    elif isinstance(tree, Break):
        print(tab, end='')
        print("break", end='')
    elif isinstance(tree, Try):
        print(tab, end='')
        print("try: ", end='')
        body = tree.body
        while body:
            print("\n", end='')
            print_program(body, tab=tab + "\t")
            print("\n", end='')
            body = body.next
        if tree.handlers:
            handler = tree.handlers
            while handler:
                print("\n", end='')
                print_program(handler, tab=tab)
                handler = handler.next
                print("\n", end='')
        if tree.orelse:
            print("\n", end='')
            print("else ", end='')
            print_program(tree.orelse, tab=tab + "\t")
            print("\n", end='')
        if tree.finalbody:
            print("\n", end='')
            print("finally: ", end='')
            print_program(tree.finalbody, tab=tab + "\t")
            print("\n", end='')
    elif isinstance(tree, ExceptHandler):
        print(tab, end='')
        print("except ", end='')
        print_program(tree.type)
        if tree.name:
            print(" as ", end='')
            print_program(tree.name)
        print(":\n", end='')
        print_program(tree.body, tab=tab+"\t")
    elif isinstance(tree, With):
        print(tab, end='')
        print("with ", end='')
        for item in tree.items:
            print_program(item)
            print(", ", end='')
        print(":\n", end='')
        print_program(tree.body, tab=tab+"\n")
    elif isinstance(tree, withitem):
        print_program(tree.context_expr)
        if tree.optional_vars:
            print(" as ", end='')
            print_program(tree.optional_vars)
    elif isinstance(tree, FunctionDef):
        print(tab, end='')
        print("def ", end='')
        print_program(tree.name)
        print("(", end='')
        print_program(tree.args)
        print("):", end='')
        body = tree.body
        while body:
            print("\n", end='')
            print_program(body, tab=tab+"\t")
            body = body.next
    elif isinstance(tree, Lambda):
        print(tab, end='')
        print_program(tree.args)
        print(" ", end='')
        print_program(tree.body)
    elif isinstance(tree, arguments):
        for arg_ in tree.args:
            print_program(arg_)
            print(", ", end='')
    elif isinstance(tree, arg):
        print(tree.arg, end='')
    elif isinstance(tree, Return):
        print(tab, end='')
        print("return ", end='')
        print_program(tree.value)
    elif isinstance(tree, Yield):
        print(tab, end='')
        print("yield ", end='')
        print_program(tree.value)
    elif isinstance(tree, YieldFrom):
        print(tab, end='')
        print("yield ", end='')
        print_program(tree.value)
    elif isinstance(tree, Global):
        print(tab, end='')
        print("global ", end='')
        for name in tree.names:
            print_program(name)
            print(", ", end='')
    elif isinstance(tree, Nonlocal):
        print(tab, end='')
        print("nonlocal ", end='')
        for name in tree.names:
            print_program(name)
            print(", ", end='')
    elif isinstance(tree, ClassDef):
        print(tab, end='')
        print("class ", end='')
        print(tree.name, end='')
        print("(", end='')
        for base in tree.bases:
            print_program(base)
            print(", ", end='')
        print(")", end='')
        body = tree.body
        while body:
            print("\n", end='')
            print_program(body, tab=tab+"\t")
            body = body.next
    elif isinstance(tree, AsyncFunctionDef):
        print(tab, end='')
        print("async def ", end='')
        print_program(tree.name)
        print("(", end='')
        print_program(tree.args)
        print("):", end='')
        body = tree.body
        while body:
            print("\n", end='')
            print_program(body, tab=tab + "\t")
            body = body.next
    elif isinstance(tree, Await):
        print(tab, end='')
        print("await ", end='')
        print_program(tree.value)
    elif isinstance(tree, AsyncFor):
        print(tab, end='')
        print("async for ", end='')
        print_program(tree.target)
        print(" in ", end='')
        print_program(tree.iter)
        print(":", end='')
        body = tree.body
        while body:
            print("\n", end='')
            print_program(body, tab=tab+"\t")
            print("\n", end='')
            body = body.next
        if tree.orelse:
            print("\n", end='')
            print("else ", end='')
            print_program(tree.orelse, tab=tab + "\t")
            print("\n", end='')
    elif isinstance(tree, AsyncWith):
        print(tab, end='')
        print("async with ", end='')
        for item in tree.items:
            print_program(item)
            print(", ", end='')
        print(":\n", end='')
        print_program(tree.body, tab=tab+"\n")
    elif isinstance(tree, Continue):
        print(tab, end='')
        print("continue", end='')
    else:
        print(tree, end='')
        
def write_program_on_file(tree, file, tab=""):
    if isinstance(tree, Module):
        body = tree.body
        while body:
            file.write("\n")
            write_program_on_file(body, file)
            body = body.next
    elif isinstance(tree, Num):
        file.write(str(tree.n))
    elif isinstance(tree, Str):
        file.write('"'+str(tree.s)+'"')
    elif isinstance(tree, FormattedValue):
        file.write("{")
        write_program_on_file(tree.value, file)
        file.write("}")
    elif isinstance(tree, JoinedStr):
        file.write('f"')
        for v in tree.values:
            write_program_on_file(v, file)
        file.write('"')
    elif isinstance(tree, Bytes):
        file.write('b"'+str(tree.b)+ '"')
    elif isinstance(tree, List):
        file.write("[")
        for el in tree.elts:
            write_program_on_file(el, file)
        file.write("]")
    elif isinstance(tree, Tuple):
        file.write("(")
        for el in tree.elts:
            write_program_on_file(el, file)
        file.write(")")
    elif isinstance(tree, Set):
        file.write("{")
        for el in tree:
            write_program_on_file(el, file)
        file.write("}")
    elif isinstance(tree, Dict):
        file.write("{")
        for key, value in zip(tree.keys, tree.values):
            write_program_on_file(key, file)
            file.write(":")
            write_program_on_file(value, file)
            file.write(",")
        file.write("}")
    elif isinstance(tree, Ellipsis):
        file.write("...")
    elif isinstance(tree, NameConstant):
        file.write(str(tree.value))
    elif isinstance(tree, Name):
        file.write(str(tree.id))
    elif isinstance(tree, Starred):
        file.write("*")
        write_program_on_file(tree.value, file)
    elif isinstance(tree, Expr):
        file.write(tab)
        write_program_on_file(tree.value, file)
    elif isinstance(tree, UnaryOp):
        write_program_on_file(tree.op, file)
        write_program_on_file(tree.operand, file)
    elif isinstance(tree, UAdd):
        file.write("++")
    elif isinstance(tree, USub):
        file.write("--")
    elif isinstance(tree, Not):
        file.write("not ")
    elif isinstance(tree, Invert):
        file.write("~")
    elif isinstance(tree, BinOp):
        write_program_on_file(tree.left, file)
        write_program_on_file(tree.op, file)
        write_program_on_file(tree.right, file)
    elif isinstance(tree, Add):
        file.write("+")
    elif isinstance(tree, Sub):
        file.write("-")
    elif isinstance(tree, Mult):
        file.write("*")
    elif isinstance(tree, Div):
        file.write("/")
    elif isinstance(tree, FloorDiv):
        file.write("//")
    elif isinstance(tree, Mod):
        file.write("%")
    elif isinstance(tree, Pow):
        file.write("**")
    elif isinstance(tree, LShift):
        file.write("<<")
    elif isinstance(tree, RShift):
        file.write(">>")
    elif isinstance(tree, BitOr):
        file.write("|")
    elif isinstance(tree, BitAnd):
        file.write("&")
    elif isinstance(tree, BitXor):
        file.write("^")
    elif isinstance(tree, MatMult):
        file.write("@")
    elif isinstance(tree, BoolOp):
        for v in tree.values:
            write_program_on_file(v, file)
            file.write(" ")
            write_program_on_file(tree.op, file)
            file.write(" ")
    elif isinstance(tree, And):
        file.write("and")
    elif isinstance(tree, Or):
        file.write("or")
    elif isinstance(tree, Compare):
        write_program_on_file(tree.left, file)
        file.write(" ")
        for op, comp in zip(tree.ops, tree.comparators):
            write_program_on_file(op, file)
            file.write(" ")
            write_program_on_file(comp, file)
            file.write(" ")
    elif isinstance(tree, Eq):
        file.write("==")
    elif isinstance(tree, NotEq):
        file.write("!=")
    elif isinstance(tree, Lt):
        file.write("<")
    elif isinstance(tree, LtE):
        file.write("<=")
    elif isinstance(tree, Gt):
        file.write(">")
    elif isinstance(tree, GtE):
        file.write(">=")
    elif isinstance(tree, Is):
        file.write("is")
    elif isinstance(tree, IsNot):
        file.write("is not")
    elif isinstance(tree, In):
        file.write("in")
    elif isinstance(tree, NotIn):
        file.write("not in")
    elif isinstance(tree, Call):
        file.write(tab)
        write_program_on_file(tree.func, file)
        file.write("(")
        for arg_ in tree.args:
            write_program_on_file(arg_, file)
            file.write(", ")
        for keyword_ in tree.keywords:
            write_program_on_file(keyword_, file)
            file.write(", ")
        file.write(")")
    elif isinstance(tree, keyword):
        write_program_on_file(tree.arg, file)
        file.write(" = ")
        write_program_on_file(tree.value, file)
    elif isinstance(tree, IfExp):
        write_program_on_file(tree.body, file)
        file.write(" if ")
        write_program_on_file(tree.test, file)
        file.write(" else ")
        write_program_on_file(tree.orelse, file)
    elif isinstance(tree, Attribute):
        write_program_on_file(tree.value, file)
        file.write(".")
        write_program_on_file(tree.attr, file)
    elif isinstance(tree, Subscript):
        write_program_on_file(tree.value, file)
        write_program_on_file(tree.slice, file)
    elif isinstance(tree, Index):
        file.write("[")
        write_program_on_file(tree.value, file)
        file.write("]")
    elif isinstance(tree, Slice):
        file.write("[")
        write_program_on_file(tree.lower, file)
        file.write(":")
        write_program_on_file(tree.upper, file)
        file.write("]")
    elif isinstance(tree, ExtSlice):
        file.write("[")
        for dim in tree.dims:
            write_program_on_file(dim, file)
            file.write(", ")
    elif isinstance(tree, ListComp):
        file.write("[")
        write_program_on_file(tree.elt, file)
        file.write(" ")
        for gen in tree.generators:
            write_program_on_file(gen, file)
            file.write(" ")
        file.write("]")
    elif isinstance(tree, SetComp):
        file.write("{")
        write_program_on_file(tree.elt, file)
        file.write(" ")
        for gen in tree.generators:
            write_program_on_file(gen, file)
            file.write(" ")
        file.write("}")
    elif isinstance(tree, GeneratorExp):
        file.write("(")
        write_program_on_file(tree.elt, file)
        file.write(" ")
        for gen in tree.generators:
            write_program_on_file(gen, file)
            file.write(" ")
        file.write(")")
    elif isinstance(tree, DictComp):
        file.write("{")
        write_program_on_file(tree.key, file)
        file.write(":")
        write_program_on_file(tree.value, file)
        file.write(" ")
        for gen in tree.generators:
            write_program_on_file(gen, file)
            file.write(" ")
        file.write("}")
    elif isinstance(tree, comprehension):
        file.write("for ")
        write_program_on_file(tree.target, file)
        file.write(" in ")
        write_program_on_file(tree.iter, file)
        for i in tree.ifs:
            file.write(" if ")
            write_program_on_file(i, file)
    elif isinstance(tree, Assign):
        file.write(tab)
        for targ in tree.targets:
            write_program_on_file(targ, file)
            file.write("=")
        file.write("=")
        write_program_on_file(tree.value, file)
    elif isinstance(tree, AnnAssign):
        file.write(tab)
        write_program_on_file(tree.target, file)
        file.write("=")
        write_program_on_file(tree.value, file)
    elif isinstance(tree, AugAssign):
        file.write(tab)
        write_program_on_file(tree.target, file)
        write_program_on_file(tree.op, file)
        file.write("=")
    elif isinstance(tree, Raise):
        file.write(tab)
        file.write("raise ")
        if tree.exc:
            write_program_on_file(tree.exc, file)
        if tree.cause:
            file.write(" from ")
            write_program_on_file(tree.cause, file)
    elif isinstance(tree, Assert):
        file.write(tab)
        file.write("assert ")
        write_program_on_file(tree.test, file)
        file.write('"')
        write_program_on_file(tree.msg, file)
        file.write('"')
    elif isinstance(tree, Delete):
        file.write(tab)
        file.write("del ")
        for el in tree.targets:
            write_program_on_file(el, file)
            file.write(", ")
    elif isinstance(tree, Pass):
        file.write(tab)
        file.write("pass")
    elif isinstance(tree, Import):
        file.write("import ")
        for n in tree.names:
            write_program_on_file(n, file)
            file.write(", ")
    elif isinstance(tree, ImportFrom):
        file.write("from ")
        for n in tree.names:
            write_program_on_file(n, file)
            file.write(", ")
    elif isinstance(tree, alias):
        write_program_on_file(tree.name, file)
        file.write(" as ")
        write_program_on_file(tree.asname, file)
    elif isinstance(tree, If):
        file.write(tab)
        file.write("if ")
        write_program_on_file(tree.test, file)
        file.write(":")
        body = tree.body
        while body:
            file.write("\n")
            write_program_on_file(body, file, tab=tab+"\t")
            file.write("\n")
            body = body.next
        if tree.orelse:
            orelse = tree.orelse
            while orelse:
                file.write("\n")
                file.write("else ")
                if isinstance(orelse, If):
                    write_program_on_file(orelse, file, tab=tab)
                else:
                    file.write("\n")
                    write_program_on_file(orelse, file, tab=tab+"\t")
                orelse = orelse.next
                file.write("\n")
    elif isinstance(tree, For):
        file.write(tab)
        file.write("for ")
        write_program_on_file(tree.target, file)
        file.write(" in ")
        write_program_on_file(tree.iter, file)
        file.write(":")
        body = tree.body
        while body:
            file.write("\n")
            write_program_on_file(body, file, tab=tab+"\t")
            file.write("\n")
            body = body.next
        if tree.orelse:
            file.write("\n")
            file.write("else ")
            write_program_on_file(tree.orelse, file, tab=tab + "\t")
            file.write("\n")
    elif isinstance(tree, While):
        file.write(tab)
        file.write("while ")
        write_program_on_file(tree.test, file)
        file.write(":")
        body = tree.body
        while body:
            file.write("\n")
            write_program_on_file(body, file, tab=tab+"\t")
            file.write("\n")
            body = body.next
        if tree.orelse:
            file.write("\n")
            file.write("else ")
            write_program_on_file(tree.orelse, file, tab=tab + "\t")
            file.write("\n")
    elif isinstance(tree, Break):
        file.write(tab)
        file.write("break")
    elif isinstance(tree, Try):
        file.write(tab)
        file.write("try: ")
        body = tree.body
        while body:
            file.write("\n")
            write_program_on_file(body, file, tab=tab + "\t")
            file.write("\n")
            body = body.next
        if tree.handlers:
            handler = tree.handlers
            while handler:
                file.write("\n")
                write_program_on_file(handler, file, tab=tab)
                handler = handler.next
                file.write("\n")
        if tree.orelse:
            file.write("\n")
            file.write("else ")
            write_program_on_file(tree.orelse, file, tab=tab + "\t")
            file.write("\n")
        if tree.finalbody:
            file.write("\n")
            file.write("finally: ")
            write_program_on_file(tree.finalbody, file, tab=tab + "\t")
            file.write("\n")
    elif isinstance(tree, ExceptHandler):
        file.write(tab)
        file.write("except ")
        write_program_on_file(tree.type, file)
        if tree.name:
            file.write(" as ")
            write_program_on_file(tree.name, file)
        file.write(":\n")
        write_program_on_file(tree.body, file, tab=tab+"\t")
    elif isinstance(tree, With):
        file.write(tab)
        file.write("with ")
        for item in tree.items:
            write_program_on_file(item, file)
            file.write(", ")
        file.write(":\n")
        write_program_on_file(tree.body, file, tab=tab+"\n")
    elif isinstance(tree, withitem):
        write_program_on_file(tree.context_expr, file)
        if tree.optional_vars:
            file.write(" as ")
            write_program_on_file(tree.optional_vars, file)
    elif isinstance(tree, FunctionDef):
        file.write(tab)
        file.write("def ")
        write_program_on_file(tree.name, file)
        file.write("(")
        write_program_on_file(tree.args, file)
        file.write("):")
        body = tree.body
        while body:
            file.write("\n")
            write_program_on_file(body, file, tab=tab+"\t")
            body = body.next
    elif isinstance(tree, Lambda):
        file.write(tab)
        write_program_on_file(tree.args, file)
        file.write(" ")
        write_program_on_file(tree.body, file)
    elif isinstance(tree, arguments):
        for arg_ in tree.args:
            write_program_on_file(arg_, file)
            file.write(", ")
    elif isinstance(tree, arg):
        file.write(tree.arg)
    elif isinstance(tree, Return):
        file.write(tab)
        file.write("return ")
        write_program_on_file(tree.value, file)
    elif isinstance(tree, Yield):
        file.write(tab)
        file.write("yield ")
        write_program_on_file(tree.value, file)
    elif isinstance(tree, YieldFrom):
        file.write(tab)
        file.write("yield ")
        write_program_on_file(tree.value, file)
    elif isinstance(tree, Global):
        file.write(tab)
        file.write("global ")
        for name in tree.names:
            write_program_on_file(name, file)
            file.write(", ")
    elif isinstance(tree, Nonlocal):
        file.write(tab)
        file.write("nonlocal ")
        for name in tree.names:
            write_program_on_file(name, file)
            file.write(", ")
    elif isinstance(tree, ClassDef):
        file.write(tab)
        file.write("class ")
        file.write(tree.name)
        file.write("(")
        for base in tree.bases:
            write_program_on_file(base, file)
            file.write(", ")
        file.write(")")
        body = tree.body
        while body:
            file.write("\n")
            write_program_on_file(body, file, tab=tab+"\t")
            body = body.next
    elif isinstance(tree, AsyncFunctionDef):
        file.write(tab)
        file.write("async def ")
        write_program_on_file(tree.name, file)
        file.write("(")
        write_program_on_file(tree.args, file)
        file.write("):")
        body = tree.body
        while body:
            file.write("\n")
            write_program_on_file(body, file, tab=tab + "\t")
            body = body.next
    elif isinstance(tree, Await):
        file.write(tab)
        file.write("await ")
        write_program_on_file(tree.value, file)
    elif isinstance(tree, AsyncFor):
        file.write(tab)
        file.write("async for ")
        write_program_on_file(tree.target, file)
        file.write(" in ")
        write_program_on_file(tree.iter, file)
        file.write(":")
        body = tree.body
        while body:
            file.write("\n")
            write_program_on_file(body, file, tab=tab+"\t")
            file.write("\n")
            body = body.next
        if tree.orelse:
            file.write("\n")
            file.write("else ")
            write_program_on_file(tree.orelse, file, tab=tab + "\t")
            file.write("\n")
    elif isinstance(tree, AsyncWith):
        file.write(tab)
        file.write("async with ")
        for item in tree.items:
            write_program_on_file(item, file)
            file.write(", ")
        file.write(":\n")
        write_program_on_file(tree.body, file, tab=tab+"\n")
    elif isinstance(tree, Continue):
        file.write(tab)
        file.write("continue")
    else:
        file.write(str(tree))