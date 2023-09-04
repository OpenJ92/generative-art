from __future__ import annotations
from perlin_noise import PerlinNoise
from numpy import array

from src.typeclass.__function__ import __Function__

## These all need a normalization strategy on the __call_data__ layer. that
## strategy must be invertable. (remember to add that to the typeclass folder).
## inherit where applicable. What's more, we have to make a Random typeclass
## that enables up to sample functions at random

## Rn -> R1
class Perlin_Noise(__Function__):
    def __init__(self, octave, seed):
        self.octave = octave
        self.seed = seed
        self.perline_noise = PerlinNoise(self.octave)

    def __call__(self, ts: array):
        return self.perline_noise(ts)


## Rn -> R1
class Perlin_Stack(__Function__):
    def __init__(self, proportions, octaves, seeds):
        self.proportions = proportions
        self.octaves = octaves
        self.seeds = seeds

    def __call__(self, ts: array):
        perlins = map(lambda octseed: Perlin_Noise(*octseed), zip(self.octaves, self.seeds))
        retval = 0
        for prop, perlin in zip(self.proportions, perlins):
            retval += retval + prop*perlin(ts)
        return retval

Perlin = Perlin_Noise | Perlin_Stack

## Rn -> Rm transform
class Perlin_Vector(__Function__):
    def __init__(self, perlins):
        self.perlins = perlins

    def __call__(self, ts: array):
        return array(list(map(lambda perlin: perlin(ts), self.perlins)))
