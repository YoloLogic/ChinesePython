# -*- coding: utf-8 -*-
"""容器库.__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/collections/__init__.py 机械生成，**不要手改**）。

英文库 Lib/collections.__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py collections
"""


"""This module implements specialized container datatypes providing
alternatives to Python's general purpose built-in containers, dict,
list, set, and tuple.

* namedtuple   factory function for creating tuple subclasses with named fields
* deque        list-like container with fast appends and pops on either end
* ChainMap     dict-like class for creating a single view of multiple mappings
* Counter      dict subclass for counting hashable objects
* OrderedDict  dict subclass that remembers the order entries were added
* defaultdict  dict subclass that calls a factory function to supply missing values
* UserDict     wrapper around dictionary objects for easier dict subclassing
* UserList     wrapper around list objects for easier list subclassing
* UserString   wrapper around string objects for easier string subclassing

"""
_英文原名表 = {'ChainMap': '链式映射', 'Counter': '计数器', 'UserDict': '用户字典', 'UserList': '用户列表', 'UserString': '用户字符串', 'namedtuple': '具名元组'}

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
__all__ = ['ChainMap', 'Counter', 'OrderedDict', 'UserDict', 'UserList', 'UserString', 'defaultdict', 'deque', 'namedtuple']
import _collections_abc
import sys as _sys
_sys.modules['collections.abc'] = _collections_abc
abc = _collections_abc
from itertools import chain as _chain
from itertools import repeat as _repeat
from itertools import starmap as _starmap
from keyword import iskeyword as _iskeyword
from operator import eq as _eq
from operator import itemgetter as _itemgetter
from reprlib import recursive_repr as _recursive_repr
from _weakref import proxy as _proxy
try:
    from _collections import deque
except ImportError:
    pass
else:
    _collections_abc.MutableSequence.register(deque)
try:
    from _collections import _deque_iterator
except ImportError:
    pass
try:
    from _collections import defaultdict
except ImportError:
    pass
heapq = None

class _OrderedDictKeysView(_collections_abc.KeysView):

    def __reversed__(self):
        yield from reversed(self._mapping)

class _OrderedDictItemsView(_collections_abc.ItemsView):

    def __reversed__(self):
        for key in reversed(self._mapping):
            yield (key, self._mapping[key])

class _OrderedDictValuesView(_collections_abc.ValuesView):

    def __reversed__(self):
        for key in reversed(self._mapping):
            yield self._mapping[key]

class _Link(object):
    __slots__ = ('prev', 'next', 'key', '__weakref__')

class OrderedDict(dict):
    """Dictionary that remembers insertion order"""

    def __new__(cls, /, *args, **kwds):
        """Create the ordered dict object and set up the underlying structures."""
        self = dict.__new__(cls)
        self.__hardroot = _Link()
        self.__root = root = _proxy(self.__hardroot)
        root.prev = root.next = root
        self.__map = {}
        return self

    def __init__(self, other=(), /, **kwds):
        """Initialize an ordered dictionary.  The signature is the same as
        regular dictionaries.  Keyword argument order is preserved.
        """
        self.__update(other, **kwds)

    def __setitem__(self, key, value, dict_setitem=dict.__setitem__, proxy=_proxy, Link=_Link):
        """od.__setitem__(i, y) <==> od[i]=y"""
        if key not in self:
            self.__map[key] = link = Link()
            root = self.__root
            last = root.prev
            link.prev, link.next, link.key = (last, root, key)
            last.next = link
            root.prev = proxy(link)
        dict_setitem(self, key, value)

    def __delitem__(self, key, dict_delitem=dict.__delitem__):
        """od.__delitem__(y) <==> del od[y]"""
        dict_delitem(self, key)
        link = self.__map.pop(key)
        link_prev = link.prev
        link_next = link.next
        link_prev.next = link_next
        link_next.prev = link_prev
        link.prev = None
        link.next = None

    def __iter__(self):
        """od.__iter__() <==> iter(od)"""
        root = self.__root
        curr = root.next
        while curr is not root:
            yield curr.key
            curr = curr.next

    def __reversed__(self):
        """od.__reversed__() <==> reversed(od)"""
        root = self.__root
        curr = root.prev
        while curr is not root:
            yield curr.key
            curr = curr.prev

    def clear(self):
        """od.clear() -> None.  Remove all items from od."""
        root = self.__root
        root.prev = root.next = root
        self.__map.clear()
        dict.clear(self)

    def popitem(self, last=True):
        """Remove and return a (key, value) pair from the dictionary.

        Pairs are returned in LIFO order if last is true or FIFO order if false.
        """
        if not self:
            raise KeyError('dictionary is empty')
        root = self.__root
        if last:
            link = root.prev
            link_prev = link.prev
            link_prev.next = root
            root.prev = link_prev
        else:
            link = root.next
            link_next = link.next
            root.next = link_next
            link_next.prev = root
        key = link.key
        del self.__map[key]
        value = dict.pop(self, key)
        return (key, value)

    def move_to_end(self, key, last=True):
        """Move an existing element to the end (or beginning if last is false).

        Raise KeyError if the element does not exist.
        """
        link = self.__map[key]
        link_prev = link.prev
        link_next = link.next
        soft_link = link_next.prev
        link_prev.next = link_next
        link_next.prev = link_prev
        root = self.__root
        if last:
            last = root.prev
            link.prev = last
            link.next = root
            root.prev = soft_link
            last.next = link
        else:
            first = root.next
            link.prev = root
            link.next = first
            first.prev = soft_link
            root.next = link

    def __sizeof__(self):
        sizeof = _sys.getsizeof
        n = len(self) + 1
        size = sizeof(self.__dict__)
        size += sizeof(self.__map) * 2
        size += sizeof(self.__hardroot) * n
        size += sizeof(self.__root) * n
        return size
    update = __update = _collections_abc.MutableMapping.update

    def keys(self):
        """D.keys() -> a set-like object providing a view on D's keys"""
        return _OrderedDictKeysView(self)

    def items(self):
        """D.items() -> a set-like object providing a view on D's items"""
        return _OrderedDictItemsView(self)

    def values(self):
        """D.values() -> an object providing a view on D's values"""
        return _OrderedDictValuesView(self)
    __ne__ = _collections_abc.MutableMapping.__ne__
    __marker = object()

    def pop(self, key, default=__marker):
        """od.pop(k[,d]) -> v, remove specified key and return the corresponding
        value.  If key is not found, d is returned if given, otherwise KeyError
        is raised.

        """
        marker = self.__marker
        result = dict.pop(self, key, marker)
        if result is not marker:
            link = self.__map.pop(key)
            link_prev = link.prev
            link_next = link.next
            link_prev.next = link_next
            link_next.prev = link_prev
            link.prev = None
            link.next = None
            return result
        if default is marker:
            raise KeyError(key)
        return default

    def setdefault(self, key, default=None):
        """Insert key with a value of default if key is not in the dictionary.

        Return the value for key if key is in the dictionary, else default.
        """
        if key in self:
            return self[key]
        self[key] = default
        return default

    @_recursive_repr()
    def __repr__(self):
        """od.__repr__() <==> repr(od)"""
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, dict(self.items()))

    def __reduce__(self):
        """Return state information for pickling"""
        state = self.__getstate__()
        if state:
            if isinstance(state, tuple):
                state, slots = state
            else:
                slots = {}
            state = state.copy()
            slots = slots.copy()
            for k in vars(OrderedDict()):
                state.pop(k, None)
                slots.pop(k, None)
            if slots:
                state = (state, slots)
            else:
                state = state or None
        return (self.__class__, (), state, None, iter(self.items()))

    def copy(self):
        """od.copy() -> a shallow copy of od"""
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        """Create a new ordered dictionary with keys from iterable and values set to value.
        """
        self = cls()
        for key in iterable:
            self[key] = value
        return self

    def __eq__(self, other):
        """od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.

        """
        if isinstance(other, OrderedDict):
            return dict.__eq__(self, other) and all(map(_eq, self, other))
        return dict.__eq__(self, other)

    def __ior__(self, other):
        self.update(other)
        return self

    def __or__(self, other):
        if not isinstance(other, dict):
            return NotImplemented
        new = self.__class__(self)
        new.update(other)
        return new

    def __ror__(self, other):
        if not isinstance(other, dict):
            return NotImplemented
        new = self.__class__(other)
        new.update(self)
        return new
try:
    from _collections import OrderedDict
except ImportError:
    pass
try:
    from _collections import _tuplegetter
except ImportError:
    _tuplegetter = lambda index, doc: property(_itemgetter(index), doc=doc)

def 具名元组(typename, field_names, *, rename=False, defaults=None, module=None):
    """Returns a new subclass of tuple with named fields.

    >>> Point = namedtuple('Point', ['x', 'y'])
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # indexable like a plain tuple
    33
    >>> x, y = p                        # unpack like a regular tuple
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessible by name
    33
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22)

    """
    if isinstance(field_names, str):
        field_names = field_names.replace(',', ' ').split()
    field_names = list(map(str, field_names))
    typename = _sys.intern(str(typename))
    if rename:
        seen = set()
        for index, name in enumerate(field_names):
            if not name.isidentifier() or _iskeyword(name) or name.startswith('_') or (name in seen):
                field_names[index] = f'_{index}'
            seen.add(name)
    for name in [typename] + field_names:
        if type(name) is not str:
            raise TypeError('Type names and field names must be strings')
        if not name.isidentifier():
            raise ValueError(f'Type names and field names must be valid identifiers: {name!r}')
        if _iskeyword(name):
            raise ValueError(f'Type names and field names cannot be a keyword: {name!r}')
    seen = set()
    for name in field_names:
        if name.startswith('_') and (not rename):
            raise ValueError(f'Field names cannot start with an underscore: {name!r}')
        if name in seen:
            raise ValueError(f'Encountered duplicate field name: {name!r}')
        seen.add(name)
    field_defaults = {}
    if defaults is not None:
        defaults = tuple(defaults)
        if len(defaults) > len(field_names):
            raise TypeError('Got more default values than field names')
        field_defaults = dict(reversed(list(zip(reversed(field_names), reversed(defaults)))))
    field_names = tuple(map(_sys.intern, field_names))
    num_fields = len(field_names)
    arg_list = ', '.join(field_names)
    if num_fields == 1:
        arg_list += ','
    repr_fmt = '(' + ', '.join((f'{name}=%r' for name in field_names)) + ')'
    tuple_new = tuple.__new__
    _dict, _tuple, _len, _map, _zip = (dict, tuple, len, map, zip)
    namespace = {'_tuple_new': tuple_new, '__builtins__': {}, '__name__': f'namedtuple_{typename}'}
    code = f'lambda _cls, {arg_list}: _tuple_new(_cls, ({arg_list}))'
    __new__ = eval(code, namespace)
    __new__.__name__ = '__new__'
    __new__.__doc__ = f'Create new instance of {typename}({arg_list})'
    if defaults is not None:
        __new__.__defaults__ = defaults

    @classmethod
    def _make(cls, iterable):
        result = tuple_new(cls, iterable)
        if _len(result) != num_fields:
            raise TypeError(f'Expected {num_fields} arguments, got {len(result)}')
        return result
    _make.__func__.__doc__ = f'Make a new {typename} object from a sequence or iterable'

    def _replace(self, /, **kwds):
        result = self._make(_map(kwds.pop, field_names, self))
        if kwds:
            raise TypeError(f'Got unexpected field names: {list(kwds)!r}')
        return result
    _replace.__doc__ = f'Return a new {typename} object replacing specified fields with new values'

    def __repr__(self):
        """Return a nicely formatted representation string"""
        return self.__class__.__name__ + repr_fmt % self

    def _asdict(self):
        """Return a new dict which maps field names to their values."""
        return _dict(_zip(self._fields, self))

    def __getnewargs__(self):
        """Return self as a plain tuple.  Used by copy and pickle."""
        return _tuple(self)
    for method in (__new__, _make.__func__, _replace, __repr__, _asdict, __getnewargs__):
        method.__qualname__ = f'{typename}.{method.__name__}'
    class_namespace = {'__doc__': f'{typename}({arg_list})', '__slots__': (), '_fields': field_names, '_field_defaults': field_defaults, '__new__': __new__, '_make': _make, '__replace__': _replace, '_replace': _replace, '__repr__': __repr__, '_asdict': _asdict, '__getnewargs__': __getnewargs__, '__match_args__': field_names}
    for index, name in enumerate(field_names):
        doc = _sys.intern(f'Alias for field number {index}')
        class_namespace[name] = _tuplegetter(index, doc)
    result = type(typename, (tuple,), class_namespace)
    if module is None:
        try:
            module = _sys._getframemodulename(1) or '__main__'
        except AttributeError:
            try:
                module = _sys._getframe(1).f_globals.get('__name__', '__main__')
            except (AttributeError, ValueError):
                pass
    if module is not None:
        result.__module__ = module
    return result

def _count_elements(mapping, iterable):
    """Tally elements from the iterable."""
    mapping_get = mapping.get
    for elem in iterable:
        mapping[elem] = mapping_get(elem, 0) + 1
try:
    from _collections import _count_elements
except ImportError:
    pass

class 计数器(dict):
    """Dict subclass for counting hashable items.  Sometimes called a bag
    or multiset.  Elements are stored as dictionary keys and their counts
    are stored as dictionary values.

    When constructed from a Mapping or Counter, the original object's
    values will be used as the initial counts.

    >>> c = Counter('abcdeabcdabcaba')  # count elements from a string

    >>> c.most_common(3)                # three most common elements
    [('a', 5), ('b', 4), ('c', 3)]
    >>> sorted(c)                       # list all unique elements
    ['a', 'b', 'c', 'd', 'e']
    >>> ''.join(sorted(c.elements()))   # list elements with repetitions
    'aaaaabbbbcccdde'
    >>> sum(c.values())                 # total of all counts
    15

    >>> c['a']                          # count of letter 'a'
    5
    >>> for elem in 'shazam':           # update counts from an iterable
    ...     c[elem] += 1                # by adding 1 to each element's count
    >>> c['a']                          # now there are seven 'a'
    7
    >>> del c['b']                      # remove all 'b'
    >>> c['b']                          # now there are zero 'b'
    0

    >>> d = Counter('simsalabim')       # make another counter
    >>> c.update(d)                     # add in the second counter
    >>> c['a']                          # now there are nine 'a'
    9

    >>> c.clear()                       # empty the counter
    >>> c
    Counter()

    Note:  If a count is set to zero or reduced to zero, it will remain
    in the counter until the entry is deleted or the counter is cleared:

    >>> c = Counter('aaabbc')
    >>> c['b'] -= 2                     # reduce the count of 'b' by two
    >>> c.most_common()                 # 'b' is still in, but its count is zero
    [('a', 3), ('c', 1), ('b', 0)]

    """

    def __init__(self, iterable=None, /, **kwds):
        """Create a new, empty Counter object.  And if given, count elements
        from an input iterable.  Or, initialize the count from another mapping
        of elements to their counts.

        >>> c = Counter()                           # a new, empty counter
        >>> c = Counter('gallahad')                 # a new counter from an iterable
        >>> c = Counter({'a': 4, 'b': 2})           # a new counter from a mapping
        >>> c = Counter(a=4, b=2)                   # a new counter from keyword args

        """
        super().__init__()
        self.update(iterable, **kwds)

    def __missing__(self, key):
        """The count of elements not in the Counter is zero."""
        return 0

    def 总计(self):
        """Sum of the counts"""
        return sum(self.values())

    def 最常见(self, n=None):
        """List the n most common elements and their counts from the most
        common to the least.  If n is None, then list all element counts.

        >>> Counter('abracadabra').most_common(3)
        [('a', 5), ('b', 2), ('r', 2)]

        """
        if n is None:
            return sorted(self.items(), key=_itemgetter(1), reverse=True)
        global heapq
        if heapq is None:
            import heapq
        return heapq.nlargest(n, self.items(), key=_itemgetter(1))

    def 元素(self):
        """Iterator over elements repeating each as many times as its count.

        >>> c = Counter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        Knuth's example for prime factors of 1836:  2**2 * 3**3 * 17**1

        >>> import math
        >>> prime_factors = Counter({2: 2, 3: 3, 17: 1})
        >>> math.prod(prime_factors.elements())
        1836

        Note, if an element's count has been set to zero or is a negative
        number, elements() will ignore it.

        """
        return _chain.from_iterable(_starmap(_repeat, self.items()))

    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError('Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')

    def update(self, iterable=None, /, **kwds):
        """Like dict.update() but add counts instead of replacing them.

        Source can be an iterable, a dictionary, or another Counter instance.

        >>> c = Counter('which')
        >>> c.update('witch')           # add elements from another iterable
        >>> d = Counter('watch')
        >>> c.update(d)                 # add elements from another counter
        >>> c['h']                      # four 'h' in which, witch, and watch
        4

        """
        if iterable is not None:
            if isinstance(iterable, _collections_abc.Mapping):
                if self:
                    self_get = self.get
                    for elem, count in iterable.items():
                        self[elem] = count + self_get(elem, 0)
                else:
                    super().update(iterable)
            else:
                _count_elements(self, iterable)
        if kwds:
            self.update(kwds)

    def 减去(self, iterable=None, /, **kwds):
        """Like dict.update() but subtracts counts instead of replacing them.
        Counts can be reduced below zero.  Both the inputs and outputs are
        allowed to contain zero and negative counts.

        Source can be an iterable, a dictionary, or another Counter instance.

        >>> c = Counter('which')
        >>> c.subtract('witch')             # subtract elements from another iterable
        >>> c.subtract(Counter('watch'))    # subtract elements from another counter
        >>> c['h']                          # 2 in which, minus 1 in witch, minus 1 in watch
        0
        >>> c['w']                          # 1 in which, minus 1 in witch, minus 1 in watch
        -1

        """
        if iterable is not None:
            self_get = self.get
            if isinstance(iterable, _collections_abc.Mapping):
                for elem, count in iterable.items():
                    self[elem] = self_get(elem, 0) - count
            else:
                for elem in iterable:
                    self[elem] = self_get(elem, 0) - 1
        if kwds:
            self.减去(kwds)

    def copy(self):
        """Return a shallow copy."""
        return self.__class__(self)

    def __reduce__(self):
        return (self.__class__, (dict(self),))

    def __delitem__(self, elem):
        """Like dict.__delitem__() but does not raise KeyError for missing values."""
        if elem in self:
            super().__delitem__(elem)

    def __repr__(self):
        if not self:
            return f'{self.__class__.__name__}()'
        try:
            d = dict(self.最常见())
        except TypeError:
            d = dict(self)
        return f'{self.__class__.__name__}({d!r})'

    def __eq__(self, other):
        """True if all counts agree. Missing counts are treated as zero."""
        if not isinstance(other, 计数器):
            return NotImplemented
        return all((self[e] == other[e] for c in (self, other) for e in c))

    def __ne__(self, other):
        """True if any counts disagree. Missing counts are treated as zero."""
        if not isinstance(other, 计数器):
            return NotImplemented
        return not self == other

    def __le__(self, other):
        """True if all counts in self are a subset of those in other."""
        if not isinstance(other, 计数器):
            return NotImplemented
        return all((self[e] <= other[e] for c in (self, other) for e in c))

    def __lt__(self, other):
        """True if all counts in self are a proper subset of those in other."""
        if not isinstance(other, 计数器):
            return NotImplemented
        return self <= other and self != other

    def __ge__(self, other):
        """True if all counts in self are a superset of those in other."""
        if not isinstance(other, 计数器):
            return NotImplemented
        return all((self[e] >= other[e] for c in (self, other) for e in c))

    def __gt__(self, other):
        """True if all counts in self are a proper superset of those in other."""
        if not isinstance(other, 计数器):
            return NotImplemented
        return self >= other and self != other

    def __add__(self, other):
        """Add counts from two counters.

        >>> Counter('abbb') + Counter('bcc')
        Counter({'b': 4, 'c': 2, 'a': 1})

        """
        if not isinstance(other, 计数器):
            return NotImplemented
        result = 计数器()
        for elem, count in self.items():
            newcount = count + other[elem]
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count
        return result

    def __sub__(self, other):
        """ Subtract count, but keep only results with positive counts.

        >>> Counter('abbbc') - Counter('bccd')
        Counter({'b': 2, 'a': 1})

        """
        if not isinstance(other, 计数器):
            return NotImplemented
        result = 计数器()
        for elem, count in self.items():
            newcount = count - other[elem]
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count < 0:
                result[elem] = 0 - count
        return result

    def __or__(self, other):
        """Union is the maximum of value in either of the input counters.

        >>> Counter('abbb') | Counter('bcc')
        Counter({'b': 3, 'c': 2, 'a': 1})

        """
        if not isinstance(other, 计数器):
            return NotImplemented
        result = 计数器()
        for elem, count in self.items():
            other_count = other[elem]
            newcount = other_count if count < other_count else count
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count
        return result

    def __and__(self, other):
        """ Intersection is the minimum of corresponding counts.

        >>> Counter('abbb') & Counter('bcc')
        Counter({'b': 1})

        """
        if not isinstance(other, 计数器):
            return NotImplemented
        result = 计数器()
        for elem, count in self.items():
            other_count = other[elem]
            newcount = count if count < other_count else other_count
            if newcount > 0:
                result[elem] = newcount
        return result

    def __pos__(self):
        """Adds an empty counter, effectively stripping negative and zero counts"""
        result = 计数器()
        for elem, count in self.items():
            if count > 0:
                result[elem] = count
        return result

    def __neg__(self):
        """Subtracts from an empty counter.  Strips positive and zero counts,
        and flips the sign on negative counts.

        """
        result = 计数器()
        for elem, count in self.items():
            if count < 0:
                result[elem] = 0 - count
        return result

    def _keep_positive(self):
        """Internal method to strip elements with a negative or zero count"""
        nonpositive = [elem for elem, count in self.items() if not count > 0]
        for elem in nonpositive:
            del self[elem]
        return self

    def __iadd__(self, other):
        """Inplace add from another counter, keeping only positive counts.

        >>> c = Counter('abbb')
        >>> c += Counter('bcc')
        >>> c
        Counter({'b': 4, 'c': 2, 'a': 1})

        """
        for elem, count in other.items():
            self[elem] += count
        return self._keep_positive()

    def __isub__(self, other):
        """Inplace subtract counter, but keep only results with positive counts.

        >>> c = Counter('abbbc')
        >>> c -= Counter('bccd')
        >>> c
        Counter({'b': 2, 'a': 1})

        """
        for elem, count in other.items():
            self[elem] -= count
        return self._keep_positive()

    def __ior__(self, other):
        """Inplace union is the maximum of value from either counter.

        >>> c = Counter('abbb')
        >>> c |= Counter('bcc')
        >>> c
        Counter({'b': 3, 'c': 2, 'a': 1})

        """
        for elem, other_count in other.items():
            count = self[elem]
            if other_count > count:
                self[elem] = other_count
        return self._keep_positive()

    def __iand__(self, other):
        """Inplace intersection is the minimum of corresponding counts.

        >>> c = Counter('abbb')
        >>> c &= Counter('bcc')
        >>> c
        Counter({'b': 1})

        """
        for elem, count in self.items():
            other_count = other[elem]
            if other_count < count:
                self[elem] = other_count
        return self._keep_positive()
_装类转发(计数器, {'elements': '元素', 'most_common': '最常见', 'subtract': '减去', 'total': '总计'}, {'elements': '元素', 'most_common': '最常见', 'subtract': '减去', 'total': '总计'})

class 链式映射(_collections_abc.MutableMapping):
    """ A ChainMap groups multiple dicts (or other mappings) together
    to create a single, updateable view.

    The underlying mappings are stored in a list.  That list is public and can
    be accessed or updated using the *maps* attribute.  There is no other
    state.

    Lookups search the underlying mappings successively until a key is found.
    In contrast, writes, updates, and deletions only operate on the first
    mapping.

    """

    def __init__(self, *maps):
        """Initialize a ChainMap by setting *maps* to the given mappings.
        If no mappings are provided, a single empty dictionary is used.

        """
        self.映射表 = list(maps) or [{}]

    def __missing__(self, key):
        raise KeyError(key)

    def __getitem__(self, key):
        for mapping in self.映射表:
            try:
                return mapping[key]
            except KeyError:
                pass
        return self.__missing__(key)

    def get(self, key, default=None):
        return self[key] if key in self else default

    def __len__(self):
        return len(set().union(*self.映射表))

    def __iter__(self):
        d = {}
        for mapping in map(dict.fromkeys, reversed(self.映射表)):
            d |= mapping
        return iter(d)

    def __contains__(self, key):
        for mapping in self.映射表:
            if key in mapping:
                return True
        return False

    def __bool__(self):
        return any(self.映射表)

    @_recursive_repr()
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(map(repr, self.映射表))})"

    @classmethod
    def fromkeys(cls, iterable, value=None, /):
        """Create a new ChainMap with keys from iterable and values set to value."""
        return cls(dict.fromkeys(iterable, value))

    def copy(self):
        """New ChainMap or subclass with a new copy of maps[0] and refs to maps[1:]"""
        return self.__class__(self.映射表[0].copy(), *self.映射表[1:])
    __copy__ = copy

    def 新子映射(self, m=None, **kwargs):
        """New ChainMap with a new map followed by all previous maps.
        If no map is provided, an empty dict is used.
        Keyword arguments update the map or new empty dict.
        """
        if m is None:
            m = kwargs
        elif kwargs:
            m.update(kwargs)
        return self.__class__(m, *self.映射表)

    @property
    def 各级父映射(self):
        """New ChainMap from maps[1:]."""
        return self.__class__(*self.映射表[1:])

    def __setitem__(self, key, value):
        self.映射表[0][key] = value

    def __delitem__(self, key):
        try:
            del self.映射表[0][key]
        except KeyError:
            raise KeyError(f'Key not found in the first mapping: {key!r}')

    def popitem(self):
        """Remove and return an item pair from maps[0]. Raise KeyError is maps[0] is empty."""
        try:
            return self.映射表[0].popitem()
        except KeyError:
            raise KeyError('No keys found in the first mapping.')

    def pop(self, key, *args):
        """Remove *key* from maps[0] and return its value. Raise KeyError if *key* not in maps[0]."""
        try:
            return self.映射表[0].pop(key, *args)
        except KeyError:
            raise KeyError(f'Key not found in the first mapping: {key!r}')

    def clear(self):
        """Clear maps[0], leaving maps[1:] intact."""
        self.映射表[0].clear()

    def __ior__(self, other):
        self.映射表[0].update(other)
        return self

    def __or__(self, other):
        if not isinstance(other, _collections_abc.Mapping):
            return NotImplemented
        m = self.copy()
        m.maps[0].update(other)
        return m

    def __ror__(self, other):
        if not isinstance(other, _collections_abc.Mapping):
            return NotImplemented
        m = dict(other)
        for child in reversed(self.映射表):
            m.update(child)
        return self.__class__(m)
_装类转发(链式映射, {'new_child': '新子映射', 'parents': '各级父映射'}, {'maps': '映射表', 'new_child': '新子映射', 'parents': '各级父映射'})

class 用户字典(_collections_abc.MutableMapping):

    def __init__(self, dict=None, /, **kwargs):
        self.数据 = {}
        if dict is not None:
            self.update(dict)
        if kwargs:
            self.update(kwargs)

    def __len__(self):
        return len(self.数据)

    def __getitem__(self, key):
        if key in self.数据:
            return self.数据[key]
        if hasattr(self.__class__, '__missing__'):
            return self.__class__.__missing__(self, key)
        raise KeyError(key)

    def __setitem__(self, key, item):
        self.数据[key] = item

    def __delitem__(self, key):
        del self.数据[key]

    def __iter__(self):
        return iter(self.数据)

    def __contains__(self, key):
        return key in self.数据

    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default

    def __repr__(self):
        return repr(self.数据)

    def __or__(self, other):
        if isinstance(other, 用户字典):
            return self.__class__(self.数据 | other.data)
        if isinstance(other, dict):
            return self.__class__(self.数据 | other)
        return NotImplemented

    def __ror__(self, other):
        if isinstance(other, 用户字典):
            return self.__class__(other.data | self.数据)
        if isinstance(other, dict):
            return self.__class__(other | self.数据)
        return NotImplemented

    def __ior__(self, other):
        if isinstance(other, 用户字典):
            self.数据 |= other.data
        else:
            self.数据 |= other
        return self

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        inst.__dict__['data'] = self.__dict__['data'].copy()
        return inst

    def copy(self):
        if self.__class__ is 用户字典:
            return 用户字典(self.数据.copy())
        import copy
        数据 = self.数据
        try:
            self.数据 = {}
            c = copy.copy(self)
        finally:
            self.数据 = 数据
        c.update(self)
        return c

    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d
_装类转发(用户字典, {}, {'data': '数据'})

class 用户列表(_collections_abc.MutableSequence):
    """A more or less complete user-defined wrapper around list objects."""

    def __init__(self, initlist=None):
        self.数据 = []
        if initlist is not None:
            if type(initlist) == type(self.数据):
                self.数据[:] = initlist
            elif isinstance(initlist, 用户列表):
                self.数据[:] = initlist.data[:]
            else:
                self.数据 = list(initlist)

    def __repr__(self):
        return repr(self.数据)

    def __lt__(self, other):
        return self.数据 < self.__cast(other)

    def __le__(self, other):
        return self.数据 <= self.__cast(other)

    def __eq__(self, other):
        return self.数据 == self.__cast(other)

    def __gt__(self, other):
        return self.数据 > self.__cast(other)

    def __ge__(self, other):
        return self.数据 >= self.__cast(other)

    def __cast(self, other):
        return other.data if isinstance(other, 用户列表) else other

    def __contains__(self, item):
        return item in self.数据

    def __len__(self):
        return len(self.数据)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self.数据[i])
        else:
            return self.数据[i]

    def __setitem__(self, i, item):
        self.数据[i] = item

    def __delitem__(self, i):
        del self.数据[i]

    def __add__(self, other):
        if isinstance(other, 用户列表):
            return self.__class__(self.数据 + other.data)
        elif isinstance(other, type(self.数据)):
            return self.__class__(self.数据 + other)
        return self.__class__(self.数据 + list(other))

    def __radd__(self, other):
        if isinstance(other, 用户列表):
            return self.__class__(other.data + self.数据)
        elif isinstance(other, type(self.数据)):
            return self.__class__(other + self.数据)
        return self.__class__(list(other) + self.数据)

    def __iadd__(self, other):
        if isinstance(other, 用户列表):
            self.数据 += other.data
        elif isinstance(other, type(self.数据)):
            self.数据 += other
        else:
            self.数据 += list(other)
        return self

    def __mul__(self, n):
        return self.__class__(self.数据 * n)
    __rmul__ = __mul__

    def __imul__(self, n):
        self.数据 *= n
        return self

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        inst.__dict__['data'] = self.__dict__['data'][:]
        return inst

    def append(self, item):
        self.数据.append(item)

    def insert(self, i, item):
        self.数据.insert(i, item)

    def pop(self, i=-1):
        return self.数据.pop(i)

    def remove(self, item):
        self.数据.remove(item)

    def clear(self):
        self.数据.clear()

    def copy(self):
        return self.__class__(self)

    def count(self, item):
        return self.数据.count(item)

    def index(self, item, *args):
        return self.数据.index(item, *args)

    def reverse(self):
        self.数据.reverse()

    def sort(self, /, *args, **kwds):
        self.数据.sort(*args, **kwds)

    def extend(self, other):
        if isinstance(other, 用户列表):
            self.数据.extend(other.data)
        else:
            self.数据.extend(other)
_装类转发(用户列表, {}, {'data': '数据'})

class 用户字符串(_collections_abc.Sequence):

    def __init__(self, seq):
        if isinstance(seq, str):
            self.数据 = seq
        elif isinstance(seq, 用户字符串):
            self.数据 = seq.data[:]
        else:
            self.数据 = str(seq)

    def __str__(self):
        return str(self.数据)

    def __repr__(self):
        return repr(self.数据)

    def __int__(self):
        return int(self.数据)

    def __float__(self):
        return float(self.数据)

    def __complex__(self):
        return complex(self.数据)

    def __hash__(self):
        return hash(self.数据)

    def __getnewargs__(self):
        return (self.数据[:],)

    def __eq__(self, string):
        if isinstance(string, 用户字符串):
            return self.数据 == string.data
        return self.数据 == string

    def __lt__(self, string):
        if isinstance(string, 用户字符串):
            return self.数据 < string.data
        return self.数据 < string

    def __le__(self, string):
        if isinstance(string, 用户字符串):
            return self.数据 <= string.data
        return self.数据 <= string

    def __gt__(self, string):
        if isinstance(string, 用户字符串):
            return self.数据 > string.data
        return self.数据 > string

    def __ge__(self, string):
        if isinstance(string, 用户字符串):
            return self.数据 >= string.data
        return self.数据 >= string

    def __contains__(self, char):
        if isinstance(char, 用户字符串):
            char = char.data
        return char in self.数据

    def __len__(self):
        return len(self.数据)

    def __getitem__(self, index):
        return self.__class__(self.数据[index])

    def __add__(self, other):
        if isinstance(other, 用户字符串):
            return self.__class__(self.数据 + other.data)
        elif isinstance(other, str):
            return self.__class__(self.数据 + other)
        return self.__class__(self.数据 + str(other))

    def __radd__(self, other):
        if isinstance(other, str):
            return self.__class__(other + self.数据)
        return self.__class__(str(other) + self.数据)

    def __mul__(self, n):
        return self.__class__(self.数据 * n)
    __rmul__ = __mul__

    def __mod__(self, args):
        return self.__class__(self.数据 % args)

    def __rmod__(self, template):
        return self.__class__(str(template) % self)

    def capitalize(self):
        return self.__class__(self.数据.capitalize())

    def casefold(self):
        return self.__class__(self.数据.casefold())

    def center(self, width, *args):
        return self.__class__(self.数据.center(width, *args))

    def count(self, sub, start=0, end=_sys.maxsize):
        if isinstance(sub, 用户字符串):
            sub = sub.data
        return self.数据.count(sub, start, end)

    def removeprefix(self, prefix, /):
        if isinstance(prefix, 用户字符串):
            prefix = prefix.data
        return self.__class__(self.数据.removeprefix(prefix))

    def removesuffix(self, suffix, /):
        if isinstance(suffix, 用户字符串):
            suffix = suffix.data
        return self.__class__(self.数据.removesuffix(suffix))

    def encode(self, encoding='utf-8', errors='strict'):
        encoding = 'utf-8' if encoding is None else encoding
        errors = 'strict' if errors is None else errors
        return self.数据.encode(encoding, errors)

    def endswith(self, suffix, start=0, end=_sys.maxsize):
        return self.数据.endswith(suffix, start, end)

    def expandtabs(self, tabsize=8):
        return self.__class__(self.数据.expandtabs(tabsize))

    def find(self, sub, start=0, end=_sys.maxsize):
        if isinstance(sub, 用户字符串):
            sub = sub.data
        return self.数据.find(sub, start, end)

    def format(self, /, *args, **kwds):
        return self.数据.format(*args, **kwds)

    def format_map(self, mapping):
        return self.数据.format_map(mapping)

    def index(self, sub, start=0, end=_sys.maxsize):
        if isinstance(sub, 用户字符串):
            sub = sub.data
        return self.数据.index(sub, start, end)

    def isalpha(self):
        return self.数据.isalpha()

    def isalnum(self):
        return self.数据.isalnum()

    def isascii(self):
        return self.数据.isascii()

    def isdecimal(self):
        return self.数据.isdecimal()

    def isdigit(self):
        return self.数据.isdigit()

    def isidentifier(self):
        return self.数据.isidentifier()

    def islower(self):
        return self.数据.islower()

    def isnumeric(self):
        return self.数据.isnumeric()

    def isprintable(self):
        return self.数据.isprintable()

    def isspace(self):
        return self.数据.isspace()

    def istitle(self):
        return self.数据.istitle()

    def isupper(self):
        return self.数据.isupper()

    def join(self, seq):
        return self.数据.join(seq)

    def ljust(self, width, *args):
        return self.__class__(self.数据.ljust(width, *args))

    def lower(self):
        return self.__class__(self.数据.lower())

    def lstrip(self, chars=None):
        return self.__class__(self.数据.lstrip(chars))
    maketrans = str.maketrans

    def partition(self, sep):
        return self.数据.partition(sep)

    def replace(self, old, new, maxsplit=-1):
        if isinstance(old, 用户字符串):
            old = old.data
        if isinstance(new, 用户字符串):
            new = new.data
        return self.__class__(self.数据.replace(old, new, maxsplit))

    def rfind(self, sub, start=0, end=_sys.maxsize):
        if isinstance(sub, 用户字符串):
            sub = sub.data
        return self.数据.rfind(sub, start, end)

    def rindex(self, sub, start=0, end=_sys.maxsize):
        if isinstance(sub, 用户字符串):
            sub = sub.data
        return self.数据.rindex(sub, start, end)

    def rjust(self, width, *args):
        return self.__class__(self.数据.rjust(width, *args))

    def rpartition(self, sep):
        return self.数据.rpartition(sep)

    def rstrip(self, chars=None):
        return self.__class__(self.数据.rstrip(chars))

    def split(self, sep=None, maxsplit=-1):
        return self.数据.split(sep, maxsplit)

    def rsplit(self, sep=None, maxsplit=-1):
        return self.数据.rsplit(sep, maxsplit)

    def splitlines(self, keepends=False):
        return self.数据.splitlines(keepends)

    def startswith(self, prefix, start=0, end=_sys.maxsize):
        return self.数据.startswith(prefix, start, end)

    def strip(self, chars=None):
        return self.__class__(self.数据.strip(chars))

    def swapcase(self):
        return self.__class__(self.数据.swapcase())

    def title(self):
        return self.__class__(self.数据.title())

    def translate(self, *args):
        return self.__class__(self.数据.translate(*args))

    def upper(self):
        return self.__class__(self.数据.upper())

    def zfill(self, width):
        return self.__class__(self.数据.zfill(width))
_装类转发(用户字符串, {}, {'data': '数据'})


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import collections as _英文库
有序字典 = _英文库.OrderedDict
默认字典 = _英文库.defaultdict
双端队列 = _英文库.deque
_模块别名 = {
    'ChainMap': '链式映射',
    'Counter': '计数器',
    'UserDict': '用户字典',
    'UserList': '用户列表',
    'UserString': '用户字符串',
    'namedtuple': '具名元组',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '计数器': {
        'elements': '元素',
        'most_common': '最常见',
        'subtract': '减去',
        'total': '总计',
    },
    '链式映射': {
        'new_child': '新子映射',
        'parents': '各级父映射',
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
    '用户列表': {
        'data': '数据',
    },
    '用户字典': {
        'data': '数据',
    },
    '用户字符串': {
        'data': '数据',
    },
    '计数器': {
        'elements': '元素',
        'most_common': '最常见',
        'subtract': '减去',
        'total': '总计',
    },
    '链式映射': {
        'maps': '映射表',
        'new_child': '新子映射',
        'parents': '各级父映射',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '具名元组',
    '用户列表',
    '用户字典',
    '用户字符串',
    '计数器',
    '链式映射',
]

# ---- 转发层结束 ----
