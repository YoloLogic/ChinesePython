# -*- coding: utf-8 -*-
"""XML工具.etree/ElementInclude —— 汉语库（由 tools/汉化库.py 从 Lib/xml/etree/ElementInclude.py 机械生成，**不要手改**）。

英文库 Lib/xml.etree/ElementInclude.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


_英文原名表 = {'DEFAULT_MAX_INCLUSION_DEPTH': '默认最大包含深度', 'FatalIncludeError': '致命包含错误', 'LimitedRecursiveIncludeError': '递归包含超限错误', 'XINCLUDE': 'XInclude命名空间', 'XINCLUDE_FALLBACK': '回退标签', 'XINCLUDE_INCLUDE': '包含标签', 'default_loader': '默认加载器', 'include': '包含'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import copy
from . import ElementTree
from urllib.parse import urljoin
XInclude命名空间 = '{http://www.w3.org/2001/XInclude}'
包含标签 = XInclude命名空间 + 'include'
回退标签 = XInclude命名空间 + 'fallback'
默认最大包含深度 = 6

class 致命包含错误(SyntaxError):
    pass

class 递归包含超限错误(致命包含错误):
    pass

def 默认加载器(href, parse, encoding=None):
    if parse == 'xml':
        with open(href, 'rb') as file:
            data = ElementTree.parse(file).getroot()
    else:
        if not encoding:
            encoding = 'UTF-8'
        with open(href, 'r', encoding=encoding) as file:
            data = file.read()
    return data

def 包含(elem, loader=None, base_url=None, max_depth=默认最大包含深度):
    if max_depth is None:
        max_depth = -1
    elif max_depth < 0:
        raise ValueError("expected non-negative depth or None for 'max_depth', got %r" % max_depth)
    if hasattr(elem, 'getroot'):
        elem = elem.getroot()
    if loader is None:
        loader = 默认加载器
    _include(elem, loader, base_url, max_depth, set())

def _include(elem, loader, base_url, max_depth, _parent_hrefs):
    i = 0
    while i < len(elem):
        e = elem[i]
        if e.tag == 包含标签:
            href = e.get('href')
            if base_url:
                href = urljoin(base_url, href)
            parse = e.get('parse', 'xml')
            if parse == 'xml':
                if href in _parent_hrefs:
                    raise 致命包含错误('recursive include of %s' % href)
                if max_depth == 0:
                    raise 递归包含超限错误('maximum xinclude depth reached when including file %s' % href)
                _parent_hrefs.add(href)
                node = loader(href, parse)
                if node is None:
                    raise 致命包含错误('cannot load %r as %r' % (href, parse))
                node = copy.copy(node)
                _include(node, loader, href, max_depth - 1, _parent_hrefs)
                _parent_hrefs.remove(href)
                if e.tail:
                    node.tail = (node.tail or '') + e.tail
                elem[i] = node
            elif parse == 'text':
                text = loader(href, parse, e.get('encoding'))
                if text is None:
                    raise 致命包含错误('cannot load %r as %r' % (href, parse))
                if e.tail:
                    text += e.tail
                if i:
                    node = elem[i - 1]
                    node.tail = (node.tail or '') + text
                else:
                    elem.text = (elem.text or '') + text
                del elem[i]
                continue
            else:
                raise 致命包含错误('unknown parse type in xi:include tag (%r)' % parse)
        elif e.tag == 回退标签:
            raise 致命包含错误('xi:fallback tag must be child of xi:include (%r)' % e.tag)
        else:
            _include(e, loader, base_url, max_depth, _parent_hrefs)
        i += 1


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'DEFAULT_MAX_INCLUSION_DEPTH': '默认最大包含深度',
    'FatalIncludeError': '致命包含错误',
    'LimitedRecursiveIncludeError': '递归包含超限错误',
    'XINCLUDE': 'XInclude命名空间',
    'XINCLUDE_FALLBACK': '回退标签',
    'XINCLUDE_INCLUDE': '包含标签',
    'default_loader': '默认加载器',
    'include': '包含',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
