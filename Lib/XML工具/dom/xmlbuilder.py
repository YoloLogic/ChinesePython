# -*- coding: utf-8 -*-
"""XML工具.dom/xmlbuilder —— 汉语库（由 tools/汉化库.py 从 Lib/xml/dom/xmlbuilder.py 机械生成，**不要手改**）。

英文库 Lib/xml.dom/xmlbuilder.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


"""Implementation of the DOM Level 3 'LS-Load' feature."""
_英文原名表 = {'DOMBuilder': 'DOM构建器', 'DOMBuilderFilter': 'DOM构建过滤器', 'DOMEntityResolver': 'DOM实体解析器', 'DOMImplementationLS': 'DOM加载保存实现', 'DOMInputSource': 'DOM输入源', 'DocumentLS': '可加载保存文档', 'Options': '选项'}

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
import copy
import XML工具.dom
from XML工具.dom.NodeFilter import NodeFilter
__all__ = ['DOMBuilder', 'DOMEntityResolver', 'DOMInputSource']

class 选项:
    """Features object that has variables set for each DOMBuilder feature.

    The DOMBuilder class uses an instance of this class to pass settings to
    the ExpatBuilder class.
    """
    namespaces = 1
    namespace_declarations = True
    validation = False
    external_parameter_entities = True
    external_general_entities = True
    external_dtd_subset = True
    validate_if_schema = False
    validate = False
    datatype_normalization = False
    create_entity_ref_nodes = True
    entities = True
    whitespace_in_element_content = True
    cdata_sections = True
    comments = True
    charset_overrides_xml_encoding = True
    infoset = False
    supported_mediatypes_only = False
    errorHandler = None
    filter = None

class DOM构建器:
    entityResolver = None
    errorHandler = None
    filter = None
    ACTION_REPLACE = 1
    ACTION_APPEND_AS_CHILDREN = 2
    ACTION_INSERT_AFTER = 3
    ACTION_INSERT_BEFORE = 4
    _legal_actions = (ACTION_REPLACE, ACTION_APPEND_AS_CHILDREN, ACTION_INSERT_AFTER, ACTION_INSERT_BEFORE)

    def __init__(self):
        self._options = 选项()

    def _get_entityResolver(self):
        return self.entityResolver

    def _set_entityResolver(self, entityResolver):
        self.entityResolver = entityResolver

    def _get_errorHandler(self):
        return self.errorHandler

    def _set_errorHandler(self, errorHandler):
        self.errorHandler = errorHandler

    def _get_filter(self):
        return self.filter

    def _set_filter(self, filter):
        self.filter = filter

    def 设特性(self, name, state):
        if self.支持特性吗(name):
            state = state and 1 or 0
            try:
                settings = self._settings[_name_xform(name), state]
            except KeyError:
                raise XML工具.dom.NotSupportedErr('unsupported feature: %r' % (name,)) from None
            else:
                for name, value in settings:
                    setattr(self._options, name, value)
        else:
            raise XML工具.dom.NotFoundErr('unknown feature: ' + repr(name))

    def 支持特性吗(self, name):
        return hasattr(self._options, _name_xform(name))

    def 能设特性吗(self, name, state):
        key = (_name_xform(name), state and 1 or 0)
        return key in self._settings
    _settings = {('namespace_declarations', 0): [('namespace_declarations', 0)], ('namespace_declarations', 1): [('namespace_declarations', 1)], ('validation', 0): [('validation', 0)], ('external_general_entities', 0): [('external_general_entities', 0)], ('external_general_entities', 1): [('external_general_entities', 1)], ('external_parameter_entities', 0): [('external_parameter_entities', 0)], ('external_parameter_entities', 1): [('external_parameter_entities', 1)], ('validate_if_schema', 0): [('validate_if_schema', 0)], ('create_entity_ref_nodes', 0): [('create_entity_ref_nodes', 0)], ('create_entity_ref_nodes', 1): [('create_entity_ref_nodes', 1)], ('entities', 0): [('create_entity_ref_nodes', 0), ('entities', 0)], ('entities', 1): [('entities', 1)], ('whitespace_in_element_content', 0): [('whitespace_in_element_content', 0)], ('whitespace_in_element_content', 1): [('whitespace_in_element_content', 1)], ('cdata_sections', 0): [('cdata_sections', 0)], ('cdata_sections', 1): [('cdata_sections', 1)], ('comments', 0): [('comments', 0)], ('comments', 1): [('comments', 1)], ('charset_overrides_xml_encoding', 0): [('charset_overrides_xml_encoding', 0)], ('charset_overrides_xml_encoding', 1): [('charset_overrides_xml_encoding', 1)], ('infoset', 0): [], ('infoset', 1): [('namespace_declarations', 0), ('validate_if_schema', 0), ('create_entity_ref_nodes', 0), ('entities', 0), ('cdata_sections', 0), ('datatype_normalization', 1), ('whitespace_in_element_content', 1), ('comments', 1), ('charset_overrides_xml_encoding', 1)], ('supported_mediatypes_only', 0): [('supported_mediatypes_only', 0)], ('namespaces', 0): [('namespaces', 0)], ('namespaces', 1): [('namespaces', 1)]}

    def 取特性(self, name):
        xname = _name_xform(name)
        try:
            return getattr(self._options, xname)
        except AttributeError:
            if name == 'infoset':
                options = self._options
                return options.datatype_normalization and options.whitespace_in_element_content and options.comments and options.charset_overrides_xml_encoding and (not (options.namespace_declarations or options.validate_if_schema or options.create_entity_ref_nodes or options.entities or options.cdata_sections))
            raise XML工具.dom.NotFoundErr('feature %s not known' % repr(name))

    def 解析URI(self, uri):
        if self.entityResolver:
            input = self.entityResolver.resolveEntity(None, uri)
        else:
            input = DOM实体解析器().resolveEntity(None, uri)
        return self.解析(input)

    def 解析(self, input):
        options = copy.copy(self._options)
        options.filter = self.filter
        options.errorHandler = self.errorHandler
        fp = input.byteStream
        if fp is None and input.systemId:
            import urllib.request
            fp = urllib.request.urlopen(input.systemId)
        return self._parse_bytestream(fp, options)

    def 带上下文解析(self, input, cnode, action):
        if action not in self._legal_actions:
            raise ValueError('not a legal action')
        raise NotImplementedError("Haven't written this yet...")

    def _parse_bytestream(self, stream, options):
        import XML工具.dom.expatbuilder
        builder = XML工具.dom.expatbuilder.makeBuilder(options)
        return builder.parseFile(stream)
_装类转发(DOM构建器, {'canSetFeature': '能设特性吗', 'getFeature': '取特性', 'parse': '解析', 'parseURI': '解析URI', 'parseWithContext': '带上下文解析', 'setFeature': '设特性', 'supportsFeature': '支持特性吗'}, {'canSetFeature': '能设特性吗', 'getFeature': '取特性', 'parse': '解析', 'parseURI': '解析URI', 'parseWithContext': '带上下文解析', 'setFeature': '设特性', 'supportsFeature': '支持特性吗'})

def _name_xform(name):
    return name.lower().replace('-', '_')

class DOM实体解析器(object):
    __slots__ = ('_opener',)

    def 解析实体(self, publicId, systemId):
        assert systemId is not None
        source = DOM输入源()
        source.publicId = publicId
        source.systemId = systemId
        source.byteStream = self._get_opener().open(systemId)
        source.encoding = self._guess_media_encoding(source)
        import posixpath, urllib.parse
        parts = urllib.parse.urlparse(systemId)
        scheme, netloc, path, params, query, fragment = parts
        if path and (not path.endswith('/')):
            path = posixpath.dirname(path) + '/'
            parts = (scheme, netloc, path, params, query, fragment)
            source.baseURI = urllib.parse.urlunparse(parts)
        return source

    def _get_opener(self):
        try:
            return self._opener
        except AttributeError:
            self._opener = self._create_opener()
            return self._opener

    def _create_opener(self):
        import urllib.request
        return urllib.request.build_opener()

    def _guess_media_encoding(self, source):
        info = source.byteStream.info()
        charset = info.get_param('charset')
        if charset is not None:
            return charset.lower()
        return None
_装类转发(DOM实体解析器, {'resolveEntity': '解析实体'}, {'resolveEntity': '解析实体'})

class DOM输入源(object):
    __slots__ = ('byteStream', 'characterStream', 'stringData', 'encoding', 'publicId', 'systemId', 'baseURI')

    def __init__(self):
        self.byteStream = None
        self.characterStream = None
        self.stringData = None
        self.encoding = None
        self.publicId = None
        self.systemId = None
        self.baseURI = None

    def _get_byteStream(self):
        return self.byteStream

    def _set_byteStream(self, byteStream):
        self.byteStream = byteStream

    def _get_characterStream(self):
        return self.characterStream

    def _set_characterStream(self, characterStream):
        self.characterStream = characterStream

    def _get_stringData(self):
        return self.stringData

    def _set_stringData(self, data):
        self.stringData = data

    def _get_encoding(self):
        return self.encoding

    def _set_encoding(self, encoding):
        self.encoding = encoding

    def _get_publicId(self):
        return self.publicId

    def _set_publicId(self, publicId):
        self.publicId = publicId

    def _get_systemId(self):
        return self.systemId

    def _set_systemId(self, systemId):
        self.systemId = systemId

    def _get_baseURI(self):
        return self.baseURI

    def _set_baseURI(self, uri):
        self.baseURI = uri

class DOM构建过滤器:
    """Element filter which can be used to tailor construction of
    a DOM instance.
    """
    FILTER_ACCEPT = 1
    FILTER_REJECT = 2
    FILTER_SKIP = 3
    FILTER_INTERRUPT = 4
    whatToShow = NodeFilter.SHOW_ALL

    def _get_whatToShow(self):
        return self.whatToShow

    def acceptNode(self, element):
        return self.FILTER_ACCEPT

    def 开始容器(self, element):
        return self.FILTER_ACCEPT
_装类转发(DOM构建过滤器, {'startContainer': '开始容器'}, {'startContainer': '开始容器'})
del NodeFilter

class 可加载保存文档:
    """Mixin to create documents that conform to the load/save spec."""
    async_ = False

    def _get_async(self):
        return False

    def _set_async(self, flag):
        if flag:
            raise XML工具.dom.NotSupportedErr('asynchronous document loading is not supported')

    def 中止(self):
        raise NotImplementedError("haven't figured out what this means yet")

    def 加载(self, uri):
        raise NotImplementedError("haven't written this yet")

    def 加载XML(self, source):
        raise NotImplementedError("haven't written this yet")

    def 保存XML(self, snode):
        if snode is None:
            snode = self
        elif snode.ownerDocument is not self:
            raise XML工具.dom.WrongDocumentErr()
        return snode.toxml()
_装类转发(可加载保存文档, {'abort': '中止', 'load': '加载', 'loadXML': '加载XML', 'saveXML': '保存XML'}, {'abort': '中止', 'load': '加载', 'loadXML': '加载XML', 'saveXML': '保存XML'})

class DOM加载保存实现:
    MODE_SYNCHRONOUS = 1
    MODE_ASYNCHRONOUS = 2

    def 建DOM构建器(self, mode, schemaType):
        if schemaType is not None:
            raise XML工具.dom.NotSupportedErr('schemaType not yet supported')
        if mode == self.MODE_SYNCHRONOUS:
            return DOM构建器()
        if mode == self.MODE_ASYNCHRONOUS:
            raise XML工具.dom.NotSupportedErr('asynchronous builders are not supported')
        raise ValueError('unknown value for mode')

    def 建DOM写出器(self):
        raise NotImplementedError("the writer interface hasn't been written yet!")

    def 建DOM输入源(self):
        return DOM输入源()
_装类转发(DOM加载保存实现, {'createDOMBuilder': '建DOM构建器', 'createDOMInputSource': '建DOM输入源', 'createDOMWriter': '建DOM写出器'}, {'createDOMBuilder': '建DOM构建器', 'createDOMInputSource': '建DOM输入源', 'createDOMWriter': '建DOM写出器'})


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'DOMBuilder': 'DOM构建器',
    'DOMBuilderFilter': 'DOM构建过滤器',
    'DOMEntityResolver': 'DOM实体解析器',
    'DOMImplementationLS': 'DOM加载保存实现',
    'DOMInputSource': 'DOM输入源',
    'DocumentLS': '可加载保存文档',
    'Options': '选项',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'DOM加载保存实现': {
        'createDOMBuilder': '建DOM构建器',
        'createDOMInputSource': '建DOM输入源',
        'createDOMWriter': '建DOM写出器',
    },
    'DOM实体解析器': {
        'resolveEntity': '解析实体',
    },
    'DOM构建器': {
        'canSetFeature': '能设特性吗',
        'getFeature': '取特性',
        'parse': '解析',
        'parseURI': '解析URI',
        'parseWithContext': '带上下文解析',
        'setFeature': '设特性',
        'supportsFeature': '支持特性吗',
    },
    'DOM构建过滤器': {
        'startContainer': '开始容器',
    },
    '可加载保存文档': {
        'abort': '中止',
        'load': '加载',
        'loadXML': '加载XML',
        'saveXML': '保存XML',
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
    'DOM加载保存实现': {
        'createDOMBuilder': '建DOM构建器',
        'createDOMInputSource': '建DOM输入源',
        'createDOMWriter': '建DOM写出器',
    },
    'DOM实体解析器': {
        'resolveEntity': '解析实体',
    },
    'DOM构建器': {
        'canSetFeature': '能设特性吗',
        'getFeature': '取特性',
        'parse': '解析',
        'parseURI': '解析URI',
        'parseWithContext': '带上下文解析',
        'setFeature': '设特性',
        'supportsFeature': '支持特性吗',
    },
    'DOM构建过滤器': {
        'startContainer': '开始容器',
    },
    '可加载保存文档': {
        'abort': '中止',
        'load': '加载',
        'loadXML': '加载XML',
        'saveXML': '保存XML',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    'DOM实体解析器',
    'DOM构建器',
    'DOM输入源',
])

# ---- 转发层结束 ----
