# -*- coding: utf-8 -*-
"""XML工具.dom/domreg —— 汉语库（由 tools/汉化库.py 从 Lib/xml/dom/domreg.py 机械生成，**不要手改**）。

英文库 Lib/xml.dom/domreg.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


"""Registration facilities for DOM. This module should not be used
directly. Instead, the functions getDOMImplementation and
registerDOMImplementation should be imported from xml.dom."""
_英文原名表 = {'getDOMImplementation': '取DOM实现', 'registerDOMImplementation': '登记DOM实现', 'registered': '已登记实现表', 'well_known_implementations': '已知实现表'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import sys
已知实现表 = {'minidom': 'xml.dom.minidom', '4DOM': 'xml.dom.DOMImplementation'}
已登记实现表 = {}

def 登记DOM实现(name, factory):
    """registerDOMImplementation(name, factory)

    Register the factory function with the name. The factory function
    should return an object which implements the DOMImplementation
    interface. The factory function can either return the same object,
    or a new one (e.g. if that implementation supports some
    customization)."""
    已登记实现表[name] = factory

def _good_enough(dom, features):
    """_good_enough(dom, features) -> Return 1 if the dom offers the features"""
    for f, v in features:
        if not dom.hasFeature(f, v):
            return 0
    return 1

def 取DOM实现(name=None, features=()):
    """getDOMImplementation(name = None, features = ()) -> DOM implementation.

    Return a suitable DOM implementation. The name is either
    well-known, the module name of a DOM implementation, or None. If
    it is not None, imports the corresponding module and returns
    DOMImplementation object if the import succeeds.

    If name is not given, consider the available implementations to
    find one with the required feature set. If no implementation can
    be found, raise an ImportError. The features list must be a sequence
    of (feature, version) pairs which are passed to hasFeature."""
    import os
    creator = None
    mod = 已知实现表.get(name)
    if mod:
        mod = __import__(mod, {}, {}, ['getDOMImplementation'])
        return mod.getDOMImplementation()
    elif name:
        return 已登记实现表[name]()
    elif not sys.flags.ignore_environment and 'PYTHON_DOM' in os.environ:
        return 取DOM实现(name=os.environ['PYTHON_DOM'])
    if isinstance(features, str):
        features = _parse_feature_string(features)
    for creator in 已登记实现表.values():
        dom = creator()
        if _good_enough(dom, features):
            return dom
    for creator in 已知实现表.keys():
        try:
            dom = 取DOM实现(name=creator)
        except Exception:
            continue
        if _good_enough(dom, features):
            return dom
    raise ImportError('no suitable DOM implementation found')

def _parse_feature_string(s):
    features = []
    parts = s.split()
    i = 0
    length = len(parts)
    while i < length:
        feature = parts[i]
        if feature[0] in '0123456789':
            raise ValueError('bad feature name: %r' % (feature,))
        i = i + 1
        version = None
        if i < length:
            v = parts[i]
            if v[0] in '0123456789':
                i = i + 1
                version = v
        features.append((feature, version))
    return tuple(features)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'getDOMImplementation': '取DOM实现',
    'registerDOMImplementation': '登记DOM实现',
    'registered': '已登记实现表',
    'well_known_implementations': '已知实现表',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
