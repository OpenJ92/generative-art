from src.typeclass.__function__ import __Function__

def Cylinder(__Function__):
    def __init__(self, instructions):
        ## Instructions determine the form of the cylinder. For example
        ## CL -> [Cosx, Sinx, r]. We need to consider how we might produce
        ## such a string. 
        self.instructions = instructions
