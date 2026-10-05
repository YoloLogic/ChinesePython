# -*- coding: utf-8 -*-
"""XML工具.sax/handler —— 汉语库（由 tools/汉化库.py 从 Lib/xml/sax/handler.py 机械生成，**不要手改**）。

英文库 Lib/xml.sax/handler.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


"""
This module contains the core classes of version 2.0 of SAX for Python.
This file provides only default classes with absolutely minimum
functionality, from which drivers and applications can be subclassed.

Many of these classes are empty and are included only as documentation
of the interfaces.

$Id$
"""
_英文原名表 = {'ContentHandler': '内容处理器', 'DTDHandler': 'DTD处理器', 'EntityResolver': '实体解析器', 'ErrorHandler': '错误处理器', 'LexicalHandler': '词法处理器', 'all_features': '全部特性', 'all_properties': '全部属性', 'feature_external_ges': '外部通用实体特性', 'feature_external_pes': '外部参数实体特性', 'feature_namespace_prefixes': '命名空间前缀特性', 'feature_namespaces': '命名空间特性', 'feature_string_interning': '字符串驻留特性', 'feature_validation': '校验特性', 'property_declaration_handler': '声明处理器属性', 'property_dom_node': 'DOM节点属性', 'property_encoding': '编码属性', 'property_interning_dict': '驻留字典属性', 'property_lexical_handler': '词法处理器属性', 'property_xml_string': 'XML字符串属性', 'version': '版本'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
版本 = '2.0beta'

class 错误处理器:
    """Basic interface for SAX error handlers.

    If you create an object that implements this interface, then
    register the object with your XMLReader, the parser will call the
    methods in your object to report all warnings and errors. There
    are three levels of errors available: warnings, (possibly)
    recoverable errors, and unrecoverable errors. All methods take a
    SAXParseException as the only parameter."""

    def error(self, exception):
        """Handle a recoverable error."""
        raise exception

    def fatalError(self, exception):
        """Handle a non-recoverable error."""
        raise exception

    def warning(self, exception):
        """Handle a warning."""
        print(exception)

class 内容处理器:
    """Interface for receiving logical document content events.

    This is the main callback interface in SAX, and the one most
    important to applications. The order of events in this interface
    mirrors the order of the information in the document."""

    def __init__(self):
        self._locator = None

    def setDocumentLocator(self, locator):
        """Called by the parser to give the application a locator for
        locating the origin of document events.

        SAX parsers are strongly encouraged (though not absolutely
        required) to supply a locator: if it does so, it must supply
        the locator to the application by invoking this method before
        invoking any of the other methods in the DocumentHandler
        interface.

        The locator allows the application to determine the end
        position of any document-related event, even if the parser is
        not reporting an error. Typically, the application will use
        this information for reporting its own errors (such as
        character content that does not match an application's
        business rules). The information returned by the locator is
        probably not sufficient for use with a search engine.

        Note that the locator will return correct information only
        during the invocation of the events in this interface. The
        application should not attempt to use it at any other time."""
        self._locator = locator

    def startDocument(self):
        """Receive notification of the beginning of a document.

        The SAX parser will invoke this method only once, before any
        other methods in this interface or in DTDHandler (except for
        setDocumentLocator)."""

    def endDocument(self):
        """Receive notification of the end of a document.

        The SAX parser will invoke this method only once, and it will
        be the last method invoked during the parse. The parser shall
        not invoke this method until it has either abandoned parsing
        (because of an unrecoverable error) or reached the end of
        input."""

    def startPrefixMapping(self, prefix, uri):
        """Begin the scope of a prefix-URI Namespace mapping.

        The information from this event is not necessary for normal
        Namespace processing: the SAX XML reader will automatically
        replace prefixes for element and attribute names when the
        http://xml.org/sax/features/namespaces feature is true (the
        default).

        There are cases, however, when applications need to use
        prefixes in character data or in attribute values, where they
        cannot safely be expanded automatically; the
        start/endPrefixMapping event supplies the information to the
        application to expand prefixes in those contexts itself, if
        necessary.

        Note that start/endPrefixMapping events are not guaranteed to
        be properly nested relative to each-other: all
        startPrefixMapping events will occur before the corresponding
        startElement event, and all endPrefixMapping events will occur
        after the corresponding endElement event, but their order is
        not guaranteed."""

    def endPrefixMapping(self, prefix):
        """End the scope of a prefix-URI mapping.

        See startPrefixMapping for details. This event will always
        occur after the corresponding endElement event, but the order
        of endPrefixMapping events is not otherwise guaranteed."""

    def startElement(self, name, attrs):
        """Signals the start of an element in non-namespace mode.

        The name parameter contains the raw XML 1.0 name of the
        element type as a string and the attrs parameter holds an
        instance of the Attributes class containing the attributes of
        the element."""

    def endElement(self, name):
        """Signals the end of an element in non-namespace mode.

        The name parameter contains the name of the element type, just
        as with the startElement event."""

    def startElementNS(self, name, qname, attrs):
        """Signals the start of an element in namespace mode.

        The name parameter contains the name of the element type as a
        (uri, localname) tuple, the qname parameter the raw XML 1.0
        name used in the source document, and the attrs parameter
        holds an instance of the Attributes class containing the
        attributes of the element.

        The uri part of the name tuple is None for elements which have
        no namespace."""

    def endElementNS(self, name, qname):
        """Signals the end of an element in namespace mode.

        The name parameter contains the name of the element type, just
        as with the startElementNS event."""

    def characters(self, content):
        """Receive notification of character data.

        The Parser will call this method to report each chunk of
        character data. SAX parsers may return all contiguous
        character data in a single chunk, or they may split it into
        several chunks; however, all of the characters in any single
        event must come from the same external entity so that the
        Locator provides useful information."""

    def ignorableWhitespace(self, whitespace):
        """Receive notification of ignorable whitespace in element content.

        Validating Parsers must use this method to report each chunk
        of ignorable whitespace (see the W3C XML 1.0 recommendation,
        section 2.10): non-validating parsers may also use this method
        if they are capable of parsing and using content models.

        SAX parsers may return all contiguous whitespace in a single
        chunk, or they may split it into several chunks; however, all
        of the characters in any single event must come from the same
        external entity, so that the Locator provides useful
        information."""

    def processingInstruction(self, target, data):
        """Receive notification of a processing instruction.

        The Parser will invoke this method once for each processing
        instruction found: note that processing instructions may occur
        before or after the main document element.

        A SAX parser should never report an XML declaration (XML 1.0,
        section 2.8) or a text declaration (XML 1.0, section 4.3.1)
        using this method."""

    def skippedEntity(self, name):
        """Receive notification of a skipped entity.

        The Parser will invoke this method once for each entity
        skipped. Non-validating processors may skip entities if they
        have not seen the declarations (because, for example, the
        entity was declared in an external DTD subset). All processors
        may skip external entities, depending on the values of the
        http://xml.org/sax/features/external-general-entities and the
        http://xml.org/sax/features/external-parameter-entities
        properties."""

class DTD处理器:
    """Handle DTD events.

    This interface specifies only those DTD events required for basic
    parsing (unparsed entities and attributes)."""

    def notationDecl(self, name, publicId, systemId):
        """Handle a notation declaration event."""

    def unparsedEntityDecl(self, name, publicId, systemId, ndata):
        """Handle an unparsed entity declaration event."""

class 实体解析器:
    """Basic interface for resolving entities. If you create an object
    implementing this interface, then register the object with your
    Parser, the parser will call the method in your object to
    resolve all external entities. Note that DefaultHandler implements
    this interface with the default behaviour."""

    def resolveEntity(self, publicId, systemId):
        """Resolve the system identifier of an entity and return either
        the system identifier to read from as a string, or an InputSource
        to read from."""
        return systemId
命名空间特性 = 'http://xml.org/sax/features/namespaces'
命名空间前缀特性 = 'http://xml.org/sax/features/namespace-prefixes'
字符串驻留特性 = 'http://xml.org/sax/features/string-interning'
校验特性 = 'http://xml.org/sax/features/validation'
外部通用实体特性 = 'http://xml.org/sax/features/external-general-entities'
外部参数实体特性 = 'http://xml.org/sax/features/external-parameter-entities'
全部特性 = [命名空间特性, 命名空间前缀特性, 字符串驻留特性, 校验特性, 外部通用实体特性, 外部参数实体特性]
词法处理器属性 = 'http://xml.org/sax/properties/lexical-handler'
声明处理器属性 = 'http://xml.org/sax/properties/declaration-handler'
DOM节点属性 = 'http://xml.org/sax/properties/dom-node'
XML字符串属性 = 'http://xml.org/sax/properties/xml-string'
编码属性 = 'http://www.python.org/sax/properties/encoding'
驻留字典属性 = 'http://www.python.org/sax/properties/interning-dict'
全部属性 = [词法处理器属性, DOM节点属性, 声明处理器属性, XML字符串属性, 编码属性, 驻留字典属性]

class 词法处理器:
    """Optional SAX2 handler for lexical events.

    This handler is used to obtain lexical information about an XML
    document, that is, information about how the document was encoded
    (as opposed to what it contains, which is reported to the
    ContentHandler), such as comments and CDATA marked section
    boundaries.

    To set the LexicalHandler of an XMLReader, use the setProperty
    method with the property identifier
    'http://xml.org/sax/properties/lexical-handler'."""

    def comment(self, content):
        """Reports a comment anywhere in the document (including the
        DTD and outside the document element).

        content is a string that holds the contents of the comment."""

    def startDTD(self, name, public_id, system_id):
        """Report the start of the DTD declarations, if the document
        has an associated DTD.

        A startEntity event will be reported before declaration events
        from the external DTD subset are reported, and this can be
        used to infer from which subset DTD declarations derive.

        name is the name of the document element type, public_id the
        public identifier of the DTD (or None if none were supplied)
        and system_id the system identifier of the external subset (or
        None if none were supplied)."""

    def endDTD(self):
        """Signals the end of DTD declarations."""

    def startCDATA(self):
        """Reports the beginning of a CDATA marked section.

        The contents of the CDATA marked section will be reported
        through the characters event."""

    def endCDATA(self):
        """Reports the end of a CDATA marked section."""


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'ContentHandler': '内容处理器',
    'DTDHandler': 'DTD处理器',
    'EntityResolver': '实体解析器',
    'ErrorHandler': '错误处理器',
    'LexicalHandler': '词法处理器',
    'all_features': '全部特性',
    'all_properties': '全部属性',
    'feature_external_ges': '外部通用实体特性',
    'feature_external_pes': '外部参数实体特性',
    'feature_namespace_prefixes': '命名空间前缀特性',
    'feature_namespaces': '命名空间特性',
    'feature_string_interning': '字符串驻留特性',
    'feature_validation': '校验特性',
    'property_declaration_handler': '声明处理器属性',
    'property_dom_node': 'DOM节点属性',
    'property_encoding': '编码属性',
    'property_interning_dict': '驻留字典属性',
    'property_lexical_handler': '词法处理器属性',
    'property_xml_string': 'XML字符串属性',
    'version': '版本',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
