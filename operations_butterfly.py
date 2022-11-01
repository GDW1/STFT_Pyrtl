import pyrtl

from operations_complex import *
import helper_functions
# N = 16 = 2^4
# n: number of stages
# index : which input sample it is
# s: current stage
# k: current butterfly number

def butterfly(input_A, index, buffer_real, buffer_imag, s, k, mod_to):
    add_output = Complex(pyrtl.Register(bitwidth=16), pyrtl.Register(bitwidth=16))
    sub_output = Complex(pyrtl.Register(bitwidth=16), pyrtl.Register(bitwidth=16))

    m = pyrtl.WireVector(bitwidth=3, name=("m" + str(s) + str(index) + str(k)))  # at most 8 elements, buffer index
    # Compute N/2^s, so we can later compute i % N/2^s
    # We observe that N is a power of 2, or N = 2^n.
    # We can't do i % N/2^s in PyRTL, but we can do
    # i % N/2^s = i - (i / (N/2^s))
    mod_by = pyrtl.WireVector(bitwidth=16)
    mod_by <<= (pyrtl.Const(16) - s)
    m1 = (pyrtl.shift_right_logical(index, mod_by))
    m2 = pyrtl.shift_left_logical(pyrtl.Const(1), mod_by)
    m <<= index - (m1 * m2)
    input_B = Complex(pyrtl.WireVector(bitwidth=16), pyrtl.WireVector(bitwidth=16))

    m_plus_one = pyrtl.WireVector(bitwidth=3)
    m_plus_one <<= m + pyrtl.Const(1)

    input_B.real <<= buffer_real[m]

    input_B.imag <<= buffer_imag[m]
    twiddle_real = pyrtl.WireVector(bitwidth=16)
    twiddle_imag = pyrtl.WireVector(bitwidth=16)

    with pyrtl.conditional_assignment:
        with k == 0:
            twiddle_real |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(1), 2))
            twiddle_imag |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(0), 2))
        with k == 1:
            twiddle_real |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(0.923879532511), 2))
            twiddle_imag |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(-0.382683432365), 2))
        with k == 2:
            twiddle_real |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(0.707106781187), 2))
            twiddle_imag |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(-0.707106781187), 2))
        with k == 3:
            twiddle_real |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(0.382683432365), 2))
            twiddle_imag |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(-0.923879532511), 2))
        with k == 4:
            twiddle_real |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(0), 2))
            twiddle_imag |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(-1), 2))
        with k == 5:
            twiddle_real |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(-0.382683432365), 2))
            twiddle_imag |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(-0.923879532511), 2))
        with k == 6:
            twiddle_real |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(-0.707106781187), 2))
            twiddle_imag |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(-0.707106781187), 2))
        with k == 7:
            twiddle_real |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(-0.923879532511), 2))
            twiddle_imag |= pyrtl.Const(int(helper_functions.float_to_ieee_hp(-0.382683432365), 2))

    add_result = ComplexAdd(input_B, ComplexMul(Complex(twiddle_real, twiddle_imag), input_A))
    add_output.real.next <<= add_result.real
    add_output.imag.next <<= add_result.imag

    sub_result = ComplexSub(input_B, ComplexMul(Complex(twiddle_real, twiddle_imag), input_A))
    sub_output.real.next <<= sub_result.real
    sub_output.imag.next <<= sub_result.imag

    buffer_real[m_plus_one] <<= input_A.real
    buffer_imag[m_plus_one] <<= input_A.imag

    return add_output, sub_output
