# -*- coding: utf-8 -*-
"""XML工具.sax/xmlreader —— 汉语库（由 tools/汉化库.py 从 Lib/xml/sax/xmlreader.py 机械生成，**不要手改**）。

英文库 Lib/xml.sax/xmlreader.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


"""An XML Reader is the SAX 2 name for an XML parser. XML Parsers
should be based on this code. """
_英文原名表 = {'AttributesImpl': '属性表', 'AttributesNSImpl': '命名空间属性表', 'IncrementalParser': '增量解析器', 'InputSource': '输入源', 'Locator': '定位器', 'XMLReader': 'XML读取器'}

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
from . import handler
from ._exceptions import SAXNotSupportedException, SAXNotRecognizedException

class XML读取器:
    """Interface for reading an XML document using callbacks.

    XMLReader is the interface that an XML parser's SAX2 driver must
    implement. This interface allows an application to set and query
    features and properties in the parser, to register event handlers
    for document processing, and to initiate a document parse.

    All SAX interfaces are assumed to be synchronous: the parse
    methods must not return until parsing is complete, and readers
    must wait for an event-handler callback to return before reporting
    the next event."""

    def __init__(self):
        self._cont_handler = handler.ContentHandler()
        self._dtd_handler = handler.DTDHandler()
        self._ent_handler = handler.EntityResolver()
        self._err_handler = handler.ErrorHandler()

    def 解析(self, source):
        """Parse an XML document from a system identifier or an InputSource."""
        raise NotImplementedError('This method must be implemented!')

    def 取内容处理器(self):
        """Returns the current ContentHandler."""
        return self._cont_handler

    def 设内容处理器(self, handler):
        """Registers a new object to receive document content events."""
        self._cont_handler = handler

    def 取DTD处理器(self):
        """Returns the current DTD handler."""
        return self._dtd_handler

    def 设DTD处理器(self, handler):
        """Register an object to receive basic DTD-related events."""
        self._dtd_handler = handler

    def 取实体解析器(self):
        """Returns the current EntityResolver."""
        return self._ent_handler

    def 设实体解析器(self, resolver):
        """Register an object to resolve external entities."""
        self._ent_handler = resolver

    def 取错误处理器(self):
        """Returns the current ErrorHandler."""
        return self._err_handler

    def 设错误处理器(self, handler):
        """Register an object to receive error-message events."""
        self._err_handler = handler

    def 设地区(self, locale):
        """Allow an application to set the locale for errors and warnings.

        SAX parsers are not required to provide localization for errors
        and warnings; if they cannot support the requested locale,
        however, they must raise a SAX exception. Applications may
        request a locale change in the middle of a parse."""
        raise SAXNotSupportedException('Locale support not implemented')

    def 取特性(self, name):
        """Looks up and returns the state of a SAX2 feature."""
        raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

    def 设特性(self, name, state):
        """Sets the state of a SAX2 feature."""
        raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

    def 取属性(self, name):
        """Looks up and returns the value of a SAX2 property."""
        raise SAXNotRecognizedException("Property '%s' not recognized" % name)

    def 设属性(self, name, value):
        """Sets the value of a SAX2 property."""
        raise SAXNotRecognizedException("Property '%s' not recognized" % name)
_装类转发(XML读取器, {'getContentHandler': '取内容处理器', 'getDTDHandler': '取DTD处理器', 'getEntityResolver': '取实体解析器', 'getErrorHandler': '取错误处理器', 'getFeature': '取特性', 'getProperty': '取属性', 'parse': '解析', 'setContentHandler': '设内容处理器', 'setDTDHandler': '设DTD处理器', 'setEntityResolver': '设实体解析器', 'setErrorHandler': '设错误处理器', 'setFeature': '设特性', 'setLocale': '设地区', 'setProperty': '设属性'}, {'getContentHandler': '取内容处理器', 'getDTDHandler': '取DTD处理器', 'getEntityResolver': '取实体解析器', 'getErrorHandler': '取错误处理器', 'getFeature': '取特性', 'getProperty': '取属性', 'parse': '解析', 'setContentHandler': '设内容处理器', 'setDTDHandler': '设DTD处理器', 'setEntityResolver': '设实体解析器', 'setErrorHandler': '设错误处理器', 'setFeature': '设特性', 'setLocale': '设地区', 'setProperty': '设属性'})

class 增量解析器(XML读取器):
    """This interface adds three extra methods to the XMLReader
    interface that allow XML parsers to support incremental
    parsing. Support for this interface is optional, since not all
    underlying XML parsers support this functionality.

    When the parser is instantiated it is ready to begin accepting
    data from the feed method immediately. After parsing has been
    finished with a call to close the reset method must be called to
    make the parser ready to accept new data, either from feed or
    using the parse method.

    Note that these methods must _not_ be called during parsing, that
    is, after parse has been called and before it returns.

    By default, the class also implements the parse method of the XMLReader
    interface using the feed, close and reset methods of the
    IncrementalParser interface as a convenience to SAX 2.0 driver
    writers."""

    def __init__(self, bufsize=2 ** 16):
        self._bufsize = bufsize
        XML读取器.__init__(self)

    def 解析(self, source):
        from . import saxutils
        source = saxutils.prepare_input_source(source)
        self.准备解析器(source)
        file = source.getCharacterStream()
        if file is None:
            file = source.getByteStream()
        while (buffer := file.read(self._bufsize)):
            self.喂入(buffer)
        self.close()

    def 喂入(self, data):
        """This method gives the raw XML data in the data parameter to
        the parser and makes it parse the data, emitting the
        corresponding events. It is allowed for XML constructs to be
        split across several calls to feed.

        feed may raise SAXException."""
        raise NotImplementedError('This method must be implemented!')

    def 准备解析器(self, source):
        """This method is called by the parse implementation to allow
        the SAX 2.0 driver to prepare itself for parsing."""
        raise NotImplementedError('prepareParser must be overridden!')

    def close(self):
        """This method is called when the entire XML document has been
        passed to the parser through the feed method, to notify the
        parser that there are no more data. This allows the parser to
        do the final checks on the document and empty the internal
        data buffer.

        The parser will not be ready to parse another document until
        the reset method has been called.

        close may raise SAXException."""
        raise NotImplementedError('This method must be implemented!')

    def 重置(self):
        """This method is called after close has been called to reset
        the parser so that it is ready to parse new documents. The
        results of calling parse or feed after close without calling
        reset are undefined."""
        raise NotImplementedError('This method must be implemented!')
_装类转发(增量解析器, {'feed': '喂入', 'parse': '解析', 'prepareParser': '准备解析器', 'reset': '重置'}, {'feed': '喂入', 'parse': '解析', 'prepareParser': '准备解析器', 'reset': '重置'})

class 定位器:
    """Interface for associating a SAX event with a document
    location. A locator object will return valid results only during
    calls to DocumentHandler methods; at any other time, the
    results are unpredictable."""

    def 取列号(self):
        """Return the column number where the current event ends."""
        return -1

    def 取行号(self):
        """Return the line number where the current event ends."""
        return -1

    def 取公共标识(self):
        """Return the public identifier for the current event."""
        return None

    def 取系统标识(self):
        """Return the system identifier for the current event."""
        return None
_装类转发(定位器, {'getColumnNumber': '取列号', 'getLineNumber': '取行号', 'getPublicId': '取公共标识', 'getSystemId': '取系统标识'}, {'getColumnNumber': '取列号', 'getLineNumber': '取行号', 'getPublicId': '取公共标识', 'getSystemId': '取系统标识'})

class 输入源:
    """Encapsulation of the information needed by the XMLReader to
    read entities.

    This class may include information about the public identifier,
    system identifier, byte stream (possibly with character encoding
    information) and/or the character stream of an entity.

    Applications will create objects of this class for use in the
    XMLReader.parse method and for returning from
    EntityResolver.resolveEntity.

    An InputSource belongs to the application, the XMLReader is not
    allowed to modify InputSource objects passed to it from the
    application, although it may make copies and modify those."""

    def __init__(self, system_id=None):
        self.__system_id = system_id
        self.__public_id = None
        self.__encoding = None
        self.__bytefile = None
        self.__charfile = None

    def 设公共标识(self, public_id):
        """Sets the public identifier of this InputSource."""
        self.__public_id = public_id

    def 取公共标识(self):
        """Returns the public identifier of this InputSource."""
        return self.__public_id

    def 设系统标识(self, system_id):
        """Sets the system identifier of this InputSource."""
        self.__system_id = system_id

    def 取系统标识(self):
        """Returns the system identifier of this InputSource."""
        return self.__system_id

    def 设编码(self, encoding):
        """Sets the character encoding of this InputSource.

        The encoding must be a string acceptable for an XML encoding
        declaration (see section 4.3.3 of the XML recommendation).

        The encoding attribute of the InputSource is ignored if the
        InputSource also contains a character stream."""
        self.__encoding = encoding

    def 取编码(self):
        """Get the character encoding of this InputSource."""
        return self.__encoding

    def 设字节流(self, bytefile):
        """Set the byte stream (a Python file-like object which does
        not perform byte-to-character conversion) for this input
        source.

        The SAX parser will ignore this if there is also a character
        stream specified, but it will use a byte stream in preference
        to opening a URI connection itself.

        If the application knows the character encoding of the byte
        stream, it should set it with the setEncoding method."""
        self.__bytefile = bytefile

    def 取字节流(self):
        """Get the byte stream for this input source.

        The getEncoding method will return the character encoding for
        this byte stream, or None if unknown."""
        return self.__bytefile

    def 设字符流(self, charfile):
        """Set the character stream for this input source. (The stream
        must be a Python 2.0 Unicode-wrapped file-like that performs
        conversion to Unicode strings.)

        If there is a character stream specified, the SAX parser will
        ignore any byte stream and will not attempt to open a URI
        connection to the system identifier."""
        self.__charfile = charfile

    def 取字符流(self):
        """Get the character stream for this input source."""
        return self.__charfile
_装类转发(输入源, {'getByteStream': '取字节流', 'getCharacterStream': '取字符流', 'getEncoding': '取编码', 'getPublicId': '取公共标识', 'getSystemId': '取系统标识', 'setByteStream': '设字节流', 'setCharacterStream': '设字符流', 'setEncoding': '设编码', 'setPublicId': '设公共标识', 'setSystemId': '设系统标识'}, {'getByteStream': '取字节流', 'getCharacterStream': '取字符流', 'getEncoding': '取编码', 'getPublicId': '取公共标识', 'getSystemId': '取系统标识', 'setByteStream': '设字节流', 'setCharacterStream': '设字符流', 'setEncoding': '设编码', 'setPublicId': '设公共标识', 'setSystemId': '设系统标识'})

class 属性表:

    def __init__(self, attrs):
        """Non-NS-aware implementation.

        attrs should be of the form {name : value}."""
        self._attrs = attrs

    def 取长度(self):
        return len(self._attrs)

    def 取类型(self, name):
        return 'CDATA'

    def 取值(self, name):
        return self._attrs[name]

    def 按QName取值(self, name):
        return self._attrs[name]

    def 按QName取名(self, name):
        if name not in self._attrs:
            raise KeyError(name)
        return name

    def 按名取QName(self, name):
        if name not in self._attrs:
            raise KeyError(name)
        return name

    def 取名字表(self):
        return list(self._attrs.keys())

    def 取QName表(self):
        return list(self._attrs.keys())

    def __len__(self):
        return len(self._attrs)

    def __getitem__(self, name):
        return self._attrs[name]

    def keys(self):
        return list(self._attrs.keys())

    def __contains__(self, name):
        return name in self._attrs

    def get(self, name, alternative=None):
        return self._attrs.get(name, alternative)

    def copy(self):
        return self.__class__(self._attrs)

    def items(self):
        return list(self._attrs.items())

    def values(self):
        return list(self._attrs.values())
_装类转发(属性表, {'getLength': '取长度', 'getNameByQName': '按QName取名', 'getNames': '取名字表', 'getQNameByName': '按名取QName', 'getQNames': '取QName表', 'getType': '取类型', 'getValue': '取值', 'getValueByQName': '按QName取值'}, {'getLength': '取长度', 'getNameByQName': '按QName取名', 'getNames': '取名字表', 'getQNameByName': '按名取QName', 'getQNames': '取QName表', 'getType': '取类型', 'getValue': '取值', 'getValueByQName': '按QName取值'})

class 命名空间属性表(属性表):

    def __init__(self, attrs, qnames):
        """NS-aware implementation.

        attrs should be of the form {(ns_uri, lname): value, ...}.
        qnames of the form {(ns_uri, lname): qname, ...}."""
        self._attrs = attrs
        self._qnames = qnames

    def 按QName取值(self, name):
        for nsname, qname in self._qnames.items():
            if qname == name:
                return self._attrs[nsname]
        raise KeyError(name)

    def 按QName取名(self, name):
        for nsname, qname in self._qnames.items():
            if qname == name:
                return nsname
        raise KeyError(name)

    def 按名取QName(self, name):
        return self._qnames[name]

    def 取QName表(self):
        return list(self._qnames.values())

    def copy(self):
        return self.__class__(self._attrs, self._qnames)
_装类转发(命名空间属性表, {'getNameByQName': '按QName取名', 'getQNameByName': '按名取QName', 'getQNames': '取QName表', 'getValueByQName': '按QName取值'}, {'getNameByQName': '按QName取名', 'getQNameByName': '按名取QName', 'getQNames': '取QName表', 'getValueByQName': '按QName取值'})

def _test():
    XML读取器()
    增量解析器()
    定位器()
if __name__ == '__main__':
    _test()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'AttributesImpl': '属性表',
    'AttributesNSImpl': '命名空间属性表',
    'IncrementalParser': '增量解析器',
    'InputSource': '输入源',
    'Locator': '定位器',
    'XMLReader': 'XML读取器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'XML读取器': {
        'getContentHandler': '取内容处理器',
        'getDTDHandler': '取DTD处理器',
        'getEntityResolver': '取实体解析器',
        'getErrorHandler': '取错误处理器',
        'getFeature': '取特性',
        'getProperty': '取属性',
        'parse': '解析',
        'setContentHandler': '设内容处理器',
        'setDTDHandler': '设DTD处理器',
        'setEntityResolver': '设实体解析器',
        'setErrorHandler': '设错误处理器',
        'setFeature': '设特性',
        'setLocale': '设地区',
        'setProperty': '设属性',
    },
    '命名空间属性表': {
        'getNameByQName': '按QName取名',
        'getQNameByName': '按名取QName',
        'getQNames': '取QName表',
        'getValueByQName': '按QName取值',
    },
    '增量解析器': {
        'feed': '喂入',
        'parse': '解析',
        'prepareParser': '准备解析器',
        'reset': '重置',
    },
    '定位器': {
        'getColumnNumber': '取列号',
        'getLineNumber': '取行号',
        'getPublicId': '取公共标识',
        'getSystemId': '取系统标识',
    },
    '属性表': {
        'getLength': '取长度',
        'getNameByQName': '按QName取名',
        'getNames': '取名字表',
        'getQNameByName': '按名取QName',
        'getQNames': '取QName表',
        'getType': '取类型',
        'getValue': '取值',
        'getValueByQName': '按QName取值',
    },
    '输入源': {
        'getByteStream': '取字节流',
        'getCharacterStream': '取字符流',
        'getEncoding': '取编码',
        'getPublicId': '取公共标识',
        'getSystemId': '取系统标识',
        'setByteStream': '设字节流',
        'setCharacterStream': '设字符流',
        'setEncoding': '设编码',
        'setPublicId': '设公共标识',
        'setSystemId': '设系统标识',
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
    'XML读取器': {
        'getContentHandler': '取内容处理器',
        'getDTDHandler': '取DTD处理器',
        'getEntityResolver': '取实体解析器',
        'getErrorHandler': '取错误处理器',
        'getFeature': '取特性',
        'getProperty': '取属性',
        'parse': '解析',
        'setContentHandler': '设内容处理器',
        'setDTDHandler': '设DTD处理器',
        'setEntityResolver': '设实体解析器',
        'setErrorHandler': '设错误处理器',
        'setFeature': '设特性',
        'setLocale': '设地区',
        'setProperty': '设属性',
    },
    '命名空间属性表': {
        'getNameByQName': '按QName取名',
        'getQNameByName': '按名取QName',
        'getQNames': '取QName表',
        'getValueByQName': '按QName取值',
    },
    '增量解析器': {
        'feed': '喂入',
        'parse': '解析',
        'prepareParser': '准备解析器',
        'reset': '重置',
    },
    '定位器': {
        'getColumnNumber': '取列号',
        'getLineNumber': '取行号',
        'getPublicId': '取公共标识',
        'getSystemId': '取系统标识',
    },
    '属性表': {
        'getLength': '取长度',
        'getNameByQName': '按QName取名',
        'getNames': '取名字表',
        'getQNameByName': '按名取QName',
        'getQNames': '取QName表',
        'getType': '取类型',
        'getValue': '取值',
        'getValueByQName': '按QName取值',
    },
    '输入源': {
        'getByteStream': '取字节流',
        'getCharacterStream': '取字符流',
        'getEncoding': '取编码',
        'getPublicId': '取公共标识',
        'getSystemId': '取系统标识',
        'setByteStream': '设字节流',
        'setCharacterStream': '设字符流',
        'setEncoding': '设编码',
        'setPublicId': '设公共标识',
        'setSystemId': '设系统标识',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
