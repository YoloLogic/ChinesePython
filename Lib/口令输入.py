# -*- coding: utf-8 -*-
"""口令输入 —— 汉语库（由 tools/汉化库.py 从 Lib/getpass.py 机械生成，**不要手改**）。

英文库 Lib/getpass.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 口令输入
"""


"""Utilities to get a password and/or the current user name.

getpass(prompt[, stream[, echo_char]]) - Prompt for a password, with echo
turned off and optional keyboard feedback.
getuser() - Get the user name from the environment or password database.

GetPassWarning - This UserWarning is issued when getpass() cannot prevent
                 echoing of the password contents while reading.

On Windows, the msvcrt module will be used.

"""
_英文原名表 = {'GetPassWarning': '取口令警告', 'getpass': '取口令', 'getuser': '取用户名', 'unix_getpass': 'Unix取口令', 'win_getpass': 'Windows取口令'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import contextlib
import io
import os
import sys
__all__ = ['getpass', 'getuser', 'GetPassWarning']

class 取口令警告(UserWarning):
    pass
import getpass as _英文身份源
取口令警告 = _英文身份源.GetPassWarning

def Unix取口令(prompt='Password: ', stream=None, *, echo_char=None):
    """Prompt for a password, with echo turned off.

    Args:
      prompt: Written on stream to ask for the input.  Default: 'Password: '
      stream: A writable file object to display the prompt.  Defaults to
              the tty.  If no tty is available defaults to sys.stderr.
      echo_char: A single ASCII character to mask input (e.g., '*').
              If None, input is hidden.
    Returns:
      The seKr3t input.
    Raises:
      EOFError: If our input tty or stdin was closed.
      GetPassWarning: When we were unable to turn echo off on the input.

    Always restores terminal settings before returning.
    """
    _check_echo_char(echo_char)
    passwd = None
    with contextlib.ExitStack() as stack:
        try:
            fd = os.open('/dev/tty', os.O_RDWR | os.O_NOCTTY)
            tty = io.FileIO(fd, 'w+')
            stack.enter_context(tty)
            input = io.TextIOWrapper(tty)
            stack.enter_context(input)
            if not stream:
                stream = input
        except OSError:
            stack.close()
            try:
                fd = sys.stdin.fileno()
            except (AttributeError, ValueError):
                fd = None
                passwd = fallback_getpass(prompt, stream)
            input = sys.stdin
            if not stream:
                stream = sys.stderr
        if fd is not None:
            try:
                old = termios.tcgetattr(fd)
                new = old[:]
                new[3] &= ~termios.ECHO
                if echo_char:
                    new[3] &= ~termios.ICANON
                tcsetattr_flags = termios.TCSAFLUSH
                if hasattr(termios, 'TCSASOFT'):
                    tcsetattr_flags |= termios.TCSASOFT
                try:
                    termios.tcsetattr(fd, tcsetattr_flags, new)
                    passwd = _raw_input(prompt, stream, input=input, echo_char=echo_char)
                finally:
                    termios.tcsetattr(fd, tcsetattr_flags, old)
                    stream.flush()
            except termios.error:
                if passwd is not None:
                    raise
                if stream is not input:
                    stack.close()
                passwd = fallback_getpass(prompt, stream)
        stream.write('\n')
        return passwd

def Windows取口令(prompt='Password: ', stream=None, *, echo_char=None):
    """Prompt for password with echo off, using Windows getwch()."""
    if sys.stdin is not sys.__stdin__:
        return fallback_getpass(prompt, stream)
    _check_echo_char(echo_char)
    for c in prompt:
        msvcrt.putwch(c)
    pw = ''
    while 1:
        c = msvcrt.getwch()
        if c == '\r' or c == '\n':
            break
        if c == '\x03':
            raise KeyboardInterrupt
        if c == '\x08':
            if echo_char and pw:
                msvcrt.putwch('\x08')
                msvcrt.putwch(' ')
                msvcrt.putwch('\x08')
            pw = pw[:-1]
        else:
            pw = pw + c
            if echo_char:
                msvcrt.putwch(echo_char)
    msvcrt.putwch('\r')
    msvcrt.putwch('\n')
    return pw

def fallback_getpass(prompt='Password: ', stream=None, *, echo_char=None):
    _check_echo_char(echo_char)
    import warnings
    warnings.warn('Can not control echo on the terminal.', 取口令警告, stacklevel=2)
    if not stream:
        stream = sys.stderr
    print('Warning: Password input may be echoed.', file=stream)
    return _raw_input(prompt, stream, echo_char=echo_char)

def _check_echo_char(echo_char):
    if echo_char is None:
        return
    if not isinstance(echo_char, str):
        raise TypeError(f"'echo_char' must be a str or None, not {type(echo_char).__name__}")
    if not (len(echo_char) == 1 and echo_char.isprintable() and echo_char.isascii()):
        raise ValueError(f"'echo_char' must be a single printable ASCII character, got: {echo_char!r}")

def _raw_input(prompt='', stream=None, input=None, echo_char=None):
    if not stream:
        stream = sys.stderr
    if not input:
        input = sys.stdin
    prompt = str(prompt)
    if prompt:
        try:
            stream.write(prompt)
        except UnicodeEncodeError:
            prompt = prompt.encode(stream.encoding, 'replace')
            prompt = prompt.decode(stream.encoding)
            stream.write(prompt)
        stream.flush()
    if echo_char:
        return _readline_with_echo_char(stream, input, echo_char)
    line = input.readline()
    if not line:
        raise EOFError
    if line[-1] == '\n':
        line = line[:-1]
    return line

def _readline_with_echo_char(stream, input, echo_char):
    passwd = ''
    eof_pressed = False
    while True:
        char = input.read(1)
        if char == '\n' or char == '\r':
            break
        elif char == '\x03':
            raise KeyboardInterrupt
        elif char == '\x7f' or char == '\x08':
            if passwd:
                stream.write('\x08 \x08')
                stream.flush()
            passwd = passwd[:-1]
        elif char == '\x04':
            if eof_pressed:
                break
            else:
                eof_pressed = True
        elif char == '\x00':
            continue
        else:
            passwd += char
            stream.write(echo_char)
            stream.flush()
            eof_pressed = False
    return passwd

def 取用户名():
    """Get the username from the environment or password database.

    First try various environment variables, then the password
    database.  This works on Windows as long as USERNAME is set.
    Any failure to find a username raises OSError.

    .. versionchanged:: 3.13
        Previously, various exceptions beyond just :exc:`OSError`
        were raised.
    """
    for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
        user = os.environ.get(name)
        if user:
            return user
    try:
        import pwd
        return pwd.getpwuid(os.getuid())[0]
    except (ImportError, KeyError) as e:
        raise OSError('No username set in the environment') from e
try:
    import termios
    (termios.tcgetattr, termios.tcsetattr)
except (ImportError, AttributeError):
    try:
        import msvcrt
    except ImportError:
        取口令 = fallback_getpass
    else:
        取口令 = Windows取口令
else:
    取口令 = Unix取口令


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import getpass as _英文库
取口令警告 = _英文库.GetPassWarning
_模块别名 = {
    'GetPassWarning': '取口令警告',
    'getpass': '取口令',
    'getuser': '取用户名',
    'unix_getpass': 'Unix取口令',
    'win_getpass': 'Windows取口令',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '取口令',
    '取口令警告',
    '取用户名',
])

# ---- 转发层结束 ----
