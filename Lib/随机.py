# -*- coding: utf-8 -*-
"""随机 —— 汉语库（由 tools/汉化库.py 从 Lib/random.py 机械生成，**不要手改**）。

英文库 Lib/random.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 随机
"""


"""Random variable generators.

    bytes
    -----
           uniform bytes (values between 0 and 255)

    integers
    --------
           uniform within range

    sequences
    ---------
           pick random element
           pick random sample
           pick weighted random sample
           generate random permutation

    distributions on the real line:
    ------------------------------
           uniform
           triangular
           normal (Gaussian)
           lognormal
           negative exponential
           gamma
           beta
           pareto
           Weibull

    distributions on the circle (angles 0 to 2pi)
    ---------------------------------------------
           circular uniform
           von Mises

    discrete distributions
    ----------------------
           binomial


General notes on the underlying Mersenne Twister core generator:

* The period is 2**19937-1.
* It is one of the most extensively tested generators in existence.
* The random() method is implemented in C, executes in a single Python step,
  and is, therefore, threadsafe.

"""
_英文原名表 = {'Random': '随机数生成器', 'SystemRandom': '系统随机数生成器', 'betavariate': '贝塔分布', 'binomialvariate': '二项分布', 'choice': '选择', 'choices': '加权抽样', 'expovariate': '指数分布', 'gauss': '高斯分布', 'getstate': '取状态', 'lognormvariate': '对数正态分布', 'normalvariate': '正态分布', 'paretovariate': '帕累托分布', 'randbytes': '随机字节', 'randint': '随机整数', 'randrange': '随机范围', 'sample': '抽样', 'seed': '设种子', 'setstate': '设状态', 'shuffle': '洗牌', 'triangular': '三角分布', 'uniform': '均匀分布', 'vonmisesvariate': '冯米塞斯分布', 'weibullvariate': '威布尔分布'}

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
from math import log as _log, exp as _exp, pi as _pi, e as _e, ceil as _ceil
from math import sqrt as _sqrt, acos as _acos, cos as _cos, sin as _sin
from math import tau as TWOPI, floor as _floor, isfinite as _isfinite
from math import lgamma as _lgamma, fabs as _fabs, log2 as _log2
from os import urandom as _urandom
from _collections_abc import Sequence as _Sequence
from operator import index as _index
from itertools import accumulate as _accumulate, repeat as _repeat
from bisect import bisect as _bisect
import os as _os
import _random
__all__ = ['Random', 'SystemRandom', 'betavariate', 'binomialvariate', 'choice', 'choices', 'expovariate', 'gammavariate', 'gauss', 'getrandbits', 'getstate', 'lognormvariate', 'normalvariate', 'paretovariate', 'randbytes', 'randint', 'random', 'randrange', 'sample', 'seed', 'setstate', 'shuffle', 'triangular', 'uniform', 'vonmisesvariate', 'weibullvariate']
NV_MAGICCONST = 4 * _exp(-0.5) / _sqrt(2.0)
LOG4 = _log(4.0)
SG_MAGICCONST = 1.0 + _log(4.5)
BPF = 53
RECIP_BPF = 2 ** (-BPF)
_ONE = 1
_sha512 = None

class 随机数生成器(_random.Random):
    """Random number generator base class used by bound module functions.

    Used to instantiate instances of Random to get generators that don't
    share state.

    Class Random can also be subclassed if you want to use a different basic
    generator of your own devising: in that case, override the following
    methods:  random(), seed(), getstate(), and setstate().
    Optionally, implement a getrandbits() method so that randrange()
    can cover arbitrarily large ranges.

    """
    版本 = 3

    def __init__(self, x=None):
        """Initialize an instance.

        Optional argument x controls seeding, as for Random.seed().
        """
        self.设种子(x)
        self.gauss_next = None

    def 设种子(self, a=None, version=2):
        """Initialize internal state from a seed.

        The only supported seed types are None, int, float,
        str, bytes, and bytearray.

        None or no argument seeds from current time or from an operating
        system specific randomness source if available.

        If *a* is an int, all bits are used.

        For version 2 (the default), all of the bits are used if *a* is a str,
        bytes, or bytearray.  For version 1 (provided for reproducing random
        sequences from older versions of Python), the algorithm for str and
        bytes generates a narrower range of seeds.

        """
        if version == 1 and isinstance(a, (str, bytes)):
            a = a.decode('latin-1') if isinstance(a, bytes) else a
            x = ord(a[0]) << 7 if a else 0
            for c in map(ord, a):
                x = (1000003 * x ^ c) & 18446744073709551615
            x ^= len(a)
            a = -2 if x == -1 else x
        elif version == 2 and isinstance(a, (str, bytes, bytearray)):
            global _sha512
            if _sha512 is None:
                try:
                    from _sha2 import sha512 as _sha512
                except ImportError:
                    from hashlib import sha512 as _sha512
            if isinstance(a, str):
                a = a.encode()
            a = int.from_bytes(a + _sha512(a).digest())
        elif not isinstance(a, (type(None), int, float, str, bytes, bytearray)):
            raise TypeError('The only supported seed types are:\nNone, int, float, str, bytes, and bytearray.')
        super().seed(a)
        self.gauss_next = None

    def 取状态(self):
        """Return internal state; can be passed to setstate() later."""
        return (self.版本, super().getstate(), self.gauss_next)

    def 设状态(self, state):
        """Restore internal state from object returned by getstate()."""
        version = state[0]
        if version == 3:
            version, internalstate, self.gauss_next = state
            super().setstate(internalstate)
        elif version == 2:
            version, internalstate, self.gauss_next = state
            try:
                internalstate = tuple((x % 2 ** 32 for x in internalstate))
            except ValueError as e:
                raise TypeError from e
            super().setstate(internalstate)
        else:
            raise ValueError('state with version %s passed to Random.setstate() of version %s' % (version, self.版本))

    def __getstate__(self):
        return self.取状态()

    def __setstate__(self, state):
        self.设状态(state)

    def __reduce__(self):
        return (self.__class__, (), self.取状态())

    def __init_subclass__(cls, /, **kwargs):
        """Control how subclasses generate random integers.

        The algorithm a subclass can use depends on the random() and/or
        getrandbits() implementation available to it and determines
        whether it can generate random integers from arbitrarily large
        ranges.
        """
        for c in cls.__mro__:
            if '_randbelow' in c.__dict__:
                break
            if 'getrandbits' in c.__dict__:
                cls._randbelow = cls._randbelow_with_getrandbits
                break
            if 'random' in c.__dict__:
                cls._randbelow = cls._randbelow_without_getrandbits
                break

    def _randbelow_with_getrandbits(self, n):
        """Return a random int in the range [0,n).  Defined for n > 0."""
        k = n.bit_length()
        r = self.getrandbits(k)
        while r >= n:
            r = self.getrandbits(k)
        return r

    def _randbelow_without_getrandbits(self, n, maxsize=1 << BPF):
        """Return a random int in the range [0,n).  Defined for n > 0.

        The implementation does not use getrandbits, but only random.
        """
        random = self.random
        if n >= maxsize:
            from warnings import warn
            warn('Underlying random() generator does not supply \nenough bits to choose from a population range this large.\nTo remove the range limitation, add a getrandbits() method.')
            return _floor(random() * n)
        rem = maxsize % n
        limit = (maxsize - rem) / maxsize
        r = random()
        while r >= limit:
            r = random()
        return _floor(r * maxsize) % n
    _randbelow = _randbelow_with_getrandbits

    def 随机字节(self, n):
        """Generate n random bytes."""
        return self.getrandbits(n * 8).to_bytes(n, 'little')

    def 随机范围(self, start, stop=None, step=_ONE):
        """Choose a random item from range(stop) or range(start, stop[, step]).

        Roughly equivalent to ``choice(range(start, stop, step))`` but
        supports arbitrarily large ranges and is optimized for common cases.

        """
        istart = _index(start)
        if stop is None:
            if step is not _ONE:
                raise TypeError('Missing a non-None stop argument')
            if istart > 0:
                return self._randbelow(istart)
            raise ValueError('empty range for randrange()')
        istop = _index(stop)
        width = istop - istart
        istep = _index(step)
        if istep == 1:
            if width > 0:
                return istart + self._randbelow(width)
            raise ValueError(f'empty range in randrange({start}, {stop})')
        if istep > 0:
            n = (width + istep - 1) // istep
        elif istep < 0:
            n = (width + istep + 1) // istep
        else:
            raise ValueError('zero step for randrange()')
        if n <= 0:
            raise ValueError(f'empty range in randrange({start}, {stop}, {step})')
        return istart + istep * self._randbelow(n)

    def 随机整数(self, a, b):
        """Return random integer in range [a, b], including both end points.
        """
        a = _index(a)
        b = _index(b)
        if b < a:
            raise ValueError(f'empty range in randint({a}, {b})')
        return a + self._randbelow(b - a + 1)

    def 选择(self, seq):
        """Choose a random element from a non-empty sequence."""
        if not len(seq):
            raise IndexError('Cannot choose from an empty sequence')
        return seq[self._randbelow(len(seq))]

    def 洗牌(self, x):
        """Shuffle list x in place, and return None."""
        randbelow = self._randbelow
        for i in reversed(range(1, len(x))):
            j = randbelow(i + 1)
            x[i], x[j] = (x[j], x[i])

    def 抽样(self, population, k, *, counts=None):
        """Chooses k unique random elements from a population sequence.

        Returns a new list containing elements from the population while
        leaving the original population unchanged.  The resulting list is
        in selection order so that all sub-slices will also be valid random
        samples.  This allows raffle winners (the sample) to be partitioned
        into grand prize and second place winners (the subslices).

        Members of the population need not be hashable or unique.  If the
        population contains repeats, then each occurrence is a possible
        selection in the sample.

        Repeated elements can be specified one at a time or with the optional
        counts parameter.  For example:

            sample(['red', 'blue'], counts=[4, 2], k=5)

        is equivalent to:

            sample(['red', 'red', 'red', 'red', 'blue', 'blue'], k=5)

        To choose a sample from a range of integers, use range() for the
        population argument.  This is especially fast and space efficient
        for sampling from a large population:

            sample(range(10000000), 60)

        """
        if not isinstance(population, _Sequence):
            raise TypeError('Population must be a sequence.  For dicts or sets, use sorted(d).')
        n = len(population)
        if counts is not None:
            cum_counts = list(_accumulate(counts))
            if len(cum_counts) != n:
                raise ValueError('The number of counts does not match the population')
            total = cum_counts.pop() if cum_counts else 0
            if not isinstance(total, int):
                raise TypeError('Counts must be integers')
            if total < 0:
                raise ValueError('Counts must be non-negative')
            selections = self.抽样(range(total), k=k)
            bisect = _bisect
            return [population[bisect(cum_counts, s)] for s in selections]
        randbelow = self._randbelow
        if not 0 <= k <= n:
            raise ValueError('Sample larger than population or is negative')
        result = [None] * k
        setsize = 21
        if k > 5:
            setsize += 4 ** _ceil(_log(k * 3, 4))
        if n <= setsize:
            pool = list(population)
            for i in range(k):
                j = randbelow(n - i)
                result[i] = pool[j]
                pool[j] = pool[n - i - 1]
        else:
            selected = set()
            selected_add = selected.add
            for i in range(k):
                j = randbelow(n)
                while j in selected:
                    j = randbelow(n)
                selected_add(j)
                result[i] = population[j]
        return result

    def 加权抽样(self, population, weights=None, *, cum_weights=None, k=1):
        """Return a k sized list of population elements chosen with replacement.

        If the relative weights or cumulative weights are not specified,
        the selections are made with equal probability.

        """
        random = self.random
        n = len(population)
        if cum_weights is None:
            if weights is None:
                floor = _floor
                n += 0.0
                return [population[floor(random() * n)] for i in _repeat(None, k)]
            try:
                cum_weights = list(_accumulate(weights))
            except TypeError:
                if not isinstance(weights, int):
                    raise
                k = weights
                raise TypeError(f'The number of choices must be a keyword argument: k={k!r}') from None
        elif weights is not None:
            raise TypeError('Cannot specify both weights and cumulative weights')
        if len(cum_weights) != n:
            raise ValueError('The number of weights does not match the population')
        total = cum_weights[-1] + 0.0
        if total <= 0.0:
            raise ValueError('Total of weights must be greater than zero')
        if not _isfinite(total):
            raise ValueError('Total of weights must be finite')
        bisect = _bisect
        hi = n - 1
        return [population[bisect(cum_weights, random() * total, 0, hi)] for i in _repeat(None, k)]

    def 均匀分布(self, a, b):
        """Get a random number in the range [a, b) or [a, b] depending on rounding.

        The mean (expected value) and variance of the random variable are:

            E[X] = (a + b) / 2
            Var[X] = (b - a) ** 2 / 12

        """
        return a + (b - a) * self.random()

    def 三角分布(self, low=0.0, high=1.0, mode=None):
        """Triangular distribution.

        Continuous distribution bounded by given lower and upper limits,
        and having a given mode value in-between.

        http://en.wikipedia.org/wiki/Triangular_distribution

        The mean (expected value) and variance of the random variable are:

            E[X] = (low + high + mode) / 3
            Var[X] = (low**2 + high**2 + mode**2 - low*high - low*mode - high*mode) / 18

        """
        u = self.random()
        try:
            c = 0.5 if mode is None else (mode - low) / (high - low)
        except ZeroDivisionError:
            return low
        if u > c:
            u = 1.0 - u
            c = 1.0 - c
            low, high = (high, low)
        return low + (high - low) * _sqrt(u * c)

    def 正态分布(self, mu=0.0, sigma=1.0):
        """Normal distribution.

        mu is the mean, and sigma is the standard deviation.

        """
        random = self.random
        while True:
            u1 = random()
            u2 = 1.0 - random()
            z = NV_MAGICCONST * (u1 - 0.5) / u2
            zz = z * z / 4.0
            if zz <= -_log(u2):
                break
        return mu + z * sigma

    def 高斯分布(self, mu=0.0, sigma=1.0):
        """Gaussian distribution.

        mu is the mean, and sigma is the standard deviation.  This is
        slightly faster than the normalvariate() function.

        Not thread-safe without a lock around calls.

        """
        random = self.random
        z = self.gauss_next
        self.gauss_next = None
        if z is None:
            x2pi = random() * TWOPI
            g2rad = _sqrt(-2.0 * _log(1.0 - random()))
            z = _cos(x2pi) * g2rad
            self.gauss_next = _sin(x2pi) * g2rad
        return mu + z * sigma

    def 对数正态分布(self, mu, sigma):
        """Log normal distribution.

        If you take the natural logarithm of this distribution, you'll get a
        normal distribution with mean mu and standard deviation sigma.
        mu can have any value, and sigma must be greater than zero.

        """
        return _exp(self.正态分布(mu, sigma))

    def 指数分布(self, lambd=1.0):
        """Exponential distribution.

        lambd is 1.0 divided by the desired mean.  It should be
        nonzero.  (The parameter would be called "lambda", but that is
        a reserved word in Python.)  Returned values range from 0 to
        positive infinity if lambd is positive, and from negative
        infinity to 0 if lambd is negative.

        The mean (expected value) and variance of the random variable are:

            E[X] = 1 / lambd
            Var[X] = 1 / lambd ** 2

        """
        return -_log(1.0 - self.random()) / lambd

    def 冯米塞斯分布(self, mu, kappa):
        """Circular data distribution.

        mu is the mean angle, expressed in radians between 0 and 2*pi, and
        kappa is the concentration parameter, which must be greater than or
        equal to zero.  If kappa is equal to zero, this distribution reduces
        to a uniform random angle over the range 0 to 2*pi.

        """
        random = self.random
        if kappa <= 1e-06:
            return TWOPI * random()
        s = 0.5 / kappa
        r = s + _sqrt(1.0 + s * s)
        while True:
            u1 = random()
            z = _cos(_pi * u1)
            d = z / (r + z)
            u2 = random()
            if u2 < 1.0 - d * d or u2 <= (1.0 - d) * _exp(d):
                break
        q = 1.0 / r
        f = (q + z) / (1.0 + q * z)
        u3 = random()
        if u3 > 0.5:
            theta = (mu + _acos(f)) % TWOPI
        else:
            theta = (mu - _acos(f)) % TWOPI
        return theta

    def gammavariate(self, alpha, beta):
        """Gamma distribution.  Not the gamma function!

        Conditions on the parameters are alpha > 0 and beta > 0.

        The probability distribution function is:

                    x ** (alpha - 1) * math.exp(-x / beta)
          pdf(x) =  --------------------------------------
                      math.gamma(alpha) * beta ** alpha

        The mean (expected value) and variance of the random variable are:

            E[X] = alpha * beta
            Var[X] = alpha * beta ** 2

        """
        if alpha <= 0.0 or beta <= 0.0:
            raise ValueError('gammavariate: alpha and beta must be > 0.0')
        random = self.random
        if alpha > 1.0:
            ainv = _sqrt(2.0 * alpha - 1.0)
            bbb = alpha - LOG4
            ccc = alpha + ainv
            while True:
                u1 = random()
                if not 1e-07 < u1 < 0.9999999:
                    continue
                u2 = 1.0 - random()
                v = _log(u1 / (1.0 - u1)) / ainv
                x = alpha * _exp(v)
                z = u1 * u1 * u2
                r = bbb + ccc * v - x
                if r + SG_MAGICCONST - 4.5 * z >= 0.0 or r >= _log(z):
                    return x * beta
        elif alpha == 1.0:
            return -_log(1.0 - random()) * beta
        else:
            while True:
                u = random()
                b = (_e + alpha) / _e
                p = b * u
                if p <= 1.0:
                    x = p ** (1.0 / alpha)
                else:
                    x = -_log((b - p) / alpha)
                u1 = random()
                if p > 1.0:
                    if u1 <= x ** (alpha - 1.0):
                        break
                elif u1 <= _exp(-x):
                    break
            return x * beta

    def 贝塔分布(self, alpha, beta):
        """Beta distribution.

        Conditions on the parameters are alpha > 0 and beta > 0.
        Returned values range between 0 and 1.

        The mean (expected value) and variance of the random variable are:

            E[X] = alpha / (alpha + beta)
            Var[X] = alpha * beta / ((alpha + beta)**2 * (alpha + beta + 1))

        """
        y = self.gammavariate(alpha, 1.0)
        if y:
            return y / (y + self.gammavariate(beta, 1.0))
        return 0.0

    def 帕累托分布(self, alpha):
        """Pareto distribution.  alpha is the shape parameter."""
        u = 1.0 - self.random()
        return u ** (-1.0 / alpha)

    def 威布尔分布(self, alpha, beta):
        """Weibull distribution.

        alpha is the scale parameter and beta is the shape parameter.

        """
        u = 1.0 - self.random()
        return alpha * (-_log(u)) ** (1.0 / beta)

    def 二项分布(self, n=1, p=0.5):
        """Binomial random variable.

        Gives the number of successes for *n* independent trials
        with the probability of success in each trial being *p*:

            sum(random() < p for i in range(n))

        Returns an integer in the range:

            0 <= X <= n

        The integer is chosen with the probability:

            P(X == k) = math.comb(n, k) * p ** k * (1 - p) ** (n - k)

        The mean (expected value) and variance of the random variable are:

            E[X] = n * p
            Var[X] = n * p * (1 - p)

        """
        if n < 0:
            raise ValueError('n must be non-negative')
        if p <= 0.0 or p >= 1.0:
            if p == 0.0:
                return 0
            if p == 1.0:
                return n
            raise ValueError('p must be in the range 0.0 <= p <= 1.0')
        random = self.random
        if n == 1:
            return _index(random() < p)
        if p > 0.5:
            return n - self.二项分布(n, 1.0 - p)
        if n * p < 10.0:
            x = y = 0
            c = _log2(1.0 - p)
            if not c:
                return x
            while True:
                try:
                    y += _floor(_log2(random()) / c) + 1
                except ValueError:
                    continue
                if y > n:
                    return x
                x += 1
        assert n * p >= 10.0 and p <= 0.5
        setup_complete = False
        spq = _sqrt(n * p * (1.0 - p))
        b = 1.15 + 2.53 * spq
        a = -0.0873 + 0.0248 * b + 0.01 * p
        c = n * p + 0.5
        vr = 0.92 - 4.2 / b
        while True:
            u = random()
            u -= 0.5
            us = 0.5 - _fabs(u)
            try:
                k = _floor((2.0 * a / us + b) * u + c)
            except ZeroDivisionError:
                continue
            if k < 0 or k > n:
                continue
            v = random()
            if us >= 0.07 and v <= vr:
                return k
            if not setup_complete:
                alpha = (2.83 + 5.1 / b) * spq
                lpq = _log(p / (1.0 - p))
                m = _floor((n + 1) * p)
                h = _lgamma(m + 1) + _lgamma(n - m + 1)
                setup_complete = True
            v *= alpha / (a / (us * us) + b)
            if _log(v) <= h - _lgamma(k + 1) - _lgamma(n - k + 1) + (k - m) * lpq:
                return k
_装类转发(随机数生成器, {'VERSION': '版本', 'betavariate': '贝塔分布', 'binomialvariate': '二项分布', 'choice': '选择', 'choices': '加权抽样', 'expovariate': '指数分布', 'gauss': '高斯分布', 'getstate': '取状态', 'lognormvariate': '对数正态分布', 'normalvariate': '正态分布', 'paretovariate': '帕累托分布', 'randbytes': '随机字节', 'randint': '随机整数', 'randrange': '随机范围', 'sample': '抽样', 'seed': '设种子', 'setstate': '设状态', 'shuffle': '洗牌', 'triangular': '三角分布', 'uniform': '均匀分布', 'vonmisesvariate': '冯米塞斯分布', 'weibullvariate': '威布尔分布'}, {'VERSION': '版本', 'betavariate': '贝塔分布', 'binomialvariate': '二项分布', 'choice': '选择', 'choices': '加权抽样', 'expovariate': '指数分布', 'gauss': '高斯分布', 'getstate': '取状态', 'lognormvariate': '对数正态分布', 'normalvariate': '正态分布', 'paretovariate': '帕累托分布', 'randbytes': '随机字节', 'randint': '随机整数', 'randrange': '随机范围', 'sample': '抽样', 'seed': '设种子', 'setstate': '设状态', 'shuffle': '洗牌', 'triangular': '三角分布', 'uniform': '均匀分布', 'vonmisesvariate': '冯米塞斯分布', 'weibullvariate': '威布尔分布'})

class 系统随机数生成器(随机数生成器):
    """Alternate random number generator using sources provided
    by the operating system (such as /dev/urandom on Unix or
    CryptGenRandom on Windows).

     Not available on all systems (see os.urandom() for details).

    """

    def random(self):
        """Get the next random number in the range 0.0 <= X < 1.0."""
        return (int.from_bytes(_urandom(7)) >> 3) * RECIP_BPF

    def getrandbits(self, k):
        """getrandbits(k) -> x.  Generates an int with k random bits."""
        if k < 0:
            raise ValueError('number of bits must be non-negative')
        numbytes = (k + 7) // 8
        x = int.from_bytes(_urandom(numbytes))
        return x >> numbytes * 8 - k

    def 随机字节(self, n):
        """Generate n random bytes."""
        return _urandom(n)

    def 设种子(self, *args, **kwds):
        """Stub method.  Not used for a system random number generator."""
        return None

    def _notimplemented(self, *args, **kwds):
        """Method should not be called for a system random number generator."""
        raise NotImplementedError('System entropy source does not have state.')
    取状态 = 设状态 = _notimplemented
_装类转发(系统随机数生成器, {'getstate': '取状态', 'randbytes': '随机字节', 'seed': '设种子', 'setstate': '设状态'}, {'getstate': '取状态', 'randbytes': '随机字节', 'seed': '设种子', 'setstate': '设状态'})
_inst = 随机数生成器()
设种子 = _inst.seed
random = _inst.random
均匀分布 = _inst.uniform
三角分布 = _inst.triangular
随机整数 = _inst.randint
选择 = _inst.choice
随机范围 = _inst.randrange
抽样 = _inst.sample
洗牌 = _inst.shuffle
加权抽样 = _inst.choices
正态分布 = _inst.normalvariate
对数正态分布 = _inst.lognormvariate
指数分布 = _inst.expovariate
冯米塞斯分布 = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
高斯分布 = _inst.gauss
贝塔分布 = _inst.betavariate
二项分布 = _inst.binomialvariate
帕累托分布 = _inst.paretovariate
威布尔分布 = _inst.weibullvariate
取状态 = _inst.getstate
设状态 = _inst.setstate
getrandbits = _inst.getrandbits
随机字节 = _inst.randbytes

def _test_generator(n, func, args):
    from statistics import stdev, fmean as mean
    from time import perf_counter
    t0 = perf_counter()
    data = [func(*args) for i in _repeat(None, n)]
    t1 = perf_counter()
    xbar = mean(data)
    sigma = stdev(data, xbar)
    low = min(data)
    high = max(data)
    print(f'{t1 - t0:.3f} sec, {n} times {func.__name__}{args!r}')
    print('avg %g, stddev %g, min %g, max %g\n' % (xbar, sigma, low, high))

def _test(N=10000):
    _test_generator(N, random, ())
    _test_generator(N, 正态分布, (0.0, 1.0))
    _test_generator(N, 对数正态分布, (0.0, 1.0))
    _test_generator(N, 冯米塞斯分布, (0.0, 1.0))
    _test_generator(N, 二项分布, (15, 0.6))
    _test_generator(N, 二项分布, (100, 0.75))
    _test_generator(N, gammavariate, (0.01, 1.0))
    _test_generator(N, gammavariate, (0.1, 1.0))
    _test_generator(N, gammavariate, (0.1, 2.0))
    _test_generator(N, gammavariate, (0.5, 1.0))
    _test_generator(N, gammavariate, (0.9, 1.0))
    _test_generator(N, gammavariate, (1.0, 1.0))
    _test_generator(N, gammavariate, (2.0, 1.0))
    _test_generator(N, gammavariate, (20.0, 1.0))
    _test_generator(N, gammavariate, (200.0, 1.0))
    _test_generator(N, 高斯分布, (0.0, 1.0))
    _test_generator(N, 贝塔分布, (3.0, 3.0))
    _test_generator(N, 三角分布, (0.0, 1.0, 1.0 / 3.0))
if hasattr(_os, 'fork'):
    _os.register_at_fork(after_in_child=_inst.seed)

def _parse_args(arg_list: list[str] | None):
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, color=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--choice', nargs='+', help='print a random choice')
    group.add_argument('-i', '--integer', type=int, metavar='N', help='print a random integer between 1 and N inclusive')
    group.add_argument('-f', '--float', type=float, metavar='N', help='print a random floating-point number between 0 and N inclusive')
    group.add_argument('--test', type=int, const=10000, nargs='?', help=argparse.SUPPRESS)
    parser.add_argument('input', nargs='*', help='if no options given, output depends on the input\n    string or multiple: same as --choice\n    integer: same as --integer\n    float: same as --float')
    args = parser.parse_args(arg_list)
    return (args, parser.format_help())

def main(arg_list: list[str] | None=None) -> int | str:
    args, help_text = _parse_args(arg_list)
    if args.choice:
        return 选择(args.choice)
    if args.integer is not None:
        return 随机整数(1, args.integer)
    if args.float is not None:
        return 均匀分布(0, args.float)
    if args.test:
        _test(args.test)
        return ''
    if len(args.input) == 1:
        val = args.input[0]
        try:
            val = int(val)
            return 随机整数(1, val)
        except ValueError:
            try:
                val = float(val)
                return 均匀分布(0, val)
            except ValueError:
                return 选择(val.split())
    if len(args.input) >= 2:
        return 选择(args.input)
    return help_text
if __name__ == '__main__':
    print(main())


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Random': '随机数生成器',
    'SystemRandom': '系统随机数生成器',
    'betavariate': '贝塔分布',
    'binomialvariate': '二项分布',
    'choice': '选择',
    'choices': '加权抽样',
    'expovariate': '指数分布',
    'gauss': '高斯分布',
    'getstate': '取状态',
    'lognormvariate': '对数正态分布',
    'normalvariate': '正态分布',
    'paretovariate': '帕累托分布',
    'randbytes': '随机字节',
    'randint': '随机整数',
    'randrange': '随机范围',
    'sample': '抽样',
    'seed': '设种子',
    'setstate': '设状态',
    'shuffle': '洗牌',
    'triangular': '三角分布',
    'uniform': '均匀分布',
    'vonmisesvariate': '冯米塞斯分布',
    'weibullvariate': '威布尔分布',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '系统随机数生成器': {
        'getstate': '取状态',
        'randbytes': '随机字节',
        'seed': '设种子',
        'setstate': '设状态',
    },
    '随机数生成器': {
        'VERSION': '版本',
        'betavariate': '贝塔分布',
        'binomialvariate': '二项分布',
        'choice': '选择',
        'choices': '加权抽样',
        'expovariate': '指数分布',
        'gauss': '高斯分布',
        'getstate': '取状态',
        'lognormvariate': '对数正态分布',
        'normalvariate': '正态分布',
        'paretovariate': '帕累托分布',
        'randbytes': '随机字节',
        'randint': '随机整数',
        'randrange': '随机范围',
        'sample': '抽样',
        'seed': '设种子',
        'setstate': '设状态',
        'shuffle': '洗牌',
        'triangular': '三角分布',
        'uniform': '均匀分布',
        'vonmisesvariate': '冯米塞斯分布',
        'weibullvariate': '威布尔分布',
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
    '系统随机数生成器': {
        'getstate': '取状态',
        'randbytes': '随机字节',
        'seed': '设种子',
        'setstate': '设状态',
    },
    '随机数生成器': {
        'VERSION': '版本',
        'betavariate': '贝塔分布',
        'binomialvariate': '二项分布',
        'choice': '选择',
        'choices': '加权抽样',
        'expovariate': '指数分布',
        'gauss': '高斯分布',
        'getstate': '取状态',
        'lognormvariate': '对数正态分布',
        'normalvariate': '正态分布',
        'paretovariate': '帕累托分布',
        'randbytes': '随机字节',
        'randint': '随机整数',
        'randrange': '随机范围',
        'sample': '抽样',
        'seed': '设种子',
        'setstate': '设状态',
        'shuffle': '洗牌',
        'triangular': '三角分布',
        'uniform': '均匀分布',
        'vonmisesvariate': '冯米塞斯分布',
        'weibullvariate': '威布尔分布',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '三角分布',
    '二项分布',
    '冯米塞斯分布',
    '加权抽样',
    '取状态',
    '均匀分布',
    '威布尔分布',
    '对数正态分布',
    '帕累托分布',
    '抽样',
    '指数分布',
    '正态分布',
    '洗牌',
    '系统随机数生成器',
    '设状态',
    '设种子',
    '贝塔分布',
    '选择',
    '随机字节',
    '随机数生成器',
    '随机整数',
    '随机范围',
    '高斯分布',
]

# ---- 转发层结束 ----
