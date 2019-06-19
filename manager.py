import array
import dataclasses
import collections


@dataclasses.dataclass
class Event:

    ## Module provided
    # The actual callable executed by the event
    process: callable
    # All possible inputs
    inputs: list = dataclasses.field(default_factory=list)
    # All possible outputs
    outputs: list = dataclasses.field(default_factory=list)

    ## User provided
    # TODO: allow optional inputs

    # Translated output of previous event to input of this event
    translator: dict = dataclasses.field(default_factory=dict)

    def is_provider(self):
        return True if not self.inputs else False

    def is_export(self):
        return True if not self.outputs else False

    def set_translation(self, output_name: str, input_name: str):
        self.translator[input_name] = output_name

    # Allows the linkage of the previous event's output to this event's input
    def translate(self, untranslated: dict):
        result = {}
        for inp in self.inputs:
            translation = self.translator.get(inp.name)
            if not translation:
                return KeyError("No translation provided for a selected input!")
            result[inp.name] = untranslated[translation]
        return result


@dataclasses.dataclass
class Input:
    name: str
    input_type: type
    required: bool = True


@dataclasses.dataclass
class Output:
    name: str
    output_type: type


class Manager:
    def __init__(self):
        # Probably not a great idea to use OrderedDict, but fine for now
        self.sequence = collections.OrderedDict()

    # TODO: allow inserting anywhere in sequence
    def add_step(self, name: str):
        self.sequence[name] = []

    def add_event(self, event: Event, step: str):
        self.sequence[step].append(event)

    # Go through sequence
    def run(self):
        last_result = {}
        for step in self.sequence.keys():
            outputs = {}
            for event in self.sequence[step]:
                if event.is_provider():
                    result = event.process()
                else:
                    if prev_outputs:
                        inputs = event.translate(prev_outputs)
                        result = event.process(inputs)
                if not event.is_export():
                    outputs.update(result)
            prev_outputs = outputs
