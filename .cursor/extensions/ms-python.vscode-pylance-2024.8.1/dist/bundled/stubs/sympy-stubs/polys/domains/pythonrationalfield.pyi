from typing import Any

from sympy.core.numbers import Integer, Rational
from sympy.polys.domains.rationalfield import RationalField
from sympy.utilities import public

class PythonRationalField(RationalField):
    dtype = ...
    zero = ...
    one = ...
    alias = ...
    def __init__(self) -> None: ...
    def get_ring(self) -> Any: ...
    def to_sympy(self, a) -> Rational | Integer: ...
    def from_sympy(self, a) -> Any: ...
    def from_ZZ_python(K1, a, K0) -> Any: ...
    def from_QQ_python(K1, a, K0): ...
    def from_ZZ_gmpy(K1, a, K0) -> Any: ...
    def from_QQ_gmpy(K1, a, K0) -> Any: ...
    def from_RealField(K1, a, K0) -> Any: ...
    def numer(self, a): ...
    def denom(self, a): ...
