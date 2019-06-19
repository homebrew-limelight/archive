import manager
import testmodule


# legibility, although these should probably be converted to objects in some way (see testmodule.py)
divider = testmodule.divide_event
get2 = testmodule.two_event
get4 = testmodule.four_event
printer = testmodule.print_event

# Create manager instance
manager = manager.Manager()

# Start with provider events
manager.add_step("get_numbers")
# Add get2 and get4 to the get_numbers step
manager.add_event(get2, "get_numbers")
manager.add_event(get4, "get_numbers")

# Divide the numbers seen before
manager.add_step("do_divide")
manager.add_event(divider, "do_divide")
# Set "four" from the last event to "dividend" in this event
divider.set_translation("four", "dividend")
# Set "two" from the last event to "divisor" in this event
divider.set_translation("two", "divisor")

# End with export event
manager.add_step("print")
manager.add_event(printer, "print")
# Set "quotient" from the last event to "printable" in this event
printer.set_translation("quotient", "printable")

# Run sequence
manager.run()
