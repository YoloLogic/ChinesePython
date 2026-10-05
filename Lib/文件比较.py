# -*- coding: utf-8 -*-
"""文件比较 —— 汉语库（由 tools/汉化库.py 从 Lib/filecmp.py 机械生成，**不要手改**）。

英文库 Lib/filecmp.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 文件比较
"""


"""Utilities for comparing files and directories.

Classes:
    dircmp

Functions:
    cmp(f1, f2, shallow=True) -> int
    cmpfiles(a, b, common) -> ([], [], [])
    clear_cache()

"""
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
import os
import stat
from itertools import filterfalse
from types import GenericAlias
__all__ = ['clear_cache', 'cmp', 'dircmp', 'cmpfiles', 'DEFAULT_IGNORES']
_cache = {}
缓冲大小 = 8 * 1024
默认忽略 = ['RCS', 'CVS', 'tags', '.git', '.hg', '.bzr', '_darcs', '__pycache__']

def 清缓存():
    """Clear the filecmp cache."""
    _cache.clear()

def 比较文件(f1, f2, shallow=True):
    """Compare two files.

    Arguments:

    f1 -- First file name

    f2 -- Second file name

    shallow -- treat files as identical if their stat signatures (type, size,
               mtime) are identical. Otherwise, files are considered different
               if their sizes or contents differ.  [default: True]

    Return value:

    True if the files are the same, False otherwise.

    This function uses a cache for past comparisons and the results,
    with cache entries invalidated if their stat information
    changes.  The cache may be cleared by calling clear_cache().

    """
    s1 = _sig(os.stat(f1))
    s2 = _sig(os.stat(f2))
    if s1[0] != stat.S_IFREG or s2[0] != stat.S_IFREG:
        return False
    if shallow and s1 == s2:
        return True
    if s1[1] != s2[1]:
        return False
    outcome = _cache.get((f1, f2, s1, s2))
    if outcome is None:
        outcome = _do_cmp(f1, f2)
        if len(_cache) > 100:
            清缓存()
        _cache[f1, f2, s1, s2] = outcome
    return outcome

def _sig(st):
    return (stat.S_IFMT(st.st_mode), st.st_size, st.st_mtime)

def _do_cmp(f1, f2):
    bufsize = 缓冲大小
    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
        while True:
            b1 = fp1.read(bufsize)
            b2 = fp2.read(bufsize)
            if b1 != b2:
                return False
            if not b1:
                return True

class 目录比较:
    """A class that manages the comparison of 2 directories.

    dircmp(a, b, ignore=None, hide=None, *, shallow=True)
      A and B are directories.
      IGNORE is a list of names to ignore,
        defaults to DEFAULT_IGNORES.
      HIDE is a list of names to hide,
        defaults to [os.curdir, os.pardir].
      SHALLOW specifies whether to just check the stat signature (do not read
        the files).
        defaults to True.

    High level usage:
      x = dircmp(dir1, dir2)
      x.report() -> prints a report on the differences between dir1 and dir2
       or
      x.report_partial_closure() -> prints report on differences between dir1
            and dir2, and reports on common immediate subdirectories.
      x.report_full_closure() -> like report_partial_closure,
            but fully recursive.

    Attributes:
     left_list, right_list: The files in dir1 and dir2,
        filtered by hide and ignore.
     common: a list of names in both dir1 and dir2.
     left_only, right_only: names only in dir1, dir2.
     common_dirs: subdirectories in both dir1 and dir2.
     common_files: files in both dir1 and dir2.
     common_funny: names in both dir1 and dir2 where the type differs between
        dir1 and dir2, or the name is not stat-able.
     same_files: list of identical files.
     diff_files: list of filenames which differ.
     funny_files: list of files which could not be compared.
     subdirs: a dictionary of dircmp instances (or MyDirCmp instances if this
       object is of type MyDirCmp, a subclass of dircmp), keyed by names
       in common_dirs.
     """

    def __init__(self, a, b, ignore=None, hide=None, *, shallow=True):
        self.left = a
        self.right = b
        if hide is None:
            self.hide = [os.curdir, os.pardir]
        else:
            self.hide = hide
        if ignore is None:
            self.ignore = 默认忽略
        else:
            self.ignore = ignore
        self.shallow = shallow

    def 阶段0(self):
        self.left_list = _filter(os.listdir(self.left), self.hide + self.ignore)
        self.right_list = _filter(os.listdir(self.right), self.hide + self.ignore)
        self.left_list.sort()
        self.right_list.sort()

    def 阶段1(self):
        a = dict(zip(map(os.path.normcase, self.left_list), self.left_list))
        b = dict(zip(map(os.path.normcase, self.right_list), self.right_list))
        self.common = list(map(a.__getitem__, filter(b.__contains__, a)))
        self.left_only = list(map(a.__getitem__, filterfalse(b.__contains__, a)))
        self.right_only = list(map(b.__getitem__, filterfalse(a.__contains__, b)))

    def 阶段2(self):
        self.common_dirs = []
        self.common_files = []
        self.common_funny = []
        for x in self.common:
            a_path = os.path.join(self.left, x)
            b_path = os.path.join(self.right, x)
            ok = True
            try:
                a_stat = os.stat(a_path)
            except (OSError, ValueError):
                ok = False
            try:
                b_stat = os.stat(b_path)
            except (OSError, ValueError):
                ok = False
            if ok:
                a_type = stat.S_IFMT(a_stat.st_mode)
                b_type = stat.S_IFMT(b_stat.st_mode)
                if a_type != b_type:
                    self.common_funny.append(x)
                elif stat.S_ISDIR(a_type):
                    self.common_dirs.append(x)
                elif stat.S_ISREG(a_type):
                    self.common_files.append(x)
                else:
                    self.common_funny.append(x)
            else:
                self.common_funny.append(x)

    def 阶段3(self):
        xx = 批量比较文件(self.left, self.right, self.common_files, self.shallow)
        self.same_files, self.diff_files, self.funny_files = xx

    def 阶段4(self):
        self.subdirs = {}
        for x in self.common_dirs:
            a_x = os.path.join(self.left, x)
            b_x = os.path.join(self.right, x)
            self.subdirs[x] = self.__class__(a_x, b_x, self.ignore, self.hide, shallow=self.shallow)

    def 阶段4闭包(self):
        self.阶段4()
        for sd in self.subdirs.values():
            sd.phase4_closure()

    def 报告(self):
        print('diff', self.left, self.right)
        if self.left_only:
            self.left_only.sort()
            print('Only in', self.left, ':', self.left_only)
        if self.right_only:
            self.right_only.sort()
            print('Only in', self.right, ':', self.right_only)
        if self.same_files:
            self.same_files.sort()
            print('Identical files :', self.same_files)
        if self.diff_files:
            self.diff_files.sort()
            print('Differing files :', self.diff_files)
        if self.funny_files:
            self.funny_files.sort()
            print('Trouble with common files :', self.funny_files)
        if self.common_dirs:
            self.common_dirs.sort()
            print('Common subdirectories :', self.common_dirs)
        if self.common_funny:
            self.common_funny.sort()
            print('Common funny cases :', self.common_funny)

    def 报告部分闭包(self):
        self.报告()
        for sd in self.subdirs.values():
            print()
            sd.report()

    def 报告全部闭包(self):
        self.报告()
        for sd in self.subdirs.values():
            print()
            sd.report_full_closure()
    methodmap = dict(subdirs=阶段4, same_files=阶段3, diff_files=阶段3, funny_files=阶段3, common_dirs=阶段2, common_files=阶段2, common_funny=阶段2, common=阶段1, left_only=阶段1, right_only=阶段1, left_list=阶段0, right_list=阶段0)

    def __getattr__(self, attr):
        if attr not in self.methodmap:
            raise AttributeError(attr)
        self.methodmap[attr](self)
        return getattr(self, attr)
    __class_getitem__ = classmethod(GenericAlias)
_装类转发(目录比较, {'phase0': '阶段0', 'phase1': '阶段1', 'phase2': '阶段2', 'phase3': '阶段3', 'phase4': '阶段4', 'phase4_closure': '阶段4闭包', 'report': '报告', 'report_full_closure': '报告全部闭包', 'report_partial_closure': '报告部分闭包'}, {'phase0': '阶段0', 'phase1': '阶段1', 'phase2': '阶段2', 'phase3': '阶段3', 'phase4': '阶段4', 'phase4_closure': '阶段4闭包', 'report': '报告', 'report_full_closure': '报告全部闭包', 'report_partial_closure': '报告部分闭包'})

def 批量比较文件(a, b, common, shallow=True):
    """Compare common files in two directories.

    a, b -- directory names
    common -- list of file names found in both directories
    shallow -- if true, do comparison based solely on stat() information

    Returns a tuple of three lists:
      files that compare equal
      files that are different
      filenames that aren't regular files.

    """
    res = ([], [], [])
    for x in common:
        ax = os.path.join(a, x)
        bx = os.path.join(b, x)
        res[_cmp(ax, bx, shallow)].append(x)
    return res

def _cmp(a, b, sh, abs=abs, cmp=比较文件):
    try:
        return not abs(cmp(a, b, sh))
    except (OSError, ValueError):
        return 2

def _filter(flist, skip):
    return list(filterfalse(skip.__contains__, flist))

def 演示():
    import sys
    import getopt
    options, args = getopt.getopt(sys.argv[1:], 'r')
    if len(args) != 2:
        raise getopt.GetoptError('need exactly two args', None)
    dd = 目录比较(args[0], args[1])
    if ('-r', '') in options:
        dd.report_full_closure()
    else:
        dd.report()
if __name__ == '__main__':
    演示()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BUFSIZE': '缓冲大小',
    'DEFAULT_IGNORES': '默认忽略',
    'clear_cache': '清缓存',
    'cmp': '比较文件',
    'cmpfiles': '批量比较文件',
    'demo': '演示',
    'dircmp': '目录比较',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '目录比较': {
        'phase0': '阶段0',
        'phase1': '阶段1',
        'phase2': '阶段2',
        'phase3': '阶段3',
        'phase4': '阶段4',
        'phase4_closure': '阶段4闭包',
        'report': '报告',
        'report_full_closure': '报告全部闭包',
        'report_partial_closure': '报告部分闭包',
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
    '目录比较': {
        'phase0': '阶段0',
        'phase1': '阶段1',
        'phase2': '阶段2',
        'phase3': '阶段3',
        'phase4': '阶段4',
        'phase4_closure': '阶段4闭包',
        'report': '报告',
        'report_full_closure': '报告全部闭包',
        'report_partial_closure': '报告部分闭包',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '批量比较文件',
    '比较文件',
    '清缓存',
    '目录比较',
    '默认忽略',
])

# ---- 转发层结束 ----
