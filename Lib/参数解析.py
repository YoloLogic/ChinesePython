# -*- coding: utf-8 -*-
"""参数解析 —— 汉语库（由 tools/汉化库.py 从 Lib/argparse.py 机械生成，**不要手改**）。

英文库 Lib/argparse.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 参数解析
"""


"""Command-line parsing library

This module is an optparse-inspired command-line parsing library that:

    - handles both optional and positional arguments
    - produces highly informative usage messages
    - supports parsers that dispatch to sub-parsers

The following is a simple usage example that sums integers from the
command-line and writes the result to a file::

    parser = argparse.ArgumentParser(
        description='sum the integers at the command line')
    parser.add_argument(
        'integers', metavar='int', nargs='+', type=int,
        help='an integer to be summed')
    parser.add_argument(
        '--log',
        help='the file where the sum should be written')
    args = parser.parse_args()
    with (open(args.log, 'w') if args.log is not None
          else contextlib.nullcontext(sys.stdout)) as log:
        log.write('%s' % sum(args.integers))

The module contains the following public classes:

    - ArgumentParser -- The main entry point for command-line parsing. As the
        example above shows, the add_argument() method is used to populate
        the parser with actions for optional and positional arguments. Then
        the parse_args() method is invoked to convert the args at the
        command-line into an object with attributes.

    - ArgumentError -- The exception raised by ArgumentParser objects when
        there are errors with the parser's actions. Errors raised while
        parsing the command-line are caught by ArgumentParser and emitted
        as command-line messages.

    - FileType -- A factory for defining types of files to be created. As the
        example above shows, instances of FileType are typically passed as
        the type= argument of add_argument() calls. Deprecated since
        Python 3.14.

    - Action -- The base class for parser actions. Typically actions are
        selected by passing strings like 'store_true' or 'append_const' to
        the action= argument of add_argument(). However, for greater
        customization of ArgumentParser actions, subclasses of Action may
        be defined and passed as the action= argument.

    - HelpFormatter, RawDescriptionHelpFormatter, RawTextHelpFormatter,
        ArgumentDefaultsHelpFormatter -- Formatter classes which
        may be passed as the formatter_class= argument to the
        ArgumentParser constructor. HelpFormatter is the default,
        RawDescriptionHelpFormatter and RawTextHelpFormatter tell the parser
        not to change the formatting for help text, and
        ArgumentDefaultsHelpFormatter adds information about argument defaults
        to the help.

All other classes in this module are considered implementation details.
(Also note that HelpFormatter and RawDescriptionHelpFormatter are only
considered public as object names -- the API of the formatter objects is
still considered an implementation detail.)
"""
_英文原名表 = {'Action': '动作', 'ArgumentDefaultsHelpFormatter': '含默认值帮助排版器', 'ArgumentError': '参数错误', 'ArgumentParser': '参数解析器', 'ArgumentTypeError': '参数类型错误', 'BooleanOptionalAction': '布尔可选动作', 'FileType': '文件类型', 'HelpFormatter': '帮助排版器', 'MetavarTypeHelpFormatter': '元变量类型帮助排版器', 'Namespace': '命名空间', 'ONE_OR_MORE': '一个或更多', 'OPTIONAL': '可选', 'PARSER': '作为解析器', 'REMAINDER': '剩余全部', 'RawDescriptionHelpFormatter': '原始描述帮助排版器', 'RawTextHelpFormatter': '原始文本帮助排版器', 'SUPPRESS': '隐藏', 'ZERO_OR_MORE': '零或更多'}

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
__version__ = '1.1'
__all__ = ['ArgumentParser', 'ArgumentError', 'ArgumentTypeError', 'BooleanOptionalAction', 'FileType', 'HelpFormatter', 'ArgumentDefaultsHelpFormatter', 'RawDescriptionHelpFormatter', 'RawTextHelpFormatter', 'MetavarTypeHelpFormatter', 'Namespace', 'Action', 'ONE_OR_MORE', 'OPTIONAL', 'PARSER', 'REMAINDER', 'SUPPRESS', 'ZERO_OR_MORE']
import os as _os
import re as _re
import sys as _sys
from gettext import gettext as _, ngettext
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

def _zh可用():
    _m = _zh()
    if _m is None:
        return False
    try:
        return _m.取模式() != 'en'
    except Exception:
        return False

def _zh正文(文):
    """英文正文 → 中文正文。没表、en 模式、出任何岔子，都原样返回。"""
    _m = _zh()
    if _m is None:
        return 文
    try:
        return _m.翻正文(文)
    except Exception:
        return 文
隐藏 = '==SUPPRESS=='
可选 = '?'
零或更多 = '*'
一个或更多 = '+'
作为解析器 = 'A...'
剩余全部 = '...'
_UNRECOGNIZED_ARGS_ATTR = '_unrecognized_args'

class _AttributeHolder(object):
    """Abstract base class that provides __repr__.

    The __repr__ method returns a string in the format::
        ClassName(attr=name, attr=name, ...)
    The attributes are determined either by a class-level attribute,
    '_kwarg_names', or by inspecting the instance __dict__.
    """

    def __repr__(self):
        type_name = type(self).__name__
        arg_strings = []
        star_args = {}
        for arg in self._get_args():
            arg_strings.append(repr(arg))
        for name, value in self._get_kwargs():
            if name.isidentifier():
                arg_strings.append('%s=%r' % (name, value))
            else:
                star_args[name] = value
        if star_args:
            arg_strings.append('**%s' % repr(star_args))
        return '%s(%s)' % (type_name, ', '.join(arg_strings))

    def _get_kwargs(self):
        return list(self.__dict__.items())

    def _get_args(self):
        return []

def _copy_items(items):
    if items is None:
        return []
    if type(items) is list:
        return items[:]
    import copy
    return copy.copy(items)

def _identity(value):
    return value

class 帮助排版器(object):
    """Formatter for generating usage messages and argument help strings.

    Only the name of this class is considered a public API. All the methods
    provided by the class are considered an implementation detail.
    """

    def __init__(self, prog, indent_increment=2, max_help_position=24, width=None, color=True):
        if width is None:
            import shutil
            width = shutil.get_terminal_size().columns
            width -= 2
        self._set_color(color)
        self._prog = prog
        self._indent_increment = indent_increment
        self._max_help_position = min(max_help_position, max(width - 20, indent_increment * 2))
        self._width = width
        self._current_indent = 0
        self._level = 0
        self._action_max_length = 0
        self._root_section = self._Section(self, None)
        self._current_section = self._root_section
        self._whitespace_matcher = _re.compile('\\s+', _re.ASCII)
        self._long_break_matcher = _re.compile('\\n\\n\\n+')

    def _set_color(self, color):
        from _colorize import can_colorize, decolor, get_theme
        if color and can_colorize():
            self._theme = get_theme(force_color=True).argparse
            self._decolor = decolor
        else:
            self._theme = get_theme(force_no_color=True).argparse
            self._decolor = _identity

    def _indent(self):
        self._current_indent += self._indent_increment
        self._level += 1

    def _dedent(self):
        self._current_indent -= self._indent_increment
        assert self._current_indent >= 0, 'Indent decreased below 0.'
        self._level -= 1

    class _Section(object):

        def __init__(self, formatter, parent, heading=None):
            self.formatter = formatter
            self.parent = parent
            self.heading = heading
            self.items = []

        def format_help(self):
            if self.parent is not None:
                self.formatter._indent()
            join = self.formatter._join_parts
            item_help = join([func(*args) for func, args in self.items])
            if self.parent is not None:
                self.formatter._dedent()
            if not item_help:
                return ''
            if self.heading is not 隐藏 and self.heading is not None:
                current_indent = self.formatter._current_indent
                heading_text = _('%(heading)s:') % dict(heading=self.heading)
                t = self.formatter._theme
                heading = f"{' ' * current_indent}{t.heading}{heading_text}{t.reset}\n"
            else:
                heading = ''
            return join(['\n', heading, item_help, '\n'])

    def _add_item(self, func, args):
        self._current_section.items.append((func, args))

    def start_section(self, heading):
        self._indent()
        section = self._Section(self, self._current_section, heading)
        self._add_item(section.format_help, [])
        self._current_section = section

    def end_section(self):
        self._current_section = self._current_section.parent
        self._dedent()

    def add_text(self, text):
        if text is not 隐藏 and text is not None:
            self._add_item(self._format_text, [text])

    def 加用法(self, usage, actions, groups, prefix=None):
        if usage is not 隐藏:
            args = (usage, actions, groups, prefix)
            self._add_item(self._format_usage, args)

    def 加参数(self, action):
        if action.help is not 隐藏:
            get_invocation = lambda x: self._decolor(self._format_action_invocation(x))
            invocation_lengths = [len(get_invocation(action)) + self._current_indent]
            for subaction in self._iter_indented_subactions(action):
                invocation_lengths.append(len(get_invocation(subaction)) + self._current_indent)
            action_length = max(invocation_lengths)
            self._action_max_length = max(self._action_max_length, action_length)
            self._add_item(self._format_action, [action])

    def add_arguments(self, actions):
        for action in actions:
            self.加参数(action)

    def format_help(self):
        help = self._root_section.format_help()
        if help:
            help = self._long_break_matcher.sub('\n\n', help)
            help = help.strip('\n') + '\n'
        return help

    def _join_parts(self, part_strings):
        return ''.join([part for part in part_strings if part and part is not 隐藏])

    def _format_usage(self, usage, actions, groups, prefix):
        t = self._theme
        if prefix is None:
            prefix = _('usage: ')
        if usage is not None:
            usage = t.prog_extra + usage % {'prog': f'{t.prog}{self._prog}{t.reset}{t.prog_extra}'} + t.reset
        elif usage is None and (not actions):
            usage = f'{t.prog}{self._prog}{t.reset}'
        elif usage is None:
            prog = '%(prog)s' % dict(prog=self._prog)
            parts, pos_start = self._get_actions_usage_parts(actions, groups)
            usage = ' '.join(filter(None, [prog, *parts]))
            text_width = self._width - self._current_indent
            if len(prefix) + len(self._decolor(usage)) > text_width:
                opt_parts = parts[:pos_start]
                pos_parts = parts[pos_start:]

                def get_lines(parts, indent, prefix=None):
                    lines = []
                    line = []
                    indent_length = len(indent)
                    if prefix is not None:
                        line_len = len(prefix) - 1
                    else:
                        line_len = indent_length - 1
                    for part in parts:
                        part_len = len(self._decolor(part))
                        if line_len + 1 + part_len > text_width and line:
                            lines.append(indent + ' '.join(line))
                            line = []
                            line_len = indent_length - 1
                        line.append(part)
                        line_len += part_len + 1
                    if line:
                        lines.append(indent + ' '.join(line))
                    if prefix is not None:
                        lines[0] = lines[0][indent_length:]
                    return lines
                prog_len = len(self._decolor(prog))
                if len(prefix) + prog_len <= 0.75 * text_width:
                    indent = ' ' * (len(prefix) + prog_len + 1)
                    if opt_parts:
                        lines = get_lines([prog] + opt_parts, indent, prefix)
                        lines.extend(get_lines(pos_parts, indent))
                    elif pos_parts:
                        lines = get_lines([prog] + pos_parts, indent, prefix)
                    else:
                        lines = [prog]
                else:
                    indent = ' ' * len(prefix)
                    parts = opt_parts + pos_parts
                    lines = get_lines(parts, indent)
                    if len(lines) > 1:
                        lines = []
                        lines.extend(get_lines(opt_parts, indent))
                        lines.extend(get_lines(pos_parts, indent))
                    lines = [prog] + lines
                usage = '\n'.join(lines)
            usage = usage.removeprefix(prog)
            usage = f'{t.prog}{prog}{t.reset}{usage}'
        return f'{t.usage}{prefix}{t.reset}{usage}\n\n'

    def _is_long_option(self, string):
        return len(string) > 2

    def _get_actions_usage_parts(self, actions, groups):
        """Get usage parts with split index for optionals/positionals.

        Returns (parts, pos_start) where pos_start is the index in parts
        where positionals begin.
        This preserves mutually exclusive group formatting across the
        optionals/positionals boundary (gh-75949).
        """
        actions = [action for action in actions if action.help is not 隐藏]
        action_groups = dict.fromkeys(actions)
        for group in groups:
            for action in group._group_actions:
                if action in action_groups:
                    action_groups[action] = group
        positionals = []
        for action in actions:
            if not action.option_strings:
                group = action_groups.pop(action)
                if group:
                    group_actions = [action2 for action2 in group._group_actions if action2.option_strings and action_groups.pop(action2, None)] + [action]
                    positionals.append((group.required, group_actions))
                else:
                    positionals.append((None, [action]))
        optionals = []
        for action in actions:
            if action.option_strings and action in action_groups:
                group = action_groups.pop(action)
                if group:
                    group_actions = [action] + [action2 for action2 in group._group_actions if action2.option_strings and action_groups.pop(action2, None)]
                    optionals.append((group.required, group_actions))
                else:
                    optionals.append((None, [action]))
        parts = []
        t = self._theme
        pos_start = None
        for i, (required, group) in enumerate(optionals + positionals):
            start = len(parts)
            if i == len(optionals):
                pos_start = start
            in_group = len(group) > 1
            for action in group:
                if not action.option_strings:
                    default = self._get_default_metavar_for_positional(action)
                    part = self._format_args(action, default)
                    if in_group:
                        if part[0] == '[' and part[-1] == ']':
                            part = part[1:-1]
                    part = t.summary_action + part + t.reset
                else:
                    option_string = action.option_strings[0]
                    if self._is_long_option(option_string):
                        option_color = t.summary_long_option
                    else:
                        option_color = t.summary_short_option
                    if action.nargs == 0:
                        part = action.format_usage()
                        part = f'{option_color}{part}{t.reset}'
                    else:
                        default = self._get_default_metavar_for_optional(action)
                        args_string = self._format_args(action, default)
                        part = f'{option_color}{option_string} {t.summary_label}{args_string}{t.reset}'
                    if not (action.required or required or in_group):
                        part = '[%s]' % part
                parts.append(part)
            if in_group:
                parts[start] = ('(' if required else '[') + parts[start]
                for i in range(start, len(parts) - 1):
                    parts[i] += ' |'
                parts[-1] += ')' if required else ']'
        if pos_start is None:
            pos_start = len(parts)
        return (parts, pos_start)

    def _format_text(self, text):
        if '%(prog)' in text:
            text = text % dict(prog=self._prog)
        text_width = max(self._width - self._current_indent, 11)
        indent = ' ' * self._current_indent
        return self._fill_text(text, text_width, indent) + '\n\n'

    def _format_action(self, action):
        help_position = min(self._action_max_length + 2, self._max_help_position)
        help_width = max(self._width - help_position, 11)
        action_width = help_position - self._current_indent - 2
        action_header = self._format_action_invocation(action)
        action_header_no_color = self._decolor(action_header)
        if not action.help:
            tup = (self._current_indent, '', action_header)
            action_header = '%*s%s\n' % tup
        elif len(action_header_no_color) <= action_width:
            action_header_color = action_header
            tup = (self._current_indent, '', action_width, action_header_no_color)
            action_header = '%*s%-*s  ' % tup
            action_header = action_header.replace(action_header_no_color, action_header_color)
            indent_first = 0
        else:
            tup = (self._current_indent, '', action_header)
            action_header = '%*s%s\n' % tup
            indent_first = help_position
        parts = [action_header]
        if action.help and action.help.strip():
            help_text = self._expand_help(action)
            if help_text:
                help_lines = self._split_lines(help_text, help_width)
                parts.append('%*s%s\n' % (indent_first, '', help_lines[0]))
                for line in help_lines[1:]:
                    parts.append('%*s%s\n' % (help_position, '', line))
        elif not action_header.endswith('\n'):
            parts.append('\n')
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))
        return self._join_parts(parts)

    def _format_action_invocation(self, action):
        t = self._theme
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            return t.action + ' '.join(self._metavar_formatter(action, default)(1)) + t.reset
        else:

            def color_option_strings(strings):
                parts = []
                for s in strings:
                    if self._is_long_option(s):
                        parts.append(f'{t.long_option}{s}{t.reset}')
                    else:
                        parts.append(f'{t.short_option}{s}{t.reset}')
                return parts
            if action.nargs == 0:
                option_strings = color_option_strings(action.option_strings)
                return ', '.join(option_strings)
            else:
                default = self._get_default_metavar_for_optional(action)
                option_strings = color_option_strings(action.option_strings)
                args_string = f'{t.label}{self._format_args(action, default)}{t.reset}'
                return ', '.join(option_strings) + ' ' + args_string

    def _metavar_formatter(self, action, default_metavar):
        if action.metavar is not None:
            result = action.metavar
        elif action.choices is not None:
            result = '{%s}' % ','.join(map(str, action.choices))
        else:
            result = default_metavar

        def format(tuple_size):
            if isinstance(result, tuple):
                return result
            else:
                return (result,) * tuple_size
        return format

    def _format_args(self, action, default_metavar):
        get_metavar = self._metavar_formatter(action, default_metavar)
        if action.nargs is None:
            result = '%s' % get_metavar(1)
        elif action.nargs == 可选:
            result = '[%s]' % get_metavar(1)
        elif action.nargs == 零或更多:
            metavar = get_metavar(1)
            if len(metavar) == 2:
                result = '[%s [%s ...]]' % metavar
            else:
                result = '[%s ...]' % metavar
        elif action.nargs == 一个或更多:
            result = '%s [%s ...]' % get_metavar(2)
        elif action.nargs == 剩余全部:
            result = '...'
        elif action.nargs == 作为解析器:
            result = '%s ...' % get_metavar(1)
        elif action.nargs == 隐藏:
            result = ''
        else:
            try:
                formats = ['%s' for _ in range(action.nargs)]
            except TypeError:
                raise ValueError('invalid nargs value') from None
            result = ' '.join(formats) % get_metavar(action.nargs)
        return result

    def _expand_help(self, action):
        help_string = self._get_help_string(action)
        if '%' not in help_string:
            return help_string
        params = dict(vars(action), prog=self._prog)
        for name in list(params):
            value = params[name]
            if value is 隐藏:
                del params[name]
            elif hasattr(value, '__name__'):
                params[name] = value.__name__
        if params.get('choices') is not None:
            params['choices'] = ', '.join(map(str, params['choices']))
        return help_string % params

    def _iter_indented_subactions(self, action):
        try:
            get_subactions = action._get_subactions
        except AttributeError:
            pass
        else:
            self._indent()
            yield from get_subactions()
            self._dedent()

    def _split_lines(self, text, width):
        text = self._whitespace_matcher.sub(' ', text).strip()
        import textwrap
        return textwrap.wrap(text, width)

    def _fill_text(self, text, width, indent):
        text = self._whitespace_matcher.sub(' ', text).strip()
        import textwrap
        return textwrap.fill(text, width, initial_indent=indent, subsequent_indent=indent)

    def _get_help_string(self, action):
        return action.help

    def _get_default_metavar_for_optional(self, action):
        return action.dest.upper()

    def _get_default_metavar_for_positional(self, action):
        return action.dest
_装类转发(帮助排版器, {'add_argument': '加参数', 'add_usage': '加用法'}, {'add_argument': '加参数', 'add_usage': '加用法'})

class 原始描述帮助排版器(帮助排版器):
    """Help message formatter which retains any formatting in descriptions.

    Only the name of this class is considered a public API. All the methods
    provided by the class are considered an implementation detail.
    """

    def _fill_text(self, text, width, indent):
        return ''.join((indent + line for line in text.splitlines(keepends=True)))

class 原始文本帮助排版器(原始描述帮助排版器):
    """Help message formatter which retains formatting of all help text.

    Only the name of this class is considered a public API. All the methods
    provided by the class are considered an implementation detail.
    """

    def _split_lines(self, text, width):
        return text.splitlines()

class 含默认值帮助排版器(帮助排版器):
    """Help message formatter which adds default values to argument help.

    Only the name of this class is considered a public API. All the methods
    provided by the class are considered an implementation detail.
    """

    def _get_help_string(self, action):
        help = action.help
        if help is None:
            help = ''
        if '%(default)' not in help and action.default is not 隐藏 and (not action.required):
            defaulting_nargs = (可选, 零或更多)
            if action.option_strings or action.nargs in defaulting_nargs:
                help += _(' (default: %(default)s)')
        return help

class 元变量类型帮助排版器(帮助排版器):
    """Help message formatter which uses the argument 'type' as the default
    metavar value (instead of the argument 'dest')

    Only the name of this class is considered a public API. All the methods
    provided by the class are considered an implementation detail.
    """

    def _get_default_metavar_for_optional(self, action):
        return action.type.__name__

    def _get_default_metavar_for_positional(self, action):
        return action.type.__name__

def _get_action_name(argument):
    if argument is None:
        return None
    elif argument.option_strings:
        return '/'.join(argument.option_strings)
    elif argument.metavar not in (None, 隐藏):
        metavar = argument.metavar
        if not isinstance(metavar, tuple):
            return metavar
        if argument.nargs == 零或更多 and len(metavar) == 2:
            return '%s[, %s]' % metavar
        elif argument.nargs == 一个或更多:
            return '%s[, %s]' % metavar
        else:
            return ', '.join(metavar)
    elif argument.dest not in (None, 隐藏):
        return argument.dest
    elif argument.choices:
        return '{%s}' % ','.join(map(str, argument.choices))
    else:
        return None

class 参数错误(Exception):
    """An error from creating or using an argument (optional or positional).

    The string value of this exception is the message, augmented with
    information about the argument that caused it.
    """

    def __init__(self, argument, message):
        self.argument_name = _get_action_name(argument)
        self.message = message

    def __str__(self):
        if self.argument_name is None:
            format = '%(message)s'
        else:
            format = _('argument %(argument_name)s: %(message)s')
        return format % dict(message=self.message, argument_name=self.argument_name)

class 参数类型错误(Exception):
    """An error from trying to convert a command line string to a type."""
    pass

class 动作(_AttributeHolder):
    """Information about how to convert command line strings to Python objects.

    Action objects are used by an ArgumentParser to represent the information
    needed to parse a single argument from one or more strings from the
    command line. The keyword arguments to the Action constructor are also
    all attributes of Action instances.

    Keyword Arguments:

        - option_strings -- A list of command-line option strings which
            should be associated with this action.

        - dest -- The name of the attribute to hold the created object(s)

        - nargs -- The number of command-line arguments that should be
            consumed. By default, one argument will be consumed and a single
            value will be produced.  Other values include:
                - N (an integer) consumes N arguments (and produces a list)
                - '?' consumes zero or one arguments
                - '*' consumes zero or more arguments (and produces a list)
                - '+' consumes one or more arguments (and produces a list)
            Note that the difference between the default and nargs=1 is that
            with the default, a single value will be produced, while with
            nargs=1, a list containing a single value will be produced.

        - const -- The value to be produced if the option is specified and the
            option uses an action that takes no values.

        - default -- The value to be produced if the option is not specified.

        - type -- A callable that accepts a single string argument, and
            returns the converted value.  The standard Python types str, int,
            float, and complex are useful examples of such callables.  If None,
            str is used.

        - choices -- A container of values that should be allowed. If not None,
            after a command-line argument has been converted to the appropriate
            type, an exception will be raised if it is not a member of this
            collection.

        - required -- True if the action must always be specified at the
            command line. This is only meaningful for optional command-line
            arguments.

        - help -- The help string describing the argument.

        - metavar -- The name to be used for the option's argument with the
            help string. If None, the 'dest' value will be used as the name.
    """

    def __init__(self, option_strings, dest, nargs=None, const=None, default=None, type=None, choices=None, required=False, help=None, metavar=None, deprecated=False):
        self.option_strings = option_strings
        self.dest = dest
        self.nargs = nargs
        self.const = const
        self.default = default
        self.type = type
        self.choices = choices
        self.required = required
        self.help = help
        self.metavar = metavar
        self.deprecated = deprecated

    def _get_kwargs(self):
        names = ['option_strings', 'dest', 'nargs', 'const', 'default', 'type', 'choices', 'required', 'help', 'metavar', 'deprecated']
        return [(name, getattr(self, name)) for name in names]

    def format_usage(self):
        return self.option_strings[0]

    def __call__(self, parser, namespace, values, option_string=None):
        raise NotImplementedError('.__call__() not defined')

class 布尔可选动作(动作):

    def __init__(self, option_strings, dest, default=None, required=False, help=None, deprecated=False):
        _option_strings = []
        for option_string in option_strings:
            _option_strings.append(option_string)
            if option_string.startswith('--'):
                if option_string.startswith('--no-'):
                    raise ValueError(f'invalid option name {option_string!r} for BooleanOptionalAction')
                option_string = '--no-' + option_string[2:]
                _option_strings.append(option_string)
        super().__init__(option_strings=_option_strings, dest=dest, nargs=0, default=default, required=required, help=help, deprecated=deprecated)

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string in self.option_strings:
            setattr(namespace, self.dest, not option_string.startswith('--no-'))

    def format_usage(self):
        return ' | '.join(self.option_strings)

class _StoreAction(动作):

    def __init__(self, option_strings, dest, nargs=None, const=None, default=None, type=None, choices=None, required=False, help=None, metavar=None, deprecated=False):
        if nargs == 0:
            raise ValueError('nargs for store actions must be != 0; if you have nothing to store, actions such as store true or store const may be more appropriate')
        if const is not None and nargs != 可选:
            raise ValueError('nargs must be %r to supply const' % 可选)
        super(_StoreAction, self).__init__(option_strings=option_strings, dest=dest, nargs=nargs, const=const, default=default, type=type, choices=choices, required=required, help=help, metavar=metavar, deprecated=deprecated)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

class _StoreConstAction(动作):

    def __init__(self, option_strings, dest, const=None, default=None, required=False, help=None, metavar=None, deprecated=False):
        super(_StoreConstAction, self).__init__(option_strings=option_strings, dest=dest, nargs=0, const=const, default=default, required=required, help=help, deprecated=deprecated)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.const)

class _StoreTrueAction(_StoreConstAction):

    def __init__(self, option_strings, dest, default=False, required=False, help=None, deprecated=False):
        super(_StoreTrueAction, self).__init__(option_strings=option_strings, dest=dest, const=True, deprecated=deprecated, required=required, help=help, default=default)

class _StoreFalseAction(_StoreConstAction):

    def __init__(self, option_strings, dest, default=True, required=False, help=None, deprecated=False):
        super(_StoreFalseAction, self).__init__(option_strings=option_strings, dest=dest, const=False, default=default, required=required, help=help, deprecated=deprecated)

class _AppendAction(动作):

    def __init__(self, option_strings, dest, nargs=None, const=None, default=None, type=None, choices=None, required=False, help=None, metavar=None, deprecated=False):
        if nargs == 0:
            raise ValueError('nargs for append actions must be != 0; if arg strings are not supplying the value to append, the append const action may be more appropriate')
        if const is not None and nargs != 可选:
            raise ValueError('nargs must be %r to supply const' % 可选)
        super(_AppendAction, self).__init__(option_strings=option_strings, dest=dest, nargs=nargs, const=const, default=default, type=type, choices=choices, required=required, help=help, metavar=metavar, deprecated=deprecated)

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None)
        items = _copy_items(items)
        items.append(values)
        setattr(namespace, self.dest, items)

class _AppendConstAction(动作):

    def __init__(self, option_strings, dest, const=None, default=None, required=False, help=None, metavar=None, deprecated=False):
        super(_AppendConstAction, self).__init__(option_strings=option_strings, dest=dest, nargs=0, const=const, default=default, required=required, help=help, metavar=metavar, deprecated=deprecated)

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None)
        items = _copy_items(items)
        items.append(self.const)
        setattr(namespace, self.dest, items)

class _CountAction(动作):

    def __init__(self, option_strings, dest, default=None, required=False, help=None, deprecated=False):
        super(_CountAction, self).__init__(option_strings=option_strings, dest=dest, nargs=0, default=default, required=required, help=help, deprecated=deprecated)

    def __call__(self, parser, namespace, values, option_string=None):
        count = getattr(namespace, self.dest, None)
        if count is None:
            count = 0
        setattr(namespace, self.dest, count + 1)

class _HelpAction(动作):

    def __init__(self, option_strings, dest=隐藏, default=隐藏, help=None, deprecated=False):
        super(_HelpAction, self).__init__(option_strings=option_strings, dest=dest, default=default, nargs=0, help=help, deprecated=deprecated)

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        parser.exit()

class _VersionAction(动作):

    def __init__(self, option_strings, version=None, dest=隐藏, default=隐藏, help=None, deprecated=False):
        if help is None:
            help = _("show program's version number and exit")
        super(_VersionAction, self).__init__(option_strings=option_strings, dest=dest, default=default, nargs=0, help=help)
        self.version = version

    def __call__(self, parser, namespace, values, option_string=None):
        version = self.version
        if version is None:
            version = parser.version
        formatter = parser._get_formatter()
        formatter.add_text(version)
        parser._print_message(formatter.format_help(), _sys.stdout)
        parser.exit()

class _SubParsersAction(动作):

    class _ChoicesPseudoAction(动作):

        def __init__(self, name, aliases, help):
            metavar = dest = name
            if aliases:
                metavar += ' (%s)' % ', '.join(aliases)
            sup = super(_SubParsersAction._ChoicesPseudoAction, self)
            sup.__init__(option_strings=[], dest=dest, help=help, metavar=metavar)

    def __init__(self, option_strings, prog, parser_class, dest=隐藏, required=False, help=None, metavar=None):
        self._prog_prefix = prog
        self._parser_class = parser_class
        self._name_parser_map = {}
        self._choices_actions = []
        self._deprecated = set()
        self._color = True
        super(_SubParsersAction, self).__init__(option_strings=option_strings, dest=dest, nargs=作为解析器, choices=self._name_parser_map, required=required, help=help, metavar=metavar)

    def add_parser(self, name, *, deprecated=False, **kwargs):
        if kwargs.get('prog') is None:
            kwargs['prog'] = '%s %s' % (self._prog_prefix, name)
        if kwargs.get('color') is None:
            kwargs['color'] = self._color
        aliases = kwargs.pop('aliases', ())
        if name in self._name_parser_map:
            raise ValueError(f'conflicting subparser: {name}')
        for alias in aliases:
            if alias in self._name_parser_map:
                raise ValueError(f'conflicting subparser alias: {alias}')
        if 'help' in kwargs:
            help = kwargs.pop('help')
            choice_action = self._ChoicesPseudoAction(name, aliases, help)
            self._choices_actions.append(choice_action)
        else:
            choice_action = None
        parser = self._parser_class(**kwargs)
        if choice_action is not None:
            parser._check_help(choice_action)
        self._name_parser_map[name] = parser
        for alias in aliases:
            self._name_parser_map[alias] = parser
        if deprecated:
            self._deprecated.add(name)
            self._deprecated.update(aliases)
        return parser

    def _get_subactions(self):
        return self._choices_actions

    def __call__(self, parser, namespace, values, option_string=None):
        parser_name = values[0]
        arg_strings = values[1:]
        if self.dest is not 隐藏:
            setattr(namespace, self.dest, parser_name)
        try:
            subparser = self._name_parser_map[parser_name]
        except KeyError:
            args = {'parser_name': parser_name, 'choices': ', '.join(self._name_parser_map)}
            msg = _('unknown parser %(parser_name)r (choices: %(choices)s)') % args
            raise 参数错误(self, msg)
        if parser_name in self._deprecated:
            parser._warning(_("command '%(parser_name)s' is deprecated") % {'parser_name': parser_name})
        subnamespace, arg_strings = subparser.parse_known_args(arg_strings, None)
        for key, value in vars(subnamespace).items():
            setattr(namespace, key, value)
        if arg_strings:
            if not hasattr(namespace, _UNRECOGNIZED_ARGS_ATTR):
                setattr(namespace, _UNRECOGNIZED_ARGS_ATTR, [])
            getattr(namespace, _UNRECOGNIZED_ARGS_ATTR).extend(arg_strings)

class _ExtendAction(_AppendAction):

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None)
        items = _copy_items(items)
        items.extend(values)
        setattr(namespace, self.dest, items)

class 文件类型(object):
    """Deprecated factory for creating file object types

    Instances of FileType are typically passed as type= arguments to the
    ArgumentParser add_argument() method.

    Keyword Arguments:
        - mode -- A string indicating how the file is to be opened. Accepts the
            same values as the builtin open() function.
        - bufsize -- The file's desired buffer size. Accepts the same values as
            the builtin open() function.
        - encoding -- The file's encoding. Accepts the same values as the
            builtin open() function.
        - errors -- A string indicating how encoding and decoding errors are to
            be handled. Accepts the same value as the builtin open() function.
    """

    def __init__(self, mode='r', bufsize=-1, encoding=None, errors=None):
        import warnings
        warnings.warn('FileType is deprecated. Simply open files after parsing arguments.', category=PendingDeprecationWarning, stacklevel=2)
        self._mode = mode
        self._bufsize = bufsize
        self._encoding = encoding
        self._errors = errors

    def __call__(self, string):
        if string == '-':
            if 'r' in self._mode:
                return _sys.stdin.buffer if 'b' in self._mode else _sys.stdin
            elif any((c in self._mode for c in 'wax')):
                return _sys.stdout.buffer if 'b' in self._mode else _sys.stdout
            else:
                msg = _('argument "-" with mode %r') % self._mode
                raise ValueError(msg)
        try:
            return open(string, self._mode, self._bufsize, self._encoding, self._errors)
        except OSError as e:
            args = {'filename': string, 'error': e}
            message = _("can't open '%(filename)s': %(error)s")
            raise 参数类型错误(message % args)

    def __repr__(self):
        args = (self._mode, self._bufsize)
        kwargs = [('encoding', self._encoding), ('errors', self._errors)]
        args_str = ', '.join([repr(arg) for arg in args if arg != -1] + ['%s=%r' % (kw, arg) for kw, arg in kwargs if arg is not None])
        return '%s(%s)' % (type(self).__name__, args_str)

class 命名空间(_AttributeHolder):
    """Simple object for storing attributes.

    Implements equality by attribute names and values, and provides a simple
    string representation.
    """

    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def __eq__(self, other):
        if not isinstance(other, 命名空间):
            return NotImplemented
        return vars(self) == vars(other)

    def __contains__(self, key):
        return key in self.__dict__

class _ActionsContainer(object):

    def __init__(self, description, prefix_chars, argument_default, conflict_handler):
        super(_ActionsContainer, self).__init__()
        self.description = description
        self.argument_default = argument_default
        self.prefix_chars = prefix_chars
        self.conflict_handler = conflict_handler
        self._registries = {}
        self.登记('action', None, _StoreAction)
        self.登记('action', 'store', _StoreAction)
        self.登记('action', 'store_const', _StoreConstAction)
        self.登记('action', 'store_true', _StoreTrueAction)
        self.登记('action', 'store_false', _StoreFalseAction)
        self.登记('action', 'append', _AppendAction)
        self.登记('action', 'append_const', _AppendConstAction)
        self.登记('action', 'count', _CountAction)
        self.登记('action', 'help', _HelpAction)
        self.登记('action', 'version', _VersionAction)
        self.登记('action', 'parsers', _SubParsersAction)
        self.登记('action', 'extend', _ExtendAction)
        self._get_handler()
        self._actions = []
        self._option_string_actions = {}
        self._action_groups = []
        self._mutually_exclusive_groups = []
        self._defaults = {}
        self._negative_number_matcher = _re.compile('-\\.?\\d')
        self._has_negative_number_optionals = []

    def 登记(self, registry_name, value, object):
        registry = self._registries.setdefault(registry_name, {})
        registry[value] = object

    def _registry_get(self, registry_name, value, default=None):
        return self._registries[registry_name].get(value, default)

    def 设默认值(self, **kwargs):
        self._defaults.update(kwargs)
        for action in self._actions:
            if action.dest in kwargs:
                action.default = kwargs[action.dest]

    def 取默认值(self, dest):
        for action in self._actions:
            if action.dest == dest and action.default is not None:
                return action.default
        return self._defaults.get(dest, None)

    def 加参数(self, *args, **kwargs):
        """
        add_argument(dest, ..., name=value, ...)
        add_argument(option_string, option_string, ..., name=value, ...)
        """
        chars = self.prefix_chars
        if not args or (len(args) == 1 and args[0][0] not in chars):
            if args and 'dest' in kwargs:
                raise TypeError('dest supplied twice for positional argument, did you mean metavar?')
            kwargs = self._get_positional_kwargs(*args, **kwargs)
        else:
            kwargs = self._get_optional_kwargs(*args, **kwargs)
        if 'default' not in kwargs:
            dest = kwargs['dest']
            if dest in self._defaults:
                kwargs['default'] = self._defaults[dest]
            elif self.argument_default is not None:
                kwargs['default'] = self.argument_default
        action_name = kwargs.get('action')
        action_class = self._pop_action_class(kwargs)
        if not callable(action_class):
            raise ValueError(f'unknown action {action_class!r}')
        action = action_class(**kwargs)
        if not action.option_strings and action.nargs == 0:
            raise ValueError(f'action {action_name!r} is not valid for positional arguments')
        type_func = self._registry_get('type', action.type, action.type)
        if not callable(type_func):
            raise TypeError(f'{type_func!r} is not callable')
        if type_func is 文件类型:
            raise TypeError(f'{type_func!r} is a FileType class object, instance of it must be passed')
        if hasattr(self, '_get_validation_formatter'):
            formatter = self._get_validation_formatter()
            try:
                formatter._format_args(action, None)
            except TypeError:
                raise ValueError('length of metavar tuple does not match nargs')
        self._check_help(action)
        return self._add_action(action)

    def 加参数组(self, *args, **kwargs):
        group = _ArgumentGroup(self, *args, **kwargs)
        self._action_groups.append(group)
        return group

    def 加互斥组(self, **kwargs):
        group = _MutuallyExclusiveGroup(self, **kwargs)
        self._mutually_exclusive_groups.append(group)
        return group

    def _add_action(self, action):
        self._check_conflict(action)
        self._actions.append(action)
        action.container = self
        for option_string in action.option_strings:
            self._option_string_actions[option_string] = action
        for option_string in action.option_strings:
            if self._negative_number_matcher.match(option_string):
                if not self._has_negative_number_optionals:
                    self._has_negative_number_optionals.append(True)
        return action

    def _remove_action(self, action):
        self._actions.remove(action)

    def _add_container_actions(self, container):
        title_group_map = {}
        for group in self._action_groups:
            if group.title in title_group_map:
                msg = f'cannot merge actions - two groups are named {group.title!r}'
                raise ValueError(msg)
            title_group_map[group.title] = group
        group_map = {}
        for group in container._action_groups:
            if group.title not in title_group_map:
                title_group_map[group.title] = self.加参数组(title=group.title, description=group.description, conflict_handler=group.conflict_handler)
            for action in group._group_actions:
                group_map[action] = title_group_map[group.title]
        for group in container._mutually_exclusive_groups:
            if group._container is container:
                cont = self
            else:
                cont = title_group_map[group._container.title]
            mutex_group = cont.add_mutually_exclusive_group(required=group.required)
            for action in group._group_actions:
                group_map[action] = mutex_group
        for action in container._actions:
            group_map.get(action, self)._add_action(action)

    def _get_positional_kwargs(self, dest, **kwargs):
        if 'required' in kwargs:
            msg = "'required' is an invalid argument for positionals"
            raise TypeError(msg)
        nargs = kwargs.get('nargs')
        if nargs == 0:
            raise ValueError('nargs for positionals must be != 0')
        if nargs not in [可选, 零或更多, 剩余全部, 隐藏]:
            kwargs['required'] = True
        return dict(kwargs, dest=dest, option_strings=[])

    def _get_optional_kwargs(self, *args, **kwargs):
        option_strings = []
        long_option_strings = []
        for option_string in args:
            if not option_string[0] in self.prefix_chars:
                raise ValueError(f'invalid option string {option_string!r}: must start with a character {self.prefix_chars!r}')
            option_strings.append(option_string)
            if len(option_string) > 1 and option_string[1] in self.prefix_chars:
                long_option_strings.append(option_string)
        dest = kwargs.pop('dest', None)
        if dest is None:
            if long_option_strings:
                dest_option_string = long_option_strings[0]
            else:
                dest_option_string = option_strings[0]
            dest = dest_option_string.lstrip(self.prefix_chars)
            if not dest:
                msg = f'dest= is required for options like {option_string!r}'
                raise TypeError(msg)
            dest = dest.replace('-', '_')
        return dict(kwargs, dest=dest, option_strings=option_strings)

    def _pop_action_class(self, kwargs, default=None):
        action = kwargs.pop('action', default)
        return self._registry_get('action', action, action)

    def _get_handler(self):
        handler_func_name = '_handle_conflict_%s' % self.conflict_handler
        try:
            return getattr(self, handler_func_name)
        except AttributeError:
            msg = f'invalid conflict_resolution value: {self.conflict_handler!r}'
            raise ValueError(msg)

    def _check_conflict(self, action):
        confl_optionals = []
        for option_string in action.option_strings:
            if option_string in self._option_string_actions:
                confl_optional = self._option_string_actions[option_string]
                confl_optionals.append((option_string, confl_optional))
        if confl_optionals:
            conflict_handler = self._get_handler()
            conflict_handler(action, confl_optionals)

    def _handle_conflict_error(self, action, conflicting_actions):
        message = ngettext('conflicting option string: %s', 'conflicting option strings: %s', len(conflicting_actions))
        conflict_string = ', '.join([option_string for option_string, action in conflicting_actions])
        raise 参数错误(action, message % conflict_string)

    def _handle_conflict_resolve(self, action, conflicting_actions):
        for option_string, action in conflicting_actions:
            action.option_strings.remove(option_string)
            self._option_string_actions.pop(option_string, None)
            if not action.option_strings:
                action.container._remove_action(action)

    def _check_help(self, action):
        if action.help and hasattr(self, '_get_validation_formatter'):
            formatter = self._get_validation_formatter()
            try:
                formatter._expand_help(action)
            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError('badly formed help string') from exc
_装类转发(_ActionsContainer, {'add_argument': '加参数', 'add_argument_group': '加参数组', 'add_mutually_exclusive_group': '加互斥组', 'get_default': '取默认值', 'register': '登记', 'set_defaults': '设默认值'}, {'add_argument': '加参数', 'add_argument_group': '加参数组', 'add_mutually_exclusive_group': '加互斥组', 'get_default': '取默认值', 'register': '登记', 'set_defaults': '设默认值'})

class _ArgumentGroup(_ActionsContainer):

    def __init__(self, container, title=None, description=None, **kwargs):
        if 'prefix_chars' in kwargs:
            import warnings
            depr_msg = "The use of the undocumented 'prefix_chars' parameter in ArgumentParser.add_argument_group() is deprecated."
            warnings.warn(depr_msg, DeprecationWarning, stacklevel=3)
        update = kwargs.setdefault
        update('conflict_handler', container.conflict_handler)
        update('prefix_chars', container.prefix_chars)
        update('argument_default', container.argument_default)
        super_init = super(_ArgumentGroup, self).__init__
        super_init(description=description, **kwargs)
        self.title = title
        self._group_actions = []
        self._registries = container._registries
        self._actions = container._actions
        self._option_string_actions = container._option_string_actions
        self._defaults = container._defaults
        self._has_negative_number_optionals = container._has_negative_number_optionals
        self._mutually_exclusive_groups = container._mutually_exclusive_groups

    def _add_action(self, action):
        action = super(_ArgumentGroup, self)._add_action(action)
        self._group_actions.append(action)
        return action

    def _remove_action(self, action):
        super(_ArgumentGroup, self)._remove_action(action)
        self._group_actions.remove(action)

    def 加参数组(self, *args, **kwargs):
        raise ValueError('argument groups cannot be nested')
_装类转发(_ArgumentGroup, {'add_argument_group': '加参数组'}, {'add_argument_group': '加参数组'})

class _MutuallyExclusiveGroup(_ArgumentGroup):

    def __init__(self, container, required=False):
        super(_MutuallyExclusiveGroup, self).__init__(container)
        self.required = required
        self._container = container

    def _add_action(self, action):
        if action.required:
            msg = 'mutually exclusive arguments must be optional'
            raise ValueError(msg)
        action = self._container._add_action(action)
        self._group_actions.append(action)
        return action

    def _remove_action(self, action):
        self._container._remove_action(action)
        self._group_actions.remove(action)

    def 加互斥组(self, **kwargs):
        raise ValueError('mutually exclusive groups cannot be nested')
_装类转发(_MutuallyExclusiveGroup, {'add_mutually_exclusive_group': '加互斥组'}, {'add_mutually_exclusive_group': '加互斥组'})

def _prog_name(prog=None):
    if prog is not None:
        return prog
    arg0 = _sys.argv[0]
    try:
        modspec = _sys.modules['__main__'].__spec__
    except (KeyError, AttributeError):
        modspec = None
    if modspec is None:
        return _os.path.basename(arg0)
    if modspec.name != '__main__' and arg0 != modspec.origin:
        return _os.path.basename(arg0)
    py = _os.path.basename(_sys.executable)
    if modspec.name != '__main__':
        modname = modspec.name.removesuffix('.__main__')
        return f'{py} -m {modname}'
    return f'{py} {arg0}'

class 参数解析器(_AttributeHolder, _ActionsContainer):
    """Object for parsing command line strings into Python objects.

    Keyword Arguments:
        - prog -- The name of the program (default:
            ``os.path.basename(sys.argv[0])``)
        - usage -- A usage message (default: auto-generated from arguments)
        - description -- A description of what the program does
        - epilog -- Text following the argument descriptions
        - parents -- Parsers whose arguments should be copied into this one
        - formatter_class -- HelpFormatter class for printing help messages
        - prefix_chars -- Characters that prefix optional arguments
        - fromfile_prefix_chars -- Characters that prefix files containing
            additional arguments
        - argument_default -- The default value for all arguments
        - conflict_handler -- String indicating how to handle conflicts
        - add_help -- Add a -h/-help option
        - allow_abbrev -- Allow long options to be abbreviated unambiguously
        - exit_on_error -- Determines whether or not ArgumentParser exits with
            error info when an error occurs
        - suggest_on_error - Enables suggestions for mistyped argument choices
            and subparser names (default: ``False``)
        - color - Allow color output in help messages (default: ``False``)
    """

    def __init__(self, prog=None, usage=None, description=None, epilog=None, parents=[], formatter_class=帮助排版器, prefix_chars='-', fromfile_prefix_chars=None, argument_default=None, conflict_handler='error', add_help=True, allow_abbrev=True, exit_on_error=True, *, suggest_on_error=False, color=True):
        superinit = super(参数解析器, self).__init__
        superinit(description=description, prefix_chars=prefix_chars, argument_default=argument_default, conflict_handler=conflict_handler)
        self.prog = _prog_name(prog)
        self.usage = usage
        self.epilog = epilog
        self.formatter_class = formatter_class
        self.fromfile_prefix_chars = fromfile_prefix_chars
        self.add_help = add_help
        self.allow_abbrev = allow_abbrev
        self.exit_on_error = exit_on_error
        self.suggest_on_error = suggest_on_error
        self.color = color
        self._cached_formatter = None
        add_group = self.加参数组
        self._positionals = add_group(_('positional arguments'))
        self._optionals = add_group(_('options'))
        self._subparsers = None
        self.登记('type', None, _identity)
        default_prefix = '-' if '-' in prefix_chars else prefix_chars[0]
        if self.add_help:
            self.加参数(default_prefix + 'h', default_prefix * 2 + 'help', action='help', default=隐藏, help=_('show this help message and exit'))
        for parent in parents:
            if not isinstance(parent, 参数解析器):
                raise TypeError('parents must be a list of ArgumentParser')
            self._add_container_actions(parent)
            defaults = parent._defaults
            self._defaults.update(defaults)

    def _get_kwargs(self):
        names = ['prog', 'usage', 'description', 'formatter_class', 'conflict_handler', 'add_help']
        return [(name, getattr(self, name)) for name in names]

    def 加子解析器(self, **kwargs):
        if self._subparsers is not None:
            raise ValueError('cannot have multiple subparser arguments')
        kwargs.setdefault('parser_class', type(self))
        if 'title' in kwargs or 'description' in kwargs:
            title = kwargs.pop('title', _('subcommands'))
            description = kwargs.pop('description', None)
            self._subparsers = self.加参数组(title, description)
        else:
            self._subparsers = self._positionals
        if kwargs.get('prog') is None:
            formatter = self.formatter_class(prog=self.prog)
            formatter._set_color(False)
            positionals = self._get_positional_actions()
            groups = self._mutually_exclusive_groups
            formatter.add_usage(None, positionals, groups, '')
            kwargs['prog'] = formatter.format_help().strip()
        parsers_class = self._pop_action_class(kwargs, 'parsers')
        action = parsers_class(option_strings=[], **kwargs)
        action._color = self.color
        self._check_help(action)
        self._subparsers._add_action(action)
        return action

    def _add_action(self, action):
        if action.option_strings:
            self._optionals._add_action(action)
        else:
            self._positionals._add_action(action)
        return action

    def _get_optional_actions(self):
        return [action for action in self._actions if action.option_strings]

    def _get_positional_actions(self):
        return [action for action in self._actions if not action.option_strings]

    def 解析参数(self, args=None, namespace=None):
        args, argv = self.解析已知参数(args, namespace)
        if argv:
            msg = _('unrecognized arguments: %s') % ' '.join(argv)
            if self.exit_on_error:
                self.error(msg)
            else:
                raise 参数错误(None, msg)
        return args

    def 解析已知参数(self, args=None, namespace=None):
        return self._parse_known_args2(args, namespace, intermixed=False)

    def _parse_known_args2(self, args, namespace, intermixed):
        if args is None:
            args = _sys.argv[1:]
        else:
            args = list(args)
        if namespace is None:
            namespace = 命名空间()
        for action in self._actions:
            if action.dest is not 隐藏:
                if not hasattr(namespace, action.dest):
                    if action.default is not 隐藏:
                        setattr(namespace, action.dest, action.default)
        for dest in self._defaults:
            if not hasattr(namespace, dest):
                setattr(namespace, dest, self._defaults[dest])
        if self.exit_on_error:
            try:
                namespace, args = self._parse_known_args(args, namespace, intermixed)
            except 参数错误 as err:
                self.error(str(err))
        else:
            namespace, args = self._parse_known_args(args, namespace, intermixed)
        if hasattr(namespace, _UNRECOGNIZED_ARGS_ATTR):
            args.extend(getattr(namespace, _UNRECOGNIZED_ARGS_ATTR))
            delattr(namespace, _UNRECOGNIZED_ARGS_ATTR)
        return (namespace, args)

    def _parse_known_args(self, arg_strings, namespace, intermixed):
        if self.fromfile_prefix_chars is not None:
            arg_strings = self._read_args_from_files(arg_strings)
        action_conflicts = {}
        for mutex_group in self._mutually_exclusive_groups:
            group_actions = mutex_group._group_actions
            for i, mutex_action in enumerate(mutex_group._group_actions):
                conflicts = action_conflicts.setdefault(mutex_action, [])
                conflicts.extend(group_actions[:i])
                conflicts.extend(group_actions[i + 1:])
        option_string_indices = {}
        arg_string_pattern_parts = []
        arg_strings_iter = iter(arg_strings)
        for i, arg_string in enumerate(arg_strings_iter):
            if arg_string == '--':
                arg_string_pattern_parts.append('-')
                for arg_string in arg_strings_iter:
                    arg_string_pattern_parts.append('A')
            else:
                option_tuples = self._parse_optional(arg_string)
                if option_tuples is None:
                    pattern = 'A'
                else:
                    option_string_indices[i] = option_tuples
                    pattern = 'O'
                arg_string_pattern_parts.append(pattern)
        arg_strings_pattern = ''.join(arg_string_pattern_parts)
        seen_actions = set()
        seen_non_default_actions = set()
        warned = set()

        def take_action(action, argument_strings, option_string=None):
            seen_actions.add(action)
            argument_values = self._get_values(action, argument_strings)
            if action.option_strings or argument_strings:
                seen_non_default_actions.add(action)
                for conflict_action in action_conflicts.get(action, []):
                    if conflict_action in seen_non_default_actions:
                        msg = _('not allowed with argument %s')
                        action_name = _get_action_name(conflict_action)
                        raise 参数错误(action, msg % action_name)
            if argument_values is not 隐藏:
                action(self, namespace, argument_values, option_string)

        def consume_optional(start_index):
            option_tuples = option_string_indices[start_index]
            if len(option_tuples) > 1:
                options = ', '.join([option_string for action, option_string, sep, explicit_arg in option_tuples])
                args = {'option': arg_strings[start_index], 'matches': options}
                msg = _('ambiguous option: %(option)s could match %(matches)s')
                raise 参数错误(None, msg % args)
            action, option_string, sep, explicit_arg = option_tuples[0]
            match_argument = self._match_argument
            action_tuples = []
            while True:
                if action is None:
                    extras.append(arg_strings[start_index])
                    extras_pattern.append('O')
                    return start_index + 1
                if explicit_arg is not None:
                    arg_count = match_argument(action, 'A')
                    chars = self.prefix_chars
                    if arg_count == 0 and option_string[1] not in chars and (explicit_arg != ''):
                        if sep or explicit_arg[0] in chars:
                            msg = _('ignored explicit argument %r')
                            raise 参数错误(action, msg % explicit_arg)
                        action_tuples.append((action, [], option_string))
                        char = option_string[0]
                        option_string = char + explicit_arg[0]
                        optionals_map = self._option_string_actions
                        if option_string in optionals_map:
                            action = optionals_map[option_string]
                            explicit_arg = explicit_arg[1:]
                            if not explicit_arg:
                                sep = explicit_arg = None
                            elif explicit_arg[0] == '=':
                                sep = '='
                                explicit_arg = explicit_arg[1:]
                            else:
                                sep = ''
                        else:
                            extras.append(char + explicit_arg)
                            extras_pattern.append('O')
                            stop = start_index + 1
                            break
                    elif arg_count == 1:
                        stop = start_index + 1
                        args = [explicit_arg]
                        action_tuples.append((action, args, option_string))
                        break
                    else:
                        msg = _('ignored explicit argument %r')
                        raise 参数错误(action, msg % explicit_arg)
                else:
                    start = start_index + 1
                    selected_patterns = arg_strings_pattern[start:]
                    arg_count = match_argument(action, selected_patterns)
                    stop = start + arg_count
                    args = arg_strings[start:stop]
                    action_tuples.append((action, args, option_string))
                    break
            assert action_tuples
            for action, args, option_string in action_tuples:
                if action.deprecated and option_string not in warned:
                    self._warning(_("option '%(option)s' is deprecated") % {'option': option_string})
                    warned.add(option_string)
                take_action(action, args, option_string)
            return stop
        positionals = self._get_positional_actions()

        def consume_positionals(start_index):
            match_partial = self._match_arguments_partial
            selected_pattern = arg_strings_pattern[start_index:]
            arg_counts = match_partial(positionals, selected_pattern)
            for action, arg_count in zip(positionals, arg_counts):
                args = arg_strings[start_index:start_index + arg_count]
                if action.nargs == 作为解析器:
                    if arg_strings_pattern[start_index] == '-':
                        assert args[0] == '--'
                        args.remove('--')
                elif action.nargs != 剩余全部:
                    if arg_strings_pattern.find('-', start_index, start_index + arg_count) >= 0:
                        args.remove('--')
                start_index += arg_count
                if args and action.deprecated and (action.dest not in warned):
                    self._warning(_("argument '%(argument_name)s' is deprecated") % {'argument_name': action.dest})
                    warned.add(action.dest)
                take_action(action, args)
            positionals[:] = positionals[len(arg_counts):]
            return start_index
        extras = []
        extras_pattern = []
        start_index = 0
        if option_string_indices:
            max_option_string_index = max(option_string_indices)
        else:
            max_option_string_index = -1
        while start_index <= max_option_string_index:
            next_option_string_index = start_index
            while next_option_string_index <= max_option_string_index:
                if next_option_string_index in option_string_indices:
                    break
                next_option_string_index += 1
            if not intermixed and start_index != next_option_string_index:
                positionals_end_index = consume_positionals(start_index)
                if positionals_end_index > start_index:
                    start_index = positionals_end_index
                    continue
                else:
                    start_index = positionals_end_index
            if start_index not in option_string_indices:
                strings = arg_strings[start_index:next_option_string_index]
                extras.extend(strings)
                extras_pattern.extend(arg_strings_pattern[start_index:next_option_string_index])
                start_index = next_option_string_index
            start_index = consume_optional(start_index)
        if not intermixed:
            stop_index = consume_positionals(start_index)
            extras.extend(arg_strings[stop_index:])
        else:
            extras.extend(arg_strings[start_index:])
            extras_pattern.extend(arg_strings_pattern[start_index:])
            extras_pattern = ''.join(extras_pattern)
            assert len(extras_pattern) == len(extras)
            arg_strings = [s for s, c in zip(extras, extras_pattern) if c != 'O']
            arg_strings_pattern = extras_pattern.replace('O', '')
            stop_index = consume_positionals(0)
            for i, c in enumerate(extras_pattern):
                if not stop_index:
                    break
                if c != 'O':
                    stop_index -= 1
                    extras[i] = None
            extras = [s for s in extras if s is not None]
        required_actions = []
        for action in self._actions:
            if action not in seen_actions:
                if action.required:
                    required_actions.append(_get_action_name(action))
                elif action.default is not None and isinstance(action.default, str) and hasattr(namespace, action.dest) and (action.default is getattr(namespace, action.dest)):
                    setattr(namespace, action.dest, self._get_value(action, action.default))
        if required_actions:
            raise 参数错误(None, _('the following arguments are required: %s') % ', '.join(required_actions))
        for group in self._mutually_exclusive_groups:
            if group.required:
                for action in group._group_actions:
                    if action in seen_non_default_actions:
                        break
                else:
                    names = [_get_action_name(action) for action in group._group_actions if action.help is not 隐藏]
                    msg = _('one of the arguments %s is required')
                    raise 参数错误(None, msg % ' '.join(names))
        return (namespace, extras)

    def _read_args_from_files(self, arg_strings):
        new_arg_strings = []
        for arg_string in arg_strings:
            if not arg_string or arg_string[0] not in self.fromfile_prefix_chars:
                new_arg_strings.append(arg_string)
            else:
                try:
                    with open(arg_string[1:], encoding=_sys.getfilesystemencoding(), errors=_sys.getfilesystemencodeerrors()) as args_file:
                        arg_strings = []
                        for arg_line in args_file.read().splitlines():
                            for arg in self.convert_arg_line_to_args(arg_line):
                                arg_strings.append(arg)
                        arg_strings = self._read_args_from_files(arg_strings)
                        new_arg_strings.extend(arg_strings)
                except OSError as err:
                    raise 参数错误(None, str(err))
        return new_arg_strings

    def convert_arg_line_to_args(self, arg_line):
        return [arg_line]

    def _match_argument(self, action, arg_strings_pattern):
        nargs_pattern = self._get_nargs_pattern(action)
        match = _re.match(nargs_pattern, arg_strings_pattern)
        if match is None:
            nargs_errors = {None: _('expected one argument'), 可选: _('expected at most one argument'), 一个或更多: _('expected at least one argument')}
            msg = nargs_errors.get(action.nargs)
            if msg is None:
                msg = ngettext('expected %s argument', 'expected %s arguments', action.nargs) % action.nargs
            raise 参数错误(action, msg)
        return len(match.group(1))

    def _match_arguments_partial(self, actions, arg_strings_pattern):
        for i in range(len(actions), 0, -1):
            actions_slice = actions[:i]
            pattern = ''.join([self._get_nargs_pattern(action) for action in actions_slice])
            match = _re.match(pattern, arg_strings_pattern)
            if match is not None:
                result = [len(string) for string in match.groups()]
                if match.end() < len(arg_strings_pattern) and arg_strings_pattern[match.end()] == 'O':
                    while result and (not result[-1]):
                        del result[-1]
                return result
        return []

    def _parse_optional(self, arg_string):
        if not arg_string:
            return None
        if not arg_string[0] in self.prefix_chars:
            return None
        if arg_string in self._option_string_actions:
            action = self._option_string_actions[arg_string]
            return [(action, arg_string, None, None)]
        if len(arg_string) == 1:
            return None
        option_string, sep, explicit_arg = arg_string.partition('=')
        if sep and option_string in self._option_string_actions:
            action = self._option_string_actions[option_string]
            return [(action, option_string, sep, explicit_arg)]
        option_tuples = self._get_option_tuples(arg_string)
        if option_tuples:
            return option_tuples
        if self._negative_number_matcher.match(arg_string):
            if not self._has_negative_number_optionals:
                return None
        if ' ' in arg_string:
            return None
        return [(None, arg_string, None, None)]

    def _get_option_tuples(self, option_string):
        result = []
        chars = self.prefix_chars
        if option_string[0] in chars and option_string[1] in chars:
            if self.allow_abbrev:
                option_prefix, sep, explicit_arg = option_string.partition('=')
                if not sep:
                    sep = explicit_arg = None
                for option_string in self._option_string_actions:
                    if option_string.startswith(option_prefix):
                        action = self._option_string_actions[option_string]
                        tup = (action, option_string, sep, explicit_arg)
                        result.append(tup)
        elif option_string[0] in chars and option_string[1] not in chars:
            option_prefix, sep, explicit_arg = option_string.partition('=')
            if not sep:
                sep = explicit_arg = None
            short_option_prefix = option_string[:2]
            short_explicit_arg = option_string[2:]
            for option_string in self._option_string_actions:
                if option_string == short_option_prefix:
                    action = self._option_string_actions[option_string]
                    tup = (action, option_string, '', short_explicit_arg)
                    result.append(tup)
                elif self.allow_abbrev and option_string.startswith(option_prefix):
                    action = self._option_string_actions[option_string]
                    tup = (action, option_string, sep, explicit_arg)
                    result.append(tup)
        else:
            raise 参数错误(None, _('unexpected option string: %s') % option_string)
        return result

    def _get_nargs_pattern(self, action):
        nargs = action.nargs
        option = action.option_strings
        if nargs is None:
            nargs_pattern = '([A])' if option else '(-*A-*)'
        elif nargs == 可选:
            nargs_pattern = '(A?)' if option else '(-*A?-*)'
        elif nargs == 零或更多:
            nargs_pattern = '(A*)' if option else '(-*[A-]*)'
        elif nargs == 一个或更多:
            nargs_pattern = '(A+)' if option else '(-*A[A-]*)'
        elif nargs == 剩余全部:
            nargs_pattern = '([AO]*)' if option else '(.*)'
        elif nargs == 作为解析器:
            nargs_pattern = '(A[AO]*)' if option else '(-*A[-AO]*)'
        elif nargs == 隐藏:
            nargs_pattern = '()' if option else '(-*)'
        else:
            nargs_pattern = '([AO]{%d})' % nargs if option else '((?:-*A){%d}-*)' % nargs
        return nargs_pattern

    def 解析混杂参数(self, args=None, namespace=None):
        args, argv = self.解析已知混杂参数(args, namespace)
        if argv:
            msg = _('unrecognized arguments: %s') % ' '.join(argv)
            if self.exit_on_error:
                self.error(msg)
            else:
                raise 参数错误(None, msg)
        return args

    def 解析已知混杂参数(self, args=None, namespace=None):
        positionals = self._get_positional_actions()
        a = [action for action in positionals if action.nargs in [作为解析器, 剩余全部]]
        if a:
            raise TypeError('parse_intermixed_args: positional arg with nargs=%s' % a[0].nargs)
        return self._parse_known_args2(args, namespace, intermixed=True)

    def _get_values(self, action, arg_strings):
        if not arg_strings and action.nargs == 可选:
            if action.option_strings:
                value = action.const
            else:
                value = action.default
            if isinstance(value, str) and value is not 隐藏:
                value = self._get_value(action, value)
        elif not arg_strings and action.nargs == 零或更多 and (not action.option_strings):
            if action.default is not None:
                value = action.default
            else:
                value = []
        elif len(arg_strings) == 1 and action.nargs in [None, 可选]:
            arg_string, = arg_strings
            value = self._get_value(action, arg_string)
            self._check_value(action, value)
        elif action.nargs == 剩余全部:
            value = [self._get_value(action, v) for v in arg_strings]
        elif action.nargs == 作为解析器:
            value = [self._get_value(action, v) for v in arg_strings]
            self._check_value(action, value[0])
        elif action.nargs == 隐藏:
            value = 隐藏
        else:
            value = [self._get_value(action, v) for v in arg_strings]
            for v in value:
                self._check_value(action, v)
        return value

    def _get_value(self, action, arg_string):
        type_func = self._registry_get('type', action.type, action.type)
        if not callable(type_func):
            raise TypeError(f'{type_func!r} is not callable')
        try:
            result = type_func(arg_string)
        except 参数类型错误 as err:
            msg = str(err)
            raise 参数错误(action, msg)
        except (TypeError, ValueError):
            name = getattr(action.type, '__name__', repr(action.type))
            args = {'type': name, 'value': arg_string}
            msg = _('invalid %(type)s value: %(value)r')
            raise 参数错误(action, msg % args)
        return result

    def _check_value(self, action, value):
        choices = action.choices
        if choices is None:
            return
        if isinstance(choices, str):
            choices = iter(choices)
        if value not in choices:
            args = {'value': str(value), 'choices': ', '.join((repr(str(choice)) for choice in action.choices))}
            msg = _('invalid choice: %(value)r (choose from %(choices)s)')
            if self.suggest_on_error and isinstance(value, str):
                if all((isinstance(choice, str) for choice in action.choices)):
                    import difflib
                    suggestions = difflib.get_close_matches(value, action.choices, 1)
                    if suggestions:
                        args['closest'] = suggestions[0]
                        msg = _('invalid choice: %(value)r, maybe you meant %(closest)r? (choose from %(choices)s)')
            raise 参数错误(action, msg % args)

    def format_usage(self):
        formatter = self._get_formatter()
        formatter.add_usage(self.usage, self._actions, self._mutually_exclusive_groups)
        return formatter.format_help()

    def format_help(self):
        formatter = self._get_formatter()
        formatter.add_usage(self.usage, self._actions, self._mutually_exclusive_groups)
        formatter.add_text(self.description)
        for action_group in self._action_groups:
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()
        formatter.add_text(self.epilog)
        return formatter.format_help()

    def _get_formatter(self):
        formatter = self.formatter_class(prog=self.prog)
        formatter._set_color(self.color)
        return formatter

    def _get_validation_formatter(self):
        if self._cached_formatter is None:
            self._cached_formatter = self._get_formatter()
        return self._cached_formatter

    def print_usage(self, file=None):
        if file is None:
            file = _sys.stdout
        self._print_message(self.format_usage(), file)

    def print_help(self, file=None):
        if file is None:
            file = _sys.stdout
        self._print_message(self.format_help(), file)

    def _print_message(self, message, file=None):
        if message:
            file = file or _sys.stderr
            try:
                file.write(message)
            except (AttributeError, OSError):
                pass

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, _sys.stderr)
        _sys.exit(status)

    def error(self, message):
        """error(message: string)

        Prints a usage message incorporating the message to stderr and
        exits.

        If you override this in a subclass, it should not return -- it
        should either exit or raise an exception.
        """
        if _zh可用():
            用法 = self.format_usage()
            if 用法.startswith('usage: '):
                用法 = '用法：' + 用法[len('usage: '):]
            self._print_message(用法, _sys.stderr)
            args = {'prog': self.prog, 'message': _zh正文(message)}
            self.exit(2, '%(prog)s：错误：%(message)s\n' % args)
        else:
            self.print_usage(_sys.stderr)
            args = {'prog': self.prog, 'message': message}
            self.exit(2, _('%(prog)s: error: %(message)s\n') % args)

    def _warning(self, message):
        if _zh可用():
            self._print_message('%(prog)s：警告：%(message)s\n' % {'prog': self.prog, 'message': _zh正文(message)}, _sys.stderr)
            return
        args = {'prog': self.prog, 'message': message}
        self._print_message(_('%(prog)s: warning: %(message)s\n') % args, _sys.stderr)
_装类转发(参数解析器, {'add_subparsers': '加子解析器', 'parse_args': '解析参数', 'parse_intermixed_args': '解析混杂参数', 'parse_known_args': '解析已知参数', 'parse_known_intermixed_args': '解析已知混杂参数'}, {'add_argument': '加参数', 'add_argument_group': '加参数组', 'add_subparsers': '加子解析器', 'parse_args': '解析参数', 'parse_intermixed_args': '解析混杂参数', 'parse_known_args': '解析已知参数', 'parse_known_intermixed_args': '解析已知混杂参数', 'register': '登记'})


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Action': '动作',
    'ArgumentDefaultsHelpFormatter': '含默认值帮助排版器',
    'ArgumentError': '参数错误',
    'ArgumentParser': '参数解析器',
    'ArgumentTypeError': '参数类型错误',
    'BooleanOptionalAction': '布尔可选动作',
    'FileType': '文件类型',
    'HelpFormatter': '帮助排版器',
    'MetavarTypeHelpFormatter': '元变量类型帮助排版器',
    'Namespace': '命名空间',
    'ONE_OR_MORE': '一个或更多',
    'OPTIONAL': '可选',
    'PARSER': '作为解析器',
    'REMAINDER': '剩余全部',
    'RawDescriptionHelpFormatter': '原始描述帮助排版器',
    'RawTextHelpFormatter': '原始文本帮助排版器',
    'SUPPRESS': '隐藏',
    'ZERO_OR_MORE': '零或更多',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '_ActionsContainer': {
        'add_argument': '加参数',
        'add_argument_group': '加参数组',
        'add_mutually_exclusive_group': '加互斥组',
        'get_default': '取默认值',
        'register': '登记',
        'set_defaults': '设默认值',
    },
    '_ArgumentGroup': {
        'add_argument_group': '加参数组',
    },
    '_MutuallyExclusiveGroup': {
        'add_mutually_exclusive_group': '加互斥组',
    },
    '参数解析器': {
        'add_subparsers': '加子解析器',
        'parse_args': '解析参数',
        'parse_intermixed_args': '解析混杂参数',
        'parse_known_args': '解析已知参数',
        'parse_known_intermixed_args': '解析已知混杂参数',
    },
    '帮助排版器': {
        'add_argument': '加参数',
        'add_usage': '加用法',
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
    '_ActionsContainer': {
        'add_argument': '加参数',
        'add_argument_group': '加参数组',
        'add_mutually_exclusive_group': '加互斥组',
        'get_default': '取默认值',
        'register': '登记',
        'set_defaults': '设默认值',
    },
    '_ArgumentGroup': {
        'add_argument_group': '加参数组',
    },
    '_MutuallyExclusiveGroup': {
        'add_mutually_exclusive_group': '加互斥组',
    },
    '参数解析器': {
        'add_argument': '加参数',
        'add_argument_group': '加参数组',
        'add_subparsers': '加子解析器',
        'parse_args': '解析参数',
        'parse_intermixed_args': '解析混杂参数',
        'parse_known_args': '解析已知参数',
        'parse_known_intermixed_args': '解析已知混杂参数',
        'register': '登记',
    },
    '帮助排版器': {
        'add_argument': '加参数',
        'add_usage': '加用法',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '一个或更多',
    '作为解析器',
    '元变量类型帮助排版器',
    '剩余全部',
    '动作',
    '原始描述帮助排版器',
    '原始文本帮助排版器',
    '参数类型错误',
    '参数解析器',
    '参数错误',
    '可选',
    '含默认值帮助排版器',
    '命名空间',
    '布尔可选动作',
    '帮助排版器',
    '文件类型',
    '隐藏',
    '零或更多',
]

# ---- 转发层结束 ----
