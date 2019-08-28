class Block:
    def __init__(self, *subblocks):
        self.components = []
        for x in subblocks:
            self.components.append(x)



class IfBlock:
    def __init__(self, if_stmnt, *subblocks):

class ForBlock:
    def __init__(self, for_stmnt, *subblocks):
        self.for_stmnt = for_stmnt
        self.components = []
        for x in subblocks:
            self.components.append(x)

class WhileBlock:
    def __init__(self, while_stmnt, *subblocks):



