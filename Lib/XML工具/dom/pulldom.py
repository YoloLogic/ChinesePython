# -*- coding: utf-8 -*-
"""XML工具.dom/pulldom —— 汉语库（由 tools/汉化库.py 从 Lib/xml/dom/pulldom.py 机械生成，**不要手改**）。

英文库 Lib/xml.dom/pulldom.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


_英文原名表 = {'CHARACTERS': '字符数据', 'COMMENT': '注释', 'DOMEventStream': 'DOM事件流', 'END_DOCUMENT': '结束文档', 'END_ELEMENT': '结束元素', 'ErrorHandler': '错误处理器', 'IGNORABLE_WHITESPACE': '可忽略空白', 'PROCESSING_INSTRUCTION': '处理指令', 'PullDOM': '拉取DOM', 'SAX2DOM': 'SAX转DOM', 'START_DOCUMENT': '开始文档', 'START_ELEMENT': '开始元素', 'default_bufsize': '默认缓冲大小', 'parse': '解析', 'parseString': '解析字符串'}

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
import XML工具.sax
import XML工具.sax.handler
开始元素 = 'START_ELEMENT'
结束元素 = 'END_ELEMENT'
注释 = 'COMMENT'
开始文档 = 'START_DOCUMENT'
结束文档 = 'END_DOCUMENT'
处理指令 = 'PROCESSING_INSTRUCTION'
可忽略空白 = 'IGNORABLE_WHITESPACE'
字符数据 = 'CHARACTERS'

class 拉取DOM(XML工具.sax.ContentHandler):
    _locator = None
    document = None

    def __init__(self, documentFactory=None):
        from XML工具.dom import XML_NAMESPACE
        self.documentFactory = documentFactory
        self.firstEvent = [None, None]
        self.lastEvent = self.firstEvent
        self.elementStack = []
        self.push = self.elementStack.append
        try:
            self.pop = self.elementStack.pop
        except AttributeError:
            pass
        self._ns_contexts = [{XML_NAMESPACE: 'xml'}]
        self._current_context = self._ns_contexts[-1]
        self.pending_events = []

    def pop(self):
        result = self.elementStack[-1]
        del self.elementStack[-1]
        return result

    def setDocumentLocator(self, locator):
        self._locator = locator

    def startPrefixMapping(self, prefix, uri):
        if not hasattr(self, '_xmlns_attrs'):
            self._xmlns_attrs = []
        self._xmlns_attrs.append((prefix or 'xmlns', uri))
        self._ns_contexts.append(self._current_context.copy())
        self._current_context[uri] = prefix or None

    def endPrefixMapping(self, prefix):
        self._current_context = self._ns_contexts.pop()

    def startElementNS(self, name, tagName, attrs):
        xmlns_uri = 'http://www.w3.org/2000/xmlns/'
        xmlns_attrs = getattr(self, '_xmlns_attrs', None)
        if xmlns_attrs is not None:
            for aname, value in xmlns_attrs:
                attrs._attrs[xmlns_uri, aname] = value
            self._xmlns_attrs = []
        uri, localname = name
        if uri:
            if tagName is None:
                prefix = self._current_context[uri]
                if prefix:
                    tagName = prefix + ':' + localname
                else:
                    tagName = localname
            if self.document:
                node = self.document.createElementNS(uri, tagName)
            else:
                node = self.建文档(uri, tagName)
        elif self.document:
            node = self.document.createElement(localname)
        else:
            node = self.建文档(None, localname)
        for aname, value in attrs.items():
            a_uri, a_localname = aname
            if a_uri == xmlns_uri:
                if a_localname == 'xmlns':
                    qname = a_localname
                else:
                    qname = 'xmlns:' + a_localname
                attr = self.document.createAttributeNS(a_uri, qname)
                node.setAttributeNodeNS(attr)
            elif a_uri:
                prefix = self._current_context[a_uri]
                if prefix:
                    qname = prefix + ':' + a_localname
                else:
                    qname = a_localname
                attr = self.document.createAttributeNS(a_uri, qname)
                node.setAttributeNodeNS(attr)
            else:
                attr = self.document.createAttribute(a_localname)
                node.setAttributeNode(attr)
            attr.value = value
        self.lastEvent[1] = [(开始元素, node), None]
        self.lastEvent = self.lastEvent[1]
        self.push(node)

    def endElementNS(self, name, tagName):
        self.lastEvent[1] = [(结束元素, self.pop()), None]
        self.lastEvent = self.lastEvent[1]

    def startElement(self, name, attrs):
        if self.document:
            node = self.document.createElement(name)
        else:
            node = self.建文档(None, name)
        for aname, value in attrs.items():
            attr = self.document.createAttribute(aname)
            attr.value = value
            node.setAttributeNode(attr)
        self.lastEvent[1] = [(开始元素, node), None]
        self.lastEvent = self.lastEvent[1]
        self.push(node)

    def endElement(self, name):
        self.lastEvent[1] = [(结束元素, self.pop()), None]
        self.lastEvent = self.lastEvent[1]

    def comment(self, s):
        if self.document:
            node = self.document.createComment(s)
            self.lastEvent[1] = [(注释, node), None]
            self.lastEvent = self.lastEvent[1]
        else:
            event = [(注释, s), None]
            self.pending_events.append(event)

    def processingInstruction(self, target, data):
        if self.document:
            node = self.document.createProcessingInstruction(target, data)
            self.lastEvent[1] = [(处理指令, node), None]
            self.lastEvent = self.lastEvent[1]
        else:
            event = [(处理指令, target, data), None]
            self.pending_events.append(event)

    def ignorableWhitespace(self, chars):
        node = self.document.createTextNode(chars)
        self.lastEvent[1] = [(可忽略空白, node), None]
        self.lastEvent = self.lastEvent[1]

    def characters(self, chars):
        node = self.document.createTextNode(chars)
        self.lastEvent[1] = [(字符数据, node), None]
        self.lastEvent = self.lastEvent[1]

    def startDocument(self):
        if self.documentFactory is None:
            import XML工具.dom.minidom
            self.documentFactory = XML工具.dom.minidom.Document.implementation

    def 建文档(self, uri, tagname):
        node = self.documentFactory.createDocument(uri, tagname, None)
        self.document = node
        self.lastEvent[1] = [(开始文档, node), None]
        self.lastEvent = self.lastEvent[1]
        self.push(node)
        for e in self.pending_events:
            if e[0][0] == 处理指令:
                _, target, data = e[0]
                n = self.document.createProcessingInstruction(target, data)
                e[0] = (处理指令, n)
            elif e[0][0] == 注释:
                n = self.document.createComment(e[0][1])
                e[0] = (注释, n)
            else:
                raise AssertionError('Unknown pending event ', e[0][0])
            self.lastEvent[1] = e
            self.lastEvent = e
        self.pending_events = None
        return node.firstChild

    def endDocument(self):
        self.lastEvent[1] = [(结束文档, self.document), None]
        self.pop()

    def clear(self):
        """clear(): Explicitly release parsing structures"""
        self.document = None
_装类转发(拉取DOM, {'buildDocument': '建文档'}, {'buildDocument': '建文档'})

class 错误处理器:

    def warning(self, exception):
        print(exception)

    def error(self, exception):
        raise exception

    def fatalError(self, exception):
        raise exception

class DOM事件流:

    def __init__(self, stream, parser, bufsize):
        self.stream = stream
        self.parser = parser
        self.bufsize = bufsize
        if not hasattr(self.parser, 'feed'):
            self.取事件 = self._slurp
        self.reset()

    def reset(self):
        self.pulldom = 拉取DOM()
        self.parser.setFeature(XML工具.sax.handler.feature_namespaces, 1)
        self.parser.setContentHandler(self.pulldom)

    def __next__(self):
        rc = self.取事件()
        if rc:
            return rc
        raise StopIteration

    def __iter__(self):
        return self

    def 展开节点(self, node):
        event = self.取事件()
        parents = [node]
        while event:
            token, cur_node = event
            if cur_node is node:
                return
            if token != 结束元素:
                parents[-1].appendChild(cur_node)
            if token == 开始元素:
                parents.append(cur_node)
            elif token == 结束元素:
                del parents[-1]
            event = self.取事件()

    def 取事件(self):
        if not self.pulldom.firstEvent[1]:
            self.pulldom.lastEvent = self.pulldom.firstEvent
        while not self.pulldom.firstEvent[1]:
            buf = self.stream.read(self.bufsize)
            if not buf:
                self.parser.close()
                return None
            self.parser.feed(buf)
        rc = self.pulldom.firstEvent[1][0]
        self.pulldom.firstEvent[1] = self.pulldom.firstEvent[1][1]
        return rc

    def _slurp(self):
        """ Fallback replacement for getEvent() using the
            standard SAX2 interface, which means we slurp the
            SAX events into memory (no performance gain, but
            we are compatible to all SAX parsers).
        """
        self.parser.parse(self.stream)
        self.取事件 = self._emit
        return self._emit()

    def _emit(self):
        """ Fallback replacement for getEvent() that emits
            the events that _slurp() read previously.
        """
        rc = self.pulldom.firstEvent[1][0]
        self.pulldom.firstEvent[1] = self.pulldom.firstEvent[1][1]
        return rc

    def clear(self):
        """clear(): Explicitly release parsing objects"""
        self.pulldom.clear()
        del self.pulldom
        self.parser = None
        self.stream = None
_装类转发(DOM事件流, {'expandNode': '展开节点', 'getEvent': '取事件'}, {'expandNode': '展开节点', 'getEvent': '取事件'})

class SAX转DOM(拉取DOM):

    def startElementNS(self, name, tagName, attrs):
        拉取DOM.startElementNS(self, name, tagName, attrs)
        curNode = self.elementStack[-1]
        parentNode = self.elementStack[-2]
        parentNode.appendChild(curNode)

    def startElement(self, name, attrs):
        拉取DOM.startElement(self, name, attrs)
        curNode = self.elementStack[-1]
        parentNode = self.elementStack[-2]
        parentNode.appendChild(curNode)

    def processingInstruction(self, target, data):
        拉取DOM.processingInstruction(self, target, data)
        node = self.lastEvent[0][1]
        parentNode = self.elementStack[-1]
        parentNode.appendChild(node)

    def ignorableWhitespace(self, chars):
        拉取DOM.ignorableWhitespace(self, chars)
        node = self.lastEvent[0][1]
        parentNode = self.elementStack[-1]
        parentNode.appendChild(node)

    def characters(self, chars):
        拉取DOM.characters(self, chars)
        node = self.lastEvent[0][1]
        parentNode = self.elementStack[-1]
        parentNode.appendChild(node)
默认缓冲大小 = 2 ** 14 - 20

def 解析(stream_or_string, parser=None, bufsize=None):
    if bufsize is None:
        bufsize = 默认缓冲大小
    if isinstance(stream_or_string, str):
        stream = open(stream_or_string, 'rb')
    else:
        stream = stream_or_string
    if not parser:
        parser = XML工具.sax.make_parser()
    return DOM事件流(stream, parser, bufsize)

def 解析字符串(string, parser=None):
    from io import StringIO
    bufsize = len(string)
    buf = StringIO(string)
    if not parser:
        parser = XML工具.sax.make_parser()
    return DOM事件流(buf, parser, bufsize)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'CHARACTERS': '字符数据',
    'COMMENT': '注释',
    'DOMEventStream': 'DOM事件流',
    'END_DOCUMENT': '结束文档',
    'END_ELEMENT': '结束元素',
    'ErrorHandler': '错误处理器',
    'IGNORABLE_WHITESPACE': '可忽略空白',
    'PROCESSING_INSTRUCTION': '处理指令',
    'PullDOM': '拉取DOM',
    'SAX2DOM': 'SAX转DOM',
    'START_DOCUMENT': '开始文档',
    'START_ELEMENT': '开始元素',
    'default_bufsize': '默认缓冲大小',
    'parse': '解析',
    'parseString': '解析字符串',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'DOM事件流': {
        'expandNode': '展开节点',
        'getEvent': '取事件',
    },
    '拉取DOM': {
        'buildDocument': '建文档',
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
    'DOM事件流': {
        'expandNode': '展开节点',
        'getEvent': '取事件',
    },
    '拉取DOM': {
        'buildDocument': '建文档',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
