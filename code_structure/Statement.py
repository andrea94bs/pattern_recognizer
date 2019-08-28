class IfStmnt:
    def __init__(self, antecedent, consequent, operator):
        self.antecedent = antecedent
        self.consequent = consequent
        self.operator = operator

class ForStmnt:
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

class Assignment:
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

class ListComprehension:
    def __init__(self, variable, list, condition):
        self.variable = variable
        self.list = list
        self.condition = condition

