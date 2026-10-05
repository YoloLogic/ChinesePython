# -*- coding: utf-8 -*-
"""文本折行 —— 汉语库（由 tools/汉化库.py 从 Lib/textwrap.py 机械生成，**不要手改**）。

英文库 Lib/textwrap.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 文本折行
"""


"""Text wrapping and filling.
"""
_英文原名表 = {'TextWrapper': '文本折行器', 'dedent': '去缩进', 'fill': '填充', 'indent': '加缩进', 'shorten': '缩短', 'wrap': '折行'}

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
import re
__all__ = ['TextWrapper', 'wrap', 'fill', 'dedent', 'indent', 'shorten']
_whitespace = '\t\n\x0b\x0c\r '

class 文本折行器:
    """
    Object for wrapping/filling text.  The public interface consists of
    the wrap() and fill() methods; the other methods are just there for
    subclasses to override in order to tweak the default behaviour.
    If you want to completely replace the main wrapping algorithm,
    you'll probably have to override _wrap_chunks().

    Several instance attributes control various aspects of wrapping:
      width (default: 70)
        the maximum width of wrapped lines (unless break_long_words
        is false)
      initial_indent (default: "")
        string that will be prepended to the first line of wrapped
        output.  Counts towards the line's width.
      subsequent_indent (default: "")
        string that will be prepended to all lines save the first
        of wrapped output; also counts towards each line's width.
      expand_tabs (default: true)
        Expand tabs in input text to spaces before further processing.
        Each tab will become 0 .. 'tabsize' spaces, depending on its position
        in its line.  If false, each tab is treated as a single character.
      tabsize (default: 8)
        Expand tabs in input text to 0 .. 'tabsize' spaces, unless
        'expand_tabs' is false.
      replace_whitespace (default: true)
        Replace all whitespace characters in the input text by spaces
        after tab expansion.  Note that if expand_tabs is false and
        replace_whitespace is true, every tab will be converted to a
        single space!
      fix_sentence_endings (default: false)
        Ensure that sentence-ending punctuation is always followed
        by two spaces.  Off by default because the algorithm is
        (unavoidably) imperfect.
      break_long_words (default: true)
        Break words longer than 'width'.  If false, those words will not
        be broken, and some lines might be longer than 'width'.
      break_on_hyphens (default: true)
        Allow breaking hyphenated words. If true, wrapping will occur
        preferably on whitespaces and right after hyphens part of
        compound words.
      drop_whitespace (default: true)
        Drop leading and trailing whitespace from lines.
      max_lines (default: None)
        Truncate wrapped lines.
      placeholder (default: ' [...]')
        Append to the last line of truncated text.
    """
    统一空白表 = dict.fromkeys(map(ord, _whitespace), ord(' '))
    词标点 = '[\\w!"\\\'&.,?]'
    字母 = '[^\\d\\W]'
    空白 = '[%s]' % re.escape(_whitespace)
    去空白 = '[^' + 空白[1:]
    词分隔正则 = re.compile('\n        ( # any whitespace\n          %(ws)s+\n        | # em-dash between words\n          (?<=%(wp)s) -{2,} (?=\\w)\n        | # word, possibly hyphenated\n          %(nws)s+? (?:\n            # hyphenated word\n              -(?: (?<=%(lt)s{2}-) | (?<=%(lt)s-%(lt)s-))\n              (?= %(lt)s -? %(lt)s)\n            | # end of word\n              (?=%(ws)s|\\z)\n            | # em-dash\n              (?<=%(wp)s) (?=-{2,}\\w)\n            )\n        )' % {'wp': 词标点, 'lt': 字母, 'ws': 空白, 'nws': 去空白}, re.VERBOSE)
    del 词标点, 字母, 去空白
    简单词分隔正则 = re.compile('(%s+)' % 空白)
    del 空白
    句末正则 = re.compile('[a-z][\\.\\!\\?][\\"\\\']?\\z')

    def __init__(self, width=70, initial_indent='', subsequent_indent='', expand_tabs=True, replace_whitespace=True, fix_sentence_endings=False, break_long_words=True, drop_whitespace=True, break_on_hyphens=True, tabsize=8, *, max_lines=None, placeholder=' [...]'):
        self.宽度 = width
        self.首行缩进 = initial_indent
        self.后续缩进 = subsequent_indent
        self.展开制表符 = expand_tabs
        self.替换空白 = replace_whitespace
        self.修句末 = fix_sentence_endings
        self.断长词 = break_long_words
        self.丢空白 = drop_whitespace
        self.按连字符断 = break_on_hyphens
        self.制表符宽度 = tabsize
        self.最多行数 = max_lines
        self.省略号 = placeholder

    def _munge_whitespace(self, text):
        """_munge_whitespace(text : string) -> string

        Munge whitespace in text: expand tabs and convert all other
        whitespace characters to spaces.  Eg. " foo\\tbar\\n\\nbaz"
        becomes " foo    bar  baz".
        """
        if self.展开制表符:
            text = text.expandtabs(self.制表符宽度)
        if self.替换空白:
            text = text.translate(self.统一空白表)
        return text

    def _split(self, text):
        """_split(text : string) -> [string]

        Split the text to wrap into indivisible chunks.  Chunks are
        not quite the same as words; see _wrap_chunks() for full
        details.  As an example, the text
          Look, goof-ball -- use the -b option!
        breaks into the following chunks:
          'Look,', ' ', 'goof-', 'ball', ' ', '--', ' ',
          'use', ' ', 'the', ' ', '-b', ' ', 'option!'
        if break_on_hyphens is True, or in:
          'Look,', ' ', 'goof-ball', ' ', '--', ' ',
          'use', ' ', 'the', ' ', '-b', ' ', option!'
        otherwise.
        """
        if self.按连字符断 is True:
            块 = self.词分隔正则.split(text)
        else:
            块 = self.简单词分隔正则.split(text)
        块 = [c for c in 块 if c]
        return 块

    def _fix_sentence_endings(self, chunks):
        """_fix_sentence_endings(chunks : [string])

        Correct for sentence endings buried in 'chunks'.  Eg. when the
        original text contains "... foo.\\nBar ...", munge_whitespace()
        and split() will convert that to [..., "foo.", " ", "Bar", ...]
        which has one too few spaces; this method simply changes the one
        space to two.
        """
        i = 0
        找匹配 = self.句末正则.search
        while i < len(chunks) - 1:
            if chunks[i + 1] == ' ' and 找匹配(chunks[i]):
                chunks[i + 1] = '  '
                i += 2
            else:
                i += 1

    def _handle_long_word(self, reversed_chunks, cur_line, cur_len, width):
        """_handle_long_word(chunks : [string],
                             cur_line : [string],
                             cur_len : int, width : int)

        Handle a chunk of text (most likely a word, not whitespace) that
        is too long to fit in any line.
        """
        if width < 1:
            剩余空间 = 1
        else:
            剩余空间 = width - cur_len
        if self.断长词 and 剩余空间 > 0:
            末尾 = 剩余空间
            一块 = reversed_chunks[-1]
            if self.按连字符断 and len(一块) > 剩余空间:
                连字符 = 一块.rfind('-', 0, 剩余空间)
                if 连字符 > 0 and any((c != '-' for c in 一块[:连字符])):
                    末尾 = 连字符 + 1
            cur_line.append(一块[:末尾])
            reversed_chunks[-1] = 一块[末尾:]
        elif not cur_line:
            cur_line.append(reversed_chunks.pop())

    def _wrap_chunks(self, chunks):
        """_wrap_chunks(chunks : [string]) -> [string]

        Wrap a sequence of text chunks and return a list of lines of
        length 'self.width' or less.  (If 'break_long_words' is false,
        some lines may be longer than this.)  Chunks correspond roughly
        to words and the whitespace between them: each chunk is
        indivisible (modulo 'break_long_words'), but a line break can
        come between any two chunks.  Chunks should not have internal
        whitespace; ie. a chunk is either all whitespace or a "word".
        Whitespace chunks will be removed from the beginning and end of
        lines, but apart from that whitespace is preserved.
        """
        行表 = []
        if self.宽度 <= 0:
            raise ValueError('invalid width %r (must be > 0)' % self.宽度)
        if self.最多行数 is not None:
            if self.最多行数 > 1:
                加缩进 = self.后续缩进
            else:
                加缩进 = self.首行缩进
            if len(加缩进) + len(self.省略号.lstrip()) > self.宽度:
                raise ValueError('placeholder too large for max width')
        chunks.reverse()
        while chunks:
            当前行 = []
            当前长 = 0
            if 行表:
                加缩进 = self.后续缩进
            else:
                加缩进 = self.首行缩进
            宽度 = self.宽度 - len(加缩进)
            if self.丢空白 and chunks[-1].strip() == '' and 行表:
                del chunks[-1]
            while chunks:
                l = len(chunks[-1])
                if 当前长 + l <= 宽度:
                    当前行.append(chunks.pop())
                    当前长 += l
                else:
                    break
            if chunks and len(chunks[-1]) > 宽度:
                self._handle_long_word(chunks, 当前行, 当前长, 宽度)
                当前长 = sum(map(len, 当前行))
            if self.丢空白 and 当前行 and (当前行[-1].strip() == ''):
                当前长 -= len(当前行[-1])
                del 当前行[-1]
            if 当前行:
                if self.最多行数 is None or len(行表) + 1 < self.最多行数 or ((not chunks or (self.丢空白 and len(chunks) == 1 and (not chunks[0].strip()))) and 当前长 <= 宽度):
                    行表.append(加缩进 + ''.join(当前行))
                else:
                    while 当前行:
                        if 当前行[-1].strip() and 当前长 + len(self.省略号) <= 宽度:
                            当前行.append(self.省略号)
                            行表.append(加缩进 + ''.join(当前行))
                            break
                        当前长 -= len(当前行[-1])
                        del 当前行[-1]
                    else:
                        if 行表:
                            上一行 = 行表[-1].rstrip()
                            if len(上一行) + len(self.省略号) <= self.宽度:
                                行表[-1] = 上一行 + self.省略号
                                break
                        行表.append(加缩进 + self.省略号.lstrip())
                    break
        return 行表

    def _split_chunks(self, text):
        text = self._munge_whitespace(text)
        return self._split(text)

    def 折行(self, text):
        """wrap(text : string) -> [string]

        Reformat the single paragraph in 'text' so it fits in lines of
        no more than 'self.width' columns, and return a list of wrapped
        lines.  Tabs in 'text' are expanded with string.expandtabs(),
        and all other whitespace characters (including newline) are
        converted to space.
        """
        块 = self._split_chunks(text)
        if self.修句末:
            self._fix_sentence_endings(块)
        return self._wrap_chunks(块)

    def 填充(self, text):
        """fill(text : string) -> string

        Reformat the single paragraph in 'text' to fit in lines of no
        more than 'self.width' columns, and return a new string
        containing the entire wrapped paragraph.
        """
        return '\n'.join(self.折行(text))
_装类转发(文本折行器, {'fill': '填充', 'sentence_end_re': '句末正则', 'unicode_whitespace_trans': '统一空白表', 'wordsep_re': '词分隔正则', 'wordsep_simple_re': '简单词分隔正则', 'wrap': '折行'}, {'break_long_words': '断长词', 'break_on_hyphens': '按连字符断', 'drop_whitespace': '丢空白', 'expand_tabs': '展开制表符', 'fill': '填充', 'fix_sentence_endings': '修句末', 'initial_indent': '首行缩进', 'max_lines': '最多行数', 'placeholder': '省略号', 'replace_whitespace': '替换空白', 'sentence_end_re': '句末正则', 'subsequent_indent': '后续缩进', 'tabsize': '制表符宽度', 'unicode_whitespace_trans': '统一空白表', 'width': '宽度', 'wordsep_re': '词分隔正则', 'wordsep_simple_re': '简单词分隔正则', 'wrap': '折行'})

def 折行(text, width=70, **kwargs):
    """Wrap a single paragraph of text, returning a list of wrapped lines.

    Reformat the single paragraph in 'text' so it fits in lines of no
    more than 'width' columns, and return a list of wrapped lines.  By
    default, tabs in 'text' are expanded with string.expandtabs(), and
    all other whitespace characters (including newline) are converted to
    space.  See TextWrapper class for available keyword args to customize
    wrapping behaviour.
    """
    w = 文本折行器(width=width, **kwargs)
    return w.wrap(text)

def 填充(text, width=70, **kwargs):
    """Fill a single paragraph of text, returning a new string.

    Reformat the single paragraph in 'text' to fit in lines of no more
    than 'width' columns, and return a new string containing the entire
    wrapped paragraph.  As with wrap(), tabs are expanded and other
    whitespace characters converted to space.  See TextWrapper class for
    available keyword args to customize wrapping behaviour.
    """
    w = 文本折行器(width=width, **kwargs)
    return w.fill(text)

def 缩短(text, width, **kwargs):
    """Collapse and truncate the given text to fit in the given width.

    The text first has its whitespace collapsed.  If it then fits in
    the *width*, it is returned as is.  Otherwise, as many words
    as possible are joined and then the placeholder is appended::

        >>> textwrap.shorten("Hello  world!", width=12)
        'Hello world!'
        >>> textwrap.shorten("Hello  world!", width=11)
        'Hello [...]'
    """
    w = 文本折行器(width=width, max_lines=1, **kwargs)
    return w.fill(' '.join(text.strip().split()))

def 去缩进(text):
    """Remove any common leading whitespace from every line in `text`.

    This can be used to make triple-quoted strings line up with the left
    edge of the display, while still presenting them in the source code
    in indented form.

    Note that tabs and spaces are both treated as whitespace, but they
    are not equal: the lines "  hello" and "\\thello" are
    considered to have no common leading whitespace.

    Entirely blank lines are normalized to a newline character.
    """
    try:
        行表 = text.split('\n')
    except (AttributeError, TypeError):
        消息 = f'expected str object, not {type(text).__qualname__!r}'
        raise TypeError(消息) from None
    非空行 = [l for l in 行表 if l and (not l.isspace())]
    左一 = min(非空行, default='')
    左二 = max(非空行, default='')
    边距 = 0
    for 边距, c in enumerate(左一):
        if c != 左二[边距] or c not in ' \t':
            break
    return '\n'.join([l[边距:] if not l.isspace() else '' for l in 行表])

def 加缩进(text, prefix, predicate=None):
    """Adds 'prefix' to the beginning of selected lines in 'text'.

    If 'predicate' is provided, 'prefix' will only be added to the lines
    where 'predicate(line)' is True. If 'predicate' is not provided,
    it will default to adding 'prefix' to all non-empty lines that do not
    consist solely of whitespace characters.
    """
    加前缀的行 = []
    if predicate is None:
        for 行 in text.splitlines(True):
            if not 行.isspace():
                加前缀的行.append(prefix)
            加前缀的行.append(行)
    else:
        for 行 in text.splitlines(True):
            if predicate(行):
                加前缀的行.append(prefix)
            加前缀的行.append(行)
    return ''.join(加前缀的行)
if __name__ == '__main__':
    print(去缩进('Hello there.\n  This is indented.'))


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'TextWrapper': '文本折行器',
    'dedent': '去缩进',
    'fill': '填充',
    'indent': '加缩进',
    'shorten': '缩短',
    'wrap': '折行',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '文本折行器': {
        'fill': '填充',
        'sentence_end_re': '句末正则',
        'unicode_whitespace_trans': '统一空白表',
        'wordsep_re': '词分隔正则',
        'wordsep_simple_re': '简单词分隔正则',
        'wrap': '折行',
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
    '文本折行器': {
        'break_long_words': '断长词',
        'break_on_hyphens': '按连字符断',
        'drop_whitespace': '丢空白',
        'expand_tabs': '展开制表符',
        'fill': '填充',
        'fix_sentence_endings': '修句末',
        'initial_indent': '首行缩进',
        'max_lines': '最多行数',
        'placeholder': '省略号',
        'replace_whitespace': '替换空白',
        'sentence_end_re': '句末正则',
        'subsequent_indent': '后续缩进',
        'tabsize': '制表符宽度',
        'unicode_whitespace_trans': '统一空白表',
        'width': '宽度',
        'wordsep_re': '词分隔正则',
        'wordsep_simple_re': '简单词分隔正则',
        'wrap': '折行',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '加缩进',
    '去缩进',
    '填充',
    '折行',
    '文本折行器',
    '缩短',
]

# ---- 转发层结束 ----
