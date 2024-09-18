from abc import ABC, abstractmethod

class Parser(__Applicative__, __Functor__, ABC):
    @abstractmethod
    ## __call__ :: (A) => String -> (A, String)
    def __call__(self, string):
        pass


class Get(Parser):
    def __call__(self, string):
        if not string: return None
        a, *string = string
        return (a, string)

class Character(Parser):
    def __init__(self, character):
        self.character = character

    def __call__(self, string):
        a, *string = string
        if a != self.character: return None
        return (a, string)

class Word(Parser):
    def __init__(self, word):
        self.word = word

    def __call__(self, string):
        output = []
        for character in self.word:
            match Character(character)(string):
                case (a, string):
                    output.append(a)
                case None:
                    return None
        return ("".join(output), string)
