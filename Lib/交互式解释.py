# -*- coding: utf-8 -*-
"""交互式解释 —— 汉语库（由 tools/汉化库.py 从 Lib/code.py 机械生成，**不要手改**）。

英文库 Lib/code.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 交互式解释
"""


"""Utilities needed to emulate Python's interactive interpreter.

"""
_英文原名表 = {'InteractiveConsole': '交互控制台', 'InteractiveInterpreter': '交互解释器', 'Quitter': '退出器', 'interact': '交互'}

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
import builtins
import sys
import traceback
from codeop import CommandCompiler, compile_command
__all__ = ['InteractiveInterpreter', 'InteractiveConsole', 'interact', 'compile_command']

class 交互解释器:
    """Base class for InteractiveConsole.

    This class deals with parsing and interpreter state (the user's
    namespace); it doesn't deal with input buffering or prompting or
    input file naming (the filename is always passed in explicitly).

    """

    def __init__(self, locals=None):
        """Constructor.

        The optional 'locals' argument specifies a mapping to use as the
        namespace in which code will be executed; it defaults to a newly
        created dictionary with key "__name__" set to "__console__" and
        key "__doc__" set to None.

        """
        if locals is None:
            locals = {'__name__': '__console__', '__doc__': None}
        self.locals = locals
        self.compile = CommandCompiler()

    def 运行源码(self, source, filename='<input>', symbol='single'):
        """Compile and run some source in the interpreter.

        Arguments are as for compile_command().

        One of several things can happen:

        1) The input is incorrect; compile_command() raised an
        exception (SyntaxError or OverflowError).  A syntax traceback
        will be printed by calling the showsyntaxerror() method.

        2) The input is incomplete, and more input is required;
        compile_command() returned None.  Nothing happens.

        3) The input is complete; compile_command() returned a code
        object.  The code is executed by calling self.runcode() (which
        also handles run-time exceptions, except for SystemExit).

        The return value is True in case 2, False in the other cases (unless
        an exception is raised).  The return value can be used to
        decide whether to use sys.ps1 or sys.ps2 to prompt the next
        line.

        """
        try:
            code = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            self.显示语法错误(filename, source=source)
            return False
        if code is None:
            return True
        self.运行代码对象(code)
        return False

    def 运行代码对象(self, code):
        """Execute a code object.

        When an exception occurs, self.showtraceback() is called to
        display a traceback.  All exceptions are caught except
        SystemExit, which is reraised.

        A note about KeyboardInterrupt: this exception may occur
        elsewhere in this code, and may not always be caught.  The
        caller should be prepared to deal with it.

        """
        try:
            exec(code, self.locals)
        except SystemExit:
            raise
        except:
            self.显示回溯()

    def 显示语法错误(self, filename=None, **kwargs):
        """Display the syntax error that just occurred.

        This doesn't display a stack trace because there isn't one.

        If a filename is given, it is stuffed in the exception instead
        of what was there before (because Python's parser always uses
        "<string>" when reading from a string).

        The output is written by self.write(), below.

        """
        try:
            typ, value, tb = sys.exc_info()
            if filename and issubclass(typ, SyntaxError):
                value.filename = filename
            source = kwargs.pop('source', '')
            self._showtraceback(typ, value, None, source)
        finally:
            typ = value = tb = None

    def 显示回溯(self):
        """Display the exception that just occurred.

        We remove the first stack item because it is our own code.

        The output is written by self.write(), below.

        """
        try:
            typ, value, tb = sys.exc_info()
            self._showtraceback(typ, value, tb.tb_next, '')
        finally:
            typ = value = tb = None

    def _showtraceback(self, typ, value, tb, source):
        sys.last_type = typ
        sys.last_traceback = tb
        value = value.with_traceback(tb)
        lines = source.splitlines()
        if source and typ is SyntaxError and (not value.text) and (value.lineno is not None) and (len(lines) >= value.lineno):
            value.text = lines[value.lineno - 1]
        sys.last_exc = sys.last_value = value
        if sys.excepthook is sys.__excepthook__:
            self._excepthook(typ, value, tb)
        else:
            try:
                sys.excepthook(typ, value, tb)
            except SystemExit:
                raise
            except BaseException as e:
                e.__context__ = None
                e = e.with_traceback(e.__traceback__.tb_next)
                print('Error in sys.excepthook:', file=sys.stderr)
                sys.__excepthook__(type(e), e, e.__traceback__)
                print(file=sys.stderr)
                print('Original exception was:', file=sys.stderr)
                sys.__excepthook__(typ, value, tb)

    def _excepthook(self, typ, value, tb):
        lines = traceback.format_exception(typ, value, tb)
        self.write(''.join(lines))

    def write(self, data):
        """Write a string.

        The base implementation writes to sys.stderr; a subclass may
        replace this with a different implementation.

        """
        sys.stderr.write(data)
_装类转发(交互解释器, {'runcode': '运行代码对象', 'runsource': '运行源码', 'showsyntaxerror': '显示语法错误', 'showtraceback': '显示回溯'}, {'runcode': '运行代码对象', 'runsource': '运行源码', 'showsyntaxerror': '显示语法错误', 'showtraceback': '显示回溯'})

class 交互控制台(交互解释器):
    """Closely emulate the behavior of the interactive Python interpreter.

    This class builds on InteractiveInterpreter and adds prompting
    using the familiar sys.ps1 and sys.ps2, and input buffering.

    """

    def __init__(self, locals=None, filename='<console>', *, local_exit=False):
        """Constructor.

        The optional locals argument will be passed to the
        InteractiveInterpreter base class.

        The optional filename argument should specify the (file)name
        of the input stream; it will show up in tracebacks.

        """
        交互解释器.__init__(self, locals)
        self.filename = filename
        self.local_exit = local_exit
        self.清缓冲()

    def 清缓冲(self):
        """Reset the input buffer."""
        self.buffer = []

    def 交互(self, banner=None, exitmsg=None):
        """Closely emulate the interactive Python console.

        The optional banner argument specifies the banner to print
        before the first interaction; by default it prints a banner
        similar to the one printed by the real Python interpreter,
        followed by the current class name in parentheses (so as not
        to confuse this with the real interpreter -- since it's so
        close!).

        The optional exitmsg argument specifies the exit message
        printed when exiting. Pass the empty string to suppress
        printing an exit message. If exitmsg is not given or None,
        a default message is printed.

        """
        try:
            sys.ps1
            delete_ps1_after = False
        except AttributeError:
            sys.ps1 = '>>> '
            delete_ps1_after = True
        try:
            _ps2 = sys.ps2
            delete_ps2_after = False
        except AttributeError:
            sys.ps2 = '... '
            delete_ps2_after = True
        cprt = 'Type "help", "copyright", "credits" or "license" for more information.'
        if banner is None:
            self.write('Python %s on %s\n%s\n(%s)\n' % (sys.version, sys.platform, cprt, self.__class__.__name__))
        elif banner:
            self.write('%s\n' % str(banner))
        more = 0
        _exit = None
        _quit = None
        if self.local_exit:
            if hasattr(builtins, 'exit'):
                _exit = builtins.exit
                builtins.exit = 退出器('exit')
            if hasattr(builtins, 'quit'):
                _quit = builtins.quit
                builtins.quit = 退出器('quit')
        try:
            while True:
                try:
                    if more:
                        prompt = sys.ps2
                    else:
                        prompt = sys.ps1
                    try:
                        line = self.原生输入(prompt)
                    except EOFError:
                        self.write('\n')
                        break
                    else:
                        more = self.压入(line)
                except KeyboardInterrupt:
                    self.write('\nKeyboardInterrupt\n')
                    self.清缓冲()
                    more = 0
                except SystemExit as e:
                    if self.local_exit:
                        self.write('\n')
                        break
                    else:
                        raise e
        finally:
            if _exit is not None:
                builtins.exit = _exit
            if _quit is not None:
                builtins.quit = _quit
            if delete_ps1_after:
                del sys.ps1
            if delete_ps2_after:
                del sys.ps2
            if exitmsg is None:
                self.write('now exiting %s...\n' % self.__class__.__name__)
            elif exitmsg != '':
                self.write('%s\n' % exitmsg)

    def 压入(self, line, filename=None, _symbol='single'):
        """Push a line to the interpreter.

        The line should not have a trailing newline; it may have
        internal newlines.  The line is appended to a buffer and the
        interpreter's runsource() method is called with the
        concatenated contents of the buffer as source.  If this
        indicates that the command was executed or invalid, the buffer
        is reset; otherwise, the command is incomplete, and the buffer
        is left as it was after the line was appended.  The return
        value is 1 if more input is required, 0 if the line was dealt
        with in some way (this is the same as runsource()).

        """
        self.buffer.append(line)
        source = '\n'.join(self.buffer)
        if filename is None:
            filename = self.filename
        more = self.运行源码(source, filename, symbol=_symbol)
        if not more:
            self.清缓冲()
        return more

    def 原生输入(self, prompt=''):
        """Write a prompt and read a line.

        The returned line does not include the trailing newline.
        When the user enters the EOF key sequence, EOFError is raised.

        The base implementation uses the built-in function
        input(); a subclass may replace this with a different
        implementation.

        """
        return input(prompt)
_装类转发(交互控制台, {'interact': '交互', 'push': '压入', 'raw_input': '原生输入', 'resetbuffer': '清缓冲'}, {'interact': '交互', 'push': '压入', 'raw_input': '原生输入', 'resetbuffer': '清缓冲', 'runsource': '运行源码'})

class 退出器:

    def __init__(self, name):
        self.name = name
        if sys.platform == 'win32':
            self.eof = 'Ctrl-Z plus Return'
        else:
            self.eof = 'Ctrl-D (i.e. EOF)'

    def __repr__(self):
        return f'Use {self.name} or {self.eof} to exit'

    def __call__(self, code=None):
        raise SystemExit(code)

def 交互(banner=None, readfunc=None, local=None, exitmsg=None, local_exit=False):
    """Closely emulate the interactive Python interpreter.

    This is a backwards compatible interface to the InteractiveConsole
    class.  When readfunc is not specified, it attempts to import the
    readline module to enable GNU readline if it is available.

    Arguments (all optional, all default to None):

    banner -- passed to InteractiveConsole.interact()
    readfunc -- if not None, replaces InteractiveConsole.raw_input()
    local -- passed to InteractiveInterpreter.__init__()
    exitmsg -- passed to InteractiveConsole.interact()
    local_exit -- passed to InteractiveConsole.__init__()

    """
    console = 交互控制台(local, local_exit=local_exit)
    if readfunc is not None:
        console.raw_input = readfunc
    else:
        try:
            import readline
        except ImportError:
            pass
    console.interact(banner, exitmsg)
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(color=True)
    parser.add_argument('-q', action='store_true', help="don't print version and copyright messages")
    args = parser.parse_args()
    if args.q or sys.flags.quiet:
        banner = ''
    else:
        banner = None
    交互(banner)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'InteractiveConsole': '交互控制台',
    'InteractiveInterpreter': '交互解释器',
    'Quitter': '退出器',
    'interact': '交互',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '交互控制台': {
        'interact': '交互',
        'push': '压入',
        'raw_input': '原生输入',
        'resetbuffer': '清缓冲',
    },
    '交互解释器': {
        'runcode': '运行代码对象',
        'runsource': '运行源码',
        'showsyntaxerror': '显示语法错误',
        'showtraceback': '显示回溯',
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
    '交互控制台': {
        'interact': '交互',
        'push': '压入',
        'raw_input': '原生输入',
        'resetbuffer': '清缓冲',
        'runsource': '运行源码',
    },
    '交互解释器': {
        'runcode': '运行代码对象',
        'runsource': '运行源码',
        'showsyntaxerror': '显示语法错误',
        'showtraceback': '显示回溯',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '交互',
    '交互控制台',
    '交互解释器',
]

# ---- 转发层结束 ----
