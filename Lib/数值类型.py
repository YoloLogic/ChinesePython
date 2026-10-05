# -*- coding: utf-8 -*-
"""数值类型 —— 汉语库（由 tools/汉化库.py 从 Lib/numbers.py 机械生成，**不要手改**）。

英文库 Lib/numbers.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 数值类型
"""


"""Abstract Base Classes (ABCs) for numbers, according to PEP 3141.

TODO: Fill out more detailed documentation on the operators."""
_英文原名表 = {'Complex': '复数', 'Integral': '整数', 'Number': '数', 'Rational': '有理数', 'Real': '实数'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
from abc import ABCMeta, abstractmethod
__all__ = ['Number', 'Complex', 'Real', 'Rational', 'Integral']

class 数(metaclass=ABCMeta):
    """All numbers inherit from this class.

    If you just want to check if an argument x is a number, without
    caring what kind, use isinstance(x, Number).
    """
    __slots__ = ()
    __hash__ = None
import numbers as _英文身份源
数 = _英文身份源.Number

class 复数(数):
    """Complex defines the operations that work on the builtin complex type.

    In short, those are: a conversion to complex, .real, .imag, +, -,
    *, /, **, abs(), .conjugate, ==, and !=.

    If it is given heterogeneous arguments, and doesn't have special
    knowledge about them, it should fall back to the builtin complex
    type as described below.
    """
    __slots__ = ()

    @abstractmethod
    def __complex__(self):
        """Return a builtin complex instance. Called for complex(self)."""

    def __bool__(self):
        """True if self != 0. Called for bool(self)."""
        return self != 0

    @property
    @abstractmethod
    def real(self):
        """Retrieve the real component of this number.

        This should subclass Real.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def imag(self):
        """Retrieve the imaginary component of this number.

        This should subclass Real.
        """
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other):
        """self + other"""
        raise NotImplementedError

    @abstractmethod
    def __radd__(self, other):
        """other + self"""
        raise NotImplementedError

    @abstractmethod
    def __neg__(self):
        """-self"""
        raise NotImplementedError

    @abstractmethod
    def __pos__(self):
        """+self"""
        raise NotImplementedError

    def __sub__(self, other):
        """self - other"""
        return self + -other

    def __rsub__(self, other):
        """other - self"""
        return -self + other

    @abstractmethod
    def __mul__(self, other):
        """self * other"""
        raise NotImplementedError

    @abstractmethod
    def __rmul__(self, other):
        """other * self"""
        raise NotImplementedError

    @abstractmethod
    def __truediv__(self, other):
        """self / other: Should promote to float when necessary."""
        raise NotImplementedError

    @abstractmethod
    def __rtruediv__(self, other):
        """other / self"""
        raise NotImplementedError

    @abstractmethod
    def __pow__(self, exponent):
        """self ** exponent; should promote to float or complex when necessary."""
        raise NotImplementedError

    @abstractmethod
    def __rpow__(self, base):
        """base ** self"""
        raise NotImplementedError

    @abstractmethod
    def __abs__(self):
        """Returns the Real distance from 0. Called for abs(self)."""
        raise NotImplementedError

    @abstractmethod
    def conjugate(self):
        """(x+y*i).conjugate() returns (x-y*i)."""
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        """self == other"""
        raise NotImplementedError
import numbers as _英文身份源
复数 = _英文身份源.Complex
复数.register(complex)

class 实数(复数):
    """To Complex, Real adds the operations that work on real numbers.

    In short, those are: a conversion to float, trunc(), divmod,
    %, <, <=, >, and >=.

    Real also provides defaults for the derived operations.
    """
    __slots__ = ()

    @abstractmethod
    def __float__(self):
        """Any Real can be converted to a native float object.

        Called for float(self)."""
        raise NotImplementedError

    @abstractmethod
    def __trunc__(self):
        """trunc(self): Truncates self to an Integral.

        Returns an Integral i such that:
          * i > 0 iff self > 0;
          * abs(i) <= abs(self);
          * for any Integral j satisfying the first two conditions,
            abs(i) >= abs(j) [i.e. i has "maximal" abs among those].
        i.e. "truncate towards 0".
        """
        raise NotImplementedError

    @abstractmethod
    def __floor__(self):
        """Finds the greatest Integral <= self."""
        raise NotImplementedError

    @abstractmethod
    def __ceil__(self):
        """Finds the least Integral >= self."""
        raise NotImplementedError

    @abstractmethod
    def __round__(self, ndigits=None):
        """Rounds self to ndigits decimal places, defaulting to 0.

        If ndigits is omitted or None, returns an Integral, otherwise
        returns a Real. Rounds half toward even.
        """
        raise NotImplementedError

    def __divmod__(self, other):
        """divmod(self, other): The pair (self // other, self % other).

        Sometimes this can be computed faster than the pair of
        operations.
        """
        return (self // other, self % other)

    def __rdivmod__(self, other):
        """divmod(other, self): The pair (other // self, other % self).

        Sometimes this can be computed faster than the pair of
        operations.
        """
        return (other // self, other % self)

    @abstractmethod
    def __floordiv__(self, other):
        """self // other: The floor() of self/other."""
        raise NotImplementedError

    @abstractmethod
    def __rfloordiv__(self, other):
        """other // self: The floor() of other/self."""
        raise NotImplementedError

    @abstractmethod
    def __mod__(self, other):
        """self % other"""
        raise NotImplementedError

    @abstractmethod
    def __rmod__(self, other):
        """other % self"""
        raise NotImplementedError

    @abstractmethod
    def __lt__(self, other):
        """self < other

        < on Reals defines a total ordering, except perhaps for NaN."""
        raise NotImplementedError

    @abstractmethod
    def __le__(self, other):
        """self <= other"""
        raise NotImplementedError

    def __complex__(self):
        """complex(self) == complex(float(self), 0)"""
        return complex(float(self))

    @property
    def real(self):
        """Real numbers are their real component."""
        return +self

    @property
    def imag(self):
        """Real numbers have no imaginary component."""
        return 0

    def conjugate(self):
        """Conjugate is a no-op for Reals."""
        return +self
import numbers as _英文身份源
实数 = _英文身份源.Real
实数.register(float)

class 有理数(实数):
    """To Real, Rational adds numerator and denominator properties.

    The numerator and denominator values should be in lowest terms,
    with a positive denominator.
    """
    __slots__ = ()

    @property
    @abstractmethod
    def numerator(self):
        """The numerator of a rational number in lowest terms."""
        raise NotImplementedError

    @property
    @abstractmethod
    def denominator(self):
        """The denominator of a rational number in lowest terms.

        This denominator should be positive.
        """
        raise NotImplementedError

    def __float__(self):
        """float(self) = self.numerator / self.denominator

        It's important that this conversion use the integer's "true"
        division rather than casting one side to float before dividing
        so that ratios of huge integers convert without overflowing.

        """
        return int(self.numerator) / int(self.denominator)
import numbers as _英文身份源
有理数 = _英文身份源.Rational

class 整数(有理数):
    """Integral adds methods that work on integral numbers.

    In short, these are conversion to int, pow with modulus, and the
    bit-string operations.
    """
    __slots__ = ()

    @abstractmethod
    def __int__(self):
        """int(self)"""
        raise NotImplementedError

    def __index__(self):
        """Called whenever an index is needed, such as in slicing"""
        return int(self)

    @abstractmethod
    def __pow__(self, exponent, modulus=None):
        """self ** exponent % modulus, but maybe faster.

        Accept the modulus argument if you want to support the
        3-argument version of pow(). Raise a TypeError if exponent < 0
        or any argument isn't Integral. Otherwise, just implement the
        2-argument version described in Complex.
        """
        raise NotImplementedError

    @abstractmethod
    def __lshift__(self, other):
        """self << other"""
        raise NotImplementedError

    @abstractmethod
    def __rlshift__(self, other):
        """other << self"""
        raise NotImplementedError

    @abstractmethod
    def __rshift__(self, other):
        """self >> other"""
        raise NotImplementedError

    @abstractmethod
    def __rrshift__(self, other):
        """other >> self"""
        raise NotImplementedError

    @abstractmethod
    def __and__(self, other):
        """self & other"""
        raise NotImplementedError

    @abstractmethod
    def __rand__(self, other):
        """other & self"""
        raise NotImplementedError

    @abstractmethod
    def __xor__(self, other):
        """self ^ other"""
        raise NotImplementedError

    @abstractmethod
    def __rxor__(self, other):
        """other ^ self"""
        raise NotImplementedError

    @abstractmethod
    def __or__(self, other):
        """self | other"""
        raise NotImplementedError

    @abstractmethod
    def __ror__(self, other):
        """other | self"""
        raise NotImplementedError

    @abstractmethod
    def __invert__(self):
        """~self"""
        raise NotImplementedError

    def __float__(self):
        """float(self) == float(int(self))"""
        return float(int(self))

    @property
    def numerator(self):
        """Integers are their own numerators."""
        return +self

    @property
    def denominator(self):
        """Integers have a denominator of 1."""
        return 1
import numbers as _英文身份源
整数 = _英文身份源.Integral
整数.register(int)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import numbers as _英文库
复数 = _英文库.Complex
整数 = _英文库.Integral
数 = _英文库.Number
有理数 = _英文库.Rational
实数 = _英文库.Real
_模块别名 = {
    'Complex': '复数',
    'Integral': '整数',
    'Number': '数',
    'Rational': '有理数',
    'Real': '实数',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '复数',
    '实数',
    '数',
    '整数',
    '有理数',
])

# ---- 转发层结束 ----
