# -*- coding: utf-8 -*-
"""XML工具.dom/minidom —— 汉语库（由 tools/汉化库.py 从 Lib/xml/dom/minidom.py 机械生成，**不要手改**）。

英文库 Lib/xml.dom/minidom.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


"""Simple implementation of the Level 1 DOM.

Namespaces and other minor Level 2 features are also supported.

parse("foo.xml")

parseString("<foo><bar/></foo>")

Todo:
=====
 * convenience methods for getting elements and text.
 * more testing
 * bring some of the writer and linearizer code into conformance with this
        interface
 * SAX 2 namespaces
"""
_英文原名表 = {'Attr': '属性节点', 'AttributeList': '属性节点表', 'CDATASection': 'CDATA节', 'CharacterData': '字符数据', 'Childless': '无子类', 'Comment': '注释', 'DOMImplementation': 'DOM实现', 'Document': '文档', 'DocumentFragment': '文档片段', 'DocumentType': '文档类型', 'Element': '元素', 'ElementInfo': '元素信息', 'Entity': '实体', 'Identified': '已标识', 'NamedNodeMap': '命名节点表', 'Node': '节点', 'Notation': '记法', 'ProcessingInstruction': '处理指令', 'ReadOnlySequentialNamedNodeMap': '只读顺序节点表', 'Text': '文本', 'TypeInfo': '类型信息', 'getDOMImplementation': '取DOM实现', 'parse': '解析', 'parseString': '解析字符串'}

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
import io
import XML工具.dom
from XML工具.dom import EMPTY_NAMESPACE, EMPTY_PREFIX, XMLNS_NAMESPACE, domreg
from XML工具.dom.minicompat import *
from XML工具.dom.xmlbuilder import DOMImplementationLS, DocumentLS
_nodeTypes_with_children = (XML工具.dom.Node.ELEMENT_NODE, XML工具.dom.Node.ENTITY_REFERENCE_NODE)

class 节点(XML工具.dom.Node):
    命名空间URI = None
    父节点 = None
    所有者文档 = None
    后兄弟 = None
    前兄弟 = None
    前缀 = EMPTY_PREFIX

    def __bool__(self):
        return True

    def 转XML(self, encoding=None, standalone=None):
        return self.转美化XML('', '', encoding, standalone)

    def 转美化XML(self, indent='\t', newl='\n', encoding=None, standalone=None):
        if encoding is None:
            writer = io.StringIO()
        else:
            writer = io.TextIOWrapper(io.BytesIO(), encoding=encoding, errors='xmlcharrefreplace', newline='\n')
        if self.节点类型 == 节点.DOCUMENT_NODE:
            self.写出XML(writer, '', indent, newl, encoding, standalone)
        else:
            self.写出XML(writer, '', indent, newl)
        if encoding is None:
            return writer.getvalue()
        else:
            return writer.detach().getvalue()

    def 有子节点吗(self):
        return bool(self.子节点表)

    def _get_childNodes(self):
        return self.子节点表

    def _get_firstChild(self):
        if self.子节点表:
            return self.子节点表[0]

    def _get_lastChild(self):
        if self.子节点表:
            return self.子节点表[-1]

    def 插到前面(self, newChild, refChild):
        if newChild.nodeType == self.DOCUMENT_FRAGMENT_NODE:
            for c in tuple(newChild.childNodes):
                self.插到前面(c, refChild)
            return newChild
        if newChild.nodeType not in self._child_node_types:
            raise XML工具.dom.HierarchyRequestErr('%s cannot be child of %s' % (repr(newChild), repr(self)))
        if newChild.parentNode is not None:
            newChild.parentNode.removeChild(newChild)
        if refChild is None:
            self.追加子节点(newChild)
        else:
            try:
                index = self.子节点表.index(refChild)
            except ValueError:
                raise XML工具.dom.NotFoundErr()
            if newChild.nodeType in _nodeTypes_with_children:
                _clear_id_cache(self)
            self.子节点表.insert(index, newChild)
            newChild.nextSibling = refChild
            refChild.previousSibling = newChild
            if index:
                node = self.子节点表[index - 1]
                node.nextSibling = newChild
                newChild.previousSibling = node
            else:
                newChild.previousSibling = None
            newChild.parentNode = self
        return newChild

    def 追加子节点(self, node):
        if node.nodeType == self.DOCUMENT_FRAGMENT_NODE:
            for c in tuple(node.childNodes):
                self.追加子节点(c)
            return node
        if node.nodeType not in self._child_node_types:
            raise XML工具.dom.HierarchyRequestErr('%s cannot be child of %s' % (repr(node), repr(self)))
        elif node.nodeType in _nodeTypes_with_children:
            _clear_id_cache(self)
        if node.parentNode is not None:
            node.parentNode.removeChild(node)
        _append_child(self, node)
        node.nextSibling = None
        return node

    def 替换子节点(self, newChild, oldChild):
        if newChild.nodeType == self.DOCUMENT_FRAGMENT_NODE:
            refChild = oldChild.nextSibling
            self.删子节点(oldChild)
            return self.插到前面(newChild, refChild)
        if newChild.nodeType not in self._child_node_types:
            raise XML工具.dom.HierarchyRequestErr('%s cannot be child of %s' % (repr(newChild), repr(self)))
        if newChild is oldChild:
            return
        if newChild.parentNode is not None:
            newChild.parentNode.removeChild(newChild)
        try:
            index = self.子节点表.index(oldChild)
        except ValueError:
            raise XML工具.dom.NotFoundErr()
        self.子节点表[index] = newChild
        newChild.parentNode = self
        oldChild.parentNode = None
        if newChild.nodeType in _nodeTypes_with_children or oldChild.nodeType in _nodeTypes_with_children:
            _clear_id_cache(self)
        newChild.nextSibling = oldChild.nextSibling
        newChild.previousSibling = oldChild.previousSibling
        oldChild.nextSibling = None
        oldChild.previousSibling = None
        if newChild.previousSibling:
            newChild.previousSibling.nextSibling = newChild
        if newChild.nextSibling:
            newChild.nextSibling.previousSibling = newChild
        return oldChild

    def 删子节点(self, oldChild):
        try:
            self.子节点表.remove(oldChild)
        except ValueError:
            raise XML工具.dom.NotFoundErr()
        if oldChild.nextSibling is not None:
            oldChild.nextSibling.previousSibling = oldChild.previousSibling
        if oldChild.previousSibling is not None:
            oldChild.previousSibling.nextSibling = oldChild.nextSibling
        oldChild.nextSibling = oldChild.previousSibling = None
        if oldChild.nodeType in _nodeTypes_with_children:
            _clear_id_cache(self)
        oldChild.parentNode = None
        return oldChild

    def 规范化(self):
        L = []
        for child in self.子节点表:
            if child.nodeType == 节点.TEXT_NODE:
                if not child.data:
                    if L:
                        L[-1].nextSibling = child.nextSibling
                    if child.nextSibling:
                        child.nextSibling.previousSibling = child.previousSibling
                    child.unlink()
                elif L and L[-1].nodeType == child.nodeType:
                    node = L[-1]
                    node.data = node.data + child.data
                    node.nextSibling = child.nextSibling
                    if child.nextSibling:
                        child.nextSibling.previousSibling = node
                    child.unlink()
                else:
                    L.append(child)
            else:
                L.append(child)
                if child.nodeType == 节点.ELEMENT_NODE:
                    child.normalize()
        self.子节点表[:] = L

    def 克隆节点(self, deep):
        return _clone_node(self, deep, self.所有者文档 or self)

    def 支持吗(self, feature, version):
        return self.所有者文档.implementation.hasFeature(feature, version)

    def _get_localName(self):
        return None

    def 同节点吗(self, other):
        return self is other

    def 取接口(self, feature):
        if self.支持吗(feature, None):
            return self
        else:
            return None

    def 取用户数据(self, key):
        try:
            return self._user_data[key][0]
        except (AttributeError, KeyError):
            return None

    def 设用户数据(self, key, data, handler):
        old = None
        try:
            d = self._user_data
        except AttributeError:
            d = {}
            self._user_data = d
        if key in d:
            old = d[key][0]
        if data is None:
            handler = None
            if old is not None:
                del d[key]
        else:
            d[key] = (data, handler)
        return old

    def _call_user_data_handler(self, operation, src, dst):
        if hasattr(self, '_user_data'):
            for key, (数据, handler) in list(self._user_data.items()):
                if handler is not None:
                    handler.handle(operation, key, 数据, src, dst)

    def 解链(self):
        self.父节点 = self.所有者文档 = None
        if self.子节点表:
            for child in self.子节点表:
                child.unlink()
            self.子节点表 = NodeList()
        self.前兄弟 = None
        self.后兄弟 = None

    def __enter__(self):
        return self

    def __exit__(self, et, ev, tb):
        self.解链()
_装类转发(节点, {'appendChild': '追加子节点', 'cloneNode': '克隆节点', 'getInterface': '取接口', 'getUserData': '取用户数据', 'hasChildNodes': '有子节点吗', 'insertBefore': '插到前面', 'isSameNode': '同节点吗', 'isSupported': '支持吗', 'namespaceURI': '命名空间URI', 'nextSibling': '后兄弟', 'normalize': '规范化', 'ownerDocument': '所有者文档', 'parentNode': '父节点', 'prefix': '前缀', 'previousSibling': '前兄弟', 'removeChild': '删子节点', 'replaceChild': '替换子节点', 'setUserData': '设用户数据', 'toprettyxml': '转美化XML', 'toxml': '转XML', 'unlink': '解链'}, {'appendChild': '追加子节点', 'childNodes': '子节点表', 'cloneNode': '克隆节点', 'getInterface': '取接口', 'getUserData': '取用户数据', 'hasChildNodes': '有子节点吗', 'insertBefore': '插到前面', 'isSameNode': '同节点吗', 'isSupported': '支持吗', 'namespaceURI': '命名空间URI', 'nextSibling': '后兄弟', 'nodeType': '节点类型', 'normalize': '规范化', 'ownerDocument': '所有者文档', 'parentNode': '父节点', 'prefix': '前缀', 'previousSibling': '前兄弟', 'removeChild': '删子节点', 'replaceChild': '替换子节点', 'setUserData': '设用户数据', 'toprettyxml': '转美化XML', 'toxml': '转XML', 'unlink': '解链', 'writexml': '写出XML'})
defproperty(节点, 'firstChild', doc='First child node, or None.')
defproperty(节点, 'lastChild', doc='Last child node, or None.')
defproperty(节点, 'localName', doc='Namespace-local name of this node.')

def _append_child(self, node):
    子节点表 = self.子节点表
    if 子节点表:
        last = 子节点表[-1]
        node.previousSibling = last
        last.nextSibling = node
    子节点表.append(node)
    node.parentNode = self

def _write_data(writer, text, attr):
    """Writes datachars to writer."""
    if not text:
        return
    if '&' in text:
        text = text.replace('&', '&amp;')
    if '<' in text:
        text = text.replace('<', '&lt;')
    if '>' in text:
        text = text.replace('>', '&gt;')
    if attr:
        if '"' in text:
            text = text.replace('"', '&quot;')
        if '\r' in text:
            text = text.replace('\r', '&#13;')
        if '\n' in text:
            text = text.replace('\n', '&#10;')
        if '\t' in text:
            text = text.replace('\t', '&#9;')
    writer.write(text)

def _get_elements_by_tagName_helper(parent, name, rc):
    for node in parent.childNodes:
        if node.nodeType == 节点.ELEMENT_NODE and (name == '*' or node.tagName == name):
            rc.append(node)
        _get_elements_by_tagName_helper(node, name, rc)
    return rc

def _get_elements_by_tagName_ns_helper(parent, nsURI, localName, rc):
    for node in parent.childNodes:
        if node.nodeType == 节点.ELEMENT_NODE:
            if (localName == '*' or node.localName == localName) and (nsURI == '*' or node.namespaceURI == nsURI):
                rc.append(node)
            _get_elements_by_tagName_ns_helper(node, nsURI, localName, rc)
    return rc

class 文档片段(节点):
    节点类型 = 节点.DOCUMENT_FRAGMENT_NODE
    节点名 = '#document-fragment'
    节点值 = None
    属性表 = None
    父节点 = None
    _child_node_types = (节点.ELEMENT_NODE, 节点.TEXT_NODE, 节点.CDATA_SECTION_NODE, 节点.ENTITY_REFERENCE_NODE, 节点.PROCESSING_INSTRUCTION_NODE, 节点.COMMENT_NODE, 节点.NOTATION_NODE)

    def __init__(self):
        self.子节点表 = NodeList()
_装类转发(文档片段, {'attributes': '属性表', 'nodeName': '节点名', 'nodeType': '节点类型', 'nodeValue': '节点值', 'parentNode': '父节点'}, {'attributes': '属性表', 'childNodes': '子节点表', 'nodeName': '节点名', 'nodeType': '节点类型', 'nodeValue': '节点值', 'parentNode': '父节点'})

class 属性节点(节点):
    __slots__ = ('_name', '_value', 'namespaceURI', '_prefix', 'childNodes', '_localName', 'ownerDocument', 'ownerElement')
    节点类型 = 节点.ATTRIBUTE_NODE
    属性表 = None
    已指定 = False
    _is_id = False
    _child_node_types = (节点.TEXT_NODE, 节点.ENTITY_REFERENCE_NODE)

    def __init__(self, qName, namespaceURI=EMPTY_NAMESPACE, localName=None, prefix=None):
        self.所有者元素 = None
        self.所有者文档 = None
        self._name = qName
        self.命名空间URI = namespaceURI
        self._prefix = prefix
        if localName is not None:
            self._localName = localName
        self.子节点表 = NodeList()
        self.子节点表.append(文本())

    def _get_localName(self):
        try:
            return self._localName
        except AttributeError:
            return self.节点名.split(':', 1)[-1]

    def _get_specified(self):
        return self.已指定

    def _get_name(self):
        return self._name

    def _set_name(self, value):
        self._name = value
        if self.所有者元素 is not None:
            _clear_id_cache(self.所有者元素)
    节点名 = 名字 = property(_get_name, _set_name)

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value
        self.子节点表[0].data = value
        if self.所有者元素 is not None:
            _clear_id_cache(self.所有者元素)
        self.子节点表[0].data = value
    节点值 = 值 = property(_get_value, _set_value)

    def _get_prefix(self):
        return self._prefix

    def _set_prefix(self, prefix):
        nsuri = self.命名空间URI
        if prefix == 'xmlns':
            if nsuri and nsuri != XMLNS_NAMESPACE:
                raise XML工具.dom.NamespaceErr("illegal use of 'xmlns' prefix for the wrong namespace")
        self._prefix = prefix
        if prefix is None:
            newName = self.本地名
        else:
            newName = '%s:%s' % (prefix, self.本地名)
        if self.所有者元素:
            _clear_id_cache(self.所有者元素)
        self.名字 = newName
    前缀 = property(_get_prefix, _set_prefix)

    def 解链(self):
        elem = self.所有者元素
        if elem is not None:
            del elem._attrs[self.节点名]
            del elem._attrsNS[self.命名空间URI, self.本地名]
            if self._is_id:
                self._is_id = False
                elem._magic_id_nodes -= 1
                self.所有者文档._magic_id_count -= 1
        for child in self.子节点表:
            child.unlink()
        del self.子节点表[:]

    def _get_isId(self):
        if self._is_id:
            return True
        doc = self.所有者文档
        elem = self.所有者元素
        if doc is None or elem is None:
            return False
        info = doc._get_elem_info(elem)
        if info is None:
            return False
        if self.命名空间URI:
            return info.isIdNS(self.命名空间URI, self.本地名)
        else:
            return info.isId(self.节点名)

    def _get_schemaType(self):
        doc = self.所有者文档
        elem = self.所有者元素
        if doc is None or elem is None:
            return _no_type
        info = doc._get_elem_info(elem)
        if info is None:
            return _no_type
        if self.命名空间URI:
            return info.getAttributeTypeNS(self.命名空间URI, self.本地名)
        else:
            return info.getAttributeType(self.节点名)
_装类转发(属性节点, {'attributes': '属性表', 'name': '名字', 'nodeName': '节点名', 'nodeType': '节点类型', 'nodeValue': '节点值', 'prefix': '前缀', 'specified': '已指定', 'unlink': '解链', 'value': '值'}, {'attributes': '属性表', 'childNodes': '子节点表', 'localName': '本地名', 'name': '名字', 'namespaceURI': '命名空间URI', 'nodeName': '节点名', 'nodeType': '节点类型', 'nodeValue': '节点值', 'ownerDocument': '所有者文档', 'ownerElement': '所有者元素', 'prefix': '前缀', 'specified': '已指定', 'unlink': '解链', 'value': '值'})
defproperty(属性节点, 'isId', doc='True if this attribute is an ID.')
defproperty(属性节点, 'localName', doc='Namespace-local name of this attribute.')
defproperty(属性节点, 'schemaType', doc='Schema type for this attribute.')

class 命名节点表(object):
    """The attribute list is a transient interface to the underlying
    dictionaries.  Mutations here will change the underlying element's
    dictionary.

    Ordering is imposed artificially and does not reflect the order of
    attributes as found in an input document.
    """
    __slots__ = ('_attrs', '_attrsNS', '_ownerElement')

    def __init__(self, attrs, attrsNS, ownerElement):
        self._attrs = attrs
        self._attrsNS = attrsNS
        self._ownerElement = ownerElement

    def _get_length(self):
        return len(self._attrs)

    def 取项(self, index):
        try:
            return self[list(self._attrs.keys())[index]]
        except IndexError:
            return None

    def items(self):
        L = []
        for node in self._attrs.values():
            L.append((node.nodeName, node.value))
        return L

    def 取项NS(self):
        L = []
        for node in self._attrs.values():
            L.append(((node.namespaceURI, node.localName), node.value))
        return L

    def __contains__(self, key):
        if isinstance(key, str):
            return key in self._attrs
        else:
            return key in self._attrsNS

    def keys(self):
        return self._attrs.keys()

    def 取键NS(self):
        return self._attrsNS.keys()

    def values(self):
        return self._attrs.values()

    def get(self, name, value=None):
        return self._attrs.get(name, value)
    __len__ = _get_length

    def _cmp(self, other):
        if self._attrs is getattr(other, '_attrs', None):
            return 0
        else:
            return (id(self) > id(other)) - (id(self) < id(other))

    def __eq__(self, other):
        return self._cmp(other) == 0

    def __ge__(self, other):
        return self._cmp(other) >= 0

    def __gt__(self, other):
        return self._cmp(other) > 0

    def __le__(self, other):
        return self._cmp(other) <= 0

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __getitem__(self, attname_or_tuple):
        if isinstance(attname_or_tuple, tuple):
            return self._attrsNS[attname_or_tuple]
        else:
            return self._attrs[attname_or_tuple]

    def __setitem__(self, attname, value):
        if isinstance(value, str):
            try:
                node = self._attrs[attname]
            except KeyError:
                node = 属性节点(attname)
                node.ownerDocument = self._ownerElement.ownerDocument
                self.设命名项(node)
            node.value = value
        else:
            if not isinstance(value, 属性节点):
                raise TypeError('value must be a string or Attr object')
            node = value
            self.设命名项(node)

    def 取命名项(self, name):
        try:
            return self._attrs[name]
        except KeyError:
            return None

    def 取命名项NS(self, namespaceURI, localName):
        try:
            return self._attrsNS[namespaceURI, localName]
        except KeyError:
            return None

    def 删命名项(self, name):
        n = self.取命名项(name)
        if n is not None:
            _clear_id_cache(self._ownerElement)
            del self._attrs[n.nodeName]
            del self._attrsNS[n.namespaceURI, n.localName]
            if hasattr(n, 'ownerElement'):
                n.ownerElement = None
            return n
        else:
            raise XML工具.dom.NotFoundErr()

    def 删命名项NS(self, namespaceURI, localName):
        n = self.取命名项NS(namespaceURI, localName)
        if n is not None:
            _clear_id_cache(self._ownerElement)
            del self._attrsNS[n.namespaceURI, n.localName]
            del self._attrs[n.nodeName]
            if hasattr(n, 'ownerElement'):
                n.ownerElement = None
            return n
        else:
            raise XML工具.dom.NotFoundErr()

    def 设命名项(self, node):
        if not isinstance(node, 属性节点):
            raise XML工具.dom.HierarchyRequestErr('%s cannot be child of %s' % (repr(node), repr(self)))
        old = self._attrs.get(node.name)
        if old:
            old.unlink()
        self._attrs[node.name] = node
        self._attrsNS[node.namespaceURI, node.localName] = node
        node.ownerElement = self._ownerElement
        _clear_id_cache(node.ownerElement)
        return old

    def 设命名项NS(self, node):
        return self.设命名项(node)

    def __delitem__(self, attname_or_tuple):
        node = self[attname_or_tuple]
        _clear_id_cache(node.ownerElement)
        node.unlink()

    def __getstate__(self):
        return (self._attrs, self._attrsNS, self._ownerElement)

    def __setstate__(self, state):
        self._attrs, self._attrsNS, self._ownerElement = state
_装类转发(命名节点表, {'getNamedItem': '取命名项', 'getNamedItemNS': '取命名项NS', 'item': '取项', 'itemsNS': '取项NS', 'keysNS': '取键NS', 'removeNamedItem': '删命名项', 'removeNamedItemNS': '删命名项NS', 'setNamedItem': '设命名项', 'setNamedItemNS': '设命名项NS'}, {'getNamedItem': '取命名项', 'getNamedItemNS': '取命名项NS', 'item': '取项', 'itemsNS': '取项NS', 'keysNS': '取键NS', 'removeNamedItem': '删命名项', 'removeNamedItemNS': '删命名项NS', 'setNamedItem': '设命名项', 'setNamedItemNS': '设命名项NS'})
defproperty(命名节点表, 'length', doc='Number of nodes in the NamedNodeMap.')
属性节点表 = 命名节点表

class 类型信息(object):
    __slots__ = ('namespace', 'name')

    def __init__(self, namespace, name):
        self.namespace = namespace
        self.名字 = name

    def __repr__(self):
        if self.namespace:
            return '<%s %r (from %r)>' % (self.__class__.__name__, self.名字, self.namespace)
        else:
            return '<%s %r>' % (self.__class__.__name__, self.名字)

    def _get_name(self):
        return self.名字

    def _get_namespace(self):
        return self.namespace
_装类转发(类型信息, {}, {'name': '名字'})
_no_type = 类型信息(None, None)

class 元素(节点):
    __slots__ = ('ownerDocument', 'parentNode', 'tagName', 'nodeName', 'prefix', 'namespaceURI', '_localName', 'childNodes', '_attrs', '_attrsNS', 'nextSibling', 'previousSibling')
    节点类型 = 节点.ELEMENT_NODE
    节点值 = None
    模式类型 = _no_type
    _magic_id_nodes = 0
    _child_node_types = (节点.ELEMENT_NODE, 节点.PROCESSING_INSTRUCTION_NODE, 节点.COMMENT_NODE, 节点.TEXT_NODE, 节点.CDATA_SECTION_NODE, 节点.ENTITY_REFERENCE_NODE)

    def __init__(self, tagName, namespaceURI=EMPTY_NAMESPACE, prefix=None, localName=None):
        self.所有者文档 = None
        self.父节点 = None
        self.标签名 = self.节点名 = tagName
        self.前缀 = prefix
        self.命名空间URI = namespaceURI
        self.子节点表 = NodeList()
        self.后兄弟 = self.前兄弟 = None
        self._attrs = None
        self._attrsNS = None

    def _ensure_attributes(self):
        if self._attrs is None:
            self._attrs = {}
            self._attrsNS = {}

    def _get_localName(self):
        try:
            return self._localName
        except AttributeError:
            return self.标签名.split(':', 1)[-1]

    def _get_tagName(self):
        return self.标签名

    def 解链(self):
        if self._attrs is not None:
            for attr in list(self._attrs.values()):
                attr.unlink()
        self._attrs = None
        self._attrsNS = None
        节点.解链(self)

    def 取属性(self, attname):
        """Returns the value of the specified attribute.

        Returns the value of the element's attribute named attname as
        a string. An empty string is returned if the element does not
        have such an attribute. Note that an empty string may also be
        returned as an explicitly given attribute value, use the
        hasAttribute method to distinguish these two cases.
        """
        if self._attrs is None:
            return ''
        try:
            return self._attrs[attname].value
        except KeyError:
            return ''

    def 取属性NS(self, namespaceURI, localName):
        if self._attrsNS is None:
            return ''
        try:
            return self._attrsNS[namespaceURI, localName].value
        except KeyError:
            return ''

    def 设属性(self, attname, value):
        attr = self.取属性节点(attname)
        if attr is None:
            attr = 属性节点(attname)
            attr.value = value
            attr.ownerDocument = self.所有者文档
            self.设属性节点(attr)
        elif value != attr.value:
            attr.value = value
            if attr.isId:
                _clear_id_cache(self)

    def 设属性NS(self, namespaceURI, qualifiedName, value):
        前缀, localname = _nssplit(qualifiedName)
        attr = self.取属性节点NS(namespaceURI, localname)
        if attr is None:
            attr = 属性节点(qualifiedName, namespaceURI, localname, 前缀)
            attr.value = value
            attr.ownerDocument = self.所有者文档
            self.设属性节点(attr)
        else:
            if value != attr.value:
                attr.value = value
                if attr.isId:
                    _clear_id_cache(self)
            if attr.prefix != 前缀:
                attr.prefix = 前缀
                attr.nodeName = qualifiedName

    def 取属性节点(self, attrname):
        if self._attrs is None:
            return None
        return self._attrs.get(attrname)

    def 取属性节点NS(self, namespaceURI, localName):
        if self._attrsNS is None:
            return None
        return self._attrsNS.get((namespaceURI, localName))

    def 设属性节点(self, attr):
        if attr.ownerElement not in (None, self):
            raise XML工具.dom.InuseAttributeErr('attribute node already owned')
        self._ensure_attributes()
        old1 = self._attrs.get(attr.name, None)
        if old1 is not None:
            self.删属性节点(old1)
        old2 = self._attrsNS.get((attr.namespaceURI, attr.localName), None)
        if old2 is not None and old2 is not old1:
            self.删属性节点(old2)
        _set_attribute_node(self, attr)
        if old1 is not attr:
            return old1
        if old2 is not attr:
            return old2
    设属性节点NS = 设属性节点

    def 删属性(self, name):
        if self._attrsNS is None:
            raise XML工具.dom.NotFoundErr()
        try:
            attr = self._attrs[name]
        except KeyError:
            raise XML工具.dom.NotFoundErr()
        self.删属性节点(attr)

    def 删属性NS(self, namespaceURI, localName):
        if self._attrsNS is None:
            raise XML工具.dom.NotFoundErr()
        try:
            attr = self._attrsNS[namespaceURI, localName]
        except KeyError:
            raise XML工具.dom.NotFoundErr()
        self.删属性节点(attr)

    def 删属性节点(self, node):
        if node is None:
            raise XML工具.dom.NotFoundErr()
        try:
            self._attrs[node.name]
        except KeyError:
            raise XML工具.dom.NotFoundErr()
        _clear_id_cache(self)
        node.unlink()
        node.ownerDocument = self.所有者文档
        return node
    removeAttributeNodeNS = 删属性节点

    def 有该属性吗(self, name):
        """Checks whether the element has an attribute with the specified name.

        Returns True if the element has an attribute with the specified name.
        Otherwise, returns False.
        """
        if self._attrs is None:
            return False
        return name in self._attrs

    def 有该属性吗NS(self, namespaceURI, localName):
        if self._attrsNS is None:
            return False
        return (namespaceURI, localName) in self._attrsNS

    def 按标签名取元素(self, name):
        """Returns all descendant elements with the given tag name.

        Returns the list of all descendant elements (not direct children
        only) with the specified tag name.
        """
        return _get_elements_by_tagName_helper(self, name, NodeList())

    def 按标签名取元素NS(self, namespaceURI, localName):
        return _get_elements_by_tagName_ns_helper(self, namespaceURI, localName, NodeList())

    def __repr__(self):
        return '<DOM Element: %s at %#x>' % (self.标签名, id(self))

    def 写出XML(self, writer, indent='', addindent='', newl=''):
        """Write an XML element to a file-like object

        Write the element to the writer object that must provide
        a write method (e.g. a file or StringIO object).
        """
        writer.write(indent + '<' + self.标签名)
        attrs = self._get_attributes()
        for a_name in attrs.keys():
            writer.write(' %s="' % a_name)
            _write_data(writer, attrs[a_name].value, True)
            writer.write('"')
        if self.子节点表:
            writer.write('>')
            if len(self.子节点表) == 1 and self.子节点表[0].nodeType in (节点.TEXT_NODE, 节点.CDATA_SECTION_NODE):
                self.子节点表[0].writexml(writer, '', '', '')
            else:
                writer.write(newl)
                for node in self.子节点表:
                    node.writexml(writer, indent + addindent, addindent, newl)
                writer.write(indent)
            writer.write('</%s>%s' % (self.标签名, newl))
        else:
            writer.write('/>%s' % newl)

    def _get_attributes(self):
        self._ensure_attributes()
        return 命名节点表(self._attrs, self._attrsNS, self)

    def 有属性吗(self):
        if self._attrs:
            return True
        else:
            return False

    def 设ID属性(self, name):
        idAttr = self.取属性节点(name)
        self.设ID属性节点(idAttr)

    def 设ID属性NS(self, namespaceURI, localName):
        idAttr = self.取属性节点NS(namespaceURI, localName)
        self.设ID属性节点(idAttr)

    def 设ID属性节点(self, idAttr):
        if idAttr is None or not self.同节点吗(idAttr.ownerElement):
            raise XML工具.dom.NotFoundErr()
        if _get_containing_entref(self) is not None:
            raise XML工具.dom.NoModificationAllowedErr()
        if not idAttr._is_id:
            idAttr._is_id = True
            self._magic_id_nodes += 1
            self.所有者文档._magic_id_count += 1
            _clear_id_cache(self)
_装类转发(元素, {'getAttribute': '取属性', 'getAttributeNS': '取属性NS', 'getAttributeNode': '取属性节点', 'getAttributeNodeNS': '取属性节点NS', 'getElementsByTagName': '按标签名取元素', 'getElementsByTagNameNS': '按标签名取元素NS', 'hasAttribute': '有该属性吗', 'hasAttributeNS': '有该属性吗NS', 'hasAttributes': '有属性吗', 'nodeType': '节点类型', 'nodeValue': '节点值', 'removeAttribute': '删属性', 'removeAttributeNS': '删属性NS', 'removeAttributeNode': '删属性节点', 'schemaType': '模式类型', 'setAttribute': '设属性', 'setAttributeNS': '设属性NS', 'setAttributeNode': '设属性节点', 'setAttributeNodeNS': '设属性节点NS', 'setIdAttribute': '设ID属性', 'setIdAttributeNS': '设ID属性NS', 'setIdAttributeNode': '设ID属性节点', 'unlink': '解链', 'writexml': '写出XML'}, {'childNodes': '子节点表', 'getAttribute': '取属性', 'getAttributeNS': '取属性NS', 'getAttributeNode': '取属性节点', 'getAttributeNodeNS': '取属性节点NS', 'getElementsByTagName': '按标签名取元素', 'getElementsByTagNameNS': '按标签名取元素NS', 'hasAttribute': '有该属性吗', 'hasAttributeNS': '有该属性吗NS', 'hasAttributes': '有属性吗', 'isSameNode': '同节点吗', 'namespaceURI': '命名空间URI', 'nextSibling': '后兄弟', 'nodeName': '节点名', 'nodeType': '节点类型', 'nodeValue': '节点值', 'ownerDocument': '所有者文档', 'parentNode': '父节点', 'prefix': '前缀', 'previousSibling': '前兄弟', 'removeAttribute': '删属性', 'removeAttributeNS': '删属性NS', 'removeAttributeNode': '删属性节点', 'schemaType': '模式类型', 'setAttribute': '设属性', 'setAttributeNS': '设属性NS', 'setAttributeNode': '设属性节点', 'setAttributeNodeNS': '设属性节点NS', 'setIdAttribute': '设ID属性', 'setIdAttributeNS': '设ID属性NS', 'setIdAttributeNode': '设ID属性节点', 'tagName': '标签名', 'unlink': '解链', 'writexml': '写出XML'})
defproperty(元素, 'attributes', doc='NamedNodeMap of attributes on the element.')
defproperty(元素, 'localName', doc='Namespace-local name of this element.')

def _set_attribute_node(element, attr):
    _clear_id_cache(element)
    element._ensure_attributes()
    element._attrs[attr.name] = attr
    element._attrsNS[attr.namespaceURI, attr.localName] = attr
    attr.ownerElement = element

class 无子类:
    """Mixin that makes childless-ness easy to implement and avoids
    the complexity of the Node methods that deal with children.
    """
    __slots__ = ()
    属性表 = None
    子节点表 = EmptyNodeList()
    首个子节点 = None
    末个子节点 = None

    def _get_firstChild(self):
        return None

    def _get_lastChild(self):
        return None

    def 追加子节点(self, node):
        raise XML工具.dom.HierarchyRequestErr(self.节点名 + ' nodes cannot have children')

    def 有子节点吗(self):
        return False

    def 插到前面(self, newChild, refChild):
        raise XML工具.dom.HierarchyRequestErr(self.节点名 + ' nodes do not have children')

    def 删子节点(self, oldChild):
        raise XML工具.dom.NotFoundErr(self.节点名 + ' nodes do not have children')

    def 规范化(self):
        pass

    def 替换子节点(self, newChild, oldChild):
        raise XML工具.dom.HierarchyRequestErr(self.节点名 + ' nodes do not have children')
_装类转发(无子类, {'appendChild': '追加子节点', 'attributes': '属性表', 'childNodes': '子节点表', 'firstChild': '首个子节点', 'hasChildNodes': '有子节点吗', 'insertBefore': '插到前面', 'lastChild': '末个子节点', 'normalize': '规范化', 'removeChild': '删子节点', 'replaceChild': '替换子节点'}, {'appendChild': '追加子节点', 'attributes': '属性表', 'childNodes': '子节点表', 'firstChild': '首个子节点', 'hasChildNodes': '有子节点吗', 'insertBefore': '插到前面', 'lastChild': '末个子节点', 'nodeName': '节点名', 'normalize': '规范化', 'removeChild': '删子节点', 'replaceChild': '替换子节点'})

class 处理指令(无子类, 节点):
    节点类型 = 节点.PROCESSING_INSTRUCTION_NODE
    __slots__ = ('target', 'data')

    def __init__(self, target, data):
        self.target = target
        self.数据 = data

    def _get_nodeValue(self):
        return self.数据

    def _set_nodeValue(self, value):
        self.数据 = value
    节点值 = property(_get_nodeValue, _set_nodeValue)

    def _get_nodeName(self):
        return self.target

    def _set_nodeName(self, value):
        self.target = value
    节点名 = property(_get_nodeName, _set_nodeName)

    def 写出XML(self, writer, indent='', addindent='', newl=''):
        writer.write('%s<?%s %s?>%s' % (indent, self.target, self.数据, newl))
_装类转发(处理指令, {'nodeName': '节点名', 'nodeType': '节点类型', 'nodeValue': '节点值', 'writexml': '写出XML'}, {'data': '数据', 'nodeName': '节点名', 'nodeType': '节点类型', 'nodeValue': '节点值', 'writexml': '写出XML'})

class 字符数据(无子类, 节点):
    __slots__ = ('_data', 'ownerDocument', 'parentNode', 'previousSibling', 'nextSibling')

    def __init__(self):
        self.所有者文档 = self.父节点 = None
        self.前兄弟 = self.后兄弟 = None
        self._data = ''
        节点.__init__(self)

    def _get_length(self):
        return len(self.数据)
    __len__ = _get_length

    def _get_data(self):
        return self._data

    def _set_data(self, data):
        self._data = data
    数据 = 节点值 = property(_get_data, _set_data)

    def __repr__(self):
        数据 = self.数据
        if len(数据) > 10:
            dotdotdot = '...'
        else:
            dotdotdot = ''
        return '<DOM %s node "%r%s">' % (self.__class__.__name__, 数据[0:10], dotdotdot)

    def 取子串数据(self, offset, count):
        if offset < 0:
            raise XML工具.dom.IndexSizeErr('offset cannot be negative')
        if offset >= len(self.数据):
            raise XML工具.dom.IndexSizeErr('offset cannot be beyond end of data')
        if count < 0:
            raise XML工具.dom.IndexSizeErr('count cannot be negative')
        return self.数据[offset:offset + count]

    def 追加数据(self, arg):
        self.数据 = self.数据 + arg

    def 插入数据(self, offset, arg):
        if offset < 0:
            raise XML工具.dom.IndexSizeErr('offset cannot be negative')
        if offset >= len(self.数据):
            raise XML工具.dom.IndexSizeErr('offset cannot be beyond end of data')
        if arg:
            self.数据 = '%s%s%s' % (self.数据[:offset], arg, self.数据[offset:])

    def 删除数据(self, offset, count):
        if offset < 0:
            raise XML工具.dom.IndexSizeErr('offset cannot be negative')
        if offset >= len(self.数据):
            raise XML工具.dom.IndexSizeErr('offset cannot be beyond end of data')
        if count < 0:
            raise XML工具.dom.IndexSizeErr('count cannot be negative')
        if count:
            self.数据 = self.数据[:offset] + self.数据[offset + count:]

    def 替换数据(self, offset, count, arg):
        if offset < 0:
            raise XML工具.dom.IndexSizeErr('offset cannot be negative')
        if offset >= len(self.数据):
            raise XML工具.dom.IndexSizeErr('offset cannot be beyond end of data')
        if count < 0:
            raise XML工具.dom.IndexSizeErr('count cannot be negative')
        if count:
            self.数据 = '%s%s%s' % (self.数据[:offset], arg, self.数据[offset + count:])
_装类转发(字符数据, {'appendData': '追加数据', 'data': '数据', 'deleteData': '删除数据', 'insertData': '插入数据', 'nodeValue': '节点值', 'replaceData': '替换数据', 'substringData': '取子串数据'}, {'appendData': '追加数据', 'data': '数据', 'deleteData': '删除数据', 'insertData': '插入数据', 'nextSibling': '后兄弟', 'nodeValue': '节点值', 'ownerDocument': '所有者文档', 'parentNode': '父节点', 'previousSibling': '前兄弟', 'replaceData': '替换数据', 'substringData': '取子串数据'})
defproperty(字符数据, 'length', doc='Length of the string data.')

class 文本(字符数据):
    __slots__ = ()
    节点类型 = 节点.TEXT_NODE
    节点名 = '#text'
    属性表 = None

    def 切分文本(self, offset):
        if offset < 0 or offset > len(self.数据):
            raise XML工具.dom.IndexSizeErr('illegal offset value')
        newText = self.__class__()
        newText.data = self.数据[offset:]
        newText.ownerDocument = self.所有者文档
        next = self.后兄弟
        if self.父节点 and self in self.父节点.childNodes:
            if next is None:
                self.父节点.appendChild(newText)
            else:
                self.父节点.insertBefore(newText, next)
        self.数据 = self.数据[:offset]
        return newText

    def 写出XML(self, writer, indent='', addindent='', newl=''):
        _write_data(writer, '%s%s%s' % (indent, self.数据, newl), False)

    def _get_wholeText(self):
        L = [self.数据]
        n = self.前兄弟
        while n is not None:
            if n.nodeType in (节点.TEXT_NODE, 节点.CDATA_SECTION_NODE):
                L.insert(0, n.data)
                n = n.previousSibling
            else:
                break
        n = self.后兄弟
        while n is not None:
            if n.nodeType in (节点.TEXT_NODE, 节点.CDATA_SECTION_NODE):
                L.append(n.data)
                n = n.nextSibling
            else:
                break
        return ''.join(L)

    def 替换整段文本(self, content):
        parent = self.父节点
        n = self.前兄弟
        while n is not None:
            if n.nodeType in (节点.TEXT_NODE, 节点.CDATA_SECTION_NODE):
                next = n.previousSibling
                parent.removeChild(n)
                n = next
            else:
                break
        n = self.后兄弟
        if not content:
            parent.removeChild(self)
        while n is not None:
            if n.nodeType in (节点.TEXT_NODE, 节点.CDATA_SECTION_NODE):
                next = n.nextSibling
                parent.removeChild(n)
                n = next
            else:
                break
        if content:
            self.数据 = content
            return self
        else:
            return None

    def _get_isWhitespaceInElementContent(self):
        if self.数据.strip():
            return False
        elem = _get_containing_element(self)
        if elem is None:
            return False
        info = self.所有者文档._get_elem_info(elem)
        if info is None:
            return False
        else:
            return info.isElementContent()
_装类转发(文本, {'attributes': '属性表', 'nodeName': '节点名', 'nodeType': '节点类型', 'replaceWholeText': '替换整段文本', 'splitText': '切分文本', 'writexml': '写出XML'}, {'attributes': '属性表', 'data': '数据', 'nextSibling': '后兄弟', 'nodeName': '节点名', 'nodeType': '节点类型', 'ownerDocument': '所有者文档', 'parentNode': '父节点', 'previousSibling': '前兄弟', 'replaceWholeText': '替换整段文本', 'splitText': '切分文本', 'writexml': '写出XML'})
defproperty(文本, 'isWhitespaceInElementContent', doc='True iff this text node contains only whitespace and is in element content.')
defproperty(文本, 'wholeText', doc='The text of all logically-adjacent text nodes.')

def _get_containing_element(node):
    c = node.parentNode
    while c is not None:
        if c.nodeType == 节点.ELEMENT_NODE:
            return c
        c = c.parentNode
    return None

def _get_containing_entref(node):
    c = node.parentNode
    while c is not None:
        if c.nodeType == 节点.ENTITY_REFERENCE_NODE:
            return c
        c = c.parentNode
    return None

class 注释(字符数据):
    节点类型 = 节点.COMMENT_NODE
    节点名 = '#comment'

    def __init__(self, data):
        字符数据.__init__(self)
        self._data = data

    def 写出XML(self, writer, indent='', addindent='', newl=''):
        if '--' in self.数据:
            raise ValueError("'--' is not allowed in a comment node")
        writer.write('%s<!--%s-->%s' % (indent, self.数据, newl))
_装类转发(注释, {'nodeName': '节点名', 'nodeType': '节点类型', 'writexml': '写出XML'}, {'data': '数据', 'nodeName': '节点名', 'nodeType': '节点类型', 'writexml': '写出XML'})

class CDATA节(文本):
    __slots__ = ()
    节点类型 = 节点.CDATA_SECTION_NODE
    节点名 = '#cdata-section'

    def 写出XML(self, writer, indent='', addindent='', newl=''):
        if self.数据.find(']]>') >= 0:
            raise ValueError("']]>' not allowed in a CDATA section")
        writer.write('<![CDATA[%s]]>' % self.数据)
_装类转发(CDATA节, {'nodeName': '节点名', 'nodeType': '节点类型', 'writexml': '写出XML'}, {'data': '数据', 'nodeName': '节点名', 'nodeType': '节点类型', 'writexml': '写出XML'})

class 只读顺序节点表(object):
    __slots__ = ('_seq',)

    def __init__(self, seq=()):
        self._seq = seq

    def __len__(self):
        return len(self._seq)

    def _get_length(self):
        return len(self._seq)

    def 取命名项(self, name):
        for n in self._seq:
            if n.nodeName == name:
                return n

    def 取命名项NS(self, namespaceURI, localName):
        for n in self._seq:
            if n.namespaceURI == namespaceURI and n.localName == localName:
                return n

    def __getitem__(self, name_or_tuple):
        if isinstance(name_or_tuple, tuple):
            node = self.取命名项NS(*name_or_tuple)
        else:
            node = self.取命名项(name_or_tuple)
        if node is None:
            raise KeyError(name_or_tuple)
        return node

    def 取项(self, index):
        if index < 0:
            return None
        try:
            return self._seq[index]
        except IndexError:
            return None

    def 删命名项(self, name):
        raise XML工具.dom.NoModificationAllowedErr('NamedNodeMap instance is read-only')

    def 删命名项NS(self, namespaceURI, localName):
        raise XML工具.dom.NoModificationAllowedErr('NamedNodeMap instance is read-only')

    def 设命名项(self, node):
        raise XML工具.dom.NoModificationAllowedErr('NamedNodeMap instance is read-only')

    def 设命名项NS(self, node):
        raise XML工具.dom.NoModificationAllowedErr('NamedNodeMap instance is read-only')

    def __getstate__(self):
        return [self._seq]

    def __setstate__(self, state):
        self._seq = state[0]
_装类转发(只读顺序节点表, {'getNamedItem': '取命名项', 'getNamedItemNS': '取命名项NS', 'item': '取项', 'removeNamedItem': '删命名项', 'removeNamedItemNS': '删命名项NS', 'setNamedItem': '设命名项', 'setNamedItemNS': '设命名项NS'}, {'getNamedItem': '取命名项', 'getNamedItemNS': '取命名项NS', 'item': '取项', 'removeNamedItem': '删命名项', 'removeNamedItemNS': '删命名项NS', 'setNamedItem': '设命名项', 'setNamedItemNS': '设命名项NS'})
defproperty(只读顺序节点表, 'length', doc='Number of entries in the NamedNodeMap.')

class 已标识:
    """Mix-in class that supports the publicId and systemId attributes."""
    __slots__ = ('publicId', 'systemId')

    def _identified_mixin_init(self, publicId, systemId):
        self.公共标识 = publicId
        self.系统标识 = systemId

    def _get_publicId(self):
        return self.公共标识

    def _get_systemId(self):
        return self.系统标识
_装类转发(已标识, {}, {'publicId': '公共标识', 'systemId': '系统标识'})

class 文档类型(已标识, 无子类, 节点):
    节点类型 = 节点.DOCUMENT_TYPE_NODE
    节点值 = None
    名字 = None
    公共标识 = None
    系统标识 = None
    内部子集 = None

    def __init__(self, qualifiedName):
        self.entities = 只读顺序节点表()
        self.notations = 只读顺序节点表()
        if qualifiedName:
            前缀, localname = _nssplit(qualifiedName)
            self.名字 = localname
        self.节点名 = self.名字

    def _get_internalSubset(self):
        return self.内部子集

    def 克隆节点(self, deep):
        if self.所有者文档 is None:
            clone = 文档类型(None)
            clone.name = self.名字
            clone.nodeName = self.名字
            operation = XML工具.dom.UserDataHandler.NODE_CLONED
            if deep:
                clone.entities._seq = []
                clone.notations._seq = []
                for n in self.notations._seq:
                    notation = 记法(n.nodeName, n.publicId, n.systemId)
                    clone.notations._seq.append(notation)
                    n._call_user_data_handler(operation, n, notation)
                for e in self.entities._seq:
                    entity = 实体(e.nodeName, e.publicId, e.systemId, e.notationName)
                    entity.actualEncoding = e.actualEncoding
                    entity.encoding = e.encoding
                    entity.version = e.version
                    clone.entities._seq.append(entity)
                    e._call_user_data_handler(operation, e, entity)
            self._call_user_data_handler(operation, self, clone)
            return clone
        else:
            return None

    def 写出XML(self, writer, indent='', addindent='', newl=''):
        writer.write('<!DOCTYPE ')
        writer.write(self.名字)
        if self.公共标识:
            writer.write("%s  PUBLIC '%s'%s  '%s'" % (newl, self.公共标识, newl, self.系统标识))
        elif self.系统标识:
            writer.write("%s  SYSTEM '%s'" % (newl, self.系统标识))
        if self.内部子集 is not None:
            writer.write(' [')
            writer.write(self.内部子集)
            writer.write(']')
        writer.write('>' + newl)
_装类转发(文档类型, {'cloneNode': '克隆节点', 'internalSubset': '内部子集', 'name': '名字', 'nodeType': '节点类型', 'nodeValue': '节点值', 'publicId': '公共标识', 'systemId': '系统标识', 'writexml': '写出XML'}, {'cloneNode': '克隆节点', 'internalSubset': '内部子集', 'name': '名字', 'nodeName': '节点名', 'nodeType': '节点类型', 'nodeValue': '节点值', 'ownerDocument': '所有者文档', 'publicId': '公共标识', 'systemId': '系统标识', 'writexml': '写出XML'})

class 实体(已标识, 节点):
    属性表 = None
    节点类型 = 节点.ENTITY_NODE
    节点值 = None
    实际编码 = None
    编码 = None
    版本 = None

    def __init__(self, name, publicId, systemId, notation):
        self.节点名 = name
        self.notationName = notation
        self.子节点表 = NodeList()
        self._identified_mixin_init(publicId, systemId)

    def _get_actualEncoding(self):
        return self.实际编码

    def _get_encoding(self):
        return self.编码

    def _get_version(self):
        return self.版本

    def 追加子节点(self, newChild):
        raise XML工具.dom.HierarchyRequestErr('cannot append children to an entity node')

    def 插到前面(self, newChild, refChild):
        raise XML工具.dom.HierarchyRequestErr('cannot insert children below an entity node')

    def 删子节点(self, oldChild):
        raise XML工具.dom.HierarchyRequestErr('cannot remove children from an entity node')

    def 替换子节点(self, newChild, oldChild):
        raise XML工具.dom.HierarchyRequestErr('cannot replace children of an entity node')
_装类转发(实体, {'actualEncoding': '实际编码', 'appendChild': '追加子节点', 'attributes': '属性表', 'encoding': '编码', 'insertBefore': '插到前面', 'nodeType': '节点类型', 'nodeValue': '节点值', 'removeChild': '删子节点', 'replaceChild': '替换子节点', 'version': '版本'}, {'actualEncoding': '实际编码', 'appendChild': '追加子节点', 'attributes': '属性表', 'childNodes': '子节点表', 'encoding': '编码', 'insertBefore': '插到前面', 'nodeName': '节点名', 'nodeType': '节点类型', 'nodeValue': '节点值', 'removeChild': '删子节点', 'replaceChild': '替换子节点', 'version': '版本'})

class 记法(已标识, 无子类, 节点):
    节点类型 = 节点.NOTATION_NODE
    节点值 = None

    def __init__(self, name, publicId, systemId):
        self.节点名 = name
        self._identified_mixin_init(publicId, systemId)
_装类转发(记法, {'nodeType': '节点类型', 'nodeValue': '节点值'}, {'nodeName': '节点名', 'nodeType': '节点类型', 'nodeValue': '节点值'})

class DOM实现(DOMImplementationLS):
    _features = [('core', '1.0'), ('core', '2.0'), ('core', None), ('xml', '1.0'), ('xml', '2.0'), ('xml', None), ('ls-load', '3.0'), ('ls-load', None)]

    def 有特性吗(self, feature, version):
        if version == '':
            version = None
        return (feature.lower(), version) in self._features

    def 建文档(self, namespaceURI, qualifiedName, doctype):
        if doctype and doctype.parentNode is not None:
            raise XML工具.dom.WrongDocumentErr('doctype object owned by another DOM tree')
        doc = self._create_document()
        add_root_element = not (namespaceURI is None and qualifiedName is None and (doctype is None))
        if not qualifiedName and add_root_element:
            raise XML工具.dom.InvalidCharacterErr('Element with no name')
        if add_root_element:
            前缀, localname = _nssplit(qualifiedName)
            if 前缀 == 'xml' and namespaceURI != 'http://www.w3.org/XML/1998/namespace':
                raise XML工具.dom.NamespaceErr("illegal use of 'xml' prefix")
            if 前缀 and (not namespaceURI):
                raise XML工具.dom.NamespaceErr('illegal use of prefix without namespaces')
            element = doc.createElementNS(namespaceURI, qualifiedName)
            if doctype:
                doc.appendChild(doctype)
            doc.appendChild(element)
        if doctype:
            doctype.parentNode = doctype.ownerDocument = doc
        doc.doctype = doctype
        doc.implementation = self
        return doc

    def 建文档类型(self, qualifiedName, publicId, systemId):
        doctype = 文档类型(qualifiedName)
        doctype.publicId = publicId
        doctype.systemId = systemId
        return doctype

    def 取接口(self, feature):
        if self.有特性吗(feature, None):
            return self
        else:
            return None

    def _create_document(self):
        return 文档()
_装类转发(DOM实现, {'createDocument': '建文档', 'createDocumentType': '建文档类型', 'getInterface': '取接口', 'hasFeature': '有特性吗'}, {'createDocument': '建文档', 'createDocumentType': '建文档类型', 'getInterface': '取接口', 'hasFeature': '有特性吗'})

class 元素信息(object):
    """Object that represents content-model information for an element.

    This implementation is not expected to be used in practice; DOM
    builders should provide implementations which do the right thing
    using information available to it.

    """
    __slots__ = ('tagName',)

    def __init__(self, name):
        self.标签名 = name

    def 取属性类型(self, aname):
        return _no_type

    def 取属性类型NS(self, namespaceURI, localName):
        return _no_type

    def 是元素内容吗(self):
        return False

    def 是空吗(self):
        """Returns true iff this element is declared to have an EMPTY
        content model."""
        return False

    def 是ID吗(self, aname):
        """Returns true iff the named attribute is a DTD-style ID."""
        return False

    def 是ID吗NS(self, namespaceURI, localName):
        """Returns true iff the identified attribute is a DTD-style ID."""
        return False

    def __getstate__(self):
        return self.标签名

    def __setstate__(self, state):
        self.标签名 = state
_装类转发(元素信息, {'getAttributeType': '取属性类型', 'getAttributeTypeNS': '取属性类型NS', 'isElementContent': '是元素内容吗', 'isEmpty': '是空吗', 'isId': '是ID吗', 'isIdNS': '是ID吗NS'}, {'getAttributeType': '取属性类型', 'getAttributeTypeNS': '取属性类型NS', 'isElementContent': '是元素内容吗', 'isEmpty': '是空吗', 'isId': '是ID吗', 'isIdNS': '是ID吗NS', 'tagName': '标签名'})

def _clear_id_cache(node):
    if node.nodeType == 节点.DOCUMENT_NODE:
        node._id_cache.clear()
        node._id_search_stack = None
    elif node.ownerDocument:
        node.ownerDocument._id_cache.clear()
        node.ownerDocument._id_search_stack = None

class 文档(节点, DocumentLS):
    __slots__ = ('_elem_info', 'doctype', '_id_search_stack', 'childNodes', '_id_cache')
    _child_node_types = (节点.ELEMENT_NODE, 节点.PROCESSING_INSTRUCTION_NODE, 节点.COMMENT_NODE, 节点.DOCUMENT_TYPE_NODE)
    实现 = DOM实现()
    节点类型 = 节点.DOCUMENT_NODE
    节点名 = '#document'
    节点值 = None
    属性表 = None
    父节点 = None
    前兄弟 = 后兄弟 = None
    实际编码 = None
    编码 = None
    standalone = None
    版本 = None
    strictErrorChecking = False
    errorHandler = None
    documentURI = None
    _magic_id_count = 0

    def __init__(self):
        self.doctype = None
        self.子节点表 = NodeList()
        self._elem_info = {}
        self._id_cache = {}
        self._id_search_stack = None

    def _get_elem_info(self, element):
        if element.namespaceURI:
            key = (element.namespaceURI, element.localName)
        else:
            key = element.tagName
        return self._elem_info.get(key)

    def _get_actualEncoding(self):
        return self.实际编码

    def _get_doctype(self):
        return self.doctype

    def _get_documentURI(self):
        return self.documentURI

    def _get_encoding(self):
        return self.编码

    def _get_errorHandler(self):
        return self.errorHandler

    def _get_standalone(self):
        return self.standalone

    def _get_strictErrorChecking(self):
        return self.strictErrorChecking

    def _get_version(self):
        return self.版本

    def 追加子节点(self, node):
        if node.nodeType not in self._child_node_types:
            raise XML工具.dom.HierarchyRequestErr('%s cannot be child of %s' % (repr(node), repr(self)))
        if node.parentNode is not None:
            node.parentNode.removeChild(node)
        if node.nodeType == 节点.ELEMENT_NODE and self._get_documentElement():
            raise XML工具.dom.HierarchyRequestErr('two document elements disallowed')
        return 节点.追加子节点(self, node)

    def 删子节点(self, oldChild):
        try:
            self.子节点表.remove(oldChild)
        except ValueError:
            raise XML工具.dom.NotFoundErr()
        oldChild.nextSibling = oldChild.previousSibling = None
        oldChild.parentNode = None
        if self.文档元素 is oldChild:
            self.文档元素 = None
        return oldChild

    def _get_documentElement(self):
        for node in self.子节点表:
            if node.nodeType == 节点.ELEMENT_NODE:
                return node

    def 解链(self):
        if self.doctype is not None:
            self.doctype.unlink()
            self.doctype = None
        节点.解链(self)

    def 克隆节点(self, deep):
        if not deep:
            return None
        clone = self.实现.createDocument(None, None, None)
        clone.encoding = self.编码
        clone.standalone = self.standalone
        clone.version = self.版本
        for n in self.子节点表:
            childclone = _clone_node(n, deep, clone)
            assert childclone.ownerDocument.isSameNode(clone)
            clone.childNodes.append(childclone)
            if childclone.nodeType == 节点.DOCUMENT_NODE:
                assert clone.documentElement is None
            elif childclone.nodeType == 节点.DOCUMENT_TYPE_NODE:
                assert clone.doctype is None
                clone.doctype = childclone
            childclone.parentNode = clone
        self._call_user_data_handler(XML工具.dom.UserDataHandler.NODE_CLONED, self, clone)
        return clone

    def 建文档片段(self):
        d = 文档片段()
        d.ownerDocument = self
        return d

    def 建元素(self, tagName):
        e = 元素(tagName)
        e.ownerDocument = self
        return e

    def 建文本节点(self, data):
        if not isinstance(data, str):
            raise TypeError('node contents must be a string')
        t = 文本()
        t.data = data
        t.ownerDocument = self
        return t

    def 建CDATA节(self, data):
        if not isinstance(data, str):
            raise TypeError('node contents must be a string')
        c = CDATA节()
        c.data = data
        c.ownerDocument = self
        return c

    def 建注释(self, data):
        c = 注释(data)
        c.ownerDocument = self
        return c

    def 建处理指令(self, target, data):
        p = 处理指令(target, data)
        p.ownerDocument = self
        return p

    def 建属性(self, qName):
        a = 属性节点(qName)
        a.ownerDocument = self
        a.value = ''
        return a

    def 建元素NS(self, namespaceURI, qualifiedName):
        前缀, 本地名 = _nssplit(qualifiedName)
        e = 元素(qualifiedName, namespaceURI, 前缀)
        e.ownerDocument = self
        return e

    def 建属性NS(self, namespaceURI, qualifiedName):
        前缀, 本地名 = _nssplit(qualifiedName)
        a = 属性节点(qualifiedName, namespaceURI, 本地名, 前缀)
        a.ownerDocument = self
        a.value = ''
        return a

    def _create_entity(self, name, publicId, systemId, notationName):
        e = 实体(name, publicId, systemId, notationName)
        e.ownerDocument = self
        return e

    def _create_notation(self, name, publicId, systemId):
        n = 记法(name, publicId, systemId)
        n.ownerDocument = self
        return n

    def 按ID取元素(self, id):
        if id in self._id_cache:
            return self._id_cache[id]
        if not (self._elem_info or self._magic_id_count):
            return None
        stack = self._id_search_stack
        if stack is None:
            stack = [self.文档元素]
            self._id_search_stack = stack
        elif not stack:
            return None
        result = None
        while stack:
            node = stack.pop()
            stack.extend([child for child in node.childNodes if child.nodeType in _nodeTypes_with_children])
            info = self._get_elem_info(node)
            if info:
                for attr in node.attributes.values():
                    if attr.namespaceURI:
                        if info.isIdNS(attr.namespaceURI, attr.localName):
                            self._id_cache[attr.value] = node
                            if attr.value == id:
                                result = node
                            elif not node._magic_id_nodes:
                                break
                    elif info.isId(attr.name):
                        self._id_cache[attr.value] = node
                        if attr.value == id:
                            result = node
                        elif not node._magic_id_nodes:
                            break
                    elif attr._is_id:
                        self._id_cache[attr.value] = node
                        if attr.value == id:
                            result = node
                        elif node._magic_id_nodes == 1:
                            break
            elif node._magic_id_nodes:
                for attr in node.attributes.values():
                    if attr._is_id:
                        self._id_cache[attr.value] = node
                        if attr.value == id:
                            result = node
            if result is not None:
                break
        return result

    def 按标签名取元素(self, name):
        return _get_elements_by_tagName_helper(self, name, NodeList())

    def 按标签名取元素NS(self, namespaceURI, localName):
        return _get_elements_by_tagName_ns_helper(self, namespaceURI, localName, NodeList())

    def 支持吗(self, feature, version):
        return self.实现.hasFeature(feature, version)

    def 导入节点(self, node, deep):
        if node.nodeType == 节点.DOCUMENT_NODE:
            raise XML工具.dom.NotSupportedErr('cannot import document nodes')
        elif node.nodeType == 节点.DOCUMENT_TYPE_NODE:
            raise XML工具.dom.NotSupportedErr('cannot import document type nodes')
        return _clone_node(node, deep, self)

    def 写出XML(self, writer, indent='', addindent='', newl='', encoding=None, standalone=None):
        declarations = []
        if encoding:
            declarations.append(f'encoding="{encoding}"')
        if standalone is not None:
            declarations.append(f'''standalone="{('yes' if standalone else 'no')}"''')
        writer.write(f"""<?xml version="1.0" {' '.join(declarations)}?>{newl}""")
        for node in self.子节点表:
            node.writexml(writer, indent, addindent, newl)

    def 重命名节点(self, n, namespaceURI, name):
        if n.ownerDocument is not self:
            raise XML工具.dom.WrongDocumentErr('cannot rename nodes from other documents;\nexpected %s,\nfound %s' % (self, n.ownerDocument))
        if n.nodeType not in (节点.ELEMENT_NODE, 节点.ATTRIBUTE_NODE):
            raise XML工具.dom.NotSupportedErr('renameNode() only applies to element and attribute nodes')
        if namespaceURI != EMPTY_NAMESPACE:
            if ':' in name:
                前缀, 本地名 = name.split(':', 1)
                if 前缀 == 'xmlns' and namespaceURI != XML工具.dom.XMLNS_NAMESPACE:
                    raise XML工具.dom.NamespaceErr("illegal use of 'xmlns' prefix")
            else:
                if name == 'xmlns' and namespaceURI != XML工具.dom.XMLNS_NAMESPACE and (n.nodeType == 节点.ATTRIBUTE_NODE):
                    raise XML工具.dom.NamespaceErr("illegal use of the 'xmlns' attribute")
                前缀 = None
                本地名 = name
        else:
            前缀 = None
            本地名 = None
        if n.nodeType == 节点.ATTRIBUTE_NODE:
            element = n.ownerElement
            if element is not None:
                is_id = n._is_id
                element.removeAttributeNode(n)
        else:
            element = None
        n.prefix = 前缀
        n._localName = 本地名
        n.namespaceURI = namespaceURI
        n.nodeName = name
        if n.nodeType == 节点.ELEMENT_NODE:
            n.tagName = name
        else:
            n.name = name
            if element is not None:
                element.setAttributeNode(n)
                if is_id:
                    element.setIdAttributeNode(n)
        return n
_装类转发(文档, {'actualEncoding': '实际编码', 'appendChild': '追加子节点', 'attributes': '属性表', 'cloneNode': '克隆节点', 'createAttribute': '建属性', 'createAttributeNS': '建属性NS', 'createCDATASection': '建CDATA节', 'createComment': '建注释', 'createDocumentFragment': '建文档片段', 'createElement': '建元素', 'createElementNS': '建元素NS', 'createProcessingInstruction': '建处理指令', 'createTextNode': '建文本节点', 'encoding': '编码', 'getElementById': '按ID取元素', 'getElementsByTagName': '按标签名取元素', 'getElementsByTagNameNS': '按标签名取元素NS', 'implementation': '实现', 'importNode': '导入节点', 'isSupported': '支持吗', 'nextSibling': '后兄弟', 'nodeName': '节点名', 'nodeType': '节点类型', 'nodeValue': '节点值', 'parentNode': '父节点', 'previousSibling': '前兄弟', 'removeChild': '删子节点', 'renameNode': '重命名节点', 'unlink': '解链', 'version': '版本', 'writexml': '写出XML'}, {'actualEncoding': '实际编码', 'appendChild': '追加子节点', 'attributes': '属性表', 'childNodes': '子节点表', 'cloneNode': '克隆节点', 'createAttribute': '建属性', 'createAttributeNS': '建属性NS', 'createCDATASection': '建CDATA节', 'createComment': '建注释', 'createDocumentFragment': '建文档片段', 'createElement': '建元素', 'createElementNS': '建元素NS', 'createProcessingInstruction': '建处理指令', 'createTextNode': '建文本节点', 'documentElement': '文档元素', 'encoding': '编码', 'getElementById': '按ID取元素', 'getElementsByTagName': '按标签名取元素', 'getElementsByTagNameNS': '按标签名取元素NS', 'implementation': '实现', 'importNode': '导入节点', 'isSupported': '支持吗', 'nextSibling': '后兄弟', 'nodeName': '节点名', 'nodeType': '节点类型', 'nodeValue': '节点值', 'parentNode': '父节点', 'previousSibling': '前兄弟', 'removeChild': '删子节点', 'renameNode': '重命名节点', 'unlink': '解链', 'version': '版本', 'writexml': '写出XML'})
defproperty(文档, 'documentElement', doc='Top-level element of this document.')

def _clone_node(node, deep, newOwnerDocument):
    """
    Clone a node and give it the new owner document.
    Called by Node.cloneNode and Document.importNode
    """
    if node.ownerDocument.isSameNode(newOwnerDocument):
        operation = XML工具.dom.UserDataHandler.NODE_CLONED
    else:
        operation = XML工具.dom.UserDataHandler.NODE_IMPORTED
    if node.nodeType == 节点.ELEMENT_NODE:
        clone = newOwnerDocument.createElementNS(node.namespaceURI, node.nodeName)
        for attr in node.attributes.values():
            clone.setAttributeNS(attr.namespaceURI, attr.nodeName, attr.value)
            a = clone.getAttributeNodeNS(attr.namespaceURI, attr.localName)
            a.specified = attr.specified
        if deep:
            for child in node.childNodes:
                c = _clone_node(child, deep, newOwnerDocument)
                clone.appendChild(c)
    elif node.nodeType == 节点.DOCUMENT_FRAGMENT_NODE:
        clone = newOwnerDocument.createDocumentFragment()
        if deep:
            for child in node.childNodes:
                c = _clone_node(child, deep, newOwnerDocument)
                clone.appendChild(c)
    elif node.nodeType == 节点.TEXT_NODE:
        clone = newOwnerDocument.createTextNode(node.data)
    elif node.nodeType == 节点.CDATA_SECTION_NODE:
        clone = newOwnerDocument.createCDATASection(node.data)
    elif node.nodeType == 节点.PROCESSING_INSTRUCTION_NODE:
        clone = newOwnerDocument.createProcessingInstruction(node.target, node.data)
    elif node.nodeType == 节点.COMMENT_NODE:
        clone = newOwnerDocument.createComment(node.data)
    elif node.nodeType == 节点.ATTRIBUTE_NODE:
        clone = newOwnerDocument.createAttributeNS(node.namespaceURI, node.nodeName)
        clone.specified = True
        clone.value = node.value
    elif node.nodeType == 节点.DOCUMENT_TYPE_NODE:
        assert node.ownerDocument is not newOwnerDocument
        operation = XML工具.dom.UserDataHandler.NODE_IMPORTED
        clone = newOwnerDocument.implementation.createDocumentType(node.name, node.publicId, node.systemId)
        clone.ownerDocument = newOwnerDocument
        if deep:
            clone.entities._seq = []
            clone.notations._seq = []
            for n in node.notations._seq:
                notation = 记法(n.nodeName, n.publicId, n.systemId)
                notation.ownerDocument = newOwnerDocument
                clone.notations._seq.append(notation)
                if hasattr(n, '_call_user_data_handler'):
                    n._call_user_data_handler(operation, n, notation)
            for e in node.entities._seq:
                entity = 实体(e.nodeName, e.publicId, e.systemId, e.notationName)
                entity.actualEncoding = e.actualEncoding
                entity.encoding = e.encoding
                entity.version = e.version
                entity.ownerDocument = newOwnerDocument
                clone.entities._seq.append(entity)
                if hasattr(e, '_call_user_data_handler'):
                    e._call_user_data_handler(operation, e, entity)
    else:
        raise XML工具.dom.NotSupportedErr('Cannot clone node %s' % repr(node))
    if hasattr(node, '_call_user_data_handler'):
        node._call_user_data_handler(operation, node, clone)
    return clone

def _nssplit(qualifiedName):
    fields = qualifiedName.split(':', 1)
    if len(fields) == 2:
        return fields
    else:
        return (None, fields[0])

def _do_pulldom_parse(func, args, kwargs):
    events = func(*args, **kwargs)
    toktype, rootNode = events.getEvent()
    events.expandNode(rootNode)
    events.clear()
    return rootNode

def 解析(file, parser=None, bufsize=None):
    """Parse a file into a DOM by filename or file object."""
    if parser is None and (not bufsize):
        from XML工具.dom import expatbuilder
        return expatbuilder.parse(file)
    else:
        from XML工具.dom import pulldom
        return _do_pulldom_parse(pulldom.parse, (file,), {'parser': parser, 'bufsize': bufsize})

def 解析字符串(string, parser=None):
    """Parse a file into a DOM from a string."""
    if parser is None:
        from XML工具.dom import expatbuilder
        return expatbuilder.parseString(string)
    else:
        from XML工具.dom import pulldom
        return _do_pulldom_parse(pulldom.parseString, (string,), {'parser': parser})

def 取DOM实现(features=None):
    if features:
        if isinstance(features, str):
            features = domreg._parse_feature_string(features)
        for f, v in features:
            if not 文档.实现.hasFeature(f, v):
                return None
    return 文档.实现


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Attr': '属性节点',
    'AttributeList': '属性节点表',
    'CDATASection': 'CDATA节',
    'CharacterData': '字符数据',
    'Childless': '无子类',
    'Comment': '注释',
    'DOMImplementation': 'DOM实现',
    'Document': '文档',
    'DocumentFragment': '文档片段',
    'DocumentType': '文档类型',
    'Element': '元素',
    'ElementInfo': '元素信息',
    'Entity': '实体',
    'Identified': '已标识',
    'NamedNodeMap': '命名节点表',
    'Node': '节点',
    'Notation': '记法',
    'ProcessingInstruction': '处理指令',
    'ReadOnlySequentialNamedNodeMap': '只读顺序节点表',
    'Text': '文本',
    'TypeInfo': '类型信息',
    'getDOMImplementation': '取DOM实现',
    'parse': '解析',
    'parseString': '解析字符串',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'CDATA节': {
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'writexml': '写出XML',
    },
    'DOM实现': {
        'createDocument': '建文档',
        'createDocumentType': '建文档类型',
        'getInterface': '取接口',
        'hasFeature': '有特性吗',
    },
    '元素': {
        'getAttribute': '取属性',
        'getAttributeNS': '取属性NS',
        'getAttributeNode': '取属性节点',
        'getAttributeNodeNS': '取属性节点NS',
        'getElementsByTagName': '按标签名取元素',
        'getElementsByTagNameNS': '按标签名取元素NS',
        'hasAttribute': '有该属性吗',
        'hasAttributeNS': '有该属性吗NS',
        'hasAttributes': '有属性吗',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'removeAttribute': '删属性',
        'removeAttributeNS': '删属性NS',
        'removeAttributeNode': '删属性节点',
        'schemaType': '模式类型',
        'setAttribute': '设属性',
        'setAttributeNS': '设属性NS',
        'setAttributeNode': '设属性节点',
        'setAttributeNodeNS': '设属性节点NS',
        'setIdAttribute': '设ID属性',
        'setIdAttributeNS': '设ID属性NS',
        'setIdAttributeNode': '设ID属性节点',
        'unlink': '解链',
        'writexml': '写出XML',
    },
    '元素信息': {
        'getAttributeType': '取属性类型',
        'getAttributeTypeNS': '取属性类型NS',
        'isElementContent': '是元素内容吗',
        'isEmpty': '是空吗',
        'isId': '是ID吗',
        'isIdNS': '是ID吗NS',
    },
    '只读顺序节点表': {
        'getNamedItem': '取命名项',
        'getNamedItemNS': '取命名项NS',
        'item': '取项',
        'removeNamedItem': '删命名项',
        'removeNamedItemNS': '删命名项NS',
        'setNamedItem': '设命名项',
        'setNamedItemNS': '设命名项NS',
    },
    '命名节点表': {
        'getNamedItem': '取命名项',
        'getNamedItemNS': '取命名项NS',
        'item': '取项',
        'itemsNS': '取项NS',
        'keysNS': '取键NS',
        'removeNamedItem': '删命名项',
        'removeNamedItemNS': '删命名项NS',
        'setNamedItem': '设命名项',
        'setNamedItemNS': '设命名项NS',
    },
    '处理指令': {
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'writexml': '写出XML',
    },
    '字符数据': {
        'appendData': '追加数据',
        'data': '数据',
        'deleteData': '删除数据',
        'insertData': '插入数据',
        'nodeValue': '节点值',
        'replaceData': '替换数据',
        'substringData': '取子串数据',
    },
    '实体': {
        'actualEncoding': '实际编码',
        'appendChild': '追加子节点',
        'attributes': '属性表',
        'encoding': '编码',
        'insertBefore': '插到前面',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'removeChild': '删子节点',
        'replaceChild': '替换子节点',
        'version': '版本',
    },
    '属性节点': {
        'attributes': '属性表',
        'name': '名字',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'prefix': '前缀',
        'specified': '已指定',
        'unlink': '解链',
        'value': '值',
    },
    '文本': {
        'attributes': '属性表',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'replaceWholeText': '替换整段文本',
        'splitText': '切分文本',
        'writexml': '写出XML',
    },
    '文档': {
        'actualEncoding': '实际编码',
        'appendChild': '追加子节点',
        'attributes': '属性表',
        'cloneNode': '克隆节点',
        'createAttribute': '建属性',
        'createAttributeNS': '建属性NS',
        'createCDATASection': '建CDATA节',
        'createComment': '建注释',
        'createDocumentFragment': '建文档片段',
        'createElement': '建元素',
        'createElementNS': '建元素NS',
        'createProcessingInstruction': '建处理指令',
        'createTextNode': '建文本节点',
        'encoding': '编码',
        'getElementById': '按ID取元素',
        'getElementsByTagName': '按标签名取元素',
        'getElementsByTagNameNS': '按标签名取元素NS',
        'implementation': '实现',
        'importNode': '导入节点',
        'isSupported': '支持吗',
        'nextSibling': '后兄弟',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'parentNode': '父节点',
        'previousSibling': '前兄弟',
        'removeChild': '删子节点',
        'renameNode': '重命名节点',
        'unlink': '解链',
        'version': '版本',
        'writexml': '写出XML',
    },
    '文档片段': {
        'attributes': '属性表',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'parentNode': '父节点',
    },
    '文档类型': {
        'cloneNode': '克隆节点',
        'internalSubset': '内部子集',
        'name': '名字',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'publicId': '公共标识',
        'systemId': '系统标识',
        'writexml': '写出XML',
    },
    '无子类': {
        'appendChild': '追加子节点',
        'attributes': '属性表',
        'childNodes': '子节点表',
        'firstChild': '首个子节点',
        'hasChildNodes': '有子节点吗',
        'insertBefore': '插到前面',
        'lastChild': '末个子节点',
        'normalize': '规范化',
        'removeChild': '删子节点',
        'replaceChild': '替换子节点',
    },
    '注释': {
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'writexml': '写出XML',
    },
    '节点': {
        'appendChild': '追加子节点',
        'cloneNode': '克隆节点',
        'getInterface': '取接口',
        'getUserData': '取用户数据',
        'hasChildNodes': '有子节点吗',
        'insertBefore': '插到前面',
        'isSameNode': '同节点吗',
        'isSupported': '支持吗',
        'namespaceURI': '命名空间URI',
        'nextSibling': '后兄弟',
        'normalize': '规范化',
        'ownerDocument': '所有者文档',
        'parentNode': '父节点',
        'prefix': '前缀',
        'previousSibling': '前兄弟',
        'removeChild': '删子节点',
        'replaceChild': '替换子节点',
        'setUserData': '设用户数据',
        'toprettyxml': '转美化XML',
        'toxml': '转XML',
        'unlink': '解链',
    },
    '记法': {
        'nodeType': '节点类型',
        'nodeValue': '节点值',
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
    'CDATA节': {
        'data': '数据',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'writexml': '写出XML',
    },
    'DOM实现': {
        'createDocument': '建文档',
        'createDocumentType': '建文档类型',
        'getInterface': '取接口',
        'hasFeature': '有特性吗',
    },
    '元素': {
        'childNodes': '子节点表',
        'getAttribute': '取属性',
        'getAttributeNS': '取属性NS',
        'getAttributeNode': '取属性节点',
        'getAttributeNodeNS': '取属性节点NS',
        'getElementsByTagName': '按标签名取元素',
        'getElementsByTagNameNS': '按标签名取元素NS',
        'hasAttribute': '有该属性吗',
        'hasAttributeNS': '有该属性吗NS',
        'hasAttributes': '有属性吗',
        'isSameNode': '同节点吗',
        'namespaceURI': '命名空间URI',
        'nextSibling': '后兄弟',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'ownerDocument': '所有者文档',
        'parentNode': '父节点',
        'prefix': '前缀',
        'previousSibling': '前兄弟',
        'removeAttribute': '删属性',
        'removeAttributeNS': '删属性NS',
        'removeAttributeNode': '删属性节点',
        'schemaType': '模式类型',
        'setAttribute': '设属性',
        'setAttributeNS': '设属性NS',
        'setAttributeNode': '设属性节点',
        'setAttributeNodeNS': '设属性节点NS',
        'setIdAttribute': '设ID属性',
        'setIdAttributeNS': '设ID属性NS',
        'setIdAttributeNode': '设ID属性节点',
        'tagName': '标签名',
        'unlink': '解链',
        'writexml': '写出XML',
    },
    '元素信息': {
        'getAttributeType': '取属性类型',
        'getAttributeTypeNS': '取属性类型NS',
        'isElementContent': '是元素内容吗',
        'isEmpty': '是空吗',
        'isId': '是ID吗',
        'isIdNS': '是ID吗NS',
        'tagName': '标签名',
    },
    '只读顺序节点表': {
        'getNamedItem': '取命名项',
        'getNamedItemNS': '取命名项NS',
        'item': '取项',
        'removeNamedItem': '删命名项',
        'removeNamedItemNS': '删命名项NS',
        'setNamedItem': '设命名项',
        'setNamedItemNS': '设命名项NS',
    },
    '命名节点表': {
        'getNamedItem': '取命名项',
        'getNamedItemNS': '取命名项NS',
        'item': '取项',
        'itemsNS': '取项NS',
        'keysNS': '取键NS',
        'removeNamedItem': '删命名项',
        'removeNamedItemNS': '删命名项NS',
        'setNamedItem': '设命名项',
        'setNamedItemNS': '设命名项NS',
    },
    '处理指令': {
        'data': '数据',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'writexml': '写出XML',
    },
    '字符数据': {
        'appendData': '追加数据',
        'data': '数据',
        'deleteData': '删除数据',
        'insertData': '插入数据',
        'nextSibling': '后兄弟',
        'nodeValue': '节点值',
        'ownerDocument': '所有者文档',
        'parentNode': '父节点',
        'previousSibling': '前兄弟',
        'replaceData': '替换数据',
        'substringData': '取子串数据',
    },
    '实体': {
        'actualEncoding': '实际编码',
        'appendChild': '追加子节点',
        'attributes': '属性表',
        'childNodes': '子节点表',
        'encoding': '编码',
        'insertBefore': '插到前面',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'removeChild': '删子节点',
        'replaceChild': '替换子节点',
        'version': '版本',
    },
    '属性节点': {
        'attributes': '属性表',
        'childNodes': '子节点表',
        'localName': '本地名',
        'name': '名字',
        'namespaceURI': '命名空间URI',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'ownerDocument': '所有者文档',
        'ownerElement': '所有者元素',
        'prefix': '前缀',
        'specified': '已指定',
        'unlink': '解链',
        'value': '值',
    },
    '已标识': {
        'publicId': '公共标识',
        'systemId': '系统标识',
    },
    '文本': {
        'attributes': '属性表',
        'data': '数据',
        'nextSibling': '后兄弟',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'ownerDocument': '所有者文档',
        'parentNode': '父节点',
        'previousSibling': '前兄弟',
        'replaceWholeText': '替换整段文本',
        'splitText': '切分文本',
        'writexml': '写出XML',
    },
    '文档': {
        'actualEncoding': '实际编码',
        'appendChild': '追加子节点',
        'attributes': '属性表',
        'childNodes': '子节点表',
        'cloneNode': '克隆节点',
        'createAttribute': '建属性',
        'createAttributeNS': '建属性NS',
        'createCDATASection': '建CDATA节',
        'createComment': '建注释',
        'createDocumentFragment': '建文档片段',
        'createElement': '建元素',
        'createElementNS': '建元素NS',
        'createProcessingInstruction': '建处理指令',
        'createTextNode': '建文本节点',
        'documentElement': '文档元素',
        'encoding': '编码',
        'getElementById': '按ID取元素',
        'getElementsByTagName': '按标签名取元素',
        'getElementsByTagNameNS': '按标签名取元素NS',
        'implementation': '实现',
        'importNode': '导入节点',
        'isSupported': '支持吗',
        'nextSibling': '后兄弟',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'parentNode': '父节点',
        'previousSibling': '前兄弟',
        'removeChild': '删子节点',
        'renameNode': '重命名节点',
        'unlink': '解链',
        'version': '版本',
        'writexml': '写出XML',
    },
    '文档片段': {
        'attributes': '属性表',
        'childNodes': '子节点表',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'parentNode': '父节点',
    },
    '文档类型': {
        'cloneNode': '克隆节点',
        'internalSubset': '内部子集',
        'name': '名字',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
        'ownerDocument': '所有者文档',
        'publicId': '公共标识',
        'systemId': '系统标识',
        'writexml': '写出XML',
    },
    '无子类': {
        'appendChild': '追加子节点',
        'attributes': '属性表',
        'childNodes': '子节点表',
        'firstChild': '首个子节点',
        'hasChildNodes': '有子节点吗',
        'insertBefore': '插到前面',
        'lastChild': '末个子节点',
        'nodeName': '节点名',
        'normalize': '规范化',
        'removeChild': '删子节点',
        'replaceChild': '替换子节点',
    },
    '注释': {
        'data': '数据',
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'writexml': '写出XML',
    },
    '类型信息': {
        'name': '名字',
    },
    '节点': {
        'appendChild': '追加子节点',
        'childNodes': '子节点表',
        'cloneNode': '克隆节点',
        'getInterface': '取接口',
        'getUserData': '取用户数据',
        'hasChildNodes': '有子节点吗',
        'insertBefore': '插到前面',
        'isSameNode': '同节点吗',
        'isSupported': '支持吗',
        'namespaceURI': '命名空间URI',
        'nextSibling': '后兄弟',
        'nodeType': '节点类型',
        'normalize': '规范化',
        'ownerDocument': '所有者文档',
        'parentNode': '父节点',
        'prefix': '前缀',
        'previousSibling': '前兄弟',
        'removeChild': '删子节点',
        'replaceChild': '替换子节点',
        'setUserData': '设用户数据',
        'toprettyxml': '转美化XML',
        'toxml': '转XML',
        'unlink': '解链',
        'writexml': '写出XML',
    },
    '记法': {
        'nodeName': '节点名',
        'nodeType': '节点类型',
        'nodeValue': '节点值',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
