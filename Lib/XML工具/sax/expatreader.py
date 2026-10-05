# -*- coding: utf-8 -*-
"""XML工具.sax/expatreader —— 汉语库（由 tools/汉化库.py 从 Lib/xml/sax/expatreader.py 机械生成，**不要手改**）。

英文库 Lib/xml.sax/expatreader.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


"""
SAX driver for the pyexpat C module.  This driver works with
pyexpat.__version__ == '2.22'.
"""
_英文原名表 = {'ExpatLocator': 'Expat定位器', 'ExpatParser': 'Expat解析器', 'create_parser': '造解析器', 'version': '版本'}

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
版本 = '0.20'
from XML工具.sax._exceptions import *
from XML工具.sax.handler import feature_validation, feature_namespaces
from XML工具.sax.handler import feature_namespace_prefixes
from XML工具.sax.handler import feature_external_ges, feature_external_pes
from XML工具.sax.handler import feature_string_interning
from XML工具.sax.handler import property_xml_string, property_interning_dict
try:
    from XML工具.parsers import expat
except ImportError:
    raise SAXReaderNotAvailable('expat not supported', None)
else:
    if not hasattr(expat, 'ParserCreate'):
        raise SAXReaderNotAvailable('expat not supported', None)
from XML工具.sax import xmlreader, saxutils, handler
AttributesImpl = xmlreader.AttributesImpl
AttributesNSImpl = xmlreader.AttributesNSImpl
try:
    import _weakref
except ImportError:

    def _mkproxy(o):
        return o
else:
    import weakref
    _mkproxy = weakref.proxy
    del weakref, _weakref

class _ClosedParser:
    pass

class Expat定位器(xmlreader.Locator):
    """Locator for use with the ExpatParser class.

    This uses a weak reference to the parser object to avoid creating
    a circular reference between the parser and the content handler.
    """

    def __init__(self, parser):
        self._ref = _mkproxy(parser)

    def 取列号(self):
        parser = self._ref
        if parser._parser is None:
            return None
        return parser._parser.ErrorColumnNumber

    def 取行号(self):
        parser = self._ref
        if parser._parser is None:
            return 1
        return parser._parser.ErrorLineNumber

    def 取公共标识(self):
        parser = self._ref
        if parser is None:
            return None
        return parser._source.getPublicId()

    def 取系统标识(self):
        parser = self._ref
        if parser is None:
            return None
        return parser._source.getSystemId()
_装类转发(Expat定位器, {'getColumnNumber': '取列号', 'getLineNumber': '取行号', 'getPublicId': '取公共标识', 'getSystemId': '取系统标识'}, {'getColumnNumber': '取列号', 'getLineNumber': '取行号', 'getPublicId': '取公共标识', 'getSystemId': '取系统标识'})

class Expat解析器(xmlreader.IncrementalParser, xmlreader.Locator):
    """SAX driver for the pyexpat C module."""

    def __init__(self, namespaceHandling=0, bufsize=2 ** 16 - 20):
        xmlreader.IncrementalParser.__init__(self, bufsize)
        self._source = xmlreader.InputSource()
        self._parser = None
        self._namespaces = namespaceHandling
        self._lex_handler_prop = None
        self._parsing = False
        self._entity_stack = []
        self._external_ges = 0
        self._interning = None

    def 解析(self, source):
        """Parse an XML document from a URL or an InputSource."""
        source = saxutils.prepare_input_source(source)
        self._source = source
        try:
            self.重置()
            self._cont_handler.setDocumentLocator(Expat定位器(self))
            xmlreader.IncrementalParser.parse(self, source)
        except:
            self._close_source()
            raise

    def 准备解析器(self, source):
        if source.getSystemId() is not None:
            self._parser.SetBase(source.getSystemId())

    def 设内容处理器(self, handler):
        xmlreader.IncrementalParser.setContentHandler(self, handler)
        if self._parsing:
            self._reset_cont_handler()

    def 取特性(self, name):
        if name == feature_namespaces:
            return self._namespaces
        elif name == feature_string_interning:
            return self._interning is not None
        elif name in (feature_validation, feature_external_pes, feature_namespace_prefixes):
            return 0
        elif name == feature_external_ges:
            return self._external_ges
        raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

    def 设特性(self, name, state):
        if self._parsing:
            raise SAXNotSupportedException('Cannot set features while parsing')
        if name == feature_namespaces:
            self._namespaces = state
        elif name == feature_external_ges:
            self._external_ges = state
        elif name == feature_string_interning:
            if state:
                if self._interning is None:
                    self._interning = {}
            else:
                self._interning = None
        elif name == feature_validation:
            if state:
                raise SAXNotSupportedException('expat does not support validation')
        elif name == feature_external_pes:
            if state:
                raise SAXNotSupportedException('expat does not read external parameter entities')
        elif name == feature_namespace_prefixes:
            if state:
                raise SAXNotSupportedException('expat does not report namespace prefixes')
        else:
            raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

    def 取属性(self, name):
        if name == handler.property_lexical_handler:
            return self._lex_handler_prop
        elif name == property_interning_dict:
            return self._interning
        elif name == property_xml_string:
            if self._parser:
                if hasattr(self._parser, 'GetInputContext'):
                    return self._parser.GetInputContext()
                else:
                    raise SAXNotRecognizedException('This version of expat does not support getting the XML string')
            else:
                raise SAXNotSupportedException('XML string cannot be returned when not parsing')
        raise SAXNotRecognizedException("Property '%s' not recognized" % name)

    def 设属性(self, name, value):
        if name == handler.property_lexical_handler:
            self._lex_handler_prop = value
            if self._parsing:
                self._reset_lex_handler_prop()
        elif name == property_interning_dict:
            self._interning = value
        elif name == property_xml_string:
            raise SAXNotSupportedException("Property '%s' cannot be set" % name)
        else:
            raise SAXNotRecognizedException("Property '%s' not recognized" % name)

    def 喂入(self, data, isFinal=False):
        if not self._parsing:
            self.重置()
            self._parsing = True
            self._cont_handler.startDocument()
        try:
            self._parser.Parse(data, isFinal)
        except expat.error as e:
            exc = SAXParseException(expat.ErrorString(e.code), e, self)
            self._err_handler.fatalError(exc)

    def flush(self):
        if self._parser is None:
            return
        was_enabled = self._parser.GetReparseDeferralEnabled()
        try:
            self._parser.SetReparseDeferralEnabled(False)
            self._parser.Parse(b'', False)
        except expat.error as e:
            exc = SAXParseException(expat.ErrorString(e.code), e, self)
            self._err_handler.fatalError(exc)
        finally:
            self._parser.SetReparseDeferralEnabled(was_enabled)

    def _close_source(self):
        source = self._source
        try:
            file = source.getCharacterStream()
            if file is not None:
                file.close()
        finally:
            file = source.getByteStream()
            if file is not None:
                file.close()

    def close(self):
        if self._entity_stack or self._parser is None or isinstance(self._parser, _ClosedParser):
            return
        try:
            self.喂入(b'', isFinal=True)
            self._cont_handler.endDocument()
            self._parsing = False
            self._parser = None
        finally:
            self._parsing = False
            if self._parser is not None:
                parser = _ClosedParser()
                parser.ErrorColumnNumber = self._parser.ErrorColumnNumber
                parser.ErrorLineNumber = self._parser.ErrorLineNumber
                self._parser = parser
            self._close_source()

    def _reset_cont_handler(self):
        self._parser.ProcessingInstructionHandler = self._cont_handler.processingInstruction
        self._parser.CharacterDataHandler = self._cont_handler.characters

    def _reset_lex_handler_prop(self):
        lex = self._lex_handler_prop
        parser = self._parser
        if lex is None:
            parser.CommentHandler = None
            parser.StartCdataSectionHandler = None
            parser.EndCdataSectionHandler = None
            parser.StartDoctypeDeclHandler = None
            parser.EndDoctypeDeclHandler = None
        else:
            parser.CommentHandler = lex.comment
            parser.StartCdataSectionHandler = lex.startCDATA
            parser.EndCdataSectionHandler = lex.endCDATA
            parser.StartDoctypeDeclHandler = self.start_doctype_decl
            parser.EndDoctypeDeclHandler = lex.endDTD

    def 重置(self):
        if self._namespaces:
            self._parser = expat.ParserCreate(self._source.getEncoding(), ' ', intern=self._interning)
            self._parser.namespace_prefixes = 1
            self._parser.StartElementHandler = self.start_element_ns
            self._parser.EndElementHandler = self.end_element_ns
        else:
            self._parser = expat.ParserCreate(self._source.getEncoding(), intern=self._interning)
            self._parser.StartElementHandler = self.start_element
            self._parser.EndElementHandler = self.end_element
        self._reset_cont_handler()
        self._parser.UnparsedEntityDeclHandler = self.unparsed_entity_decl
        self._parser.NotationDeclHandler = self.notation_decl
        self._parser.StartNamespaceDeclHandler = self.start_namespace_decl
        self._parser.EndNamespaceDeclHandler = self.end_namespace_decl
        self._decl_handler_prop = None
        if self._lex_handler_prop:
            self._reset_lex_handler_prop()
        self._parser.ExternalEntityRefHandler = self.external_entity_ref
        try:
            self._parser.SkippedEntityHandler = self.skipped_entity_handler
        except AttributeError:
            pass
        self._parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE)
        self._parsing = False
        self._entity_stack = []

    def 取列号(self):
        if self._parser is None:
            return None
        return self._parser.ErrorColumnNumber

    def 取行号(self):
        if self._parser is None:
            return 1
        return self._parser.ErrorLineNumber

    def 取公共标识(self):
        return self._source.getPublicId()

    def 取系统标识(self):
        return self._source.getSystemId()

    def start_element(self, name, attrs):
        self._cont_handler.startElement(name, AttributesImpl(attrs))

    def end_element(self, name):
        self._cont_handler.endElement(name)

    def start_element_ns(self, name, attrs):
        pair = name.split()
        if len(pair) == 1:
            pair = (None, name)
        elif len(pair) == 3:
            pair = (pair[0], pair[1])
        else:
            pair = tuple(pair)
        newattrs = {}
        qnames = {}
        for aname, value in attrs.items():
            parts = aname.split()
            length = len(parts)
            if length == 1:
                qname = aname
                apair = (None, aname)
            elif length == 3:
                qname = '%s:%s' % (parts[2], parts[1])
                apair = (parts[0], parts[1])
            else:
                qname = parts[1]
                apair = tuple(parts)
            newattrs[apair] = value
            qnames[apair] = qname
        self._cont_handler.startElementNS(pair, None, AttributesNSImpl(newattrs, qnames))

    def end_element_ns(self, name):
        pair = name.split()
        if len(pair) == 1:
            pair = (None, name)
        elif len(pair) == 3:
            pair = (pair[0], pair[1])
        else:
            pair = tuple(pair)
        self._cont_handler.endElementNS(pair, None)

    def processing_instruction(self, target, data):
        self._cont_handler.processingInstruction(target, data)

    def character_data(self, data):
        self._cont_handler.characters(data)

    def start_namespace_decl(self, prefix, uri):
        self._cont_handler.startPrefixMapping(prefix, uri)

    def end_namespace_decl(self, prefix):
        self._cont_handler.endPrefixMapping(prefix)

    def start_doctype_decl(self, name, sysid, pubid, has_internal_subset):
        self._lex_handler_prop.startDTD(name, pubid, sysid)

    def unparsed_entity_decl(self, name, base, sysid, pubid, notation_name):
        self._dtd_handler.unparsedEntityDecl(name, pubid, sysid, notation_name)

    def notation_decl(self, name, base, sysid, pubid):
        self._dtd_handler.notationDecl(name, pubid, sysid)

    def external_entity_ref(self, context, base, sysid, pubid):
        if not self._external_ges:
            return 1
        source = self._ent_handler.resolveEntity(pubid, sysid)
        source = saxutils.prepare_input_source(source, self._source.getSystemId() or '')
        self._entity_stack.append((self._parser, self._source))
        self._parser = self._parser.ExternalEntityParserCreate(context)
        self._source = source
        try:
            xmlreader.IncrementalParser.parse(self, source)
        except:
            return 0
        self._parser, self._source = self._entity_stack[-1]
        del self._entity_stack[-1]
        return 1

    def skipped_entity_handler(self, name, is_pe):
        if is_pe:
            name = '%' + name
        self._cont_handler.skippedEntity(name)
_装类转发(Expat解析器, {'feed': '喂入', 'getColumnNumber': '取列号', 'getFeature': '取特性', 'getLineNumber': '取行号', 'getProperty': '取属性', 'getPublicId': '取公共标识', 'getSystemId': '取系统标识', 'parse': '解析', 'prepareParser': '准备解析器', 'reset': '重置', 'setContentHandler': '设内容处理器', 'setFeature': '设特性', 'setProperty': '设属性'}, {'feed': '喂入', 'getColumnNumber': '取列号', 'getFeature': '取特性', 'getLineNumber': '取行号', 'getProperty': '取属性', 'getPublicId': '取公共标识', 'getSystemId': '取系统标识', 'parse': '解析', 'prepareParser': '准备解析器', 'reset': '重置', 'setContentHandler': '设内容处理器', 'setFeature': '设特性', 'setProperty': '设属性'})

def 造解析器(*args, **kwargs):
    return Expat解析器(*args, **kwargs)
if __name__ == '__main__':
    import XML工具.sax.saxutils
    p = 造解析器()
    p.setContentHandler(XML工具.sax.saxutils.XMLGenerator())
    p.setErrorHandler(XML工具.sax.ErrorHandler())
    p.parse('http://www.ibiblio.org/xml/examples/shakespeare/hamlet.xml')


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'ExpatLocator': 'Expat定位器',
    'ExpatParser': 'Expat解析器',
    'create_parser': '造解析器',
    'version': '版本',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'Expat定位器': {
        'getColumnNumber': '取列号',
        'getLineNumber': '取行号',
        'getPublicId': '取公共标识',
        'getSystemId': '取系统标识',
    },
    'Expat解析器': {
        'feed': '喂入',
        'getColumnNumber': '取列号',
        'getFeature': '取特性',
        'getLineNumber': '取行号',
        'getProperty': '取属性',
        'getPublicId': '取公共标识',
        'getSystemId': '取系统标识',
        'parse': '解析',
        'prepareParser': '准备解析器',
        'reset': '重置',
        'setContentHandler': '设内容处理器',
        'setFeature': '设特性',
        'setProperty': '设属性',
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
    'Expat定位器': {
        'getColumnNumber': '取列号',
        'getLineNumber': '取行号',
        'getPublicId': '取公共标识',
        'getSystemId': '取系统标识',
    },
    'Expat解析器': {
        'feed': '喂入',
        'getColumnNumber': '取列号',
        'getFeature': '取特性',
        'getLineNumber': '取行号',
        'getProperty': '取属性',
        'getPublicId': '取公共标识',
        'getSystemId': '取系统标识',
        'parse': '解析',
        'prepareParser': '准备解析器',
        'reset': '重置',
        'setContentHandler': '设内容处理器',
        'setFeature': '设特性',
        'setProperty': '设属性',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
