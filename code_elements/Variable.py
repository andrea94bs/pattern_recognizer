class Variable:
    def __init__(self, var_name, **attributes_names):
        self.name = var_name
        self.attribute_variables = attributes_names

    def getName(self):
        return self.name

    def getAttributes(self):
        return self.attribute_variables

    def toString(self):
        s = self.name
        for x in self.attribute_variables:
            s.append('.' + x)
        return s