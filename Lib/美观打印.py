# -*- coding: utf-8 -*-
"""美观打印 —— 汉语库（由 tools/汉化库.py 从 Lib/pprint.py 机械生成，**不要手改**）。

英文库 Lib/pprint.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 美观打印
"""


"""Support to pretty-print lists, tuples, & dictionaries recursively.

Very simple, but useful, especially in debugging data structures.

Classes
-------

PrettyPrinter()
    Handle pretty-printing operations onto a stream using a configured
    set of formatting parameters.

Functions
---------

pformat()
    Format a Python object into a pretty-printed representation.

pprint()
    Pretty-print a Python object to a stream [default is sys.stdout].

saferepr()
    Generate a 'standard' repr()-like value, but protect against recursive
    data structures.

"""
_英文原名表 = {'PrettyPrinter': '美观打印器', 'isreadable': '可读吗', 'isrecursive': '递归吗', 'pformat': '格式化', 'pp': '便捷打印', 'pprint': '美观打印', 'saferepr': '安全表示'}

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
import collections as _collections
import sys as _sys
import types as _types
from io import StringIO as _StringIO
__all__ = ['pprint', 'pformat', 'isreadable', 'isrecursive', 'saferepr', 'PrettyPrinter', 'pp']

def 美观打印(object, stream=None, indent=1, width=80, depth=None, *, compact=False, sort_dicts=True, underscore_numbers=False):
    """Pretty-print a Python object to a stream [default is sys.stdout]."""
    printer = 美观打印器(stream=stream, indent=indent, width=width, depth=depth, compact=compact, sort_dicts=sort_dicts, underscore_numbers=underscore_numbers)
    printer.pprint(object)

def 格式化(object, indent=1, width=80, depth=None, *, compact=False, sort_dicts=True, underscore_numbers=False):
    """Format a Python object into a pretty-printed representation."""
    return 美观打印器(indent=indent, width=width, depth=depth, compact=compact, sort_dicts=sort_dicts, underscore_numbers=underscore_numbers).pformat(object)

def 便捷打印(object, *args, sort_dicts=False, **kwargs):
    """Pretty-print a Python object"""
    美观打印(object, *args, sort_dicts=sort_dicts, **kwargs)

def 安全表示(object):
    """Version of repr() which can handle recursive data structures."""
    return 美观打印器()._safe_repr(object, {}, None, 0)[0]

def 可读吗(object):
    """Determine if saferepr(object) is readable by eval()."""
    return 美观打印器()._safe_repr(object, {}, None, 0)[1]

def 递归吗(object):
    """Determine if object requires a recursive representation."""
    return 美观打印器()._safe_repr(object, {}, None, 0)[2]

class _safe_key:
    """Helper function for key functions when sorting unorderable objects.

    The wrapped-object will fallback to a Py2.x style comparison for
    unorderable types (sorting first comparing the type name and then by
    the obj ids).  Does not work recursively, so dict.items() must have
    _safe_key applied to both the key and the value.

    """
    __slots__ = ['obj']

    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        try:
            return self.obj < other.obj
        except TypeError:
            return (str(type(self.obj)), id(self.obj)) < (str(type(other.obj)), id(other.obj))

def _safe_tuple(t):
    """Helper function for comparing 2-tuples"""
    return (_safe_key(t[0]), _safe_key(t[1]))

class 美观打印器:

    def __init__(self, indent=1, width=80, depth=None, stream=None, *, compact=False, sort_dicts=True, underscore_numbers=False):
        """Handle pretty printing operations onto a stream using a set of
        configured parameters.

        indent
            Number of spaces to indent for each level of nesting.

        width
            Attempted maximum number of columns in the output.

        depth
            The maximum depth to print out nested structures.

        stream
            The desired output stream.  If omitted (or false), the standard
            output stream available at construction will be used.

        compact
            If true, several items will be combined in one line.

        sort_dicts
            If true, dict keys are sorted.

        underscore_numbers
            If true, digit groups are separated with underscores.

        """
        indent = int(indent)
        width = int(width)
        if indent < 0:
            raise ValueError('indent must be >= 0')
        if depth is not None and depth <= 0:
            raise ValueError('depth must be > 0')
        if not width:
            raise ValueError('width must be != 0')
        self._depth = depth
        self._indent_per_level = indent
        self._width = width
        if stream is not None:
            self._stream = stream
        else:
            self._stream = _sys.stdout
        self._compact = bool(compact)
        self._sort_dicts = sort_dicts
        self._underscore_numbers = underscore_numbers

    def 美观打印(self, object):
        if self._stream is not None:
            self._format(object, self._stream, 0, 0, {}, 0)
            self._stream.write('\n')

    def 格式化(self, object):
        sio = _StringIO()
        self._format(object, sio, 0, 0, {}, 0)
        return sio.getvalue()

    def 递归吗(self, object):
        return self.format(object, {}, 0, 0)[2]

    def 可读吗(self, object):
        s, readable, recursive = self.format(object, {}, 0, 0)
        return readable and (not recursive)

    def _format(self, object, stream, indent, allowance, context, level):
        objid = id(object)
        if objid in context:
            stream.write(_recursion(object))
            self._recursive = True
            self._readable = False
            return
        rep = self._repr(object, context, level)
        max_width = self._width - indent - allowance
        if len(rep) > max_width:
            p = self._dispatch.get(type(object).__repr__, None)
            from dataclasses import is_dataclass
            if p is not None:
                context[objid] = 1
                p(self, object, stream, indent, allowance, context, level + 1)
                del context[objid]
                return
            elif is_dataclass(object) and (not isinstance(object, type)) and object.__dataclass_params__.repr and hasattr(object.__repr__, '__wrapped__') and ('__create_fn__' in object.__repr__.__wrapped__.__qualname__):
                context[objid] = 1
                self._pprint_dataclass(object, stream, indent, allowance, context, level + 1)
                del context[objid]
                return
        stream.write(rep)

    def _pprint_dataclass(self, object, stream, indent, allowance, context, level):
        from dataclasses import fields as dataclass_fields
        cls_name = object.__class__.__name__
        indent += len(cls_name) + 1
        items = [(f.name, getattr(object, f.name)) for f in dataclass_fields(object) if f.repr]
        stream.write(cls_name + '(')
        self._format_namespace_items(items, stream, indent, allowance, context, level)
        stream.write(')')
    _dispatch = {}

    def _pprint_dict(self, object, stream, indent, allowance, context, level):
        write = stream.write
        write('{')
        if self._indent_per_level > 1:
            write((self._indent_per_level - 1) * ' ')
        length = len(object)
        if length:
            if self._sort_dicts:
                items = sorted(object.items(), key=_safe_tuple)
            else:
                items = object.items()
            self._format_dict_items(items, stream, indent, allowance + 1, context, level)
        write('}')
    _dispatch[dict.__repr__] = _pprint_dict

    def _pprint_ordered_dict(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return
        cls = object.__class__
        stream.write(cls.__name__ + '(')
        self._format(list(object.items()), stream, indent + len(cls.__name__) + 1, allowance + 1, context, level)
        stream.write(')')
    _dispatch[_collections.OrderedDict.__repr__] = _pprint_ordered_dict

    def _pprint_list(self, object, stream, indent, allowance, context, level):
        stream.write('[')
        self._format_items(object, stream, indent, allowance + 1, context, level)
        stream.write(']')
    _dispatch[list.__repr__] = _pprint_list

    def _pprint_tuple(self, object, stream, indent, allowance, context, level):
        stream.write('(')
        endchar = ',)' if len(object) == 1 else ')'
        self._format_items(object, stream, indent, allowance + len(endchar), context, level)
        stream.write(endchar)
    _dispatch[tuple.__repr__] = _pprint_tuple

    def _pprint_set(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return
        typ = object.__class__
        if typ is set:
            stream.write('{')
            endchar = '}'
        else:
            stream.write(typ.__name__ + '({')
            endchar = '})'
            indent += len(typ.__name__) + 1
        object = sorted(object, key=_safe_key)
        self._format_items(object, stream, indent, allowance + len(endchar), context, level)
        stream.write(endchar)
    _dispatch[set.__repr__] = _pprint_set
    _dispatch[frozenset.__repr__] = _pprint_set

    def _pprint_str(self, object, stream, indent, allowance, context, level):
        write = stream.write
        if not len(object):
            write(repr(object))
            return
        chunks = []
        lines = object.splitlines(True)
        if level == 1:
            indent += 1
            allowance += 1
        max_width1 = max_width = self._width - indent
        for i, line in enumerate(lines):
            rep = repr(line)
            if i == len(lines) - 1:
                max_width1 -= allowance
            if len(rep) <= max_width1:
                chunks.append(rep)
            else:
                import re
                parts = re.findall('\\S*\\s*', line)
                assert parts
                assert not parts[-1]
                parts.pop()
                max_width2 = max_width
                current = ''
                for j, part in enumerate(parts):
                    candidate = current + part
                    if j == len(parts) - 1 and i == len(lines) - 1:
                        max_width2 -= allowance
                    if len(repr(candidate)) > max_width2:
                        if current:
                            chunks.append(repr(current))
                        current = part
                    else:
                        current = candidate
                if current:
                    chunks.append(repr(current))
        if len(chunks) == 1:
            write(rep)
            return
        if level == 1:
            write('(')
        for i, rep in enumerate(chunks):
            if i > 0:
                write('\n' + ' ' * indent)
            write(rep)
        if level == 1:
            write(')')
    _dispatch[str.__repr__] = _pprint_str

    def _pprint_bytes(self, object, stream, indent, allowance, context, level):
        write = stream.write
        if len(object) <= 4:
            write(repr(object))
            return
        parens = level == 1
        if parens:
            indent += 1
            allowance += 1
            write('(')
        delim = ''
        for rep in _wrap_bytes_repr(object, self._width - indent, allowance):
            write(delim)
            write(rep)
            if not delim:
                delim = '\n' + ' ' * indent
        if parens:
            write(')')
    _dispatch[bytes.__repr__] = _pprint_bytes

    def _pprint_bytearray(self, object, stream, indent, allowance, context, level):
        write = stream.write
        write('bytearray(')
        self._pprint_bytes(bytes(object), stream, indent + 10, allowance + 1, context, level + 1)
        write(')')
    _dispatch[bytearray.__repr__] = _pprint_bytearray

    def _pprint_mappingproxy(self, object, stream, indent, allowance, context, level):
        stream.write('mappingproxy(')
        self._format(object.copy(), stream, indent + 13, allowance + 1, context, level)
        stream.write(')')
    _dispatch[_types.MappingProxyType.__repr__] = _pprint_mappingproxy

    def _pprint_simplenamespace(self, object, stream, indent, allowance, context, level):
        if type(object) is _types.SimpleNamespace:
            cls_name = 'namespace'
        else:
            cls_name = object.__class__.__name__
        indent += len(cls_name) + 1
        items = object.__dict__.items()
        stream.write(cls_name + '(')
        self._format_namespace_items(items, stream, indent, allowance, context, level)
        stream.write(')')
    _dispatch[_types.SimpleNamespace.__repr__] = _pprint_simplenamespace

    def _format_dict_items(self, items, stream, indent, allowance, context, level):
        write = stream.write
        indent += self._indent_per_level
        delimnl = ',\n' + ' ' * indent
        last_index = len(items) - 1
        for i, (key, ent) in enumerate(items):
            last = i == last_index
            rep = self._repr(key, context, level)
            write(rep)
            write(': ')
            self._format(ent, stream, indent + len(rep) + 2, allowance if last else 1, context, level)
            if not last:
                write(delimnl)

    def _format_namespace_items(self, items, stream, indent, allowance, context, level):
        write = stream.write
        delimnl = ',\n' + ' ' * indent
        last_index = len(items) - 1
        for i, (key, ent) in enumerate(items):
            last = i == last_index
            write(key)
            write('=')
            if id(ent) in context:
                write('...')
            else:
                self._format(ent, stream, indent + len(key) + 1, allowance if last else 1, context, level)
            if not last:
                write(delimnl)

    def _format_items(self, items, stream, indent, allowance, context, level):
        write = stream.write
        indent += self._indent_per_level
        if self._indent_per_level > 1:
            write((self._indent_per_level - 1) * ' ')
        delimnl = ',\n' + ' ' * indent
        delim = ''
        width = max_width = self._width - indent + 1
        it = iter(items)
        try:
            next_ent = next(it)
        except StopIteration:
            return
        last = False
        while not last:
            ent = next_ent
            try:
                next_ent = next(it)
            except StopIteration:
                last = True
                max_width -= allowance
                width -= allowance
            if self._compact:
                rep = self._repr(ent, context, level)
                w = len(rep) + 2
                if width < w:
                    width = max_width
                    if delim:
                        delim = delimnl
                if width >= w:
                    width -= w
                    write(delim)
                    delim = ', '
                    write(rep)
                    continue
            write(delim)
            delim = delimnl
            self._format(ent, stream, indent, allowance if last else 1, context, level)

    def _repr(self, object, context, level):
        repr, readable, recursive = self.format(object, context.copy(), self._depth, level)
        if not readable:
            self._readable = False
        if recursive:
            self._recursive = True
        return repr

    def format(self, object, context, maxlevels, level):
        """Format object for a specific context, returning a string
        and flags indicating whether the representation is 'readable'
        and whether the object represents a recursive construct.
        """
        return self._safe_repr(object, context, maxlevels, level)

    def _pprint_default_dict(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return
        rdf = self._repr(object.default_factory, context, level)
        cls = object.__class__
        indent += len(cls.__name__) + 1
        stream.write('%s(%s,\n%s' % (cls.__name__, rdf, ' ' * indent))
        self._pprint_dict(object, stream, indent, allowance + 1, context, level)
        stream.write(')')
    _dispatch[_collections.defaultdict.__repr__] = _pprint_default_dict

    def _pprint_counter(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return
        cls = object.__class__
        stream.write(cls.__name__ + '({')
        if self._indent_per_level > 1:
            stream.write((self._indent_per_level - 1) * ' ')
        items = object.most_common()
        self._format_dict_items(items, stream, indent + len(cls.__name__) + 1, allowance + 2, context, level)
        stream.write('})')
    _dispatch[_collections.Counter.__repr__] = _pprint_counter

    def _pprint_chain_map(self, object, stream, indent, allowance, context, level):
        if not len(object.maps):
            stream.write(repr(object))
            return
        cls = object.__class__
        stream.write(cls.__name__ + '(')
        indent += len(cls.__name__) + 1
        for i, m in enumerate(object.maps):
            if i == len(object.maps) - 1:
                self._format(m, stream, indent, allowance + 1, context, level)
                stream.write(')')
            else:
                self._format(m, stream, indent, 1, context, level)
                stream.write(',\n' + ' ' * indent)
    _dispatch[_collections.ChainMap.__repr__] = _pprint_chain_map

    def _pprint_deque(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return
        cls = object.__class__
        stream.write(cls.__name__ + '(')
        indent += len(cls.__name__) + 1
        stream.write('[')
        if object.maxlen is None:
            self._format_items(object, stream, indent, allowance + 2, context, level)
            stream.write('])')
        else:
            self._format_items(object, stream, indent, 2, context, level)
            rml = self._repr(object.maxlen, context, level)
            stream.write('],\n%smaxlen=%s)' % (' ' * indent, rml))
    _dispatch[_collections.deque.__repr__] = _pprint_deque

    def _pprint_user_dict(self, object, stream, indent, allowance, context, level):
        self._format(object.data, stream, indent, allowance, context, level - 1)
    _dispatch[_collections.UserDict.__repr__] = _pprint_user_dict

    def _pprint_user_list(self, object, stream, indent, allowance, context, level):
        self._format(object.data, stream, indent, allowance, context, level - 1)
    _dispatch[_collections.UserList.__repr__] = _pprint_user_list

    def _pprint_user_string(self, object, stream, indent, allowance, context, level):
        self._format(object.data, stream, indent, allowance, context, level - 1)
    _dispatch[_collections.UserString.__repr__] = _pprint_user_string

    def _safe_repr(self, object, context, maxlevels, level):
        typ = type(object)
        if typ in _builtin_scalars:
            return (repr(object), True, False)
        r = getattr(typ, '__repr__', None)
        if issubclass(typ, int) and r is int.__repr__:
            if self._underscore_numbers:
                return (f'{object:_d}', True, False)
            else:
                return (repr(object), True, False)
        if issubclass(typ, dict) and r is dict.__repr__:
            if not object:
                return ('{}', True, False)
            objid = id(object)
            if maxlevels and level >= maxlevels:
                return ('{...}', False, objid in context)
            if objid in context:
                return (_recursion(object), False, True)
            context[objid] = 1
            readable = True
            recursive = False
            components = []
            append = components.append
            level += 1
            if self._sort_dicts:
                items = sorted(object.items(), key=_safe_tuple)
            else:
                items = object.items()
            for k, v in items:
                krepr, kreadable, krecur = self.format(k, context, maxlevels, level)
                vrepr, vreadable, vrecur = self.format(v, context, maxlevels, level)
                append('%s: %s' % (krepr, vrepr))
                readable = readable and kreadable and vreadable
                if krecur or vrecur:
                    recursive = True
            del context[objid]
            return ('{%s}' % ', '.join(components), readable, recursive)
        if issubclass(typ, list) and r is list.__repr__ or (issubclass(typ, tuple) and r is tuple.__repr__):
            if issubclass(typ, list):
                if not object:
                    return ('[]', True, False)
                format = '[%s]'
            elif len(object) == 1:
                format = '(%s,)'
            else:
                if not object:
                    return ('()', True, False)
                format = '(%s)'
            objid = id(object)
            if maxlevels and level >= maxlevels:
                return (format % '...', False, objid in context)
            if objid in context:
                return (_recursion(object), False, True)
            context[objid] = 1
            readable = True
            recursive = False
            components = []
            append = components.append
            level += 1
            for o in object:
                orepr, oreadable, orecur = self.format(o, context, maxlevels, level)
                append(orepr)
                if not oreadable:
                    readable = False
                if orecur:
                    recursive = True
            del context[objid]
            return (format % ', '.join(components), readable, recursive)
        rep = repr(object)
        return (rep, rep and (not rep.startswith('<')), False)
_装类转发(美观打印器, {'isreadable': '可读吗', 'isrecursive': '递归吗', 'pformat': '格式化', 'pprint': '美观打印'}, {'isreadable': '可读吗', 'isrecursive': '递归吗', 'pformat': '格式化', 'pprint': '美观打印'})
_builtin_scalars = frozenset({str, bytes, bytearray, float, complex, bool, type(None)})

def _recursion(object):
    return '<Recursion on %s with id=%s>' % (type(object).__name__, id(object))

def _wrap_bytes_repr(object, width, allowance):
    current = b''
    last = len(object) // 4 * 4
    for i in range(0, len(object), 4):
        part = object[i:i + 4]
        candidate = current + part
        if i == last:
            width -= allowance
        if len(repr(candidate)) > width:
            if current:
                yield repr(current)
            current = part
        else:
            current = candidate
    if current:
        yield repr(current)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'PrettyPrinter': '美观打印器',
    'isreadable': '可读吗',
    'isrecursive': '递归吗',
    'pformat': '格式化',
    'pp': '便捷打印',
    'pprint': '美观打印',
    'saferepr': '安全表示',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '美观打印器': {
        'isreadable': '可读吗',
        'isrecursive': '递归吗',
        'pformat': '格式化',
        'pprint': '美观打印',
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
    '美观打印器': {
        'isreadable': '可读吗',
        'isrecursive': '递归吗',
        'pformat': '格式化',
        'pprint': '美观打印',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '便捷打印',
    '可读吗',
    '安全表示',
    '格式化',
    '美观打印',
    '美观打印器',
    '递归吗',
])

# ---- 转发层结束 ----
