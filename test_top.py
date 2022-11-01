import struct

import numpy as np
import pyrtl

from operations_complex import Complex


## Generate Inputs
from helper_functions import float_to_ieee_hp
from top import top

input_test = pyrtl.Input(bitwidth=16, name="input_test")

input_len = 16
inputs = [(i+10) for i in range(input_len)]

outputs = top(Complex(input_test, pyrtl.Const(0, bitwidth=16)))

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

for i in range(input_len):
    sim.step({
        'input_test': int(float_to_ieee_hp(inputs[i]), base=2)
    })
# sim_trace.render_trace()
print(inputs)
fft = np.fft.fft(inputs, n=input_len)
i =0
for output in outputs:
    y = struct.pack("H", int(bin(sim.inspect(output.real)), 2))
    o_r = np.frombuffer(y, dtype=np.float16)[0]
    y = struct.pack("H", int(bin(sim.inspect(output.imag)), 2))
    o_i = np.frombuffer(y, dtype=np.float16)[0]
    print(o_r,"+",o_i,"j")# --> ", fft[i])
    i += 1

print(np.fft.fft(inputs, n=input_len))
pyrtl.output_to_verilog(open('STFT.v', "w"))