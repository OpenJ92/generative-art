from src.typeclass import Function

class ReduceOverChunks(Function):
    def __init__(self, size, scales):
        self.size = size
        self.scales = scales

    ## def __call__(self, data : array):
    ##     ## retrieve data from Data and chunck into some 'chunk_size'
    ##     ## arrays and pad as needed. then take the dot product with
    ##     ## provided array of scales. The implementation I'm considering
    ##     ## is in size of 2 and scale of the square of elements of a 
    ##     ## hypersphere. Perhaps we'll 'realize' that form here for use
    ##     ## elsewhere. 
    ##     output = zeros((self.size))
    ##     for index in range(0, len(array), size):
    ##         output += scales[index//self.size]*data[index:index+size]

    ##     return output

    def __call__(self, data : array):
        ## retrieve data from Data and chunck into some 'chunk_size'
        ## arrays and pad as needed. then take the dot product with
        ## provided array of scales. The implementation I'm considering
        ## is in size of 2 and scale of the square of elements of a 
        ## hypersphere. Perhaps we'll 'realize' that form here for use
        ## elsewhere. 
        output = []
        for index in range(0, len(array), size):
            output.append(Point(data[index:index+size]))

        return output
