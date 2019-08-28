from code_elements.Structure import Structure

class IfStatement(Structure):
    def __init__(self, *expressions, body):
        self.expressions = []
        for x in expressions:
            self.expressions.append(x)
        self.body = body

    def getExpressions(self):
        return self.expressions

    def getBody(self):
        if self.body:
            return self.body
        return None
