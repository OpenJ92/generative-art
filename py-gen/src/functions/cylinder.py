from src.typeclass.function import Function

def Cylinder(Function):
    def __init__(self, instructions):
        ## Instructions determine the form of the cylinder. For example
        ## CL -> [Cosx, Sinx, r]. We need to consider how we might produce
        ## such a string. 
        self.instructions = instructions
