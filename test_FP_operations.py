import pyrtl
from operations_FP import FPAdder, FPMul
from helper_functions import float_to_ieee_hp, ieee_hp_to_float
from helper_functions_unit_test import run_simulation_two_param


def Test_FP_add(a, b, expected):
    # This function adds 1 and 1 together and prints the output
    output_value = run_simulation_two_param(
        FPAdder,
        16,
        16,
        int(float_to_ieee_hp(a), 2),
        int(float_to_ieee_hp(b), 2)
    )
    actual = (bin(output_value)[2:].zfill(16))
    expected_bin = (float_to_ieee_hp(expected))
    print("OUTPUT OF SIMULATION     :", ieee_hp_to_float(int(actual, 2)))
    print("EXPECTATION OF SIMULATION:", ieee_hp_to_float(int(expected_bin, 2)))
    assert abs(ieee_hp_to_float(int(actual, 2)) - ieee_hp_to_float(int(expected_bin, 2))) < .2, (a, "+", b,"=",expected,": FAILED")
    print(a, "+", b,"=",expected,": PASSED")
    print("_______________________________________")
    pyrtl.reset_working_block()


def Test_FP_mul(a, b, expected):
    # This function adds 1 and 1 together and prints the output
    output_value = run_simulation_two_param(
        FPMul,
        16,
        16,
        int(float_to_ieee_hp(a), 2),
        int(float_to_ieee_hp(b), 2)
    )
    actual = (bin(output_value)[2:].zfill(16))
    expected_bin = (float_to_ieee_hp(expected))
    print("OUTPUT OF SIMULATION     :", ieee_hp_to_float(int(actual, 2)), "---> ", actual)
    print("EXPECTATION OF SIMULATION:", ieee_hp_to_float(int(expected_bin, 2)), "---> ", expected_bin)
    assert abs(ieee_hp_to_float(int(actual, 2)) - ieee_hp_to_float(int(expected_bin, 2))) < .2, (a, "*", b,"=",expected,": FAILED")
    print(a, "*", b,"=",expected,": PASSED")
    print("_______________________________________")
    pyrtl.reset_working_block()

print("______ Begin Tests ________")
Test_FP_add(2, 2, 4)
Test_FP_mul(2, 2, 4)
Test_FP_mul(2.5, 2, 5)
Test_FP_add(3, 2, 3+2)
Test_FP_add(1.1, 1.2, 2.3)
Test_FP_mul(2.0, 3.0, 6.0)
Test_FP_mul(7, 3.0, 21)
Test_FP_mul(1.5, 4.5, 6.75)
Test_FP_mul(8.3, 22.9, 190.07)


print(ieee_hp_to_float(int(float_to_ieee_hp(0.923879532511), 2)))