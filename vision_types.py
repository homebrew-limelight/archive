from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)

import numpy as np
from pydantic import BaseModel, Schema, create_model, confloat, conint


# Note: using NewType with np.ndarray requires numpy type stubs
# Currently located in stubs/numpy/__init__.pyi

# # shape: (x, y, 3); dtype: uint8; color format: BGR
# Mat = NewType("Mat", np.ndarray)

# # shape: (x, y); dtype: uint8 (0 or 255); color format: Gray
# MatBW = NewType("MatBW", np.ndarray)

# # shape: (1, x, 4); dtype: int32
# Contour = NewType("Contour", np.ndarray)


class Mat(np.ndarray):
    pass


class Contour(np.ndarray):
    pass


"""
Table for RangeType
Where F = Elipsis (...)
(max_val, start_max)
(F, ?): no exists
(x, F): possible max <= x; default = x
(x, y): possible max <= x; default = y
(x, N): possible max <= x; default = None
(N, y): possible max any ; default = y
(N, F): possible max any ; default = None
(N, N): Same as (N, F)
"""

# I give up trying to put `# type: ignore` on everything
def range_type(
    name: str,
    min_val: Optional[float] = ...,  # If ...: exclude option
    max_val: Optional[float] = ...,
    *,
    start_min: Optional[float] = ...,  # If not ...: set as default
    start_max: Optional[float] = ...,
    wanted_type: Type[Union[int, float]] = float,  # one of: (float, int)
    return_object: bool = True  # if False, return new class
):
    # Convert min and max to wanted type; common params to both min and max schema params

    schema_options = {}
    if min_val not in (..., None):
        schema_options["ge"] = wanted_type(min_val)
    if max_val not in (..., None):
        schema_options["le"] = wanted_type(max_val)

    defined_type = {float: confloat, int: conint}[wanted_type](**schema_options)

    if None in (min_val, max_val, start_min, start_max):
        defined_type = Optional[defined_type]

    # Create schema

    options: Dict[str, Tuple[Type, Schema]] = {}
    if min_val is not ...:
        if min_val is not None:
            default = wanted_type(min_val)
        else:
            default = wanted_type(start_min) if start_min not in (..., None) else None
        options["min"] = (defined_type, Schema(default, **schema_options))

    if max_val is not ...:
        if max_val is not None:
            default = wanted_type(max_val)
        else:
            default = wanted_type(start_max) if start_max not in (..., None) else None
        options["max"] = (defined_type, Schema(default, **schema_options))

    # Create anonymous class
    cls = create_model(model_name=name, **options)

    if return_object:
        # Create instance of the new class
        return cls()
    return cls