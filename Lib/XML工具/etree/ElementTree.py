# -*- coding: utf-8 -*-
"""XML工具.etree/ElementTree —— 汉语库（由 tools/汉化库.py 从 Lib/xml/etree/ElementTree.py 机械生成，**不要手改**）。

英文库 Lib/xml.etree/ElementTree.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


"""Lightweight XML support for Python.

 XML is an inherently hierarchical data format, and the most natural way to
 represent it is with a tree.  This module has two classes for this purpose:

    1. ElementTree represents the whole XML document as a tree and

    2. Element represents a single node in this tree.

 Interactions with the whole document (reading and writing to/from files) are
 usually done on the ElementTree level.  Interactions with a single XML
 element and its sub-elements are done on the Element level.

 Element is a flexible container object designed to store hierarchical data
 structures in memory. It can be described as a cross between a list and a
 dictionary.  Each Element has a number of properties associated with it:

    'tag' - a string containing the element's name.

    'attributes' - a Python dictionary storing the element's attributes.

    'text' - a string containing the element's text content.

    'tail' - an optional string containing text after the element's end tag.

    And a number of child elements stored in a Python sequence.

 To create an element instance, use the Element constructor,
 or the SubElement factory function.

 You can also use the ElementTree class to wrap an element structure
 and convert it to and from XML.

"""
_英文原名表 = {'C14NWriterTarget': '规范化写出目标', 'Comment': '注释', 'Element': '元素', 'ElementTree': '元素树', 'HTML_EMPTY': 'HTML空元素表', 'PI': '处理指令简写', 'ParseError': '解析错误', 'ProcessingInstruction': '处理指令', 'QName': '限定名', 'SubElement': '子元素', 'TreeBuilder': '树构建器', 'VERSION': '版本', 'XML': 'XML命名空间', 'XMLID': '解析XMLID', 'XMLParser': 'XML解析器', 'XMLPullParser': 'XML拉取解析器', 'canonicalize': '规范化', 'dump': '转储', 'fromstring': '从字符串解析', 'fromstringlist': '从字符串表解析', 'indent': '缩进', 'iselement': '是元素吗', 'iterparse': '迭代解析', 'parse': '解析', 'register_namespace': '登记命名空间', 'tostring': '转字符串', 'tostringlist': '转字符串表'}

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
__all__ = ['Comment', 'dump', 'Element', 'ElementTree', 'fromstring', 'fromstringlist', 'indent', 'iselement', 'iterparse', 'parse', 'ParseError', 'PI', 'ProcessingInstruction', 'QName', 'SubElement', 'tostring', 'tostringlist', 'TreeBuilder', 'VERSION', 'XML', 'XMLID', 'XMLParser', 'XMLPullParser', 'register_namespace', 'canonicalize', 'C14NWriterTarget']
版本 = '1.3.0'
import sys
import re
import warnings
import io
import collections
import collections.abc
import contextlib
import weakref
from . import ElementPath

class 解析错误(SyntaxError):
    """An error when parsing an XML document.

    In addition to its exception value, a ParseError contains
    two extra attributes:
        'code'     - the specific exception code
        'position' - the line and column of the error

    """
    pass

def 是元素吗(element):
    """Return True if *element* appears to be an Element."""
    return hasattr(element, 'tag')

class 元素:
    """An XML element.

    This class is the reference implementation of the Element interface.

    An element's length is its number of subelements.  That means if you
    want to check if an element is truly empty, you should check BOTH
    its length AND its text attribute.

    The element tag, attribute names, and attribute values can be either
    bytes or strings.

    *tag* is the element name.  *attrib* is an optional dictionary containing
    element attributes. *extra* are additional element attributes given as
    keyword arguments.

    Example form:
        <tag attrib>text<child/>...</tag>tail

    """
    tag = None
    "The element's name."
    attrib = None
    "Dictionary of the element's attributes."
    text = None
    '\n    Text before first subelement. This is either a string or the value None.\n    Note that if there is no text, this attribute may be either\n    None or the empty string, depending on the parser.\n\n    '
    tail = None
    "\n    Text after this element's end tag, but before the next sibling element's\n    start tag.  This is either a string or the value None.  Note that if there\n    was no text, this attribute may be either None or an empty string,\n    depending on the parser.\n\n    "

    def __init__(self, tag, attrib={}, **extra):
        if not isinstance(attrib, dict):
            raise TypeError('attrib must be dict, not %s' % (attrib.__class__.__name__,))
        self.tag = tag
        self.attrib = {**attrib, **extra}
        self._children = []

    def __repr__(self):
        return '<%s %r at %#x>' % (self.__class__.__name__, self.tag, id(self))

    def makeelement(self, tag, attrib):
        """Create a new element with the same type.

        *tag* is a string containing the element name.
        *attrib* is a dictionary containing the element attributes.

        Do not call this method, use the SubElement factory function instead.

        """
        return self.__class__(tag, attrib)

    def __copy__(self):
        elem = self.makeelement(self.tag, self.attrib)
        elem.text = self.text
        elem.tail = self.tail
        elem[:] = self
        return elem

    def __len__(self):
        return len(self._children)

    def __bool__(self):
        warnings.warn("Testing an element's truth value will always return True in future versions.  Use specific 'len(elem)' or 'elem is not None' test instead.", DeprecationWarning, stacklevel=2)
        return len(self._children) != 0

    def __getitem__(self, index):
        return self._children[index]

    def __setitem__(self, index, element):
        if isinstance(index, slice):
            for elt in element:
                self._assert_is_element(elt)
        else:
            self._assert_is_element(element)
        self._children[index] = element

    def __delitem__(self, index):
        del self._children[index]

    def append(self, subelement):
        """Add *subelement* to the end of this element.

        The new element will appear in document order after the last existing
        subelement (or directly after the text, if it's the first subelement),
        but before the end tag for this element.

        """
        self._assert_is_element(subelement)
        self._children.append(subelement)

    def extend(self, elements):
        """Append subelements from a sequence.

        *elements* is a sequence with zero or more elements.

        """
        for element in elements:
            self._assert_is_element(element)
            self._children.append(element)

    def insert(self, index, subelement):
        """Insert *subelement* at position *index*."""
        self._assert_is_element(subelement)
        self._children.insert(index, subelement)

    def _assert_is_element(self, e):
        if not isinstance(e, _Element_Py):
            raise TypeError('expected an Element, not %s' % type(e).__name__)

    def remove(self, subelement):
        """Remove matching subelement.

        Unlike the find methods, this method compares elements based on
        identity, NOT ON tag value or contents.  To remove subelements by
        other means, the easiest way is to use a list comprehension to
        select what elements to keep, and then use slice assignment to update
        the parent element.

        ValueError is raised if a matching element could not be found.

        """
        try:
            self._children.remove(subelement)
        except ValueError:
            raise ValueError('Element.remove(x): element not found') from None

    def find(self, path, namespaces=None):
        """Find first matching element by tag name or path.

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full
        name.

        Return the first matching element, or None if no element was found.

        """
        return ElementPath.find(self, path, namespaces)

    def 查找文本(self, path, default=None, namespaces=None):
        """Find text for first matching element by tag name or path.

        *path* is a string having either an element tag or an XPath,
        *default* is the value to return if the element was not found,
        *namespaces* is an optional mapping from namespace prefix to full
        name.

        Return text content of first matching element, or default value if
        none was found.  Note that if an element is found having no text
        content, the empty string is returned.

        """
        return ElementPath.findtext(self, path, default, namespaces)

    def findall(self, path, namespaces=None):
        """Find all matching subelements by tag name or path.

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full
        name.

        Returns list containing all matching elements in document order.

        """
        return ElementPath.findall(self, path, namespaces)

    def 迭代查找(self, path, namespaces=None):
        """Find all matching subelements by tag name or path.

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full
        name.

        Return an iterable yielding all matching elements in document order.

        """
        return ElementPath.iterfind(self, path, namespaces)

    def clear(self):
        """Reset element.

        This function removes all subelements, clears all attributes, and sets
        the text and tail attributes to None.

        """
        self.attrib.clear()
        self._children = []
        self.text = self.tail = None

    def get(self, key, default=None):
        """Get element attribute.

        Equivalent to attrib.get, but some implementations may handle this a
        bit more efficiently.  *key* is what attribute to look for, and
        *default* is what to return if the attribute was not found.

        Returns a string containing the attribute value, or the default if
        attribute was not found.

        """
        return self.attrib.get(key, default)

    def set(self, key, value):
        """Set element attribute.

        Equivalent to attrib[key] = value, but some implementations may handle
        this a bit more efficiently.  *key* is what attribute to set, and
        *value* is the attribute value to set it to.

        """
        self.attrib[key] = value

    def keys(self):
        """Get list of attribute names.

        Names are returned in an arbitrary order, just like an ordinary
        Python dict.  Equivalent to attrib.keys()

        """
        return self.attrib.keys()

    def items(self):
        """Get element attributes as a sequence.

        The attributes are returned in arbitrary order.  Equivalent to
        attrib.items().

        Return a list of (name, value) tuples.

        """
        return self.attrib.items()

    def iter(self, tag=None):
        """Create tree iterator.

        The iterator loops over the element and all subelements in document
        order, returning all elements with a matching tag.

        If the tree structure is modified during iteration, new or removed
        elements may or may not be included.  To get a stable set, use the
        list() function on the iterator, and loop over the resulting list.

        *tag* is what tags to look for (default is to return all elements)

        Return an iterator containing all the matching elements.

        """
        if tag == '*':
            tag = None
        if tag is None or self.tag == tag:
            yield self
        for e in self._children:
            yield from e.iter(tag)

    def itertext(self):
        """Create text iterator.

        The iterator loops over the element and all subelements in document
        order, returning all inner text.

        """
        tag = self.tag
        if not isinstance(tag, str) and tag is not None:
            return
        t = self.text
        if t:
            yield t
        for e in self:
            yield from e.itertext()
            t = e.tail
            if t:
                yield t
_装类转发(元素, {'findtext': '查找文本', 'iterfind': '迭代查找'}, {'findtext': '查找文本', 'iterfind': '迭代查找'})

def 子元素(parent, tag, attrib={}, **extra):
    """Subelement factory which creates an element instance, and appends it
    to an existing parent.

    The element tag, attribute names, and attribute values can be either
    bytes or Unicode strings.

    *parent* is the parent element, *tag* is the subelements name, *attrib* is
    an optional directory containing element attributes, *extra* are
    additional attributes given as keyword arguments.

    """
    attrib = {**attrib, **extra}
    element = parent.makeelement(tag, attrib)
    parent.append(element)
    return element

def 注释(text=None):
    """Comment element factory.

    This function creates a special element which the standard serializer
    serializes as an XML comment.

    *text* is a string containing the comment string.

    """
    element = 元素(注释)
    element.text = text
    return element

def 处理指令(target, text=None):
    """Processing Instruction element factory.

    This function creates a special element which the standard serializer
    serializes as an XML comment.

    *target* is a string containing the processing instruction, *text* is a
    string containing the processing instruction contents, if any.

    """
    element = 元素(处理指令)
    element.text = target
    if text:
        element.text = element.text + ' ' + text
    return element
处理指令简写 = 处理指令

class 限定名:
    """Qualified name wrapper.

    This class can be used to wrap a QName attribute value in order to get
    proper namespace handing on output.

    *text_or_uri* is a string containing the QName value either in the form
    {uri}local, or if the tag argument is given, the URI part of a QName.

    *tag* is an optional argument which if given, will make the first
    argument (text_or_uri) be interpreted as a URI, and this argument (tag)
    be interpreted as a local name.

    """

    def __init__(self, text_or_uri, tag=None):
        if tag:
            text_or_uri = '{%s}%s' % (text_or_uri, tag)
        self.text = text_or_uri

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.text)

    def __hash__(self):
        return hash(self.text)

    def __le__(self, other):
        if isinstance(other, 限定名):
            return self.text <= other.text
        return self.text <= other

    def __lt__(self, other):
        if isinstance(other, 限定名):
            return self.text < other.text
        return self.text < other

    def __ge__(self, other):
        if isinstance(other, 限定名):
            return self.text >= other.text
        return self.text >= other

    def __gt__(self, other):
        if isinstance(other, 限定名):
            return self.text > other.text
        return self.text > other

    def __eq__(self, other):
        if isinstance(other, 限定名):
            return self.text == other.text
        return self.text == other

class 元素树:
    """An XML element hierarchy.

    This class also provides support for serialization to and from
    standard XML.

    *element* is an optional root element node,
    *file* is an optional file handle or file name of an XML file whose
    contents will be used to initialize the tree with.

    """

    def __init__(self, element=None, file=None):
        if element is not None and (not 是元素吗(element)):
            raise TypeError('expected an Element, not %s' % type(element).__name__)
        self._root = element
        if file:
            self.解析(file)

    def 取根(self):
        """Return root element of this tree."""
        return self._root

    def _setroot(self, element):
        """Replace root element of this tree.

        This will discard the current contents of the tree and replace it
        with the given element.  Use with care!

        """
        if not 是元素吗(element):
            raise TypeError('expected an Element, not %s' % type(element).__name__)
        self._root = element

    def 解析(self, source, parser=None):
        """Load external XML document into element tree.

        *source* is a file name or file object, *parser* is an optional
        parser instance that defaults to XMLParser.

        ParseError is raised if the parser fails to parse the document.

        Returns the root element of the given source document.

        """
        close_source = False
        if not hasattr(source, 'read'):
            source = open(source, 'rb')
            close_source = True
        try:
            if parser is None:
                parser = XML解析器()
                if hasattr(parser, '_parse_whole'):
                    self._root = parser._parse_whole(source)
                    return self._root
            while (data := source.read(65536)):
                parser.feed(data)
            self._root = parser.close()
            return self._root
        finally:
            if close_source:
                source.close()

    def iter(self, tag=None):
        """Create and return tree iterator for the root element.

        The iterator loops over all elements in this tree, in document
        order.

        *tag* is a string with the tag name to iterate over
        (default is to return all elements).

        """
        return self._root.iter(tag)

    def find(self, path, namespaces=None):
        """Find first matching element by tag name or path.

        Same as getroot().find(path), which is Element.find()

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full
        name.

        Return the first matching element, or None if no element was found.

        """
        if path[:1] == '/':
            path = '.' + path
            warnings.warn('This search is broken in 1.3 and earlier, and will be fixed in a future version.  If you rely on the current behaviour, change it to %r' % path, FutureWarning, stacklevel=2)
        return self._root.find(path, namespaces)

    def 查找文本(self, path, default=None, namespaces=None):
        """Find first matching element by tag name or path.

        Same as getroot().findtext(path),  which is Element.findtext()

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full
        name.

        Return the first matching element, or None if no element was found.

        """
        if path[:1] == '/':
            path = '.' + path
            warnings.warn('This search is broken in 1.3 and earlier, and will be fixed in a future version.  If you rely on the current behaviour, change it to %r' % path, FutureWarning, stacklevel=2)
        return self._root.findtext(path, default, namespaces)

    def findall(self, path, namespaces=None):
        """Find all matching subelements by tag name or path.

        Same as getroot().findall(path), which is Element.findall().

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full
        name.

        Return list containing all matching elements in document order.

        """
        if path[:1] == '/':
            path = '.' + path
            warnings.warn('This search is broken in 1.3 and earlier, and will be fixed in a future version.  If you rely on the current behaviour, change it to %r' % path, FutureWarning, stacklevel=2)
        return self._root.findall(path, namespaces)

    def 迭代查找(self, path, namespaces=None):
        """Find all matching subelements by tag name or path.

        Same as getroot().iterfind(path), which is element.iterfind()

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return an iterable yielding all matching elements in document order.

        """
        if path[:1] == '/':
            path = '.' + path
            warnings.warn('This search is broken in 1.3 and earlier, and will be fixed in a future version.  If you rely on the current behaviour, change it to %r' % path, FutureWarning, stacklevel=2)
        return self._root.iterfind(path, namespaces)

    def 写出(self, file_or_filename, encoding=None, xml_declaration=None, default_namespace=None, method=None, *, short_empty_elements=True):
        """Write element tree to a file as XML.

        Arguments:
          *file_or_filename* -- file name or a file object opened for
                                writing

          *encoding* -- the output encoding (default: US-ASCII)

          *xml_declaration* -- bool indicating if an XML declaration should
                               be added to the output. If None, an XML
                               declaration is added if encoding IS NOT
                               either of: US-ASCII, UTF-8, or Unicode

          *default_namespace* -- sets the default XML namespace (for
                                 "xmlns")

          *method* -- either "xml" (default), "html, "text", or "c14n"

          *short_empty_elements* -- controls the formatting of elements
                                    that contain no content.  If True
                                    (default) they are emitted as a single
                                    self-closed tag, otherwise they are
                                    emitted as a pair of start/end tags

        """
        if self._root is None:
            raise TypeError('ElementTree not initialized')
        if not method:
            method = 'xml'
        elif method not in _serialize:
            raise ValueError('unknown method %r' % method)
        if not encoding:
            if method == 'c14n':
                encoding = 'utf-8'
            else:
                encoding = 'us-ascii'
        with _get_writer(file_or_filename, encoding) as (写出, declared_encoding):
            if method == 'xml' and (xml_declaration or (xml_declaration is None and encoding.lower() != 'unicode' and (declared_encoding.lower() not in ('utf-8', 'us-ascii')))):
                写出("<?xml version='1.0' encoding='%s'?>\n" % (declared_encoding,))
            if method == 'text':
                _serialize_text(写出, self._root)
            else:
                qnames, namespaces = _namespaces(self._root, default_namespace)
                serialize = _serialize[method]
                serialize(写出, self._root, qnames, namespaces, short_empty_elements=short_empty_elements)

    def write_c14n(self, file):
        return self.write(file, method='c14n')
_装类转发(元素树, {'findtext': '查找文本', 'getroot': '取根', 'iterfind': '迭代查找', 'parse': '解析', 'write': '写出'}, {'findtext': '查找文本', 'getroot': '取根', 'iterfind': '迭代查找', 'parse': '解析', 'write': '写出'})

@contextlib.contextmanager
def _get_writer(file_or_filename, encoding):
    try:
        写出 = file_or_filename.write
    except AttributeError:
        if encoding.lower() == 'unicode':
            encoding = 'utf-8'
        with open(file_or_filename, 'w', encoding=encoding, errors='xmlcharrefreplace') as file:
            yield (file.write, encoding)
    else:
        if encoding.lower() == 'unicode':
            yield (写出, getattr(file_or_filename, 'encoding', None) or 'utf-8')
        else:
            with contextlib.ExitStack() as stack:
                if isinstance(file_or_filename, io.BufferedIOBase):
                    file = file_or_filename
                elif isinstance(file_or_filename, io.RawIOBase):
                    file = io.BufferedWriter(file_or_filename)
                    stack.callback(file.detach)
                else:
                    file = io.BufferedIOBase()
                    file.writable = lambda: True
                    file.write = 写出
                    try:
                        file.seekable = file_or_filename.seekable
                        file.tell = file_or_filename.tell
                    except AttributeError:
                        pass
                file = io.TextIOWrapper(file, encoding=encoding, errors='xmlcharrefreplace', newline='\n')
                stack.callback(file.detach)
                yield (file.write, encoding)

def _namespaces(elem, default_namespace=None):
    qnames = {None: None}
    namespaces = {}
    if default_namespace:
        namespaces[default_namespace] = ''

    def add_qname(qname):
        try:
            if qname[:1] == '{':
                uri, tag = qname[1:].rsplit('}', 1)
                prefix = namespaces.get(uri)
                if prefix is None:
                    prefix = _namespace_map.get(uri)
                    if prefix is None:
                        prefix = 'ns%d' % len(namespaces)
                    if prefix != 'xml':
                        namespaces[uri] = prefix
                if prefix:
                    qnames[qname] = '%s:%s' % (prefix, tag)
                else:
                    qnames[qname] = tag
            else:
                if default_namespace:
                    raise ValueError('cannot use non-qualified names with default_namespace option')
                qnames[qname] = qname
        except TypeError:
            _raise_serialization_error(qname)
    for elem in elem.iter():
        tag = elem.tag
        if isinstance(tag, 限定名):
            if tag.text not in qnames:
                add_qname(tag.text)
        elif isinstance(tag, str):
            if tag not in qnames:
                add_qname(tag)
        elif tag is not None and tag is not 注释 and (tag is not 处理指令简写):
            _raise_serialization_error(tag)
        for key, value in elem.items():
            if isinstance(key, 限定名):
                key = key.text
            if key not in qnames:
                add_qname(key)
            if isinstance(value, 限定名) and value.text not in qnames:
                add_qname(value.text)
        text = elem.text
        if isinstance(text, 限定名) and text.text not in qnames:
            add_qname(text.text)
    return (qnames, namespaces)

def _serialize_xml(write, elem, qnames, namespaces, short_empty_elements, **kwargs):
    tag = elem.tag
    text = elem.text
    if tag is 注释:
        write('<!--%s-->' % text)
    elif tag is 处理指令:
        write('<?%s?>' % text)
    else:
        tag = qnames[tag]
        if tag is None:
            if text:
                write(_escape_cdata(text))
            for e in elem:
                _serialize_xml(write, e, qnames, None, short_empty_elements=short_empty_elements)
        else:
            write('<' + tag)
            items = list(elem.items())
            if items or namespaces:
                if namespaces:
                    for v, k in sorted(namespaces.items(), key=lambda x: x[1]):
                        if k:
                            k = ':' + k
                        write(' xmlns%s="%s"' % (k, _escape_attrib(v)))
                for k, v in items:
                    if isinstance(k, 限定名):
                        k = k.text
                    if isinstance(v, 限定名):
                        v = qnames[v.text]
                    else:
                        v = _escape_attrib(v)
                    write(' %s="%s"' % (qnames[k], v))
            if text or len(elem) or (not short_empty_elements):
                write('>')
                if text:
                    write(_escape_cdata(text))
                for e in elem:
                    _serialize_xml(write, e, qnames, None, short_empty_elements=short_empty_elements)
                write('</' + tag + '>')
            else:
                write(' />')
    if elem.tail:
        write(_escape_cdata(elem.tail))
_CDATA_CONTENT_ELEMENTS = {'script', 'style', 'xmp', 'iframe', 'noembed', 'noframes', 'plaintext'}
HTML空元素表 = {'area', 'base', 'basefont', 'br', 'col', 'embed', 'frame', 'hr', 'img', 'input', 'isindex', 'link', 'meta', 'param', 'source', 'track', 'wbr', 'plaintext'}

def _serialize_html(write, elem, qnames, namespaces, **kwargs):
    tag = elem.tag
    text = elem.text
    if tag is 注释:
        write('<!--%s-->' % _escape_cdata(text))
    elif tag is 处理指令:
        write('<?%s?>' % _escape_cdata(text))
    else:
        tag = qnames[tag]
        if tag is None:
            if text:
                write(_escape_cdata(text))
            for e in elem:
                _serialize_html(write, e, qnames, None)
        else:
            write('<' + tag)
            items = list(elem.items())
            if items or namespaces:
                if namespaces:
                    for v, k in sorted(namespaces.items(), key=lambda x: x[1]):
                        if k:
                            k = ':' + k
                        write(' xmlns%s="%s"' % (k, _escape_attrib(v)))
                for k, v in items:
                    if isinstance(k, 限定名):
                        k = k.text
                    if isinstance(v, 限定名):
                        v = qnames[v.text]
                    else:
                        v = _escape_attrib_html(v)
                    write(' %s="%s"' % (qnames[k], v))
            write('>')
            ltag = tag.lower()
            if text:
                if ltag in _CDATA_CONTENT_ELEMENTS:
                    write(text)
                else:
                    write(_escape_cdata(text))
            for e in elem:
                _serialize_html(write, e, qnames, None)
            if ltag not in HTML空元素表:
                write('</' + tag + '>')
    if elem.tail:
        write(_escape_cdata(elem.tail))

def _serialize_text(write, elem):
    for part in elem.itertext():
        write(part)
    if elem.tail:
        write(elem.tail)
_serialize = {'xml': _serialize_xml, 'html': _serialize_html, 'text': _serialize_text}

def 登记命名空间(prefix, uri):
    """Register a namespace prefix.

    The registry is global, and any existing mapping for either the
    given prefix or the namespace URI will be removed.

    *prefix* is the namespace prefix, *uri* is a namespace uri. Tags and
    attributes in this namespace will be serialized with prefix if possible.

    ValueError is raised if prefix is reserved or is invalid.

    """
    if re.match('ns\\d+$', prefix):
        raise ValueError('Prefix format reserved for internal use')
    for k, v in list(_namespace_map.items()):
        if k == uri or v == prefix:
            del _namespace_map[k]
    _namespace_map[uri] = prefix
_namespace_map = {'http://www.w3.org/XML/1998/namespace': 'xml', 'http://www.w3.org/1999/xhtml': 'html', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#': 'rdf', 'http://schemas.xmlsoap.org/wsdl/': 'wsdl', 'http://www.w3.org/2001/XMLSchema': 'xs', 'http://www.w3.org/2001/XMLSchema-instance': 'xsi', 'http://purl.org/dc/elements/1.1/': 'dc'}
登记命名空间._namespace_map = _namespace_map

def _raise_serialization_error(text):
    raise TypeError('cannot serialize %r (type %s)' % (text, type(text).__name__))

def _escape_cdata(text):
    try:
        if '&' in text:
            text = text.replace('&', '&amp;')
        if '<' in text:
            text = text.replace('<', '&lt;')
        if '>' in text:
            text = text.replace('>', '&gt;')
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)

def _escape_attrib(text):
    try:
        if '&' in text:
            text = text.replace('&', '&amp;')
        if '<' in text:
            text = text.replace('<', '&lt;')
        if '>' in text:
            text = text.replace('>', '&gt;')
        if '"' in text:
            text = text.replace('"', '&quot;')
        if '\r' in text:
            text = text.replace('\r', '&#13;')
        if '\n' in text:
            text = text.replace('\n', '&#10;')
        if '\t' in text:
            text = text.replace('\t', '&#09;')
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)

def _escape_attrib_html(text):
    try:
        if '&' in text:
            text = text.replace('&', '&amp;')
        if '>' in text:
            text = text.replace('>', '&gt;')
        if '"' in text:
            text = text.replace('"', '&quot;')
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)

def 转字符串(element, encoding=None, method=None, *, xml_declaration=None, default_namespace=None, short_empty_elements=True):
    """Generate string representation of XML element.

    All subelements are included.  If encoding is "unicode", a string
    is returned. Otherwise a bytestring is returned.

    *element* is an Element instance, *encoding* is an optional output
    encoding defaulting to US-ASCII, *method* is an optional output which
    can be one of "xml" (default), "html", "text" or "c14n",
    *default_namespace* sets the default XML namespace (for "xmlns").

    Returns an (optionally) encoded string containing the XML data.

    """
    stream = io.StringIO() if encoding == 'unicode' else io.BytesIO()
    元素树(element).write(stream, encoding, xml_declaration=xml_declaration, default_namespace=default_namespace, method=method, short_empty_elements=short_empty_elements)
    return stream.getvalue()

class _ListDataStream(io.BufferedIOBase):
    """An auxiliary stream accumulating into a list reference."""

    def __init__(self, lst):
        self.lst = lst

    def writable(self):
        return True

    def seekable(self):
        return True

    def 写出(self, b):
        self.lst.append(b)

    def tell(self):
        return len(self.lst)
_装类转发(_ListDataStream, {'write': '写出'}, {'write': '写出'})

def 转字符串表(element, encoding=None, method=None, *, xml_declaration=None, default_namespace=None, short_empty_elements=True):
    lst = []
    stream = _ListDataStream(lst)
    元素树(element).write(stream, encoding, xml_declaration=xml_declaration, default_namespace=default_namespace, method=method, short_empty_elements=short_empty_elements)
    return lst

def 转储(elem):
    """Write element tree or element structure to sys.stdout.

    This function should be used for debugging only.

    *elem* is either an ElementTree, or a single Element.  The exact output
    format is implementation dependent.  In this version, it's written as an
    ordinary XML file.

    """
    if not isinstance(elem, 元素树):
        elem = 元素树(elem)
    elem.write(sys.stdout, encoding='unicode')
    tail = elem.getroot().tail
    if not tail or tail[-1] != '\n':
        sys.stdout.write('\n')

def 缩进(tree, space='  ', level=0):
    """Indent an XML document by inserting newlines and indentation space
    after elements.

    *tree* is the ElementTree or Element to modify.  The (root) element
    itself will not be changed, but the tail text of all elements in its
    subtree will be adapted.

    *space* is the whitespace to insert for each indentation level, two
    space characters by default.

    *level* is the initial indentation level. Setting this to a higher
    value than 0 can be used for indenting subtrees that are more deeply
    nested inside of a document.
    """
    if isinstance(tree, 元素树):
        tree = tree.getroot()
    if level < 0:
        raise ValueError(f'Initial indentation level must be >= 0, got {level}')
    if not len(tree):
        return
    indentations = ['\n' + level * space]

    def _indent_children(elem, level):
        child_level = level + 1
        try:
            child_indentation = indentations[child_level]
        except IndexError:
            child_indentation = indentations[level] + space
            indentations.append(child_indentation)
        if not elem.text or not elem.text.strip():
            elem.text = child_indentation
        for child in elem:
            if len(child):
                _indent_children(child, child_level)
            if not child.tail or not child.tail.strip():
                child.tail = child_indentation
        if not child.tail.strip():
            child.tail = indentations[level]
    _indent_children(tree, 0)

def 解析(source, parser=None):
    """Parse XML document into element tree.

    *source* is a filename or file object containing XML data,
    *parser* is an optional parser instance defaulting to XMLParser.

    Return an ElementTree instance.

    """
    tree = 元素树()
    tree.parse(source, parser)
    return tree

def 迭代解析(source, events=None, parser=None):
    """Incrementally parse XML document into ElementTree.

    This class also reports what's going on to the user based on the
    *events* it is initialized with.  The supported events are the strings
    "start", "end", "start-ns" and "end-ns" (the "ns" events are used to get
    detailed namespace information).  If *events* is omitted, only
    "end" events are reported.

    *source* is a filename or file object containing XML data, *events* is
    a list of events to report back, *parser* is an optional parser
    instance.

    Returns an iterator providing (event, elem) pairs.

    """
    pullparser = XML拉取解析器(events=events, _parser=parser)
    if not hasattr(source, 'read'):
        source = open(source, 'rb')
        close_source = True
    else:
        close_source = False

    def iterator(source):
        try:
            while True:
                yield from pullparser.read_events()
                data = source.read(16 * 1024)
                if not data:
                    break
                pullparser.feed(data)
            root = pullparser._close_and_return_root()
            yield from pullparser.read_events()
            it = wr()
            if it is not None:
                it.root = root
        finally:
            if close_source:
                source.close()
    gen = iterator(source)

    class IterParseIterator(collections.abc.Iterator):
        __next__ = gen.__next__

        def close(self):
            if close_source:
                source.close()
            gen.close()

        def __del__(self):
            if close_source:
                source.close()
    it = IterParseIterator()
    it.root = None
    wr = weakref.ref(it)
    return it

class XML拉取解析器:

    def __init__(self, events=None, *, _parser=None):
        self._events_queue = collections.deque()
        self._parser = _parser or XML解析器(target=树构建器())
        if events is None:
            events = ('end',)
        self._parser._setevents(self._events_queue, events)

    def feed(self, data):
        """Feed encoded data to parser."""
        if self._parser is None:
            raise ValueError('feed() called after end of stream')
        if data:
            try:
                self._parser.feed(data)
            except SyntaxError as exc:
                self._events_queue.append(exc)

    def _close_and_return_root(self):
        root = self._parser.close()
        self._parser = None
        return root

    def close(self):
        """Finish feeding data to parser.

        Unlike XMLParser, does not return the root element. Use
        read_events() to consume elements from XMLPullParser.
        """
        self._close_and_return_root()

    def read_events(self):
        """Return an iterator over currently available (event, elem) pairs.

        Events are consumed from the internal event queue as they are
        retrieved from the iterator.
        """
        events = self._events_queue
        while events:
            event = events.popleft()
            if isinstance(event, Exception):
                raise event
            else:
                yield event

    def flush(self):
        if self._parser is None:
            raise ValueError('flush() called after end of stream')
        self._parser.flush()

def XML命名空间(text, parser=None):
    """Parse XML document from string constant.

    This function can be used to embed "XML Literals" in Python code.

    *text* is a string containing XML data, *parser* is an
    optional parser instance, defaulting to the standard XMLParser.

    Returns an Element instance.

    """
    if not parser:
        parser = XML解析器(target=树构建器())
    parser.feed(text)
    return parser.close()

def 解析XMLID(text, parser=None):
    """Parse XML document from string constant for its IDs.

    *text* is a string containing XML data, *parser* is an
    optional parser instance, defaulting to the standard XMLParser.

    Returns an (Element, dict) tuple, in which the
    dict maps element id:s to elements.

    """
    if not parser:
        parser = XML解析器(target=树构建器())
    parser.feed(text)
    tree = parser.close()
    ids = {}
    for elem in tree.iter():
        id = elem.get('id')
        if id:
            ids[id] = elem
    return (tree, ids)
从字符串解析 = XML命名空间

def 从字符串表解析(sequence, parser=None):
    """Parse XML document from sequence of string fragments.

    *sequence* is a list of other sequence, *parser* is an optional parser
    instance, defaulting to the standard XMLParser.

    Returns an Element instance.

    """
    if not parser:
        parser = XML解析器(target=树构建器())
    for text in sequence:
        parser.feed(text)
    return parser.close()

class 树构建器:
    """Generic element structure builder.

    This builder converts a sequence of start, data, and end method
    calls to a well-formed element structure.

    You can use this class to build an element structure using a custom XML
    parser, or a parser for some other XML-like format.

    *element_factory* is an optional element factory which is called
    to create new Element instances, as necessary.

    *comment_factory* is a factory to create comments to be used instead of
    the standard factory.  If *insert_comments* is false (the default),
    comments will not be inserted into the tree.

    *pi_factory* is a factory to create processing instructions to be used
    instead of the standard factory.  If *insert_pis* is false (the default),
    processing instructions will not be inserted into the tree.
    """

    def __init__(self, element_factory=None, *, comment_factory=None, pi_factory=None, insert_comments=False, insert_pis=False):
        self._data = []
        self._elem = []
        self._last = None
        self._root = None
        self._tail = None
        if comment_factory is None:
            comment_factory = 注释
        self._comment_factory = comment_factory
        self.insert_comments = insert_comments
        if pi_factory is None:
            pi_factory = 处理指令
        self._pi_factory = pi_factory
        self.insert_pis = insert_pis
        if element_factory is None:
            element_factory = 元素
        self._factory = element_factory

    def close(self):
        """Flush builder buffers and return toplevel document Element."""
        assert len(self._elem) == 0, 'missing end tags'
        assert self._root is not None, 'missing toplevel element'
        return self._root

    def _flush(self):
        if self._data:
            if self._last is not None:
                text = ''.join(self._data)
                if self._tail:
                    assert self._last.tail is None, 'internal error (tail)'
                    self._last.tail = text
                else:
                    assert self._last.text is None, 'internal error (text)'
                    self._last.text = text
            self._data = []

    def data(self, data):
        """Add text to current element."""
        self._data.append(data)

    def start(self, tag, attrs):
        """Open new element and return it.

        *tag* is the element name, *attrs* is a dict containing element
        attributes.

        """
        self._flush()
        self._last = elem = self._factory(tag, attrs)
        if self._elem:
            self._elem[-1].append(elem)
        elif self._root is None:
            self._root = elem
        self._elem.append(elem)
        self._tail = 0
        return elem

    def end(self, tag):
        """Close and return current Element.

        *tag* is the element name.

        """
        self._flush()
        self._last = self._elem.pop()
        assert self._last.tag == tag, 'end tag mismatch (expected %s, got %s)' % (self._last.tag, tag)
        self._tail = 1
        return self._last

    def comment(self, text):
        """Create a comment using the comment_factory.

        *text* is the text of the comment.
        """
        return self._handle_single(self._comment_factory, self.insert_comments, text)

    def pi(self, target, text=None):
        """Create a processing instruction using the pi_factory.

        *target* is the target name of the processing instruction.
        *text* is the data of the processing instruction, or ''.
        """
        return self._handle_single(self._pi_factory, self.insert_pis, target, text)

    def _handle_single(self, factory, insert, *args):
        elem = factory(*args)
        if insert:
            self._flush()
            self._last = elem
            if self._elem:
                self._elem[-1].append(elem)
            self._tail = 1
        return elem

class XML解析器:
    """Element structure builder for XML source data based on the expat parser.

    *target* is an optional target object which defaults to an instance of the
    standard TreeBuilder class, *encoding* is an optional encoding string
    which if given, overrides the encoding specified in the XML file:
    http://www.iana.org/assignments/character-sets

    """

    def __init__(self, *, target=None, encoding=None):
        try:
            from XML工具.parsers import expat
        except ImportError:
            try:
                import pyexpat as expat
            except ImportError:
                raise ImportError('No module named expat; use SimpleXMLTreeBuilder instead')
        parser = expat.ParserCreate(encoding, '}')
        if target is None:
            target = 树构建器()
        self.parser = self._parser = parser
        self.target = self._target = target
        self._error = expat.error
        self._names = {}
        parser.DefaultHandlerExpand = self._default
        if hasattr(target, 'start'):
            parser.StartElementHandler = self._start
        if hasattr(target, 'end'):
            parser.EndElementHandler = self._end
        if hasattr(target, 'start_ns'):
            parser.StartNamespaceDeclHandler = self._start_ns
        if hasattr(target, 'end_ns'):
            parser.EndNamespaceDeclHandler = self._end_ns
        if hasattr(target, 'data'):
            parser.CharacterDataHandler = target.data
        if hasattr(target, 'comment'):
            parser.CommentHandler = target.comment
        if hasattr(target, 'pi'):
            parser.ProcessingInstructionHandler = target.pi
        parser.buffer_text = 1
        parser.ordered_attributes = 1
        self._doctype = None
        self.entity = {}
        try:
            self.version = 'Expat %d.%d.%d' % expat.version_info
        except AttributeError:
            pass

    def _setevents(self, events_queue, events_to_report):
        parser = self._parser
        append = events_queue.append
        for event_name in events_to_report:
            if event_name == 'start':
                parser.ordered_attributes = 1

                def handler(tag, attrib_in, event=event_name, append=append, start=self._start):
                    append((event, start(tag, attrib_in)))
                parser.StartElementHandler = handler
            elif event_name == 'end':

                def handler(tag, event=event_name, append=append, end=self._end):
                    append((event, end(tag)))
                parser.EndElementHandler = handler
            elif event_name == 'start-ns':
                if hasattr(self.target, 'start_ns'):

                    def handler(prefix, uri, event=event_name, append=append, start_ns=self._start_ns):
                        append((event, start_ns(prefix, uri)))
                else:

                    def handler(prefix, uri, event=event_name, append=append):
                        append((event, (prefix or '', uri or '')))
                parser.StartNamespaceDeclHandler = handler
            elif event_name == 'end-ns':
                if hasattr(self.target, 'end_ns'):

                    def handler(prefix, event=event_name, append=append, end_ns=self._end_ns):
                        append((event, end_ns(prefix)))
                else:

                    def handler(prefix, event=event_name, append=append):
                        append((event, None))
                parser.EndNamespaceDeclHandler = handler
            elif event_name == 'comment':

                def handler(text, event=event_name, append=append, self=self):
                    append((event, self.target.comment(text)))
                parser.CommentHandler = handler
            elif event_name == 'pi':

                def handler(pi_target, data, event=event_name, append=append, self=self):
                    append((event, self.target.pi(pi_target, data)))
                parser.ProcessingInstructionHandler = handler
            else:
                raise ValueError('unknown event %r' % event_name)

    def _raiseerror(self, value):
        err = 解析错误(value)
        err.code = value.code
        err.position = (value.lineno, value.offset)
        raise err

    def _fixname(self, key):
        try:
            name = self._names[key]
        except KeyError:
            name = key
            if '}' in name:
                name = '{' + name
            self._names[key] = name
        return name

    def _start_ns(self, prefix, uri):
        return self.target.start_ns(prefix or '', uri or '')

    def _end_ns(self, prefix):
        return self.target.end_ns(prefix or '')

    def _start(self, tag, attr_list):
        fixname = self._fixname
        tag = fixname(tag)
        attrib = {}
        if attr_list:
            for i in range(0, len(attr_list), 2):
                attrib[fixname(attr_list[i])] = attr_list[i + 1]
        return self.target.start(tag, attrib)

    def _end(self, tag):
        return self.target.end(self._fixname(tag))

    def _default(self, text):
        prefix = text[:1]
        if prefix == '&':
            try:
                data_handler = self.target.data
            except AttributeError:
                return
            try:
                data_handler(self.entity[text[1:-1]])
            except KeyError:
                from XML工具.parsers import expat
                err = expat.error('undefined entity %s: line %d, column %d' % (text, self.parser.ErrorLineNumber, self.parser.ErrorColumnNumber))
                err.code = 11
                err.lineno = self.parser.ErrorLineNumber
                err.offset = self.parser.ErrorColumnNumber
                raise err
        elif prefix == '<' and text[:9] == '<!DOCTYPE':
            self._doctype = []
        elif self._doctype is not None:
            if prefix == '>':
                self._doctype = None
                return
            text = text.strip()
            if not text:
                return
            self._doctype.append(text)
            n = len(self._doctype)
            if n > 2:
                type = self._doctype[1]
                if type == 'PUBLIC' and n == 4:
                    name, type, pubid, system = self._doctype
                    if pubid:
                        pubid = pubid[1:-1]
                elif type == 'SYSTEM' and n == 3:
                    name, type, system = self._doctype
                    pubid = None
                else:
                    return
                if hasattr(self.target, 'doctype'):
                    self.target.doctype(name, pubid, system[1:-1])
                elif hasattr(self, 'doctype'):
                    warnings.warn('The doctype() method of XMLParser is ignored.  Define doctype() method on the TreeBuilder target.', RuntimeWarning)
                self._doctype = None

    def feed(self, data):
        """Feed encoded data to parser."""
        try:
            self.parser.Parse(data, False)
        except self._error as v:
            self._raiseerror(v)

    def close(self):
        """Finish feeding data to parser and return element structure."""
        try:
            self.parser.Parse(b'', True)
        except self._error as v:
            self._raiseerror(v)
        try:
            close_handler = self.target.close
        except AttributeError:
            pass
        else:
            return close_handler()
        finally:
            del self.parser, self._parser
            del self.target, self._target

    def flush(self):
        was_enabled = self.parser.GetReparseDeferralEnabled()
        try:
            self.parser.SetReparseDeferralEnabled(False)
            self.parser.Parse(b'', False)
        except self._error as v:
            self._raiseerror(v)
        finally:
            self.parser.SetReparseDeferralEnabled(was_enabled)

def 规范化(xml_data=None, *, out=None, from_file=None, **options):
    """Convert XML to its C14N 2.0 serialised form.

    If *out* is provided, it must be a file or file-like object that
    receives the serialised canonical XML output (text, not bytes) through
    its ``.write()`` method.  To write to a file, open it in text mode with
    encoding "utf-8".  If *out* is not provided, this function returns the
    output as text string.

    Either *xml_data* (an XML string) or *from_file* (a file path or
    file-like object) must be provided as input.

    The configuration options are the same as for the ``C14NWriterTarget``.
    """
    if xml_data is None and from_file is None:
        raise ValueError("Either 'xml_data' or 'from_file' must be provided as input")
    sio = None
    if out is None:
        sio = out = io.StringIO()
    parser = XML解析器(target=规范化写出目标(out.write, **options))
    if xml_data is not None:
        parser.feed(xml_data)
        parser.close()
    elif from_file is not None:
        解析(from_file, parser=parser)
    return sio.getvalue() if sio is not None else None
_looks_like_prefix_name = re.compile('^\\w+:\\w+$', re.UNICODE).match

class 规范化写出目标:
    """
    Canonicalization writer target for the XMLParser.

    Serialises parse events to XML C14N 2.0.

    The *write* function is used for writing out the resulting data stream
    as text (not bytes).  To write to a file, open it in text mode with
    encoding "utf-8" and pass its ``.write`` method.

    Configuration options:

    - *with_comments*: set to true to include comments
    - *strip_text*: set to true to strip whitespace before and after text
                    content
    - *rewrite_prefixes*: set to true to replace namespace prefixes by
                          "n{number}"
    - *qname_aware_tags*: a set of qname aware tag names in which prefixes
                          should be replaced in text content
    - *qname_aware_attrs*: a set of qname aware attribute names in which
                           prefixes should be replaced in text content
    - *exclude_attrs*: a set of attribute names that should not be
                       serialised
    - *exclude_tags*: a set of tag names that should not be serialised
    """

    def __init__(self, write, *, with_comments=False, strip_text=False, rewrite_prefixes=False, qname_aware_tags=None, qname_aware_attrs=None, exclude_attrs=None, exclude_tags=None):
        self._write = write
        self._data = []
        self._with_comments = with_comments
        self._strip_text = strip_text
        self._exclude_attrs = set(exclude_attrs) if exclude_attrs else None
        self._exclude_tags = set(exclude_tags) if exclude_tags else None
        self._rewrite_prefixes = rewrite_prefixes
        if qname_aware_tags:
            self._qname_aware_tags = set(qname_aware_tags)
        else:
            self._qname_aware_tags = None
        if qname_aware_attrs:
            self._find_qname_aware_attrs = set(qname_aware_attrs).intersection
        else:
            self._find_qname_aware_attrs = None
        self._declared_ns_stack = [[('http://www.w3.org/XML/1998/namespace', 'xml')]]
        self._ns_stack = []
        if not rewrite_prefixes:
            self._ns_stack.append(list(_namespace_map.items()))
        self._ns_stack.append([])
        self._prefix_map = {}
        self._preserve_space = [False]
        self._pending_start = None
        self._root_seen = False
        self._root_done = False
        self._ignored_depth = 0

    def _iter_namespaces(self, ns_stack, _reversed=reversed):
        for namespaces in _reversed(ns_stack):
            if namespaces:
                yield from namespaces

    def _resolve_prefix_name(self, prefixed_name):
        prefix, name = prefixed_name.split(':', 1)
        for uri, p in self._iter_namespaces(self._ns_stack):
            if p == prefix:
                return f'{{{uri}}}{name}'
        raise ValueError(f'Prefix {prefix} of QName "{prefixed_name}" is not declared in scope')

    def _qname(self, qname, uri=None):
        if uri is None:
            uri, tag = qname[1:].rsplit('}', 1) if qname[:1] == '{' else ('', qname)
        else:
            tag = qname
        prefixes_seen = set()
        for u, prefix in self._iter_namespaces(self._declared_ns_stack):
            if u == uri and prefix not in prefixes_seen:
                return (f'{prefix}:{tag}' if prefix else tag, tag, uri)
            prefixes_seen.add(prefix)
        if self._rewrite_prefixes:
            if uri in self._prefix_map:
                prefix = self._prefix_map[uri]
            else:
                prefix = self._prefix_map[uri] = f'n{len(self._prefix_map)}'
            self._declared_ns_stack[-1].append((uri, prefix))
            return (f'{prefix}:{tag}', tag, uri)
        if not uri and '' not in prefixes_seen:
            return (tag, tag, uri)
        for u, prefix in self._iter_namespaces(self._ns_stack):
            if u == uri:
                self._declared_ns_stack[-1].append((uri, prefix))
                return (f'{prefix}:{tag}' if prefix else tag, tag, uri)
        if not uri:
            return (tag, tag, uri)
        raise ValueError(f'Namespace "{uri}" is not declared in scope')

    def data(self, data):
        if not self._ignored_depth:
            self._data.append(data)

    def _flush(self, _join_text=''.join):
        data = _join_text(self._data)
        del self._data[:]
        if self._strip_text and (not self._preserve_space[-1]):
            data = data.strip()
        if self._pending_start is not None:
            args, self._pending_start = (self._pending_start, None)
            qname_text = data if data and _looks_like_prefix_name(data) else None
            self._start(*args, qname_text)
            if qname_text is not None:
                return
        if data and self._root_seen:
            self._write(_escape_cdata_c14n(data))

    def start_ns(self, prefix, uri):
        if self._ignored_depth:
            return
        if self._data:
            self._flush()
        self._ns_stack[-1].append((uri, prefix))

    def start(self, tag, attrs):
        if self._exclude_tags is not None and (self._ignored_depth or tag in self._exclude_tags):
            self._ignored_depth += 1
            return
        if self._data:
            self._flush()
        new_namespaces = []
        self._declared_ns_stack.append(new_namespaces)
        if self._qname_aware_tags is not None and tag in self._qname_aware_tags:
            self._pending_start = (tag, attrs, new_namespaces)
            return
        self._start(tag, attrs, new_namespaces)

    def _start(self, tag, attrs, new_namespaces, qname_text=None):
        if self._exclude_attrs is not None and attrs:
            attrs = {k: v for k, v in attrs.items() if k not in self._exclude_attrs}
        qnames = {tag, *attrs}
        resolved_names = {}
        if qname_text is not None:
            qname = resolved_names[qname_text] = self._resolve_prefix_name(qname_text)
            qnames.add(qname)
        if self._find_qname_aware_attrs is not None and attrs:
            qattrs = self._find_qname_aware_attrs(attrs)
            if qattrs:
                for attr_name in qattrs:
                    value = attrs[attr_name]
                    if _looks_like_prefix_name(value):
                        qname = resolved_names[value] = self._resolve_prefix_name(value)
                        qnames.add(qname)
            else:
                qattrs = None
        else:
            qattrs = None
        parse_qname = self._qname
        parsed_qnames = {n: parse_qname(n) for n in sorted(qnames, key=lambda n: n.split('}', 1))}
        if new_namespaces:
            attr_list = [('xmlns:' + prefix if prefix else 'xmlns', uri) for uri, prefix in new_namespaces]
            attr_list.sort()
        else:
            attr_list = []
        if attrs:
            for k, v in sorted(attrs.items()):
                if qattrs is not None and k in qattrs and (v in resolved_names):
                    v = parsed_qnames[resolved_names[v]][0]
                attr_qname, attr_name, uri = parsed_qnames[k]
                attr_list.append((attr_qname if uri else attr_name, v))
        space_behaviour = attrs.get('{http://www.w3.org/XML/1998/namespace}space')
        self._preserve_space.append(space_behaviour == 'preserve' if space_behaviour else self._preserve_space[-1])
        写出 = self._write
        写出('<' + parsed_qnames[tag][0])
        if attr_list:
            写出(''.join([f' {k}="{_escape_attrib_c14n(v)}"' for k, v in attr_list]))
        写出('>')
        if qname_text is not None:
            写出(_escape_cdata_c14n(parsed_qnames[resolved_names[qname_text]][0]))
        self._root_seen = True
        self._ns_stack.append([])

    def end(self, tag):
        if self._ignored_depth:
            self._ignored_depth -= 1
            return
        if self._data:
            self._flush()
        self._write(f'</{self._qname(tag)[0]}>')
        self._preserve_space.pop()
        self._root_done = len(self._preserve_space) == 1
        self._declared_ns_stack.pop()
        self._ns_stack.pop()

    def comment(self, text):
        if not self._with_comments:
            return
        if self._ignored_depth:
            return
        if self._root_done:
            self._write('\n')
        elif self._root_seen and self._data:
            self._flush()
        self._write(f'<!--{_escape_cdata_c14n(text)}-->')
        if not self._root_seen:
            self._write('\n')

    def pi(self, target, data):
        if self._ignored_depth:
            return
        if self._root_done:
            self._write('\n')
        elif self._root_seen and self._data:
            self._flush()
        self._write(f'<?{target} {_escape_cdata_c14n(data)}?>' if data else f'<?{target}?>')
        if not self._root_seen:
            self._write('\n')

def _escape_cdata_c14n(text):
    try:
        if '&' in text:
            text = text.replace('&', '&amp;')
        if '<' in text:
            text = text.replace('<', '&lt;')
        if '>' in text:
            text = text.replace('>', '&gt;')
        if '\r' in text:
            text = text.replace('\r', '&#xD;')
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)

def _escape_attrib_c14n(text):
    try:
        if '&' in text:
            text = text.replace('&', '&amp;')
        if '<' in text:
            text = text.replace('<', '&lt;')
        if '"' in text:
            text = text.replace('"', '&quot;')
        if '\t' in text:
            text = text.replace('\t', '&#x9;')
        if '\n' in text:
            text = text.replace('\n', '&#xA;')
        if '\r' in text:
            text = text.replace('\r', '&#xD;')
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)
try:
    _Element_Py = 元素
    from _elementtree import *
    from _elementtree import _set_factories
except ImportError:
    pass
else:
    _set_factories(注释, 处理指令)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import xml.etree.ElementTree as _英文库
元素 = _英文库.Element
解析错误 = _英文库.ParseError
子元素 = _英文库.SubElement
树构建器 = _英文库.TreeBuilder
XML解析器 = _英文库.XMLParser

# 同名模块的工厂沿用（见 D-085）—— 第二份模块沿用第一份的函数对象
_系统 = __import__('sys')
_旧份 = _系统.modules.get('XML工具.etree.ElementTree')
_有C = False
try:
    import _elementtree
    _有C = True
except ImportError:
    pass
if _旧份 is not None and _旧份 is not _系统.modules.get(__name__) and _有C:
    try:
        处理指令 = _旧份.处理指令
        处理指令简写 = _旧份.处理指令
        注释 = _旧份.注释
    except AttributeError:
        pass
_模块别名 = {
    'C14NWriterTarget': '规范化写出目标',
    'Comment': '注释',
    'Element': '元素',
    'ElementTree': '元素树',
    'HTML_EMPTY': 'HTML空元素表',
    'PI': '处理指令简写',
    'ParseError': '解析错误',
    'ProcessingInstruction': '处理指令',
    'QName': '限定名',
    'SubElement': '子元素',
    'TreeBuilder': '树构建器',
    'VERSION': '版本',
    'XML': 'XML命名空间',
    'XMLID': '解析XMLID',
    'XMLParser': 'XML解析器',
    'XMLPullParser': 'XML拉取解析器',
    'canonicalize': '规范化',
    'dump': '转储',
    'fromstring': '从字符串解析',
    'fromstringlist': '从字符串表解析',
    'indent': '缩进',
    'iselement': '是元素吗',
    'iterparse': '迭代解析',
    'parse': '解析',
    'register_namespace': '登记命名空间',
    'tostring': '转字符串',
    'tostringlist': '转字符串表',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '_ListDataStream': {
        'write': '写出',
    },
    '元素': {
        'findtext': '查找文本',
        'iterfind': '迭代查找',
    },
    '元素树': {
        'findtext': '查找文本',
        'getroot': '取根',
        'iterfind': '迭代查找',
        'parse': '解析',
        'write': '写出',
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
    '_ListDataStream': {
        'write': '写出',
    },
    '元素': {
        'findtext': '查找文本',
        'iterfind': '迭代查找',
    },
    '元素树': {
        'findtext': '查找文本',
        'getroot': '取根',
        'iterfind': '迭代查找',
        'parse': '解析',
        'write': '写出',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'XML命名空间',
    'XML拉取解析器',
    'XML解析器',
    '从字符串表解析',
    '从字符串解析',
    '元素',
    '元素树',
    '处理指令',
    '处理指令简写',
    '子元素',
    '是元素吗',
    '树构建器',
    '注释',
    '版本',
    '登记命名空间',
    '缩进',
    '规范化',
    '规范化写出目标',
    '解析',
    '解析XMLID',
    '解析错误',
    '转储',
    '转字符串',
    '转字符串表',
    '迭代解析',
    '限定名',
]

# ---- 转发层结束 ----
