# generative-art

## [py-gen](/py-gen)
- [functions](/py-gen/src/functions)
    
    functions classes inherit from the typeclass [\_\_Function\_\_](py-gen/src/typeclass/__function__.py) which require definitions on `__call__` and `__call_data__` which operate on numpy ndarrays or [\_\_Data\_\_](/py-gen/src/atoms.py) respectively. These objects are primarily used in the [\_\_Sculpture\_\_](py-gen/src/typeclass/__sculpture__.py) class.
- [sculptures](py-gen/src/sculptures)
    
    Sculptures are the basic units of construction for any generative work done in the program. Examples that utilize the system well include those found in the [unitcube.py](py-gen/src/sculptures/unitcube.py) and [unitplane.py](py-gen/src/sculptures/unitplane.py). Sculptures have no constraints on form so long as the output is of the class [\_\_Sculpture\_\_](py-gen/src/typeclass/__sculpture__.py).
- [typeclass](py-gen/src/typeclass)
    
    Typeclass forms are ABC classes which the above forms inherit from to enforce method definitions for submission to more generic classes like [\_\_Sculpture\_\_](py-gen/src/typeclass/__sculpture__.py) class and upcoming \_\_Enviornment\_\_, \_\_Photograph\_\_ and \_\_Video\_\_ classes.
