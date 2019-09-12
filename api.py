from fastapi import FastAPI
from pydantic import BaseModel, Schema, create_model, conint, confloat
from typing import Any, Dict, Optional, Tuple, Type, Union, cast
from pprint import pprint

# Install all packages with `pip install fastapi[all]`


app = FastAPI()


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
def RangeType(
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


class Settings(BaseModel):
    class Blur(BaseModel):
        enable: bool = True
        strength: conint(ge=0) = 10

    blur = Blur()

    class Threshold(BaseModel):
        enable: bool = False
        hue = RangeType("Hue", 0, 180)
        sat = RangeType("Sat", 0, 255)
        lum = RangeType("Lum", 0, 255)

    threshold = Threshold()

    class Morph(BaseModel):  # Morph stands for Morphological Transformations
        enable: bool = True
        erode: conint(ge=0) = 5
        dilate: conint(ge=0) = 5
        erode_before_dilate: bool = True

    morph = Morph()

    class ContourFiltering(BaseModel):
        area = RangeType("Area", 0, None, start_min=None)
        perimeter = RangeType("Perimeter", 0, None, start_min=None)
        width = RangeType("Width", 0, None, start_min=None)
        height = RangeType("Height", 0, None, start_min=None)
        solidity = RangeType("Solidity", 0, 100, start_min=None, start_max=None)
        vertex_count = RangeType(
            "VertexCount", 0, None, start_min=None, wanted_type=int
        )
        ratio = RangeType("Ratio", 0, None, start_min=None)

    contours = ContourFiltering()


global_settings = Settings()


@app.get("/", response_model=Settings)
def read_settings():
    return global_settings


@app.put("/")
def update_settings(settings_in: Settings):
    global global_settings
    global_settings = settings_in
    return settings_in.json(skip_defaults=True)


# Better way to run: `uvicorn api:app --reload`
if __name__ == "__main__":
    import uvicorn

    print("Go to http://127.0.0.1:8000/docs")

    uvicorn.run(app)
