import manager
import testmodule


# Create manager instance
manager = manager.Manager()

# Register module with manager
manager.register_module(testmodule.METADATA)

# Create step, and add events Give Two and Give Four to step
manager.add_step("get_numbers")
manager.add_event(manager.events["Test Module"]["Give Two"], "get_numbers")
manager.add_event(manager.events["Test Module"]["Give Four"], "get_numbers")

# Add step divide
manager.add_step("divide")
# Add to step divide:
#   use "four" from last outputs as "dividend" for this inputs
#   use "two" from last outputs as "divisor" for this inputs
manager.add_translation("divide", "four", "dividend")
manager.add_translation("divide", "two", "divisor")
# Add event Divide from Test Module to divide step
manager.add_event(manager.events["Test Module"]["Divide"], "divide")

# Add step "print time" and add Printer event to it
manager.add_step("print time")
# Use "quotient" from last outputs as "printable" for this inputs
manager.add_translation("print time", "quotient", "printable")
manager.add_event(manager.events["Test Module"]["Printer"], "print time")

# Run events
manager.run()
