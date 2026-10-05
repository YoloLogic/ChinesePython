# -*- coding: utf-8 -*-
"""配置解析 —— 汉语库（由 tools/汉化库.py 从 Lib/configparser.py 机械生成，**不要手改**）。

英文库 Lib/configparser.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 配置解析
"""


"""Configuration file parser.

A configuration file consists of sections, lead by a "[section]" header,
and followed by "name: value" entries, with continuations and such in
the style of RFC 822.

Intrinsic defaults can be specified by passing them into the
ConfigParser constructor as a dictionary.

class:

ConfigParser -- responsible for parsing a list of
                    configuration files, and managing the parsed database.

    methods:

    __init__(defaults=None, dict_type=_default_dict, allow_no_value=False,
             delimiters=('=', ':'), comment_prefixes=('#', ';'),
             inline_comment_prefixes=None, strict=True,
             empty_lines_in_values=True, default_section='DEFAULT',
             interpolation=<unset>, converters=<unset>,
             allow_unnamed_section=False):
        Create the parser. When `defaults` is given, it is initialized into the
        dictionary or intrinsic defaults. The keys must be strings, the values
        must be appropriate for %()s string interpolation.

        When `dict_type` is given, it will be used to create the dictionary
        objects for the list of sections, for the options within a section, and
        for the default values.

        When `delimiters` is given, it will be used as the set of substrings
        that divide keys from values.

        When `comment_prefixes` is given, it will be used as the set of
        substrings that prefix comments in empty lines. Comments can be
        indented.

        When `inline_comment_prefixes` is given, it will be used as the set of
        substrings that prefix comments in non-empty lines.

        When `strict` is True, the parser won't allow for any section or option
        duplicates while reading from a single source (file, string or
        dictionary). Default is True.

        When `empty_lines_in_values` is False (default: True), each empty line
        marks the end of an option. Otherwise, internal empty lines of
        a multiline option are kept as part of the value.

        When `allow_no_value` is True (default: False), options without
        values are accepted; the value presented for these is None.

        When `default_section` is given, the name of the special section is
        named accordingly. By default it is called ``"DEFAULT"`` but this can
        be customized to point to any other valid section name. Its current
        value can be retrieved using the ``parser_instance.default_section``
        attribute and may be modified at runtime.

        When `interpolation` is given, it should be an Interpolation subclass
        instance. It will be used as the handler for option value
        pre-processing when using getters. RawConfigParser objects don't do
        any sort of interpolation, whereas ConfigParser uses an instance of
        BasicInterpolation. The library also provides a ``zc.buildout``
        inspired ExtendedInterpolation implementation.

        When `converters` is given, it should be a dictionary where each key
        represents the name of a type converter and each value is a callable
        implementing the conversion from string to the desired datatype. Every
        converter gets its corresponding get*() method on the parser object and
        section proxies.

        When `allow_unnamed_section` is True (default: False), options
        without section are accepted: the section for these is
        ``configparser.UNNAMED_SECTION``.

    sections()
        Return all the configuration section names, sans DEFAULT.

    has_section(section)
        Return whether the given section exists.

    has_option(section, option)
        Return whether the given option exists in the given section.

    options(section)
        Return list of configuration options for the named section.

    read(filenames, encoding=None)
        Read and parse the iterable of named configuration files, given by
        name.  A single filename is also allowed.  Non-existing files
        are ignored.  Return list of successfully read files.

    read_file(f, filename=None)
        Read and parse one configuration file, given as a file object.
        The filename defaults to f.name; it is only used in error
        messages (if f has no `name` attribute, the string `<???>` is used).

    read_string(string)
        Read configuration from a given string.

    read_dict(dictionary)
        Read configuration from a dictionary. Keys are section names,
        values are dictionaries with keys and values that should be present
        in the section. If the used dictionary type preserves order, sections
        and their keys will be added in order. Values are automatically
        converted to strings.

    get(section, option, raw=False, vars=None, fallback=_UNSET)
        Return a string value for the named option.  All % interpolations are
        expanded in the return values, based on the defaults passed into the
        constructor and the DEFAULT section.  Additional substitutions may be
        provided using the `vars` argument, which must be a dictionary whose
        contents override any pre-existing defaults. If `option` is a key in
        `vars`, the value from `vars` is used.

    getint(section, options, raw=False, vars=None, fallback=_UNSET)
        Like get(), but convert value to an integer.

    getfloat(section, options, raw=False, vars=None, fallback=_UNSET)
        Like get(), but convert value to a float.

    getboolean(section, options, raw=False, vars=None, fallback=_UNSET)
        Like get(), but convert value to a boolean (currently case
        insensitively defined as 0, false, no, off for False, and 1, true,
        yes, on for True).  Returns False or True.

    items(section=_UNSET, raw=False, vars=None)
        If section is given, return a list of tuples with (name, value) for
        each option in the section. Otherwise, return a list of tuples with
        (section_name, section_proxy) for each section, including DEFAULTSECT.

    remove_section(section)
        Remove the given file section and all its options.

    remove_option(section, option)
        Remove the given option from the given section.

    set(section, option, value)
        Set the given option.

    write(fp, space_around_delimiters=True)
        Write the configuration state in .ini format. If
        `space_around_delimiters` is True (the default), delimiters
        between keys and values are surrounded by spaces.
"""
_英文原名表 = {'BasicInterpolation': '基本插值', 'ConfigParser': '配置解析器', 'ConverterMapping': '转换器映射', 'DEFAULTSECT': '默认小节', 'DuplicateOptionError': '重复选项错误', 'DuplicateSectionError': '重复小节错误', 'Error': '错误', 'ExtendedInterpolation': '扩展插值', 'Interpolation': '插值', 'InterpolationDepthError': '插值深度错误', 'InterpolationError': '插值错误', 'InterpolationMissingOptionError': '插值缺选项错误', 'InterpolationSyntaxError': '插值语法错误', 'InvalidWriteError': '无效写入错误', 'MAX_INTERPOLATION_DEPTH': '最大插值深度', 'MissingSectionHeaderError': '缺小节头错误', 'MultilineContinuationError': '多行续行错误', 'NoOptionError': '无选项错误', 'NoSectionError': '无小节错误', 'ParsingError': '解析错误', 'RawConfigParser': '原始配置解析器', 'SectionProxy': '小节代理', 'UNNAMED_SECTION': '未命名小节', 'UnnamedSectionDisabledError': '未命名小节禁用错误'}

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
from collections.abc import Iterable, MutableMapping
from collections import ChainMap as _ChainMap
import contextlib
import functools
import io
import itertools
import os
import re
import sys
__all__ = ('NoSectionError', 'DuplicateOptionError', 'DuplicateSectionError', 'NoOptionError', 'InterpolationError', 'InterpolationDepthError', 'InterpolationMissingOptionError', 'InterpolationSyntaxError', 'ParsingError', 'MissingSectionHeaderError', 'MultilineContinuationError', 'UnnamedSectionDisabledError', 'InvalidWriteError', 'ConfigParser', 'RawConfigParser', 'Interpolation', 'BasicInterpolation', 'ExtendedInterpolation', 'SectionProxy', 'ConverterMapping', 'DEFAULTSECT', 'MAX_INTERPOLATION_DEPTH', 'UNNAMED_SECTION')
_default_dict = dict
默认小节 = 'DEFAULT'
最大插值深度 = 10

class 错误(Exception):
    """Base class for ConfigParser exceptions."""

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message
    __str__ = __repr__

class 无小节错误(错误):
    """Raised when no section matches a requested option."""

    def __init__(self, section):
        错误.__init__(self, 'No section: %r' % (section,))
        self.section = section
        self.args = (section,)

class 重复小节错误(错误):
    """Raised when a section is repeated in an input source.

    Possible repetitions that raise this exception are: multiple creation
    using the API or in strict parsers when a section is found more than once
    in a single input file, string or dictionary.
    """

    def __init__(self, section, source=None, lineno=None):
        msg = [repr(section), ' already exists']
        if source is not None:
            message = ['While reading from ', repr(source)]
            if lineno is not None:
                message.append(' [line {0:2d}]'.format(lineno))
            message.append(': section ')
            message.extend(msg)
            msg = message
        else:
            msg.insert(0, 'Section ')
        错误.__init__(self, ''.join(msg))
        self.section = section
        self.source = source
        self.lineno = lineno
        self.args = (section, source, lineno)

class 重复选项错误(错误):
    """Raised by strict parsers when an option is repeated in an input source.

    Current implementation raises this exception only when an option is found
    more than once in a single file, string or dictionary.
    """

    def __init__(self, section, option, source=None, lineno=None):
        msg = [repr(option), ' in section ', repr(section), ' already exists']
        if source is not None:
            message = ['While reading from ', repr(source)]
            if lineno is not None:
                message.append(' [line {0:2d}]'.format(lineno))
            message.append(': option ')
            message.extend(msg)
            msg = message
        else:
            msg.insert(0, 'Option ')
        错误.__init__(self, ''.join(msg))
        self.section = section
        self.option = option
        self.source = source
        self.lineno = lineno
        self.args = (section, option, source, lineno)

class 无选项错误(错误):
    """A requested option was not found."""

    def __init__(self, option, section):
        错误.__init__(self, 'No option %r in section: %r' % (option, section))
        self.option = option
        self.section = section
        self.args = (option, section)

class 插值错误(错误):
    """Base class for interpolation-related exceptions."""

    def __init__(self, option, section, msg):
        错误.__init__(self, msg)
        self.option = option
        self.section = section
        self.args = (option, section, msg)

class 插值缺选项错误(插值错误):
    """A string substitution required a setting which was not available."""

    def __init__(self, option, section, rawval, reference):
        msg = 'Bad value substitution: option {!r} in section {!r} contains an interpolation key {!r} which is not a valid option name. Raw value: {!r}'.format(option, section, reference, rawval)
        插值错误.__init__(self, option, section, msg)
        self.reference = reference
        self.args = (option, section, rawval, reference)

class 插值语法错误(插值错误):
    """Raised when the source text contains invalid syntax.

    Current implementation raises this exception when the source text into
    which substitutions are made does not conform to the required syntax.
    """

class 插值深度错误(插值错误):
    """Raised when substitutions are nested too deeply."""

    def __init__(self, option, section, rawval):
        msg = 'Recursion limit exceeded in value substitution: option {!r} in section {!r} contains an interpolation key which cannot be substituted in {} steps. Raw value: {!r}'.format(option, section, 最大插值深度, rawval)
        插值错误.__init__(self, option, section, msg)
        self.args = (option, section, rawval)

class 解析错误(错误):
    """Raised when a configuration file does not follow legal syntax."""

    def __init__(self, source, *args):
        super().__init__(f'Source contains parsing errors: {source!r}')
        self.source = source
        self.errors = []
        self.args = (source,)
        if args:
            self.append(*args)

    def append(self, lineno, line):
        self.errors.append((lineno, line))
        self.message += f'\n\t[line {lineno:2d}]: {line!r}'

    def combine(self, others):
        messages = [self.message]
        for other in others:
            for lineno, line in other.errors:
                self.errors.append((lineno, line))
                messages.append(f'\n\t[line {lineno:2d}]: {line!r}')
        self.message = ''.join(messages)
        return self

    @staticmethod
    def _raise_all(exceptions: Iterable['ParsingError']):
        """
        Combine any number of ParsingErrors into one and raise it.
        """
        exceptions = iter(exceptions)
        with contextlib.suppress(StopIteration):
            raise next(exceptions).combine(exceptions)

class 缺小节头错误(解析错误):
    """Raised when a key-value pair is found before any section header."""

    def __init__(self, filename, lineno, line):
        错误.__init__(self, 'File contains no section headers.\nfile: %r, line: %d\n%r' % (filename, lineno, line))
        self.source = filename
        self.lineno = lineno
        self.line = line
        self.args = (filename, lineno, line)

class 多行续行错误(解析错误):
    """Raised when a key without value is followed by continuation line"""

    def __init__(self, filename, lineno, line):
        错误.__init__(self, 'Key without value continued with an indented line.\nfile: %r, line: %d\n%r' % (filename, lineno, line))
        self.source = filename
        self.lineno = lineno
        self.line = line
        self.args = (filename, lineno, line)

class 未命名小节禁用错误(错误):
    """Raised when an attempt to use UNNAMED_SECTION is made with the
    feature disabled."""

    def __init__(self):
        错误.__init__(self, 'Support for UNNAMED_SECTION is disabled.')

class _UnnamedSection:

    def __repr__(self):
        return '<UNNAMED_SECTION>'

class 无效写入错误(错误):
    """Raised when attempting to write data that the parser would read back differently.
    ex: writing a key which begins with the section header pattern would read back as a
    new section """

    def __init__(self, msg=''):
        错误.__init__(self, msg)
未命名小节 = _UnnamedSection()
_UNSET = object()

class 插值:
    """Dummy interpolation that passes the value through with no changes."""

    def 取值之前(self, parser, section, option, value, defaults):
        return value

    def 设置之前(self, parser, section, option, value):
        return value

    def 读之前(self, parser, section, option, value):
        return value

    def before_write(self, parser, section, option, value):
        return value
_装类转发(插值, {'before_get': '取值之前', 'before_read': '读之前', 'before_set': '设置之前'}, {'before_get': '取值之前', 'before_read': '读之前', 'before_set': '设置之前'})

class 基本插值(插值):
    """Interpolation as implemented in the classic ConfigParser.

    The option values can contain format strings which refer to other values in
    the same section, or values in the special default section.

    For example:

        something: %(dir)s/whatever

    would resolve the "%(dir)s" to the value of dir.  All reference
    expansions are done late, on demand. If a user needs to use a bare % in
    a configuration file, she can escape it by writing %%. Other % usage
    is considered a user error and raises `InterpolationSyntaxError`."""
    _KEYCRE = re.compile('%\\(([^)]+)\\)s')

    def 取值之前(self, parser, section, option, value, defaults):
        L = []
        self._interpolate_some(parser, option, L, value, section, defaults, 1)
        return ''.join(L)

    def 设置之前(self, parser, section, option, value):
        tmp_value = value.replace('%%', '')
        tmp_value = self._KEYCRE.sub('', tmp_value)
        if '%' in tmp_value:
            raise ValueError('invalid interpolation syntax in %r at position %d' % (value, tmp_value.find('%')))
        return value

    def _interpolate_some(self, parser, option, accum, rest, section, map, depth):
        rawval = parser.get(section, option, raw=True, fallback=rest)
        if depth > 最大插值深度:
            raise 插值深度错误(option, section, rawval)
        while rest:
            p = rest.find('%')
            if p < 0:
                accum.append(rest)
                return
            if p > 0:
                accum.append(rest[:p])
                rest = rest[p:]
            c = rest[1:2]
            if c == '%':
                accum.append('%')
                rest = rest[2:]
            elif c == '(':
                m = self._KEYCRE.match(rest)
                if m is None:
                    raise 插值语法错误(option, section, 'bad interpolation variable reference %r' % rest)
                var = parser.optionxform(m.group(1))
                rest = rest[m.end():]
                try:
                    v = map[var]
                except KeyError:
                    raise 插值缺选项错误(option, section, rawval, var) from None
                if '%' in v:
                    self._interpolate_some(parser, option, accum, v, section, map, depth + 1)
                else:
                    accum.append(v)
            else:
                raise 插值语法错误(option, section, "'%%' must be followed by '%%' or '(', found: %r" % (rest,))
_装类转发(基本插值, {'before_get': '取值之前', 'before_set': '设置之前'}, {'before_get': '取值之前', 'before_set': '设置之前'})

class 扩展插值(插值):
    """Advanced variant of interpolation, supports the syntax used by
    `zc.buildout`. Enables interpolation between sections."""
    _KEYCRE = re.compile('\\$\\{([^}]+)\\}')

    def 取值之前(self, parser, section, option, value, defaults):
        L = []
        self._interpolate_some(parser, option, L, value, section, defaults, 1)
        return ''.join(L)

    def 设置之前(self, parser, section, option, value):
        tmp_value = value.replace('$$', '')
        tmp_value = self._KEYCRE.sub('', tmp_value)
        if '$' in tmp_value:
            raise ValueError('invalid interpolation syntax in %r at position %d' % (value, tmp_value.find('$')))
        return value

    def _interpolate_some(self, parser, option, accum, rest, section, map, depth):
        rawval = parser.get(section, option, raw=True, fallback=rest)
        if depth > 最大插值深度:
            raise 插值深度错误(option, section, rawval)
        while rest:
            p = rest.find('$')
            if p < 0:
                accum.append(rest)
                return
            if p > 0:
                accum.append(rest[:p])
                rest = rest[p:]
            c = rest[1:2]
            if c == '$':
                accum.append('$')
                rest = rest[2:]
            elif c == '{':
                m = self._KEYCRE.match(rest)
                if m is None:
                    raise 插值语法错误(option, section, 'bad interpolation variable reference %r' % rest)
                path = m.group(1).split(':')
                rest = rest[m.end():]
                sect = section
                opt = option
                try:
                    if len(path) == 1:
                        opt = parser.optionxform(path[0])
                        v = map[opt]
                    elif len(path) == 2:
                        sect = path[0]
                        opt = parser.optionxform(path[1])
                        v = parser.get(sect, opt, raw=True)
                    else:
                        raise 插值语法错误(option, section, "More than one ':' found: %r" % (rest,))
                except (KeyError, 无小节错误, 无选项错误):
                    raise 插值缺选项错误(option, section, rawval, ':'.join(path)) from None
                if v is None:
                    continue
                if '$' in v:
                    self._interpolate_some(parser, opt, accum, v, sect, dict(parser.items(sect, raw=True)), depth + 1)
                else:
                    accum.append(v)
            else:
                raise 插值语法错误(option, section, "'$' must be followed by '$' or '{', found: %r" % (rest,))
_装类转发(扩展插值, {'before_get': '取值之前', 'before_set': '设置之前'}, {'before_get': '取值之前', 'before_set': '设置之前'})

class _ReadState:
    elements_added: set[str]
    cursect: dict[str, str] | None = None
    sectname: str | None = None
    optname: str | None = None
    lineno: int = 0
    indent_level: int = 0
    errors: list[解析错误]

    def __init__(self):
        self.elements_added = set()
        self.errors = list()

class _Line(str):
    __slots__ = ('clean', 'has_comments')

    def __new__(cls, val, *args, **kwargs):
        return super().__new__(cls, val)

    def __init__(self, val, comments):
        trimmed = val.strip()
        self.clean = comments.strip(trimmed)
        self.has_comments = trimmed != self.clean

class _CommentSpec:

    def __init__(self, full_prefixes, inline_prefixes):
        full_patterns = (f'^({re.escape(prefix)}).*' for prefix in full_prefixes)
        inline_patterns = (f'(^|\\s)({re.escape(prefix)}.*)' for prefix in inline_prefixes)
        self.pattern = re.compile('|'.join(itertools.chain(full_patterns, inline_patterns)))

    def strip(self, text):
        return self.pattern.sub('', text).rstrip()

    def wrap(self, text):
        return _Line(text, self)

class 原始配置解析器(MutableMapping):
    """ConfigParser that does not do interpolation."""
    _SECT_TMPL = '\n        \\[                                 # [\n        (?P<header>.+)                     # very permissive!\n        \\]                                 # ]\n        '
    _OPT_TMPL = '\n        (?P<option>                        # very permissive!\n            (?:(?!{delim})\\S)*             # non-delimiter non-whitespace\n            (?:\\s+(?:(?!{delim})\\S)+)*)    # optionally more words\n        \\s*(?P<vi>{delim})\\s*              # any number of space/tab,\n                                           # followed by any of the\n                                           # allowed delimiters,\n                                           # followed by any space/tab\n        (?P<value>.*)$                     # everything up to eol\n        '
    _OPT_NV_TMPL = '\n        (?P<option>                        # very permissive!\n            (?:(?!{delim})\\S)*             # non-delimiter non-whitespace\n            (?:\\s+(?:(?!{delim})\\S)+)*)    # optionally more words\n        \\s*(?:                             # any number of space/tab,\n        (?P<vi>{delim})\\s*                 # optionally followed by\n                                           # any of the allowed\n                                           # delimiters, followed by any\n                                           # space/tab\n        (?P<value>.*))?$                   # everything up to eol\n        '
    _DEFAULT_INTERPOLATION = 插值()
    SECTCRE = re.compile(_SECT_TMPL, re.VERBOSE)
    OPTCRE = re.compile(_OPT_TMPL.format(delim='=|:'), re.VERBOSE)
    OPTCRE_NV = re.compile(_OPT_NV_TMPL.format(delim='=|:'), re.VERBOSE)
    NONSPACECRE = re.compile('\\S')
    BOOLEAN_STATES = {'1': True, 'yes': True, 'true': True, 'on': True, '0': False, 'no': False, 'false': False, 'off': False}

    def __init__(self, defaults=None, dict_type=_default_dict, allow_no_value=False, *, delimiters=('=', ':'), comment_prefixes=('#', ';'), inline_comment_prefixes=None, strict=True, empty_lines_in_values=True, default_section=默认小节, interpolation=_UNSET, converters=_UNSET, allow_unnamed_section=False):
        self._dict = dict_type
        self._sections = self._dict()
        self._defaults = self._dict()
        self._converters = 转换器映射(self)
        self._proxies = self._dict()
        self._proxies[default_section] = 小节代理(self, default_section)
        self._delimiters = tuple(delimiters)
        if delimiters == ('=', ':'):
            self._optcre = self.OPTCRE_NV if allow_no_value else self.OPTCRE
        else:
            d = '|'.join((re.escape(d) for d in delimiters))
            if allow_no_value:
                self._optcre = re.compile(self._OPT_NV_TMPL.format(delim=d), re.VERBOSE)
            else:
                self._optcre = re.compile(self._OPT_TMPL.format(delim=d), re.VERBOSE)
        self._comments = _CommentSpec(comment_prefixes or (), inline_comment_prefixes or ())
        self._strict = strict
        self._allow_no_value = allow_no_value
        self._empty_lines_in_values = empty_lines_in_values
        self.default_section = default_section
        self._interpolation = interpolation
        if self._interpolation is _UNSET:
            self._interpolation = self._DEFAULT_INTERPOLATION
        if self._interpolation is None:
            self._interpolation = 插值()
        if not isinstance(self._interpolation, 插值):
            raise TypeError(f'interpolation= must be None or an instance of Interpolation; got an object of type {type(self._interpolation)}')
        if converters is not _UNSET:
            self._converters.update(converters)
        if defaults:
            self._read_defaults(defaults)
        self._allow_unnamed_section = allow_unnamed_section

    def 默认值们(self):
        return self._defaults

    def 小节们(self):
        """Return a list of section names, excluding [DEFAULT]"""
        return list(self._sections.keys())

    def 加小节(self, section):
        """Create a new section in the configuration.

        Raise DuplicateSectionError if a section by the specified name
        already exists. Raise ValueError if name is DEFAULT.
        """
        if section == self.default_section:
            raise ValueError('Invalid section name: %r' % section)
        if section is 未命名小节:
            if not self._allow_unnamed_section:
                raise 未命名小节禁用错误
        if section in self._sections:
            raise 重复小节错误(section)
        self._sections[section] = self._dict()
        self._proxies[section] = 小节代理(self, section)

    def 有小节吗(self, section):
        """Indicate whether the named section is present in the configuration.

        The DEFAULT section is not acknowledged.
        """
        return section in self._sections

    def 选项们(self, section):
        """Return a list of option names for the given section name."""
        try:
            opts = self._sections[section].copy()
        except KeyError:
            raise 无小节错误(section) from None
        opts.update(self._defaults)
        return list(opts.keys())

    def 读取(self, filenames, encoding=None):
        """Read and parse a filename or an iterable of filenames.

        Files that cannot be opened are silently ignored; this is
        designed so that you can specify an iterable of potential
        configuration file locations (e.g. current directory, user's
        home directory, systemwide directory), and all existing
        configuration files in the iterable will be read.  A single
        filename may also be given.

        Return list of successfully read files.
        """
        if isinstance(filenames, (str, bytes, os.PathLike)):
            filenames = [filenames]
        encoding = io.text_encoding(encoding)
        read_ok = []
        for filename in filenames:
            try:
                with open(filename, encoding=encoding) as fp:
                    self._read(fp, filename)
            except OSError:
                continue
            if isinstance(filename, os.PathLike):
                filename = os.fspath(filename)
            read_ok.append(filename)
        return read_ok

    def 读文件(self, f, source=None):
        """Like read() but the argument must be a file-like object.

        The `f` argument must be iterable, returning one line at a time.
        Optional second argument is the `source` specifying the name of the
        file being read. If not given, it is taken from f.name. If `f` has no
        `name` attribute, `<???>` is used.
        """
        if source is None:
            try:
                source = f.name
            except AttributeError:
                source = '<???>'
        self._read(f, source)

    def 读字符串(self, string, source='<string>'):
        """Read configuration from a given string."""
        sfile = io.StringIO(string)
        self.读文件(sfile, source)

    def 读字典(self, dictionary, source='<dict>'):
        """Read configuration from a dictionary.

        Keys are section names, values are dictionaries with keys and values
        that should be present in the section. If the used dictionary type
        preserves order, sections and their keys will be added in order.

        All types held in the dictionary are converted to strings during
        reading, including section names, option names and keys.

        Optional second argument is the `source` specifying the name of the
        dictionary being read.
        """
        elements_added = set()
        for section, keys in dictionary.items():
            if section is not 未命名小节:
                section = str(section)
            try:
                self.加小节(section)
            except (重复小节错误, ValueError):
                if self._strict and section in elements_added:
                    raise
            elements_added.add(section)
            for key, value in keys.items():
                key = self.optionxform(str(key))
                if value is not None:
                    value = str(value)
                if self._strict and (section, key) in elements_added:
                    raise 重复选项错误(section, key, source)
                elements_added.add((section, key))
                self.set(section, key, value)

    def 取值(self, section, option, *, raw=False, vars=None, fallback=_UNSET):
        """Get an option value for a given section.

        If `vars` is provided, it must be a dictionary. The option is looked up
        in `vars` (if provided), `section`, and in `DEFAULTSECT` in that order.
        If the key is not found and `fallback` is provided, it is used as
        a fallback value. `None` can be provided as a `fallback` value.

        If interpolation is enabled and the optional argument `raw` is False,
        all interpolations are expanded in the return values.

        Arguments `raw`, `vars`, and `fallback` are keyword only.

        The section DEFAULT is special.
        """
        try:
            d = self._unify_values(section, vars)
        except 无小节错误:
            if fallback is _UNSET:
                raise
            else:
                return fallback
        option = self.optionxform(option)
        try:
            value = d[option]
        except KeyError:
            if fallback is _UNSET:
                raise 无选项错误(option, section)
            else:
                return fallback
        if raw or value is None:
            return value
        else:
            return self._interpolation.before_get(self, section, option, value, d)

    def _get(self, section, conv, option, **kwargs):
        return conv(self.get(section, option, **kwargs))

    def _get_conv(self, section, option, conv, *, raw=False, vars=None, fallback=_UNSET, **kwargs):
        try:
            return self._get(section, conv, option, raw=raw, vars=vars, **kwargs)
        except (无小节错误, 无选项错误):
            if fallback is _UNSET:
                raise
            return fallback

    def 取整数(self, section, option, *, raw=False, vars=None, fallback=_UNSET, **kwargs):
        return self._get_conv(section, option, int, raw=raw, vars=vars, fallback=fallback, **kwargs)

    def 取浮点(self, section, option, *, raw=False, vars=None, fallback=_UNSET, **kwargs):
        return self._get_conv(section, option, float, raw=raw, vars=vars, fallback=fallback, **kwargs)

    def 取布尔(self, section, option, *, raw=False, vars=None, fallback=_UNSET, **kwargs):
        return self._get_conv(section, option, self._convert_to_boolean, raw=raw, vars=vars, fallback=fallback, **kwargs)

    def 项们(self, section=_UNSET, raw=False, vars=None):
        """Return a list of (name, value) tuples for each option in a section.

        All % interpolations are expanded in the return values, based on the
        defaults passed into the constructor, unless the optional argument
        `raw` is true.  Additional substitutions may be provided using the
        `vars` argument, which must be a dictionary whose contents overrides
        any pre-existing defaults.

        The section DEFAULT is special.
        """
        if section is _UNSET:
            return super().items()
        d = self._defaults.copy()
        try:
            d.update(self._sections[section])
        except KeyError:
            if section != self.default_section:
                raise 无小节错误(section)
        orig_keys = list(d.keys())
        if vars:
            for key, value in vars.items():
                d[self.optionxform(key)] = value
        value_getter = lambda option: self._interpolation.before_get(self, section, option, d[option], d)
        if raw:
            value_getter = lambda option: d[option]
        return [(option, value_getter(option)) for option in orig_keys]

    def popitem(self):
        """Remove a section from the parser and return it as
        a (section_name, section_proxy) tuple. If no section is present, raise
        KeyError.

        The section DEFAULT is never returned because it cannot be removed.
        """
        for key in self.小节们():
            value = self[key]
            del self[key]
            return (key, value)
        raise KeyError

    def optionxform(self, optionstr):
        return optionstr.lower()

    def 有选项吗(self, section, option):
        """Check for the existence of a given option in a given section.
        If the specified `section` is None or an empty string, DEFAULT is
        assumed. If the specified `section` does not exist, returns False."""
        if not section or section == self.default_section:
            option = self.optionxform(option)
            return option in self._defaults
        elif section not in self._sections:
            return False
        else:
            option = self.optionxform(option)
            return option in self._sections[section] or option in self._defaults

    def set(self, section, option, value=None):
        """Set an option."""
        if value:
            value = self._interpolation.before_set(self, section, option, value)
        if not section or section == self.default_section:
            sectdict = self._defaults
        else:
            try:
                sectdict = self._sections[section]
            except KeyError:
                raise 无小节错误(section) from None
        sectdict[self.optionxform(option)] = value

    def 写出(self, fp, space_around_delimiters=True):
        """Write an .ini-format representation of the configuration state.

        If `space_around_delimiters` is True (the default), delimiters
        between keys and values are surrounded by spaces.

        Please note that comments in the original configuration file are not
        preserved when writing the configuration back.
        """
        if space_around_delimiters:
            d = ' {} '.format(self._delimiters[0])
        else:
            d = self._delimiters[0]
        if self._defaults:
            self._write_section(fp, self.default_section, self._defaults.items(), d)
        if 未命名小节 in self._sections and self._sections[未命名小节]:
            self._write_section(fp, 未命名小节, self._sections[未命名小节].items(), d, unnamed=True)
        for section in self._sections:
            if section is 未命名小节:
                continue
            self._write_section(fp, section, self._sections[section].items(), d)

    def _write_section(self, fp, section_name, section_items, delimiter, unnamed=False):
        """Write a single section to the specified 'fp'."""
        if not unnamed:
            fp.write('[{}]\n'.format(section_name))
        for key, value in section_items:
            self._validate_key_contents(key)
            value = self._interpolation.before_write(self, section_name, key, value)
            if value is not None or not self._allow_no_value:
                value = delimiter + str(value).replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\n\t')
            else:
                value = ''
            fp.write('{}{}\n'.format(key, value))
        fp.write('\n')

    def 删选项(self, section, option):
        """Remove an option."""
        if not section or section == self.default_section:
            sectdict = self._defaults
        else:
            try:
                sectdict = self._sections[section]
            except KeyError:
                raise 无小节错误(section) from None
        option = self.optionxform(option)
        existed = option in sectdict
        if existed:
            del sectdict[option]
        return existed

    def 删小节(self, section):
        """Remove a file section."""
        existed = section in self._sections
        if existed:
            del self._sections[section]
            del self._proxies[section]
        return existed

    def __getitem__(self, key):
        if key != self.default_section and (not self.有小节吗(key)):
            raise KeyError(key)
        return self._proxies[key]

    def __setitem__(self, key, value):
        if key in self and self[key] is value:
            return
        if key == self.default_section:
            self._defaults.clear()
        elif key in self._sections:
            self._sections[key].clear()
        self.读字典({key: value})

    def __delitem__(self, key):
        if key == self.default_section:
            raise ValueError('Cannot remove the default section.')
        if not self.有小节吗(key):
            raise KeyError(key)
        self.删小节(key)

    def __contains__(self, key):
        return key == self.default_section or self.有小节吗(key)

    def __len__(self):
        return len(self._sections) + 1

    def __iter__(self):
        return itertools.chain((self.default_section,), self._sections.keys())

    def _read(self, fp, fpname):
        """Parse a sectioned configuration file.

        Each section in a configuration file contains a header, indicated by
        a name in square brackets (`[]`), plus key/value options, indicated by
        `name` and `value` delimited with a specific substring (`=` or `:` by
        default).

        Values can span multiple lines, as long as they are indented deeper
        than the first line of the value. Depending on the parser's mode, blank
        lines may be treated as parts of multiline values or ignored.

        Configuration files may include comments, prefixed by specific
        characters (`#` and `;` by default). Comments may appear on their own
        in an otherwise empty line or may be entered in lines holding values or
        section names. Please note that comments get stripped off when reading configuration files.
        """
        try:
            解析错误._raise_all(self._read_inner(fp, fpname))
        finally:
            self._join_multiline_values()

    def _read_inner(self, fp, fpname):
        st = _ReadState()
        for st.lineno, line in enumerate(map(self._comments.wrap, fp), start=1):
            if not line.clean:
                if self._empty_lines_in_values:
                    if not line.has_comments and st.cursect is not None and st.optname and (st.cursect[st.optname] is not None):
                        st.cursect[st.optname].append('')
                else:
                    st.indent_level = sys.maxsize
                continue
            first_nonspace = self.NONSPACECRE.search(line)
            st.cur_indent_level = first_nonspace.start() if first_nonspace else 0
            if self._handle_continuation_line(st, line, fpname):
                continue
            self._handle_rest(st, line, fpname)
        return st.errors

    def _handle_continuation_line(self, st, line, fpname):
        is_continue = st.cursect is not None and st.optname and (st.cur_indent_level > st.indent_level)
        if is_continue:
            if st.cursect[st.optname] is None:
                raise 多行续行错误(fpname, st.lineno, line)
            st.cursect[st.optname].append(line.clean)
        return is_continue

    def _handle_rest(self, st, line, fpname):
        if self._allow_unnamed_section and st.cursect is None:
            self._handle_header(st, 未命名小节, fpname)
        st.indent_level = st.cur_indent_level
        mo = self.SECTCRE.match(line.clean)
        if not mo and st.cursect is None:
            raise 缺小节头错误(fpname, st.lineno, line)
        self._handle_header(st, mo.group('header'), fpname) if mo else self._handle_option(st, line, fpname)

    def _handle_header(self, st, sectname, fpname):
        st.sectname = sectname
        if st.sectname in self._sections:
            if self._strict and st.sectname in st.elements_added:
                raise 重复小节错误(st.sectname, fpname, st.lineno)
            st.cursect = self._sections[st.sectname]
            st.elements_added.add(st.sectname)
        elif st.sectname == self.default_section:
            st.cursect = self._defaults
        else:
            st.cursect = self._dict()
            self._sections[st.sectname] = st.cursect
            self._proxies[st.sectname] = 小节代理(self, st.sectname)
            st.elements_added.add(st.sectname)
        st.optname = None

    def _handle_option(self, st, line, fpname):
        st.indent_level = st.cur_indent_level
        mo = self._optcre.match(line.clean)
        if not mo:
            st.errors.append(解析错误(fpname, st.lineno, line))
            return
        st.optname, vi, optval = mo.group('option', 'vi', 'value')
        if not st.optname:
            st.errors.append(解析错误(fpname, st.lineno, line))
        st.optname = self.optionxform(st.optname.rstrip())
        if self._strict and (st.sectname, st.optname) in st.elements_added:
            raise 重复选项错误(st.sectname, st.optname, fpname, st.lineno)
        st.elements_added.add((st.sectname, st.optname))
        if optval is not None:
            optval = optval.strip()
            st.cursect[st.optname] = [optval]
        else:
            st.cursect[st.optname] = None

    def _join_multiline_values(self):
        默认值们 = (self.default_section, self._defaults)
        all_sections = itertools.chain((默认值们,), self._sections.items())
        for section, 选项们 in all_sections:
            for name, val in 选项们.items():
                if isinstance(val, list):
                    val = '\n'.join(val).rstrip()
                选项们[name] = self._interpolation.before_read(self, section, name, val)

    def _read_defaults(self, defaults):
        """Read the defaults passed in the initializer.
        Note: values can be non-string."""
        for key, value in defaults.items():
            self._defaults[self.optionxform(key)] = value

    def _unify_values(self, section, vars):
        """Create a sequence of lookups with 'vars' taking priority over
        the 'section' which takes priority over the DEFAULTSECT.

        """
        sectiondict = {}
        try:
            sectiondict = self._sections[section]
        except KeyError:
            if section != self.default_section:
                raise 无小节错误(section) from None
        vardict = {}
        if vars:
            for key, value in vars.items():
                if value is not None:
                    value = str(value)
                vardict[self.optionxform(key)] = value
        return _ChainMap(vardict, sectiondict, self._defaults)

    def _convert_to_boolean(self, value):
        """Return a boolean value translating from other types if necessary.
        """
        if value.lower() not in self.BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % value)
        return self.BOOLEAN_STATES[value.lower()]

    def _validate_key_contents(self, key):
        """Raises an InvalidWriteError for any keys containing
        delimiters or that begins with the section header pattern"""
        if re.match(self.SECTCRE, key):
            raise 无效写入错误(f'Cannot write key {key}; begins with section pattern')
        for delim in self._delimiters:
            if delim in key:
                raise 无效写入错误(f'Cannot write key {key}; contains delimiter {delim}')

    def _validate_value_types(self, *, section='', option='', value=''):
        """Raises a TypeError for illegal non-string values.

        Legal non-string values are UNNAMED_SECTION and falsey values if
        they are allowed.

        For compatibility reasons this method is not used in classic set()
        for RawConfigParsers. It is invoked in every case for mapping protocol
        access and in ConfigParser.set().
        """
        if section is 未命名小节:
            if not self._allow_unnamed_section:
                raise 未命名小节禁用错误
        elif not isinstance(section, str):
            raise TypeError('section names must be strings or UNNAMED_SECTION')
        if not isinstance(option, str):
            raise TypeError('option keys must be strings')
        if not self._allow_no_value or value:
            if not isinstance(value, str):
                raise TypeError('option values must be strings')

    @property
    def converters(self):
        return self._converters
_装类转发(原始配置解析器, {'add_section': '加小节', 'defaults': '默认值们', 'get': '取值', 'getboolean': '取布尔', 'getfloat': '取浮点', 'getint': '取整数', 'has_option': '有选项吗', 'has_section': '有小节吗', 'items': '项们', 'options': '选项们', 'read': '读取', 'read_dict': '读字典', 'read_file': '读文件', 'read_string': '读字符串', 'remove_option': '删选项', 'remove_section': '删小节', 'sections': '小节们', 'write': '写出'}, {'add_section': '加小节', 'defaults': '默认值们', 'get': '取值', 'getboolean': '取布尔', 'getfloat': '取浮点', 'getint': '取整数', 'has_option': '有选项吗', 'has_section': '有小节吗', 'items': '项们', 'options': '选项们', 'read': '读取', 'read_dict': '读字典', 'read_file': '读文件', 'read_string': '读字符串', 'remove_option': '删选项', 'remove_section': '删小节', 'sections': '小节们', 'write': '写出'})

class 配置解析器(原始配置解析器):
    """ConfigParser implementing interpolation."""
    _DEFAULT_INTERPOLATION = 基本插值()

    def set(self, section, option, value=None):
        """Set an option.  Extends RawConfigParser.set by validating type and
        interpolation syntax on the value."""
        self._validate_value_types(option=option, value=value)
        super().set(section, option, value)

    def 加小节(self, section):
        """Create a new section in the configuration.  Extends
        RawConfigParser.add_section by validating if the section name is
        a string."""
        self._validate_value_types(section=section)
        super().add_section(section)

    def _read_defaults(self, defaults):
        """Reads the defaults passed in the initializer, implicitly converting
        values to strings like the rest of the API.

        Does not perform interpolation for backwards compatibility.
        """
        try:
            hold_interpolation = self._interpolation
            self._interpolation = 插值()
            self.读字典({self.default_section: defaults})
        finally:
            self._interpolation = hold_interpolation
_装类转发(配置解析器, {'add_section': '加小节'}, {'add_section': '加小节', 'read_dict': '读字典'})

class 小节代理(MutableMapping):
    """A proxy for a single section from a parser."""

    def __init__(self, parser, name):
        """Creates a view on a section of the specified `name` in `parser`."""
        self._parser = parser
        self._name = name
        for conv in parser.converters:
            key = 'get' + conv
            getter = functools.partial(self.get, _impl=getattr(parser, key))
            setattr(self, key, getter)

    def __repr__(self):
        return '<Section: {}>'.format(self._name)

    def __getitem__(self, key):
        if not self._parser.has_option(self._name, key):
            raise KeyError(key)
        return self._parser.get(self._name, key)

    def __setitem__(self, key, value):
        self._parser._validate_value_types(option=key, value=value)
        return self._parser.set(self._name, key, value)

    def __delitem__(self, key):
        if not (self._parser.has_option(self._name, key) and self._parser.remove_option(self._name, key)):
            raise KeyError(key)

    def __contains__(self, key):
        return self._parser.has_option(self._name, key)

    def __len__(self):
        return len(self._options())

    def __iter__(self):
        return self._options().__iter__()

    def _options(self):
        if self._name != self._parser.default_section:
            return self._parser.options(self._name)
        else:
            return self._parser.defaults()

    @property
    def parser(self):
        return self._parser

    @property
    def name(self):
        return self._name

    def 取值(self, option, fallback=None, *, raw=False, vars=None, _impl=None, **kwargs):
        """Get an option value.

        Unless `fallback` is provided, `None` will be returned if the option
        is not found.

        """
        if not _impl:
            _impl = self._parser.get
        return _impl(self._name, option, raw=raw, vars=vars, fallback=fallback, **kwargs)
_装类转发(小节代理, {'get': '取值'}, {'get': '取值'})

class 转换器映射(MutableMapping):
    """Enables reuse of get*() methods between the parser and section proxies.

    If a parser class implements a getter directly, the value for the given
    key will be ``None``. The presence of the converter name here enables
    section proxies to find and use the implementation on the parser class.
    """
    GETTERCRE = re.compile('^get(?P<name>.+)$')

    def __init__(self, parser):
        self._parser = parser
        self._data = {}
        for getter in dir(self._parser):
            m = self.GETTERCRE.match(getter)
            if not m or not callable(getattr(self._parser, getter)):
                continue
            self._data[m.group('name')] = None

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        try:
            k = 'get' + key
        except TypeError:
            raise ValueError('Incompatible key: {} (type: {})'.format(key, type(key)))
        if k == 'get':
            raise ValueError('Incompatible key: cannot use "" as a name')
        self._data[key] = value
        func = functools.partial(self._parser._get_conv, conv=value)
        func.converter = value
        setattr(self._parser, k, func)
        for proxy in self._parser.values():
            getter = functools.partial(proxy.get, _impl=func)
            setattr(proxy, k, getter)

    def __delitem__(self, key):
        try:
            k = 'get' + (key or None)
        except TypeError:
            raise KeyError(key)
        del self._data[key]
        for inst in itertools.chain((self._parser,), self._parser.values()):
            try:
                delattr(inst, k)
            except AttributeError:
                continue

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BasicInterpolation': '基本插值',
    'ConfigParser': '配置解析器',
    'ConverterMapping': '转换器映射',
    'DEFAULTSECT': '默认小节',
    'DuplicateOptionError': '重复选项错误',
    'DuplicateSectionError': '重复小节错误',
    'Error': '错误',
    'ExtendedInterpolation': '扩展插值',
    'Interpolation': '插值',
    'InterpolationDepthError': '插值深度错误',
    'InterpolationError': '插值错误',
    'InterpolationMissingOptionError': '插值缺选项错误',
    'InterpolationSyntaxError': '插值语法错误',
    'InvalidWriteError': '无效写入错误',
    'MAX_INTERPOLATION_DEPTH': '最大插值深度',
    'MissingSectionHeaderError': '缺小节头错误',
    'MultilineContinuationError': '多行续行错误',
    'NoOptionError': '无选项错误',
    'NoSectionError': '无小节错误',
    'ParsingError': '解析错误',
    'RawConfigParser': '原始配置解析器',
    'SectionProxy': '小节代理',
    'UNNAMED_SECTION': '未命名小节',
    'UnnamedSectionDisabledError': '未命名小节禁用错误',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '原始配置解析器': {
        'add_section': '加小节',
        'defaults': '默认值们',
        'get': '取值',
        'getboolean': '取布尔',
        'getfloat': '取浮点',
        'getint': '取整数',
        'has_option': '有选项吗',
        'has_section': '有小节吗',
        'items': '项们',
        'options': '选项们',
        'read': '读取',
        'read_dict': '读字典',
        'read_file': '读文件',
        'read_string': '读字符串',
        'remove_option': '删选项',
        'remove_section': '删小节',
        'sections': '小节们',
        'write': '写出',
    },
    '基本插值': {
        'before_get': '取值之前',
        'before_set': '设置之前',
    },
    '小节代理': {
        'get': '取值',
    },
    '扩展插值': {
        'before_get': '取值之前',
        'before_set': '设置之前',
    },
    '插值': {
        'before_get': '取值之前',
        'before_read': '读之前',
        'before_set': '设置之前',
    },
    '配置解析器': {
        'add_section': '加小节',
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
    '原始配置解析器': {
        'add_section': '加小节',
        'defaults': '默认值们',
        'get': '取值',
        'getboolean': '取布尔',
        'getfloat': '取浮点',
        'getint': '取整数',
        'has_option': '有选项吗',
        'has_section': '有小节吗',
        'items': '项们',
        'options': '选项们',
        'read': '读取',
        'read_dict': '读字典',
        'read_file': '读文件',
        'read_string': '读字符串',
        'remove_option': '删选项',
        'remove_section': '删小节',
        'sections': '小节们',
        'write': '写出',
    },
    '基本插值': {
        'before_get': '取值之前',
        'before_set': '设置之前',
    },
    '小节代理': {
        'get': '取值',
    },
    '扩展插值': {
        'before_get': '取值之前',
        'before_set': '设置之前',
    },
    '插值': {
        'before_get': '取值之前',
        'before_read': '读之前',
        'before_set': '设置之前',
    },
    '配置解析器': {
        'add_section': '加小节',
        'read_dict': '读字典',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '原始配置解析器',
    '基本插值',
    '多行续行错误',
    '小节代理',
    '扩展插值',
    '插值',
    '插值深度错误',
    '插值缺选项错误',
    '插值语法错误',
    '插值错误',
    '无小节错误',
    '无效写入错误',
    '无选项错误',
    '最大插值深度',
    '未命名小节',
    '未命名小节禁用错误',
    '缺小节头错误',
    '解析错误',
    '转换器映射',
    '配置解析器',
    '重复小节错误',
    '重复选项错误',
    '默认小节',
]

# ---- 转发层结束 ----
