# -*- coding: utf-8 -*-
"""类型注解 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`typing`（typing 的官方用例按模块名自证（D-132）⇒ 深拷贝不行；整模块薄壳只加中文别名，真模块不动）。
改名字 = 改 `tools\库词表.py` 里的 `包装层["typing"]`，然后：

    python tools\汉化包装层.py typing

可逆性：删这个文件 + 删词表那一段，英文 `typing` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import typing as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
抽象集合 = __英文模块.AbstractSet
带注解 = __英文模块.Annotated
任意 = __英文模块.Any
任意字符串 = __英文模块.AnyStr
异步管理器 = __英文模块.AsyncContextManager
异步生成器 = __英文模块.AsyncGenerator
异步可迭代 = __英文模块.AsyncIterable
异步迭代器 = __英文模块.AsyncIterator
可等待 = __英文模块.Awaitable
二进制IO = __英文模块.BinaryIO
字节串 = __英文模块.ByteString
可调用 = __英文模块.Callable
链映射 = __英文模块.ChainMap
类变量 = __英文模块.ClassVar
集合类 = __英文模块.Collection
拼接 = __英文模块.Concatenate
容器 = __英文模块.Container
上下文管理器 = __英文模块.ContextManager
协程 = __英文模块.Coroutine
计数器 = __英文模块.Counter
默认字典 = __英文模块.DefaultDict
双端队列 = __英文模块.Deque
字典 = __英文模块.Dict
最终 = __英文模块.Final
前向引用 = __英文模块.ForwardRef
冻结集合 = __英文模块.FrozenSet
生成器 = __英文模块.Generator
泛型 = __英文模块.Generic
可哈希 = __英文模块.Hashable
输入输出 = __英文模块.IO
项视图 = __英文模块.ItemsView
可迭代 = __英文模块.Iterable
迭代器 = __英文模块.Iterator
键视图 = __英文模块.KeysView
列表 = __英文模块.List
字面值 = __英文模块.Literal
字面字符串 = __英文模块.LiteralString
映射 = __英文模块.Mapping
映射视图 = __英文模块.MappingView
匹配对象 = __英文模块.Match
可变映射 = __英文模块.MutableMapping
可变序列 = __英文模块.MutableSequence
可变集合 = __英文模块.MutableSet
具名元组 = __英文模块.NamedTuple
永不 = __英文模块.Never
新类型 = __英文模块.NewType
无默认 = __英文模块.NoDefault
无返回 = __英文模块.NoReturn
非必需 = __英文模块.NotRequired
可选 = __英文模块.Optional
有序字典 = __英文模块.OrderedDict
形参规格 = __英文模块.ParamSpec
形参规格实参 = __英文模块.ParamSpecArgs
规格关键字 = __英文模块.ParamSpecKwargs
模式对象 = __英文模块.Pattern
协议 = __英文模块.Protocol
只读 = __英文模块.ReadOnly
必需 = __英文模块.Required
可逆 = __英文模块.Reversible
自身类型 = __英文模块.Self
序列 = __英文模块.Sequence
集合 = __英文模块.Set
有长度 = __英文模块.Sized
支持取绝对值 = __英文模块.SupportsAbs
支持字节 = __英文模块.SupportsBytes
支持复数 = __英文模块.SupportsComplex
支持浮点 = __英文模块.SupportsFloat
支持下标 = __英文模块.SupportsIndex
支持整数 = __英文模块.SupportsInt
支持舍入 = __英文模块.SupportsRound
类型检查中 = __英文模块.TYPE_CHECKING
文本 = __英文模块.Text
文本IO = __英文模块.TextIO
元组 = __英文模块.Tuple
类型对象 = __英文模块.Type
类型别名 = __英文模块.TypeAlias
类型别名类型 = __英文模块.TypeAliasType
类型守卫 = __英文模块.TypeGuard
类型是 = __英文模块.TypeIs
类型变量 = __英文模块.TypeVar
类型变量元组 = __英文模块.TypeVarTuple
类型字典 = __英文模块.TypedDict
联合 = __英文模块.Union
解包 = __英文模块.Unpack
值视图 = __英文模块.ValuesView
断言不会 = __英文模块.assert_never
断言类型 = __英文模块.assert_type
转换 = __英文模块.cast
清重载 = __英文模块.clear_overloads
数据类变换 = __英文模块.dataclass_transform
求值前向引用 = __英文模块.evaluate_forward_ref
最终标注 = __英文模块.final
取实参 = __英文模块.get_args
取原点 = __英文模块.get_origin
取重载 = __英文模块.get_overloads
取协议成员 = __英文模块.get_protocol_members
取类型提示 = __英文模块.get_type_hints
是协议吗 = __英文模块.is_protocol
是类型字典吗 = __英文模块.is_typeddict
不查类型 = __英文模块.no_type_check
不查类型装饰 = __英文模块.no_type_check_decorator
重载 = __英文模块.overload
覆盖标注 = __英文模块.override
揭示类型 = __英文模块.reveal_type
运行时可查 = __英文模块.runtime_checkable

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
AbstractSet = __英文模块.AbstractSet
Annotated = __英文模块.Annotated
Any = __英文模块.Any
AnyStr = __英文模块.AnyStr
AsyncContextManager = __英文模块.AsyncContextManager
AsyncGenerator = __英文模块.AsyncGenerator
AsyncIterable = __英文模块.AsyncIterable
AsyncIterator = __英文模块.AsyncIterator
Awaitable = __英文模块.Awaitable
BinaryIO = __英文模块.BinaryIO
ByteString = __英文模块.ByteString
Callable = __英文模块.Callable
ChainMap = __英文模块.ChainMap
ClassVar = __英文模块.ClassVar
Collection = __英文模块.Collection
Concatenate = __英文模块.Concatenate
Container = __英文模块.Container
ContextManager = __英文模块.ContextManager
Coroutine = __英文模块.Coroutine
Counter = __英文模块.Counter
DefaultDict = __英文模块.DefaultDict
Deque = __英文模块.Deque
Dict = __英文模块.Dict
Final = __英文模块.Final
ForwardRef = __英文模块.ForwardRef
FrozenSet = __英文模块.FrozenSet
Generator = __英文模块.Generator
Generic = __英文模块.Generic
Hashable = __英文模块.Hashable
IO = __英文模块.IO
ItemsView = __英文模块.ItemsView
Iterable = __英文模块.Iterable
Iterator = __英文模块.Iterator
KeysView = __英文模块.KeysView
List = __英文模块.List
Literal = __英文模块.Literal
LiteralString = __英文模块.LiteralString
Mapping = __英文模块.Mapping
MappingView = __英文模块.MappingView
Match = __英文模块.Match
MutableMapping = __英文模块.MutableMapping
MutableSequence = __英文模块.MutableSequence
MutableSet = __英文模块.MutableSet
NamedTuple = __英文模块.NamedTuple
Never = __英文模块.Never
NewType = __英文模块.NewType
NoDefault = __英文模块.NoDefault
NoReturn = __英文模块.NoReturn
NotRequired = __英文模块.NotRequired
Optional = __英文模块.Optional
OrderedDict = __英文模块.OrderedDict
ParamSpec = __英文模块.ParamSpec
ParamSpecArgs = __英文模块.ParamSpecArgs
ParamSpecKwargs = __英文模块.ParamSpecKwargs
Pattern = __英文模块.Pattern
Protocol = __英文模块.Protocol
ReadOnly = __英文模块.ReadOnly
Required = __英文模块.Required
Reversible = __英文模块.Reversible
Self = __英文模块.Self
Sequence = __英文模块.Sequence
Set = __英文模块.Set
Sized = __英文模块.Sized
SupportsAbs = __英文模块.SupportsAbs
SupportsBytes = __英文模块.SupportsBytes
SupportsComplex = __英文模块.SupportsComplex
SupportsFloat = __英文模块.SupportsFloat
SupportsIndex = __英文模块.SupportsIndex
SupportsInt = __英文模块.SupportsInt
SupportsRound = __英文模块.SupportsRound
TYPE_CHECKING = __英文模块.TYPE_CHECKING
Text = __英文模块.Text
TextIO = __英文模块.TextIO
Tuple = __英文模块.Tuple
Type = __英文模块.Type
TypeAlias = __英文模块.TypeAlias
TypeAliasType = __英文模块.TypeAliasType
TypeGuard = __英文模块.TypeGuard
TypeIs = __英文模块.TypeIs
TypeVar = __英文模块.TypeVar
TypeVarTuple = __英文模块.TypeVarTuple
TypedDict = __英文模块.TypedDict
Union = __英文模块.Union
Unpack = __英文模块.Unpack
ValuesView = __英文模块.ValuesView
assert_never = __英文模块.assert_never
assert_type = __英文模块.assert_type
cast = __英文模块.cast
clear_overloads = __英文模块.clear_overloads
dataclass_transform = __英文模块.dataclass_transform
evaluate_forward_ref = __英文模块.evaluate_forward_ref
final = __英文模块.final
get_args = __英文模块.get_args
get_origin = __英文模块.get_origin
get_overloads = __英文模块.get_overloads
get_protocol_members = __英文模块.get_protocol_members
get_type_hints = __英文模块.get_type_hints
is_protocol = __英文模块.is_protocol
is_typeddict = __英文模块.is_typeddict
no_type_check = __英文模块.no_type_check
no_type_check_decorator = __英文模块.no_type_check_decorator
overload = __英文模块.overload
override = __英文模块.override
reveal_type = __英文模块.reveal_type
runtime_checkable = __英文模块.runtime_checkable

__all__ = [
    'AbstractSet',
    'Annotated',
    'Any',
    'AnyStr',
    'AsyncContextManager',
    'AsyncGenerator',
    'AsyncIterable',
    'AsyncIterator',
    'Awaitable',
    'BinaryIO',
    'ByteString',
    'Callable',
    'ChainMap',
    'ClassVar',
    'Collection',
    'Concatenate',
    'Container',
    'ContextManager',
    'Coroutine',
    'Counter',
    'DefaultDict',
    'Deque',
    'Dict',
    'Final',
    'ForwardRef',
    'FrozenSet',
    'Generator',
    'Generic',
    'Hashable',
    'IO',
    'ItemsView',
    'Iterable',
    'Iterator',
    'KeysView',
    'List',
    'Literal',
    'LiteralString',
    'Mapping',
    'MappingView',
    'Match',
    'MutableMapping',
    'MutableSequence',
    'MutableSet',
    'NamedTuple',
    'Never',
    'NewType',
    'NoDefault',
    'NoReturn',
    'NotRequired',
    'Optional',
    'OrderedDict',
    'ParamSpec',
    'ParamSpecArgs',
    'ParamSpecKwargs',
    'Pattern',
    'Protocol',
    'ReadOnly',
    'Required',
    'Reversible',
    'Self',
    'Sequence',
    'Set',
    'Sized',
    'SupportsAbs',
    'SupportsBytes',
    'SupportsComplex',
    'SupportsFloat',
    'SupportsIndex',
    'SupportsInt',
    'SupportsRound',
    'TYPE_CHECKING',
    'Text',
    'TextIO',
    'Tuple',
    'Type',
    'TypeAlias',
    'TypeAliasType',
    'TypeGuard',
    'TypeIs',
    'TypeVar',
    'TypeVarTuple',
    'TypedDict',
    'Union',
    'Unpack',
    'ValuesView',
    'assert_never',
    'assert_type',
    'cast',
    'clear_overloads',
    'dataclass_transform',
    'evaluate_forward_ref',
    'final',
    'get_args',
    'get_origin',
    'get_overloads',
    'get_protocol_members',
    'get_type_hints',
    'is_protocol',
    'is_typeddict',
    'no_type_check',
    'no_type_check_decorator',
    'overload',
    'override',
    'reveal_type',
    'runtime_checkable',
    '抽象集合',
    '带注解',
    '任意',
    '任意字符串',
    '异步管理器',
    '异步生成器',
    '异步可迭代',
    '异步迭代器',
    '可等待',
    '二进制IO',
    '字节串',
    '可调用',
    '链映射',
    '类变量',
    '集合类',
    '拼接',
    '容器',
    '上下文管理器',
    '协程',
    '计数器',
    '默认字典',
    '双端队列',
    '字典',
    '最终',
    '前向引用',
    '冻结集合',
    '生成器',
    '泛型',
    '可哈希',
    '输入输出',
    '项视图',
    '可迭代',
    '迭代器',
    '键视图',
    '列表',
    '字面值',
    '字面字符串',
    '映射',
    '映射视图',
    '匹配对象',
    '可变映射',
    '可变序列',
    '可变集合',
    '具名元组',
    '永不',
    '新类型',
    '无默认',
    '无返回',
    '非必需',
    '可选',
    '有序字典',
    '形参规格',
    '形参规格实参',
    '规格关键字',
    '模式对象',
    '协议',
    '只读',
    '必需',
    '可逆',
    '自身类型',
    '序列',
    '集合',
    '有长度',
    '支持取绝对值',
    '支持字节',
    '支持复数',
    '支持浮点',
    '支持下标',
    '支持整数',
    '支持舍入',
    '类型检查中',
    '文本',
    '文本IO',
    '元组',
    '类型对象',
    '类型别名',
    '类型别名类型',
    '类型守卫',
    '类型是',
    '类型变量',
    '类型变量元组',
    '类型字典',
    '联合',
    '解包',
    '值视图',
    '断言不会',
    '断言类型',
    '转换',
    '清重载',
    '数据类变换',
    '求值前向引用',
    '最终标注',
    '取实参',
    '取原点',
    '取重载',
    '取协议成员',
    '取类型提示',
    '是协议吗',
    '是类型字典吗',
    '不查类型',
    '不查类型装饰',
    '重载',
    '覆盖标注',
    '揭示类型',
    '运行时可查',
]


def __getattr__(名):
    """兜底转发：没在这儿显式列出来的名字（含私有名）照样到得了 C 那边。

    为什么必须有：硬约束是「英文原名一个都不能少」，而 C 模块的内部名
    我们没法一个个预料 —— 官方测试碰得到的、`dir(zlib)` 里有的一切，
    靠这一条全部兜住（PEP 562 的模块级 `__getattr__`）。
    """
    return getattr(__英文模块, 名)


def __dir__():
    # `dir()` 两边都算上：Shell 补全 / 官方那种按 `dir()` 算的判据都看得见。
    # ⚠ **壳自己的辅助函数不列**（D-147）：官方 `test_signal.test_functions_module_attr`
    #   会遍历 `dir()`，要求每个「非内置函数」的 `__module__` 是英文模块名 ——
    #   壳里的 `__getattr__`/`__dir__` 是 Python 函数、`__module__` 是汉语模块名
    #   ⇒ 列出来就挂（实测）。
    return sorted((set(globals()) | set(dir(__英文模块)))
                  - {"__getattr__", "__dir__", "__英文模块"})
