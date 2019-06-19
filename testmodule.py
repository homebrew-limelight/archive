import manager


def divide(inputs):
    quotient = inputs["dividend"] / inputs["divisor"]
    return {"quotient": quotient}


def printer(inputs):
    print(inputs["printable"])


def give_two():
    return {"two": 2}


def give_four():
    return {"four": 4}


# probably turn these into child classes of Event in some way
# that way, you can do divide_event() for example, then add user defined things like set_translation without affecting object
divide_event = manager.Event(
    process=divide,
    inputs=[
        manager.Input(name="dividend", input_type=int),
        manager.Input(name="divisor", input_type=int),
    ],
    outputs=[manager.Output(name="quotient", output_type=float)],
)

print_event = manager.Event(
    process=printer, inputs=[manager.Input(name="printable", input_type=str)]
)

two_event = manager.Event(
    process=give_two, outputs=[manager.Output(name="two", output_type=int)]
)

four_event = manager.Event(
    process=give_four, outputs=[manager.Output(name="four", output_type=int)]
)
