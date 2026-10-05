# -*- coding: utf-8 -*-
"""XML工具.dom/NodeFilter —— 汉语库（由 tools/汉化库.py 从 Lib/xml/dom/NodeFilter.py 机械生成，**不要手改**）。

英文库 Lib/xml.dom/NodeFilter.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


_英文原名表 = {'NodeFilter': '节点过滤器'}

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

class 节点过滤器:
    """
    This is the DOM2 NodeFilter interface. It contains only constants.
    """
    接受过滤 = 1
    拒绝过滤 = 2
    跳过过滤 = 3
    显示全部 = 4294967295
    显示元素 = 1
    显示属性 = 2
    显示文本 = 4
    显示CDATA节 = 8
    显示实体引用 = 16
    显示实体 = 32
    显示处理指令 = 64
    显示注释 = 128
    显示文档 = 256
    显示文档类型 = 512
    显示文档片段 = 1024
    显示记法 = 2048

    def acceptNode(self, node):
        raise NotImplementedError
_装类转发(节点过滤器, {'FILTER_ACCEPT': '接受过滤', 'FILTER_REJECT': '拒绝过滤', 'FILTER_SKIP': '跳过过滤', 'SHOW_ALL': '显示全部', 'SHOW_ATTRIBUTE': '显示属性', 'SHOW_CDATA_SECTION': '显示CDATA节', 'SHOW_COMMENT': '显示注释', 'SHOW_DOCUMENT': '显示文档', 'SHOW_DOCUMENT_FRAGMENT': '显示文档片段', 'SHOW_DOCUMENT_TYPE': '显示文档类型', 'SHOW_ELEMENT': '显示元素', 'SHOW_ENTITY': '显示实体', 'SHOW_ENTITY_REFERENCE': '显示实体引用', 'SHOW_NOTATION': '显示记法', 'SHOW_PROCESSING_INSTRUCTION': '显示处理指令', 'SHOW_TEXT': '显示文本'}, {'FILTER_ACCEPT': '接受过滤', 'FILTER_REJECT': '拒绝过滤', 'FILTER_SKIP': '跳过过滤', 'SHOW_ALL': '显示全部', 'SHOW_ATTRIBUTE': '显示属性', 'SHOW_CDATA_SECTION': '显示CDATA节', 'SHOW_COMMENT': '显示注释', 'SHOW_DOCUMENT': '显示文档', 'SHOW_DOCUMENT_FRAGMENT': '显示文档片段', 'SHOW_DOCUMENT_TYPE': '显示文档类型', 'SHOW_ELEMENT': '显示元素', 'SHOW_ENTITY': '显示实体', 'SHOW_ENTITY_REFERENCE': '显示实体引用', 'SHOW_NOTATION': '显示记法', 'SHOW_PROCESSING_INSTRUCTION': '显示处理指令', 'SHOW_TEXT': '显示文本'})


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'NodeFilter': '节点过滤器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '节点过滤器': {
        'FILTER_ACCEPT': '接受过滤',
        'FILTER_REJECT': '拒绝过滤',
        'FILTER_SKIP': '跳过过滤',
        'SHOW_ALL': '显示全部',
        'SHOW_ATTRIBUTE': '显示属性',
        'SHOW_CDATA_SECTION': '显示CDATA节',
        'SHOW_COMMENT': '显示注释',
        'SHOW_DOCUMENT': '显示文档',
        'SHOW_DOCUMENT_FRAGMENT': '显示文档片段',
        'SHOW_DOCUMENT_TYPE': '显示文档类型',
        'SHOW_ELEMENT': '显示元素',
        'SHOW_ENTITY': '显示实体',
        'SHOW_ENTITY_REFERENCE': '显示实体引用',
        'SHOW_NOTATION': '显示记法',
        'SHOW_PROCESSING_INSTRUCTION': '显示处理指令',
        'SHOW_TEXT': '显示文本',
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
    '节点过滤器': {
        'FILTER_ACCEPT': '接受过滤',
        'FILTER_REJECT': '拒绝过滤',
        'FILTER_SKIP': '跳过过滤',
        'SHOW_ALL': '显示全部',
        'SHOW_ATTRIBUTE': '显示属性',
        'SHOW_CDATA_SECTION': '显示CDATA节',
        'SHOW_COMMENT': '显示注释',
        'SHOW_DOCUMENT': '显示文档',
        'SHOW_DOCUMENT_FRAGMENT': '显示文档片段',
        'SHOW_DOCUMENT_TYPE': '显示文档类型',
        'SHOW_ELEMENT': '显示元素',
        'SHOW_ENTITY': '显示实体',
        'SHOW_ENTITY_REFERENCE': '显示实体引用',
        'SHOW_NOTATION': '显示记法',
        'SHOW_PROCESSING_INSTRUCTION': '显示处理指令',
        'SHOW_TEXT': '显示文本',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
