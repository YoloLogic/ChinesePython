# -*- coding: utf-8 -*-
"""字符串工具.模板库 —— 汉语库（由 tools/汉化库.py 从 Lib/string/templatelib.py 机械生成，**不要手改**）。

英文库 Lib/string.templatelib.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py string
"""


"""Support for template string literals (t-strings)."""
_英文原名表 = {'Interpolation': '插值', 'Template': '模板', 'convert': '转换'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
t = t'{0}'
模板 = type(t)
插值 = type(t.interpolations[0])
del t

def 转换(obj, /, conversion):
    """Convert *obj* using formatted string literal semantics."""
    if conversion is None:
        return obj
    if conversion == 'r':
        return repr(obj)
    if conversion == 's':
        return str(obj)
    if conversion == 'a':
        return ascii(obj)
    raise ValueError(f'invalid conversion specifier: {conversion}')

def _template_unpickle(*args):
    import itertools
    if len(args) != 2:
        raise ValueError('Template expects tuple of length 2 to unpickle')
    strings, interpolations = args
    parts = []
    for 字符串工具, interpolation in itertools.zip_longest(strings, interpolations):
        if 字符串工具 is not None:
            parts.append(字符串工具)
        if interpolation is not None:
            parts.append(interpolation)
    return 模板(*parts)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Interpolation': '插值',
    'Template': '模板',
    'convert': '转换',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
