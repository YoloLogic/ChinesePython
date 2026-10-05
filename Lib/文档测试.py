# -*- coding: utf-8 -*-
"""文档测试 —— 汉语库（由 tools/汉化库.py 从 Lib/doctest.py 机械生成，**不要手改**）。

英文库 Lib/doctest.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 文档测试
"""


"""Module doctest -- a framework for running examples in docstrings.

In simplest use, end each module M to be tested with:

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

Then running the module as a script will cause the examples in the
docstrings to get executed and verified:

python M.py

This won't display anything unless an example fails, in which case the
failing example(s) and the cause(s) of the failure(s) are printed to stdout
(why not stderr? because stderr is a lame hack <0.2 wink>), and the final
line of output is "Test failed.".

Run it with the -v switch instead:

python M.py -v

and a detailed report of all examples tried is printed to stdout, along
with assorted summaries at the end.

You can force verbose mode by passing "verbose=True" to testmod, or prohibit
it by passing "verbose=False".  In either of those cases, sys.argv is not
examined by testmod.

There are a variety of other ways to run doctests, including integration
with the unittest framework, and support for running non-Python text
files containing doctests.  There are also many ways to override parts
of doctest's default behaviors.  See the Library Reference Manual for
details.
"""
_英文原名表 = {'BLANKLINE_MARKER': '空行标记', 'COMPARISON_FLAGS': '比较标志', 'DONT_ACCEPT_BLANKLINE': '不接受空行标记', 'DONT_ACCEPT_TRUE_FOR_1': '不接受1代真', 'DebugRunner': '调试运行器', 'DocFileCase': '文档文件用例', 'DocFileSuite': '文档文件套件', 'DocFileTest': '文档文件测试', 'DocTest': '文档测试', 'DocTestCase': '文档测试用例', 'DocTestFailure': '文档测试失败', 'DocTestFinder': '文档测试查找器', 'DocTestParser': '文档测试解析器', 'DocTestRunner': '文档测试运行器', 'DocTestSuite': '文档测试套件', 'ELLIPSIS': '省略号', 'ELLIPSIS_MARKER': '省略号标记', 'Example': '示例', 'FAIL_FAST': '快速失败', 'IGNORE_EXCEPTION_DETAIL': '忽略异常细节', 'NORMALIZE_WHITESPACE': '规范化空白', 'OPTIONFLAGS_BY_NAME': '按名索引的选项标志', 'OutputChecker': '输出检查器', 'REPORTING_FLAGS': '报告标志', 'REPORT_CDIFF': '报告上下文差异', 'REPORT_NDIFF': '报告逐行差异', 'REPORT_ONLY_FIRST_FAILURE': '只报首个失败', 'REPORT_UDIFF': '报告统一差异', 'SKIP': '跳过该例', 'SkipDocTestCase': '跳过文档测试用例', 'TestResults': '测试结果', 'UnexpectedException': '意外异常', 'debug_script': '调试脚本', 'debug_src': '调试源码', 'master': '主运行器', 'register_optionflag': '登记选项标志', 'run_docstring_examples': '运行文档串示例', 'script_from_examples': '从示例生成脚本', 'set_unittest_reportflags': '设单元测试报告标志', 'testfile': '测试文件', 'testmod': '测试模块', 'testsource': '测试源码'}

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
__docformat__ = 'reStructuredText en'
__all__ = ['register_optionflag', 'DONT_ACCEPT_TRUE_FOR_1', 'DONT_ACCEPT_BLANKLINE', 'NORMALIZE_WHITESPACE', 'ELLIPSIS', 'SKIP', 'IGNORE_EXCEPTION_DETAIL', 'COMPARISON_FLAGS', 'REPORT_UDIFF', 'REPORT_CDIFF', 'REPORT_NDIFF', 'REPORT_ONLY_FIRST_FAILURE', 'REPORTING_FLAGS', 'FAIL_FAST', 'Example', 'DocTest', 'DocTestParser', 'DocTestFinder', 'DocTestRunner', 'OutputChecker', 'DocTestFailure', 'UnexpectedException', 'DebugRunner', 'testmod', 'testfile', 'run_docstring_examples', 'DocTestSuite', 'DocFileSuite', 'set_unittest_reportflags', 'script_from_examples', 'testsource', 'debug_src', 'debug']
import __future__
import difflib
import functools
import inspect
import linecache
import os
import pdb
import re
import sys
import traceback
import unittest
from io import StringIO, IncrementalNewlineDecoder
from collections import namedtuple
import _colorize
from _colorize import ANSIColors, can_colorize
__unittest = True

class 测试结果(namedtuple('TestResults', 'failed attempted')):

    def __new__(cls, failed, attempted, *, skipped=0):
        results = super().__new__(cls, failed, attempted)
        results.skipped = skipped
        return results

    def __repr__(self):
        if self.skipped:
            return f'TestResults(failed={self.failed}, attempted={self.attempted}, skipped={self.skipped})'
        else:
            return super().__repr__()
按名索引的选项标志 = {}

def 登记选项标志(name):
    return 按名索引的选项标志.setdefault(name, 1 << len(按名索引的选项标志))
不接受1代真 = 登记选项标志('DONT_ACCEPT_TRUE_FOR_1')
不接受空行标记 = 登记选项标志('DONT_ACCEPT_BLANKLINE')
规范化空白 = 登记选项标志('NORMALIZE_WHITESPACE')
省略号 = 登记选项标志('ELLIPSIS')
跳过该例 = 登记选项标志('SKIP')
忽略异常细节 = 登记选项标志('IGNORE_EXCEPTION_DETAIL')
比较标志 = 不接受1代真 | 不接受空行标记 | 规范化空白 | 省略号 | 跳过该例 | 忽略异常细节
报告统一差异 = 登记选项标志('REPORT_UDIFF')
报告上下文差异 = 登记选项标志('REPORT_CDIFF')
报告逐行差异 = 登记选项标志('REPORT_NDIFF')
只报首个失败 = 登记选项标志('REPORT_ONLY_FIRST_FAILURE')
快速失败 = 登记选项标志('FAIL_FAST')
报告标志 = 报告统一差异 | 报告上下文差异 | 报告逐行差异 | 只报首个失败 | 快速失败
空行标记 = '<BLANKLINE>'
省略号标记 = '...'

def _extract_future_flags(globs):
    """
    Return the compiler-flags associated with the future features that
    have been imported into the given namespace (globs).
    """
    flags = 0
    for fname in __future__.all_feature_names:
        feature = globs.get(fname, None)
        if feature is getattr(__future__, fname):
            flags |= feature.compiler_flag
    return flags

def _normalize_module(module, depth=2):
    """
    Return the module specified by `module`.  In particular:
      - If `module` is a module, then return module.
      - If `module` is a string, then import and return the
        module with that name.
      - If `module` is None, then return the calling module.
        The calling module is assumed to be the module of
        the stack frame at the given depth in the call stack.
    """
    if inspect.ismodule(module):
        return module
    elif isinstance(module, str):
        return __import__(module, globals(), locals(), ['*'])
    elif module is None:
        try:
            try:
                return sys.modules[sys._getframemodulename(depth)]
            except AttributeError:
                return sys.modules[sys._getframe(depth).f_globals['__name__']]
        except KeyError:
            pass
    else:
        raise TypeError('Expected a module, string, or None')

def _newline_convert(data):
    return IncrementalNewlineDecoder(None, True).decode(data, True)

def _load_testfile(filename, package, module_relative, encoding):
    if module_relative:
        package = _normalize_module(package, 3)
        filename = _module_relative_path(package, filename)
        if (loader := getattr(package, '__loader__', None)) is None:
            try:
                loader = package.__spec__.loader
            except AttributeError:
                pass
        if hasattr(loader, 'get_data'):
            file_contents = loader.get_data(filename)
            file_contents = file_contents.decode(encoding)
            return (_newline_convert(file_contents), filename)
    with open(filename, encoding=encoding) as f:
        return (f.read(), filename)

def _indent(s, indent=4):
    """
    Add the given number of space characters to the beginning of
    every non-blank line in `s`, and return the result.
    """
    return re.sub('(?m)^(?!$)', indent * ' ', s)

def _exception_traceback(exc_info):
    """
    Return a string containing a traceback message for the given
    exc_info tuple (as returned by sys.exc_info()).
    """
    excout = StringIO()
    exc_type, exc_val, exc_tb = exc_info
    traceback.print_exception(exc_type, exc_val, exc_tb, file=excout)
    return excout.getvalue()

class _SpoofOut(StringIO):

    def getvalue(self):
        result = StringIO.getvalue(self)
        if result and (not result.endswith('\n')):
            result += '\n'
        return result

    def truncate(self, size=None):
        self.seek(size)
        StringIO.truncate(self)

def _ellipsis_match(want, got):
    """
    Essentially the only subtle case:
    >>> _ellipsis_match('aa...aa', 'aaa')
    False
    """
    if 省略号标记 not in want:
        return want == got
    ws = want.split(省略号标记)
    assert len(ws) >= 2
    startpos, endpos = (0, len(got))
    w = ws[0]
    if w:
        if got.startswith(w):
            startpos = len(w)
            del ws[0]
        else:
            return False
    w = ws[-1]
    if w:
        if got.endswith(w):
            endpos -= len(w)
            del ws[-1]
        else:
            return False
    if startpos > endpos:
        return False
    for w in ws:
        startpos = got.find(w, startpos, endpos)
        if startpos < 0:
            return False
        startpos += len(w)
    return True

def _comment_line(line):
    """Return a commented form of the given line"""
    line = line.rstrip()
    if line:
        return '# ' + line
    else:
        return '#'

def _strip_exception_details(msg):
    start, end = (0, len(msg))
    i = msg.find('\n')
    if i >= 0:
        end = i
    i = msg.find(':', 0, end)
    if i >= 0:
        end = i
    i = msg.rfind('.', 0, end)
    if i >= 0:
        start = i + 1
    return msg[start:end]

class _OutputRedirectingPdb(pdb.Pdb):
    """
    A specialized version of the python debugger that redirects stdout
    to a given stream when interacting with the user.  Stdout is *not*
    redirected when traced code is executed.
    """

    def __init__(self, out):
        self.__out = out
        self.__debugger_used = False
        pdb.Pdb.__init__(self, stdout=out, nosigint=True)
        self.use_rawinput = 1

    def set_trace(self, frame=None, *, commands=None):
        self.__debugger_used = True
        if frame is None:
            frame = sys._getframe().f_back
        pdb.Pdb.set_trace(self, frame, commands=commands)

    def set_continue(self):
        if self.__debugger_used:
            pdb.Pdb.set_continue(self)

    def trace_dispatch(self, *args):
        save_stdout = sys.stdout
        sys.stdout = self.__out
        try:
            return pdb.Pdb.trace_dispatch(self, *args)
        finally:
            sys.stdout = save_stdout

def _module_relative_path(module, test_path):
    if not inspect.ismodule(module):
        raise TypeError('Expected a module: %r' % module)
    if test_path.startswith('/'):
        raise ValueError('Module-relative files may not have absolute paths')
    test_path = os.path.join(*test_path.split('/'))
    if hasattr(module, '__file__'):
        basedir = os.path.split(module.__file__)[0]
    elif module.__name__ == '__main__':
        if len(sys.argv) > 0 and sys.argv[0] != '':
            basedir = os.path.split(sys.argv[0])[0]
        else:
            basedir = os.curdir
    else:
        if hasattr(module, '__path__'):
            for directory in module.__path__:
                fullpath = os.path.join(directory, test_path)
                if os.path.exists(fullpath):
                    return fullpath
        raise ValueError("Can't resolve paths relative to the module %r (it has no __file__)" % module.__name__)
    return os.path.join(basedir, test_path)

class 示例:
    """
    A single doctest example, consisting of source code and expected
    output.  `Example` defines the following attributes:

      - source: A single Python statement, always ending with a newline.
        The constructor adds a newline if needed.

      - want: The expected output from running the source code (either
        from stdout, or a traceback in case of exception).  `want` ends
        with a newline unless it's empty, in which case it's an empty
        string.  The constructor adds a newline if needed.

      - exc_msg: The exception message generated by the example, if
        the example is expected to generate an exception; or `None` if
        it is not expected to generate an exception.  This exception
        message is compared against the return value of
        `traceback.format_exception_only()`.  `exc_msg` ends with a
        newline unless it's `None`.  The constructor adds a newline
        if needed.

      - lineno: The line number within the DocTest string containing
        this Example where the Example begins.  This line number is
        zero-based, with respect to the beginning of the DocTest.

      - indent: The example's indentation in the DocTest string.
        I.e., the number of space characters that precede the
        example's first prompt.

      - options: A dictionary mapping from option flags to True or
        False, which is used to override default options for this
        example.  Any option flags not contained in this dictionary
        are left at their default value (as specified by the
        DocTestRunner's optionflags).  By default, no options are set.
    """

    def __init__(self, source, want, exc_msg=None, lineno=0, indent=0, options=None):
        if not source.endswith('\n'):
            source += '\n'
        if want and (not want.endswith('\n')):
            want += '\n'
        if exc_msg is not None and (not exc_msg.endswith('\n')):
            exc_msg += '\n'
        self.source = source
        self.want = want
        self.lineno = lineno
        self.indent = indent
        if options is None:
            options = {}
        self.options = options
        self.exc_msg = exc_msg

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.source == other.source and self.want == other.want and (self.lineno == other.lineno) and (self.indent == other.indent) and (self.options == other.options) and (self.exc_msg == other.exc_msg)

    def __hash__(self):
        return hash((self.source, self.want, self.lineno, self.indent, self.exc_msg))

class 文档测试:
    """
    A collection of doctest examples that should be run in a single
    namespace.  Each `DocTest` defines the following attributes:

      - examples: the list of examples.

      - globs: The namespace (aka globals) that the examples should
        be run in.

      - name: A name identifying the DocTest (typically, the name of
        the object whose docstring this DocTest was extracted from).

      - filename: The name of the file that this DocTest was extracted
        from, or `None` if the filename is unknown.

      - lineno: The line number within filename where this DocTest
        begins, or `None` if the line number is unavailable.  This
        line number is zero-based, with respect to the beginning of
        the file.

      - docstring: The string that the examples were extracted from,
        or `None` if the string is unavailable.
    """

    def __init__(self, examples, globs, name, filename, lineno, docstring):
        """
        Create a new DocTest containing the given examples.  The
        DocTest's globals are initialized with a copy of `globs`.
        """
        assert not isinstance(examples, str), 'DocTest no longer accepts str; use DocTestParser instead'
        self.examples = examples
        self.docstring = docstring
        self.globs = globs.copy()
        self.name = name
        self.filename = filename
        self.lineno = lineno

    def __repr__(self):
        if len(self.examples) == 0:
            examples = 'no examples'
        elif len(self.examples) == 1:
            examples = '1 example'
        else:
            examples = '%d examples' % len(self.examples)
        return '<%s %s from %s:%s (%s)>' % (self.__class__.__name__, self.name, self.filename, self.lineno, examples)

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.examples == other.examples and self.docstring == other.docstring and (self.globs == other.globs) and (self.name == other.name) and (self.filename == other.filename) and (self.lineno == other.lineno)

    def __hash__(self):
        return hash((self.docstring, self.name, self.filename, self.lineno))

    def __lt__(self, other):
        if not isinstance(other, 文档测试):
            return NotImplemented
        self_lno = self.lineno if self.lineno is not None else -1
        other_lno = other.lineno if other.lineno is not None else -1
        return (self.name, self.filename, self_lno, id(self)) < (other.name, other.filename, other_lno, id(other))

class 文档测试解析器:
    """
    A class used to parse strings containing doctest examples.
    """
    _EXAMPLE_RE = re.compile('\n        # Source consists of a PS1 line followed by zero or more PS2 lines.\n        (?P<source>\n            (?:^(?P<indent> [ ]*) >>>    .*)    # PS1 line\n            (?:\\n           [ ]*  \\.\\.\\. .*)*)  # PS2 lines\n        \\n?\n        # Want consists of any non-blank lines that do not start with PS1.\n        (?P<want> (?:(?![ ]*$)    # Not a blank line\n                     (?![ ]*>>>)  # Not a line starting with PS1\n                     .+$\\n?       # But any other line\n                  )*)\n        ', re.MULTILINE | re.VERBOSE)
    _EXCEPTION_RE = re.compile("\n        # Grab the traceback header.  Different versions of Python have\n        # said different things on the first traceback line.\n        ^(?P<hdr> Traceback\\ \\(\n            (?: most\\ recent\\ call\\ last\n            |   innermost\\ last\n            ) \\) :\n        )\n        \\s* $                # toss trailing whitespace on the header.\n        (?P<stack> .*?)      # don't blink: absorb stuff until...\n        ^ (?P<msg> \\w+ .*)   #     a line *starts* with alphanum.\n        ", re.VERBOSE | re.MULTILINE | re.DOTALL)
    _IS_BLANK_OR_COMMENT = re.compile('^[ ]*(#.*)?$').match

    def 解析(self, string, name='<string>'):
        """
        Divide the given string into examples and intervening text,
        and return them as a list of alternating Examples and strings.
        Line numbers for the Examples are 0-based.  The optional
        argument `name` is a name identifying this string, and is only
        used for error messages.
        """
        string = string.expandtabs()
        min_indent = self._min_indent(string)
        if min_indent > 0:
            string = '\n'.join([l[min_indent:] for l in string.split('\n')])
        output = []
        charno, lineno = (0, 0)
        for m in self._EXAMPLE_RE.finditer(string):
            output.append(string[charno:m.start()])
            lineno += string.count('\n', charno, m.start())
            source, options, want, exc_msg = self._parse_example(m, name, lineno)
            if not self._IS_BLANK_OR_COMMENT(source):
                output.append(示例(source, want, exc_msg, lineno=lineno, indent=min_indent + len(m.group('indent')), options=options))
            lineno += string.count('\n', m.start(), m.end())
            charno = m.end()
        output.append(string[charno:])
        return output

    def 取文档测试(self, string, globs, name, filename, lineno):
        """
        Extract all doctest examples from the given string, and
        collect them into a `DocTest` object.

        `globs`, `name`, `filename`, and `lineno` are attributes for
        the new `DocTest` object.  See the documentation for `DocTest`
        for more information.
        """
        return 文档测试(self.取示例(string, name), globs, name, filename, lineno, string)

    def 取示例(self, string, name='<string>'):
        """
        Extract all doctest examples from the given string, and return
        them as a list of `Example` objects.  Line numbers are
        0-based, because it's most common in doctests that nothing
        interesting appears on the same line as opening triple-quote,
        and so the first interesting line is called "line 1" then.

        The optional argument `name` is a name identifying this
        string, and is only used for error messages.
        """
        return [x for x in self.解析(string, name) if isinstance(x, 示例)]

    def _parse_example(self, m, name, lineno):
        """
        Given a regular expression match from `_EXAMPLE_RE` (`m`),
        return a pair `(source, want)`, where `source` is the matched
        example's source code (with prompts and indentation stripped);
        and `want` is the example's expected output (with indentation
        stripped).

        `name` is the string's name, and `lineno` is the line number
        where the example starts; both are used for error messages.
        """
        indent = len(m.group('indent'))
        source_lines = m.group('source').split('\n')
        self._check_prompt_blank(source_lines, indent, name, lineno)
        self._check_prefix(source_lines[1:], ' ' * indent + '.', name, lineno)
        source = '\n'.join([sl[indent + 4:] for sl in source_lines])
        want = m.group('want')
        want_lines = want.split('\n')
        if len(want_lines) > 1 and re.match(' *$', want_lines[-1]):
            del want_lines[-1]
        self._check_prefix(want_lines, ' ' * indent, name, lineno + len(source_lines))
        want = '\n'.join([wl[indent:] for wl in want_lines])
        m = self._EXCEPTION_RE.match(want)
        if m:
            exc_msg = m.group('msg')
        else:
            exc_msg = None
        options = self._find_options(source, name, lineno)
        return (source, options, want, exc_msg)
    _OPTION_DIRECTIVE_RE = re.compile('#\\s*doctest:\\s*([^\\n\\\'"]*)$', re.MULTILINE)

    def _find_options(self, source, name, lineno):
        """
        Return a dictionary containing option overrides extracted from
        option directives in the given source string.

        `name` is the string's name, and `lineno` is the line number
        where the example starts; both are used for error messages.
        """
        options = {}
        for m in self._OPTION_DIRECTIVE_RE.finditer(source):
            option_strings = m.group(1).replace(',', ' ').split()
            for option in option_strings:
                if option[0] not in '+-' or option[1:] not in 按名索引的选项标志:
                    raise ValueError('line %r of the doctest for %s has an invalid option: %r' % (lineno + 1, name, option))
                flag = 按名索引的选项标志[option[1:]]
                options[flag] = option[0] == '+'
        if options and self._IS_BLANK_OR_COMMENT(source):
            raise ValueError('line %r of the doctest for %s has an option directive on a line with no example: %r' % (lineno, name, source))
        return options
    _INDENT_RE = re.compile('^([ ]*)(?=\\S)', re.MULTILINE)

    def _min_indent(self, s):
        """Return the minimum indentation of any non-blank line in `s`"""
        indents = [len(indent) for indent in self._INDENT_RE.findall(s)]
        if len(indents) > 0:
            return min(indents)
        else:
            return 0

    def _check_prompt_blank(self, lines, indent, name, lineno):
        """
        Given the lines of a source string (including prompts and
        leading indentation), check to make sure that every prompt is
        followed by a space character.  If any line is not followed by
        a space character, then raise ValueError.
        """
        for i, line in enumerate(lines):
            if len(line) >= indent + 4 and line[indent + 3] != ' ':
                raise ValueError('line %r of the docstring for %s lacks blank after %s: %r' % (lineno + i + 1, name, line[indent:indent + 3], line))

    def _check_prefix(self, lines, prefix, name, lineno):
        """
        Check that every line in the given list starts with the given
        prefix; if any line does not, then raise a ValueError.
        """
        for i, line in enumerate(lines):
            if line and (not line.startswith(prefix)):
                raise ValueError('line %r of the docstring for %s has inconsistent leading whitespace: %r' % (lineno + i + 1, name, line))
_装类转发(文档测试解析器, {'get_doctest': '取文档测试', 'get_examples': '取示例', 'parse': '解析'}, {'get_doctest': '取文档测试', 'get_examples': '取示例', 'parse': '解析'})

class 文档测试查找器:
    """
    A class used to extract the DocTests that are relevant to a given
    object, from its docstring and the docstrings of its contained
    objects.  Doctests can currently be extracted from the following
    object types: modules, functions, classes, methods, staticmethods,
    classmethods, and properties.
    """

    def __init__(self, verbose=False, parser=文档测试解析器(), recurse=True, exclude_empty=True):
        """
        Create a new doctest finder.

        The optional argument `parser` specifies a class or
        function that should be used to create new DocTest objects (or
        objects that implement the same interface as DocTest).  The
        signature for this factory function should match the signature
        of the DocTest constructor.

        If the optional argument `recurse` is false, then `find` will
        only examine the given object, and not any contained objects.

        If the optional argument `exclude_empty` is false, then `find`
        will include tests for objects with empty docstrings.
        """
        self._parser = parser
        self._verbose = verbose
        self._recurse = recurse
        self._exclude_empty = exclude_empty

    def 查找(self, obj, name=None, module=None, globs=None, extraglobs=None):
        """
        Return a list of the DocTests that are defined by the given
        object's docstring, or by any of its contained objects'
        docstrings.

        The optional parameter `module` is the module that contains
        the given object.  If the module is not specified or is None, then
        the test finder will attempt to automatically determine the
        correct module.  The object's module is used:

            - As a default namespace, if `globs` is not specified.
            - To prevent the DocTestFinder from extracting DocTests
              from objects that are imported from other modules.
            - To find the name of the file containing the object.
            - To help find the line number of the object within its
              file.

        Contained objects whose module does not match `module` are ignored.

        If `module` is False, no attempt to find the module will be made.
        This is obscure, of use mostly in tests:  if `module` is False, or
        is None but cannot be found automatically, then all objects are
        considered to belong to the (non-existent) module, so all contained
        objects will (recursively) be searched for doctests.

        The globals for each DocTest is formed by combining `globs`
        and `extraglobs` (bindings in `extraglobs` override bindings
        in `globs`).  A new copy of the globals dictionary is created
        for each DocTest.  If `globs` is not specified, then it
        defaults to the module's `__dict__`, if specified, or {}
        otherwise.  If `extraglobs` is not specified, then it defaults
        to {}.

        """
        if name is None:
            name = getattr(obj, '__name__', None)
            if name is None:
                raise ValueError("DocTestFinder.find: name must be given when obj.__name__ doesn't exist: %r" % (type(obj),))
        if module is False:
            module = None
        elif module is None:
            module = inspect.getmodule(obj)
        try:
            file = inspect.getsourcefile(obj)
        except TypeError:
            source_lines = None
        else:
            if not file:
                file = inspect.getfile(obj)
                if not file[0] + file[-2:] == '<]>':
                    file = None
            if file is None:
                source_lines = None
            else:
                if module is not None:
                    source_lines = linecache.getlines(file, module.__dict__)
                else:
                    source_lines = linecache.getlines(file)
                if not source_lines:
                    source_lines = None
        if globs is None:
            if module is None:
                globs = {}
            else:
                globs = module.__dict__.copy()
        else:
            globs = globs.copy()
        if extraglobs is not None:
            globs.update(extraglobs)
        if '__name__' not in globs:
            globs['__name__'] = '__main__'
        tests = []
        self._find(tests, obj, name, module, source_lines, globs, {})
        tests.sort()
        return tests

    def _from_module(self, module, object):
        """
        Return true if the given object is defined in the given
        module.
        """
        if module is None:
            return True
        elif inspect.getmodule(object) is not None:
            return module is inspect.getmodule(object)
        elif inspect.isfunction(object):
            return module.__dict__ is object.__globals__
        elif inspect.ismethoddescriptor(object) or inspect.ismethodwrapper(object):
            if hasattr(object, '__objclass__'):
                obj_mod = object.__objclass__.__module__
            elif hasattr(object, '__module__'):
                obj_mod = object.__module__
            else:
                return True
            return module.__name__ == obj_mod
        elif inspect.isclass(object):
            return module.__name__ == object.__module__
        elif hasattr(object, '__module__'):
            return module.__name__ == object.__module__
        elif isinstance(object, property):
            return True
        else:
            raise ValueError('object must be a class or function')

    def _is_routine(self, obj):
        """
        Safely unwrap objects and determine if they are functions.
        """
        maybe_routine = obj
        try:
            maybe_routine = inspect.unwrap(maybe_routine)
        except ValueError:
            pass
        return inspect.isroutine(maybe_routine)

    def _find(self, tests, obj, name, module, source_lines, globs, seen):
        """
        Find tests for the given object and any contained objects, and
        add them to `tests`.
        """
        if self._verbose:
            print('Finding tests in %s' % name)
        if id(obj) in seen:
            return
        seen[id(obj)] = 1
        test = self._get_test(obj, name, module, globs, source_lines)
        if test is not None:
            tests.append(test)
        if inspect.ismodule(obj) and self._recurse:
            for valname, val in obj.__dict__.items():
                valname = '%s.%s' % (name, valname)
                if (self._is_routine(val) or inspect.isclass(val)) and self._from_module(module, val):
                    self._find(tests, val, valname, module, source_lines, globs, seen)
        if inspect.ismodule(obj) and self._recurse:
            for valname, val in getattr(obj, '__test__', {}).items():
                if not isinstance(valname, str):
                    raise ValueError('DocTestFinder.find: __test__ keys must be strings: %r' % (type(valname),))
                if not (inspect.isroutine(val) or inspect.isclass(val) or inspect.ismodule(val) or isinstance(val, str)):
                    raise ValueError('DocTestFinder.find: __test__ values must be strings, functions, methods, classes, or modules: %r' % (type(val),))
                valname = '%s.__test__.%s' % (name, valname)
                self._find(tests, val, valname, module, source_lines, globs, seen)
        if inspect.isclass(obj) and self._recurse:
            for valname, val in obj.__dict__.items():
                if isinstance(val, (staticmethod, classmethod)):
                    val = val.__func__
                if (inspect.isroutine(val) or inspect.isclass(val) or isinstance(val, property)) and self._from_module(module, val):
                    valname = '%s.%s' % (name, valname)
                    self._find(tests, val, valname, module, source_lines, globs, seen)

    def _get_test(self, obj, name, module, globs, source_lines):
        """
        Return a DocTest for the given object, if it defines a docstring;
        otherwise, return None.
        """
        if isinstance(obj, str):
            docstring = obj
        else:
            try:
                if obj.__doc__ is None:
                    docstring = ''
                else:
                    docstring = obj.__doc__
                    if not isinstance(docstring, str):
                        docstring = str(docstring)
            except (TypeError, AttributeError):
                docstring = ''
        lineno = self._find_lineno(obj, source_lines)
        if self._exclude_empty and (not docstring):
            return None
        if module is None:
            filename = None
        else:
            filename = getattr(module, '__file__', None) or module.__name__
            if filename[-4:] == '.pyc':
                filename = filename[:-1]
        return self._parser.get_doctest(docstring, globs, name, filename, lineno)

    def _find_lineno(self, obj, source_lines):
        """
        Return a line number of the given object's docstring.

        Returns `None` if the given object does not have a docstring.
        """
        lineno = None
        docstring = getattr(obj, '__doc__', None)
        if inspect.ismodule(obj) and docstring is not None:
            lineno = 0
        if inspect.isclass(obj) and docstring is not None:
            if source_lines is None:
                return None
            pat = re.compile('^\\s*class\\s*%s\\b' % re.escape(getattr(obj, '__name__', '-')))
            for i, line in enumerate(source_lines):
                if pat.match(line):
                    lineno = i
                    break
        if inspect.ismethod(obj):
            obj = obj.__func__
        if isinstance(obj, property):
            obj = obj.fget
        if isinstance(obj, functools.cached_property):
            obj = obj.func
        if inspect.isroutine(obj) and getattr(obj, '__doc__', None):
            obj = inspect.unwrap(obj)
            try:
                obj = obj.__code__
            except AttributeError:
                return None
        if inspect.istraceback(obj):
            obj = obj.tb_frame
        if inspect.isframe(obj):
            obj = obj.f_code
        if inspect.iscode(obj):
            lineno = obj.co_firstlineno - 1
        if lineno is not None:
            if source_lines is None:
                return lineno + 1
            pat = re.compile('(^|.*:)\\s*\\w*("|\\\')')
            for lineno in range(lineno, len(source_lines)):
                if pat.match(source_lines[lineno]):
                    return lineno
        return None
_装类转发(文档测试查找器, {'find': '查找'}, {'find': '查找'})

class 文档测试运行器:
    """
    A class used to run DocTest test cases, and accumulate statistics.
    The `run` method is used to process a single DocTest case.  It
    returns a TestResults instance.

        >>> save_colorize = _colorize.COLORIZE
        >>> _colorize.COLORIZE = False

        >>> tests = DocTestFinder().find(_TestClass)
        >>> runner = DocTestRunner(verbose=False)
        >>> tests.sort(key = lambda test: test.name)
        >>> for test in tests:
        ...     print(test.name, '->', runner.run(test))
        _TestClass -> TestResults(failed=0, attempted=2)
        _TestClass.__init__ -> TestResults(failed=0, attempted=2)
        _TestClass.get -> TestResults(failed=0, attempted=2)
        _TestClass.square -> TestResults(failed=0, attempted=1)

    The `summarize` method prints a summary of all the test cases that
    have been run by the runner, and returns an aggregated TestResults
    instance:

        >>> runner.summarize(verbose=1)
        4 items passed all tests:
           2 tests in _TestClass
           2 tests in _TestClass.__init__
           2 tests in _TestClass.get
           1 test in _TestClass.square
        7 tests in 4 items.
        7 passed.
        Test passed.
        TestResults(failed=0, attempted=7)

    The aggregated number of tried examples and failed examples is also
    available via the `tries`, `failures` and `skips` attributes:

        >>> runner.tries
        7
        >>> runner.failures
        0
        >>> runner.skips
        0

    The comparison between expected outputs and actual outputs is done
    by an `OutputChecker`.  This comparison may be customized with a
    number of option flags; see the documentation for `testmod` for
    more information.  If the option flags are insufficient, then the
    comparison may also be customized by passing a subclass of
    `OutputChecker` to the constructor.

    The test runner's display output can be controlled in two ways.
    First, an output function (`out`) can be passed to
    `TestRunner.run`; this function will be called with strings that
    should be displayed.  It defaults to `sys.stdout.write`.  If
    capturing the output is not sufficient, then the display output
    can be also customized by subclassing DocTestRunner, and
    overriding the methods `report_start`, `report_success`,
    `report_unexpected_exception`, and `report_failure`.

        >>> _colorize.COLORIZE = save_colorize
    """
    DIVIDER = '*' * 70

    def __init__(self, checker=None, verbose=None, optionflags=0):
        """
        Create a new test runner.

        Optional keyword arg `checker` is the `OutputChecker` that
        should be used to compare the expected outputs and actual
        outputs of doctest examples.

        Optional keyword arg 'verbose' prints lots of stuff if true,
        only failures if false; by default, it's true iff '-v' is in
        sys.argv.

        Optional argument `optionflags` can be used to control how the
        test runner compares expected output to actual output, and how
        it displays failures.  See the documentation for `testmod` for
        more information.
        """
        self._checker = checker or 输出检查器()
        if verbose is None:
            verbose = '-v' in sys.argv
        self._verbose = verbose
        self.optionflags = optionflags
        self.original_optionflags = optionflags
        self.tries = 0
        self.failures = 0
        self.skips = 0
        self._stats = {}
        self._fakeout = _SpoofOut()

    def 报告开始(self, out, test, example):
        """
        Report that the test runner is about to process the given
        example.  (Only displays a message if verbose=True)
        """
        if self._verbose:
            if example.want:
                out('Trying:\n' + _indent(example.source) + 'Expecting:\n' + _indent(example.want))
            else:
                out('Trying:\n' + _indent(example.source) + 'Expecting nothing\n')

    def 报告成功(self, out, test, example, got):
        """
        Report that the given example ran successfully.  (Only
        displays a message if verbose=True)
        """
        if self._verbose:
            out('ok\n')

    def 报告失败(self, out, test, example, got):
        """
        Report that the given example failed.
        """
        out(self._failure_header(test, example) + self._checker.output_difference(example, got, self.optionflags))

    def 报告意外异常(self, out, test, example, exc_info):
        """
        Report that the given example raised an unexpected exception.
        """
        out(self._failure_header(test, example) + 'Exception raised:\n' + _indent(_exception_traceback(exc_info)))

    def _failure_header(self, test, example):
        red, reset = (ANSIColors.RED, ANSIColors.RESET) if can_colorize() else ('', '')
        out = [f'{red}{self.DIVIDER}{reset}']
        if test.filename:
            if test.lineno is not None and example.lineno is not None:
                lineno = test.lineno + example.lineno + 1
            else:
                lineno = '?'
            out.append('File "%s", line %s, in %s' % (test.filename, lineno, test.name))
        else:
            out.append('Line %s, in %s' % (example.lineno + 1, test.name))
        out.append('Failed example:')
        source = example.source
        out.append(_indent(source))
        return '\n'.join(out)

    def __run(self, test, compileflags, out):
        """
        Run the examples in `test`.  Write the outcome of each example
        with one of the `DocTestRunner.report_*` methods, using the
        writer function `out`.  `compileflags` is the set of compiler
        flags that should be used to execute examples.  Return a TestResults
        instance.  The examples are run in the namespace `test.globs`.
        """
        failures = attempted = skips = 0
        original_optionflags = self.optionflags
        SUCCESS, FAILURE, BOOM = range(3)
        check = self._checker.check_output
        for examplenum, example in enumerate(test.examples):
            attempted += 1
            quiet = self.optionflags & 只报首个失败 and failures > 0
            self.optionflags = original_optionflags
            if example.options:
                for optionflag, val in example.options.items():
                    if val:
                        self.optionflags |= optionflag
                    else:
                        self.optionflags &= ~optionflag
            if self.optionflags & 跳过该例:
                skips += 1
                continue
            if not quiet:
                self.报告开始(out, test, example)
            filename = '<doctest %s[%d]>' % (test.name, examplenum)
            try:
                exec(compile(example.source, filename, 'single', compileflags, True), test.globs)
                self.debugger.set_continue()
                exc_info = None
            except KeyboardInterrupt:
                raise
            except BaseException as exc:
                exc_info = (type(exc), exc, exc.__traceback__.tb_next)
                self.debugger.set_continue()
            got = self._fakeout.getvalue()
            self._fakeout.truncate(0)
            outcome = FAILURE
            if exc_info is None:
                if check(example.want, got, self.optionflags):
                    outcome = SUCCESS
            else:
                formatted_ex = traceback.format_exception_only(*exc_info[:2])
                if issubclass(exc_info[0], SyntaxError):
                    exception_line_prefixes = (f'{exc_info[0].__qualname__}:', f'{exc_info[0].__module__}.{exc_info[0].__qualname__}:')
                    exc_msg_index = next((index for index, line in enumerate(formatted_ex) if line.startswith(exception_line_prefixes)))
                    formatted_ex = formatted_ex[exc_msg_index:]
                exc_msg = ''.join(formatted_ex)
                if not quiet:
                    got += _exception_traceback(exc_info)
                if example.exc_msg is None:
                    outcome = BOOM
                elif check(example.exc_msg, exc_msg, self.optionflags):
                    outcome = SUCCESS
                elif self.optionflags & 忽略异常细节:
                    if check(_strip_exception_details(example.exc_msg), _strip_exception_details(exc_msg), self.optionflags):
                        outcome = SUCCESS
            if outcome is SUCCESS:
                if not quiet:
                    self.报告成功(out, test, example, got)
            elif outcome is FAILURE:
                if not quiet:
                    self.报告失败(out, test, example, got)
                failures += 1
            elif outcome is BOOM:
                if not quiet:
                    self.报告意外异常(out, test, example, exc_info)
                failures += 1
            else:
                assert False, ('unknown outcome', outcome)
            if failures and self.optionflags & 快速失败:
                break
        self.optionflags = original_optionflags
        self.__record_outcome(test, failures, attempted, skips)
        return 测试结果(failures, attempted, skipped=skips)

    def __record_outcome(self, test, failures, tries, skips):
        """
        Record the fact that the given DocTest (`test`) generated `failures`
        failures out of `tries` tried examples.
        """
        failures2, tries2, skips2 = self._stats.get(test.name, (0, 0, 0))
        self._stats[test.name] = (failures + failures2, tries + tries2, skips + skips2)
        self.failures += failures
        self.tries += tries
        self.skips += skips
    __LINECACHE_FILENAME_RE = re.compile('<doctest (?P<name>.+)\\[(?P<examplenum>\\d+)\\]>$')

    def __patched_linecache_getlines(self, filename, module_globals=None):
        m = self.__LINECACHE_FILENAME_RE.match(filename)
        if m and m.group('name') == self.test.name:
            example = self.test.examples[int(m.group('examplenum'))]
            return example.source.splitlines(keepends=True)
        else:
            return self.save_linecache_getlines(filename, module_globals)

    def 运行(self, test, compileflags=None, out=None, clear_globs=True):
        """
        Run the examples in `test`, and display the results using the
        writer function `out`.

        The examples are run in the namespace `test.globs`.  If
        `clear_globs` is true (the default), then this namespace will
        be cleared after the test runs, to help with garbage
        collection.  If you would like to examine the namespace after
        the test completes, then use `clear_globs=False`.

        `compileflags` gives the set of flags that should be used by
        the Python compiler when running the examples.  If not
        specified, then it will default to the set of future-import
        flags that apply to `globs`.

        The output of each example is checked using
        `DocTestRunner.check_output`, and the results are formatted by
        the `DocTestRunner.report_*` methods.
        """
        self.test = test
        if compileflags is None:
            compileflags = _extract_future_flags(test.globs)
        save_stdout = sys.stdout
        if out is None:
            encoding = save_stdout.encoding
            if encoding is None or encoding.lower() == 'utf-8':
                out = save_stdout.write
            else:

                def out(s):
                    s = str(s.encode(encoding, 'backslashreplace'), encoding)
                    save_stdout.write(s)
        sys.stdout = self._fakeout
        save_trace = sys.gettrace()
        save_set_trace = pdb.set_trace
        self.debugger = _OutputRedirectingPdb(save_stdout)
        self.debugger.reset()
        pdb.set_trace = self.debugger.set_trace
        self.save_linecache_getlines = linecache.getlines
        linecache.getlines = self.__patched_linecache_getlines
        save_displayhook = sys.displayhook
        sys.displayhook = sys.__displayhook__
        saved_can_colorize = _colorize.can_colorize
        _colorize.can_colorize = lambda *args, **kwargs: False
        color_variables = {'PYTHON_COLORS': None, 'FORCE_COLOR': None}
        for key in color_variables:
            color_variables[key] = os.environ.pop(key, None)
        try:
            return self.__run(test, compileflags, out)
        finally:
            sys.stdout = save_stdout
            pdb.set_trace = save_set_trace
            sys.settrace(save_trace)
            linecache.getlines = self.save_linecache_getlines
            sys.displayhook = save_displayhook
            _colorize.can_colorize = saved_can_colorize
            for key, value in color_variables.items():
                if value is not None:
                    os.environ[key] = value
            if clear_globs:
                test.globs.clear()
                import builtins
                builtins._ = None

    def 汇总(self, verbose=None):
        """
        Print a summary of all the test cases that have been run by
        this DocTestRunner, and return a TestResults instance.

        The optional `verbose` argument controls how detailed the
        summary is.  If the verbosity is not specified, then the
        DocTestRunner's verbosity is used.
        """
        if verbose is None:
            verbose = self._verbose
        notests, passed, failed = ([], [], [])
        total_tries = total_failures = total_skips = 0
        for name, (failures, tries, skips) in self._stats.items():
            assert failures <= tries
            total_tries += tries
            total_failures += failures
            total_skips += skips
            if tries == 0:
                notests.append(name)
            elif failures == 0:
                passed.append((name, tries))
            else:
                failed.append((name, (failures, tries, skips)))
        ansi = _colorize.get_colors()
        bold_green = ansi.BOLD_GREEN
        bold_red = ansi.BOLD_RED
        green = ansi.GREEN
        red = ansi.RED
        reset = ansi.RESET
        yellow = ansi.YELLOW
        if verbose:
            if notests:
                print(f'{_n_items(notests)} had no tests:')
                notests.sort()
                for name in notests:
                    print(f'    {name}')
            if passed:
                print(f'{green}{_n_items(passed)} passed all tests:{reset}')
                for name, count in sorted(passed):
                    s = '' if count == 1 else 's'
                    print(f' {green}{count:3d} test{s} in {name}{reset}')
        if failed:
            print(f'{red}{self.DIVIDER}{reset}')
            print(f'{_n_items(failed)} had failures:')
            for name, (failures, tries, skips) in sorted(failed):
                print(f' {failures:3d} of {tries:3d} in {name}')
        if verbose:
            s = '' if total_tries == 1 else 's'
            print(f'{total_tries} test{s} in {_n_items(self._stats)}.')
            and_f = f' and {red}{total_failures} failed{reset}' if total_failures else ''
            print(f'{green}{total_tries - total_failures} passed{reset}{and_f}.')
        if total_failures:
            s = '' if total_failures == 1 else 's'
            msg = f'{bold_red}***Test Failed*** {total_failures} failure{s}{reset}'
            if total_skips:
                s = '' if total_skips == 1 else 's'
                msg = f'{msg} and {yellow}{total_skips} skipped test{s}{reset}'
            print(f'{msg}.')
        elif verbose:
            print(f'{bold_green}Test passed.{reset}')
        return 测试结果(total_failures, total_tries, skipped=total_skips)

    def 合并(self, other):
        d = self._stats
        for name, (failures, tries, skips) in other._stats.items():
            if name in d:
                failures2, tries2, skips2 = d[name]
                failures = failures + failures2
                tries = tries + tries2
                skips = skips + skips2
            d[name] = (failures, tries, skips)
_装类转发(文档测试运行器, {'merge': '合并', 'report_failure': '报告失败', 'report_start': '报告开始', 'report_success': '报告成功', 'report_unexpected_exception': '报告意外异常', 'run': '运行', 'summarize': '汇总'}, {'merge': '合并', 'report_failure': '报告失败', 'report_start': '报告开始', 'report_success': '报告成功', 'report_unexpected_exception': '报告意外异常', 'run': '运行', 'summarize': '汇总'})

def _n_items(items: list | dict) -> str:
    """
    Helper to pluralise the number of items in a list.
    """
    n = len(items)
    s = '' if n == 1 else 's'
    return f'{n} item{s}'

class 输出检查器:
    """
    A class used to check whether the actual output from a doctest
    example matches the expected output.  `OutputChecker` defines two
    methods: `check_output`, which compares a given pair of outputs,
    and returns true if they match; and `output_difference`, which
    returns a string describing the differences between two outputs.
    """

    def _toAscii(self, s):
        """
        Convert string to hex-escaped ASCII string.
        """
        return str(s.encode('ASCII', 'backslashreplace'), 'ASCII')

    def 检查输出(self, want, got, optionflags):
        """
        Return True iff the actual output from an example (`got`)
        matches the expected output (`want`).  These strings are
        always considered to match if they are identical; but
        depending on what option flags the test runner is using,
        several non-exact match types are also possible.  See the
        documentation for `TestRunner` for more information about
        option flags.
        """
        got = self._toAscii(got)
        want = self._toAscii(want)
        if got == want:
            return True
        if not optionflags & 不接受1代真:
            if (got, want) == ('True\n', '1\n'):
                return True
            if (got, want) == ('False\n', '0\n'):
                return True
        if not optionflags & 不接受空行标记:
            want = re.sub('(?m)^%s\\s*?$' % re.escape(空行标记), '', want)
            got = re.sub('(?m)^[^\\S\\n]+$', '', got)
            if got == want:
                return True
        if optionflags & 规范化空白:
            got = ' '.join(got.split())
            want = ' '.join(want.split())
            if got == want:
                return True
        if optionflags & 省略号:
            if _ellipsis_match(want, got):
                return True
        return False

    def _do_a_fancy_diff(self, want, got, optionflags):
        if not optionflags & (报告统一差异 | 报告上下文差异 | 报告逐行差异):
            return False
        if optionflags & 报告逐行差异:
            return True
        return want.count('\n') > 2 and got.count('\n') > 2

    def 输出差异(self, example, got, optionflags):
        """
        Return a string describing the differences between the
        expected output for a given example (`example`) and the actual
        output (`got`).  `optionflags` is the set of option flags used
        to compare `want` and `got`.
        """
        want = example.want
        if not optionflags & 不接受空行标记:
            got = re.sub('(?m)^[ ]*(?=\n)', 空行标记, got)
        if self._do_a_fancy_diff(want, got, optionflags):
            want_lines = want.splitlines(keepends=True)
            got_lines = got.splitlines(keepends=True)
            if optionflags & 报告统一差异:
                diff = difflib.unified_diff(want_lines, got_lines, n=2)
                diff = list(diff)[2:]
                kind = 'unified diff with -expected +actual'
            elif optionflags & 报告上下文差异:
                diff = difflib.context_diff(want_lines, got_lines, n=2)
                diff = list(diff)[2:]
                kind = 'context diff with expected followed by actual'
            elif optionflags & 报告逐行差异:
                engine = difflib.Differ(charjunk=difflib.IS_CHARACTER_JUNK)
                diff = list(engine.compare(want_lines, got_lines))
                kind = 'ndiff with -expected +actual'
            else:
                assert 0, 'Bad diff option'
            return 'Differences (%s):\n' % kind + _indent(''.join(diff))
        if want and got:
            return 'Expected:\n%sGot:\n%s' % (_indent(want), _indent(got))
        elif want:
            return 'Expected:\n%sGot nothing\n' % _indent(want)
        elif got:
            return 'Expected nothing\nGot:\n%s' % _indent(got)
        else:
            return 'Expected nothing\nGot nothing\n'
_装类转发(输出检查器, {'check_output': '检查输出', 'output_difference': '输出差异'}, {'check_output': '检查输出', 'output_difference': '输出差异'})

class 文档测试失败(Exception):
    """A DocTest example has failed in debugging mode.

    The exception instance has variables:

    - test: the DocTest object being run

    - example: the Example object that failed

    - got: the actual output
    """

    def __init__(self, test, example, got):
        self.test = test
        self.example = example
        self.got = got

    def __str__(self):
        return str(self.test)

class 意外异常(Exception):
    """A DocTest example has encountered an unexpected exception

    The exception instance has variables:

    - test: the DocTest object being run

    - example: the Example object that failed

    - exc_info: the exception info
    """

    def __init__(self, test, example, exc_info):
        self.test = test
        self.example = example
        self.exc_info = exc_info

    def __str__(self):
        return str(self.test)

class 调试运行器(文档测试运行器):
    """Run doc tests but raise an exception as soon as there is a failure.

       If an unexpected exception occurs, an UnexpectedException is raised.
       It contains the test, the example, and the original exception:

         >>> runner = DebugRunner(verbose=False)
         >>> test = DocTestParser().get_doctest('>>> raise KeyError\\n42',
         ...                                    {}, 'foo', 'foo.py', 0)
         >>> try:
         ...     runner.run(test)
         ... except UnexpectedException as f:
         ...     failure = f

         >>> failure.test is test
         True

         >>> failure.example.want
         '42\\n'

         >>> exc_info = failure.exc_info
         >>> raise exc_info[1] # Already has the traceback
         Traceback (most recent call last):
         ...
         KeyError

       We wrap the original exception to give the calling application
       access to the test and example information.

       If the output doesn't match, then a DocTestFailure is raised:

         >>> test = DocTestParser().get_doctest('''
         ...      >>> x = 1
         ...      >>> x
         ...      2
         ...      ''', {}, 'foo', 'foo.py', 0)

         >>> try:
         ...    runner.run(test)
         ... except DocTestFailure as f:
         ...    failure = f

       DocTestFailure objects provide access to the test:

         >>> failure.test is test
         True

       As well as to the example:

         >>> failure.example.want
         '2\\n'

       and the actual output:

         >>> failure.got
         '1\\n'

       If a failure or error occurs, the globals are left intact:

         >>> del test.globs['__builtins__']
         >>> test.globs
         {'x': 1}

         >>> test = DocTestParser().get_doctest('''
         ...      >>> x = 2
         ...      >>> raise KeyError
         ...      ''', {}, 'foo', 'foo.py', 0)

         >>> runner.run(test)
         Traceback (most recent call last):
         ...
         doctest.UnexpectedException: <DocTest foo from foo.py:0 (2 examples)>

         >>> del test.globs['__builtins__']
         >>> test.globs
         {'x': 2}

       But the globals are cleared if there is no error:

         >>> test = DocTestParser().get_doctest('''
         ...      >>> x = 2
         ...      ''', {}, 'foo', 'foo.py', 0)

         >>> runner.run(test)
         TestResults(failed=0, attempted=1)

         >>> test.globs
         {}

       """

    def 运行(self, test, compileflags=None, out=None, clear_globs=True):
        r = 文档测试运行器.运行(self, test, compileflags, out, False)
        if clear_globs:
            test.globs.clear()
        return r

    def 报告意外异常(self, out, test, example, exc_info):
        raise 意外异常(test, example, exc_info)

    def 报告失败(self, out, test, example, got):
        raise 文档测试失败(test, example, got)
_装类转发(调试运行器, {'report_failure': '报告失败', 'report_unexpected_exception': '报告意外异常', 'run': '运行'}, {'report_failure': '报告失败', 'report_unexpected_exception': '报告意外异常', 'run': '运行'})
主运行器 = None

def 测试模块(m=None, name=None, globs=None, verbose=None, report=True, optionflags=0, extraglobs=None, raise_on_error=False, exclude_empty=False):
    """m=None, name=None, globs=None, verbose=None, report=True,
       optionflags=0, extraglobs=None, raise_on_error=False,
       exclude_empty=False

    Test examples in docstrings in functions and classes reachable
    from module m (or the current module if m is not supplied), starting
    with m.__doc__.

    Also test examples reachable from dict m.__test__ if it exists.
    m.__test__ maps names to functions, classes and strings;
    function and class docstrings are tested even if the name is private;
    strings are tested directly, as if they were docstrings.

    Return (#failures, #tests).

    See help(doctest) for an overview.

    Optional keyword arg "name" gives the name of the module; by default
    use m.__name__.

    Optional keyword arg "globs" gives a dict to be used as the globals
    when executing examples; by default, use m.__dict__.  A copy of this
    dict is actually used for each docstring, so that each docstring's
    examples start with a clean slate.

    Optional keyword arg "extraglobs" gives a dictionary that should be
    merged into the globals that are used to execute examples.  By
    default, no extra globals are used.  This is new in 2.4.

    Optional keyword arg "verbose" prints lots of stuff if true, prints
    only failures if false; by default, it's true iff "-v" is in sys.argv.

    Optional keyword arg "report" prints a summary at the end when true,
    else prints nothing at the end.  In verbose mode, the summary is
    detailed, else very brief (in fact, empty if all tests passed).

    Optional keyword arg "optionflags" or's together module constants,
    and defaults to 0.  This is new in 2.3.  Possible values (see the
    docs for details):

        DONT_ACCEPT_TRUE_FOR_1
        DONT_ACCEPT_BLANKLINE
        NORMALIZE_WHITESPACE
        ELLIPSIS
        SKIP
        IGNORE_EXCEPTION_DETAIL
        REPORT_UDIFF
        REPORT_CDIFF
        REPORT_NDIFF
        REPORT_ONLY_FIRST_FAILURE

    Optional keyword arg "raise_on_error" raises an exception on the
    first unexpected exception or failure. This allows failures to be
    post-mortem debugged.

    Advanced tomfoolery:  testmod runs methods of a local instance of
    class doctest.Tester, then merges the results into (or creates)
    global Tester instance doctest.master.  Methods of doctest.master
    can be called directly too, if you want to do something unusual.
    Passing report=0 to testmod is especially useful then, to delay
    displaying a summary.  Invoke doctest.master.summarize(verbose)
    when you're done fiddling.
    """
    global 主运行器
    if m is None:
        m = sys.modules.get('__main__')
    if not inspect.ismodule(m):
        raise TypeError('testmod: module required; %r' % (m,))
    if name is None:
        name = m.__name__
    finder = 文档测试查找器(exclude_empty=exclude_empty)
    if raise_on_error:
        runner = 调试运行器(verbose=verbose, optionflags=optionflags)
    else:
        runner = 文档测试运行器(verbose=verbose, optionflags=optionflags)
    for test in finder.find(m, name, globs=globs, extraglobs=extraglobs):
        runner.run(test)
    if report:
        runner.summarize()
    if 主运行器 is None:
        主运行器 = runner
    else:
        主运行器.merge(runner)
    return 测试结果(runner.failures, runner.tries, skipped=runner.skips)

def 测试文件(filename, module_relative=True, name=None, package=None, globs=None, verbose=None, report=True, optionflags=0, extraglobs=None, raise_on_error=False, parser=文档测试解析器(), encoding=None):
    """
    Test examples in the given file.  Return (#failures, #tests).

    Optional keyword arg "module_relative" specifies how filenames
    should be interpreted:

      - If "module_relative" is True (the default), then "filename"
         specifies a module-relative path.  By default, this path is
         relative to the calling module's directory; but if the
         "package" argument is specified, then it is relative to that
         package.  To ensure os-independence, "filename" should use
         "/" characters to separate path segments, and should not
         be an absolute path (i.e., it may not begin with "/").

      - If "module_relative" is False, then "filename" specifies an
        os-specific path.  The path may be absolute or relative (to
        the current working directory).

    Optional keyword arg "name" gives the name of the test; by default
    use the file's basename.

    Optional keyword argument "package" is a Python package or the
    name of a Python package whose directory should be used as the
    base directory for a module relative filename.  If no package is
    specified, then the calling module's directory is used as the base
    directory for module relative filenames.  It is an error to
    specify "package" if "module_relative" is False.

    Optional keyword arg "globs" gives a dict to be used as the globals
    when executing examples; by default, use {}.  A copy of this dict
    is actually used for each docstring, so that each docstring's
    examples start with a clean slate.

    Optional keyword arg "extraglobs" gives a dictionary that should be
    merged into the globals that are used to execute examples.  By
    default, no extra globals are used.

    Optional keyword arg "verbose" prints lots of stuff if true, prints
    only failures if false; by default, it's true iff "-v" is in sys.argv.

    Optional keyword arg "report" prints a summary at the end when true,
    else prints nothing at the end.  In verbose mode, the summary is
    detailed, else very brief (in fact, empty if all tests passed).

    Optional keyword arg "optionflags" or's together module constants,
    and defaults to 0.  Possible values (see the docs for details):

        DONT_ACCEPT_TRUE_FOR_1
        DONT_ACCEPT_BLANKLINE
        NORMALIZE_WHITESPACE
        ELLIPSIS
        SKIP
        IGNORE_EXCEPTION_DETAIL
        REPORT_UDIFF
        REPORT_CDIFF
        REPORT_NDIFF
        REPORT_ONLY_FIRST_FAILURE

    Optional keyword arg "raise_on_error" raises an exception on the
    first unexpected exception or failure. This allows failures to be
    post-mortem debugged.

    Optional keyword arg "parser" specifies a DocTestParser (or
    subclass) that should be used to extract tests from the files.

    Optional keyword arg "encoding" specifies an encoding that should
    be used to convert the file to unicode.

    Advanced tomfoolery:  testmod runs methods of a local instance of
    class doctest.Tester, then merges the results into (or creates)
    global Tester instance doctest.master.  Methods of doctest.master
    can be called directly too, if you want to do something unusual.
    Passing report=0 to testmod is especially useful then, to delay
    displaying a summary.  Invoke doctest.master.summarize(verbose)
    when you're done fiddling.
    """
    global 主运行器
    if package and (not module_relative):
        raise ValueError('Package may only be specified for module-relative paths.')
    text, filename = _load_testfile(filename, package, module_relative, encoding or 'utf-8')
    if name is None:
        name = os.path.basename(filename)
    if globs is None:
        globs = {}
    else:
        globs = globs.copy()
    if extraglobs is not None:
        globs.update(extraglobs)
    if '__name__' not in globs:
        globs['__name__'] = '__main__'
    if raise_on_error:
        runner = 调试运行器(verbose=verbose, optionflags=optionflags)
    else:
        runner = 文档测试运行器(verbose=verbose, optionflags=optionflags)
    test = parser.get_doctest(text, globs, name, filename, 0)
    runner.run(test)
    if report:
        runner.summarize()
    if 主运行器 is None:
        主运行器 = runner
    else:
        主运行器.merge(runner)
    return 测试结果(runner.failures, runner.tries, skipped=runner.skips)

def 运行文档串示例(f, globs, verbose=False, name='NoName', compileflags=None, optionflags=0):
    """
    Test examples in the given object's docstring (`f`), using `globs`
    as globals.  Optional argument `name` is used in failure messages.
    If the optional argument `verbose` is true, then generate output
    even if there are no failures.

    `compileflags` gives the set of flags that should be used by the
    Python compiler when running the examples.  If not specified, then
    it will default to the set of future-import flags that apply to
    `globs`.

    Optional keyword arg `optionflags` specifies options for the
    testing and output.  See the documentation for `testmod` for more
    information.
    """
    finder = 文档测试查找器(verbose=verbose, recurse=False)
    runner = 文档测试运行器(verbose=verbose, optionflags=optionflags)
    for test in finder.find(f, name, globs=globs):
        runner.run(test, compileflags=compileflags)
_unittest_reportflags = 0

def 设单元测试报告标志(flags):
    """Sets the unittest option flags.

    The old flag is returned so that a runner could restore the old
    value if it wished to:

      >>> import doctest
      >>> old = doctest._unittest_reportflags
      >>> doctest.set_unittest_reportflags(REPORT_NDIFF |
      ...                          REPORT_ONLY_FIRST_FAILURE) == old
      True

      >>> doctest._unittest_reportflags == (REPORT_NDIFF |
      ...                                   REPORT_ONLY_FIRST_FAILURE)
      True

    Only reporting flags can be set:

      >>> doctest.set_unittest_reportflags(ELLIPSIS)
      Traceback (most recent call last):
      ...
      ValueError: ('Only reporting flags allowed', 8)

      >>> doctest.set_unittest_reportflags(old) == (REPORT_NDIFF |
      ...                                   REPORT_ONLY_FIRST_FAILURE)
      True
    """
    global _unittest_reportflags
    if flags & 报告标志 != flags:
        raise ValueError('Only reporting flags allowed', flags)
    old = _unittest_reportflags
    _unittest_reportflags = flags
    return old

class 文档测试用例(unittest.TestCase):

    def __init__(self, test, optionflags=0, setUp=None, tearDown=None, checker=None):
        unittest.TestCase.__init__(self)
        self._dt_optionflags = optionflags
        self._dt_checker = checker
        self._dt_test = test
        self._dt_setUp = setUp
        self._dt_tearDown = tearDown

    def setUp(self):
        test = self._dt_test
        self._dt_globs = test.globs.copy()
        if self._dt_setUp is not None:
            self._dt_setUp(test)

    def tearDown(self):
        test = self._dt_test
        if self._dt_tearDown is not None:
            self._dt_tearDown(test)
        test.globs.clear()
        test.globs.update(self._dt_globs)

    def runTest(self):
        test = self._dt_test
        old = sys.stdout
        new = StringIO()
        optionflags = self._dt_optionflags
        if not optionflags & 报告标志:
            optionflags |= _unittest_reportflags
        runner = 文档测试运行器(optionflags=optionflags, checker=self._dt_checker, verbose=False)
        try:
            runner.DIVIDER = '-' * 70
            results = runner.run(test, out=new.write, clear_globs=False)
            if results.skipped == results.attempted:
                raise unittest.SkipTest('all examples were skipped')
        finally:
            sys.stdout = old
        if results.failed:
            raise self.failureException(self.格式化失败(new.getvalue().rstrip('\n')))

    def 格式化失败(self, err):
        test = self._dt_test
        if test.lineno is None:
            lineno = 'unknown line number'
        else:
            lineno = '%s' % test.lineno
        lname = '.'.join(test.name.split('.')[-1:])
        return 'Failed doctest test for %s\n  File "%s", line %s, in %s\n\n%s' % (test.name, test.filename, lineno, lname, err)

    def debug(self):
        """Run the test case without results and without catching exceptions

           The unit test framework includes a debug method on test cases
           and test suites to support post-mortem debugging.  The test code
           is run in such a way that errors are not caught.  This way a
           caller can catch the errors and initiate post-mortem debugging.

           The DocTestCase provides a debug method that raises
           UnexpectedException errors if there is an unexpected
           exception:

             >>> test = DocTestParser().get_doctest('>>> raise KeyError\\n42',
             ...                {}, 'foo', 'foo.py', 0)
             >>> case = DocTestCase(test)
             >>> try:
             ...     case.debug()
             ... except UnexpectedException as f:
             ...     failure = f

           The UnexpectedException contains the test, the example, and
           the original exception:

             >>> failure.test is test
             True

             >>> failure.example.want
             '42\\n'

             >>> exc_info = failure.exc_info
             >>> raise exc_info[1] # Already has the traceback
             Traceback (most recent call last):
             ...
             KeyError

           If the output doesn't match, then a DocTestFailure is raised:

             >>> test = DocTestParser().get_doctest('''
             ...      >>> x = 1
             ...      >>> x
             ...      2
             ...      ''', {}, 'foo', 'foo.py', 0)
             >>> case = DocTestCase(test)

             >>> try:
             ...    case.debug()
             ... except DocTestFailure as f:
             ...    failure = f

           DocTestFailure objects provide access to the test:

             >>> failure.test is test
             True

           As well as to the example:

             >>> failure.example.want
             '2\\n'

           and the actual output:

             >>> failure.got
             '1\\n'

           """
        self.setUp()
        runner = 调试运行器(optionflags=self._dt_optionflags, checker=self._dt_checker, verbose=False)
        runner.run(self._dt_test, clear_globs=False)
        self.tearDown()

    def id(self):
        return self._dt_test.name

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self._dt_test == other._dt_test and self._dt_optionflags == other._dt_optionflags and (self._dt_setUp == other._dt_setUp) and (self._dt_tearDown == other._dt_tearDown) and (self._dt_checker == other._dt_checker)

    def __hash__(self):
        return hash((self._dt_optionflags, self._dt_setUp, self._dt_tearDown, self._dt_checker))

    def __repr__(self):
        name = self._dt_test.name.split('.')
        return '%s (%s)' % (name[-1], '.'.join(name[:-1]))
    __str__ = object.__str__

    def shortDescription(self):
        return 'Doctest: ' + self._dt_test.name
_装类转发(文档测试用例, {'format_failure': '格式化失败'}, {'format_failure': '格式化失败'})

class 跳过文档测试用例(文档测试用例):

    def __init__(self, module):
        self.module = module
        文档测试用例.__init__(self, None)

    def setUp(self):
        self.skipTest('DocTestSuite will not work with -O2 and above')

    def test_skip(self):
        pass

    def shortDescription(self):
        return 'Skipping tests from %s' % self.module.__name__
    __str__ = shortDescription

class _DocTestSuite(unittest.TestSuite):

    def _removeTestAtIndex(self, index):
        pass

def 文档测试套件(module=None, globs=None, extraglobs=None, test_finder=None, **options):
    """
    Convert doctest tests for a module to a unittest test suite.

    This converts each documentation string in a module that
    contains doctest tests to a unittest test case.  If any of the
    tests in a doc string fail, then the test case fails.  An exception
    is raised showing the name of the file containing the test and a
    (sometimes approximate) line number.

    The `module` argument provides the module to be tested.  The argument
    can be either a module or a module name.

    If no argument is given, the calling module is used.

    A number of options may be provided as keyword arguments:

    setUp
      A set-up function.  This is called before running the
      tests in each file. The setUp function will be passed a DocTest
      object.  The setUp function can access the test globals as the
      globs attribute of the test passed.

    tearDown
      A tear-down function.  This is called after running the
      tests in each file.  The tearDown function will be passed a DocTest
      object.  The tearDown function can access the test globals as the
      globs attribute of the test passed.

    globs
      A dictionary containing initial global variables for the tests.

    optionflags
       A set of doctest option flags expressed as an integer.
    """
    if test_finder is None:
        test_finder = 文档测试查找器()
    module = _normalize_module(module)
    tests = test_finder.find(module, globs=globs, extraglobs=extraglobs)
    if not tests and sys.flags.optimize >= 2:
        suite = _DocTestSuite()
        suite.addTest(跳过文档测试用例(module))
        return suite
    tests.sort()
    suite = _DocTestSuite()
    for test in tests:
        if len(test.examples) == 0:
            continue
        if not test.filename:
            filename = module.__file__
            if filename[-4:] == '.pyc':
                filename = filename[:-1]
            test.filename = filename
        suite.addTest(文档测试用例(test, **options))
    return suite

class 文档文件用例(文档测试用例):

    def id(self):
        return '_'.join(self._dt_test.name.split('.'))

    def __repr__(self):
        return self._dt_test.filename

    def 格式化失败(self, err):
        return 'Failed doctest test for %s\n  File "%s", line 0\n\n%s' % (self._dt_test.name, self._dt_test.filename, err)
_装类转发(文档文件用例, {'format_failure': '格式化失败'}, {'format_failure': '格式化失败'})

def 文档文件测试(path, module_relative=True, package=None, globs=None, parser=文档测试解析器(), encoding=None, **options):
    if globs is None:
        globs = {}
    else:
        globs = globs.copy()
    if package and (not module_relative):
        raise ValueError('Package may only be specified for module-relative paths.')
    doc, path = _load_testfile(path, package, module_relative, encoding or 'utf-8')
    if '__file__' not in globs:
        globs['__file__'] = path
    name = os.path.basename(path)
    test = parser.get_doctest(doc, globs, name, path, 0)
    return 文档文件用例(test, **options)

def 文档文件套件(*paths, **kw):
    """A unittest suite for one or more doctest files.

    The path to each doctest file is given as a string; the
    interpretation of that string depends on the keyword argument
    "module_relative".

    A number of options may be provided as keyword arguments:

    module_relative
      If "module_relative" is True, then the given file paths are
      interpreted as os-independent module-relative paths.  By
      default, these paths are relative to the calling module's
      directory; but if the "package" argument is specified, then
      they are relative to that package.  To ensure os-independence,
      "filename" should use "/" characters to separate path
      segments, and may not be an absolute path (i.e., it may not
      begin with "/").

      If "module_relative" is False, then the given file paths are
      interpreted as os-specific paths.  These paths may be absolute
      or relative (to the current working directory).

    package
      A Python package or the name of a Python package whose directory
      should be used as the base directory for module relative paths.
      If "package" is not specified, then the calling module's
      directory is used as the base directory for module relative
      filenames.  It is an error to specify "package" if
      "module_relative" is False.

    setUp
      A set-up function.  This is called before running the
      tests in each file. The setUp function will be passed a DocTest
      object.  The setUp function can access the test globals as the
      globs attribute of the test passed.

    tearDown
      A tear-down function.  This is called after running the
      tests in each file.  The tearDown function will be passed a DocTest
      object.  The tearDown function can access the test globals as the
      globs attribute of the test passed.

    globs
      A dictionary containing initial global variables for the tests.

    optionflags
      A set of doctest option flags expressed as an integer.

    parser
      A DocTestParser (or subclass) that should be used to extract
      tests from the files.

    encoding
      An encoding that will be used to convert the files to unicode.
    """
    suite = _DocTestSuite()
    if kw.get('module_relative', True):
        kw['package'] = _normalize_module(kw.get('package'))
    for path in paths:
        suite.addTest(文档文件测试(path, **kw))
    return suite

def 从示例生成脚本(s):
    """Extract script from text with examples.

       Converts text with examples to a Python script.  Example input is
       converted to regular code.  Example output and all other words
       are converted to comments:

       >>> text = '''
       ...       Here are examples of simple math.
       ...
       ...           Python has super accurate integer addition
       ...
       ...           >>> 2 + 2
       ...           5
       ...
       ...           And very friendly error messages:
       ...
       ...           >>> 1/0
       ...           To Infinity
       ...           And
       ...           Beyond
       ...
       ...           You can use logic if you want:
       ...
       ...           >>> if 0:
       ...           ...    blah
       ...           ...    blah
       ...           ...
       ...
       ...           Ho hum
       ...           '''

       >>> print(script_from_examples(text))
       # Here are examples of simple math.
       #
       #     Python has super accurate integer addition
       #
       2 + 2
       # Expected:
       ## 5
       #
       #     And very friendly error messages:
       #
       1/0
       # Expected:
       ## To Infinity
       ## And
       ## Beyond
       #
       #     You can use logic if you want:
       #
       if 0:
          blah
          blah
       #
       #     Ho hum
       <BLANKLINE>
       """
    output = []
    for piece in 文档测试解析器().parse(s):
        if isinstance(piece, 示例):
            output.append(piece.source[:-1])
            want = piece.want
            if want:
                output.append('# Expected:')
                output += ['## ' + l for l in want.split('\n')[:-1]]
        else:
            output += [_comment_line(l) for l in piece.split('\n')[:-1]]
    while output and output[-1] == '#':
        output.pop()
    while output and output[0] == '#':
        output.pop(0)
    return '\n'.join(output) + '\n'

def 测试源码(module, name):
    """Extract the test sources from a doctest docstring as a script.

    Provide the module (or dotted name of the module) containing the
    test to be debugged and the name (within the module) of the object
    with the doc string with tests to be debugged.
    """
    module = _normalize_module(module)
    tests = 文档测试查找器().find(module)
    test = [t for t in tests if t.name == name]
    if not test:
        raise ValueError(name, 'not found in tests')
    test = test[0]
    testsrc = 从示例生成脚本(test.docstring)
    return testsrc

def 调试源码(src, pm=False, globs=None):
    """Debug a single doctest docstring, in argument `src`"""
    testsrc = 从示例生成脚本(src)
    调试脚本(testsrc, pm, globs)

def 调试脚本(src, pm=False, globs=None):
    """Debug a test script.  `src` is the script, as a string."""
    import pdb
    if globs:
        globs = globs.copy()
    else:
        globs = {}
    if pm:
        try:
            exec(src, globs, globs)
        except:
            print(sys.exc_info()[1])
            p = pdb.Pdb(nosigint=True)
            p.reset()
            p.interaction(None, sys.exc_info()[2])
    else:
        pdb.Pdb(nosigint=True).run('exec(%r)' % src, globs, globs)

def debug(module, name, pm=False):
    """Debug a single doctest docstring.

    Provide the module (or dotted name of the module) containing the
    test to be debugged and the name (within the module) of the object
    with the docstring with tests to be debugged.
    """
    module = _normalize_module(module)
    testsrc = 测试源码(module, name)
    调试脚本(testsrc, pm, module.__dict__)

class _TestClass:
    """
    A pointless class, for sanity-checking of docstring testing.

    Methods:
        square()
        get()

    >>> _TestClass(13).get() + _TestClass(-12).get()
    1
    >>> hex(_TestClass(13).square().get())
    '0xa9'
    """

    def __init__(self, val):
        """val -> _TestClass object with associated value val.

        >>> t = _TestClass(123)
        >>> print(t.get())
        123
        """
        self.val = val

    def square(self):
        """square() -> square TestClass's associated value

        >>> _TestClass(13).square().get()
        169
        """
        self.val = self.val ** 2
        return self

    def get(self):
        """get() -> return TestClass's associated value.

        >>> x = _TestClass(-42)
        >>> print(x.get())
        -42
        """
        return self.val
__test__ = {'_TestClass': _TestClass, 'string': '\n                      Example of a string object, searched as-is.\n                      >>> x = 1; y = 2\n                      >>> x + y, x * y\n                      (3, 2)\n                      ', 'bool-int equivalence': '\n                                    In 2.2, boolean expressions displayed\n                                    0 or 1.  By default, we still accept\n                                    them.  This can be disabled by passing\n                                    DONT_ACCEPT_TRUE_FOR_1 to the new\n                                    optionflags argument.\n                                    >>> 4 == 4\n                                    1\n                                    >>> 4 == 4\n                                    True\n                                    >>> 4 > 4\n                                    0\n                                    >>> 4 > 4\n                                    False\n                                    ', 'blank lines': "\n                Blank lines can be marked with <BLANKLINE>:\n                    >>> print('foo\\n\\nbar\\n')\n                    foo\n                    <BLANKLINE>\n                    bar\n                    <BLANKLINE>\n            ", 'ellipsis': "\n                If the ellipsis flag is used, then '...' can be used to\n                elide substrings in the desired output:\n                    >>> print(list(range(1000))) #doctest: +ELLIPSIS\n                    [0, 1, 2, ..., 999]\n            ", 'whitespace normalization': '\n                If the whitespace normalization flag is used, then\n                differences in whitespace are ignored.\n                    >>> print(list(range(30))) #doctest: +NORMALIZE_WHITESPACE\n                    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,\n                     15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,\n                     27, 28, 29]\n            '}

def _test():
    import argparse
    parser = argparse.ArgumentParser(description='doctest runner', color=True)
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print very verbose output for all tests')
    parser.add_argument('-o', '--option', action='append', choices=按名索引的选项标志.keys(), default=[], help='specify a doctest option flag to apply to the test run; may be specified more than once to apply multiple options')
    parser.add_argument('-f', '--fail-fast', action='store_true', help='stop running tests after first failure (this is a shorthand for -o FAIL_FAST, and is in addition to any other -o options)')
    parser.add_argument('file', nargs='+', help='file containing the tests to run')
    args = parser.parse_args()
    testfiles = args.file
    verbose = args.verbose
    options = 0
    for option in args.option:
        options |= 按名索引的选项标志[option]
    if args.fail_fast:
        options |= 快速失败
    for filename in testfiles:
        if filename.endswith('.py'):
            dirname, filename = os.path.split(filename)
            sys.path.insert(0, dirname)
            m = __import__(filename[:-3])
            del sys.path[0]
            failures, _ = 测试模块(m, verbose=verbose, optionflags=options)
        else:
            failures, _ = 测试文件(filename, module_relative=False, verbose=verbose, optionflags=options)
        if failures:
            return 1
    return 0
if __name__ == '__main__':
    sys.exit(_test())


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BLANKLINE_MARKER': '空行标记',
    'COMPARISON_FLAGS': '比较标志',
    'DONT_ACCEPT_BLANKLINE': '不接受空行标记',
    'DONT_ACCEPT_TRUE_FOR_1': '不接受1代真',
    'DebugRunner': '调试运行器',
    'DocFileCase': '文档文件用例',
    'DocFileSuite': '文档文件套件',
    'DocFileTest': '文档文件测试',
    'DocTest': '文档测试',
    'DocTestCase': '文档测试用例',
    'DocTestFailure': '文档测试失败',
    'DocTestFinder': '文档测试查找器',
    'DocTestParser': '文档测试解析器',
    'DocTestRunner': '文档测试运行器',
    'DocTestSuite': '文档测试套件',
    'ELLIPSIS': '省略号',
    'ELLIPSIS_MARKER': '省略号标记',
    'Example': '示例',
    'FAIL_FAST': '快速失败',
    'IGNORE_EXCEPTION_DETAIL': '忽略异常细节',
    'NORMALIZE_WHITESPACE': '规范化空白',
    'OPTIONFLAGS_BY_NAME': '按名索引的选项标志',
    'OutputChecker': '输出检查器',
    'REPORTING_FLAGS': '报告标志',
    'REPORT_CDIFF': '报告上下文差异',
    'REPORT_NDIFF': '报告逐行差异',
    'REPORT_ONLY_FIRST_FAILURE': '只报首个失败',
    'REPORT_UDIFF': '报告统一差异',
    'SKIP': '跳过该例',
    'SkipDocTestCase': '跳过文档测试用例',
    'TestResults': '测试结果',
    'UnexpectedException': '意外异常',
    'debug_script': '调试脚本',
    'debug_src': '调试源码',
    'master': '主运行器',
    'register_optionflag': '登记选项标志',
    'run_docstring_examples': '运行文档串示例',
    'script_from_examples': '从示例生成脚本',
    'set_unittest_reportflags': '设单元测试报告标志',
    'testfile': '测试文件',
    'testmod': '测试模块',
    'testsource': '测试源码',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '文档文件用例': {
        'format_failure': '格式化失败',
    },
    '文档测试查找器': {
        'find': '查找',
    },
    '文档测试用例': {
        'format_failure': '格式化失败',
    },
    '文档测试解析器': {
        'get_doctest': '取文档测试',
        'get_examples': '取示例',
        'parse': '解析',
    },
    '文档测试运行器': {
        'merge': '合并',
        'report_failure': '报告失败',
        'report_start': '报告开始',
        'report_success': '报告成功',
        'report_unexpected_exception': '报告意外异常',
        'run': '运行',
        'summarize': '汇总',
    },
    '调试运行器': {
        'report_failure': '报告失败',
        'report_unexpected_exception': '报告意外异常',
        'run': '运行',
    },
    '输出检查器': {
        'check_output': '检查输出',
        'output_difference': '输出差异',
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
    '文档文件用例': {
        'format_failure': '格式化失败',
    },
    '文档测试查找器': {
        'find': '查找',
    },
    '文档测试用例': {
        'format_failure': '格式化失败',
    },
    '文档测试解析器': {
        'get_doctest': '取文档测试',
        'get_examples': '取示例',
        'parse': '解析',
    },
    '文档测试运行器': {
        'merge': '合并',
        'report_failure': '报告失败',
        'report_start': '报告开始',
        'report_success': '报告成功',
        'report_unexpected_exception': '报告意外异常',
        'run': '运行',
        'summarize': '汇总',
    },
    '调试运行器': {
        'report_failure': '报告失败',
        'report_unexpected_exception': '报告意外异常',
        'run': '运行',
    },
    '输出检查器': {
        'check_output': '检查输出',
        'output_difference': '输出差异',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '不接受1代真',
    '不接受空行标记',
    '从示例生成脚本',
    '只报首个失败',
    '快速失败',
    '忽略异常细节',
    '意外异常',
    '报告上下文差异',
    '报告标志',
    '报告统一差异',
    '报告逐行差异',
    '文档文件套件',
    '文档测试',
    '文档测试失败',
    '文档测试套件',
    '文档测试查找器',
    '文档测试解析器',
    '文档测试运行器',
    '比较标志',
    '测试文件',
    '测试模块',
    '测试源码',
    '登记选项标志',
    '省略号',
    '示例',
    '规范化空白',
    '设单元测试报告标志',
    '调试源码',
    '调试运行器',
    '跳过该例',
    '输出检查器',
    '运行文档串示例',
])

# ---- 转发层结束 ----
