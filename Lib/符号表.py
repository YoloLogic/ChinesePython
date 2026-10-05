# -*- coding: utf-8 -*-
"""符号表 —— 汉语库（由 tools/汉化库.py 从 Lib/symtable.py 机械生成，**不要手改**）。

英文库 Lib/symtable.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 符号表
"""


"""Interface to the compiler's internal symbol tables"""
_英文原名表 = {'Class': '类作用域', 'Function': '函数作用域', 'Symbol': '符号', 'SymbolTable': '符号表对象', 'SymbolTableFactory': '符号表工厂', 'SymbolTableType': '符号表类型', 'main': '主函数', 'symtable': '取符号表'}

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
import _symtable
from _symtable import USE, DEF_GLOBAL, DEF_NONLOCAL, DEF_LOCAL, DEF_PARAM, DEF_TYPE_PARAM, DEF_FREE_CLASS, DEF_IMPORT, DEF_BOUND, DEF_ANNOT, DEF_COMP_ITER, DEF_COMP_CELL, SCOPE_OFF, SCOPE_MASK, FREE, LOCAL, GLOBAL_IMPLICIT, GLOBAL_EXPLICIT, CELL
import weakref
from enum import StrEnum
__all__ = ['symtable', 'SymbolTableType', 'SymbolTable', 'Class', 'Function', 'Symbol']

def 取符号表(code, filename, compile_type):
    """ Return the toplevel *SymbolTable* for the source code.

    *filename* is the name of the file with the code
    and *compile_type* is the *compile()* mode argument.
    """
    top = _symtable.symtable(code, filename, compile_type)
    return _newSymbolTable(top, filename)

class 符号表工厂:

    def __init__(self):
        self.__memo = weakref.WeakValueDictionary()

    def new(self, table, filename):
        if table.type == _symtable.TYPE_FUNCTION:
            return 函数作用域(table, filename)
        if table.type == _symtable.TYPE_CLASS:
            return 类作用域(table, filename)
        return 符号表对象(table, filename)

    def __call__(self, table, filename):
        key = (table, filename)
        obj = self.__memo.get(key, None)
        if obj is None:
            obj = self.__memo[key] = self.new(table, filename)
        return obj
_newSymbolTable = 符号表工厂()

class 符号表类型(StrEnum):
    模块 = 'module'
    函数 = 'function'
    类 = 'class'
    注解 = 'annotation'
    类型别名 = 'type alias'
    类型形参 = 'type parameters'
    类型变量 = 'type variable'
_装类转发(符号表类型, {'ANNOTATION': '注解', 'CLASS': '类', 'FUNCTION': '函数', 'MODULE': '模块', 'TYPE_ALIAS': '类型别名', 'TYPE_PARAMETERS': '类型形参', 'TYPE_VARIABLE': '类型变量'}, {'ANNOTATION': '注解', 'CLASS': '类', 'FUNCTION': '函数', 'MODULE': '模块', 'TYPE_ALIAS': '类型别名', 'TYPE_PARAMETERS': '类型形参', 'TYPE_VARIABLE': '类型变量'})

class 符号表对象:

    def __init__(self, raw_table, filename):
        self._table = raw_table
        self._filename = filename
        self._symbols = {}

    def __repr__(self):
        if self.__class__ == 符号表对象:
            kind = ''
        else:
            kind = '%s ' % self.__class__.__name__
        if self._table.name == 'top':
            return '<{0}SymbolTable for module {1}>'.format(kind, self._filename)
        else:
            return '<{0}SymbolTable for {1} in {2}>'.format(kind, self._table.name, self._filename)

    def 取类型(self):
        """Return the type of the symbol table.

        The value returned is one of the values in
        the ``SymbolTableType`` enumeration.
        """
        if self._table.type == _symtable.TYPE_MODULE:
            return 符号表类型.模块
        if self._table.type == _symtable.TYPE_FUNCTION:
            return 符号表类型.函数
        if self._table.type == _symtable.TYPE_CLASS:
            return 符号表类型.类
        if self._table.type == _symtable.TYPE_ANNOTATION:
            return 符号表类型.注解
        if self._table.type == _symtable.TYPE_TYPE_ALIAS:
            return 符号表类型.类型别名
        if self._table.type == _symtable.TYPE_TYPE_PARAMETERS:
            return 符号表类型.类型形参
        if self._table.type == _symtable.TYPE_TYPE_VARIABLE:
            return 符号表类型.类型变量
        assert False, f'unexpected type: {self._table.type}'

    def 取ID(self):
        """Return an identifier for the table.
        """
        return self._table.id

    def 取名字(self):
        """Return the table's name.

        This corresponds to the name of the class, function
        or 'top' if the table is for a class, function or
        global respectively.
        """
        return self._table.name

    def 取行号(self):
        """Return the number of the first line in the
        block for the table.
        """
        return self._table.lineno

    def 已优化吗(self):
        """Return *True* if the locals in the table
        are optimizable.
        """
        return bool(self._table.type == _symtable.TYPE_FUNCTION)

    def 是嵌套吗(self):
        """Return *True* if the block is a nested class
        or function."""
        return bool(self._table.nested)

    def 有子表吗(self):
        """Return *True* if the block has nested namespaces.
        """
        return bool(self._table.children)

    def 取标识符(self):
        """Return a view object containing the names of symbols in the table.
        """
        return self._table.symbols.keys()

    def 查找符号(self, name):
        """Lookup a *name* in the table.

        Returns a *Symbol* instance.
        """
        sym = self._symbols.get(name)
        if sym is None:
            flags = self._table.symbols[name]
            namespaces = self.__check_children(name)
            module_scope = self._table.name == 'top'
            sym = self._symbols[name] = 符号(name, flags, namespaces, module_scope=module_scope)
        return sym

    def 取符号表项(self):
        """Return a list of *Symbol* instances for
        names in the table.
        """
        return [self.查找符号(ident) for ident in self.取标识符()]

    def __check_children(self, name):
        return [_newSymbolTable(st, self._filename) for st in self._table.children if st.name == name]

    def 取子表(self):
        """Return a list of the nested symbol tables.
        """
        return [_newSymbolTable(st, self._filename) for st in self._table.children]
_装类转发(符号表对象, {'get_children': '取子表', 'get_id': '取ID', 'get_identifiers': '取标识符', 'get_lineno': '取行号', 'get_name': '取名字', 'get_symbols': '取符号表项', 'get_type': '取类型', 'has_children': '有子表吗', 'is_nested': '是嵌套吗', 'is_optimized': '已优化吗', 'lookup': '查找符号'}, {'get_children': '取子表', 'get_id': '取ID', 'get_identifiers': '取标识符', 'get_lineno': '取行号', 'get_name': '取名字', 'get_symbols': '取符号表项', 'get_type': '取类型', 'has_children': '有子表吗', 'is_nested': '是嵌套吗', 'is_optimized': '已优化吗', 'lookup': '查找符号'})

def _get_scope(flags):
    return flags >> SCOPE_OFF & SCOPE_MASK

class 函数作用域(符号表对象):
    __params = None
    __locals = None
    __frees = None
    __globals = None
    __nonlocals = None

    def __idents_matching(self, test_func):
        return tuple((ident for ident in self.取标识符() if test_func(self._table.symbols[ident])))

    def 取形参(self):
        """Return a tuple of parameters to the function.
        """
        if self.__params is None:
            self.__params = self.__idents_matching(lambda x: x & DEF_PARAM)
        return self.__params

    def 取局部变量(self):
        """Return a tuple of locals in the function.
        """
        if self.__locals is None:
            locs = (LOCAL, CELL)
            test = lambda x: _get_scope(x) in locs
            self.__locals = self.__idents_matching(test)
        return self.__locals

    def 取全局变量(self):
        """Return a tuple of globals in the function.
        """
        if self.__globals is None:
            glob = (GLOBAL_IMPLICIT, GLOBAL_EXPLICIT)
            test = lambda x: _get_scope(x) in glob
            self.__globals = self.__idents_matching(test)
        return self.__globals

    def 取非局部变量(self):
        """Return a tuple of nonlocals in the function.
        """
        if self.__nonlocals is None:
            self.__nonlocals = self.__idents_matching(lambda x: x & DEF_NONLOCAL)
        return self.__nonlocals

    def 取自由变量(self):
        """Return a tuple of free variables in the function.
        """
        if self.__frees is None:
            是自由变量吗 = lambda x: _get_scope(x) == FREE
            self.__frees = self.__idents_matching(是自由变量吗)
        return self.__frees
_装类转发(函数作用域, {'get_frees': '取自由变量', 'get_globals': '取全局变量', 'get_locals': '取局部变量', 'get_nonlocals': '取非局部变量', 'get_parameters': '取形参'}, {'get_frees': '取自由变量', 'get_globals': '取全局变量', 'get_identifiers': '取标识符', 'get_locals': '取局部变量', 'get_nonlocals': '取非局部变量', 'get_parameters': '取形参'})

class 类作用域(符号表对象):
    __methods = None

    def 取方法(self):
        """Return a tuple of methods declared in the class.
        """
        import warnings
        typename = f'{self.__class__.__module__}.{self.__class__.__name__}'
        warnings.warn(f'{typename}.get_methods() is deprecated and will be removed in Python 3.16.', DeprecationWarning, stacklevel=2)
        if self.__methods is None:
            d = {}

            def is_local_symbol(ident):
                flags = self._table.symbols.get(ident, 0)
                return flags >> SCOPE_OFF & SCOPE_MASK == LOCAL
            for st in self._table.children:
                if is_local_symbol(st.name):
                    match st.type:
                        case _symtable.TYPE_FUNCTION:
                            if st.name == 'genexpr' and '.0' in st.varnames:
                                continue
                            d[st.name] = 1
                        case _symtable.TYPE_TYPE_PARAMETERS:
                            scope_name = st.name
                            for c in st.children:
                                if c.name == scope_name and c.type == _symtable.TYPE_FUNCTION:
                                    assert scope_name != 'genexpr' or '.0' not in c.varnames
                                    d[scope_name] = 1
                                    break
            self.__methods = tuple(d)
        return self.__methods
_装类转发(类作用域, {'get_methods': '取方法'}, {'get_methods': '取方法'})

class 符号:

    def __init__(self, name, flags, namespaces=None, *, module_scope=False):
        self.__name = name
        self.__flags = flags
        self.__scope = _get_scope(flags)
        self.__namespaces = namespaces or ()
        self.__module_scope = module_scope

    def __repr__(self):
        flags_str = '|'.join(self._flags_str())
        return f'<symbol {self.__name!r}: {self._scope_str()}, {flags_str}>'

    def _scope_str(self):
        return _scopes_value_to_name.get(self.__scope) or str(self.__scope)

    def _flags_str(self):
        for flagname, flagvalue in _flags:
            if self.__flags & flagvalue == flagvalue:
                yield flagname

    def 取名字(self):
        """Return a name of a symbol.
        """
        return self.__name

    def 被引用吗(self):
        """Return *True* if the symbol is used in
        its block.
        """
        return bool(self.__flags & USE)

    def 是形参吗(self):
        """Return *True* if the symbol is a parameter.
        """
        return bool(self.__flags & DEF_PARAM)

    def 是类型形参吗(self):
        """Return *True* if the symbol is a type parameter.
        """
        return bool(self.__flags & DEF_TYPE_PARAM)

    def 是全局吗(self):
        """Return *True* if the symbol is global.
        """
        return bool(self.__scope in (GLOBAL_IMPLICIT, GLOBAL_EXPLICIT) or (self.__module_scope and self.__flags & DEF_BOUND))

    def 是非局部吗(self):
        """Return *True* if the symbol is nonlocal."""
        return bool(self.__flags & DEF_NONLOCAL)

    def 声明为全局吗(self):
        """Return *True* if the symbol is declared global
        with a global statement."""
        return bool(self.__scope == GLOBAL_EXPLICIT)

    def 是局部吗(self):
        """Return *True* if the symbol is local.
        """
        return bool(self.__scope in (LOCAL, CELL) or (self.__module_scope and self.__flags & DEF_BOUND))

    def 有注解吗(self):
        """Return *True* if the symbol is annotated.
        """
        return bool(self.__flags & DEF_ANNOT)

    def 是自由变量吗(self):
        """Return *True* if a referenced symbol is
        not assigned to.
        """
        return bool(self.__scope == FREE)

    def 是类自由变量吗(self):
        """Return *True* if a class-scoped symbol is free from
        the perspective of a method."""
        return bool(self.__flags & DEF_FREE_CLASS)

    def 是导入的吗(self):
        """Return *True* if the symbol is created from
        an import statement.
        """
        return bool(self.__flags & DEF_IMPORT)

    def 被赋值吗(self):
        """Return *True* if a symbol is assigned to."""
        return bool(self.__flags & DEF_LOCAL)

    def 是推导迭代变量吗(self):
        """Return *True* if the symbol is a comprehension iteration variable.
        """
        return bool(self.__flags & DEF_COMP_ITER)

    def 是推导单元吗(self):
        """Return *True* if the symbol is a cell in an inlined comprehension.
        """
        return bool(self.__flags & DEF_COMP_CELL)

    def 是命名空间吗(self):
        """Returns *True* if name binding introduces new namespace.

        If the name is used as the target of a function or class
        statement, this will be true.

        Note that a single name can be bound to multiple objects.  If
        is_namespace() is true, the name may also be bound to other
        objects, like an int or list, that does not introduce a new
        namespace.
        """
        return bool(self.__namespaces)

    def 取命名空间表(self):
        """Return a list of namespaces bound to this name"""
        return self.__namespaces

    def 取命名空间(self):
        """Return the single namespace bound to this name.

        Raises ValueError if the name is bound to multiple namespaces
        or no namespace.
        """
        if len(self.__namespaces) == 0:
            raise ValueError('name is not bound to any namespaces')
        elif len(self.__namespaces) > 1:
            raise ValueError('name is bound to multiple namespaces')
        else:
            return self.__namespaces[0]
_装类转发(符号, {'get_name': '取名字', 'get_namespace': '取命名空间', 'get_namespaces': '取命名空间表', 'is_annotated': '有注解吗', 'is_assigned': '被赋值吗', 'is_comp_cell': '是推导单元吗', 'is_comp_iter': '是推导迭代变量吗', 'is_declared_global': '声明为全局吗', 'is_free': '是自由变量吗', 'is_free_class': '是类自由变量吗', 'is_global': '是全局吗', 'is_imported': '是导入的吗', 'is_local': '是局部吗', 'is_namespace': '是命名空间吗', 'is_nonlocal': '是非局部吗', 'is_parameter': '是形参吗', 'is_referenced': '被引用吗', 'is_type_parameter': '是类型形参吗'}, {'get_name': '取名字', 'get_namespace': '取命名空间', 'get_namespaces': '取命名空间表', 'is_annotated': '有注解吗', 'is_assigned': '被赋值吗', 'is_comp_cell': '是推导单元吗', 'is_comp_iter': '是推导迭代变量吗', 'is_declared_global': '声明为全局吗', 'is_free': '是自由变量吗', 'is_free_class': '是类自由变量吗', 'is_global': '是全局吗', 'is_imported': '是导入的吗', 'is_local': '是局部吗', 'is_namespace': '是命名空间吗', 'is_nonlocal': '是非局部吗', 'is_parameter': '是形参吗', 'is_referenced': '被引用吗', 'is_type_parameter': '是类型形参吗'})
_flags = [('USE', USE)]
_flags.extend((kv for kv in globals().items() if kv[0].startswith('DEF_')))
_scopes_names = ('FREE', 'LOCAL', 'GLOBAL_IMPLICIT', 'GLOBAL_EXPLICIT', 'CELL')
_scopes_value_to_name = {globals()[n]: n for n in _scopes_names}

def 主函数(args):
    import sys

    def print_symbols(table, level=0):
        indent = '    ' * level
        nested = 'nested ' if table.is_nested() else ''
        if table.get_type() == 'module':
            what = f'from file {table._filename!r}'
        else:
            what = f'{table.get_name()!r}'
        print(f'{indent}symbol table for {nested}{table.get_type()} {what}:')
        for ident in table.get_identifiers():
            symbol = table.lookup(ident)
            flags = ', '.join(symbol._flags_str()).lower()
            print(f'    {indent}{symbol._scope_str().lower()} symbol {symbol.get_name()!r}: {flags}')
        print()
        for table2 in table.get_children():
            print_symbols(table2, level + 1)
    for filename in args or ['-']:
        if filename == '-':
            src = sys.stdin.read()
            filename = '<stdin>'
        else:
            with open(filename, 'rb') as f:
                src = f.read()
        mod = 取符号表(src, filename, 'exec')
        print_symbols(mod)
if __name__ == '__main__':
    import sys
    主函数(sys.argv[1:])


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Class': '类作用域',
    'Function': '函数作用域',
    'Symbol': '符号',
    'SymbolTable': '符号表对象',
    'SymbolTableFactory': '符号表工厂',
    'SymbolTableType': '符号表类型',
    'main': '主函数',
    'symtable': '取符号表',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '函数作用域': {
        'get_frees': '取自由变量',
        'get_globals': '取全局变量',
        'get_locals': '取局部变量',
        'get_nonlocals': '取非局部变量',
        'get_parameters': '取形参',
    },
    '符号': {
        'get_name': '取名字',
        'get_namespace': '取命名空间',
        'get_namespaces': '取命名空间表',
        'is_annotated': '有注解吗',
        'is_assigned': '被赋值吗',
        'is_comp_cell': '是推导单元吗',
        'is_comp_iter': '是推导迭代变量吗',
        'is_declared_global': '声明为全局吗',
        'is_free': '是自由变量吗',
        'is_free_class': '是类自由变量吗',
        'is_global': '是全局吗',
        'is_imported': '是导入的吗',
        'is_local': '是局部吗',
        'is_namespace': '是命名空间吗',
        'is_nonlocal': '是非局部吗',
        'is_parameter': '是形参吗',
        'is_referenced': '被引用吗',
        'is_type_parameter': '是类型形参吗',
    },
    '符号表对象': {
        'get_children': '取子表',
        'get_id': '取ID',
        'get_identifiers': '取标识符',
        'get_lineno': '取行号',
        'get_name': '取名字',
        'get_symbols': '取符号表项',
        'get_type': '取类型',
        'has_children': '有子表吗',
        'is_nested': '是嵌套吗',
        'is_optimized': '已优化吗',
        'lookup': '查找符号',
    },
    '符号表类型': {
        'ANNOTATION': '注解',
        'CLASS': '类',
        'FUNCTION': '函数',
        'MODULE': '模块',
        'TYPE_ALIAS': '类型别名',
        'TYPE_PARAMETERS': '类型形参',
        'TYPE_VARIABLE': '类型变量',
    },
    '类作用域': {
        'get_methods': '取方法',
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
    '函数作用域': {
        'get_frees': '取自由变量',
        'get_globals': '取全局变量',
        'get_identifiers': '取标识符',
        'get_locals': '取局部变量',
        'get_nonlocals': '取非局部变量',
        'get_parameters': '取形参',
    },
    '符号': {
        'get_name': '取名字',
        'get_namespace': '取命名空间',
        'get_namespaces': '取命名空间表',
        'is_annotated': '有注解吗',
        'is_assigned': '被赋值吗',
        'is_comp_cell': '是推导单元吗',
        'is_comp_iter': '是推导迭代变量吗',
        'is_declared_global': '声明为全局吗',
        'is_free': '是自由变量吗',
        'is_free_class': '是类自由变量吗',
        'is_global': '是全局吗',
        'is_imported': '是导入的吗',
        'is_local': '是局部吗',
        'is_namespace': '是命名空间吗',
        'is_nonlocal': '是非局部吗',
        'is_parameter': '是形参吗',
        'is_referenced': '被引用吗',
        'is_type_parameter': '是类型形参吗',
    },
    '符号表对象': {
        'get_children': '取子表',
        'get_id': '取ID',
        'get_identifiers': '取标识符',
        'get_lineno': '取行号',
        'get_name': '取名字',
        'get_symbols': '取符号表项',
        'get_type': '取类型',
        'has_children': '有子表吗',
        'is_nested': '是嵌套吗',
        'is_optimized': '已优化吗',
        'lookup': '查找符号',
    },
    '符号表类型': {
        'ANNOTATION': '注解',
        'CLASS': '类',
        'FUNCTION': '函数',
        'MODULE': '模块',
        'TYPE_ALIAS': '类型别名',
        'TYPE_PARAMETERS': '类型形参',
        'TYPE_VARIABLE': '类型变量',
    },
    '类作用域': {
        'get_methods': '取方法',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '函数作用域',
    '取符号表',
    '符号',
    '符号表对象',
    '符号表类型',
    '类作用域',
])

# ---- 转发层结束 ----
