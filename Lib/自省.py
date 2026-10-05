# -*- coding: utf-8 -*-
"""自省 —— 汉语库（由 tools/汉化库.py 从 Lib/inspect.py 机械生成，**不要手改**）。

英文库 Lib/inspect.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 自省
"""


"""Get useful information from live Python objects.

This module encapsulates the interface provided by the internal special
attributes (co_*, tb_*, etc.) in a friendlier fashion.
It also provides some help for examining source code and class layout.

Here are some of the useful functions provided by this module:

    ismodule(), isclass(), ismethod(), ispackage(), isfunction(),
        isgeneratorfunction(), isgenerator(), istraceback(), isframe(),
        iscode(), isbuiltin(), isroutine() - check object types
    getmembers() - get members of an object that satisfy a given condition

    getfile(), getsourcefile(), getsource() - find an object's source code
    getdoc(), getcomments() - get documentation on an object
    getmodule() - determine the module that an object came from
    getclasstree() - arrange classes so as to represent their hierarchy

    getargvalues(), getcallargs() - get info about function arguments
    getfullargspec() - same, with support for Python 3 features
    formatargvalues() - format an argument spec
    getouterframes(), getinnerframes() - get info about frames
    currentframe() - get the current stack frame
    stack(), trace() - get info about frames on the stack or in a traceback

    signature() - get a Signature object for the callable
"""
_英文原名表 = {'AGEN_CLOSED': '异步生成器已关闭', 'AGEN_CREATED': '异步生成器已创建', 'AGEN_RUNNING': '异步生成器运行中', 'AGEN_SUSPENDED': '异步生成器已挂起', 'ArgInfo': '参数信息', 'Arguments': '实参信息', 'Attribute': '属性信息', 'BlockFinder': '代码块查找器', 'BoundArguments': '绑定参数', 'BufferFlags': '缓冲标志', 'CORO_CLOSED': '协程已关闭', 'CORO_CREATED': '协程已创建', 'CORO_RUNNING': '协程运行中', 'CORO_SUSPENDED': '协程已挂起', 'ClassFoundException': '找到类异常', 'ClosureVars': '闭包变量', 'EndOfBlock': '代码块结束', 'FrameInfo': '帧信息', 'FullArgSpec': '完整参数规格', 'GEN_CLOSED': '生成器已关闭', 'GEN_CREATED': '生成器已创建', 'GEN_RUNNING': '生成器运行中', 'GEN_SUSPENDED': '生成器已挂起', 'Parameter': '形参', 'Signature': '签名', 'TPFLAGS_IS_ABSTRACT': '抽象标志位', 'Traceback': '回溯信息', 'classify_class_attrs': '分类类属性', 'cleandoc': '清理文档', 'currentframe': '当前帧', 'findsource': '找源码', 'formatannotation': '格式化注解', 'formatannotationrelativeto': '相对格式化注解', 'formatargvalues': '格式化参数值', 'getargs': '取参数', 'getargvalues': '取参数值', 'getasyncgenlocals': '取异步生成器局部变量', 'getasyncgenstate': '取异步生成器状态', 'getattr_static': '静态取属性', 'getblock': '取代码块', 'getcallargs': '取调用参数', 'getclasstree': '取类树', 'getclosurevars': '取闭包变量', 'getcomments': '取注释', 'getcoroutinelocals': '取协程局部变量', 'getcoroutinestate': '取协程状态', 'getdoc': '取文档', 'getfile': '取文件', 'getframeinfo': '取帧信息', 'getfullargspec': '取完整参数规格', 'getgeneratorlocals': '取生成器局部变量', 'getgeneratorstate': '取生成器状态', 'getinnerframes': '取内层帧', 'getlineno': '取行号', 'getmembers': '取成员', 'getmembers_static': '静态取成员', 'getmodule': '取模块', 'getmodulename': '取模块名', 'getmro': '取方法解析顺序', 'getouterframes': '取外层帧', 'getsource': '取源码', 'getsourcefile': '取源文件', 'getsourcelines': '取源码行', 'indentsize': '取缩进宽度', 'isabstract': '是抽象的吗', 'isasyncgen': '是异步生成器吗', 'isasyncgenfunction': '是异步生成器函数吗', 'isawaitable': '可等待吗', 'isbuiltin': '是内置函数吗', 'isclass': '是类吗', 'iscode': '是代码对象吗', 'iscoroutine': '是协程吗', 'iscoroutinefunction': '是协程函数吗', 'isdatadescriptor': '是数据描述符吗', 'isframe': '是帧吗', 'isfunction': '是函数吗', 'isgenerator': '是生成器吗', 'isgeneratorfunction': '是生成器函数吗', 'isgetsetdescriptor': '是取得设置描述符吗', 'ismemberdescriptor': '是成员描述符吗', 'ismethod': '是方法吗', 'ismethodwrapper': '是方法包装器吗', 'ismodule': '是模块吗', 'ispackage': '是包吗', 'isroutine': '是例程吗', 'istraceback': '是回溯吗', 'markcoroutinefunction': '标记协程函数', 'signature': '取签名', 'stack': '调用栈', 'trace': '回溯帧', 'unwrap': '解开包装', 'walktree': '遍历类树'}

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
__author__ = ('Ka-Ping Yee <ping@lfw.org>', 'Yury Selivanov <yselivanov@sprymix.com>')
__all__ = ['AGEN_CLOSED', 'AGEN_CREATED', 'AGEN_RUNNING', 'AGEN_SUSPENDED', 'ArgInfo', 'Arguments', 'Attribute', 'BlockFinder', 'BoundArguments', 'BufferFlags', 'CORO_CLOSED', 'CORO_CREATED', 'CORO_RUNNING', 'CORO_SUSPENDED', 'CO_ASYNC_GENERATOR', 'CO_COROUTINE', 'CO_GENERATOR', 'CO_ITERABLE_COROUTINE', 'CO_NESTED', 'CO_NEWLOCALS', 'CO_NOFREE', 'CO_OPTIMIZED', 'CO_VARARGS', 'CO_VARKEYWORDS', 'CO_HAS_DOCSTRING', 'CO_METHOD', 'ClassFoundException', 'ClosureVars', 'EndOfBlock', 'FrameInfo', 'FullArgSpec', 'GEN_CLOSED', 'GEN_CREATED', 'GEN_RUNNING', 'GEN_SUSPENDED', 'Parameter', 'Signature', 'TPFLAGS_IS_ABSTRACT', 'Traceback', 'classify_class_attrs', 'cleandoc', 'currentframe', 'findsource', 'formatannotation', 'formatannotationrelativeto', 'formatargvalues', 'get_annotations', 'getabsfile', 'getargs', 'getargvalues', 'getasyncgenlocals', 'getasyncgenstate', 'getattr_static', 'getblock', 'getcallargs', 'getclasstree', 'getclosurevars', 'getcomments', 'getcoroutinelocals', 'getcoroutinestate', 'getdoc', 'getfile', 'getframeinfo', 'getfullargspec', 'getgeneratorlocals', 'getgeneratorstate', 'getinnerframes', 'getlineno', 'getmembers', 'getmembers_static', 'getmodule', 'getmodulename', 'getmro', 'getouterframes', 'getsource', 'getsourcefile', 'getsourcelines', 'indentsize', 'isabstract', 'isasyncgen', 'isasyncgenfunction', 'isawaitable', 'isbuiltin', 'isclass', 'iscode', 'iscoroutine', 'iscoroutinefunction', 'isdatadescriptor', 'isframe', 'isfunction', 'isgenerator', 'isgeneratorfunction', 'isgetsetdescriptor', 'ismemberdescriptor', 'ismethod', 'ismethoddescriptor', 'ismethodwrapper', 'ismodule', 'ispackage', 'isroutine', 'istraceback', 'markcoroutinefunction', 'signature', 'stack', 'trace', 'unwrap', 'walktree']
import abc
from annotationlib import Format, ForwardRef
from annotationlib import get_annotations
import ast
import dis
import collections.abc
import enum
import importlib.machinery
import itertools
import linecache
import os
import re
import sys
import tokenize
import token
import types
import functools
import builtins
from keyword import iskeyword
from operator import attrgetter
from collections import namedtuple, OrderedDict
from weakref import ref as make_weakref
mod_dict = globals()
for k, v in dis.COMPILER_FLAG_NAMES.items():
    mod_dict['CO_' + v] = k
del k, v, mod_dict
抽象标志位 = 1 << 20

def 是模块吗(object):
    """Return true if the object is a module."""
    return isinstance(object, types.ModuleType)

def 是类吗(object):
    """Return true if the object is a class."""
    return isinstance(object, type)

def 是方法吗(object):
    """Return true if the object is an instance method."""
    return isinstance(object, types.MethodType)

def 是包吗(object):
    """Return true if the object is a package."""
    return 是模块吗(object) and hasattr(object, '__path__')

def ismethoddescriptor(object):
    """Return true if the object is a method descriptor.

    But not if ismethod(), isclass() or isfunction() is true.

    An object passing this test (for example, int.__add__) has a __get__
    attribute, but not a __set__ attribute or a __delete__ attribute.
    Beyond that, the set of attributes varies; __name__ is usually
    sensible, and __doc__ often is.

    Methods implemented via descriptors that also pass one of the other
    tests (ismethod(), isclass(), isfunction()) make this function return
    false, simply because those other tests promise more -- you can, for
    example, count on having the __func__ attribute when an object passes
    ismethod()."""
    if 是类吗(object) or 是方法吗(object) or 是函数吗(object):
        return False
    tp = type(object)
    return hasattr(tp, '__get__') and (not hasattr(tp, '__set__')) and (not hasattr(tp, '__delete__'))

def 是数据描述符吗(object):
    """Return true if the object is a data descriptor.

    But not if ismethod(), isclass() or isfunction() is true.

    Data descriptors have a __set__ or a __delete__ attribute.  Examples are
    properties, getsets, and members.  For the latter two (defined only in C
    extension modules) more specific tests are available as well:
    isgetsetdescriptor() and ismemberdescriptor(), respectively.

    Typically, data descriptors will also have __name__ and __doc__ attributes
    (properties, getsets, and members have both of these attributes), but this
    is not guaranteed."""
    if 是类吗(object) or 是方法吗(object) or 是函数吗(object):
        return False
    tp = type(object)
    return hasattr(tp, '__set__') or hasattr(tp, '__delete__')
if hasattr(types, 'MemberDescriptorType'):

    def 是成员描述符吗(object):
        """Return true if the object is a member descriptor.

        Member descriptors are specialized descriptors defined in extension
        modules."""
        return isinstance(object, types.MemberDescriptorType)
else:

    def 是成员描述符吗(object):
        """Return true if the object is a member descriptor.

        Member descriptors are specialized descriptors defined in extension
        modules."""
        return False
if hasattr(types, 'GetSetDescriptorType'):

    def 是取得设置描述符吗(object):
        """Return true if the object is a getset descriptor.

        getset descriptors are specialized descriptors defined in extension
        modules."""
        return isinstance(object, types.GetSetDescriptorType)
else:

    def 是取得设置描述符吗(object):
        """Return true if the object is a getset descriptor.

        getset descriptors are specialized descriptors defined in extension
        modules."""
        return False

def 是函数吗(object):
    """Return true if the object is a user-defined function.

    Function objects provide these attributes:
        __doc__         documentation string
        __name__        name with which this function was defined
        __qualname__    qualified name of this function
        __module__      name of the module the function was defined in or None
        __code__        code object containing compiled function bytecode
        __defaults__    tuple of any default values for arguments
        __globals__     global namespace in which this function was defined
        __annotations__ dict of parameter annotations
        __kwdefaults__  dict of keyword only parameters with defaults
        __dict__        namespace which is supporting arbitrary function attributes
        __closure__     a tuple of cells or None
        __type_params__ tuple of type parameters"""
    return isinstance(object, types.FunctionType)

def _has_code_flag(f, flag):
    """Return true if ``f`` is a function (or a method or functools.partial
    wrapper wrapping a function or a functools.partialmethod wrapping a
    function) whose code object has the given ``flag``
    set in its flags."""
    f = functools._unwrap_partialmethod(f)
    while 是方法吗(f):
        f = f.__func__
    f = functools._unwrap_partial(f)
    if not (是函数吗(f) or _signature_is_functionlike(f)):
        return False
    return bool(f.__code__.co_flags & flag)

def 是生成器函数吗(obj):
    """Return true if the object is a user-defined generator function.

    Generator function objects provide the same attributes as functions.
    See help(isfunction) for a list of attributes."""
    return _has_code_flag(obj, CO_GENERATOR)
_is_coroutine_mark = object()

def _has_coroutine_mark(f):
    while 是方法吗(f):
        f = f.__func__
    f = functools._unwrap_partial(f)
    return getattr(f, '_is_coroutine_marker', None) is _is_coroutine_mark

def 标记协程函数(func):
    """
    Decorator to ensure callable is recognised as a coroutine function.
    """
    if hasattr(func, '__func__'):
        func = func.__func__
    func._is_coroutine_marker = _is_coroutine_mark
    return func

def 是协程函数吗(obj):
    """Return true if the object is a coroutine function.

    Coroutine functions are normally defined with "async def" syntax, but may
    be marked via markcoroutinefunction.
    """
    return _has_code_flag(obj, CO_COROUTINE) or _has_coroutine_mark(obj)

def 是异步生成器函数吗(obj):
    """Return true if the object is an asynchronous generator function.

    Asynchronous generator functions are defined with "async def"
    syntax and have "yield" expressions in their body.
    """
    return _has_code_flag(obj, CO_ASYNC_GENERATOR)

def 是异步生成器吗(object):
    """Return true if the object is an asynchronous generator."""
    return isinstance(object, types.AsyncGeneratorType)

def 是生成器吗(object):
    """Return true if the object is a generator.

    Generator objects provide these attributes:
        gi_code         code object
        gi_frame        frame object or possibly None once the generator has
                        been exhausted
        gi_running      set to 1 when generator is executing, 0 otherwise
        gi_suspended    set to 1 when the generator is suspended at a yield point, 0 otherwise
        gi_yieldfrom    object being iterated by yield from or None

        __iter__()      defined to support iteration over container
        close()         raises a new GeneratorExit exception inside the
                        generator to terminate the iteration
        send()          resumes the generator and "sends" a value that becomes
                        the result of the current yield-expression
        throw()         used to raise an exception inside the generator"""
    return isinstance(object, types.GeneratorType)

def 是协程吗(object):
    """Return true if the object is a coroutine."""
    return isinstance(object, types.CoroutineType)

def 可等待吗(object):
    """Return true if object can be passed to an ``await`` expression."""
    return isinstance(object, types.CoroutineType) or (isinstance(object, types.GeneratorType) and bool(object.gi_code.co_flags & CO_ITERABLE_COROUTINE)) or isinstance(object, collections.abc.Awaitable)

def 是回溯吗(object):
    """Return true if the object is a traceback.

    Traceback objects provide these attributes:
        tb_frame        frame object at this level
        tb_lasti        index of last attempted instruction in bytecode
        tb_lineno       current line number in Python source code
        tb_next         next inner traceback object (called by this level)"""
    return isinstance(object, types.TracebackType)

def 是帧吗(object):
    """Return true if the object is a frame object.

    Frame objects provide these attributes:
        f_back          next outer frame object (this frame's caller)
        f_builtins      built-in namespace seen by this frame
        f_code          code object being executed in this frame
        f_globals       global namespace seen by this frame
        f_lasti         index of last attempted instruction in bytecode
        f_lineno        current line number in Python source code
        f_locals        local namespace seen by this frame
        f_trace         tracing function for this frame, or None
        f_trace_lines   is a tracing event triggered for each source line?
        f_trace_opcodes are per-opcode events being requested?

        clear()          used to clear all references to local variables"""
    return isinstance(object, types.FrameType)

def 是代码对象吗(object):
    """Return true if the object is a code object.

    Code objects provide these attributes:
        co_argcount         number of arguments (not including *, ** args
                            or keyword only arguments)
        co_code             string of raw compiled bytecode
        co_cellvars         tuple of names of cell variables
        co_consts           tuple of constants used in the bytecode
        co_filename         name of file in which this code object was created
        co_firstlineno      number of first line in Python source code
        co_flags            bitmap: 1=optimized | 2=newlocals | 4=*arg | 8=**arg
                            | 16=nested | 32=generator | 64=nofree | 128=coroutine
                            | 256=iterable_coroutine | 512=async_generator
                            | 0x4000000=has_docstring
        co_freevars         tuple of names of free variables
        co_posonlyargcount  number of positional only arguments
        co_kwonlyargcount   number of keyword only arguments (not including ** arg)
        co_lnotab           encoded mapping of line numbers to bytecode indices
        co_name             name with which this code object was defined
        co_names            tuple of names other than arguments and function locals
        co_nlocals          number of local variables
        co_stacksize        virtual machine stack space required
        co_varnames         tuple of names of arguments and local variables
        co_qualname         fully qualified function name

        co_lines()          returns an iterator that yields successive bytecode ranges
        co_positions()      returns an iterator of source code positions for each bytecode instruction
        replace()           returns a copy of the code object with a new values"""
    return isinstance(object, types.CodeType)

def 是内置函数吗(object):
    """Return true if the object is a built-in function or method.

    Built-in functions and methods provide these attributes:
        __doc__         documentation string
        __name__        original name of this function or method
        __self__        instance to which a method is bound, or None"""
    return isinstance(object, types.BuiltinFunctionType)

def 是方法包装器吗(object):
    """Return true if the object is a method wrapper."""
    return isinstance(object, types.MethodWrapperType)

def 是例程吗(object):
    """Return true if the object is any kind of function or method."""
    return 是内置函数吗(object) or 是函数吗(object) or 是方法吗(object) or ismethoddescriptor(object) or 是方法包装器吗(object) or isinstance(object, functools._singledispatchmethod_get)

def 是抽象的吗(object):
    """Return true if the object is an abstract base class (ABC)."""
    if not isinstance(object, type):
        return False
    if object.__flags__ & 抽象标志位:
        return True
    if not issubclass(type(object), abc.ABCMeta):
        return False
    if hasattr(object, '__abstractmethods__'):
        return False
    for 名字, value in object.__dict__.items():
        if getattr(value, '__isabstractmethod__', False):
            return True
    for base in object.__bases__:
        for 名字 in getattr(base, '__abstractmethods__', ()):
            value = getattr(object, 名字, None)
            if getattr(value, '__isabstractmethod__', False):
                return True
    return False

def _getmembers(object, predicate, getter):
    results = []
    processed = set()
    names = dir(object)
    if 是类吗(object):
        mro = 取方法解析顺序(object)
        try:
            for base in object.__bases__:
                for k, v in base.__dict__.items():
                    if isinstance(v, types.DynamicClassAttribute):
                        names.append(k)
        except AttributeError:
            pass
    else:
        mro = ()
    for key in names:
        try:
            value = getter(object, key)
            if key in processed:
                raise AttributeError
        except AttributeError:
            for base in mro:
                if key in base.__dict__:
                    value = base.__dict__[key]
                    break
            else:
                continue
        if not predicate or predicate(value):
            results.append((key, value))
        processed.add(key)
    results.sort(key=lambda pair: pair[0])
    return results

def 取成员(object, predicate=None):
    """Return all members of an object as (name, value) pairs sorted by name.
    Optionally, only return members that satisfy a given predicate."""
    return _getmembers(object, predicate, getattr)

def 静态取成员(object, predicate=None):
    """Return all members of an object as (name, value) pairs sorted by name
    without triggering dynamic lookup via the descriptor protocol,
    __getattr__ or __getattribute__. Optionally, only return members that
    satisfy a given predicate.

    Note: this function may not be able to retrieve all members
       that getmembers can fetch (like dynamically created attributes)
       and may find members that getmembers can't (like descriptors
       that raise AttributeError). It can also return descriptor objects
       instead of instance members in some cases.
    """
    return _getmembers(object, predicate, 静态取属性)
属性信息 = namedtuple('Attribute', 'name kind defining_class object')

def 分类类属性(cls):
    """Return list of attribute-descriptor tuples.

    For each name in dir(cls), the return list contains a 4-tuple
    with these elements:

        0. The name (a string).

        1. The kind of attribute this is, one of these strings:
               'class method'    created via classmethod()
               'static method'   created via staticmethod()
               'property'        created via property()
               'method'          any other flavor of method or descriptor
               'data'            not a method

        2. The class which defined this attribute (a class).

        3. The object as obtained by calling getattr; if this fails, or if the
           resulting object does not live anywhere in the class' mro (including
           metaclasses) then the object is looked up in the defining class's
           dict (found by walking the mro).

    If one of the items in dir(cls) is stored in the metaclass it will now
    be discovered and not have None be listed as the class in which it was
    defined.  Any items whose home class cannot be discovered are skipped.
    """
    mro = 取方法解析顺序(cls)
    metamro = 取方法解析顺序(type(cls))
    metamro = tuple((cls for cls in metamro if cls not in (type, object)))
    class_bases = (cls,) + mro
    all_bases = class_bases + metamro
    names = dir(cls)
    for base in mro:
        for k, v in base.__dict__.items():
            if isinstance(v, types.DynamicClassAttribute) and v.fget is not None:
                names.append(k)
    result = []
    processed = set()
    for 名字 in names:
        homecls = None
        get_obj = None
        dict_obj = None
        if 名字 not in processed:
            try:
                if 名字 == '__dict__':
                    raise Exception("__dict__ is special, don't want the proxy")
                get_obj = getattr(cls, 名字)
            except Exception:
                pass
            else:
                homecls = getattr(get_obj, '__objclass__', homecls)
                if homecls not in class_bases:
                    homecls = None
                    last_cls = None
                    for srch_cls in class_bases:
                        srch_obj = getattr(srch_cls, 名字, None)
                        if srch_obj is get_obj:
                            last_cls = srch_cls
                    for srch_cls in metamro:
                        try:
                            srch_obj = srch_cls.__getattr__(cls, 名字)
                        except AttributeError:
                            continue
                        if srch_obj is get_obj:
                            last_cls = srch_cls
                    if last_cls is not None:
                        homecls = last_cls
        for base in all_bases:
            if 名字 in base.__dict__:
                dict_obj = base.__dict__[名字]
                if homecls not in metamro:
                    homecls = base
                break
        if homecls is None:
            continue
        obj = get_obj if get_obj is not None else dict_obj
        if isinstance(dict_obj, (staticmethod, types.BuiltinMethodType)):
            种类 = 'static method'
            obj = dict_obj
        elif isinstance(dict_obj, (classmethod, types.ClassMethodDescriptorType)):
            种类 = 'class method'
            obj = dict_obj
        elif isinstance(dict_obj, property):
            种类 = 'property'
            obj = dict_obj
        elif 是例程吗(obj):
            种类 = 'method'
        else:
            种类 = 'data'
        result.append(属性信息(名字, 种类, homecls, obj))
        processed.add(名字)
    return result

def 取方法解析顺序(cls):
    """Return tuple of base classes (including cls) in method resolution order."""
    return cls.__mro__

def 解开包装(func, *, stop=None):
    """Get the object wrapped by *func*.

   Follows the chain of :attr:`__wrapped__` attributes returning the last
   object in the chain.

   *stop* is an optional callback accepting an object in the wrapper chain
   as its sole argument that allows the unwrapping to be terminated early if
   the callback returns a true value. If the callback never returns a true
   value, the last object in the chain is returned as usual. For example,
   :func:`signature` uses this to stop unwrapping if any object in the
   chain has a ``__signature__`` attribute defined.

   :exc:`ValueError` is raised if a cycle is encountered.

    """
    f = func
    memo = {id(f): f}
    recursion_limit = sys.getrecursionlimit()
    while not isinstance(func, type) and hasattr(func, '__wrapped__'):
        if stop is not None and stop(func):
            break
        func = func.__wrapped__
        id_func = id(func)
        if id_func in memo or len(memo) >= recursion_limit:
            raise ValueError('wrapper loop when unwrapping {!r}'.format(f))
        memo[id_func] = func
    return func

def 取缩进宽度(line):
    """Return the indent size, in spaces, at the start of a line of text."""
    expline = line.expandtabs()
    return len(expline) - len(expline.lstrip())

def _findclass(func):
    cls = sys.modules.get(func.__module__)
    if cls is None:
        return None
    for 名字 in func.__qualname__.split('.')[:-1]:
        cls = getattr(cls, 名字)
    if not 是类吗(cls):
        return None
    return cls

def _finddoc(obj):
    if 是类吗(obj):
        for base in obj.__mro__:
            if base is not object:
                try:
                    doc = base.__doc__
                except AttributeError:
                    continue
                if doc is not None:
                    return doc
        return None
    if 是方法吗(obj):
        名字 = obj.__func__.__name__
        self = obj.__self__
        if 是类吗(self) and getattr(getattr(self, 名字, None), '__func__') is obj.__func__:
            cls = self
        else:
            cls = self.__class__
    elif 是函数吗(obj):
        名字 = obj.__name__
        cls = _findclass(obj)
        if cls is None or getattr(cls, 名字) is not obj:
            return None
    elif 是内置函数吗(obj):
        名字 = obj.__name__
        self = obj.__self__
        if 是类吗(self) and self.__qualname__ + '.' + 名字 == obj.__qualname__:
            cls = self
        else:
            cls = self.__class__
    elif isinstance(obj, property):
        名字 = obj.__name__
        cls = _findclass(obj.fget)
        if cls is None or getattr(cls, 名字) is not obj:
            return None
    elif ismethoddescriptor(obj) or 是数据描述符吗(obj):
        名字 = obj.__name__
        cls = obj.__objclass__
        if getattr(cls, 名字) is not obj:
            return None
        if 是成员描述符吗(obj):
            slots = getattr(cls, '__slots__', None)
            if isinstance(slots, dict) and 名字 in slots:
                return slots[名字]
    else:
        return None
    for base in cls.__mro__:
        try:
            doc = getattr(base, 名字).__doc__
        except AttributeError:
            continue
        if doc is not None:
            return doc
    return None

def 取文档(object):
    """Get the documentation string for an object.

    All tabs are expanded to spaces.  To clean up docstrings that are
    indented to line up with blocks of code, any whitespace than can be
    uniformly removed from the second line onwards is removed."""
    try:
        doc = object.__doc__
    except AttributeError:
        return None
    if doc is None:
        try:
            doc = _finddoc(object)
        except (AttributeError, TypeError):
            return None
    if not isinstance(doc, str):
        return None
    return 清理文档(doc)

def 清理文档(doc):
    """Clean up indentation from docstrings.

    Any whitespace that can be uniformly removed from the second line
    onwards is removed."""
    lines = doc.expandtabs().split('\n')
    margin = sys.maxsize
    for line in lines[1:]:
        content = len(line.lstrip(' '))
        if content:
            indent = len(line) - content
            margin = min(margin, indent)
    if lines:
        lines[0] = lines[0].lstrip(' ')
    if margin < sys.maxsize:
        for i in range(1, len(lines)):
            lines[i] = lines[i][margin:]
    while lines and (not lines[-1]):
        lines.pop()
    while lines and (not lines[0]):
        lines.pop(0)
    return '\n'.join(lines)

def 取文件(object):
    """Work out which source or compiled file an object was defined in."""
    if 是模块吗(object):
        if getattr(object, '__file__', None):
            return object.__file__
        raise TypeError('{!r} is a built-in module'.format(object))
    if 是类吗(object):
        if hasattr(object, '__module__'):
            module = sys.modules.get(object.__module__)
            if getattr(module, '__file__', None):
                return module.__file__
            if object.__module__ == '__main__':
                raise OSError('source code not available')
        raise TypeError('{!r} is a built-in class'.format(object))
    if 是方法吗(object):
        object = object.__func__
    if 是函数吗(object):
        object = object.__code__
    if 是回溯吗(object):
        object = object.tb_frame
    if 是帧吗(object):
        object = object.f_code
    if 是代码对象吗(object):
        return object.co_filename
    raise TypeError('module, class, method, function, traceback, frame, or code object was expected, got {}'.format(type(object).__name__))

def 取模块名(path):
    """Return the module name for a given file, or None."""
    fname = os.path.basename(path)
    suffixes = [(-len(suffix), suffix) for suffix in importlib.machinery.all_suffixes()]
    suffixes.sort()
    for neglen, suffix in suffixes:
        if fname.endswith(suffix):
            return fname[:neglen]
    return None

def 取源文件(object):
    """Return the filename that can be used to locate an object's source.
    Return None if no way can be identified to get the source.
    """
    filename = 取文件(object)
    all_bytecode_suffixes = importlib.machinery.BYTECODE_SUFFIXES[:]
    if any((filename.endswith(s) for s in all_bytecode_suffixes)):
        filename = os.path.splitext(filename)[0] + importlib.machinery.SOURCE_SUFFIXES[0]
    elif any((filename.endswith(s) for s in importlib.machinery.EXTENSION_SUFFIXES)):
        return None
    elif filename.endswith('.fwork'):
        return None
    if filename in linecache.cache:
        return filename
    if os.path.exists(filename):
        return filename
    module = 取模块(object, filename)
    if getattr(module, '__loader__', None) is not None:
        return filename
    elif getattr(getattr(module, '__spec__', None), 'loader', None) is not None:
        return filename

def getabsfile(object, _filename=None):
    """Return an absolute path to the source or compiled file for an object.

    The idea is for each object to have a unique origin, so this routine
    normalizes the result as much as possible."""
    if _filename is None:
        _filename = 取源文件(object) or 取文件(object)
    return os.path.normcase(os.path.abspath(_filename))
modulesbyfile = {}
_filesbymodname = {}

def 取模块(object, _filename=None):
    """Return the module an object was defined in, or None if not found."""
    if 是模块吗(object):
        return object
    if hasattr(object, '__module__'):
        return sys.modules.get(object.__module__)
    if _filename is not None and _filename in modulesbyfile:
        return sys.modules.get(modulesbyfile[_filename])
    try:
        file = getabsfile(object, _filename)
    except (TypeError, FileNotFoundError):
        return None
    if file in modulesbyfile:
        return sys.modules.get(modulesbyfile[file])
    for modname, module in sys.modules.copy().items():
        if 是模块吗(module) and hasattr(module, '__file__'):
            f = module.__file__
            if f == _filesbymodname.get(modname, None):
                continue
            _filesbymodname[modname] = f
            f = getabsfile(module)
            modulesbyfile[f] = modulesbyfile[os.path.realpath(f)] = module.__name__
    if file in modulesbyfile:
        return sys.modules.get(modulesbyfile[file])
    main = sys.modules['__main__']
    if not hasattr(object, '__name__'):
        return None
    if hasattr(main, object.__name__):
        mainobject = getattr(main, object.__name__)
        if mainobject is object:
            return main
    builtin = sys.modules['builtins']
    if hasattr(builtin, object.__name__):
        builtinobject = getattr(builtin, object.__name__)
        if builtinobject is object:
            return builtin

class 找到类异常(Exception):
    pass

def 找源码(object):
    """Return the entire source file and starting line number for an object.

    The argument may be a module, class, method, function, traceback, frame,
    or code object.  The source code is returned as a list of all the lines
    in the file and the line number indexes a line in that list.  An OSError
    is raised if the source code cannot be retrieved."""
    file = 取源文件(object)
    if file:
        linecache.checkcache(file)
    else:
        file = 取文件(object)
        if not (file.startswith('<') and file.endswith('>')) or file.endswith('.fwork'):
            raise OSError('source code not available')
    module = 取模块(object, file)
    if module:
        lines = linecache.getlines(file, module.__dict__)
        if not lines and file.startswith('<') and hasattr(object, '__code__'):
            lines = linecache._getlines_from_code(object.__code__)
    else:
        lines = linecache.getlines(file)
    if not lines:
        raise OSError('could not get source code')
    if 是模块吗(object):
        return (lines, 0)
    if 是类吗(object):
        try:
            lnum = vars(object)['__firstlineno__'] - 1
        except (TypeError, KeyError):
            raise OSError('source code not available')
        if lnum >= len(lines):
            raise OSError('lineno is out of bounds')
        return (lines, lnum)
    if 是方法吗(object):
        object = object.__func__
    if 是函数吗(object):
        object = object.__code__
    if 是回溯吗(object):
        object = object.tb_frame
    if 是帧吗(object):
        object = object.f_code
    if 是代码对象吗(object):
        if not hasattr(object, 'co_firstlineno'):
            raise OSError('could not find function definition')
        lnum = object.co_firstlineno - 1
        if lnum >= len(lines):
            raise OSError('lineno is out of bounds')
        return (lines, lnum)
    raise OSError('could not find code object')

def 取注释(object):
    """Get lines of comments immediately preceding an object's source code.

    Returns None when source can't be found.
    """
    try:
        lines, lnum = 找源码(object)
    except (OSError, TypeError):
        return None
    if 是模块吗(object):
        start = 0
        if lines and lines[0][:2] == '#!':
            start = 1
        while start < len(lines) and lines[start].strip() in ('', '#'):
            start = start + 1
        if start < len(lines) and lines[start][:1] == '#':
            comments = []
            end = start
            while end < len(lines) and lines[end][:1] == '#':
                comments.append(lines[end].expandtabs())
                end = end + 1
            return ''.join(comments)
    elif lnum > 0:
        indent = 取缩进宽度(lines[lnum])
        end = lnum - 1
        if end >= 0 and lines[end].lstrip()[:1] == '#' and (取缩进宽度(lines[end]) == indent):
            comments = [lines[end].expandtabs().lstrip()]
            if end > 0:
                end = end - 1
                comment = lines[end].expandtabs().lstrip()
                while comment[:1] == '#' and 取缩进宽度(lines[end]) == indent:
                    comments[:0] = [comment]
                    end = end - 1
                    if end < 0:
                        break
                    comment = lines[end].expandtabs().lstrip()
            while comments and comments[0].strip() == '#':
                comments[:1] = []
            while comments and comments[-1].strip() == '#':
                comments[-1:] = []
            return ''.join(comments)

class 代码块结束(Exception):
    pass

class 代码块查找器:
    """Provide a tokeneater() method to detect the end of a code block."""

    def __init__(self):
        self.indent = 0
        self.singleline = False
        self.started = False
        self.passline = False
        self.indecorator = False
        self.last = 1
        self.body_col0 = None

    def 处理词法单元(self, type, token, srowcol, erowcol, line):
        if not self.started and (not self.indecorator):
            if type in (tokenize.INDENT, tokenize.COMMENT, tokenize.NL):
                pass
            elif token == 'async':
                pass
            elif token == '@':
                self.indecorator = True
            else:
                self.singleline = token not in ('def', 'class')
                self.started = True
            self.passline = True
        elif type == tokenize.NEWLINE:
            self.passline = False
            self.last = srowcol[0]
            if self.singleline:
                raise 代码块结束
            if self.indecorator:
                self.indecorator = False
        elif self.passline:
            pass
        elif type == tokenize.INDENT:
            if self.body_col0 is None and self.started:
                self.body_col0 = erowcol[1]
            self.indent = self.indent + 1
            self.passline = True
        elif type == tokenize.DEDENT:
            self.indent = self.indent - 1
            if self.indent <= 0:
                raise 代码块结束
        elif type == tokenize.COMMENT:
            if self.body_col0 is not None and srowcol[1] >= self.body_col0:
                self.last = srowcol[0]
        elif self.indent == 0 and type not in (tokenize.COMMENT, tokenize.NL):
            raise 代码块结束
_装类转发(代码块查找器, {'tokeneater': '处理词法单元'}, {'tokeneater': '处理词法单元'})

def 取代码块(lines):
    """Extract the block of code at the top of the given list of lines."""
    blockfinder = 代码块查找器()
    try:
        tokens = tokenize.generate_tokens(iter(lines).__next__)
        for _token in tokens:
            blockfinder.tokeneater(*_token)
    except (代码块结束, IndentationError):
        pass
    except SyntaxError as e:
        if 'unmatched' not in e.msg:
            raise e from None
        _, *_token_info = _token
        try:
            blockfinder.tokeneater(tokenize.NEWLINE, *_token_info)
        except (代码块结束, IndentationError):
            pass
    return lines[:blockfinder.last]

def 取源码行(object):
    """Return a list of source lines and starting line number for an object.

    The argument may be a module, class, method, function, traceback, frame,
    or code object.  The source code is returned as a list of the lines
    corresponding to the object and the line number indicates where in the
    original source file the first line of code was found.  An OSError is
    raised if the source code cannot be retrieved."""
    object = 解开包装(object)
    lines, lnum = 找源码(object)
    if 是回溯吗(object):
        object = object.tb_frame
    if 是模块吗(object) or (是帧吗(object) and object.f_code.co_name == '<module>'):
        return (lines, 0)
    else:
        return (取代码块(lines[lnum:]), lnum + 1)

def 取源码(object):
    """Return the text of the source code for an object.

    The argument may be a module, class, method, function, traceback, frame,
    or code object.  The source code is returned as a single string.  An
    OSError is raised if the source code cannot be retrieved."""
    lines, lnum = 取源码行(object)
    return ''.join(lines)

def 遍历类树(classes, children, parent):
    """Recursive helper function for getclasstree()."""
    results = []
    classes.sort(key=attrgetter('__module__', '__name__'))
    for c in classes:
        results.append((c, c.__bases__))
        if c in children:
            results.append(遍历类树(children[c], children, c))
    return results

def 取类树(classes, unique=False):
    """Arrange the given list of classes into a hierarchy of nested lists.

    Where a nested list appears, it contains classes derived from the class
    whose entry immediately precedes the list.  Each entry is a 2-tuple
    containing a class and a tuple of its base classes.  If the 'unique'
    argument is true, exactly one entry appears in the returned structure
    for each class in the given list.  Otherwise, classes using multiple
    inheritance and their descendants will appear multiple times."""
    children = {}
    roots = []
    for c in classes:
        if c.__bases__:
            for parent in c.__bases__:
                if parent not in children:
                    children[parent] = []
                if c not in children[parent]:
                    children[parent].append(c)
                if unique and parent in classes:
                    break
        elif c not in roots:
            roots.append(c)
    for parent in children:
        if parent not in classes:
            roots.append(parent)
    return 遍历类树(roots, children, None)
实参信息 = namedtuple('Arguments', 'args, varargs, varkw')

def 取参数(co):
    """Get information about the arguments accepted by a code object.

    Three things are returned: (args, varargs, varkw), where
    'args' is the list of argument names. Keyword-only arguments are
    appended. 'varargs' and 'varkw' are the names of the * and **
    arguments or None."""
    if not 是代码对象吗(co):
        raise TypeError('{!r} is not a code object'.format(co))
    names = co.co_varnames
    nargs = co.co_argcount
    nkwargs = co.co_kwonlyargcount
    参数 = list(names[:nargs])
    kwonlyargs = list(names[nargs:nargs + nkwargs])
    nargs += nkwargs
    varargs = None
    if co.co_flags & CO_VARARGS:
        varargs = co.co_varnames[nargs]
        nargs = nargs + 1
    varkw = None
    if co.co_flags & CO_VARKEYWORDS:
        varkw = co.co_varnames[nargs]
    return 实参信息(参数 + kwonlyargs, varargs, varkw)
完整参数规格 = namedtuple('FullArgSpec', 'args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations')

def 取完整参数规格(func):
    """Get the names and default values of a callable object's parameters.

    A tuple of seven things is returned:
    (args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations).
    'args' is a list of the parameter names.
    'varargs' and 'varkw' are the names of the * and ** parameters or None.
    'defaults' is an n-tuple of the default values of the last n parameters.
    'kwonlyargs' is a list of keyword-only parameter names.
    'kwonlydefaults' is a dictionary mapping names from kwonlyargs to defaults.
    'annotations' is a dictionary mapping parameter names to annotations.

    Notable differences from inspect.signature():
      - the "self" parameter is always reported, even for bound methods
      - wrapper chains defined by __wrapped__ *not* unwrapped automatically
    """
    try:
        sig = _signature_from_callable(func, follow_wrapper_chains=False, skip_bound_arg=False, sigcls=签名, eval_str=False)
    except Exception as ex:
        raise TypeError('unsupported callable') from ex
    参数 = []
    varargs = None
    varkw = None
    posonlyargs = []
    kwonlyargs = []
    annotations = {}
    defaults = ()
    kwdefaults = {}
    if sig.return_annotation is not sig.empty:
        annotations['return'] = sig.return_annotation
    for param in sig.parameters.values():
        种类 = param.kind
        名字 = param.name
        if 种类 is _POSITIONAL_ONLY:
            posonlyargs.append(名字)
            if param.default is not param.empty:
                defaults += (param.default,)
        elif 种类 is _POSITIONAL_OR_KEYWORD:
            参数.append(名字)
            if param.default is not param.empty:
                defaults += (param.default,)
        elif 种类 is _VAR_POSITIONAL:
            varargs = 名字
        elif 种类 is _KEYWORD_ONLY:
            kwonlyargs.append(名字)
            if param.default is not param.empty:
                kwdefaults[名字] = param.default
        elif 种类 is _VAR_KEYWORD:
            varkw = 名字
        if param.annotation is not param.empty:
            annotations[名字] = param.annotation
    if not kwdefaults:
        kwdefaults = None
    if not defaults:
        defaults = None
    return 完整参数规格(posonlyargs + 参数, varargs, varkw, defaults, kwonlyargs, kwdefaults, annotations)
参数信息 = namedtuple('ArgInfo', 'args varargs keywords locals')

def 取参数值(frame):
    """Get information about arguments passed into a particular frame.

    A tuple of four things is returned: (args, varargs, varkw, locals).
    'args' is a list of the argument names.
    'varargs' and 'varkw' are the names of the * and ** arguments or None.
    'locals' is the locals dictionary of the given frame."""
    参数, varargs, varkw = 取参数(frame.f_code)
    return 参数信息(参数, varargs, varkw, frame.f_locals)

def 格式化注解(annotation, base_module=None, *, quote_annotation_strings=True):
    if not quote_annotation_strings and isinstance(annotation, str):
        return annotation
    if getattr(annotation, '__module__', None) == 'typing':

        def repl(match):
            text = match.group()
            return text.removeprefix('typing.')
        return re.sub('[\\w\\.]+', repl, repr(annotation))
    if isinstance(annotation, types.GenericAlias):
        return str(annotation)
    if isinstance(annotation, type):
        if annotation.__module__ in ('builtins', base_module):
            return annotation.__qualname__
        return annotation.__module__ + '.' + annotation.__qualname__
    if isinstance(annotation, ForwardRef):
        return annotation.__forward_arg__
    return repr(annotation)

def 相对格式化注解(object):
    module = getattr(object, '__module__', None)

    def _formatannotation(annotation):
        return 格式化注解(annotation, module)
    return _formatannotation

def 格式化参数值(args, varargs, varkw, locals, formatarg=str, formatvarargs=lambda name: '*' + name, formatvarkw=lambda name: '**' + name, formatvalue=lambda value: '=' + repr(value)):
    """Format an argument spec from the 4 values returned by getargvalues.

    The first four arguments are (args, varargs, varkw, locals).  The
    next four arguments are the corresponding optional formatting functions
    that are called to turn names and values into strings.  The ninth
    argument is an optional function to format the sequence of arguments."""

    def convert(name, locals=locals, formatarg=formatarg, formatvalue=formatvalue):
        return formatarg(name) + formatvalue(locals[name])
    specs = []
    for i in range(len(args)):
        specs.append(convert(args[i]))
    if varargs:
        specs.append(formatvarargs(varargs) + formatvalue(locals[varargs]))
    if varkw:
        specs.append(formatvarkw(varkw) + formatvalue(locals[varkw]))
    return '(' + ', '.join(specs) + ')'

def _missing_arguments(f_name, argnames, pos, values):
    names = [repr(名字) for 名字 in argnames if 名字 not in values]
    missing = len(names)
    if missing == 1:
        s = names[0]
    elif missing == 2:
        s = '{} and {}'.format(*names)
    else:
        tail = ', {} and {}'.format(*names[-2:])
        del names[-2:]
        s = ', '.join(names) + tail
    raise TypeError('%s() missing %i required %s argument%s: %s' % (f_name, missing, 'positional' if pos else 'keyword-only', '' if missing == 1 else 's', s))

def _too_many(f_name, args, kwonly, varargs, defcount, given, values):
    atleast = len(args) - defcount
    kwonly_given = len([arg for arg in kwonly if arg in values])
    if varargs:
        plural = atleast != 1
        sig = 'at least %d' % (atleast,)
    elif defcount:
        plural = True
        sig = 'from %d to %d' % (atleast, len(args))
    else:
        plural = len(args) != 1
        sig = str(len(args))
    kwonly_sig = ''
    if kwonly_given:
        msg = ' positional argument%s (and %d keyword-only argument%s)'
        kwonly_sig = msg % ('s' if given != 1 else '', kwonly_given, 's' if kwonly_given != 1 else '')
    raise TypeError('%s() takes %s positional argument%s but %d%s %s given' % (f_name, sig, 's' if plural else '', given, kwonly_sig, 'was' if given == 1 and (not kwonly_given) else 'were'))

def 取调用参数(func, /, *positional, **named):
    """Get the mapping of arguments to values.

    A dict is returned, with keys the function argument names (including the
    names of the * and ** arguments, if any), and values the respective bound
    values from 'positional' and 'named'."""
    spec = 取完整参数规格(func)
    参数, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, ann = spec
    f_name = func.__name__
    arg2value = {}
    if 是方法吗(func) and func.__self__ is not None:
        positional = (func.__self__,) + positional
    num_pos = len(positional)
    num_args = len(参数)
    num_defaults = len(defaults) if defaults else 0
    n = min(num_pos, num_args)
    for i in range(n):
        arg2value[参数[i]] = positional[i]
    if varargs:
        arg2value[varargs] = tuple(positional[n:])
    possible_kwargs = set(参数 + kwonlyargs)
    if varkw:
        arg2value[varkw] = {}
    for kw, value in named.items():
        if kw not in possible_kwargs:
            if not varkw:
                raise TypeError('%s() got an unexpected keyword argument %r' % (f_name, kw))
            arg2value[varkw][kw] = value
            continue
        if kw in arg2value:
            raise TypeError('%s() got multiple values for argument %r' % (f_name, kw))
        arg2value[kw] = value
    if num_pos > num_args and (not varargs):
        _too_many(f_name, 参数, kwonlyargs, varargs, num_defaults, num_pos, arg2value)
    if num_pos < num_args:
        req = 参数[:num_args - num_defaults]
        for arg in req:
            if arg not in arg2value:
                _missing_arguments(f_name, req, True, arg2value)
        for i, arg in enumerate(参数[num_args - num_defaults:]):
            if arg not in arg2value:
                arg2value[arg] = defaults[i]
    missing = 0
    for kwarg in kwonlyargs:
        if kwarg not in arg2value:
            if kwonlydefaults and kwarg in kwonlydefaults:
                arg2value[kwarg] = kwonlydefaults[kwarg]
            else:
                missing += 1
    if missing:
        _missing_arguments(f_name, kwonlyargs, False, arg2value)
    return arg2value
闭包变量 = namedtuple('ClosureVars', 'nonlocals globals builtins unbound')

def 取闭包变量(func):
    """
    Get the mapping of free variables to their current values.

    Returns a named tuple of dicts mapping the current nonlocal, global
    and builtin references as seen by the body of the function. A final
    set of unbound names that could not be resolved is also provided.
    """
    if 是方法吗(func):
        func = func.__func__
    if not 是函数吗(func):
        raise TypeError('{!r} is not a Python function'.format(func))
    code = func.__code__
    if func.__closure__ is None:
        nonlocal_vars = {}
    else:
        nonlocal_vars = {var: cell.cell_contents for var, cell in zip(code.co_freevars, func.__closure__)}
    global_ns = func.__globals__
    builtin_ns = global_ns.get('__builtins__', builtins.__dict__)
    if 是模块吗(builtin_ns):
        builtin_ns = builtin_ns.__dict__
    global_vars = {}
    builtin_vars = {}
    unbound_names = set()
    global_names = set()
    for instruction in dis.get_instructions(code):
        opname = instruction.opname
        名字 = instruction.argval
        if opname == 'LOAD_ATTR':
            unbound_names.add(名字)
        elif opname == 'LOAD_GLOBAL':
            global_names.add(名字)
    for 名字 in global_names:
        try:
            global_vars[名字] = global_ns[名字]
        except KeyError:
            try:
                builtin_vars[名字] = builtin_ns[名字]
            except KeyError:
                unbound_names.add(名字)
    return 闭包变量(nonlocal_vars, global_vars, builtin_vars, unbound_names)
_Traceback = namedtuple('_Traceback', 'filename lineno function code_context index')

class 回溯信息(_Traceback):

    def __new__(cls, filename, lineno, function, code_context, index, *, positions=None):
        instance = super().__new__(cls, filename, lineno, function, code_context, index)
        instance.positions = positions
        return instance

    def __repr__(self):
        return 'Traceback(filename={!r}, lineno={!r}, function={!r}, code_context={!r}, index={!r}, positions={!r})'.format(self.filename, self.lineno, self.function, self.code_context, self.index, self.positions)

def _get_code_position_from_tb(tb):
    code, instruction_index = (tb.tb_frame.f_code, tb.tb_lasti)
    return _get_code_position(code, instruction_index)

def _get_code_position(code, instruction_index):
    if instruction_index < 0:
        return (None, None, None, None)
    positions_gen = code.co_positions()
    return next(itertools.islice(positions_gen, instruction_index // 2, None))

def 取帧信息(frame, context=1):
    """Get information about a frame or traceback object.

    A tuple of five things is returned: the filename, the line number of
    the current line, the function name, a list of lines of context from
    the source code, and the index of the current line within that list.
    The optional second argument specifies the number of lines of context
    to return, which are centered around the current line."""
    if 是回溯吗(frame):
        positions = _get_code_position_from_tb(frame)
        lineno = frame.tb_lineno
        frame = frame.tb_frame
    else:
        lineno = frame.f_lineno
        positions = _get_code_position(frame.f_code, frame.f_lasti)
    if positions[0] is None:
        frame, *positions = (frame, lineno, *positions[1:])
    else:
        frame, *positions = (frame, *positions)
    lineno = positions[0]
    if not 是帧吗(frame):
        raise TypeError('{!r} is not a frame or traceback object'.format(frame))
    filename = 取源文件(frame) or 取文件(frame)
    if context > 0:
        start = lineno - 1 - context // 2
        try:
            lines, lnum = 找源码(frame)
        except OSError:
            lines = index = None
        else:
            start = max(0, min(start, len(lines) - context))
            lines = lines[start:start + context]
            index = lineno - 1 - start
    else:
        lines = index = None
    return 回溯信息(filename, lineno, frame.f_code.co_name, lines, index, positions=dis.Positions(*positions))

def 取行号(frame):
    """Get the line number from a frame object, allowing for optimization."""
    return frame.f_lineno
_FrameInfo = namedtuple('_FrameInfo', ('frame',) + 回溯信息._fields)

class 帧信息(_FrameInfo):

    def __new__(cls, frame, filename, lineno, function, code_context, index, *, positions=None):
        instance = super().__new__(cls, frame, filename, lineno, function, code_context, index)
        instance.positions = positions
        return instance

    def __repr__(self):
        return 'FrameInfo(frame={!r}, filename={!r}, lineno={!r}, function={!r}, code_context={!r}, index={!r}, positions={!r})'.format(self.frame, self.filename, self.lineno, self.function, self.code_context, self.index, self.positions)

def 取外层帧(frame, context=1):
    """Get a list of records for a frame and all higher (calling) frames.

    Each record contains a frame object, filename, line number, function
    name, a list of lines of context, and index within the context."""
    framelist = []
    while frame:
        traceback_info = 取帧信息(frame, context)
        frameinfo = (frame,) + traceback_info
        framelist.append(帧信息(*frameinfo, positions=traceback_info.positions))
        frame = frame.f_back
    return framelist

def 取内层帧(tb, context=1):
    """Get a list of records for a traceback's frame and all lower frames.

    Each record contains a frame object, filename, line number, function
    name, a list of lines of context, and index within the context."""
    framelist = []
    while tb:
        traceback_info = 取帧信息(tb, context)
        frameinfo = (tb.tb_frame,) + traceback_info
        framelist.append(帧信息(*frameinfo, positions=traceback_info.positions))
        tb = tb.tb_next
    return framelist

def 当前帧():
    """Return the frame of the caller or None if this is not possible."""
    return sys._getframe(1) if hasattr(sys, '_getframe') else None

def 调用栈(context=1):
    """Return a list of records for the stack above the caller's frame."""
    return 取外层帧(sys._getframe(1), context)

def 回溯帧(context=1):
    """Return a list of records for the stack below the current exception."""
    exc = sys.exception()
    tb = None if exc is None else exc.__traceback__
    return 取内层帧(tb, context)
_sentinel = object()
_static_getmro = type.__dict__['__mro__'].__get__
_get_dunder_dict_of_class = type.__dict__['__dict__'].__get__

def _check_instance(obj, attr):
    instance_dict = {}
    try:
        instance_dict = object.__getattribute__(obj, '__dict__')
    except AttributeError:
        pass
    return dict.get(instance_dict, attr, _sentinel)

def _check_class(klass, attr):
    for entry in _static_getmro(klass):
        if _shadowed_dict(type(entry)) is _sentinel and attr in entry.__dict__:
            return entry.__dict__[attr]
    return _sentinel

@functools.lru_cache()
def _shadowed_dict_from_weakref_mro_tuple(*weakref_mro):
    for weakref_entry in weakref_mro:
        entry = weakref_entry()
        dunder_dict = _get_dunder_dict_of_class(entry)
        if '__dict__' in dunder_dict:
            class_dict = dunder_dict['__dict__']
            if not (type(class_dict) is types.GetSetDescriptorType and class_dict.__name__ == '__dict__' and (class_dict.__objclass__ is entry)):
                return class_dict
    return _sentinel

def _shadowed_dict(klass):
    return _shadowed_dict_from_weakref_mro_tuple(*[make_weakref(entry) for entry in _static_getmro(klass)])

def 静态取属性(obj, attr, default=_sentinel):
    """Retrieve attributes without triggering dynamic lookup via the
       descriptor protocol,  __getattr__ or __getattribute__.

       Note: this function may not be able to retrieve all attributes
       that getattr can fetch (like dynamically created attributes)
       and may find attributes that getattr can't (like descriptors
       that raise AttributeError). It can also return descriptor objects
       instead of instance members in some cases. See the
       documentation for details.
    """
    instance_result = _sentinel
    objtype = type(obj)
    if type not in _static_getmro(objtype):
        klass = objtype
        dict_attr = _shadowed_dict(klass)
        if dict_attr is _sentinel or type(dict_attr) is types.MemberDescriptorType:
            instance_result = _check_instance(obj, attr)
    else:
        klass = obj
    klass_result = _check_class(klass, attr)
    if instance_result is not _sentinel and klass_result is not _sentinel:
        if _check_class(type(klass_result), '__get__') is not _sentinel and (_check_class(type(klass_result), '__set__') is not _sentinel or _check_class(type(klass_result), '__delete__') is not _sentinel):
            return klass_result
    if instance_result is not _sentinel:
        return instance_result
    if klass_result is not _sentinel:
        return klass_result
    if obj is klass:
        for entry in _static_getmro(type(klass)):
            if _shadowed_dict(type(entry)) is _sentinel and attr in entry.__dict__:
                return entry.__dict__[attr]
    if default is not _sentinel:
        return default
    raise AttributeError(attr)
生成器已创建 = 'GEN_CREATED'
生成器运行中 = 'GEN_RUNNING'
生成器已挂起 = 'GEN_SUSPENDED'
生成器已关闭 = 'GEN_CLOSED'

def 取生成器状态(generator):
    """Get current state of a generator-iterator.

    Possible states are:
      GEN_CREATED: Waiting to start execution.
      GEN_RUNNING: Currently being executed by the interpreter.
      GEN_SUSPENDED: Currently suspended at a yield expression.
      GEN_CLOSED: Execution has completed.
    """
    if generator.gi_running:
        return 生成器运行中
    if generator.gi_suspended:
        return 生成器已挂起
    if generator.gi_frame is None:
        return 生成器已关闭
    return 生成器已创建

def 取生成器局部变量(generator):
    """
    Get the mapping of generator local variables to their current values.

    A dict is returned, with the keys the local variable names and values the
    bound values."""
    if not 是生成器吗(generator):
        raise TypeError('{!r} is not a Python generator'.format(generator))
    frame = getattr(generator, 'gi_frame', None)
    if frame is not None:
        return generator.gi_frame.f_locals
    else:
        return {}
协程已创建 = 'CORO_CREATED'
协程运行中 = 'CORO_RUNNING'
协程已挂起 = 'CORO_SUSPENDED'
协程已关闭 = 'CORO_CLOSED'

def 取协程状态(coroutine):
    """Get current state of a coroutine object.

    Possible states are:
      CORO_CREATED: Waiting to start execution.
      CORO_RUNNING: Currently being executed by the interpreter.
      CORO_SUSPENDED: Currently suspended at an await expression.
      CORO_CLOSED: Execution has completed.
    """
    if coroutine.cr_running:
        return 协程运行中
    if coroutine.cr_suspended:
        return 协程已挂起
    if coroutine.cr_frame is None:
        return 协程已关闭
    return 协程已创建

def 取协程局部变量(coroutine):
    """
    Get the mapping of coroutine local variables to their current values.

    A dict is returned, with the keys the local variable names and values the
    bound values."""
    frame = getattr(coroutine, 'cr_frame', None)
    if frame is not None:
        return frame.f_locals
    else:
        return {}
异步生成器已创建 = 'AGEN_CREATED'
异步生成器运行中 = 'AGEN_RUNNING'
异步生成器已挂起 = 'AGEN_SUSPENDED'
异步生成器已关闭 = 'AGEN_CLOSED'

def 取异步生成器状态(agen):
    """Get current state of an asynchronous generator object.

    Possible states are:
      AGEN_CREATED: Waiting to start execution.
      AGEN_RUNNING: Currently being executed by the interpreter.
      AGEN_SUSPENDED: Currently suspended at a yield expression.
      AGEN_CLOSED: Execution has completed.
    """
    if agen.ag_running:
        return 异步生成器运行中
    if agen.ag_suspended:
        return 异步生成器已挂起
    if agen.ag_frame is None:
        return 异步生成器已关闭
    return 异步生成器已创建

def 取异步生成器局部变量(agen):
    """
    Get the mapping of asynchronous generator local variables to their current
    values.

    A dict is returned, with the keys the local variable names and values the
    bound values."""
    if not 是异步生成器吗(agen):
        raise TypeError(f'{agen!r} is not a Python async generator')
    frame = getattr(agen, 'ag_frame', None)
    if frame is not None:
        return agen.ag_frame.f_locals
    else:
        return {}
_NonUserDefinedCallables = (types.WrapperDescriptorType, types.MethodWrapperType, types.ClassMethodDescriptorType, types.BuiltinFunctionType)

def _signature_get_user_defined_method(cls, method_name, *, follow_wrapper_chains=True):
    """Private helper. Checks if ``cls`` has an attribute
    named ``method_name`` and returns it only if it is a
    pure python function.
    """
    if method_name == '__new__':
        meth = getattr(cls, method_name, None)
    else:
        meth = 静态取属性(cls, method_name, None)
    if meth is None:
        return None
    unwrapped_meth = None
    if follow_wrapper_chains:
        unwrapped_meth = 解开包装(meth, stop=lambda m: hasattr(m, '__signature__') or _signature_is_builtin(m))
    if isinstance(meth, _NonUserDefinedCallables) or isinstance(unwrapped_meth, _NonUserDefinedCallables):
        return None
    if method_name != '__new__':
        meth = _descriptor_get(meth, cls)
    return meth

def _signature_get_partial(wrapped_sig, partial, extra_args=()):
    """Private helper to calculate how 'wrapped_sig' signature will
    look like after applying a 'functools.partial' object (or alike)
    on it.
    """
    old_params = wrapped_sig.parameters
    new_params = OrderedDict(old_params.items())
    partial_args = partial.args or ()
    partial_keywords = partial.keywords or {}
    if extra_args:
        partial_args = extra_args + partial_args
    try:
        ba = wrapped_sig.bind_partial(*partial_args, **partial_keywords)
    except TypeError as ex:
        msg = 'partial object {!r} has incorrect arguments'.format(partial)
        raise ValueError(msg) from ex
    transform_to_kwonly = False
    for param_name, param in old_params.items():
        try:
            arg_value = ba.arguments[param_name]
        except KeyError:
            pass
        else:
            if param.kind is _POSITIONAL_ONLY:
                if arg_value is functools.Placeholder:
                    new_params[param_name] = param.replace(default=_empty)
                else:
                    new_params.pop(param_name)
                continue
            if param.kind is _POSITIONAL_OR_KEYWORD:
                if param_name in partial_keywords:
                    transform_to_kwonly = True
                    new_params[param_name] = param.replace(default=arg_value)
                else:
                    if arg_value is functools.Placeholder:
                        new_param = param.replace(kind=_POSITIONAL_ONLY, default=_empty)
                        new_params[param_name] = new_param
                    else:
                        new_params.pop(param_name)
                    continue
            if param.kind is _KEYWORD_ONLY:
                new_params[param_name] = param.replace(default=arg_value)
        if transform_to_kwonly:
            assert param.kind is not _POSITIONAL_ONLY
            if param.kind is _POSITIONAL_OR_KEYWORD:
                new_param = new_params[param_name].replace(kind=_KEYWORD_ONLY)
                new_params[param_name] = new_param
                new_params.move_to_end(param_name)
            elif param.kind in (_KEYWORD_ONLY, _VAR_KEYWORD):
                new_params.move_to_end(param_name)
            elif param.kind is _VAR_POSITIONAL:
                new_params.pop(param.name)
    return wrapped_sig.replace(parameters=new_params.values())

def _signature_bound_method(sig):
    """Private helper to transform signatures for unbound
    functions to bound methods.
    """
    params = tuple(sig.parameters.values())
    if not params or params[0].kind in (_VAR_KEYWORD, _KEYWORD_ONLY):
        raise ValueError('invalid method signature')
    种类 = params[0].kind
    if 种类 in (_POSITIONAL_OR_KEYWORD, _POSITIONAL_ONLY):
        params = params[1:]
    elif 种类 is not _VAR_POSITIONAL:
        raise ValueError('invalid argument type')
    return sig.replace(parameters=params)

def _signature_is_builtin(obj):
    """Private helper to test if `obj` is a callable that might
    support Argument Clinic's __text_signature__ protocol.
    """
    return 是内置函数吗(obj) or ismethoddescriptor(obj) or isinstance(obj, _NonUserDefinedCallables) or (obj is type) or (obj is object)

def _signature_is_functionlike(obj):
    """Private helper to test if `obj` is a duck type of FunctionType.
    A good example of such objects are functions compiled with
    Cython, which have all attributes that a pure Python function
    would have, but have their code statically compiled.
    """
    if not callable(obj) or 是类吗(obj):
        return False
    名字 = getattr(obj, '__name__', None)
    code = getattr(obj, '__code__', None)
    defaults = getattr(obj, '__defaults__', _void)
    kwdefaults = getattr(obj, '__kwdefaults__', _void)
    return isinstance(code, types.CodeType) and isinstance(名字, str) and (defaults is None or isinstance(defaults, tuple)) and (kwdefaults is None or isinstance(kwdefaults, dict))

def _signature_strip_non_python_syntax(signature):
    """
    Private helper function. Takes a signature in Argument Clinic's
    extended signature format.

    Returns a tuple of two things:
      * that signature re-rendered in standard Python syntax, and
      * the index of the "self" parameter (generally 0), or None if
        the function does not have a "self" parameter.
    """
    if not signature:
        return (signature, None)
    self_parameter = None
    lines = [l.encode('ascii') for l in signature.split('\n') if l]
    generator = iter(lines).__next__
    token_stream = tokenize.tokenize(generator)
    text = []
    add = text.append
    current_parameter = 0
    OP = token.OP
    ERRORTOKEN = token.ERRORTOKEN
    t = next(token_stream)
    assert t.type == tokenize.ENCODING
    for t in token_stream:
        type, string = (t.type, t.string)
        if type == OP:
            if string == ',':
                current_parameter += 1
        if type == OP and string == '$':
            assert self_parameter is None
            self_parameter = current_parameter
            continue
        add(string)
        if string == ',':
            add(' ')
    clean_signature = ''.join(text).strip().replace('\n', '')
    return (clean_signature, self_parameter)

def _signature_fromstr(cls, obj, s, skip_bound_arg=True):
    """Private helper to parse content of '__text_signature__'
    and return a Signature based on it.
    """
    形参 = cls._parameter_cls
    clean_signature, self_parameter = _signature_strip_non_python_syntax(s)
    program = 'def foo' + clean_signature + ': pass'
    try:
        module = ast.parse(program)
    except SyntaxError:
        module = None
    if not isinstance(module, ast.Module):
        raise ValueError('{!r} builtin has invalid signature'.format(obj))
    f = module.body[0]
    参数表 = []
    empty = 形参.empty
    module = None
    module_dict = {}
    module_name = getattr(obj, '__module__', None)
    if not module_name:
        objclass = getattr(obj, '__objclass__', None)
        module_name = getattr(objclass, '__module__', None)
    if module_name:
        module = sys.modules.get(module_name, None)
        if module:
            module_dict = module.__dict__
    sys_module_dict = sys.modules.copy()

    def parse_name(node):
        assert isinstance(node, ast.arg)
        if node.annotation is not None:
            raise ValueError('Annotations are not currently supported')
        return node.arg

    def wrap_value(s):
        try:
            value = eval(s, module_dict)
        except NameError:
            try:
                value = eval(s, sys_module_dict)
            except NameError:
                raise ValueError
        if isinstance(value, (str, int, float, bytes, bool, type(None))):
            return ast.Constant(value)
        raise ValueError

    class RewriteSymbolics(ast.NodeTransformer):

        def visit_Attribute(self, node):
            a = []
            n = node
            while isinstance(n, ast.Attribute):
                a.append(n.attr)
                n = n.value
            if not isinstance(n, ast.Name):
                raise ValueError
            a.append(n.id)
            value = '.'.join(reversed(a))
            return wrap_value(value)

        def visit_Name(self, node):
            if not isinstance(node.ctx, ast.Load):
                raise ValueError()
            return wrap_value(node.id)

        def visit_BinOp(self, node):
            left = self.visit(node.left)
            right = self.visit(node.right)
            if not isinstance(left, ast.Constant) or not isinstance(right, ast.Constant):
                raise ValueError
            if isinstance(node.op, ast.Add):
                return ast.Constant(left.value + right.value)
            elif isinstance(node.op, ast.Sub):
                return ast.Constant(left.value - right.value)
            elif isinstance(node.op, ast.BitOr):
                return ast.Constant(left.value | right.value)
            raise ValueError

    def p(name_node, default_node, default=empty):
        名字 = parse_name(name_node)
        if default_node and default_node is not _empty:
            try:
                default_node = RewriteSymbolics().visit(default_node)
                default = ast.literal_eval(default_node)
            except ValueError:
                raise ValueError('{!r} builtin has invalid signature'.format(obj)) from None
        参数表.append(形参(名字, 种类, default=default, annotation=empty))
    total_non_kw_args = len(f.args.posonlyargs) + len(f.args.args)
    required_non_kw_args = total_non_kw_args - len(f.args.defaults)
    defaults = itertools.chain(itertools.repeat(None, required_non_kw_args), f.args.defaults)
    种类 = 形参.POSITIONAL_ONLY
    for 名字, 默认值 in zip(f.args.posonlyargs, defaults):
        p(名字, 默认值)
    种类 = 形参.POSITIONAL_OR_KEYWORD
    for 名字, 默认值 in zip(f.args.args, defaults):
        p(名字, 默认值)
    if f.args.vararg:
        种类 = 形参.VAR_POSITIONAL
        p(f.args.vararg, empty)
    种类 = 形参.KEYWORD_ONLY
    for 名字, 默认值 in zip(f.args.kwonlyargs, f.args.kw_defaults):
        p(名字, 默认值)
    if f.args.kwarg:
        种类 = 形参.VAR_KEYWORD
        p(f.args.kwarg, empty)
    if self_parameter is not None:
        assert 参数表
        _self = getattr(obj, '__self__', None)
        self_isbound = _self is not None
        self_ismodule = 是模块吗(_self)
        if self_isbound and (self_ismodule or skip_bound_arg):
            参数表.pop(0)
        else:
            p = 参数表[0].replace(kind=形参.POSITIONAL_ONLY)
            参数表[0] = p
    return cls(参数表, return_annotation=cls.empty)

def _signature_from_builtin(cls, func, skip_bound_arg=True):
    """Private helper function to get signature for
    builtin callables.
    """
    if not _signature_is_builtin(func):
        raise TypeError('{!r} is not a Python builtin function'.format(func))
    s = getattr(func, '__text_signature__', None)
    if not s:
        raise ValueError('no signature found for builtin {!r}'.format(func))
    return _signature_fromstr(cls, func, s, skip_bound_arg)

def _signature_from_function(cls, func, skip_bound_arg=True, globals=None, locals=None, eval_str=False, *, annotation_format=Format.VALUE):
    """Private helper: constructs Signature for the given python function."""
    is_duck_function = False
    if not 是函数吗(func):
        if _signature_is_functionlike(func):
            is_duck_function = True
        else:
            raise TypeError('{!r} is not a Python function'.format(func))
    s = getattr(func, '__text_signature__', None)
    if s:
        return _signature_fromstr(cls, func, s, skip_bound_arg)
    形参 = cls._parameter_cls
    func_code = func.__code__
    pos_count = func_code.co_argcount
    arg_names = func_code.co_varnames
    posonly_count = func_code.co_posonlyargcount
    positional = arg_names[:pos_count]
    keyword_only_count = func_code.co_kwonlyargcount
    keyword_only = arg_names[pos_count:pos_count + keyword_only_count]
    annotations = get_annotations(func, globals=globals, locals=locals, eval_str=eval_str, format=annotation_format)
    defaults = func.__defaults__
    kwdefaults = func.__kwdefaults__
    if defaults:
        pos_default_count = len(defaults)
    else:
        pos_default_count = 0
    参数表 = []
    non_default_count = pos_count - pos_default_count
    posonly_left = posonly_count
    for 名字 in positional[:non_default_count]:
        种类 = _POSITIONAL_ONLY if posonly_left else _POSITIONAL_OR_KEYWORD
        注解 = annotations.get(名字, _empty)
        参数表.append(形参(名字, annotation=注解, kind=种类))
        if posonly_left:
            posonly_left -= 1
    for offset, 名字 in enumerate(positional[non_default_count:]):
        种类 = _POSITIONAL_ONLY if posonly_left else _POSITIONAL_OR_KEYWORD
        注解 = annotations.get(名字, _empty)
        参数表.append(形参(名字, annotation=注解, kind=种类, default=defaults[offset]))
        if posonly_left:
            posonly_left -= 1
    if func_code.co_flags & CO_VARARGS:
        名字 = arg_names[pos_count + keyword_only_count]
        注解 = annotations.get(名字, _empty)
        参数表.append(形参(名字, annotation=注解, kind=_VAR_POSITIONAL))
    for 名字 in keyword_only:
        默认值 = _empty
        if kwdefaults is not None:
            默认值 = kwdefaults.get(名字, _empty)
        注解 = annotations.get(名字, _empty)
        参数表.append(形参(名字, annotation=注解, kind=_KEYWORD_ONLY, default=默认值))
    if func_code.co_flags & CO_VARKEYWORDS:
        index = pos_count + keyword_only_count
        if func_code.co_flags & CO_VARARGS:
            index += 1
        名字 = arg_names[index]
        注解 = annotations.get(名字, _empty)
        参数表.append(形参(名字, annotation=注解, kind=_VAR_KEYWORD))
    return cls(参数表, return_annotation=annotations.get('return', _empty), __validate_parameters__=is_duck_function)

def _descriptor_get(descriptor, obj):
    if 是类吗(descriptor):
        return descriptor
    get = getattr(type(descriptor), '__get__', _sentinel)
    if get is _sentinel:
        return descriptor
    return get(descriptor, obj, type(obj))

def _signature_from_callable(obj, *, follow_wrapper_chains=True, skip_bound_arg=True, globals=None, locals=None, eval_str=False, sigcls, annotation_format=Format.VALUE):
    """Private helper function to get signature for arbitrary
    callable objects.
    """
    _get_signature_of = functools.partial(_signature_from_callable, follow_wrapper_chains=follow_wrapper_chains, skip_bound_arg=skip_bound_arg, globals=globals, locals=locals, sigcls=sigcls, eval_str=eval_str, annotation_format=annotation_format)
    if not callable(obj):
        raise TypeError('{!r} is not a callable object'.format(obj))
    if isinstance(obj, types.MethodType):
        sig = _get_signature_of(obj.__func__)
        if skip_bound_arg:
            return _signature_bound_method(sig)
        else:
            return sig
    if follow_wrapper_chains:
        obj = 解开包装(obj, stop=lambda f: hasattr(f, '__signature__') or isinstance(f, types.MethodType))
        if isinstance(obj, types.MethodType):
            return _get_signature_of(obj)
    try:
        sig = obj.__signature__
    except AttributeError:
        pass
    else:
        if sig is not None:
            if not isinstance(sig, 签名):
                raise TypeError('unexpected object {!r} in __signature__ attribute'.format(sig))
            return sig
    try:
        partialmethod = obj.__partialmethod__
    except AttributeError:
        pass
    else:
        if isinstance(partialmethod, functools.partialmethod):
            wrapped_sig = _get_signature_of(partialmethod.func)
            sig = _signature_get_partial(wrapped_sig, partialmethod, (None,))
            first_wrapped_param = tuple(wrapped_sig.parameters.values())[0]
            if first_wrapped_param.kind is 形参.VAR_POSITIONAL:
                return sig
            else:
                sig_params = tuple(sig.parameters.values())
                assert not sig_params or first_wrapped_param is not sig_params[0]
                if partialmethod.args.count(functools.Placeholder):
                    first_wrapped_param = first_wrapped_param.replace(kind=形参.POSITIONAL_ONLY)
                new_params = (first_wrapped_param,) + sig_params
                return sig.replace(parameters=new_params)
    if isinstance(obj, functools.partial):
        wrapped_sig = _get_signature_of(obj.func)
        return _signature_get_partial(wrapped_sig, obj)
    if 是函数吗(obj) or _signature_is_functionlike(obj):
        return _signature_from_function(sigcls, obj, skip_bound_arg=skip_bound_arg, globals=globals, locals=locals, eval_str=eval_str, annotation_format=annotation_format)
    if _signature_is_builtin(obj):
        return _signature_from_builtin(sigcls, obj, skip_bound_arg=skip_bound_arg)
    if isinstance(obj, type):
        call = _signature_get_user_defined_method(type(obj), '__call__', follow_wrapper_chains=follow_wrapper_chains)
        if call is not None:
            return _get_signature_of(call)
        new = _signature_get_user_defined_method(obj, '__new__', follow_wrapper_chains=follow_wrapper_chains)
        init = _signature_get_user_defined_method(obj, '__init__', follow_wrapper_chains=follow_wrapper_chains)
        for base in obj.__mro__:
            if new is not None and '__new__' in base.__dict__:
                sig = _get_signature_of(new)
                if skip_bound_arg:
                    sig = _signature_bound_method(sig)
                return sig
            elif init is not None and '__init__' in base.__dict__:
                return _get_signature_of(init)
        for base in obj.__mro__[:-1]:
            try:
                text_sig = base.__text_signature__
            except AttributeError:
                pass
            else:
                if text_sig:
                    return _signature_fromstr(sigcls, base, text_sig)
        if type not in obj.__mro__:
            obj_init = obj.__init__
            obj_new = obj.__new__
            if follow_wrapper_chains:
                obj_init = 解开包装(obj_init)
                obj_new = 解开包装(obj_new)
            if obj_init is object.__init__ and obj_new is object.__new__:
                return sigcls.from_callable(object)
            else:
                raise ValueError('no signature found for builtin type {!r}'.format(obj))
    else:
        call = 静态取属性(type(obj), '__call__', None)
        if call is not None:
            try:
                text_sig = obj.__text_signature__
            except AttributeError:
                pass
            else:
                if text_sig:
                    return _signature_fromstr(sigcls, obj, text_sig)
            call = _descriptor_get(call, obj)
            return _get_signature_of(call)
    raise ValueError('callable {!r} is not supported by signature'.format(obj))

class _void:
    """A private marker - used in Parameter & Signature."""

class _empty:
    """Marker object for Signature.empty and Parameter.empty."""

class _ParameterKind(enum.IntEnum):
    POSITIONAL_ONLY = 'positional-only'
    POSITIONAL_OR_KEYWORD = 'positional or keyword'
    VAR_POSITIONAL = 'variadic positional'
    KEYWORD_ONLY = 'keyword-only'
    VAR_KEYWORD = 'variadic keyword'

    def __new__(cls, description):
        value = len(cls.__members__)
        member = int.__new__(cls, value)
        member._value_ = value
        member.description = description
        return member

    def __str__(self):
        return self.名字
_装类转发(_ParameterKind, {}, {'name': '名字'})
_POSITIONAL_ONLY = _ParameterKind.POSITIONAL_ONLY
_POSITIONAL_OR_KEYWORD = _ParameterKind.POSITIONAL_OR_KEYWORD
_VAR_POSITIONAL = _ParameterKind.VAR_POSITIONAL
_KEYWORD_ONLY = _ParameterKind.KEYWORD_ONLY
_VAR_KEYWORD = _ParameterKind.VAR_KEYWORD

class 形参:
    """Represents a parameter in a function signature.

    Has the following public attributes:

    * name : str
        The name of the parameter as a string.
    * default : object
        The default value for the parameter if specified.  If the
        parameter has no default value, this attribute is set to
        `Parameter.empty`.
    * annotation
        The annotation for the parameter if specified.  If the
        parameter has no annotation, this attribute is set to
        `Parameter.empty`.
    * kind
        Describes how argument values are bound to the parameter.
        Possible values: `Parameter.POSITIONAL_ONLY`,
        `Parameter.POSITIONAL_OR_KEYWORD`, `Parameter.VAR_POSITIONAL`,
        `Parameter.KEYWORD_ONLY`, `Parameter.VAR_KEYWORD`.
        Every value has a `description` attribute describing meaning.
    """
    __slots__ = ('_name', '_kind', '_default', '_annotation')
    POSITIONAL_ONLY = _POSITIONAL_ONLY
    POSITIONAL_OR_KEYWORD = _POSITIONAL_OR_KEYWORD
    VAR_POSITIONAL = _VAR_POSITIONAL
    KEYWORD_ONLY = _KEYWORD_ONLY
    VAR_KEYWORD = _VAR_KEYWORD
    empty = _empty

    def __init__(self, name, kind, *, default=_empty, annotation=_empty):
        try:
            self._kind = _ParameterKind(kind)
        except ValueError:
            raise ValueError(f'value {kind!r} is not a valid Parameter.kind')
        if default is not _empty:
            if self._kind in (_VAR_POSITIONAL, _VAR_KEYWORD):
                msg = '{} parameters cannot have default values'
                msg = msg.format(self._kind.description)
                raise ValueError(msg)
        self._default = default
        self._annotation = annotation
        if name is _empty:
            raise ValueError('name is a required attribute for Parameter')
        if not isinstance(name, str):
            msg = 'name must be a str, not a {}'.format(type(name).__name__)
            raise TypeError(msg)
        if name[0] == '.' and name[1:].isdigit():
            if self._kind != _POSITIONAL_OR_KEYWORD:
                msg = 'implicit arguments must be passed as positional or keyword arguments, not {}'
                msg = msg.format(self._kind.description)
                raise ValueError(msg)
            self._kind = _POSITIONAL_ONLY
            name = 'implicit{}'.format(name[1:])
        elif name == '.format':
            name = 'format'
        is_keyword = iskeyword(name) and self._kind is not _POSITIONAL_ONLY
        if is_keyword or not name.isidentifier():
            raise ValueError('{!r} is not a valid parameter name'.format(name))
        self._name = name

    def __reduce__(self):
        return (type(self), (self._name, self._kind), {'_default': self._default, '_annotation': self._annotation})

    def __setstate__(self, state):
        self._default = state['_default']
        self._annotation = state['_annotation']

    @property
    def 名字(self):
        return self._name

    @property
    def 默认值(self):
        return self._default

    @property
    def 注解(self):
        return self._annotation

    @property
    def 种类(self):
        return self._kind

    def replace(self, *, name=_void, kind=_void, annotation=_void, default=_void):
        """Creates a customized copy of the Parameter."""
        if name is _void:
            name = self._name
        if kind is _void:
            kind = self._kind
        if annotation is _void:
            annotation = self._annotation
        if default is _void:
            default = self._default
        return type(self)(name, kind, default=default, annotation=annotation)

    def __str__(self):
        return self._format()

    def _format(self, *, quote_annotation_strings=True):
        种类 = self.种类
        formatted = self._name
        if self._annotation is not _empty:
            注解 = 格式化注解(self._annotation, quote_annotation_strings=quote_annotation_strings)
            formatted = '{}: {}'.format(formatted, 注解)
        if self._default is not _empty:
            if self._annotation is not _empty:
                formatted = '{} = {}'.format(formatted, repr(self._default))
            else:
                formatted = '{}={}'.format(formatted, repr(self._default))
        if 种类 == _VAR_POSITIONAL:
            formatted = '*' + formatted
        elif 种类 == _VAR_KEYWORD:
            formatted = '**' + formatted
        return formatted
    __replace__ = replace

    def __repr__(self):
        return '<{} "{}">'.format(self.__class__.__name__, self)

    def __hash__(self):
        return hash((self._name, self._kind, self._annotation, self._default))

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, 形参):
            return NotImplemented
        return self._name == other._name and self._kind == other._kind and (self._default == other._default) and (self._annotation == other._annotation)
_装类转发(形参, {'annotation': '注解', 'default': '默认值', 'kind': '种类', 'name': '名字'}, {'annotation': '注解', 'default': '默认值', 'kind': '种类', 'name': '名字'})

class 绑定参数:
    """Result of `Signature.bind` call.  Holds the mapping of arguments
    to the function's parameters.

    Has the following public attributes:

    * arguments : dict
        An ordered mutable mapping of parameters' names to arguments' values.
        Does not contain arguments' default values.
    * signature : Signature
        The Signature object that created this instance.
    * args : tuple
        Tuple of positional arguments values.
    * kwargs : dict
        Dict of keyword arguments values.
    """
    __slots__ = ('arguments', '_signature', '__weakref__')

    def __init__(self, signature, arguments):
        self.arguments = arguments
        self._signature = signature

    @property
    def 取签名(self):
        return self._signature

    @property
    def 参数(self):
        参数 = []
        for param_name, param in self._signature.parameters.items():
            if param.kind in (_VAR_KEYWORD, _KEYWORD_ONLY):
                break
            try:
                arg = self.arguments[param_name]
            except KeyError:
                break
            else:
                if param.kind == _VAR_POSITIONAL:
                    参数.extend(arg)
                else:
                    参数.append(arg)
        return tuple(参数)

    @property
    def 关键字参数(self):
        关键字参数 = {}
        kwargs_started = False
        for param_name, param in self._signature.parameters.items():
            if not kwargs_started:
                if param.kind in (_VAR_KEYWORD, _KEYWORD_ONLY):
                    kwargs_started = True
                elif param_name not in self.arguments:
                    kwargs_started = True
                    continue
            if not kwargs_started:
                continue
            try:
                arg = self.arguments[param_name]
            except KeyError:
                pass
            else:
                if param.kind == _VAR_KEYWORD:
                    关键字参数.update(arg)
                else:
                    关键字参数[param_name] = arg
        return 关键字参数

    def 应用默认值(self):
        """Set default values for missing arguments.

        For variable-positional arguments (*args) the default is an
        empty tuple.

        For variable-keyword arguments (**kwargs) the default is an
        empty dict.
        """
        arguments = self.arguments
        new_arguments = []
        for 名字, param in self._signature.parameters.items():
            try:
                new_arguments.append((名字, arguments[名字]))
            except KeyError:
                if param.default is not _empty:
                    val = param.default
                elif param.kind is _VAR_POSITIONAL:
                    val = ()
                elif param.kind is _VAR_KEYWORD:
                    val = {}
                else:
                    continue
                new_arguments.append((名字, val))
        self.arguments = dict(new_arguments)

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, 绑定参数):
            return NotImplemented
        return self.取签名 == other.signature and self.arguments == other.arguments

    def __setstate__(self, state):
        self._signature = state['_signature']
        self.arguments = state['arguments']

    def __getstate__(self):
        return {'_signature': self._signature, 'arguments': self.arguments}

    def __repr__(self):
        参数 = []
        for arg, value in self.arguments.items():
            参数.append('{}={!r}'.format(arg, value))
        return '<{} ({})>'.format(self.__class__.__name__, ', '.join(参数))
_装类转发(绑定参数, {'apply_defaults': '应用默认值', 'args': '参数', 'kwargs': '关键字参数', 'signature': '取签名'}, {'apply_defaults': '应用默认值', 'args': '参数', 'kwargs': '关键字参数', 'signature': '取签名'})

class 签名:
    """A Signature object represents the overall signature of a function.
    It stores a Parameter object for each parameter accepted by the
    function, as well as information specific to the function itself.

    A Signature object has the following public attributes and methods:

    * parameters : OrderedDict
        An ordered mapping of parameters' names to the corresponding
        Parameter objects (keyword-only arguments are in the same order
        as listed in `code.co_varnames`).
    * return_annotation : object
        The annotation for the return type of the function if specified.
        If the function has no annotation for its return type, this
        attribute is set to `Signature.empty`.
    * bind(*args, **kwargs) -> BoundArguments
        Creates a mapping from positional and keyword arguments to
        parameters.
    * bind_partial(*args, **kwargs) -> BoundArguments
        Creates a partial mapping from positional and keyword arguments
        to parameters (simulating 'functools.partial' behavior.)
    """
    __slots__ = ('_return_annotation', '_parameters')
    _parameter_cls = 形参
    _bound_arguments_cls = 绑定参数
    empty = _empty

    def __init__(self, parameters=None, *, return_annotation=_empty, __validate_parameters__=True):
        """Constructs Signature from the given list of Parameter
        objects and 'return_annotation'.  All arguments are optional.
        """
        if parameters is None:
            params = OrderedDict()
        elif __validate_parameters__:
            params = OrderedDict()
            top_kind = _POSITIONAL_ONLY
            seen_default = False
            seen_var_parameters = set()
            for param in parameters:
                种类 = param.kind
                名字 = param.name
                if 种类 in (_VAR_POSITIONAL, _VAR_KEYWORD):
                    if 种类 in seen_var_parameters:
                        msg = f'more than one {种类.description} parameter'
                        raise ValueError(msg)
                    seen_var_parameters.add(种类)
                if 种类 < top_kind:
                    msg = 'wrong parameter order: {} parameter before {} parameter'
                    msg = msg.format(top_kind.description, 种类.description)
                    raise ValueError(msg)
                elif 种类 > top_kind:
                    top_kind = 种类
                if 种类 in (_POSITIONAL_ONLY, _POSITIONAL_OR_KEYWORD):
                    if param.default is _empty:
                        if seen_default:
                            msg = 'non-default argument follows default argument'
                            raise ValueError(msg)
                    else:
                        seen_default = True
                if 名字 in params:
                    msg = 'duplicate parameter name: {!r}'.format(名字)
                    raise ValueError(msg)
                params[名字] = param
        else:
            params = OrderedDict(((param.name, param) for param in parameters))
        self._parameters = types.MappingProxyType(params)
        self._return_annotation = return_annotation

    @classmethod
    def 由可调用对象取(cls, obj, *, follow_wrapped=True, globals=None, locals=None, eval_str=False, annotation_format=Format.VALUE):
        """Constructs Signature for the given callable object."""
        return _signature_from_callable(obj, sigcls=cls, follow_wrapper_chains=follow_wrapped, globals=globals, locals=locals, eval_str=eval_str, annotation_format=annotation_format)

    @property
    def 参数表(self):
        return self._parameters

    @property
    def 返回注解(self):
        return self._return_annotation

    def replace(self, *, parameters=_void, return_annotation=_void):
        """Creates a customized copy of the Signature.
        Pass 'parameters' and/or 'return_annotation' arguments
        to override them in the new copy.
        """
        if parameters is _void:
            parameters = self.参数表.values()
        if return_annotation is _void:
            return_annotation = self._return_annotation
        return type(self)(parameters, return_annotation=return_annotation)
    __replace__ = replace

    def _hash_basis(self):
        params = tuple((param for param in self.参数表.values() if param.kind != _KEYWORD_ONLY))
        kwo_params = {param.name: param for param in self.参数表.values() if param.kind == _KEYWORD_ONLY}
        return (params, kwo_params, self.返回注解)

    def __hash__(self):
        params, kwo_params, 返回注解 = self._hash_basis()
        kwo_params = frozenset(kwo_params.values())
        return hash((params, kwo_params, 返回注解))

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, 签名):
            return NotImplemented
        return self._hash_basis() == other._hash_basis()

    def _bind(self, args, kwargs, *, partial=False):
        """Private method. Don't use directly."""
        arguments = {}
        参数表 = iter(self.参数表.values())
        parameters_ex = ()
        arg_vals = iter(args)
        pos_only_param_in_kwargs = []
        while True:
            try:
                arg_val = next(arg_vals)
            except StopIteration:
                try:
                    param = next(参数表)
                except StopIteration:
                    break
                else:
                    if param.kind == _VAR_POSITIONAL:
                        break
                    elif param.name in kwargs:
                        if param.kind == _POSITIONAL_ONLY:
                            if param.default is _empty:
                                msg = f'missing a required positional-only argument: {param.name!r}'
                                raise TypeError(msg)
                            pos_only_param_in_kwargs.append(param)
                            continue
                        parameters_ex = (param,)
                        break
                    elif param.kind == _VAR_KEYWORD or param.default is not _empty:
                        parameters_ex = (param,)
                        break
                    elif partial:
                        parameters_ex = (param,)
                        break
                    else:
                        if param.kind == _KEYWORD_ONLY:
                            argtype = ' keyword-only'
                        else:
                            argtype = ''
                        msg = 'missing a required{argtype} argument: {arg!r}'
                        msg = msg.format(arg=param.name, argtype=argtype)
                        raise TypeError(msg) from None
            else:
                try:
                    param = next(参数表)
                except StopIteration:
                    raise TypeError('too many positional arguments') from None
                else:
                    if param.kind in (_VAR_KEYWORD, _KEYWORD_ONLY):
                        raise TypeError('too many positional arguments') from None
                    if param.kind == _VAR_POSITIONAL:
                        values = [arg_val]
                        values.extend(arg_vals)
                        arguments[param.name] = tuple(values)
                        break
                    if param.name in kwargs and param.kind != _POSITIONAL_ONLY:
                        raise TypeError('multiple values for argument {arg!r}'.format(arg=param.name)) from None
                    arguments[param.name] = arg_val
        kwargs_param = None
        for param in itertools.chain(parameters_ex, 参数表):
            if param.kind == _VAR_KEYWORD:
                kwargs_param = param
                continue
            if param.kind == _VAR_POSITIONAL:
                continue
            param_name = param.name
            try:
                arg_val = kwargs.pop(param_name)
            except KeyError:
                if not partial and param.kind != _VAR_POSITIONAL and (param.default is _empty):
                    raise TypeError('missing a required argument: {arg!r}'.format(arg=param_name)) from None
            else:
                arguments[param_name] = arg_val
        if kwargs:
            if kwargs_param is not None:
                arguments[kwargs_param.name] = kwargs
            elif pos_only_param_in_kwargs:
                raise TypeError('got some positional-only arguments passed as keyword arguments: {arg!r}'.format(arg=', '.join((param.name for param in pos_only_param_in_kwargs))))
            else:
                raise TypeError('got an unexpected keyword argument {arg!r}'.format(arg=next(iter(kwargs))))
        return self._bound_arguments_cls(self, arguments)

    def 绑定(self, /, *args, **kwargs):
        """Get a BoundArguments object, that maps the passed `args`
        and `kwargs` to the function's signature.  Raises `TypeError`
        if the passed arguments can not be bound.
        """
        return self._bind(args, kwargs)

    def 部分绑定(self, /, *args, **kwargs):
        """Get a BoundArguments object, that partially maps the
        passed `args` and `kwargs` to the function's signature.
        Raises `TypeError` if the passed arguments can not be bound.
        """
        return self._bind(args, kwargs, partial=True)

    def __reduce__(self):
        return (type(self), (tuple(self._parameters.values()),), {'_return_annotation': self._return_annotation})

    def __setstate__(self, state):
        self._return_annotation = state['_return_annotation']

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self)

    def __str__(self):
        return self.format()

    def format(self, *, max_width=None, quote_annotation_strings=True):
        """Create a string representation of the Signature object.

        If *max_width* integer is passed,
        signature will try to fit into the *max_width*.
        If signature is longer than *max_width*,
        all parameters will be on separate lines.

        If *quote_annotation_strings* is False, annotations
        in the signature are displayed without opening and closing quotation
        marks. This is useful when the signature was created with the
        STRING format or when ``from __future__ import annotations`` was used.
        """
        result = []
        render_pos_only_separator = False
        render_kw_only_separator = True
        for param in self.参数表.values():
            formatted = param._format(quote_annotation_strings=quote_annotation_strings)
            种类 = param.kind
            if 种类 == _POSITIONAL_ONLY:
                render_pos_only_separator = True
            elif render_pos_only_separator:
                result.append('/')
                render_pos_only_separator = False
            if 种类 == _VAR_POSITIONAL:
                render_kw_only_separator = False
            elif 种类 == _KEYWORD_ONLY and render_kw_only_separator:
                result.append('*')
                render_kw_only_separator = False
            result.append(formatted)
        if render_pos_only_separator:
            result.append('/')
        rendered = '({})'.format(', '.join(result))
        if max_width is not None and len(rendered) > max_width:
            rendered = '(\n    {}\n)'.format(',\n    '.join(result))
        if self.返回注解 is not _empty:
            anno = 格式化注解(self.返回注解, quote_annotation_strings=quote_annotation_strings)
            rendered += ' -> {}'.format(anno)
        return rendered
_装类转发(签名, {'bind': '绑定', 'bind_partial': '部分绑定', 'from_callable': '由可调用对象取', 'parameters': '参数表', 'return_annotation': '返回注解'}, {'bind': '绑定', 'bind_partial': '部分绑定', 'from_callable': '由可调用对象取', 'parameters': '参数表', 'return_annotation': '返回注解'})

def 取签名(obj, *, follow_wrapped=True, globals=None, locals=None, eval_str=False, annotation_format=Format.VALUE):
    """Get a signature object for the passed callable."""
    return 签名.由可调用对象取(obj, follow_wrapped=follow_wrapped, globals=globals, locals=locals, eval_str=eval_str, annotation_format=annotation_format)

class 缓冲标志(enum.IntFlag):
    SIMPLE = 0
    WRITABLE = 1
    FORMAT = 4
    ND = 8
    STRIDES = 16 | ND
    C_CONTIGUOUS = 32 | STRIDES
    F_CONTIGUOUS = 64 | STRIDES
    ANY_CONTIGUOUS = 128 | STRIDES
    INDIRECT = 256 | STRIDES
    CONTIG = ND | WRITABLE
    CONTIG_RO = ND
    STRIDED = STRIDES | WRITABLE
    STRIDED_RO = STRIDES
    RECORDS = STRIDES | WRITABLE | FORMAT
    RECORDS_RO = STRIDES | FORMAT
    FULL = INDIRECT | WRITABLE | FORMAT
    FULL_RO = INDIRECT | FORMAT
    READ = 256
    WRITE = 512

def _main():
    """ Logic for inspecting an object given at command line """
    import argparse
    import importlib
    parser = argparse.ArgumentParser(color=True)
    parser.add_argument('object', help="The object to be analysed. It supports the 'module:qualname' syntax")
    parser.add_argument('-d', '--details', action='store_true', help='Display info about the module rather than its source code')
    参数 = parser.parse_args()
    target = 参数.object
    mod_name, has_attrs, attrs = target.partition(':')
    try:
        obj = module = importlib.import_module(mod_name)
    except Exception as exc:
        msg = 'Failed to import {} ({}: {})'.format(mod_name, type(exc).__name__, exc)
        print(msg, file=sys.stderr)
        sys.exit(2)
    if has_attrs:
        parts = attrs.split('.')
        obj = module
        for part in parts:
            obj = getattr(obj, part)
    if module.__name__ in sys.builtin_module_names:
        print("Can't get info for builtin modules.", file=sys.stderr)
        sys.exit(1)
    if 参数.details:
        print('Target: {}'.format(target))
        print('Origin: {}'.format(取源文件(module)))
        print('Cached: {}'.format(module.__cached__))
        if obj is module:
            print('Loader: {}'.format(repr(module.__loader__)))
            if hasattr(module, '__path__'):
                print('Submodule search path: {}'.format(module.__path__))
        else:
            try:
                __, lineno = 找源码(obj)
            except Exception:
                pass
            else:
                print('Line: {}'.format(lineno))
        print('\n')
    else:
        print(取源码(obj))
if __name__ == '__main__':
    _main()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 本模块别名：词表里有、但规则不让改定义的名字（内置名最典型，比如 `open`）
_本模块别名 = {
    '取绝对文件名': 'getabsfile',
    '文件到模块表': 'modulesbyfile',
    '是方法描述符吗': 'ismethoddescriptor',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'AGEN_CLOSED': '异步生成器已关闭',
    'AGEN_CREATED': '异步生成器已创建',
    'AGEN_RUNNING': '异步生成器运行中',
    'AGEN_SUSPENDED': '异步生成器已挂起',
    'ArgInfo': '参数信息',
    'Arguments': '实参信息',
    'Attribute': '属性信息',
    'BlockFinder': '代码块查找器',
    'BoundArguments': '绑定参数',
    'BufferFlags': '缓冲标志',
    'CORO_CLOSED': '协程已关闭',
    'CORO_CREATED': '协程已创建',
    'CORO_RUNNING': '协程运行中',
    'CORO_SUSPENDED': '协程已挂起',
    'ClassFoundException': '找到类异常',
    'ClosureVars': '闭包变量',
    'EndOfBlock': '代码块结束',
    'FrameInfo': '帧信息',
    'FullArgSpec': '完整参数规格',
    'GEN_CLOSED': '生成器已关闭',
    'GEN_CREATED': '生成器已创建',
    'GEN_RUNNING': '生成器运行中',
    'GEN_SUSPENDED': '生成器已挂起',
    'Parameter': '形参',
    'Signature': '签名',
    'TPFLAGS_IS_ABSTRACT': '抽象标志位',
    'Traceback': '回溯信息',
    'classify_class_attrs': '分类类属性',
    'cleandoc': '清理文档',
    'currentframe': '当前帧',
    'findsource': '找源码',
    'formatannotation': '格式化注解',
    'formatannotationrelativeto': '相对格式化注解',
    'formatargvalues': '格式化参数值',
    'getargs': '取参数',
    'getargvalues': '取参数值',
    'getasyncgenlocals': '取异步生成器局部变量',
    'getasyncgenstate': '取异步生成器状态',
    'getattr_static': '静态取属性',
    'getblock': '取代码块',
    'getcallargs': '取调用参数',
    'getclasstree': '取类树',
    'getclosurevars': '取闭包变量',
    'getcomments': '取注释',
    'getcoroutinelocals': '取协程局部变量',
    'getcoroutinestate': '取协程状态',
    'getdoc': '取文档',
    'getfile': '取文件',
    'getframeinfo': '取帧信息',
    'getfullargspec': '取完整参数规格',
    'getgeneratorlocals': '取生成器局部变量',
    'getgeneratorstate': '取生成器状态',
    'getinnerframes': '取内层帧',
    'getlineno': '取行号',
    'getmembers': '取成员',
    'getmembers_static': '静态取成员',
    'getmodule': '取模块',
    'getmodulename': '取模块名',
    'getmro': '取方法解析顺序',
    'getouterframes': '取外层帧',
    'getsource': '取源码',
    'getsourcefile': '取源文件',
    'getsourcelines': '取源码行',
    'indentsize': '取缩进宽度',
    'isabstract': '是抽象的吗',
    'isasyncgen': '是异步生成器吗',
    'isasyncgenfunction': '是异步生成器函数吗',
    'isawaitable': '可等待吗',
    'isbuiltin': '是内置函数吗',
    'isclass': '是类吗',
    'iscode': '是代码对象吗',
    'iscoroutine': '是协程吗',
    'iscoroutinefunction': '是协程函数吗',
    'isdatadescriptor': '是数据描述符吗',
    'isframe': '是帧吗',
    'isfunction': '是函数吗',
    'isgenerator': '是生成器吗',
    'isgeneratorfunction': '是生成器函数吗',
    'isgetsetdescriptor': '是取得设置描述符吗',
    'ismemberdescriptor': '是成员描述符吗',
    'ismethod': '是方法吗',
    'ismethodwrapper': '是方法包装器吗',
    'ismodule': '是模块吗',
    'ispackage': '是包吗',
    'isroutine': '是例程吗',
    'istraceback': '是回溯吗',
    'markcoroutinefunction': '标记协程函数',
    'signature': '取签名',
    'stack': '调用栈',
    'trace': '回溯帧',
    'unwrap': '解开包装',
    'walktree': '遍历类树',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '代码块查找器': {
        'tokeneater': '处理词法单元',
    },
    '形参': {
        'annotation': '注解',
        'default': '默认值',
        'kind': '种类',
        'name': '名字',
    },
    '签名': {
        'bind': '绑定',
        'bind_partial': '部分绑定',
        'from_callable': '由可调用对象取',
        'parameters': '参数表',
        'return_annotation': '返回注解',
    },
    '绑定参数': {
        'apply_defaults': '应用默认值',
        'args': '参数',
        'kwargs': '关键字参数',
        'signature': '取签名',
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
    '_ParameterKind': {
        'name': '名字',
    },
    '代码块查找器': {
        'tokeneater': '处理词法单元',
    },
    '形参': {
        'annotation': '注解',
        'default': '默认值',
        'kind': '种类',
        'name': '名字',
    },
    '签名': {
        'bind': '绑定',
        'bind_partial': '部分绑定',
        'from_callable': '由可调用对象取',
        'parameters': '参数表',
        'return_annotation': '返回注解',
    },
    '绑定参数': {
        'apply_defaults': '应用默认值',
        'args': '参数',
        'kwargs': '关键字参数',
        'signature': '取签名',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '代码块查找器',
    '代码块结束',
    '分类类属性',
    '协程已关闭',
    '协程已创建',
    '协程已挂起',
    '协程运行中',
    '参数信息',
    '取代码块',
    '取内层帧',
    '取协程局部变量',
    '取协程状态',
    '取参数',
    '取参数值',
    '取外层帧',
    '取完整参数规格',
    '取帧信息',
    '取异步生成器局部变量',
    '取异步生成器状态',
    '取成员',
    '取文件',
    '取文档',
    '取方法解析顺序',
    '取模块',
    '取模块名',
    '取注释',
    '取源文件',
    '取源码',
    '取源码行',
    '取生成器局部变量',
    '取生成器状态',
    '取签名',
    '取类树',
    '取绝对文件名',
    '取缩进宽度',
    '取行号',
    '取调用参数',
    '取闭包变量',
    '可等待吗',
    '回溯信息',
    '回溯帧',
    '完整参数规格',
    '实参信息',
    '属性信息',
    '帧信息',
    '异步生成器已关闭',
    '异步生成器已创建',
    '异步生成器已挂起',
    '异步生成器运行中',
    '当前帧',
    '形参',
    '找到类异常',
    '找源码',
    '抽象标志位',
    '文件到模块表',
    '是代码对象吗',
    '是例程吗',
    '是内置函数吗',
    '是函数吗',
    '是包吗',
    '是协程函数吗',
    '是协程吗',
    '是取得设置描述符吗',
    '是回溯吗',
    '是帧吗',
    '是异步生成器函数吗',
    '是异步生成器吗',
    '是成员描述符吗',
    '是抽象的吗',
    '是数据描述符吗',
    '是方法包装器吗',
    '是方法吗',
    '是方法描述符吗',
    '是模块吗',
    '是生成器函数吗',
    '是生成器吗',
    '是类吗',
    '标记协程函数',
    '格式化参数值',
    '格式化注解',
    '清理文档',
    '生成器已关闭',
    '生成器已创建',
    '生成器已挂起',
    '生成器运行中',
    '相对格式化注解',
    '签名',
    '绑定参数',
    '缓冲标志',
    '解开包装',
    '调用栈',
    '遍历类树',
    '闭包变量',
    '静态取属性',
    '静态取成员',
])

# ---- 转发层结束 ----
