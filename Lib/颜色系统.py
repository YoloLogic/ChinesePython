# -*- coding: utf-8 -*-
"""颜色系统 —— 汉语库（由 tools/汉化库.py 从 Lib/colorsys.py 机械生成，**不要手改**）。

英文库 Lib/colorsys.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 颜色系统
"""


"""Conversion functions between RGB and other color systems.

This modules provides two functions for each color system ABC:

  rgb_to_abc(r, g, b) --> a, b, c
  abc_to_rgb(a, b, c) --> r, g, b

All inputs and outputs are triples of floats in the range [0.0...1.0]
(with the exception of I and Q, which covers a slightly larger range).
Inputs outside the valid range may cause exceptions or invalid outputs.

Supported color systems:
RGB: Red, Green, Blue components
YIQ: Luminance, Chrominance (used by composite video signals)
HLS: Hue, Luminance, Saturation
HSV: Hue, Saturation, Value
"""
_英文原名表 = {'ONE_SIXTH': '六分之一', 'ONE_THIRD': '三分之一', 'TWO_THIRD': '三分之二', 'hls_to_rgb': 'HLS转RGB', 'hsv_to_rgb': 'HSV转RGB', 'rgb_to_hls': 'RGB转HLS', 'rgb_to_hsv': 'RGB转HSV', 'rgb_to_yiq': 'RGB转YIQ', 'yiq_to_rgb': 'YIQ转RGB'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['rgb_to_yiq', 'yiq_to_rgb', 'rgb_to_hls', 'hls_to_rgb', 'rgb_to_hsv', 'hsv_to_rgb']
三分之一 = 1.0 / 3.0
六分之一 = 1.0 / 6.0
三分之二 = 2.0 / 3.0

def RGB转YIQ(r, g, b):
    y = 0.3 * r + 0.59 * g + 0.11 * b
    i = 0.74 * (r - y) - 0.27 * (b - y)
    q = 0.48 * (r - y) + 0.41 * (b - y)
    return (y, i, q)

def YIQ转RGB(y, i, q):
    r = y + 0.9468822170900693 * i + 0.6235565819861433 * q
    g = y - 0.27478764629897834 * i - 0.6356910791873801 * q
    b = y - 1.1085450346420322 * i + 1.7090069284064666 * q
    if r < 0.0:
        r = 0.0
    if g < 0.0:
        g = 0.0
    if b < 0.0:
        b = 0.0
    if r > 1.0:
        r = 1.0
    if g > 1.0:
        g = 1.0
    if b > 1.0:
        b = 1.0
    return (r, g, b)

def RGB转HLS(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    sumc = maxc + minc
    rangec = maxc - minc
    l = sumc / 2.0
    if minc == maxc:
        return (0.0, l, 0.0)
    if l <= 0.5:
        s = rangec / sumc
    else:
        s = rangec / (2.0 - maxc - minc)
    rc = (maxc - r) / rangec
    gc = (maxc - g) / rangec
    bc = (maxc - b) / rangec
    if r == maxc:
        h = bc - gc
    elif g == maxc:
        h = 2.0 + rc - bc
    else:
        h = 4.0 + gc - rc
    h = h / 6.0 % 1.0
    return (h, l, s)

def HLS转RGB(h, l, s):
    if s == 0.0:
        return (l, l, l)
    if l <= 0.5:
        m2 = l * (1.0 + s)
    else:
        m2 = l + s - l * s
    m1 = 2.0 * l - m2
    return (_v(m1, m2, h + 三分之一), _v(m1, m2, h), _v(m1, m2, h - 三分之一))

def _v(m1, m2, hue):
    hue = hue % 1.0
    if hue < 六分之一:
        return m1 + (m2 - m1) * hue * 6.0
    if hue < 0.5:
        return m2
    if hue < 三分之二:
        return m1 + (m2 - m1) * (三分之二 - hue) * 6.0
    return m1

def RGB转HSV(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    rangec = maxc - minc
    v = maxc
    if minc == maxc:
        return (0.0, 0.0, v)
    s = rangec / maxc
    rc = (maxc - r) / rangec
    gc = (maxc - g) / rangec
    bc = (maxc - b) / rangec
    if r == maxc:
        h = bc - gc
    elif g == maxc:
        h = 2.0 + rc - bc
    else:
        h = 4.0 + gc - rc
    h = h / 6.0 % 1.0
    return (h, s, v)

def HSV转RGB(h, s, v):
    if s == 0.0:
        return (v, v, v)
    i = int(h * 6.0)
    f = h * 6.0 - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'ONE_SIXTH': '六分之一',
    'ONE_THIRD': '三分之一',
    'TWO_THIRD': '三分之二',
    'hls_to_rgb': 'HLS转RGB',
    'hsv_to_rgb': 'HSV转RGB',
    'rgb_to_hls': 'RGB转HLS',
    'rgb_to_hsv': 'RGB转HSV',
    'rgb_to_yiq': 'RGB转YIQ',
    'yiq_to_rgb': 'YIQ转RGB',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'HLS转RGB',
    'HSV转RGB',
    'RGB转HLS',
    'RGB转HSV',
    'RGB转YIQ',
    'YIQ转RGB',
]

# ---- 转发层结束 ----
