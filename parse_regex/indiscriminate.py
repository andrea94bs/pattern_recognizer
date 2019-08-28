import ast
from FSA.test import MyVisitor


class State:
    def __init__(self):
        pass
    def run(input):
        pass

class Q1(State):
    def __init__(self):
        self.name="q1"
        self.isfinal = 0
    def run(self, input):
        if isinstance(input, ast.Assign):
            return Q2(), input
        else:
            return Q1(), None

class Q2(State):
    def __init__(self):
        self.name="q2"
        self.isfinal = 1
    def run(self, input):
        return 'end'

class Fsa:
    def __init__(self, initial):
        self.initial = initial

    def run(self, input):
        pattern = []
        current = self.initial
        for line in input:
            r = current.run(input)
            if r == 'end':
                print(pattern)
            else:
                pattern.append(input)
                print(pattern)
                current = r[0]

if __name__ == '__main__':
    input = open('test_file.py', 'r').read()
    input = ast.parse(input)
    # MyTransformer().visit(car_controller)
    # pattern = IndiscriminateFollow()
    # pattern_root = pattern.root
    input = MyVisitor().visit(input)

    q1 = Q1()
    q2 = Q2()
    fsa = Fsa(q1)
    fsa.run(input)
