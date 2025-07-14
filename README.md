# Generative Art

This repository hosts **py-gen**, a Python suite for algorithmic art. The code treats every drawing as a data pipeline:

1. **Data** – geometric primitives such as points, segments or triangles defined in `src/atoms.py`.
2. **Functions** – transformations that operate on data arrays. These live under `src/functions` and implement the `Function` typeclass.
3. **Sculptures** – pair a data object with a function in order to produce new data through the `Sculpture` executor.
4. **Executors and Helpers** – modules that run sculptures, apply kinetic updates and ultimately write SVG output.

By chaining these stages together, `py-gen` can take basic numeric inputs and progressively transform them into complex shapes ready for rendering or further manipulation.

### Repository Layout

- `py-gen/src/atoms.py` – core data definitions for primitives and composites.
- `py-gen/src/functions/` – collection of mathematical operations used to transform data.
- `py-gen/src/sculptures/` – examples of sculptures built from data and functions.
- `py-gen/src/typeclass/` – abstract base classes providing the pipeline interfaces.

See [`__main__.py`](py-gen/__main__.py) for a minimal entry point.
