from dataclasses import dataclass
from pydantic.dataclasses import dataclass as pydataclass
from function import Function
from manager import Manager, Pipeline, fullname


class Box(Function):
    @pydataclass
    class Settings:
        pass

    @dataclass
    class Inputs:
        pass

    @dataclass
    class Outputs:
        A: int

    def process(self, inputs):
        print("A")
        return Box.Outputs(5)


class BBox(Function):
    @pydataclass
    class Settings:
        pass

    @dataclass
    class Inputs:
        B: int
        pass

    @dataclass
    class Outputs:
        pass

    def process(self, inputs):
        print(inputs.B)
        pass


m = Manager()
m.register(Box)
m.register(BBox)

p = Pipeline(m)
b = p.create_node(fullname(Box), Box.Settings)
c = p.create_node(fullname(BBox), Box.Settings)

p.connect_node(b, c, {"A": "B"})

p.run_pipeline()
