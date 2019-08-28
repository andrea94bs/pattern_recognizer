class Function:
    def __init__(self, name, *params):
        self.params = []
        self.name = name
        if params:
            for x in params:
                self.params.append(x)
