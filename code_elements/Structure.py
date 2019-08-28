from abc import abstractmethod

class Structure:
    def __init__(self, body):
        self.body = body
    @abstractmethod
    def getBody(self):
        return self.body
