from fsa.Fsa2 import *
from parse_regex.parser import *
from inspect import *
import astor

s = open("program_test.py", 'r', encoding="utf-8")
p = open("pattern_program_test.py", 'r', encoding="utf-8")

x = s.read()
x = parse(x,first_iter=True)

y = p.read()
y = parse(y,with_ids=True, first_iter=True)
# print_program(y)
#
#
f = Fsa(y)

# print(f.memory_pattern)
result = f.run(x)
print(result)
# while state:
#     print(state)
#     state = state.next