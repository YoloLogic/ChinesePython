# -*- coding: utf-8 -*-
"""统计 —— 汉语库（由 tools/汉化库.py 从 Lib/statistics.py 机械生成，**不要手改**）。

英文库 Lib/statistics.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 统计
"""


"""
Basic statistics module.

This module provides functions for calculating statistics of data, including
averages, variance, and standard deviation.

Calculating averages
--------------------

==================  ==================================================
Function            Description
==================  ==================================================
mean                Arithmetic mean (average) of data.
fmean               Fast, floating-point arithmetic mean.
geometric_mean      Geometric mean of data.
harmonic_mean       Harmonic mean of data.
median              Median (middle value) of data.
median_low          Low median of data.
median_high         High median of data.
median_grouped      Median, or 50th percentile, of grouped data.
mode                Mode (most common value) of data.
multimode           List of modes (most common values of data).
quantiles           Divide data into intervals with equal probability.
==================  ==================================================

Calculate the arithmetic mean ("the average") of data:

>>> mean([-1.0, 2.5, 3.25, 5.75])
2.625


Calculate the standard median of discrete data:

>>> median([2, 3, 4, 5])
3.5


Calculate the median, or 50th percentile, of data grouped into class intervals
centred on the data values provided. E.g. if your data points are rounded to
the nearest whole number:

>>> median_grouped([2, 2, 3, 3, 3, 4])  #doctest: +ELLIPSIS
2.8333333333...

This should be interpreted in this way: you have two data points in the class
interval 1.5-2.5, three data points in the class interval 2.5-3.5, and one in
the class interval 3.5-4.5. The median of these data points is 2.8333...


Calculating variability or spread
---------------------------------

==================  =============================================
Function            Description
==================  =============================================
pvariance           Population variance of data.
variance            Sample variance of data.
pstdev              Population standard deviation of data.
stdev               Sample standard deviation of data.
==================  =============================================

Calculate the standard deviation of sample data:

>>> stdev([2.5, 3.25, 5.5, 11.25, 11.75])  #doctest: +ELLIPSIS
4.38961843444...

If you have previously calculated the mean, you can pass it as the optional
second argument to the four "spread" functions to avoid recalculating it:

>>> data = [1, 2, 2, 4, 4, 4, 5, 6]
>>> mu = mean(data)
>>> pvariance(data, mu)
2.5


Statistics for relations between two inputs
-------------------------------------------

==================  ====================================================
Function            Description
==================  ====================================================
covariance          Sample covariance for two variables.
correlation         Pearson's correlation coefficient for two variables.
linear_regression   Intercept and slope for simple linear regression.
==================  ====================================================

Calculate covariance, Pearson's correlation, and simple linear regression
for two inputs:

>>> x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> y = [1, 2, 3, 1, 2, 3, 1, 2, 3]
>>> covariance(x, y)
0.75
>>> correlation(x, y)  #doctest: +ELLIPSIS
0.31622776601...
>>> linear_regression(x, y)  #doctest:
LinearRegression(slope=0.1, intercept=1.5)


Exceptions
----------

A single exception is defined: StatisticsError is a subclass of ValueError.

"""
_英文原名表 = {'NormalDist': '正态分布', 'StatisticsError': '统计错误', 'correlation': '相关系数', 'covariance': '协方差', 'fmean': '浮点平均值', 'geometric_mean': '几何平均值', 'harmonic_mean': '调和平均值', 'kde': '核密度估计', 'kde_random': '随机核密度', 'linear_regression': '线性回归', 'mean': '平均值', 'median': '中位数', 'median_grouped': '分组中位数', 'median_high': '高中位数', 'median_low': '低中位数', 'mode': '众数', 'multimode': '多众数', 'pstdev': '总体标准差', 'pvariance': '总体方差', 'quantiles': '分位数', 'stdev': '样本标准差', 'variance': '方差'}

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
__all__ = ['NormalDist', 'StatisticsError', 'correlation', 'covariance', 'fmean', 'geometric_mean', 'harmonic_mean', 'kde', 'kde_random', 'linear_regression', 'mean', 'median', 'median_grouped', 'median_high', 'median_low', 'mode', 'multimode', 'pstdev', 'pvariance', 'quantiles', 'stdev', 'variance']
import math
import numbers
import random
import sys
from fractions import Fraction
from decimal import Decimal
from itertools import count, groupby, repeat
from bisect import bisect_left, bisect_right
from math import hypot, sqrt, fabs, exp, erfc, tau, log, fsum, sumprod
from math import isfinite, isinf, pi, cos, sin, tan, cosh, asin, atan, acos
from functools import reduce
from operator import itemgetter
from collections import Counter, namedtuple, defaultdict
_SQRT2 = sqrt(2.0)
_random = random

class 统计错误(ValueError):
    pass
import statistics as _英文身份源
统计错误 = _英文身份源.StatisticsError

def 平均值(data):
    """Return the sample arithmetic mean of data.

    >>> mean([1, 2, 3, 4, 4])
    2.8

    >>> from fractions import Fraction as F
    >>> mean([F(3, 7), F(1, 21), F(5, 3), F(1, 3)])
    Fraction(13, 21)

    >>> from decimal import Decimal as D
    >>> mean([D("0.5"), D("0.75"), D("0.625"), D("0.375")])
    Decimal('0.5625')

    If ``data`` is empty, StatisticsError will be raised.

    """
    T, total, n = _sum(data)
    if n < 1:
        raise 统计错误('mean requires at least one data point')
    return _convert(total / n, T)

def 浮点平均值(data, weights=None):
    """Convert data to floats and compute the arithmetic mean.

    This runs faster than the mean() function and it always returns a float.
    If the input dataset is empty, it raises a StatisticsError.

    >>> fmean([3.5, 4.0, 5.25])
    4.25

    """
    if weights is None:
        try:
            n = len(data)
        except TypeError:
            counter = count()
            total = fsum(map(itemgetter(0), zip(data, counter)))
            n = next(counter)
        else:
            total = fsum(data)
        if not n:
            raise 统计错误('fmean requires at least one data point')
        return total / n
    if not isinstance(weights, (list, tuple)):
        weights = list(weights)
    try:
        num = sumprod(data, weights)
    except ValueError:
        raise 统计错误('data and weights must be the same length')
    den = fsum(weights)
    if not den:
        raise 统计错误('sum of weights must be non-zero')
    return num / den

def 几何平均值(data):
    """Convert data to floats and compute the geometric mean.

    Raises a StatisticsError if the input dataset is empty
    or if it contains a negative value.

    Returns zero if the product of inputs is zero.

    No special efforts are made to achieve exact results.
    (However, this may change in the future.)

    >>> round(geometric_mean([54, 24, 36]), 9)
    36.0

    """
    n = 0
    found_zero = False

    def count_positive(iterable):
        nonlocal n, found_zero
        for n, x in enumerate(iterable, start=1):
            if x > 0.0 or math.isnan(x):
                yield x
            elif x == 0.0:
                found_zero = True
            else:
                raise 统计错误('No negative inputs allowed', x)
    total = fsum(map(log, count_positive(data)))
    if not n:
        raise 统计错误('Must have a non-empty dataset')
    if math.isnan(total):
        return math.nan
    if found_zero:
        return math.nan if total == math.inf else 0.0
    return exp(total / n)

def 调和平均值(data, weights=None):
    """Return the harmonic mean of data.

    The harmonic mean is the reciprocal of the arithmetic mean of the
    reciprocals of the data.  It can be used for averaging ratios or
    rates, for example speeds.

    Suppose a car travels 40 km/hr for 5 km and then speeds-up to
    60 km/hr for another 5 km. What is the average speed?

        >>> harmonic_mean([40, 60])
        48.0

    Suppose a car travels 40 km/hr for 5 km, and when traffic clears,
    speeds-up to 60 km/hr for the remaining 30 km of the journey. What
    is the average speed?

        >>> harmonic_mean([40, 60], weights=[5, 30])
        56.0

    If ``data`` is empty, or any element is less than zero,
    ``harmonic_mean`` will raise ``StatisticsError``.

    """
    if iter(data) is data:
        data = list(data)
    errmsg = 'harmonic mean does not support negative values'
    n = len(data)
    if n < 1:
        raise 统计错误('harmonic_mean requires at least one data point')
    elif n == 1 and weights is None:
        x = data[0]
        if isinstance(x, (numbers.Real, Decimal)):
            if x < 0:
                raise 统计错误(errmsg)
            return x
        else:
            raise TypeError('unsupported type')
    if weights is None:
        weights = repeat(1, n)
        sum_weights = n
    else:
        if iter(weights) is weights:
            weights = list(weights)
        if len(weights) != n:
            raise 统计错误('Number of weights does not match data size')
        _, sum_weights, _ = _sum((w for w in _fail_neg(weights, errmsg)))
    try:
        data = _fail_neg(data, errmsg)
        T, total, count = _sum((w / x if w else 0 for w, x in zip(weights, data)))
    except ZeroDivisionError:
        return 0
    if total <= 0:
        raise 统计错误('Weighted sum must be positive')
    return _convert(sum_weights / total, T)

def 中位数(data):
    """Return the median (middle value) of numeric data.

    When the number of data points is odd, return the middle data point.
    When the number of data points is even, the median is interpolated by
    taking the average of the two middle values:

    >>> median([1, 3, 5])
    3
    >>> median([1, 3, 5, 7])
    4.0

    """
    data = sorted(data)
    n = len(data)
    if n == 0:
        raise 统计错误('no median for empty data')
    if n % 2 == 1:
        return data[n // 2]
    else:
        i = n // 2
        return (data[i - 1] + data[i]) / 2

def 低中位数(data):
    """Return the low median of numeric data.

    When the number of data points is odd, the middle value is returned.
    When it is even, the smaller of the two middle values is returned.

    >>> median_low([1, 3, 5])
    3
    >>> median_low([1, 3, 5, 7])
    3

    """
    data = sorted(data)
    n = len(data)
    if n == 0:
        raise 统计错误('no median for empty data')
    if n % 2 == 1:
        return data[n // 2]
    else:
        return data[n // 2 - 1]

def 高中位数(data):
    """Return the high median of data.

    When the number of data points is odd, the middle value is returned.
    When it is even, the larger of the two middle values is returned.

    >>> median_high([1, 3, 5])
    3
    >>> median_high([1, 3, 5, 7])
    5

    """
    data = sorted(data)
    n = len(data)
    if n == 0:
        raise 统计错误('no median for empty data')
    return data[n // 2]

def 分组中位数(data, interval=1.0):
    """Estimates the median for numeric data binned around the midpoints
    of consecutive, fixed-width intervals.

    The *data* can be any iterable of numeric data with each value being
    exactly the midpoint of a bin.  At least one value must be present.

    The *interval* is width of each bin.

    For example, demographic information may have been summarized into
    consecutive ten-year age groups with each group being represented
    by the 5-year midpoints of the intervals:

        >>> demographics = Counter({
        ...    25: 172,   # 20 to 30 years old
        ...    35: 484,   # 30 to 40 years old
        ...    45: 387,   # 40 to 50 years old
        ...    55:  22,   # 50 to 60 years old
        ...    65:   6,   # 60 to 70 years old
        ... })

    The 50th percentile (median) is the 536th person out of the 1071
    member cohort.  That person is in the 30 to 40 year old age group.

    The regular median() function would assume that everyone in the
    tricenarian age group was exactly 35 years old.  A more tenable
    assumption is that the 484 members of that age group are evenly
    distributed between 30 and 40.  For that, we use median_grouped().

        >>> data = list(demographics.elements())
        >>> median(data)
        35
        >>> round(median_grouped(data, interval=10), 1)
        37.5

    The caller is responsible for making sure the data points are separated
    by exact multiples of *interval*.  This is essential for getting a
    correct result.  The function does not check this precondition.

    Inputs may be any numeric type that can be coerced to a float during
    the interpolation step.

    """
    data = sorted(data)
    n = len(data)
    if not n:
        raise 统计错误('no median for empty data')
    x = data[n // 2]
    i = bisect_left(data, x)
    j = bisect_right(data, x, lo=i)
    try:
        interval = float(interval)
        x = float(x)
    except ValueError:
        raise TypeError(f'Value cannot be converted to a float')
    L = x - interval / 2.0
    cf = i
    f = j - i
    return L + interval * (n / 2 - cf) / f

def 众数(data):
    """Return the most common data point from discrete or nominal data.

    ``mode`` assumes discrete data, and returns a single value. This is the
    standard treatment of the mode as commonly taught in schools:

        >>> mode([1, 1, 2, 3, 3, 3, 3, 4])
        3

    This also works with nominal (non-numeric) data:

        >>> mode(["red", "blue", "blue", "red", "green", "red", "red"])
        'red'

    If there are multiple modes with same frequency, return the first one
    encountered:

        >>> mode(['red', 'red', 'green', 'blue', 'blue'])
        'red'

    If *data* is empty, ``mode``, raises StatisticsError.

    """
    pairs = Counter(iter(data)).most_common(1)
    try:
        return pairs[0][0]
    except IndexError:
        raise 统计错误('no mode for empty data') from None

def 多众数(data):
    """Return a list of the most frequently occurring values.

    Will return more than one result if there are multiple modes
    or an empty list if *data* is empty.

    >>> multimode('aabbbbbbbbcc')
    ['b']
    >>> multimode('aabbbbccddddeeffffgg')
    ['b', 'd', 'f']
    >>> multimode('')
    []

    """
    counts = Counter(iter(data))
    if not counts:
        return []
    maxcount = max(counts.values())
    return [value for value, count in counts.items() if count == maxcount]

def 方差(data, xbar=None):
    """Return the sample variance of data.

    data should be an iterable of Real-valued numbers, with at least two
    values. The optional argument xbar, if given, should be the mean of
    the data. If it is missing or None, the mean is automatically calculated.

    Use this function when your data is a sample from a population. To
    calculate the variance from the entire population, see ``pvariance``.

    Examples:

    >>> data = [2.75, 1.75, 1.25, 0.25, 0.5, 1.25, 3.5]
    >>> variance(data)
    1.3720238095238095

    If you have already calculated the mean of your data, you can pass it as
    the optional second argument ``xbar`` to avoid recalculating it:

    >>> m = mean(data)
    >>> variance(data, m)
    1.3720238095238095

    This function does not check that ``xbar`` is actually the mean of
    ``data``. Giving arbitrary values for ``xbar`` may lead to invalid or
    impossible results.

    Decimals and Fractions are supported:

    >>> from decimal import Decimal as D
    >>> variance([D("27.5"), D("30.25"), D("30.25"), D("34.5"), D("41.75")])
    Decimal('31.01875')

    >>> from fractions import Fraction as F
    >>> variance([F(1, 6), F(1, 2), F(5, 3)])
    Fraction(67, 108)

    """
    T, ss, c, n = _ss(data, xbar)
    if n < 2:
        raise 统计错误('variance requires at least two data points')
    return _convert(ss / (n - 1), T)

def 总体方差(data, mu=None):
    """Return the population variance of ``data``.

    data should be a sequence or iterable of Real-valued numbers, with at least one
    value. The optional argument mu, if given, should be the mean of
    the data. If it is missing or None, the mean is automatically calculated.

    Use this function to calculate the variance from the entire population.
    To estimate the variance from a sample, the ``variance`` function is
    usually a better choice.

    Examples:

    >>> data = [0.0, 0.25, 0.25, 1.25, 1.5, 1.75, 2.75, 3.25]
    >>> pvariance(data)
    1.25

    If you have already calculated the mean of the data, you can pass it as
    the optional second argument to avoid recalculating it:

    >>> mu = mean(data)
    >>> pvariance(data, mu)
    1.25

    Decimals and Fractions are supported:

    >>> from decimal import Decimal as D
    >>> pvariance([D("27.5"), D("30.25"), D("30.25"), D("34.5"), D("41.75")])
    Decimal('24.815')

    >>> from fractions import Fraction as F
    >>> pvariance([F(1, 4), F(5, 4), F(1, 2)])
    Fraction(13, 72)

    """
    T, ss, c, n = _ss(data, mu)
    if n < 1:
        raise 统计错误('pvariance requires at least one data point')
    return _convert(ss / n, T)

def 样本标准差(data, xbar=None):
    """Return the square root of the sample variance.

    See ``variance`` for arguments and other details.

    >>> stdev([1.5, 2.5, 2.5, 2.75, 3.25, 4.75])
    1.0810874155219827

    """
    T, ss, c, n = _ss(data, xbar)
    if n < 2:
        raise 统计错误('stdev requires at least two data points')
    mss = ss / (n - 1)
    try:
        mss_numerator = mss.numerator
        mss_denominator = mss.denominator
    except AttributeError:
        raise ValueError('inf or nan encountered in data')
    if issubclass(T, Decimal):
        return _decimal_sqrt_of_frac(mss_numerator, mss_denominator)
    return _float_sqrt_of_frac(mss_numerator, mss_denominator)

def 总体标准差(data, mu=None):
    """Return the square root of the population variance.

    See ``pvariance`` for arguments and other details.

    >>> pstdev([1.5, 2.5, 2.5, 2.75, 3.25, 4.75])
    0.986893273527251

    """
    T, ss, c, n = _ss(data, mu)
    if n < 1:
        raise 统计错误('pstdev requires at least one data point')
    mss = ss / n
    try:
        mss_numerator = mss.numerator
        mss_denominator = mss.denominator
    except AttributeError:
        raise ValueError('inf or nan encountered in data')
    if issubclass(T, Decimal):
        return _decimal_sqrt_of_frac(mss_numerator, mss_denominator)
    return _float_sqrt_of_frac(mss_numerator, mss_denominator)

def 协方差(x, y, /):
    """Covariance

    Return the sample covariance of two inputs *x* and *y*. Covariance
    is a measure of the joint variability of two inputs.

    >>> x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> y = [1, 2, 3, 1, 2, 3, 1, 2, 3]
    >>> covariance(x, y)
    0.75
    >>> z = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    >>> covariance(x, z)
    -7.5
    >>> covariance(z, x)
    -7.5

    """
    n = len(x)
    if len(y) != n:
        raise 统计错误('covariance requires that both inputs have same number of data points')
    if n < 2:
        raise 统计错误('covariance requires at least two data points')
    xbar = fsum(x) / n
    ybar = fsum(y) / n
    sxy = sumprod((xi - xbar for xi in x), (yi - ybar for yi in y))
    return sxy / (n - 1)

def 相关系数(x, y, /, *, method='linear'):
    """Pearson's correlation coefficient

    Return the Pearson's correlation coefficient for two inputs. Pearson's
    correlation coefficient *r* takes values between -1 and +1. It measures
    the strength and direction of a linear relationship.

    >>> x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> y = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    >>> correlation(x, x)
    1.0
    >>> correlation(x, y)
    -1.0

    If *method* is "ranked", computes Spearman's rank correlation coefficient
    for two inputs.  The data is replaced by ranks.  Ties are averaged
    so that equal values receive the same rank.  The resulting coefficient
    measures the strength of a monotonic relationship.

    Spearman's rank correlation coefficient is appropriate for ordinal
    data or for continuous data that doesn't meet the linear proportion
    requirement for Pearson's correlation coefficient.

    """
    n = len(x)
    if len(y) != n:
        raise 统计错误('correlation requires that both inputs have same number of data points')
    if n < 2:
        raise 统计错误('correlation requires at least two data points')
    if method not in {'linear', 'ranked'}:
        raise ValueError(f'Unknown method: {method!r}')
    if method == 'ranked':
        start = (n - 1) / -2
        x = _rank(x, start=start)
        y = _rank(y, start=start)
    else:
        xbar = fsum(x) / n
        ybar = fsum(y) / n
        x = [xi - xbar for xi in x]
        y = [yi - ybar for yi in y]
    sxy = sumprod(x, y)
    sxx = sumprod(x, x)
    syy = sumprod(y, y)
    try:
        return sxy / _sqrtprod(sxx, syy)
    except ZeroDivisionError:
        raise 统计错误('at least one of the inputs is constant')
LinearRegression = namedtuple('LinearRegression', ('slope', 'intercept'))

def 线性回归(x, y, /, *, proportional=False):
    """Slope and intercept for simple linear regression.

    Return the slope and intercept of simple linear regression
    parameters estimated using ordinary least squares. Simple linear
    regression describes relationship between an independent variable
    *x* and a dependent variable *y* in terms of a linear function:

        y = slope * x + intercept + noise

    where *slope* and *intercept* are the regression parameters that are
    estimated, and noise represents the variability of the data that was
    not explained by the linear regression (it is equal to the
    difference between predicted and actual values of the dependent
    variable).

    The parameters are returned as a named tuple.

    >>> x = [1, 2, 3, 4, 5]
    >>> noise = NormalDist().samples(5, seed=42)
    >>> y = [3 * x[i] + 2 + noise[i] for i in range(5)]
    >>> linear_regression(x, y)  #doctest: +ELLIPSIS
    LinearRegression(slope=3.17495..., intercept=1.00925...)

    If *proportional* is true, the independent variable *x* and the
    dependent variable *y* are assumed to be directly proportional.
    The data is fit to a line passing through the origin.

    Since the *intercept* will always be 0.0, the underlying linear
    function simplifies to:

        y = slope * x + noise

    >>> y = [3 * x[i] + noise[i] for i in range(5)]
    >>> linear_regression(x, y, proportional=True)  #doctest: +ELLIPSIS
    LinearRegression(slope=2.90475..., intercept=0.0)

    """
    n = len(x)
    if len(y) != n:
        raise 统计错误('linear regression requires that both inputs have same number of data points')
    if n < 2:
        raise 统计错误('linear regression requires at least two data points')
    if not proportional:
        xbar = fsum(x) / n
        ybar = fsum(y) / n
        x = [xi - xbar for xi in x]
        y = (yi - ybar for yi in y)
    sxy = sumprod(x, y) + 0.0
    sxx = sumprod(x, x)
    try:
        slope = sxy / sxx
    except ZeroDivisionError:
        raise 统计错误('x is constant')
    intercept = 0.0 if proportional else ybar - slope * xbar
    return LinearRegression(slope=slope, intercept=intercept)
_kernel_specs = {}

def 登记(*kernels):
    """Load the kernel's pdf, cdf, invcdf, and support into _kernel_specs."""

    def deco(builder):
        spec = dict(zip(('pdf', 'cdf', 'invcdf', 'support'), builder()))
        for kernel in kernels:
            _kernel_specs[kernel] = spec
        return builder
    return deco

@登记('normal', 'gauss')
def 正态核():
    sqrt2pi = sqrt(2 * pi)
    neg_sqrt2 = -sqrt(2)
    概率密度 = lambda t: exp(-1 / 2 * t * t) / sqrt2pi
    累积概率 = lambda t: 1 / 2 * erfc(t / neg_sqrt2)
    invcdf = lambda t: _normal_dist_inv_cdf(t, 0.0, 1.0)
    support = None
    return (概率密度, 累积概率, invcdf, support)

@登记('logistic')
def 逻辑核():
    概率密度 = lambda t: 1 / 2 / (1.0 + cosh(t))
    累积概率 = lambda t: 1.0 - 1.0 / (exp(t) + 1.0)
    invcdf = lambda p: log(p / (1.0 - p))
    support = None
    return (概率密度, 累积概率, invcdf, support)

@登记('sigmoid')
def S形核():
    c1 = 1 / pi
    c2 = 2 / pi
    c3 = pi / 2
    概率密度 = lambda t: c1 / cosh(t)
    累积概率 = lambda t: c2 * atan(exp(t))
    invcdf = lambda p: log(tan(p * c3))
    support = None
    return (概率密度, 累积概率, invcdf, support)

@登记('rectangular', 'uniform')
def 矩形核():
    概率密度 = lambda t: 1 / 2
    累积概率 = lambda t: 1 / 2 * t + 1 / 2
    invcdf = lambda p: 2.0 * p - 1.0
    support = 1.0
    return (概率密度, 累积概率, invcdf, support)

@登记('triangular')
def 三角核():
    概率密度 = lambda t: 1.0 - abs(t)
    累积概率 = lambda t: t * t * (1 / 2 if t < 0.0 else -1 / 2) + t + 1 / 2
    invcdf = lambda p: sqrt(2.0 * p) - 1.0 if p < 1 / 2 else 1.0 - sqrt(2.0 - 2.0 * p)
    support = 1.0
    return (概率密度, 累积概率, invcdf, support)

@登记('parabolic', 'epanechnikov')
def 抛物核():
    概率密度 = lambda t: 3 / 4 * (1.0 - t * t)
    累积概率 = lambda t: sumprod((-1 / 4, 3 / 4, 1 / 2), (t ** 3, t, 1.0))
    invcdf = lambda p: 2.0 * cos((acos(2.0 * p - 1.0) + pi) / 3.0)
    support = 1.0
    return (概率密度, 累积概率, invcdf, support)

def _newton_raphson(f_inv_estimate, f, f_prime, tolerance=1e-12):

    def 逆函数(y):
        """Return x such that f(x) ≈ y within the specified tolerance."""
        x = f_inv_estimate(y)
        while abs((diff := (f(x) - y))) > tolerance:
            x -= diff / f_prime(x)
        return x
    return 逆函数

def _quartic_invcdf_estimate(p):
    sign, p = (1.0, p) if p <= 1 / 2 else (-1.0, 1.0 - p)
    if p < 0.0106:
        return ((2.0 * p) ** 0.3838 - 1.0) * sign
    x = (2.0 * p) ** 0.4258865685331 - 1.0
    if p < 0.499:
        x += 0.026818732 * sin(7.101753784 * p + 2.73230839482953)
    return x * sign

@登记('quartic', 'biweight')
def 四次核():
    概率密度 = lambda t: 15 / 16 * (1.0 - t * t) ** 2
    累积概率 = lambda t: sumprod((3 / 16, -5 / 8, 15 / 16, 1 / 2), (t ** 5, t ** 3, t, 1.0))
    invcdf = _newton_raphson(_quartic_invcdf_estimate, f=累积概率, f_prime=概率密度)
    support = 1.0
    return (概率密度, 累积概率, invcdf, support)

def _triweight_invcdf_estimate(p):
    sign, p = (1.0, p) if p <= 1 / 2 else (-1.0, 1.0 - p)
    x = (2.0 * p) ** 0.3400218741872791 - 1.0
    if 1e-05 < p < 0.499:
        x -= 0.033 * sin(1.07 * tau * (p - 0.035))
    return x * sign

@登记('triweight')
def 三权核():
    概率密度 = lambda t: 35 / 32 * (1.0 - t * t) ** 3
    累积概率 = lambda t: sumprod((-5 / 32, 21 / 32, -35 / 32, 35 / 32, 1 / 2), (t ** 7, t ** 5, t ** 3, t, 1.0))
    invcdf = _newton_raphson(_triweight_invcdf_estimate, f=累积概率, f_prime=概率密度)
    support = 1.0
    return (概率密度, 累积概率, invcdf, support)

@登记('cosine')
def 余弦核():
    c1 = pi / 4
    c2 = pi / 2
    概率密度 = lambda t: c1 * cos(c2 * t)
    累积概率 = lambda t: 1 / 2 * sin(c2 * t) + 1 / 2
    invcdf = lambda p: 2.0 * asin(2.0 * p - 1.0) / pi
    support = 1.0
    return (概率密度, 累积概率, invcdf, support)
del 登记, 正态核, 逻辑核, S形核
del 矩形核, 三角核, 抛物核
del 四次核, 三权核, 余弦核

def 核密度估计(data, h, kernel='normal', *, cumulative=False):
    """Kernel Density Estimation:  Create a continuous probability density
    function or cumulative distribution function from discrete samples.

    The basic idea is to smooth the data using a kernel function
    to help draw inferences about a population from a sample.

    The degree of smoothing is controlled by the scaling parameter h
    which is called the bandwidth.  Smaller values emphasize local
    features while larger values give smoother results.

    The kernel determines the relative weights of the sample data
    points.  Generally, the choice of kernel shape does not matter
    as much as the more influential bandwidth smoothing parameter.

    Kernels that give some weight to every sample point:

       normal (gauss)
       logistic
       sigmoid

    Kernels that only give weight to sample points within
    the bandwidth:

       rectangular (uniform)
       triangular
       parabolic (epanechnikov)
       quartic (biweight)
       triweight
       cosine

    If *cumulative* is true, will return a cumulative distribution function.

    A StatisticsError will be raised if the data sequence is empty.

    Example
    -------

    Given a sample of six data points, construct a continuous
    function that estimates the underlying probability density:

        >>> sample = [-2.1, -1.3, -0.4, 1.9, 5.1, 6.2]
        >>> f_hat = kde(sample, h=1.5)

    Compute the area under the curve:

        >>> area = sum(f_hat(x) for x in range(-20, 20))
        >>> round(area, 4)
        1.0

    Plot the estimated probability density function at
    evenly spaced points from -6 to 10:

        >>> for x in range(-6, 11):
        ...     density = f_hat(x)
        ...     plot = ' ' * int(density * 400) + 'x'
        ...     print(f'{x:2}: {density:.3f} {plot}')
        ...
        -6: 0.002 x
        -5: 0.009    x
        -4: 0.031             x
        -3: 0.070                             x
        -2: 0.111                                             x
        -1: 0.125                                                   x
         0: 0.110                                            x
         1: 0.086                                   x
         2: 0.068                            x
         3: 0.059                        x
         4: 0.066                           x
         5: 0.082                                 x
         6: 0.082                                 x
         7: 0.058                        x
         8: 0.028            x
         9: 0.009    x
        10: 0.002 x

    Estimate P(4.5 < X <= 7.5), the probability that a new sample value
    will be between 4.5 and 7.5:

        >>> cdf = kde(sample, h=1.5, cumulative=True)
        >>> round(cdf(7.5) - cdf(4.5), 2)
        0.22

    References
    ----------

    Kernel density estimation and its application:
    https://www.itm-conferences.org/articles/itmconf/pdf/2018/08/itmconf_sam2018_00037.pdf

    Kernel functions in common use:
    https://en.wikipedia.org/wiki/Kernel_(statistics)#kernel_functions_in_common_use

    Interactive graphical demonstration and exploration:
    https://demonstrations.wolfram.com/KernelDensityEstimation/

    Kernel estimation of cumulative distribution function of a random variable with bounded support
    https://www.econstor.eu/bitstream/10419/207829/1/10.21307_stattrans-2016-037.pdf

    """
    n = len(data)
    if not n:
        raise 统计错误('Empty data sequence')
    if not isinstance(data[0], (int, float)):
        raise TypeError('Data sequence must contain ints or floats')
    if h <= 0.0:
        raise 统计错误(f'Bandwidth h must be positive, not h={h!r}')
    kernel_spec = _kernel_specs.get(kernel)
    if kernel_spec is None:
        raise 统计错误(f'Unknown kernel name: {kernel!r}')
    K = kernel_spec['pdf']
    W = kernel_spec['cdf']
    support = kernel_spec['support']
    if support is None:

        def 概率密度(x):
            return sum((K((x - x_i) / h) for x_i in data)) / (len(data) * h)

        def 累积概率(x):
            return sum((W((x - x_i) / h) for x_i in data)) / len(data)
    else:
        sample = sorted(data)
        bandwidth = h * support

        def 概率密度(x):
            nonlocal n, sample
            if len(data) != n:
                sample = sorted(data)
                n = len(data)
            i = bisect_left(sample, x - bandwidth)
            j = bisect_right(sample, x + bandwidth)
            supported = sample[i:j]
            return sum((K((x - x_i) / h) for x_i in supported)) / (n * h)

        def 累积概率(x):
            nonlocal n, sample
            if len(data) != n:
                sample = sorted(data)
                n = len(data)
            i = bisect_left(sample, x - bandwidth)
            j = bisect_right(sample, x + bandwidth)
            supported = sample[i:j]
            return sum((W((x - x_i) / h) for x_i in supported), i) / n
    if cumulative:
        累积概率.__doc__ = f'CDF estimate with h={h!r} and kernel={kernel!r}'
        return 累积概率
    else:
        概率密度.__doc__ = f'PDF estimate with h={h!r} and kernel={kernel!r}'
        return 概率密度

def 随机核密度(data, h, kernel='normal', *, seed=None):
    """Return a function that makes a random selection from the estimated
    probability density function created by kde(data, h, kernel).

    Providing a *seed* allows reproducible selections within a single
    thread.  The seed may be an integer, float, str, or bytes.

    A StatisticsError will be raised if the *data* sequence is empty.

    Example:

    >>> data = [-2.1, -1.3, -0.4, 1.9, 5.1, 6.2]
    >>> rand = kde_random(data, h=1.5, seed=8675309)
    >>> new_selections = [rand() for i in range(10)]
    >>> [round(x, 1) for x in new_selections]
    [0.7, 6.2, 1.2, 6.9, 7.0, 1.8, 2.5, -0.5, -1.8, 5.6]

    """
    n = len(data)
    if not n:
        raise 统计错误('Empty data sequence')
    if not isinstance(data[0], (int, float)):
        raise TypeError('Data sequence must contain ints or floats')
    if h <= 0.0:
        raise 统计错误(f'Bandwidth h must be positive, not h={h!r}')
    kernel_spec = _kernel_specs.get(kernel)
    if kernel_spec is None:
        raise 统计错误(f'Unknown kernel name: {kernel!r}')
    invcdf = kernel_spec['invcdf']
    prng = _random.Random(seed)
    random = prng.random
    choice = prng.choice

    def rand():
        return choice(data) + h * invcdf(random())
    rand.__doc__ = f'Random KDE selection with h={h!r} and kernel={kernel!r}'
    return rand

def 分位数(data, *, n=4, method='exclusive'):
    """Divide *data* into *n* continuous intervals with equal probability.

    Returns a list of (n - 1) cut points separating the intervals.

    Set *n* to 4 for quartiles (the default).  Set *n* to 10 for deciles.
    Set *n* to 100 for percentiles which gives the 99 cuts points that
    separate *data* in to 100 equal sized groups.

    The *data* can be any iterable containing sample.
    The cut points are linearly interpolated between data points.

    If *method* is set to *inclusive*, *data* is treated as population
    data.  The minimum value is treated as the 0th percentile and the
    maximum value is treated as the 100th percentile.

    """
    if n < 1:
        raise 统计错误('n must be at least 1')
    data = sorted(data)
    ld = len(data)
    if ld < 2:
        if ld == 1:
            return data * (n - 1)
        raise 统计错误('must have at least one data point')
    if method == 'inclusive':
        m = ld - 1
        result = []
        for i in range(1, n):
            j, delta = divmod(i * m, n)
            interpolated = (data[j] * (n - delta) + data[j + 1] * delta) / n
            result.append(interpolated)
        return result
    if method == 'exclusive':
        m = ld + 1
        result = []
        for i in range(1, n):
            j = i * m // n
            j = 1 if j < 1 else ld - 1 if j > ld - 1 else j
            delta = i * m - j * n
            interpolated = (data[j - 1] * (n - delta) + data[j] * delta) / n
            result.append(interpolated)
        return result
    raise ValueError(f'Unknown method: {method!r}')

class 正态分布:
    """Normal distribution of a random variable"""
    __slots__ = {'_mu': 'Arithmetic mean of a normal distribution', '_sigma': 'Standard deviation of a normal distribution'}

    def __init__(self, mu=0.0, sigma=1.0):
        """NormalDist where mu is the mean and sigma is the standard deviation."""
        if sigma < 0.0:
            raise 统计错误('sigma must be non-negative')
        self._mu = float(mu)
        self._sigma = float(sigma)

    @classmethod
    def 从样本算(cls, data):
        """Make a normal distribution instance from sample data."""
        return cls(*_mean_stdev(data))

    def samples(self, n, *, seed=None):
        """Generate *n* samples for a given mean and standard deviation."""
        rnd = random.random if seed is None else random.Random(seed).random
        逆累积概率 = _normal_dist_inv_cdf
        mu = self._mu
        sigma = self._sigma
        return [逆累积概率(rnd(), mu, sigma) for _ in repeat(None, n)]

    def 概率密度(self, x):
        """Probability density function.  P(x <= X < x+dx) / dx"""
        方差 = self._sigma * self._sigma
        if not 方差:
            raise 统计错误('pdf() not defined when sigma is zero')
        diff = x - self._mu
        return exp(diff * diff / (-2.0 * 方差)) / sqrt(tau * 方差)

    def 累积概率(self, x):
        """Cumulative distribution function.  P(X <= x)"""
        if not self._sigma:
            raise 统计错误('cdf() not defined when sigma is zero')
        return 0.5 * erfc((self._mu - x) / (self._sigma * _SQRT2))

    def 逆累积概率(self, p):
        """Inverse cumulative distribution function.  x : P(X <= x) = p

        Finds the value of the random variable such that the probability of
        the variable being less than or equal to that value equals the given
        probability.

        This function is also called the percent point function or quantile
        function.
        """
        if p <= 0.0 or p >= 1.0:
            raise 统计错误('p must be in the range 0.0 < p < 1.0')
        return _normal_dist_inv_cdf(p, self._mu, self._sigma)

    def 分位数(self, n=4):
        """Divide into *n* continuous intervals with equal probability.

        Returns a list of (n - 1) cut points separating the intervals.

        Set *n* to 4 for quartiles (the default).  Set *n* to 10 for deciles.
        Set *n* to 100 for percentiles which gives the 99 cuts points that
        separate the normal distribution in to 100 equal sized groups.
        """
        return [self.逆累积概率(i / n) for i in range(1, n)]

    def 重叠度(self, other):
        """Compute the overlapping coefficient (OVL) between two normal distributions.

        Measures the agreement between two normal probability distributions.
        Returns a value between 0.0 and 1.0 giving the overlapping area in
        the two underlying probability density functions.

            >>> N1 = NormalDist(2.4, 1.6)
            >>> N2 = NormalDist(3.2, 2.0)
            >>> N1.overlap(N2)
            0.8035050657330205
        """
        if not isinstance(other, 正态分布):
            raise TypeError('Expected another NormalDist instance')
        X, Y = (self, other)
        if (Y._sigma, Y._mu) < (X._sigma, X._mu):
            X, Y = (Y, X)
        X_var, Y_var = (X.variance, Y.variance)
        if not X_var or not Y_var:
            raise 统计错误('overlap() not defined when sigma is zero')
        dv = Y_var - X_var
        dm = fabs(Y._mu - X._mu)
        if not dv:
            return erfc(dm / (2.0 * X._sigma * _SQRT2))
        a = X._mu * Y_var - Y._mu * X_var
        b = X._sigma * Y._sigma * sqrt(dm * dm + dv * log(Y_var / X_var))
        x1 = (a + b) / dv
        x2 = (a - b) / dv
        return 1.0 - (fabs(Y.cdf(x1) - X.cdf(x1)) + fabs(Y.cdf(x2) - X.cdf(x2)))

    def 标准分(self, x):
        """Compute the Standard Score.  (x - mean) / stdev

        Describes *x* in terms of the number of standard deviations
        above or below the mean of the normal distribution.
        """
        if not self._sigma:
            raise 统计错误('zscore() not defined when sigma is zero')
        return (x - self._mu) / self._sigma

    @property
    def 平均值(self):
        """Arithmetic mean of the normal distribution."""
        return self._mu

    @property
    def 中位数(self):
        """Return the median of the normal distribution"""
        return self._mu

    @property
    def 众数(self):
        """Return the mode of the normal distribution

        The mode is the value x where which the probability density
        function (pdf) takes its maximum value.
        """
        return self._mu

    @property
    def 样本标准差(self):
        """Standard deviation of the normal distribution."""
        return self._sigma

    @property
    def 方差(self):
        """Square of the standard deviation."""
        return self._sigma * self._sigma

    def __add__(x1, x2):
        """Add a constant or another NormalDist instance.

        If *other* is a constant, translate mu by the constant,
        leaving sigma unchanged.

        If *other* is a NormalDist, add both the means and the variances.
        Mathematically, this works only if the two distributions are
        independent or if they are jointly normally distributed.
        """
        if isinstance(x2, 正态分布):
            return 正态分布(x1._mu + x2._mu, hypot(x1._sigma, x2._sigma))
        return 正态分布(x1._mu + x2, x1._sigma)

    def __sub__(x1, x2):
        """Subtract a constant or another NormalDist instance.

        If *other* is a constant, translate by the constant mu,
        leaving sigma unchanged.

        If *other* is a NormalDist, subtract the means and add the variances.
        Mathematically, this works only if the two distributions are
        independent or if they are jointly normally distributed.
        """
        if isinstance(x2, 正态分布):
            return 正态分布(x1._mu - x2._mu, hypot(x1._sigma, x2._sigma))
        return 正态分布(x1._mu - x2, x1._sigma)

    def __mul__(x1, x2):
        """Multiply both mu and sigma by a constant.

        Used for rescaling, perhaps to change measurement units.
        Sigma is scaled with the absolute value of the constant.
        """
        return 正态分布(x1._mu * x2, x1._sigma * fabs(x2))

    def __truediv__(x1, x2):
        """Divide both mu and sigma by a constant.

        Used for rescaling, perhaps to change measurement units.
        Sigma is scaled with the absolute value of the constant.
        """
        return 正态分布(x1._mu / x2, x1._sigma / fabs(x2))

    def __pos__(x1):
        """Return a copy of the instance."""
        return 正态分布(x1._mu, x1._sigma)

    def __neg__(x1):
        """Negates mu while keeping sigma the same."""
        return 正态分布(-x1._mu, x1._sigma)
    __radd__ = __add__

    def __rsub__(x1, x2):
        """Subtract a NormalDist from a constant or another NormalDist."""
        return -(x1 - x2)
    __rmul__ = __mul__

    def __eq__(x1, x2):
        """Two NormalDist objects are equal if their mu and sigma are both equal."""
        if not isinstance(x2, 正态分布):
            return NotImplemented
        return x1._mu == x2._mu and x1._sigma == x2._sigma

    def __hash__(self):
        """NormalDist objects hash equal if their mu and sigma are both equal."""
        return hash((self._mu, self._sigma))

    def __repr__(self):
        return f'{type(self).__name__}(mu={self._mu!r}, sigma={self._sigma!r})'

    def __getstate__(self):
        return (self._mu, self._sigma)

    def __setstate__(self, state):
        self._mu, self._sigma = state
_装类转发(正态分布, {'cdf': '累积概率', 'from_samples': '从样本算', 'inv_cdf': '逆累积概率', 'mean': '平均值', 'median': '中位数', 'mode': '众数', 'overlap': '重叠度', 'pdf': '概率密度', 'quantiles': '分位数', 'stdev': '样本标准差', 'variance': '方差', 'zscore': '标准分'}, {'cdf': '累积概率', 'from_samples': '从样本算', 'inv_cdf': '逆累积概率', 'mean': '平均值', 'median': '中位数', 'mode': '众数', 'overlap': '重叠度', 'pdf': '概率密度', 'quantiles': '分位数', 'stdev': '样本标准差', 'variance': '方差', 'zscore': '标准分'})

def _sum(data):
    """_sum(data) -> (type, sum, count)

    Return a high-precision sum of the given numeric data as a fraction,
    together with the type to be converted to and the count of items.

    Examples
    --------

    >>> _sum([3, 2.25, 4.5, -0.5, 0.25])
    (<class 'float'>, Fraction(19, 2), 5)

    Some sources of round-off error will be avoided:

    # Built-in sum returns zero.
    >>> _sum([1e50, 1, -1e50] * 1000)
    (<class 'float'>, Fraction(1000, 1), 3000)

    Fractions and Decimals are also supported:

    >>> from fractions import Fraction as F
    >>> _sum([F(2, 3), F(7, 5), F(1, 4), F(5, 6)])
    (<class 'fractions.Fraction'>, Fraction(63, 20), 4)

    >>> from decimal import Decimal as D
    >>> data = [D("0.1375"), D("0.2108"), D("0.3061"), D("0.0419")]
    >>> _sum(data)
    (<class 'decimal.Decimal'>, Fraction(6963, 10000), 4)

    Mixed types are currently treated as an error, except that int is
    allowed.

    """
    count = 0
    types = set()
    types_add = types.add
    partials = {}
    partials_get = partials.get
    for typ, values in groupby(data, type):
        types_add(typ)
        for n, d in map(_exact_ratio, values):
            count += 1
            partials[d] = partials_get(d, 0) + n
    if None in partials:
        total = partials[None]
        assert not _isfinite(total)
    else:
        total = sum((Fraction(n, d) for d, n in partials.items()))
    T = reduce(_coerce, types, int)
    return (T, total, count)

def _ss(data, c=None):
    """Return the exact mean and sum of square deviations of sequence data.

    Calculations are done in a single pass, allowing the input to be an iterator.

    If given *c* is used the mean; otherwise, it is calculated from the data.
    Use the *c* argument with care, as it can lead to garbage results.

    """
    if c is not None:
        T, ssd, count = _sum(((d := (x - c)) * d for x in data))
        return (T, ssd, c, count)
    count = 0
    types = set()
    types_add = types.add
    sx_partials = defaultdict(int)
    sxx_partials = defaultdict(int)
    for typ, values in groupby(data, type):
        types_add(typ)
        for n, d in map(_exact_ratio, values):
            count += 1
            sx_partials[d] += n
            sxx_partials[d] += n * n
    if not count:
        ssd = c = Fraction(0)
    elif None in sx_partials:
        ssd = c = sx_partials[None]
        assert not _isfinite(ssd)
    else:
        sx = sum((Fraction(n, d) for d, n in sx_partials.items()))
        sxx = sum((Fraction(n, d * d) for d, n in sxx_partials.items()))
        ssd = (count * sxx - sx * sx) / count
        c = sx / count
    T = reduce(_coerce, types, int)
    return (T, ssd, c, count)

def _isfinite(x):
    try:
        return x.is_finite()
    except AttributeError:
        return math.isfinite(x)

def _coerce(T, S):
    """Coerce types T and S to a common type, or raise TypeError.

    Coercion rules are currently an implementation detail. See the CoerceTest
    test class in test_statistics for details.

    """
    assert T is not bool, 'initial type T is bool'
    if T is S:
        return T
    if S is int or S is bool:
        return T
    if T is int:
        return S
    if issubclass(S, T):
        return S
    if issubclass(T, S):
        return T
    if issubclass(T, int):
        return S
    if issubclass(S, int):
        return T
    if issubclass(T, Fraction) and issubclass(S, float):
        return S
    if issubclass(T, float) and issubclass(S, Fraction):
        return T
    msg = "don't know how to coerce %s and %s"
    raise TypeError(msg % (T.__name__, S.__name__))

def _exact_ratio(x):
    """Return Real number x to exact (numerator, denominator) pair.

    >>> _exact_ratio(0.25)
    (1, 4)

    x is expected to be an int, Fraction, Decimal or float.

    """
    try:
        return x.as_integer_ratio()
    except AttributeError:
        pass
    except (OverflowError, ValueError):
        assert not _isfinite(x)
        return (x, None)
    try:
        return (x.numerator, x.denominator)
    except AttributeError:
        msg = f"can't convert type '{type(x).__name__}' to numerator/denominator"
        raise TypeError(msg)

def _convert(value, T):
    """Convert value to given numeric type T."""
    if type(value) is T:
        return value
    if issubclass(T, int) and value.denominator != 1:
        T = float
    try:
        return T(value)
    except TypeError:
        if issubclass(T, Decimal):
            return T(value.numerator) / T(value.denominator)
        else:
            raise

def _fail_neg(values, errmsg='negative value'):
    """Iterate over values, failing if any are less than zero."""
    for x in values:
        if x < 0:
            raise 统计错误(errmsg)
        yield x

def _rank(data, /, *, key=None, reverse=False, ties='average', start=1) -> list[float]:
    """Rank order a dataset. The lowest value has rank 1.

    Ties are averaged so that equal values receive the same rank:

        >>> data = [31, 56, 31, 25, 75, 18]
        >>> _rank(data)
        [3.5, 5.0, 3.5, 2.0, 6.0, 1.0]

    The operation is idempotent:

        >>> _rank([3.5, 5.0, 3.5, 2.0, 6.0, 1.0])
        [3.5, 5.0, 3.5, 2.0, 6.0, 1.0]

    It is possible to rank the data in reverse order so that the
    highest value has rank 1.  Also, a key-function can extract
    the field to be ranked:

        >>> goals = [('eagles', 45), ('bears', 48), ('lions', 44)]
        >>> _rank(goals, key=itemgetter(1), reverse=True)
        [2.0, 1.0, 3.0]

    Ranks are conventionally numbered starting from one; however,
    setting *start* to zero allows the ranks to be used as array indices:

        >>> prize = ['Gold', 'Silver', 'Bronze', 'Certificate']
        >>> scores = [8.1, 7.3, 9.4, 8.3]
        >>> [prize[int(i)] for i in _rank(scores, start=0, reverse=True)]
        ['Bronze', 'Certificate', 'Gold', 'Silver']

    """
    if ties != 'average':
        raise ValueError(f'Unknown tie resolution method: {ties!r}')
    if key is not None:
        data = map(key, data)
    val_pos = sorted(zip(data, count()), reverse=reverse)
    i = start - 1
    result = [0] * len(val_pos)
    for _, g in groupby(val_pos, key=itemgetter(0)):
        group = list(g)
        size = len(group)
        rank = i + (size + 1) / 2
        for value, orig_pos in group:
            result[orig_pos] = rank
        i += size
    return result

def _integer_sqrt_of_frac_rto(n: int, m: int) -> int:
    """Square root of n/m, rounded to the nearest integer using round-to-odd."""
    a = math.isqrt(n // m)
    return a | (a * a * m != n)
_sqrt_bit_width: int = 2 * sys.float_info.mant_dig + 3

def _float_sqrt_of_frac(n: int, m: int) -> float:
    """Square root of n/m as a float, correctly rounded."""
    q = (n.bit_length() - m.bit_length() - _sqrt_bit_width) // 2
    if q >= 0:
        numerator = _integer_sqrt_of_frac_rto(n, m << 2 * q) << q
        denominator = 1
    else:
        numerator = _integer_sqrt_of_frac_rto(n << -2 * q, m)
        denominator = 1 << -q
    return numerator / denominator

def _decimal_sqrt_of_frac(n: int, m: int) -> Decimal:
    """Square root of n/m as a Decimal, correctly rounded."""
    if n <= 0:
        if not n:
            return Decimal('0.0')
        n, m = (-n, -m)
    root = (Decimal(n) / Decimal(m)).sqrt()
    nr, dr = root.as_integer_ratio()
    plus = root.next_plus()
    np, dp = plus.as_integer_ratio()
    if 4 * n * (dr * dp) ** 2 > m * (dr * np + dp * nr) ** 2:
        return plus
    minus = root.next_minus()
    nm, dm = minus.as_integer_ratio()
    if 4 * n * (dr * dm) ** 2 < m * (dr * nm + dm * nr) ** 2:
        return minus
    return root

def _mean_stdev(data):
    """In one pass, compute the mean and sample standard deviation as floats."""
    T, ss, xbar, n = _ss(data)
    if n < 2:
        raise 统计错误('stdev requires at least two data points')
    mss = ss / (n - 1)
    try:
        return (float(xbar), _float_sqrt_of_frac(mss.numerator, mss.denominator))
    except AttributeError:
        return (float(xbar), float(xbar) / float(ss))

def _sqrtprod(x: float, y: float) -> float:
    """Return sqrt(x * y) computed with improved accuracy and without overflow/underflow."""
    h = sqrt(x * y)
    if not isfinite(h):
        if isinf(h) and (not isinf(x)) and (not isinf(y)):
            scale = 2.0 ** (-512)
            return _sqrtprod(scale * x, scale * y) / scale
        return h
    if not h:
        if x and y:
            scale = 2.0 ** 537
            return _sqrtprod(scale * x, scale * y) / scale
        return h
    d = sumprod((x, h), (y, -h))
    return h + d / (2.0 * h)

def _normal_dist_inv_cdf(p, mu, sigma):
    q = p - 0.5
    if fabs(q) <= 0.425:
        r = 0.180625 - q * q
        num = (((((((2509.0809287301227 * r + 33430.57558358813) * r + 67265.7709270087) * r + 45921.95393154987) * r + 13731.69376550946) * r + 1971.5909503065513) * r + 133.14166789178438) * r + 3.3871328727963665) * q
        den = ((((((5226.495278852854 * r + 28729.085735721943) * r + 39307.89580009271) * r + 21213.794301586597) * r + 5394.196021424751) * r + 687.1870074920579) * r + 42.31333070160091) * r + 1.0
        x = num / den
        return mu + x * sigma
    r = p if q <= 0.0 else 1.0 - p
    r = sqrt(-log(r))
    if r <= 5.0:
        r = r - 1.6
        num = ((((((0.0007745450142783414 * r + 0.022723844989269184) * r + 0.2417807251774506) * r + 1.2704582524523684) * r + 3.6478483247632045) * r + 5.769497221460691) * r + 4.630337846156546) * r + 1.4234371107496835
        den = ((((((1.0507500716444169e-09 * r + 0.0005475938084995345) * r + 0.015198666563616457) * r + 0.14810397642748008) * r + 0.6897673349851) * r + 1.6763848301838038) * r + 2.053191626637759) * r + 1.0
    else:
        r = r - 5.0
        num = ((((((2.0103343992922881e-07 * r + 2.7115555687434876e-05) * r + 0.0012426609473880784) * r + 0.026532189526576124) * r + 0.29656057182850487) * r + 1.7848265399172913) * r + 5.463784911164114) * r + 6.657904643501103
        den = ((((((2.0442631033899397e-15 * r + 1.421511758316446e-07) * r + 1.8463183175100548e-05) * r + 0.0007868691311456133) * r + 0.014875361290850615) * r + 0.1369298809227358) * r + 0.599832206555888) * r + 1.0
    x = num / den
    if q < 0.0:
        x = -x
    return mu + x * sigma
try:
    from _statistics import _normal_dist_inv_cdf
except ImportError:
    pass


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import statistics as _英文库
统计错误 = _英文库.StatisticsError
_模块别名 = {
    'NormalDist': '正态分布',
    'StatisticsError': '统计错误',
    'correlation': '相关系数',
    'covariance': '协方差',
    'fmean': '浮点平均值',
    'geometric_mean': '几何平均值',
    'harmonic_mean': '调和平均值',
    'kde': '核密度估计',
    'kde_random': '随机核密度',
    'linear_regression': '线性回归',
    'mean': '平均值',
    'median': '中位数',
    'median_grouped': '分组中位数',
    'median_high': '高中位数',
    'median_low': '低中位数',
    'mode': '众数',
    'multimode': '多众数',
    'pstdev': '总体标准差',
    'pvariance': '总体方差',
    'quantiles': '分位数',
    'stdev': '样本标准差',
    'variance': '方差',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '正态分布': {
        'cdf': '累积概率',
        'from_samples': '从样本算',
        'inv_cdf': '逆累积概率',
        'mean': '平均值',
        'median': '中位数',
        'mode': '众数',
        'overlap': '重叠度',
        'pdf': '概率密度',
        'quantiles': '分位数',
        'stdev': '样本标准差',
        'variance': '方差',
        'zscore': '标准分',
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
    '正态分布': {
        'cdf': '累积概率',
        'from_samples': '从样本算',
        'inv_cdf': '逆累积概率',
        'mean': '平均值',
        'median': '中位数',
        'mode': '众数',
        'overlap': '重叠度',
        'pdf': '概率密度',
        'quantiles': '分位数',
        'stdev': '样本标准差',
        'variance': '方差',
        'zscore': '标准分',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '中位数',
    '众数',
    '低中位数',
    '几何平均值',
    '分位数',
    '分组中位数',
    '协方差',
    '多众数',
    '平均值',
    '总体方差',
    '总体标准差',
    '方差',
    '样本标准差',
    '核密度估计',
    '正态分布',
    '浮点平均值',
    '相关系数',
    '线性回归',
    '统计错误',
    '调和平均值',
    '随机核密度',
    '高中位数',
])

# ---- 转发层结束 ----
