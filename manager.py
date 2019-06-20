import array
import dataclasses
import collections


class Event:
    def __init__(self, name, event):
        self.name = name
        self.inputs = event.get("inputs")
        self.outputs = event.get("outputs")
        self.process = event["process"]
        self.translator = {}

    def is_provider(self):
        return True if not self.inputs else False

    def is_export(self):
        return True if not self.outputs else False


class Module:
    def __init__(self, metadata: dict):
        self.name = metadata["name"]
        self.events = {}
        self.__parse_events__(metadata["events"])

    def __parse_events__(self, events):
        for event in events.keys():
            # Add new event object to events list
            self.events[event] = Event(event, events[event])


@dataclasses.dataclass
class Step:
    name: str
    translator: dict = dataclasses.field(default_factory=dict)
    events: list = dataclasses.field(default_factory=list)

    def add_event(self, event: Event):
        self.events.append(event)

    def add_translation(self, output_name: str, input_name: str):
        self.translator[input_name] = output_name

    def get_inputs(self):
        inputs = []
        for event in self.events:
            for event_input in event.inputs:
                inputs.append(event_input)
        return inputs

    # Allows the linkage of the previous event's output to this event's input
    def translate(self, untranslated: dict):
        result = {}
        for inp in self.get_inputs():
            translation = self.translator.get(inp["name"])
            if not translation:
                return KeyError("No translation provided for a selected input!")
            result[inp["name"]] = untranslated[translation]
        return result


class Manager:
    def __init__(self):
        # Probably not a great idea to use OrderedDict, but fine for now
        self.modules = []
        self.events = {}
        self.sequence = {}

    def register_module(self, metadata: dict):
        module = Module(metadata)
        self.modules.append(module)
        self.events[module.name] = {}
        for event in module.events.keys():
            self.events[module.name][event] = module.events[event]

    def add_translation(self, step: str, input_name: str, output_name: str):
        self.sequence[step].add_translation(input_name, output_name)

    # TODO: allow inserting anywhere in sequence
    def add_step(self, name: str):
        self.sequence[name] = Step(name=name)

    def add_event(self, event: Event, step: str):
        self.sequence[step].add_event(event)

    # Go through sequence
    def run(self):
        last_result = {}
        for step in self.sequence.keys():
            outputs = {}
            for event in self.sequence[step].events:
                if event.is_provider():
                    result = event.process()
                else:
                    if prev_outputs:
                        inputs = self.sequence[step].translate(prev_outputs)
                        result = event.process(inputs)
                if not event.is_export():
                    outputs.update(result)
            prev_outputs = outputs
