# -*- coding: utf-8 -*-
"""制表符检查 —— 汉语库（由 tools/汉化库.py 从 Lib/tabnanny.py 机械生成，**不要手改**）。

英文库 Lib/tabnanny.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 制表符检查
"""


"""The Tab Nanny despises ambiguous indentation.  She knows no mercy.

tabnanny -- Detection of ambiguous indentation

For the time being this module is intended to be called as a script.
However it is possible to import it into an IDE and use the function
check() described below.

Warning: The API provided by this module is likely to change in future
releases; such changes may not be backward compatible.
"""
_英文原名表 = {'Whitespace': '空白串', 'check': '检查', 'errprint': '错误打印', 'filename_only': '只报文件名', 'format_witnesses': '格式化见证', 'main': '主函数', 'process_tokens': '处理词法单元'}

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
__version__ = '6'
import os
import sys
import tokenize
__all__ = ['check', 'NannyNag', 'process_tokens']
verbose = 0
只报文件名 = 0

def 错误打印(*args):
    sep = ''
    for arg in args:
        sys.stderr.write(sep + str(arg))
        sep = ' '
    sys.stderr.write('\n')
    sys.exit(1)

def 主函数():
    import getopt
    global verbose, 只报文件名
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'qv')
    except getopt.error as msg:
        错误打印(msg)
    for o, a in opts:
        if o == '-q':
            只报文件名 = 只报文件名 + 1
        if o == '-v':
            verbose = verbose + 1
    if not args:
        错误打印('Usage:', sys.argv[0], '[-v] file_or_directory ...')
    for arg in args:
        检查(arg)

class NannyNag(Exception):
    """
    Raised by process_tokens() if detecting an ambiguous indent.
    Captured and handled in check().
    """

    def __init__(self, lineno, msg, line):
        self.lineno, self.msg, self.line = (lineno, msg, line)

    def 取行号(self):
        return self.lineno

    def 取消息(self):
        return self.msg

    def 取行(self):
        return self.line
_装类转发(NannyNag, {'get_line': '取行', 'get_lineno': '取行号', 'get_msg': '取消息'}, {'get_line': '取行', 'get_lineno': '取行号', 'get_msg': '取消息'})

def 检查(file):
    """check(file_or_dir)

    If file_or_dir is a directory and not a symbolic link, then recursively
    descend the directory tree named by file_or_dir, checking all .py files
    along the way. If file_or_dir is an ordinary Python source file, it is
    checked for whitespace related problems. The diagnostic messages are
    written to standard output using the print statement.
    """
    if os.path.isdir(file) and (not os.path.islink(file)):
        if verbose:
            print('%r: listing directory' % (file,))
        names = os.listdir(file)
        for name in names:
            fullname = os.path.join(file, name)
            if os.path.isdir(fullname) and (not os.path.islink(fullname)) or os.path.normcase(name[-3:]) == '.py':
                检查(fullname)
        return
    try:
        f = tokenize.open(file)
    except OSError as msg:
        错误打印('%r: I/O Error: %s' % (file, msg))
        return
    if verbose > 1:
        print('checking %r ...' % file)
    try:
        处理词法单元(tokenize.generate_tokens(f.readline))
    except tokenize.TokenError as msg:
        错误打印('%r: Token Error: %s' % (file, msg))
        return
    except IndentationError as msg:
        错误打印('%r: Indentation Error: %s' % (file, msg))
        return
    except SyntaxError as msg:
        错误打印('%r: Syntax Error: %s' % (file, msg))
        return
    except NannyNag as nag:
        badline = nag.get_lineno()
        line = nag.get_line()
        if verbose:
            print('%r: *** Line %d: trouble in tab city! ***' % (file, badline))
            print('offending line: %r' % (line,))
            print(nag.get_msg())
        else:
            if ' ' in file:
                file = '"' + file + '"'
            if 只报文件名:
                print(file)
            else:
                print(file, badline, repr(line))
        return
    finally:
        f.close()
    if verbose:
        print('%r: Clean bill of health.' % (file,))

class 空白串:
    S, T = ' \t'

    def __init__(self, ws):
        self.raw = ws
        S, T = (空白串.S, 空白串.T)
        count = []
        b = n = nt = 0
        for ch in self.raw:
            if ch == S:
                n = n + 1
                b = b + 1
            elif ch == T:
                n = n + 1
                nt = nt + 1
                if b >= len(count):
                    count = count + [0] * (b - len(count) + 1)
                count[b] = count[b] + 1
                b = 0
            else:
                break
        self.n = n
        self.nt = nt
        self.norm = (tuple(count), b)
        self.is_simple = len(count) <= 1

    def 最长连续空格(self):
        count, trailing = self.norm
        return max(len(count) - 1, trailing)

    def 缩进层级(self, tabsize):
        count, trailing = self.norm
        il = 0
        for i in range(tabsize, len(count)):
            il = il + i // tabsize * count[i]
        return trailing + tabsize * (il + self.nt)

    def 相等吗(self, other):
        return self.norm == other.norm

    def 不相等见证(self, other):
        n = max(self.最长连续空格(), other.longest_run_of_spaces()) + 1
        a = []
        for ts in range(1, n + 1):
            if self.缩进层级(ts) != other.indent_level(ts):
                a.append((ts, self.缩进层级(ts), other.indent_level(ts)))
        return a

    def 小于吗(self, other):
        if self.n >= other.n:
            return False
        if self.is_simple and other.is_simple:
            return self.nt <= other.nt
        n = max(self.最长连续空格(), other.longest_run_of_spaces()) + 1
        for ts in range(2, n + 1):
            if self.缩进层级(ts) >= other.indent_level(ts):
                return False
        return True

    def 不小于见证(self, other):
        n = max(self.最长连续空格(), other.longest_run_of_spaces()) + 1
        a = []
        for ts in range(1, n + 1):
            if self.缩进层级(ts) >= other.indent_level(ts):
                a.append((ts, self.缩进层级(ts), other.indent_level(ts)))
        return a
_装类转发(空白串, {'equal': '相等吗', 'indent_level': '缩进层级', 'less': '小于吗', 'longest_run_of_spaces': '最长连续空格', 'not_equal_witness': '不相等见证', 'not_less_witness': '不小于见证'}, {'equal': '相等吗', 'indent_level': '缩进层级', 'less': '小于吗', 'longest_run_of_spaces': '最长连续空格', 'not_equal_witness': '不相等见证', 'not_less_witness': '不小于见证'})

def 格式化见证(w):
    firsts = (str(tup[0]) for tup in w)
    prefix = 'at tab size'
    if len(w) > 1:
        prefix = prefix + 's'
    return prefix + ' ' + ', '.join(firsts)

def 处理词法单元(tokens):
    try:
        _process_tokens(tokens)
    except TabError as e:
        raise NannyNag(e.lineno, e.msg, e.text)

def _process_tokens(tokens):
    INDENT = tokenize.INDENT
    DEDENT = tokenize.DEDENT
    NEWLINE = tokenize.NEWLINE
    JUNK = (tokenize.COMMENT, tokenize.NL)
    indents = [空白串('')]
    check_equal = 0
    for type, token, start, end, line in tokens:
        if type == NEWLINE:
            check_equal = 1
        elif type == INDENT:
            check_equal = 0
            thisguy = 空白串(token)
            if not indents[-1].less(thisguy):
                witness = indents[-1].not_less_witness(thisguy)
                msg = 'indent not greater e.g. ' + 格式化见证(witness)
                raise NannyNag(start[0], msg, line)
            indents.append(thisguy)
        elif type == DEDENT:
            check_equal = 1
            del indents[-1]
        elif check_equal and type not in JUNK:
            check_equal = 0
            thisguy = 空白串(line)
            if not indents[-1].equal(thisguy):
                witness = indents[-1].not_equal_witness(thisguy)
                msg = 'indent not equal e.g. ' + 格式化见证(witness)
                raise NannyNag(start[0], msg, line)
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
    'Whitespace': '空白串',
    'check': '检查',
    'errprint': '错误打印',
    'filename_only': '只报文件名',
    'format_witnesses': '格式化见证',
    'main': '主函数',
    'process_tokens': '处理词法单元',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'NannyNag': {
        'get_line': '取行',
        'get_lineno': '取行号',
        'get_msg': '取消息',
    },
    '空白串': {
        'equal': '相等吗',
        'indent_level': '缩进层级',
        'less': '小于吗',
        'longest_run_of_spaces': '最长连续空格',
        'not_equal_witness': '不相等见证',
        'not_less_witness': '不小于见证',
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
    'NannyNag': {
        'get_line': '取行',
        'get_lineno': '取行号',
        'get_msg': '取消息',
    },
    '空白串': {
        'equal': '相等吗',
        'indent_level': '缩进层级',
        'less': '小于吗',
        'longest_run_of_spaces': '最长连续空格',
        'not_equal_witness': '不相等见证',
        'not_less_witness': '不小于见证',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '处理词法单元',
    '检查',
]

# ---- 转发层结束 ----
