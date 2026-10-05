# -*- coding: utf-8 -*-
"""文件名匹配 —— 汉语库（由 tools/汉化库.py 从 Lib/fnmatch.py 机械生成，**不要手改**）。

英文库 Lib/fnmatch.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 文件名匹配
"""


"""Filename matching with shell patterns.

fnmatch(FILENAME, PATTERN) matches according to the local convention.
fnmatchcase(FILENAME, PATTERN) always takes case in account.

The functions operate by translating the pattern into a regular
expression.  They cache the compiled regular expressions for speed.

The function translate(PATTERN) returns a regular expression
corresponding to PATTERN.  (It does not compile it.)
"""
_英文原名表 = {'filterfalse': '筛掉', 'fnmatch': '匹配文件名', 'fnmatchcase': '区分大小写匹配', 'translate': '转正则'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import functools
import itertools
import os
import posixpath
import re
__all__ = ['filter', 'filterfalse', 'fnmatch', 'fnmatchcase', 'translate']

def 匹配文件名(name, pat):
    """Test whether FILENAME matches PATTERN.

    Patterns are Unix shell style:

    *       matches everything
    ?       matches any single character
    [seq]   matches any character in seq
    [!seq]  matches any char not in seq

    An initial period in FILENAME is not special.
    Both FILENAME and PATTERN are first case-normalized
    if the operating system requires it.
    If you don't want this, use fnmatchcase(FILENAME, PATTERN).
    """
    name = os.path.normcase(name)
    pat = os.path.normcase(pat)
    return 区分大小写匹配(name, pat)

@functools.lru_cache(maxsize=32768, typed=True)
def _compile_pattern(pat):
    if isinstance(pat, bytes):
        pat_str = str(pat, 'ISO-8859-1')
        res_str = 转正则(pat_str)
        res = bytes(res_str, 'ISO-8859-1')
    else:
        res = 转正则(pat)
    return re.compile(res).match

def filter(names, pat):
    """Construct a list from those elements of the iterable NAMES that match PAT."""
    result = []
    pat = os.path.normcase(pat)
    match = _compile_pattern(pat)
    if os.path is posixpath:
        for name in names:
            if match(name):
                result.append(name)
    else:
        for name in names:
            if match(os.path.normcase(name)):
                result.append(name)
    return result

def 筛掉(names, pat):
    """Construct a list from those elements of the iterable NAMES that do not match PAT."""
    pat = os.path.normcase(pat)
    match = _compile_pattern(pat)
    if os.path is posixpath:
        return list(itertools.filterfalse(match, names))
    result = []
    for name in names:
        if match(os.path.normcase(name)) is None:
            result.append(name)
    return result

def 区分大小写匹配(name, pat):
    """Test whether FILENAME matches PATTERN, including case.

    This is a version of fnmatch() which doesn't case-normalize
    its arguments.
    """
    match = _compile_pattern(pat)
    return match(name) is not None

def 转正则(pat):
    """Translate a shell PATTERN to a regular expression.

    There is no way to quote meta-characters.
    """
    parts, star_indices = _translate(pat, '*', '.')
    return _join_translated_parts(parts, star_indices)
_re_setops_sub = re.compile('([&~|])').sub
_re_escape = functools.lru_cache(maxsize=512)(re.escape)

def _translate(pat, star, question_mark):
    res = []
    add = res.append
    star_indices = []
    i, n = (0, len(pat))
    while i < n:
        c = pat[i]
        i = i + 1
        if c == '*':
            star_indices.append(len(res))
            add(star)
            while i < n and pat[i] == '*':
                i += 1
        elif c == '?':
            add(question_mark)
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j + 1
            if j < n and pat[j] == ']':
                j = j + 1
            while j < n and pat[j] != ']':
                j = j + 1
            if j >= n:
                add('\\[')
            else:
                stuff = pat[i:j]
                if '-' not in stuff:
                    stuff = stuff.replace('\\', '\\\\')
                else:
                    chunks = []
                    k = i + 2 if pat[i] == '!' else i + 1
                    while True:
                        k = pat.find('-', k, j)
                        if k < 0:
                            break
                        chunks.append(pat[i:k])
                        i = k + 1
                        k = k + 3
                    chunk = pat[i:j]
                    if chunk:
                        chunks.append(chunk)
                    else:
                        chunks[-1] += '-'
                    for k in range(len(chunks) - 1, 0, -1):
                        if chunks[k - 1][-1] > chunks[k][0]:
                            chunks[k - 1] = chunks[k - 1][:-1] + chunks[k][1:]
                            del chunks[k]
                    stuff = '-'.join((s.replace('\\', '\\\\').replace('-', '\\-') for s in chunks))
                i = j + 1
                if not stuff:
                    add('(?!)')
                elif stuff == '!':
                    add('.')
                else:
                    stuff = _re_setops_sub('\\\\\\1', stuff)
                    if stuff[0] == '!':
                        stuff = '^' + stuff[1:]
                    elif stuff[0] in ('^', '['):
                        stuff = '\\' + stuff
                    add(f'[{stuff}]')
        else:
            add(_re_escape(c))
    assert i == n
    return (res, star_indices)

def _join_translated_parts(parts, star_indices):
    if not star_indices:
        return f"(?s:{''.join(parts)})\\z"
    iter_star_indices = iter(star_indices)
    j = next(iter_star_indices)
    buffer = parts[:j]
    append, extend = (buffer.append, buffer.extend)
    i = j + 1
    for j in iter_star_indices:
        append('(?>.*?')
        extend(parts[i:j])
        append(')')
        i = j + 1
    append('.*')
    extend(parts[i:])
    res = ''.join(buffer)
    return f'(?s:{res})\\z'


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
    '筛出': 'filter',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'filterfalse': '筛掉',
    'fnmatch': '匹配文件名',
    'fnmatchcase': '区分大小写匹配',
    'translate': '转正则',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '匹配文件名',
    '区分大小写匹配',
    '筛出',
    '筛掉',
    '转正则',
]

# ---- 转发层结束 ----
