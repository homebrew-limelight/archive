import uuid
from collections import defaultdict
from dataclasses import fields, dataclass
from itertools import chain
from typing import Dict, Type, Any, List, Set, Iterable, Mapping, Optional

from toposort import toposort

from function import Function


def fullname(cls: type) -> str:

    module = cls.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return cls.__qualname__
    else:
        return module + '.' + cls.__qualname__


class Node:
    def __init__(self, function: Function):
        self.id: uuid = uuid.uuid4() #TODO: DEBUG ONLY
        self.function: Function = function
        self.inputs: Dict[Node, Dict[str, str]] = defaultdict(lambda: dict())
        self.taken_inputs: Set[str] = set()

        self.input_class: Type[dataclass] = type(self.function).Inputs
        self.output_class: Type[dataclass] = type(self.function).Outputs

        self.input_class_field_names: Set[str] = {x.name for x in fields(self.input_class)}
        self.output_class_field_names: Set[str] = {x.name for x in fields(self.output_class)}

    def __call__(self, inputs, settings=None):
        return self.function(inputs, settings)

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

    def __repr__(self) -> str:
        return f"Node{str(self.id.__str__)}"


class Manager:
    def __init__(self):
        self.idDict: Dict[str, Type[Function]] = {}

    def register(self, cls: Type[Function]) -> None:
        self.idDict[fullname(cls)] = cls

    def create(self, name: str, settings) -> Node:
        return Node(self.idDict[name](settings))


class Pipeline:
    def __init__(self, manager: Manager):
        self.manager: Manager = manager
        self.nodes: Dict[uuid, Node] = {}
        self.adjList: Dict[Node, Set[Node]] = {}
        self.run_order: Optional[List[Node]] = None

    def create_node(self, qual_name: str, settings) -> uuid:
        node_id = uuid.uuid4()
        node = self.manager.create(qual_name, settings)
        node.id = node_id
        self.nodes[node_id] = node
        self.adjList[node] = set()
        return node_id

    def connect_node(self, output_node_id: uuid, input_node_id: uuid, io_mapping: Mapping[str, str]):
        if output_node_id == input_node_id:
            raise ValueError("uuids must be different")
        output_node = self.nodes[output_node_id]
        input_node = self.nodes[input_node_id]

        difference = io_mapping.keys() - output_node.output_class_field_names
        if difference:
            raise ValueError(f"nonexistent args in Outputs: {difference}")

        input_node.add_input(output_node, io_mapping)

        self.adjList[input_node].add(output_node)

    def run_pipeline(self):
        if self.run_order is None:
            self.run_order = list(chain.from_iterable(toposort(self.adjList)))

        storage: Dict[Node, Any] = {}

        for n in self.run_order:  # Each node to be processed
            data: Dict[str, Any] = {}  # Data for Inputs dataclass
            for input_node, cur_dict in n.inputs.items():  # Iterate through needed inputs Dict[Node, Dict[str, str]]
                cur_data = storage[input_node]  # Fetch outputs for current Node
                for output_name, input_name in cur_dict.items():
                    data[input_name] = getattr(cur_data, output_name)  # place outputs in data dict

            storage[n] = n(n.input_class(**data))



