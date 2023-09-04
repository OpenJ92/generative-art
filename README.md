# generative-art

generative-art is a python svg generation suite. It models the act of making a parameterized mathematical forms in any real space using numpy ndarrays at it's base. Works generated here have been displayed in the New York Metropolitan Area.

### TODO
- ~~construct \_\_Function\_\_~~
    - ~~implement Hypercube~~
    - ~~implement Hypersphere~~
    - ~~implement Bezier~~
- ~~construct \_\_Sculpture\_\_~~
- ~~construct \_\_Data\_\_~~
- construct \_\_Camera\_\_ 
- construct \_\_Enviornment\_\_
- construct \_\_Photograph\_\_ 
- construct \_\_Video\_\_
- ~~construct \_\_Generation\_\_~~
- integrate Mediapipe MLAs
- integrate OpenCV
- integrate multiprocessing

# [py-gen](/py-gen)
- [functions](/py-gen/src/functions)
    
    > functions classes inherit from the typeclass [\_\_Function\_\_](py-gen/src/typeclass/__function__.py) which require definitions on `__call__` and `__call_data__`. These operate on numpy ndarrays or [\_\_Data\_\_](/py-gen/src/atoms.py) respectively and are used primarily in the [\_\_Sculpture\_\_](py-gen/src/typeclass/__sculpture__.py) class.
- [sculptures](py-gen/src/sculptures)
    
    > Sculptures are the basic units of construction for any generative work done in the program. Examples that utilize the system well include those found in the [unitcube.py](py-gen/src/sculptures/unitcube.py) and [unitplane.py](py-gen/src/sculptures/unitplane.py). Sculptures have no constraints on form so long as the output is of the class [\_\_Sculpture\_\_](py-gen/src/typeclass/__sculpture__.py).
- [typeclass](py-gen/src/typeclass)
    
    > Typeclass forms are ABC classes which the above forms inherit from to enforce method definitions for submission to more generic classes like [\_\_Sculpture\_\_](py-gen/src/typeclass/__sculpture__.py) class and upcoming \_\_Camera\_\_, \_\_Enviornment\_\_, \_\_Photograph\_\_ and \_\_Video\_\_ classes.
