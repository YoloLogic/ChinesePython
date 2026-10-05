# -*- coding: utf-8 -*-
"""复数数学 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`cmath`（纯 C 扩展，没有 `.py` 源码可深拷贝 —— 走**机制 4：包装层**）。
改名字 = 改 `tools\库词表.py` 里的 `包装层["cmath"]`，然后：

    python tools\汉化包装层.py cmath

可逆性：删这个文件 + 删词表那一段，英文 `cmath` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import cmath as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
反余弦 = __英文模块.acos
反双曲余弦 = __英文模块.acosh
反正弦 = __英文模块.asin
反双曲正弦 = __英文模块.asinh
反正切 = __英文模块.atan
反双曲正切 = __英文模块.atanh
余弦 = __英文模块.cos
双曲余弦 = __英文模块.cosh
自然常数 = __英文模块.e
指数 = __英文模块.exp
无穷 = __英文模块.inf
纯虚无穷 = __英文模块.infj
近似相等吗 = __英文模块.isclose
有限吗 = __英文模块.isfinite
无穷吗 = __英文模块.isinf
非数吗 = __英文模块.isnan
对数 = __英文模块.log
十底对数 = __英文模块.log10
非数 = __英文模块.nan
纯虚非数 = __英文模块.nanj
辐角 = __英文模块.phase
圆周率 = __英文模块.pi
转极坐标 = __英文模块.polar
转直角坐标 = __英文模块.rect
正弦 = __英文模块.sin
双曲正弦 = __英文模块.sinh
平方根 = __英文模块.sqrt
正切 = __英文模块.tan
双曲正切 = __英文模块.tanh
圆周率二倍 = __英文模块.tau

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
acos = __英文模块.acos
acosh = __英文模块.acosh
asin = __英文模块.asin
asinh = __英文模块.asinh
atan = __英文模块.atan
atanh = __英文模块.atanh
cos = __英文模块.cos
cosh = __英文模块.cosh
e = __英文模块.e
exp = __英文模块.exp
inf = __英文模块.inf
infj = __英文模块.infj
isclose = __英文模块.isclose
isfinite = __英文模块.isfinite
isinf = __英文模块.isinf
isnan = __英文模块.isnan
log = __英文模块.log
log10 = __英文模块.log10
nan = __英文模块.nan
nanj = __英文模块.nanj
phase = __英文模块.phase
pi = __英文模块.pi
polar = __英文模块.polar
rect = __英文模块.rect
sin = __英文模块.sin
sinh = __英文模块.sinh
sqrt = __英文模块.sqrt
tan = __英文模块.tan
tanh = __英文模块.tanh
tau = __英文模块.tau

__all__ = [
    'acos',
    'acosh',
    'asin',
    'asinh',
    'atan',
    'atanh',
    'cos',
    'cosh',
    'e',
    'exp',
    'inf',
    'infj',
    'isclose',
    'isfinite',
    'isinf',
    'isnan',
    'log',
    'log10',
    'nan',
    'nanj',
    'phase',
    'pi',
    'polar',
    'rect',
    'sin',
    'sinh',
    'sqrt',
    'tan',
    'tanh',
    'tau',
    '反余弦',
    '反双曲余弦',
    '反正弦',
    '反双曲正弦',
    '反正切',
    '反双曲正切',
    '余弦',
    '双曲余弦',
    '自然常数',
    '指数',
    '无穷',
    '纯虚无穷',
    '近似相等吗',
    '有限吗',
    '无穷吗',
    '非数吗',
    '对数',
    '十底对数',
    '非数',
    '纯虚非数',
    '辐角',
    '圆周率',
    '转极坐标',
    '转直角坐标',
    '正弦',
    '双曲正弦',
    '平方根',
    '正切',
    '双曲正切',
    '圆周率二倍',
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
