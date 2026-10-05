# -*- coding: utf-8 -*-
"""数学 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`math`（纯 C 扩展，没有 `.py` 源码可深拷贝 —— 走**机制 4：包装层**）。
改名字 = 改 `tools\库词表.py` 里的 `包装层["math"]`，然后：

    python tools\汉化包装层.py math

可逆性：删这个文件 + 删词表那一段，英文 `math` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import math as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
反余弦 = __英文模块.acos
反双曲余弦 = __英文模块.acosh
反正弦 = __英文模块.asin
反双曲正弦 = __英文模块.asinh
反正切 = __英文模块.atan
反正切2 = __英文模块.atan2
反双曲正切 = __英文模块.atanh
立方根 = __英文模块.cbrt
向上取整 = __英文模块.ceil
组合数 = __英文模块.comb
复制符号 = __英文模块.copysign
余弦 = __英文模块.cos
双曲余弦 = __英文模块.cosh
转角度 = __英文模块.degrees
欧氏距离 = __英文模块.dist
自然常数 = __英文模块.e
误差函数 = __英文模块.erf
补误差函数 = __英文模块.erfc
指数 = __英文模块.exp
二的指数 = __英文模块.exp2
指数减一 = __英文模块.expm1
绝对值 = __英文模块.fabs
阶乘 = __英文模块.factorial
向下取整 = __英文模块.floor
乘加 = __英文模块.fma
浮点取余 = __英文模块.fmod
拆分尾数指数 = __英文模块.frexp
精确求和 = __英文模块.fsum
伽马函数 = __英文模块.gamma
最大公约数 = __英文模块.gcd
欧氏范数 = __英文模块.hypot
无穷 = __英文模块.inf
近似相等吗 = __英文模块.isclose
有限吗 = __英文模块.isfinite
无穷吗 = __英文模块.isinf
非数吗 = __英文模块.isnan
整数平方根 = __英文模块.isqrt
最小公倍数 = __英文模块.lcm
乘二次幂 = __英文模块.ldexp
伽马对数 = __英文模块.lgamma
对数 = __英文模块.log
十底对数 = __英文模块.log10
对数加一 = __英文模块.log1p
二底对数 = __英文模块.log2
拆分整数小数 = __英文模块.modf
非数 = __英文模块.nan
下一个浮点数 = __英文模块.nextafter
排列数 = __英文模块.perm
圆周率 = __英文模块.pi
幂 = __英文模块.pow
连乘 = __英文模块.prod
转弧度 = __英文模块.radians
余数 = __英文模块.remainder
正弦 = __英文模块.sin
双曲正弦 = __英文模块.sinh
平方根 = __英文模块.sqrt
点积 = __英文模块.sumprod
正切 = __英文模块.tan
双曲正切 = __英文模块.tanh
圆周率二倍 = __英文模块.tau
截断取整 = __英文模块.trunc
浮点间距 = __英文模块.ulp

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
acos = __英文模块.acos
acosh = __英文模块.acosh
asin = __英文模块.asin
asinh = __英文模块.asinh
atan = __英文模块.atan
atan2 = __英文模块.atan2
atanh = __英文模块.atanh
cbrt = __英文模块.cbrt
ceil = __英文模块.ceil
comb = __英文模块.comb
copysign = __英文模块.copysign
cos = __英文模块.cos
cosh = __英文模块.cosh
degrees = __英文模块.degrees
dist = __英文模块.dist
e = __英文模块.e
erf = __英文模块.erf
erfc = __英文模块.erfc
exp = __英文模块.exp
exp2 = __英文模块.exp2
expm1 = __英文模块.expm1
fabs = __英文模块.fabs
factorial = __英文模块.factorial
floor = __英文模块.floor
fma = __英文模块.fma
fmod = __英文模块.fmod
frexp = __英文模块.frexp
fsum = __英文模块.fsum
gamma = __英文模块.gamma
gcd = __英文模块.gcd
hypot = __英文模块.hypot
inf = __英文模块.inf
isclose = __英文模块.isclose
isfinite = __英文模块.isfinite
isinf = __英文模块.isinf
isnan = __英文模块.isnan
isqrt = __英文模块.isqrt
lcm = __英文模块.lcm
ldexp = __英文模块.ldexp
lgamma = __英文模块.lgamma
log = __英文模块.log
log10 = __英文模块.log10
log1p = __英文模块.log1p
log2 = __英文模块.log2
modf = __英文模块.modf
nan = __英文模块.nan
nextafter = __英文模块.nextafter
perm = __英文模块.perm
pi = __英文模块.pi
pow = __英文模块.pow
prod = __英文模块.prod
radians = __英文模块.radians
remainder = __英文模块.remainder
sin = __英文模块.sin
sinh = __英文模块.sinh
sqrt = __英文模块.sqrt
sumprod = __英文模块.sumprod
tan = __英文模块.tan
tanh = __英文模块.tanh
tau = __英文模块.tau
trunc = __英文模块.trunc
ulp = __英文模块.ulp

__all__ = [
    'acos',
    'acosh',
    'asin',
    'asinh',
    'atan',
    'atan2',
    'atanh',
    'cbrt',
    'ceil',
    'comb',
    'copysign',
    'cos',
    'cosh',
    'degrees',
    'dist',
    'e',
    'erf',
    'erfc',
    'exp',
    'exp2',
    'expm1',
    'fabs',
    'factorial',
    'floor',
    'fma',
    'fmod',
    'frexp',
    'fsum',
    'gamma',
    'gcd',
    'hypot',
    'inf',
    'isclose',
    'isfinite',
    'isinf',
    'isnan',
    'isqrt',
    'lcm',
    'ldexp',
    'lgamma',
    'log',
    'log10',
    'log1p',
    'log2',
    'modf',
    'nan',
    'nextafter',
    'perm',
    'pi',
    'pow',
    'prod',
    'radians',
    'remainder',
    'sin',
    'sinh',
    'sqrt',
    'sumprod',
    'tan',
    'tanh',
    'tau',
    'trunc',
    'ulp',
    '反余弦',
    '反双曲余弦',
    '反正弦',
    '反双曲正弦',
    '反正切',
    '反正切2',
    '反双曲正切',
    '立方根',
    '向上取整',
    '组合数',
    '复制符号',
    '余弦',
    '双曲余弦',
    '转角度',
    '欧氏距离',
    '自然常数',
    '误差函数',
    '补误差函数',
    '指数',
    '二的指数',
    '指数减一',
    '绝对值',
    '阶乘',
    '向下取整',
    '乘加',
    '浮点取余',
    '拆分尾数指数',
    '精确求和',
    '伽马函数',
    '最大公约数',
    '欧氏范数',
    '无穷',
    '近似相等吗',
    '有限吗',
    '无穷吗',
    '非数吗',
    '整数平方根',
    '最小公倍数',
    '乘二次幂',
    '伽马对数',
    '对数',
    '十底对数',
    '对数加一',
    '二底对数',
    '拆分整数小数',
    '非数',
    '下一个浮点数',
    '排列数',
    '圆周率',
    '幂',
    '连乘',
    '转弧度',
    '余数',
    '正弦',
    '双曲正弦',
    '平方根',
    '点积',
    '正切',
    '双曲正切',
    '圆周率二倍',
    '截断取整',
    '浮点间距',
]


def __getattr__(名):
    """兜底转发：没在这儿显式列出来的名字（含私有名）照样到得了 C 那边。

    为什么必须有：硬约束是「英文原名一个都不能少」，而 C 模块的内部名
    我们没法一个个预料 —— 官方测试碰得到的、`dir(zlib)` 里有的一切，
    靠这一条全部兜住（PEP 562 的模块级 `__getattr__`）。
    """
    return getattr(__英文模块, 名)


def __dir__():
    # `dir()` 两边都算上：Shell 补全 / 官方那种按 `dir()` 算的判据都看得见。
    # ⚠ **壳自己的辅助函数不列**（D-147）：官方 `test_signal.test_functions_module_attr`
    #   会遍历 `dir()`，要求每个「非内置函数」的 `__module__` 是英文模块名 ——
    #   壳里的 `__getattr__`/`__dir__` 是 Python 函数、`__module__` 是汉语模块名
    #   ⇒ 列出来就挂（实测）。
    return sorted((set(globals()) | set(dir(__英文模块)))
                  - {"__getattr__", "__dir__", "__英文模块"})
