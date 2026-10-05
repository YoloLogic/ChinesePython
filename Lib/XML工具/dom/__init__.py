# -*- coding: utf-8 -*-
"""XML工具.dom/__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/xml/dom/__init__.py 机械生成，**不要手改**）。

英文库 Lib/xml.dom/__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


"""W3C Document Object Model implementation for Python.

The Python mapping of the Document Object Model is documented in the
Python Library Reference in the section on the xml.dom package.

This package contains the following modules:

minidom -- A simple implementation of the Level 1 DOM with namespace
           support added (based on the Level 2 specification) and other
           minor Level 2 functionality.

pulldom -- DOM builder supporting on-demand tree-building for selected
           subtrees of the document.

"""
_英文原名表 = {'Node': '节点'}

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

class 节点:
    """Class giving the NodeType constants."""
    __slots__ = ()
    元素节点 = 1
    属性节点 = 2
    文本节点 = 3
    CDATA节节点 = 4
    实体引用节点 = 5
    实体节点 = 6
    处理指令节点 = 7
    注释节点 = 8
    文档节点 = 9
    文档类型节点 = 10
    文档片段节点 = 11
    记法节点 = 12
_装类转发(节点, {'ATTRIBUTE_NODE': '属性节点', 'CDATA_SECTION_NODE': 'CDATA节节点', 'COMMENT_NODE': '注释节点', 'DOCUMENT_FRAGMENT_NODE': '文档片段节点', 'DOCUMENT_NODE': '文档节点', 'DOCUMENT_TYPE_NODE': '文档类型节点', 'ELEMENT_NODE': '元素节点', 'ENTITY_NODE': '实体节点', 'ENTITY_REFERENCE_NODE': '实体引用节点', 'NOTATION_NODE': '记法节点', 'PROCESSING_INSTRUCTION_NODE': '处理指令节点', 'TEXT_NODE': '文本节点'}, {'ATTRIBUTE_NODE': '属性节点', 'CDATA_SECTION_NODE': 'CDATA节节点', 'COMMENT_NODE': '注释节点', 'DOCUMENT_FRAGMENT_NODE': '文档片段节点', 'DOCUMENT_NODE': '文档节点', 'DOCUMENT_TYPE_NODE': '文档类型节点', 'ELEMENT_NODE': '元素节点', 'ENTITY_NODE': '实体节点', 'ENTITY_REFERENCE_NODE': '实体引用节点', 'NOTATION_NODE': '记法节点', 'PROCESSING_INSTRUCTION_NODE': '处理指令节点', 'TEXT_NODE': '文本节点'})
INDEX_SIZE_ERR = 1
DOMSTRING_SIZE_ERR = 2
HIERARCHY_REQUEST_ERR = 3
WRONG_DOCUMENT_ERR = 4
INVALID_CHARACTER_ERR = 5
NO_DATA_ALLOWED_ERR = 6
NO_MODIFICATION_ALLOWED_ERR = 7
NOT_FOUND_ERR = 8
NOT_SUPPORTED_ERR = 9
INUSE_ATTRIBUTE_ERR = 10
INVALID_STATE_ERR = 11
SYNTAX_ERR = 12
INVALID_MODIFICATION_ERR = 13
NAMESPACE_ERR = 14
INVALID_ACCESS_ERR = 15
VALIDATION_ERR = 16

class DOMException(Exception):
    """Abstract base class for DOM exceptions.
    Exceptions with specific codes are specializations of this class."""

    def __init__(self, *args, **kw):
        if self.__class__ is DOMException:
            raise RuntimeError('DOMException should not be instantiated directly')
        Exception.__init__(self, *args, **kw)

    def _get_code(self):
        return self.code

class IndexSizeErr(DOMException):
    code = INDEX_SIZE_ERR

class DomstringSizeErr(DOMException):
    code = DOMSTRING_SIZE_ERR

class HierarchyRequestErr(DOMException):
    code = HIERARCHY_REQUEST_ERR

class WrongDocumentErr(DOMException):
    code = WRONG_DOCUMENT_ERR

class InvalidCharacterErr(DOMException):
    code = INVALID_CHARACTER_ERR

class NoDataAllowedErr(DOMException):
    code = NO_DATA_ALLOWED_ERR

class NoModificationAllowedErr(DOMException):
    code = NO_MODIFICATION_ALLOWED_ERR

class NotFoundErr(DOMException):
    code = NOT_FOUND_ERR

class NotSupportedErr(DOMException):
    code = NOT_SUPPORTED_ERR

class InuseAttributeErr(DOMException):
    code = INUSE_ATTRIBUTE_ERR

class InvalidStateErr(DOMException):
    code = INVALID_STATE_ERR

class SyntaxErr(DOMException):
    code = SYNTAX_ERR

class InvalidModificationErr(DOMException):
    code = INVALID_MODIFICATION_ERR

class NamespaceErr(DOMException):
    code = NAMESPACE_ERR

class InvalidAccessErr(DOMException):
    code = INVALID_ACCESS_ERR

class ValidationErr(DOMException):
    code = VALIDATION_ERR

class UserDataHandler:
    """Class giving the operation constants for UserDataHandler.handle()."""
    NODE_CLONED = 1
    NODE_IMPORTED = 2
    NODE_DELETED = 3
    NODE_RENAMED = 4
XML_NAMESPACE = 'http://www.w3.org/XML/1998/namespace'
XMLNS_NAMESPACE = 'http://www.w3.org/2000/xmlns/'
XHTML_NAMESPACE = 'http://www.w3.org/1999/xhtml'
EMPTY_NAMESPACE = None
EMPTY_PREFIX = None
from .domreg import getDOMImplementation, registerDOMImplementation


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Node': '节点',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '节点': {
        'ATTRIBUTE_NODE': '属性节点',
        'CDATA_SECTION_NODE': 'CDATA节节点',
        'COMMENT_NODE': '注释节点',
        'DOCUMENT_FRAGMENT_NODE': '文档片段节点',
        'DOCUMENT_NODE': '文档节点',
        'DOCUMENT_TYPE_NODE': '文档类型节点',
        'ELEMENT_NODE': '元素节点',
        'ENTITY_NODE': '实体节点',
        'ENTITY_REFERENCE_NODE': '实体引用节点',
        'NOTATION_NODE': '记法节点',
        'PROCESSING_INSTRUCTION_NODE': '处理指令节点',
        'TEXT_NODE': '文本节点',
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
    '节点': {
        'ATTRIBUTE_NODE': '属性节点',
        'CDATA_SECTION_NODE': 'CDATA节节点',
        'COMMENT_NODE': '注释节点',
        'DOCUMENT_FRAGMENT_NODE': '文档片段节点',
        'DOCUMENT_NODE': '文档节点',
        'DOCUMENT_TYPE_NODE': '文档类型节点',
        'ELEMENT_NODE': '元素节点',
        'ENTITY_NODE': '实体节点',
        'ENTITY_REFERENCE_NODE': '实体引用节点',
        'NOTATION_NODE': '记法节点',
        'PROCESSING_INSTRUCTION_NODE': '处理指令节点',
        'TEXT_NODE': '文本节点',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
