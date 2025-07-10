from __future__ import annotations
from perlin_noise import PerlinNoise
from numpy import array, square
from numpy.random import randint, rand

from src.functions.sphere import Sphere
from src.typeclass import Function, Random

## These all need a normalization strategy on the call_data layer. that
## strategy must be invertable. (remember to add that to the typeclass folder).
## inherit where applicable. What's more, we have to make a Random typeclass
## that enables up to sample functions at random


## Rn -> R1
class Perlin_Noise(Random, Function):
    def __init__(self, octave, seed, scale=1):
        self.octave = octave
        self.seed = seed
        self.scale = scale
        self.perline_noise = PerlinNoise(self.octave, self.seed)

    def __call__(self, ts: array):
        return self.scale * self.perline_noise(ts)

    @classmethod
    def random(cls):
        return cls(randint(low=1, high=20), randint(999999999), rand())


## Rn -> R1
class Perlin_Stack(Random, Function):
    def __init__(self, proportions, octaves, seeds):
        self.proportions = proportions
        self.octaves = octaves
        self.seeds = seeds

    def __call__(self, ts: array):
        perlins = []
        for octave, seed, proportion in  zip(self.octaves, self.seeds, self.proportions):
            perlins.append(Perlin_Noise(octave, int(seed), proportion))

        retval = 0
        for perlin in perlins:
            retval += retval + perlin(ts)
        return retval

    @classmethod
    def random(cls):
        size = randint(low=1, high=5)
        proportions = square(
            Sphere()(
                rand(
                    size,
                )
            )
        )
        octaves = randint(low=2, high=4, size=(size + 1,))
        seeds = randint(999999999, size=(size + 1,))
        return cls(proportions, octaves, seeds)


Perlin = Perlin_Noise | Perlin_Stack


## Rn -> Rm transform
class Perlin_Vector(Random, Function):
    def __init__(self, perlins):
        self.perlins = perlins

    def __call__(self, ts: array):
        return array(list(map(lambda perlin: perlin(ts), self.perlins)))

    @classmethod
    def random(cls):
        return lambda size: cls([Perlin_Stack.random() for _ in range(size)])
