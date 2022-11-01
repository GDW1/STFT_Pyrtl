import pyrtl

from helper_functions import count_zeroes_from_end


def FPAdder(input_A, input_B):
    a_sign = input_A[15]
    a_expo = input_A[10:15]
    a_frac = input_A[0:10]

    b_sign = input_B[15]
    b_expo = input_B[10:15]
    b_frac = input_B[0:10]

    c_sign = pyrtl.WireVector(bitwidth=1)
    c_expo = pyrtl.WireVector(bitwidth=5)
    c_frac = pyrtl.WireVector(bitwidth=10)

    c = pyrtl.WireVector(bitwidth=16)
    c <<= pyrtl.concat(c_sign, c_expo, c_frac)

    # max exponant
    max_expo = pyrtl.WireVector(bitwidth=a_expo.bitwidth)
    max_expo <<= pyrtl.select((a_expo > b_expo), a_expo, b_expo)

    # mantissas
    a_prepend_value = (a_expo != 0)
    b_prepend_value = (b_expo != 0)
    extra_zeros = pyrtl.Const(0, bitwidth=(2 ** a_expo.bitwidth))
    a_mant = pyrtl.concat(a_prepend_value, a_frac, extra_zeros)
    b_mant = pyrtl.concat(b_prepend_value, b_frac, extra_zeros)

    # normalized mantissas
    normalized_a_mant = pyrtl.shift_right_logical(a_mant, max_expo - a_expo)
    normalized_b_mant = pyrtl.shift_right_logical(b_mant, max_expo - b_expo)

    # signed normalized mantissas
    signed_normalized_a_mant = pyrtl.select(a_sign, 0 - normalized_a_mant, normalized_a_mant).sign_extended(
        normalized_a_mant.bitwidth + 2)
    signed_normalized_b_mant = pyrtl.select(b_sign, 0 - normalized_b_mant, normalized_b_mant).sign_extended(
        normalized_b_mant.bitwidth + 2)

    # calculate sum of mantissas
    sm = pyrtl.WireVector(bitwidth=(signed_normalized_a_mant.bitwidth))
    sm <<= signed_normalized_a_mant + signed_normalized_b_mant

    # sign
    c_sign <<= sm[-1]

    # absolute value of sum
    abs_sm = pyrtl.WireVector(bitwidth=(sm.bitwidth - 1))
    abs_sm <<= pyrtl.select(c_sign, 0 - sm, sm)

    # first set 1 index
    num_zeros = count_zeroes_from_end(abs_sm)

    # normalized sum
    normalized_abs_sm = pyrtl.shift_left_logical(abs_sm, num_zeros)

    # get c's exponent and fraction
    is_zero = (abs_sm == 0)
    with pyrtl.conditional_assignment:
        with is_zero:
            c_expo |= 0
            c_frac |= 0
        with pyrtl.otherwise:
            c_expo |= max_expo + 1 - num_zeros
            c_frac |= normalized_abs_sm[-11:-1]

    return c


def FPMul(input_A, input_B):
    A_s = pyrtl.WireVector(bitwidth=1)
    A_e = pyrtl.WireVector(bitwidth=5)
    A_f = pyrtl.WireVector(bitwidth=11)
    B_s = pyrtl.WireVector(bitwidth=1)
    B_e = pyrtl.WireVector(bitwidth=5)
    B_f = pyrtl.WireVector(bitwidth=11)

    A_s <<= input_A[-1]
    A_e <<= input_A[10:15]
    A_f <<= pyrtl.concat(pyrtl.Const(1, bitwidth=1), input_A[0:10])

    B_s <<= input_B[-1]
    B_e <<= input_B[10:15]
    B_f <<= pyrtl.concat(pyrtl.Const(1, bitwidth=1), input_B[0:10])

    #  XOR sign bits to determine product sign.
    oProd_s = pyrtl.WireVector(bitwidth=1)
    oProd_s <<= A_s ^ B_s

    #  Multiply the fractions of A and B
    pre_prod_frac = pyrtl.WireVector(bitwidth=22)
    pre_prod_frac <<= A_f * B_f#~pyrtl.corecircuits.mult_signed(A_f, B_f) + 1

    #  Add exponents of A and B
    pre_prod_exp = pyrtl.WireVector(bitwidth=6)
    pre_prod_exp <<= A_e + B_e

    # If top bit of product frac is 0, shift left one
    oProd_e = pyrtl.WireVector(bitwidth=5)
    oProd_f = pyrtl.WireVector(bitwidth=10)

    oProd_e <<= pyrtl.select(pre_prod_frac[-1], pre_prod_exp - pyrtl.Const(14), pre_prod_exp - pyrtl.Const(15))
    oProd_f <<= pyrtl.select(pre_prod_frac[-1], pre_prod_frac[11:22], pre_prod_frac[10:20])

    # Detect underflow
    underflow = pyrtl.WireVector(bitwidth=1)

    underflow <<= pre_prod_exp < pyrtl.Const(0x10, bitwidth=6)

    oProd = pyrtl.WireVector(bitwidth=16)
    # Detect zero conditions (either product frac doesn't start with 1, or underflow)
    with pyrtl.conditional_assignment:
        with underflow:
            oProd |= 0
        with B_e == 0:
            oProd |= 0
        with A_e == 0:
            oProd |= 0
        with pyrtl.otherwise:
            oProd |= pyrtl.concat(oProd_s, oProd_e, oProd_f)

    return oProd

