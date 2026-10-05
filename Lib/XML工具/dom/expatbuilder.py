# -*- coding: utf-8 -*-
"""XML工具.dom/expatbuilder —— 汉语库（由 tools/汉化库.py 从 Lib/xml/dom/expatbuilder.py 机械生成，**不要手改**）。

英文库 Lib/xml.dom/expatbuilder.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


"""Facility to use the Expat parser to load a minidom instance
from a string or file.

This avoids all the overhead of SAX and pulldom to gain performance.
"""
_英文原名表 = {'CDATA_SECTION_NODE': 'CDATA节节点', 'DOCUMENT_NODE': '文档节点', 'ElementInfo': '元素信息', 'ExpatBuilder': 'Expat构建器', 'ExpatBuilderNS': 'Expat构建器NS', 'FILTER_ACCEPT': '接受过滤', 'FILTER_INTERRUPT': '中断过滤', 'FILTER_REJECT': '拒绝过滤', 'FILTER_SKIP': '跳过过滤', 'FilterCrutch': '过滤器辅助器', 'FilterVisibilityController': '过滤器可见性控制器', 'FragmentBuilder': '片段构建器', 'FragmentBuilderNS': '片段构建器NS', 'InternalSubsetExtractor': '内部子集提取器', 'Namespaces': '命名空间处理器', 'ParseEscape': '解析中止', 'Rejecter': '拒绝者', 'Skipper': '跳过者', 'TEXT_NODE': '文本节点', 'makeBuilder': '造构建器', 'parse': '解析', 'parseFragment': '解析片段', 'parseFragmentString': '解析片段字符串', 'parseString': '解析字符串', 'theDOMImplementation': '本DOM实现'}

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
from XML工具.dom import xmlbuilder, minidom, Node
from XML工具.dom import EMPTY_NAMESPACE, EMPTY_PREFIX, XMLNS_NAMESPACE
from XML工具.parsers import expat
from XML工具.dom.minidom import _append_child, _set_attribute_node
from XML工具.dom.NodeFilter import NodeFilter
文本节点 = Node.TEXT_NODE
CDATA节节点 = Node.CDATA_SECTION_NODE
文档节点 = Node.DOCUMENT_NODE
接受过滤 = xmlbuilder.DOMBuilderFilter.FILTER_ACCEPT
拒绝过滤 = xmlbuilder.DOMBuilderFilter.FILTER_REJECT
跳过过滤 = xmlbuilder.DOMBuilderFilter.FILTER_SKIP
中断过滤 = xmlbuilder.DOMBuilderFilter.FILTER_INTERRUPT
本DOM实现 = minidom.getDOMImplementation()
_typeinfo_map = {'CDATA': minidom.TypeInfo(None, 'cdata'), 'ENUM': minidom.TypeInfo(None, 'enumeration'), 'ENTITY': minidom.TypeInfo(None, 'entity'), 'ENTITIES': minidom.TypeInfo(None, 'entities'), 'ID': minidom.TypeInfo(None, 'id'), 'IDREF': minidom.TypeInfo(None, 'idref'), 'IDREFS': minidom.TypeInfo(None, 'idrefs'), 'NMTOKEN': minidom.TypeInfo(None, 'nmtoken'), 'NMTOKENS': minidom.TypeInfo(None, 'nmtokens')}

class 元素信息(object):
    __slots__ = ('_attr_info', '_model', 'tagName')

    def __init__(self, tagName, model=None):
        self.tagName = tagName
        self._attr_info = []
        self._model = model

    def __getstate__(self):
        return (self._attr_info, self._model, self.tagName)

    def __setstate__(self, state):
        self._attr_info, self._model, self.tagName = state

    def getAttributeType(self, aname):
        for info in self._attr_info:
            if info[1] == aname:
                t = info[-2]
                if t[0] == '(':
                    return _typeinfo_map['ENUM']
                else:
                    return _typeinfo_map[info[-2]]
        return minidom._no_type

    def getAttributeTypeNS(self, namespaceURI, localName):
        return minidom._no_type

    def isElementContent(self):
        if self._model:
            type = self._model[0]
            return type not in (expat.model.XML_CTYPE_ANY, expat.model.XML_CTYPE_MIXED)
        else:
            return False

    def isEmpty(self):
        if self._model:
            return self._model[0] == expat.model.XML_CTYPE_EMPTY
        else:
            return False

    def isId(self, aname):
        for info in self._attr_info:
            if info[1] == aname:
                return info[-2] == 'ID'
        return False

    def isIdNS(self, euri, ename, auri, aname):
        return self.isId((auri, aname))

def _intern(builder, s):
    return builder._intern_setdefault(s, s)

def _parse_ns_name(builder, name):
    assert ' ' in name
    parts = name.split(' ')
    intern = builder._intern_setdefault
    if len(parts) == 3:
        uri, localname, prefix = parts
        prefix = intern(prefix, prefix)
        qname = '%s:%s' % (prefix, localname)
        qname = intern(qname, qname)
        localname = intern(localname, localname)
    elif len(parts) == 2:
        uri, localname = parts
        prefix = EMPTY_PREFIX
        qname = localname = intern(localname, localname)
    else:
        raise ValueError('Unsupported syntax: spaces in URIs not supported: %r' % name)
    return (intern(uri, uri), localname, prefix, qname)

class Expat构建器:
    """Document builder that uses Expat to build a ParsedXML.DOM document
    instance."""

    def __init__(self, options=None):
        if options is None:
            options = xmlbuilder.Options()
        self._options = options
        if self._options.filter is not None:
            self._filter = 过滤器可见性控制器(self._options.filter)
        else:
            self._filter = None
            self._finish_start_element = id
        self._parser = None
        self.重置()

    def 造解析器(self):
        """Create a new parser object."""
        return expat.ParserCreate()

    def 取解析器(self):
        """Return the parser object, creating a new one if needed."""
        if not self._parser:
            self._parser = self.造解析器()
            self._intern_setdefault = self._parser.intern.setdefault
            self._parser.buffer_text = True
            self._parser.ordered_attributes = True
            self._parser.specified_attributes = True
            self.装上(self._parser)
        return self._parser

    def 重置(self):
        """Free all data structures used during DOM construction."""
        self.document = 本DOM实现.createDocument(EMPTY_NAMESPACE, None, None)
        self.curNode = self.document
        self._elem_info = self.document._elem_info
        self._cdata = False

    def 装上(self, parser):
        """Install the callbacks needed to build the DOM into the parser."""
        parser.StartDoctypeDeclHandler = self.start_doctype_decl_handler
        parser.StartElementHandler = self.first_element_handler
        parser.EndElementHandler = self.end_element_handler
        parser.ProcessingInstructionHandler = self.pi_handler
        if self._options.entities:
            parser.EntityDeclHandler = self.entity_decl_handler
        parser.NotationDeclHandler = self.notation_decl_handler
        if self._options.comments:
            parser.CommentHandler = self.comment_handler
        if self._options.cdata_sections:
            parser.StartCdataSectionHandler = self.start_cdata_section_handler
            parser.EndCdataSectionHandler = self.end_cdata_section_handler
            parser.CharacterDataHandler = self.character_data_handler_cdata
        else:
            parser.CharacterDataHandler = self.character_data_handler
        parser.ExternalEntityRefHandler = self.external_entity_ref_handler
        parser.XmlDeclHandler = self.xml_decl_handler
        parser.ElementDeclHandler = self.element_decl_handler
        parser.AttlistDeclHandler = self.attlist_decl_handler

    def 解析文件(self, file):
        """Parse a document from a file object, returning the document
        node."""
        parser = self.取解析器()
        first_buffer = True
        try:
            while (buffer := file.read(16 * 1024)):
                parser.Parse(buffer, False)
                if first_buffer and self.document.documentElement:
                    self._setup_subset(buffer)
                first_buffer = False
            parser.Parse(b'', True)
        except 解析中止:
            pass
        doc = self.document
        self.重置()
        self._parser = None
        return doc

    def 解析字符串(self, string):
        """Parse a document from a string, returning the document node."""
        parser = self.取解析器()
        try:
            parser.Parse(string, True)
            self._setup_subset(string)
        except 解析中止:
            pass
        doc = self.document
        self.重置()
        self._parser = None
        return doc

    def _setup_subset(self, buffer):
        """Load the internal subset if there might be one."""
        if self.document.doctype:
            extractor = 内部子集提取器()
            extractor.parseString(buffer)
            subset = extractor.getSubset()
            self.document.doctype.internalSubset = subset

    def start_doctype_decl_handler(self, doctypeName, systemId, publicId, has_internal_subset):
        doctype = self.document.implementation.createDocumentType(doctypeName, publicId, systemId)
        doctype.ownerDocument = self.document
        _append_child(self.document, doctype)
        self.document.doctype = doctype
        if self._filter and self._filter.acceptNode(doctype) == 拒绝过滤:
            self.document.doctype = None
            del self.document.childNodes[-1]
            doctype = None
            self._parser.EntityDeclHandler = None
            self._parser.NotationDeclHandler = None
        if has_internal_subset:
            if doctype is not None:
                doctype.entities._seq = []
                doctype.notations._seq = []
            self._parser.CommentHandler = None
            self._parser.ProcessingInstructionHandler = None
            self._parser.EndDoctypeDeclHandler = self.end_doctype_decl_handler

    def end_doctype_decl_handler(self):
        if self._options.comments:
            self._parser.CommentHandler = self.comment_handler
        self._parser.ProcessingInstructionHandler = self.pi_handler
        if not (self._elem_info or self._filter):
            self._finish_end_element = id

    def pi_handler(self, target, data):
        node = self.document.createProcessingInstruction(target, data)
        _append_child(self.curNode, node)
        if self._filter and self._filter.acceptNode(node) == 拒绝过滤:
            self.curNode.removeChild(node)

    def character_data_handler_cdata(self, data):
        childNodes = self.curNode.childNodes
        if self._cdata:
            if self._cdata_continue and childNodes[-1].nodeType == CDATA节节点:
                childNodes[-1].appendData(data)
                return
            node = self.document.createCDATASection(data)
            self._cdata_continue = True
        elif childNodes and childNodes[-1].nodeType == 文本节点:
            node = childNodes[-1]
            value = node.data + data
            node.data = value
            return
        else:
            node = minidom.Text()
            node.data = data
            node.ownerDocument = self.document
        _append_child(self.curNode, node)

    def character_data_handler(self, data):
        childNodes = self.curNode.childNodes
        if childNodes and childNodes[-1].nodeType == 文本节点:
            node = childNodes[-1]
            node.data = node.data + data
            return
        node = minidom.Text()
        node.data = node.data + data
        node.ownerDocument = self.document
        _append_child(self.curNode, node)

    def entity_decl_handler(self, entityName, is_parameter_entity, value, base, systemId, publicId, notationName):
        if is_parameter_entity:
            return
        if not self._options.entities:
            return
        node = self.document._create_entity(entityName, publicId, systemId, notationName)
        if value is not None:
            child = self.document.createTextNode(value)
            node.childNodes.append(child)
        self.document.doctype.entities._seq.append(node)
        if self._filter and self._filter.acceptNode(node) == 拒绝过滤:
            del self.document.doctype.entities._seq[-1]

    def notation_decl_handler(self, notationName, base, systemId, publicId):
        node = self.document._create_notation(notationName, publicId, systemId)
        self.document.doctype.notations._seq.append(node)
        if self._filter and self._filter.acceptNode(node) == 接受过滤:
            del self.document.doctype.notations._seq[-1]

    def comment_handler(self, data):
        node = self.document.createComment(data)
        _append_child(self.curNode, node)
        if self._filter and self._filter.acceptNode(node) == 拒绝过滤:
            self.curNode.removeChild(node)

    def start_cdata_section_handler(self):
        self._cdata = True
        self._cdata_continue = False

    def end_cdata_section_handler(self):
        self._cdata = False
        self._cdata_continue = False

    def external_entity_ref_handler(self, context, base, systemId, publicId):
        return 1

    def first_element_handler(self, name, attributes):
        if self._filter is None and (not self._elem_info):
            self._finish_end_element = id
        self.取解析器().StartElementHandler = self.start_element_handler
        self.start_element_handler(name, attributes)

    def start_element_handler(self, name, attributes):
        node = self.document.createElement(name)
        _append_child(self.curNode, node)
        self.curNode = node
        if attributes:
            for i in range(0, len(attributes), 2):
                a = minidom.Attr(attributes[i], EMPTY_NAMESPACE, None, EMPTY_PREFIX)
                value = attributes[i + 1]
                a.value = value
                a.ownerDocument = self.document
                _set_attribute_node(node, a)
        if node is not self.document.documentElement:
            self._finish_start_element(node)

    def _finish_start_element(self, node):
        if self._filter:
            if node is self.document.documentElement:
                return
            filt = self._filter.startContainer(node)
            if filt == 拒绝过滤:
                拒绝者(self)
            elif filt == 跳过过滤:
                跳过者(self)
            else:
                return
            self.curNode = node.parentNode
            node.parentNode.removeChild(node)
            node.unlink()

    def end_element_handler(self, name):
        curNode = self.curNode
        self.curNode = curNode.parentNode
        self._finish_end_element(curNode)

    def _finish_end_element(self, curNode):
        info = self._elem_info.get(curNode.tagName)
        if info:
            self._handle_white_text_nodes(curNode, info)
        if self._filter:
            if curNode is self.document.documentElement:
                return
            if self._filter.acceptNode(curNode) == 拒绝过滤:
                self.curNode.removeChild(curNode)
                curNode.unlink()

    def _handle_white_text_nodes(self, node, info):
        if self._options.whitespace_in_element_content or not info.isElementContent():
            return
        L = []
        for child in node.childNodes:
            if child.nodeType == 文本节点 and (not child.data.strip()):
                L.append(child)
        for child in L:
            node.removeChild(child)

    def element_decl_handler(self, name, model):
        info = self._elem_info.get(name)
        if info is None:
            self._elem_info[name] = 元素信息(name, model)
        else:
            assert info._model is None
            info._model = model

    def attlist_decl_handler(self, elem, name, type, default, required):
        info = self._elem_info.get(elem)
        if info is None:
            info = 元素信息(elem)
            self._elem_info[elem] = info
        info._attr_info.append([None, name, None, None, default, 0, type, required])

    def xml_decl_handler(self, version, encoding, standalone):
        self.document.version = version
        self.document.encoding = encoding
        if standalone >= 0:
            if standalone:
                self.document.standalone = True
            else:
                self.document.standalone = False
_装类转发(Expat构建器, {'createParser': '造解析器', 'getParser': '取解析器', 'install': '装上', 'parseFile': '解析文件', 'parseString': '解析字符串', 'reset': '重置'}, {'createParser': '造解析器', 'getParser': '取解析器', 'install': '装上', 'parseFile': '解析文件', 'parseString': '解析字符串', 'reset': '重置'})
_ALLOWED_FILTER_RETURNS = (接受过滤, 拒绝过滤, 跳过过滤)

class 过滤器可见性控制器(object):
    """Wrapper around a DOMBuilderFilter which implements the checks
    to make the whatToShow filter attribute work."""
    __slots__ = ('filter',)

    def __init__(self, filter):
        self.filter = filter

    def 开始容器(self, node):
        mask = self._nodetype_mask[node.nodeType]
        if self.filter.whatToShow & mask:
            val = self.filter.startContainer(node)
            if val == 中断过滤:
                raise 解析中止
            if val not in _ALLOWED_FILTER_RETURNS:
                raise ValueError('startContainer() returned illegal value: ' + repr(val))
            return val
        else:
            return 接受过滤

    def acceptNode(self, node):
        mask = self._nodetype_mask[node.nodeType]
        if self.filter.whatToShow & mask:
            val = self.filter.acceptNode(node)
            if val == 中断过滤:
                raise 解析中止
            if val == 跳过过滤:
                parent = node.parentNode
                for child in node.childNodes[:]:
                    parent.appendChild(child)
                return 拒绝过滤
            if val not in _ALLOWED_FILTER_RETURNS:
                raise ValueError('acceptNode() returned illegal value: ' + repr(val))
            return val
        else:
            return 接受过滤
    _nodetype_mask = {Node.ELEMENT_NODE: NodeFilter.SHOW_ELEMENT, Node.ATTRIBUTE_NODE: NodeFilter.SHOW_ATTRIBUTE, Node.TEXT_NODE: NodeFilter.SHOW_TEXT, Node.CDATA_SECTION_NODE: NodeFilter.SHOW_CDATA_SECTION, Node.ENTITY_REFERENCE_NODE: NodeFilter.SHOW_ENTITY_REFERENCE, Node.ENTITY_NODE: NodeFilter.SHOW_ENTITY, Node.PROCESSING_INSTRUCTION_NODE: NodeFilter.SHOW_PROCESSING_INSTRUCTION, Node.COMMENT_NODE: NodeFilter.SHOW_COMMENT, Node.DOCUMENT_NODE: NodeFilter.SHOW_DOCUMENT, Node.DOCUMENT_TYPE_NODE: NodeFilter.SHOW_DOCUMENT_TYPE, Node.DOCUMENT_FRAGMENT_NODE: NodeFilter.SHOW_DOCUMENT_FRAGMENT, Node.NOTATION_NODE: NodeFilter.SHOW_NOTATION}
_装类转发(过滤器可见性控制器, {'startContainer': '开始容器'}, {'startContainer': '开始容器'})

class 过滤器辅助器(object):
    __slots__ = ('_builder', '_level', '_old_start', '_old_end')

    def __init__(self, builder):
        self._level = 0
        self._builder = builder
        parser = builder._parser
        self._old_start = parser.StartElementHandler
        self._old_end = parser.EndElementHandler
        parser.StartElementHandler = self.start_element_handler
        parser.EndElementHandler = self.end_element_handler

class 拒绝者(过滤器辅助器):
    __slots__ = ()

    def __init__(self, builder):
        过滤器辅助器.__init__(self, builder)
        parser = builder._parser
        for name in ('ProcessingInstructionHandler', 'CommentHandler', 'CharacterDataHandler', 'StartCdataSectionHandler', 'EndCdataSectionHandler', 'ExternalEntityRefHandler'):
            setattr(parser, name, None)

    def start_element_handler(self, *args):
        self._level = self._level + 1

    def end_element_handler(self, *args):
        if self._level == 0:
            parser = self._builder._parser
            self._builder.install(parser)
            parser.StartElementHandler = self._old_start
            parser.EndElementHandler = self._old_end
        else:
            self._level = self._level - 1

class 跳过者(过滤器辅助器):
    __slots__ = ()

    def start_element_handler(self, *args):
        node = self._builder.curNode
        self._old_start(*args)
        if self._builder.curNode is not node:
            self._level = self._level + 1

    def end_element_handler(self, *args):
        if self._level == 0:
            self._builder._parser.StartElementHandler = self._old_start
            self._builder._parser.EndElementHandler = self._old_end
            self._builder = None
        else:
            self._level = self._level - 1
            self._old_end(*args)
_FRAGMENT_BUILDER_INTERNAL_SYSTEM_ID = 'http://xml.python.org/entities/fragment-builder/internal'
_FRAGMENT_BUILDER_TEMPLATE = '<!DOCTYPE wrapper\n  %%s [\n  <!ENTITY fragment-builder-internal\n    SYSTEM "%s">\n%%s\n]>\n<wrapper %%s\n>&fragment-builder-internal;</wrapper>' % _FRAGMENT_BUILDER_INTERNAL_SYSTEM_ID

class 片段构建器(Expat构建器):
    """Builder which constructs document fragments given XML source
    text and a context node.

    The context node is expected to provide information about the
    namespace declarations which are in scope at the start of the
    fragment.
    """

    def __init__(self, context, options=None):
        if context.nodeType == 文档节点:
            self.originalDocument = context
            self.context = context
        else:
            self.originalDocument = context.ownerDocument
            self.context = context
        Expat构建器.__init__(self, options)

    def 重置(self):
        Expat构建器.重置(self)
        self.fragment = None

    def 解析文件(self, file):
        """Parse a document fragment from a file object, returning the
        fragment node."""
        return self.解析字符串(file.read())

    def 解析字符串(self, string):
        """Parse a document fragment from a string, returning the
        fragment node."""
        self._source = string
        parser = self.取解析器()
        doctype = self.originalDocument.doctype
        ident = ''
        if doctype:
            subset = doctype.internalSubset or self._getDeclarations()
            if doctype.publicId:
                ident = 'PUBLIC "%s" "%s"' % (doctype.publicId, doctype.systemId)
            elif doctype.systemId:
                ident = 'SYSTEM "%s"' % doctype.systemId
        else:
            subset = ''
        nsattrs = self._getNSattrs()
        document = _FRAGMENT_BUILDER_TEMPLATE % (ident, subset, nsattrs)
        try:
            parser.Parse(document, True)
        except:
            self.重置()
            raise
        fragment = self.fragment
        self.重置()
        return fragment

    def _getDeclarations(self):
        """Re-create the internal subset from the DocumentType node.

        This is only needed if we don't already have the
        internalSubset as a string.
        """
        doctype = self.context.ownerDocument.doctype
        s = ''
        if doctype:
            for i in range(doctype.notations.length):
                notation = doctype.notations.item(i)
                if s:
                    s = s + '\n  '
                s = '%s<!NOTATION %s' % (s, notation.nodeName)
                if notation.publicId:
                    s = '%s PUBLIC "%s"\n             "%s">' % (s, notation.publicId, notation.systemId)
                else:
                    s = '%s SYSTEM "%s">' % (s, notation.systemId)
            for i in range(doctype.entities.length):
                entity = doctype.entities.item(i)
                if s:
                    s = s + '\n  '
                s = '%s<!ENTITY %s' % (s, entity.nodeName)
                if entity.publicId:
                    s = '%s PUBLIC "%s"\n             "%s"' % (s, entity.publicId, entity.systemId)
                elif entity.systemId:
                    s = '%s SYSTEM "%s"' % (s, entity.systemId)
                else:
                    s = '%s "%s"' % (s, entity.firstChild.data)
                if entity.notationName:
                    s = '%s NOTATION %s' % (s, entity.notationName)
                s = s + '>'
        return s

    def _getNSattrs(self):
        return ''

    def external_entity_ref_handler(self, context, base, systemId, publicId):
        if systemId == _FRAGMENT_BUILDER_INTERNAL_SYSTEM_ID:
            old_document = self.document
            old_cur_node = self.curNode
            parser = self._parser.ExternalEntityParserCreate(context)
            self.document = self.originalDocument
            self.fragment = self.document.createDocumentFragment()
            self.curNode = self.fragment
            try:
                parser.Parse(self._source, True)
            finally:
                self.curNode = old_cur_node
                self.document = old_document
                self._source = None
            return -1
        else:
            return Expat构建器.external_entity_ref_handler(self, context, base, systemId, publicId)
_装类转发(片段构建器, {'parseFile': '解析文件', 'parseString': '解析字符串', 'reset': '重置'}, {'getParser': '取解析器', 'parseFile': '解析文件', 'parseString': '解析字符串', 'reset': '重置'})

class 命名空间处理器:
    """Mix-in class for builders; adds support for namespaces."""

    def _initNamespaces(self):
        self._ns_ordered_prefixes = []

    def 造解析器(self):
        """Create a new namespace-handling parser."""
        parser = expat.ParserCreate(namespace_separator=' ')
        parser.namespace_prefixes = True
        return parser

    def 装上(self, parser):
        """Insert the namespace-handlers onto the parser."""
        Expat构建器.装上(self, parser)
        if self._options.namespace_declarations:
            parser.StartNamespaceDeclHandler = self.start_namespace_decl_handler

    def start_namespace_decl_handler(self, prefix, uri):
        """Push this namespace declaration on our storage."""
        self._ns_ordered_prefixes.append((prefix, uri))

    def start_element_handler(self, name, attributes):
        if ' ' in name:
            uri, localname, prefix, qname = _parse_ns_name(self, name)
        else:
            uri = EMPTY_NAMESPACE
            qname = name
            localname = None
            prefix = EMPTY_PREFIX
        node = minidom.Element(qname, uri, prefix, localname)
        node.ownerDocument = self.document
        _append_child(self.curNode, node)
        self.curNode = node
        if self._ns_ordered_prefixes:
            for prefix, uri in self._ns_ordered_prefixes:
                if prefix:
                    a = minidom.Attr(_intern(self, 'xmlns:' + prefix), XMLNS_NAMESPACE, prefix, 'xmlns')
                else:
                    a = minidom.Attr('xmlns', XMLNS_NAMESPACE, 'xmlns', EMPTY_PREFIX)
                a.value = uri
                a.ownerDocument = self.document
                _set_attribute_node(node, a)
            del self._ns_ordered_prefixes[:]
        if attributes:
            node._ensure_attributes()
            _attrs = node._attrs
            _attrsNS = node._attrsNS
            for i in range(0, len(attributes), 2):
                aname = attributes[i]
                value = attributes[i + 1]
                if ' ' in aname:
                    uri, localname, prefix, qname = _parse_ns_name(self, aname)
                    a = minidom.Attr(qname, uri, localname, prefix)
                    _attrs[qname] = a
                    _attrsNS[uri, localname] = a
                else:
                    a = minidom.Attr(aname, EMPTY_NAMESPACE, aname, EMPTY_PREFIX)
                    _attrs[aname] = a
                    _attrsNS[EMPTY_NAMESPACE, aname] = a
                a.ownerDocument = self.document
                a.value = value
                a.ownerElement = node
    if __debug__:

        def end_element_handler(self, name):
            curNode = self.curNode
            if ' ' in name:
                uri, localname, prefix, qname = _parse_ns_name(self, name)
                assert curNode.namespaceURI == uri and curNode.localName == localname and (curNode.prefix == prefix), 'element stack messed up! (namespace)'
            else:
                assert curNode.nodeName == name, 'element stack messed up - bad nodeName'
                assert curNode.namespaceURI == EMPTY_NAMESPACE, 'element stack messed up - bad namespaceURI'
            self.curNode = curNode.parentNode
            self._finish_end_element(curNode)
_装类转发(命名空间处理器, {'createParser': '造解析器', 'install': '装上'}, {'createParser': '造解析器', 'install': '装上'})

class Expat构建器NS(命名空间处理器, Expat构建器):
    """Document builder that supports namespaces."""

    def 重置(self):
        Expat构建器.重置(self)
        self._initNamespaces()
_装类转发(Expat构建器NS, {'reset': '重置'}, {'reset': '重置'})

class 片段构建器NS(命名空间处理器, 片段构建器):
    """Fragment builder that supports namespaces."""

    def 重置(self):
        片段构建器.重置(self)
        self._initNamespaces()

    def _getNSattrs(self):
        """Return string of namespace attributes from this element and
        ancestors."""
        attrs = ''
        context = self.context
        L = []
        while context:
            if hasattr(context, '_ns_prefix_uri'):
                for prefix, uri in context._ns_prefix_uri.items():
                    if prefix in L:
                        continue
                    L.append(prefix)
                    if prefix:
                        declname = 'xmlns:' + prefix
                    else:
                        declname = 'xmlns'
                    if attrs:
                        attrs = "%s\n    %s='%s'" % (attrs, declname, uri)
                    else:
                        attrs = " %s='%s'" % (declname, uri)
            context = context.parentNode
        return attrs
_装类转发(片段构建器NS, {'reset': '重置'}, {'reset': '重置'})

class 解析中止(Exception):
    """Exception raised to short-circuit parsing in InternalSubsetExtractor."""
    pass

class 内部子集提取器(Expat构建器):
    """XML processor which can rip out the internal document type subset."""
    subset = None

    def 取子集(self):
        """Return the internal subset as a string."""
        return self.subset

    def 解析文件(self, file):
        try:
            Expat构建器.解析文件(self, file)
        except 解析中止:
            pass

    def 解析字符串(self, string):
        try:
            Expat构建器.解析字符串(self, string)
        except 解析中止:
            pass

    def 装上(self, parser):
        parser.StartDoctypeDeclHandler = self.start_doctype_decl_handler
        parser.StartElementHandler = self.start_element_handler

    def start_doctype_decl_handler(self, name, publicId, systemId, has_internal_subset):
        if has_internal_subset:
            parser = self.取解析器()
            self.subset = []
            parser.DefaultHandler = self.subset.append
            parser.EndDoctypeDeclHandler = self.end_doctype_decl_handler
        else:
            raise 解析中止()

    def end_doctype_decl_handler(self):
        s = ''.join(self.subset).replace('\r\n', '\n').replace('\r', '\n')
        self.subset = s
        raise 解析中止()

    def start_element_handler(self, name, attrs):
        raise 解析中止()
_装类转发(内部子集提取器, {'getSubset': '取子集', 'install': '装上', 'parseFile': '解析文件', 'parseString': '解析字符串'}, {'getParser': '取解析器', 'getSubset': '取子集', 'install': '装上', 'parseFile': '解析文件', 'parseString': '解析字符串'})

def 解析(file, namespaces=True):
    """Parse a document, returning the resulting Document node.

    'file' may be either a file name or an open file object.
    """
    if namespaces:
        builder = Expat构建器NS()
    else:
        builder = Expat构建器()
    if isinstance(file, str):
        with open(file, 'rb') as fp:
            result = builder.parseFile(fp)
    else:
        result = builder.parseFile(file)
    return result

def 解析字符串(string, namespaces=True):
    """Parse a document from a string, returning the resulting
    Document node.
    """
    if namespaces:
        builder = Expat构建器NS()
    else:
        builder = Expat构建器()
    return builder.parseString(string)

def 解析片段(file, context, namespaces=True):
    """Parse a fragment of a document, given the context from which it
    was originally extracted.  context should be the parent of the
    node(s) which are in the fragment.

    'file' may be either a file name or an open file object.
    """
    if namespaces:
        builder = 片段构建器NS(context)
    else:
        builder = 片段构建器(context)
    if isinstance(file, str):
        with open(file, 'rb') as fp:
            result = builder.parseFile(fp)
    else:
        result = builder.parseFile(file)
    return result

def 解析片段字符串(string, context, namespaces=True):
    """Parse a fragment of a document from a string, given the context
    from which it was originally extracted.  context should be the
    parent of the node(s) which are in the fragment.
    """
    if namespaces:
        builder = 片段构建器NS(context)
    else:
        builder = 片段构建器(context)
    return builder.parseString(string)

def 造构建器(options):
    """Create a builder based on an Options object."""
    if options.namespaces:
        return Expat构建器NS(options)
    else:
        return Expat构建器(options)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'CDATA_SECTION_NODE': 'CDATA节节点',
    'DOCUMENT_NODE': '文档节点',
    'ElementInfo': '元素信息',
    'ExpatBuilder': 'Expat构建器',
    'ExpatBuilderNS': 'Expat构建器NS',
    'FILTER_ACCEPT': '接受过滤',
    'FILTER_INTERRUPT': '中断过滤',
    'FILTER_REJECT': '拒绝过滤',
    'FILTER_SKIP': '跳过过滤',
    'FilterCrutch': '过滤器辅助器',
    'FilterVisibilityController': '过滤器可见性控制器',
    'FragmentBuilder': '片段构建器',
    'FragmentBuilderNS': '片段构建器NS',
    'InternalSubsetExtractor': '内部子集提取器',
    'Namespaces': '命名空间处理器',
    'ParseEscape': '解析中止',
    'Rejecter': '拒绝者',
    'Skipper': '跳过者',
    'TEXT_NODE': '文本节点',
    'makeBuilder': '造构建器',
    'parse': '解析',
    'parseFragment': '解析片段',
    'parseFragmentString': '解析片段字符串',
    'parseString': '解析字符串',
    'theDOMImplementation': '本DOM实现',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'Expat构建器': {
        'createParser': '造解析器',
        'getParser': '取解析器',
        'install': '装上',
        'parseFile': '解析文件',
        'parseString': '解析字符串',
        'reset': '重置',
    },
    'Expat构建器NS': {
        'reset': '重置',
    },
    '内部子集提取器': {
        'getSubset': '取子集',
        'install': '装上',
        'parseFile': '解析文件',
        'parseString': '解析字符串',
    },
    '命名空间处理器': {
        'createParser': '造解析器',
        'install': '装上',
    },
    '片段构建器': {
        'parseFile': '解析文件',
        'parseString': '解析字符串',
        'reset': '重置',
    },
    '片段构建器NS': {
        'reset': '重置',
    },
    '过滤器可见性控制器': {
        'startContainer': '开始容器',
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
    'Expat构建器': {
        'createParser': '造解析器',
        'getParser': '取解析器',
        'install': '装上',
        'parseFile': '解析文件',
        'parseString': '解析字符串',
        'reset': '重置',
    },
    'Expat构建器NS': {
        'reset': '重置',
    },
    '内部子集提取器': {
        'getParser': '取解析器',
        'getSubset': '取子集',
        'install': '装上',
        'parseFile': '解析文件',
        'parseString': '解析字符串',
    },
    '命名空间处理器': {
        'createParser': '造解析器',
        'install': '装上',
    },
    '片段构建器': {
        'getParser': '取解析器',
        'parseFile': '解析文件',
        'parseString': '解析字符串',
        'reset': '重置',
    },
    '片段构建器NS': {
        'reset': '重置',
    },
    '过滤器可见性控制器': {
        'startContainer': '开始容器',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
