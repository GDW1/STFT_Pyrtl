import pyrtl

from helper_functions import float_to_ieee_hp
from operations_butterfly import butterfly

######################################## STAGE 1 BUFFER #########################################
from operations_complex import ComplexMul, Complex

buffer_10_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_10_real")
buffer_10_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_10_imag")

######################################### STAGE 2 BUFFERS #########################################
buffer_20_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_20_real")
buffer_20_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_20_imag")

buffer_21_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_21_real")
buffer_21_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_21_imag")

######################################### STAGE 3 BUFFERS #########################################
buffer_30_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_30_real")
buffer_30_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_30_imag")

buffer_31_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_31_real")
buffer_31_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_31_imag")

buffer_32_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_32_real")
buffer_32_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_32_imag")

buffer_33_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_33_real")
buffer_33_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_33_imag")

######################################### STAGE 4 BUFFERS #########################################
buffer_40_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_40_real")
buffer_40_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_40_imag")

buffer_41_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_41_real")
buffer_41_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_41_imag")

buffer_42_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_42_real")
buffer_42_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_42_imag")

buffer_43_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_43_real")
buffer_43_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_43_imag")

buffer_44_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_44_real")
buffer_44_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_44_imag")

buffer_45_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_45_real")
buffer_45_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_45_imag")

buffer_46_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_46_real")
buffer_46_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_46_imag")

buffer_47_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_47_real")
buffer_47_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_47_imag")

cycle = pyrtl.Register(bitwidth=4, name="cycle")
cycle.next <<= cycle + 1  # Increment counter each cycle


def top(input_A):
    n = pyrtl.Const(4, bitwidth=3)  # 4 STFT stages for 16 samples
    s1 = pyrtl.Const(1)
    s2 = pyrtl.Const(2)
    s3 = pyrtl.Const(3)
    s4 = pyrtl.Const(4)
    # Stage 1
    x10, x11 = butterfly(input_A, cycle, buffer_10_real, buffer_10_imag, s1, pyrtl.Const(0), pyrtl.Const(8))

    # Stage 2
    x20, x21 = butterfly(x10, cycle, buffer_20_real, buffer_20_imag, s2, pyrtl.Const(0), pyrtl.Const(4))
    x22, x23 = butterfly(x11, cycle, buffer_21_real, buffer_21_imag, s2, pyrtl.Const(4), pyrtl.Const(4))

    # Stage 3
    x30, x31 = butterfly(x20, cycle, buffer_30_real, buffer_30_imag, s3, pyrtl.Const(0), pyrtl.Const(2))
    x32, x33 = butterfly(x21, cycle, buffer_31_real, buffer_31_imag, s3, pyrtl.Const(4), pyrtl.Const(2))
    x34, x35 = butterfly(x22, cycle, buffer_32_real, buffer_32_imag, s3, pyrtl.Const(2), pyrtl.Const(2))
    x36, x37 = butterfly(x23, cycle, buffer_33_real, buffer_33_imag, s3, pyrtl.Const(6), pyrtl.Const(2))

    # Stage 4
    x40, x41 = butterfly(x30, cycle, buffer_40_real, buffer_40_imag, s4, pyrtl.Const(0), pyrtl.Const(1))
    x42, x43 = butterfly(x31, cycle, buffer_41_real, buffer_41_imag, s4, pyrtl.Const(4), pyrtl.Const(1))
    x44, x45 = butterfly(x32, cycle, buffer_42_real, buffer_42_imag, s4, pyrtl.Const(2), pyrtl.Const(1))
    x46, x47 = butterfly(x33, cycle, buffer_43_real, buffer_43_imag, s4, pyrtl.Const(6), pyrtl.Const(1))
    x48, x49 = butterfly(x34, cycle, buffer_44_real, buffer_44_imag, s4, pyrtl.Const(1), pyrtl.Const(1))
    x50, x51 = butterfly(x35, cycle, buffer_45_real, buffer_45_imag, s4, pyrtl.Const(5), pyrtl.Const(1))
    x52, x53 = butterfly(x36, cycle, buffer_46_real, buffer_46_imag, s4, pyrtl.Const(3), pyrtl.Const(1))
    x54, x55 = butterfly(x37, cycle, buffer_47_real, buffer_47_imag, s4, pyrtl.Const(7), pyrtl.Const(1))

    return ComplexMul(x40, Complex(pyrtl.Const(int(float_to_ieee_hp(1), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           ComplexMul(x48, Complex(pyrtl.Const(int(float_to_ieee_hp(8), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           ComplexMul(x44, Complex(pyrtl.Const(int(float_to_ieee_hp(4), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           ComplexMul(x52, Complex(pyrtl.Const(int(float_to_ieee_hp(8), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           ComplexMul(x42, Complex(pyrtl.Const(int(float_to_ieee_hp(2), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           ComplexMul(x50, Complex(pyrtl.Const(int(float_to_ieee_hp(8), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           ComplexMul(x46, Complex(pyrtl.Const(int(float_to_ieee_hp(4), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           ComplexMul(x54, Complex(pyrtl.Const(int(float_to_ieee_hp(8), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           x41, \
           ComplexMul(x49, Complex(pyrtl.Const(int(float_to_ieee_hp(8), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           ComplexMul(x45, Complex(pyrtl.Const(int(float_to_ieee_hp(4), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           ComplexMul(x53, Complex(pyrtl.Const(int(float_to_ieee_hp(8), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           ComplexMul(x43, Complex(pyrtl.Const(int(float_to_ieee_hp(2), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           ComplexMul(x51, Complex(pyrtl.Const(int(float_to_ieee_hp(8), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           ComplexMul(x47, Complex(pyrtl.Const(int(float_to_ieee_hp(4), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16))), \
           ComplexMul(x55, Complex(pyrtl.Const(int(float_to_ieee_hp(8), 2), bitwidth=16), pyrtl.Const(int(float_to_ieee_hp(0), 2), bitwidth=16)))
