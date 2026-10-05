# -*- coding: utf-8 -*-
"""词法切分 —— 汉语库（由 tools/汉化库.py 从 Lib/shlex.py 机械生成，**不要手改**）。

英文库 Lib/shlex.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 词法切分
"""


"""A lexical analyzer class for simple shell-like syntaxes."""
_英文原名表 = {'join': '拼接', 'quote': '加引号', 'shlex': '词法切分器', 'split': '切分'}

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
from io import StringIO
__all__ = ['shlex', 'split', 'quote', 'join']

class 词法切分器:
    """A lexical analyzer class for simple shell-like syntaxes."""

    def __init__(self, instream=None, infile=None, posix=False, punctuation_chars=False):
        from collections import deque
        if isinstance(instream, str):
            instream = StringIO(instream)
        if instream is not None:
            self.instream = instream
            self.infile = infile
        else:
            self.instream = sys.stdin
            self.infile = None
        self.posix = posix
        if posix:
            self.到末尾 = None
        else:
            self.到末尾 = ''
        self.注释符 = '#'
        self.词字符 = 'abcdfeghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
        if self.posix:
            self.词字符 += 'ßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ'
        self.whitespace = ' \t\r\n'
        self.按空白切分 = False
        self.quotes = '\'"'
        self.escape = '\\'
        self.可转义引号 = '"'
        self.state = ' '
        self.pushback = deque()
        self.行号 = 1
        self.debug = 0
        self.当前记号 = ''
        self.filestack = deque()
        self.source = None
        if not punctuation_chars:
            punctuation_chars = ''
        elif punctuation_chars is True:
            punctuation_chars = '();<>|&'
        self._punctuation_chars = punctuation_chars
        if punctuation_chars:
            self._pushback_chars = deque()
            self.词字符 += '~-./*?='
            t = self.词字符.maketrans(dict.fromkeys(punctuation_chars))
            self.词字符 = self.词字符.translate(t)

    @property
    def 标点字符(self):
        return self._punctuation_chars

    def 压回记号(self, tok):
        """Push a token onto the stack popped by the get_token method"""
        if self.debug >= 1:
            print('shlex: pushing token ' + repr(tok))
        self.pushback.appendleft(tok)

    def 压入来源(self, newstream, newfile=None):
        """Push an input source onto the lexer's input source stack."""
        if isinstance(newstream, str):
            newstream = StringIO(newstream)
        self.filestack.appendleft((self.infile, self.instream, self.行号))
        self.infile = newfile
        self.instream = newstream
        self.行号 = 1
        if self.debug:
            if newfile is not None:
                print('shlex: pushing to file %s' % (self.infile,))
            else:
                print('shlex: pushing to stream %s' % (self.instream,))

    def 弹出来源(self):
        """Pop the input source stack."""
        self.instream.close()
        self.infile, self.instream, self.行号 = self.filestack.popleft()
        if self.debug:
            print('shlex: popping to %s, line %d' % (self.instream, self.行号))
        self.state = ' '

    def 取记号(self):
        """Get a token from the input stream (or from stack if it's nonempty)"""
        if self.pushback:
            tok = self.pushback.popleft()
            if self.debug >= 1:
                print('shlex: popping token ' + repr(tok))
            return tok
        raw = self.读记号()
        if self.source is not None:
            while raw == self.source:
                spec = self.来源钩子(self.读记号())
                if spec:
                    newfile, newstream = spec
                    self.压入来源(newstream, newfile)
                raw = self.取记号()
        while raw == self.到末尾:
            if not self.filestack:
                return self.到末尾
            else:
                self.弹出来源()
                raw = self.取记号()
        if self.debug >= 1:
            if raw != self.到末尾:
                print('shlex: token=' + repr(raw))
            else:
                print('shlex: token=EOF')
        return raw

    def 读记号(self):
        quoted = False
        escapedstate = ' '
        while True:
            if self.标点字符 and self._pushback_chars:
                nextchar = self._pushback_chars.pop()
            else:
                nextchar = self.instream.read(1)
            if nextchar == '\n':
                self.行号 += 1
            if self.debug >= 3:
                print('shlex: in state %r I see character: %r' % (self.state, nextchar))
            if self.state is None:
                self.当前记号 = ''
                break
            elif self.state == ' ':
                if not nextchar:
                    self.state = None
                    break
                elif nextchar in self.whitespace:
                    if self.debug >= 2:
                        print('shlex: I see whitespace in whitespace state')
                    if self.当前记号 or (self.posix and quoted):
                        break
                    else:
                        continue
                elif nextchar in self.注释符:
                    self.instream.readline()
                    self.行号 += 1
                elif self.posix and nextchar in self.escape:
                    escapedstate = 'a'
                    self.state = nextchar
                elif nextchar in self.词字符:
                    self.当前记号 = nextchar
                    self.state = 'a'
                elif nextchar in self.标点字符:
                    self.当前记号 = nextchar
                    self.state = 'c'
                elif nextchar in self.quotes:
                    if not self.posix:
                        self.当前记号 = nextchar
                    self.state = nextchar
                elif self.按空白切分:
                    self.当前记号 = nextchar
                    self.state = 'a'
                else:
                    self.当前记号 = nextchar
                    if self.当前记号 or (self.posix and quoted):
                        break
                    else:
                        continue
            elif self.state in self.quotes:
                quoted = True
                if not nextchar:
                    if self.debug >= 2:
                        print('shlex: I see EOF in quotes state')
                    raise ValueError('No closing quotation')
                if nextchar == self.state:
                    if not self.posix:
                        self.当前记号 += nextchar
                        self.state = ' '
                        break
                    else:
                        self.state = 'a'
                elif self.posix and nextchar in self.escape and (self.state in self.可转义引号):
                    escapedstate = self.state
                    self.state = nextchar
                else:
                    self.当前记号 += nextchar
            elif self.state in self.escape:
                if not nextchar:
                    if self.debug >= 2:
                        print('shlex: I see EOF in escape state')
                    raise ValueError('No escaped character')
                if escapedstate in self.quotes and nextchar != self.state and (nextchar != escapedstate):
                    self.当前记号 += self.state
                self.当前记号 += nextchar
                self.state = escapedstate
            elif self.state in ('a', 'c'):
                if not nextchar:
                    self.state = None
                    break
                elif nextchar in self.whitespace:
                    if self.debug >= 2:
                        print('shlex: I see whitespace in word state')
                    self.state = ' '
                    if self.当前记号 or (self.posix and quoted):
                        break
                    else:
                        continue
                elif nextchar in self.注释符:
                    self.instream.readline()
                    self.行号 += 1
                    if self.posix:
                        self.state = ' '
                        if self.当前记号 or (self.posix and quoted):
                            break
                        else:
                            continue
                elif self.state == 'c':
                    if nextchar in self.标点字符:
                        self.当前记号 += nextchar
                    else:
                        if nextchar not in self.whitespace:
                            self._pushback_chars.append(nextchar)
                        self.state = ' '
                        break
                elif self.posix and nextchar in self.quotes:
                    self.state = nextchar
                elif self.posix and nextchar in self.escape:
                    escapedstate = 'a'
                    self.state = nextchar
                elif nextchar in self.词字符 or nextchar in self.quotes or (self.按空白切分 and nextchar not in self.标点字符):
                    self.当前记号 += nextchar
                else:
                    if self.标点字符:
                        self._pushback_chars.append(nextchar)
                    else:
                        self.pushback.appendleft(nextchar)
                    if self.debug >= 2:
                        print('shlex: I see punctuation in word state')
                    self.state = ' '
                    if self.当前记号 or (self.posix and quoted):
                        break
                    else:
                        continue
        result = self.当前记号
        self.当前记号 = ''
        if self.posix and (not quoted) and (result == ''):
            result = None
        if self.debug > 1:
            if result:
                print('shlex: raw token=' + repr(result))
            else:
                print('shlex: raw token=EOF')
        return result

    def 来源钩子(self, newfile):
        """Hook called on a filename to be sourced."""
        import os.path
        if newfile[0] == '"':
            newfile = newfile[1:-1]
        if isinstance(self.infile, str) and (not os.path.isabs(newfile)):
            newfile = os.path.join(os.path.dirname(self.infile), newfile)
        return (newfile, open(newfile, 'r'))

    def error_leader(self, infile=None, lineno=None):
        """Emit a C-compiler-like, Emacs-friendly error-message leader."""
        if infile is None:
            infile = self.infile
        if lineno is None:
            lineno = self.行号
        return '"%s", line %d: ' % (infile, lineno)

    def __iter__(self):
        return self

    def __next__(self):
        当前记号 = self.取记号()
        if 当前记号 == self.到末尾:
            raise StopIteration
        return 当前记号
_装类转发(词法切分器, {'get_token': '取记号', 'pop_source': '弹出来源', 'punctuation_chars': '标点字符', 'push_source': '压入来源', 'push_token': '压回记号', 'read_token': '读记号', 'sourcehook': '来源钩子'}, {'commenters': '注释符', 'eof': '到末尾', 'escapedquotes': '可转义引号', 'get_token': '取记号', 'lineno': '行号', 'pop_source': '弹出来源', 'punctuation_chars': '标点字符', 'push_source': '压入来源', 'push_token': '压回记号', 'read_token': '读记号', 'sourcehook': '来源钩子', 'token': '当前记号', 'whitespace_split': '按空白切分', 'wordchars': '词字符'})

def 切分(s, comments=False, posix=True):
    """Split the string *s* using shell-like syntax."""
    if s is None:
        raise ValueError('s argument must not be None')
    lex = 词法切分器(s, posix=posix)
    lex.whitespace_split = True
    if not comments:
        lex.commenters = ''
    return list(lex)

def 拼接(split_command):
    """Return a shell-escaped string from *split_command*."""
    return ' '.join((加引号(arg) for arg in split_command))

def 加引号(s):
    """Return a shell-escaped version of the string *s*."""
    if not s:
        return "''"
    if not isinstance(s, str):
        raise TypeError(f'expected string object, got {type(s).__name__!r}')
    safe_chars = b'%+,-./0123456789:=@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz'
    if s.isascii() and (not s.encode().translate(None, delete=safe_chars)):
        return s
    return "'" + s.replace("'", '\'"\'"\'') + "'"

def _print_tokens(lexer):
    while (tt := lexer.get_token()):
        print('Token: ' + repr(tt))
if __name__ == '__main__':
    if len(sys.argv) == 1:
        _print_tokens(词法切分器())
    else:
        fn = sys.argv[1]
        with open(fn) as f:
            _print_tokens(词法切分器(f, fn))


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'join': '拼接',
    'quote': '加引号',
    'shlex': '词法切分器',
    'split': '切分',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '词法切分器': {
        'get_token': '取记号',
        'pop_source': '弹出来源',
        'punctuation_chars': '标点字符',
        'push_source': '压入来源',
        'push_token': '压回记号',
        'read_token': '读记号',
        'sourcehook': '来源钩子',
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
    '词法切分器': {
        'commenters': '注释符',
        'eof': '到末尾',
        'escapedquotes': '可转义引号',
        'get_token': '取记号',
        'lineno': '行号',
        'pop_source': '弹出来源',
        'punctuation_chars': '标点字符',
        'push_source': '压入来源',
        'push_token': '压回记号',
        'read_token': '读记号',
        'sourcehook': '来源钩子',
        'token': '当前记号',
        'whitespace_split': '按空白切分',
        'wordchars': '词字符',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '切分',
    '加引号',
    '拼接',
    '词法切分器',
])

# ---- 转发层结束 ----
