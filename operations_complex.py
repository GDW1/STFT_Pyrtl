import pyrtl
from operations_FP import FPAdder, FPMul

"""
Complex operations for Floating point IEEE numbers
Inputs are all IEEE, half-precision floating point numbers 
"""
class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

def ComplexAdd(input_A, input_B):
    add_real = pyrtl.WireVector(bitwidth=16)
    add_imag = pyrtl.WireVector(bitwidth=16)

    add_real <<= FPAdder(input_A.real, input_B.real)
    add_imag <<= FPAdder(input_A.imag, input_B.imag)

    return Complex(add_real, add_imag)


def ComplexSub(input_A, input_B):
    sub_real = pyrtl.WireVector(bitwidth=16)
    sub_imag = pyrtl.WireVector(bitwidth=16)

    sub_real <<= FPAdder(input_A.real, pyrtl.concat(~input_B.real[-1], input_B.real[0:15]))
    sub_imag <<= FPAdder(input_A.imag, pyrtl.concat(~input_B.imag[-1], input_B.imag[0:15]))

    return Complex(sub_real, sub_imag)


def ComplexMul(input_A, input_B):
    mult_real = pyrtl.WireVector(bitwidth=16)
    mult_imag = pyrtl.WireVector(bitwidth=16)

    mult_real <<= FPAdder(FPMul(input_A.real, input_B.real), FPMul(input_A.imag, pyrtl.concat(~input_B.imag[-1], input_B.imag[0:15])))
    mult_imag <<= FPAdder(FPMul(input_A.real, input_B.imag), FPMul(input_A.imag, input_B.real))

    return Complex(mult_real, mult_imag)