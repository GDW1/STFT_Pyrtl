import numpy as np
import pyrtl
from decimal import *
"""
float_to_ieee_hp:
converts python floating point numbers to IEEE half precision floating point numbers
"""
def float_to_ieee_hp(n):
    return bin(np.float16(n).view('H'))[2:].zfill(16)

def ieee_hp_to_float(n):
    n = str(bin(n)[2:].zfill(16))
    M_val = 1
    for i in range(6, len(str(n))):
        if n[i] == '1':
            M_val += (1/(2**(i-5)))

    mult = int(str(n)[1:6], 2)-15
    return ((-1) ** (int(str(n)[0]))) * (2 ** mult) * M_val

# counts the number of wires that come before the first 1
def count_zeroes_from_end(x, start='msb'):
    if start not in ('msb', 'lsb'):
        raise pyrtl.PyrtlError('Invalid start parameter')

    def _count(x, found):
        end = x[-1] if start == 'msb' else x[0]
        is_zero = end == 0
        to_add = ~found & is_zero
        if len(x) == 1:
            return to_add
        else:
            rest = x[:-1] if start == 'msb' else x[1:]
            rest_to_add = _count(rest, found | ~is_zero)
            return to_add + rest_to_add

    return _count(x, pyrtl.as_wires(False))