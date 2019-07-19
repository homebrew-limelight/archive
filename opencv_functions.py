from dataclasses import dataclass
from enum import Enum
import cv2
import pydantic
from pydantic import BaseModel

from function import Function
from vision_types import Mat


class BlurType(Enum):
    BOX = 1
    GAUSSIAN = 2
    MEDIAN = 3
    BILATERAL = 4


class Blur(Function):
    has_sideeffect = False
    require_restart = frozenset()

    @dataclass
    class Settings:
        blurType: BlurType
        value: int
        
    @dataclass
    class Inputs:
        image: Mat

    @dataclass
    class Outputs:
        image: Mat

    def __call__(self, inputs):
        ksize = 2 * inputs.radius + 1
        if type is BlurType.BOX:
            return Blur.Outputs(image=cv2.blur(inputs.image, (ksize, ksize)))
        elif type is BlurType.GAUSSIAN:
            return Blur.Outputs(image=cv2.GaussianBlur(inputs.image, (ksize, ksize)))
        elif type is BlurType.MEDIAN:
            return Blur.Outputs(image=cv2.medianBlur(inputs.image, ksize))
        else:
            return Blur.Outputs(image=cv2.bilateralFilter(inputs.image, ksize))
