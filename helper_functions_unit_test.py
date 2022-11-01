import uuid

import pyrtl

"""
Runs a Simulation on a unit and returns the output of the wire (note that the unit must take in exactly 2 parameters)
Takes in the:
unit (the component to test)
input_width (how many bits wide the input is)
output_width (how many bits wide the output is)
A_val (The value of the first input)
B_val (The value of the first input)
"""

def run_simulation_two_param(unit, input_width, output_width, A_val, B_val):
    test_uuid = str(str(uuid.uuid4()))
    A_name = ("A_" + test_uuid)
    B_name = ("B_" + test_uuid)
    output_wire = pyrtl.WireVector(bitwidth=output_width, name=("output_unit_test_" + test_uuid))
    A_wire      = pyrtl.Input(bitwidth=input_width, name=A_name)
    B_wire      = pyrtl.Input(bitwidth=input_width, name=B_name)
    output_wire <<= unit(A_wire, B_wire)
    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)
    inputs = {
        A_name: A_val,
        B_name: B_val
    }
    sim.step(inputs)
    output = sim_trace.trace[("output_unit_test_" + test_uuid)][0]
#    print("variable inspection:", bin(sim_trace.trace[("ppm")][0]))
    return output
