class Assignment:
    def __init__(self, v_1, v_2):
        self.v_1 = v_1
        self.v_2 = v_2

    def getAntecedent(self):
        return self.v_1

    def getConsequent(self):
        return self.v_2

    def toString(self):
        return (self.getAntecedent() + '=' + self.getConsequent())