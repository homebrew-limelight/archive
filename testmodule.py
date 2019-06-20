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


METADATA = {
    "name": "Test Module",
    "events": {
        "Divide": {
            "process": divide,
            "inputs": [
                {"name": "dividend", "type": int},
                {"name": "divisor", "type": int},
            ],
            "outputs": [{"name": "quotient", "type": float}],
        },
        "Printer": {"process": printer, "inputs": [{"name": "printable", "type": str}]},
        "Give Two": {"process": give_two, "outputs": [{"name": "two", "type": int}]},
        "Give Four": {"process": give_four, "outputs": [{"name": "four", "type": int}]},
    },
}
