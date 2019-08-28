class Assignment:
    def __init__(self, *var_1, var_2):
        self.var_1 = var_1
        self.var_2 = var_2

    def get_var_1(self):
        return self.var_1

    def get_var_2(self):
        return self.var_2

class ForStmnt:
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

class IfStmnt:
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent