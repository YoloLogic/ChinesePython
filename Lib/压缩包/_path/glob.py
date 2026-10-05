# -*- coding: utf-8 -*-
"""压缩包._path/glob —— 汉语库（由 tools/汉化库.py 从 Lib/zipfile/_path/glob.py 机械生成，**不要手改**）。

英文库 Lib/zipfile._path/glob.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py zipfile
"""


import os
import re
_default_seps = os.sep + str(os.altsep) * bool(os.altsep)

class Translator:
    """
    >>> Translator('xyz')
    Traceback (most recent call last):
    ...
    AssertionError: Invalid separators

    >>> Translator('')
    Traceback (most recent call last):
    ...
    AssertionError: Invalid separators
    """
    seps: str

    def __init__(self, seps: str=_default_seps):
        assert seps and set(seps) <= set(_default_seps), 'Invalid separators'
        self.seps = seps

    def translate(self, pattern):
        """
        Given a glob pattern, produce a regex that matches it.
        """
        return self.extend(self.match_dirs(self.translate_core(pattern)))

    def extend(self, pattern):
        """
        Extend regex for pattern-wide concerns.

        Apply '(?s:)' to create a non-matching group that
        matches newlines (valid on Unix).

        Append '\\z' to imply fullmatch even when match is used.
        """
        return f'(?s:{pattern})\\z'

    def match_dirs(self, pattern):
        """
        Ensure that zipfile.Path directory names are matched.

        zipfile.Path directory names always end in a slash.
        """
        return f'{pattern}[/]?'

    def translate_core(self, pattern):
        """
        Given a glob pattern, produce a regex that matches it.

        >>> t = Translator()
        >>> t.translate_core('*.txt').replace('\\\\\\\\', '')
        '[^/]*\\\\.txt'
        >>> t.translate_core('a?txt')
        'a[^/]txt'
        >>> t.translate_core('**/*').replace('\\\\\\\\', '')
        '.*/[^/][^/]*'
        """
        self.restrict_rglob(pattern)
        return ''.join(map(self.replace, separate(self.star_not_empty(pattern))))

    def replace(self, match):
        """
        Perform the replacements for a match from :func:`separate`.
        """
        return match.group('set') or re.escape(match.group(0)).replace('\\*\\*', '.*').replace('\\*', f'[^{re.escape(self.seps)}]*').replace('\\?', '[^/]')

    def restrict_rglob(self, pattern):
        """
        Raise ValueError if ** appears in anything but a full path segment.

        >>> Translator().translate('**foo')
        Traceback (most recent call last):
        ...
        ValueError: ** must appear alone in a path segment
        """
        seps_pattern = f'[{re.escape(self.seps)}]+'
        segments = re.split(seps_pattern, pattern)
        if any(('**' in segment and segment != '**' for segment in segments)):
            raise ValueError('** must appear alone in a path segment')

    def star_not_empty(self, pattern):
        """
        Ensure that * will not match an empty segment.
        """

        def handle_segment(match):
            segment = match.group(0)
            return '?*' if segment == '*' else segment
        not_seps_pattern = f'[^{re.escape(self.seps)}]+'
        return re.sub(not_seps_pattern, handle_segment, pattern)

def separate(pattern):
    """
    Separate out character sets to avoid translating their contents.

    >>> [m.group(0) for m in separate('*.txt')]
    ['*.txt']
    >>> [m.group(0) for m in separate('a[?]txt')]
    ['a', '[?]', 'txt']
    """
    return re.finditer('([^\\[]+)|(?P<set>[\\[].*?[\\]])|([\\[][^\\]]*$)', pattern)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# ---- 转发层结束 ----
