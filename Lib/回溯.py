# -*- coding: utf-8 -*-
"""回溯 —— 汉语库（由 tools/汉化库.py 从 Lib/traceback.py 机械生成，**不要手改**）。

英文库 Lib/traceback.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 回溯
"""


"""Extract, format and print information about Python stack traces."""
_英文原名表 = {'BUILTIN_EXCEPTION_LIMIT': '内置异常上限', 'FrameSummary': '帧摘要', 'StackSummary': '栈摘要', 'TracebackException': '回溯异常', 'clear_frames': '清帧', 'extract_stack': '提取栈', 'extract_tb': '提取回溯', 'format_exc': '格式化当前异常', 'format_exception': '格式化异常', 'format_exception_only': '只格式化异常', 'format_list': '格式化表', 'format_stack': '格式化栈', 'format_tb': '格式化回溯', 'print_exc': '打印当前异常', 'print_exception': '打印异常', 'print_last': '打印最后一个', 'print_list': '打印表', 'print_stack': '打印栈', 'print_tb': '打印回溯', 'walk_stack': '遍历栈', 'walk_tb': '遍历回溯'}

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
import collections.abc
import itertools
import linecache
import sys
import textwrap
import warnings
import codeop
import keyword
import tokenize
import io
import _colorize
from contextlib import suppress
_zh_模块 = None
_zh_找过 = False

def _zh():
    global _zh_模块, _zh_找过
    if not _zh_找过:
        _zh_找过 = True
        try:
            import zh_traceback as _m
        except Exception:
            _m = None
        _zh_模块 = _m
    return _zh_模块

def _框架(英文模板, *参数):
    """回溯框架行的固定说法。表坏了、没登记、en 模式，都原样返回英文。

    ⚠ 这里**必须**自己兜住异常（照 D-027）：`_框架` 在格式化回溯的最里层，
      内存紧张时翻译那几步的分配会失败；要是让异常冒出去，
      就会变成「打印报错」这件事本身又报错 → 再打印 → 递归到爆栈。
      实测 `test_atexit` 的 set_nomemory(0) 就是这么挂的（退出码 0xC00000FD）。
    """
    _m = _zh()
    if _m is not None:
        try:
            return _m.框架(英文模板, *参数)
        except BaseException:
            pass
    return 英文模板.format(*参数)

def _显示异常名(名):
    """显示用的异常名。`module.类名` 也能翻（只换类名那部分）。

    **只影响显示**：`type.__name__` / `__qualname__` / `__module__` 一个字没动，
    `TracebackException.exc_type_str` 也一个字没动 —— 所以 pickle、inspect、
    logging、`except` 匹配统统照旧。查不到就原样返回。
    """
    _m = _zh()
    if _m is None or 名 is None:
        return 名
    try:
        return _m.翻显示名(名)
    except Exception:
        return 名
__all__ = ['extract_stack', 'extract_tb', 'format_exception', 'format_exception_only', 'format_list', 'format_stack', 'format_tb', 'print_exc', 'format_exc', 'print_exception', 'print_last', 'print_stack', 'print_tb', 'clear_frames', 'FrameSummary', 'StackSummary', 'TracebackException', 'walk_stack', 'walk_tb', 'print_list']

def 打印表(extracted_list, file=None):
    """Print the list of tuples as returned by extract_tb() or
    extract_stack() as a formatted stack trace to the given file."""
    if file is None:
        file = sys.stderr
    for item in 栈摘要.从表建(extracted_list).format():
        print(item, file=file, end='')

def 格式化表(extracted_list):
    """Format a list of tuples or FrameSummary objects for printing.

    Given a list of tuples or FrameSummary objects as returned by
    extract_tb() or extract_stack(), return a list of strings ready
    for printing.

    Each string in the resulting list corresponds to the item with the
    same index in the argument list.  Each string ends in a newline;
    the strings may contain internal newlines as well, for those items
    whose source text line is not None.
    """
    return 栈摘要.从表建(extracted_list).format()

def 打印回溯(tb, limit=None, file=None):
    """Print up to 'limit' stack trace entries from the traceback 'tb'.

    If 'limit' is omitted or None, all entries are printed.  If 'file'
    is omitted or None, the output goes to sys.stderr; otherwise
    'file' should be an open file or file-like object with a write()
    method.
    """
    打印表(提取回溯(tb, limit=limit), file=file)

def 格式化回溯(tb, limit=None):
    """A shorthand for 'format_list(extract_tb(tb, limit))'."""
    return 提取回溯(tb, limit=limit).format()

def 提取回溯(tb, limit=None):
    """
    Return a StackSummary object representing a list of
    pre-processed entries from traceback.

    This is useful for alternate formatting of stack traces.  If
    'limit' is omitted or None, all entries are extracted.  A
    pre-processed stack trace entry is a FrameSummary object
    representing the information that is usually printed for a
    stack trace. The line attribute is a string with
    leading and trailing whitespace stripped; if the source is not
    available the corresponding attribute is None.
    """
    return 栈摘要._extract_from_extended_frame_gen(_walk_tb_with_full_positions(tb), limit=limit)
_cause_message = '\nThe above exception was the direct cause of the following exception:\n\n'
_context_message = '\nDuring handling of the above exception, another exception occurred:\n\n'

class _Sentinel:

    def __repr__(self):
        return '<implicit>'
_sentinel = _Sentinel()

def _parse_value_tb(exc, value, tb):
    if (value is _sentinel) != (tb is _sentinel):
        raise ValueError('Both or neither of value and tb must be given')
    if value is tb is _sentinel:
        if exc is not None:
            if isinstance(exc, BaseException):
                return (exc, exc.__traceback__)
            raise TypeError(f'Exception expected for value, {type(exc).__name__} found')
        else:
            return (None, None)
    return (value, tb)

def 打印异常(exc, /, value=_sentinel, tb=_sentinel, limit=None, file=None, chain=True, **kwargs):
    """Print exception up to 'limit' stack trace entries from 'tb' to 'file'.

    This differs from print_tb() in the following ways: (1) if
    traceback is not None, it prints a header "Traceback (most recent
    call last):"; (2) it prints the exception type and value after the
    stack trace; (3) if type is SyntaxError and value has the
    appropriate format, it prints the line where the syntax error
    occurred with a caret on the next line indicating the approximate
    position of the error.
    """
    colorize = kwargs.get('colorize', False)
    value, tb = _parse_value_tb(exc, value, tb)
    te = 回溯异常(type(value), value, tb, limit=limit, compact=True)
    te.print(file=file, chain=chain, colorize=colorize)
内置异常上限 = object()

def _print_exception_bltin(exc, /):
    file = sys.stderr if sys.stderr is not None else sys.__stderr__
    colorize = _colorize.can_colorize(file=file)
    return 打印异常(exc, limit=内置异常上限, file=file, colorize=colorize)

def 格式化异常(exc, /, value=_sentinel, tb=_sentinel, limit=None, chain=True, **kwargs):
    """Format a stack trace and the exception information.

    The arguments have the same meaning as the corresponding arguments
    to print_exception().  The return value is a list of strings, each
    ending in a newline and some containing internal newlines.  When
    these lines are concatenated and printed, exactly the same text is
    printed as does print_exception().
    """
    colorize = kwargs.get('colorize', False)
    value, tb = _parse_value_tb(exc, value, tb)
    te = 回溯异常(type(value), value, tb, limit=limit, compact=True)
    return list(te.format(chain=chain, colorize=colorize))

def 只格式化异常(exc, /, value=_sentinel, *, show_group=False, **kwargs):
    """Format the exception part of a traceback.

    The return value is a list of strings, each ending in a newline.

    The list contains the exception's message, which is
    normally a single string; however, for :exc:`SyntaxError` exceptions, it
    contains several lines that (when printed) display detailed information
    about where the syntax error occurred. Following the message, the list
    contains the exception's ``__notes__``.

    When *show_group* is ``True``, and the exception is an instance of
    :exc:`BaseExceptionGroup`, the nested exceptions are included as
    well, recursively, with indentation relative to their nesting depth.
    """
    colorize = kwargs.get('colorize', False)
    if value is _sentinel:
        value = exc
    te = 回溯异常(type(value), value, None, compact=True)
    return list(te.format_exception_only(show_group=show_group, colorize=colorize))

def _format_final_exc_line(etype, value, *, insert_final_newline=True, colorize=False):
    valuestr = _safe_string(value, 'exception')
    _m = _zh()
    if _m is not None:
        try:
            if etype is not None:
                etype = _m.翻异常名(etype)
            valuestr = _m.翻正文(valuestr)
        except Exception:
            pass
    end_char = '\n' if insert_final_newline else ''
    if colorize:
        theme = _colorize.get_theme(force_color=True).traceback
    else:
        theme = _colorize.get_theme(force_no_color=True).traceback
    if value is None or not valuestr:
        行 = f'{theme.type}{etype}{theme.reset}{end_char}'
    else:
        行 = f'{theme.type}{etype}{theme.reset}: {theme.message}{valuestr}{theme.reset}{end_char}'
    return 行

def _safe_string(value, what, func=str):
    try:
        return func(value)
    except:
        return f'<{what} {func.__name__}() failed>'

def 打印当前异常(limit=None, file=None, chain=True):
    """Shorthand for 'print_exception(sys.exception(), limit=limit, file=file, chain=chain)'."""
    打印异常(sys.exception(), limit=limit, file=file, chain=chain)

def 格式化当前异常(limit=None, chain=True):
    """Like print_exc() but return a string."""
    return ''.join(格式化异常(sys.exception(), limit=limit, chain=chain))

def 打印最后一个(limit=None, file=None, chain=True):
    """This is a shorthand for 'print_exception(sys.last_exc, limit=limit, file=file, chain=chain)'."""
    if not hasattr(sys, 'last_exc') and (not hasattr(sys, 'last_type')):
        raise ValueError('no last exception')
    if hasattr(sys, 'last_exc'):
        打印异常(sys.last_exc, limit=limit, file=file, chain=chain)
    else:
        打印异常(sys.last_type, sys.last_value, sys.last_traceback, limit=limit, file=file, chain=chain)

def 打印栈(f=None, limit=None, file=None):
    """Print a stack trace from its invocation point.

    The optional 'f' argument can be used to specify an alternate
    stack frame at which to start. The optional 'limit' and 'file'
    arguments have the same meaning as for print_exception().
    """
    if f is None:
        f = sys._getframe().f_back
    打印表(提取栈(f, limit=limit), file=file)

def 格式化栈(f=None, limit=None):
    """Shorthand for 'format_list(extract_stack(f, limit))'."""
    if f is None:
        f = sys._getframe().f_back
    return 格式化表(提取栈(f, limit=limit))

def 提取栈(f=None, limit=None):
    """Extract the raw traceback from the current stack frame.

    The return value has the same format as for extract_tb().  The
    optional 'f' and 'limit' arguments have the same meaning as for
    print_stack().  Each item in the list is a FrameSummary object,
    and the entries are in order from oldest to newest stack frame.
    """
    if f is None:
        f = sys._getframe().f_back
    stack = 栈摘要.提取(遍历栈(f), limit=limit)
    stack.reverse()
    return stack

def 清帧(tb):
    """Clear all references to local variables in the frames of a traceback."""
    while tb is not None:
        try:
            tb.tb_frame.clear()
        except RuntimeError:
            pass
        tb = tb.tb_next

class 帧摘要:
    """Information about a single frame from a traceback.

    - :attr:`filename` The filename for the frame.
    - :attr:`lineno` The line within filename for the frame that was
      active when the frame was captured.
    - :attr:`name` The name of the function or method that was executing
      when the frame was captured.
    - :attr:`line` The text from the linecache module for the line
      of code that was running when the frame was captured.
    - :attr:`locals` Either None if locals were not supplied, or a dict
      mapping the name to the repr() of the variable.
    """
    __slots__ = ('filename', 'lineno', 'end_lineno', 'colno', 'end_colno', 'name', '_lines', '_lines_dedented', 'locals', '_code')

    def __init__(self, filename, lineno, name, *, lookup_line=True, locals=None, line=None, end_lineno=None, colno=None, end_colno=None, **kwargs):
        """Construct a FrameSummary.

        :param lookup_line: If True, `linecache` is consulted for the source
            code line. Otherwise, the line will be looked up when first needed.
        :param locals: If supplied the frame locals, which will be captured as
            object representations.
        :param line: If provided, use this instead of looking up the line in
            the linecache.
        """
        self.filename = filename
        self.lineno = lineno
        self.end_lineno = lineno if end_lineno is None else end_lineno
        self.colno = colno
        self.end_colno = end_colno
        self.name = name
        self._code = kwargs.get('_code')
        self._lines = line
        self._lines_dedented = None
        if lookup_line:
            self.行
        self.locals = {k: _safe_string(v, 'local', func=repr) for k, v in locals.items()} if locals else None

    def __eq__(self, other):
        if isinstance(other, 帧摘要):
            return self.filename == other.filename and self.lineno == other.lineno and (self.name == other.name) and (self.locals == other.locals)
        if isinstance(other, tuple):
            return (self.filename, self.lineno, self.name, self.行) == other
        return NotImplemented

    def __getitem__(self, pos):
        return (self.filename, self.lineno, self.name, self.行)[pos]

    def __iter__(self):
        return iter([self.filename, self.lineno, self.name, self.行])

    def __repr__(self):
        return '<FrameSummary file {filename}, line {lineno} in {name}>'.format(filename=self.filename, lineno=self.lineno, name=self.name)

    def __len__(self):
        return 4

    def _set_lines(self):
        if self._lines is None and self.lineno is not None and (self.end_lineno is not None):
            lines = []
            for lineno in range(self.lineno, self.end_lineno + 1):
                行 = linecache.getline(self.filename, lineno).rstrip()
                if not 行 and self._code is not None and self.filename.startswith('<'):
                    行 = linecache._getline_from_code(self._code, lineno).rstrip()
                lines.append(行)
            self._lines = '\n'.join(lines) + '\n'

    @property
    def _original_lines(self):
        self._set_lines()
        return self._lines

    @property
    def _dedented_lines(self):
        self._set_lines()
        if self._lines_dedented is None and self._lines is not None:
            self._lines_dedented = textwrap.dedent(self._lines)
        return self._lines_dedented

    @property
    def 行(self):
        self._set_lines()
        if self._lines is None:
            return None
        return self._lines.partition('\n')[0].strip()
_装类转发(帧摘要, {'line': '行'}, {'line': '行'})

def 遍历栈(f):
    """Walk a stack yielding the frame and line number for each frame.

    This will follow f.f_back from the given frame. If no frame is given, the
    current stack is used. Usually used with StackSummary.extract.
    """
    if f is None:
        f = sys._getframe().f_back

    def walk_stack_generator(frame):
        while frame is not None:
            yield (frame, frame.f_lineno)
            frame = frame.f_back
    return walk_stack_generator(f)

def 遍历回溯(tb):
    """Walk a traceback yielding the frame and line number for each frame.

    This will follow tb.tb_next (and thus is in the opposite order to
    walk_stack). Usually used with StackSummary.extract.
    """
    while tb is not None:
        yield (tb.tb_frame, tb.tb_lineno)
        tb = tb.tb_next

def _walk_tb_with_full_positions(tb):
    while tb is not None:
        positions = _get_code_position(tb.tb_frame.f_code, tb.tb_lasti)
        if positions[0] is None:
            yield (tb.tb_frame, (tb.tb_lineno,) + positions[1:])
        else:
            yield (tb.tb_frame, positions)
        tb = tb.tb_next

def _get_code_position(code, instruction_index):
    if instruction_index < 0:
        return (None, None, None, None)
    positions_gen = code.co_positions()
    return next(itertools.islice(positions_gen, instruction_index // 2, None))
_RECURSIVE_CUTOFF = 3

class 栈摘要(list):
    """A list of FrameSummary objects, representing a stack of frames."""

    @classmethod
    def 提取(klass, frame_gen, *, limit=None, lookup_lines=True, capture_locals=False):
        """Create a StackSummary from a traceback or stack object.

        :param frame_gen: A generator that yields (frame, lineno) tuples
            whose summaries are to be included in the stack.
        :param limit: None to include all frames or the number of frames to
            include.
        :param lookup_lines: If True, lookup lines for each frame immediately,
            otherwise lookup is deferred until the frame is rendered.
        :param capture_locals: If True, the local variables from each frame will
            be captured as object representations into the FrameSummary.
        """

        def extended_frame_gen():
            for f, lineno in frame_gen:
                yield (f, (lineno, None, None, None))
        return klass._extract_from_extended_frame_gen(extended_frame_gen(), limit=limit, lookup_lines=lookup_lines, capture_locals=capture_locals)

    @classmethod
    def _extract_from_extended_frame_gen(klass, frame_gen, *, limit=None, lookup_lines=True, capture_locals=False):
        builtin_limit = limit is 内置异常上限
        if limit is None or builtin_limit:
            limit = getattr(sys, 'tracebacklimit', None)
            if limit is not None and limit < 0:
                limit = 0
        if limit is not None:
            if builtin_limit:
                frame_gen = tuple(frame_gen)
                frame_gen = frame_gen[len(frame_gen) - limit:]
            elif limit >= 0:
                frame_gen = itertools.islice(frame_gen, limit)
            else:
                frame_gen = collections.deque(frame_gen, maxlen=-limit)
        result = klass()
        fnames = set()
        for f, (lineno, end_lineno, colno, end_colno) in frame_gen:
            co = f.f_code
            filename = co.co_filename
            name = co.co_name
            fnames.add(filename)
            linecache.lazycache(filename, f.f_globals)
            if capture_locals:
                f_locals = f.f_locals
            else:
                f_locals = None
            result.append(帧摘要(filename, lineno, name, lookup_line=False, locals=f_locals, end_lineno=end_lineno, colno=colno, end_colno=end_colno, _code=f.f_code))
        for filename in fnames:
            linecache.checkcache(filename)
        if lookup_lines:
            for f in result:
                f.line
        return result

    @classmethod
    def 从表建(klass, a_list):
        """
        Create a StackSummary object from a supplied list of
        FrameSummary objects or old-style list of tuples.
        """
        result = 栈摘要()
        for frame in a_list:
            if isinstance(frame, 帧摘要):
                result.append(frame)
            else:
                filename, lineno, name, 行 = frame
                result.append(帧摘要(filename, lineno, name, line=行))
        return result

    def format_frame_summary(self, frame_summary, **kwargs):
        """Format the lines for a single FrameSummary.

        Returns a string representing one frame involved in the stack. This
        gets called for every frame to be printed in the stack summary.
        """
        colorize = kwargs.get('colorize', False)
        row = []
        filename = frame_summary.filename
        if frame_summary.filename.startswith('<stdin-') and frame_summary.filename.endswith('>'):
            filename = '<stdin>'
        if colorize:
            theme = _colorize.get_theme(force_color=True).traceback
        else:
            theme = _colorize.get_theme(force_no_color=True).traceback
        row.append(_框架('  File {}"{}"{}, line {}{}{}, in {}{}{}\n', theme.filename, filename, theme.reset, theme.line_no, frame_summary.lineno, theme.reset, theme.frame, frame_summary.name, theme.reset))
        if frame_summary._dedented_lines and frame_summary._dedented_lines.strip():
            if frame_summary.colno is None or frame_summary.end_colno is None:
                row.append(textwrap.indent(frame_summary.line, '    ') + '\n')
            else:
                all_lines_original = frame_summary._original_lines.splitlines()
                first_line = all_lines_original[0]
                last_line = all_lines_original[frame_summary.end_lineno - frame_summary.lineno]
                start_offset = _byte_offset_to_character_offset(first_line, frame_summary.colno)
                end_offset = _byte_offset_to_character_offset(last_line, frame_summary.end_colno)
                all_lines = frame_summary._dedented_lines.splitlines()[:frame_summary.end_lineno - frame_summary.lineno + 1]
                dedent_characters = len(first_line) - len(all_lines[0])
                start_offset = max(0, start_offset - dedent_characters)
                end_offset = max(0, end_offset - dedent_characters)
                dp_start_offset = _display_width(all_lines[0], offset=start_offset)
                dp_end_offset = _display_width(all_lines[-1], offset=end_offset)
                segment = '\n'.join(all_lines)
                segment = segment[start_offset:len(segment) - (len(all_lines[-1]) - end_offset)]
                anchors = None
                show_carets = False
                with suppress(Exception):
                    anchors = _extract_caret_anchors_from_line_segment(segment)
                show_carets = self._should_show_carets(start_offset, end_offset, all_lines, anchors)
                result = []
                significant_lines = {0, len(all_lines) - 1}
                anchors_left_end_offset = 0
                anchors_right_start_offset = 0
                primary_char = '^'
                secondary_char = '^'
                if anchors:
                    anchors_left_end_offset = anchors.left_end_offset
                    anchors_right_start_offset = anchors.right_start_offset
                    if anchors.left_end_lineno == 0:
                        anchors_left_end_offset += start_offset
                    if anchors.right_start_lineno == 0:
                        anchors_right_start_offset += start_offset
                    anchors_left_end_offset = _display_width(all_lines[anchors.left_end_lineno], offset=anchors_left_end_offset)
                    anchors_right_start_offset = _display_width(all_lines[anchors.right_start_lineno], offset=anchors_right_start_offset)
                    primary_char = anchors.primary_char
                    secondary_char = anchors.secondary_char
                    significant_lines.update(range(anchors.left_end_lineno - 1, anchors.left_end_lineno + 2))
                    significant_lines.update(range(anchors.right_start_lineno - 1, anchors.right_start_lineno + 2))
                significant_lines.discard(-1)
                significant_lines.discard(len(all_lines))

                def output_line(lineno):
                    """output all_lines[lineno] along with carets"""
                    result.append(all_lines[lineno] + '\n')
                    if not show_carets:
                        return
                    num_spaces = len(all_lines[lineno]) - len(all_lines[lineno].lstrip())
                    carets = []
                    num_carets = dp_end_offset if lineno == len(all_lines) - 1 else _display_width(all_lines[lineno])
                    for col in range(num_carets):
                        if col < num_spaces or (lineno == 0 and col < dp_start_offset):
                            carets.append(' ')
                        elif anchors and (lineno > anchors.left_end_lineno or (lineno == anchors.left_end_lineno and col >= anchors_left_end_offset)) and (lineno < anchors.right_start_lineno or (lineno == anchors.right_start_lineno and col < anchors_right_start_offset)):
                            carets.append(secondary_char)
                        else:
                            carets.append(primary_char)
                    if colorize:
                        行 = result[-1]
                        colorized_line_parts = []
                        colorized_carets_parts = []
                        for color, group in itertools.groupby(itertools.zip_longest(行, carets, fillvalue=''), key=lambda x: x[1]):
                            caret_group = list(group)
                            if color == '^':
                                colorized_line_parts.append(theme.error_highlight + ''.join((char for char, _ in caret_group)) + theme.reset)
                                colorized_carets_parts.append(theme.error_highlight + ''.join((caret for _, caret in caret_group)) + theme.reset)
                            elif color == '~':
                                colorized_line_parts.append(theme.error_range + ''.join((char for char, _ in caret_group)) + theme.reset)
                                colorized_carets_parts.append(theme.error_range + ''.join((caret for _, caret in caret_group)) + theme.reset)
                            else:
                                colorized_line_parts.append(''.join((char for char, _ in caret_group)))
                                colorized_carets_parts.append(''.join((caret for _, caret in caret_group)))
                        colorized_line = ''.join(colorized_line_parts)
                        colorized_carets = ''.join(colorized_carets_parts)
                        result[-1] = colorized_line
                        result.append(colorized_carets + '\n')
                    else:
                        result.append(''.join(carets) + '\n')
                sig_lines_list = sorted(significant_lines)
                for i, lineno in enumerate(sig_lines_list):
                    if i:
                        linediff = lineno - sig_lines_list[i - 1]
                        if linediff == 2:
                            output_line(lineno - 1)
                        elif linediff > 2:
                            result.append(f'...<{linediff - 1} lines>...\n')
                    output_line(lineno)
                row.append(textwrap.indent(textwrap.dedent(''.join(result)), '    ', lambda line: True))
        if frame_summary.locals:
            for name, value in sorted(frame_summary.locals.items()):
                row.append('    {name} = {value}\n'.format(name=name, value=value))
        return ''.join(row)

    def _should_show_carets(self, start_offset, end_offset, all_lines, anchors):
        with suppress(SyntaxError, ImportError):
            import ast
            tree = ast.parse('\n'.join(all_lines))
            if not tree.body:
                return False
            statement = tree.body[0]
            value = None

            def _spawns_full_line(value):
                return value.lineno == 1 and value.end_lineno == len(all_lines) and (value.col_offset == start_offset) and (value.end_col_offset == end_offset)
            match statement:
                case ast.Return(value=ast.Call()):
                    if isinstance(statement.value.func, ast.Name):
                        value = statement.value
                case ast.Assign(value=ast.Call()):
                    if len(statement.targets) == 1 and isinstance(statement.targets[0], ast.Name):
                        value = statement.value
            if value is not None and _spawns_full_line(value):
                return False
        if anchors:
            return True
        if all_lines[0][:start_offset].lstrip() or all_lines[-1][end_offset:].rstrip():
            return True
        return False

    def format(self, **kwargs):
        """Format the stack ready for printing.

        Returns a list of strings ready for printing.  Each string in the
        resulting list corresponds to a single frame from the stack.
        Each string ends in a newline; the strings may contain internal
        newlines as well, for those items with source text lines.

        For long sequences of the same frame and line, the first few
        repetitions are shown, followed by a summary line stating the exact
        number of further repetitions.
        """
        colorize = kwargs.get('colorize', False)
        result = []
        last_file = None
        last_line = None
        last_name = None
        count = 0
        for frame_summary in self:
            formatted_frame = self.format_frame_summary(frame_summary, colorize=colorize)
            if formatted_frame is None:
                continue
            if last_file is None or last_file != frame_summary.filename or last_line is None or (last_line != frame_summary.lineno) or (last_name is None) or (last_name != frame_summary.name):
                if count > _RECURSIVE_CUTOFF:
                    count -= _RECURSIVE_CUTOFF
                    result.append(_框架('  [Previous line repeated {} more time{}]\n', count, 's' if count > 1 else ''))
                last_file = frame_summary.filename
                last_line = frame_summary.lineno
                last_name = frame_summary.name
                count = 0
            count += 1
            if count > _RECURSIVE_CUTOFF:
                continue
            result.append(formatted_frame)
        if count > _RECURSIVE_CUTOFF:
            count -= _RECURSIVE_CUTOFF
            result.append(_框架('  [Previous line repeated {} more time{}]\n', count, 's' if count > 1 else ''))
        return result
_装类转发(栈摘要, {'extract': '提取', 'from_list': '从表建'}, {'extract': '提取', 'from_list': '从表建'})

def _byte_offset_to_character_offset(str, offset):
    as_utf8 = str.encode('utf-8')
    return len(as_utf8[:offset].decode('utf-8', errors='replace'))
_Anchors = collections.namedtuple('_Anchors', ['left_end_lineno', 'left_end_offset', 'right_start_lineno', 'right_start_offset', 'primary_char', 'secondary_char'], defaults=['~', '^'])

def _extract_caret_anchors_from_line_segment(segment):
    """
    Given source code `segment` corresponding to a FrameSummary, determine:
        - for binary ops, the location of the binary op
        - for indexing and function calls, the location of the brackets.
    `segment` is expected to be a valid Python expression.
    """
    import ast
    try:
        tree = ast.parse(f'(\n{segment}\n)')
    except SyntaxError:
        return None
    if len(tree.body) != 1:
        return None
    lines = segment.splitlines()

    def normalize(lineno, offset):
        """Get character index given byte offset"""
        return _byte_offset_to_character_offset(lines[lineno], offset)

    def next_valid_char(lineno, col):
        """Gets the next valid character index in `lines`, if
        the current location is not valid. Handles empty lines.
        """
        while lineno < len(lines) and col >= len(lines[lineno]):
            col = 0
            lineno += 1
        assert lineno < len(lines) and col < len(lines[lineno])
        return (lineno, col)

    def increment(lineno, col):
        """Get the next valid character index in `lines`."""
        col += 1
        lineno, col = next_valid_char(lineno, col)
        return (lineno, col)

    def nextline(lineno, col):
        """Get the next valid character at least on the next line"""
        col = 0
        lineno += 1
        lineno, col = next_valid_char(lineno, col)
        return (lineno, col)

    def increment_until(lineno, col, stop):
        """Get the next valid non-"\\#" character that satisfies the `stop` predicate"""
        while True:
            ch = lines[lineno][col]
            if ch in '\\#':
                lineno, col = nextline(lineno, col)
            elif not stop(ch):
                lineno, col = increment(lineno, col)
            else:
                break
        return (lineno, col)

    def setup_positions(expr, force_valid=True):
        """Get the lineno/col position of the end of `expr`. If `force_valid` is True,
        forces the position to be a valid character (e.g. if the position is beyond the
        end of the line, move to the next line)
        """
        lineno = expr.end_lineno - 2
        col = normalize(lineno, expr.end_col_offset)
        return next_valid_char(lineno, col) if force_valid else (lineno, col)
    statement = tree.body[0]
    match statement:
        case ast.Expr(expr):
            match expr:
                case ast.BinOp():
                    lineno, col = setup_positions(expr.left)
                    lineno, col = increment_until(lineno, col, lambda x: not x.isspace() and x != ')')
                    right_col = col + 1
                    if right_col < len(lines[lineno]) and (expr.right.lineno - 2 > lineno or right_col < normalize(expr.right.lineno - 2, expr.right.col_offset)) and (not (ch := lines[lineno][right_col]).isspace()) and (ch not in '\\#'):
                        right_col += 1
                    return _Anchors(lineno, col, lineno, right_col)
                case ast.Subscript():
                    left_lineno, left_col = setup_positions(expr.value)
                    left_lineno, left_col = increment_until(left_lineno, left_col, lambda x: x == '[')
                    right_lineno, right_col = setup_positions(expr, force_valid=False)
                    return _Anchors(left_lineno, left_col, right_lineno, right_col)
                case ast.Call():
                    left_lineno, left_col = setup_positions(expr.func)
                    left_lineno, left_col = increment_until(left_lineno, left_col, lambda x: x == '(')
                    right_lineno, right_col = setup_positions(expr, force_valid=False)
                    return _Anchors(left_lineno, left_col, right_lineno, right_col)
    return None
_WIDE_CHAR_SPECIFIERS = 'WF'

def _display_width(line, offset=None):
    """Calculate the amount of width space the given source
    code segment might take if it were to be displayed on a fixed
    width output device. Supports wide unicode characters and emojis."""
    if offset is None:
        offset = len(line)
    if line.isascii():
        return offset
    import unicodedata
    return sum((2 if unicodedata.east_asian_width(char) in _WIDE_CHAR_SPECIFIERS else 1 for char in line[:offset]))

class _ExceptionPrintContext:

    def __init__(self):
        self.seen = set()
        self.exception_group_depth = 0
        self.need_close = False

    def indent(self):
        return ' ' * (2 * self.exception_group_depth)

    def emit(self, text_gen, margin_char=None):
        if margin_char is None:
            margin_char = '|'
        indent_str = self.indent()
        if self.exception_group_depth:
            indent_str += margin_char + ' '
        if isinstance(text_gen, str):
            yield textwrap.indent(text_gen, indent_str, lambda line: True)
        else:
            for text in text_gen:
                yield textwrap.indent(text, indent_str, lambda line: True)

class 回溯异常:
    """An exception ready for rendering.

    The traceback module captures enough attributes from the original exception
    to this intermediary form to ensure that no references are held, while
    still being able to fully print or format it.

    max_group_width and max_group_depth control the formatting of exception
    groups. The depth refers to the nesting level of the group, and the width
    refers to the size of a single exception group's exceptions array. The
    formatted output is truncated when either limit is exceeded.

    Use `from_exception` to create TracebackException instances from exception
    objects, or the constructor to create TracebackException instances from
    individual components.

    - :attr:`__cause__` A TracebackException of the original *__cause__*.
    - :attr:`__context__` A TracebackException of the original *__context__*.
    - :attr:`exceptions` For exception groups - a list of TracebackException
      instances for the nested *exceptions*.  ``None`` for other exceptions.
    - :attr:`__suppress_context__` The *__suppress_context__* value from the
      original exception.
    - :attr:`stack` A `StackSummary` representing the traceback.
    - :attr:`exc_type` (deprecated) The class of the original traceback.
    - :attr:`exc_type_str` String display of exc_type
    - :attr:`filename` For syntax errors - the filename where the error
      occurred.
    - :attr:`lineno` For syntax errors - the linenumber where the error
      occurred.
    - :attr:`end_lineno` For syntax errors - the end linenumber where the error
      occurred. Can be `None` if not present.
    - :attr:`text` For syntax errors - the text where the error
      occurred.
    - :attr:`offset` For syntax errors - the offset into the text where the
      error occurred.
    - :attr:`end_offset` For syntax errors - the end offset into the text where
      the error occurred. Can be `None` if not present.
    - :attr:`msg` For syntax errors - the compiler error message.
    """

    def __init__(self, exc_type, exc_value, exc_traceback, *, limit=None, lookup_lines=True, capture_locals=False, compact=False, max_group_width=15, max_group_depth=10, save_exc_type=True, _seen=None):
        is_recursive_call = _seen is not None
        if _seen is None:
            _seen = set()
        _seen.add(id(exc_value))
        self.max_group_width = max_group_width
        self.max_group_depth = max_group_depth
        self.stack = 栈摘要._extract_from_extended_frame_gen(_walk_tb_with_full_positions(exc_traceback), limit=limit, lookup_lines=lookup_lines, capture_locals=capture_locals)
        self._exc_type = exc_type if save_exc_type else None
        self._str = _safe_string(exc_value, 'exception')
        try:
            self.__notes__ = getattr(exc_value, '__notes__', None)
        except Exception as e:
            self.__notes__ = [f"Ignored error getting __notes__: {_safe_string(e, '__notes__', repr)}"]
        self._is_syntax_error = False
        self._have_exc_type = exc_type is not None
        if exc_type is not None:
            self.exc_type_qualname = exc_type.__qualname__
            self.exc_type_module = exc_type.__module__
        else:
            self.exc_type_qualname = None
            self.exc_type_module = None
        if exc_type and issubclass(exc_type, SyntaxError):
            self.filename = exc_value.filename
            lno = exc_value.lineno
            self.lineno = str(lno) if lno is not None else None
            end_lno = exc_value.end_lineno
            self.end_lineno = str(end_lno) if end_lno is not None else None
            self.text = exc_value.text
            self.offset = exc_value.offset
            self.end_offset = exc_value.end_offset
            self.msg = exc_value.msg
            self._is_syntax_error = True
            self._exc_metadata = getattr(exc_value, '_metadata', None)
        elif exc_type and issubclass(exc_type, ImportError) and (getattr(exc_value, 'name_from', None) is not None):
            wrong_name = getattr(exc_value, 'name_from', None)
            suggestion = _compute_suggestion_error(exc_value, exc_traceback, wrong_name)
            if suggestion:
                self._str += f". Did you mean: '{suggestion}'?"
        elif exc_type and issubclass(exc_type, (NameError, AttributeError)) and (getattr(exc_value, 'name', None) is not None):
            wrong_name = getattr(exc_value, 'name', None)
            suggestion = _compute_suggestion_error(exc_value, exc_traceback, wrong_name)
            if suggestion:
                self._str += f". Did you mean: '{suggestion}'?"
            if issubclass(exc_type, NameError):
                wrong_name = getattr(exc_value, 'name', None)
                if wrong_name is not None and wrong_name in sys.stdlib_module_names:
                    if suggestion:
                        self._str += f" Or did you forget to import '{wrong_name}'?"
                    else:
                        self._str += f". Did you forget to import '{wrong_name}'?"
        self._str显示 = self._str
        _m = _zh()
        if _m is not None and isinstance(exc_value, KeyError) and (type(exc_value).__str__ is KeyError.__str__) and (len(exc_value.args) == 1) and isinstance(exc_value.args[0], str):
            try:
                原 = exc_value.args[0]
                新 = _m.翻正文(原)
                if 新 != 原:
                    self._str显示 = repr(新)
            except Exception:
                pass
        if lookup_lines:
            self._load_lines()
        self.__suppress_context__ = exc_value.__suppress_context__ if exc_value is not None else False
        if not is_recursive_call:
            queue = [(self, exc_value)]
            while queue:
                te, e = queue.pop()
                if e is not None and e.__cause__ is not None and (id(e.__cause__) not in _seen):
                    cause = 回溯异常(type(e.__cause__), e.__cause__, e.__cause__.__traceback__, limit=limit, lookup_lines=lookup_lines, capture_locals=capture_locals, max_group_width=max_group_width, max_group_depth=max_group_depth, _seen=_seen)
                else:
                    cause = None
                if compact:
                    need_context = cause is None and e is not None and (not e.__suppress_context__)
                else:
                    need_context = True
                if e is not None and e.__context__ is not None and need_context and (id(e.__context__) not in _seen):
                    context = 回溯异常(type(e.__context__), e.__context__, e.__context__.__traceback__, limit=limit, lookup_lines=lookup_lines, capture_locals=capture_locals, max_group_width=max_group_width, max_group_depth=max_group_depth, _seen=_seen)
                else:
                    context = None
                if e is not None and isinstance(e, BaseExceptionGroup):
                    exceptions = []
                    for exc in e.exceptions:
                        texc = 回溯异常(type(exc), exc, exc.__traceback__, limit=limit, lookup_lines=lookup_lines, capture_locals=capture_locals, max_group_width=max_group_width, max_group_depth=max_group_depth, _seen=_seen)
                        exceptions.append(texc)
                else:
                    exceptions = None
                te.__cause__ = cause
                te.__context__ = context
                te.exceptions = exceptions
                if cause:
                    queue.append((te.__cause__, e.__cause__))
                if context:
                    queue.append((te.__context__, e.__context__))
                if exceptions:
                    queue.extend(zip(te.exceptions, e.exceptions))

    @classmethod
    def 从异常建(cls, exc, *args, **kwargs):
        """Create a TracebackException from an exception."""
        return cls(type(exc), exc, exc.__traceback__, *args, **kwargs)

    @property
    def 异常类型(self):
        warnings.warn('Deprecated in 3.13. Use exc_type_str instead.', DeprecationWarning, stacklevel=2)
        return self._exc_type

    @property
    def 异常类型串(self):
        if not self._have_exc_type:
            return None
        stype = self.exc_type_qualname
        smod = self.exc_type_module
        if smod not in ('__main__', 'builtins'):
            if not isinstance(smod, str):
                smod = '<unknown>'
            stype = smod + '.' + stype
        return stype

    def _load_lines(self):
        """Private API. force all lines in the stack to be loaded."""
        for frame in self.stack:
            frame.line

    def __eq__(self, other):
        if isinstance(other, 回溯异常):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __str__(self):
        return self._str

    def 只格式化异常(self, *, show_group=False, _depth=0, **kwargs):
        """Format the exception part of the traceback.

        The return value is a generator of strings, each ending in a newline.

        Generator yields the exception message.
        For :exc:`SyntaxError` exceptions, it
        also yields (before the exception message)
        several lines that (when printed)
        display detailed information about where the syntax error occurred.
        Following the message, generator also yields
        all the exception's ``__notes__``.

        When *show_group* is ``True``, and the exception is an instance of
        :exc:`BaseExceptionGroup`, the nested exceptions are included as
        well, recursively, with indentation relative to their nesting depth.
        """
        colorize = kwargs.get('colorize', False)
        indent = 3 * _depth * ' '
        if not self._have_exc_type:
            yield (indent + _format_final_exc_line(None, self._str显示, colorize=colorize))
            return
        stype = _显示异常名(self.异常类型串)
        if not self._is_syntax_error:
            if _depth > 0:
                formatted = _format_final_exc_line(stype, self._str显示, insert_final_newline=False, colorize=colorize).split('\n')
                yield from [indent + l + '\n' for l in formatted]
            else:
                yield _format_final_exc_line(stype, self._str显示, colorize=colorize)
        else:
            yield from [indent + l for l in self._format_syntax_error(stype, colorize=colorize)]
        if isinstance(self.__notes__, collections.abc.Sequence) and (not isinstance(self.__notes__, (str, bytes))):
            for note in self.__notes__:
                note = _safe_string(note, 'note')
                yield from [indent + l + '\n' for l in note.split('\n')]
        elif self.__notes__ is not None:
            yield (indent + '{}\n'.format(_safe_string(self.__notes__, '__notes__', func=repr)))
        if self.exceptions and show_group:
            for ex in self.exceptions:
                yield from ex.format_exception_only(show_group=show_group, _depth=_depth + 1, colorize=colorize)

    def _find_keyword_typos(self):
        assert self._is_syntax_error
        try:
            import _suggestions
        except ImportError:
            _suggestions = None
        if self.msg != 'invalid syntax' and 'Perhaps you forgot a comma' not in self.msg:
            return
        if not self._exc_metadata:
            return
        行, offset, source = self._exc_metadata
        end_line = int(self.lineno) if self.lineno is not None else 0
        lines = None
        from_filename = False
        if source is None:
            if self.filename:
                try:
                    with open(self.filename) as f:
                        lines = f.read().splitlines()
                except Exception:
                    行, end_line, offset = (0, 1, 0)
                else:
                    from_filename = True
            lines = lines if lines is not None else self.text.splitlines()
        else:
            lines = source.splitlines()
        error_code = lines[行 - 1 if 行 > 0 else 0:end_line]
        error_code = textwrap.dedent('\n'.join(error_code))
        if len(error_code) > 1024:
            return
        error_lines = error_code.splitlines()
        tokens = tokenize.generate_tokens(io.StringIO(error_code).readline)
        tokens_left_to_process = 10
        import difflib
        for token in tokens:
            start, end = (token.start, token.end)
            if token.type != tokenize.NAME:
                continue
            the_end = end_line if 行 == 0 else end_line + 1
            if from_filename and token.start[0] + 行 != the_end:
                continue
            wrong_name = token.string
            if wrong_name in keyword.kwlist:
                continue
            tokens_left_to_process -= 1
            if tokens_left_to_process < 0:
                break
            max_matches = 3
            matches = []
            if _suggestions is not None:
                suggestion = _suggestions._generate_suggestions(keyword.kwlist, wrong_name)
                if suggestion:
                    matches.append(suggestion)
            matches.extend(difflib.get_close_matches(wrong_name, keyword.kwlist, n=max_matches, cutoff=0.5))
            matches = matches[:max_matches]
            for suggestion in matches:
                if not suggestion or suggestion == wrong_name:
                    continue
                the_lines = error_lines.copy()
                the_line = the_lines[start[0] - 1][:]
                chars = list(the_line)
                chars[token.start[1]:token.end[1]] = suggestion
                the_lines[start[0] - 1] = ''.join(chars)
                code = '\n'.join(the_lines)
                try:
                    codeop.compile_command(code, symbol='exec', flags=codeop.PyCF_ONLY_AST)
                except SyntaxError:
                    continue
                self.text = token.line
                self.offset = token.start[1] + 1
                self.end_offset = token.end[1] + 1
                self.lineno = start[0]
                self.end_lineno = end[0]
                self.msg = f"invalid syntax. Did you mean '{suggestion}'?"
                return

    def _format_syntax_error(self, stype, **kwargs):
        """Format SyntaxError exceptions (internal helper)."""
        colorize = kwargs.get('colorize', False)
        if colorize:
            theme = _colorize.get_theme(force_color=True).traceback
        else:
            theme = _colorize.get_theme(force_no_color=True).traceback
        filename_suffix = ''
        if self.lineno is not None:
            yield _框架('  File {}"{}"{}, line {}{}{}\n', theme.filename, self.filename or '<string>', theme.reset, theme.line_no, self.lineno, theme.reset)
        elif self.filename is not None:
            filename_suffix = ' ({})'.format(self.filename)
        text = self.text
        if isinstance(text, str):
            with suppress(Exception):
                self._find_keyword_typos()
            text = self.text
            rtext = text.rstrip('\n')
            ltext = rtext.lstrip(' \n\x0c')
            spaces = len(rtext) - len(ltext)
            if self.offset is None:
                yield '    {}\n'.format(ltext)
            elif isinstance(self.offset, int):
                offset = self.offset
                if self.lineno == self.end_lineno:
                    end_offset = self.end_offset if isinstance(self.end_offset, int) and self.end_offset != 0 else offset
                else:
                    end_offset = len(rtext) + 1
                if self.text and offset > len(self.text):
                    offset = len(rtext) + 1
                if self.text and end_offset > len(self.text):
                    end_offset = len(rtext) + 1
                if offset >= end_offset or end_offset < 0:
                    end_offset = offset + 1
                colno = offset - 1 - spaces
                end_colno = end_offset - 1 - spaces
                caretspace = ' '
                if colno >= 0:
                    caretspace = (c if c.isspace() else ' ' for c in ltext[:colno])
                    start_color = end_color = ''
                    if colorize:
                        ltext = ltext[:colno] + theme.error_highlight + ltext[colno:end_colno] + theme.reset + ltext[end_colno:]
                        start_color = theme.error_highlight
                        end_color = theme.reset
                    yield '    {}\n'.format(ltext)
                    yield '    {}{}{}{}\n'.format(''.join(caretspace), start_color, '^' * (end_colno - colno), end_color)
                else:
                    yield '    {}\n'.format(ltext)
        msg = self.msg or '<no detail available>'
        _m = _zh()
        if _m is not None:
            try:
                stype = _m.翻异常名(stype)
                msg = _m.翻正文(msg)
            except Exception:
                pass
        yield '{}{}{}: {}{}{}{}\n'.format(theme.type, stype, theme.reset, theme.message, msg, theme.reset, filename_suffix)

    def format(self, *, chain=True, _ctx=None, **kwargs):
        """Format the exception.

        If chain is not *True*, *__cause__* and *__context__* will not be formatted.

        The return value is a generator of strings, each ending in a newline and
        some containing internal newlines. `print_exception` is a wrapper around
        this method which just prints the lines to a file.

        The message indicating which exception occurred is always the last
        string in the output.
        """
        colorize = kwargs.get('colorize', False)
        if _ctx is None:
            _ctx = _ExceptionPrintContext()
        output = []
        exc = self
        if chain:
            while exc:
                if exc.__cause__ is not None:
                    chained_msg = _框架(_cause_message)
                    chained_exc = exc.__cause__
                elif exc.__context__ is not None and (not exc.__suppress_context__):
                    chained_msg = _框架(_context_message)
                    chained_exc = exc.__context__
                else:
                    chained_msg = None
                    chained_exc = None
                output.append((chained_msg, exc))
                exc = chained_exc
        else:
            output.append((None, exc))
        for msg, exc in reversed(output):
            if msg is not None:
                yield from _ctx.emit(msg)
            if exc.exceptions is None:
                if exc.stack:
                    yield from _ctx.emit(_框架('Traceback (most recent call last):\n'))
                    yield from _ctx.emit(exc.stack.format(colorize=colorize))
                yield from _ctx.emit(exc.format_exception_only(colorize=colorize))
            elif _ctx.exception_group_depth > self.max_group_depth:
                yield from _ctx.emit(_框架('... (max_group_depth is {})\n', self.max_group_depth))
            else:
                is_toplevel = _ctx.exception_group_depth == 0
                if is_toplevel:
                    _ctx.exception_group_depth += 1
                if exc.stack:
                    yield from _ctx.emit(_框架('Exception Group Traceback (most recent call last):\n'), margin_char='+' if is_toplevel else None)
                    yield from _ctx.emit(exc.stack.format(colorize=colorize))
                yield from _ctx.emit(exc.format_exception_only(colorize=colorize))
                num_excs = len(exc.exceptions)
                if num_excs <= self.max_group_width:
                    n = num_excs
                else:
                    n = self.max_group_width + 1
                _ctx.need_close = False
                for i in range(n):
                    last_exc = i == n - 1
                    if last_exc:
                        _ctx.need_close = True
                    if self.max_group_width is not None:
                        truncated = i >= self.max_group_width
                    else:
                        truncated = False
                    title = f'{i + 1}' if not truncated else '...'
                    yield (_ctx.indent() + ('+-' if i == 0 else '  ') + f'+---------------- {title} ----------------\n')
                    _ctx.exception_group_depth += 1
                    if not truncated:
                        yield from exc.exceptions[i].format(chain=chain, _ctx=_ctx, colorize=colorize)
                    else:
                        remaining = num_excs - self.max_group_width
                        plural = 's' if remaining > 1 else ''
                        yield from _ctx.emit(_框架('and {} more exception{}\n', remaining, plural))
                    if last_exc and _ctx.need_close:
                        yield (_ctx.indent() + '+------------------------------------\n')
                        _ctx.need_close = False
                    _ctx.exception_group_depth -= 1
                if is_toplevel:
                    assert _ctx.exception_group_depth == 1
                    _ctx.exception_group_depth = 0

    def print(self, *, file=None, chain=True, **kwargs):
        """Print the result of self.format(chain=chain) to 'file'."""
        colorize = kwargs.get('colorize', False)
        if file is None:
            file = sys.stderr
        for 行 in self.format(chain=chain, colorize=colorize):
            print(行, file=file, end='')
_装类转发(回溯异常, {'exc_type': '异常类型', 'exc_type_str': '异常类型串', 'format_exception_only': '只格式化异常', 'from_exception': '从异常建'}, {'exc_type': '异常类型', 'exc_type_str': '异常类型串', 'format_exception_only': '只格式化异常', 'from_exception': '从异常建'})
_MAX_CANDIDATE_ITEMS = 750
_MAX_STRING_SIZE = 40
_MOVE_COST = 2
_CASE_COST = 1

def _substitution_cost(ch_a, ch_b):
    if ch_a == ch_b:
        return 0
    if ch_a.lower() == ch_b.lower():
        return _CASE_COST
    return _MOVE_COST

def _get_safe___dir__(obj):
    try:
        d = obj.__dir__()
    except TypeError:
        d = type(obj).__dir__(obj)
    return sorted((x for x in d if isinstance(x, str)))

def _compute_suggestion_error(exc_value, tb, wrong_name):
    if wrong_name is None or not isinstance(wrong_name, str):
        return None
    if isinstance(exc_value, AttributeError):
        obj = exc_value.obj
        try:
            d = _get_safe___dir__(obj)
            hide_underscored = wrong_name[:1] != '_'
            if hide_underscored and tb is not None:
                while tb.tb_next is not None:
                    tb = tb.tb_next
                frame = tb.tb_frame
                if 'self' in frame.f_locals and frame.f_locals['self'] is obj:
                    hide_underscored = False
            if hide_underscored:
                d = [x for x in d if x[:1] != '_']
        except Exception:
            return None
    elif isinstance(exc_value, ImportError):
        try:
            mod = __import__(exc_value.name)
            d = _get_safe___dir__(mod)
            if wrong_name[:1] != '_':
                d = [x for x in d if x[:1] != '_']
        except Exception:
            return None
    else:
        assert isinstance(exc_value, NameError)
        if tb is None:
            return None
        while tb.tb_next is not None:
            tb = tb.tb_next
        frame = tb.tb_frame
        d = list(frame.f_locals) + list(frame.f_globals) + list(frame.f_builtins)
        d = [x for x in d if isinstance(x, str)]
        if 'self' in frame.f_locals:
            self = frame.f_locals['self']
            try:
                has_wrong_name = hasattr(self, wrong_name)
            except Exception:
                has_wrong_name = False
            if has_wrong_name:
                return f'self.{wrong_name}'
    try:
        import _suggestions
    except ImportError:
        pass
    else:
        return _suggestions._generate_suggestions(d, wrong_name)
    if len(d) > _MAX_CANDIDATE_ITEMS:
        return None
    wrong_name_len = len(wrong_name)
    if wrong_name_len > _MAX_STRING_SIZE:
        return None
    best_distance = wrong_name_len
    suggestion = None
    for possible_name in d:
        if possible_name == wrong_name:
            continue
        max_distance = (len(possible_name) + wrong_name_len + 3) * _MOVE_COST // 6
        max_distance = min(max_distance, best_distance - 1)
        current_distance = _levenshtein_distance(wrong_name, possible_name, max_distance)
        if current_distance > max_distance:
            continue
        if not suggestion or current_distance < best_distance:
            suggestion = possible_name
            best_distance = current_distance
    return suggestion

def _levenshtein_distance(a, b, max_cost):
    if a == b:
        return 0
    pre = 0
    while a[pre:] and b[pre:] and (a[pre] == b[pre]):
        pre += 1
    a = a[pre:]
    b = b[pre:]
    post = 0
    while a[:post or None] and b[:post or None] and (a[post - 1] == b[post - 1]):
        post -= 1
    a = a[:post or None]
    b = b[:post or None]
    if not a or not b:
        return _MOVE_COST * (len(a) + len(b))
    if len(a) > _MAX_STRING_SIZE or len(b) > _MAX_STRING_SIZE:
        return max_cost + 1
    if len(b) < len(a):
        a, b = (b, a)
    if (len(b) - len(a)) * _MOVE_COST > max_cost:
        return max_cost + 1
    row = list(range(_MOVE_COST, _MOVE_COST * (len(a) + 1), _MOVE_COST))
    result = 0
    for bindex in range(len(b)):
        bchar = b[bindex]
        distance = result = bindex * _MOVE_COST
        minimum = sys.maxsize
        for index in range(len(a)):
            substitute = distance + _substitution_cost(bchar, a[index])
            distance = row[index]
            insert_delete = min(result, distance) + _MOVE_COST
            result = min(insert_delete, substitute)
            row[index] = result
            if result < minimum:
                minimum = result
        if minimum > max_cost:
            return max_cost + 1
    return result


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BUILTIN_EXCEPTION_LIMIT': '内置异常上限',
    'FrameSummary': '帧摘要',
    'StackSummary': '栈摘要',
    'TracebackException': '回溯异常',
    'clear_frames': '清帧',
    'extract_stack': '提取栈',
    'extract_tb': '提取回溯',
    'format_exc': '格式化当前异常',
    'format_exception': '格式化异常',
    'format_exception_only': '只格式化异常',
    'format_list': '格式化表',
    'format_stack': '格式化栈',
    'format_tb': '格式化回溯',
    'print_exc': '打印当前异常',
    'print_exception': '打印异常',
    'print_last': '打印最后一个',
    'print_list': '打印表',
    'print_stack': '打印栈',
    'print_tb': '打印回溯',
    'walk_stack': '遍历栈',
    'walk_tb': '遍历回溯',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '回溯异常': {
        'exc_type': '异常类型',
        'exc_type_str': '异常类型串',
        'format_exception_only': '只格式化异常',
        'from_exception': '从异常建',
    },
    '帧摘要': {
        'line': '行',
    },
    '栈摘要': {
        'extract': '提取',
        'from_list': '从表建',
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
    '回溯异常': {
        'exc_type': '异常类型',
        'exc_type_str': '异常类型串',
        'format_exception_only': '只格式化异常',
        'from_exception': '从异常建',
    },
    '帧摘要': {
        'line': '行',
    },
    '栈摘要': {
        'extract': '提取',
        'from_list': '从表建',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '只格式化异常',
    '回溯异常',
    '帧摘要',
    '打印回溯',
    '打印异常',
    '打印当前异常',
    '打印最后一个',
    '打印栈',
    '打印表',
    '提取回溯',
    '提取栈',
    '栈摘要',
    '格式化回溯',
    '格式化异常',
    '格式化当前异常',
    '格式化栈',
    '格式化表',
    '清帧',
    '遍历回溯',
    '遍历栈',
])

# ---- 转发层结束 ----
