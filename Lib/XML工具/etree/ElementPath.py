# -*- coding: utf-8 -*-
"""XML工具.etree/ElementPath —— 汉语库（由 tools/汉化库.py 从 Lib/xml/etree/ElementPath.py 机械生成，**不要手改**）。

英文库 Lib/xml.etree/ElementPath.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


_英文原名表 = {'findtext': '查找文本', 'get_parent_map': '取父节点表', 'iterfind': '迭代查找', 'ops': '操作表', 'prepare_child': '准备子节点', 'prepare_descendant': '准备后代', 'prepare_parent': '准备父节点', 'prepare_predicate': '准备谓词', 'prepare_self': '准备自身', 'prepare_star': '准备星号', 'xpath_tokenizer': 'XPath分词器', 'xpath_tokenizer_re': 'XPath分词正则'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import re
XPath分词正则 = re.compile('(\'[^\']*\'|\\"[^\\"]*\\"|::|//?|\\.\\.|\\(\\)|!=|[/.*:\\[\\]\\(\\)@=])|((?:\\{[^}]+\\})?[^/\\[\\]\\(\\)@!=\\s]+)|\\s+')

def XPath分词器(pattern, namespaces=None):
    default_namespace = namespaces.get('') if namespaces else None
    parsing_attribute = False
    for token in XPath分词正则.findall(pattern):
        ttype, tag = token
        if tag and tag[0] != '{':
            if ':' in tag:
                prefix, uri = tag.split(':', 1)
                try:
                    if not namespaces:
                        raise KeyError
                    yield (ttype, '{%s}%s' % (namespaces[prefix], uri))
                except KeyError:
                    raise SyntaxError('prefix %r not found in prefix map' % prefix) from None
            elif default_namespace and (not parsing_attribute):
                yield (ttype, '{%s}%s' % (default_namespace, tag))
            else:
                yield token
            parsing_attribute = False
        else:
            yield token
            parsing_attribute = ttype == '@'

def 取父节点表(context):
    parent_map = context.parent_map
    if parent_map is None:
        context.parent_map = parent_map = {}
        for p in context.root.iter():
            for e in p:
                parent_map[e] = p
    return parent_map

def _is_wildcard_tag(tag):
    return tag[:3] == '{*}' or tag[-2:] == '}*'

def _prepare_tag(tag):
    _isinstance, _str = (isinstance, str)
    if tag == '{*}*':

        def select(context, result):
            for elem in result:
                if _isinstance(elem.tag, _str):
                    yield elem
    elif tag == '{}*':

        def select(context, result):
            for elem in result:
                el_tag = elem.tag
                if _isinstance(el_tag, _str) and el_tag[0] != '{':
                    yield elem
    elif tag[:3] == '{*}':
        suffix = tag[2:]
        no_ns = slice(-len(suffix), None)
        tag = tag[3:]

        def select(context, result):
            for elem in result:
                el_tag = elem.tag
                if el_tag == tag or (_isinstance(el_tag, _str) and el_tag[no_ns] == suffix):
                    yield elem
    elif tag[-2:] == '}*':
        ns = tag[:-1]
        ns_only = slice(None, len(ns))

        def select(context, result):
            for elem in result:
                el_tag = elem.tag
                if _isinstance(el_tag, _str) and el_tag[ns_only] == ns:
                    yield elem
    else:
        raise RuntimeError(f'internal parser error, got {tag}')
    return select

def 准备子节点(next, token):
    tag = token[1]
    if _is_wildcard_tag(tag):
        select_tag = _prepare_tag(tag)

        def select(context, result):

            def select_child(result):
                for elem in result:
                    yield from elem
            return select_tag(context, select_child(result))
    else:
        if tag[:2] == '{}':
            tag = tag[2:]

        def select(context, result):
            for elem in result:
                for e in elem:
                    if e.tag == tag:
                        yield e
    return select

def 准备星号(next, token):

    def select(context, result):
        for elem in result:
            yield from elem
    return select

def 准备自身(next, token):

    def select(context, result):
        yield from result
    return select

def 准备后代(next, token):
    try:
        token = next()
    except StopIteration:
        return
    if token[0] == '*':
        tag = '*'
    elif not token[0]:
        tag = token[1]
    else:
        raise SyntaxError('invalid descendant')
    if _is_wildcard_tag(tag):
        select_tag = _prepare_tag(tag)

        def select(context, result):

            def select_child(result):
                for elem in result:
                    for e in elem.iter():
                        if e is not elem:
                            yield e
            return select_tag(context, select_child(result))
    else:
        if tag[:2] == '{}':
            tag = tag[2:]

        def select(context, result):
            for elem in result:
                for e in elem.iter(tag):
                    if e is not elem:
                        yield e
    return select

def 准备父节点(next, token):

    def select(context, result):
        parent_map = 取父节点表(context)
        result_map = {}
        for elem in result:
            if elem in parent_map:
                parent = parent_map[elem]
                if parent not in result_map:
                    result_map[parent] = None
                    yield parent
    return select

def 准备谓词(next, token):
    signature = []
    predicate = []
    while 1:
        try:
            token = next()
        except StopIteration:
            return
        if token[0] == ']':
            break
        if token == ('', ''):
            continue
        if token[0] and token[0][:1] in '\'"':
            token = ("'", token[0][1:-1])
        signature.append(token[0] or '-')
        predicate.append(token[1])
    signature = ''.join(signature)
    if signature == '@-':
        key = predicate[1]

        def select(context, result):
            for elem in result:
                if elem.get(key) is not None:
                    yield elem
        return select
    if signature == "@-='" or signature == "@-!='":
        key = predicate[1]
        value = predicate[-1]

        def select(context, result):
            for elem in result:
                if elem.get(key) == value:
                    yield elem

        def select_negated(context, result):
            for elem in result:
                if (attr_value := elem.get(key)) is not None and attr_value != value:
                    yield elem
        return select_negated if '!=' in signature else select
    if signature == '-' and (not re.match('\\-?\\d+$', predicate[0])):
        tag = predicate[0]

        def select(context, result):
            for elem in result:
                if elem.find(tag) is not None:
                    yield elem
        return select
    if signature == ".='" or signature == ".!='" or ((signature == "-='" or signature == "-!='") and (not re.match('\\-?\\d+$', predicate[0]))):
        tag = predicate[0]
        value = predicate[-1]
        if tag:

            def select(context, result):
                for elem in result:
                    for e in elem.findall(tag):
                        if ''.join(e.itertext()) == value:
                            yield elem
                            break

            def select_negated(context, result):
                for elem in result:
                    for e in elem.iterfind(tag):
                        if ''.join(e.itertext()) != value:
                            yield elem
                            break
        else:

            def select(context, result):
                for elem in result:
                    if ''.join(elem.itertext()) == value:
                        yield elem

            def select_negated(context, result):
                for elem in result:
                    if ''.join(elem.itertext()) != value:
                        yield elem
        return select_negated if '!=' in signature else select
    if signature == '-' or signature == '-()' or signature == '-()-':
        if signature == '-':
            index = int(predicate[0]) - 1
            if index < 0:
                raise SyntaxError('XPath position >= 1 expected')
        else:
            if predicate[0] != 'last':
                raise SyntaxError('unsupported function')
            if signature == '-()-':
                try:
                    index = int(predicate[2]) - 1
                except ValueError:
                    raise SyntaxError('unsupported expression')
                if index > -2:
                    raise SyntaxError('XPath offset from last() must be negative')
            else:
                index = -1

        def select(context, result):
            parent_map = 取父节点表(context)
            cache = {}
            for elem in result:
                try:
                    parent = parent_map[elem]
                except KeyError:
                    continue
                key = (parent, elem.tag)
                if key not in cache:
                    elems = parent.findall(elem.tag)
                    try:
                        cache[key] = elems[index]
                    except IndexError:
                        cache[key] = None
                if cache[key] is elem:
                    yield elem
        return select
    raise SyntaxError('invalid predicate')
操作表 = {'': 准备子节点, '*': 准备星号, '.': 准备自身, '..': 准备父节点, '//': 准备后代, '[': 准备谓词}
_cache = {}

class _SelectorContext:
    parent_map = None

    def __init__(self, root):
        self.root = root

def 迭代查找(elem, path, namespaces=None):
    if path[-1:] == '/':
        path = path + '*'
    cache_key = (path,)
    if namespaces:
        cache_key += tuple(sorted(namespaces.items()))
    try:
        selector = _cache[cache_key]
    except KeyError:
        if len(_cache) > 100:
            _cache.clear()
        if path[:1] == '/':
            raise SyntaxError('cannot use absolute path on element')
        next = iter(XPath分词器(path, namespaces)).__next__
        try:
            token = next()
        except StopIteration:
            return
        selector = []
        while 1:
            try:
                selector.append(操作表[token[0]](next, token))
            except StopIteration:
                raise SyntaxError('invalid path') from None
            try:
                token = next()
                if token[0] == '/':
                    token = next()
            except StopIteration:
                break
        _cache[cache_key] = selector
    result = [elem]
    context = _SelectorContext(elem)
    for select in selector:
        result = select(context, result)
    return result

def find(elem, path, namespaces=None):
    return next(迭代查找(elem, path, namespaces), None)

def findall(elem, path, namespaces=None):
    return list(迭代查找(elem, path, namespaces))

def 查找文本(elem, path, default=None, namespaces=None):
    try:
        elem = next(迭代查找(elem, path, namespaces))
        if elem.text is None:
            return ''
        return elem.text
    except StopIteration:
        return default


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'findtext': '查找文本',
    'get_parent_map': '取父节点表',
    'iterfind': '迭代查找',
    'ops': '操作表',
    'prepare_child': '准备子节点',
    'prepare_descendant': '准备后代',
    'prepare_parent': '准备父节点',
    'prepare_predicate': '准备谓词',
    'prepare_self': '准备自身',
    'prepare_star': '准备星号',
    'xpath_tokenizer': 'XPath分词器',
    'xpath_tokenizer_re': 'XPath分词正则',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
