# -*- coding: utf-8 -*-
"""枚举 —— 汉语库（由 tools/汉化库.py 从 Lib/enum.py 机械生成，**不要手改**）。

英文库 Lib/enum.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 枚举
"""


_英文原名表 = {'CONFORM': '符合', 'CONTINUOUS': '连续', 'EJECT': '弹出', 'Enum': '枚举', 'EnumCheck': '枚举检查', 'EnumDict': '枚举字典', 'EnumMeta': '枚举元类', 'EnumType': '枚举类型', 'FlagBoundary': '标志边界', 'IntEnum': '整数枚举', 'IntFlag': '整数标志', 'KEEP': '保留', 'NAMED_FLAGS': '具名标志', 'ReprEnum': '表示枚举', 'STRICT': '严格', 'StrEnum': '字符串枚举', 'UNIQUE': '唯一', 'auto': '自动', 'global_enum': '全局枚举', 'global_enum_repr': '全局枚举表示', 'global_flag_repr': '全局标志表示', 'global_str': '全局字符串', 'member': '成员', 'nonmember': '非成员', 'pickle_by_enum_name': '按枚举名腌制', 'pickle_by_global_name': '按全局名腌制', 'show_flag_values': '显示标志值', 'unique': '唯一化', 'verify': '校验'}

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
import sys
import builtins as bltns
from types import MappingProxyType, DynamicClassAttribute
__all__ = ['EnumType', 'EnumMeta', 'EnumDict', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 'ReprEnum', 'auto', 'unique', 'property', 'verify', 'member', 'nonmember', 'FlagBoundary', 'STRICT', 'CONFORM', 'EJECT', 'KEEP', 'global_flag_repr', 'global_enum_repr', 'global_str', 'global_enum', 'EnumCheck', 'CONTINUOUS', 'NAMED_FLAGS', 'UNIQUE', 'pickle_by_global_name', 'pickle_by_enum_name']
枚举 = Flag = 弹出 = _stdlib_enums = 表示枚举 = None

class 非成员(object):
    """
    Protects item from becoming an Enum member during class creation.
    """

    def __init__(self, value):
        self.value = value

class 成员(object):
    """
    Forces item to become an Enum member during class creation.
    """

    def __init__(self, value):
        self.value = value

def _is_descriptor(obj):
    """
    Returns True if obj is a descriptor, False otherwise.
    """
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')

def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
    """
    return len(name) > 4 and name[:2] == name[-2:] == '__' and (name[2] != '_') and (name[-3] != '_')

def _is_sunder(name):
    """
    Returns True if a _sunder_ name, False otherwise.
    """
    return len(name) > 2 and name[0] == name[-1] == '_' and (name[1] != '_') and (name[-2] != '_')

def _is_internal_class(cls_name, obj):
    if not isinstance(obj, type):
        return False
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    return qualname == s_pattern or qualname.endswith(e_pattern)

def _is_private(cls_name, name):
    pattern = '_%s__' % (cls_name,)
    pat_len = len(pattern)
    if len(name) > pat_len and name.startswith(pattern) and (name[-1] != '_' or name[-2] != '_'):
        return True
    else:
        return False

def _is_single_bit(num):
    """
    True if only one bit set in num (should be an int)
    """
    if num == 0:
        return False
    num &= num - 1
    return num == 0

def _make_class_unpicklable(obj):
    """
    Make the given obj un-picklable.

    obj should be either a dictionary, or an Enum
    """

    def _break_on_call_reduce(self, proto):
        raise TypeError('%r cannot be pickled' % self)
    if isinstance(obj, dict):
        obj['__reduce_ex__'] = _break_on_call_reduce
        obj['__module__'] = '<unknown>'
    else:
        setattr(obj, '__reduce_ex__', _break_on_call_reduce)
        setattr(obj, '__module__', '<unknown>')

def _iter_bits_lsb(num):
    original = num
    if isinstance(num, 枚举):
        num = num.value
    if num < 0:
        raise ValueError('%r is not a positive integer' % original)
    while num:
        b = num & ~num + 1
        yield b
        num ^= b

def 显示标志值(value):
    return list(_iter_bits_lsb(value))

def bin(num, max_bits=None):
    """
    Like built-in bin(), except negative values are represented in
    twos-complement, and the leading bit always indicates sign
    (0=positive, 1=negative).

    >>> bin(10)
    '0b0 1010'
    >>> bin(~10)   # ~10 is -11
    '0b1 0101'
    """
    num = num.__index__()
    ceiling = 2 ** num.bit_length()
    if num >= 0:
        s = bltns.bin(num + ceiling).replace('1', '0', 1)
    else:
        s = bltns.bin(~num ^ ceiling - 1 + ceiling)
    sign = s[:3]
    digits = s[3:]
    if max_bits is not None:
        if len(digits) < max_bits:
            digits = (sign[-1] * max_bits + digits)[-max_bits:]
    return '%s %s' % (sign, digits)

class _not_given:

    def __repr__(self):
        return '<not given>'
_not_given = _not_given()

class _auto_null:

    def __repr__(self):
        return '_auto_null'
_auto_null = _auto_null()

class 自动:
    """
    Instances are replaced with an appropriate value in Enum class suites.
    """

    def __init__(self, value=_auto_null):
        self.value = value

    def __repr__(self):
        return 'auto(%r)' % self.value

class property(DynamicClassAttribute):
    """
    This is a descriptor, used to define attributes that act differently
    when accessed through an enum member and through an enum class.
    Instance access is the same as property(), but access to an attribute
    through the enum class will instead look in the class' _member_map_ for
    a corresponding enum member.
    """
    成员 = None
    _attr_type = None
    _cls_type = None

    def __get__(self, instance, ownerclass=None):
        if instance is None:
            if self.成员 is not None:
                return self.成员
            else:
                raise AttributeError('%r has no attribute %r' % (ownerclass, self.name))
        if self.fget is not None:
            return self.fget(instance)
        elif self._attr_type == 'attr':
            return getattr(self._cls_type, self.name)
        elif self._attr_type == 'desc':
            return getattr(instance._value_, self.name)
        try:
            return ownerclass._member_map_[self.name]
        except KeyError:
            raise AttributeError('%r has no attribute %r' % (ownerclass, self.name)) from None

    def __set__(self, instance, value):
        if self.fset is not None:
            return self.fset(instance, value)
        raise AttributeError('<enum %r> cannot set attribute %r' % (self.clsname, self.name))

    def __delete__(self, instance):
        if self.fdel is not None:
            return self.fdel(instance)
        raise AttributeError('<enum %r> cannot delete attribute %r' % (self.clsname, self.name))

    def __set_name__(self, ownerclass, name):
        self.name = name
        self.clsname = ownerclass.__name__
_装类转发(property, {'member': '成员'}, {'member': '成员'})

class _proto_member:
    """
    intermediate step for enum members between class execution and final creation
    """

    def __init__(self, value):
        self.value = value

    def __set_name__(self, enum_class, member_name):
        """
        convert each quasi-member into an instance of the new enum class
        """
        delattr(enum_class, member_name)
        value = self.value
        if not isinstance(value, tuple):
            args = (value,)
        else:
            args = value
        if enum_class._member_type_ is tuple:
            args = (args,)
        if not enum_class._use_args_:
            enum_member = enum_class._new_member_(enum_class)
        else:
            enum_member = enum_class._new_member_(enum_class, *args)
        if not hasattr(enum_member, '_value_'):
            if enum_class._member_type_ is object:
                enum_member._value_ = value
            else:
                try:
                    enum_member._value_ = enum_class._member_type_(*args)
                except Exception as exc:
                    new_exc = TypeError('_value_ not set in __new__, unable to create it')
                    new_exc.__cause__ = exc
                    raise new_exc
        value = enum_member._value_
        enum_member._name_ = member_name
        enum_member.__objclass__ = enum_class
        enum_member.__init__(*args)
        enum_member._sort_order_ = len(enum_class._member_names_)
        if Flag is not None and issubclass(enum_class, Flag):
            if isinstance(value, int):
                enum_class._flag_mask_ |= value
                if _is_single_bit(value):
                    enum_class._singles_mask_ |= value
            enum_class._all_bits_ = 2 ** enum_class._flag_mask_.bit_length() - 1
        try:
            try:
                enum_member = enum_class._value2member_map_[value]
            except TypeError:
                for name, canonical_member in enum_class._member_map_.items():
                    if canonical_member._value_ == value:
                        enum_member = canonical_member
                        break
                else:
                    raise KeyError
        except KeyError:
            if Flag is None or not issubclass(enum_class, Flag):
                enum_class._member_names_.append(member_name)
            elif Flag is not None and issubclass(enum_class, Flag) and isinstance(value, int) and _is_single_bit(value):
                enum_class._member_names_.append(member_name)
        enum_class._add_member_(member_name, enum_member)
        try:
            enum_class._value2member_map_.setdefault(value, enum_member)
            if value not in enum_class._hashable_values_:
                enum_class._hashable_values_.append(value)
        except TypeError:
            enum_class._unhashable_values_.append(value)
            enum_class._unhashable_values_map_.setdefault(member_name, []).append(value)

class 枚举字典(dict):
    """
    Track enum member order and ensure member names are not reused.

    EnumType will use the names found in self._member_names as the
    enumeration member names.
    """

    def __init__(self, cls_name=None):
        super().__init__()
        self._member_names = {}
        self._last_values = []
        self._ignore = []
        self._auto_called = False
        self._cls_name = cls_name

    def __setitem__(self, key, value):
        """
        Changes anything not dundered or not a descriptor.

        If an enum member name is used twice, an error is raised; duplicate
        values are not checked for.

        Single underscore (sunder) names are reserved.
        """
        if self._cls_name is not None and _is_private(self._cls_name, key):
            pass
        elif _is_sunder(key):
            if key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_') and (not key.startswith('_repr_')):
                raise ValueError('_sunder_ names, such as %r, are reserved for future Enum use' % (key,))
            if key == '_generate_next_value_':
                if self._auto_called:
                    raise TypeError('_generate_next_value_ must be defined before members')
                _gnv = value.__func__ if isinstance(value, staticmethod) else value
                setattr(self, '_generate_next_value', _gnv)
            elif key == '_ignore_':
                if isinstance(value, str):
                    value = value.replace(',', ' ').split()
                else:
                    value = list(value)
                self._ignore = value
                already = set(value) & set(self._member_names)
                if already:
                    raise ValueError('_ignore_ cannot specify already set names: %r' % (already,))
        elif _is_dunder(key):
            if key == '__order__':
                key = '_order_'
        elif key in self._member_names:
            raise TypeError('%r already defined as %r' % (key, self[key]))
        elif key in self._ignore:
            pass
        elif isinstance(value, 非成员):
            value = value.value
        elif _is_descriptor(value):
            pass
        elif self._cls_name is not None and _is_internal_class(self._cls_name, value):
            pass
        else:
            if key in self:
                raise TypeError('%r already defined as %r' % (key, self[key]))
            elif isinstance(value, 成员):
                value = value.value
            non_auto_store = True
            single = False
            if isinstance(value, 自动):
                single = True
                value = (value,)
            if isinstance(value, tuple) and any((isinstance(v, 自动) for v in value)):
                auto_valued = []
                t = type(value)
                for v in value:
                    if isinstance(v, 自动):
                        non_auto_store = False
                        if v.value == _auto_null:
                            v.value = self._generate_next_value(key, 1, len(self._member_names), self._last_values[:])
                            self._auto_called = True
                        v = v.value
                        self._last_values.append(v)
                    auto_valued.append(v)
                if single:
                    value = auto_valued[0]
                else:
                    try:
                        value = t(auto_valued)
                    except TypeError:
                        value = t(*auto_valued)
            self._member_names[key] = None
            if non_auto_store:
                self._last_values.append(value)
        super().__setitem__(key, value)

    @property
    def 成员名字(self):
        return list(self._member_names)

    def update(self, members, **more_members):
        try:
            for name in members.keys():
                self[name] = members[name]
        except AttributeError:
            for name, value in members:
                self[name] = value
        for name, value in more_members.items():
            self[name] = value
_装类转发(枚举字典, {'member_names': '成员名字'}, {'member_names': '成员名字'})
_EnumDict = 枚举字典

class 枚举类型(type):
    """
    Metaclass for Enum
    """

    @classmethod
    def __prepare__(metacls, cls, bases, **kwds):
        metacls._check_for_existing_members_(cls, bases)
        enum_dict = 枚举字典(cls)
        member_type, first_enum = metacls._get_mixins_(cls, bases)
        if first_enum is not None:
            enum_dict['_generate_next_value_'] = getattr(first_enum, '_generate_next_value_', None)
        return enum_dict

    def __new__(metacls, cls, bases, classdict, *, boundary=None, _simple=False, **kwds):
        if _simple:
            return super().__new__(metacls, cls, bases, classdict, **kwds)
        classdict.setdefault('_ignore_', []).append('_ignore_')
        ignore = classdict['_ignore_']
        for key in ignore:
            classdict.pop(key, None)
        成员名字 = classdict._member_names
        invalid_names = set(成员名字) & {'mro', ''}
        if invalid_names:
            raise ValueError('invalid enum member name(s) %s' % ','.join((repr(n) for n in invalid_names)))
        _order_ = classdict.pop('_order_', None)
        _gnv = classdict.get('_generate_next_value_')
        if _gnv is not None and type(_gnv) is not staticmethod:
            _gnv = staticmethod(_gnv)
        classdict = dict(classdict.items())
        if _gnv is not None:
            classdict['_generate_next_value_'] = _gnv
        member_type, first_enum = metacls._get_mixins_(cls, bases)
        __new__, save_new, use_args = metacls._find_new_(classdict, member_type, first_enum)
        classdict['_new_member_'] = __new__
        classdict['_use_args_'] = use_args
        for name in 成员名字:
            value = classdict[name]
            classdict[name] = _proto_member(value)
        classdict['_member_names_'] = []
        classdict['_member_map_'] = {}
        classdict['_value2member_map_'] = {}
        classdict['_hashable_values_'] = []
        classdict['_unhashable_values_'] = []
        classdict['_unhashable_values_map_'] = {}
        classdict['_member_type_'] = member_type
        classdict['_value_repr_'] = metacls._find_data_repr_(cls, bases)
        classdict['_boundary_'] = boundary or getattr(first_enum, '_boundary_', None)
        classdict['_flag_mask_'] = 0
        classdict['_singles_mask_'] = 0
        classdict['_all_bits_'] = 0
        classdict['_inverted_'] = None
        try:
            classdict['_%s__in_progress' % cls] = True
            enum_class = super().__new__(metacls, cls, bases, classdict, **kwds)
            classdict['_%s__in_progress' % cls] = False
            delattr(enum_class, '_%s__in_progress' % cls)
        except Exception as e:
            if hasattr(e, '__notes__'):
                del e.__notes__
            raise
        classdict.update(enum_class.__dict__)
        if 表示枚举 is not None and 表示枚举 in bases:
            if member_type is object:
                raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
            if '__format__' not in classdict:
                enum_class.__format__ = member_type.__format__
                classdict['__format__'] = enum_class.__format__
            if '__str__' not in classdict:
                method = member_type.__str__
                if method is object.__str__:
                    method = member_type.__repr__
                enum_class.__str__ = method
                classdict['__str__'] = enum_class.__str__
        for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
            if name not in classdict:
                enum_method = getattr(first_enum, name)
                found_method = getattr(enum_class, name)
                object_method = getattr(object, name)
                data_type_method = getattr(member_type, name)
                if found_method in (data_type_method, object_method):
                    setattr(enum_class, name, enum_method)
        if Flag is not None and issubclass(enum_class, Flag):
            for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__'):
                if name not in classdict:
                    enum_method = getattr(Flag, name)
                    setattr(enum_class, name, enum_method)
                    classdict[name] = enum_method
        if 枚举 is not None:
            if save_new:
                enum_class.__new_member__ = __new__
            enum_class.__new__ = 枚举.__new__
        if _order_ is not None:
            if isinstance(_order_, str):
                _order_ = _order_.replace(',', ' ').split()
        if Flag is None and cls != 'Flag' or (Flag is not None and (not issubclass(enum_class, Flag))):
            delattr(enum_class, '_boundary_')
            delattr(enum_class, '_flag_mask_')
            delattr(enum_class, '_singles_mask_')
            delattr(enum_class, '_all_bits_')
            delattr(enum_class, '_inverted_')
        elif Flag is not None and issubclass(enum_class, Flag):
            member_list = [m._value_ for m in enum_class]
            if member_list != sorted(member_list):
                enum_class._iter_member_ = enum_class._iter_member_by_def_
            if _order_:
                _order_ = [o for o in _order_ if o not in enum_class._member_map_ or _is_single_bit(enum_class[o]._value_)]
        if _order_:
            _order_ = [o for o in _order_ if o not in enum_class._member_map_ or (o in enum_class._member_map_ and o in enum_class._member_names_)]
            if _order_ != enum_class._member_names_:
                raise TypeError('member order does not match _order_:\n  %r\n  %r' % (enum_class._member_names_, _order_))
        return enum_class

    def __bool__(cls):
        """
        classes/types should always be True.
        """
        return True

    def __call__(cls, value, names=_not_given, *values, module=None, qualname=None, type=None, start=1, boundary=None):
        """
        Either returns an existing member, or creates a new enum class.

        This method is used both when an enum class is given a value to
        match to an enumeration member (i.e. Color(3)) and for the
        functional API (i.e. Color = Enum('Color', names='RED GREEN BLUE')).

        The value lookup branch is chosen if the enum is final.

        When used for the functional API:

        `value` will be the name of the new class.

        `names` should be either a string of white-space/comma delimited
        names (values will start at `start`), or an iterator/mapping of
        name, value pairs.

        `module` should be set to the module this class is being created in;
        if it is not set, an attempt to find that module will be made, but
        if it fails the class will not be picklable.

        `qualname` should be set to the actual location this class can be
        found at in its module; by default it is set to the global scope.
        If this is not correct, unpickling will fail in some circumstances.

        `type`, if set, will be mixed in as the first base class.
        """
        if cls._member_map_:
            if names is not _not_given:
                value = (value, names) + values
            return cls.__new__(cls, value)
        if names is _not_given and type is None:
            raise TypeError(f'{cls} has no members; specify `names=()` if you meant to create a new, empty, enum')
        return cls._create_(class_name=value, names=None if names is _not_given else names, module=module, qualname=qualname, type=type, start=start, boundary=boundary)

    def __contains__(cls, value):
        """Return True if `value` is in `cls`.

        `value` is in `cls` if:
        1) `value` is a member of `cls`, or
        2) `value` is the value of one of the `cls`'s members.
        3) `value` is a pseudo-member (flags)
        """
        if isinstance(value, cls):
            return True
        if issubclass(cls, Flag):
            try:
                result = cls._missing_(value)
                return isinstance(result, cls)
            except ValueError:
                pass
        return value in cls._unhashable_values_ or value in cls._hashable_values_

    def __delattr__(cls, attr):
        if attr in cls._member_map_:
            raise AttributeError('%r cannot delete member %r.' % (cls.__name__, attr))
        super().__delattr__(attr)

    def __dir__(cls):
        interesting = set(['__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__'] + cls._member_names_)
        if cls._new_member_ is not object.__new__:
            interesting.add('__new__')
        if cls.__init_subclass__ is not object.__init_subclass__:
            interesting.add('__init_subclass__')
        if cls._member_type_ is object:
            return sorted(interesting)
        else:
            return sorted(set(dir(cls._member_type_)) | interesting)

    def __getitem__(cls, name):
        """
        Return the member matching `name`.
        """
        return cls._member_map_[name]

    def __iter__(cls):
        """
        Return members in definition order.
        """
        return (cls._member_map_[name] for name in cls._member_names_)

    def __len__(cls):
        """
        Return the number of members (no aliases)
        """
        return len(cls._member_names_)

    @bltns.property
    def __members__(cls):
        """
        Returns a mapping of member name->value.

        This mapping lists all enum members, including aliases.  Note that
        this is a read-only view of the internal mapping.
        """
        return MappingProxyType(cls._member_map_)

    def __repr__(cls):
        if Flag is not None and issubclass(cls, Flag):
            return '<flag %r>' % cls.__name__
        else:
            return '<enum %r>' % cls.__name__

    def __reversed__(cls):
        """
        Return members in reverse definition order.
        """
        return (cls._member_map_[name] for name in reversed(cls._member_names_))

    def __setattr__(cls, name, value):
        """
        Block attempts to reassign Enum members.

        A simple assignment to the class namespace only changes one of the
        several possible ways to get an Enum member from the Enum class,
        resulting in an inconsistent Enumeration.
        """
        member_map = cls.__dict__.get('_member_map_', {})
        if name in member_map:
            raise AttributeError('cannot reassign member %r' % (name,))
        super().__setattr__(name, value)

    def _create_(cls, class_name, names, *, module=None, qualname=None, type=None, start=1, boundary=None):
        """
        Convenience method to create a new Enum class.

        `names` can be:

        * A string containing member names, separated either with spaces or
          commas.  Values are incremented by 1 from `start`.
        * An iterable of member names.  Values are incremented by 1 from `start`.
        * An iterable of (member name, value) pairs.
        * A mapping of member name -> value pairs.
        """
        metacls = cls.__class__
        bases = (cls,) if type is None else (type, cls)
        _, first_enum = cls._get_mixins_(class_name, bases)
        classdict = metacls.__prepare__(class_name, bases)
        if isinstance(names, str):
            names = names.replace(',', ' ').split()
        if isinstance(names, (tuple, list)) and names and isinstance(names[0], str):
            original_names, names = (names, [])
            last_values = []
            for count, name in enumerate(original_names):
                value = first_enum._generate_next_value_(name, start, count, last_values[:])
                last_values.append(value)
                names.append((name, value))
        if names is None:
            names = ()
        for item in names:
            if isinstance(item, str):
                member_name, member_value = (item, names[item])
            else:
                member_name, member_value = item
            classdict[member_name] = member_value
        if module is None:
            try:
                module = sys._getframemodulename(2)
            except AttributeError:
                try:
                    module = sys._getframe(2).f_globals['__name__']
                except (AttributeError, ValueError, KeyError):
                    pass
        if module is None:
            _make_class_unpicklable(classdict)
        else:
            classdict['__module__'] = module
        if qualname is not None:
            classdict['__qualname__'] = qualname
        return metacls.__new__(metacls, class_name, bases, classdict, boundary=boundary)

    def _convert_(cls, name, module, filter, source=None, *, boundary=None, as_global=False):
        """
        Create a new Enum subclass that replaces a collection of global constants
        """
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
        else:
            source = module_globals
        members = [(name, value) for name, value in source.items() if filter(name)]
        try:
            members.sort(key=lambda t: (t[1], t[0]))
        except TypeError:
            members.sort(key=lambda t: t[0])
        body = {t[0]: t[1] for t in members}
        body['__module__'] = module
        tmp_cls = type(name, (object,), body)
        cls = _simple_enum(etype=cls, boundary=boundary or 保留)(tmp_cls)
        if as_global:
            全局枚举(cls)
        else:
            sys.modules[cls.__module__].__dict__.update(cls.__members__)
        module_globals[name] = cls
        return cls

    @classmethod
    def _check_for_existing_members_(mcls, class_name, bases):
        for chain in bases:
            for base in chain.__mro__:
                if isinstance(base, 枚举类型) and base._member_names_:
                    raise TypeError('<enum %r> cannot extend %r' % (class_name, base))

    @classmethod
    def _get_mixins_(mcls, class_name, bases):
        """
        Returns the type for creating enum members, and the first inherited
        enum class.

        bases: the tuple of bases that was given to __new__
        """
        if not bases:
            return (object, 枚举)
        first_enum = bases[-1]
        if not isinstance(first_enum, 枚举类型):
            raise TypeError('new enumerations should be created as `EnumName([mixin_type, ...] [data_type,] enum_type)`')
        member_type = mcls._find_data_type_(class_name, bases) or object
        return (member_type, first_enum)

    @classmethod
    def _find_data_repr_(mcls, class_name, bases):
        for chain in bases:
            for base in chain.__mro__:
                if base is object:
                    continue
                elif isinstance(base, 枚举类型):
                    return base._value_repr_
                elif '__repr__' in base.__dict__:
                    if '__dataclass_fields__' in base.__dict__ and '__dataclass_params__' in base.__dict__ and base.__dict__['__dataclass_params__'].repr:
                        return _dataclass_repr
                    else:
                        return base.__dict__['__repr__']
        return None

    @classmethod
    def _find_data_type_(mcls, class_name, bases):
        data_types = set()
        base_chain = set()
        for chain in bases:
            candidate = None
            for base in chain.__mro__:
                base_chain.add(base)
                if base is object:
                    continue
                elif isinstance(base, 枚举类型):
                    if base._member_type_ is not object:
                        data_types.add(base._member_type_)
                        break
                elif '__new__' in base.__dict__ or '__dataclass_fields__' in base.__dict__:
                    data_types.add(candidate or base)
                    break
                else:
                    candidate = candidate or base
        if len(data_types) > 1:
            raise TypeError('too many data types for %r: %r' % (class_name, data_types))
        elif data_types:
            return data_types.pop()
        else:
            return None

    @classmethod
    def _find_new_(mcls, classdict, member_type, first_enum):
        """
        Returns the __new__ to be used for creating the enum members.

        classdict: the class dictionary given to __new__
        member_type: the data type whose __new__ will be used by default
        first_enum: enumeration to check for an overriding __new__
        """
        __new__ = classdict.get('__new__', None)
        save_new = first_enum is not None and __new__ is not None
        if __new__ is None:
            for method in ('__new_member__', '__new__'):
                for possible in (member_type, first_enum):
                    target = getattr(possible, method, None)
                    if target not in {None, None.__new__, object.__new__, 枚举.__new__}:
                        __new__ = target
                        break
                if __new__ is not None:
                    break
            else:
                __new__ = object.__new__
        if first_enum is None or __new__ in (枚举.__new__, object.__new__):
            use_args = False
        else:
            use_args = True
        return (__new__, save_new, use_args)

    def _add_member_(cls, name, member):
        if name in cls._member_map_:
            if cls._member_map_[name] is not member:
                raise NameError('%r is already bound: %r' % (name, cls._member_map_[name]))
            return
        found_descriptor = None
        descriptor_type = None
        class_type = None
        for base in cls.__mro__[1:]:
            attr = base.__dict__.get(name)
            if attr is not None:
                if isinstance(attr, (property, DynamicClassAttribute)):
                    found_descriptor = attr
                    class_type = base
                    descriptor_type = 'enum'
                    break
                elif _is_descriptor(attr):
                    found_descriptor = attr
                    descriptor_type = descriptor_type or 'desc'
                    class_type = class_type or base
                    continue
                else:
                    descriptor_type = 'attr'
                    class_type = base
        if found_descriptor:
            redirect = property()
            redirect.member = member
            redirect.__set_name__(cls, name)
            if descriptor_type in ('enum', 'desc'):
                redirect.fget = getattr(found_descriptor, 'fget', None)
                redirect._get = getattr(found_descriptor, '__get__', None)
                redirect.fset = getattr(found_descriptor, 'fset', None)
                redirect._set = getattr(found_descriptor, '__set__', None)
                redirect.fdel = getattr(found_descriptor, 'fdel', None)
                redirect._del = getattr(found_descriptor, '__delete__', None)
            redirect._attr_type = descriptor_type
            redirect._cls_type = class_type
            setattr(cls, name, redirect)
        else:
            setattr(cls, name, member)
        cls._member_map_[name] = member

    @property
    def __signature__(cls):
        from inspect import Parameter, Signature
        if cls._member_names_:
            return Signature([Parameter('values', Parameter.VAR_POSITIONAL)])
        else:
            return Signature([Parameter('new_class_name', Parameter.POSITIONAL_ONLY), Parameter('names', Parameter.POSITIONAL_OR_KEYWORD), Parameter('module', Parameter.KEYWORD_ONLY, default=None), Parameter('qualname', Parameter.KEYWORD_ONLY, default=None), Parameter('type', Parameter.KEYWORD_ONLY, default=None), Parameter('start', Parameter.KEYWORD_ONLY, default=1), Parameter('boundary', Parameter.KEYWORD_ONLY, default=None)])
枚举元类 = 枚举类型

class 枚举(metaclass=枚举类型):
    """
    Create a collection of name/value pairs.

    Example enumeration:

    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3

    Access them by:

    - attribute access:

      >>> Color.RED
      <Color.RED: 1>

    - value lookup:

      >>> Color(1)
      <Color.RED: 1>

    - name lookup:

      >>> Color['RED']
      <Color.RED: 1>

    Enumerations can be iterated over, and know how many members they have:

    >>> len(Color)
    3

    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.
    """

    def __new__(cls, value):
        if type(value) is cls:
            return value
        try:
            return cls._value2member_map_[value]
        except KeyError:
            pass
        except TypeError:
            for name, unhashable_values in cls._unhashable_values_map_.items():
                if value in unhashable_values:
                    return cls[name]
            for name, 成员 in cls._member_map_.items():
                if value == 成员._value_:
                    return cls[name]
        if not cls._member_map_:
            if getattr(cls, '_%s__in_progress' % cls.__name__, False):
                raise TypeError('do not use `super().__new__; call the appropriate __new__ directly') from None
            raise TypeError('%r has no members defined' % cls)
        try:
            exc = None
            result = cls._missing_(value)
        except Exception as e:
            exc = e
            result = None
        try:
            if isinstance(result, cls):
                return result
            elif Flag is not None and issubclass(cls, Flag) and (cls._boundary_ is 弹出) and isinstance(result, int):
                return result
            else:
                ve_exc = ValueError('%r is not a valid %s' % (value, cls.__qualname__))
                if result is None and exc is None:
                    raise ve_exc
                elif exc is None:
                    exc = TypeError('error in %s._missing_: returned %r instead of None or a valid member' % (cls.__name__, result))
                if not isinstance(exc, ValueError):
                    exc.__context__ = ve_exc
                raise exc
        finally:
            exc = None
            ve_exc = None

    def _add_alias_(self, name):
        self.__class__._add_member_(name, self)

    def _add_value_alias_(self, value):
        cls = self.__class__
        try:
            if value in cls._value2member_map_:
                if cls._value2member_map_[value] is not self:
                    raise ValueError('%r is already bound: %r' % (value, cls._value2member_map_[value]))
                return
        except TypeError:
            for m in cls._member_map_.values():
                if m._value_ == value:
                    if m is not self:
                        raise ValueError('%r is already bound: %r' % (value, cls._value2member_map_[value]))
                    return
        try:
            cls._value2member_map_.setdefault(value, self)
            cls._hashable_values_.append(value)
        except TypeError:
            cls._unhashable_values_.append(value)
            cls._unhashable_values_map_.setdefault(self.name, []).append(value)

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_values: the list of values assigned
        """
        if not last_values:
            return start
        try:
            last_value = sorted(last_values).pop()
        except TypeError:
            raise TypeError('unable to sort non-numeric values') from None
        try:
            return last_value + 1
        except TypeError:
            raise TypeError('unable to increment %r' % (last_value,)) from None

    @classmethod
    def _missing_(cls, value):
        return None

    def __repr__(self):
        v_repr = self.__class__._value_repr_ or repr
        return '<%s.%s: %s>' % (self.__class__.__name__, self._name_, v_repr(self._value_))

    def __str__(self):
        return '%s.%s' % (self.__class__.__name__, self._name_)

    def __dir__(self):
        """
        Returns public methods and other interesting attributes.
        """
        interesting = set()
        if self.__class__._member_type_ is not object:
            interesting = set(object.__dir__(self))
        for name in getattr(self, '__dict__', []):
            if name[0] != '_' and name not in self._member_map_:
                interesting.add(name)
        for cls in self.__class__.mro():
            for name, obj in cls.__dict__.items():
                if name[0] == '_':
                    continue
                if isinstance(obj, property):
                    if obj.fget is not None or name not in self._member_map_:
                        interesting.add(name)
                    else:
                        interesting.discard(name)
                elif name not in self._member_map_:
                    interesting.add(name)
        names = sorted(set(['__class__', '__doc__', '__eq__', '__hash__', '__module__']) | interesting)
        return names

    def __format__(self, format_spec):
        return str.__format__(str(self), format_spec)

    def __hash__(self):
        return hash(self._name_)

    def __reduce_ex__(self, proto):
        return (self.__class__, (self._value_,))

    def __deepcopy__(self, memo):
        return self

    def __copy__(self):
        return self

    @property
    def name(self):
        """The name of the Enum member."""
        return self._name_

    @property
    def value(self):
        """The value of the Enum member."""
        return self._value_

class 表示枚举(枚举):
    """
    Only changes the repr(), leaving str() and format() to the mixed-in type.
    """

class 整数枚举(int, 表示枚举):
    """
    Enum where members are also (and must be) ints
    """

class 字符串枚举(str, 表示枚举):
    """
    Enum where members are also (and must be) strings
    """

    def __new__(cls, *values):
        """values must already be of type `str`"""
        if len(values) > 3:
            raise TypeError('too many arguments for str(): %r' % (values,))
        if len(values) == 1:
            if not isinstance(values[0], str):
                raise TypeError('%r is not a string' % (values[0],))
        if len(values) >= 2:
            if not isinstance(values[1], str):
                raise TypeError('encoding must be a string, not %r' % (values[1],))
        if len(values) == 3:
            if not isinstance(values[2], str):
                raise TypeError('errors must be a string, not %r' % values[2])
        value = str(*values)
        成员 = str.__new__(cls, value)
        成员._value_ = value
        return 成员

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Return the lower-cased version of the member name.
        """
        return name.lower()

def 按全局名腌制(self, proto):
    return self.name
_reduce_ex_by_global_name = 按全局名腌制

def 按枚举名腌制(self, proto):
    return (getattr, (self.__class__, self._name_))

class 标志边界(字符串枚举):
    """
    control how out of range values are handled
    "strict" -> error is raised             [default for Flag]
    "conform" -> extra bits are discarded
    "eject" -> lose flag status
    "keep" -> keep flag status and all bits [default for IntFlag]
    """
    严格 = 自动()
    符合 = 自动()
    弹出 = 自动()
    保留 = 自动()
_装类转发(标志边界, {'CONFORM': '符合', 'EJECT': '弹出', 'KEEP': '保留', 'STRICT': '严格'}, {'CONFORM': '符合', 'EJECT': '弹出', 'KEEP': '保留', 'STRICT': '严格'})
严格, 符合, 弹出, 保留 = 标志边界

class Flag(枚举, boundary=严格):
    """
    Support for flags
    """
    _numeric_repr_ = repr

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_values: the last value assigned or None
        """
        if not count:
            return start if start is not None else 1
        last_value = max(last_values)
        try:
            high_bit = _high_bit(last_value)
        except Exception:
            raise TypeError('invalid flag value %r' % last_value) from None
        return 2 ** (high_bit + 1)

    @classmethod
    def _iter_member_by_value_(cls, value):
        """
        Extract all members from the value in definition (i.e. increasing value) order.
        """
        for val in _iter_bits_lsb(value & cls._flag_mask_):
            yield cls._value2member_map_.get(val)
    _iter_member_ = _iter_member_by_value_

    @classmethod
    def _iter_member_by_def_(cls, value):
        """
        Extract all members from the value in definition order.
        """
        yield from sorted(cls._iter_member_by_value_(value), key=lambda m: m._sort_order_)

    @classmethod
    def _missing_(cls, value):
        """
        Create a composite member containing all canonical members present in `value`.

        If non-member values are present, result depends on `_boundary_` setting.
        """
        if not isinstance(value, int):
            raise ValueError('%r is not a valid %s' % (value, cls.__qualname__))
        flag_mask = cls._flag_mask_
        singles_mask = cls._singles_mask_
        all_bits = cls._all_bits_
        neg_value = None
        if not ~all_bits <= value <= all_bits or value & (all_bits ^ flag_mask):
            if cls._boundary_ is 严格:
                max_bits = max(value.bit_length(), flag_mask.bit_length())
                raise ValueError('%r invalid value %r\n    given %s\n  allowed %s' % (cls, value, bin(value, max_bits), bin(flag_mask, max_bits)))
            elif cls._boundary_ is 符合:
                value = value & flag_mask
            elif cls._boundary_ is 弹出:
                return value
            elif cls._boundary_ is 保留:
                if value < 0:
                    value = max(all_bits + 1, 2 ** value.bit_length()) + value
            else:
                raise ValueError('%r unknown flag boundary %r' % (cls, cls._boundary_))
        if value < 0:
            neg_value = value
            value = all_bits + 1 + value
        unknown = value & ~flag_mask
        aliases = value & ~singles_mask
        member_value = value & singles_mask
        if unknown and cls._boundary_ is not 保留:
            raise ValueError('%s(%r) -->  unknown values %r [%s]' % (cls.__name__, value, unknown, bin(unknown)))
        if cls._member_type_ is object:
            pseudo_member = object.__new__(cls)
        else:
            pseudo_member = cls._member_type_.__new__(cls, value)
        if not hasattr(pseudo_member, '_value_'):
            pseudo_member._value_ = value
        if member_value or aliases:
            members = []
            combined_value = 0
            for m in cls._iter_member_(member_value):
                members.append(m)
                combined_value |= m._value_
            if aliases:
                value = member_value | aliases
                for n, pm in cls._member_map_.items():
                    if pm not in members and pm._value_ and (pm._value_ & value == pm._value_):
                        members.append(pm)
                        combined_value |= pm._value_
            unknown = value ^ combined_value
            pseudo_member._name_ = '|'.join([m._name_ for m in members])
            if not combined_value:
                pseudo_member._name_ = None
            elif unknown and cls._boundary_ is 严格:
                raise ValueError('%r: no members with value %r' % (cls, unknown))
            elif unknown:
                pseudo_member._name_ += '|%s' % cls._numeric_repr_(unknown)
        else:
            pseudo_member._name_ = None
        pseudo_member = cls._value2member_map_.setdefault(value, pseudo_member)
        if neg_value is not None:
            cls._value2member_map_[neg_value] = pseudo_member
        return pseudo_member

    def __contains__(self, other):
        """
        Returns True if self has at least the same flags set as other.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("unsupported operand type(s) for 'in': %r and %r" % (type(other).__qualname__, self.__class__.__qualname__))
        return other._value_ & self._value_ == other._value_

    def __iter__(self):
        """
        Returns flags in definition order.
        """
        yield from self._iter_member_(self._value_)

    def __len__(self):
        return self._value_.bit_count()

    def __repr__(self):
        cls_name = self.__class__.__name__
        v_repr = self.__class__._value_repr_ or repr
        if self._name_ is None:
            return '<%s: %s>' % (cls_name, v_repr(self._value_))
        else:
            return '<%s.%s: %s>' % (cls_name, self._name_, v_repr(self._value_))

    def __str__(self):
        cls_name = self.__class__.__name__
        if self._name_ is None:
            return '%s(%r)' % (cls_name, self._value_)
        else:
            return '%s.%s' % (cls_name, self._name_)

    def __bool__(self):
        return bool(self._value_)

    def _get_value(self, flag):
        if isinstance(flag, self.__class__):
            return flag._value_
        elif self._member_type_ is not object and isinstance(flag, self._member_type_):
            return flag
        return NotImplemented

    def __or__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        for flag in (self, other):
            if self._get_value(flag) is None:
                raise TypeError(f"'{flag}' cannot be combined with other flags with |")
        value = self._value_
        return self.__class__(value | other_value)

    def __and__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        for flag in (self, other):
            if self._get_value(flag) is None:
                raise TypeError(f"'{flag}' cannot be combined with other flags with &")
        value = self._value_
        return self.__class__(value & other_value)

    def __xor__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        for flag in (self, other):
            if self._get_value(flag) is None:
                raise TypeError(f"'{flag}' cannot be combined with other flags with ^")
        value = self._value_
        return self.__class__(value ^ other_value)

    def __invert__(self):
        if self._get_value(self) is None:
            raise TypeError(f"'{self}' cannot be inverted")
        if self._inverted_ is None:
            if self._boundary_ in (弹出, 保留):
                self._inverted_ = self.__class__(~self._value_)
            else:
                self._inverted_ = self.__class__(self._singles_mask_ & ~self._value_)
        return self._inverted_
    __rand__ = __and__
    __ror__ = __or__
    __rxor__ = __xor__

class 整数标志(int, 表示枚举, Flag, boundary=保留):
    """
    Support for integer-based Flags
    """

def _high_bit(value):
    """
    returns index of highest bit, or -1 if value is zero or negative
    """
    return value.bit_length() - 1

def 唯一化(enumeration):
    """
    Class decorator for enumerations ensuring unique member values.
    """
    duplicates = []
    for name, 成员 in enumeration.__members__.items():
        if name != 成员.name:
            duplicates.append((name, 成员.name))
    if duplicates:
        alias_details = ', '.join(['%s -> %s' % (alias, name) for alias, name in duplicates])
        raise ValueError('duplicate values found in %r: %s' % (enumeration, alias_details))
    return enumeration

def _dataclass_repr(self):
    dcf = self.__dataclass_fields__
    return ', '.join(('%s=%r' % (k, getattr(self, k)) for k in dcf.keys() if dcf[k].repr))

def 全局枚举表示(self):
    """
    use module.enum_name instead of class.enum_name

    the module is the last module in case of a multi-module name
    """
    module = self.__class__.__module__.split('.')[-1]
    return '%s.%s' % (module, self._name_)

def 全局标志表示(self):
    """
    use module.flag_name instead of class.flag_name

    the module is the last module in case of a multi-module name
    """
    module = self.__class__.__module__.split('.')[-1]
    cls_name = self.__class__.__name__
    if self._name_ is None:
        return '%s.%s(%r)' % (module, cls_name, self._value_)
    if _is_single_bit(self._value_):
        return '%s.%s' % (module, self._name_)
    if self._boundary_ is not 标志边界.保留:
        return '|'.join(['%s.%s' % (module, name) for name in self.name.split('|')])
    else:
        name = []
        for n in self._name_.split('|'):
            if n[0].isdigit():
                name.append(n)
            else:
                name.append('%s.%s' % (module, n))
        return '|'.join(name)

def 全局字符串(self):
    """
    use enum_name instead of class.enum_name
    """
    if self._name_ is None:
        cls_name = self.__class__.__name__
        return '%s(%r)' % (cls_name, self._value_)
    else:
        return self._name_

def 全局枚举(cls, update_str=False):
    """
    decorator that makes the repr() of an enum member reference its module
    instead of its class; also exports all members to the enum's module's
    global namespace
    """
    if issubclass(cls, Flag):
        cls.__repr__ = 全局标志表示
    else:
        cls.__repr__ = 全局枚举表示
    if not issubclass(cls, 表示枚举) or update_str:
        cls.__str__ = 全局字符串
    sys.modules[cls.__module__].__dict__.update(cls.__members__)
    return cls

def _simple_enum(etype=枚举, *, boundary=None, use_args=None):
    """
    Class decorator that converts a normal class into an :class:`Enum`.  No
    safety checks are done, and some advanced behavior (such as
    :func:`__init_subclass__`) is not available.  Enum creation can be faster
    using :func:`_simple_enum`.

        >>> from enum import Enum, _simple_enum
        >>> @_simple_enum(Enum)
        ... class Color:
        ...     RED = auto()
        ...     GREEN = auto()
        ...     BLUE = auto()
        >>> Color
        <enum 'Color'>
    """

    def convert_class(cls):
        nonlocal use_args
        cls_name = cls.__name__
        if use_args is None:
            use_args = etype._use_args_
        __new__ = cls.__dict__.get('__new__')
        if __new__ is not None:
            new_member = __new__.__func__
        else:
            new_member = etype._member_type_.__new__
        attrs = {}
        body = {}
        if __new__ is not None:
            body['__new_member__'] = new_member
        body['_new_member_'] = new_member
        body['_use_args_'] = use_args
        body['_generate_next_value_'] = gnv = etype._generate_next_value_
        body['_member_names_'] = 成员名字 = []
        body['_member_map_'] = member_map = {}
        body['_value2member_map_'] = value2member_map = {}
        body['_hashable_values_'] = hashable_values = []
        body['_unhashable_values_'] = unhashable_values = []
        body['_unhashable_values_map_'] = {}
        body['_member_type_'] = member_type = etype._member_type_
        body['_value_repr_'] = etype._value_repr_
        if issubclass(etype, Flag):
            body['_boundary_'] = boundary or etype._boundary_
            body['_flag_mask_'] = None
            body['_all_bits_'] = None
            body['_singles_mask_'] = None
            body['_inverted_'] = None
            body['__or__'] = Flag.__or__
            body['__xor__'] = Flag.__xor__
            body['__and__'] = Flag.__and__
            body['__ror__'] = Flag.__ror__
            body['__rxor__'] = Flag.__rxor__
            body['__rand__'] = Flag.__rand__
            body['__invert__'] = Flag.__invert__
        for name, obj in cls.__dict__.items():
            if name in ('__dict__', '__weakref__'):
                continue
            if _is_dunder(name) or _is_private(cls_name, name) or _is_sunder(name) or _is_descriptor(obj):
                body[name] = obj
            else:
                attrs[name] = obj
        if cls.__dict__.get('__doc__') is None:
            body['__doc__'] = 'An enumeration.'
        enum_class = type(cls_name, (etype,), body, boundary=boundary, _simple=True)
        for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
            if name not in body:
                enum_method = getattr(etype, name)
                found_method = getattr(enum_class, name)
                object_method = getattr(object, name)
                data_type_method = getattr(member_type, name)
                if found_method in (data_type_method, object_method):
                    setattr(enum_class, name, enum_method)
        gnv_last_values = []
        if issubclass(enum_class, Flag):
            single_bits = multi_bits = 0
            for name, value in attrs.items():
                if isinstance(value, 自动) and 自动.value is _auto_null:
                    value = gnv(name, 1, len(成员名字), gnv_last_values)
                if use_args:
                    if not isinstance(value, tuple):
                        value = (value,)
                    成员 = new_member(enum_class, *value)
                    value = value[0]
                else:
                    成员 = new_member(enum_class)
                if __new__ is None:
                    成员._value_ = value
                try:
                    contained = value2member_map.get(成员._value_)
                except TypeError:
                    contained = None
                    if 成员._value_ in unhashable_values or 成员.value in hashable_values:
                        for m in enum_class:
                            if m._value_ == 成员._value_:
                                contained = m
                                break
                if contained is not None:
                    contained._add_alias_(name)
                else:
                    成员._name_ = name
                    成员.__objclass__ = enum_class
                    成员.__init__(value)
                    成员._sort_order_ = len(成员名字)
                    if name not in ('name', 'value'):
                        setattr(enum_class, name, 成员)
                        member_map[name] = 成员
                    else:
                        enum_class._add_member_(name, 成员)
                    value2member_map[value] = 成员
                    hashable_values.append(value)
                    if _is_single_bit(value):
                        成员名字.append(name)
                        single_bits |= value
                    else:
                        multi_bits |= value
                    gnv_last_values.append(value)
            enum_class._flag_mask_ = single_bits | multi_bits
            enum_class._singles_mask_ = single_bits
            enum_class._all_bits_ = 2 ** (single_bits | multi_bits).bit_length() - 1
            member_list = [m._value_ for m in enum_class]
            if member_list != sorted(member_list):
                enum_class._iter_member_ = enum_class._iter_member_by_def_
        else:
            for name, value in attrs.items():
                if isinstance(value, 自动):
                    if value.value is _auto_null:
                        value.value = gnv(name, 1, len(成员名字), gnv_last_values)
                    value = value.value
                if use_args:
                    if not isinstance(value, tuple):
                        value = (value,)
                    成员 = new_member(enum_class, *value)
                    value = value[0]
                else:
                    成员 = new_member(enum_class)
                if __new__ is None:
                    成员._value_ = value
                try:
                    contained = value2member_map.get(成员._value_)
                except TypeError:
                    contained = None
                    if 成员._value_ in unhashable_values or 成员._value_ in hashable_values:
                        for m in enum_class:
                            if m._value_ == 成员._value_:
                                contained = m
                                break
                if contained is not None:
                    contained._add_alias_(name)
                else:
                    成员._name_ = name
                    成员.__objclass__ = enum_class
                    成员.__init__(value)
                    成员._sort_order_ = len(成员名字)
                    if name not in ('name', 'value'):
                        setattr(enum_class, name, 成员)
                        member_map[name] = 成员
                    else:
                        enum_class._add_member_(name, 成员)
                    成员名字.append(name)
                    gnv_last_values.append(value)
                    try:
                        enum_class._value2member_map_.setdefault(value, 成员)
                        if value not in hashable_values:
                            hashable_values.append(value)
                    except TypeError:
                        enum_class._unhashable_values_.append(value)
                        enum_class._unhashable_values_map_.setdefault(name, []).append(value)
        if '__new__' in body:
            enum_class.__new_member__ = enum_class.__new__
        enum_class.__new__ = 枚举.__new__
        return enum_class
    return convert_class

@_simple_enum(字符串枚举)
class 枚举检查:
    """
    various conditions to check an enumeration for
    """
    连续 = 'no skipped integer values'
    具名标志 = 'multi-flag aliases may not contain unnamed flags'
    唯一 = 'one name per value'
_装类转发(枚举检查, {'CONTINUOUS': '连续', 'NAMED_FLAGS': '具名标志', 'UNIQUE': '唯一'}, {'CONTINUOUS': '连续', 'NAMED_FLAGS': '具名标志', 'UNIQUE': '唯一'})
连续, 具名标志, 唯一 = 枚举检查

class 校验:
    """
    Check an enumeration for various constraints. (see EnumCheck)
    """

    def __init__(self, *checks):
        self.checks = checks

    def __call__(self, enumeration):
        checks = self.checks
        cls_name = enumeration.__name__
        if Flag is not None and issubclass(enumeration, Flag):
            enum_type = 'flag'
        elif issubclass(enumeration, 枚举):
            enum_type = 'enum'
        else:
            raise TypeError("the 'verify' decorator only works with Enum and Flag")
        for check in checks:
            if check is 唯一:
                duplicates = []
                for name, 成员 in enumeration.__members__.items():
                    if name != 成员.name:
                        duplicates.append((name, 成员.name))
                if duplicates:
                    alias_details = ', '.join(['%s -> %s' % (alias, name) for alias, name in duplicates])
                    raise ValueError('aliases found in %r: %s' % (enumeration, alias_details))
            elif check is 连续:
                values = set((e.value for e in enumeration))
                if len(values) < 2:
                    continue
                low, high = (min(values), max(values))
                missing = []
                if enum_type == 'flag':
                    for i in range(_high_bit(low) + 1, _high_bit(high)):
                        if 2 ** i not in values:
                            missing.append(2 ** i)
                elif enum_type == 'enum':
                    for i in range(low + 1, high):
                        if i not in values:
                            missing.append(i)
                else:
                    raise Exception('verify: unknown type %r' % enum_type)
                if missing:
                    raise ValueError(('invalid %s %r: missing values %s' % (enum_type, cls_name, ', '.join((str(m) for m in missing))))[:256])
            elif check is 具名标志:
                成员名字 = enumeration._member_names_
                member_values = [m.value for m in enumeration]
                missing_names = []
                missing_value = 0
                for name, alias in enumeration._member_map_.items():
                    if name in 成员名字:
                        continue
                    if alias.value < 0:
                        continue
                    values = list(_iter_bits_lsb(alias.value))
                    missed = [v for v in values if v not in member_values]
                    if missed:
                        missing_names.append(name)
                        for val in missed:
                            missing_value |= val
                if missing_names:
                    if len(missing_names) == 1:
                        alias = 'alias %s is missing' % missing_names[0]
                    else:
                        alias = 'aliases %s and %s are missing' % (', '.join(missing_names[:-1]), missing_names[-1])
                    if _is_single_bit(missing_value):
                        value = 'value 0x%x' % missing_value
                    else:
                        value = 'combined values of 0x%x' % missing_value
                    raise ValueError('invalid Flag %r: %s %s [use enum.show_flag_values(value) for details]' % (cls_name, alias, value))
        return enumeration

def _test_simple_enum(checked_enum, simple_enum):
    """
    A function that can be used to test an enum created with :func:`_simple_enum`
    against the version created by subclassing :class:`Enum`::

        >>> from enum import Enum, _simple_enum, _test_simple_enum
        >>> @_simple_enum(Enum)
        ... class Color:
        ...     RED = auto()
        ...     GREEN = auto()
        ...     BLUE = auto()
        >>> class CheckedColor(Enum):
        ...     RED = auto()
        ...     GREEN = auto()
        ...     BLUE = auto()
        >>> _test_simple_enum(CheckedColor, Color)

    If differences are found, a :exc:`TypeError` is raised.
    """
    failed = []
    if checked_enum.__dict__ != simple_enum.__dict__:
        checked_dict = checked_enum.__dict__
        checked_keys = list(checked_dict.keys())
        simple_dict = simple_enum.__dict__
        simple_keys = list(simple_dict.keys())
        成员名字 = set(list(checked_enum._member_map_.keys()) + list(simple_enum._member_map_.keys()))
        for key in set(checked_keys + simple_keys):
            if key in ('__module__', '_member_map_', '_value2member_map_', '__doc__', '__static_attributes__', '__firstlineno__'):
                continue
            elif key in 成员名字:
                continue
            elif key not in simple_keys:
                failed.append('missing key: %r' % (key,))
            elif key not in checked_keys:
                failed.append('extra key:   %r' % (key,))
            else:
                checked_value = checked_dict[key]
                simple_value = simple_dict[key]
                if callable(checked_value) or isinstance(checked_value, bltns.property):
                    continue
                if key == '__doc__':
                    compressed_checked_value = checked_value.replace(' ', '').replace('\t', '')
                    compressed_simple_value = simple_value.replace(' ', '').replace('\t', '')
                    if compressed_checked_value != compressed_simple_value:
                        failed.append('%r:\n         %s\n         %s' % (key, 'checked -> %r' % (checked_value,), 'simple  -> %r' % (simple_value,)))
                elif checked_value != simple_value:
                    failed.append('%r:\n         %s\n         %s' % (key, 'checked -> %r' % (checked_value,), 'simple  -> %r' % (simple_value,)))
        failed.sort()
        for name in 成员名字:
            failed_member = []
            if name not in simple_keys:
                failed.append('missing member from simple enum: %r' % name)
            elif name not in checked_keys:
                failed.append('extra member in simple enum: %r' % name)
            else:
                checked_member_dict = checked_enum[name].__dict__
                checked_member_keys = list(checked_member_dict.keys())
                simple_member_dict = simple_enum[name].__dict__
                simple_member_keys = list(simple_member_dict.keys())
                for key in set(checked_member_keys + simple_member_keys):
                    if key in ('__module__', '__objclass__', '_inverted_'):
                        continue
                    elif key not in simple_member_keys:
                        failed_member.append('missing key %r not in the simple enum member %r' % (key, name))
                    elif key not in checked_member_keys:
                        failed_member.append('extra key %r in simple enum member %r' % (key, name))
                    else:
                        checked_value = checked_member_dict[key]
                        simple_value = simple_member_dict[key]
                        if checked_value != simple_value:
                            failed_member.append('%r:\n         %s\n         %s' % (key, 'checked member -> %r' % (checked_value,), 'simple member  -> %r' % (simple_value,)))
            if failed_member:
                failed.append('%r member mismatch:\n      %s' % (name, '\n      '.join(failed_member)))
        for method in ('__str__', '__repr__', '__reduce_ex__', '__format__', '__getnewargs_ex__', '__getnewargs__', '__reduce_ex__', '__reduce__'):
            if method in simple_keys and method in checked_keys:
                continue
            elif method not in simple_keys and method not in checked_keys:
                checked_method = getattr(checked_enum, method, None)
                simple_method = getattr(simple_enum, method, None)
                if hasattr(checked_method, '__func__'):
                    checked_method = checked_method.__func__
                    simple_method = simple_method.__func__
                if checked_method != simple_method:
                    failed.append('%r:  %-30s %s' % (method, 'checked -> %r' % (checked_method,), 'simple -> %r' % (simple_method,)))
            else:
                pass
    if failed:
        raise TypeError('enum mismatch:\n   %s' % '\n   '.join(failed))

def _old_convert_(etype, name, module, filter, source=None, *, boundary=None):
    """
    Create a new Enum subclass that replaces a collection of global constants
    """
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
    else:
        source = module_globals
    members = [(name, value) for name, value in source.items() if filter(name)]
    try:
        members.sort(key=lambda t: (t[1], t[0]))
    except TypeError:
        members.sort(key=lambda t: t[0])
    cls = etype(name, members, module=module, boundary=boundary or 保留)
    return cls
_stdlib_enums = (整数枚举, 字符串枚举, 整数标志)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'CONFORM': '符合',
    'CONTINUOUS': '连续',
    'EJECT': '弹出',
    'Enum': '枚举',
    'EnumCheck': '枚举检查',
    'EnumDict': '枚举字典',
    'EnumMeta': '枚举元类',
    'EnumType': '枚举类型',
    'FlagBoundary': '标志边界',
    'IntEnum': '整数枚举',
    'IntFlag': '整数标志',
    'KEEP': '保留',
    'NAMED_FLAGS': '具名标志',
    'ReprEnum': '表示枚举',
    'STRICT': '严格',
    'StrEnum': '字符串枚举',
    'UNIQUE': '唯一',
    'auto': '自动',
    'global_enum': '全局枚举',
    'global_enum_repr': '全局枚举表示',
    'global_flag_repr': '全局标志表示',
    'global_str': '全局字符串',
    'member': '成员',
    'nonmember': '非成员',
    'pickle_by_enum_name': '按枚举名腌制',
    'pickle_by_global_name': '按全局名腌制',
    'show_flag_values': '显示标志值',
    'unique': '唯一化',
    'verify': '校验',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'property': {
        'member': '成员',
    },
    '枚举字典': {
        'member_names': '成员名字',
    },
    '枚举检查': {
        'CONTINUOUS': '连续',
        'NAMED_FLAGS': '具名标志',
        'UNIQUE': '唯一',
    },
    '标志边界': {
        'CONFORM': '符合',
        'EJECT': '弹出',
        'KEEP': '保留',
        'STRICT': '严格',
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
    'property': {
        'member': '成员',
    },
    '枚举字典': {
        'member_names': '成员名字',
    },
    '枚举检查': {
        'CONTINUOUS': '连续',
        'NAMED_FLAGS': '具名标志',
        'UNIQUE': '唯一',
    },
    '标志边界': {
        'CONFORM': '符合',
        'EJECT': '弹出',
        'KEEP': '保留',
        'STRICT': '严格',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '严格',
    '保留',
    '全局字符串',
    '全局枚举',
    '全局枚举表示',
    '全局标志表示',
    '具名标志',
    '唯一',
    '唯一化',
    '字符串枚举',
    '弹出',
    '成员',
    '按全局名腌制',
    '按枚举名腌制',
    '整数枚举',
    '整数标志',
    '枚举',
    '枚举元类',
    '枚举字典',
    '枚举检查',
    '枚举类型',
    '标志边界',
    '校验',
    '符合',
    '自动',
    '表示枚举',
    '连续',
    '非成员',
]

# ---- 转发层结束 ----
