# -*- coding: utf-8 -*-
"""文件输入 —— 汉语库（由 tools/汉化库.py 从 Lib/fileinput.py 机械生成，**不要手改**）。

英文库 Lib/fileinput.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 文件输入
"""


"""Helper class to quickly write a loop over all standard input files.

Typical use is:

    import fileinput
    for line in fileinput.input(encoding="utf-8"):
        process(line)

This iterates over the lines of all files listed in sys.argv[1:],
defaulting to sys.stdin if the list is empty.  If a filename is '-' it
is also replaced by sys.stdin and the optional arguments mode and
openhook are ignored.  To specify an alternative list of filenames,
pass it as the argument to input().  A single file name is also allowed.

Functions filename(), lineno() return the filename and cumulative line
number of the line that has just been read; filelineno() returns its
line number in the current file; isfirstline() returns true iff the
line just read is the first line of its file; isstdin() returns true
iff the line was read from sys.stdin.  Function nextfile() closes the
current file so that the next iteration will read the first line from
the next file (if any); lines not read from the file will not count
towards the cumulative line count; the filename is not changed until
after the first line of the next file has been read.  Function close()
closes the sequence.

Before any lines have been read, filename() returns None and both line
numbers are zero; nextfile() has no effect.  After all lines have been
read, filename() and the line number functions return the values
pertaining to the last line read; nextfile() has no effect.

All files are opened in text mode by default, you can override this by
setting the mode parameter to input() or FileInput.__init__().
If an I/O error occurs during opening or reading a file, the OSError
exception is raised.

If sys.stdin is used more than once, the second and further use will
return no lines, except perhaps for interactive use, or if it has been
explicitly reset (e.g. using sys.stdin.seek(0)).

Empty files are opened and immediately closed; the only time their
presence in the list of filenames is noticeable at all is when the
last file opened is empty.

It is possible that the last line of a file doesn't end in a newline
character; otherwise lines are returned including the trailing
newline.

Class FileInput is the implementation; its methods filename(),
lineno(), fileline(), isfirstline(), isstdin(), nextfile() and close()
correspond to the functions in the module.  In addition it has a
readline() method which returns the next input line, and a
__getitem__() method which implements the sequence behavior.  The
sequence must be accessed in strictly sequential order; sequence
access and readline() cannot be mixed.

Optional in-place filtering: if the keyword argument inplace=True is
passed to input() or to the FileInput constructor, the file is moved
to a backup file and standard output is directed to the input file.
This makes it possible to write a filter that rewrites its input file
in place.  If the keyword argument backup=".<some extension>" is also
given, it specifies the extension for the backup file, and the backup
file remains around; by default, the extension is ".bak" and it is
deleted when the output file is closed.  In-place filtering is
disabled when standard input is read.  XXX The current implementation
does not work for MS-DOS 8+3 filesystems.
"""
_英文原名表 = {'filelineno': '本文件行号', 'filename': '文件名', 'hook_compressed': '压缩钩子', 'hook_encoded': '编码钩子', 'isfirstline': '是第一行吗', 'isstdin': '是标准输入吗', 'lineno': '当前行号', 'nextfile': '下一个文件'}

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
import io
import sys, os
from types import GenericAlias
__all__ = ['input', 'close', 'nextfile', 'filename', 'lineno', 'filelineno', 'fileno', 'isfirstline', 'isstdin', 'FileInput', 'hook_compressed', 'hook_encoded']
_state = None

def input(files=None, inplace=False, backup='', *, mode='r', openhook=None, encoding=None, errors=None):
    """Return an instance of the FileInput class, which can be iterated.

    The parameters are passed to the constructor of the FileInput class.
    The returned instance, in addition to being an iterator,
    keeps global state for the functions of this module,.
    """
    global _state
    if _state and _state._file:
        raise RuntimeError('input() already active')
    _state = FileInput(files, inplace, backup, mode=mode, openhook=openhook, encoding=encoding, errors=errors)
    return _state

def close():
    """Close the sequence."""
    global _state
    state = _state
    _state = None
    if state:
        state.close()

def 下一个文件():
    """
    Close the current file so that the next iteration will read the first
    line from the next file (if any); lines not read from the file will
    not count towards the cumulative line count. The filename is not
    changed until after the first line of the next file has been read.
    Before the first line has been read, this function has no effect;
    it cannot be used to skip the first file. After the last line of the
    last file has been read, this function has no effect.
    """
    if not _state:
        raise RuntimeError('no active input()')
    return _state.nextfile()

def 文件名():
    """
    Return the name of the file currently being read.
    Before the first line has been read, returns None.
    """
    if not _state:
        raise RuntimeError('no active input()')
    return _state.filename()

def 当前行号():
    """
    Return the cumulative line number of the line that has just been read.
    Before the first line has been read, returns 0. After the last line
    of the last file has been read, returns the line number of that line.
    """
    if not _state:
        raise RuntimeError('no active input()')
    return _state.lineno()

def 本文件行号():
    """
    Return the line number in the current file. Before the first line
    has been read, returns 0. After the last line of the last file has
    been read, returns the line number of that line within the file.
    """
    if not _state:
        raise RuntimeError('no active input()')
    return _state.filelineno()

def fileno():
    """
    Return the file number of the current file. When no file is currently
    opened, returns -1.
    """
    if not _state:
        raise RuntimeError('no active input()')
    return _state.fileno()

def 是第一行吗():
    """
    Returns true the line just read is the first line of its file,
    otherwise returns false.
    """
    if not _state:
        raise RuntimeError('no active input()')
    return _state.isfirstline()

def 是标准输入吗():
    """
    Returns true if the last line was read from sys.stdin,
    otherwise returns false.
    """
    if not _state:
        raise RuntimeError('no active input()')
    return _state.isstdin()

class FileInput:
    """FileInput([files[, inplace[, backup]]], *, mode=None, openhook=None)

    Class FileInput is the implementation of the module; its methods
    filename(), lineno(), fileline(), isfirstline(), isstdin(), fileno(),
    nextfile() and close() correspond to the functions of the same name
    in the module.
    In addition it has a readline() method which returns the next
    input line, and a __getitem__() method which implements the
    sequence behavior. The sequence must be accessed in strictly
    sequential order; random access and readline() cannot be mixed.
    """

    def __init__(self, files=None, inplace=False, backup='', *, mode='r', openhook=None, encoding=None, errors=None):
        if isinstance(files, str):
            files = (files,)
        elif isinstance(files, os.PathLike):
            files = (os.fspath(files),)
        else:
            if files is None:
                files = sys.argv[1:]
            if not files:
                files = ('-',)
            else:
                files = tuple(files)
        self._files = files
        self._inplace = inplace
        self._backup = backup
        self._savestdout = None
        self._output = None
        self._filename = None
        self._startlineno = 0
        self._filelineno = 0
        self._file = None
        self._isstdin = False
        self._backupfilename = None
        self._encoding = encoding
        self._errors = errors
        if sys.flags.warn_default_encoding and 'b' not in mode and (encoding is None) and (openhook is None):
            import warnings
            warnings.warn("'encoding' argument not specified.", EncodingWarning, 2)
        if mode not in ('r', 'rb'):
            raise ValueError("FileInput opening mode must be 'r' or 'rb'")
        self._mode = mode
        self._write_mode = mode.replace('r', 'w')
        if openhook:
            if inplace:
                raise ValueError('FileInput cannot use an opening hook in inplace mode')
            if not callable(openhook):
                raise ValueError('FileInput openhook must be callable')
        self._openhook = openhook

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.下一个文件()
        finally:
            self._files = ()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            line = self._readline()
            if line:
                self._filelineno += 1
                return line
            if not self._file:
                raise StopIteration
            self.下一个文件()

    def 下一个文件(self):
        savestdout = self._savestdout
        self._savestdout = None
        if savestdout:
            sys.stdout = savestdout
        output = self._output
        self._output = None
        try:
            if output:
                output.close()
        finally:
            file = self._file
            self._file = None
            try:
                del self._readline
            except AttributeError:
                pass
            try:
                if file and (not self._isstdin):
                    file.close()
            finally:
                backupfilename = self._backupfilename
                self._backupfilename = None
                if backupfilename and (not self._backup):
                    try:
                        os.unlink(backupfilename)
                    except OSError:
                        pass
                self._isstdin = False

    def readline(self):
        while True:
            line = self._readline()
            if line:
                self._filelineno += 1
                return line
            if not self._file:
                return line
            self.下一个文件()

    def _readline(self):
        if not self._files:
            if 'b' in self._mode:
                return b''
            else:
                return ''
        self._filename = self._files[0]
        self._files = self._files[1:]
        self._startlineno = self.当前行号()
        self._filelineno = 0
        self._file = None
        self._isstdin = False
        self._backupfilename = 0
        if 'b' not in self._mode:
            encoding = self._encoding or 'locale'
        else:
            encoding = None
        if self._filename == '-':
            self._filename = '<stdin>'
            if 'b' in self._mode:
                self._file = getattr(sys.stdin, 'buffer', sys.stdin)
            else:
                self._file = sys.stdin
            self._isstdin = True
        elif self._inplace:
            self._backupfilename = os.fspath(self._filename) + (self._backup or '.bak')
            try:
                os.unlink(self._backupfilename)
            except OSError:
                pass
            os.rename(self._filename, self._backupfilename)
            self._file = open(self._backupfilename, self._mode, encoding=encoding, errors=self._errors)
            try:
                perm = os.fstat(self._file.fileno()).st_mode
            except OSError:
                self._output = open(self._filename, self._write_mode, encoding=encoding, errors=self._errors)
            else:
                mode = os.O_CREAT | os.O_WRONLY | os.O_TRUNC
                if hasattr(os, 'O_BINARY'):
                    mode |= os.O_BINARY
                fd = os.open(self._filename, mode, perm)
                self._output = os.fdopen(fd, self._write_mode, encoding=encoding, errors=self._errors)
                try:
                    os.chmod(self._filename, perm)
                except OSError:
                    pass
            self._savestdout = sys.stdout
            sys.stdout = self._output
        elif self._openhook:
            if self._encoding is None:
                self._file = self._openhook(self._filename, self._mode)
            else:
                self._file = self._openhook(self._filename, self._mode, encoding=self._encoding, errors=self._errors)
        else:
            self._file = open(self._filename, self._mode, encoding=encoding, errors=self._errors)
        self._readline = self._file.readline
        return self._readline()

    def 文件名(self):
        return self._filename

    def 当前行号(self):
        return self._startlineno + self._filelineno

    def 本文件行号(self):
        return self._filelineno

    def fileno(self):
        if self._file:
            try:
                return self._file.fileno()
            except ValueError:
                return -1
        else:
            return -1

    def 是第一行吗(self):
        return self._filelineno == 1

    def 是标准输入吗(self):
        return self._isstdin
    __class_getitem__ = classmethod(GenericAlias)
_装类转发(FileInput, {'filelineno': '本文件行号', 'filename': '文件名', 'isfirstline': '是第一行吗', 'isstdin': '是标准输入吗', 'lineno': '当前行号', 'nextfile': '下一个文件'}, {'filelineno': '本文件行号', 'filename': '文件名', 'isfirstline': '是第一行吗', 'isstdin': '是标准输入吗', 'lineno': '当前行号', 'nextfile': '下一个文件'})

def 压缩钩子(filename, mode, *, encoding=None, errors=None):
    if encoding is None and 'b' not in mode:
        encoding = 'locale'
    ext = os.path.splitext(filename)[1]
    if ext == '.gz':
        import gzip
        stream = gzip.open(filename, mode)
    elif ext == '.bz2':
        import bz2
        stream = bz2.BZ2File(filename, mode)
    else:
        return open(filename, mode, encoding=encoding, errors=errors)
    if 'b' not in mode:
        stream = io.TextIOWrapper(stream, encoding=encoding, errors=errors)
    return stream

def 编码钩子(encoding, errors=None):

    def openhook(filename, mode):
        return open(filename, mode, encoding=encoding, errors=errors)
    return openhook

def _test():
    import getopt
    inplace = False
    backup = False
    opts, args = getopt.getopt(sys.argv[1:], 'ib:')
    for o, a in opts:
        if o == '-i':
            inplace = True
        if o == '-b':
            backup = a
    for line in input(args, inplace=inplace, backup=backup):
        if line[-1:] == '\n':
            line = line[:-1]
        if line[-1:] == '\r':
            line = line[:-1]
        print('%d: %s[%d]%s %s' % (当前行号(), 文件名(), 本文件行号(), 是第一行吗() and '*' or '', line))
    print('%d: %s[%d]' % (当前行号(), 文件名(), 本文件行号()))
if __name__ == '__main__':
    _test()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 本模块别名：词表里有、但规则不让改定义的名字（内置名最典型，比如 `open`）
_本模块别名 = {
    '读入': 'input',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'filelineno': '本文件行号',
    'filename': '文件名',
    'hook_compressed': '压缩钩子',
    'hook_encoded': '编码钩子',
    'isfirstline': '是第一行吗',
    'isstdin': '是标准输入吗',
    'lineno': '当前行号',
    'nextfile': '下一个文件',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'FileInput': {
        'filelineno': '本文件行号',
        'filename': '文件名',
        'isfirstline': '是第一行吗',
        'isstdin': '是标准输入吗',
        'lineno': '当前行号',
        'nextfile': '下一个文件',
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
    'FileInput': {
        'filelineno': '本文件行号',
        'filename': '文件名',
        'isfirstline': '是第一行吗',
        'isstdin': '是标准输入吗',
        'lineno': '当前行号',
        'nextfile': '下一个文件',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '下一个文件',
    '压缩钩子',
    '当前行号',
    '文件名',
    '是标准输入吗',
    '是第一行吗',
    '本文件行号',
    '编码钩子',
    '读入',
])

# ---- 转发层结束 ----
