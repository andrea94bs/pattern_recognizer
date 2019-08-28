from abc import ABC, abstractmethod

class LogicalFunction(ABC):
    def __init__(self, *operands):
        self.operands = operands

    @abstractmethod
    def getOperands(self):
        pass

    @abstractmethod
    def getOperator(self):
        pass

class OrFunction(LogicalFunction):
    def __init__(self, *operands):
        super(OrFunction, self).__init__(operands)
        self.operator = 'OR'