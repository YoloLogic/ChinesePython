# -*- coding: utf-8 -*-
"""命令行选项 —— 汉语库（由 tools/汉化库.py 从 Lib/optparse.py 机械生成，**不要手改**）。

英文库 Lib/optparse.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 命令行选项
"""


"""A powerful, extensible, and easy-to-use option parser.

By Greg Ward <gward@python.net>

Originally distributed as Optik.

For support, use the optik-users@lists.sourceforge.net mailing list
(http://lists.sourceforge.net/lists/listinfo/optik-users).

Simple usage example:

   from optparse import OptionParser

   parser = OptionParser()
   parser.add_option("-f", "--file", dest="filename",
                     help="write report to FILE", metavar="FILE")
   parser.add_option("-q", "--quiet",
                     action="store_false", dest="verbose", default=True,
                     help="don't print status messages to stdout")

   (options, args) = parser.parse_args()
"""
_英文原名表 = {'AmbiguousOptionError': '选项歧义错误', 'BadOptionError': '坏选项错误', 'HelpFormatter': '帮助格式化器', 'IndentedHelpFormatter': '缩进帮助格式化器', 'NO_DEFAULT': '无默认值', 'OptParseError': '选项解析错误', 'Option': '选项', 'OptionConflictError': '选项冲突错误', 'OptionContainer': '选项容器', 'OptionError': '选项错误', 'OptionGroup': '选项组', 'OptionParser': '选项解析器', 'OptionValueError': '选项值错误', 'SUPPRESS_HELP': '隐藏帮助', 'SUPPRESS_USAGE': '隐藏用法', 'TitledHelpFormatter': '标题帮助格式化器', 'Values': '值集合', 'check_builtin': '检查内置类型', 'check_choice': '检查候选项', 'make_option': '造选项'}

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
__version__ = '1.5.3'
__all__ = ['Option', 'make_option', 'SUPPRESS_HELP', 'SUPPRESS_USAGE', 'Values', 'OptionContainer', 'OptionGroup', 'OptionParser', 'HelpFormatter', 'IndentedHelpFormatter', 'TitledHelpFormatter', 'OptParseError', 'OptionError', 'OptionConflictError', 'OptionValueError', 'BadOptionError', 'check_choice']
__copyright__ = '\nCopyright (c) 2001-2006 Gregory P. Ward.  All rights reserved.\nCopyright (c) 2002 Python Software Foundation.  All rights reserved.\n\nRedistribution and use in source and binary forms, with or without\nmodification, are permitted provided that the following conditions are\nmet:\n\n  * Redistributions of source code must retain the above copyright\n    notice, this list of conditions and the following disclaimer.\n\n  * Redistributions in binary form must reproduce the above copyright\n    notice, this list of conditions and the following disclaimer in the\n    documentation and/or other materials provided with the distribution.\n\n  * Neither the name of the author nor the names of its\n    contributors may be used to endorse or promote products derived from\n    this software without specific prior written permission.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS\nIS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED\nTO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A\nPARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR\nCONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,\nEXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,\nPROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR\nPROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF\nLIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING\nNEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\nSOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n'
import sys, os
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

def _repr(self):
    return '<%s at 0x%x: %s>' % (self.__class__.__name__, id(self), self)

class 选项解析错误(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class 选项错误(选项解析错误):
    """
    Raised if an Option instance is created with invalid or
    inconsistent arguments.
    """

    def __init__(self, msg, option):
        self.msg = msg
        self.option_id = str(option)

    def __str__(self):
        if self.option_id:
            return 'option %s: %s' % (self.option_id, self.msg)
        else:
            return self.msg

class 选项冲突错误(选项错误):
    """
    Raised if conflicting options are added to an OptionParser.
    """

class 选项值错误(选项解析错误):
    """
    Raised if an invalid option value is encountered on the command
    line.
    """

class 坏选项错误(选项解析错误):
    """
    Raised if an invalid option is seen on the command line.
    """

    def __init__(self, opt_str):
        self.opt_str = opt_str

    def __str__(self):
        return _('no such option: %s') % self.opt_str

class 选项歧义错误(坏选项错误):
    """
    Raised if an ambiguous option is seen on the command line.
    """

    def __init__(self, opt_str, possibilities):
        坏选项错误.__init__(self, opt_str)
        self.possibilities = possibilities

    def __str__(self):
        return _('ambiguous option: %s (%s?)') % (self.opt_str, ', '.join(self.possibilities))

class 帮助格式化器:
    """
    Abstract base class for formatting option help.  OptionParser
    instances should use one of the HelpFormatter subclasses for
    formatting help; by default IndentedHelpFormatter is used.

    Instance attributes:
      parser : OptionParser
        the controlling OptionParser instance
      indent_increment : int
        the number of columns to indent per nesting level
      max_help_position : int
        the maximum starting column for option help text
      help_position : int
        the calculated starting column for option help text;
        initially the same as the maximum
      width : int
        total number of columns for output (pass None to constructor for
        this value to be taken from the $COLUMNS environment variable)
      level : int
        current indentation level
      current_indent : int
        current indentation level (in columns)
      help_width : int
        number of columns available for option help text (calculated)
      default_tag : str
        text to replace with each option's default value, "%default"
        by default.  Set to false value to disable default value expansion.
      option_strings : { Option : str }
        maps Option instances to the snippet of help text explaining
        the syntax of that option, e.g. "-h, --help" or
        "-fFILE, --file=FILE"
      _short_opt_fmt : str
        format string controlling how short options with values are
        printed in help text.  Must be either "%s%s" ("-fFILE") or
        "%s %s" ("-f FILE"), because those are the two syntaxes that
        Optik supports.
      _long_opt_fmt : str
        similar but for long options; must be either "%s %s" ("--file FILE")
        or "%s=%s" ("--file=FILE").
    """
    NO_DEFAULT_VALUE = 'none'

    def __init__(self, indent_increment, max_help_position, width, short_first):
        self.parser = None
        self.indent_increment = indent_increment
        if width is None:
            try:
                width = int(os.environ['COLUMNS'])
            except (KeyError, ValueError):
                width = 80
            width -= 2
        self.width = width
        self.help_position = self.max_help_position = min(max_help_position, max(width - 20, indent_increment * 2))
        self.current_indent = 0
        self.level = 0
        self.help_width = None
        self.short_first = short_first
        self.default_tag = '%default'
        self.option_strings = {}
        self._short_opt_fmt = '%s %s'
        self._long_opt_fmt = '%s=%s'

    def 设解析器(self, parser):
        self.parser = parser

    def 设短选项分隔符(self, delim):
        if delim not in ('', ' '):
            raise ValueError('invalid metavar delimiter for short options: %r' % delim)
        self._short_opt_fmt = '%s' + delim + '%s'

    def 设长选项分隔符(self, delim):
        if delim not in ('=', ' '):
            raise ValueError('invalid metavar delimiter for long options: %r' % delim)
        self._long_opt_fmt = '%s' + delim + '%s'

    def 增缩进(self):
        self.current_indent += self.indent_increment
        self.level += 1

    def 减缩进(self):
        self.current_indent -= self.indent_increment
        assert self.current_indent >= 0, 'Indent decreased below 0.'
        self.level -= 1

    def 格式化用法(self, usage):
        raise NotImplementedError('subclasses must implement')

    def 格式化标题(self, heading):
        raise NotImplementedError('subclasses must implement')

    def _format_text(self, text):
        """
        Format a paragraph of free-form text for inclusion in the
        help output at the current indentation level.
        """
        import textwrap
        text_width = max(self.width - self.current_indent, 11)
        增缩进 = ' ' * self.current_indent
        return textwrap.fill(text, text_width, initial_indent=增缩进, subsequent_indent=增缩进)

    def 格式化说明(self, description):
        if description:
            return self._format_text(description) + '\n'
        else:
            return ''

    def 格式化结尾(self, epilog):
        if epilog:
            return '\n' + self._format_text(epilog) + '\n'
        else:
            return ''

    def 展开默认值(self, option):
        if self.parser is None or not self.default_tag:
            return option.help
        default_value = self.parser.defaults.get(option.dest)
        if default_value is 无默认值 or default_value is None:
            default_value = self.NO_DEFAULT_VALUE
        return option.help.replace(self.default_tag, str(default_value))

    def 格式化选项(self, option):
        result = []
        opts = self.option_strings[option]
        opt_width = self.help_position - self.current_indent - 2
        if len(opts) > opt_width:
            opts = '%*s%s\n' % (self.current_indent, '', opts)
            indent_first = self.help_position
        else:
            opts = '%*s%-*s  ' % (self.current_indent, '', opt_width, opts)
            indent_first = 0
        result.append(opts)
        if option.help:
            import textwrap
            help_text = self.展开默认值(option)
            help_lines = textwrap.wrap(help_text, self.help_width)
            result.append('%*s%s\n' % (indent_first, '', help_lines[0]))
            result.extend(['%*s%s\n' % (self.help_position, '', line) for line in help_lines[1:]])
        elif opts[-1] != '\n':
            result.append('\n')
        return ''.join(result)

    def 存选项字符串(self, parser):
        self.增缩进()
        max_len = 0
        for opt in parser.option_list:
            strings = self.格式化选项字符串(opt)
            self.option_strings[opt] = strings
            max_len = max(max_len, len(strings) + self.current_indent)
        self.增缩进()
        for group in parser.option_groups:
            for opt in group.option_list:
                strings = self.格式化选项字符串(opt)
                self.option_strings[opt] = strings
                max_len = max(max_len, len(strings) + self.current_indent)
        self.减缩进()
        self.减缩进()
        self.help_position = min(max_len + 2, self.max_help_position)
        self.help_width = max(self.width - self.help_position, 11)

    def 格式化选项字符串(self, option):
        """Return a comma-separated list of option strings & metavariables."""
        if option.takes_value():
            metavar = option.metavar or option.dest.upper()
            short_opts = [self._short_opt_fmt % (sopt, metavar) for sopt in option._short_opts]
            long_opts = [self._long_opt_fmt % (lopt, metavar) for lopt in option._long_opts]
        else:
            short_opts = option._short_opts
            long_opts = option._long_opts
        if self.short_first:
            opts = short_opts + long_opts
        else:
            opts = long_opts + short_opts
        return ', '.join(opts)
_装类转发(帮助格式化器, {'dedent': '减缩进', 'expand_default': '展开默认值', 'format_description': '格式化说明', 'format_epilog': '格式化结尾', 'format_heading': '格式化标题', 'format_option': '格式化选项', 'format_option_strings': '格式化选项字符串', 'format_usage': '格式化用法', 'indent': '增缩进', 'set_long_opt_delimiter': '设长选项分隔符', 'set_parser': '设解析器', 'set_short_opt_delimiter': '设短选项分隔符', 'store_option_strings': '存选项字符串'}, {'dedent': '减缩进', 'expand_default': '展开默认值', 'format_description': '格式化说明', 'format_epilog': '格式化结尾', 'format_heading': '格式化标题', 'format_option': '格式化选项', 'format_option_strings': '格式化选项字符串', 'format_usage': '格式化用法', 'indent': '增缩进', 'set_long_opt_delimiter': '设长选项分隔符', 'set_parser': '设解析器', 'set_short_opt_delimiter': '设短选项分隔符', 'store_option_strings': '存选项字符串'})

class 缩进帮助格式化器(帮助格式化器):
    """Format help with indented section bodies.
    """

    def __init__(self, indent_increment=2, max_help_position=24, width=None, short_first=1):
        帮助格式化器.__init__(self, indent_increment, max_help_position, width, short_first)

    def 格式化用法(self, usage):
        return _('Usage: %s\n') % usage

    def 格式化标题(self, heading):
        return '%*s%s:\n' % (self.current_indent, '', heading)
_装类转发(缩进帮助格式化器, {'format_heading': '格式化标题', 'format_usage': '格式化用法'}, {'format_heading': '格式化标题', 'format_usage': '格式化用法'})

class 标题帮助格式化器(帮助格式化器):
    """Format help with underlined section headers.
    """

    def __init__(self, indent_increment=0, max_help_position=24, width=None, short_first=0):
        帮助格式化器.__init__(self, indent_increment, max_help_position, width, short_first)

    def 格式化用法(self, usage):
        return '%s  %s\n' % (self.格式化标题(_('Usage')), usage)

    def 格式化标题(self, heading):
        return '%s\n%s\n' % (heading, '=-'[self.level] * len(heading))
_装类转发(标题帮助格式化器, {'format_heading': '格式化标题', 'format_usage': '格式化用法'}, {'format_heading': '格式化标题', 'format_usage': '格式化用法'})

def _parse_num(val, type):
    if val[:2].lower() == '0x':
        radix = 16
    elif val[:2].lower() == '0b':
        radix = 2
        val = val[2:] or '0'
    elif val[:1] == '0':
        radix = 8
    else:
        radix = 10
    return type(val, radix)

def _parse_int(val):
    return _parse_num(val, int)
_builtin_cvt = {'int': (_parse_int, _('integer')), 'long': (_parse_int, _('integer')), 'float': (float, _('floating-point')), 'complex': (complex, _('complex'))}

def 检查内置类型(option, opt, value):
    cvt, what = _builtin_cvt[option.type]
    try:
        return cvt(value)
    except ValueError:
        raise 选项值错误(_('option %s: invalid %s value: %r') % (opt, what, value))

def 检查候选项(option, opt, value):
    if value in option.choices:
        return value
    else:
        choices = ', '.join(map(repr, option.choices))
        raise 选项值错误(_('option %s: invalid choice: %r (choose from %s)') % (opt, value, choices))
无默认值 = ('NO', 'DEFAULT')

class 选项:
    """
    Instance attributes:
      _short_opts : [string]
      _long_opts : [string]

      action : string
      type : string
      dest : string
      default : any
      nargs : int
      const : any
      choices : [string]
      callback : function
      callback_args : (any*)
      callback_kwargs : { string : any }
      help : string
      metavar : string
    """
    ATTRS = ['action', 'type', 'dest', 'default', 'nargs', 'const', 'choices', 'callback', 'callback_args', 'callback_kwargs', 'help', 'metavar']
    ACTIONS = ('store', 'store_const', 'store_true', 'store_false', 'append', 'append_const', 'count', 'callback', 'help', 'version')
    STORE_ACTIONS = ('store', 'store_const', 'store_true', 'store_false', 'append', 'append_const', 'count')
    TYPED_ACTIONS = ('store', 'append', 'callback')
    ALWAYS_TYPED_ACTIONS = ('store', 'append')
    CONST_ACTIONS = ('store_const', 'append_const')
    TYPES = ('string', 'int', 'long', 'float', 'complex', 'choice')
    TYPE_CHECKER = {'int': 检查内置类型, 'long': 检查内置类型, 'float': 检查内置类型, 'complex': 检查内置类型, 'choice': 检查候选项}
    CHECK_METHODS = None

    def __init__(self, *opts, **attrs):
        self._short_opts = []
        self._long_opts = []
        opts = self._check_opt_strings(opts)
        self._set_opt_strings(opts)
        self._set_attrs(attrs)
        for checker in self.CHECK_METHODS:
            checker(self)

    def _check_opt_strings(self, opts):
        opts = [opt for opt in opts if opt]
        if not opts:
            raise TypeError('at least one option string must be supplied')
        return opts

    def _set_opt_strings(self, opts):
        for opt in opts:
            if len(opt) < 2:
                raise 选项错误('invalid option string %r: must be at least two characters long' % opt, self)
            elif len(opt) == 2:
                if not (opt[0] == '-' and opt[1] != '-'):
                    raise 选项错误('invalid short option string %r: must be of the form -x, (x any non-dash char)' % opt, self)
                self._short_opts.append(opt)
            else:
                if not (opt[0:2] == '--' and opt[2] != '-'):
                    raise 选项错误('invalid long option string %r: must start with --, followed by non-dash' % opt, self)
                self._long_opts.append(opt)

    def _set_attrs(self, attrs):
        for attr in self.ATTRS:
            if attr in attrs:
                setattr(self, attr, attrs[attr])
                del attrs[attr]
            elif attr == 'default':
                setattr(self, attr, 无默认值)
            else:
                setattr(self, attr, None)
        if attrs:
            attrs = sorted(attrs.keys())
            raise 选项错误('invalid keyword arguments: %s' % ', '.join(attrs), self)

    def _check_action(self):
        if self.action is None:
            self.action = 'store'
        elif self.action not in self.ACTIONS:
            raise 选项错误('invalid action: %r' % self.action, self)

    def _check_type(self):
        if self.type is None:
            if self.action in self.ALWAYS_TYPED_ACTIONS:
                if self.choices is not None:
                    self.type = 'choice'
                else:
                    self.type = 'string'
        else:
            if isinstance(self.type, type):
                self.type = self.type.__name__
            if self.type == 'str':
                self.type = 'string'
            if self.type not in self.TYPES:
                raise 选项错误('invalid option type: %r' % self.type, self)
            if self.action not in self.TYPED_ACTIONS:
                raise 选项错误('must not supply a type for action %r' % self.action, self)

    def _check_choice(self):
        if self.type == 'choice':
            if self.choices is None:
                raise 选项错误("must supply a list of choices for type 'choice'", self)
            elif not isinstance(self.choices, (tuple, list)):
                raise 选项错误("choices must be a list of strings ('%s' supplied)" % str(type(self.choices)).split("'")[1], self)
        elif self.choices is not None:
            raise 选项错误('must not supply choices for type %r' % self.type, self)

    def _check_dest(self):
        要取值吗 = self.action in self.STORE_ACTIONS or self.type is not None
        if self.dest is None and 要取值吗:
            if self._long_opts:
                self.dest = self._long_opts[0][2:].replace('-', '_')
            else:
                self.dest = self._short_opts[0][1]

    def _check_const(self):
        if self.action not in self.CONST_ACTIONS and self.const is not None:
            raise 选项错误("'const' must not be supplied for action %r" % self.action, self)

    def _check_nargs(self):
        if self.action in self.TYPED_ACTIONS:
            if self.nargs is None:
                self.nargs = 1
        elif self.nargs is not None:
            raise 选项错误("'nargs' must not be supplied for action %r" % self.action, self)

    def _check_callback(self):
        if self.action == 'callback':
            if not callable(self.callback):
                raise 选项错误('callback not callable: %r' % self.callback, self)
            if self.callback_args is not None and (not isinstance(self.callback_args, tuple)):
                raise 选项错误('callback_args, if supplied, must be a tuple: not %r' % self.callback_args, self)
            if self.callback_kwargs is not None and (not isinstance(self.callback_kwargs, dict)):
                raise 选项错误('callback_kwargs, if supplied, must be a dict: not %r' % self.callback_kwargs, self)
        else:
            if self.callback is not None:
                raise 选项错误('callback supplied (%r) for non-callback option' % self.callback, self)
            if self.callback_args is not None:
                raise 选项错误('callback_args supplied for non-callback option', self)
            if self.callback_kwargs is not None:
                raise 选项错误('callback_kwargs supplied for non-callback option', self)
    CHECK_METHODS = [_check_action, _check_type, _check_choice, _check_dest, _check_const, _check_nargs, _check_callback]

    def __str__(self):
        return '/'.join(self._short_opts + self._long_opts)
    __repr__ = _repr

    def 要取值吗(self):
        return self.type is not None

    def 取选项字符串(self):
        if self._long_opts:
            return self._long_opts[0]
        else:
            return self._short_opts[0]

    def 检查值(self, opt, value):
        checker = self.TYPE_CHECKER.get(self.type)
        if checker is None:
            return value
        else:
            return checker(self, opt, value)

    def 转换值(self, opt, value):
        if value is not None:
            if self.nargs == 1:
                return self.检查值(opt, value)
            else:
                return tuple([self.检查值(opt, v) for v in value])

    def 处理(self, opt, value, values, parser):
        value = self.转换值(opt, value)
        return self.take_action(self.action, self.dest, opt, value, values, parser)

    def take_action(self, action, dest, opt, value, values, parser):
        if action == 'store':
            setattr(values, dest, value)
        elif action == 'store_const':
            setattr(values, dest, self.const)
        elif action == 'store_true':
            setattr(values, dest, True)
        elif action == 'store_false':
            setattr(values, dest, False)
        elif action == 'append':
            values.ensure_value(dest, []).append(value)
        elif action == 'append_const':
            values.ensure_value(dest, []).append(self.const)
        elif action == 'count':
            setattr(values, dest, values.ensure_value(dest, 0) + 1)
        elif action == 'callback':
            args = self.callback_args or ()
            kwargs = self.callback_kwargs or {}
            self.callback(self, opt, value, parser, *args, **kwargs)
        elif action == 'help':
            parser.print_help()
            parser.exit()
        elif action == 'version':
            parser.print_version()
            parser.exit()
        else:
            raise ValueError('unknown action %r' % self.action)
        return 1
_装类转发(选项, {'check_value': '检查值', 'convert_value': '转换值', 'get_opt_string': '取选项字符串', 'process': '处理', 'takes_value': '要取值吗'}, {'check_value': '检查值', 'convert_value': '转换值', 'get_opt_string': '取选项字符串', 'process': '处理', 'takes_value': '要取值吗'})
隐藏帮助 = 'SUPPRESS' + 'HELP'
隐藏用法 = 'SUPPRESS' + 'USAGE'

class 值集合:

    def __init__(self, defaults=None):
        if defaults:
            for attr, val in defaults.items():
                setattr(self, attr, val)

    def __str__(self):
        return str(self.__dict__)
    __repr__ = _repr

    def __eq__(self, other):
        if isinstance(other, 值集合):
            return self.__dict__ == other.__dict__
        elif isinstance(other, dict):
            return self.__dict__ == other
        else:
            return NotImplemented

    def _update_careful(self, dict):
        """
        Update the option values from an arbitrary dictionary, but only
        use keys from dict that already have a corresponding attribute
        in self.  Any keys in dict without a corresponding attribute
        are silently ignored.
        """
        for attr in dir(self):
            if attr in dict:
                dval = dict[attr]
                if dval is not None:
                    setattr(self, attr, dval)

    def _update_loose(self, dict):
        """
        Update the option values from an arbitrary dictionary,
        using all keys from the dictionary regardless of whether
        they have a corresponding attribute in self or not.
        """
        self.__dict__.update(dict)

    def _update(self, dict, mode):
        if mode == 'careful':
            self._update_careful(dict)
        elif mode == 'loose':
            self._update_loose(dict)
        else:
            raise ValueError('invalid update mode: %r' % mode)

    def 读模块(self, modname, mode='careful'):
        __import__(modname)
        mod = sys.modules[modname]
        self._update(vars(mod), mode)

    def 读文件(self, filename, mode='careful'):
        vars = {}
        exec(open(filename).read(), vars)
        self._update(vars, mode)

    def 确保值(self, attr, value):
        if not hasattr(self, attr) or getattr(self, attr) is None:
            setattr(self, attr, value)
        return getattr(self, attr)
_装类转发(值集合, {'ensure_value': '确保值', 'read_file': '读文件', 'read_module': '读模块'}, {'ensure_value': '确保值', 'read_file': '读文件', 'read_module': '读模块'})

class 选项容器:
    """
    Abstract base class.

    Class attributes:
      standard_option_list : [Option]
        list of standard options that will be accepted by all instances
        of this parser class (intended to be overridden by subclasses).

    Instance attributes:
      option_list : [Option]
        the list of Option objects contained by this OptionContainer
      _short_opt : { string : Option }
        dictionary mapping short option strings, eg. "-f" or "-X",
        to the Option instances that implement them.  If an Option
        has multiple short option strings, it will appear in this
        dictionary multiple times. [1]
      _long_opt : { string : Option }
        dictionary mapping long option strings, eg. "--file" or
        "--exclude", to the Option instances that implement them.
        Again, a given Option can occur multiple times in this
        dictionary. [1]
      defaults : { string : any }
        dictionary mapping option destination names to default
        values for each destination [1]

    [1] These mappings are common to (shared by) all components of the
        controlling OptionParser, where they are initially created.

    """

    def __init__(self, option_class, conflict_handler, description):
        self._create_option_list()
        self.option_class = option_class
        self.设冲突处理(conflict_handler)
        self.设说明(description)

    def _create_option_mappings(self):
        self._short_opt = {}
        self._long_opt = {}
        self.defaults = {}

    def _share_option_mappings(self, parser):
        self._short_opt = parser._short_opt
        self._long_opt = parser._long_opt
        self.defaults = parser.defaults

    def 设冲突处理(self, handler):
        if handler not in ('error', 'resolve'):
            raise ValueError('invalid conflict_resolution value %r' % handler)
        self.conflict_handler = handler

    def 设说明(self, description):
        self.description = description

    def 取说明(self):
        return self.description

    def 销毁(self):
        """see OptionParser.destroy()."""
        del self._short_opt
        del self._long_opt
        del self.defaults

    def _check_conflict(self, option):
        conflict_opts = []
        for opt in option._short_opts:
            if opt in self._short_opt:
                conflict_opts.append((opt, self._short_opt[opt]))
        for opt in option._long_opts:
            if opt in self._long_opt:
                conflict_opts.append((opt, self._long_opt[opt]))
        if conflict_opts:
            handler = self.conflict_handler
            if handler == 'error':
                raise 选项冲突错误('conflicting option string(s): %s' % ', '.join([co[0] for co in conflict_opts]), option)
            elif handler == 'resolve':
                for opt, c_option in conflict_opts:
                    if opt.startswith('--'):
                        c_option._long_opts.remove(opt)
                        del self._long_opt[opt]
                    else:
                        c_option._short_opts.remove(opt)
                        del self._short_opt[opt]
                    if not (c_option._short_opts or c_option._long_opts):
                        c_option.container.option_list.remove(c_option)

    def 加选项(self, *args, **kwargs):
        """add_option(Option)
           add_option(opt_str, ..., kwarg=val, ...)
        """
        if isinstance(args[0], str):
            option = self.option_class(*args, **kwargs)
        elif len(args) == 1 and (not kwargs):
            option = args[0]
            if not isinstance(option, 选项):
                raise TypeError('not an Option instance: %r' % option)
        else:
            raise TypeError('invalid arguments')
        self._check_conflict(option)
        self.option_list.append(option)
        option.container = self
        for opt in option._short_opts:
            self._short_opt[opt] = option
        for opt in option._long_opts:
            self._long_opt[opt] = option
        if option.dest is not None:
            if option.default is not 无默认值:
                self.defaults[option.dest] = option.default
            elif option.dest not in self.defaults:
                self.defaults[option.dest] = None
        return option

    def 加选项们(self, option_list):
        for option in option_list:
            self.加选项(option)

    def 取选项(self, opt_str):
        return self._short_opt.get(opt_str) or self._long_opt.get(opt_str)

    def 有选项吗(self, opt_str):
        return opt_str in self._short_opt or opt_str in self._long_opt

    def 删选项(self, opt_str):
        option = self._short_opt.get(opt_str)
        if option is None:
            option = self._long_opt.get(opt_str)
        if option is None:
            raise ValueError('no such option %r' % opt_str)
        for opt in option._short_opts:
            del self._short_opt[opt]
        for opt in option._long_opts:
            del self._long_opt[opt]
        option.container.option_list.remove(option)

    def 格式化选项帮助(self, formatter):
        if not self.option_list:
            return ''
        result = []
        for option in self.option_list:
            if not option.help is 隐藏帮助:
                result.append(formatter.format_option(option))
        return ''.join(result)

    def 格式化说明(self, formatter):
        return formatter.format_description(self.取说明())

    def 格式化帮助(self, formatter):
        result = []
        if self.description:
            result.append(self.格式化说明(formatter))
        if self.option_list:
            result.append(self.格式化选项帮助(formatter))
        return '\n'.join(result)
_装类转发(选项容器, {'add_option': '加选项', 'add_options': '加选项们', 'destroy': '销毁', 'format_description': '格式化说明', 'format_help': '格式化帮助', 'format_option_help': '格式化选项帮助', 'get_description': '取说明', 'get_option': '取选项', 'has_option': '有选项吗', 'remove_option': '删选项', 'set_conflict_handler': '设冲突处理', 'set_description': '设说明'}, {'add_option': '加选项', 'add_options': '加选项们', 'destroy': '销毁', 'format_description': '格式化说明', 'format_help': '格式化帮助', 'format_option_help': '格式化选项帮助', 'get_description': '取说明', 'get_option': '取选项', 'has_option': '有选项吗', 'remove_option': '删选项', 'set_conflict_handler': '设冲突处理', 'set_description': '设说明'})

class 选项组(选项容器):

    def __init__(self, parser, title, description=None):
        self.parser = parser
        选项容器.__init__(self, parser.option_class, parser.conflict_handler, description)
        self.title = title

    def _create_option_list(self):
        self.option_list = []
        self._share_option_mappings(self.parser)

    def 设标题(self, title):
        self.title = title

    def 销毁(self):
        """see OptionParser.destroy()."""
        选项容器.销毁(self)
        del self.option_list

    def 格式化帮助(self, formatter):
        result = formatter.format_heading(self.title)
        formatter.indent()
        result += 选项容器.格式化帮助(self, formatter)
        formatter.dedent()
        return result
_装类转发(选项组, {'destroy': '销毁', 'format_help': '格式化帮助', 'set_title': '设标题'}, {'destroy': '销毁', 'format_help': '格式化帮助', 'set_title': '设标题'})

class 选项解析器(选项容器):
    """
    Class attributes:
      standard_option_list : [Option]
        list of standard options that will be accepted by all instances
        of this parser class (intended to be overridden by subclasses).

    Instance attributes:
      usage : string
        a usage string for your program.  Before it is displayed
        to the user, "%prog" will be expanded to the name of
        your program (self.prog or os.path.basename(sys.argv[0])).
      prog : string
        the name of the current program (to override
        os.path.basename(sys.argv[0])).
      description : string
        A paragraph of text giving a brief overview of your program.
        optparse reformats this paragraph to fit the current terminal
        width and prints it when the user requests help (after usage,
        but before the list of options).
      epilog : string
        paragraph of help text to print after option help

      option_groups : [OptionGroup]
        list of option groups in this parser (option groups are
        irrelevant for parsing the command-line, but very useful
        for generating help)

      allow_interspersed_args : bool = true
        if true, positional arguments may be interspersed with options.
        Assuming -a and -b each take a single argument, the command-line
          -ablah foo bar -bboo baz
        will be interpreted the same as
          -ablah -bboo -- foo bar baz
        If this flag were false, that command line would be interpreted as
          -ablah -- foo bar -bboo baz
        -- ie. we stop processing options as soon as we see the first
        non-option argument.  (This is the tradition followed by
        Python's getopt module, Perl's Getopt::Std, and other argument-
        parsing libraries, but it is generally annoying to users.)

      process_default_values : bool = true
        if true, option default values are processed similarly to option
        values from the command line: that is, they are passed to the
        type-checking function for the option's type (as long as the
        default value is a string).  (This really only matters if you
        have defined custom types; see SF bug #955889.)  Set it to false
        to restore the behaviour of Optik 1.4.1 and earlier.

      rargs : [string]
        the argument list currently being parsed.  Only set when
        parse_args() is active, and continually trimmed down as
        we consume arguments.  Mainly there for the benefit of
        callback options.
      largs : [string]
        the list of leftover arguments that we have skipped while
        parsing options.  If allow_interspersed_args is false, this
        list is always empty.
      values : Values
        the set of option values currently being accumulated.  Only
        set when parse_args() is active.  Also mainly for callbacks.

    Because of the 'rargs', 'largs', and 'values' attributes,
    OptionParser is not thread-safe.  If, for some perverse reason, you
    need to parse command-line arguments simultaneously in different
    threads, use different OptionParser instances.

    """
    standard_option_list = []

    def __init__(self, usage=None, option_list=None, option_class=选项, version=None, conflict_handler='error', description=None, formatter=None, add_help_option=True, prog=None, epilog=None):
        选项容器.__init__(self, option_class, conflict_handler, description)
        self.设用法(usage)
        self.prog = prog
        self.version = version
        self.allow_interspersed_args = True
        self.process_default_values = True
        if formatter is None:
            formatter = 缩进帮助格式化器()
        self.formatter = formatter
        self.formatter.set_parser(self)
        self.epilog = epilog
        self._populate_option_list(option_list, add_help=add_help_option)
        self._init_parsing_state()

    def 销毁(self):
        """
        Declare that you are done with this OptionParser.  This cleans up
        reference cycles so the OptionParser (and all objects referenced by
        it) can be garbage-collected promptly.  After calling destroy(), the
        OptionParser is unusable.
        """
        选项容器.销毁(self)
        for group in self.option_groups:
            group.destroy()
        del self.option_list
        del self.option_groups
        del self.formatter

    def _create_option_list(self):
        self.option_list = []
        self.option_groups = []
        self._create_option_mappings()

    def _add_help_option(self):
        self.加选项('-h', '--help', action='help', help=_('show this help message and exit'))

    def _add_version_option(self):
        self.加选项('--version', action='version', help=_("show program's version number and exit"))

    def _populate_option_list(self, option_list, add_help=True):
        if self.standard_option_list:
            self.加选项们(self.standard_option_list)
        if option_list:
            self.加选项们(option_list)
        if self.version:
            self._add_version_option()
        if add_help:
            self._add_help_option()

    def _init_parsing_state(self):
        self.rargs = None
        self.largs = None
        self.values = None

    def 设用法(self, usage):
        if usage is None:
            self.usage = _('%prog [options]')
        elif usage is 隐藏用法:
            self.usage = None
        elif usage.lower().startswith('usage: '):
            self.usage = usage[7:]
        else:
            self.usage = usage

    def 允许穿插参数(self):
        """Set parsing to not stop on the first non-option, allowing
        interspersing switches with command arguments. This is the
        default behavior. See also disable_interspersed_args() and the
        class documentation description of the attribute
        allow_interspersed_args."""
        self.allow_interspersed_args = True

    def 禁止穿插参数(self):
        """Set parsing to stop on the first non-option. Use this if
        you have a command processor which runs another command that
        has options of its own and you want to make sure these options
        don't get confused.
        """
        self.allow_interspersed_args = False

    def 设处理默认值(self, process):
        self.process_default_values = process

    def 设默认值(self, dest, value):
        self.defaults[dest] = value

    def 设默认值们(self, **kwargs):
        self.defaults.update(kwargs)

    def _get_all_options(self):
        options = self.option_list[:]
        for group in self.option_groups:
            options.extend(group.option_list)
        return options

    def 取默认值(self):
        if not self.process_default_values:
            return 值集合(self.defaults)
        defaults = self.defaults.copy()
        for option in self._get_all_options():
            default = defaults.get(option.dest)
            if isinstance(default, str):
                opt_str = option.get_opt_string()
                defaults[option.dest] = option.check_value(opt_str, default)
        return 值集合(defaults)

    def 加选项组(self, *args, **kwargs):
        if isinstance(args[0], str):
            group = 选项组(self, *args, **kwargs)
        elif len(args) == 1 and (not kwargs):
            group = args[0]
            if not isinstance(group, 选项组):
                raise TypeError('not an OptionGroup instance: %r' % group)
            if group.parser is not self:
                raise ValueError('invalid OptionGroup (wrong parser)')
        else:
            raise TypeError('invalid arguments')
        self.option_groups.append(group)
        return group

    def 取选项组(self, opt_str):
        option = self._short_opt.get(opt_str) or self._long_opt.get(opt_str)
        if option and option.container is not self:
            return option.container
        return None

    def _get_args(self, args):
        if args is None:
            return sys.argv[1:]
        else:
            return args[:]

    def 解析参数(self, args=None, values=None):
        """
        parse_args(args : [string] = sys.argv[1:],
                   values : Values = None)
        -> (values : Values, args : [string])

        Parse the command-line options found in 'args' (default:
        sys.argv[1:]).  Any errors result in a call to 'error()', which
        by default prints the usage message to stderr and calls
        sys.exit() with an error message.  On success returns a pair
        (values, args) where 'values' is a Values instance (with all
        your option values) and 'args' is the list of arguments left
        over after parsing options.
        """
        rargs = self._get_args(args)
        if values is None:
            values = self.取默认值()
        self.rargs = rargs
        self.largs = largs = []
        self.values = values
        try:
            stop = self._process_args(largs, rargs, values)
        except (坏选项错误, 选项值错误) as err:
            self.error(str(err))
        args = largs + rargs
        return self.检查值们(values, args)

    def 检查值们(self, values, args):
        """
        check_values(values : Values, args : [string])
        -> (values : Values, args : [string])

        Check that the supplied option values and leftover arguments are
        valid.  Returns the option values and leftover arguments
        (possibly adjusted, possibly completely new -- whatever you
        like).  Default implementation just returns the passed-in
        values; subclasses may override as desired.
        """
        return (values, args)

    def _process_args(self, largs, rargs, values):
        """_process_args(largs : [string],
                         rargs : [string],
                         values : Values)

        Process command-line arguments and populate 'values', consuming
        options and arguments from 'rargs'.  If 'allow_interspersed_args' is
        false, stop at the first non-option argument.  If true, accumulate any
        interspersed non-option arguments in 'largs'.
        """
        while rargs:
            arg = rargs[0]
            if arg == '--':
                del rargs[0]
                return
            elif arg[0:2] == '--':
                self._process_long_opt(rargs, values)
            elif arg[:1] == '-' and len(arg) > 1:
                self._process_short_opts(rargs, values)
            elif self.allow_interspersed_args:
                largs.append(arg)
                del rargs[0]
            else:
                return

    def _match_long_opt(self, opt):
        """_match_long_opt(opt : string) -> string

        Determine which long option string 'opt' matches, ie. which one
        it is an unambiguous abbreviation for.  Raises BadOptionError if
        'opt' doesn't unambiguously match any long option string.
        """
        return _match_abbrev(opt, self._long_opt)

    def _process_long_opt(self, rargs, values):
        arg = rargs.pop(0)
        if '=' in arg:
            opt, next_arg = arg.split('=', 1)
            rargs.insert(0, next_arg)
            had_explicit_value = True
        else:
            opt = arg
            had_explicit_value = False
        opt = self._match_long_opt(opt)
        option = self._long_opt[opt]
        if option.takes_value():
            nargs = option.nargs
            if len(rargs) < nargs:
                self.error(ngettext('%(option)s option requires %(number)d argument', '%(option)s option requires %(number)d arguments', nargs) % {'option': opt, 'number': nargs})
            elif nargs == 1:
                value = rargs.pop(0)
            else:
                value = tuple(rargs[0:nargs])
                del rargs[0:nargs]
        elif had_explicit_value:
            self.error(_('%s option does not take a value') % opt)
        else:
            value = None
        option.process(opt, value, values, self)

    def _process_short_opts(self, rargs, values):
        arg = rargs.pop(0)
        stop = False
        i = 1
        for ch in arg[1:]:
            opt = '-' + ch
            option = self._short_opt.get(opt)
            i += 1
            if not option:
                raise 坏选项错误(opt)
            if option.takes_value():
                if i < len(arg):
                    rargs.insert(0, arg[i:])
                    stop = True
                nargs = option.nargs
                if len(rargs) < nargs:
                    self.error(ngettext('%(option)s option requires %(number)d argument', '%(option)s option requires %(number)d arguments', nargs) % {'option': opt, 'number': nargs})
                elif nargs == 1:
                    value = rargs.pop(0)
                else:
                    value = tuple(rargs[0:nargs])
                    del rargs[0:nargs]
            else:
                value = None
            option.process(opt, value, values, self)
            if stop:
                break

    def 取程序名(self):
        if self.prog is None:
            return os.path.basename(sys.argv[0])
        else:
            return self.prog

    def 展开程序名(self, s):
        return s.replace('%prog', self.取程序名())

    def 取说明(self):
        return self.展开程序名(self.description)

    def exit(self, status=0, msg=None):
        if msg:
            sys.stderr.write(msg)
        sys.exit(status)

    def error(self, msg):
        """error(msg : string)

        Print a usage message incorporating 'msg' to stderr and exit.
        If you override this in a subclass, it should not return -- it
        should either exit or raise an exception.
        """
        if _zh可用():
            用法 = self.取用法()
            if 用法.startswith('Usage: '):
                用法 = '用法：' + 用法[len('Usage: '):]
            print(用法, file=sys.stderr)
            self.exit(2, '%s：错误：%s\n' % (self.取程序名(), _zh正文(msg)))
        else:
            self.打印用法(sys.stderr)
            self.exit(2, '%s: error: %s\n' % (self.取程序名(), msg))

    def 取用法(self):
        if self.usage:
            return self.formatter.format_usage(self.展开程序名(self.usage))
        else:
            return ''

    def 打印用法(self, file=None):
        """print_usage(file : file = stdout)

        Print the usage message for the current program (self.usage) to
        'file' (default stdout).  Any occurrence of the string "%prog" in
        self.usage is replaced with the name of the current program
        (basename of sys.argv[0]).  Does nothing if self.usage is empty
        or not defined.
        """
        if self.usage:
            print(self.取用法(), file=file)

    def 取版本(self):
        if self.version:
            return self.展开程序名(self.version)
        else:
            return ''

    def 打印版本(self, file=None):
        """print_version(file : file = stdout)

        Print the version message for this program (self.version) to
        'file' (default stdout).  As with print_usage(), any occurrence
        of "%prog" in self.version is replaced by the current program's
        name.  Does nothing if self.version is empty or undefined.
        """
        if self.version:
            print(self.取版本(), file=file)

    def 格式化选项帮助(self, formatter=None):
        if formatter is None:
            formatter = self.formatter
        formatter.store_option_strings(self)
        result = []
        result.append(formatter.format_heading(_('Options')))
        formatter.indent()
        if self.option_list:
            result.append(选项容器.格式化选项帮助(self, formatter))
            result.append('\n')
        for group in self.option_groups:
            result.append(group.format_help(formatter))
            result.append('\n')
        formatter.dedent()
        return ''.join(result[:-1])

    def 格式化结尾(self, formatter):
        return formatter.format_epilog(self.epilog)

    def 格式化帮助(self, formatter=None):
        if formatter is None:
            formatter = self.formatter
        result = []
        if self.usage:
            result.append(self.取用法() + '\n')
        if self.description:
            result.append(self.格式化说明(formatter) + '\n')
        result.append(self.格式化选项帮助(formatter))
        result.append(self.格式化结尾(formatter))
        return ''.join(result)

    def 打印帮助(self, file=None):
        """print_help(file : file = stdout)

        Print an extended help message, listing all options and any
        help text provided with them, to 'file' (default stdout).
        """
        if file is None:
            file = sys.stdout
        file.write(self.格式化帮助())
_装类转发(选项解析器, {'add_option_group': '加选项组', 'check_values': '检查值们', 'destroy': '销毁', 'disable_interspersed_args': '禁止穿插参数', 'enable_interspersed_args': '允许穿插参数', 'expand_prog_name': '展开程序名', 'format_epilog': '格式化结尾', 'format_help': '格式化帮助', 'format_option_help': '格式化选项帮助', 'get_default_values': '取默认值', 'get_description': '取说明', 'get_option_group': '取选项组', 'get_prog_name': '取程序名', 'get_usage': '取用法', 'get_version': '取版本', 'parse_args': '解析参数', 'print_help': '打印帮助', 'print_usage': '打印用法', 'print_version': '打印版本', 'set_default': '设默认值', 'set_defaults': '设默认值们', 'set_process_default_values': '设处理默认值', 'set_usage': '设用法'}, {'add_option': '加选项', 'add_option_group': '加选项组', 'add_options': '加选项们', 'check_values': '检查值们', 'destroy': '销毁', 'disable_interspersed_args': '禁止穿插参数', 'enable_interspersed_args': '允许穿插参数', 'expand_prog_name': '展开程序名', 'format_description': '格式化说明', 'format_epilog': '格式化结尾', 'format_help': '格式化帮助', 'format_option_help': '格式化选项帮助', 'get_default_values': '取默认值', 'get_description': '取说明', 'get_option_group': '取选项组', 'get_prog_name': '取程序名', 'get_usage': '取用法', 'get_version': '取版本', 'parse_args': '解析参数', 'print_help': '打印帮助', 'print_usage': '打印用法', 'print_version': '打印版本', 'set_default': '设默认值', 'set_defaults': '设默认值们', 'set_process_default_values': '设处理默认值', 'set_usage': '设用法'})

def _match_abbrev(s, wordmap):
    """_match_abbrev(s : string, wordmap : {string : Option}) -> string

    Return the string key in 'wordmap' for which 's' is an unambiguous
    abbreviation.  If 's' is found to be ambiguous or doesn't match any of
    'words', raise BadOptionError.
    """
    if s in wordmap:
        return s
    else:
        possibilities = [word for word in wordmap.keys() if word.startswith(s)]
        if len(possibilities) == 1:
            return possibilities[0]
        elif not possibilities:
            raise 坏选项错误(s)
        else:
            possibilities.sort()
            raise 选项歧义错误(s, possibilities)
造选项 = 选项


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'AmbiguousOptionError': '选项歧义错误',
    'BadOptionError': '坏选项错误',
    'HelpFormatter': '帮助格式化器',
    'IndentedHelpFormatter': '缩进帮助格式化器',
    'NO_DEFAULT': '无默认值',
    'OptParseError': '选项解析错误',
    'Option': '选项',
    'OptionConflictError': '选项冲突错误',
    'OptionContainer': '选项容器',
    'OptionError': '选项错误',
    'OptionGroup': '选项组',
    'OptionParser': '选项解析器',
    'OptionValueError': '选项值错误',
    'SUPPRESS_HELP': '隐藏帮助',
    'SUPPRESS_USAGE': '隐藏用法',
    'TitledHelpFormatter': '标题帮助格式化器',
    'Values': '值集合',
    'check_builtin': '检查内置类型',
    'check_choice': '检查候选项',
    'make_option': '造选项',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '值集合': {
        'ensure_value': '确保值',
        'read_file': '读文件',
        'read_module': '读模块',
    },
    '帮助格式化器': {
        'dedent': '减缩进',
        'expand_default': '展开默认值',
        'format_description': '格式化说明',
        'format_epilog': '格式化结尾',
        'format_heading': '格式化标题',
        'format_option': '格式化选项',
        'format_option_strings': '格式化选项字符串',
        'format_usage': '格式化用法',
        'indent': '增缩进',
        'set_long_opt_delimiter': '设长选项分隔符',
        'set_parser': '设解析器',
        'set_short_opt_delimiter': '设短选项分隔符',
        'store_option_strings': '存选项字符串',
    },
    '标题帮助格式化器': {
        'format_heading': '格式化标题',
        'format_usage': '格式化用法',
    },
    '缩进帮助格式化器': {
        'format_heading': '格式化标题',
        'format_usage': '格式化用法',
    },
    '选项': {
        'check_value': '检查值',
        'convert_value': '转换值',
        'get_opt_string': '取选项字符串',
        'process': '处理',
        'takes_value': '要取值吗',
    },
    '选项容器': {
        'add_option': '加选项',
        'add_options': '加选项们',
        'destroy': '销毁',
        'format_description': '格式化说明',
        'format_help': '格式化帮助',
        'format_option_help': '格式化选项帮助',
        'get_description': '取说明',
        'get_option': '取选项',
        'has_option': '有选项吗',
        'remove_option': '删选项',
        'set_conflict_handler': '设冲突处理',
        'set_description': '设说明',
    },
    '选项组': {
        'destroy': '销毁',
        'format_help': '格式化帮助',
        'set_title': '设标题',
    },
    '选项解析器': {
        'add_option_group': '加选项组',
        'check_values': '检查值们',
        'destroy': '销毁',
        'disable_interspersed_args': '禁止穿插参数',
        'enable_interspersed_args': '允许穿插参数',
        'expand_prog_name': '展开程序名',
        'format_epilog': '格式化结尾',
        'format_help': '格式化帮助',
        'format_option_help': '格式化选项帮助',
        'get_default_values': '取默认值',
        'get_description': '取说明',
        'get_option_group': '取选项组',
        'get_prog_name': '取程序名',
        'get_usage': '取用法',
        'get_version': '取版本',
        'parse_args': '解析参数',
        'print_help': '打印帮助',
        'print_usage': '打印用法',
        'print_version': '打印版本',
        'set_default': '设默认值',
        'set_defaults': '设默认值们',
        'set_process_default_values': '设处理默认值',
        'set_usage': '设用法',
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
    '值集合': {
        'ensure_value': '确保值',
        'read_file': '读文件',
        'read_module': '读模块',
    },
    '帮助格式化器': {
        'dedent': '减缩进',
        'expand_default': '展开默认值',
        'format_description': '格式化说明',
        'format_epilog': '格式化结尾',
        'format_heading': '格式化标题',
        'format_option': '格式化选项',
        'format_option_strings': '格式化选项字符串',
        'format_usage': '格式化用法',
        'indent': '增缩进',
        'set_long_opt_delimiter': '设长选项分隔符',
        'set_parser': '设解析器',
        'set_short_opt_delimiter': '设短选项分隔符',
        'store_option_strings': '存选项字符串',
    },
    '标题帮助格式化器': {
        'format_heading': '格式化标题',
        'format_usage': '格式化用法',
    },
    '缩进帮助格式化器': {
        'format_heading': '格式化标题',
        'format_usage': '格式化用法',
    },
    '选项': {
        'check_value': '检查值',
        'convert_value': '转换值',
        'get_opt_string': '取选项字符串',
        'process': '处理',
        'takes_value': '要取值吗',
    },
    '选项容器': {
        'add_option': '加选项',
        'add_options': '加选项们',
        'destroy': '销毁',
        'format_description': '格式化说明',
        'format_help': '格式化帮助',
        'format_option_help': '格式化选项帮助',
        'get_description': '取说明',
        'get_option': '取选项',
        'has_option': '有选项吗',
        'remove_option': '删选项',
        'set_conflict_handler': '设冲突处理',
        'set_description': '设说明',
    },
    '选项组': {
        'destroy': '销毁',
        'format_help': '格式化帮助',
        'set_title': '设标题',
    },
    '选项解析器': {
        'add_option': '加选项',
        'add_option_group': '加选项组',
        'add_options': '加选项们',
        'check_values': '检查值们',
        'destroy': '销毁',
        'disable_interspersed_args': '禁止穿插参数',
        'enable_interspersed_args': '允许穿插参数',
        'expand_prog_name': '展开程序名',
        'format_description': '格式化说明',
        'format_epilog': '格式化结尾',
        'format_help': '格式化帮助',
        'format_option_help': '格式化选项帮助',
        'get_default_values': '取默认值',
        'get_description': '取说明',
        'get_option_group': '取选项组',
        'get_prog_name': '取程序名',
        'get_usage': '取用法',
        'get_version': '取版本',
        'parse_args': '解析参数',
        'print_help': '打印帮助',
        'print_usage': '打印用法',
        'print_version': '打印版本',
        'set_default': '设默认值',
        'set_defaults': '设默认值们',
        'set_process_default_values': '设处理默认值',
        'set_usage': '设用法',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '值集合',
    '坏选项错误',
    '帮助格式化器',
    '标题帮助格式化器',
    '检查候选项',
    '缩进帮助格式化器',
    '选项',
    '选项值错误',
    '选项冲突错误',
    '选项容器',
    '选项组',
    '选项解析器',
    '选项解析错误',
    '选项错误',
    '造选项',
    '隐藏帮助',
    '隐藏用法',
]

# ---- 转发层结束 ----
