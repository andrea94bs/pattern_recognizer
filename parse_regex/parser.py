from inspect import *
from fsa import Fsa2
from fsa.Fsa2 import *


def string_to_ast(pattern_program):
    return ast.parse(pattern_program)


def parse(x, first_iter=False, with_ids=False):
    global iter
    var_id = '_VAR_'
    fun_id = '_FUN_'
    attr_id = '_ATTR_'
    class_id = '_CLASS_'
    every_expr_id = '_EVERY_'
    assign_id = '_ASSIGNMENT_'
    statement_id = '_STAT_'
    base_id = '_BASE_'
    bases_id = '_BASES_'
    arg_id = '_ARG_'
    args_id = "_ARGS_"
    tuple_id = "_TUP_"
    num_id = "_NUM_"
    global binding_id
    global class_index
    global variable_index
    global function_index
    global variables_memory
    if first_iter:
        x = re.sub(r'(\t|^)print(.*)', r'\1print(\2)', x)
        binding_id = 0
        class_index = 0
        variable_index = 0
        function_index = 0
        variables_memory = {}
        if with_ids:
            return parse(ast.parse(x), first_iter=False, with_ids=True)
        else:
            return parse(ast.parse(x), first_iter=False)
    binding_id += 1
    if isinstance(x, ast.Num):
        if with_ids:

            return Fsa2.Num(n=x.n, binding_id=binding_id)
        else:
            return Fsa2.Num(n=x.n)
    elif isinstance(x, ast.Str):
        if with_ids:

            return Fsa2.Str(s=x.s, binding_id=binding_id)
        else:
            return Fsa2.Str(s=x.s)
    elif isinstance(x, ast.FormattedValue):
        if with_ids:

            return Fsa2.FormattedValue(value=parse(x.value, first_iter=False, with_ids=True), conversion=x.conversion,
                                       format_spec=parse(x.format_spec, first_iter=False, with_ids=True),
                                       binding_id=binding_id)
        else:
            return Fsa2.FormattedValue(value=parse(x.value, first_iter=False), conversion=x.conversion,
                                       format_spec=parse(x.format_spec, first_iter=False))
    elif isinstance(x, ast.Bytes):
        if with_ids:

            return Fsa2.Bytes(s=x.s, binding_id=binding_id)
        else:
            return Fsa2.Bytes(s=x.s)
    elif isinstance(x, ast.Ellipsis):
        if with_ids:

            return Fsa2.Ellipsis(binding_id=binding_id)
        else:
            return Fsa2.Ellipsis()
    elif isinstance(x, ast.NameConstant):
        if with_ids:

            return Fsa2.NameConstant(value=x.value, binding_id=binding_id)
        else:
            return Fsa2.NameConstant(value=x.value)
    elif isinstance(x, ast.Name):
        if x.id.startswith(var_id) or x.id.startswith(every_expr_id) or x.id.startswith(fun_id) or x.id.startswith(
                base_id) or x.id.startswith(num_id):
            if x.id[len(x.id) - 1] == "*":
                name = x.id[0:len(x.id) - 1]
                multi = True
            else:
                name = x.id
                multi = False
            if x.id.startswith(var_id) or x.id.startswith(base_id):
                if variables_memory and '_MULTI_' not in x.id:
                    for e in variables_memory:
                        if x.id == e:
                            variables_memory.get(e).append(binding_id)
                            break
                    else:
                        variables_memory[x.id] = [binding_id]
                        temp_for_debug = variables_memory
                else:
                    if '_MULTI_' not in x.id:
                        variables_memory[x.id] = [binding_id]
                if with_ids:
                    return Fsa2.GenericName(name=name, multi=multi, binding_id=binding_id)
                else:
                    return Fsa2.GenericName(name=name, multi=multi)
            elif x.id.startswith(fun_id):
                if variables_memory and '_MULTI_' not in x.id:
                    for e in variables_memory:
                        if x.id == e:
                            variables_memory.get(e).append(binding_id)
                            break
                    else:
                        variables_memory[x.id] = [binding_id]
                    temp_for_debug = variables_memory
                else:
                    if '_MULTI_' not in x.id:
                        variables_memory[x.id] = [binding_id]
                if with_ids:
                    return Fsa2.GenericCall(name=name, binding_id=binding_id)
                else:
                    return Fsa2.GenericCall(name=name)
            elif x.id.startswith(num_id):
                if "_GT_" in x.id and "_LT_" in x.id:
                    return GenericNum(gt=parse_num(True, x.id)[0], lt=parse_num(True, x.id)[1])
                elif "_GT_" in x.id :
                    return GenericNum(gt=parse_num(False, x.id)[0])
                elif "_LT_" in x.id:
                    return GenericNum(lt=parse_num(False, x.id)[0])
                else:
                    return GenericNum()
            else:
                if with_ids:
                    return Fsa2.GenericExpression(multi=multi, binding_id=binding_id)
                else:
                    return Fsa2.GenericExpression(multi=multi)
        elif '_BIN_OPS_' in x.id:
            return Fsa2.GenericBinOp()
        elif '_TUP_' in x.id:
            return Fsa2.GenericTuple();
        else:
            if with_ids:
                return Fsa2.Name(id=x.id, ctx=parse(x.ctx, first_iter=False, with_ids=True), binding_id=binding_id)
            else:
                return Fsa2.Name(id=x.id, ctx=parse(x.ctx, first_iter=False))
    elif isinstance(x, ast.Load):
        if with_ids:

            return Fsa2.Load(binding_id=binding_id)
        else:
            return Fsa2.Load()
    elif isinstance(x, ast.Store):
        if with_ids:

            return Fsa2.Store(binding_id=binding_id)
        else:
            return Fsa2.Store()
    elif isinstance(x, ast.Del):
        if with_ids:

            return Fsa2.Del(binding_id=binding_id)
        else:
            return Fsa2.Del()
    elif isinstance(x, ast.UAdd):
        if with_ids:

            return Fsa2.UAdd(binding_id=binding_id)
        else:
            return Fsa2.UAdd()
    elif isinstance(x, ast.USub):
        if with_ids:

            return Fsa2.USub(binding_id=binding_id)
        else:
            return Fsa2.USub()
    elif isinstance(x, ast.Not):
        if with_ids:

            return Fsa2.Not(binding_id=binding_id)
        else:
            return Fsa2.Not()
    elif isinstance(x, ast.Invert):

        if with_ids:

            return Fsa2.Invert(binding_id=binding_id)
        else:
            return Fsa2.Invert()
    elif isinstance(x, ast.Add):
        if with_ids:

            return Fsa2.Add(binding_id=binding_id)
        else:
            return Fsa2.Add()
    elif isinstance(x, ast.Sub):
        if with_ids:

            return Fsa2.Sub(binding_id=binding_id)
        else:
            return Fsa2.Sub()
    elif isinstance(x, ast.Mult):
        if with_ids:

            return Fsa2.Mult(binding_id=binding_id)
        else:
            return Fsa2.Mult()
    elif isinstance(x, ast.Div):
        if with_ids:

            return Fsa2.Div(binding_id=binding_id)
        else:
            return Fsa2.Div()
    elif isinstance(x, ast.FloorDiv):
        if with_ids:

            return Fsa2.FloorDiv(binding_id=binding_id)
        else:
            return Fsa2.FloorDiv(binding_id=binding_id)
    elif isinstance(x, ast.Mod):
        if with_ids:

            return Fsa2.Mod(binding_id=binding_id)
        else:
            return Fsa2.Mod()
    elif isinstance(x, ast.Pow):
        if with_ids:

            return Fsa2.Pow(binding_id=binding_id)
        else:
            return Fsa2.Pow()
    elif isinstance(x, ast.LShift):
        if with_ids:

            return Fsa2.LShift(binding_id=binding_id)
        else:
            return Fsa2.LShift()
    elif isinstance(x, ast.RShift):
        if with_ids:

            return Fsa2.RShift(binding_id=binding_id)
        else:
            return Fsa2.RShift()
    elif isinstance(x, ast.BitOr):
        if with_ids:

            return Fsa2.BitOr(binding_id=binding_id)
        else:
            return Fsa2.BitOr()
    elif isinstance(x, ast.BitXor):
        if with_ids:

            return Fsa2.BitXor(binding_id=binding_id)
        else:
            return Fsa2.BitXor()
    elif isinstance(x, ast.BitAnd):
        if with_ids:

            return Fsa2.BitAnd(binding_id=binding_id)
        else:
            return Fsa2.BitAnd()
    elif isinstance(x, ast.MatMult):
        if with_ids:

            return Fsa2.MatMult(binding_id=binding_id)
        else:
            return Fsa2.MatMult()
    elif isinstance(x, ast.And):
        if with_ids:

            return Fsa2.And(binding_id=binding_id)
        else:
            return Fsa2.And()
    elif isinstance(x, ast.Or):
        if with_ids:

            return Fsa2.Or(binding_id=binding_id)
        else:
            return Fsa2.Or()
    elif isinstance(x, ast.Eq):
        if with_ids:

            return Fsa2.Eq(binding_id=binding_id)
        else:
            return Fsa2.Or()
    elif isinstance(x, ast.NotEq):
        if with_ids:

            return Fsa2.NotEq(binding_id=binding_id)
        else:
            return Fsa2.NotEq()
    elif isinstance(x, ast.Lt):
        if with_ids:

            return Fsa2.Lt(binding_id=binding_id)
        else:
            return Fsa2.Lt()
    elif isinstance(x, ast.LtE):
        if with_ids:

            return Fsa2.LtE(binding_id=binding_id)
        else:
            return Fsa2.LtE()
    elif isinstance(x, ast.Gt):
        if with_ids:

            return Fsa2.Gt(binding_id=binding_id)
        else:
            return Fsa2.Gt()
    elif isinstance(x, ast.GtE):
        if with_ids:

            return Fsa2.GtE(binding_id=binding_id)
        else:
            return Fsa2.GtE()
    elif isinstance(x, ast.Is):
        if with_ids:

            return Fsa2.Is(binding_id=binding_id)
        else:
            return Fsa2.Is()
    elif isinstance(x, ast.IsNot):
        if with_ids:

            return Fsa2.IsNot(binding_id=binding_id)
        else:
            return Fsa2.IsNot()
    elif isinstance(x, ast.In):
        if with_ids:

            return Fsa2.In(binding_id=binding_id)
        else:
            return Fsa2.In()
    elif isinstance(x, ast.NotIn):
        if with_ids:

            return Fsa2.NotIn(binding_id=binding_id)
        else:
            return Fsa2.NotIn()
    elif isinstance(x, ast.Pass):
        if with_ids:

            return Fsa2.Pass(binding_id=binding_id)
        else:
            return Fsa2.Pass()
    elif isinstance(x, ast.Break):
        if with_ids:

            return Fsa2.Break(binding_id=binding_id)
        else:
            return Fsa2.Break()
    elif isinstance(x, ast.Continue):
        if with_ids:

            return Fsa2.Continue(binding_id=binding_id)
        else:
            return Fsa2.Continue()
    elif isinstance(x, ast.keyword):
        if x.arg.startswidth(var_id) or x.arg.startswidth(attr_id):
            if variables_memory and '_MULTI_' not in x.arg:
                for e in variables_memory:
                    if x.arg == e:
                        variables_memory.get(e).append(binding_id)
                        break
                else:
                    variables_memory[x.arg] = [binding_id]
            else:
                if '_MULTI_' not in x.arg:
                    temp_for_debug = variables_memory
                    variables_memory[x.arg] = [binding_id]
        if with_ids:

            return Fsa2.keyword(arg=parse(x.arg, first_iter=False, with_ids=True),
                                value=parse(x.value, first_iter=False, with_ids=True)
                                , binding_id=binding_id)
        else:
            return Fsa2.keyword(arg=parse(x.arg, first_iter=False), value=parse(x.value, first_iter=False))
    elif isinstance(x, ast.arg):
        if x.arg.startswith(var_id) or x.arg.startswith(attr_id):
            if variables_memory and '_MULTI_' not in x.arg:
                for e in variables_memory:
                    if x.arg == e:
                        variables_memory.get(e).append(binding_id)
                        break
                else:
                    variables_memory[x.arg] = [binding_id]
            else:
                if '_MULTI_' not in x.arg:
                    temp_for_debug = variables_memory
                    variables_memory[x.arg] = [binding_id]
        if x.arg.startswith(arg_id):
            if with_ids:
                return Fsa2.generic_arg(binding_id=binding_id)
            else:
                return Fsa2.generic_arg()
        else:
            if with_ids:

                return Fsa2.arg(arg=parse(x.arg, first_iter=False, with_ids=True),
                                annotation=parse(x.annotation, first_iter=False, with_ids=True),
                                binding_id=binding_id)
            else:
                return Fsa2.arg(arg=parse(x.arg, first_iter=False), annotation=parse(x.annotation, first_iter=False))
    elif isinstance(x, ast.arguments):
        args = []
        kwonlyargs = []
        defaults = []
        kw_defaults = []
        for y in x.args:
            args.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        for y in x.kwonlyargs:
            kwonlyargs.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        for y in x.defaults:
            defaults.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        for y in x.kw_defaults:
            kw_defaults.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        if with_ids:

            return Fsa2.arguments(args=args, vararg=parse(x.vararg, first_iter=False, with_ids=True),
                                  kwonlyargs=kwonlyargs,
                                  kwarg=parse(x.kwarg, first_iter=False, with_ids=True), defaults=defaults,
                                  kw_defaults=kw_defaults
                                  , binding_id=binding_id)
        else:
            return Fsa2.arguments(args=args, vararg=parse(x.vararg, first_iter=False), kwonlyargs=kwonlyargs,
                                  kwarg=parse(x.kwarg, first_iter=False), defaults=defaults, kw_defaults=kw_defaults)
    elif isinstance(x, ast.comprehension):
        ifs = []
        for y in x.ifs:
            ifs.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        if with_ids:

            return Fsa2.comprehension(target=parse(x.target, first_iter=False, with_ids=True),
                                      iter=parse(x.target, first_iter=False, with_ids=True),
                                      ifs=ifs, is_async=parse(x.is_async, first_iter=False, with_ids=True),
                                      binding_id=binding_id)
        else:
            return Fsa2.comprehension(target=parse(x.target, first_iter=False), iter=parse(x.target, first_iter=False),
                                      ifs=ifs, is_async=parse(x.is_async, first_iter=False))
    elif isinstance(x, ast.keyword):
        if with_ids:

            return Fsa2.keyword(arg=parse(x.arg, first_iter=False, with_ids=True),
                                value=parse(x.value, first_iter=False, with_ids=True),
                                binding_id=binding_id)
        else:
            return Fsa2.keyword(arg=parse(x.arg, first_iter=False), value=parse(x.value, first_iter=False))
    elif isinstance(x, ast.Call):
        args = []
        keywords = []
        for y in x.args:
            args.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        for y in x.keywords:
            keywords.append(Fsa2.keyword(arg=y.arg, value=parse(y.value, first_iter=False) if not with_ids else
            parse(y.value, first_iter=False, with_ids=True)))
        func = parse(x.func, first_iter=False, with_ids=True) if with_ids else parse(x.func, first_iter=False)
        if isinstance(func, Fsa2.GenericCall):
            if with_ids:
                return Fsa2.GenericCall(name=func.name, binding_id=binding_id, args=args, keywords=keywords)
            else:
                return Fsa2.GenericCall(name=func.name)
        else:
            if with_ids:

                name = func.attr if isinstance(func, Fsa2.Attribute) else func.id
                return Fsa2.Call(func=func, args=args, keywords=keywords,
                                 binding_id=binding_id)
            else:
                return Fsa2.Call(func=func, args=args, keywords=keywords)
    elif isinstance(x, ast.Starred):
        if with_ids:

            return Fsa2.Starred(value=parse(x.value, first_iter=False, with_ids=True),
                                ctx=parse(x.ctx, first_iter=False, with_ids=True),
                                binding_id=binding_id)
        else:
            return Fsa2.Starred(value=parse(x.value, first_iter=False), ctx=parse(x.ctx, first_iter=False))
    elif isinstance(x, ast.JoinedStr) or isinstance(x, ast.Dict) or isinstance(x, ast.BoolOp):
        values = []
        for y in x.values:
            values.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        if isinstance(x, ast.JoinedStr):
            if with_ids:

                return Fsa2.JoinedStr(values=values, binding_id=binding_id)
            else:
                return Fsa2.JoinedStr(values=values)
        elif isinstance(x, ast.Dict):
            keys = []
            for y in x.keys:
                keys.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
            if with_ids:

                return Fsa2.Dict(keys=keys, values=values, binding_id=binding_id)
            else:
                return Fsa2.Dict(keys=keys, values=values)
        elif isinstance(x, ast.BoolOp):
            if with_ids:

                return Fsa2.BoolOp(op=parse(x.op, first_iter=False, with_ids=True), values=values,
                                   binding_id=binding_id)
            else:
                return Fsa2.BoolOp(op=parse(x.op, first_iter=False), values=values)
    elif isinstance(x, ast.List) or isinstance(x, ast.Tuple) or isinstance(x, ast.Set):
        elts = []
        for y in x.elts:
            elts.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        if isinstance(x, ast.List):
            if with_ids:
                return Fsa2.List(elts=elts, ctx=parse(x.ctx, first_iter=False, with_ids=True), binding_id=binding_id)
            else:
                return Fsa2.List(elts=elts, ctx=parse(x.ctx, first_iter=False))
        elif isinstance(x, ast.Tuple):
            if with_ids:
                return Fsa2.Tuple(elts=elts, ctx=parse(x.ctx, first_iter=False, with_ids=True), binding_id=binding_id)
            else:
                return Fsa2.Tuple(elts=elts, ctx=parse(x.ctx, first_iter=False))
        elif isinstance(x, ast.Set):
            if with_ids:

                return Fsa2.Set(elts=elts, binding_id=binding_id)
            else:
                return Fsa2.Set(elts=elts)
    elif isinstance(x, ast.Attribute):
        if attr_id in x.attr or fun_id in x.attr:
            if '_MULTI_' in x.attr:
                multi = True
            else:
                multi = False
            if attr_id in x.attr:
                if variables_memory and '_MULTI_' not in x.attr:
                    for e in variables_memory:
                        if x.attr == e:
                            variables_memory.get(e).append(binding_id)
                            break
                    else:
                        variables_memory[x.attr] = [binding_id]
                else:
                    if '_MULTI_' not in x.attr:
                        temp_for_debug = variables_memory
                        variables_memory[x.attr] = [binding_id]
                if with_ids:
                    return Fsa2.GenericAttribute(name=x.attr, multi=multi, binding_id=binding_id)
                else:
                    return Fsa2.GenericAttribute(name=x.attr, multi=multi)
            elif fun_id in x.attr:
                if variables_memory and '_MULTI_' not in x.attr:
                    for e in variables_memory:
                        if x.attr == e:
                            variables_memory.get(e).append(binding_id)
                            break
                    else:
                        variables_memory[x.attr] = [binding_id]
                else:
                    if '_MULTI_' not in x.attr:
                        temp_for_debug = variables_memory
                        variables_memory[x.attr] = [binding_id]
                if with_ids:
                    return Fsa2.GenericCall(name=x.attr, multi=multi, binding_id=binding_id)
                else:
                    return Fsa2.GenericCall(name=x.attr, multi=multi)
        else:
            if with_ids:
                return Fsa2.Attribute(value=parse(x.value, first_iter=False, with_ids=True),
                                      attr=parse(x.attr, first_iter=False, with_ids=True),
                                      ctx=parse(x.ctx, with_ids=True, first_iter=False),
                                      binding_id=binding_id)
            else:
                return Fsa2.Attribute(value=parse(x.value, first_iter=False), attr=parse(x.attr, first_iter=False),
                                      ctx=parse(x.ctx, first_iter=False, with_ids=False))
    elif isinstance(x, ast.Subscript):
        if with_ids:

            return Fsa2.Subscript(value=parse(x.value, first_iter=False, with_ids=True),
                                  slice=parse(x.slice, first_iter=False, with_ids=True),
                                  ctx=parse(x.ctx, first_iter=False, with_ids=True),
                                  binding_id=binding_id)
        else:
            return Fsa2.Subscript(value=parse(x.value, first_iter=False), slice=parse(x.slice, first_iter=False),
                                  ctx=parse(x.ctx, first_iter=False))
    elif isinstance(x, ast.Index):
        if with_ids:

            return Fsa2.Index(value=parse(x.value, first_iter=False, with_ids=True), binding_id=binding_id)
        else:
            return Fsa2.Index(value=parse(x.value, first_iter=False))
    elif isinstance(x, ast.Slice):
        if with_ids:

            return Fsa2.Slice(lower=parse(x.lower, first_iter=False, with_ids=True),
                              upper=parse(x.upper, first_iter=False, with_ids=True),
                              step=parse(x.step, first_iter=False, with_ids=True),
                              binding_id=binding_id)
        else:
            return Fsa2.Slice(lower=parse(x.lower, first_iter=False), upper=parse(x.upper, first_iter=False),
                              step=parse(x.step, first_iter=False))
    elif isinstance(x, ast.ExtSlice):
        dims = []
        for y in x.dims:
            dims.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        if with_ids:

            return Fsa2.ExtSlice(dims, binding_id=binding_id)
        else:
            return Fsa2.ExtSlice(dims)
    elif isinstance(x, ast.ListComp) or isinstance(x, ast.SetComp) or isinstance(x, ast.GeneratorExp) or isinstance(x,
                                                                                                                    ast.DictComp):
        generators = []
        for y in x.generators:
            ifs = []
            for z in y.ifs:
                ifs.append(parse(z, first_iter=False, with_ids=True) if with_ids else parse(z, first_iter=False))
            generators.append(Fsa2.comprehension(
                target=parse(y.target, first_iter=False, with_ids=True) if with_ids else parse(y.target,
                                                                                               first_iter=False),
                iter=parse(y.iter, first_iter=False, with_ids=True) if with_ids else parse(y.iter, first_iter=False),
                ifs=ifs, is_async=y.is_async))
        if isinstance(x, ast.ListComp):
            if with_ids:

                return Fsa2.ListComp(elt=parse(x.elt, first_iter=False, with_ids=True), generators=generators,
                                     binding_id=binding_id)
            else:
                return Fsa2.ListComp(elt=parse(x.elt, first_iter=False), generators=generators)
        elif isinstance(x, ast.SetComp):
            if with_ids:

                return Fsa2.SetComp(elt=parse(x.elt, first_iter=False, with_ids=True), generators=generators,
                                    binding_id=binding_id)
            else:

                return Fsa2.SetComp(elt=parse(x.elt, first_iter=False), generators=generators,
                                    binding_id=binding_id)
        elif isinstance(x, ast.GeneratorExp):
            if with_ids:

                return Fsa2.GeneratorExp(elt=parse(x.elt, first_iter=False, with_ids=True), generators=generators,
                                         binding_id=binding_id)
            else:
                return Fsa2.GeneratorExp(elt=parse(x.elt, first_iter=False), generators=generators)
        elif isinstance(x, ast.DictComp):
            if with_ids:

                return Fsa2.DictComp(key=parse(x.key, first_iter=False, with_ids=True),
                                     value=parse(x.value, first_iter=False, with_ids=True),
                                     generators=generators, binding_id=binding_id)
            else:
                return Fsa2.DictComp(key=parse(x.key, first_iter=False), value=parse(x.value, first_iter=False),
                                     generators=generators)
    elif isinstance(x, ast.Module) or isinstance(x, ast.ClassDef) or isinstance(x, ast.FunctionDef) \
            or isinstance(x, ast.If) or isinstance(x, ast.For) or isinstance(x, ast.While) \
            or isinstance(x, ast.Try) or isinstance(x, ast.ExceptHandler) or isinstance(x, ast.With) or isinstance(x,
                                                                                                                   ast.AsyncFunctionDef):
        if x.body:
            body = parse(x.body[0], first_iter=False, with_ids=True) if with_ids else parse(x.body[0], first_iter=False)
            for i in range(1, len(x.body)):
                if i == 1:
                    next = body.attach(
                        parse(x.body[i], first_iter=False, with_ids=True) if with_ids else parse(x.body[i],
                                                                                                 first_iter=False))
                else:
                    next = next.attach(
                        parse(x.body[i], first_iter=False, with_ids=True) if with_ids else parse(x.body[i],
                                                                                                 first_iter=False))
        else:
            body = None
        if isinstance(x, ast.Module):
            if with_ids:
                temp_for_debug = variables_memory
                return Fsa2.Module(body=body, binding_id=binding_id), variables_memory
            else:
                return Fsa2.Module(body=body)
        elif isinstance(x, ast.ClassDef):
            bases = []
            for y in x.bases:
                bases.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
            if class_id in x.name:
                if x.name[len(x.name) - 1] == "*":
                    multi = True
                else:
                    multi = False
                if variables_memory and '_MULTI_' not in x.name:
                    for e in variables_memory:
                        if x.name == e:
                            variables_memory.get(e).append(binding_id)
                            break
                    else:
                        variables_memory[x.name] = [binding_id]
                else:
                    if '_MULTI_' not in x.name:
                        temp_for_debug = variables_memory
                        variables_memory[x.name] = [binding_id]
                if with_ids:
                    return Fsa2.GenericClassDef(name=x.name, multi=multi, body=body, bases=bases, binding_id=binding_id)
                else:
                    return Fsa2.GenericClassDef(multi=multi, body=body, bases=bases)
            else:
                if with_ids:

                    return Fsa2.ClassDef(name=parse(x.name, first_iter=False, with_ids=True), bases=bases,
                                         keywords=x.keywords,
                                         decorator_list=x.decorator_list, body=body, binding_id=binding_id)
                else:
                    return Fsa2.ClassDef(name=parse(x.name, first_iter=False), bases=bases, keywords=x.keywords,
                                         decorator_list=x.decorator_list, body=body)
        elif isinstance(x, ast.FunctionDef) or isinstance(x, ast.AsyncFunctionDef):
            kwonlyargs = []
            defaults = []
            kw_defaults = []
            args = parse(x.args, first_iter=False, with_ids=True) if with_ids else parse(x.args, first_iter=False)
            for z in defaults:
                defaults.append(parse(z, first_iter=False, with_ids=True) if with_ids else parse(z, first_iter=False))
            if isinstance(x, ast.AsyncFunctionDef):
                if fun_id in x.name:
                    if variables_memory and '_MULTI_' not in x.name:
                        for e in variables_memory:
                            if x.name == e:
                                variables_memory.get(e).append(binding_id)
                                break
                        else:
                            variables_memory[x.name] = [binding_id]
                    else:
                        if '_MULTI_' not in x.name:
                            temp_for_debug = variables_memory
                            variables_memory[x.name] = [binding_id]
                    if x.name[len(x.name) - 1] == "*":
                        multi = True
                    else:
                        multi = False
                    if with_ids:
                        return Fsa2.GenericAsyncFunctionDef(name=x.name, binding_id=binding_id)
                    else:
                        return Fsa2.GenericAsyncFunctionDef(name=x.name)
                else:
                    if with_ids:
                        return Fsa2.AsyncFunctionDef(name=parse(x.name, first_iter=False, with_ids=True), args=args,
                                                     decorator_list=x.decorator_list,
                                                     returns=x.returns, body=body, binding_id=binding_id)
                    else:
                        return Fsa2.AsyncFunctionDef(name=parse(x.name, first_iter=False), args=args,
                                                     decorator_list=x.decorator_list,
                                                     returns=x.returns, body=body)
            else:
                if fun_id in x.name:
                    if variables_memory and '_MULTI_' not in x.name:
                        for e in variables_memory:
                            if x.name == e:
                                variables_memory.get(e).append(binding_id)
                                break
                        else:
                            variables_memory[x.name] = [binding_id]
                    else:
                        if '_MULTI_' not in x.name:
                            temp_for_debug = variables_memory
                            variables_memory[x.name] = [binding_id]
                    if x.name[len(x.name) - 1] == "*":
                        multi = True
                    else:
                        multi = False
                    if with_ids:
                        return Fsa2.GenericFunctionDef(name=x.name, multi=multi, body=body, args=args,
                                                       binding_id=binding_id)
                    else:
                        return Fsa2.GenericFunctionDef(multi=multi, body=body, args=args)
                else:
                    if with_ids:
                        return Fsa2.FunctionDef(name=parse(x.name, first_iter=False, with_ids=True), args=args,
                                                decorator_list=x.decorator_list,
                                                returns=x.returns, body=body, binding_id=binding_id)
                    else:
                        return Fsa2.FunctionDef(name=parse(x.name, first_iter=False), args=args,
                                                decorator_list=x.decorator_list,
                                                returns=x.returns, body=body)
        elif isinstance(x, ast.If) or isinstance(x, ast.For) or isinstance(x, ast.While) or isinstance(x,
                                                                                                       ast.AsyncFor) or isinstance(
            x, ast.Try):
            test = None
            if isinstance(x, ast.For) or isinstance(x, ast.While) or isinstance(x, ast.AsyncFor) or isinstance(x,
                                                                                                               ast.Try):
                if x.orelse:
                    orelse = parse(x.orelse[0], first_iter=False, with_ids=True) if with_ids else parse(x.orelse[0],
                                                                                                        first_iter=False)
                    for i in range(1, len(x.orelse)):
                        if i == 1:
                            next = orelse.attach(
                                parse(x.orelse[i], first_iter=False, with_ids=True) if with_ids else parse(x.orelse[i],
                                                                                                           first_iter=False))
                        else:
                            next = next.attach(
                                parse(x.orelse[i], first_iter=False, with_ids=True) if with_ids else parse(x.orelse[i],
                                                                                                           first_iter=False))
                else:
                    orelse = None
            if isinstance(x, ast.If) or isinstance(x, ast.While):
                test = parse(x.test, first_iter=False, with_ids=True) if with_ids else parse(x.test, first_iter=False)
            if isinstance(x, ast.If):
                if x.orelse:
                    if isinstance(x.orelse[0], ast.If):
                        if x.orelse[0].body:
                            body_orelse = parse(x.orelse[0].body[0], first_iter=False) if with_ids else parse(
                                x.orelse[0].body[0], first_iter=False)
                            for i in range(1, len(x.orelse[0].body)):
                                if i == 1:
                                    next = body_orelse.attach(
                                        parse(x.orelse[0].body[i], first_iter=False, with_ids=True) if with_ids else
                                        parse(x.orelse[0].body[i], first_iter=False))
                                else:
                                    next = next.attach(parse(x.orelse[0].body[i], first_iter=False, with_ids=True)
                                                       if with_ids else parse(x.orelse[0].body[i], first_iter=False))
                        orelse = Fsa2.If(test=parse(x.orelse[0].test), body=body_orelse, orelse=None)
                        if x.orelse[0].orelse:
                            orelse.orelse = (
                                parse(x.orelse[0].orelse[0], first_iter=False, with_ids=True) if with_ids else
                                parse(x.orelse[0].orelse[0], first_iter=False))
                    else:
                        orelse = parse(x.orelse[0], with_ids=True) if with_ids else parse(x.orelse[0])
                else:
                    orelse = None
                if with_ids:

                    return Fsa2.If(test=test, body=body, orelse=orelse, binding_id=binding_id)
                else:
                    return Fsa2.If(test=test, body=body, orelse=orelse)
            elif isinstance(x, ast.While):
                if with_ids:

                    return Fsa2.While(test=test, body=body, orelse=orelse, binding_id=binding_id)
                else:
                    return Fsa2.While(test=test, body=body, orelse=orelse)
            elif isinstance(x, ast.For):
                if with_ids:

                    return Fsa2.For(target=parse(x.target, first_iter=False, with_ids=True),
                                    iter=parse(x.iter, first_iter=False, with_ids=True), body=body, orelse=orelse,
                                    binding_id=binding_id)
                else:
                    return Fsa2.For(target=parse(x.target, first_iter=False), iter=parse(x.iter, first_iter=False),
                                    body=body, orelse=orelse)
            elif isinstance(x, ast.AsyncFor):
                if with_ids:

                    return Fsa2.AsyncFor(target=parse(x.target, first_iter=False, with_ids=True),
                                         iter=parse(x.iter, first_iter=False, with_ids=True),
                                         body=body, orelse=orelse
                                         , binding_id=binding_id)
                else:
                    return Fsa2.AsyncFor(target=parse(x.target, first_iter=False), iter=parse(x.iter, first_iter=False),
                                         body=body, orelse=orelse)
            elif isinstance(x, ast.Try):
                if x.handlers:
                    handlers = parse(x.handlers[0], first_iter=False, with_ids=True) if with_ids else parse(
                        x.handlers[0], first_iter=False)
                    for i in range(1, len(x.handlers)):
                        if i == 1:
                            next = handlers.attach(
                                parse(x.handlers[i], first_iter=False, with_ids=True) if with_ids else
                                parse(x.handlers[i], first_iter=False))
                        else:
                            next = next.attach(parse(x.handlers[i], first_iter=False, with_ids=True) if with_ids else
                                               parse(x.handlers[i], first_iter=False))
                else:
                    handlers = None
                if x.finalbody:
                    finalbody = parse(x.finalbody[0], first_iter=False, with_ids=True) if with_ids else parse(
                        x.finalbody[0], first_iter=False)
                    for i in range(1, len(x.finalbody)):
                        if i == 1:
                            next = finalbody.attach(
                                parse(x.finalbody[i], first_iter=False, with_ids=True) if with_ids else parse(
                                    x.finalbody[i], first_iter=False))
                        else:
                            next = next.attach(
                                parse(x.finalbody[i], first_iter=False, with_ids=True) if with_ids else parse(
                                    x.finalbody[i], first_iter=False))
                else:
                    finalbody = None
                if with_ids:

                    return Fsa2.Try(body=body, handlers=handlers, orelse=orelse, finalbody=finalbody,
                                    binding_id=binding_id)
                else:
                    return Fsa2.Try(body=body, handlers=handlers, orelse=orelse, finalbody=finalbody)
        elif isinstance(x, ast.ExceptHandler):
            if with_ids:

                return Fsa2.ExceptHandler(type=parse(x.type, first_iter=False, with_ids=True), name=x.name, body=body,
                                          binding_id=binding_id)
            else:
                return Fsa2.ExceptHandler(type=parse(x.type, first_iter=False), name=x.name, body=body)
        elif isinstance(x, ast.With) or isinstance(x, ast.AsyncWith):
            items = []
            for y in x.items:
                items.append(Fsa2.withitem(
                    context_expr=parse(y.context_expr, first_iter=False, with_ids=True) if with_ids else parse(
                        y.context_expr, first_iter=False),
                    optional_vars=parse(y.optional_vars, first_iter=False, with_ids=True) if with_ids else parse(
                        y.optional_vars, first_iter=False)))
            if isinstance(x, ast.With):
                if with_ids:

                    return Fsa2.With(items=items, body=body, binding_id=binding_id)
                else:
                    return Fsa2.With(items=items, body=body)
            else:
                if with_ids:

                    return Fsa2.AsyncWith(items=items, body=body, binding_id=binding_id)
                else:
                    return Fsa2.AsyncWith(items=items, body=body)
    elif isinstance(x, ast.Lambda):
        if with_ids:

            return Fsa2.Lambda(args=parse(x.args, first_iter=False, with_ids=True),
                               body=parse(x.body, first_iter=False, with_ids=True),
                               binding_id=binding_id)
        else:
            return Fsa2.Lambda(args=parse(x.args, first_iter=False), body=parse(x.body, first_iter=False))
    elif isinstance(x, ast.Return):
        if with_ids:

            return Fsa2.Return(value=parse(x.value, first_iter=False, with_ids=True), binding_id=binding_id)
        else:
            return Fsa2.Return(value=parse(x.value, first_iter=False))
    elif isinstance(x, ast.Yield):
        if with_ids:

            return Fsa2.Yield(parse(x.value, first_iter=False, with_ids=True), binding_id=binding_id)
        else:
            return Fsa2.Yield(parse(x.value, first_iter=False))
    elif isinstance(x, ast.YieldFrom):
        if with_ids:

            return Fsa2.YieldFrom(parse(x.value, first_iter=False, with_ids=True), binding_id=binding_id)
        else:
            return Fsa2.YieldFrom(parse(x.value, first_iter=False))
    elif isinstance(x, ast.Expr):
        if isinstance(x.value, ast.Name):
            if x.value.id.startswith(statement_id) or x.value.id.startswith(fun_id) \
                    or x.value.id.startswith(assign_id):
                if x.value.id.endswith('_MULTI_'):
                    multi = True
                else:
                    multi = False
                if x.value.id.startswith(statement_id):
                    if with_ids:
                        return Fsa2.GenericStatement(multi=multi, binding_id=binding_id)
                    else:
                        return Fsa2.GenericStatement(multi=multi)
                elif x.value.id.startswith(assign_id):
                    if with_ids:
                        return Fsa2.GenericAssign(binding_id=binding_id)
                    else:
                        return Fsa2.GenericAssign()
        if with_ids:
            return Fsa2.Expr(value=parse(x.value, first_iter=False, with_ids=True), binding_id=binding_id)
        else:
            return Fsa2.Expr(value=parse(x.value, first_iter=False))
    elif isinstance(x, ast.UnaryOp):
        if with_ids:

            return Fsa2.UnaryOp(op=parse(x.op, first_iter=False, with_ids=True),
                                operand=parse(x.operand, first_iter=False, with_ids=True),
                                binding_id=binding_id)
        else:
            return Fsa2.UnaryOp(op=parse(x.op, first_iter=False), operand=parse(x.operand, first_iter=False))
    elif isinstance(x, ast.BinOp):
        if with_ids:

            return Fsa2.BinOp(left=parse(x.left, first_iter=False, with_ids=True),
                              op=parse(x.op, first_iter=False, with_ids=True),
                              right=parse(x.right, first_iter=False, with_ids=True),
                              binding_id=binding_id)
        else:
            return Fsa2.BinOp(left=parse(x.left, first_iter=False), op=parse(x.op, first_iter=False),
                              right=parse(x.right, first_iter=False))
    elif isinstance(x, ast.Compare):
        comparators = []
        ops = []
        for y in x.ops:
            ops.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        for y in x.comparators:
            comparators.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        if with_ids:

            return Fsa2.Compare(left=parse(x.left, first_iter=False, with_ids=True), ops=ops, comparators=comparators,
                                binding_id=binding_id)
        else:
            return Fsa2.Compare(left=parse(x.left, first_iter=False), ops=ops, comparators=comparators)
    elif isinstance(x, ast.IfExp):
        if with_ids:

            return Fsa2.IfExp(test=parse(x.test, first_iter=False, with_ids=True),
                              body=parse(x.test, first_iter=False, with_ids=True),
                              orelse=parse(x.orelse, first_iter=False, with_ids=True),
                              binding_id=binding_id)
        else:
            return Fsa2.IfExp(test=parse(x.test, first_iter=False), body=parse(x.test, first_iter=False),
                              orelse=parse(x.orelse, first_iter=False))

    elif isinstance(x, ast.Assign) or isinstance(x, ast.AnnAssign) or isinstance(x, ast.Delete):
        targets = []
        if isinstance(x, ast.Assign) or isinstance(x, ast.Delete):
            for y in x.targets:
                targets.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        if isinstance(x, ast.Assign) or isinstance(x, ast.AnnAssign):
            value = parse(x.value, first_iter=False, with_ids=True) if with_ids else parse(x.value, first_iter=False)
        if isinstance(x, ast.Assign):
            if with_ids:

                return Fsa2.Assign(targets=targets, value=parse(value, first_iter=False, with_ids=True),
                                   binding_id=binding_id)
            else:
                return Fsa2.Assign(targets=targets, value=parse(value, first_iter=False))
        elif isinstance(x, ast.Delete):
            if with_ids:

                return Fsa2.Delete(targets=targets, binding_id=binding_id)
            else:
                return Fsa2.Delete(targets=targets)
        elif isinstance(x, ast.AnnAssign):
            if with_ids:

                return Fsa2.AnnAssign(target=parse(x.target, first_iter=False, with_ids=True),
                                      annotation=parse(x.annotation, first_iter=False, with_ids=True),
                                      value=parse(value, first_iter=False, with_ids=True), simple=x.simple,
                                      binding_id=binding_id)
            else:
                return Fsa2.AnnAssign(target=parse(x.target, first_iter=False),
                                      annotation=parse(x.annotation, first_iter=False),
                                      value=parse(value, first_iter=False), simple=x.simple)
    elif isinstance(x, ast.AugAssign):
        if with_ids:

            return Fsa2.AugAssign(target=parse(x.target, first_iter=False, with_ids=True),
                                  op=parse(x.op, first_iter=False, with_ids=True),
                                  value=parse(x.value, first_iter=False, with_ids=True), binding_id=binding_id)
        else:
            return Fsa2.AugAssign(target=parse(x.target, first_iter=False), op=parse(x.op, first_iter=False),
                                  value=parse(x.value, first_iter=False))
    elif isinstance(x, ast.Raise):
        if with_ids:

            return Fsa2.Raise(exc=parse(x.exc, first_iter=False, with_ids=True),
                              cause=parse(x.cause, first_iter=False, with_ids=True),
                              binding_id=binding_id)
        else:
            return Fsa2.Raise(exc=parse(x.exc, first_iter=False), cause=parse(x.cause, first_iter=False))
    elif isinstance(x, ast.Assert):
        if with_ids:

            return Fsa2.Assert(test=parse(x.test, first_iter=False, with_ids=True),
                               msg=parse(x.msg, first_iter=False, with_ids=True),
                               binding_id=binding_id)
        else:
            return Fsa2.Assert(test=parse(x.test, first_iter=False), msg=parse(x.msg, first_iter=False))
    elif isinstance(x, ast.Import):
        names = []
        for y in x.names:
            names.append(Fsa2.alias(
                name=parse(y.name, first_iter=False, with_ids=True) if with_ids else parse(y.name, first_iter=False)
                , asname=parse(y.asname, first_iter=False, with_ids=True) if with_ids else parse(y.asname,
                                                                                                 first_iter=False)))
        if with_ids:

            return Fsa2.Import(names=names, binding_id=binding_id)
        else:
            return Fsa2.Import(names=names)
    elif isinstance(x, ast.ImportFrom):
        names = []
        for y in x.names:
            names.append(Fsa2.alias(name=parse(y.name, first_iter=False, with_ids=True)
            if with_ids else parse(y.name, first_iter=False),
                                    asname=parse(y.asname, first_iter=False, with_ids=True)
                                    if with_ids else parse(y.asname, first_iter=False)))
        if with_ids:
            return Fsa2.ImportFrom(module=x.module, names=names, level=parse(x.level, first_iter=False, with_ids=True),
                                   binding_id=binding_id)
        else:
            return Fsa2.ImportFrom(module=x.module, names=names, level=parse(x.level, first_iter=False))
    elif isinstance(x, ast.Global):
        names = []
        for y in x.names:
            names.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        if with_ids:

            return Fsa2.Global(names=names, binding_id=binding_id)
        else:
            return Fsa2.Global(names=names)
    elif isinstance(x, ast.Nonlocal):
        names = []
        for y in x.names:
            names.append(parse(y, first_iter=False, with_ids=True) if with_ids else parse(y, first_iter=False))
        if with_ids:

            return Fsa2.Nonlocal(names=names, binding_id=binding_id)
        else:
            return Fsa2.Nonlocal(names=names)
    elif isinstance(x, ast.Await):
        if with_ids:

            return Fsa2.Await(
                value=parse(x.value, first_iter=False, with_ids=True) if with_ids else parse(x.value, first_iter=False),
                binding_id=binding_id)
        else:
            return Fsa2.Await(
                value=parse(x.value, first_iter=False, with_ids=True) if with_ids else parse(x.value, first_iter=False))
    else:
        return x


def expand_node(node):
    fields = dict(ast.iter_fields(node))
    to_add = []
    if 'body' in fields:
        to_add.append(node.body)
    if 'orelse' in fields:
        to_add.append(node.orelse)
    if 'finalbody' in fields:
        to_add.append(node.finalbody)
    if to_add:
        return to_add
    else:
        return None


def create_fsa(pattern):
    root = parse(pattern)
    statements = []
    for x in root.body:
        statements.append(visit_node(x, nesting_level=1))


def visit_node(node, nesting_level):
    statements = []

    print(node)
    print(nesting_level)
    while 'body' in dict(ast.iter_fields(node)) or 'orelse' in dict(ast.iter_fields(node)) or \
            'finalbody' in dict(ast.iter_fields(node)):
        if 'body' in dict(ast.iter_fields(node)):
            for x in node.body:
                statements.append(x)
        if 'orelse' in dict(ast.iter_fields(node)):
            for x in node.body:
                statements.append(x)
            if 'finalbody' in dict(ast.iter_fields(node)):
                for x in node.finalbody:
                    statements.append(x)
        elif 'finalbody' in dict(ast.iter_fields(node)):
            for x in node.finalbody:
                statements.append(x)
    for x in statements:
        visit_node(x, nesting_level=nesting_level + 1)


def parse_num(both_lt_gt, num):
    i = 0
    l = 0
    if both_lt_gt:
        for c in num:
            if c == '_':
                i += 1
            l += 1
            if i == 3:
                lt_index = num[l:].find("_")
                temp = num[l + lt_index + 3 + 1:]
                return (int(num[l:l + lt_index])), (int(temp))
    else:
        for c in num:
            if c == '_':
                i += 1
            l += 1
            if i == 3:
                return int(num[l:]), None
