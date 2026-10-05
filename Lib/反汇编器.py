# -*- coding: utf-8 -*-
"""反汇编器 —— 汉语库（由 tools/汉化库.py 从 Lib/dis.py 机械生成，**不要手改**）。

英文库 Lib/dis.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 反汇编器
"""


"""Disassembler of Python byte code into mnemonics."""
_英文原名表 = {'ArgResolver': '参数解析器', 'Bytecode': '字节码', 'Formatter': '格式化器', 'Instruction': '指令', 'code_info': '代码信息', 'dis': '反汇编', 'disassemble': '反汇编代码', 'distb': '反汇编回溯', 'findlabels': '找标签', 'findlinestarts': '找行号起点', 'get_instructions': '取指令', 'main': '主函数', 'pretty_flags': '美化标志', 'print_instructions': '打印指令', 'show_code': '显示代码'}

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
import types
import collections
import io
from opcode import *
from opcode import __all__ as _opcodes_all, _cache_format, _inline_cache_entries, _nb_ops, _common_constants, _intrinsic_1_descs, _intrinsic_2_descs, _special_method_names, _specializations, _specialized_opmap
from _opcode import get_executor
__all__ = ['code_info', 'dis', 'disassemble', 'distb', 'disco', 'findlinestarts', 'findlabels', 'show_code', 'get_instructions', 'Instruction', 'Bytecode'] + _opcodes_all
del _opcodes_all
_have_code = (types.MethodType, types.FunctionType, types.CodeType, classmethod, staticmethod, type)
CONVERT_VALUE = opmap['CONVERT_VALUE']
SET_FUNCTION_ATTRIBUTE = opmap['SET_FUNCTION_ATTRIBUTE']
FUNCTION_ATTR_FLAGS = ('defaults', 'kwdefaults', 'annotations', 'closure', 'annotate')
ENTER_EXECUTOR = opmap['ENTER_EXECUTOR']
LOAD_GLOBAL = opmap['LOAD_GLOBAL']
LOAD_SMALL_INT = opmap['LOAD_SMALL_INT']
BINARY_OP = opmap['BINARY_OP']
JUMP_BACKWARD = opmap['JUMP_BACKWARD']
FOR_ITER = opmap['FOR_ITER']
SEND = opmap['SEND']
LOAD_ATTR = opmap['LOAD_ATTR']
LOAD_SUPER_ATTR = opmap['LOAD_SUPER_ATTR']
CALL_INTRINSIC_1 = opmap['CALL_INTRINSIC_1']
CALL_INTRINSIC_2 = opmap['CALL_INTRINSIC_2']
LOAD_COMMON_CONSTANT = opmap['LOAD_COMMON_CONSTANT']
LOAD_SPECIAL = opmap['LOAD_SPECIAL']
LOAD_FAST_LOAD_FAST = opmap['LOAD_FAST_LOAD_FAST']
LOAD_FAST_BORROW_LOAD_FAST_BORROW = opmap['LOAD_FAST_BORROW_LOAD_FAST_BORROW']
STORE_FAST_LOAD_FAST = opmap['STORE_FAST_LOAD_FAST']
STORE_FAST_STORE_FAST = opmap['STORE_FAST_STORE_FAST']
IS_OP = opmap['IS_OP']
CONTAINS_OP = opmap['CONTAINS_OP']
END_ASYNC_FOR = opmap['END_ASYNC_FOR']
CACHE = opmap['CACHE']
_all_opname = list(opname)
_all_opmap = dict(opmap)
for name, op in _specialized_opmap.items():
    assert op < len(_all_opname)
    _all_opname[op] = name
    _all_opmap[name] = op
deoptmap = {specialized: base for base, family in _specializations.items() for specialized in family}

def _try_compile(source, name):
    """Attempts to compile the given source, first as an expression and
       then as a statement if the first approach fails.

       Utility function to accept strings in functions that otherwise
       expect code objects
    """
    try:
        return compile(source, name, 'eval')
    except SyntaxError:
        pass
    return compile(source, name, 'exec')

def 反汇编(x=None, *, file=None, depth=None, show_caches=False, adaptive=False, show_offsets=False, show_positions=False):
    """Disassemble classes, methods, functions, and other compiled objects.

    With no argument, disassemble the last traceback.

    Compiled objects currently include generator objects, async generator
    objects, and coroutine objects, all of which store their code object
    in a special attribute.
    """
    if x is None:
        反汇编回溯(file=file, show_caches=show_caches, adaptive=adaptive, show_offsets=show_offsets, show_positions=show_positions)
        return
    if hasattr(x, '__func__'):
        x = x.__func__
    if hasattr(x, '__code__'):
        x = x.__code__
    elif hasattr(x, 'gi_code'):
        x = x.gi_code
    elif hasattr(x, 'ag_code'):
        x = x.ag_code
    elif hasattr(x, 'cr_code'):
        x = x.cr_code
    if hasattr(x, '__dict__'):
        items = sorted(x.__dict__.items())
        for name, x1 in items:
            if isinstance(x1, _have_code):
                print('Disassembly of %s:' % name, file=file)
                try:
                    反汇编(x1, file=file, depth=depth, show_caches=show_caches, adaptive=adaptive, show_offsets=show_offsets, show_positions=show_positions)
                except TypeError as msg:
                    print('Sorry:', msg, file=file)
                print(file=file)
    elif hasattr(x, 'co_code'):
        _disassemble_recursive(x, file=file, depth=depth, show_caches=show_caches, adaptive=adaptive, show_offsets=show_offsets, show_positions=show_positions)
    elif isinstance(x, (bytes, bytearray)):
        labels_map = _make_labels_map(x)
        label_width = 4 + len(str(len(labels_map)))
        formatter = 格式化器(file=file, offset_width=len(str(max(len(x) - 2, 9999))) if show_offsets else 0, label_width=label_width, show_caches=show_caches)
        arg_resolver = 参数解析器(labels_map=labels_map)
        _disassemble_bytes(x, arg_resolver=arg_resolver, formatter=formatter)
    elif isinstance(x, str):
        _disassemble_str(x, file=file, depth=depth, show_caches=show_caches, adaptive=adaptive, show_offsets=show_offsets, show_positions=show_positions)
    else:
        raise TypeError("don't know how to disassemble %s objects" % type(x).__name__)

def 反汇编回溯(tb=None, *, file=None, show_caches=False, adaptive=False, show_offsets=False, show_positions=False):
    """Disassemble a traceback (default: last traceback)."""
    if tb is None:
        try:
            if hasattr(sys, 'last_exc'):
                tb = sys.last_exc.__traceback__
            else:
                tb = sys.last_traceback
        except AttributeError:
            raise RuntimeError('no last traceback to disassemble') from None
        while tb.tb_next:
            tb = tb.tb_next
    反汇编代码(tb.tb_frame.f_code, tb.tb_lasti, file=file, show_caches=show_caches, adaptive=adaptive, show_offsets=show_offsets, show_positions=show_positions)
COMPILER_FLAG_NAMES = {1: 'OPTIMIZED', 2: 'NEWLOCALS', 4: 'VARARGS', 8: 'VARKEYWORDS', 16: 'NESTED', 32: 'GENERATOR', 64: 'NOFREE', 128: 'COROUTINE', 256: 'ITERABLE_COROUTINE', 512: 'ASYNC_GENERATOR', 67108864: 'HAS_DOCSTRING', 134217728: 'METHOD'}

def 美化标志(flags):
    """Return pretty representation of code flags."""
    names = []
    for i in range(32):
        flag = 1 << i
        if flags & flag:
            names.append(COMPILER_FLAG_NAMES.get(flag, hex(flag)))
            flags ^= flag
            if not flags:
                break
    else:
        names.append(hex(flags))
    return ', '.join(names)

class _Unknown:

    def __repr__(self):
        return '<unknown>'
UNKNOWN = _Unknown()

def _get_code_object(x):
    """Helper to handle methods, compiled or raw code objects, and strings."""
    if hasattr(x, '__func__'):
        x = x.__func__
    if hasattr(x, '__code__'):
        x = x.__code__
    elif hasattr(x, 'gi_code'):
        x = x.gi_code
    elif hasattr(x, 'ag_code'):
        x = x.ag_code
    elif hasattr(x, 'cr_code'):
        x = x.cr_code
    if isinstance(x, str):
        x = _try_compile(x, '<disassembly>')
    if hasattr(x, 'co_code'):
        return x
    raise TypeError("don't know how to disassemble %s objects" % type(x).__name__)

def _deoptop(op):
    name = _all_opname[op]
    return _all_opmap[deoptmap[name]] if name in deoptmap else op

def _get_code_array(co, adaptive):
    if adaptive:
        code = co._co_code_adaptive
        res = []
        found = False
        for i in range(0, len(code), 2):
            op, 参数 = (code[i], code[i + 1])
            if op == ENTER_EXECUTOR:
                try:
                    ex = get_executor(co, i)
                except (ValueError, RuntimeError):
                    ex = None
                if ex:
                    op, 参数 = (ex.get_opcode(), ex.get_oparg())
                    found = True
            res.append(op.to_bytes())
            res.append(参数.to_bytes())
        return code if not found else b''.join(res)
    else:
        return co.co_code

def 代码信息(x):
    """Formatted details of methods, functions, or code."""
    return _format_code_info(_get_code_object(x))

def _format_code_info(co):
    lines = []
    lines.append('Name:              %s' % co.co_name)
    lines.append('Filename:          %s' % co.co_filename)
    lines.append('Argument count:    %s' % co.co_argcount)
    lines.append('Positional-only arguments: %s' % co.co_posonlyargcount)
    lines.append('Kw-only arguments: %s' % co.co_kwonlyargcount)
    lines.append('Number of locals:  %s' % co.co_nlocals)
    lines.append('Stack size:        %s' % co.co_stacksize)
    lines.append('Flags:             %s' % 美化标志(co.co_flags))
    if co.co_consts:
        lines.append('Constants:')
        for i_c in enumerate(co.co_consts):
            lines.append('%4d: %r' % i_c)
    if co.co_names:
        lines.append('Names:')
        for i_n in enumerate(co.co_names):
            lines.append('%4d: %s' % i_n)
    if co.co_varnames:
        lines.append('Variable names:')
        for i_n in enumerate(co.co_varnames):
            lines.append('%4d: %s' % i_n)
    if co.co_freevars:
        lines.append('Free variables:')
        for i_n in enumerate(co.co_freevars):
            lines.append('%4d: %s' % i_n)
    if co.co_cellvars:
        lines.append('Cell variables:')
        for i_n in enumerate(co.co_cellvars):
            lines.append('%4d: %s' % i_n)
    return '\n'.join(lines)

def 显示代码(co, *, file=None):
    """Print details of methods, functions, or code to *file*.

    If *file* is not provided, the output is printed on stdout.
    """
    print(代码信息(co), file=file)
Positions = collections.namedtuple('Positions', ['lineno', 'end_lineno', 'col_offset', 'end_col_offset'], defaults=[None] * 4)
_Instruction = collections.namedtuple('_Instruction', ['opname', 'opcode', 'arg', 'argval', 'argrepr', 'offset', 'start_offset', 'starts_line', 'line_number', 'label', 'positions', 'cache_info'], defaults=[None, None, None])
_Instruction.opname.__doc__ = 'Human readable name for operation'
_Instruction.opcode.__doc__ = 'Numeric code for operation'
_Instruction.arg.__doc__ = 'Numeric argument to operation (if any), otherwise None'
_Instruction.argval.__doc__ = 'Resolved arg value (if known), otherwise same as arg'
_Instruction.argrepr.__doc__ = 'Human readable description of operation argument'
_Instruction.offset.__doc__ = 'Start index of operation within bytecode sequence'
_Instruction.start_offset.__doc__ = 'Start index of operation within bytecode sequence, including extended args if present; otherwise equal to Instruction.offset'
_Instruction.starts_line.__doc__ = 'True if this opcode starts a source line, otherwise False'
_Instruction.line_number.__doc__ = 'source line number associated with this opcode (if any), otherwise None'
_Instruction.label.__doc__ = 'A label (int > 0) if this instruction is a jump target, otherwise None'
_Instruction.positions.__doc__ = 'dis.Positions object holding the span of source code covered by this instruction'
_Instruction.cache_info.__doc__ = 'list of (name, size, data), one for each cache entry of the instruction'
_ExceptionTableEntryBase = collections.namedtuple('_ExceptionTableEntryBase', 'start end target depth lasti')

class _ExceptionTableEntry(_ExceptionTableEntryBase):
    pass
_OPNAME_WIDTH = 20
_OPARG_WIDTH = 5

def _get_cache_size(opname):
    return _inline_cache_entries.get(opname, 0)

def _get_jump_target(op, arg, offset):
    """Gets the bytecode offset of the jump target if this is a jump instruction.

    Otherwise return None.
    """
    deop = _deoptop(op)
    caches = _get_cache_size(_all_opname[deop])
    if deop in hasjrel:
        if _is_backward_jump(deop):
            arg = -arg
        target = offset + 2 + arg * 2
        target += 2 * caches
    elif deop in hasjabs:
        target = arg * 2
    else:
        target = None
    return target

class 指令(_Instruction):
    """Details for a bytecode operation.

       Defined fields:
         opname - human readable name for operation
         opcode - numeric code for operation
         arg - numeric argument to operation (if any), otherwise None
         argval - resolved arg value (if known), otherwise same as arg
         argrepr - human readable description of operation argument
         offset - start index of operation within bytecode sequence
         start_offset - start index of operation within bytecode sequence including extended args if present;
                        otherwise equal to Instruction.offset
         starts_line - True if this opcode starts a source line, otherwise False
         line_number - source line number associated with this opcode (if any), otherwise None
         label - A label if this instruction is a jump target, otherwise None
         positions - Optional dis.Positions object holding the span of source code
                     covered by this instruction
         cache_info - information about the format and content of the instruction's cache
                        entries (if any)
    """

    @staticmethod
    def make(opname, arg, argval, argrepr, offset, start_offset, starts_line, line_number, label=None, positions=None, cache_info=None):
        return 指令(opname, _all_opmap[opname], arg, argval, argrepr, offset, start_offset, starts_line, line_number, label, positions, cache_info)

    @property
    def oparg(self):
        """Alias for Instruction.arg."""
        return self.参数

    @property
    def baseopcode(self):
        """Numeric code for the base operation if operation is specialized.

        Otherwise equal to Instruction.opcode.
        """
        return _deoptop(self.操作码)

    @property
    def baseopname(self):
        """Human readable name for the base operation if operation is specialized.

        Otherwise equal to Instruction.opname.
        """
        return opname[self.baseopcode]

    @property
    def cache_offset(self):
        """Start index of the cache entries following the operation."""
        return self.偏移 + 2

    @property
    def 结束偏移(self):
        """End index of the cache entries following the operation."""
        return self.cache_offset + _get_cache_size(_all_opname[self.操作码]) * 2

    @property
    def 跳转目标(self):
        """Bytecode index of the jump target if this is a jump operation.

        Otherwise return None.
        """
        return _get_jump_target(self.操作码, self.参数, self.偏移)

    @property
    def 是跳转目标吗(self):
        """True if other code jumps to here, otherwise False"""
        return self.label is not None

    def __str__(self):
        output = io.StringIO()
        formatter = 格式化器(file=output)
        formatter.print_instruction(self, False)
        return output.getvalue()
_装类转发(指令, {'end_offset': '结束偏移', 'is_jump_target': '是跳转目标吗', 'jump_target': '跳转目标'}, {'arg': '参数', 'end_offset': '结束偏移', 'is_jump_target': '是跳转目标吗', 'jump_target': '跳转目标', 'offset': '偏移', 'opcode': '操作码'})

class 格式化器:

    def __init__(self, file=None, lineno_width=0, offset_width=0, label_width=0, line_offset=0, show_caches=False, *, show_positions=False):
        """Create a Formatter

        *file* where to write the output
        *lineno_width* sets the width of the source location field (0 omits it).
        Should be large enough for a line number or full positions (depending
        on the value of *show_positions*).
        *offset_width* sets the width of the instruction offset field
        *label_width* sets the width of the label field
        *show_caches* is a boolean indicating whether to display cache lines
        *show_positions* is a boolean indicating whether full positions should
        be reported instead of only the line numbers.
        """
        self.file = file
        self.lineno_width = lineno_width
        self.offset_width = offset_width
        self.label_width = label_width
        self.show_caches = show_caches
        self.show_positions = show_positions

    def 打印一条指令(self, instr, mark_as_current=False):
        self.打印指令行(instr, mark_as_current)
        if self.show_caches and instr.cache_info:
            偏移 = instr.offset
            for name, size, data in instr.cache_info:
                for i in range(size):
                    偏移 += 2
                    if i == 0:
                        argrepr = f'{name}: {int.from_bytes(data, sys.byteorder)}'
                    else:
                        argrepr = ''
                    self.打印指令行(指令('CACHE', CACHE, 0, None, argrepr, 偏移, 偏移, False, None, None, instr.positions), False)

    def 打印指令行(self, instr, mark_as_current):
        """Format instruction details for inclusion in disassembly output."""
        lineno_width = self.lineno_width
        offset_width = self.offset_width
        label_width = self.label_width
        new_source_line = lineno_width > 0 and instr.starts_line and (instr.offset > 0)
        if new_source_line:
            print(file=self.file)
        fields = []
        if lineno_width:
            if self.show_positions:
                if (instr_positions := instr.positions):
                    if all((p is None for p in instr_positions)):
                        positions_str = _NO_LINENO
                    else:
                        ps = tuple(('?' if p is None else p for p in instr_positions))
                        positions_str = f'{ps[0]}:{ps[2]}-{ps[1]}:{ps[3]}'
                    fields.append(f'{positions_str:{lineno_width}}')
                else:
                    fields.append(' ' * lineno_width)
            elif instr.starts_line:
                lineno_fmt = '%%%dd' if instr.line_number is not None else '%%%ds'
                lineno_fmt = lineno_fmt % lineno_width
                lineno = _NO_LINENO if instr.line_number is None else instr.line_number
                fields.append(lineno_fmt % lineno)
            else:
                fields.append(' ' * lineno_width)
        if instr.label is not None:
            lbl = f'L{instr.label}:'
            fields.append(f'{lbl:>{label_width}}')
        else:
            fields.append(' ' * label_width)
        if offset_width > 0:
            fields.append(f'{repr(instr.offset):>{offset_width}}  ')
        if mark_as_current:
            fields.append('-->')
        else:
            fields.append('   ')
        fields.append(instr.opname.ljust(_OPNAME_WIDTH))
        if instr.arg is not None:
            参数 = repr(instr.arg)
            opname_excess = max(0, len(instr.opname) - _OPNAME_WIDTH)
            fields.append(repr(instr.arg).rjust(_OPARG_WIDTH - opname_excess))
            if instr.argrepr:
                fields.append('(' + instr.argrepr + ')')
        print(' '.join(fields).rstrip(), file=self.file)

    def 打印异常表(self, exception_entries):
        file = self.file
        if exception_entries:
            print('ExceptionTable:', file=file)
            for entry in exception_entries:
                lasti = ' lasti' if entry.lasti else ''
                start = entry.start_label
                end = entry.end_label
                target = entry.target_label
                print(f'  L{start} to L{end} -> L{target} [{entry.depth}]{lasti}', file=file)
_装类转发(格式化器, {'print_exception_table': '打印异常表', 'print_instruction': '打印一条指令', 'print_instruction_line': '打印指令行'}, {'print_exception_table': '打印异常表', 'print_instruction': '打印一条指令', 'print_instruction_line': '打印指令行'})

class 参数解析器:

    def __init__(self, co_consts=None, names=None, varname_from_oparg=None, labels_map=None):
        self.co_consts = co_consts
        self.names = names
        self.varname_from_oparg = varname_from_oparg
        self.labels_map = labels_map or {}

    def offset_from_jump_arg(self, op, arg, offset):
        deop = _deoptop(op)
        if deop in hasjabs:
            return arg * 2
        elif deop in hasjrel:
            signed_arg = -arg if _is_backward_jump(deop) else arg
            argval = offset + 2 + signed_arg * 2
            caches = _get_cache_size(_all_opname[deop])
            argval += 2 * caches
            return argval
        return None

    def get_label_for_offset(self, offset):
        return self.labels_map.get(offset, None)

    def get_argval_argrepr(self, op, arg, offset):
        get_name = None if self.names is None else self.names.__getitem__
        argval = None
        argrepr = ''
        deop = _deoptop(op)
        if arg is not None:
            argval = arg
            if deop in hasconst:
                argval, argrepr = _get_const_info(deop, arg, self.co_consts)
            elif deop in hasname:
                if deop == LOAD_GLOBAL:
                    argval, argrepr = _get_name_info(arg // 2, get_name)
                    if arg & 1 and argrepr:
                        argrepr = f'{argrepr} + NULL'
                elif deop == LOAD_ATTR:
                    argval, argrepr = _get_name_info(arg // 2, get_name)
                    if arg & 1 and argrepr:
                        argrepr = f'{argrepr} + NULL|self'
                elif deop == LOAD_SUPER_ATTR:
                    argval, argrepr = _get_name_info(arg // 4, get_name)
                    if arg & 1 and argrepr:
                        argrepr = f'{argrepr} + NULL|self'
                else:
                    argval, argrepr = _get_name_info(arg, get_name)
            elif deop in hasjump or deop in hasexc:
                argval = self.offset_from_jump_arg(op, arg, offset)
                lbl = self.get_label_for_offset(argval)
                assert lbl is not None
                preposition = 'from' if deop == END_ASYNC_FOR else 'to'
                argrepr = f'{preposition} L{lbl}'
            elif deop in (LOAD_FAST_LOAD_FAST, LOAD_FAST_BORROW_LOAD_FAST_BORROW, STORE_FAST_LOAD_FAST, STORE_FAST_STORE_FAST):
                arg1 = arg >> 4
                arg2 = arg & 15
                val1, argrepr1 = _get_name_info(arg1, self.varname_from_oparg)
                val2, argrepr2 = _get_name_info(arg2, self.varname_from_oparg)
                argrepr = argrepr1 + ', ' + argrepr2
                argval = (val1, val2)
            elif deop in haslocal or deop in hasfree:
                argval, argrepr = _get_name_info(arg, self.varname_from_oparg)
            elif deop in hascompare:
                argval = cmp_op[arg >> 5]
                argrepr = argval
                if arg & 16:
                    argrepr = f'bool({argrepr})'
            elif deop == CONVERT_VALUE:
                argval = (None, str, repr, ascii)[arg]
                argrepr = ('', 'str', 'repr', 'ascii')[arg]
            elif deop == SET_FUNCTION_ATTRIBUTE:
                argrepr = ', '.join((s for i, s in enumerate(FUNCTION_ATTR_FLAGS) if arg & 1 << i))
            elif deop == BINARY_OP:
                _, argrepr = _nb_ops[arg]
            elif deop == CALL_INTRINSIC_1:
                argrepr = _intrinsic_1_descs[arg]
            elif deop == CALL_INTRINSIC_2:
                argrepr = _intrinsic_2_descs[arg]
            elif deop == LOAD_COMMON_CONSTANT:
                obj = _common_constants[arg]
                if isinstance(obj, type):
                    argrepr = obj.__name__
                else:
                    argrepr = repr(obj)
            elif deop == LOAD_SPECIAL:
                argrepr = _special_method_names[arg]
            elif deop == IS_OP:
                argrepr = 'is not' if argval else 'is'
            elif deop == CONTAINS_OP:
                argrepr = 'not in' if argval else 'in'
        return (argval, argrepr)

def 取指令(x, *, first_line=None, show_caches=None, adaptive=False):
    """Iterator for the opcodes in methods, functions or code

    Generates a series of Instruction named tuples giving the details of
    each operations in the supplied code.

    If *first_line* is not None, it indicates the line number that should
    be reported for the first source line in the disassembled code.
    Otherwise, the source line information (if any) is taken directly from
    the disassembled code object.
    """
    co = _get_code_object(x)
    linestarts = dict(找行号起点(co))
    if first_line is not None:
        line_offset = first_line - co.co_firstlineno
    else:
        line_offset = 0
    original_code = co.co_code
    arg_resolver = 参数解析器(co_consts=co.co_consts, names=co.co_names, varname_from_oparg=co._varname_from_oparg, labels_map=_make_labels_map(original_code))
    return _get_instructions_bytes(_get_code_array(co, adaptive), linestarts=linestarts, line_offset=line_offset, co_positions=co.co_positions(), original_code=original_code, arg_resolver=arg_resolver)

def _get_const_value(op, arg, co_consts):
    """Helper to get the value of the const in a hasconst op.

       Returns the dereferenced constant if this is possible.
       Otherwise (if it is a LOAD_CONST and co_consts is not
       provided) returns the dis.UNKNOWN sentinel.
    """
    assert op in hasconst or op == LOAD_SMALL_INT
    if op == LOAD_SMALL_INT:
        return arg
    argval = UNKNOWN
    if co_consts is not None:
        argval = co_consts[arg]
    return argval

def _get_const_info(op, arg, co_consts):
    """Helper to get optional details about const references

       Returns the dereferenced constant and its repr if the value
       can be calculated.
       Otherwise returns the sentinel value dis.UNKNOWN for the value
       and an empty string for its repr.
    """
    argval = _get_const_value(op, arg, co_consts)
    argrepr = repr(argval) if argval is not UNKNOWN else ''
    return (argval, argrepr)

def _get_name_info(name_index, get_name, **extrainfo):
    """Helper to get optional details about named references

       Returns the dereferenced name as both value and repr if the name
       list is defined.
       Otherwise returns the sentinel value dis.UNKNOWN for the value
       and an empty string for its repr.
    """
    if get_name is not None:
        argval = get_name(name_index, **extrainfo)
        return (argval, argval)
    else:
        return (UNKNOWN, '')

def _parse_varint(iterator):
    b = next(iterator)
    val = b & 63
    while b & 64:
        val <<= 6
        b = next(iterator)
        val |= b & 63
    return val

def _parse_exception_table(code):
    iterator = iter(code.co_exceptiontable)
    entries = []
    try:
        while True:
            start = _parse_varint(iterator) * 2
            length = _parse_varint(iterator) * 2
            end = start + length
            target = _parse_varint(iterator) * 2
            dl = _parse_varint(iterator)
            depth = dl >> 1
            lasti = bool(dl & 1)
            entries.append(_ExceptionTableEntry(start, end, target, depth, lasti))
    except StopIteration:
        return entries

def _is_backward_jump(op):
    return opname[op] in ('JUMP_BACKWARD', 'JUMP_BACKWARD_NO_INTERRUPT', 'END_ASYNC_FOR')

def _get_instructions_bytes(code, linestarts=None, line_offset=0, co_positions=None, original_code=None, arg_resolver=None):
    """Iterate over the instructions in a bytecode string.

    Generates a sequence of Instruction namedtuples giving the details of each
    opcode.

    """
    original_code = original_code or code
    co_positions = co_positions or iter(())
    starts_line = False
    local_line_number = None
    line_number = None
    for 偏移, start_offset, op, 参数 in _unpack_opargs(original_code):
        if linestarts is not None:
            starts_line = 偏移 in linestarts
            if starts_line:
                local_line_number = linestarts[偏移]
            if local_line_number is not None:
                line_number = local_line_number + line_offset
            else:
                line_number = None
        positions = Positions(*next(co_positions, ()))
        deop = _deoptop(op)
        op = code[偏移]
        if arg_resolver:
            argval, argrepr = arg_resolver.get_argval_argrepr(op, 参数, 偏移)
        else:
            argval, argrepr = (参数, repr(参数))
        caches = _get_cache_size(_all_opname[deop])
        for _ in range(caches):
            next(co_positions, ())
        if caches:
            cache_info = []
            cache_offset = 偏移
            for name, size in _cache_format[opname[deop]].items():
                data = code[cache_offset + 2:cache_offset + 2 + 2 * size]
                cache_offset += size * 2
                cache_info.append((name, size, data))
        else:
            cache_info = None
        label = arg_resolver.get_label_for_offset(偏移) if arg_resolver else None
        yield 指令(_all_opname[op], op, 参数, argval, argrepr, 偏移, start_offset, starts_line, line_number, label, positions, cache_info)

def 反汇编代码(co, lasti=-1, *, file=None, show_caches=False, adaptive=False, show_offsets=False, show_positions=False):
    """Disassemble a code object."""
    linestarts = dict(找行号起点(co))
    exception_entries = _parse_exception_table(co)
    if show_positions:
        lineno_width = _get_positions_width(co)
    else:
        lineno_width = _get_lineno_width(linestarts)
    labels_map = _make_labels_map(co.co_code, exception_entries=exception_entries)
    label_width = 4 + len(str(len(labels_map)))
    formatter = 格式化器(file=file, lineno_width=lineno_width, offset_width=len(str(max(len(co.co_code) - 2, 9999))) if show_offsets else 0, label_width=label_width, show_caches=show_caches, show_positions=show_positions)
    arg_resolver = 参数解析器(co_consts=co.co_consts, names=co.co_names, varname_from_oparg=co._varname_from_oparg, labels_map=labels_map)
    _disassemble_bytes(_get_code_array(co, adaptive), lasti, linestarts, exception_entries=exception_entries, co_positions=co.co_positions(), original_code=co.co_code, arg_resolver=arg_resolver, formatter=formatter)

def _disassemble_recursive(co, *, file=None, depth=None, show_caches=False, adaptive=False, show_offsets=False, show_positions=False):
    反汇编代码(co, file=file, show_caches=show_caches, adaptive=adaptive, show_offsets=show_offsets, show_positions=show_positions)
    if depth is None or depth > 0:
        if depth is not None:
            depth = depth - 1
        for x in co.co_consts:
            if hasattr(x, 'co_code'):
                print(file=file)
                print('Disassembly of %r:' % (x,), file=file)
                _disassemble_recursive(x, file=file, depth=depth, show_caches=show_caches, adaptive=adaptive, show_offsets=show_offsets, show_positions=show_positions)

def _make_labels_map(original_code, exception_entries=()):
    jump_targets = set(找标签(original_code))
    labels = set(jump_targets)
    for start, end, target, _, _ in exception_entries:
        labels.add(start)
        labels.add(end)
        labels.add(target)
    labels = sorted(labels)
    labels_map = {偏移: i + 1 for i, 偏移 in enumerate(sorted(labels))}
    for e in exception_entries:
        e.start_label = labels_map[e.start]
        e.end_label = labels_map[e.end]
        e.target_label = labels_map[e.target]
    return labels_map
_NO_LINENO = '  --'

def _get_lineno_width(linestarts):
    if linestarts is None:
        return 0
    maxlineno = max(filter(None, linestarts.values()), default=-1)
    if maxlineno == -1:
        return 0
    lineno_width = max(3, len(str(maxlineno)))
    if lineno_width < len(_NO_LINENO) and None in linestarts.values():
        lineno_width = len(_NO_LINENO)
    return lineno_width

def _get_positions_width(code):
    has_value = False
    values_width = 0
    for positions in code.co_positions():
        has_value |= any((isinstance(p, int) for p in positions))
        width = sum((1 if p is None else len(str(p)) for p in positions))
        values_width = max(width, values_width)
    if has_value:
        return 1 + max(len(_NO_LINENO), 3 + values_width)
    return 0

def _disassemble_bytes(code, lasti=-1, linestarts=None, *, line_offset=0, exception_entries=(), co_positions=None, original_code=None, arg_resolver=None, formatter=None):
    assert formatter is not None
    assert arg_resolver is not None
    instrs = _get_instructions_bytes(code, linestarts=linestarts, line_offset=line_offset, co_positions=co_positions, original_code=original_code, arg_resolver=arg_resolver)
    打印指令(instrs, exception_entries, formatter, lasti=lasti)

def 打印指令(instrs, exception_entries, formatter, lasti=-1):
    for instr in instrs:
        is_current_instr = instr.offset <= lasti <= instr.offset + 2 * _get_cache_size(_all_opname[_deoptop(instr.opcode)])
        formatter.print_instruction(instr, is_current_instr)
    formatter.print_exception_table(exception_entries)

def _disassemble_str(source, **kwargs):
    """Compile the source string, then disassemble the code object."""
    _disassemble_recursive(_try_compile(source, '<dis>'), **kwargs)
disco = 反汇编代码
_INT_BITS = 32
_INT_OVERFLOW = 2 ** (_INT_BITS - 1)

def _unpack_opargs(code):
    extended_arg = 0
    extended_args_offset = 0
    caches = 0
    for i in range(0, len(code), 2):
        if caches:
            caches -= 1
            continue
        op = code[i]
        deop = _deoptop(op)
        caches = _get_cache_size(_all_opname[deop])
        if deop in hasarg:
            参数 = code[i + 1] | extended_arg
            extended_arg = 参数 << 8 if deop == EXTENDED_ARG else 0
            if extended_arg >= _INT_OVERFLOW:
                extended_arg -= 2 * _INT_OVERFLOW
        else:
            参数 = None
            extended_arg = 0
        if deop == EXTENDED_ARG:
            extended_args_offset += 1
            yield (i, i, op, 参数)
        else:
            start_offset = i - extended_args_offset * 2
            yield (i, start_offset, op, 参数)
            extended_args_offset = 0

def 找标签(code):
    """Detect all offsets in a byte code which are jump targets.

    Return the list of offsets.

    """
    labels = []
    for 偏移, _, op, 参数 in _unpack_opargs(code):
        if 参数 is not None:
            label = _get_jump_target(op, 参数, 偏移)
            if label is None:
                continue
            if label not in labels:
                labels.append(label)
    return labels

def 找行号起点(code):
    """Find the offsets in a byte code which are start of lines in the source.

    Generate pairs (offset, lineno)
    lineno will be an integer or None the offset does not have a source line.
    """
    lastline = False
    for start, end, line in code.co_lines():
        if line is not lastline:
            lastline = line
            yield (start, line)
    return

def _find_imports(co):
    """Find import statements in the code

    Generate triplets (name, level, fromlist) where
    name is the imported module and level, fromlist are
    the corresponding args to __import__.
    """
    IMPORT_NAME = opmap['IMPORT_NAME']
    consts = co.co_consts
    names = co.co_names
    opargs = [(op, 参数) for _, _, op, 参数 in _unpack_opargs(co.co_code) if op != EXTENDED_ARG]
    for i, (op, oparg) in enumerate(opargs):
        if op == IMPORT_NAME and i >= 2:
            from_op = opargs[i - 1]
            level_op = opargs[i - 2]
            if from_op[0] in hasconst and (level_op[0] in hasconst or level_op[0] == LOAD_SMALL_INT):
                level = _get_const_value(level_op[0], level_op[1], consts)
                fromlist = _get_const_value(from_op[0], from_op[1], consts)
                yield (names[oparg], level, fromlist)

def _find_store_names(co):
    """Find names of variables which are written in the code

    Generate sequence of strings
    """
    STORE_OPS = {opmap['STORE_NAME'], opmap['STORE_GLOBAL']}
    names = co.co_names
    for _, _, op, 参数 in _unpack_opargs(co.co_code):
        if op in STORE_OPS:
            yield names[参数]

class 字节码:
    """The bytecode operations of a piece of code

    Instantiate this with a function, method, other compiled object, string of
    code, or a code object (as returned by compile()).

    Iterating over this yields the bytecode operations as Instruction instances.
    """

    def __init__(self, x, *, first_line=None, current_offset=None, show_caches=False, adaptive=False, show_offsets=False, show_positions=False):
        self.codeobj = co = _get_code_object(x)
        if first_line is None:
            self.first_line = co.co_firstlineno
            self._line_offset = 0
        else:
            self.first_line = first_line
            self._line_offset = first_line - co.co_firstlineno
        self._linestarts = dict(找行号起点(co))
        self._original_object = x
        self.current_offset = current_offset
        self.exception_entries = _parse_exception_table(co)
        self.show_caches = show_caches
        self.adaptive = adaptive
        self.show_offsets = show_offsets
        self.show_positions = show_positions

    def __iter__(self):
        co = self.codeobj
        original_code = co.co_code
        labels_map = _make_labels_map(original_code, self.exception_entries)
        arg_resolver = 参数解析器(co_consts=co.co_consts, names=co.co_names, varname_from_oparg=co._varname_from_oparg, labels_map=labels_map)
        return _get_instructions_bytes(_get_code_array(co, self.adaptive), linestarts=self._linestarts, line_offset=self._line_offset, co_positions=co.co_positions(), original_code=original_code, arg_resolver=arg_resolver)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self._original_object)

    @classmethod
    def from_traceback(cls, tb, *, show_caches=False, adaptive=False):
        """ Construct a Bytecode from the given traceback """
        while tb.tb_next:
            tb = tb.tb_next
        return cls(tb.tb_frame.f_code, current_offset=tb.tb_lasti, show_caches=show_caches, adaptive=adaptive)

    def 信息(self):
        """Return formatted information about the code object."""
        return _format_code_info(self.codeobj)

    def 反汇编(self):
        """Return a formatted view of the bytecode operations."""
        co = self.codeobj
        if self.current_offset is not None:
            偏移 = self.current_offset
        else:
            偏移 = -1
        with io.StringIO() as output:
            code = _get_code_array(co, self.adaptive)
            offset_width = len(str(max(len(code) - 2, 9999))) if self.show_offsets else 0
            if self.show_positions:
                lineno_width = _get_positions_width(co)
            else:
                lineno_width = _get_lineno_width(self._linestarts)
            labels_map = _make_labels_map(co.co_code, self.exception_entries)
            label_width = 4 + len(str(len(labels_map)))
            formatter = 格式化器(file=output, lineno_width=lineno_width, offset_width=offset_width, label_width=label_width, line_offset=self._line_offset, show_caches=self.show_caches, show_positions=self.show_positions)
            arg_resolver = 参数解析器(co_consts=co.co_consts, names=co.co_names, varname_from_oparg=co._varname_from_oparg, labels_map=labels_map)
            _disassemble_bytes(code, linestarts=self._linestarts, line_offset=self._line_offset, lasti=偏移, exception_entries=self.exception_entries, co_positions=co.co_positions(), original_code=co.co_code, arg_resolver=arg_resolver, formatter=formatter)
            return output.getvalue()
_装类转发(字节码, {'dis': '反汇编', 'info': '信息'}, {'dis': '反汇编', 'info': '信息'})

def 主函数(args=None):
    import argparse
    parser = argparse.ArgumentParser(color=True)
    parser.add_argument('-C', '--show-caches', action='store_true', help='show inline caches')
    parser.add_argument('-O', '--show-offsets', action='store_true', help='show instruction offsets')
    parser.add_argument('-P', '--show-positions', action='store_true', help='show instruction positions')
    parser.add_argument('-S', '--specialized', action='store_true', help='show specialized bytecode')
    parser.add_argument('infile', nargs='?', default='-')
    args = parser.parse_args(args=args)
    if args.infile == '-':
        name = '<stdin>'
        source = sys.stdin.buffer.read()
    else:
        name = args.infile
        with open(args.infile, 'rb') as infile:
            source = infile.read()
    code = compile(source, name, 'exec')
    反汇编(code, show_caches=args.show_caches, adaptive=args.specialized, show_offsets=args.show_offsets, show_positions=args.show_positions)
if __name__ == '__main__':
    主函数()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'ArgResolver': '参数解析器',
    'Bytecode': '字节码',
    'Formatter': '格式化器',
    'Instruction': '指令',
    'code_info': '代码信息',
    'dis': '反汇编',
    'disassemble': '反汇编代码',
    'distb': '反汇编回溯',
    'findlabels': '找标签',
    'findlinestarts': '找行号起点',
    'get_instructions': '取指令',
    'main': '主函数',
    'pretty_flags': '美化标志',
    'print_instructions': '打印指令',
    'show_code': '显示代码',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '字节码': {
        'dis': '反汇编',
        'info': '信息',
    },
    '指令': {
        'end_offset': '结束偏移',
        'is_jump_target': '是跳转目标吗',
        'jump_target': '跳转目标',
    },
    '格式化器': {
        'print_exception_table': '打印异常表',
        'print_instruction': '打印一条指令',
        'print_instruction_line': '打印指令行',
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
    '字节码': {
        'dis': '反汇编',
        'info': '信息',
    },
    '指令': {
        'arg': '参数',
        'end_offset': '结束偏移',
        'is_jump_target': '是跳转目标吗',
        'jump_target': '跳转目标',
        'offset': '偏移',
        'opcode': '操作码',
    },
    '格式化器': {
        'print_exception_table': '打印异常表',
        'print_instruction': '打印一条指令',
        'print_instruction_line': '打印指令行',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
