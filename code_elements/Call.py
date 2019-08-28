class Call:
    def __init__(self, main_var, functionName, **attribute_vars):
        self.attribute_vars = attribute_vars
        self.main_var = main_var
        self.functionName = functionName

    def getFunction(self):
        return self.functionName

    def getMainVar(self):
        return self.main_var

    def getAttributeVars(self):
        return self.attribute_vars

    def toString(self):
        s = self.functionName
        for x in self.attribute_vars:
            s.append('.' + x)
        return s