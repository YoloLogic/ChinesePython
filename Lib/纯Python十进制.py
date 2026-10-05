# -*- coding: utf-8 -*-
"""纯Python十进制 —— 汉语库（由 tools/汉化库.py 从 Lib/_pydecimal.py 机械生成，**不要手改**）。

英文库 Lib/_pydecimal.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 纯Python十进制
"""


"""Python decimal arithmetic module"""
_英文原名表 = {'BasicContext': '基本上下文', 'Clamped': '被钳位', 'Context': '十进制上下文', 'ConversionSyntax': '转换语法错误', 'Decimal': '十进制数', 'DecimalException': '十进制错误', 'DecimalTuple': '十进制元组', 'DefaultContext': '默认上下文', 'DivisionByZero': '除零', 'DivisionImpossible': '除不尽', 'DivisionUndefined': '除法未定义', 'ExtendedContext': '扩展上下文', 'FloatOperation': '浮点混用', 'HAVE_CONTEXTVAR': '有上下文变量', 'HAVE_THREADS': '有线程支持', 'IEEEContext': 'IEEE上下文', 'IEEE_CONTEXT_MAX_BITS': 'IEEE上下文最大位数', 'Inexact': '不精确', 'InvalidContext': '无效上下文', 'InvalidOperation': '无效运算', 'MAX_EMAX': '最大指数上限', 'MAX_PREC': '最大精度', 'MIN_EMIN': '最小指数下限', 'MIN_ETINY': '最小指数理论下限', 'Overflow': '上溢', 'ROUND_05UP': '零五上舍入', 'ROUND_CEILING': '向上取整', 'ROUND_DOWN': '向下舍入', 'ROUND_FLOOR': '向下取整', 'ROUND_HALF_DOWN': '半下舍入', 'ROUND_HALF_EVEN': '银行家舍入', 'ROUND_HALF_UP': '四舍五入', 'ROUND_UP': '向上舍入', 'Rounded': '已舍入', 'Subnormal': '次正规', 'Underflow': '下溢', 'getcontext': '取上下文', 'localcontext': '本地上下文', 'setcontext': '设上下文'}

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
__all__ = ['Decimal', 'Context', 'DecimalTuple', 'DefaultContext', 'BasicContext', 'ExtendedContext', 'DecimalException', 'Clamped', 'InvalidOperation', 'DivisionByZero', 'Inexact', 'Rounded', 'Subnormal', 'Overflow', 'Underflow', 'FloatOperation', 'DivisionImpossible', 'InvalidContext', 'ConversionSyntax', 'DivisionUndefined', 'ROUND_DOWN', 'ROUND_HALF_UP', 'ROUND_HALF_EVEN', 'ROUND_CEILING', 'ROUND_FLOOR', 'ROUND_UP', 'ROUND_HALF_DOWN', 'ROUND_05UP', 'setcontext', 'getcontext', 'localcontext', 'IEEEContext', 'MAX_PREC', 'MAX_EMAX', 'MIN_EMIN', 'MIN_ETINY', 'IEEE_CONTEXT_MAX_BITS', 'HAVE_THREADS', 'HAVE_CONTEXTVAR']
__xname__ = __name__
__name__ = 'decimal'
__version__ = '1.70'
__libmpdec_version__ = '2.4.2'
import math as _math
import numbers as _numbers
import sys
try:
    from collections import namedtuple as _namedtuple
    十进制元组 = _namedtuple('DecimalTuple', 'sign digits exponent', module='decimal')
except ImportError:
    十进制元组 = lambda *args: args
向下舍入 = 'ROUND_DOWN'
四舍五入 = 'ROUND_HALF_UP'
银行家舍入 = 'ROUND_HALF_EVEN'
向上取整 = 'ROUND_CEILING'
向下取整 = 'ROUND_FLOOR'
向上舍入 = 'ROUND_UP'
半下舍入 = 'ROUND_HALF_DOWN'
零五上舍入 = 'ROUND_05UP'
有线程支持 = True
有上下文变量 = True
if sys.maxsize == 2 ** 63 - 1:
    最大精度 = 999999999999999999
    最大指数上限 = 999999999999999999
    最小指数下限 = -999999999999999999
    IEEE上下文最大位数 = 512
else:
    最大精度 = 425000000
    最大指数上限 = 425000000
    最小指数下限 = -425000000
    IEEE上下文最大位数 = 256
最小指数理论下限 = 最小指数下限 - (最大精度 - 1)

class 十进制错误(ArithmeticError):
    """Base exception class.

    Used exceptions derive from this.
    If an exception derives from another exception besides this (such as
    Underflow (Inexact, Rounded, Subnormal)) that indicates that it is only
    called if the others are present.  This isn't actually used for
    anything, though.

    handle  -- Called when context._raise_error is called and the
               trap_enabler is not set.  First argument is self, second is
               the context.  More arguments can be given, those being after
               the explanation in _raise_error (For example,
               context._raise_error(NewError, '(-x)!', self._sign) would
               call NewError().handle(context, self._sign).)

    To define a new exception, it should be sufficient to have it derive
    from DecimalException.
    """

    def handle(self, context, *args):
        pass

class 被钳位(十进制错误):
    """Exponent of a 0 changed to fit bounds.

    This occurs and signals clamped if the exponent of a result has been
    altered in order to fit the constraints of a specific concrete
    representation.  This may occur when the exponent of a zero result would
    be outside the bounds of a representation, or when a large normal
    number would have an encoded exponent that cannot be represented.  In
    this latter case, the exponent is reduced to fit and the corresponding
    number of zero digits are appended to the coefficient ("fold-down").
    """

class 无效运算(十进制错误):
    """An invalid operation was performed.

    Various bad things cause this:

    Something creates a signaling NaN
    -INF + INF
    0 * (+-)INF
    (+-)INF / (+-)INF
    x % 0
    (+-)INF % x
    x._rescale( non-integer )
    sqrt(-x) , x > 0
    0 ** 0
    x ** (non-integer)
    x ** (+-)INF
    An operand is invalid

    The result of the operation after this is a quiet positive NaN,
    except when the cause is a signaling NaN, in which case the result is
    also a quiet NaN, but with the original sign, and an optional
    diagnostic information.
    """

    def handle(self, context, *args):
        if args:
            ans = _dec_from_triple(args[0]._sign, args[0]._int, 'n', True)
            return ans._fix_nan(context)
        return _NaN

class 转换语法错误(无效运算):
    """Trying to convert badly formed string.

    This occurs and signals invalid-operation if a string is being
    converted to a number and it does not conform to the numeric string
    syntax.  The result is [0,qNaN].
    """

    def handle(self, context, *args):
        return _NaN

class 除零(十进制错误, ZeroDivisionError):
    """Division by 0.

    This occurs and signals division-by-zero if division of a finite number
    by zero was attempted (during a divide-integer or divide operation, or a
    power operation with negative right-hand operand), and the dividend was
    not zero.

    The result of the operation is [sign,inf], where sign is the exclusive
    or of the signs of the operands for divide, or is 1 for an odd power of
    -0, for power.
    """

    def handle(self, context, sign, *args):
        return _SignedInfinity[sign]

class 除不尽(无效运算):
    """Cannot perform the division adequately.

    This occurs and signals invalid-operation if the integer result of a
    divide-integer or remainder operation had too many digits (would be
    longer than precision).  The result is [0,qNaN].
    """

    def handle(self, context, *args):
        return _NaN

class 除法未定义(无效运算, ZeroDivisionError):
    """Undefined result of division.

    This occurs and signals invalid-operation if division by zero was
    attempted (during a divide-integer, divide, or remainder operation), and
    the dividend is also zero.  The result is [0,qNaN].
    """

    def handle(self, context, *args):
        return _NaN

class 不精确(十进制错误):
    """Had to round, losing information.

    This occurs and signals inexact whenever the result of an operation is
    not exact (that is, it needed to be rounded and any discarded digits
    were non-zero), or if an overflow or underflow condition occurs.  The
    result in all cases is unchanged.

    The inexact signal may be tested (or trapped) to determine if a given
    operation (or sequence of operations) was inexact.
    """

class 无效上下文(无效运算):
    """Invalid context.  Unknown rounding, for example.

    This occurs and signals invalid-operation if an invalid context was
    detected during an operation.  This can occur if contexts are not
    checked on creation and either the precision exceeds the capability of
    the underlying concrete representation or an unknown or unsupported
    rounding was specified.  These aspects of the context need only be
    checked when the values are required to be used.  The result is
    [0,qNaN].
    """

    def handle(self, context, *args):
        return _NaN

class 已舍入(十进制错误):
    """Number got rounded (not  necessarily changed during rounding).

    This occurs and signals rounded whenever the result of an operation is
    rounded (that is, some zero or non-zero digits were discarded from the
    coefficient), or if an overflow or underflow condition occurs.  The
    result in all cases is unchanged.

    The rounded signal may be tested (or trapped) to determine if a given
    operation (or sequence of operations) caused a loss of precision.
    """

class 次正规(十进制错误):
    """Exponent < Emin before rounding.

    This occurs and signals subnormal whenever the result of a conversion or
    operation is subnormal (that is, its adjusted exponent is less than
    Emin, before any rounding).  The result in all cases is unchanged.

    The subnormal signal may be tested (or trapped) to determine if a given
    or operation (or sequence of operations) yielded a subnormal result.
    """

class 上溢(不精确, 已舍入):
    """Numerical overflow.

    This occurs and signals overflow if the adjusted exponent of a result
    (from a conversion or from an operation that is not an attempt to divide
    by zero), after rounding, would be greater than the largest value that
    can be handled by the implementation (the value Emax).

    The result depends on the rounding mode:

    For round-half-up and round-half-even (and for round-half-down and
    round-up, if implemented), the result of the operation is [sign,inf],
    where sign is the sign of the intermediate result.  For round-down, the
    result is the largest finite number that can be represented in the
    current precision, with the sign of the intermediate result.  For
    round-ceiling, the result is the same as for round-down if the sign of
    the intermediate result is 1, or is [0,inf] otherwise.  For round-floor,
    the result is the same as for round-down if the sign of the intermediate
    result is 0, or is [1,inf] otherwise.  In all cases, Inexact and Rounded
    will also be raised.
    """

    def handle(self, context, sign, *args):
        if context.rounding in (四舍五入, 银行家舍入, 半下舍入, 向上舍入):
            return _SignedInfinity[sign]
        if sign == 0:
            if context.rounding == 向上取整:
                return _SignedInfinity[sign]
            return _dec_from_triple(sign, '9' * context.prec, context.Emax - context.prec + 1)
        if sign == 1:
            if context.rounding == 向下取整:
                return _SignedInfinity[sign]
            return _dec_from_triple(sign, '9' * context.prec, context.Emax - context.prec + 1)

class 下溢(不精确, 已舍入, 次正规):
    """Numerical underflow with result rounded to 0.

    This occurs and signals underflow if a result is inexact and the
    adjusted exponent of the result would be smaller (more negative) than
    the smallest value that can be handled by the implementation (the value
    Emin).  That is, the result is both inexact and subnormal.

    The result after an underflow will be a subnormal number rounded, if
    necessary, so that its exponent is not less than Etiny.  This may result
    in 0 with the sign of the intermediate result and an exponent of Etiny.

    In all cases, Inexact, Rounded, and Subnormal will also be raised.
    """

class 浮点混用(十进制错误, TypeError):
    """Enable stricter semantics for mixing floats and Decimals.

    If the signal is not trapped (default), mixing floats and Decimals is
    permitted in the Decimal() constructor, context.create_decimal() and
    all comparison operators. Both conversion and comparisons are exact.
    Any occurrence of a mixed operation is silently recorded by setting
    FloatOperation in the context flags.  Explicit conversions with
    Decimal.from_float() or context.create_decimal_from_float() do not
    set the flag.

    Otherwise (the signal is trapped), only equality comparisons and
    explicit conversions are silent.  All other mixed operations raise
    FloatOperation.
    """
_signals = [被钳位, 除零, 不精确, 上溢, 已舍入, 下溢, 无效运算, 次正规, 浮点混用]
_condition_map = {转换语法错误: 无效运算, 除不尽: 无效运算, 除法未定义: 无效运算, 无效上下文: 无效运算}
_rounding_modes = (向下舍入, 四舍五入, 银行家舍入, 向上取整, 向下取整, 向上舍入, 半下舍入, 零五上舍入)
import contextvars
_current_context_var = contextvars.ContextVar('decimal_context')
_context_attributes = frozenset(['prec', 'Emin', 'Emax', 'capitals', 'clamp', 'rounding', 'flags', 'traps'])

def 取上下文():
    """Returns this thread's context.

    If this thread does not yet have a context, returns
    a new context and sets this thread's context.
    New contexts are copies of DefaultContext.
    """
    try:
        return _current_context_var.get()
    except LookupError:
        context = 十进制上下文()
        _current_context_var.set(context)
        return context

def 设上下文(context):
    """Set this thread's context to context."""
    if context in (默认上下文, 基本上下文, 扩展上下文):
        context = context.copy()
        context.clear_flags()
    _current_context_var.set(context)
del contextvars

def 本地上下文(ctx=None, **kwargs):
    """Return a context manager for a copy of the supplied context

    Uses a copy of the current context if no context is specified
    The returned context manager creates a local decimal context
    in a with statement:
        def sin(x):
             with localcontext() as ctx:
                 ctx.prec += 2
                 # Rest of sin calculation algorithm
                 # uses a precision 2 greater than normal
             return +s  # Convert result to normal precision

         def sin(x):
             with localcontext(ExtendedContext):
                 # Rest of sin calculation algorithm
                 # uses the Extended Context from the
                 # General Decimal Arithmetic Specification
             return +s  # Convert result to normal context

    >>> setcontext(DefaultContext)
    >>> print(getcontext().prec)
    28
    >>> with localcontext():
    ...     ctx = getcontext()
    ...     ctx.prec += 2
    ...     print(ctx.prec)
    ...
    30
    >>> with localcontext(ExtendedContext):
    ...     print(getcontext().prec)
    ...
    9
    >>> print(getcontext().prec)
    28
    """
    if ctx is None:
        ctx = 取上下文()
    ctx_manager = _ContextManager(ctx)
    for key, value in kwargs.items():
        if key not in _context_attributes:
            raise TypeError(f"'{key}' is an invalid keyword argument for this function")
        setattr(ctx_manager.new_context, key, value)
    return ctx_manager

def IEEE上下文(bits, /):
    """
    Return a context object initialized to the proper values for one of the
    IEEE interchange formats.  The argument must be a multiple of 32 and less
    than IEEE_CONTEXT_MAX_BITS.
    """
    if bits <= 0 or bits > IEEE上下文最大位数 or bits % 32:
        raise ValueError(f'argument must be a multiple of 32, with a maximum of {IEEE上下文最大位数}')
    ctx = 十进制上下文()
    ctx.prec = 9 * (bits // 32) - 2
    ctx.Emax = 3 * (1 << bits // 16 + 3)
    ctx.Emin = 1 - ctx.Emax
    ctx.rounding = 银行家舍入
    ctx.clamp = 1
    ctx.traps = dict.fromkeys(_signals, False)
    return ctx

class 十进制数(object):
    """Floating-point class for decimal arithmetic."""
    __slots__ = ('_exp', '_int', '_sign', '_is_special')

    def __new__(cls, value='0', context=None):
        """Create a decimal point instance.

        >>> Decimal('3.14')              # string input
        Decimal('3.14')
        >>> Decimal((0, (3, 1, 4), -2))  # tuple (sign, digit_tuple, exponent)
        Decimal('3.14')
        >>> Decimal(314)                 # int
        Decimal('314')
        >>> Decimal(Decimal(314))        # another decimal instance
        Decimal('314')
        >>> Decimal('  3.14  \\n')        # leading and trailing whitespace okay
        Decimal('3.14')
        """
        self = object.__new__(cls)
        if isinstance(value, str):
            m = _parser(value.strip().replace('_', ''))
            if m is None:
                if context is None:
                    context = 取上下文()
                return context._raise_error(转换语法错误, 'Invalid literal for Decimal: %r' % value)
            if m.group('sign') == '-':
                self._sign = 1
            else:
                self._sign = 0
            intpart = m.group('int')
            if intpart is not None:
                fracpart = m.group('frac') or ''
                指数 = int(m.group('exp') or '0')
                self._int = str(int(intpart + fracpart))
                self._exp = 指数 - len(fracpart)
                self._is_special = False
            else:
                diag = m.group('diag')
                if diag is not None:
                    self._int = str(int(diag or '0')).lstrip('0')
                    if m.group('signal'):
                        self._exp = 'N'
                    else:
                        self._exp = 'n'
                else:
                    self._int = '0'
                    self._exp = 'F'
                self._is_special = True
            return self
        if isinstance(value, int):
            if value >= 0:
                self._sign = 0
            else:
                self._sign = 1
            self._exp = 0
            self._int = str(abs(value))
            self._is_special = False
            return self
        if isinstance(value, 十进制数):
            self._exp = value._exp
            self._sign = value._sign
            self._int = value._int
            self._is_special = value._is_special
            return self
        if isinstance(value, _WorkRep):
            self._sign = value.sign
            self._int = str(value.int)
            self._exp = int(value.exp)
            self._is_special = False
            return self
        if isinstance(value, (list, tuple)):
            if len(value) != 3:
                raise ValueError('Invalid tuple size in creation of Decimal from list or tuple.  The list or tuple should have exactly three elements.')
            if not (isinstance(value[0], int) and value[0] in (0, 1)):
                raise ValueError('Invalid sign.  The first value in the tuple should be an integer; either 0 for a positive number or 1 for a negative number.')
            self._sign = value[0]
            if value[2] == 'F':
                self._int = '0'
                self._exp = value[2]
                self._is_special = True
            else:
                digits = []
                for digit in value[1]:
                    if isinstance(digit, int) and 0 <= digit <= 9:
                        if digits or digit != 0:
                            digits.append(digit)
                    else:
                        raise ValueError('The second value in the tuple must be composed of integers in the range 0 through 9.')
                if value[2] in ('n', 'N'):
                    self._int = ''.join(map(str, digits))
                    self._exp = value[2]
                    self._is_special = True
                elif isinstance(value[2], int):
                    self._int = ''.join(map(str, digits or [0]))
                    self._exp = value[2]
                    self._is_special = False
                else:
                    raise ValueError("The third value in the tuple must be an integer, or one of the strings 'F', 'n', 'N'.")
            return self
        if isinstance(value, float):
            if context is None:
                context = 取上下文()
            context._raise_error(浮点混用, 'strict semantics for mixing floats and Decimals are enabled')
            value = 十进制数.从浮点数(value)
            self._exp = value._exp
            self._sign = value._sign
            self._int = value._int
            self._is_special = value._is_special
            return self
        raise TypeError('Cannot convert %r to Decimal' % value)

    @classmethod
    def 从数值(cls, number):
        """Converts a real number to a decimal number, exactly.

        >>> Decimal.from_number(314)              # int
        Decimal('314')
        >>> Decimal.from_number(0.1)              # float
        Decimal('0.1000000000000000055511151231257827021181583404541015625')
        >>> Decimal.from_number(Decimal('3.14'))  # another decimal instance
        Decimal('3.14')
        """
        if isinstance(number, (int, 十进制数, float)):
            return cls(number)
        raise TypeError('Cannot convert %r to Decimal' % number)

    @classmethod
    def 从浮点数(cls, f):
        """Converts a float to a decimal number, exactly.

        Note that Decimal.from_float(0.1) is not the same as Decimal('0.1').
        Since 0.1 is not exactly representable in binary floating point, the
        value is stored as the nearest representable value which is
        0x1.999999999999ap-4.  The exact equivalent of the value in decimal
        is 0.1000000000000000055511151231257827021181583404541015625.

        >>> Decimal.from_float(0.1)
        Decimal('0.1000000000000000055511151231257827021181583404541015625')
        >>> Decimal.from_float(float('nan'))
        Decimal('NaN')
        >>> Decimal.from_float(float('inf'))
        Decimal('Infinity')
        >>> Decimal.from_float(-float('inf'))
        Decimal('-Infinity')
        >>> Decimal.from_float(-0.0)
        Decimal('-0')

        """
        if isinstance(f, int):
            sign = 0 if f >= 0 else 1
            k = 0
            coeff = str(abs(f))
        elif isinstance(f, float):
            if _math.isinf(f) or _math.isnan(f):
                return cls(repr(f))
            if _math.copysign(1.0, f) == 1.0:
                sign = 0
            else:
                sign = 1
            n, d = abs(f).as_integer_ratio()
            k = d.bit_length() - 1
            coeff = str(n * 5 ** k)
        else:
            raise TypeError('argument must be int or float.')
        result = _dec_from_triple(sign, coeff, -k)
        if cls is 十进制数:
            return result
        else:
            return cls(result)

    def _isnan(self):
        """Returns whether the number is not actually one.

        0 if a number
        1 if NaN
        2 if sNaN
        """
        if self._is_special:
            指数 = self._exp
            if 指数 == 'n':
                return 1
            elif 指数 == 'N':
                return 2
        return 0

    def _isinfinity(self):
        """Returns whether the number is infinite

        0 if finite or not a number
        1 if +INF
        -1 if -INF
        """
        if self._exp == 'F':
            if self._sign:
                return -1
            return 1
        return 0

    def _check_nans(self, other=None, context=None):
        """Returns whether the number is not actually one.

        if self, other are sNaN, signal
        if self, other are NaN return nan
        return 0

        Done before operations.
        """
        self_is_nan = self._isnan()
        if other is None:
            other_is_nan = False
        else:
            other_is_nan = other._isnan()
        if self_is_nan or other_is_nan:
            if context is None:
                context = 取上下文()
            if self_is_nan == 2:
                return context._raise_error(无效运算, 'sNaN', self)
            if other_is_nan == 2:
                return context._raise_error(无效运算, 'sNaN', other)
            if self_is_nan:
                return self._fix_nan(context)
            return other._fix_nan(context)
        return 0

    def _compare_check_nans(self, other, context):
        """Version of _check_nans used for the signaling comparisons
        compare_signal, __le__, __lt__, __ge__, __gt__.

        Signal InvalidOperation if either self or other is a (quiet
        or signaling) NaN.  Signaling NaNs take precedence over quiet
        NaNs.

        Return 0 if neither operand is a NaN.

        """
        if context is None:
            context = 取上下文()
        if self._is_special or other._is_special:
            if self.是信号NaN吗():
                return context._raise_error(无效运算, 'comparison involving sNaN', self)
            elif other.is_snan():
                return context._raise_error(无效运算, 'comparison involving sNaN', other)
            elif self.是安静NaN吗():
                return context._raise_error(无效运算, 'comparison involving NaN', self)
            elif other.is_qnan():
                return context._raise_error(无效运算, 'comparison involving NaN', other)
        return 0

    def __bool__(self):
        """Return True if self is nonzero; otherwise return False.

        NaNs and infinities are considered nonzero.
        """
        return self._is_special or self._int != '0'

    def _cmp(self, other):
        """Compare the two non-NaN decimal instances self and other.

        Returns -1 if self < other, 0 if self == other and 1
        if self > other.  This routine is for internal use only."""
        if self._is_special or other._is_special:
            self_inf = self._isinfinity()
            other_inf = other._isinfinity()
            if self_inf == other_inf:
                return 0
            elif self_inf < other_inf:
                return -1
            else:
                return 1
        if not self:
            if not other:
                return 0
            else:
                return -(-1) ** other._sign
        if not other:
            return (-1) ** self._sign
        if other._sign < self._sign:
            return -1
        if self._sign < other._sign:
            return 1
        self_adjusted = self.调整指数()
        other_adjusted = other.adjusted()
        if self_adjusted == other_adjusted:
            self_padded = self._int + '0' * (self._exp - other._exp)
            other_padded = other._int + '0' * (other._exp - self._exp)
            if self_padded == other_padded:
                return 0
            elif self_padded < other_padded:
                return -(-1) ** self._sign
            else:
                return (-1) ** self._sign
        elif self_adjusted > other_adjusted:
            return (-1) ** self._sign
        else:
            return -(-1) ** self._sign

    def __eq__(self, other, context=None):
        self, other = _convert_for_comparison(self, other, equality_op=True)
        if other is NotImplemented:
            return other
        if self._check_nans(other, context):
            return False
        return self._cmp(other) == 0

    def __lt__(self, other, context=None):
        self, other = _convert_for_comparison(self, other)
        if other is NotImplemented:
            return other
        ans = self._compare_check_nans(other, context)
        if ans:
            return False
        return self._cmp(other) < 0

    def __le__(self, other, context=None):
        self, other = _convert_for_comparison(self, other)
        if other is NotImplemented:
            return other
        ans = self._compare_check_nans(other, context)
        if ans:
            return False
        return self._cmp(other) <= 0

    def __gt__(self, other, context=None):
        self, other = _convert_for_comparison(self, other)
        if other is NotImplemented:
            return other
        ans = self._compare_check_nans(other, context)
        if ans:
            return False
        return self._cmp(other) > 0

    def __ge__(self, other, context=None):
        self, other = _convert_for_comparison(self, other)
        if other is NotImplemented:
            return other
        ans = self._compare_check_nans(other, context)
        if ans:
            return False
        return self._cmp(other) >= 0

    def 比较(self, other, context=None):
        """Compare self to other.  Return a decimal value:

        a or b is a NaN ==> Decimal('NaN')
        a < b           ==> Decimal('-1')
        a == b          ==> Decimal('0')
        a > b           ==> Decimal('1')
        """
        other = _convert_other(other, raiseit=True)
        if self._is_special or (other and other._is_special):
            ans = self._check_nans(other, context)
            if ans:
                return ans
        return 十进制数(self._cmp(other))

    def __hash__(self):
        """x.__hash__() <==> hash(x)"""
        if self._is_special:
            if self.是信号NaN吗():
                raise TypeError('Cannot hash a signaling NaN value.')
            elif self.是NaN吗():
                return object.__hash__(self)
            elif self._sign:
                return -_PyHASH_INF
            else:
                return _PyHASH_INF
        if self._exp >= 0:
            exp_hash = pow(10, self._exp, _PyHASH_MODULUS)
        else:
            exp_hash = pow(_PyHASH_10INV, -self._exp, _PyHASH_MODULUS)
        hash_ = int(self._int) * exp_hash % _PyHASH_MODULUS
        ans = hash_ if self >= 0 else -hash_
        return -2 if ans == -1 else ans

    def 转元组(self):
        """Represents the number as a triple tuple.

        To show the internals exactly as they are.
        """
        return 十进制元组(self._sign, tuple(map(int, self._int)), self._exp)

    def 转整数比(self):
        """Express a finite Decimal instance in the form n / d.

        Returns a pair (n, d) of integers.  When called on an infinity
        or NaN, raises OverflowError or ValueError respectively.

        >>> Decimal('3.14').as_integer_ratio()
        (157, 50)
        >>> Decimal('-123e5').as_integer_ratio()
        (-12300000, 1)
        >>> Decimal('0.00').as_integer_ratio()
        (0, 1)

        """
        if self._is_special:
            if self.是NaN吗():
                raise ValueError('cannot convert NaN to integer ratio')
            else:
                raise OverflowError('cannot convert Infinity to integer ratio')
        if not self:
            return (0, 1)
        n = int(self._int)
        if self._exp >= 0:
            n, d = (n * 10 ** self._exp, 1)
        else:
            d5 = -self._exp
            while d5 > 0 and n % 5 == 0:
                n //= 5
                d5 -= 1
            d2 = -self._exp
            shift2 = min((n & -n).bit_length() - 1, d2)
            if shift2:
                n >>= shift2
                d2 -= shift2
            d = 5 ** d5 << d2
        if self._sign:
            n = -n
        return (n, d)

    def __repr__(self):
        """Represents the number as an instance of Decimal."""
        return "Decimal('%s')" % str(self)

    def __str__(self, eng=False, context=None):
        """Return string representation of the number in scientific notation.

        Captures all of the information in the underlying representation.
        """
        sign = ['', '-'][self._sign]
        if self._is_special:
            if self._exp == 'F':
                return sign + 'Infinity'
            elif self._exp == 'n':
                return sign + 'NaN' + self._int
            else:
                return sign + 'sNaN' + self._int
        leftdigits = self._exp + len(self._int)
        if self._exp <= 0 and leftdigits > -6:
            dotplace = leftdigits
        elif not eng:
            dotplace = 1
        elif self._int == '0':
            dotplace = (leftdigits + 1) % 3 - 1
        else:
            dotplace = (leftdigits - 1) % 3 + 1
        if dotplace <= 0:
            intpart = '0'
            fracpart = '.' + '0' * -dotplace + self._int
        elif dotplace >= len(self._int):
            intpart = self._int + '0' * (dotplace - len(self._int))
            fracpart = ''
        else:
            intpart = self._int[:dotplace]
            fracpart = '.' + self._int[dotplace:]
        if leftdigits == dotplace:
            指数 = ''
        else:
            if context is None:
                context = 取上下文()
            指数 = ['e', 'E'][context.capitals] + '%+d' % (leftdigits - dotplace)
        return sign + intpart + fracpart + 指数

    def 转工程字符串(self, context=None):
        """Convert to a string, using engineering notation if an exponent is needed.

        Engineering notation has an exponent which is a multiple of 3.  This
        can leave up to 3 digits to the left of the decimal place and may
        require the addition of either one or two trailing zeros.
        """
        return self.__str__(eng=True, context=context)

    def __neg__(self, context=None):
        """Returns a copy with the sign switched.

        Rounds, if it has reason.
        """
        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans
        if context is None:
            context = 取上下文()
        if not self and context.rounding != 向下取整:
            ans = self.复制绝对值()
        else:
            ans = self.复制相反数()
        return ans._fix(context)

    def __pos__(self, context=None):
        """Returns a copy, unless it is a sNaN.

        Rounds the number (if more than precision digits)
        """
        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans
        if context is None:
            context = 取上下文()
        if not self and context.rounding != 向下取整:
            ans = self.复制绝对值()
        else:
            ans = 十进制数(self)
        return ans._fix(context)

    def __abs__(self, round=True, context=None):
        """Returns the absolute value of self.

        If the keyword argument 'round' is false, do not round.  The
        expression self.__abs__(round=False) is equivalent to
        self.copy_abs().
        """
        if not round:
            return self.复制绝对值()
        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans
        if self._sign:
            ans = self.__neg__(context=context)
        else:
            ans = self.__pos__(context=context)
        return ans

    def __add__(self, other, context=None):
        """Returns self + other.

        -INF + INF (or the reverse) cause InvalidOperation errors.
        """
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        if context is None:
            context = 取上下文()
        if self._is_special or other._is_special:
            ans = self._check_nans(other, context)
            if ans:
                return ans
            if self._isinfinity():
                if self._sign != other._sign and other._isinfinity():
                    return context._raise_error(无效运算, '-INF + INF')
                return 十进制数(self)
            if other._isinfinity():
                return 十进制数(other)
        指数 = min(self._exp, other._exp)
        negativezero = 0
        if context.rounding == 向下取整 and self._sign != other._sign:
            negativezero = 1
        if not self and (not other):
            sign = min(self._sign, other._sign)
            if negativezero:
                sign = 1
            ans = _dec_from_triple(sign, '0', 指数)
            ans = ans._fix(context)
            return ans
        if not self:
            指数 = max(指数, other._exp - context.prec - 1)
            ans = other._rescale(指数, context.rounding)
            ans = ans._fix(context)
            return ans
        if not other:
            指数 = max(指数, self._exp - context.prec - 1)
            ans = self._rescale(指数, context.rounding)
            ans = ans._fix(context)
            return ans
        op1 = _WorkRep(self)
        op2 = _WorkRep(other)
        op1, op2 = _normalize(op1, op2, context.prec)
        result = _WorkRep()
        if op1.sign != op2.sign:
            if op1.int == op2.int:
                ans = _dec_from_triple(negativezero, '0', 指数)
                ans = ans._fix(context)
                return ans
            if op1.int < op2.int:
                op1, op2 = (op2, op1)
            if op1.sign == 1:
                result.sign = 1
                op1.sign, op2.sign = (op2.sign, op1.sign)
            else:
                result.sign = 0
        elif op1.sign == 1:
            result.sign = 1
            op1.sign, op2.sign = (0, 0)
        else:
            result.sign = 0
        if op2.sign == 0:
            result.int = op1.int + op2.int
        else:
            result.int = op1.int - op2.int
        result.exp = op1.exp
        ans = 十进制数(result)
        ans = ans._fix(context)
        return ans
    __radd__ = __add__

    def __sub__(self, other, context=None):
        """Return self - other"""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        if self._is_special or other._is_special:
            ans = self._check_nans(other, context=context)
            if ans:
                return ans
        return self.__add__(other.copy_negate(), context=context)

    def __rsub__(self, other, context=None):
        """Return other - self"""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        return other.__sub__(self, context=context)

    def __mul__(self, other, context=None):
        """Return self * other.

        (+-) INF * 0 (or its reverse) raise InvalidOperation.
        """
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        if context is None:
            context = 取上下文()
        resultsign = self._sign ^ other._sign
        if self._is_special or other._is_special:
            ans = self._check_nans(other, context)
            if ans:
                return ans
            if self._isinfinity():
                if not other:
                    return context._raise_error(无效运算, '(+-)INF * 0')
                return _SignedInfinity[resultsign]
            if other._isinfinity():
                if not self:
                    return context._raise_error(无效运算, '0 * (+-)INF')
                return _SignedInfinity[resultsign]
        resultexp = self._exp + other._exp
        if not self or not other:
            ans = _dec_from_triple(resultsign, '0', resultexp)
            ans = ans._fix(context)
            return ans
        if self._int == '1':
            ans = _dec_from_triple(resultsign, other._int, resultexp)
            ans = ans._fix(context)
            return ans
        if other._int == '1':
            ans = _dec_from_triple(resultsign, self._int, resultexp)
            ans = ans._fix(context)
            return ans
        op1 = _WorkRep(self)
        op2 = _WorkRep(other)
        ans = _dec_from_triple(resultsign, str(op1.int * op2.int), resultexp)
        ans = ans._fix(context)
        return ans
    __rmul__ = __mul__

    def __truediv__(self, other, context=None):
        """Return self / other."""
        other = _convert_other(other)
        if other is NotImplemented:
            return NotImplemented
        if context is None:
            context = 取上下文()
        sign = self._sign ^ other._sign
        if self._is_special or other._is_special:
            ans = self._check_nans(other, context)
            if ans:
                return ans
            if self._isinfinity() and other._isinfinity():
                return context._raise_error(无效运算, '(+-)INF/(+-)INF')
            if self._isinfinity():
                return _SignedInfinity[sign]
            if other._isinfinity():
                context._raise_error(被钳位, 'Division by infinity')
                return _dec_from_triple(sign, '0', context.Etiny())
        if not other:
            if not self:
                return context._raise_error(除法未定义, '0 / 0')
            return context._raise_error(除零, 'x / 0', sign)
        if not self:
            指数 = self._exp - other._exp
            coeff = 0
        else:
            移位 = len(other._int) - len(self._int) + context.prec + 1
            指数 = self._exp - other._exp - 移位
            op1 = _WorkRep(self)
            op2 = _WorkRep(other)
            if 移位 >= 0:
                coeff, 余数 = divmod(op1.int * 10 ** 移位, op2.int)
            else:
                coeff, 余数 = divmod(op1.int, op2.int * 10 ** (-移位))
            if 余数:
                if coeff % 5 == 0:
                    coeff += 1
            else:
                ideal_exp = self._exp - other._exp
                while 指数 < ideal_exp and coeff % 10 == 0:
                    coeff //= 10
                    指数 += 1
        ans = _dec_from_triple(sign, str(coeff), 指数)
        return ans._fix(context)

    def _divide(self, other, context):
        """Return (self // other, self % other), to context.prec precision.

        Assumes that neither self nor other is a NaN, that self is not
        infinite and that other is nonzero.
        """
        sign = self._sign ^ other._sign
        if other._isinfinity():
            ideal_exp = self._exp
        else:
            ideal_exp = min(self._exp, other._exp)
        expdiff = self.调整指数() - other.adjusted()
        if not self or other._isinfinity() or expdiff <= -2:
            return (_dec_from_triple(sign, '0', 0), self._rescale(ideal_exp, context.rounding))
        if expdiff <= context.prec:
            op1 = _WorkRep(self)
            op2 = _WorkRep(other)
            if op1.exp >= op2.exp:
                op1.int *= 10 ** (op1.exp - op2.exp)
            else:
                op2.int *= 10 ** (op2.exp - op1.exp)
            q, r = divmod(op1.int, op2.int)
            if q < 10 ** context.prec:
                return (_dec_from_triple(sign, str(q), 0), _dec_from_triple(self._sign, str(r), ideal_exp))
        ans = context._raise_error(除不尽, 'quotient too large in //, % or divmod')
        return (ans, ans)

    def __rtruediv__(self, other, context=None):
        """Swaps self/other and returns __truediv__."""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        return other.__truediv__(self, context=context)

    def __divmod__(self, other, context=None):
        """
        Return (self // other, self % other)
        """
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        if context is None:
            context = 取上下文()
        ans = self._check_nans(other, context)
        if ans:
            return (ans, ans)
        sign = self._sign ^ other._sign
        if self._isinfinity():
            if other._isinfinity():
                ans = context._raise_error(无效运算, 'divmod(INF, INF)')
                return (ans, ans)
            else:
                return (_SignedInfinity[sign], context._raise_error(无效运算, 'INF % x'))
        if not other:
            if not self:
                ans = context._raise_error(除法未定义, 'divmod(0, 0)')
                return (ans, ans)
            else:
                return (context._raise_error(除零, 'x // 0', sign), context._raise_error(无效运算, 'x % 0'))
        quotient, 余数 = self._divide(other, context)
        余数 = 余数._fix(context)
        return (quotient, 余数)

    def __rdivmod__(self, other, context=None):
        """Swaps self/other and returns __divmod__."""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        return other.__divmod__(self, context=context)

    def __mod__(self, other, context=None):
        """
        self % other
        """
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        if context is None:
            context = 取上下文()
        ans = self._check_nans(other, context)
        if ans:
            return ans
        if self._isinfinity():
            return context._raise_error(无效运算, 'INF % x')
        elif not other:
            if self:
                return context._raise_error(无效运算, 'x % 0')
            else:
                return context._raise_error(除法未定义, '0 % 0')
        余数 = self._divide(other, context)[1]
        余数 = 余数._fix(context)
        return 余数

    def __rmod__(self, other, context=None):
        """Swaps self/other and returns __mod__."""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        return other.__mod__(self, context=context)

    def 就近余数(self, other, context=None):
        """
        Remainder nearest to 0-  abs(remainder-near) <= other/2
        """
        if context is None:
            context = 取上下文()
        other = _convert_other(other, raiseit=True)
        ans = self._check_nans(other, context)
        if ans:
            return ans
        if self._isinfinity():
            return context._raise_error(无效运算, 'remainder_near(infinity, x)')
        if not other:
            if self:
                return context._raise_error(无效运算, 'remainder_near(x, 0)')
            else:
                return context._raise_error(除法未定义, 'remainder_near(0, 0)')
        if other._isinfinity():
            ans = 十进制数(self)
            return ans._fix(context)
        ideal_exponent = min(self._exp, other._exp)
        if not self:
            ans = _dec_from_triple(self._sign, '0', ideal_exponent)
            return ans._fix(context)
        expdiff = self.调整指数() - other.adjusted()
        if expdiff >= context.prec + 1:
            return context._raise_error(除不尽)
        if expdiff <= -2:
            ans = self._rescale(ideal_exponent, context.rounding)
            return ans._fix(context)
        op1 = _WorkRep(self)
        op2 = _WorkRep(other)
        if op1.exp >= op2.exp:
            op1.int *= 10 ** (op1.exp - op2.exp)
        else:
            op2.int *= 10 ** (op2.exp - op1.exp)
        q, r = divmod(op1.int, op2.int)
        if 2 * r + (q & 1) > op2.int:
            r -= op2.int
            q += 1
        if q >= 10 ** context.prec:
            return context._raise_error(除不尽)
        sign = self._sign
        if r < 0:
            sign = 1 - sign
            r = -r
        ans = _dec_from_triple(sign, str(r), ideal_exponent)
        return ans._fix(context)

    def __floordiv__(self, other, context=None):
        """self // other"""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        if context is None:
            context = 取上下文()
        ans = self._check_nans(other, context)
        if ans:
            return ans
        if self._isinfinity():
            if other._isinfinity():
                return context._raise_error(无效运算, 'INF // INF')
            else:
                return _SignedInfinity[self._sign ^ other._sign]
        if not other:
            if self:
                return context._raise_error(除零, 'x // 0', self._sign ^ other._sign)
            else:
                return context._raise_error(除法未定义, '0 // 0')
        return self._divide(other, context)[0]

    def __rfloordiv__(self, other, context=None):
        """Swaps self/other and returns __floordiv__."""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        return other.__floordiv__(self, context=context)

    def __float__(self):
        """Float representation."""
        if self._isnan():
            if self.是信号NaN吗():
                raise ValueError('Cannot convert signaling NaN to float')
            s = '-nan' if self._sign else 'nan'
        else:
            s = str(self)
        return float(s)

    def __int__(self):
        """Converts self to an int, truncating if necessary."""
        if self._is_special:
            if self._isnan():
                raise ValueError('Cannot convert NaN to integer')
            elif self._isinfinity():
                raise OverflowError('Cannot convert infinity to integer')
        s = (-1) ** self._sign
        if self._exp >= 0:
            return s * int(self._int) * 10 ** self._exp
        else:
            return s * int(self._int[:self._exp] or '0')
    __trunc__ = __int__

    @property
    def 实部(self):
        return self

    @property
    def 虚部(self):
        return 十进制数(0)

    def 共轭(self):
        return self

    def __complex__(self):
        return complex(float(self))

    def _fix_nan(self, context):
        """Decapitate the payload of a NaN to fit the context"""
        payload = self._int
        max_payload_len = context.prec - context.clamp
        if len(payload) > max_payload_len:
            payload = payload[len(payload) - max_payload_len:].lstrip('0')
            return _dec_from_triple(self._sign, payload, self._exp, True)
        return 十进制数(self)

    def _fix(self, context):
        """Round if it is necessary to keep self within prec precision.

        Rounds and fixes the exponent.  Does not raise on a sNaN.

        Arguments:
        self - Decimal instance
        context - context used.
        """
        if self._is_special:
            if self._isnan():
                return self._fix_nan(context)
            else:
                return 十进制数(self)
        指数理论下限 = context.Etiny()
        指数上限 = context.Etop()
        if not self:
            exp_max = [context.Emax, 指数上限][context.clamp]
            new_exp = min(max(self._exp, 指数理论下限), exp_max)
            if new_exp != self._exp:
                context._raise_error(被钳位)
                return _dec_from_triple(self._sign, '0', new_exp)
            else:
                return 十进制数(self)
        exp_min = len(self._int) + self._exp - context.prec
        if exp_min > 指数上限:
            ans = context._raise_error(上溢, 'above Emax', self._sign)
            context._raise_error(不精确)
            context._raise_error(已舍入)
            return ans
        self_is_subnormal = exp_min < 指数理论下限
        if self_is_subnormal:
            exp_min = 指数理论下限
        if self._exp < exp_min:
            digits = len(self._int) + self._exp - exp_min
            if digits < 0:
                self = _dec_from_triple(self._sign, '1', exp_min - 1)
                digits = 0
            rounding_method = self._pick_rounding_function[context.rounding]
            changed = rounding_method(self, digits)
            coeff = self._int[:digits] or '0'
            if changed > 0:
                coeff = str(int(coeff) + 1)
                if len(coeff) > context.prec:
                    coeff = coeff[:-1]
                    exp_min += 1
            if exp_min > 指数上限:
                ans = context._raise_error(上溢, 'above Emax', self._sign)
            else:
                ans = _dec_from_triple(self._sign, coeff, exp_min)
            if changed and self_is_subnormal:
                context._raise_error(下溢)
            if self_is_subnormal:
                context._raise_error(次正规)
            if changed:
                context._raise_error(不精确)
            context._raise_error(已舍入)
            if not ans:
                context._raise_error(被钳位)
            return ans
        if self_is_subnormal:
            context._raise_error(次正规)
        if context.clamp == 1 and self._exp > 指数上限:
            context._raise_error(被钳位)
            self_padded = self._int + '0' * (self._exp - 指数上限)
            return _dec_from_triple(self._sign, self_padded, 指数上限)
        return 十进制数(self)

    def _round_down(self, prec):
        """Also known as round-towards-0, truncate."""
        if _all_zeros(self._int, prec):
            return 0
        else:
            return -1

    def _round_up(self, prec):
        """Rounds away from 0."""
        return -self._round_down(prec)

    def _round_half_up(self, prec):
        """Rounds 5 up (away from 0)"""
        if self._int[prec] in '56789':
            return 1
        elif _all_zeros(self._int, prec):
            return 0
        else:
            return -1

    def _round_half_down(self, prec):
        """Round 5 down"""
        if _exact_half(self._int, prec):
            return -1
        else:
            return self._round_half_up(prec)

    def _round_half_even(self, prec):
        """Round 5 to even, rest to nearest."""
        if _exact_half(self._int, prec) and (prec == 0 or self._int[prec - 1] in '02468'):
            return -1
        else:
            return self._round_half_up(prec)

    def _round_ceiling(self, prec):
        """Rounds up (not away from 0 if negative.)"""
        if self._sign:
            return self._round_down(prec)
        else:
            return -self._round_down(prec)

    def _round_floor(self, prec):
        """Rounds down (not towards 0 if negative)"""
        if not self._sign:
            return self._round_down(prec)
        else:
            return -self._round_down(prec)

    def _round_05up(self, prec):
        """Round down unless digit prec-1 is 0 or 5."""
        if prec and self._int[prec - 1] not in '05':
            return self._round_down(prec)
        else:
            return -self._round_down(prec)
    _pick_rounding_function = dict(ROUND_DOWN=_round_down, ROUND_UP=_round_up, ROUND_HALF_UP=_round_half_up, ROUND_HALF_DOWN=_round_half_down, ROUND_HALF_EVEN=_round_half_even, ROUND_CEILING=_round_ceiling, ROUND_FLOOR=_round_floor, ROUND_05UP=_round_05up)

    def __round__(self, n=None):
        """Round self to the nearest integer, or to a given precision.

        If only one argument is supplied, round a finite Decimal
        instance self to the nearest integer.  If self is infinite or
        a NaN then a Python exception is raised.  If self is finite
        and lies exactly halfway between two integers then it is
        rounded to the integer with even last digit.

        >>> round(Decimal('123.456'))
        123
        >>> round(Decimal('-456.789'))
        -457
        >>> round(Decimal('-3.0'))
        -3
        >>> round(Decimal('2.5'))
        2
        >>> round(Decimal('3.5'))
        4
        >>> round(Decimal('Inf'))
        Traceback (most recent call last):
          ...
        OverflowError: cannot round an infinity
        >>> round(Decimal('NaN'))
        Traceback (most recent call last):
          ...
        ValueError: cannot round a NaN

        If a second argument n is supplied, self is rounded to n
        decimal places using the rounding mode for the current
        context.

        For an integer n, round(self, -n) is exactly equivalent to
        self.quantize(Decimal('1En')).

        >>> round(Decimal('123.456'), 0)
        Decimal('123')
        >>> round(Decimal('123.456'), 2)
        Decimal('123.46')
        >>> round(Decimal('123.456'), -2)
        Decimal('1E+2')
        >>> round(Decimal('-Infinity'), 37)
        Decimal('NaN')
        >>> round(Decimal('sNaN123'), 0)
        Decimal('NaN123')

        """
        if n is not None:
            if not isinstance(n, int):
                raise TypeError('Second argument to round should be integral')
            指数 = _dec_from_triple(0, '1', -n)
            return self.量化(指数)
        if self._is_special:
            if self.是NaN吗():
                raise ValueError('cannot round a NaN')
            else:
                raise OverflowError('cannot round an infinity')
        return int(self._rescale(0, 银行家舍入))

    def __floor__(self):
        """Return the floor of self, as an integer.

        For a finite Decimal instance self, return the greatest
        integer n such that n <= self.  If self is infinite or a NaN
        then a Python exception is raised.

        """
        if self._is_special:
            if self.是NaN吗():
                raise ValueError('cannot round a NaN')
            else:
                raise OverflowError('cannot round an infinity')
        return int(self._rescale(0, 向下取整))

    def __ceil__(self):
        """Return the ceiling of self, as an integer.

        For a finite Decimal instance self, return the least integer n
        such that n >= self.  If self is infinite or a NaN then a
        Python exception is raised.

        """
        if self._is_special:
            if self.是NaN吗():
                raise ValueError('cannot round a NaN')
            else:
                raise OverflowError('cannot round an infinity')
        return int(self._rescale(0, 向上取整))

    def 乘加(self, other, third, context=None):
        """Fused multiply-add.

        Returns self*other+third with no rounding of the intermediate
        product self*other.

        self and other are multiplied together, with no rounding of
        the result.  The third operand is then added to the result,
        and a single final rounding is performed.
        """
        other = _convert_other(other, raiseit=True)
        third = _convert_other(third, raiseit=True)
        if self._is_special or other._is_special:
            if context is None:
                context = 取上下文()
            if self._exp == 'N':
                return context._raise_error(无效运算, 'sNaN', self)
            if other._exp == 'N':
                return context._raise_error(无效运算, 'sNaN', other)
            if self._exp == 'n':
                product = self
            elif other._exp == 'n':
                product = other
            elif self._exp == 'F':
                if not other:
                    return context._raise_error(无效运算, 'INF * 0 in fma')
                product = _SignedInfinity[self._sign ^ other._sign]
            elif other._exp == 'F':
                if not self:
                    return context._raise_error(无效运算, '0 * INF in fma')
                product = _SignedInfinity[self._sign ^ other._sign]
        else:
            product = _dec_from_triple(self._sign ^ other._sign, str(int(self._int) * int(other._int)), self._exp + other._exp)
        return product.__add__(third, context)

    def _power_modulo(self, other, modulo, context=None):
        """Three argument version of __pow__"""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        modulo = _convert_other(modulo)
        if modulo is NotImplemented:
            return modulo
        if context is None:
            context = 取上下文()
        self_is_nan = self._isnan()
        other_is_nan = other._isnan()
        modulo_is_nan = modulo._isnan()
        if self_is_nan or other_is_nan or modulo_is_nan:
            if self_is_nan == 2:
                return context._raise_error(无效运算, 'sNaN', self)
            if other_is_nan == 2:
                return context._raise_error(无效运算, 'sNaN', other)
            if modulo_is_nan == 2:
                return context._raise_error(无效运算, 'sNaN', modulo)
            if self_is_nan:
                return self._fix_nan(context)
            if other_is_nan:
                return other._fix_nan(context)
            return modulo._fix_nan(context)
        if not (self._isinteger() and other._isinteger() and modulo._isinteger()):
            return context._raise_error(无效运算, 'pow() 3rd argument not allowed unless all arguments are integers')
        if other < 0:
            return context._raise_error(无效运算, 'pow() 2nd argument cannot be negative when 3rd argument specified')
        if not modulo:
            return context._raise_error(无效运算, 'pow() 3rd argument cannot be 0')
        if modulo.adjusted() >= context.prec:
            return context._raise_error(无效运算, 'insufficient precision: pow() 3rd argument must not have more than precision digits')
        if not other and (not self):
            return context._raise_error(无效运算, 'at least one of pow() 1st argument and 2nd argument must be nonzero; 0**0 is not defined')
        if other._iseven():
            sign = 0
        else:
            sign = self._sign
        modulo = abs(int(modulo))
        base = _WorkRep(self.取整数值())
        exponent = _WorkRep(other.to_integral_value())
        base = base.int % modulo * pow(10, base.exp, modulo) % modulo
        for i in range(exponent.exp):
            base = pow(base, 10, modulo)
        base = pow(base, exponent.int, modulo)
        return _dec_from_triple(sign, str(base), 0)

    def _power_exact(self, other, p):
        """Attempt to compute self**other exactly.

        Given Decimals self and other and an integer p, attempt to
        compute an exact result for the power self**other, with p
        digits of precision.  Return None if self**other is not
        exactly representable in p digits.

        Assumes that elimination of special cases has already been
        performed: self and other must both be nonspecial; self must
        be positive and not numerically equal to 1; other must be
        nonzero.  For efficiency, other._exp should not be too large,
        so that 10**abs(other._exp) is a feasible calculation."""
        x = _WorkRep(self)
        xc, xe = (x.int, x.exp)
        while xc % 10 == 0:
            xc //= 10
            xe += 1
        y = _WorkRep(other)
        yc, ye = (y.int, y.exp)
        while yc % 10 == 0:
            yc //= 10
            ye += 1
        if xc == 1:
            xe *= yc
            while xe % 10 == 0:
                xe //= 10
                ye += 1
            if ye < 0:
                return None
            exponent = xe * 10 ** ye
            if y.sign == 1:
                exponent = -exponent
            if other._isinteger() and other._sign == 0:
                ideal_exponent = self._exp * int(other)
                zeros = min(exponent - ideal_exponent, p - 1)
            else:
                zeros = 0
            return _dec_from_triple(0, '1' + '0' * zeros, exponent - zeros)
        if y.sign == 1:
            last_digit = xc % 10
            if last_digit in (2, 4, 6, 8):
                if xc & -xc != xc:
                    return None
                e = _nbits(xc) - 1
                emax = p * 93 // 65
                if ye >= len(str(emax)):
                    return None
                e = _decimal_lshift_exact(e * yc, ye)
                xe = _decimal_lshift_exact(xe * yc, ye)
                if e is None or xe is None:
                    return None
                if e > emax:
                    return None
                xc = 5 ** e
            elif last_digit == 5:
                e = _nbits(xc) * 28 // 65
                xc, 余数 = divmod(5 ** e, xc)
                if 余数:
                    return None
                while xc % 5 == 0:
                    xc //= 5
                    e -= 1
                emax = p * 10 // 3
                if ye >= len(str(emax)):
                    return None
                e = _decimal_lshift_exact(e * yc, ye)
                xe = _decimal_lshift_exact(xe * yc, ye)
                if e is None or xe is None:
                    return None
                if e > emax:
                    return None
                xc = 2 ** e
            else:
                return None
            assert xc > 1, self
            assert xc % 10 != 0, self
            strxc = str(xc)
            if len(strxc) > p:
                return None
            xe = -e - xe
            return _dec_from_triple(0, strxc, xe)
        if ye >= 0:
            m, n = (yc * 10 ** ye, 1)
        else:
            if xe != 0 and len(str(abs(yc * xe))) <= -ye:
                return None
            xc_bits = _nbits(xc)
            if len(str(abs(yc) * xc_bits)) <= -ye:
                return None
            m, n = (yc, 10 ** (-ye))
            while m % 2 == n % 2 == 0:
                m //= 2
                n //= 2
            while m % 5 == n % 5 == 0:
                m //= 5
                n //= 5
        if n > 1:
            if xc_bits <= n:
                return None
            xe, rem = divmod(xe, n)
            if rem != 0:
                return None
            a = 1 << -(-_nbits(xc) // n)
            while True:
                q, r = divmod(xc, a ** (n - 1))
                if a <= q:
                    break
                else:
                    a = (a * (n - 1) + q) // n
            if not (a == q and r == 0):
                return None
            xc = a
        if xc > 1 and m > p * 100 // _log10_lb(xc):
            return None
        xc = xc ** m
        xe *= m
        assert xc > 1, self
        assert xc % 10 != 0, self
        str_xc = str(xc)
        if len(str_xc) > p:
            return None
        if other._isinteger() and other._sign == 0:
            ideal_exponent = self._exp * int(other)
            zeros = min(xe - ideal_exponent, p - len(str_xc))
        else:
            zeros = 0
        return _dec_from_triple(0, str_xc + '0' * zeros, xe - zeros)

    def __pow__(self, other, modulo=None, context=None):
        """Return self ** other [ % modulo].

        With two arguments, compute self**other.

        With three arguments, compute (self**other) % modulo.  For the
        three argument form, the following restrictions on the
        arguments hold:

         - all three arguments must be integral
         - other must be nonnegative
         - either self or other (or both) must be nonzero
         - modulo must be nonzero and must have at most p digits,
           where p is the context precision.

        If any of these restrictions is violated the InvalidOperation
        flag is raised.

        The result of pow(self, other, modulo) is identical to the
        result that would be obtained by computing (self**other) %
        modulo with unbounded precision, but is computed more
        efficiently.  It is always exact.
        """
        if modulo is not None:
            return self._power_modulo(other, modulo, context)
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        if context is None:
            context = 取上下文()
        ans = self._check_nans(other, context)
        if ans:
            return ans
        if not other:
            if not self:
                return context._raise_error(无效运算, '0 ** 0')
            else:
                return _One
        result_sign = 0
        if self._sign == 1:
            if other._isinteger():
                if not other._iseven():
                    result_sign = 1
            elif self:
                return context._raise_error(无效运算, 'x ** y with x negative and y not an integer')
            self = self.复制相反数()
        if not self:
            if other._sign == 0:
                return _dec_from_triple(result_sign, '0', 0)
            else:
                return _SignedInfinity[result_sign]
        if self._isinfinity():
            if other._sign == 0:
                return _SignedInfinity[result_sign]
            else:
                return _dec_from_triple(result_sign, '0', 0)
        if self == _One:
            if other._isinteger():
                if other._sign == 1:
                    multiplier = 0
                elif other > context.prec:
                    multiplier = context.prec
                else:
                    multiplier = int(other)
                指数 = self._exp * multiplier
                if 指数 < 1 - context.prec:
                    指数 = 1 - context.prec
                    context._raise_error(已舍入)
            else:
                context._raise_error(不精确)
                context._raise_error(已舍入)
                指数 = 1 - context.prec
            return _dec_from_triple(result_sign, '1' + '0' * -指数, 指数)
        self_adj = self.调整指数()
        if other._isinfinity():
            if (other._sign == 0) == (self_adj < 0):
                return _dec_from_triple(result_sign, '0', 0)
            else:
                return _SignedInfinity[result_sign]
        ans = None
        exact = False
        bound = self._log10_exp_bound() + other.adjusted()
        if (self_adj >= 0) == (other._sign == 0):
            if bound >= len(str(context.Emax)):
                ans = _dec_from_triple(result_sign, '1', context.Emax + 1)
        else:
            指数理论下限 = context.Etiny()
            if bound >= len(str(-指数理论下限)):
                ans = _dec_from_triple(result_sign, '1', 指数理论下限 - 1)
        if ans is None:
            ans = self._power_exact(other, context.prec + 1)
            if ans is not None:
                if result_sign == 1:
                    ans = _dec_from_triple(1, ans._int, ans._exp)
                exact = True
        if ans is None:
            p = context.prec
            x = _WorkRep(self)
            xc, xe = (x.int, x.exp)
            y = _WorkRep(other)
            yc, ye = (y.int, y.exp)
            if y.sign == 1:
                yc = -yc
            extra = 3
            while True:
                coeff, 指数 = _dpower(xc, xe, yc, ye, p + extra)
                if coeff % (5 * 10 ** (len(str(coeff)) - p - 1)):
                    break
                extra += 3
            ans = _dec_from_triple(result_sign, str(coeff), 指数)
        if exact and (not other._isinteger()):
            if len(ans._int) <= context.prec:
                expdiff = context.prec + 1 - len(ans._int)
                ans = _dec_from_triple(ans._sign, ans._int + '0' * expdiff, ans._exp - expdiff)
            newcontext = context.copy()
            newcontext.clear_flags()
            for exception in _signals:
                newcontext.traps[exception] = 0
            ans = ans._fix(newcontext)
            newcontext._raise_error(不精确)
            if newcontext.flags[次正规]:
                newcontext._raise_error(下溢)
            if newcontext.flags[上溢]:
                context._raise_error(上溢, 'above Emax', ans._sign)
            for exception in (下溢, 次正规, 不精确, 已舍入, 被钳位):
                if newcontext.flags[exception]:
                    context._raise_error(exception)
        else:
            ans = ans._fix(context)
        return ans

    def __rpow__(self, other, modulo=None, context=None):
        """Swaps self/other and returns __pow__."""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        return other.__pow__(self, modulo, context=context)

    def 规范化(self, context=None):
        """Normalize- strip trailing 0s, change anything equal to 0 to 0e0"""
        if context is None:
            context = 取上下文()
        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans
        dup = self._fix(context)
        if dup._isinfinity():
            return dup
        if not dup:
            return _dec_from_triple(dup._sign, '0', 0)
        exp_max = [context.Emax, context.Etop()][context.clamp]
        end = len(dup._int)
        指数 = dup._exp
        while dup._int[end - 1] == '0' and 指数 < exp_max:
            指数 += 1
            end -= 1
        return _dec_from_triple(dup._sign, dup._int[:end], 指数)

    def 量化(self, exp, rounding=None, context=None):
        """Quantize self so its exponent is the same as that of exp.

        Similar to self._rescale(exp._exp) but with error checking.
        """
        exp = _convert_other(exp, raiseit=True)
        if context is None:
            context = 取上下文()
        if rounding is None:
            rounding = context.rounding
        if self._is_special or exp._is_special:
            ans = self._check_nans(exp, context)
            if ans:
                return ans
            if exp._isinfinity() or self._isinfinity():
                if exp._isinfinity() and self._isinfinity():
                    return 十进制数(self)
                return context._raise_error(无效运算, 'quantize with one INF')
        if not context.Etiny() <= exp._exp <= context.Emax:
            return context._raise_error(无效运算, 'target exponent out of bounds in quantize')
        if not self:
            ans = _dec_from_triple(self._sign, '0', exp._exp)
            return ans._fix(context)
        self_adjusted = self.调整指数()
        if self_adjusted > context.Emax:
            return context._raise_error(无效运算, 'exponent of quantize result too large for current context')
        if self_adjusted - exp._exp + 1 > context.prec:
            return context._raise_error(无效运算, 'quantize result has too many digits for current context')
        ans = self._rescale(exp._exp, rounding)
        if ans.adjusted() > context.Emax:
            return context._raise_error(无效运算, 'exponent of quantize result too large for current context')
        if len(ans._int) > context.prec:
            return context._raise_error(无效运算, 'quantize result has too many digits for current context')
        if ans and ans.adjusted() < context.Emin:
            context._raise_error(次正规)
        if ans._exp > self._exp:
            if ans != self:
                context._raise_error(不精确)
            context._raise_error(已舍入)
        ans = ans._fix(context)
        return ans

    def 同量级吗(self, other, context=None):
        """Return True if self and other have the same exponent; otherwise
        return False.

        If either operand is a special value, the following rules are used:
           * return True if both operands are infinities
           * return True if both operands are NaNs
           * otherwise, return False.
        """
        other = _convert_other(other, raiseit=True)
        if self._is_special or other._is_special:
            return self.是NaN吗() and other.is_nan() or (self.是无穷吗() and other.is_infinite())
        return self._exp == other._exp

    def _rescale(self, exp, rounding):
        """Rescale self so that the exponent is exp, either by padding with zeros
        or by truncating digits, using the given rounding mode.

        Specials are returned without change.  This operation is
        quiet: it raises no flags, and uses no information from the
        context.

        exp = exp to scale to (an integer)
        rounding = rounding mode
        """
        if self._is_special:
            return 十进制数(self)
        if not self:
            return _dec_from_triple(self._sign, '0', exp)
        if self._exp >= exp:
            return _dec_from_triple(self._sign, self._int + '0' * (self._exp - exp), exp)
        digits = len(self._int) + self._exp - exp
        if digits < 0:
            self = _dec_from_triple(self._sign, '1', exp - 1)
            digits = 0
        this_function = self._pick_rounding_function[rounding]
        changed = this_function(self, digits)
        coeff = self._int[:digits] or '0'
        if changed == 1:
            coeff = str(int(coeff) + 1)
        return _dec_from_triple(self._sign, coeff, exp)

    def _round(self, places, rounding):
        """Round a nonzero, nonspecial Decimal to a fixed number of
        significant figures, using the given rounding mode.

        Infinities, NaNs and zeros are returned unaltered.

        This operation is quiet: it raises no flags, and uses no
        information from the context.

        """
        if places <= 0:
            raise ValueError('argument should be at least 1 in _round')
        if self._is_special or not self:
            return 十进制数(self)
        ans = self._rescale(self.调整指数() + 1 - places, rounding)
        if ans.adjusted() != self.调整指数():
            ans = ans._rescale(ans.adjusted() + 1 - places, rounding)
        return ans

    def 精确取整(self, rounding=None, context=None):
        """Rounds to a nearby integer.

        If no rounding mode is specified, take the rounding mode from
        the context.  This method raises the Rounded and Inexact flags
        when appropriate.

        See also: to_integral_value, which does exactly the same as
        this method except that it doesn't raise Inexact or Rounded.
        """
        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans
            return 十进制数(self)
        if self._exp >= 0:
            return 十进制数(self)
        if not self:
            return _dec_from_triple(self._sign, '0', 0)
        if context is None:
            context = 取上下文()
        if rounding is None:
            rounding = context.rounding
        ans = self._rescale(0, rounding)
        if ans != self:
            context._raise_error(不精确)
        context._raise_error(已舍入)
        return ans

    def 取整数值(self, rounding=None, context=None):
        """Rounds to the nearest integer, without raising inexact, rounded."""
        if context is None:
            context = 取上下文()
        if rounding is None:
            rounding = context.rounding
        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans
            return 十进制数(self)
        if self._exp >= 0:
            return 十进制数(self)
        else:
            return self._rescale(0, rounding)
    to_integral = 取整数值

    def 平方根(self, context=None):
        """Return the square root of self."""
        if context is None:
            context = 取上下文()
        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans
            if self._isinfinity() and self._sign == 0:
                return 十进制数(self)
        if not self:
            ans = _dec_from_triple(self._sign, '0', self._exp // 2)
            return ans._fix(context)
        if self._sign == 1:
            return context._raise_error(无效运算, 'sqrt(-x), x > 0')
        prec = context.prec + 1
        op = _WorkRep(self)
        e = op.exp >> 1
        if op.exp & 1:
            c = op.int * 10
            l = (len(self._int) >> 1) + 1
        else:
            c = op.int
            l = len(self._int) + 1 >> 1
        移位 = prec - l
        if 移位 >= 0:
            c *= 100 ** 移位
            exact = True
        else:
            c, 余数 = divmod(c, 100 ** (-移位))
            exact = not 余数
        e -= 移位
        n = 10 ** prec
        while True:
            q = c // n
            if n <= q:
                break
            else:
                n = n + q >> 1
        exact = exact and n * n == c
        if exact:
            if 移位 >= 0:
                n //= 10 ** 移位
            else:
                n *= 10 ** (-移位)
            e += 移位
        elif n % 5 == 0:
            n += 1
        ans = _dec_from_triple(0, str(n), e)
        context = context._shallow_copy()
        rounding = context._set_rounding(银行家舍入)
        ans = ans._fix(context)
        context.rounding = rounding
        return ans

    def max(self, other, context=None):
        """Returns the larger value.

        Like max(self, other) except if one is not a number, returns
        NaN (and signals if one is sNaN).  Also rounds.
        """
        other = _convert_other(other, raiseit=True)
        if context is None:
            context = 取上下文()
        if self._is_special or other._is_special:
            sn = self._isnan()
            on = other._isnan()
            if sn or on:
                if on == 1 and sn == 0:
                    return self._fix(context)
                if sn == 1 and on == 0:
                    return other._fix(context)
                return self._check_nans(other, context)
        c = self._cmp(other)
        if c == 0:
            c = self.全序比较(other)
        if c == -1:
            ans = other
        else:
            ans = self
        return ans._fix(context)

    def min(self, other, context=None):
        """Returns the smaller value.

        Like min(self, other) except if one is not a number, returns
        NaN (and signals if one is sNaN).  Also rounds.
        """
        other = _convert_other(other, raiseit=True)
        if context is None:
            context = 取上下文()
        if self._is_special or other._is_special:
            sn = self._isnan()
            on = other._isnan()
            if sn or on:
                if on == 1 and sn == 0:
                    return self._fix(context)
                if sn == 1 and on == 0:
                    return other._fix(context)
                return self._check_nans(other, context)
        c = self._cmp(other)
        if c == 0:
            c = self.全序比较(other)
        if c == -1:
            ans = self
        else:
            ans = other
        return ans._fix(context)

    def _isinteger(self):
        """Returns whether self is an integer"""
        if self._is_special:
            return False
        if self._exp >= 0:
            return True
        rest = self._int[self._exp:]
        return rest == '0' * len(rest)

    def _iseven(self):
        """Returns True if self is even.  Assumes self is an integer."""
        if not self or self._exp > 0:
            return True
        return self._int[-1 + self._exp] in '02468'

    def 调整指数(self):
        """Return the adjusted exponent of self"""
        try:
            return self._exp + len(self._int) - 1
        except TypeError:
            return 0

    def 取规范形(self):
        """Returns the same Decimal object.

        As we do not have different encodings for the same number, the
        received object already is in its canonical form.
        """
        return self

    def 带信号比较(self, other, context=None):
        """Compares self to the other operand numerically.

        It's pretty much like compare(), but all NaNs signal, with signaling
        NaNs taking precedence over quiet NaNs.
        """
        other = _convert_other(other, raiseit=True)
        ans = self._compare_check_nans(other, context)
        if ans:
            return ans
        return self.比较(other, context=context)

    def 全序比较(self, other, context=None):
        """Compares self to other using the abstract representations.

        This is not like the standard compare, which use their numerical
        value. Note that a total ordering is defined for all possible
        abstract representations.
        """
        other = _convert_other(other, raiseit=True)
        if self._sign and (not other._sign):
            return _NegativeOne
        if not self._sign and other._sign:
            return _One
        sign = self._sign
        self_nan = self._isnan()
        other_nan = other._isnan()
        if self_nan or other_nan:
            if self_nan == other_nan:
                self_key = (len(self._int), self._int)
                other_key = (len(other._int), other._int)
                if self_key < other_key:
                    if sign:
                        return _One
                    else:
                        return _NegativeOne
                if self_key > other_key:
                    if sign:
                        return _NegativeOne
                    else:
                        return _One
                return _Zero
            if sign:
                if self_nan == 1:
                    return _NegativeOne
                if other_nan == 1:
                    return _One
                if self_nan == 2:
                    return _NegativeOne
                if other_nan == 2:
                    return _One
            else:
                if self_nan == 1:
                    return _One
                if other_nan == 1:
                    return _NegativeOne
                if self_nan == 2:
                    return _One
                if other_nan == 2:
                    return _NegativeOne
        if self < other:
            return _NegativeOne
        if self > other:
            return _One
        if self._exp < other._exp:
            if sign:
                return _One
            else:
                return _NegativeOne
        if self._exp > other._exp:
            if sign:
                return _NegativeOne
            else:
                return _One
        return _Zero

    def 全序绝对值比较(self, other, context=None):
        """Compares self to other using abstract repr., ignoring sign.

        Like compare_total, but with operand's sign ignored and assumed to
        be 0.
        """
        other = _convert_other(other, raiseit=True)
        s = self.复制绝对值()
        o = other.copy_abs()
        return s.compare_total(o)

    def 复制绝对值(self):
        """Returns a copy with the sign set to 0. """
        return _dec_from_triple(0, self._int, self._exp, self._is_special)

    def 复制相反数(self):
        """Returns a copy with the sign inverted."""
        if self._sign:
            return _dec_from_triple(0, self._int, self._exp, self._is_special)
        else:
            return _dec_from_triple(1, self._int, self._exp, self._is_special)

    def 复制符号(self, other, context=None):
        """Returns self with the sign of other."""
        other = _convert_other(other, raiseit=True)
        return _dec_from_triple(other._sign, self._int, self._exp, self._is_special)

    def 指数(self, context=None):
        """Returns e ** self."""
        if context is None:
            context = 取上下文()
        ans = self._check_nans(context=context)
        if ans:
            return ans
        if self._isinfinity() == -1:
            return _Zero
        if not self:
            return _One
        if self._isinfinity() == 1:
            return 十进制数(self)
        p = context.prec
        adj = self.调整指数()
        if self._sign == 0 and adj > len(str((context.Emax + 1) * 3)):
            ans = _dec_from_triple(0, '1', context.Emax + 1)
        elif self._sign == 1 and adj > len(str((-context.Etiny() + 1) * 3)):
            ans = _dec_from_triple(0, '1', context.Etiny() - 1)
        elif self._sign == 0 and adj < -p:
            ans = _dec_from_triple(0, '1' + '0' * (p - 1) + '1', -p)
        elif self._sign == 1 and adj < -p - 1:
            ans = _dec_from_triple(0, '9' * (p + 1), -p - 1)
        else:
            op = _WorkRep(self)
            c, e = (op.int, op.exp)
            if op.sign == 1:
                c = -c
            extra = 3
            while True:
                coeff, 指数 = _dexp(c, e, p + extra)
                if coeff % (5 * 10 ** (len(str(coeff)) - p - 1)):
                    break
                extra += 3
            ans = _dec_from_triple(0, str(coeff), 指数)
        context = context._shallow_copy()
        rounding = context._set_rounding(银行家舍入)
        ans = ans._fix(context)
        context.rounding = rounding
        return ans

    def 是规范形吗(self):
        """Return True if self is canonical; otherwise return False.

        Currently, the encoding of a Decimal instance is always
        canonical, so this method returns True for any Decimal.
        """
        return True

    def 是有限吗(self):
        """Return True if self is finite; otherwise return False.

        A Decimal instance is considered finite if it is neither
        infinite nor a NaN.
        """
        return not self._is_special

    def 是无穷吗(self):
        """Return True if self is infinite; otherwise return False."""
        return self._exp == 'F'

    def 是NaN吗(self):
        """Return True if self is a qNaN or sNaN; otherwise return False."""
        return self._exp in ('n', 'N')

    def 是正规数吗(self, context=None):
        """Return True if self is a normal number; otherwise return False."""
        if self._is_special or not self:
            return False
        if context is None:
            context = 取上下文()
        return context.Emin <= self.调整指数()

    def 是安静NaN吗(self):
        """Return True if self is a quiet NaN; otherwise return False."""
        return self._exp == 'n'

    def 带符号吗(self):
        """Return True if self is negative; otherwise return False."""
        return self._sign == 1

    def 是信号NaN吗(self):
        """Return True if self is a signaling NaN; otherwise return False."""
        return self._exp == 'N'

    def 是次正规吗(self, context=None):
        """Return True if self is subnormal; otherwise return False."""
        if self._is_special or not self:
            return False
        if context is None:
            context = 取上下文()
        return self.调整指数() < context.Emin

    def 是零吗(self):
        """Return True if self is a zero; otherwise return False."""
        return not self._is_special and self._int == '0'

    def _ln_exp_bound(self):
        """Compute a lower bound for the adjusted exponent of self.ln().
        In other words, compute r such that self.ln() >= 10**r.  Assumes
        that self is finite and positive and that self != 1.
        """
        adj = self._exp + len(self._int) - 1
        if adj >= 1:
            return len(str(adj * 23 // 10)) - 1
        if adj <= -2:
            return len(str((-1 - adj) * 23 // 10)) - 1
        op = _WorkRep(self)
        c, e = (op.int, op.exp)
        if adj == 0:
            num = str(c - 10 ** (-e))
            den = str(c)
            return len(num) - len(den) - (num < den)
        return e + len(str(10 ** (-e) - c)) - 1

    def 自然对数(self, context=None):
        """Returns the natural (base e) logarithm of self."""
        if context is None:
            context = 取上下文()
        ans = self._check_nans(context=context)
        if ans:
            return ans
        if not self:
            return _NegativeInfinity
        if self._isinfinity() == 1:
            return _Infinity
        if self == _One:
            return _Zero
        if self._sign == 1:
            return context._raise_error(无效运算, 'ln of a negative value')
        op = _WorkRep(self)
        c, e = (op.int, op.exp)
        p = context.prec
        places = p - self._ln_exp_bound() + 2
        while True:
            coeff = _dlog(c, e, places)
            if coeff % (5 * 10 ** (len(str(abs(coeff))) - p - 1)):
                break
            places += 3
        ans = _dec_from_triple(int(coeff < 0), str(abs(coeff)), -places)
        context = context._shallow_copy()
        rounding = context._set_rounding(银行家舍入)
        ans = ans._fix(context)
        context.rounding = rounding
        return ans

    def _log10_exp_bound(self):
        """Compute a lower bound for the adjusted exponent of self.log10().
        In other words, find r such that self.log10() >= 10**r.
        Assumes that self is finite and positive and that self != 1.
        """
        adj = self._exp + len(self._int) - 1
        if adj >= 1:
            return len(str(adj)) - 1
        if adj <= -2:
            return len(str(-1 - adj)) - 1
        op = _WorkRep(self)
        c, e = (op.int, op.exp)
        if adj == 0:
            num = str(c - 10 ** (-e))
            den = str(231 * c)
            return len(num) - len(den) - (num < den) + 2
        num = str(10 ** (-e) - c)
        return len(num) + e - (num < '231') - 1

    def 常用对数(self, context=None):
        """Returns the base 10 logarithm of self."""
        if context is None:
            context = 取上下文()
        ans = self._check_nans(context=context)
        if ans:
            return ans
        if not self:
            return _NegativeInfinity
        if self._isinfinity() == 1:
            return _Infinity
        if self._sign == 1:
            return context._raise_error(无效运算, 'log10 of a negative value')
        if self._int[0] == '1' and self._int[1:] == '0' * (len(self._int) - 1):
            ans = 十进制数(self._exp + len(self._int) - 1)
        else:
            op = _WorkRep(self)
            c, e = (op.int, op.exp)
            p = context.prec
            places = p - self._log10_exp_bound() + 2
            while True:
                coeff = _dlog10(c, e, places)
                if coeff % (5 * 10 ** (len(str(abs(coeff))) - p - 1)):
                    break
                places += 3
            ans = _dec_from_triple(int(coeff < 0), str(abs(coeff)), -places)
        context = context._shallow_copy()
        rounding = context._set_rounding(银行家舍入)
        ans = ans._fix(context)
        context.rounding = rounding
        return ans

    def 指数对数(self, context=None):
        """ Returns the exponent of the magnitude of self's MSD.

        The result is the integer which is the exponent of the magnitude
        of the most significant digit of self (as though it were truncated
        to a single digit while maintaining the value of that digit and
        without limiting the resulting exponent).
        """
        ans = self._check_nans(context=context)
        if ans:
            return ans
        if context is None:
            context = 取上下文()
        if self._isinfinity():
            return _Infinity
        if not self:
            return context._raise_error(除零, 'logb(0)', 1)
        ans = 十进制数(self.调整指数())
        return ans._fix(context)

    def _islogical(self):
        """Return True if self is a logical operand.

        For being logical, it must be a finite number with a sign of 0,
        an exponent of 0, and a coefficient whose digits must all be
        either 0 or 1.
        """
        if self._sign != 0 or self._exp != 0:
            return False
        for dig in self._int:
            if dig not in '01':
                return False
        return True

    def _fill_logical(self, context, opa, opb):
        dif = context.prec - len(opa)
        if dif > 0:
            opa = '0' * dif + opa
        elif dif < 0:
            opa = opa[-context.prec:]
        dif = context.prec - len(opb)
        if dif > 0:
            opb = '0' * dif + opb
        elif dif < 0:
            opb = opb[-context.prec:]
        return (opa, opb)

    def 逻辑与(self, other, context=None):
        """Applies an 'and' operation between self and other's digits.

        Both self and other must be logical numbers.
        """
        if context is None:
            context = 取上下文()
        other = _convert_other(other, raiseit=True)
        if not self._islogical() or not other._islogical():
            return context._raise_error(无效运算)
        opa, opb = self._fill_logical(context, self._int, other._int)
        result = ''.join([str(int(a) & int(b)) for a, b in zip(opa, opb)])
        return _dec_from_triple(0, result.lstrip('0') or '0', 0)

    def 逻辑非(self, context=None):
        """Invert all its digits.

        The self must be logical number.
        """
        if context is None:
            context = 取上下文()
        return self.逻辑异或(_dec_from_triple(0, '1' * context.prec, 0), context)

    def 逻辑或(self, other, context=None):
        """Applies an 'or' operation between self and other's digits.

        Both self and other must be logical numbers.
        """
        if context is None:
            context = 取上下文()
        other = _convert_other(other, raiseit=True)
        if not self._islogical() or not other._islogical():
            return context._raise_error(无效运算)
        opa, opb = self._fill_logical(context, self._int, other._int)
        result = ''.join([str(int(a) | int(b)) for a, b in zip(opa, opb)])
        return _dec_from_triple(0, result.lstrip('0') or '0', 0)

    def 逻辑异或(self, other, context=None):
        """Applies an 'xor' operation between self and other's digits.

        Both self and other must be logical numbers.
        """
        if context is None:
            context = 取上下文()
        other = _convert_other(other, raiseit=True)
        if not self._islogical() or not other._islogical():
            return context._raise_error(无效运算)
        opa, opb = self._fill_logical(context, self._int, other._int)
        result = ''.join([str(int(a) ^ int(b)) for a, b in zip(opa, opb)])
        return _dec_from_triple(0, result.lstrip('0') or '0', 0)

    def 绝对值最大(self, other, context=None):
        """Compares the values numerically with their sign ignored."""
        other = _convert_other(other, raiseit=True)
        if context is None:
            context = 取上下文()
        if self._is_special or other._is_special:
            sn = self._isnan()
            on = other._isnan()
            if sn or on:
                if on == 1 and sn == 0:
                    return self._fix(context)
                if sn == 1 and on == 0:
                    return other._fix(context)
                return self._check_nans(other, context)
        c = self.复制绝对值()._cmp(other.copy_abs())
        if c == 0:
            c = self.全序比较(other)
        if c == -1:
            ans = other
        else:
            ans = self
        return ans._fix(context)

    def 绝对值最小(self, other, context=None):
        """Compares the values numerically with their sign ignored."""
        other = _convert_other(other, raiseit=True)
        if context is None:
            context = 取上下文()
        if self._is_special or other._is_special:
            sn = self._isnan()
            on = other._isnan()
            if sn or on:
                if on == 1 and sn == 0:
                    return self._fix(context)
                if sn == 1 and on == 0:
                    return other._fix(context)
                return self._check_nans(other, context)
        c = self.复制绝对值()._cmp(other.copy_abs())
        if c == 0:
            c = self.全序比较(other)
        if c == -1:
            ans = self
        else:
            ans = other
        return ans._fix(context)

    def 下一个更小(self, context=None):
        """Returns the largest representable number smaller than itself."""
        if context is None:
            context = 取上下文()
        ans = self._check_nans(context=context)
        if ans:
            return ans
        if self._isinfinity() == -1:
            return _NegativeInfinity
        if self._isinfinity() == 1:
            return _dec_from_triple(0, '9' * context.prec, context.Etop())
        context = context.copy()
        context._set_rounding(向下取整)
        context._ignore_all_flags()
        new_self = self._fix(context)
        if new_self != self:
            return new_self
        return self.__sub__(_dec_from_triple(0, '1', context.Etiny() - 1), context)

    def 下一个更大(self, context=None):
        """Returns the smallest representable number larger than itself."""
        if context is None:
            context = 取上下文()
        ans = self._check_nans(context=context)
        if ans:
            return ans
        if self._isinfinity() == 1:
            return _Infinity
        if self._isinfinity() == -1:
            return _dec_from_triple(1, '9' * context.prec, context.Etop())
        context = context.copy()
        context._set_rounding(向上取整)
        context._ignore_all_flags()
        new_self = self._fix(context)
        if new_self != self:
            return new_self
        return self.__add__(_dec_from_triple(0, '1', context.Etiny() - 1), context)

    def 朝某值下一个(self, other, context=None):
        """Returns the number closest to self, in the direction towards other.

        The result is the closest representable number to self
        (excluding self) that is in the direction towards other,
        unless both have the same value.  If the two operands are
        numerically equal, then the result is a copy of self with the
        sign set to be the same as the sign of other.
        """
        other = _convert_other(other, raiseit=True)
        if context is None:
            context = 取上下文()
        ans = self._check_nans(other, context)
        if ans:
            return ans
        comparison = self._cmp(other)
        if comparison == 0:
            return self.复制符号(other)
        if comparison == -1:
            ans = self.下一个更大(context)
        else:
            ans = self.下一个更小(context)
        if ans._isinfinity():
            context._raise_error(上溢, 'Infinite result from next_toward', ans._sign)
            context._raise_error(不精确)
            context._raise_error(已舍入)
        elif ans.adjusted() < context.Emin:
            context._raise_error(下溢)
            context._raise_error(次正规)
            context._raise_error(不精确)
            context._raise_error(已舍入)
            if not ans:
                context._raise_error(被钳位)
        return ans

    def 数值类别(self, context=None):
        """Returns an indication of the class of self.

        The class is one of the following strings:
          sNaN
          NaN
          -Infinity
          -Normal
          -Subnormal
          -Zero
          +Zero
          +Subnormal
          +Normal
          +Infinity
        """
        if self.是信号NaN吗():
            return 'sNaN'
        if self.是安静NaN吗():
            return 'NaN'
        inf = self._isinfinity()
        if inf == 1:
            return '+Infinity'
        if inf == -1:
            return '-Infinity'
        if self.是零吗():
            if self._sign:
                return '-Zero'
            else:
                return '+Zero'
        if context is None:
            context = 取上下文()
        if self.是次正规吗(context=context):
            if self._sign:
                return '-Subnormal'
            else:
                return '+Subnormal'
        if self._sign:
            return '-Normal'
        else:
            return '+Normal'

    def 基数(self):
        """Just returns 10, as this is Decimal, :)"""
        return 十进制数(10)

    def 循环移位(self, other, context=None):
        """Returns a rotated copy of self, value-of-other times."""
        if context is None:
            context = 取上下文()
        other = _convert_other(other, raiseit=True)
        ans = self._check_nans(other, context)
        if ans:
            return ans
        if other._exp != 0:
            return context._raise_error(无效运算)
        if not -context.prec <= int(other) <= context.prec:
            return context._raise_error(无效运算)
        if self._isinfinity():
            return 十进制数(self)
        torot = int(other)
        rotdig = self._int
        topad = context.prec - len(rotdig)
        if topad > 0:
            rotdig = '0' * topad + rotdig
        elif topad < 0:
            rotdig = rotdig[-topad:]
        rotated = rotdig[torot:] + rotdig[:torot]
        return _dec_from_triple(self._sign, rotated.lstrip('0') or '0', self._exp)

    def 按指数缩放(self, other, context=None):
        """Returns self operand after adding the second value to its exp."""
        if context is None:
            context = 取上下文()
        other = _convert_other(other, raiseit=True)
        ans = self._check_nans(other, context)
        if ans:
            return ans
        if other._exp != 0:
            return context._raise_error(无效运算)
        liminf = -2 * (context.Emax + context.prec)
        limsup = 2 * (context.Emax + context.prec)
        if not liminf <= int(other) <= limsup:
            return context._raise_error(无效运算)
        if self._isinfinity():
            return 十进制数(self)
        d = _dec_from_triple(self._sign, self._int, self._exp + int(other))
        d = d._fix(context)
        return d

    def 移位(self, other, context=None):
        """Returns a shifted copy of self, value-of-other times."""
        if context is None:
            context = 取上下文()
        other = _convert_other(other, raiseit=True)
        ans = self._check_nans(other, context)
        if ans:
            return ans
        if other._exp != 0:
            return context._raise_error(无效运算)
        if not -context.prec <= int(other) <= context.prec:
            return context._raise_error(无效运算)
        if self._isinfinity():
            return 十进制数(self)
        torot = int(other)
        rotdig = self._int
        topad = context.prec - len(rotdig)
        if topad > 0:
            rotdig = '0' * topad + rotdig
        elif topad < 0:
            rotdig = rotdig[-topad:]
        if torot < 0:
            shifted = rotdig[:torot]
        else:
            shifted = rotdig + '0' * torot
            shifted = shifted[-context.prec:]
        return _dec_from_triple(self._sign, shifted.lstrip('0') or '0', self._exp)

    def __reduce__(self):
        return (self.__class__, (str(self),))

    def __copy__(self):
        if type(self) is 十进制数:
            return self
        return self.__class__(str(self))

    def __deepcopy__(self, memo):
        if type(self) is 十进制数:
            return self
        return self.__class__(str(self))

    def __format__(self, specifier, context=None, _localeconv=None):
        """Format a Decimal instance according to the given specifier.

        The specifier should be a standard format specifier, with the
        form described in PEP 3101.  Formatting types 'e', 'E', 'f',
        'F', 'g', 'G', 'n' and '%' are supported.  If the formatting
        type is omitted it defaults to 'g' or 'G', depending on the
        value of context.capitals.
        """
        if context is None:
            context = 取上下文()
        spec = _parse_format_specifier(specifier, _localeconv=_localeconv)
        if self._is_special:
            sign = _format_sign(self._sign, spec)
            body = str(self.复制绝对值())
            if spec['type'] == '%':
                body += '%'
            return _format_align(sign, body, spec)
        if spec['type'] is None:
            spec['type'] = ['g', 'G'][context.capitals]
        if spec['type'] == '%':
            self = _dec_from_triple(self._sign, self._int, self._exp + 2)
        rounding = context.rounding
        precision = spec['precision']
        if precision is not None:
            if spec['type'] in 'eE':
                self = self._round(precision + 1, rounding)
            elif spec['type'] in 'fF%':
                self = self._rescale(-precision, rounding)
            elif spec['type'] in 'gG' and len(self._int) > precision:
                self = self._round(precision, rounding)
        if not self and self._exp > 0 and (spec['type'] in 'fF%'):
            self = self._rescale(0, rounding)
        if not self and spec['no_neg_0'] and self._sign:
            adjusted_sign = 0
        else:
            adjusted_sign = self._sign
        leftdigits = self._exp + len(self._int)
        if spec['type'] in 'eE':
            if not self and precision is not None:
                dotplace = 1 - precision
            else:
                dotplace = 1
        elif spec['type'] in 'fF%':
            dotplace = leftdigits
        elif spec['type'] in 'gG':
            if self._exp <= 0 and leftdigits > -6:
                dotplace = leftdigits
            else:
                dotplace = 1
        if dotplace < 0:
            intpart = '0'
            fracpart = '0' * -dotplace + self._int
        elif dotplace > len(self._int):
            intpart = self._int + '0' * (dotplace - len(self._int))
            fracpart = ''
        else:
            intpart = self._int[:dotplace] or '0'
            fracpart = self._int[dotplace:]
        指数 = leftdigits - dotplace
        return _format_number(adjusted_sign, intpart, fracpart, 指数, spec)
_装类转发(十进制数, {'adjusted': '调整指数', 'as_integer_ratio': '转整数比', 'as_tuple': '转元组', 'canonical': '取规范形', 'compare': '比较', 'compare_signal': '带信号比较', 'compare_total': '全序比较', 'compare_total_mag': '全序绝对值比较', 'conjugate': '共轭', 'copy_abs': '复制绝对值', 'copy_negate': '复制相反数', 'copy_sign': '复制符号', 'exp': '指数', 'fma': '乘加', 'from_float': '从浮点数', 'from_number': '从数值', 'imag': '虚部', 'is_canonical': '是规范形吗', 'is_finite': '是有限吗', 'is_infinite': '是无穷吗', 'is_nan': '是NaN吗', 'is_normal': '是正规数吗', 'is_qnan': '是安静NaN吗', 'is_signed': '带符号吗', 'is_snan': '是信号NaN吗', 'is_subnormal': '是次正规吗', 'is_zero': '是零吗', 'ln': '自然对数', 'log10': '常用对数', 'logb': '指数对数', 'logical_and': '逻辑与', 'logical_invert': '逻辑非', 'logical_or': '逻辑或', 'logical_xor': '逻辑异或', 'max_mag': '绝对值最大', 'min_mag': '绝对值最小', 'next_minus': '下一个更小', 'next_plus': '下一个更大', 'next_toward': '朝某值下一个', 'normalize': '规范化', 'number_class': '数值类别', 'quantize': '量化', 'radix': '基数', 'real': '实部', 'remainder_near': '就近余数', 'rotate': '循环移位', 'same_quantum': '同量级吗', 'scaleb': '按指数缩放', 'shift': '移位', 'sqrt': '平方根', 'to_eng_string': '转工程字符串', 'to_integral_exact': '精确取整', 'to_integral_value': '取整数值'}, {'adjusted': '调整指数', 'as_integer_ratio': '转整数比', 'as_tuple': '转元组', 'canonical': '取规范形', 'compare': '比较', 'compare_signal': '带信号比较', 'compare_total': '全序比较', 'compare_total_mag': '全序绝对值比较', 'conjugate': '共轭', 'copy_abs': '复制绝对值', 'copy_negate': '复制相反数', 'copy_sign': '复制符号', 'exp': '指数', 'fma': '乘加', 'from_float': '从浮点数', 'from_number': '从数值', 'imag': '虚部', 'is_canonical': '是规范形吗', 'is_finite': '是有限吗', 'is_infinite': '是无穷吗', 'is_nan': '是NaN吗', 'is_normal': '是正规数吗', 'is_qnan': '是安静NaN吗', 'is_signed': '带符号吗', 'is_snan': '是信号NaN吗', 'is_subnormal': '是次正规吗', 'is_zero': '是零吗', 'ln': '自然对数', 'log10': '常用对数', 'logb': '指数对数', 'logical_and': '逻辑与', 'logical_invert': '逻辑非', 'logical_or': '逻辑或', 'logical_xor': '逻辑异或', 'max_mag': '绝对值最大', 'min_mag': '绝对值最小', 'next_minus': '下一个更小', 'next_plus': '下一个更大', 'next_toward': '朝某值下一个', 'normalize': '规范化', 'number_class': '数值类别', 'quantize': '量化', 'radix': '基数', 'real': '实部', 'remainder_near': '就近余数', 'rotate': '循环移位', 'same_quantum': '同量级吗', 'scaleb': '按指数缩放', 'shift': '移位', 'sqrt': '平方根', 'to_eng_string': '转工程字符串', 'to_integral_exact': '精确取整', 'to_integral_value': '取整数值'})

def _dec_from_triple(sign, coefficient, exponent, special=False):
    """Create a decimal instance directly, without any validation,
    normalization (e.g. removal of leading zeros) or argument
    conversion.

    This function is for *internal use only*.
    """
    self = object.__new__(十进制数)
    self._sign = sign
    self._int = coefficient
    self._exp = exponent
    self._is_special = special
    return self
_numbers.Number.register(十进制数)

class _ContextManager(object):
    """Context manager class to support localcontext().

      Sets a copy of the supplied context in __enter__() and restores
      the previous decimal context in __exit__()
    """

    def __init__(self, new_context):
        self.new_context = new_context.copy()

    def __enter__(self):
        self.saved_context = 取上下文()
        设上下文(self.new_context)
        return self.new_context

    def __exit__(self, t, v, tb):
        设上下文(self.saved_context)

class 十进制上下文(object):
    """Contains the context for a Decimal instance.

    Contains:
    prec - precision (for use in rounding, division, square roots..)
    rounding - rounding type (how you round)
    traps - If traps[exception] = 1, then the exception is
                    raised when it is caused.  Otherwise, a value is
                    substituted in.
    flags  - When an exception is caused, flags[exception] is set.
             (Whether or not the trap_enabler is set)
             Should be reset by user of Decimal instance.
    Emin -   Minimum exponent
    Emax -   Maximum exponent
    capitals -      If 1, 1*10^1 is printed as 1E+1.
                    If 0, printed as 1e1
    clamp -  If 1, change exponents if too high (Default 0)
    """

    def __init__(self, prec=None, rounding=None, Emin=None, Emax=None, capitals=None, clamp=None, flags=None, traps=None, _ignored_flags=None):
        try:
            dc = 默认上下文
        except NameError:
            pass
        self.prec = prec if prec is not None else dc.prec
        self.rounding = rounding if rounding is not None else dc.rounding
        self.Emin = Emin if Emin is not None else dc.Emin
        self.Emax = Emax if Emax is not None else dc.Emax
        self.capitals = capitals if capitals is not None else dc.capitals
        self.clamp = clamp if clamp is not None else dc.clamp
        if _ignored_flags is None:
            self._ignored_flags = []
        else:
            self._ignored_flags = _ignored_flags
        if traps is None:
            self.traps = dc.traps.copy()
        elif not isinstance(traps, dict):
            self.traps = dict(((s, int(s in traps)) for s in _signals + traps))
        else:
            self.traps = traps
        if flags is None:
            self.flags = dict.fromkeys(_signals, 0)
        elif not isinstance(flags, dict):
            self.flags = dict(((s, int(s in flags)) for s in _signals + flags))
        else:
            self.flags = flags

    def _set_integer_check(self, name, value, vmin, vmax):
        if not isinstance(value, int):
            raise TypeError('%s must be an integer' % name)
        if vmin == '-inf':
            if value > vmax:
                raise ValueError('%s must be in [%s, %d]. got: %s' % (name, vmin, vmax, value))
        elif vmax == 'inf':
            if value < vmin:
                raise ValueError('%s must be in [%d, %s]. got: %s' % (name, vmin, vmax, value))
        elif value < vmin or value > vmax:
            raise ValueError('%s must be in [%d, %d]. got %s' % (name, vmin, vmax, value))
        return object.__setattr__(self, name, value)

    def _set_signal_dict(self, name, d):
        if not isinstance(d, dict):
            raise TypeError('%s must be a signal dict' % d)
        for key in d:
            if not key in _signals:
                raise KeyError('%s is not a valid signal dict' % d)
        for key in _signals:
            if not key in d:
                raise KeyError('%s is not a valid signal dict' % d)
        return object.__setattr__(self, name, d)

    def __setattr__(self, name, value):
        if name == 'prec':
            return self._set_integer_check(name, value, 1, 'inf')
        elif name == 'Emin':
            return self._set_integer_check(name, value, '-inf', 0)
        elif name == 'Emax':
            return self._set_integer_check(name, value, 0, 'inf')
        elif name == 'capitals':
            return self._set_integer_check(name, value, 0, 1)
        elif name == 'clamp':
            return self._set_integer_check(name, value, 0, 1)
        elif name == 'rounding':
            if not value in _rounding_modes:
                raise TypeError('%s: invalid rounding mode' % value)
            return object.__setattr__(self, name, value)
        elif name == 'flags' or name == 'traps':
            return self._set_signal_dict(name, value)
        elif name == '_ignored_flags':
            return object.__setattr__(self, name, value)
        else:
            raise AttributeError("'decimal.Context' object has no attribute '%s'" % name)

    def __delattr__(self, name):
        raise AttributeError('%s cannot be deleted' % name)

    def __reduce__(self):
        flags = [sig for sig, v in self.flags.items() if v]
        traps = [sig for sig, v in self.traps.items() if v]
        return (self.__class__, (self.prec, self.rounding, self.Emin, self.Emax, self.capitals, self.clamp, flags, traps))

    def __repr__(self):
        """Show the current context."""
        s = []
        s.append('Context(prec=%(prec)d, rounding=%(rounding)s, Emin=%(Emin)d, Emax=%(Emax)d, capitals=%(capitals)d, clamp=%(clamp)d' % vars(self))
        names = [f.__name__ for f, v in self.flags.items() if v]
        s.append('flags=[' + ', '.join(names) + ']')
        names = [t.__name__ for t, v in self.traps.items() if v]
        s.append('traps=[' + ', '.join(names) + ']')
        return ', '.join(s) + ')'

    def 清标志(self):
        """Reset all flags to zero"""
        for flag in self.flags:
            self.flags[flag] = 0

    def 清陷阱(self):
        """Reset all traps to zero"""
        for flag in self.traps:
            self.traps[flag] = 0

    def _shallow_copy(self):
        """Returns a shallow copy from self."""
        nc = 十进制上下文(self.prec, self.rounding, self.Emin, self.Emax, self.capitals, self.clamp, self.flags, self.traps, self._ignored_flags)
        return nc

    def copy(self):
        """Returns a deep copy from self."""
        nc = 十进制上下文(self.prec, self.rounding, self.Emin, self.Emax, self.capitals, self.clamp, self.flags.copy(), self.traps.copy(), self._ignored_flags)
        return nc
    __copy__ = copy

    def _raise_error(self, condition, explanation=None, *args):
        """Handles an error

        If the flag is in _ignored_flags, returns the default response.
        Otherwise, it sets the flag, then, if the corresponding
        trap_enabler is set, it reraises the exception.  Otherwise, it returns
        the default value after setting the flag.
        """
        error = _condition_map.get(condition, condition)
        if error in self._ignored_flags:
            return error().handle(self, *args)
        self.flags[error] = 1
        if not self.traps[error]:
            return condition().handle(self, *args)
        raise error(explanation)

    def _ignore_all_flags(self):
        """Ignore all flags, if they are raised"""
        return self._ignore_flags(*_signals)

    def _ignore_flags(self, *flags):
        """Ignore the flags, if they are raised"""
        self._ignored_flags = self._ignored_flags + list(flags)
        return list(flags)

    def _regard_flags(self, *flags):
        """Stop ignoring the flags, if they are raised"""
        if flags and isinstance(flags[0], (tuple, list)):
            flags = flags[0]
        for flag in flags:
            self._ignored_flags.remove(flag)
    __hash__ = None

    def 指数理论下限(self):
        """Returns Etiny (= Emin - prec + 1)"""
        return int(self.Emin - self.prec + 1)

    def 指数上限(self):
        """Returns maximum exponent (= Emax - prec + 1)"""
        return int(self.Emax - self.prec + 1)

    def _set_rounding(self, type):
        """Sets the rounding type.

        Sets the rounding type, and returns the current (previous)
        rounding type.  Often used like:

        context = context.copy()
        # so you don't change the calling context
        # if an error occurs in the middle.
        rounding = context._set_rounding(ROUND_UP)
        val = self.__sub__(other, context=context)
        context._set_rounding(rounding)

        This will make it round up for that operation.
        """
        rounding = self.rounding
        self.rounding = type
        return rounding

    def 造十进制数(self, num='0'):
        """Creates a new Decimal instance but using self as context.

        This method implements the to-number operation of the
        IBM Decimal specification."""
        if isinstance(num, str) and (num != num.strip() or '_' in num):
            return self._raise_error(转换语法错误, 'trailing or leading whitespace and underscores are not permitted.')
        d = 十进制数(num, context=self)
        if d._isnan() and len(d._int) > self.prec - self.clamp:
            return self._raise_error(转换语法错误, 'diagnostic info too long in NaN')
        return d._fix(self)

    def 从浮点造十进制数(self, f):
        """Creates a new Decimal instance from a float but rounding using self
        as the context.

        >>> context = Context(prec=5, rounding=ROUND_DOWN)
        >>> context.create_decimal_from_float(3.1415926535897932)
        Decimal('3.1415')
        >>> context = Context(prec=5, traps=[Inexact])
        >>> context.create_decimal_from_float(3.1415926535897932)
        Traceback (most recent call last):
            ...
        decimal.Inexact: None

        """
        d = 十进制数.从浮点数(f)
        return d._fix(self)

    def abs(self, a):
        """Returns the absolute value of the operand.

        If the operand is negative, the result is the same as using the
        minus operation on the operand.  Otherwise, the result is the same
        as using the plus operation on the operand.

        >>> ExtendedContext.abs(Decimal('2.1'))
        Decimal('2.1')
        >>> ExtendedContext.abs(Decimal('-100'))
        Decimal('100')
        >>> ExtendedContext.abs(Decimal('101.5'))
        Decimal('101.5')
        >>> ExtendedContext.abs(Decimal('-101.5'))
        Decimal('101.5')
        >>> ExtendedContext.abs(-1)
        Decimal('1')
        """
        a = _convert_other(a, raiseit=True)
        return a.__abs__(context=self)

    def add(self, a, b):
        """Return the sum of the two operands.

        >>> ExtendedContext.add(Decimal('12'), Decimal('7.00'))
        Decimal('19.00')
        >>> ExtendedContext.add(Decimal('1E+2'), Decimal('1.01E+4'))
        Decimal('1.02E+4')
        >>> ExtendedContext.add(1, Decimal(2))
        Decimal('3')
        >>> ExtendedContext.add(Decimal(8), 5)
        Decimal('13')
        >>> ExtendedContext.add(5, 5)
        Decimal('10')
        """
        a = _convert_other(a, raiseit=True)
        r = a.__add__(b, context=self)
        if r is NotImplemented:
            raise TypeError('Unable to convert %s to Decimal' % b)
        else:
            return r

    def _apply(self, a):
        return str(a._fix(self))

    def 取规范形(self, a):
        """Returns the same Decimal object.

        As we do not have different encodings for the same number, the
        received object already is in its canonical form.

        >>> ExtendedContext.canonical(Decimal('2.50'))
        Decimal('2.50')
        """
        if not isinstance(a, 十进制数):
            raise TypeError('canonical requires a Decimal as an argument.')
        return a.canonical()

    def 比较(self, a, b):
        """Compares values numerically.

        If the signs of the operands differ, a value representing each
        operand ('-1' if the operand is less than zero, '0' if the operand
        is zero or negative zero, or '1' if the operand is greater than
        zero) is used in place of that operand for the comparison instead of
        the actual operand.

        The comparison is then effected by subtracting the second operand
        from the first and then returning a value according to the result of
        the subtraction: '-1' if the result is less than zero, '0' if the
        result is zero or negative zero, or '1' if the result is greater
        than zero.

        >>> ExtendedContext.compare(Decimal('2.1'), Decimal('3'))
        Decimal('-1')
        >>> ExtendedContext.compare(Decimal('2.1'), Decimal('2.1'))
        Decimal('0')
        >>> ExtendedContext.compare(Decimal('2.1'), Decimal('2.10'))
        Decimal('0')
        >>> ExtendedContext.compare(Decimal('3'), Decimal('2.1'))
        Decimal('1')
        >>> ExtendedContext.compare(Decimal('2.1'), Decimal('-3'))
        Decimal('1')
        >>> ExtendedContext.compare(Decimal('-3'), Decimal('2.1'))
        Decimal('-1')
        >>> ExtendedContext.compare(1, 2)
        Decimal('-1')
        >>> ExtendedContext.compare(Decimal(1), 2)
        Decimal('-1')
        >>> ExtendedContext.compare(1, Decimal(2))
        Decimal('-1')
        """
        a = _convert_other(a, raiseit=True)
        return a.compare(b, context=self)

    def 带信号比较(self, a, b):
        """Compares the values of the two operands numerically.

        It's pretty much like compare(), but all NaNs signal, with signaling
        NaNs taking precedence over quiet NaNs.

        >>> c = ExtendedContext
        >>> c.compare_signal(Decimal('2.1'), Decimal('3'))
        Decimal('-1')
        >>> c.compare_signal(Decimal('2.1'), Decimal('2.1'))
        Decimal('0')
        >>> c.flags[InvalidOperation] = 0
        >>> print(c.flags[InvalidOperation])
        0
        >>> c.compare_signal(Decimal('NaN'), Decimal('2.1'))
        Decimal('NaN')
        >>> print(c.flags[InvalidOperation])
        1
        >>> c.flags[InvalidOperation] = 0
        >>> print(c.flags[InvalidOperation])
        0
        >>> c.compare_signal(Decimal('sNaN'), Decimal('2.1'))
        Decimal('NaN')
        >>> print(c.flags[InvalidOperation])
        1
        >>> c.compare_signal(-1, 2)
        Decimal('-1')
        >>> c.compare_signal(Decimal(-1), 2)
        Decimal('-1')
        >>> c.compare_signal(-1, Decimal(2))
        Decimal('-1')
        """
        a = _convert_other(a, raiseit=True)
        return a.compare_signal(b, context=self)

    def 全序比较(self, a, b):
        """Compares two operands using their abstract representation.

        This is not like the standard compare, which use their numerical
        value.  Note that a total ordering is defined for all possible
        abstract representations.

        >>> ExtendedContext.compare_total(Decimal('12.73'), Decimal('127.9'))
        Decimal('-1')
        >>> ExtendedContext.compare_total(Decimal('-127'),  Decimal('12'))
        Decimal('-1')
        >>> ExtendedContext.compare_total(Decimal('12.30'), Decimal('12.3'))
        Decimal('-1')
        >>> ExtendedContext.compare_total(Decimal('12.30'), Decimal('12.30'))
        Decimal('0')
        >>> ExtendedContext.compare_total(Decimal('12.3'),  Decimal('12.300'))
        Decimal('1')
        >>> ExtendedContext.compare_total(Decimal('12.3'),  Decimal('NaN'))
        Decimal('-1')
        >>> ExtendedContext.compare_total(1, 2)
        Decimal('-1')
        >>> ExtendedContext.compare_total(Decimal(1), 2)
        Decimal('-1')
        >>> ExtendedContext.compare_total(1, Decimal(2))
        Decimal('-1')
        """
        a = _convert_other(a, raiseit=True)
        return a.compare_total(b)

    def 全序绝对值比较(self, a, b):
        """Compares two operands using their abstract representation ignoring sign.

        Like compare_total, but with operand's sign ignored and assumed to
        be 0.
        """
        a = _convert_other(a, raiseit=True)
        return a.compare_total_mag(b)

    def 复制绝对值(self, a):
        """Returns a copy of the operand with the sign set to 0.

        >>> ExtendedContext.copy_abs(Decimal('2.1'))
        Decimal('2.1')
        >>> ExtendedContext.copy_abs(Decimal('-100'))
        Decimal('100')
        >>> ExtendedContext.copy_abs(-1)
        Decimal('1')
        """
        a = _convert_other(a, raiseit=True)
        return a.copy_abs()

    def 复制十进制数(self, a):
        """Returns a copy of the decimal object.

        >>> ExtendedContext.copy_decimal(Decimal('2.1'))
        Decimal('2.1')
        >>> ExtendedContext.copy_decimal(Decimal('-1.00'))
        Decimal('-1.00')
        >>> ExtendedContext.copy_decimal(1)
        Decimal('1')
        """
        a = _convert_other(a, raiseit=True)
        return 十进制数(a)

    def 复制相反数(self, a):
        """Returns a copy of the operand with the sign inverted.

        >>> ExtendedContext.copy_negate(Decimal('101.5'))
        Decimal('-101.5')
        >>> ExtendedContext.copy_negate(Decimal('-101.5'))
        Decimal('101.5')
        >>> ExtendedContext.copy_negate(1)
        Decimal('-1')
        """
        a = _convert_other(a, raiseit=True)
        return a.copy_negate()

    def 复制符号(self, a, b):
        """Copies the second operand's sign to the first one.

        In detail, it returns a copy of the first operand with the sign
        equal to the sign of the second operand.

        >>> ExtendedContext.copy_sign(Decimal( '1.50'), Decimal('7.33'))
        Decimal('1.50')
        >>> ExtendedContext.copy_sign(Decimal('-1.50'), Decimal('7.33'))
        Decimal('1.50')
        >>> ExtendedContext.copy_sign(Decimal( '1.50'), Decimal('-7.33'))
        Decimal('-1.50')
        >>> ExtendedContext.copy_sign(Decimal('-1.50'), Decimal('-7.33'))
        Decimal('-1.50')
        >>> ExtendedContext.copy_sign(1, -2)
        Decimal('-1')
        >>> ExtendedContext.copy_sign(Decimal(1), -2)
        Decimal('-1')
        >>> ExtendedContext.copy_sign(1, Decimal(-2))
        Decimal('-1')
        """
        a = _convert_other(a, raiseit=True)
        return a.copy_sign(b)

    def 除(self, a, b):
        """Decimal division in a specified context.

        >>> ExtendedContext.divide(Decimal('1'), Decimal('3'))
        Decimal('0.333333333')
        >>> ExtendedContext.divide(Decimal('2'), Decimal('3'))
        Decimal('0.666666667')
        >>> ExtendedContext.divide(Decimal('5'), Decimal('2'))
        Decimal('2.5')
        >>> ExtendedContext.divide(Decimal('1'), Decimal('10'))
        Decimal('0.1')
        >>> ExtendedContext.divide(Decimal('12'), Decimal('12'))
        Decimal('1')
        >>> ExtendedContext.divide(Decimal('8.00'), Decimal('2'))
        Decimal('4.00')
        >>> ExtendedContext.divide(Decimal('2.400'), Decimal('2.0'))
        Decimal('1.20')
        >>> ExtendedContext.divide(Decimal('1000'), Decimal('100'))
        Decimal('10')
        >>> ExtendedContext.divide(Decimal('1000'), Decimal('1'))
        Decimal('1000')
        >>> ExtendedContext.divide(Decimal('2.40E+6'), Decimal('2'))
        Decimal('1.20E+6')
        >>> ExtendedContext.divide(5, 5)
        Decimal('1')
        >>> ExtendedContext.divide(Decimal(5), 5)
        Decimal('1')
        >>> ExtendedContext.divide(5, Decimal(5))
        Decimal('1')
        """
        a = _convert_other(a, raiseit=True)
        r = a.__truediv__(b, context=self)
        if r is NotImplemented:
            raise TypeError('Unable to convert %s to Decimal' % b)
        else:
            return r

    def 整除(self, a, b):
        """Divides two numbers and returns the integer part of the result.

        >>> ExtendedContext.divide_int(Decimal('2'), Decimal('3'))
        Decimal('0')
        >>> ExtendedContext.divide_int(Decimal('10'), Decimal('3'))
        Decimal('3')
        >>> ExtendedContext.divide_int(Decimal('1'), Decimal('0.3'))
        Decimal('3')
        >>> ExtendedContext.divide_int(10, 3)
        Decimal('3')
        >>> ExtendedContext.divide_int(Decimal(10), 3)
        Decimal('3')
        >>> ExtendedContext.divide_int(10, Decimal(3))
        Decimal('3')
        """
        a = _convert_other(a, raiseit=True)
        r = a.__floordiv__(b, context=self)
        if r is NotImplemented:
            raise TypeError('Unable to convert %s to Decimal' % b)
        else:
            return r

    def divmod(self, a, b):
        """Return (a // b, a % b).

        >>> ExtendedContext.divmod(Decimal(8), Decimal(3))
        (Decimal('2'), Decimal('2'))
        >>> ExtendedContext.divmod(Decimal(8), Decimal(4))
        (Decimal('2'), Decimal('0'))
        >>> ExtendedContext.divmod(8, 4)
        (Decimal('2'), Decimal('0'))
        >>> ExtendedContext.divmod(Decimal(8), 4)
        (Decimal('2'), Decimal('0'))
        >>> ExtendedContext.divmod(8, Decimal(4))
        (Decimal('2'), Decimal('0'))
        """
        a = _convert_other(a, raiseit=True)
        r = a.__divmod__(b, context=self)
        if r is NotImplemented:
            raise TypeError('Unable to convert %s to Decimal' % b)
        else:
            return r

    def 指数(self, a):
        """Returns e ** a.

        >>> c = ExtendedContext.copy()
        >>> c.Emin = -999
        >>> c.Emax = 999
        >>> c.exp(Decimal('-Infinity'))
        Decimal('0')
        >>> c.exp(Decimal('-1'))
        Decimal('0.367879441')
        >>> c.exp(Decimal('0'))
        Decimal('1')
        >>> c.exp(Decimal('1'))
        Decimal('2.71828183')
        >>> c.exp(Decimal('0.693147181'))
        Decimal('2.00000000')
        >>> c.exp(Decimal('+Infinity'))
        Decimal('Infinity')
        >>> c.exp(10)
        Decimal('22026.4658')
        """
        a = _convert_other(a, raiseit=True)
        return a.exp(context=self)

    def 乘加(self, a, b, c):
        """Returns a multiplied by b, plus c.

        The first two operands are multiplied together, using multiply,
        the third operand is then added to the result of that
        multiplication, using add, all with only one final rounding.

        >>> ExtendedContext.fma(Decimal('3'), Decimal('5'), Decimal('7'))
        Decimal('22')
        >>> ExtendedContext.fma(Decimal('3'), Decimal('-5'), Decimal('7'))
        Decimal('-8')
        >>> ExtendedContext.fma(Decimal('888565290'), Decimal('1557.96930'), Decimal('-86087.7578'))
        Decimal('1.38435736E+12')
        >>> ExtendedContext.fma(1, 3, 4)
        Decimal('7')
        >>> ExtendedContext.fma(1, Decimal(3), 4)
        Decimal('7')
        >>> ExtendedContext.fma(1, 3, Decimal(4))
        Decimal('7')
        """
        a = _convert_other(a, raiseit=True)
        return a.fma(b, c, context=self)

    def 是规范形吗(self, a):
        """Return True if the operand is canonical; otherwise return False.

        Currently, the encoding of a Decimal instance is always
        canonical, so this method returns True for any Decimal.

        >>> ExtendedContext.is_canonical(Decimal('2.50'))
        True
        """
        if not isinstance(a, 十进制数):
            raise TypeError('is_canonical requires a Decimal as an argument.')
        return a.is_canonical()

    def 是有限吗(self, a):
        """Return True if the operand is finite; otherwise return False.

        A Decimal instance is considered finite if it is neither
        infinite nor a NaN.

        >>> ExtendedContext.is_finite(Decimal('2.50'))
        True
        >>> ExtendedContext.is_finite(Decimal('-0.3'))
        True
        >>> ExtendedContext.is_finite(Decimal('0'))
        True
        >>> ExtendedContext.is_finite(Decimal('Inf'))
        False
        >>> ExtendedContext.is_finite(Decimal('NaN'))
        False
        >>> ExtendedContext.is_finite(1)
        True
        """
        a = _convert_other(a, raiseit=True)
        return a.is_finite()

    def 是无穷吗(self, a):
        """Return True if the operand is infinite; otherwise return False.

        >>> ExtendedContext.is_infinite(Decimal('2.50'))
        False
        >>> ExtendedContext.is_infinite(Decimal('-Inf'))
        True
        >>> ExtendedContext.is_infinite(Decimal('NaN'))
        False
        >>> ExtendedContext.is_infinite(1)
        False
        """
        a = _convert_other(a, raiseit=True)
        return a.is_infinite()

    def 是NaN吗(self, a):
        """Return True if the operand is a qNaN or sNaN;
        otherwise return False.

        >>> ExtendedContext.is_nan(Decimal('2.50'))
        False
        >>> ExtendedContext.is_nan(Decimal('NaN'))
        True
        >>> ExtendedContext.is_nan(Decimal('-sNaN'))
        True
        >>> ExtendedContext.is_nan(1)
        False
        """
        a = _convert_other(a, raiseit=True)
        return a.is_nan()

    def 是正规数吗(self, a):
        """Return True if the operand is a normal number;
        otherwise return False.

        >>> c = ExtendedContext.copy()
        >>> c.Emin = -999
        >>> c.Emax = 999
        >>> c.is_normal(Decimal('2.50'))
        True
        >>> c.is_normal(Decimal('0.1E-999'))
        False
        >>> c.is_normal(Decimal('0.00'))
        False
        >>> c.is_normal(Decimal('-Inf'))
        False
        >>> c.is_normal(Decimal('NaN'))
        False
        >>> c.is_normal(1)
        True
        """
        a = _convert_other(a, raiseit=True)
        return a.is_normal(context=self)

    def 是安静NaN吗(self, a):
        """Return True if the operand is a quiet NaN; otherwise return False.

        >>> ExtendedContext.is_qnan(Decimal('2.50'))
        False
        >>> ExtendedContext.is_qnan(Decimal('NaN'))
        True
        >>> ExtendedContext.is_qnan(Decimal('sNaN'))
        False
        >>> ExtendedContext.is_qnan(1)
        False
        """
        a = _convert_other(a, raiseit=True)
        return a.is_qnan()

    def 带符号吗(self, a):
        """Return True if the operand is negative; otherwise return False.

        >>> ExtendedContext.is_signed(Decimal('2.50'))
        False
        >>> ExtendedContext.is_signed(Decimal('-12'))
        True
        >>> ExtendedContext.is_signed(Decimal('-0'))
        True
        >>> ExtendedContext.is_signed(8)
        False
        >>> ExtendedContext.is_signed(-8)
        True
        """
        a = _convert_other(a, raiseit=True)
        return a.is_signed()

    def 是信号NaN吗(self, a):
        """Return True if the operand is a signaling NaN;
        otherwise return False.

        >>> ExtendedContext.is_snan(Decimal('2.50'))
        False
        >>> ExtendedContext.is_snan(Decimal('NaN'))
        False
        >>> ExtendedContext.is_snan(Decimal('sNaN'))
        True
        >>> ExtendedContext.is_snan(1)
        False
        """
        a = _convert_other(a, raiseit=True)
        return a.is_snan()

    def 是次正规吗(self, a):
        """Return True if the operand is subnormal; otherwise return False.

        >>> c = ExtendedContext.copy()
        >>> c.Emin = -999
        >>> c.Emax = 999
        >>> c.is_subnormal(Decimal('2.50'))
        False
        >>> c.is_subnormal(Decimal('0.1E-999'))
        True
        >>> c.is_subnormal(Decimal('0.00'))
        False
        >>> c.is_subnormal(Decimal('-Inf'))
        False
        >>> c.is_subnormal(Decimal('NaN'))
        False
        >>> c.is_subnormal(1)
        False
        """
        a = _convert_other(a, raiseit=True)
        return a.is_subnormal(context=self)

    def 是零吗(self, a):
        """Return True if the operand is a zero; otherwise return False.

        >>> ExtendedContext.is_zero(Decimal('0'))
        True
        >>> ExtendedContext.is_zero(Decimal('2.50'))
        False
        >>> ExtendedContext.is_zero(Decimal('-0E+2'))
        True
        >>> ExtendedContext.is_zero(1)
        False
        >>> ExtendedContext.is_zero(0)
        True
        """
        a = _convert_other(a, raiseit=True)
        return a.is_zero()

    def 自然对数(self, a):
        """Returns the natural (base e) logarithm of the operand.

        >>> c = ExtendedContext.copy()
        >>> c.Emin = -999
        >>> c.Emax = 999
        >>> c.ln(Decimal('0'))
        Decimal('-Infinity')
        >>> c.ln(Decimal('1.000'))
        Decimal('0')
        >>> c.ln(Decimal('2.71828183'))
        Decimal('1.00000000')
        >>> c.ln(Decimal('10'))
        Decimal('2.30258509')
        >>> c.ln(Decimal('+Infinity'))
        Decimal('Infinity')
        >>> c.ln(1)
        Decimal('0')
        """
        a = _convert_other(a, raiseit=True)
        return a.ln(context=self)

    def 常用对数(self, a):
        """Returns the base 10 logarithm of the operand.

        >>> c = ExtendedContext.copy()
        >>> c.Emin = -999
        >>> c.Emax = 999
        >>> c.log10(Decimal('0'))
        Decimal('-Infinity')
        >>> c.log10(Decimal('0.001'))
        Decimal('-3')
        >>> c.log10(Decimal('1.000'))
        Decimal('0')
        >>> c.log10(Decimal('2'))
        Decimal('0.301029996')
        >>> c.log10(Decimal('10'))
        Decimal('1')
        >>> c.log10(Decimal('70'))
        Decimal('1.84509804')
        >>> c.log10(Decimal('+Infinity'))
        Decimal('Infinity')
        >>> c.log10(0)
        Decimal('-Infinity')
        >>> c.log10(1)
        Decimal('0')
        """
        a = _convert_other(a, raiseit=True)
        return a.log10(context=self)

    def 指数对数(self, a):
        """ Returns the exponent of the magnitude of the operand's MSD.

        The result is the integer which is the exponent of the magnitude
        of the most significant digit of the operand (as though the
        operand were truncated to a single digit while maintaining the
        value of that digit and without limiting the resulting exponent).

        >>> ExtendedContext.logb(Decimal('250'))
        Decimal('2')
        >>> ExtendedContext.logb(Decimal('2.50'))
        Decimal('0')
        >>> ExtendedContext.logb(Decimal('0.03'))
        Decimal('-2')
        >>> ExtendedContext.logb(Decimal('0'))
        Decimal('-Infinity')
        >>> ExtendedContext.logb(1)
        Decimal('0')
        >>> ExtendedContext.logb(10)
        Decimal('1')
        >>> ExtendedContext.logb(100)
        Decimal('2')
        """
        a = _convert_other(a, raiseit=True)
        return a.logb(context=self)

    def 逻辑与(self, a, b):
        """Applies the logical operation 'and' between each operand's digits.

        The operands must be both logical numbers.

        >>> ExtendedContext.logical_and(Decimal('0'), Decimal('0'))
        Decimal('0')
        >>> ExtendedContext.logical_and(Decimal('0'), Decimal('1'))
        Decimal('0')
        >>> ExtendedContext.logical_and(Decimal('1'), Decimal('0'))
        Decimal('0')
        >>> ExtendedContext.logical_and(Decimal('1'), Decimal('1'))
        Decimal('1')
        >>> ExtendedContext.logical_and(Decimal('1100'), Decimal('1010'))
        Decimal('1000')
        >>> ExtendedContext.logical_and(Decimal('1111'), Decimal('10'))
        Decimal('10')
        >>> ExtendedContext.logical_and(110, 1101)
        Decimal('100')
        >>> ExtendedContext.logical_and(Decimal(110), 1101)
        Decimal('100')
        >>> ExtendedContext.logical_and(110, Decimal(1101))
        Decimal('100')
        """
        a = _convert_other(a, raiseit=True)
        return a.logical_and(b, context=self)

    def 逻辑非(self, a):
        """Invert all the digits in the operand.

        The operand must be a logical number.

        >>> ExtendedContext.logical_invert(Decimal('0'))
        Decimal('111111111')
        >>> ExtendedContext.logical_invert(Decimal('1'))
        Decimal('111111110')
        >>> ExtendedContext.logical_invert(Decimal('111111111'))
        Decimal('0')
        >>> ExtendedContext.logical_invert(Decimal('101010101'))
        Decimal('10101010')
        >>> ExtendedContext.logical_invert(1101)
        Decimal('111110010')
        """
        a = _convert_other(a, raiseit=True)
        return a.logical_invert(context=self)

    def 逻辑或(self, a, b):
        """Applies the logical operation 'or' between each operand's digits.

        The operands must be both logical numbers.

        >>> ExtendedContext.logical_or(Decimal('0'), Decimal('0'))
        Decimal('0')
        >>> ExtendedContext.logical_or(Decimal('0'), Decimal('1'))
        Decimal('1')
        >>> ExtendedContext.logical_or(Decimal('1'), Decimal('0'))
        Decimal('1')
        >>> ExtendedContext.logical_or(Decimal('1'), Decimal('1'))
        Decimal('1')
        >>> ExtendedContext.logical_or(Decimal('1100'), Decimal('1010'))
        Decimal('1110')
        >>> ExtendedContext.logical_or(Decimal('1110'), Decimal('10'))
        Decimal('1110')
        >>> ExtendedContext.logical_or(110, 1101)
        Decimal('1111')
        >>> ExtendedContext.logical_or(Decimal(110), 1101)
        Decimal('1111')
        >>> ExtendedContext.logical_or(110, Decimal(1101))
        Decimal('1111')
        """
        a = _convert_other(a, raiseit=True)
        return a.logical_or(b, context=self)

    def 逻辑异或(self, a, b):
        """Applies the logical operation 'xor' between each operand's digits.

        The operands must be both logical numbers.

        >>> ExtendedContext.logical_xor(Decimal('0'), Decimal('0'))
        Decimal('0')
        >>> ExtendedContext.logical_xor(Decimal('0'), Decimal('1'))
        Decimal('1')
        >>> ExtendedContext.logical_xor(Decimal('1'), Decimal('0'))
        Decimal('1')
        >>> ExtendedContext.logical_xor(Decimal('1'), Decimal('1'))
        Decimal('0')
        >>> ExtendedContext.logical_xor(Decimal('1100'), Decimal('1010'))
        Decimal('110')
        >>> ExtendedContext.logical_xor(Decimal('1111'), Decimal('10'))
        Decimal('1101')
        >>> ExtendedContext.logical_xor(110, 1101)
        Decimal('1011')
        >>> ExtendedContext.logical_xor(Decimal(110), 1101)
        Decimal('1011')
        >>> ExtendedContext.logical_xor(110, Decimal(1101))
        Decimal('1011')
        """
        a = _convert_other(a, raiseit=True)
        return a.logical_xor(b, context=self)

    def max(self, a, b):
        """max compares two values numerically and returns the maximum.

        If either operand is a NaN then the general rules apply.
        Otherwise, the operands are compared as though by the compare
        operation.  If they are numerically equal then the left-hand operand
        is chosen as the result.  Otherwise the maximum (closer to positive
        infinity) of the two operands is chosen as the result.

        >>> ExtendedContext.max(Decimal('3'), Decimal('2'))
        Decimal('3')
        >>> ExtendedContext.max(Decimal('-10'), Decimal('3'))
        Decimal('3')
        >>> ExtendedContext.max(Decimal('1.0'), Decimal('1'))
        Decimal('1')
        >>> ExtendedContext.max(Decimal('7'), Decimal('NaN'))
        Decimal('7')
        >>> ExtendedContext.max(1, 2)
        Decimal('2')
        >>> ExtendedContext.max(Decimal(1), 2)
        Decimal('2')
        >>> ExtendedContext.max(1, Decimal(2))
        Decimal('2')
        """
        a = _convert_other(a, raiseit=True)
        return a.max(b, context=self)

    def 绝对值最大(self, a, b):
        """Compares the values numerically with their sign ignored.

        >>> ExtendedContext.max_mag(Decimal('7'), Decimal('NaN'))
        Decimal('7')
        >>> ExtendedContext.max_mag(Decimal('7'), Decimal('-10'))
        Decimal('-10')
        >>> ExtendedContext.max_mag(1, -2)
        Decimal('-2')
        >>> ExtendedContext.max_mag(Decimal(1), -2)
        Decimal('-2')
        >>> ExtendedContext.max_mag(1, Decimal(-2))
        Decimal('-2')
        """
        a = _convert_other(a, raiseit=True)
        return a.max_mag(b, context=self)

    def min(self, a, b):
        """min compares two values numerically and returns the minimum.

        If either operand is a NaN then the general rules apply.
        Otherwise, the operands are compared as though by the compare
        operation.  If they are numerically equal then the left-hand operand
        is chosen as the result.  Otherwise the minimum (closer to negative
        infinity) of the two operands is chosen as the result.

        >>> ExtendedContext.min(Decimal('3'), Decimal('2'))
        Decimal('2')
        >>> ExtendedContext.min(Decimal('-10'), Decimal('3'))
        Decimal('-10')
        >>> ExtendedContext.min(Decimal('1.0'), Decimal('1'))
        Decimal('1.0')
        >>> ExtendedContext.min(Decimal('7'), Decimal('NaN'))
        Decimal('7')
        >>> ExtendedContext.min(1, 2)
        Decimal('1')
        >>> ExtendedContext.min(Decimal(1), 2)
        Decimal('1')
        >>> ExtendedContext.min(1, Decimal(29))
        Decimal('1')
        """
        a = _convert_other(a, raiseit=True)
        return a.min(b, context=self)

    def 绝对值最小(self, a, b):
        """Compares the values numerically with their sign ignored.

        >>> ExtendedContext.min_mag(Decimal('3'), Decimal('-2'))
        Decimal('-2')
        >>> ExtendedContext.min_mag(Decimal('-3'), Decimal('NaN'))
        Decimal('-3')
        >>> ExtendedContext.min_mag(1, -2)
        Decimal('1')
        >>> ExtendedContext.min_mag(Decimal(1), -2)
        Decimal('1')
        >>> ExtendedContext.min_mag(1, Decimal(-2))
        Decimal('1')
        """
        a = _convert_other(a, raiseit=True)
        return a.min_mag(b, context=self)

    def 取负(self, a):
        """Minus corresponds to unary prefix minus in Python.

        The operation is evaluated using the same rules as subtract; the
        operation minus(a) is calculated as subtract('0', a) where the '0'
        has the same exponent as the operand.

        >>> ExtendedContext.minus(Decimal('1.3'))
        Decimal('-1.3')
        >>> ExtendedContext.minus(Decimal('-1.3'))
        Decimal('1.3')
        >>> ExtendedContext.minus(1)
        Decimal('-1')
        """
        a = _convert_other(a, raiseit=True)
        return a.__neg__(context=self)

    def 乘(self, a, b):
        """multiply multiplies two operands.

        If either operand is a special value then the general rules apply.
        Otherwise, the operands are multiplied together
        ('long multiplication'), resulting in a number which may be as long
        as the sum of the lengths of the two operands.

        >>> ExtendedContext.multiply(Decimal('1.20'), Decimal('3'))
        Decimal('3.60')
        >>> ExtendedContext.multiply(Decimal('7'), Decimal('3'))
        Decimal('21')
        >>> ExtendedContext.multiply(Decimal('0.9'), Decimal('0.8'))
        Decimal('0.72')
        >>> ExtendedContext.multiply(Decimal('0.9'), Decimal('-0'))
        Decimal('-0.0')
        >>> ExtendedContext.multiply(Decimal('654321'), Decimal('654321'))
        Decimal('4.28135971E+11')
        >>> ExtendedContext.multiply(7, 7)
        Decimal('49')
        >>> ExtendedContext.multiply(Decimal(7), 7)
        Decimal('49')
        >>> ExtendedContext.multiply(7, Decimal(7))
        Decimal('49')
        """
        a = _convert_other(a, raiseit=True)
        r = a.__mul__(b, context=self)
        if r is NotImplemented:
            raise TypeError('Unable to convert %s to Decimal' % b)
        else:
            return r

    def 下一个更小(self, a):
        """Returns the largest representable number smaller than a.

        >>> c = ExtendedContext.copy()
        >>> c.Emin = -999
        >>> c.Emax = 999
        >>> ExtendedContext.next_minus(Decimal('1'))
        Decimal('0.999999999')
        >>> c.next_minus(Decimal('1E-1007'))
        Decimal('0E-1007')
        >>> ExtendedContext.next_minus(Decimal('-1.00000003'))
        Decimal('-1.00000004')
        >>> c.next_minus(Decimal('Infinity'))
        Decimal('9.99999999E+999')
        >>> c.next_minus(1)
        Decimal('0.999999999')
        """
        a = _convert_other(a, raiseit=True)
        return a.next_minus(context=self)

    def 下一个更大(self, a):
        """Returns the smallest representable number larger than a.

        >>> c = ExtendedContext.copy()
        >>> c.Emin = -999
        >>> c.Emax = 999
        >>> ExtendedContext.next_plus(Decimal('1'))
        Decimal('1.00000001')
        >>> c.next_plus(Decimal('-1E-1007'))
        Decimal('-0E-1007')
        >>> ExtendedContext.next_plus(Decimal('-1.00000003'))
        Decimal('-1.00000002')
        >>> c.next_plus(Decimal('-Infinity'))
        Decimal('-9.99999999E+999')
        >>> c.next_plus(1)
        Decimal('1.00000001')
        """
        a = _convert_other(a, raiseit=True)
        return a.next_plus(context=self)

    def 朝某值下一个(self, a, b):
        """Returns the number closest to a, in direction towards b.

        The result is the closest representable number from the first
        operand (but not the first operand) that is in the direction
        towards the second operand, unless the operands have the same
        value.

        >>> c = ExtendedContext.copy()
        >>> c.Emin = -999
        >>> c.Emax = 999
        >>> c.next_toward(Decimal('1'), Decimal('2'))
        Decimal('1.00000001')
        >>> c.next_toward(Decimal('-1E-1007'), Decimal('1'))
        Decimal('-0E-1007')
        >>> c.next_toward(Decimal('-1.00000003'), Decimal('0'))
        Decimal('-1.00000002')
        >>> c.next_toward(Decimal('1'), Decimal('0'))
        Decimal('0.999999999')
        >>> c.next_toward(Decimal('1E-1007'), Decimal('-100'))
        Decimal('0E-1007')
        >>> c.next_toward(Decimal('-1.00000003'), Decimal('-10'))
        Decimal('-1.00000004')
        >>> c.next_toward(Decimal('0.00'), Decimal('-0.0000'))
        Decimal('-0.00')
        >>> c.next_toward(0, 1)
        Decimal('1E-1007')
        >>> c.next_toward(Decimal(0), 1)
        Decimal('1E-1007')
        >>> c.next_toward(0, Decimal(1))
        Decimal('1E-1007')
        """
        a = _convert_other(a, raiseit=True)
        return a.next_toward(b, context=self)

    def 规范化(self, a):
        """normalize reduces an operand to its simplest form.

        Essentially a plus operation with all trailing zeros removed from the
        result.

        >>> ExtendedContext.normalize(Decimal('2.1'))
        Decimal('2.1')
        >>> ExtendedContext.normalize(Decimal('-2.0'))
        Decimal('-2')
        >>> ExtendedContext.normalize(Decimal('1.200'))
        Decimal('1.2')
        >>> ExtendedContext.normalize(Decimal('-120'))
        Decimal('-1.2E+2')
        >>> ExtendedContext.normalize(Decimal('120.00'))
        Decimal('1.2E+2')
        >>> ExtendedContext.normalize(Decimal('0.00'))
        Decimal('0')
        >>> ExtendedContext.normalize(6)
        Decimal('6')
        """
        a = _convert_other(a, raiseit=True)
        return a.normalize(context=self)

    def 数值类别(self, a):
        """Returns an indication of the class of the operand.

        The class is one of the following strings:
          -sNaN
          -NaN
          -Infinity
          -Normal
          -Subnormal
          -Zero
          +Zero
          +Subnormal
          +Normal
          +Infinity

        >>> c = ExtendedContext.copy()
        >>> c.Emin = -999
        >>> c.Emax = 999
        >>> c.number_class(Decimal('Infinity'))
        '+Infinity'
        >>> c.number_class(Decimal('1E-10'))
        '+Normal'
        >>> c.number_class(Decimal('2.50'))
        '+Normal'
        >>> c.number_class(Decimal('0.1E-999'))
        '+Subnormal'
        >>> c.number_class(Decimal('0'))
        '+Zero'
        >>> c.number_class(Decimal('-0'))
        '-Zero'
        >>> c.number_class(Decimal('-0.1E-999'))
        '-Subnormal'
        >>> c.number_class(Decimal('-1E-10'))
        '-Normal'
        >>> c.number_class(Decimal('-2.50'))
        '-Normal'
        >>> c.number_class(Decimal('-Infinity'))
        '-Infinity'
        >>> c.number_class(Decimal('NaN'))
        'NaN'
        >>> c.number_class(Decimal('-NaN'))
        'NaN'
        >>> c.number_class(Decimal('sNaN'))
        'sNaN'
        >>> c.number_class(123)
        '+Normal'
        """
        a = _convert_other(a, raiseit=True)
        return a.number_class(context=self)

    def 取正(self, a):
        """Plus corresponds to unary prefix plus in Python.

        The operation is evaluated using the same rules as add; the
        operation plus(a) is calculated as add('0', a) where the '0'
        has the same exponent as the operand.

        >>> ExtendedContext.plus(Decimal('1.3'))
        Decimal('1.3')
        >>> ExtendedContext.plus(Decimal('-1.3'))
        Decimal('-1.3')
        >>> ExtendedContext.plus(-1)
        Decimal('-1')
        """
        a = _convert_other(a, raiseit=True)
        return a.__pos__(context=self)

    def 幂(self, a, b, modulo=None):
        """Raises a to the power of b, to modulo if given.

        With two arguments, compute a**b.  If a is negative then b
        must be integral.  The result will be inexact unless b is
        integral and the result is finite and can be expressed exactly
        in 'precision' digits.

        With three arguments, compute (a**b) % modulo.  For the
        three argument form, the following restrictions on the
        arguments hold:

         - all three arguments must be integral
         - b must be nonnegative
         - at least one of a or b must be nonzero
         - modulo must be nonzero and have at most 'precision' digits

        The result of pow(a, b, modulo) is identical to the result
        that would be obtained by computing (a**b) % modulo with
        unbounded precision, but is computed more efficiently.  It is
        always exact.

        >>> c = ExtendedContext.copy()
        >>> c.Emin = -999
        >>> c.Emax = 999
        >>> c.power(Decimal('2'), Decimal('3'))
        Decimal('8')
        >>> c.power(Decimal('-2'), Decimal('3'))
        Decimal('-8')
        >>> c.power(Decimal('2'), Decimal('-3'))
        Decimal('0.125')
        >>> c.power(Decimal('1.7'), Decimal('8'))
        Decimal('69.7575744')
        >>> c.power(Decimal('10'), Decimal('0.301029996'))
        Decimal('2.00000000')
        >>> c.power(Decimal('Infinity'), Decimal('-1'))
        Decimal('0')
        >>> c.power(Decimal('Infinity'), Decimal('0'))
        Decimal('1')
        >>> c.power(Decimal('Infinity'), Decimal('1'))
        Decimal('Infinity')
        >>> c.power(Decimal('-Infinity'), Decimal('-1'))
        Decimal('-0')
        >>> c.power(Decimal('-Infinity'), Decimal('0'))
        Decimal('1')
        >>> c.power(Decimal('-Infinity'), Decimal('1'))
        Decimal('-Infinity')
        >>> c.power(Decimal('-Infinity'), Decimal('2'))
        Decimal('Infinity')
        >>> c.power(Decimal('0'), Decimal('0'))
        Decimal('NaN')

        >>> c.power(Decimal('3'), Decimal('7'), Decimal('16'))
        Decimal('11')
        >>> c.power(Decimal('-3'), Decimal('7'), Decimal('16'))
        Decimal('-11')
        >>> c.power(Decimal('-3'), Decimal('8'), Decimal('16'))
        Decimal('1')
        >>> c.power(Decimal('3'), Decimal('7'), Decimal('-16'))
        Decimal('11')
        >>> c.power(Decimal('23E12345'), Decimal('67E189'), Decimal('123456789'))
        Decimal('11729830')
        >>> c.power(Decimal('-0'), Decimal('17'), Decimal('1729'))
        Decimal('-0')
        >>> c.power(Decimal('-23'), Decimal('0'), Decimal('65537'))
        Decimal('1')
        >>> ExtendedContext.power(7, 7)
        Decimal('823543')
        >>> ExtendedContext.power(Decimal(7), 7)
        Decimal('823543')
        >>> ExtendedContext.power(7, Decimal(7), 2)
        Decimal('1')
        """
        a = _convert_other(a, raiseit=True)
        r = a.__pow__(b, modulo, context=self)
        if r is NotImplemented:
            raise TypeError('Unable to convert %s to Decimal' % b)
        else:
            return r

    def 量化(self, a, b):
        """Returns a value equal to 'a' (rounded), having the exponent of 'b'.

        The coefficient of the result is derived from that of the left-hand
        operand.  It may be rounded using the current rounding setting (if
        the exponent is being increased), multiplied by a positive power of
        ten (if the exponent is being decreased), or is unchanged (if the
        exponent is already equal to that of the right-hand operand).

        Unlike other operations, if the length of the coefficient after the
        quantize operation would be greater than precision then an Invalid
        operation condition is raised.  This guarantees that, unless there
        is an error condition, the exponent of the result of a quantize is
        always equal to that of the right-hand operand.

        Also unlike other operations, quantize will never raise Underflow,
        even if the result is subnormal and inexact.

        >>> ExtendedContext.quantize(Decimal('2.17'), Decimal('0.001'))
        Decimal('2.170')
        >>> ExtendedContext.quantize(Decimal('2.17'), Decimal('0.01'))
        Decimal('2.17')
        >>> ExtendedContext.quantize(Decimal('2.17'), Decimal('0.1'))
        Decimal('2.2')
        >>> ExtendedContext.quantize(Decimal('2.17'), Decimal('1e+0'))
        Decimal('2')
        >>> ExtendedContext.quantize(Decimal('2.17'), Decimal('1e+1'))
        Decimal('0E+1')
        >>> ExtendedContext.quantize(Decimal('-Inf'), Decimal('Infinity'))
        Decimal('-Infinity')
        >>> ExtendedContext.quantize(Decimal('2'), Decimal('Infinity'))
        Decimal('NaN')
        >>> ExtendedContext.quantize(Decimal('-0.1'), Decimal('1'))
        Decimal('-0')
        >>> ExtendedContext.quantize(Decimal('-0'), Decimal('1e+5'))
        Decimal('-0E+5')
        >>> ExtendedContext.quantize(Decimal('+35236450.6'), Decimal('1e-2'))
        Decimal('NaN')
        >>> ExtendedContext.quantize(Decimal('-35236450.6'), Decimal('1e-2'))
        Decimal('NaN')
        >>> ExtendedContext.quantize(Decimal('217'), Decimal('1e-1'))
        Decimal('217.0')
        >>> ExtendedContext.quantize(Decimal('217'), Decimal('1e-0'))
        Decimal('217')
        >>> ExtendedContext.quantize(Decimal('217'), Decimal('1e+1'))
        Decimal('2.2E+2')
        >>> ExtendedContext.quantize(Decimal('217'), Decimal('1e+2'))
        Decimal('2E+2')
        >>> ExtendedContext.quantize(1, 2)
        Decimal('1')
        >>> ExtendedContext.quantize(Decimal(1), 2)
        Decimal('1')
        >>> ExtendedContext.quantize(1, Decimal(2))
        Decimal('1')
        """
        a = _convert_other(a, raiseit=True)
        return a.quantize(b, context=self)

    def 基数(self):
        """Just returns 10, as this is Decimal, :)

        >>> ExtendedContext.radix()
        Decimal('10')
        """
        return 十进制数(10)

    def 余数(self, a, b):
        """Returns the remainder from integer division.

        The result is the residue of the dividend after the operation of
        calculating integer division as described for divide-integer,
        rounded to precision digits if necessary.  The sign of the result,
        if non-zero, is the same as that of the original dividend.

        This operation will fail under the same conditions as integer
        division (that is, if integer division on the same two operands
        would fail, the remainder cannot be calculated).

        >>> ExtendedContext.remainder(Decimal('2.1'), Decimal('3'))
        Decimal('2.1')
        >>> ExtendedContext.remainder(Decimal('10'), Decimal('3'))
        Decimal('1')
        >>> ExtendedContext.remainder(Decimal('-10'), Decimal('3'))
        Decimal('-1')
        >>> ExtendedContext.remainder(Decimal('10.2'), Decimal('1'))
        Decimal('0.2')
        >>> ExtendedContext.remainder(Decimal('10'), Decimal('0.3'))
        Decimal('0.1')
        >>> ExtendedContext.remainder(Decimal('3.6'), Decimal('1.3'))
        Decimal('1.0')
        >>> ExtendedContext.remainder(22, 6)
        Decimal('4')
        >>> ExtendedContext.remainder(Decimal(22), 6)
        Decimal('4')
        >>> ExtendedContext.remainder(22, Decimal(6))
        Decimal('4')
        """
        a = _convert_other(a, raiseit=True)
        r = a.__mod__(b, context=self)
        if r is NotImplemented:
            raise TypeError('Unable to convert %s to Decimal' % b)
        else:
            return r

    def 就近余数(self, a, b):
        """Returns to be "a - b * n", where n is the integer nearest the exact
        value of "x / b" (if two integers are equally near then the even one
        is chosen).  If the result is equal to 0 then its sign will be the
        sign of a.

        This operation will fail under the same conditions as integer
        division (that is, if integer division on the same two operands
        would fail, the remainder cannot be calculated).

        >>> ExtendedContext.remainder_near(Decimal('2.1'), Decimal('3'))
        Decimal('-0.9')
        >>> ExtendedContext.remainder_near(Decimal('10'), Decimal('6'))
        Decimal('-2')
        >>> ExtendedContext.remainder_near(Decimal('10'), Decimal('3'))
        Decimal('1')
        >>> ExtendedContext.remainder_near(Decimal('-10'), Decimal('3'))
        Decimal('-1')
        >>> ExtendedContext.remainder_near(Decimal('10.2'), Decimal('1'))
        Decimal('0.2')
        >>> ExtendedContext.remainder_near(Decimal('10'), Decimal('0.3'))
        Decimal('0.1')
        >>> ExtendedContext.remainder_near(Decimal('3.6'), Decimal('1.3'))
        Decimal('-0.3')
        >>> ExtendedContext.remainder_near(3, 11)
        Decimal('3')
        >>> ExtendedContext.remainder_near(Decimal(3), 11)
        Decimal('3')
        >>> ExtendedContext.remainder_near(3, Decimal(11))
        Decimal('3')
        """
        a = _convert_other(a, raiseit=True)
        return a.remainder_near(b, context=self)

    def 循环移位(self, a, b):
        """Returns a rotated copy of a, b times.

        The coefficient of the result is a rotated copy of the digits in
        the coefficient of the first operand.  The number of places of
        rotation is taken from the absolute value of the second operand,
        with the rotation being to the left if the second operand is
        positive or to the right otherwise.

        >>> ExtendedContext.rotate(Decimal('34'), Decimal('8'))
        Decimal('400000003')
        >>> ExtendedContext.rotate(Decimal('12'), Decimal('9'))
        Decimal('12')
        >>> ExtendedContext.rotate(Decimal('123456789'), Decimal('-2'))
        Decimal('891234567')
        >>> ExtendedContext.rotate(Decimal('123456789'), Decimal('0'))
        Decimal('123456789')
        >>> ExtendedContext.rotate(Decimal('123456789'), Decimal('+2'))
        Decimal('345678912')
        >>> ExtendedContext.rotate(1333333, 1)
        Decimal('13333330')
        >>> ExtendedContext.rotate(Decimal(1333333), 1)
        Decimal('13333330')
        >>> ExtendedContext.rotate(1333333, Decimal(1))
        Decimal('13333330')
        """
        a = _convert_other(a, raiseit=True)
        return a.rotate(b, context=self)

    def 同量级吗(self, a, b):
        """Returns True if the two operands have the same exponent.

        The result is never affected by either the sign or the coefficient
        of either operand.

        >>> ExtendedContext.same_quantum(Decimal('2.17'), Decimal('0.001'))
        False
        >>> ExtendedContext.same_quantum(Decimal('2.17'), Decimal('0.01'))
        True
        >>> ExtendedContext.same_quantum(Decimal('2.17'), Decimal('1'))
        False
        >>> ExtendedContext.same_quantum(Decimal('Inf'), Decimal('-Inf'))
        True
        >>> ExtendedContext.same_quantum(10000, -1)
        True
        >>> ExtendedContext.same_quantum(Decimal(10000), -1)
        True
        >>> ExtendedContext.same_quantum(10000, Decimal(-1))
        True
        """
        a = _convert_other(a, raiseit=True)
        return a.same_quantum(b)

    def 按指数缩放(self, a, b):
        """Returns the first operand after adding the second value its exp.

        >>> ExtendedContext.scaleb(Decimal('7.50'), Decimal('-2'))
        Decimal('0.0750')
        >>> ExtendedContext.scaleb(Decimal('7.50'), Decimal('0'))
        Decimal('7.50')
        >>> ExtendedContext.scaleb(Decimal('7.50'), Decimal('3'))
        Decimal('7.50E+3')
        >>> ExtendedContext.scaleb(1, 4)
        Decimal('1E+4')
        >>> ExtendedContext.scaleb(Decimal(1), 4)
        Decimal('1E+4')
        >>> ExtendedContext.scaleb(1, Decimal(4))
        Decimal('1E+4')
        """
        a = _convert_other(a, raiseit=True)
        return a.scaleb(b, context=self)

    def 移位(self, a, b):
        """Returns a shifted copy of a, b times.

        The coefficient of the result is a shifted copy of the digits
        in the coefficient of the first operand.  The number of places
        to shift is taken from the absolute value of the second operand,
        with the shift being to the left if the second operand is
        positive or to the right otherwise.  Digits shifted into the
        coefficient are zeros.

        >>> ExtendedContext.shift(Decimal('34'), Decimal('8'))
        Decimal('400000000')
        >>> ExtendedContext.shift(Decimal('12'), Decimal('9'))
        Decimal('0')
        >>> ExtendedContext.shift(Decimal('123456789'), Decimal('-2'))
        Decimal('1234567')
        >>> ExtendedContext.shift(Decimal('123456789'), Decimal('0'))
        Decimal('123456789')
        >>> ExtendedContext.shift(Decimal('123456789'), Decimal('+2'))
        Decimal('345678900')
        >>> ExtendedContext.shift(88888888, 2)
        Decimal('888888800')
        >>> ExtendedContext.shift(Decimal(88888888), 2)
        Decimal('888888800')
        >>> ExtendedContext.shift(88888888, Decimal(2))
        Decimal('888888800')
        """
        a = _convert_other(a, raiseit=True)
        return a.shift(b, context=self)

    def 平方根(self, a):
        """Square root of a non-negative number to context precision.

        If the result must be inexact, it is rounded using the
        round-half-even algorithm.

        >>> ExtendedContext.sqrt(Decimal('0'))
        Decimal('0')
        >>> ExtendedContext.sqrt(Decimal('-0'))
        Decimal('-0')
        >>> ExtendedContext.sqrt(Decimal('0.39'))
        Decimal('0.624499800')
        >>> ExtendedContext.sqrt(Decimal('100'))
        Decimal('10')
        >>> ExtendedContext.sqrt(Decimal('1'))
        Decimal('1')
        >>> ExtendedContext.sqrt(Decimal('1.0'))
        Decimal('1.0')
        >>> ExtendedContext.sqrt(Decimal('1.00'))
        Decimal('1.0')
        >>> ExtendedContext.sqrt(Decimal('7'))
        Decimal('2.64575131')
        >>> ExtendedContext.sqrt(Decimal('10'))
        Decimal('3.16227766')
        >>> ExtendedContext.sqrt(2)
        Decimal('1.41421356')
        >>> ExtendedContext.prec
        9
        """
        a = _convert_other(a, raiseit=True)
        return a.sqrt(context=self)

    def 减(self, a, b):
        """Return the difference between the two operands.

        >>> ExtendedContext.subtract(Decimal('1.3'), Decimal('1.07'))
        Decimal('0.23')
        >>> ExtendedContext.subtract(Decimal('1.3'), Decimal('1.30'))
        Decimal('0.00')
        >>> ExtendedContext.subtract(Decimal('1.3'), Decimal('2.07'))
        Decimal('-0.77')
        >>> ExtendedContext.subtract(8, 5)
        Decimal('3')
        >>> ExtendedContext.subtract(Decimal(8), 5)
        Decimal('3')
        >>> ExtendedContext.subtract(8, Decimal(5))
        Decimal('3')
        """
        a = _convert_other(a, raiseit=True)
        r = a.__sub__(b, context=self)
        if r is NotImplemented:
            raise TypeError('Unable to convert %s to Decimal' % b)
        else:
            return r

    def 转工程字符串(self, a):
        """Convert to a string, using engineering notation if an exponent is needed.

        Engineering notation has an exponent which is a multiple of 3.  This
        can leave up to 3 digits to the left of the decimal place and may
        require the addition of either one or two trailing zeros.

        The operation is not affected by the context.

        >>> ExtendedContext.to_eng_string(Decimal('123E+1'))
        '1.23E+3'
        >>> ExtendedContext.to_eng_string(Decimal('123E+3'))
        '123E+3'
        >>> ExtendedContext.to_eng_string(Decimal('123E-10'))
        '12.3E-9'
        >>> ExtendedContext.to_eng_string(Decimal('-123E-12'))
        '-123E-12'
        >>> ExtendedContext.to_eng_string(Decimal('7E-7'))
        '700E-9'
        >>> ExtendedContext.to_eng_string(Decimal('7E+1'))
        '70'
        >>> ExtendedContext.to_eng_string(Decimal('0E+1'))
        '0.00E+3'

        """
        a = _convert_other(a, raiseit=True)
        return a.to_eng_string(context=self)

    def 转科学串(self, a):
        """Converts a number to a string, using scientific notation.

        The operation is not affected by the context.
        """
        a = _convert_other(a, raiseit=True)
        return a.__str__(context=self)

    def 精确取整(self, a):
        """Rounds to an integer.

        When the operand has a negative exponent, the result is the same
        as using the quantize() operation using the given operand as the
        left-hand-operand, 1E+0 as the right-hand-operand, and the precision
        of the operand as the precision setting; Inexact and Rounded flags
        are allowed in this operation.  The rounding mode is taken from the
        context.

        >>> ExtendedContext.to_integral_exact(Decimal('2.1'))
        Decimal('2')
        >>> ExtendedContext.to_integral_exact(Decimal('100'))
        Decimal('100')
        >>> ExtendedContext.to_integral_exact(Decimal('100.0'))
        Decimal('100')
        >>> ExtendedContext.to_integral_exact(Decimal('101.5'))
        Decimal('102')
        >>> ExtendedContext.to_integral_exact(Decimal('-101.5'))
        Decimal('-102')
        >>> ExtendedContext.to_integral_exact(Decimal('10E+5'))
        Decimal('1.0E+6')
        >>> ExtendedContext.to_integral_exact(Decimal('7.89E+77'))
        Decimal('7.89E+77')
        >>> ExtendedContext.to_integral_exact(Decimal('-Inf'))
        Decimal('-Infinity')
        """
        a = _convert_other(a, raiseit=True)
        return a.to_integral_exact(context=self)

    def 取整数值(self, a):
        """Rounds to an integer.

        When the operand has a negative exponent, the result is the same
        as using the quantize() operation using the given operand as the
        left-hand-operand, 1E+0 as the right-hand-operand, and the precision
        of the operand as the precision setting, except that no flags will
        be set.  The rounding mode is taken from the context.

        >>> ExtendedContext.to_integral_value(Decimal('2.1'))
        Decimal('2')
        >>> ExtendedContext.to_integral_value(Decimal('100'))
        Decimal('100')
        >>> ExtendedContext.to_integral_value(Decimal('100.0'))
        Decimal('100')
        >>> ExtendedContext.to_integral_value(Decimal('101.5'))
        Decimal('102')
        >>> ExtendedContext.to_integral_value(Decimal('-101.5'))
        Decimal('-102')
        >>> ExtendedContext.to_integral_value(Decimal('10E+5'))
        Decimal('1.0E+6')
        >>> ExtendedContext.to_integral_value(Decimal('7.89E+77'))
        Decimal('7.89E+77')
        >>> ExtendedContext.to_integral_value(Decimal('-Inf'))
        Decimal('-Infinity')
        """
        a = _convert_other(a, raiseit=True)
        return a.to_integral_value(context=self)
    to_integral = 取整数值
_装类转发(十进制上下文, {'Etiny': '指数理论下限', 'Etop': '指数上限', 'canonical': '取规范形', 'clear_flags': '清标志', 'clear_traps': '清陷阱', 'compare': '比较', 'compare_signal': '带信号比较', 'compare_total': '全序比较', 'compare_total_mag': '全序绝对值比较', 'copy_abs': '复制绝对值', 'copy_decimal': '复制十进制数', 'copy_negate': '复制相反数', 'copy_sign': '复制符号', 'create_decimal': '造十进制数', 'create_decimal_from_float': '从浮点造十进制数', 'divide': '除', 'divide_int': '整除', 'exp': '指数', 'fma': '乘加', 'is_canonical': '是规范形吗', 'is_finite': '是有限吗', 'is_infinite': '是无穷吗', 'is_nan': '是NaN吗', 'is_normal': '是正规数吗', 'is_qnan': '是安静NaN吗', 'is_signed': '带符号吗', 'is_snan': '是信号NaN吗', 'is_subnormal': '是次正规吗', 'is_zero': '是零吗', 'ln': '自然对数', 'log10': '常用对数', 'logb': '指数对数', 'logical_and': '逻辑与', 'logical_invert': '逻辑非', 'logical_or': '逻辑或', 'logical_xor': '逻辑异或', 'max_mag': '绝对值最大', 'min_mag': '绝对值最小', 'minus': '取负', 'multiply': '乘', 'next_minus': '下一个更小', 'next_plus': '下一个更大', 'next_toward': '朝某值下一个', 'normalize': '规范化', 'number_class': '数值类别', 'plus': '取正', 'power': '幂', 'quantize': '量化', 'radix': '基数', 'remainder': '余数', 'remainder_near': '就近余数', 'rotate': '循环移位', 'same_quantum': '同量级吗', 'scaleb': '按指数缩放', 'shift': '移位', 'sqrt': '平方根', 'subtract': '减', 'to_eng_string': '转工程字符串', 'to_integral_exact': '精确取整', 'to_integral_value': '取整数值', 'to_sci_string': '转科学串'}, {'Etiny': '指数理论下限', 'Etop': '指数上限', 'canonical': '取规范形', 'clear_flags': '清标志', 'clear_traps': '清陷阱', 'compare': '比较', 'compare_signal': '带信号比较', 'compare_total': '全序比较', 'compare_total_mag': '全序绝对值比较', 'copy_abs': '复制绝对值', 'copy_decimal': '复制十进制数', 'copy_negate': '复制相反数', 'copy_sign': '复制符号', 'create_decimal': '造十进制数', 'create_decimal_from_float': '从浮点造十进制数', 'divide': '除', 'divide_int': '整除', 'exp': '指数', 'fma': '乘加', 'is_canonical': '是规范形吗', 'is_finite': '是有限吗', 'is_infinite': '是无穷吗', 'is_nan': '是NaN吗', 'is_normal': '是正规数吗', 'is_qnan': '是安静NaN吗', 'is_signed': '带符号吗', 'is_snan': '是信号NaN吗', 'is_subnormal': '是次正规吗', 'is_zero': '是零吗', 'ln': '自然对数', 'log10': '常用对数', 'logb': '指数对数', 'logical_and': '逻辑与', 'logical_invert': '逻辑非', 'logical_or': '逻辑或', 'logical_xor': '逻辑异或', 'max_mag': '绝对值最大', 'min_mag': '绝对值最小', 'minus': '取负', 'multiply': '乘', 'next_minus': '下一个更小', 'next_plus': '下一个更大', 'next_toward': '朝某值下一个', 'normalize': '规范化', 'number_class': '数值类别', 'plus': '取正', 'power': '幂', 'quantize': '量化', 'radix': '基数', 'remainder': '余数', 'remainder_near': '就近余数', 'rotate': '循环移位', 'same_quantum': '同量级吗', 'scaleb': '按指数缩放', 'shift': '移位', 'sqrt': '平方根', 'subtract': '减', 'to_eng_string': '转工程字符串', 'to_integral_exact': '精确取整', 'to_integral_value': '取整数值', 'to_sci_string': '转科学串'})

class _WorkRep(object):
    __slots__ = ('sign', 'int', 'exp')

    def __init__(self, value=None):
        if value is None:
            self.sign = None
            self.int = 0
            self.指数 = None
        elif isinstance(value, 十进制数):
            self.sign = value._sign
            self.int = int(value._int)
            self.指数 = value._exp
        else:
            self.sign = value[0]
            self.int = value[1]
            self.指数 = value[2]

    def __repr__(self):
        return '(%r, %r, %r)' % (self.sign, self.int, self.指数)
_装类转发(_WorkRep, {}, {'exp': '指数'})

def _normalize(op1, op2, prec=0):
    """Normalizes op1, op2 to have the same exp and length of coefficient.

    Done during addition.
    """
    if op1.exp < op2.exp:
        tmp = op2
        other = op1
    else:
        tmp = op1
        other = op2
    tmp_len = len(str(tmp.int))
    other_len = len(str(other.int))
    指数 = tmp.exp + min(-1, tmp_len - prec - 2)
    if other_len + other.exp - 1 < 指数:
        other.int = 1
        other.exp = 指数
    tmp.int *= 10 ** (tmp.exp - other.exp)
    tmp.exp = other.exp
    return (op1, op2)
_nbits = int.bit_length

def _decimal_lshift_exact(n, e):
    """ Given integers n and e, return n * 10**e if it's an integer, else None.

    The computation is designed to avoid computing large powers of 10
    unnecessarily.

    >>> _decimal_lshift_exact(3, 4)
    30000
    >>> _decimal_lshift_exact(300, -999999999)  # returns None

    """
    if n == 0:
        return 0
    elif e >= 0:
        return n * 10 ** e
    else:
        str_n = str(abs(n))
        val_n = len(str_n) - len(str_n.rstrip('0'))
        return None if val_n < -e else n // 10 ** (-e)

def _sqrt_nearest(n, a):
    """Closest integer to the square root of the positive integer n.  a is
    an initial approximation to the square root.  Any positive integer
    will do for a, but the closer a is to the square root of n the
    faster convergence will be.

    """
    if n <= 0 or a <= 0:
        raise ValueError('Both arguments to _sqrt_nearest should be positive.')
    b = 0
    while a != b:
        b, a = (a, a - -n // a >> 1)
    return a

def _rshift_nearest(x, shift):
    """Given an integer x and a nonnegative integer shift, return closest
    integer to x / 2**shift; use round-to-even in case of a tie.

    """
    b, q = (1 << shift, x >> shift)
    return q + (2 * (x & b - 1) + (q & 1) > b)

def _div_nearest(a, b):
    """Closest integer to a/b, a and b positive integers; rounds to even
    in the case of a tie.

    """
    q, r = divmod(a, b)
    return q + (2 * r + (q & 1) > b)

def _ilog(x, M, L=8):
    """Integer approximation to M*log(x/M), with absolute error boundable
    in terms only of x/M.

    Given positive integers x and M, return an integer approximation to
    M * log(x/M).  For L = 8 and 0.1 <= x/M <= 10 the difference
    between the approximation and the exact result is at most 22.  For
    L = 8 and 1.0 <= x/M <= 10.0 the difference is at most 15.  In
    both cases these are upper bounds on the error; it will usually be
    much smaller."""
    y = x - M
    R = 0
    while R <= L and abs(y) << L - R >= M or (R > L and abs(y) >> R - L >= M):
        y = _div_nearest(M * y << 1, M + _sqrt_nearest(M * (M + _rshift_nearest(y, R)), M))
        R += 1
    T = -int(-10 * len(str(M)) // (3 * L))
    yshift = _rshift_nearest(y, R)
    w = _div_nearest(M, T)
    for k in range(T - 1, 0, -1):
        w = _div_nearest(M, k) - _div_nearest(yshift * w, M)
    return _div_nearest(w * y, M)

def _dlog10(c, e, p):
    """Given integers c, e and p with c > 0, p >= 0, compute an integer
    approximation to 10**p * log10(c*10**e), with an absolute error of
    at most 1.  Assumes that c*10**e is not exactly 1."""
    p += 2
    l = len(str(c))
    f = e + l - (e + l >= 1)
    if p > 0:
        M = 10 ** p
        k = e + p - f
        if k >= 0:
            c *= 10 ** k
        else:
            c = _div_nearest(c, 10 ** (-k))
        log_d = _ilog(c, M)
        log_10 = _log10_digits(p)
        log_d = _div_nearest(log_d * M, log_10)
        log_tenpower = f * M
    else:
        log_d = 0
        log_tenpower = _div_nearest(f, 10 ** (-p))
    return _div_nearest(log_tenpower + log_d, 100)

def _dlog(c, e, p):
    """Given integers c, e and p with c > 0, compute an integer
    approximation to 10**p * log(c*10**e), with an absolute error of
    at most 1.  Assumes that c*10**e is not exactly 1."""
    p += 2
    l = len(str(c))
    f = e + l - (e + l >= 1)
    if p > 0:
        k = e + p - f
        if k >= 0:
            c *= 10 ** k
        else:
            c = _div_nearest(c, 10 ** (-k))
        log_d = _ilog(c, 10 ** p)
    else:
        log_d = 0
    if f:
        extra = len(str(abs(f))) - 1
        if p + extra >= 0:
            f_log_ten = _div_nearest(f * _log10_digits(p + extra), 10 ** extra)
        else:
            f_log_ten = 0
    else:
        f_log_ten = 0
    return _div_nearest(f_log_ten + log_d, 100)

class _Log10Memoize(object):
    """Class to compute, store, and allow retrieval of, digits of the
    constant log(10) = 2.302585....  This constant is needed by
    Decimal.ln, Decimal.log10, Decimal.exp and Decimal.__pow__."""

    def __init__(self):
        self.digits = '23025850929940456840179914546843642076011014886'

    def getdigits(self, p):
        """Given an integer p >= 0, return floor(10**p)*log(10).

        For example, self.getdigits(3) returns 2302.
        """
        if p < 0:
            raise ValueError('p should be nonnegative')
        if p >= len(self.digits):
            extra = 3
            while True:
                M = 10 ** (p + extra + 2)
                digits = str(_div_nearest(_ilog(10 * M, M), 100))
                if digits[-extra:] != '0' * extra:
                    break
                extra += 3
            self.digits = digits.rstrip('0')[:-1]
        return int(self.digits[:p + 1])
_log10_digits = _Log10Memoize().getdigits

def _iexp(x, M, L=8):
    """Given integers x and M, M > 0, such that x/M is small in absolute
    value, compute an integer approximation to M*exp(x/M).  For 0 <=
    x/M <= 2.4, the absolute error in the result is bounded by 60 (and
    is usually much smaller)."""
    R = _nbits((x << L) // M)
    T = -int(-10 * len(str(M)) // (3 * L))
    y = _div_nearest(x, T)
    Mshift = M << R
    for i in range(T - 1, 0, -1):
        y = _div_nearest(x * (Mshift + y), Mshift * i)
    for k in range(R - 1, -1, -1):
        Mshift = M << k + 2
        y = _div_nearest(y * (y + Mshift), Mshift)
    return M + y

def _dexp(c, e, p):
    """Compute an approximation to exp(c*10**e), with p decimal places of
    precision.

    Returns integers d, f such that:

      10**(p-1) <= d <= 10**p, and
      (d-1)*10**f < exp(c*10**e) < (d+1)*10**f

    In other words, d*10**f is an approximation to exp(c*10**e) with p
    digits of precision, and with an error in d of at most 1.  This is
    almost, but not quite, the same as the error being < 1ulp: when d
    = 10**(p-1) the error could be up to 10 ulp."""
    p += 2
    extra = max(0, e + len(str(c)) - 1)
    q = p + extra
    移位 = e + q
    if 移位 >= 0:
        cshift = c * 10 ** 移位
    else:
        cshift = c // 10 ** (-移位)
    quot, rem = divmod(cshift, _log10_digits(q))
    rem = _div_nearest(rem, 10 ** extra)
    return (_div_nearest(_iexp(rem, 10 ** p), 1000), quot - p + 3)

def _dpower(xc, xe, yc, ye, p):
    """Given integers xc, xe, yc and ye representing Decimals x = xc*10**xe and
    y = yc*10**ye, compute x**y.  Returns a pair of integers (c, e) such that:

      10**(p-1) <= c <= 10**p, and
      (c-1)*10**e < x**y < (c+1)*10**e

    in other words, c*10**e is an approximation to x**y with p digits
    of precision, and with an error in c of at most 1.  (This is
    almost, but not quite, the same as the error being < 1ulp: when c
    == 10**(p-1) we can only guarantee error < 10ulp.)

    We assume that: x is positive and not equal to 1, and y is nonzero.
    """
    b = len(str(abs(yc))) + ye
    lxc = _dlog(xc, xe, p + b + 1)
    移位 = ye - b
    if 移位 >= 0:
        pc = lxc * yc * 10 ** 移位
    else:
        pc = _div_nearest(lxc * yc, 10 ** (-移位))
    if pc == 0:
        if (len(str(xc)) + xe >= 1) == (yc > 0):
            coeff, 指数 = (10 ** (p - 1) + 1, 1 - p)
        else:
            coeff, 指数 = (10 ** p - 1, -p)
    else:
        coeff, 指数 = _dexp(pc, -(p + 1), p + 1)
        coeff = _div_nearest(coeff, 10)
        指数 += 1
    return (coeff, 指数)

def _log10_lb(c, correction={'1': 100, '2': 70, '3': 53, '4': 40, '5': 31, '6': 23, '7': 16, '8': 10, '9': 5}):
    """Compute a lower bound for 100*log10(c) for a positive integer c."""
    if c <= 0:
        raise ValueError('The argument to _log10_lb should be nonnegative.')
    str_c = str(c)
    return 100 * len(str_c) - correction[str_c[0]]

def _convert_other(other, raiseit=False, allow_float=False):
    """Convert other to Decimal.

    Verifies that it's ok to use in an implicit construction.
    If allow_float is true, allow conversion from float;  this
    is used in the comparison methods (__eq__ and friends).

    """
    if isinstance(other, 十进制数):
        return other
    if isinstance(other, int):
        return 十进制数(other)
    if allow_float and isinstance(other, float):
        return 十进制数.从浮点数(other)
    if raiseit:
        raise TypeError('Unable to convert %s to Decimal' % other)
    return NotImplemented

def _convert_for_comparison(self, other, equality_op=False):
    """Given a Decimal instance self and a Python object other, return
    a pair (s, o) of Decimal instances such that "s op o" is
    equivalent to "self op other" for any of the 6 comparison
    operators "op".

    """
    if isinstance(other, 十进制数):
        return (self, other)
    if isinstance(other, _numbers.Rational):
        if not self._is_special:
            self = _dec_from_triple(self._sign, str(int(self._int) * other.denominator), self._exp)
        return (self, 十进制数(other.numerator))
    if equality_op and isinstance(other, _numbers.Complex) and (other.imag == 0):
        other = other.real
    if isinstance(other, float):
        context = 取上下文()
        if equality_op:
            context.flags[浮点混用] = 1
        else:
            context._raise_error(浮点混用, 'strict semantics for mixing floats and Decimals are enabled')
        return (self, 十进制数.从浮点数(other))
    return (NotImplemented, NotImplemented)
默认上下文 = 十进制上下文(prec=28, rounding=银行家舍入, traps=[除零, 上溢, 无效运算], flags=[], Emax=999999, Emin=-999999, capitals=1, clamp=0)
基本上下文 = 十进制上下文(prec=9, rounding=四舍五入, traps=[除零, 上溢, 无效运算, 被钳位, 下溢], flags=[])
扩展上下文 = 十进制上下文(prec=9, rounding=银行家舍入, traps=[], flags=[])
import re
_parser = re.compile('        # A numeric string consists of:\n#    \\s*\n    (?P<sign>[-+])?              # an optional sign, followed by either...\n    (\n        (?=\\d|\\.\\d)              # ...a number (with at least one digit)\n        (?P<int>\\d*)             # having a (possibly empty) integer part\n        (\\.(?P<frac>\\d*))?       # followed by an optional fractional part\n        (E(?P<exp>[-+]?\\d+))?    # followed by an optional exponent, or...\n    |\n        Inf(inity)?              # ...an infinity, or...\n    |\n        (?P<signal>s)?           # ...an (optionally signaling)\n        NaN                      # NaN\n        (?P<diag>\\d*)            # with (possibly empty) diagnostic info.\n    )\n#    \\s*\n    \\z\n', re.VERBOSE | re.IGNORECASE).match
_all_zeros = re.compile('0*$').match
_exact_half = re.compile('50*$').match
_parse_format_specifier_regex = re.compile('\\A\n(?:\n   (?P<fill>.)?\n   (?P<align>[<>=^])\n)?\n(?P<sign>[-+ ])?\n(?P<no_neg_0>z)?\n(?P<alt>\\#)?\n(?P<zeropad>0)?\n(?P<minimumwidth>\\d+)?\n(?P<thousands_sep>[,_])?\n(?:\\.\n    (?=[\\d,_])  # lookahead for digit or separator\n    (?P<precision>\\d+)?\n    (?P<frac_separators>[,_])?\n)?\n(?P<type>[eEfFgGn%])?\n\\z\n', re.VERBOSE | re.DOTALL)
del re
try:
    import locale as _locale
except ImportError:
    pass

def _parse_format_specifier(format_spec, _localeconv=None):
    """Parse and validate a format specifier.

    Turns a standard numeric format specifier into a dict, with the
    following entries:

      fill: fill character to pad field to minimum width
      align: alignment type, either '<', '>', '=' or '^'
      sign: either '+', '-' or ' '
      minimumwidth: nonnegative integer giving minimum width
      zeropad: boolean, indicating whether to pad with zeros
      thousands_sep: string to use as thousands separator, or ''
      grouping: grouping for thousands separators, in format
        used by localeconv
      decimal_point: string to use for decimal point
      precision: nonnegative integer giving precision, or None
      type: one of the characters 'eEfFgG%', or None

    """
    m = _parse_format_specifier_regex.match(format_spec)
    if m is None:
        raise ValueError('Invalid format specifier: ' + format_spec)
    format_dict = m.groupdict()
    fill = format_dict['fill']
    align = format_dict['align']
    format_dict['zeropad'] = format_dict['zeropad'] is not None
    if format_dict['zeropad']:
        if fill is not None:
            raise ValueError("Fill character conflicts with '0' in format specifier: " + format_spec)
        if align is not None:
            raise ValueError("Alignment conflicts with '0' in format specifier: " + format_spec)
    format_dict['fill'] = fill or ' '
    format_dict['align'] = align or '>'
    if format_dict['sign'] is None:
        format_dict['sign'] = '-'
    format_dict['minimumwidth'] = int(format_dict['minimumwidth'] or '0')
    if format_dict['precision'] is not None:
        format_dict['precision'] = int(format_dict['precision'])
    if format_dict['precision'] == 0:
        if format_dict['type'] is None or format_dict['type'] in 'gGn':
            format_dict['precision'] = 1
    if format_dict['type'] == 'n':
        format_dict['type'] = 'g'
        if _localeconv is None:
            _localeconv = _locale.localeconv()
        if format_dict['thousands_sep'] is not None:
            raise ValueError("Explicit thousands separator conflicts with 'n' type in format specifier: " + format_spec)
        format_dict['thousands_sep'] = _localeconv['thousands_sep']
        format_dict['grouping'] = _localeconv['grouping']
        format_dict['decimal_point'] = _localeconv['decimal_point']
    else:
        if format_dict['thousands_sep'] is None:
            format_dict['thousands_sep'] = ''
        format_dict['grouping'] = [3, 0]
        format_dict['decimal_point'] = '.'
    if format_dict['frac_separators'] is None:
        format_dict['frac_separators'] = ''
    return format_dict

def _format_align(sign, body, spec):
    """Given an unpadded, non-aligned numeric string 'body' and sign
    string 'sign', add padding and alignment conforming to the given
    format specifier dictionary 'spec' (as produced by
    parse_format_specifier).

    """
    minimumwidth = spec['minimumwidth']
    fill = spec['fill']
    padding = fill * (minimumwidth - len(sign) - len(body))
    align = spec['align']
    if align == '<':
        result = sign + body + padding
    elif align == '>':
        result = padding + sign + body
    elif align == '=':
        result = sign + padding + body
    elif align == '^':
        half = len(padding) // 2
        result = padding[:half] + sign + body + padding[half:]
    else:
        raise ValueError('Unrecognised alignment field')
    return result

def _group_lengths(grouping):
    """Convert a localeconv-style grouping into a (possibly infinite)
    iterable of integers representing group lengths.

    """
    from itertools import chain, repeat
    if not grouping:
        return []
    elif grouping[-1] == 0 and len(grouping) >= 2:
        return chain(grouping[:-1], repeat(grouping[-2]))
    elif grouping[-1] == _locale.CHAR_MAX:
        return grouping[:-1]
    else:
        raise ValueError('unrecognised format for grouping')

def _insert_thousands_sep(digits, spec, min_width=1):
    """Insert thousands separators into a digit string.

    spec is a dictionary whose keys should include 'thousands_sep' and
    'grouping'; typically it's the result of parsing the format
    specifier using _parse_format_specifier.

    The min_width keyword argument gives the minimum length of the
    result, which will be padded on the left with zeros if necessary.

    If necessary, the zero padding adds an extra '0' on the left to
    avoid a leading thousands separator.  For example, inserting
    commas every three digits in '123456', with min_width=8, gives
    '0,123,456', even though that has length 9.

    """
    sep = spec['thousands_sep']
    grouping = spec['grouping']
    groups = []
    for l in _group_lengths(grouping):
        if l <= 0:
            raise ValueError('group length should be positive')
        l = min(max(len(digits), min_width, 1), l)
        groups.append('0' * (l - len(digits)) + digits[-l:])
        digits = digits[:-l]
        min_width -= l
        if not digits and min_width <= 0:
            break
        min_width -= len(sep)
    else:
        l = max(len(digits), min_width, 1)
        groups.append('0' * (l - len(digits)) + digits[-l:])
    return sep.join(reversed(groups))

def _format_sign(is_negative, spec):
    """Determine sign character."""
    if is_negative:
        return '-'
    elif spec['sign'] in ' +':
        return spec['sign']
    else:
        return ''

def _format_number(is_negative, intpart, fracpart, exp, spec):
    """Format a number, given the following data:

    is_negative: true if the number is negative, else false
    intpart: string of digits that must appear before the decimal point
    fracpart: string of digits that must come after the point
    exp: exponent, as an integer
    spec: dictionary resulting from parsing the format specifier

    This function uses the information in spec to:
      insert separators (decimal separator and thousands separators)
      format the sign
      format the exponent
      add trailing '%' for the '%' type
      zero-pad if necessary
      fill and align if necessary
    """
    sign = _format_sign(is_negative, spec)
    frac_sep = spec['frac_separators']
    if fracpart and frac_sep:
        fracpart = frac_sep.join((fracpart[pos:pos + 3] for pos in range(0, len(fracpart), 3)))
    if fracpart or spec['alt']:
        fracpart = spec['decimal_point'] + fracpart
    if exp != 0 or spec['type'] in 'eE':
        echar = {'E': 'E', 'e': 'e', 'G': 'E', 'g': 'e'}[spec['type']]
        fracpart += '{0}{1:+}'.format(echar, exp)
    if spec['type'] == '%':
        fracpart += '%'
    if spec['zeropad']:
        min_width = spec['minimumwidth'] - len(fracpart) - len(sign)
    else:
        min_width = 0
    intpart = _insert_thousands_sep(intpart, spec, min_width)
    return _format_align(sign, intpart + fracpart, spec)
_Infinity = 十进制数('Inf')
_NegativeInfinity = 十进制数('-Inf')
_NaN = 十进制数('NaN')
_Zero = 十进制数(0)
_One = 十进制数(1)
_NegativeOne = 十进制数(-1)
_SignedInfinity = (_Infinity, _NegativeInfinity)
_PyHASH_MODULUS = sys.hash_info.modulus
_PyHASH_INF = sys.hash_info.inf
_PyHASH_NAN = sys.hash_info.nan
_PyHASH_10INV = pow(10, _PyHASH_MODULUS - 2, _PyHASH_MODULUS)
del sys


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BasicContext': '基本上下文',
    'Clamped': '被钳位',
    'Context': '十进制上下文',
    'ConversionSyntax': '转换语法错误',
    'Decimal': '十进制数',
    'DecimalException': '十进制错误',
    'DecimalTuple': '十进制元组',
    'DefaultContext': '默认上下文',
    'DivisionByZero': '除零',
    'DivisionImpossible': '除不尽',
    'DivisionUndefined': '除法未定义',
    'ExtendedContext': '扩展上下文',
    'FloatOperation': '浮点混用',
    'HAVE_CONTEXTVAR': '有上下文变量',
    'HAVE_THREADS': '有线程支持',
    'IEEEContext': 'IEEE上下文',
    'IEEE_CONTEXT_MAX_BITS': 'IEEE上下文最大位数',
    'Inexact': '不精确',
    'InvalidContext': '无效上下文',
    'InvalidOperation': '无效运算',
    'MAX_EMAX': '最大指数上限',
    'MAX_PREC': '最大精度',
    'MIN_EMIN': '最小指数下限',
    'MIN_ETINY': '最小指数理论下限',
    'Overflow': '上溢',
    'ROUND_05UP': '零五上舍入',
    'ROUND_CEILING': '向上取整',
    'ROUND_DOWN': '向下舍入',
    'ROUND_FLOOR': '向下取整',
    'ROUND_HALF_DOWN': '半下舍入',
    'ROUND_HALF_EVEN': '银行家舍入',
    'ROUND_HALF_UP': '四舍五入',
    'ROUND_UP': '向上舍入',
    'Rounded': '已舍入',
    'Subnormal': '次正规',
    'Underflow': '下溢',
    'getcontext': '取上下文',
    'localcontext': '本地上下文',
    'setcontext': '设上下文',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '十进制上下文': {
        'Etiny': '指数理论下限',
        'Etop': '指数上限',
        'canonical': '取规范形',
        'clear_flags': '清标志',
        'clear_traps': '清陷阱',
        'compare': '比较',
        'compare_signal': '带信号比较',
        'compare_total': '全序比较',
        'compare_total_mag': '全序绝对值比较',
        'copy_abs': '复制绝对值',
        'copy_decimal': '复制十进制数',
        'copy_negate': '复制相反数',
        'copy_sign': '复制符号',
        'create_decimal': '造十进制数',
        'create_decimal_from_float': '从浮点造十进制数',
        'divide': '除',
        'divide_int': '整除',
        'exp': '指数',
        'fma': '乘加',
        'is_canonical': '是规范形吗',
        'is_finite': '是有限吗',
        'is_infinite': '是无穷吗',
        'is_nan': '是NaN吗',
        'is_normal': '是正规数吗',
        'is_qnan': '是安静NaN吗',
        'is_signed': '带符号吗',
        'is_snan': '是信号NaN吗',
        'is_subnormal': '是次正规吗',
        'is_zero': '是零吗',
        'ln': '自然对数',
        'log10': '常用对数',
        'logb': '指数对数',
        'logical_and': '逻辑与',
        'logical_invert': '逻辑非',
        'logical_or': '逻辑或',
        'logical_xor': '逻辑异或',
        'max_mag': '绝对值最大',
        'min_mag': '绝对值最小',
        'minus': '取负',
        'multiply': '乘',
        'next_minus': '下一个更小',
        'next_plus': '下一个更大',
        'next_toward': '朝某值下一个',
        'normalize': '规范化',
        'number_class': '数值类别',
        'plus': '取正',
        'power': '幂',
        'quantize': '量化',
        'radix': '基数',
        'remainder': '余数',
        'remainder_near': '就近余数',
        'rotate': '循环移位',
        'same_quantum': '同量级吗',
        'scaleb': '按指数缩放',
        'shift': '移位',
        'sqrt': '平方根',
        'subtract': '减',
        'to_eng_string': '转工程字符串',
        'to_integral_exact': '精确取整',
        'to_integral_value': '取整数值',
        'to_sci_string': '转科学串',
    },
    '十进制数': {
        'adjusted': '调整指数',
        'as_integer_ratio': '转整数比',
        'as_tuple': '转元组',
        'canonical': '取规范形',
        'compare': '比较',
        'compare_signal': '带信号比较',
        'compare_total': '全序比较',
        'compare_total_mag': '全序绝对值比较',
        'conjugate': '共轭',
        'copy_abs': '复制绝对值',
        'copy_negate': '复制相反数',
        'copy_sign': '复制符号',
        'exp': '指数',
        'fma': '乘加',
        'from_float': '从浮点数',
        'from_number': '从数值',
        'imag': '虚部',
        'is_canonical': '是规范形吗',
        'is_finite': '是有限吗',
        'is_infinite': '是无穷吗',
        'is_nan': '是NaN吗',
        'is_normal': '是正规数吗',
        'is_qnan': '是安静NaN吗',
        'is_signed': '带符号吗',
        'is_snan': '是信号NaN吗',
        'is_subnormal': '是次正规吗',
        'is_zero': '是零吗',
        'ln': '自然对数',
        'log10': '常用对数',
        'logb': '指数对数',
        'logical_and': '逻辑与',
        'logical_invert': '逻辑非',
        'logical_or': '逻辑或',
        'logical_xor': '逻辑异或',
        'max_mag': '绝对值最大',
        'min_mag': '绝对值最小',
        'next_minus': '下一个更小',
        'next_plus': '下一个更大',
        'next_toward': '朝某值下一个',
        'normalize': '规范化',
        'number_class': '数值类别',
        'quantize': '量化',
        'radix': '基数',
        'real': '实部',
        'remainder_near': '就近余数',
        'rotate': '循环移位',
        'same_quantum': '同量级吗',
        'scaleb': '按指数缩放',
        'shift': '移位',
        'sqrt': '平方根',
        'to_eng_string': '转工程字符串',
        'to_integral_exact': '精确取整',
        'to_integral_value': '取整数值',
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
    '_WorkRep': {
        'exp': '指数',
    },
    '十进制上下文': {
        'Etiny': '指数理论下限',
        'Etop': '指数上限',
        'canonical': '取规范形',
        'clear_flags': '清标志',
        'clear_traps': '清陷阱',
        'compare': '比较',
        'compare_signal': '带信号比较',
        'compare_total': '全序比较',
        'compare_total_mag': '全序绝对值比较',
        'copy_abs': '复制绝对值',
        'copy_decimal': '复制十进制数',
        'copy_negate': '复制相反数',
        'copy_sign': '复制符号',
        'create_decimal': '造十进制数',
        'create_decimal_from_float': '从浮点造十进制数',
        'divide': '除',
        'divide_int': '整除',
        'exp': '指数',
        'fma': '乘加',
        'is_canonical': '是规范形吗',
        'is_finite': '是有限吗',
        'is_infinite': '是无穷吗',
        'is_nan': '是NaN吗',
        'is_normal': '是正规数吗',
        'is_qnan': '是安静NaN吗',
        'is_signed': '带符号吗',
        'is_snan': '是信号NaN吗',
        'is_subnormal': '是次正规吗',
        'is_zero': '是零吗',
        'ln': '自然对数',
        'log10': '常用对数',
        'logb': '指数对数',
        'logical_and': '逻辑与',
        'logical_invert': '逻辑非',
        'logical_or': '逻辑或',
        'logical_xor': '逻辑异或',
        'max_mag': '绝对值最大',
        'min_mag': '绝对值最小',
        'minus': '取负',
        'multiply': '乘',
        'next_minus': '下一个更小',
        'next_plus': '下一个更大',
        'next_toward': '朝某值下一个',
        'normalize': '规范化',
        'number_class': '数值类别',
        'plus': '取正',
        'power': '幂',
        'quantize': '量化',
        'radix': '基数',
        'remainder': '余数',
        'remainder_near': '就近余数',
        'rotate': '循环移位',
        'same_quantum': '同量级吗',
        'scaleb': '按指数缩放',
        'shift': '移位',
        'sqrt': '平方根',
        'subtract': '减',
        'to_eng_string': '转工程字符串',
        'to_integral_exact': '精确取整',
        'to_integral_value': '取整数值',
        'to_sci_string': '转科学串',
    },
    '十进制数': {
        'adjusted': '调整指数',
        'as_integer_ratio': '转整数比',
        'as_tuple': '转元组',
        'canonical': '取规范形',
        'compare': '比较',
        'compare_signal': '带信号比较',
        'compare_total': '全序比较',
        'compare_total_mag': '全序绝对值比较',
        'conjugate': '共轭',
        'copy_abs': '复制绝对值',
        'copy_negate': '复制相反数',
        'copy_sign': '复制符号',
        'exp': '指数',
        'fma': '乘加',
        'from_float': '从浮点数',
        'from_number': '从数值',
        'imag': '虚部',
        'is_canonical': '是规范形吗',
        'is_finite': '是有限吗',
        'is_infinite': '是无穷吗',
        'is_nan': '是NaN吗',
        'is_normal': '是正规数吗',
        'is_qnan': '是安静NaN吗',
        'is_signed': '带符号吗',
        'is_snan': '是信号NaN吗',
        'is_subnormal': '是次正规吗',
        'is_zero': '是零吗',
        'ln': '自然对数',
        'log10': '常用对数',
        'logb': '指数对数',
        'logical_and': '逻辑与',
        'logical_invert': '逻辑非',
        'logical_or': '逻辑或',
        'logical_xor': '逻辑异或',
        'max_mag': '绝对值最大',
        'min_mag': '绝对值最小',
        'next_minus': '下一个更小',
        'next_plus': '下一个更大',
        'next_toward': '朝某值下一个',
        'normalize': '规范化',
        'number_class': '数值类别',
        'quantize': '量化',
        'radix': '基数',
        'real': '实部',
        'remainder_near': '就近余数',
        'rotate': '循环移位',
        'same_quantum': '同量级吗',
        'scaleb': '按指数缩放',
        'shift': '移位',
        'sqrt': '平方根',
        'to_eng_string': '转工程字符串',
        'to_integral_exact': '精确取整',
        'to_integral_value': '取整数值',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'IEEE上下文',
    'IEEE上下文最大位数',
    '上溢',
    '下溢',
    '不精确',
    '十进制上下文',
    '十进制元组',
    '十进制数',
    '十进制错误',
    '半下舍入',
    '取上下文',
    '向上取整',
    '向上舍入',
    '向下取整',
    '向下舍入',
    '四舍五入',
    '基本上下文',
    '已舍入',
    '扩展上下文',
    '无效上下文',
    '无效运算',
    '最大指数上限',
    '最大精度',
    '最小指数下限',
    '最小指数理论下限',
    '有上下文变量',
    '有线程支持',
    '本地上下文',
    '次正规',
    '浮点混用',
    '被钳位',
    '设上下文',
    '转换语法错误',
    '银行家舍入',
    '除不尽',
    '除法未定义',
    '除零',
    '零五上舍入',
    '默认上下文',
]

# ---- 转发层结束 ----
