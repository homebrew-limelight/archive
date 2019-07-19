from dataclasses import dataclass
from function import Function
from litegraph import LiteGraph, LiteGraphPipeline
from litegraph_example import BASIC_SUM
from manager import Manager


class Five(Function):
    has_sideeffect = False
    require_restart = frozenset()

    @dataclass
    class Inputs:
        pass

    @dataclass
    class Outputs:
        five: int

    def __call__(self, inputs):
        return self.Outputs(five=5)


class Sum(Function):
    has_sideeffect = False
    require_restart = frozenset()

    @dataclass
    class Inputs:
        num1: int
        num2: int

    @dataclass
    class Outputs:
        out: int

    def __call__(self, inputs):
        out = inputs.num1 + inputs.num2
        print(out)
        return self.Outputs(out=out)


class Print(Function):
    has_sideeffect = True
    require_restart = frozenset()

    @dataclass
    class Inputs:
        val: int

    @dataclass
    class Outputs:
        pass

    def __call__(self, inputs):
        print(f"Print node: {inputs.val}")

        return self.Outputs()


m = Manager()
m.register(Five, Sum, Print)

# p = Pipeline(m)
# b = p.create_node_raw(fullname(Box), Box.Settings)
# c = p.create_node_raw(fullname(BBox), Box.Settings)
# d = p.create_node_raw(fullname(BBox), Box.Settings)
#
# p.connect_node(b, c, {"A": "B"})
# p.connect_node(b, d, {"A": "B"})
#
# p.run_pipeline()

a = LiteGraph.make(BASIC_SUM)
b = LiteGraphPipeline.from_litegraph(m, a)

b.run_pipeline()
