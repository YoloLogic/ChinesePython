# -*- coding: utf-8 -*-
"""分数 —— 汉语库（由 tools/汉化库.py 从 Lib/fractions.py 机械生成，**不要手改**）。

英文库 Lib/fractions.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 分数
"""


"""Fraction, infinite-precision, rational numbers."""
_英文原名表 = {'Fraction': '分数'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
_实例属性全表 = {}
_反表 = {}

def _装类转发(_类, _对, _属性=None):
    if getattr(_类, '__module__', None) != __name__:
        return
    for _英, _中 in _对.items():
        if _中 in _类.__dict__:
            setattr(_类, _英, _类.__dict__[_中])
    if _属性:
        _实例属性全表.update(_属性)
        _反表.update({_中: _英 for _英, _中 in _属性.items()})
        for _英, _中 in _属性.items():
            if _英 not in _类.__dict__ and _中 in _类.__dict__:
                setattr(_类, _英, _类.__dict__[_中])
        if '__getattr__' not in _类.__dict__:

            def _取(self, _名, _对=_实例属性全表, _反=_反表):
                if _名 in _对:
                    try:
                        return object.__getattribute__(self, _对[_名])
                    except AttributeError:
                        pass
                    try:
                        return object.__getattribute__(self, _名)
                    except AttributeError:
                        pass
                if _名 in _反:
                    try:
                        return object.__getattribute__(self, _反[_名])
                    except AttributeError:
                        pass
                raise AttributeError(_名)
            try:
                _类.__getattr__ = _取
            except TypeError:
                return
        if not [_基 for _基 in _类.__mro__ if _基 is not object and '__setattr__' in _基.__dict__ and (not getattr(_基.__dict__['__setattr__'], '_中文转发钩子', False))]:

            def _设(self, _名, _值, _对=_实例属性全表, _反=_反表):
                _英 = _名 if _名 in _对 else _反.get(_名)
                if _英 is None:
                    object.__setattr__(self, _名, _值)
                    return
                _中 = _对[_英]
                _成 = False
                for _名2 in (_中, _英):
                    try:
                        object.__setattr__(self, _名2, _值)
                        _成 = True
                    except AttributeError:
                        pass
                if not _成:
                    raise AttributeError(_名)
            _设._中文转发钩子 = True
            try:
                _类.__setattr__ = _设
            except TypeError:
                return
import functools
import math
import numbers
import operator
import re
import sys
__all__ = ['Fraction']
_PyHASH_MODULUS = sys.hash_info.modulus
_PyHASH_INF = sys.hash_info.inf

@functools.lru_cache(maxsize=1 << 14)
def _hash_algorithm(numerator, denominator):
    try:
        dinv = pow(denominator, -1, _PyHASH_MODULUS)
    except ValueError:
        hash_ = _PyHASH_INF
    else:
        hash_ = hash(hash(abs(numerator)) * dinv)
    result = hash_ if numerator >= 0 else -hash_
    return -2 if result == -1 else result
_RATIONAL_FORMAT = re.compile('\n    \\A\\s*                                  # optional whitespace at the start,\n    (?P<sign>[-+]?)                        # an optional sign, then\n    (?=\\d|\\.\\d)                            # lookahead for digit or .digit\n    (?P<num>\\d*|\\d+(_\\d+)*)                # numerator (possibly empty)\n    (?:                                    # followed by\n       (?:\\s*/\\s*(?P<denom>\\d+(_\\d+)*))?   # an optional denominator\n    |                                      # or\n       (?:\\.(?P<decimal>\\d*|\\d+(_\\d+)*))?  # an optional fractional part\n       (?:E(?P<exp>[-+]?\\d+(_\\d+)*))?      # and optional exponent\n    )\n    \\s*\\z                                  # and optional whitespace to finish\n', re.VERBOSE | re.IGNORECASE)

def _round_to_exponent(n, d, exponent, no_neg_zero=False):
    """Round a rational number to the nearest multiple of a given power of 10.

    Rounds the rational number n/d to the nearest integer multiple of
    10**exponent, rounding to the nearest even integer multiple in the case of
    a tie. Returns a pair (sign: bool, significand: int) representing the
    rounded value (-1)**sign * significand * 10**exponent.

    If no_neg_zero is true, then the returned sign will always be False when
    the significand is zero. Otherwise, the sign reflects the sign of the
    input.

    d must be positive, but n and d need not be relatively prime.
    """
    if exponent >= 0:
        d *= 10 ** exponent
    else:
        n *= 10 ** (-exponent)
    q, r = divmod(n + (d >> 1), d)
    if r == 0 and d & 1 == 0:
        q &= -2
    sign = q < 0 if no_neg_zero else n < 0
    return (sign, abs(q))

def _round_to_figures(n, d, figures):
    """Round a rational number to a given number of significant figures.

    Rounds the rational number n/d to the given number of significant figures
    using the round-ties-to-even rule, and returns a triple
    (sign: bool, significand: int, exponent: int) representing the rounded
    value (-1)**sign * significand * 10**exponent.

    In the special case where n = 0, returns a significand of zero and
    an exponent of 1 - figures, for compatibility with formatting.
    Otherwise, the returned significand satisfies
    10**(figures - 1) <= significand < 10**figures.

    d must be positive, but n and d need not be relatively prime.
    figures must be positive.
    """
    if n == 0:
        return (False, 0, 1 - figures)
    str_n, str_d = (str(abs(n)), str(d))
    m = len(str_n) - len(str_d) + (str_d <= str_n)
    exponent = m - figures
    sign, significand = _round_to_exponent(n, d, exponent)
    if len(str(significand)) == figures + 1:
        significand //= 10
        exponent += 1
    return (sign, significand, exponent)
_GENERAL_FORMAT_SPECIFICATION_MATCHER = re.compile("\n    (?:\n        (?P<fill>.)?\n        (?P<align>[<>=^])\n    )?\n    (?P<sign>[-+ ]?)\n    # Alt flag forces a slash and denominator in the output, even for\n    # integer-valued Fraction objects.\n    (?P<alt>\\#)?\n    # We don't implement the zeropad flag since there's no single obvious way\n    # to interpret it.\n    (?P<minimumwidth>0|[1-9][0-9]*)?\n    (?P<thousands_sep>[,_])?\n", re.DOTALL | re.VERBOSE).fullmatch
_FLOAT_FORMAT_SPECIFICATION_MATCHER = re.compile("\n    (?:\n        (?P<fill>.)?\n        (?P<align>[<>=^])\n    )?\n    (?P<sign>[-+ ]?)\n    (?P<no_neg_zero>z)?\n    (?P<alt>\\#)?\n    # A '0' that's *not* followed by another digit is parsed as a minimum width\n    # rather than a zeropad flag.\n    (?P<zeropad>0(?=[0-9]))?\n    (?P<minimumwidth>[0-9]+)?\n    (?P<thousands_sep>[,_])?\n    (?:\\.\n        (?=[,_0-9])  # lookahead for digit or separator\n        (?P<precision>[0-9]+)?\n        (?P<frac_separators>[,_])?\n    )?\n    (?P<presentation_type>[eEfFgG%])\n", re.DOTALL | re.VERBOSE).fullmatch

class 分数(numbers.Rational):
    """This class implements rational numbers.

    In the two-argument form of the constructor, Fraction(8, 6) will
    produce a rational number equivalent to 4/3. Both arguments must
    be Rational. The numerator defaults to 0 and the denominator
    defaults to 1 so that Fraction(3) == 3 and Fraction() == 0.

    Fractions can also be constructed from:

      - numeric strings similar to those accepted by the
        float constructor (for example, '-2.3' or '1e10')

      - strings of the form '123/456'

      - float and Decimal instances

      - other Rational instances (including integers)

    """
    __slots__ = ('_numerator', '_denominator')

    def __new__(cls, numerator=0, denominator=None):
        """Constructs a Rational.

        Takes a string like '3/2' or '1.5', another Rational instance, a
        numerator/denominator pair, or a float.

        Examples
        --------

        >>> Fraction(10, -8)
        Fraction(-5, 4)
        >>> Fraction(Fraction(1, 7), 5)
        Fraction(1, 35)
        >>> Fraction(Fraction(1, 7), Fraction(2, 3))
        Fraction(3, 14)
        >>> Fraction('314')
        Fraction(314, 1)
        >>> Fraction('-35/4')
        Fraction(-35, 4)
        >>> Fraction('3.1415') # conversion from numeric string
        Fraction(6283, 2000)
        >>> Fraction('-47e-2') # string may include a decimal exponent
        Fraction(-47, 100)
        >>> Fraction(1.47)  # direct construction from float (exact conversion)
        Fraction(6620291452234629, 4503599627370496)
        >>> Fraction(2.25)
        Fraction(9, 4)
        >>> Fraction(Decimal('1.47'))
        Fraction(147, 100)

        """
        self = super(分数, cls).__new__(cls)
        if denominator is None:
            if type(numerator) is int:
                self._numerator = numerator
                self._denominator = 1
                return self
            elif isinstance(numerator, numbers.Rational):
                self._numerator = numerator.numerator
                self._denominator = numerator.denominator
                return self
            elif isinstance(numerator, float) or (not isinstance(numerator, type) and hasattr(numerator, 'as_integer_ratio')):
                self._numerator, self._denominator = numerator.as_integer_ratio()
                return self
            elif isinstance(numerator, str):
                m = _RATIONAL_FORMAT.match(numerator)
                if m is None:
                    raise ValueError('Invalid literal for Fraction: %r' % numerator)
                numerator = int(m.group('num') or '0')
                denom = m.group('denom')
                if denom:
                    denominator = int(denom)
                else:
                    denominator = 1
                    decimal = m.group('decimal')
                    if decimal:
                        decimal = decimal.replace('_', '')
                        scale = 10 ** len(decimal)
                        numerator = numerator * scale + int(decimal)
                        denominator *= scale
                    exp = m.group('exp')
                    if exp:
                        exp = int(exp)
                        if exp >= 0:
                            numerator *= 10 ** exp
                        else:
                            denominator *= 10 ** (-exp)
                if m.group('sign') == '-':
                    numerator = -numerator
            else:
                raise TypeError('argument should be a string or a Rational instance or have the as_integer_ratio() method')
        elif type(numerator) is int is type(denominator):
            pass
        elif isinstance(numerator, numbers.Rational) and isinstance(denominator, numbers.Rational):
            numerator, denominator = (numerator.numerator * denominator.denominator, denominator.numerator * numerator.denominator)
        else:
            raise TypeError('both arguments should be Rational instances')
        if denominator == 0:
            raise ZeroDivisionError('Fraction(%s, 0)' % numerator)
        g = math.gcd(numerator, denominator)
        if denominator < 0:
            g = -g
        numerator //= g
        denominator //= g
        self._numerator = numerator
        self._denominator = denominator
        return self

    @classmethod
    def 从数值(cls, number):
        """Converts a finite real number to a rational number, exactly.

        Beware that Fraction.from_number(0.3) != Fraction(3, 10).

        """
        if type(number) is int:
            return cls._from_coprime_ints(number, 1)
        elif isinstance(number, numbers.Rational):
            return cls._from_coprime_ints(number.numerator, number.denominator)
        elif isinstance(number, float) or (not isinstance(number, type) and hasattr(number, 'as_integer_ratio')):
            return cls._from_coprime_ints(*number.as_integer_ratio())
        else:
            raise TypeError('argument should be a Rational instance or have the as_integer_ratio() method')

    @classmethod
    def 从浮点(cls, f):
        """Converts a finite float to a rational number, exactly.

        Beware that Fraction.from_float(0.3) != Fraction(3, 10).

        """
        if isinstance(f, numbers.Integral):
            return cls(f)
        elif not isinstance(f, float):
            raise TypeError('%s.from_float() only takes floats, not %r (%s)' % (cls.__name__, f, type(f).__name__))
        return cls._from_coprime_ints(*f.as_integer_ratio())

    @classmethod
    def 从十进制(cls, dec):
        """Converts a finite Decimal instance to a rational number, exactly."""
        from decimal import Decimal
        if isinstance(dec, numbers.Integral):
            dec = Decimal(int(dec))
        elif not isinstance(dec, Decimal):
            raise TypeError('%s.from_decimal() only takes Decimals, not %r (%s)' % (cls.__name__, dec, type(dec).__name__))
        return cls._from_coprime_ints(*dec.as_integer_ratio())

    @classmethod
    def _from_coprime_ints(cls, numerator, denominator, /):
        """Convert a pair of ints to a rational number, for internal use.

        The ratio of integers should be in lowest terms and the denominator
        should be positive.
        """
        obj = super(分数, cls).__new__(cls)
        obj._numerator = numerator
        obj._denominator = denominator
        return obj

    def is_integer(self):
        """Return True if the Fraction is an integer."""
        return self._denominator == 1

    def as_integer_ratio(self):
        """Return a pair of integers, whose ratio is equal to the original Fraction.

        The ratio is in lowest terms and has a positive denominator.
        """
        return (self._numerator, self._denominator)

    def 限制分母(self, max_denominator=1000000):
        """Closest Fraction to self with denominator at most max_denominator.

        >>> Fraction('3.141592653589793').limit_denominator(10)
        Fraction(22, 7)
        >>> Fraction('3.141592653589793').limit_denominator(100)
        Fraction(311, 99)
        >>> Fraction(4321, 8765).limit_denominator(10000)
        Fraction(4321, 8765)

        """
        if max_denominator < 1:
            raise ValueError('max_denominator should be at least 1')
        if self._denominator <= max_denominator:
            return 分数(self)
        p0, q0, p1, q1 = (0, 1, 1, 0)
        n, d = (self._numerator, self._denominator)
        while True:
            a = n // d
            q2 = q0 + a * q1
            if q2 > max_denominator:
                break
            p0, q0, p1, q1 = (p1, q1, p0 + a * p1, q2)
            n, d = (d, n - a * d)
        k = (max_denominator - q0) // q1
        if 2 * d * (q0 + k * q1) <= self._denominator:
            return 分数._from_coprime_ints(p1, q1)
        else:
            return 分数._from_coprime_ints(p0 + k * p1, q0 + k * q1)

    @property
    def numerator(a):
        return a._numerator

    @property
    def denominator(a):
        return a._denominator

    def __repr__(self):
        """repr(self)"""
        return '%s(%s, %s)' % (self.__class__.__name__, self._numerator, self._denominator)

    def __str__(self):
        """str(self)"""
        if self._denominator == 1:
            return str(self._numerator)
        else:
            return '%s/%s' % (self._numerator, self._denominator)

    def _format_general(self, match):
        """Helper method for __format__.

        Handles fill, alignment, signs, and thousands separators in the
        case of no presentation type.
        """
        fill = match['fill'] or ' '
        align = match['align'] or '>'
        pos_sign = '' if match['sign'] == '-' else match['sign']
        alternate_form = bool(match['alt'])
        minimumwidth = int(match['minimumwidth'] or '0')
        thousands_sep = match['thousands_sep'] or ''
        n, d = (self._numerator, self._denominator)
        if d > 1 or alternate_form:
            body = f'{abs(n):{thousands_sep}}/{d:{thousands_sep}}'
        else:
            body = f'{abs(n):{thousands_sep}}'
        sign = '-' if n < 0 else pos_sign
        padding = fill * (minimumwidth - len(sign) - len(body))
        if align == '>':
            return padding + sign + body
        elif align == '<':
            return sign + body + padding
        elif align == '^':
            half = len(padding) // 2
            return padding[:half] + sign + body + padding[half:]
        else:
            return sign + padding + body

    def _format_float_style(self, match):
        """Helper method for __format__; handles float presentation types."""
        fill = match['fill'] or ' '
        align = match['align'] or '>'
        pos_sign = '' if match['sign'] == '-' else match['sign']
        no_neg_zero = bool(match['no_neg_zero'])
        alternate_form = bool(match['alt'])
        zeropad = bool(match['zeropad'])
        minimumwidth = int(match['minimumwidth'] or '0')
        thousands_sep = match['thousands_sep']
        precision = int(match['precision'] or '6')
        frac_sep = match['frac_separators'] or ''
        presentation_type = match['presentation_type']
        trim_zeros = presentation_type in 'gG' and (not alternate_form)
        trim_point = not alternate_form
        exponent_indicator = 'E' if presentation_type in 'EFG' else 'e'
        if align == '=' and fill == '0':
            zeropad = True
        if presentation_type in 'fF%':
            exponent = -precision
            if presentation_type == '%':
                exponent -= 2
            negative, significand = _round_to_exponent(self._numerator, self._denominator, exponent, no_neg_zero)
            scientific = False
            point_pos = precision
        else:
            figures = max(precision, 1) if presentation_type in 'gG' else precision + 1
            negative, significand, exponent = _round_to_figures(self._numerator, self._denominator, figures)
            scientific = presentation_type in 'eE' or exponent > 0 or exponent + figures <= -4
            point_pos = figures - 1 if scientific else -exponent
        if presentation_type == '%':
            suffix = '%'
        elif scientific:
            suffix = f'{exponent_indicator}{exponent + point_pos:+03d}'
        else:
            suffix = ''
        digits = f'{significand:0{point_pos + 1}d}'
        sign = '-' if negative else pos_sign
        leading = digits[:len(digits) - point_pos]
        frac_part = digits[len(digits) - point_pos:]
        if trim_zeros:
            frac_part = frac_part.rstrip('0')
        separator = '' if trim_point and (not frac_part) else '.'
        if frac_sep:
            frac_part = frac_sep.join((frac_part[pos:pos + 3] for pos in range(0, len(frac_part), 3)))
        trailing = separator + frac_part + suffix
        if zeropad:
            min_leading = minimumwidth - len(sign) - len(trailing)
            leading = leading.zfill(3 * min_leading // 4 + 1 if thousands_sep else min_leading)
        if thousands_sep:
            first_pos = 1 + (len(leading) - 1) % 3
            leading = leading[:first_pos] + ''.join((thousands_sep + leading[pos:pos + 3] for pos in range(first_pos, len(leading), 3)))
        body = leading + trailing
        padding = fill * (minimumwidth - len(sign) - len(body))
        if align == '>':
            return padding + sign + body
        elif align == '<':
            return sign + body + padding
        elif align == '^':
            half = len(padding) // 2
            return padding[:half] + sign + body + padding[half:]
        else:
            return sign + padding + body

    def __format__(self, format_spec, /):
        """Format this fraction according to the given format specification."""
        if (match := _GENERAL_FORMAT_SPECIFICATION_MATCHER(format_spec)):
            return self._format_general(match)
        if (match := _FLOAT_FORMAT_SPECIFICATION_MATCHER(format_spec)):
            if match['align'] is None or match['zeropad'] is None:
                return self._format_float_style(match)
        raise ValueError(f'Invalid format specifier {format_spec!r} for object of type {type(self).__name__!r}')

    def _operator_fallbacks(monomorphic_operator, fallback_operator, handle_complex=True):
        """Generates forward and reverse operators given a purely-rational
        operator and a function from the operator module.

        Use this like:
        __op__, __rop__ = _operator_fallbacks(just_rational_op, operator.op)

        In general, we want to implement the arithmetic operations so
        that mixed-mode operations either call an implementation whose
        author knew about the types of both arguments, or convert both
        to the nearest built in type and do the operation there. In
        Fraction, that means that we define __add__ and __radd__ as:

            def __add__(self, other):
                # Both types have numerators/denominator attributes,
                # so do the operation directly
                if isinstance(other, (int, Fraction)):
                    return Fraction(self.numerator * other.denominator +
                                    other.numerator * self.denominator,
                                    self.denominator * other.denominator)
                # float and complex don't have those operations, but we
                # know about those types, so special case them.
                elif isinstance(other, float):
                    return float(self) + other
                elif isinstance(other, complex):
                    return complex(self) + other
                # Let the other type take over.
                return NotImplemented

            def __radd__(self, other):
                # radd handles more types than add because there's
                # nothing left to fall back to.
                if isinstance(other, numbers.Rational):
                    return Fraction(self.numerator * other.denominator +
                                    other.numerator * self.denominator,
                                    self.denominator * other.denominator)
                elif isinstance(other, Real):
                    return float(other) + float(self)
                elif isinstance(other, Complex):
                    return complex(other) + complex(self)
                return NotImplemented


        There are 5 different cases for a mixed-type addition on
        Fraction. I'll refer to all of the above code that doesn't
        refer to Fraction, float, or complex as "boilerplate". 'r'
        will be an instance of Fraction, which is a subtype of
        Rational (r : Fraction <: Rational), and b : B <:
        Complex. The first three involve 'r + b':

            1. If B <: Fraction, int, float, or complex, we handle
               that specially, and all is well.
            2. If Fraction falls back to the boilerplate code, and it
               were to return a value from __add__, we'd miss the
               possibility that B defines a more intelligent __radd__,
               so the boilerplate should return NotImplemented from
               __add__. In particular, we don't handle Rational
               here, even though we could get an exact answer, in case
               the other type wants to do something special.
            3. If B <: Fraction, Python tries B.__radd__ before
               Fraction.__add__. This is ok, because it was
               implemented with knowledge of Fraction, so it can
               handle those instances before delegating to Real or
               Complex.

        The next two situations describe 'b + r'. We assume that b
        didn't know about Fraction in its implementation, and that it
        uses similar boilerplate code:

            4. If B <: Rational, then __radd_ converts both to the
               builtin rational type (hey look, that's us) and
               proceeds.
            5. Otherwise, __radd__ tries to find the nearest common
               base ABC, and fall back to its builtin type. Since this
               class doesn't subclass a concrete type, there's no
               implementation to fall back to, so we need to try as
               hard as possible to return an actual value, or the user
               will get a TypeError.

        """

        def forward(a, b):
            if isinstance(b, 分数):
                return monomorphic_operator(a, b)
            elif isinstance(b, int):
                return monomorphic_operator(a, 分数(b))
            elif isinstance(b, float):
                return fallback_operator(float(a), b)
            elif handle_complex and isinstance(b, complex):
                return fallback_operator(float(a), b)
            else:
                return NotImplemented
        forward.__name__ = '__' + fallback_operator.__name__ + '__'
        forward.__doc__ = monomorphic_operator.__doc__

        def reverse(b, a):
            if isinstance(a, numbers.Rational):
                return monomorphic_operator(分数(a), b)
            elif isinstance(a, numbers.Real):
                return fallback_operator(float(a), float(b))
            elif handle_complex and isinstance(a, numbers.Complex):
                return fallback_operator(complex(a), float(b))
            else:
                return NotImplemented
        reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
        reverse.__doc__ = monomorphic_operator.__doc__
        return (forward, reverse)

    def _add(a, b):
        """a + b"""
        na, da = (a._numerator, a._denominator)
        nb, db = (b._numerator, b._denominator)
        g = math.gcd(da, db)
        if g == 1:
            return 分数._from_coprime_ints(na * db + da * nb, da * db)
        s = da // g
        t = na * (db // g) + nb * s
        g2 = math.gcd(t, g)
        if g2 == 1:
            return 分数._from_coprime_ints(t, s * db)
        return 分数._from_coprime_ints(t // g2, s * (db // g2))
    __add__, __radd__ = _operator_fallbacks(_add, operator.add)

    def _sub(a, b):
        """a - b"""
        na, da = (a._numerator, a._denominator)
        nb, db = (b._numerator, b._denominator)
        g = math.gcd(da, db)
        if g == 1:
            return 分数._from_coprime_ints(na * db - da * nb, da * db)
        s = da // g
        t = na * (db // g) - nb * s
        g2 = math.gcd(t, g)
        if g2 == 1:
            return 分数._from_coprime_ints(t, s * db)
        return 分数._from_coprime_ints(t // g2, s * (db // g2))
    __sub__, __rsub__ = _operator_fallbacks(_sub, operator.sub)

    def _mul(a, b):
        """a * b"""
        na, da = (a._numerator, a._denominator)
        nb, db = (b._numerator, b._denominator)
        g1 = math.gcd(na, db)
        if g1 > 1:
            na //= g1
            db //= g1
        g2 = math.gcd(nb, da)
        if g2 > 1:
            nb //= g2
            da //= g2
        return 分数._from_coprime_ints(na * nb, db * da)
    __mul__, __rmul__ = _operator_fallbacks(_mul, operator.mul)

    def _div(a, b):
        """a / b"""
        nb, db = (b._numerator, b._denominator)
        if nb == 0:
            raise ZeroDivisionError('Fraction(%s, 0)' % db)
        na, da = (a._numerator, a._denominator)
        g1 = math.gcd(na, nb)
        if g1 > 1:
            na //= g1
            nb //= g1
        g2 = math.gcd(db, da)
        if g2 > 1:
            da //= g2
            db //= g2
        n, d = (na * db, nb * da)
        if d < 0:
            n, d = (-n, -d)
        return 分数._from_coprime_ints(n, d)
    __truediv__, __rtruediv__ = _operator_fallbacks(_div, operator.truediv)

    def _floordiv(a, b):
        """a // b"""
        return a.numerator * b.denominator // (a.denominator * b.numerator)
    __floordiv__, __rfloordiv__ = _operator_fallbacks(_floordiv, operator.floordiv, False)

    def _divmod(a, b):
        """(a // b, a % b)"""
        da, db = (a.denominator, b.denominator)
        div, n_mod = divmod(a.numerator * db, da * b.numerator)
        return (div, 分数(n_mod, da * db))
    __divmod__, __rdivmod__ = _operator_fallbacks(_divmod, divmod, False)

    def _mod(a, b):
        """a % b"""
        da, db = (a.denominator, b.denominator)
        return 分数(a.numerator * db % (b.numerator * da), da * db)
    __mod__, __rmod__ = _operator_fallbacks(_mod, operator.mod, False)

    def __pow__(a, b, modulo=None):
        """a ** b

        If b is not an integer, the result will be a float or complex
        since roots are generally irrational. If b is an integer, the
        result will be rational.

        """
        if modulo is not None:
            return NotImplemented
        if isinstance(b, numbers.Rational):
            if b.denominator == 1:
                power = b.numerator
                if power >= 0:
                    return 分数._from_coprime_ints(a._numerator ** power, a._denominator ** power)
                elif a._numerator > 0:
                    return 分数._from_coprime_ints(a._denominator ** (-power), a._numerator ** (-power))
                elif a._numerator == 0:
                    raise ZeroDivisionError('Fraction(%s, 0)' % a._denominator ** (-power))
                else:
                    return 分数._from_coprime_ints((-a._denominator) ** (-power), (-a._numerator) ** (-power))
            else:
                return float(a) ** float(b)
        elif isinstance(b, (float, complex)):
            return float(a) ** b
        else:
            return NotImplemented

    def __rpow__(b, a, modulo=None):
        """a ** b"""
        if modulo is not None:
            return NotImplemented
        if b._denominator == 1 and b._numerator >= 0:
            return a ** b._numerator
        if isinstance(a, numbers.Rational):
            return 分数(a.numerator, a.denominator) ** b
        if b._denominator == 1:
            return a ** b._numerator
        return a ** float(b)

    def __pos__(a):
        """+a: Coerces a subclass instance to Fraction"""
        return 分数._from_coprime_ints(a._numerator, a._denominator)

    def __neg__(a):
        """-a"""
        return 分数._from_coprime_ints(-a._numerator, a._denominator)

    def __abs__(a):
        """abs(a)"""
        return 分数._from_coprime_ints(abs(a._numerator), a._denominator)

    def __int__(a, _index=operator.index):
        """int(a)"""
        if a._numerator < 0:
            return _index(-(-a._numerator // a._denominator))
        else:
            return _index(a._numerator // a._denominator)

    def __trunc__(a):
        """math.trunc(a)"""
        if a._numerator < 0:
            return -(-a._numerator // a._denominator)
        else:
            return a._numerator // a._denominator

    def __floor__(a):
        """math.floor(a)"""
        return a._numerator // a._denominator

    def __ceil__(a):
        """math.ceil(a)"""
        return -(-a._numerator // a._denominator)

    def __round__(self, ndigits=None):
        """round(self, ndigits)

        Rounds half toward even.
        """
        if ndigits is None:
            d = self._denominator
            floor, remainder = divmod(self._numerator, d)
            if remainder * 2 < d:
                return floor
            elif remainder * 2 > d:
                return floor + 1
            elif floor % 2 == 0:
                return floor
            else:
                return floor + 1
        shift = 10 ** abs(ndigits)
        if ndigits > 0:
            return 分数(round(self * shift), shift)
        else:
            return 分数(round(self / shift) * shift)

    def __hash__(self):
        """hash(self)"""
        return _hash_algorithm(self._numerator, self._denominator)

    def __eq__(a, b):
        """a == b"""
        if type(b) is int:
            return a._numerator == b and a._denominator == 1
        if isinstance(b, numbers.Rational):
            return a._numerator == b.numerator and a._denominator == b.denominator
        if isinstance(b, numbers.Complex) and b.imag == 0:
            b = b.real
        if isinstance(b, float):
            if math.isnan(b) or math.isinf(b):
                return 0.0 == b
            else:
                return a == a.from_float(b)
        else:
            return NotImplemented

    def _richcmp(self, other, op):
        """Helper for comparison operators, for internal use only.

        Implement comparison between a Rational instance `self`, and
        either another Rational instance or a float `other`.  If
        `other` is not a Rational instance or a float, return
        NotImplemented. `op` should be one of the six standard
        comparison operators.

        """
        if isinstance(other, numbers.Rational):
            return op(self._numerator * other.denominator, self._denominator * other.numerator)
        if isinstance(other, float):
            if math.isnan(other) or math.isinf(other):
                return op(0.0, other)
            else:
                return op(self, self.从浮点(other))
        else:
            return NotImplemented

    def __lt__(a, b):
        """a < b"""
        return a._richcmp(b, operator.lt)

    def __gt__(a, b):
        """a > b"""
        return a._richcmp(b, operator.gt)

    def __le__(a, b):
        """a <= b"""
        return a._richcmp(b, operator.le)

    def __ge__(a, b):
        """a >= b"""
        return a._richcmp(b, operator.ge)

    def __bool__(a):
        """a != 0"""
        return bool(a._numerator)

    def __reduce__(self):
        return (self.__class__, (self._numerator, self._denominator))

    def __copy__(self):
        if type(self) == 分数:
            return self
        return self.__class__(self._numerator, self._denominator)

    def __deepcopy__(self, memo):
        if type(self) == 分数:
            return self
        return self.__class__(self._numerator, self._denominator)
_装类转发(分数, {'from_decimal': '从十进制', 'from_float': '从浮点', 'from_number': '从数值', 'limit_denominator': '限制分母'}, {'from_decimal': '从十进制', 'from_float': '从浮点', 'from_number': '从数值', 'limit_denominator': '限制分母'})


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Fraction': '分数',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '分数': {
        'from_decimal': '从十进制',
        'from_float': '从浮点',
        'from_number': '从数值',
        'limit_denominator': '限制分母',
    },
}
_转发跳过 = []
_无 = object()    # 哨兵：类属性**值就是 None** 时 ≠ 「没找到」（D-126 修的真 bug）
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # ★必须从 __dict__ 拿**描述符本体**，不能用 getattr(类, 名)：
        #   getattr 会把 classmethod/staticmethod/property **绑到本类上**，
        #   再挂成别名之后，**子类**调用拿到的还是绑死在本类的那个 ——
        #   DummyFraction.from_number(...) 会返回基类实例
        #   （fractions 的 testFromNumber_subclass 就是这么挂的，见 D-035）。
        _原 = _类.__dict__.get(_中, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _中 in _基.__dict__:
                    _原 = _基.__dict__[_中]
                    break
        if _原 is _无:
            _转发跳过.append((_类名, _英, _中))
            continue
        setattr(_类, _英, _原)

# 中文成员名的兜底（D-125 起，D-126 推广到全部类）：上面主循环只认「中文名在类里」，
#   找不到就跳过 —— 可中文名**本来就不在类里**有两种情况：① 类名走了身份别名
#   （机制 3），指向英文那个对象；② 改名被规则挡下（那个名字是 import 进来的）。
#   实测 `注解库.前向引用('X').求值()`、`选择器.select选择器.选择` 都是 AttributeError。
#   这里反过来挂：从英文名取**描述符本体**，把中文名加上去。只加描述符别名，
#   **不装钩子**（英文类协议不改，照 D-070）；C 类型不可变、setattr 抛 TypeError 就跳过
#   （C 类型的方法名归机制 1 的方法名表管）。
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # 中文名已经在类里（改名成功）⇒ 没事，主循环已把英文名补回去了。
        if _中 in _类.__dict__ or any(_中 in _基.__dict__ for _基 in _类.__mro__):
            continue
        _原 = _类.__dict__.get(_英, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _英 in _基.__dict__:
                    _原 = _基.__dict__[_英]
                    break
        if _原 is None:
            _转发跳过.append((_类名, _英, _中))
            continue
        try:
            setattr(_类, _中, _原)
        except TypeError:
            continue    # C 类型不可变挂不上；主循环已经记过一笔，不重复记
        if (_类名, _英, _中) in _转发跳过:
            _转发跳过.remove((_类名, _英, _中))

# 实例属性：两个方向都翻（英文名 <-> 中文名）。
# **逻辑只有一份**，在 `_装类转发` 里 —— 每个类定义紧后面已经装过一次
# （照 D-040），这里是文件末尾的兜底，幂等。
_实例属性 = {
    '分数': {
        'from_decimal': '从十进制',
        'from_float': '从浮点',
        'from_number': '从数值',
        'limit_denominator': '限制分母',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '分数',
])

# ---- 转发层结束 ----
