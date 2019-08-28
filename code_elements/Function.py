class Function:
    def  __init__(self, *parameters, name):
        self.name = name
        self.parameters = parameters

    def getName(self):
        return self.name

    def getParameters(self):
        return self.parameters