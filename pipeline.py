import uuid
from itertools import chain
from typing import Dict, Set, List, Mapping, Any

from toposort import toposort

from manager import Node, Manager


class Pipeline:
    def __init__(self, manager: Manager):
        self.manager: Manager = manager
        self.nodes: Dict[uuid, Node] = {}
        self.adjList: Dict[Node, Set[Node]] = {}
        self.run_order: List[Node] = []

    def create_node(self, qual_name: str, obj: Dict[str, Any]) -> uuid:
        settings = self.manager.make_settings(qual_name, obj)
        return self.create_node_raw(qual_name, settings)

    def create_node_raw(self, qual_name: str, settings) -> uuid:
        node_id = uuid.uuid4()
        node = self.manager.create_node(qual_name, settings)
        node.id = node_id
        self.nodes[node_id] = node
        self.adjList[node] = set()
        return node_id

    def connect_node(self, output_node_id: uuid, input_node_id: uuid, io_mapping: Mapping[str, str]) -> None:
        if output_node_id == input_node_id:
            raise ValueError("ids must be different")
        output_node = self.nodes[output_node_id]
        input_node = self.nodes[input_node_id]

        difference = io_mapping.keys() - output_node.output_class_field_names
        if difference:
            raise ValueError(f"nonexistent args in Outputs: {difference}")

        self.run_order.clear()  # clear ordering of the nodes

        input_node.add_input(output_node, io_mapping)

        self.adjList[input_node].add(output_node)

    def _validate_valid_pipeline(self) -> None:
        if not self.nodes:
            raise ValueError("no nodes present")

        if not self.run_order:
            self.run_order = list(chain.from_iterable(toposort(self.adjList)))

    def run_pipeline(self) -> None:
        self._validate_valid_pipeline()

        storage: Dict[Node, Any] = {}

        for n in self.run_order:  # Each node to be processed
            data: Dict[str, Any] = {}  # Data for Inputs dataclass
            for input_node, cur_dict in n.inputs.items():  # Iterate through needed inputs Dict[Node, Dict[str, str]]
                cur_data = storage[input_node]  # Fetch outputs for current Node
                for output_name, input_name in cur_dict.items():
                    data[input_name] = getattr(cur_data, output_name)  # place outputs in data dict

            storage[n] = n(n.input_class(**data))

    def clear(self):
        for node in self.nodes.values():
            node.function.dispose()

        self.nodes.clear()
        self.adjList.clear()
        self.run_order.clear()
