from collections import defaultdict
from dataclasses import fields, dataclass
from typing import Dict, Type, Set, Iterable, Mapping, Any
from function import Function


def fullname(cls: type) -> str:
    return cls.__name__


class Node:
    def __init__(self, function: Function):
        self.function: Function = function
        self.inputs: Dict[Node, Dict[str, str]] = defaultdict(lambda: dict())
        self.taken_inputs: Set[str] = set()

        self.input_class: Type[dataclass] = type(self.function).Inputs
        self.output_class: Type[dataclass] = type(self.function).Outputs

        self.input_class_field_names: Set[str] = {x.name for x in fields(self.input_class)}
        self.output_class_field_names: Set[str] = {x.name for x in fields(self.output_class)}

    def __call__(self, inputs):
        return self.function(inputs)

    def add_input(self, data_node: "Node", args: Mapping[str, str]) -> None:
        all_args = set(args.values())

        intersection = self.taken_inputs & all_args
        if intersection:
            raise ValueError(f"repeated args: {intersection}")

        difference = all_args - self.input_class_field_names
        if difference:
            raise ValueError(f"nonexistent args in Inputs: {difference}")

        self.inputs[data_node].update(args)
        self.taken_inputs |= all_args

    def remove_input(self, data_node: "Node", args: Iterable[str]) -> None:
        all_args = [*args]
        self.inputs[data_node] -= all_args
        self.taken_inputs -= all_args


class Manager:
    def __init__(self):
        self.idDict: Dict[str, Type[Function]] = {}

    def register(self, *clses: Type[Function]) -> None:
        for cls in clses:
            self.idDict[fullname(cls)] = cls

    def make_settings(self, name: str, obj: Dict[str, Any]):
        return self.idDict[name].Settings(**obj)

    def create_node(self, name: str, settings) -> Node:
        return Node(self.idDict[name](settings))

