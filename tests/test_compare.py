from fsa.Fsa2 import *
from fsa.Fsa2 import GenericGlobal
from parse_regex.parser import *
import unittest
import ast

def test_placeholder_equal(self):
    t1 = parse("1")
    t2 = parse("1")
    self.assertEqual(t1.compare(t2), True)

def test_placeholder_different(self):
    t1 = parse("1")
    t2 = parse("2")
    self.assertNotEqual(t1.compare(t2), True)

def test_placeholder_another_node(self):
    t1 = parse("2")
    t2 = parse("'s'")
    self.assertNotEqual(t1.compare(t2), True)

def test_placeholder_another_type(self):
    t1 = parse("2")
    t2 = 0
    self.assertRaises(TypeError)

def test_generic_placeholder_equal(self):
    t1 = GenericNum()
    t2 = parse("2").body[0]
    self.assertEqual(t1.compare(t2), True)

def test_generic_placeholder_another_node(self):
    t1 = GenericNum()
    t2 = parse("'s'").body[0]
    self.assertNotEqual(t1.compare(t2), True)

def test_generic_placeholder_another_type(self):
     t1 = GenericNum()
     t2 = 0
     self.assertRaises(TypeError)




class Test(unittest.TestCase):
    def test_num_equal(self):
        t1 = parse("1")
        t2 = parse("1")
        self.assertEqual(t1.compare(t2), True)

    def test_num_different(self):
        t1 = parse("1")
        t2 = parse("2")
        self.assertNotEqual(t1.compare(t2), True)

    def test_num_another_node(self):
        t1 = parse("2")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_num_another_type(self):
        t1 = parse("2")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_num_equal(self):
        t1 = GenericNum()
        t2 = parse("2").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_num_another_node(self):
        t1 = GenericNum()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_num_another_type(self):
         t1 = GenericNum()
         t2 = 0
         self.assertRaises(TypeError)

    def test_str_equal(self):
        t1 = parse("'s'")
        t2 = parse("'s'")
        self.assertEqual(t1.compare(t2), True)

    def test_str_different(self):
        t1 = parse("'s'")
        t2 = parse("'t'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_str_another_node(self):
        t1 = parse("'s'")
        t2 = parse('2')
        self.assertNotEqual(t1.compare(t2), True)

    def test_str_another_type(self):
        t1 = parse('"s"')
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_str_equal(self):
        t1 = GenericStr()
        t2 = parse('"s"').body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_str_another_node(self):
        t1 = GenericStr()
        t2 = parse('1').body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_str_another_type(self):
         t1 = GenericNum()
         t2 = 0
         self.assertRaises(TypeError)

    def test_form_value_equal(self):
        t1 = parse('f"sin({a}) is {sin(a):.3}"')
        t2 = parse('f"sin({a}) is {sin(a):.3}"')
        self.assertEqual(t1.compare(t2), True)

    def test_form_value_different(self):
        t1 = parse('f"sin({a}) is {sin(a):.3}"')
        t2 = parse('f"sin({b}) is {sin(b):.3}"')
        self.assertNotEqual(t1.compare(t2), True)

    def test_form_value_another_node(self):
        t1 = parse('f"sin({a}) is {sin(a):.3}"')
        t2 = parse('"s"')
        self.assertNotEqual(t1.compare(t2), True)

    def test_form_value_another_type(self):
        t1 = parse('f"sin({a}) is {sin(a):.3}"')
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_form_value_equal(self):
        t1 = GenericJoinedStr()
        t2 = parse('f"sin({a}) is {sin(a):.3}"').body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_form_value_another_node(self):
        t1 = GenericFormattedValue()
        t2 = parse('"s"').body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_form_value_another_type(self):
        t1 = GenericFormattedValue()
        t2 = 0
        self.assertRaises(TypeError)

    def test_bytes_equal(self):
        t1 = parse("b'1'")
        t2 = parse("b'1'")
        self.assertEqual(t1.compare(t2), True)

    def test_bytes_different(self):
        t1 = parse("b'1'")
        t2 = parse("b'2'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_bytes_another_node(self):
        t1 = parse("b'1'")
        t2 = parse('"s"')
        self.assertNotEqual(t1.compare(t2), True)

    def test_bytes_another_type(self):
        t1 = parse('b"2"')
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_bytes_equal(self):
        t1 = GenericBytes()
        t2 = parse('b"1"').body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_bytes_another_node(self):
        t1 = GenericBytes()
        t2 = parse('"s"').body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_bytes_another_type(self):
         t1 = GenericBytes()
         t2 = 0
         self.assertRaises(TypeError)

    def test_list_equal(self):
        t1 = parse("[1,2,3]")
        t2 = parse("[1,2,3]")
        self.assertEqual(t1.compare(t2), True)

    def test_list_different(self):
        t1 = parse("[1,2,3]")
        t2 = parse("[3,4,5]")
        self.assertNotEqual(t1.compare(t2), True)

    def test_list_another_node(self):
        t1 = parse("[1,2,3]")
        t2 = parse('"s"')
        self.assertNotEqual(t1.compare(t2), True)

    def test_list_another_type(self):
        t1 = parse('[1,2,3]')
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_list_equal(self):
        t1 = GenericList()
        t2 = parse('[1,2,3]').body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_list_another_node(self):
        t1 = GenericList()
        t2 = parse('"s"').body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_list_another_type(self):
         t1 = GenericList()
         t2 = 0
         self.assertRaises(TypeError)

    def test_tuple_equal(self):
        t1 = parse("(1,2)")
        t2 = parse("(1,2)")
        self.assertEqual(t1.compare(t2), True)

    def test_tuple_different(self):
        t1 = parse("(1,2)")
        t2 = parse("(3,4)")
        self.assertNotEqual(t1.compare(t2), True)

    def test_tuple_another_node(self):
        t1 = parse("(1,2)")
        t2 = parse('"s"')
        self.assertNotEqual(t1.compare(t2), True)

    def test_tuple_another_type(self):
        t1 = parse("(1,2)")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_tuple_equal(self):
        t1 = GenericTuple()
        t2 = parse("(1,2)").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_tuple_another_node(self):
        t1 = GenericTuple()
        t2 = parse('"s"').body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_tuple_another_type(self):
         t1 = GenericTuple()
         t2 = 0
         self.assertRaises(TypeError)

    def test_set_equal(self):
        t1 = parse("{1,2,3}")
        t2 = parse("{1,2,3}")
        self.assertEqual(t1.compare(t2), True)

    def test_set_different(self):
        t1 = parse("{1,2,3}")
        t2 = parse("{3,4,5}")
        self.assertNotEqual(t1.compare(t2), True)

    def test_set_another_node(self):
        t1 = parse("{1,2,3}")
        t2 = parse('"s"')
        self.assertNotEqual(t1.compare(t2), True)

    def test_set_another_type(self):
        t1 = parse("{1,2,3}")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_set_equal(self):
        t1 = GenericSet()
        t2 = parse("{1,2,3}").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_set_another_node(self):
        t1 = GenericSet()
        t2 = parse('"s"').body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_set_another_type(self):
         t1 = GenericSet()
         t2 = 0
         self.assertRaises(TypeError)

    def test_dict_equal(self):
        t1 = parse("{1:2,3:4}")
        t2 = parse("{1:2,3:4}")
        self.assertEqual(t1.compare(t2), True)

    def test_dict_different(self):
        t1 = parse("{1:2,3:4}")
        t2 = parse("{5:6, 7:8}")
        self.assertNotEqual(t1.compare(t2), True)

    def test_dict_another_node(self):
        t1 = parse("{1:2,3:4}")
        t2 = parse('"s"')
        self.assertNotEqual(t1.compare(t2), True)

    def test_dict_another_type(self):
        t1 = parse("{1:2,3:4}")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_dict_equal(self):
        t1 = GenericDict()
        t2 = parse("{1:2,3:4}").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_dict_another_node(self):
        t1 = GenericDict()
        t2 = parse('"s"').body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_dict_another_type(self):
         t1 = GenericDict()
         t2 = 0
         self.assertRaises(TypeError)

    def test_ellipsis_equal(self):
        t1 = parse("...")
        t2 = parse("...")
        self.assertEqual(t1.compare(t2), True)

    def test_ellipsis_another_node(self):
        t1 = parse("...")
        t2 = parse('"s"')
        self.assertNotEqual(t1.compare(t2), True)

    def test_ellipsis_another_type(self):
        t1 = parse('...')
        t2 = 0
        self.assertRaises(TypeError)

    def test_name_constant_equal(self):
        t1 = parse("True")
        t2 = parse("True")
        self.assertEqual(t1.compare(t2), True)

    def test_name_constant_different(self):
        t1 = parse("True")
        t2 = parse("None")
        self.assertNotEqual(t1.compare(t2), True)

    def test_name_constant_another_node(self):
        t1 = parse("True")
        t2 = parse('"s"')
        self.assertNotEqual(t1.compare(t2), True)

    def test_name_constant_another_type(self):
        t1 = parse('True')
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_name_constant_equal(self):
        t1 = GenericNameConstant()
        t2 = parse("True").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_name_constant_another_node(self):
        t1 = GenericNameConstant()
        t2 = parse('"s"').body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_name_constant_another_type(self):
        t1 = GenericNameConstant()
        t2 = 0
        self.assertRaises(TypeError)

    def test_name_equal(self):
       t1 = parse("x")
       t2 = parse("x")
       self.assertEqual(t1.compare(t2), True)

    def test_name_different(self):
        t1 = parse("x")
        t2 = parse("y")
        self.assertNotEqual(t1.compare(t2), True)

    def test_name_another_node(self):
        t1 = parse("x")
        t2 = parse('"s"')
        self.assertNotEqual(t1.compare(t2), True)

    def test_name_another_type(self):
        t1 = parse('x')
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_name_equal(self):
        t1 = GenericName(number=1)
        t2 = parse('x').body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_name_another_node(self):
        t1 = GenericName(number=1)
        t2 = parse('"s"').body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_name_another_type(self):
         t1 = GenericName(number=1)
         t2 = 0
         self.assertRaises(TypeError)

    def test_starred_equal(self):
        t1 = parse("*x")
        t2 = parse("*x")
        self.assertEqual(t1.compare(t2), True)

    def test_starred_different(self):
        t1 = parse("*x")
        t2 = parse("*y")
        self.assertNotEqual(t1.compare(t2), True)

    def test_starred_another_node(self):
        t1 = parse("*x")
        t2 = parse('"s"')
        self.assertNotEqual(t1.compare(t2), True)

    def test_starred_another_type(self):
        t1 = parse("*x")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_starred_equal(self):
        t1 = GenericStarred()
        t2 = parse("*x").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_starred_another_node(self):
        t1 = GenericStarred()
        t2 = parse('"s"').body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_starred_another_type(self):
        t1 = GenericStarred()
        t2 = 0
        self.assertRaises(TypeError)

    def test_expr_another_node(self):
        t1 = parse("2")
        t2 = parse("pass")
        self.assertNotEqual(t1.compare(t2), True)

    def test_expr_another_type(self):
        t1 = parse("2")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_expr_equal(self):
        t1 = GenericExpr()
        t2 = parse("2").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_expr_another_node(self):
        t1 = GenericExpr()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_expr_another_type(self):
         t1 = GenericExpr()
         t2 = 0
         self.assertRaises(TypeError)

    def test_unary_op_equal(self):
        t1 = parse("not x")
        t2 = parse("not x")
        self.assertEqual(t1.compare(t2), True)

    def test_unary_op_different(self):
        t1 = parse("not x")
        t2 = parse("not y")
        self.assertNotEqual(t1.compare(t2), True)

    def test_unary_op_another_node(self):
        t1 = parse("not x")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_unary_op_another_type(self):
        t1 = parse("not x")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_unary_op_equal(self):
        t1 = GenericUnaryOp()
        t2 = parse("not x").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_unary_op_another_node(self):
        t1 = GenericUnaryOp()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_unary_op_another_type(self):
         t1 = GenericUnaryOp()
         t2 = 0
         self.assertRaises(TypeError)

    def test_bin_op_mult_equal(self):
        t1 = parse("x*y")
        t2 = parse("x*y")
        self.assertEqual(t1.compare(t2), True)

    def test_bin_op_mult_different(self):
        t1 = parse("x*y")
        t2 = parse("a*b")
        self.assertNotEqual(t1.compare(t2), True)

    def test_bin_op_mult_another_node(self):
        t1 = parse("x*y")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_bin_op_mult_another_type(self):
        t1 = parse("x*y")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_mult_op_and_equal(self):
        t1 = GenericBinOp()
        t2 = parse("x*y").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_bin_op_mult_another_node(self):
        t1 = GenericBinOp()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_bin_op_mult_another_type(self):
         t1 = GenericBinOp()
         t2 = 0
         self.assertRaises(TypeError)

    def test_bin_op_mult_div_equal(self):
        t1 = parse("x*y")
        t2 = parse("x*y")
        self.assertEqual(t1.compare(t2), True)

    def test_bin_op_mult_div_different(self):
        t1 = parse("x*y")
        t2 = parse("a/b")
        self.assertNotEqual(t1.compare(t2), True)

    def test_bin_op_mult_div_another_node(self):
        t1 = parse("x*y")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_bin_op_mult_div_another_type(self):
        t1 = parse("x*y")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_bin_op_mult_div_equal(self):
        t1 = GenericBinOp()
        t2 = parse("x*y").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_bin_op_mult_div_another_node(self):
        t1 = GenericBinOp()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_bin_op_mult_div_another_type(self):
         t1 = GenericBinOp()
         t2 = 0
         self.assertRaises(TypeError)

    def test_bool_op_and_equal(self):
        t1 = parse("x and y")
        t2 = parse("x and y")
        self.assertEqual(t1.compare(t2), True)

    def test_bool_op_and_different(self):
        t1 = parse("x and y")
        t2 = parse("a and b")
        self.assertNotEqual(t1.compare(t2), True)

    def test_bool_op_and_another_node(self):
        t1 = parse("x and y")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_bool_op_and_another_type(self):
        t1 = parse("x and y")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_bool_op_and_equal(self):
        t1 = GenericBoolOp()
        t2 = parse("x and y").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_bool_op_and_another_node(self):
        t1 = GenericBoolOp()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_bool_op_and_another_type(self):
         t1 = GenericBoolOp()
         t2 = 0
         self.assertRaises(TypeError)

    def test_bool_op_and_or_equal(self):
        t1 = parse("x and y")
        t2 = parse("x and y")
        self.assertEqual(t1.compare(t2), True)

    def test_bool_op_and_or_different(self):
        t1 = parse("x and y")
        t2 = parse("a and b")
        self.assertNotEqual(t1.compare(t2), True)

    def test_bool_op_and_or_another_node(self):
        t1 = parse("x or y")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_bool_op_and_or_another_type(self):
        t1 = parse("x and y")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_bool_op_and_or_equal(self):
        t1 = GenericBoolOp()
        t2 = parse("x and y").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_bool_op_and_or_another_node(self):
        t1 = GenericBoolOp()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_bool_op_and_or_another_type(self):
         t1 = GenericBoolOp()
         t2 = 0
         self.assertRaises(TypeError)

    def test_compare_equal(self):
        t1 = parse("x==y")
        t2 = parse("x==y")
        self.assertEqual(t1.compare(t2), True)

    def test_compare_different(self):
        t1 = parse("x==y")
        t2 = parse("a==b")
        self.assertNotEqual(t1.compare(t2), True)

    def test_compare_another_node(self):
        t1 = parse("x==y")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_compare_another_type(self):
        t1 = parse("x==y")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_compare_equal(self):
        t1 = GenericCompare()
        t2 = parse("x==y").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_compare_another_node(self):
        t1 = GenericCompare()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_compare_another_type(self):
         t1 = GenericCompare()
         t2 = 0
         self.assertRaises(TypeError)

    def test_call_equal(self):
        t1 = parse("f(x, y=1)")
        t2 = parse("f(x, y=1)")
        self.assertEqual(t1.compare(t2), True)

    def test_call_different(self):
        t1 = parse("f(x, y=1)")
        t2 = parse("g(a, b=1)")
        self.assertNotEqual(t1.compare(t2), True)

    def test_call_another_node(self):
        t1 = parse("f(x, y=1)")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_call_another_type(self):
        t1 = parse("f(x, y=1)")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_call_equal(self):
        t1 = GenericCall()
        t2 = parse("f(x, y=1)").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_call_another_node(self):
        t1 = GenericCall()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_call_another_type(self):
         t1 = GenericCall()
         t2 = 0
         self.assertRaises(TypeError)

    def test_if_exp_equal(self):
        t1 = parse("a if b else c")
        t2 = parse("a if b else c")
        self.assertEqual(t1.compare(t2), True)

    def test_if_exp_different(self):
        t1 = parse("a if b else c")
        t2 = parse("d if e else f")
        self.assertNotEqual(t1.compare(t2), True)

    def test_if_exp_another_node(self):
        t1 = parse("a if b else c")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_if_exp_another_type(self):
        t1 = parse("a if b else c")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_if_exp_equal(self):
        t1 = GenericIfExp()
        t2 = parse("a if b else c").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_if_exp_another_node(self):
        t1 = GenericIfExp()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_if_exp_another_type(self):
         t1 = GenericIfExp()
         t2 = 0
         self.assertRaises(TypeError)

    def test_attribute_equal(self):
        t1 = parse("a.b")
        t2 = parse("a.b")
        self.assertEqual(t1.compare(t2), True)

    def test_attribute_different(self):
        t1 = parse("a.b")
        t2 = parse("c.d")
        self.assertNotEqual(t1.compare(t2), True)

    def test_attribute_another_node(self):
        t1 = parse("a.b")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_attribute_another_type(self):
        t1 = parse("a.b")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_attribute_equal(self):
        t1 = GenericAttribute()
        t2 = parse("a.b").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_attribute_another_node(self):
        t1 = GenericAttribute()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_attribute_another_type(self):
         t1 = GenericAttribute()
         t2 = 0
         self.assertRaises(TypeError)

    def test_subscript_equal(self):
        t1 = parse("l[1]")
        t2 = parse("l[1]")
        self.assertEqual(t1.compare(t2), True)

    def test_subscript_different(self):
        t1 = parse("l[1]")
        t2 = parse("m[2]")
        self.assertNotEqual(t1.compare(t2), True)

    def test_subscript_another_node(self):
        t1 = parse("l[1]")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_subscript_another_type(self):
        t1 = parse("l[1]")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_subscript_equal(self):
        t1 = GenericSubscript()
        t2 = parse("l[1]").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_subscript_another_node(self):
        t1 = GenericSubscript()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_subscript_another_type(self):
         t1 = GenericSubscript()
         t2 = 0
         self.assertRaises(TypeError)

    def test_slice_equal(self):
        t1 = parse("l[1:2]")
        t2 = parse("l[1:2]")
        self.assertEqual(t1.compare(t2), True)

    def test_slice_different(self):
        t1 = parse("l[1:2]")
        t2 = parse("m[3:4]")
        self.assertNotEqual(t1.compare(t2), True)

    def test_slice_another_node(self):
        t1 = parse("l[1:2]")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_slice_another_type(self):
        t1 = parse("l[1:2]")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_slice_equal(self):
        t1 = GenericSlice()
        t2 = parse("l[1:2]").body[0].value.slice
        self.assertEqual(t1.compare(t2), True)

    def test_generic_slice_another_node(self):
        t1 = GenericSlice()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_slice_another_type(self):
         t1 = GenericSlice()
         t2 = 0
         self.assertRaises(TypeError)

    def test_ext_slice_equal(self):
        t1 = parse("l[1:2, 3]")
        t2 = parse("l[1:2, 3]")
        self.assertEqual(t1.compare(t2), True)

    def test_ext_slice_different(self):
        t1 = parse("l[1:2, 3]")
        t2 = parse("m[4:5, 6]")
        self.assertNotEqual(t1.compare(t2), True)

    def test_ext_slice_another_node(self):
        t1 = parse("l[1:2, 3]")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_ext_slice_another_type(self):
        t1 = parse("l[1:2, 3]")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_ext_slice_equal(self):
        t1 = GenericExtSlice()
        t2 = parse("l[1:2, 3]").body[0].value.slice
        self.assertEqual(t1.compare(t2), True)

    def test_generic_ext_slice_another_node(self):
        t1 = GenericExtSlice()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_ext_slice_another_type(self):
         t1 = GenericExtSlice()
         t2 = 0
         self.assertRaises(TypeError)

    def test_list_comp_equal(self):
        t1 = parse("[x for x in y if a]")
        t2 = parse("[x for x in y if a]")
        self.assertEqual(t1.compare(t2), True)

    def test_list_comp_different(self):
        t1 = parse("[x for x in y if a]")
        t2 = parse("[z for z in k if b]")
        self.assertNotEqual(t1.compare(t2), True)

    def test_list_comp_another_node(self):
        t1 = parse("[x for x in y if a]")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_list_comp_another_type(self):
        t1 = parse("[x for x in y if a]")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_list_comp_equal(self):
        t1 = GenericListComp()
        t2 = parse("[x for x in y if a]").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_list_comp_another_node(self):
        t1 = GenericListComp()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_list_comp_another_type(self):
         t1 = GenericListComp()
         t2 = 0
         self.assertRaises(TypeError)

    def test_set_comp_equal(self):
        t1 = parse("{x for x in y if a}")
        t2 = parse("{x for x in y if a}")
        self.assertEqual(t1.compare(t2), True)

    def test_set_comp_different(self):
        t1 = parse("{x for x in y if a}")
        t2 = parse("{z for z in q if b}")
        self.assertNotEqual(t1.compare(t2), True)

    def test_set_comp_another_node(self):
        t1 = parse("{x for x in y if a}")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_set_comp_another_type(self):
        t1 = parse("{x for x in y if a}")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_set_comp_equal(self):
        t1 = GenericSetComp()
        t2 = parse("{x for x in y if a}").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_set_comp_another_node(self):
        t1 = GenericSetComp()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_set_comp_another_type(self):
        t1 = GenericSetComp()
        t2 = 0
        self.assertRaises(TypeError)

    def test_gen_exp_equal(self):
        t1 = parse("(x for x in y if a)")
        t2 = parse("(x for x in y if a)")
        self.assertEqual(t1.compare(t2), True)

    def test_gen_exp_different(self):
        t1 = parse("(x for x in y if a)")
        t2 = parse("(z for z in q if b)")
        self.assertNotEqual(t1.compare(t2), True)

    def test_gen_exp_another_node(self):
        t1 = parse("(x for x in y if a)")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_gen_exp_another_type(self):
        t1 = parse("(x for x in y if a)")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_gen_exp_equal(self):
        t1 = GenericGeneratorExp()
        t2 = parse("(x for x in y if a)").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_gen_exp_another_node(self):
        t1 = GenericGeneratorExp()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_gen_exp_another_type(self):
        t1 = GenericGeneratorExp()
        t2 = 0
        self.assertRaises(TypeError)

    def test_dict_comp_equal(self):
        t1 = parse("{k : x for x in y if a}")
        t2 = parse("{k : x for x in y if a}")
        self.assertEqual(t1.compare(t2), True)

    def test_dict_comp_different(self):
        t1 = parse("{k : x for x in y if a}")
        t2 = parse("{j : z for z in q if b}")
        self.assertNotEqual(t1.compare(t2), True)

    def test_dict_comp_another_node(self):
        t1 = parse("{k : x for x in y if a}")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_dict_comp_another_type(self):
        t1 = parse("{k : x for x in y if a}")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_dict_comp_equal(self):
        t1 = GenericDictComp()
        t2 = parse("{k : x for x in y if a}").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_dict_comp_another_node(self):
        t1 = GenericDictComp()
        t2 = parse("'s'").body[0].value
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_dict_comp_another_type(self):
        t1 = GenericDictComp()
        t2 = 0
        self.assertRaises(TypeError)

    def test_assign_equal(self):
        t1 = parse("a=b")
        t2 = parse("a=b")
        self.assertEqual(t1.compare(t2), True)

    def test_assign_different(self):
        t1 = parse("a=b")
        t2 = parse("c=d")
        self.assertNotEqual(t1.compare(t2), True)

    def test_assign_another_node(self):
        t1 = parse("a=b")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_assign_another_type(self):
        t1 = parse("a=b")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_assign_equal(self):
        t1 = GenericAssign()
        t2 = parse("a=b").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_assign_another_node(self):
        t1 = GenericAssign()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_assign_another_type(self):
        t1 = GenericAssign()
        t2 = 0
        self.assertRaises(TypeError)

    def test_ann_assign_equal(self):
        t1 = parse("a : int =b")
        t2 = parse("a : int =b")
        self.assertEqual(t1.compare(t2), True)

    def test_ann_assign_different(self):
        t1 = parse("a : int =b")
        t2 = parse("c : int =d")
        self.assertNotEqual(t1.compare(t2), True)

    def test_ann_assign_another_node(self):
        t1 = parse("a : int =b")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_ann_assign_another_type(self):
        t1 = parse("a : int =b")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_ann_assign_equal(self):
        t1 = GenericAnnAssign()
        t2 = parse("a : int =b").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_ann_assign_another_node(self):
        t1 = GenericAnnAssign()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_ann_assign_another_type(self):
        t1 = GenericAnnAssign()
        t2 = 0
        self.assertRaises(TypeError)

    def test_aug_assign_equal(self):
        t1 = parse("a+=1")
        t2 = parse("a+=1")
        self.assertEqual(t1.compare(t2), True)

    def test_aug_assign_different(self):
        t1 = parse("a+=1")
        t2 = parse("b+=2")
        self.assertNotEqual(t1.compare(t2), True)

    def test_aug_assign_another_node(self):
        t1 = parse("a+=1")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_aug_assign_another_type(self):
        t1 = parse("a+=1")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_aug_assign_equal(self):
        t1 = GenericAugAssign()
        t2 = parse("a+=1").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_aug_assign_another_node(self):
        t1 = GenericAugAssign()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_aug_assign_another_type(self):
        t1 = GenericAugAssign()
        t2 = 0
        self.assertRaises(TypeError)

    def test_raise_equal(self):
        t1 = parse("raise TypeError")
        t2 = parse("raise TypeError")
        self.assertEqual(t1.compare(t2), True)

    def test_raise_different(self):
        t1 = parse("raise TypeError")
        t2 = parse("raise SyntaxError")
        self.assertNotEqual(t1.compare(t2), True)

    def test_raise_another_node(self):
        t1 = parse("raise TypeError")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_raise_another_type(self):
        t1 = parse("raise TypeError")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_raise_equal(self):
        t1 = GenericRaise()
        t2 = parse("raise TypeError").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_raise_another_node(self):
        t1 = GenericRaise()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_raise_another_type(self):
        t1 = GenericRaise()
        t2 = 0
        self.assertRaises(TypeError)

    def test_assert_equal(self):
        t1 = parse("assert (a > 10), 'error'")
        t2 = parse("assert (a > 10), 'error'")
        self.assertEqual(t1.compare(t2), True)

    def test_assert_different(self):
        t1 = parse("assert (a > 10), 'error'")
        t2 = parse("assert (b < 10), 'wrong'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_assert_another_node(self):
        t1 = parse("assert (a > 10), 'error'")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_assert_another_type(self):
        t1 = parse("assert (a > 10), 'error'")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_assert_equal(self):
        t1 = GenericAssert()
        t2 = parse("assert (a > 10), 'error'").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_assert_another_node(self):
        t1 = GenericAssert()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_assert_another_type(self):
        t1 = GenericAssert()
        t2 = 0
        self.assertRaises(TypeError)

    def test_del_equal(self):
        t1 = parse("del x,y")
        t2 = parse("del x,y")
        self.assertEqual(t1.compare(t2), True)

    def test_del_different(self):
        t1 = parse("del x, y")
        t2 = parse("del a, b")
        self.assertNotEqual(t1.compare(t2), True)

    def test_del_another_node(self):
        t1 = parse("del x, y")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_del_another_type(self):
        t1 = parse("del x, y")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_del_equal(self):
        t1 = GenericDelete()
        t2 = parse("del x, y").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_del_another_node(self):
        t1 = GenericDelete()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_del_another_type(self):
        t1 = GenericDelete()
        t2 = 0
        self.assertRaises(TypeError)

    def test_pass_equal(self):
        t1 = parse("pass")
        t2 = parse("pass")
        self.assertEqual(t1.compare(t2), True)

    def test_pass_another_node(self):
        t1 = parse("pass")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_pass_another_type(self):
        t1 = parse("pass")
        t2 = 0
        self.assertRaises(TypeError)

    def test_import_equal(self):
        t1 = parse("import x")
        t2 = parse("import x")
        self.assertEqual(t1.compare(t2), True)

    def test_import_different(self):
        t1 = parse("import x")
        t2 = parse("import y")
        self.assertNotEqual(t1.compare(t2), True)

    def test_import_another_node(self):
        t1 = parse("import x")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_import_another_type(self):
        t1 = parse("import x")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_import_equal(self):
        t1 = GenericImport()
        t2 = parse("import x").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_import_another_node(self):
        t1 = GenericImport()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_import_another_type(self):
        t1 = GenericImport()
        t2 = 0
        self.assertRaises(TypeError)

    def test_import_from_equal(self):
        t1 = parse("from x import y")
        t2 = parse("from x import y")
        self.assertEqual(t1.compare(t2), True)

    def test_import_from_different(self):
        t1 = parse("from x import y")
        t2 = parse("from a import b")
        self.assertNotEqual(t1.compare(t2), True)

    def test_import_from_another_node(self):
        t1 = parse("from x import y")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_import_from_another_type(self):
        t1 = parse("from x import y")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_import_from_equal(self):
        t1 = GenericImportFrom()
        t2 = parse("from x import y").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_import_from_another_node(self):
        t1 = GenericImportFrom()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_import_from_another_type(self):
        t1 = GenericImportFrom()
        t2 = 0
        self.assertRaises(TypeError)

    def test_if_equal(self):
        t1 = parse("if (a==b):\n    f(x)\nelse: pass")
        t2 = parse("if (a==b):\n    f(x)\nelse: pass")
        self.assertEqual(t1.compare(t2), True)

    def test_if_different(self):
        t1 = parse("if (a==b):\n    f(x)\nelse: pass")
        t2 = parse("if (c==d):\n    g(y)\nelse: pass")
        self.assertNotEqual(t1.compare(t2), True)

    def test_if_another_node(self):
        t1 = parse("if (a==b):\n    f(x)\nelse: pass")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_if_another_type(self):
        t1 = parse("if (a==b):\n    f(x)\nelse: pass")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_if_equal(self):
        t1 = GenericIf()
        t2 = parse("if (a==b):\n    f(x)\nelse: pass").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_if_another_node(self):
        t1 = GenericIf()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_if_another_type(self):
        t1 = GenericIf()
        t2 = 0
        self.assertRaises(TypeError)

    def test_for_equal(self):
        t1 = parse("for a in b:\n    f(x)\nelse: pass")
        t2 = parse("for a in b:\n    f(x)\nelse: pass")
        self.assertEqual(t1.compare(t2), True)

    def test_for_different(self):
        t1 = parse("for a in b:\n    f(x)\nelse: pass")
        t2 = parse("for c in d:\n    g(y)\nelse: pass")
        self.assertNotEqual(t1.compare(t2), True)

    def test_for_another_node(self):
        t1 = parse("for a in b:\n    f(x)\nelse: pass")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_for_another_type(self):
        t1 = parse("for a in b:\n    f(x)\nelse: pass")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_for_equal(self):
        t1 = GenericFor()
        t2 = parse("for a in b:\n    f(x)\nelse: pass").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_for_another_node(self):
        t1 = GenericFor()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_for_another_type(self):
        t1 = GenericFor()
        t2 = 0
        self.assertRaises(TypeError)

    def test_while_equal(self):
        t1 = parse("while a == b:\n    f(x)\nelse: pass")
        t2 = parse("while a == b:\n    f(x)\nelse: pass")
        self.assertEqual(t1.compare(t2), True)

    def test_while_different(self):
        t1 = parse("while a == b:\n    f(x)\nelse: pass")
        t2 = parse("while c == d:\n    g(y)\nelse: pass")
        self.assertNotEqual(t1.compare(t2), True)

    def test_while_another_node(self):
        t1 = parse("while a == b:\n    f(x)\nelse: pass")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_while_another_type(self):
        t1 = parse("while a == b:\n    f(x)\nelse: pass")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_while_equal(self):
        t1 = GenericWhile()
        t2 = parse("while a == b:\n    f(x)\nelse: pass").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_while_another_node(self):
        t1 = GenericWhile()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_while_another_type(self):
        t1 = GenericWhile()
        t2 = 0
        self.assertRaises(TypeError)

    def test_break_equal(self):
        t1 = parse("break")
        t2 = parse("break")
        self.assertEqual(t1.compare(t2), True)

    def test_break_another_node(self):
        t1 = parse("break")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_break_another_type(self):
        t1 = parse("break")
        t2 = 0
        self.assertRaises(TypeError)

    def test_continue_equal(self):
        t1 = parse("continue")
        t2 = parse("continue")
        self.assertEqual(t1.compare(t2), True)

    def test_continue_another_node(self):
        t1 = parse("continue")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_continue_another_type(self):
        t1 = parse("continue")
        t2 = 0
        self.assertRaises(TypeError)

    def test_try_equal(self):
        t1 = parse("try:\n  f(x)\nexcept Exception as e:\n  pass\nfinally:\n return")
        t2 = parse("try:\n  f(x)\nexcept Exception as e:\n  pass\nfinally:\n return")
        self.assertEqual(t1.compare(t2), True)

    def test_try_different(self):
        t1 = parse("try:\n  f(x)\nexcept Exception as e:\n  pass\nfinally:\n return")
        t2 = parse("try:\n  f(x)\nfinally:\n return")
        self.assertNotEqual(t1.compare(t2), True)

    def test_try_another_node(self):
        t1 = parse("try:\n  f(x)\nexcept Exception as e:\n  pass\nfinally:\n return")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_try_another_type(self):
        t1 = parse("try:\n  f(x)\nexcept Exception as e:\n  pass\nfinally:\n return")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_try_equal(self):
        t1 = GenericTry()
        t2 = parse("try:\n  f(x)\nexcept Exception as e:\n  pass\nfinally:\n return").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_try_another_node(self):
        t1 = GenericTry()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_try_another_type(self):
        t1 = GenericTry()
        t2 = 0
        self.assertRaises(TypeError)

    def test_with_equal(self):
        t1 = parse("with a as b:\n  c")
        t2 = parse("with a as b:\n  c")
        self.assertEqual(t1.compare(t2), True)

    def test_with_different(self):
        t1 = parse("with a as b:\n  c")
        t2 = parse("with d:\n   e")
        self.assertNotEqual(t1.compare(t2), True)

    def test_with_another_node(self):
        t1 = parse("with a as b:\n  c")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_with_another_type(self):
        t1 = parse("with a as b:\n  c")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_with_equal(self):
        t1 = GenericWith()
        t2 = parse("with a as b:\n  c").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_with_another_node(self):
        t1 = GenericWith()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_with_another_type(self):
        t1 = GenericWith()
        t2 = 0
        self.assertRaises(TypeError)

    def test_function_def_equal(self):
        t1 = parse("def f(x, y=a):\n    return g(z)")
        t2 = parse("def f(x, y=a):\n    return g(z)")
        self.assertEqual(t1.compare(t2), True)

    def test_function_def_different(self):
        t1 = parse("def f(x, y=a):\n    return g(z)")
        t2 = parse("def h(q, w=b):\n    return")
        self.assertNotEqual(t1.compare(t2), True)

    def test_function_def_another_node(self):
        t1 = parse("def f(x, y=a):\n    return g(z)")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_function_def_another_type(self):
        t1 = parse("def f(x, y=a):\n    return g(z)")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_function_def_equal(self):
        t1 = GenericFunctionDef()
        t2 = parse("def f(x, y=a):\n    return g(z)").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_function_def_another_node(self):
        t1 = GenericFunctionDef()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_function_def_another_type(self):
        t1 = GenericFunctionDef()
        t2 = 0
        self.assertRaises(TypeError)

    def test_lambda_equal(self):
        t1 = parse("lambda a : a + 10")
        t2 = parse("lambda a : a + 10")
        self.assertEqual(t1.compare(t2), True)

    def test_lambda_different(self):
        t1 = parse("lambda a : a + 10")
        t2 = parse("lambda a, b : a * b")
        self.assertNotEqual(t1.compare(t2), True)

    def test_lambda_another_node(self):
        t1 = parse("lambda a, b : a * b")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_lambda_another_type(self):
        t1 = parse("lambda a, b : a * b")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_lambda_equal(self):
        t1 = GenericLambda()
        t2 = parse("lambda a, b : a * b").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_lambda_another_node(self):
        t1 = GenericLambda()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_lambda_another_type(self):
        t1 = GenericLambda()
        t2 = 0
        self.assertRaises(TypeError)

    def test_return_equal(self):
        t1 = parse("return x")
        t2 = parse("return x")
        self.assertEqual(t1.compare(t2), True)

    def test_return_different(self):
        t1 = parse("return x")
        t2 = parse("return")
        self.assertNotEqual(t1.compare(t2), True)

    def test_return_another_node(self):
        t1 = parse("return x")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_return_another_type(self):
        t1 = parse("return x")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_return_equal(self):
        t1 = GenericReturn()
        t2 = parse("return x").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_return_another_node(self):
        t1 = GenericReturn()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_return_another_type(self):
        t1 = GenericReturn()
        t2 = 0
        self.assertRaises(TypeError)

    def test_yield_equal(self):
        t1 = parse("yield i*i")
        t2 = parse("yield i*i")
        self.assertEqual(t1.compare(t2), True)

    def test_yield_different(self):
        t1 = parse("yield i*i")
        t2 = parse("yield a-b")
        self.assertNotEqual(t1.compare(t2), True)

    def test_yield_another_node(self):
        t1 = parse("yield i*i")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_yield_another_type(self):
        t1 = parse("yield i*i")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_yield_equal(self):
        t1 = GenericYield()
        t2 = parse("yield i*i").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_yield_another_node(self):
        t1 = GenericYield()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_yield_another_type(self):
        t1 = GenericYield()
        t2 = 0
        self.assertRaises(TypeError)

    def test_yield_from_equal(self):
        t1 = parse("yield from range(x)")
        t2 = parse("yield from range(x)")
        self.assertEqual(t1.compare(t2), True)

    def test_yield_from_different(self):
        t1 = parse("yield from range(x)")
        t2 = parse("yield from range(x, 0, -1)")
        self.assertNotEqual(t1.compare(t2), True)

    def test_yield_from_another_node(self):
        t1 = parse("yield from range(x, 0, -1)")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_yield_from_another_type(self):
        t1 = parse("yield from range(x, 0, -1)")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_yield_from_equal(self):
        t1 = GenericYieldFrom()
        t2 = parse("yield from range(x, 0, -1)").body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_yield_from_another_node(self):
        t1 = GenericYieldFrom()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_yield_from_another_type(self):
        t1 = GenericYieldFrom()
        t2 = 0
        self.assertRaises(TypeError)

    def test_global_equal(self):
        t1 = parse("global x,y")
        t2 = parse("global x,y")
        self.assertEqual(t1.compare(t2), True)

    def test_global_different(self):
        t1 = parse("global x,y")
        t2 = parse("global z,q,w")
        self.assertNotEqual(t1.compare(t2), True)

    def test_global_another_node(self):
        t1 = parse("global x,y")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_global_another_type(self):
        t1 = parse("global x,y")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_global_equal(self):
        t1 = GenericGlobal()
        t2 = parse("global x,y").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_global_another_node(self):
        t1 = GenericGlobal()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_global_another_type(self):
        t1 = GenericGlobal()
        t2 = 0
        self.assertRaises(TypeError)

    def test_nonlocal_equal(self):
        t1 = parse("nonlocal x,y")
        t2 = parse("nonlocal x,y")
        self.assertEqual(t1.compare(t2), True)

    def test_nonlocal_different(self):
        t1 = parse("nonlocal x,y")
        t2 = parse("nonlocal x")
        self.assertNotEqual(t1.compare(t2), True)

    def test_nonlocal_another_node(self):
        t1 = parse("nonlocal x,y")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_nonlocal_another_type(self):
        t1 = parse("nonlocal x,y")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_nonlocal_equal(self):
        t1 = GenericNonlocal()
        t2 = parse("nonlocal x,y").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_nonlocal_another_node(self):
        t1 = GenericNonlocal()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_nonlocal_another_type(self):
        t1 = GenericNonlocal()
        t2 = 0
        self.assertRaises(TypeError)

    def test_class_def_equal(self):
        t1 = parse("class c(base):\n  x=y\nf(x)")
        t2 = parse("class c(base):\n  x=y\nf(x)")
        self.assertEqual(t1.compare(t2), True)

    def test_class_def_different(self):
        t1 = parse("class c(base):\n  x=y\nf(x)")
        t2 = parse("class b(base_2, base_3):\n  h(y)\nreturn a")
        self.assertNotEqual(t1.compare(t2), True)

    def test_class_def_another_node(self):
        t1 = parse("class c(base):\n  x=y\nf(x)")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_class_def_another_type(self):
        t1 = parse("class c(base):\n  x=y\nf(x)")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_class_def_equal(self):
        t1 = GenericClassDef()
        t2 = parse("class c(base):\n  x=y\nf(x)").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_class_def_another_node(self):
        t1 = GenericClassDef()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_class_def_another_type(self):
        t1 = GenericClassDef()
        t2 = 0
        self.assertRaises(TypeError)

    def test_async_function_def_equal(self):
        t1 = parse("async def c(base):\n  x=y\nf(x)")
        t2 = parse("async def c(base):\n  x=y\nf(x)")
        self.assertEqual(t1.compare(t2), True)

    def test_async_function_def_different(self):
        t1 = parse("async def c(base):\n  x=y\nf(x)")
        t2 = parse("async def b():\n  h(y)\nreturn a")
        self.assertNotEqual(t1.compare(t2), True)

    def test_async_function_def_another_node(self):
        t1 = parse("async def c(base):\n  x=y\nf(x)")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_async_function_def_another_type(self):
        t1 = parse("async def c(base):\n  x=y\nf(x)")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_async_function_def_equal(self):
        t1 = GenericAsyncFunctionDef()
        t2 = parse("async def c(base):\n  x=y\nf(x)").body[0]
        self.assertEqual(t1.compare(t2), True)

    def test_generic_async_function_def_another_node(self):
        t1 = GenericAsyncFunctionDef()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_async_function_def_another_type(self):
        t1 = GenericAsyncFunctionDef()
        t2 = 0
        self.assertRaises(TypeError)

    def test_await_equal(self):
        t1 = parse("async def f(x):\n  await h(a)")
        t2 = parse("async def f(x):\n  await h(a)")
        self.assertEqual(t1.compare(t2), True)

    def test_await_different(self):
        t1 = parse("async def f(x):\n  await h(a)")
        t2 = parse("async def k(y):\n  await l(b)\nreturn x")
        self.assertNotEqual(t1.compare(t2), True)

    def test_await_another_node(self):
        t1 = parse("async def f(x):\n  await h(a)")
        t2 = parse("'s'")
        self.assertNotEqual(t1.compare(t2), True)

    def test_await_another_type(self):
        t1 = parse("async def f(x):\n  await h(a)")
        t2 = 0
        self.assertRaises(TypeError)

    def test_generic_await_equal(self):
        t1 = GenericAwait()
        t2 = parse("async def f(x):\n  await h(a)").body[0].body[0].value
        self.assertEqual(t1.compare(t2), True)

    def test_generic_await_another_node(self):
        t1 = GenericAwait()
        t2 = parse("'s'").body[0]
        self.assertNotEqual(t1.compare(t2), True)

    def test_generic_await_another_type(self):
        t1 = GenericAwait()
        t2 = 0
        self.assertRaises(TypeError)


if __name__ == '__main__':
    unittest.main()