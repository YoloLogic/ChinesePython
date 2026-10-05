# -*- coding: utf-8 -*-
"""差异比较 —— 汉语库（由 tools/汉化库.py 从 Lib/difflib.py 机械生成，**不要手改**）。

英文库 Lib/difflib.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 差异比较
"""


"""
Module difflib -- helpers for computing deltas between objects.

Function get_close_matches(word, possibilities, n=3, cutoff=0.6):
    Use SequenceMatcher to return list of the best "good enough" matches.

Function context_diff(a, b):
    For two lists of strings, return a delta in context diff format.

Function ndiff(a, b):
    Return a delta: the difference between `a` and `b` (lists of strings).

Function restore(delta, which):
    Return one of the two sequences that generated an ndiff delta.

Function unified_diff(a, b):
    For two lists of strings, return a delta in unified diff format.

Class SequenceMatcher:
    A flexible class for comparing pairs of sequences of any type.

Class Differ:
    For producing human-readable deltas from sequences of lines of text.

Class HtmlDiff:
    For producing HTML side by side comparison with change highlights.
"""
_英文原名表 = {'Differ': '行差异器', 'HtmlDiff': 'HTML差异', 'IS_CHARACTER_JUNK': '是忽略字符吗', 'IS_LINE_JUNK': '是忽略行吗', 'Match': '匹配项', 'SequenceMatcher': '序列比较器', 'context_diff': '上下文差异', 'diff_bytes': '字节差异', 'get_close_matches': '取最相近', 'ndiff': '逐行差异', 'restore': '还原', 'unified_diff': '统一差异'}

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
__all__ = ['get_close_matches', 'ndiff', 'restore', 'SequenceMatcher', 'Differ', 'IS_CHARACTER_JUNK', 'IS_LINE_JUNK', 'context_diff', 'unified_diff', 'diff_bytes', 'HtmlDiff', 'Match']
from heapq import nlargest as _nlargest
from collections import namedtuple as _namedtuple
from types import GenericAlias
匹配项 = _namedtuple('Match', 'a b size')

def _calculate_ratio(matches, length):
    if length:
        return 2.0 * matches / length
    return 1.0

class 序列比较器:
    """
    SequenceMatcher is a flexible class for comparing pairs of sequences of
    any type, so long as the sequence elements are hashable.  The basic
    algorithm predates, and is a little fancier than, an algorithm
    published in the late 1980's by Ratcliff and Obershelp under the
    hyperbolic name "gestalt pattern matching".  The basic idea is to find
    the longest contiguous matching subsequence that contains no "junk"
    elements (R-O doesn't address junk).  The same idea is then applied
    recursively to the pieces of the sequences to the left and to the right
    of the matching subsequence.  This does not yield minimal edit
    sequences, but does tend to yield matches that "look right" to people.

    SequenceMatcher tries to compute a "human-friendly diff" between two
    sequences.  Unlike e.g. UNIX(tm) diff, the fundamental notion is the
    longest *contiguous* & junk-free matching subsequence.  That's what
    catches peoples' eyes.  The Windows(tm) windiff has another interesting
    notion, pairing up elements that appear uniquely in each sequence.
    That, and the method here, appear to yield more intuitive difference
    reports than does diff.  This method appears to be the least vulnerable
    to syncing up on blocks of "junk lines", though (like blank lines in
    ordinary text files, or maybe "<P>" lines in HTML files).  That may be
    because this is the only method of the 3 that has a *concept* of
    "junk" <wink>.

    Example, comparing two strings, and considering blanks to be "junk":

    >>> s = SequenceMatcher(lambda x: x == " ",
    ...                     "private Thread currentThread;",
    ...                     "private volatile Thread currentThread;")
    >>>

    .ratio() returns a float in [0, 1], measuring the "similarity" of the
    sequences.  As a rule of thumb, a .ratio() value over 0.6 means the
    sequences are close matches:

    >>> print(round(s.ratio(), 2))
    0.87
    >>>

    If you're only interested in where the sequences match,
    .get_matching_blocks() is handy:

    >>> for block in s.get_matching_blocks():
    ...     print("a[%d] and b[%d] match for %d elements" % block)
    a[0] and b[0] match for 8 elements
    a[8] and b[17] match for 21 elements
    a[29] and b[38] match for 0 elements

    Note that the last tuple returned by .get_matching_blocks() is always a
    dummy, (len(a), len(b), 0), and this is the only case in which the last
    tuple element (number of elements matched) is 0.

    If you want to know how to change the first sequence into the second,
    use .get_opcodes():

    >>> for opcode in s.get_opcodes():
    ...     print("%6s a[%d:%d] b[%d:%d]" % opcode)
     equal a[0:8] b[0:8]
    insert a[8:8] b[8:17]
     equal a[8:29] b[17:38]

    See the Differ class for a fancy human-friendly file differencer, which
    uses SequenceMatcher both to compare sequences of lines, and to compare
    sequences of characters within similar (near-matching) lines.

    See also function get_close_matches() in this module, which shows how
    simple code building on SequenceMatcher can be used to do useful work.

    Timing:  Basic R-O is cubic time worst case and quadratic time expected
    case.  SequenceMatcher is quadratic time for the worst case and has
    expected-case behavior dependent in a complicated way on how many
    elements the sequences have in common; best case time is linear.
    """

    def __init__(self, isjunk=None, a='', b='', autojunk=True):
        """Construct a SequenceMatcher.

        Optional arg isjunk is None (the default), or a one-argument
        function that takes a sequence element and returns true iff the
        element is junk.  None is equivalent to passing "lambda x: 0", i.e.
        no elements are considered to be junk.  For example, pass
            lambda x: x in " \\t"
        if you're comparing lines as sequences of characters, and don't
        want to synch up on blanks or hard tabs.

        Optional arg a is the first of two sequences to be compared.  By
        default, an empty string.  The elements of a must be hashable.  See
        also .set_seqs() and .set_seq1().

        Optional arg b is the second of two sequences to be compared.  By
        default, an empty string.  The elements of b must be hashable. See
        also .set_seqs() and .set_seq2().

        Optional arg autojunk should be set to False to disable the
        "automatic junk heuristic" that treats popular elements as junk
        (see module documentation for more information).
        """
        self.isjunk = isjunk
        self.a = self.b = None
        self.autojunk = autojunk
        self.设序列(a, b)

    def 设序列(self, a, b):
        """Set the two sequences to be compared.

        >>> s = SequenceMatcher()
        >>> s.set_seqs("abcd", "bcde")
        >>> s.ratio()
        0.75
        """
        self.设首序列(a)
        self.设次序列(b)

    def 设首序列(self, a):
        """Set the first sequence to be compared.

        The second sequence to be compared is not changed.

        >>> s = SequenceMatcher(None, "abcd", "bcde")
        >>> s.ratio()
        0.75
        >>> s.set_seq1("bcde")
        >>> s.ratio()
        1.0
        >>>

        SequenceMatcher computes and caches detailed information about the
        second sequence, so if you want to compare one sequence S against
        many sequences, use .set_seq2(S) once and call .set_seq1(x)
        repeatedly for each of the other sequences.

        See also set_seqs() and set_seq2().
        """
        if a is self.a:
            return
        self.a = a
        self.匹配块表 = self.操作码表 = None

    def 设次序列(self, b):
        """Set the second sequence to be compared.

        The first sequence to be compared is not changed.

        >>> s = SequenceMatcher(None, "abcd", "bcde")
        >>> s.ratio()
        0.75
        >>> s.set_seq2("abcd")
        >>> s.ratio()
        1.0
        >>>

        SequenceMatcher computes and caches detailed information about the
        second sequence, so if you want to compare one sequence S against
        many sequences, use .set_seq2(S) once and call .set_seq1(x)
        repeatedly for each of the other sequences.

        See also set_seqs() and set_seq1().
        """
        if b is self.b:
            return
        self.b = b
        self.匹配块表 = self.操作码表 = None
        self.全量计数 = None
        self.__chain_b()

    def __chain_b(self):
        b = self.b
        self.元素表 = 元素表 = {}
        for i, elt in enumerate(b):
            indices = 元素表.setdefault(elt, [])
            indices.append(i)
        self.忽略集 = junk = set()
        isjunk = self.isjunk
        if isjunk:
            for elt in 元素表.keys():
                if isjunk(elt):
                    junk.add(elt)
            for elt in junk:
                del 元素表[elt]
        self.常见集 = popular = set()
        n = len(b)
        if self.autojunk and n >= 200:
            ntest = n // 100 + 1
            for elt, idxs in 元素表.items():
                if len(idxs) > ntest:
                    popular.add(elt)
            for elt in popular:
                del 元素表[elt]

    def 找最长匹配(self, alo=0, ahi=None, blo=0, bhi=None):
        """Find longest matching block in a[alo:ahi] and b[blo:bhi].

        By default it will find the longest match in the entirety of a and b.

        If isjunk is not defined:

        Return (i,j,k) such that a[i:i+k] is equal to b[j:j+k], where
            alo <= i <= i+k <= ahi
            blo <= j <= j+k <= bhi
        and for all (i',j',k') meeting those conditions,
            k >= k'
            i <= i'
            and if i == i', j <= j'

        In other words, of all maximal matching blocks, return one that
        starts earliest in a, and of all those maximal matching blocks that
        start earliest in a, return the one that starts earliest in b.

        >>> s = SequenceMatcher(None, " abcd", "abcd abcd")
        >>> s.find_longest_match(0, 5, 0, 9)
        Match(a=0, b=4, size=5)

        If isjunk is defined, first the longest matching block is
        determined as above, but with the additional restriction that no
        junk element appears in the block.  Then that block is extended as
        far as possible by matching (only) junk elements on both sides.  So
        the resulting block never matches on junk except as identical junk
        happens to be adjacent to an "interesting" match.

        Here's the same example as before, but considering blanks to be
        junk.  That prevents " abcd" from matching the " abcd" at the tail
        end of the second sequence directly.  Instead only the "abcd" can
        match, and matches the leftmost "abcd" in the second sequence:

        >>> s = SequenceMatcher(lambda x: x==" ", " abcd", "abcd abcd")
        >>> s.find_longest_match(0, 5, 0, 9)
        Match(a=1, b=0, size=4)

        If no blocks match, return (alo, blo, 0).

        >>> s = SequenceMatcher(None, "ab", "c")
        >>> s.find_longest_match(0, 2, 0, 1)
        Match(a=0, b=0, size=0)
        """
        a, b, 元素表, 是忽略元素吗 = (self.a, self.b, self.元素表, self.忽略集.__contains__)
        if ahi is None:
            ahi = len(a)
        if bhi is None:
            bhi = len(b)
        besti, bestj, bestsize = (alo, blo, 0)
        j2len = {}
        nothing = []
        for i in range(alo, ahi):
            j2lenget = j2len.get
            newj2len = {}
            for j in 元素表.get(a[i], nothing):
                if j < blo:
                    continue
                if j >= bhi:
                    break
                k = newj2len[j] = j2lenget(j - 1, 0) + 1
                if k > bestsize:
                    besti, bestj, bestsize = (i - k + 1, j - k + 1, k)
            j2len = newj2len
        while besti > alo and bestj > blo and (not 是忽略元素吗(b[bestj - 1])) and (a[besti - 1] == b[bestj - 1]):
            besti, bestj, bestsize = (besti - 1, bestj - 1, bestsize + 1)
        while besti + bestsize < ahi and bestj + bestsize < bhi and (not 是忽略元素吗(b[bestj + bestsize])) and (a[besti + bestsize] == b[bestj + bestsize]):
            bestsize += 1
        while besti > alo and bestj > blo and 是忽略元素吗(b[bestj - 1]) and (a[besti - 1] == b[bestj - 1]):
            besti, bestj, bestsize = (besti - 1, bestj - 1, bestsize + 1)
        while besti + bestsize < ahi and bestj + bestsize < bhi and 是忽略元素吗(b[bestj + bestsize]) and (a[besti + bestsize] == b[bestj + bestsize]):
            bestsize = bestsize + 1
        return 匹配项(besti, bestj, bestsize)

    def 取匹配块(self):
        """Return list of triples describing matching subsequences.

        Each triple is of the form (i, j, n), and means that
        a[i:i+n] == b[j:j+n].  The triples are monotonically increasing in
        i and in j.  New in Python 2.5, it's also guaranteed that if
        (i, j, n) and (i', j', n') are adjacent triples in the list, and
        the second is not the last triple in the list, then i+n != i' or
        j+n != j'.  IOW, adjacent triples never describe adjacent equal
        blocks.

        The last triple is a dummy, (len(a), len(b), 0), and is the only
        triple with n==0.

        >>> s = SequenceMatcher(None, "abxcd", "abcd")
        >>> list(s.get_matching_blocks())
        [Match(a=0, b=0, size=2), Match(a=3, b=2, size=2), Match(a=5, b=4, size=0)]
        """
        if self.匹配块表 is not None:
            return self.匹配块表
        la, lb = (len(self.a), len(self.b))
        queue = [(0, la, 0, lb)]
        匹配块表 = []
        while queue:
            alo, ahi, blo, bhi = queue.pop()
            i, j, k = x = self.找最长匹配(alo, ahi, blo, bhi)
            if k:
                匹配块表.append(x)
                if alo < i and blo < j:
                    queue.append((alo, i, blo, j))
                if i + k < ahi and j + k < bhi:
                    queue.append((i + k, ahi, j + k, bhi))
        匹配块表.sort()
        i1 = j1 = k1 = 0
        non_adjacent = []
        for i2, j2, k2 in 匹配块表:
            if i1 + k1 == i2 and j1 + k1 == j2:
                k1 += k2
            else:
                if k1:
                    non_adjacent.append((i1, j1, k1))
                i1, j1, k1 = (i2, j2, k2)
        if k1:
            non_adjacent.append((i1, j1, k1))
        non_adjacent.append((la, lb, 0))
        self.匹配块表 = list(map(匹配项._make, non_adjacent))
        return self.匹配块表

    def 取操作码(self):
        """Return list of 5-tuples describing how to turn a into b.

        Each tuple is of the form (tag, i1, i2, j1, j2).  The first tuple
        has i1 == j1 == 0, and remaining tuples have i1 == the i2 from the
        tuple preceding it, and likewise for j1 == the previous j2.

        The tags are strings, with these meanings:

        'replace':  a[i1:i2] should be replaced by b[j1:j2]
        'delete':   a[i1:i2] should be deleted.
                    Note that j1==j2 in this case.
        'insert':   b[j1:j2] should be inserted at a[i1:i1].
                    Note that i1==i2 in this case.
        'equal':    a[i1:i2] == b[j1:j2]

        >>> a = "qabxcd"
        >>> b = "abycdf"
        >>> s = SequenceMatcher(None, a, b)
        >>> for tag, i1, i2, j1, j2 in s.get_opcodes():
        ...    print(("%7s a[%d:%d] (%s) b[%d:%d] (%s)" %
        ...           (tag, i1, i2, a[i1:i2], j1, j2, b[j1:j2])))
         delete a[0:1] (q) b[0:0] ()
          equal a[1:3] (ab) b[0:2] (ab)
        replace a[3:4] (x) b[2:3] (y)
          equal a[4:6] (cd) b[3:5] (cd)
         insert a[6:6] () b[5:6] (f)
        """
        if self.操作码表 is not None:
            return self.操作码表
        i = j = 0
        self.操作码表 = answer = []
        for ai, bj, size in self.取匹配块():
            tag = ''
            if i < ai and j < bj:
                tag = 'replace'
            elif i < ai:
                tag = 'delete'
            elif j < bj:
                tag = 'insert'
            if tag:
                answer.append((tag, i, ai, j, bj))
            i, j = (ai + size, bj + size)
            if size:
                answer.append(('equal', ai, i, bj, j))
        return answer

    def 取分组操作码(self, n=3):
        """ Isolate change clusters by eliminating ranges with no changes.

        Return a generator of groups with up to n lines of context.
        Each group is in the same format as returned by get_opcodes().

        >>> from pprint import pprint
        >>> a = list(map(str, range(1,40)))
        >>> b = a[:]
        >>> b[8:8] = ['i']     # Make an insertion
        >>> b[20] += 'x'       # Make a replacement
        >>> b[23:28] = []      # Make a deletion
        >>> b[30] += 'y'       # Make another replacement
        >>> pprint(list(SequenceMatcher(None,a,b).get_grouped_opcodes()))
        [[('equal', 5, 8, 5, 8), ('insert', 8, 8, 8, 9), ('equal', 8, 11, 9, 12)],
         [('equal', 16, 19, 17, 20),
          ('replace', 19, 20, 20, 21),
          ('equal', 20, 22, 21, 23),
          ('delete', 22, 27, 23, 23),
          ('equal', 27, 30, 23, 26)],
         [('equal', 31, 34, 27, 30),
          ('replace', 34, 35, 30, 31),
          ('equal', 35, 38, 31, 34)]]
        """
        codes = self.取操作码()
        if not codes:
            codes = [('equal', 0, 1, 0, 1)]
        if codes[0][0] == 'equal':
            tag, i1, i2, j1, j2 = codes[0]
            codes[0] = (tag, max(i1, i2 - n), i2, max(j1, j2 - n), j2)
        if codes[-1][0] == 'equal':
            tag, i1, i2, j1, j2 = codes[-1]
            codes[-1] = (tag, i1, min(i2, i1 + n), j1, min(j2, j1 + n))
        nn = n + n
        group = []
        for tag, i1, i2, j1, j2 in codes:
            if tag == 'equal' and i2 - i1 > nn:
                group.append((tag, i1, min(i2, i1 + n), j1, min(j2, j1 + n)))
                yield group
                group = []
                i1, j1 = (max(i1, i2 - n), max(j1, j2 - n))
            group.append((tag, i1, i2, j1, j2))
        if group and (not (len(group) == 1 and group[0][0] == 'equal')):
            yield group

    def 相似度(self):
        """Return a measure of the sequences' similarity (float in [0,1]).

        Where T is the total number of elements in both sequences, and
        M is the number of matches, this is 2.0*M / T.
        Note that this is 1 if the sequences are identical, and 0 if
        they have nothing in common.

        .ratio() is expensive to compute if you haven't already computed
        .get_matching_blocks() or .get_opcodes(), in which case you may
        want to try .quick_ratio() or .real_quick_ratio() first to get an
        upper bound.

        >>> s = SequenceMatcher(None, "abcd", "bcde")
        >>> s.ratio()
        0.75
        >>> s.quick_ratio()
        0.75
        >>> s.real_quick_ratio()
        1.0
        """
        matches = sum((triple[-1] for triple in self.取匹配块()))
        return _calculate_ratio(matches, len(self.a) + len(self.b))

    def 快速相似度(self):
        """Return an upper bound on ratio() relatively quickly.

        This isn't defined beyond that it is an upper bound on .ratio(), and
        is faster to compute.
        """
        if self.全量计数 is None:
            self.全量计数 = 全量计数 = {}
            for elt in self.b:
                全量计数[elt] = 全量计数.get(elt, 0) + 1
        全量计数 = self.全量计数
        avail = {}
        availhas, matches = (avail.__contains__, 0)
        for elt in self.a:
            if availhas(elt):
                numb = avail[elt]
            else:
                numb = 全量计数.get(elt, 0)
            avail[elt] = numb - 1
            if numb > 0:
                matches = matches + 1
        return _calculate_ratio(matches, len(self.a) + len(self.b))

    def 极快相似度(self):
        """Return an upper bound on ratio() very quickly.

        This isn't defined beyond that it is an upper bound on .ratio(), and
        is faster to compute than either .ratio() or .quick_ratio().
        """
        la, lb = (len(self.a), len(self.b))
        return _calculate_ratio(min(la, lb), la + lb)
    __class_getitem__ = classmethod(GenericAlias)
_装类转发(序列比较器, {'find_longest_match': '找最长匹配', 'get_grouped_opcodes': '取分组操作码', 'get_matching_blocks': '取匹配块', 'get_opcodes': '取操作码', 'quick_ratio': '快速相似度', 'ratio': '相似度', 'real_quick_ratio': '极快相似度', 'set_seq1': '设首序列', 'set_seq2': '设次序列', 'set_seqs': '设序列'}, {'b2j': '元素表', 'bjunk': '忽略集', 'bpopular': '常见集', 'find_longest_match': '找最长匹配', 'fullbcount': '全量计数', 'get_grouped_opcodes': '取分组操作码', 'get_matching_blocks': '取匹配块', 'get_opcodes': '取操作码', 'matching_blocks': '匹配块表', 'opcodes': '操作码表', 'quick_ratio': '快速相似度', 'ratio': '相似度', 'real_quick_ratio': '极快相似度', 'set_seq1': '设首序列', 'set_seq2': '设次序列', 'set_seqs': '设序列'})

def 取最相近(word, possibilities, n=3, cutoff=0.6):
    """Use SequenceMatcher to return list of the best "good enough" matches.

    word is a sequence for which close matches are desired (typically a
    string).

    possibilities is a list of sequences against which to match word
    (typically a list of strings).

    Optional arg n (default 3) is the maximum number of close matches to
    return.  n must be > 0.

    Optional arg cutoff (default 0.6) is a float in [0, 1].  Possibilities
    that don't score at least that similar to word are ignored.

    The best (no more than n) matches among the possibilities are returned
    in a list, sorted by similarity score, most similar first.

    >>> get_close_matches("appel", ["ape", "apple", "peach", "puppy"])
    ['apple', 'ape']
    >>> import keyword as _keyword
    >>> get_close_matches("wheel", _keyword.kwlist)
    ['while']
    >>> get_close_matches("Apple", _keyword.kwlist)
    []
    >>> get_close_matches("accept", _keyword.kwlist)
    ['except']
    """
    if not n > 0:
        raise ValueError('n must be > 0: %r' % (n,))
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError('cutoff must be in [0.0, 1.0]: %r' % (cutoff,))
    result = []
    s = 序列比较器()
    s.set_seq2(word)
    for x in possibilities:
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and s.quick_ratio() >= cutoff and (s.ratio() >= cutoff):
            result.append((s.ratio(), x))
    result = _nlargest(n, result)
    return [x for score, x in result]

def _keep_original_ws(s, tag_s):
    """Replace whitespace with the original whitespace characters in `s`"""
    return ''.join((c if tag_c == ' ' and c.isspace() else tag_c for c, tag_c in zip(s, tag_s)))

class 行差异器:
    """
    Differ is a class for comparing sequences of lines of text, and
    producing human-readable differences or deltas.  Differ uses
    SequenceMatcher both to compare sequences of lines, and to compare
    sequences of characters within similar (near-matching) lines.

    Each line of a Differ delta begins with a two-letter code:

        '- '    line unique to sequence 1
        '+ '    line unique to sequence 2
        '  '    line common to both sequences
        '? '    line not present in either input sequence

    Lines beginning with '? ' attempt to guide the eye to intraline
    differences, and were not present in either input sequence.  These lines
    can be confusing if the sequences contain tab characters.

    Note that Differ makes no claim to produce a *minimal* diff.  To the
    contrary, minimal diffs are often counter-intuitive, because they synch
    up anywhere possible, sometimes accidental matches 100 pages apart.
    Restricting synch points to contiguous matches preserves some notion of
    locality, at the occasional cost of producing a longer diff.

    Example: Comparing two texts.

    First we set up the texts, sequences of individual single-line strings
    ending with newlines (such sequences can also be obtained from the
    `readlines()` method of file-like objects):

    >>> text1 = '''  1. Beautiful is better than ugly.
    ...   2. Explicit is better than implicit.
    ...   3. Simple is better than complex.
    ...   4. Complex is better than complicated.
    ... '''.splitlines(keepends=True)
    >>> len(text1)
    4
    >>> text1[0][-1]
    '\\n'
    >>> text2 = '''  1. Beautiful is better than ugly.
    ...   3.   Simple is better than complex.
    ...   4. Complicated is better than complex.
    ...   5. Flat is better than nested.
    ... '''.splitlines(keepends=True)

    Next we instantiate a Differ object:

    >>> d = Differ()

    Note that when instantiating a Differ object we may pass functions to
    filter out line and character 'junk'.  See Differ.__init__ for details.

    Finally, we compare the two:

    >>> result = list(d.compare(text1, text2))

    'result' is a list of strings, so let's pretty-print it:

    >>> from pprint import pprint as _pprint
    >>> _pprint(result)
    ['    1. Beautiful is better than ugly.\\n',
     '-   2. Explicit is better than implicit.\\n',
     '-   3. Simple is better than complex.\\n',
     '+   3.   Simple is better than complex.\\n',
     '?     ++\\n',
     '-   4. Complex is better than complicated.\\n',
     '?            ^                     ---- ^\\n',
     '+   4. Complicated is better than complex.\\n',
     '?           ++++ ^                      ^\\n',
     '+   5. Flat is better than nested.\\n']

    As a single multi-line string it looks like this:

    >>> print(''.join(result), end="")
        1. Beautiful is better than ugly.
    -   2. Explicit is better than implicit.
    -   3. Simple is better than complex.
    +   3.   Simple is better than complex.
    ?     ++
    -   4. Complex is better than complicated.
    ?            ^                     ---- ^
    +   4. Complicated is better than complex.
    ?           ++++ ^                      ^
    +   5. Flat is better than nested.
    """

    def __init__(self, linejunk=None, charjunk=None):
        """
        Construct a text differencer, with optional filters.

        The two optional keyword parameters are for filter functions:

        - `linejunk`: A function that should accept a single string argument,
          and return true iff the string is junk. The module-level function
          `IS_LINE_JUNK` may be used to filter out lines without visible
          characters, except for at most one splat ('#').  It is recommended
          to leave linejunk None; the underlying SequenceMatcher class has
          an adaptive notion of "noise" lines that's better than any static
          definition the author has ever been able to craft.

        - `charjunk`: A function that should accept a string of length 1. The
          module-level function `IS_CHARACTER_JUNK` may be used to filter out
          whitespace characters (a blank or tab; **note**: bad idea to include
          newline in this!).  Use of IS_CHARACTER_JUNK is recommended.
        """
        self.linejunk = linejunk
        self.charjunk = charjunk

    def 比较(self, a, b):
        """
        Compare two sequences of lines; generate the resulting delta.

        Each sequence must contain individual single-line strings ending with
        newlines. Such sequences can be obtained from the `readlines()` method
        of file-like objects.  The delta generated also consists of newline-
        terminated strings, ready to be printed as-is via the writelines()
        method of a file-like object.

        Example:

        >>> print(''.join(Differ().compare('one\\ntwo\\nthree\\n'.splitlines(True),
        ...                                'ore\\ntree\\nemu\\n'.splitlines(True))),
        ...       end="")
        - one
        ?  ^
        + ore
        ?  ^
        - two
        - three
        ?  -
        + tree
        + emu
        """
        cruncher = 序列比较器(self.linejunk, a, b)
        for tag, alo, ahi, blo, bhi in cruncher.get_opcodes():
            if tag == 'replace':
                g = self._fancy_replace(a, alo, ahi, b, blo, bhi)
            elif tag == 'delete':
                g = self._dump('-', a, alo, ahi)
            elif tag == 'insert':
                g = self._dump('+', b, blo, bhi)
            elif tag == 'equal':
                g = self._dump(' ', a, alo, ahi)
            else:
                raise ValueError('unknown tag %r' % (tag,))
            yield from g

    def _dump(self, tag, x, lo, hi):
        """Generate comparison results for a same-tagged range."""
        for i in range(lo, hi):
            yield ('%s %s' % (tag, x[i]))

    def _plain_replace(self, a, alo, ahi, b, blo, bhi):
        assert alo < ahi and blo < bhi
        if bhi - blo < ahi - alo:
            first = self._dump('+', b, blo, bhi)
            second = self._dump('-', a, alo, ahi)
        else:
            first = self._dump('-', a, alo, ahi)
            second = self._dump('+', b, blo, bhi)
        for g in (first, second):
            yield from g

    def _fancy_replace(self, a, alo, ahi, b, blo, bhi):
        """
        When replacing one block of lines with another, search the blocks
        for *similar* lines; the best-matching pair (if any) is used as a
        synch point, and intraline difference marking is done on the
        similar pair. Lots of work, but often worth it.

        Example:

        >>> d = Differ()
        >>> results = d._fancy_replace(['abcDefghiJkl\\n'], 0, 1,
        ...                            ['abcdefGhijkl\\n'], 0, 1)
        >>> print(''.join(results), end="")
        - abcDefghiJkl
        ?    ^  ^  ^
        + abcdefGhijkl
        ?    ^  ^  ^
        """
        cutoff = 0.74999
        cruncher = 序列比较器(self.charjunk)
        crqr = cruncher.real_quick_ratio
        cqr = cruncher.quick_ratio
        cr = cruncher.ratio
        WINDOW = 10
        best_i = best_j = None
        dump_i, dump_j = (alo, blo)
        for j in range(blo, bhi):
            cruncher.set_seq2(b[j])
            aequiv = alo + (j - blo)
            arange = range(max(aequiv - WINDOW, dump_i), min(aequiv + WINDOW + 1, ahi))
            if not arange:
                break
            best_ratio = cutoff
            for i in arange:
                cruncher.set_seq1(a[i])
                if crqr() > best_ratio and cqr() > best_ratio and (cr() > best_ratio):
                    best_i, best_j, best_ratio = (i, j, cr())
            if best_i is None:
                continue
            yield from self._fancy_helper(a, dump_i, best_i, b, dump_j, best_j)
            aelt, belt = (a[best_i], b[best_j])
            if aelt != belt:
                atags = btags = ''
                cruncher.set_seqs(aelt, belt)
                for tag, ai1, ai2, bj1, bj2 in cruncher.get_opcodes():
                    la, lb = (ai2 - ai1, bj2 - bj1)
                    if tag == 'replace':
                        atags += '^' * la
                        btags += '^' * lb
                    elif tag == 'delete':
                        atags += '-' * la
                    elif tag == 'insert':
                        btags += '+' * lb
                    elif tag == 'equal':
                        atags += ' ' * la
                        btags += ' ' * lb
                    else:
                        raise ValueError('unknown tag %r' % (tag,))
                yield from self._qformat(aelt, belt, atags, btags)
            else:
                yield ('  ' + aelt)
            dump_i, dump_j = (best_i + 1, best_j + 1)
            best_i = best_j = None
        yield from self._fancy_helper(a, dump_i, ahi, b, dump_j, bhi)

    def _fancy_helper(self, a, alo, ahi, b, blo, bhi):
        g = []
        if alo < ahi:
            if blo < bhi:
                g = self._plain_replace(a, alo, ahi, b, blo, bhi)
            else:
                g = self._dump('-', a, alo, ahi)
        elif blo < bhi:
            g = self._dump('+', b, blo, bhi)
        yield from g

    def _qformat(self, aline, bline, atags, btags):
        """
        Format "?" output and deal with tabs.

        Example:

        >>> d = Differ()
        >>> results = d._qformat('\\tabcDefghiJkl\\n', '\\tabcdefGhijkl\\n',
        ...                      '  ^ ^  ^      ', '  ^ ^  ^      ')
        >>> for line in results: print(repr(line))
        ...
        '- \\tabcDefghiJkl\\n'
        '? \\t ^ ^  ^\\n'
        '+ \\tabcdefGhijkl\\n'
        '? \\t ^ ^  ^\\n'
        """
        atags = _keep_original_ws(aline, atags).rstrip()
        btags = _keep_original_ws(bline, btags).rstrip()
        yield ('- ' + aline)
        if atags:
            yield f'? {atags}\n'
        yield ('+ ' + bline)
        if btags:
            yield f'? {btags}\n'
_装类转发(行差异器, {'compare': '比较'}, {'compare': '比较'})

def 是忽略行吗(line, pat=None):
    """
    Return True for ignorable line: if `line` is blank or contains a single '#'.

    Examples:

    >>> IS_LINE_JUNK('\\n')
    True
    >>> IS_LINE_JUNK('  #   \\n')
    True
    >>> IS_LINE_JUNK('hello\\n')
    False
    """
    if pat is None:
        return line.strip() in '#'
    return pat(line) is not None

def 是忽略字符吗(ch, ws=' \t'):
    """
    Return True for ignorable character: iff `ch` is a space or tab.

    Examples:

    >>> IS_CHARACTER_JUNK(' ')
    True
    >>> IS_CHARACTER_JUNK('\\t')
    True
    >>> IS_CHARACTER_JUNK('\\n')
    False
    >>> IS_CHARACTER_JUNK('x')
    False
    """
    return ch in ws

def _format_range_unified(start, stop):
    """Convert range to the "ed" format"""
    beginning = start + 1
    length = stop - start
    if length == 1:
        return '{}'.format(beginning)
    if not length:
        beginning -= 1
    return '{},{}'.format(beginning, length)

def 统一差异(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n'):
    """
    Compare two sequences of lines; generate the delta as a unified diff.

    Unified diffs are a compact way of showing line changes and a few
    lines of context.  The number of context lines is set by 'n' which
    defaults to three.

    By default, the diff control lines (those with ---, +++, or @@) are
    created with a trailing newline.  This is helpful so that inputs
    created from file.readlines() result in diffs that are suitable for
    file.writelines() since both the inputs and outputs have trailing
    newlines.

    For inputs that do not have trailing newlines, set the lineterm
    argument to "" so that the output will be uniformly newline free.

    The unidiff format normally has a header for filenames and modification
    times.  Any or all of these may be specified using strings for
    'fromfile', 'tofile', 'fromfiledate', and 'tofiledate'.
    The modification times are normally expressed in the ISO 8601 format.

    Example:

    >>> for line in unified_diff('one two three four'.split(),
    ...             'zero one tree four'.split(), 'Original', 'Current',
    ...             '2005-01-26 23:30:50', '2010-04-02 10:20:52',
    ...             lineterm=''):
    ...     print(line)                 # doctest: +NORMALIZE_WHITESPACE
    --- Original        2005-01-26 23:30:50
    +++ Current         2010-04-02 10:20:52
    @@ -1,4 +1,4 @@
    +zero
     one
    -two
    -three
    +tree
     four
    """
    _check_types(a, b, fromfile, tofile, fromfiledate, tofiledate, lineterm)
    started = False
    for group in 序列比较器(None, a, b).get_grouped_opcodes(n):
        if not started:
            started = True
            fromdate = '\t{}'.format(fromfiledate) if fromfiledate else ''
            todate = '\t{}'.format(tofiledate) if tofiledate else ''
            yield '--- {}{}{}'.format(fromfile, fromdate, lineterm)
            yield '+++ {}{}{}'.format(tofile, todate, lineterm)
        first, last = (group[0], group[-1])
        file1_range = _format_range_unified(first[1], last[2])
        file2_range = _format_range_unified(first[3], last[4])
        yield '@@ -{} +{} @@{}'.format(file1_range, file2_range, lineterm)
        for tag, i1, i2, j1, j2 in group:
            if tag == 'equal':
                for line in a[i1:i2]:
                    yield (' ' + line)
                continue
            if tag in {'replace', 'delete'}:
                for line in a[i1:i2]:
                    yield ('-' + line)
            if tag in {'replace', 'insert'}:
                for line in b[j1:j2]:
                    yield ('+' + line)

def _format_range_context(start, stop):
    """Convert range to the "ed" format"""
    beginning = start + 1
    length = stop - start
    if not length:
        beginning -= 1
    if length <= 1:
        return '{}'.format(beginning)
    return '{},{}'.format(beginning, beginning + length - 1)

def 上下文差异(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n'):
    """
    Compare two sequences of lines; generate the delta as a context diff.

    Context diffs are a compact way of showing line changes and a few
    lines of context.  The number of context lines is set by 'n' which
    defaults to three.

    By default, the diff control lines (those with *** or ---) are
    created with a trailing newline.  This is helpful so that inputs
    created from file.readlines() result in diffs that are suitable for
    file.writelines() since both the inputs and outputs have trailing
    newlines.

    For inputs that do not have trailing newlines, set the lineterm
    argument to "" so that the output will be uniformly newline free.

    The context diff format normally has a header for filenames and
    modification times.  Any or all of these may be specified using
    strings for 'fromfile', 'tofile', 'fromfiledate', and 'tofiledate'.
    The modification times are normally expressed in the ISO 8601 format.
    If not specified, the strings default to blanks.

    Example:

    >>> print(''.join(context_diff('one\\ntwo\\nthree\\nfour\\n'.splitlines(True),
    ...       'zero\\none\\ntree\\nfour\\n'.splitlines(True), 'Original', 'Current')),
    ...       end="")
    *** Original
    --- Current
    ***************
    *** 1,4 ****
      one
    ! two
    ! three
      four
    --- 1,4 ----
    + zero
      one
    ! tree
      four
    """
    _check_types(a, b, fromfile, tofile, fromfiledate, tofiledate, lineterm)
    prefix = dict(insert='+ ', delete='- ', replace='! ', equal='  ')
    started = False
    for group in 序列比较器(None, a, b).get_grouped_opcodes(n):
        if not started:
            started = True
            fromdate = '\t{}'.format(fromfiledate) if fromfiledate else ''
            todate = '\t{}'.format(tofiledate) if tofiledate else ''
            yield '*** {}{}{}'.format(fromfile, fromdate, lineterm)
            yield '--- {}{}{}'.format(tofile, todate, lineterm)
        first, last = (group[0], group[-1])
        yield ('***************' + lineterm)
        file1_range = _format_range_context(first[1], last[2])
        yield '*** {} ****{}'.format(file1_range, lineterm)
        if any((tag in {'replace', 'delete'} for tag, _, _, _, _ in group)):
            for tag, i1, i2, _, _ in group:
                if tag != 'insert':
                    for line in a[i1:i2]:
                        yield (prefix[tag] + line)
        file2_range = _format_range_context(first[3], last[4])
        yield '--- {} ----{}'.format(file2_range, lineterm)
        if any((tag in {'replace', 'insert'} for tag, _, _, _, _ in group)):
            for tag, _, _, j1, j2 in group:
                if tag != 'delete':
                    for line in b[j1:j2]:
                        yield (prefix[tag] + line)

def _check_types(a, b, *args):
    if a and (not isinstance(a[0], str)):
        raise TypeError('lines to compare must be str, not %s (%r)' % (type(a[0]).__name__, a[0]))
    if b and (not isinstance(b[0], str)):
        raise TypeError('lines to compare must be str, not %s (%r)' % (type(b[0]).__name__, b[0]))
    if isinstance(a, str):
        raise TypeError('input must be a sequence of strings, not %s' % type(a).__name__)
    if isinstance(b, str):
        raise TypeError('input must be a sequence of strings, not %s' % type(b).__name__)
    for arg in args:
        if not isinstance(arg, str):
            raise TypeError('all arguments must be str, not: %r' % (arg,))

def 字节差异(dfunc, a, b, fromfile=b'', tofile=b'', fromfiledate=b'', tofiledate=b'', n=3, lineterm=b'\n'):
    """
    Compare `a` and `b`, two sequences of lines represented as bytes rather
    than str. This is a wrapper for `dfunc`, which is typically either
    unified_diff() or context_diff(). Inputs are losslessly converted to
    strings so that `dfunc` only has to worry about strings, and encoded
    back to bytes on return. This is necessary to compare files with
    unknown or inconsistent encoding. All other inputs (except `n`) must be
    bytes rather than str.
    """

    def decode(s):
        try:
            return s.decode('ascii', 'surrogateescape')
        except AttributeError as err:
            msg = 'all arguments must be bytes, not %s (%r)' % (type(s).__name__, s)
            raise TypeError(msg) from err
    a = list(map(decode, a))
    b = list(map(decode, b))
    fromfile = decode(fromfile)
    tofile = decode(tofile)
    fromfiledate = decode(fromfiledate)
    tofiledate = decode(tofiledate)
    lineterm = decode(lineterm)
    lines = dfunc(a, b, fromfile, tofile, fromfiledate, tofiledate, n, lineterm)
    for line in lines:
        yield line.encode('ascii', 'surrogateescape')

def 逐行差异(a, b, linejunk=None, charjunk=是忽略字符吗):
    """
    Compare `a` and `b` (lists of strings); return a `Differ`-style delta.

    Optional keyword parameters `linejunk` and `charjunk` are for filter
    functions, or can be None:

    - linejunk: A function that should accept a single string argument and
      return true iff the string is junk.  The default is None, and is
      recommended; the underlying SequenceMatcher class has an adaptive
      notion of "noise" lines.

    - charjunk: A function that accepts a character (string of length
      1), and returns true iff the character is junk. The default is
      the module-level function IS_CHARACTER_JUNK, which filters out
      whitespace characters (a blank or tab; note: it's a bad idea to
      include newline in this!).

    Tools/scripts/ndiff.py is a command-line front-end to this function.

    Example:

    >>> diff = ndiff('one\\ntwo\\nthree\\n'.splitlines(keepends=True),
    ...              'ore\\ntree\\nemu\\n'.splitlines(keepends=True))
    >>> print(''.join(diff), end="")
    - one
    ?  ^
    + ore
    ?  ^
    - two
    - three
    ?  -
    + tree
    + emu
    """
    return 行差异器(linejunk, charjunk).compare(a, b)

def _mdiff(fromlines, tolines, context=None, linejunk=None, charjunk=是忽略字符吗):
    """Returns generator yielding marked up from/to side by side differences.

    Arguments:
    fromlines -- list of text lines to compared to tolines
    tolines -- list of text lines to be compared to fromlines
    context -- number of context lines to display on each side of difference,
               if None, all from/to text lines will be generated.
    linejunk -- passed on to ndiff (see ndiff documentation)
    charjunk -- passed on to ndiff (see ndiff documentation)

    This function returns an iterator which returns a tuple:
    (from line tuple, to line tuple, boolean flag)

    from/to line tuple -- (line num, line text)
        line num -- integer or None (to indicate a context separation)
        line text -- original line text with following markers inserted:
            '\\0+' -- marks start of added text
            '\\0-' -- marks start of deleted text
            '\\0^' -- marks start of changed text
            '\\1' -- marks end of added/deleted/changed text

    boolean flag -- None indicates context separation, True indicates
        either "from" or "to" line contains a change, otherwise False.

    This function/iterator was originally developed to generate side by side
    file difference for making HTML pages (see HtmlDiff class for example
    usage).

    Note, this function utilizes the ndiff function to generate the side by
    side difference markup.  Optional ndiff arguments may be passed to this
    function and they in turn will be passed to ndiff.
    """
    import re
    change_re = re.compile('(\\++|\\-+|\\^+)')
    diff_lines_iterator = 逐行差异(fromlines, tolines, linejunk, charjunk)

    def _make_line(lines, format_key, side, num_lines=[0, 0]):
        """Returns line of text with user's change markup and line formatting.

        lines -- list of lines from the ndiff generator to produce a line of
                 text from.  When producing the line of text to return, the
                 lines used are removed from this list.
        format_key -- '+' return first line in list with "add" markup around
                          the entire line.
                      '-' return first line in list with "delete" markup around
                          the entire line.
                      '?' return first line in list with add/delete/change
                          intraline markup (indices obtained from second line)
                      None return first line in list with no markup
        side -- indice into the num_lines list (0=from,1=to)
        num_lines -- from/to current line number.  This is NOT intended to be a
                     passed parameter.  It is present as a keyword argument to
                     maintain memory of the current line numbers between calls
                     of this function.

        Note, this function is purposefully not defined at the module scope so
        that data it needs from its parent function (within whose context it
        is defined) does not need to be of module scope.
        """
        num_lines[side] += 1
        if format_key is None:
            return (num_lines[side], lines.pop(0)[2:])
        if format_key == '?':
            text, markers = (lines.pop(0), lines.pop(0))
            sub_info = []

            def record_sub_info(match_object, sub_info=sub_info):
                sub_info.append([match_object.group(1)[0], match_object.span()])
                return match_object.group(1)
            change_re.sub(record_sub_info, markers)
            for key, (begin, end) in reversed(sub_info):
                text = text[0:begin] + '\x00' + key + text[begin:end] + '\x01' + text[end:]
            text = text[2:]
        else:
            text = lines.pop(0)[2:]
            if not text:
                text = ' '
            text = '\x00' + format_key + text + '\x01'
        return (num_lines[side], text)

    def _line_iterator():
        """Yields from/to lines of text with a change indication.

        This function is an iterator.  It itself pulls lines from a
        differencing iterator, processes them and yields them.  When it can
        it yields both a "from" and a "to" line, otherwise it will yield one
        or the other.  In addition to yielding the lines of from/to text, a
        boolean flag is yielded to indicate if the text line(s) have
        differences in them.

        Note, this function is purposefully not defined at the module scope so
        that data it needs from its parent function (within whose context it
        is defined) does not need to be of module scope.
        """
        lines = []
        num_blanks_pending, num_blanks_to_yield = (0, 0)
        while True:
            while len(lines) < 4:
                lines.append(next(diff_lines_iterator, 'X'))
            s = ''.join([line[0] for line in lines])
            if s.startswith('X'):
                num_blanks_to_yield = num_blanks_pending
            elif s.startswith('-?+?'):
                yield (_make_line(lines, '?', 0), _make_line(lines, '?', 1), True)
                continue
            elif s.startswith('--++'):
                num_blanks_pending -= 1
                yield (_make_line(lines, '-', 0), None, True)
                continue
            elif s.startswith(('--?+', '--+', '- ')):
                from_line, to_line = (_make_line(lines, '-', 0), None)
                num_blanks_to_yield, num_blanks_pending = (num_blanks_pending - 1, 0)
            elif s.startswith('-+?'):
                yield (_make_line(lines, None, 0), _make_line(lines, '?', 1), True)
                continue
            elif s.startswith('-?+'):
                yield (_make_line(lines, '?', 0), _make_line(lines, None, 1), True)
                continue
            elif s.startswith('-'):
                num_blanks_pending -= 1
                yield (_make_line(lines, '-', 0), None, True)
                continue
            elif s.startswith('+--'):
                num_blanks_pending += 1
                yield (None, _make_line(lines, '+', 1), True)
                continue
            elif s.startswith(('+ ', '+-')):
                from_line, to_line = (None, _make_line(lines, '+', 1))
                num_blanks_to_yield, num_blanks_pending = (num_blanks_pending + 1, 0)
            elif s.startswith('+'):
                num_blanks_pending += 1
                yield (None, _make_line(lines, '+', 1), True)
                continue
            elif s.startswith(' '):
                yield (_make_line(lines[:], None, 0), _make_line(lines, None, 1), False)
                continue
            while num_blanks_to_yield < 0:
                num_blanks_to_yield += 1
                yield (None, ('', '\n'), True)
            while num_blanks_to_yield > 0:
                num_blanks_to_yield -= 1
                yield (('', '\n'), None, True)
            if s.startswith('X'):
                return
            else:
                yield (from_line, to_line, True)

    def _line_pair_iterator():
        """Yields from/to lines of text with a change indication.

        This function is an iterator.  It itself pulls lines from the line
        iterator.  Its difference from that iterator is that this function
        always yields a pair of from/to text lines (with the change
        indication).  If necessary it will collect single from/to lines
        until it has a matching pair from/to pair to yield.

        Note, this function is purposefully not defined at the module scope so
        that data it needs from its parent function (within whose context it
        is defined) does not need to be of module scope.
        """
        line_iterator = _line_iterator()
        fromlines, tolines = ([], [])
        while True:
            while len(fromlines) == 0 or len(tolines) == 0:
                try:
                    from_line, to_line, found_diff = next(line_iterator)
                except StopIteration:
                    return
                if from_line is not None:
                    fromlines.append((from_line, found_diff))
                if to_line is not None:
                    tolines.append((to_line, found_diff))
            from_line, fromDiff = fromlines.pop(0)
            to_line, to_diff = tolines.pop(0)
            yield (from_line, to_line, fromDiff or to_diff)
    line_pair_iterator = _line_pair_iterator()
    if context is None:
        yield from line_pair_iterator
    else:
        context += 1
        lines_to_write = 0
        while True:
            index, contextLines = (0, [None] * context)
            found_diff = False
            while found_diff is False:
                try:
                    from_line, to_line, found_diff = next(line_pair_iterator)
                except StopIteration:
                    return
                i = index % context
                contextLines[i] = (from_line, to_line, found_diff)
                index += 1
            if index > context:
                yield (None, None, None)
                lines_to_write = context
            else:
                lines_to_write = index
                index = 0
            while lines_to_write:
                i = index % context
                index += 1
                yield contextLines[i]
                lines_to_write -= 1
            lines_to_write = context - 1
            try:
                while lines_to_write:
                    from_line, to_line, found_diff = next(line_pair_iterator)
                    if found_diff:
                        lines_to_write = context - 1
                    else:
                        lines_to_write -= 1
                    yield (from_line, to_line, found_diff)
            except StopIteration:
                return
_file_template = '\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n\n<html>\n\n<head>\n    <meta http-equiv="Content-Type"\n          content="text/html; charset=%(charset)s" />\n    <title></title>\n    <style type="text/css">%(styles)s\n    </style>\n</head>\n\n<body>\n    %(table)s%(legend)s\n</body>\n\n</html>'
_styles = '\n        :root {color-scheme: light dark}\n        table.diff {font-family: Menlo, Consolas, Monaco, Liberation Mono, Lucida Console, monospace; border:medium}\n        .diff_header {background-color:#e0e0e0}\n        td.diff_header {text-align:right}\n        .diff_next {background-color:#c0c0c0}\n        .diff_add {background-color:palegreen}\n        .diff_chg {background-color:#ffff77}\n        .diff_sub {background-color:#ffaaaa}\n\n        @media (prefers-color-scheme: dark) {\n            .diff_header {background-color:#666}\n            .diff_next {background-color:#393939}\n            .diff_add {background-color:darkgreen}\n            .diff_chg {background-color:#847415}\n            .diff_sub {background-color:darkred}\n        }'
_table_template = '\n    <table class="diff" id="difflib_chg_%(prefix)s_top"\n           cellspacing="0" cellpadding="0" rules="groups" >\n        <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>\n        <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>\n        %(header_row)s\n        <tbody>\n%(data_rows)s        </tbody>\n    </table>'
_legend = '\n    <table class="diff" summary="Legends">\n        <tr> <th colspan="2"> Legends </th> </tr>\n        <tr> <td> <table border="" summary="Colors">\n                      <tr><th> Colors </th> </tr>\n                      <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>\n                      <tr><td class="diff_chg">Changed</td> </tr>\n                      <tr><td class="diff_sub">Deleted</td> </tr>\n                  </table></td>\n             <td> <table border="" summary="Links">\n                      <tr><th colspan="2"> Links </th> </tr>\n                      <tr><td>(f)irst change</td> </tr>\n                      <tr><td>(n)ext change</td> </tr>\n                      <tr><td>(t)op</td> </tr>\n                  </table></td> </tr>\n    </table>'

class HTML差异(object):
    """For producing HTML side by side comparison with change highlights.

    This class can be used to create an HTML table (or a complete HTML file
    containing the table) showing a side by side, line by line comparison
    of text with inter-line and intra-line change highlights.  The table can
    be generated in either full or contextual difference mode.

    The following methods are provided for HTML generation:

    make_table -- generates HTML for a single side by side table
    make_file -- generates complete HTML file with a single side by side table

    See tools/scripts/diff.py for an example usage of this class.
    """
    _file_template = _file_template
    _styles = _styles
    _table_template = _table_template
    _legend = _legend
    _default_prefix = 0

    def __init__(self, tabsize=8, wrapcolumn=None, linejunk=None, charjunk=是忽略字符吗):
        """HtmlDiff instance initializer

        Arguments:
        tabsize -- tab stop spacing, defaults to 8.
        wrapcolumn -- column number where lines are broken and wrapped,
            defaults to None where lines are not wrapped.
        linejunk,charjunk -- keyword arguments passed into ndiff() (used by
            HtmlDiff() to generate the side by side HTML differences).  See
            ndiff() documentation for argument default values and descriptions.
        """
        self._tabsize = tabsize
        self._wrapcolumn = wrapcolumn
        self._linejunk = linejunk
        self._charjunk = charjunk

    def 造网页(self, fromlines, tolines, fromdesc='', todesc='', context=False, numlines=5, *, charset='utf-8'):
        """Returns HTML file of side by side comparison with change highlights

        Arguments:
        fromlines -- list of "from" lines
        tolines -- list of "to" lines
        fromdesc -- "from" file column header string
        todesc -- "to" file column header string
        context -- set to True for contextual differences (defaults to False
            which shows full differences).
        numlines -- number of context lines.  When context is set True,
            controls number of lines displayed before and after the change.
            When context is False, controls the number of lines to place
            the "next" link anchors before the next change (so click of
            "next" link jumps to just before the change).
        charset -- charset of the HTML document
        """
        return (self._file_template % dict(styles=self._styles, legend=self._legend, table=self.造表格(fromlines, tolines, fromdesc, todesc, context=context, numlines=numlines), charset=charset)).encode(charset, 'xmlcharrefreplace').decode(charset)

    def _tab_newline_replace(self, fromlines, tolines):
        """Returns from/to line lists with tabs expanded and newlines removed.

        Instead of tab characters being replaced by the number of spaces
        needed to fill in to the next tab stop, this function will fill
        the space with tab characters.  This is done so that the difference
        algorithms can identify changes in a file when tabs are replaced by
        spaces and vice versa.  At the end of the HTML generation, the tab
        characters will be replaced with a nonbreakable space.
        """

        def expand_tabs(line):
            line = line.replace(' ', '\x00')
            line = line.expandtabs(self._tabsize)
            line = line.replace(' ', '\t')
            return line.replace('\x00', ' ').rstrip('\n')
        fromlines = [expand_tabs(line) for line in fromlines]
        tolines = [expand_tabs(line) for line in tolines]
        return (fromlines, tolines)

    def _split_line(self, data_list, line_num, text):
        """Builds list of text lines by splitting text lines at wrap point

        This function will determine if the input text line needs to be
        wrapped (split) into separate lines.  If so, the first wrap point
        will be determined and the first line appended to the output
        text line list.  This function is used recursively to handle
        the second part of the split line to further split it.
        """
        if not line_num:
            data_list.append((line_num, text))
            return
        size = len(text)
        max = self._wrapcolumn
        if size <= max or size - text.count('\x00') * 3 <= max:
            data_list.append((line_num, text))
            return
        i = 0
        n = 0
        mark = ''
        while n < max and i < size:
            if text[i] == '\x00':
                i += 1
                mark = text[i]
                i += 1
            elif text[i] == '\x01':
                i += 1
                mark = ''
            else:
                i += 1
                n += 1
        line1 = text[:i]
        line2 = text[i:]
        if mark:
            line1 = line1 + '\x01'
            line2 = '\x00' + mark + line2
        data_list.append((line_num, line1))
        self._split_line(data_list, '>', line2)

    def _line_wrapper(self, diffs):
        """Returns iterator that splits (wraps) mdiff text lines"""
        for fromdata, todata, flag in diffs:
            if flag is None:
                yield (fromdata, todata, flag)
                continue
            (fromline, fromtext), (toline, totext) = (fromdata, todata)
            fromlist, tolist = ([], [])
            self._split_line(fromlist, fromline, fromtext)
            self._split_line(tolist, toline, totext)
            while fromlist or tolist:
                if fromlist:
                    fromdata = fromlist.pop(0)
                else:
                    fromdata = ('', ' ')
                if tolist:
                    todata = tolist.pop(0)
                else:
                    todata = ('', ' ')
                yield (fromdata, todata, flag)

    def _collect_lines(self, diffs):
        """Collects mdiff output into separate lists

        Before storing the mdiff from/to data into a list, it is converted
        into a single line of text with HTML markup.
        """
        fromlist, tolist, flaglist = ([], [], [])
        for fromdata, todata, flag in diffs:
            try:
                fromlist.append(self._format_line(0, flag, *fromdata))
                tolist.append(self._format_line(1, flag, *todata))
            except TypeError:
                fromlist.append(None)
                tolist.append(None)
            flaglist.append(flag)
        return (fromlist, tolist, flaglist)

    def _format_line(self, side, flag, linenum, text):
        """Returns HTML markup of "from" / "to" text lines

        side -- 0 or 1 indicating "from" or "to" text
        flag -- indicates if difference on line
        linenum -- line number (used for line number column)
        text -- line text to be marked up
        """
        try:
            linenum = '%d' % linenum
            id = ' id="%s%s"' % (self._prefix[side], linenum)
        except TypeError:
            id = ''
        text = text.replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;')
        text = text.replace(' ', '&nbsp;').rstrip()
        return '<td class="diff_header"%s>%s</td><td nowrap="nowrap">%s</td>' % (id, linenum, text)

    def _make_prefix(self):
        """Create unique anchor prefixes"""
        fromprefix = 'from%d_' % HTML差异._default_prefix
        toprefix = 'to%d_' % HTML差异._default_prefix
        HTML差异._default_prefix += 1
        self._prefix = [fromprefix, toprefix]

    def _convert_flags(self, fromlist, tolist, flaglist, context, numlines):
        """Makes list of "next" links"""
        toprefix = self._prefix[1]
        next_id = [''] * len(flaglist)
        next_href = [''] * len(flaglist)
        num_chg, in_change = (0, False)
        last = 0
        for i, flag in enumerate(flaglist):
            if flag:
                if not in_change:
                    in_change = True
                    last = i
                    i = max([0, i - numlines])
                    next_id[i] = ' id="difflib_chg_%s_%d"' % (toprefix, num_chg)
                    num_chg += 1
                    next_href[last] = '<a href="#difflib_chg_%s_%d">n</a>' % (toprefix, num_chg)
            else:
                in_change = False
        if not flaglist:
            flaglist = [False]
            next_id = ['']
            next_href = ['']
            last = 0
            if context:
                fromlist = ['<td></td><td>&nbsp;No Differences Found&nbsp;</td>']
                tolist = fromlist
            else:
                fromlist = tolist = ['<td></td><td>&nbsp;Empty File&nbsp;</td>']
        if not flaglist[0]:
            next_href[0] = '<a href="#difflib_chg_%s_0">f</a>' % toprefix
        next_href[last] = '<a href="#difflib_chg_%s_top">t</a>' % toprefix
        return (fromlist, tolist, flaglist, next_href, next_id)

    def 造表格(self, fromlines, tolines, fromdesc='', todesc='', context=False, numlines=5):
        """Returns HTML table of side by side comparison with change highlights

        Arguments:
        fromlines -- list of "from" lines
        tolines -- list of "to" lines
        fromdesc -- "from" file column header string
        todesc -- "to" file column header string
        context -- set to True for contextual differences (defaults to False
            which shows full differences).
        numlines -- number of context lines.  When context is set True,
            controls number of lines displayed before and after the change.
            When context is False, controls the number of lines to place
            the "next" link anchors before the next change (so click of
            "next" link jumps to just before the change).
        """
        self._make_prefix()
        fromlines, tolines = self._tab_newline_replace(fromlines, tolines)
        if context:
            context_lines = numlines
        else:
            context_lines = None
        diffs = _mdiff(fromlines, tolines, context_lines, linejunk=self._linejunk, charjunk=self._charjunk)
        if self._wrapcolumn:
            diffs = self._line_wrapper(diffs)
        fromlist, tolist, flaglist = self._collect_lines(diffs)
        fromlist, tolist, flaglist, next_href, next_id = self._convert_flags(fromlist, tolist, flaglist, context, numlines)
        s = []
        fmt = '            <tr><td class="diff_next"%s>%s</td>%s' + '<td class="diff_next">%s</td>%s</tr>\n'
        for i in range(len(flaglist)):
            if flaglist[i] is None:
                if i > 0:
                    s.append('        </tbody>        \n        <tbody>\n')
            else:
                s.append(fmt % (next_id[i], next_href[i], fromlist[i], next_href[i], tolist[i]))
        if fromdesc or todesc:
            header_row = '<thead><tr>%s%s%s%s</tr></thead>' % ('<th class="diff_next"><br /></th>', '<th colspan="2" class="diff_header">%s</th>' % fromdesc, '<th class="diff_next"><br /></th>', '<th colspan="2" class="diff_header">%s</th>' % todesc)
        else:
            header_row = ''
        table = self._table_template % dict(data_rows=''.join(s), header_row=header_row, prefix=self._prefix[1])
        return table.replace('\x00+', '<span class="diff_add">').replace('\x00-', '<span class="diff_sub">').replace('\x00^', '<span class="diff_chg">').replace('\x01', '</span>').replace('\t', '&nbsp;')
_装类转发(HTML差异, {'make_file': '造网页', 'make_table': '造表格'}, {'make_file': '造网页', 'make_table': '造表格'})

def 还原(delta, which):
    """
    Generate one of the two sequences that generated a delta.

    Given a `delta` produced by `Differ.compare()` or `ndiff()`, extract
    lines originating from file 1 or 2 (parameter `which`), stripping off line
    prefixes.

    Examples:

    >>> diff = ndiff('one\\ntwo\\nthree\\n'.splitlines(keepends=True),
    ...              'ore\\ntree\\nemu\\n'.splitlines(keepends=True))
    >>> diff = list(diff)
    >>> print(''.join(restore(diff, 1)), end="")
    one
    two
    three
    >>> print(''.join(restore(diff, 2)), end="")
    ore
    tree
    emu
    """
    try:
        tag = {1: '- ', 2: '+ '}[int(which)]
    except KeyError:
        raise ValueError('unknown delta choice (must be 1 or 2): %r' % which) from None
    prefixes = ('  ', tag)
    for line in delta:
        if line[:2] in prefixes:
            yield line[2:]


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Differ': '行差异器',
    'HtmlDiff': 'HTML差异',
    'IS_CHARACTER_JUNK': '是忽略字符吗',
    'IS_LINE_JUNK': '是忽略行吗',
    'Match': '匹配项',
    'SequenceMatcher': '序列比较器',
    'context_diff': '上下文差异',
    'diff_bytes': '字节差异',
    'get_close_matches': '取最相近',
    'ndiff': '逐行差异',
    'restore': '还原',
    'unified_diff': '统一差异',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'HTML差异': {
        'make_file': '造网页',
        'make_table': '造表格',
    },
    '序列比较器': {
        'find_longest_match': '找最长匹配',
        'get_grouped_opcodes': '取分组操作码',
        'get_matching_blocks': '取匹配块',
        'get_opcodes': '取操作码',
        'quick_ratio': '快速相似度',
        'ratio': '相似度',
        'real_quick_ratio': '极快相似度',
        'set_seq1': '设首序列',
        'set_seq2': '设次序列',
        'set_seqs': '设序列',
    },
    '行差异器': {
        'compare': '比较',
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
    'HTML差异': {
        'make_file': '造网页',
        'make_table': '造表格',
    },
    '序列比较器': {
        'b2j': '元素表',
        'bjunk': '忽略集',
        'bpopular': '常见集',
        'find_longest_match': '找最长匹配',
        'fullbcount': '全量计数',
        'get_grouped_opcodes': '取分组操作码',
        'get_matching_blocks': '取匹配块',
        'get_opcodes': '取操作码',
        'matching_blocks': '匹配块表',
        'opcodes': '操作码表',
        'quick_ratio': '快速相似度',
        'ratio': '相似度',
        'real_quick_ratio': '极快相似度',
        'set_seq1': '设首序列',
        'set_seq2': '设次序列',
        'set_seqs': '设序列',
    },
    '行差异器': {
        'compare': '比较',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    'HTML差异',
    '上下文差异',
    '匹配项',
    '取最相近',
    '字节差异',
    '序列比较器',
    '是忽略字符吗',
    '是忽略行吗',
    '统一差异',
    '行差异器',
    '还原',
    '逐行差异',
])

# ---- 转发层结束 ----
