import uuid
from collections import namedtuple
from dataclasses import fields
from typing import Optional, List, Mapping, Any, Dict, Tuple, Type
from pydantic import BaseModel

from manager import Manager
from pipeline import Pipeline


class LiteGraph(BaseModel):
    @classmethod
    def make(cls, raw_json):
        model = LiteGraph.parse_raw(raw_json)
        model.raw_json = raw_json

        model.links = [LiteGraph.Link(*item) for item in model.links]

        return model

    # Same as make(), but update existing model in-place
    def update(self, raw_json):
        new_model = self.make(raw_json)

        # implementation from BaseModel.construct

        self.__setattr__("__values__", new_model.__values__)
        self.__setattr__("__fields_set__", new_model.__fields_set__)

        return self

    class Node(BaseModel):
        class Input(BaseModel):
            name: str
            type: str
            link: Optional[int]

        class Output(BaseModel):
            name: str
            type: str
            links: Optional[List[int]]

        id: int
        type: str
        inputs: Optional[List[Input]]
        outputs: Optional[List[Output]]
        properties: Mapping[str, Any]

    Link = namedtuple("Link", ["id", "in_node", "in_id", "out_node", "out_id", "type"])

    raw_json = """{"last_node_id":0,"last_link_id":0,"nodes":[],"links":[],"groups":[],"config":{},"version":0.4}"""

    nodes: List[Node] = []
    links: List[Link] = []


class LiteGraphPipeline(Pipeline):
    @classmethod
    def from_litegraph(cls, manager: Manager, litegraph: LiteGraph) -> "LiteGraphPipeline":
        pipeline = LiteGraphPipeline(manager)
        for node in litegraph.nodes:
            pipeline.id_to_uuid[node.id] = pipeline.create_node(node.type, node.properties)

        for link in litegraph.links:
            output_node_uuid = pipeline.id_to_uuid[link.in_node]
            input_node_uuid = pipeline.id_to_uuid[link.out_node]

            pipeline.connect_node_id(output_node_uuid, input_node_uuid, {link.in_id: link.out_id})

        return pipeline

    def __init__(self, manager: Manager):
        self.id_to_uuid: Dict[int, uuid] = dict()
        super().__init__(manager)

    def connect_node_id(self, output_node_id: uuid, input_node_id: uuid, io_mapping: Mapping[int, int]) -> None:
        if output_node_id == input_node_id:
            raise ValueError("ids must be different")
        output_node = self.nodes[output_node_id]
        input_node = self.nodes[input_node_id]

        def class_field_index(output_index, input_index) -> Tuple[str, str]:
            return fields(output_node.output_class)[output_index].name, \
                   fields(input_node.input_class)[input_index].name

        uuid_mapping: Mapping[str, str] = dict([class_field_index(k, v) for (k, v) in io_mapping.items()])

        difference = uuid_mapping.keys() - output_node.output_class_field_names
        if difference:
            raise ValueError(f"nonexistent args in Outputs: {difference}")

        self.run_order.clear()  # clear ordering of the nodes

        input_node.add_input(output_node, uuid_mapping)

        self.adjList[input_node].add(output_node)