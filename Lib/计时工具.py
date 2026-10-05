# -*- coding: utf-8 -*-
"""计时工具 —— 汉语库（由 tools/汉化库.py 从 Lib/timeit.py 机械生成，**不要手改**）。

英文库 Lib/timeit.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 计时工具
"""


"""Tool for measuring execution time of small code snippets.

This module avoids a number of common traps for measuring execution
times.  See also Tim Peters' introduction to the Algorithms chapter in
the Python Cookbook, published by O'Reilly.

Library usage: see the Timer class.

Command line usage:
    python timeit.py [-n N] [-r N] [-s S] [-p] [-h] [--] [statement]

Options:
  -n/--number N: how many times to execute 'statement' (default: see below)
  -r/--repeat N: how many times to repeat the timer (default 5)
  -s/--setup S: statement to be executed once initially (default 'pass').
                Execution time of this setup statement is NOT timed.
  -p/--process: use time.process_time() (default is time.perf_counter())
  -v/--verbose: print raw timing results; repeat for more digits precision
  -u/--unit: set the output time unit (nsec, usec, msec, or sec)
  -h/--help: print this usage message and exit
  --: separate options from statement, use when statement starts with -
  statement: statement to be timed (default 'pass')

A multi-line statement may be given by specifying each line as a
separate argument; indented lines are possible by enclosing an
argument in quotes and using leading spaces.  Multiple -s options are
treated similarly.

If -n is not given, a suitable number of loops is calculated by trying
increasing numbers from the sequence 1, 2, 5, 10, 20, 50, ... until the
total time is at least 0.2 seconds.

Note: there is a certain baseline overhead associated with executing a
pass statement.  It differs between versions.  The code here doesn't try
to hide it, but you should be aware of it.  The baseline overhead can be
measured by invoking the program without arguments.

Classes:

    Timer

Functions:

    timeit(string, string) -> float
    repeat(string, string) -> list
    default_timer() -> float
"""
_英文原名表 = {'Timer': '计时器', 'default_number': '默认次数', 'default_repeat': '默认重复次数', 'default_timer': '默认计时器', 'dummy_src_name': '虚拟源码名', 'main': '主函数', 'reindent': '重排缩进', 'repeat': '重复次数', 'template': '模板', 'timeit': '计时'}

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
import gc
import itertools
import sys
import time
__all__ = ['Timer', 'timeit', 'repeat', 'default_timer']
虚拟源码名 = '<timeit-src>'
默认次数 = 1000000
默认重复次数 = 5
默认计时器 = time.perf_counter
_globals = globals
模板 = '\ndef inner(_it, _timer{init}):\n    {setup}\n    _t0 = _timer()\n    for _i in _it:\n        {stmt}\n        pass\n    _t1 = _timer()\n    return _t1 - _t0\n'

def 重排缩进(src, indent):
    """Helper to reindent a multi-line statement."""
    return src.replace('\n', '\n' + ' ' * indent)

class 计时器:
    """Class for timing execution speed of small code snippets.

    The constructor takes a statement to be timed, an additional
    statement used for setup, and a timer function.  Both statements
    default to 'pass'; the timer function is platform-dependent (see
    module doc string).  If 'globals' is specified, the code will be
    executed within that namespace (as opposed to inside timeit's
    namespace).

    To measure the execution time of the first statement, use the
    timeit() method.  The repeat() method is a convenience to call
    timeit() multiple times and return a list of results.

    The statements may contain newlines, as long as they don't contain
    multi-line string literals.
    """

    def __init__(self, stmt='pass', setup='pass', timer=默认计时器, globals=None):
        """Constructor.  See class doc string."""
        self.timer = timer
        local_ns = {}
        global_ns = _globals() if globals is None else globals
        init = ''
        if isinstance(setup, str):
            compile(setup, 虚拟源码名, 'exec')
            stmtprefix = setup + '\n'
            setup = 重排缩进(setup, 4)
        elif callable(setup):
            local_ns['_setup'] = setup
            init += ', _setup=_setup'
            stmtprefix = ''
            setup = '_setup()'
        else:
            raise ValueError('setup is neither a string nor callable')
        if isinstance(stmt, str):
            compile(stmtprefix + stmt, 虚拟源码名, 'exec')
            stmt = 重排缩进(stmt, 8)
        elif callable(stmt):
            local_ns['_stmt'] = stmt
            init += ', _stmt=_stmt'
            stmt = '_stmt()'
        else:
            raise ValueError('stmt is neither a string nor callable')
        src = 模板.format(stmt=stmt, setup=setup, init=init)
        self.src = src
        code = compile(src, 虚拟源码名, 'exec')
        exec(code, global_ns, local_ns)
        self.inner = local_ns['inner']

    def 打印异常(self, file=None):
        """Helper to print a traceback from the timed code.

        Typical use:

            t = Timer(...)       # outside the try/except
            try:
                t.timeit(...)    # or t.repeat(...)
            except:
                t.print_exc()

        The advantage over the standard traceback is that source lines
        in the compiled template will be displayed.

        The optional file argument directs where the traceback is
        sent; it defaults to sys.stderr.
        """
        import linecache, traceback
        if self.src is not None:
            linecache.cache[虚拟源码名] = (len(self.src), None, self.src.split('\n'), 虚拟源码名)
        traceback.print_exc(file=file)

    def 计时(self, number=默认次数):
        """Time 'number' executions of the main statement.

        To be precise, this executes the setup statement once, and
        then returns the time it takes to execute the main statement
        a number of times, as float seconds if using the default timer.   The
        argument is the number of times through the loop, defaulting
        to one million.  The main statement, the setup statement and
        the timer function to be used are passed to the constructor.
        """
        it = itertools.repeat(None, number)
        gcold = gc.isenabled()
        gc.disable()
        try:
            timing = self.inner(it, self.timer)
        finally:
            if gcold:
                gc.enable()
        return timing

    def 重复次数(self, repeat=默认重复次数, number=默认次数):
        """Call timeit() a few times.

        This is a convenience function that calls the timeit()
        repeatedly, returning a list of results.  The first argument
        specifies how many times to call timeit(), defaulting to 5;
        the second argument specifies the timer argument, defaulting
        to one million.

        Note: it's tempting to calculate mean and standard deviation
        from the result vector and report these.  However, this is not
        very useful.  In a typical case, the lowest value gives a
        lower bound for how fast your machine can run the given code
        snippet; higher values in the result vector are typically not
        caused by variability in Python's speed, but by other
        processes interfering with your timing accuracy.  So the min()
        of the result is probably the only number you should be
        interested in.  After that, you should look at the entire
        vector and apply common sense rather than statistics.
        """
        r = []
        for i in range(repeat):
            t = self.计时(number)
            r.append(t)
        return r

    def 自动定次(self, callback=None):
        """Return the number of loops and time taken so that total time >= 0.2.

        Calls the timeit method with increasing numbers from the sequence
        1, 2, 5, 10, 20, 50, ... until the time taken is at least 0.2
        second.  Returns (number, time_taken).

        If *callback* is given and is not None, it will be called after
        each trial with two arguments: ``callback(number, time_taken)``.
        """
        i = 1
        while True:
            for j in (1, 2, 5):
                number = i * j
                time_taken = self.计时(number)
                if callback:
                    callback(number, time_taken)
                if time_taken >= 0.2:
                    return (number, time_taken)
            i *= 10
_装类转发(计时器, {'autorange': '自动定次', 'print_exc': '打印异常', 'repeat': '重复次数', 'timeit': '计时'}, {'autorange': '自动定次', 'print_exc': '打印异常', 'repeat': '重复次数', 'timeit': '计时'})

def 计时(stmt='pass', setup='pass', timer=默认计时器, number=默认次数, globals=None):
    """Convenience function to create Timer object and call timeit method."""
    return 计时器(stmt, setup, timer, globals).timeit(number)

def 重复次数(stmt='pass', setup='pass', timer=默认计时器, repeat=默认重复次数, number=默认次数, globals=None):
    """Convenience function to create Timer object and call repeat method."""
    return 计时器(stmt, setup, timer, globals).repeat(repeat, number)

def 主函数(args=None, *, _wrap_timer=None):
    """Main program, used when run as a script.

    The optional 'args' argument specifies the command line to be parsed,
    defaulting to sys.argv[1:].

    The return value is an exit code to be passed to sys.exit(); it
    may be None to indicate success.

    When an exception happens during timing, a traceback is printed to
    stderr and the return value is 1.  Exceptions at other times
    (including the template compilation) are not caught.

    '_wrap_timer' is an internal interface used for unit testing.  If it
    is not None, it must be a callable that accepts a timer function
    and returns another timer function (used for unit testing).
    """
    if args is None:
        args = sys.argv[1:]
    import getopt
    try:
        opts, args = getopt.getopt(args, 'n:u:s:r:pvh', ['number=', 'setup=', 'repeat=', 'process', 'verbose', 'unit=', 'help'])
    except getopt.error as err:
        print(err)
        print('use -h/--help for command line help')
        return 2
    timer = 默认计时器
    stmt = '\n'.join(args) or 'pass'
    number = 0
    setup = []
    重复次数 = 默认重复次数
    verbose = 0
    time_unit = None
    units = {'nsec': 1e-09, 'usec': 1e-06, 'msec': 0.001, 'sec': 1.0}
    precision = 3
    for o, a in opts:
        if o in ('-n', '--number'):
            number = int(a)
        if o in ('-s', '--setup'):
            setup.append(a)
        if o in ('-u', '--unit'):
            if a in units:
                time_unit = a
            else:
                print('Unrecognized unit. Please select nsec, usec, msec, or sec.', file=sys.stderr)
                return 2
        if o in ('-r', '--repeat'):
            重复次数 = int(a)
            if 重复次数 <= 0:
                重复次数 = 1
        if o in ('-p', '--process'):
            timer = time.process_time
        if o in ('-v', '--verbose'):
            if verbose:
                precision += 1
            verbose += 1
        if o in ('-h', '--help'):
            print(__doc__, end='')
            return 0
    setup = '\n'.join(setup) or 'pass'
    import os
    sys.path.insert(0, os.curdir)
    if _wrap_timer is not None:
        timer = _wrap_timer(timer)
    t = 计时器(stmt, setup, timer)
    if number == 0:
        callback = None
        if verbose:

            def callback(number, time_taken):
                msg = '{num} loop{s} -> {secs:.{prec}g} sec'
                plural = number != 1
                print(msg.format(num=number, s='s' if plural else '', secs=time_taken, prec=precision))
        try:
            number, _ = t.autorange(callback)
        except:
            t.print_exc()
            return 1
        if verbose:
            print()
    try:
        raw_timings = t.repeat(重复次数, number)
    except:
        t.print_exc()
        return 1

    def format_time(dt):
        unit = time_unit
        if unit is not None:
            scale = units[unit]
        else:
            scales = [(scale, unit) for unit, scale in units.items()]
            scales.sort(reverse=True)
            for scale, unit in scales:
                if dt >= scale:
                    break
        return '%.*g %s' % (precision, dt / scale, unit)
    if verbose:
        print('raw times: %s' % ', '.join(map(format_time, raw_timings)))
        print()
    timings = [dt / number for dt in raw_timings]
    best = min(timings)
    print('%d loop%s, best of %d: %s per loop' % (number, 's' if number != 1 else '', 重复次数, format_time(best)))
    best = min(timings)
    worst = max(timings)
    if worst >= best * 4:
        import warnings
        warnings.warn_explicit('The test results are likely unreliable. The worst time (%s) was more than four times slower than the best time (%s).' % (format_time(worst), format_time(best)), UserWarning, '', 0)
    return None
if __name__ == '__main__':
    sys.exit(主函数())


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Timer': '计时器',
    'default_number': '默认次数',
    'default_repeat': '默认重复次数',
    'default_timer': '默认计时器',
    'dummy_src_name': '虚拟源码名',
    'main': '主函数',
    'reindent': '重排缩进',
    'repeat': '重复次数',
    'template': '模板',
    'timeit': '计时',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '计时器': {
        'autorange': '自动定次',
        'print_exc': '打印异常',
        'repeat': '重复次数',
        'timeit': '计时',
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
    '计时器': {
        'autorange': '自动定次',
        'print_exc': '打印异常',
        'repeat': '重复次数',
        'timeit': '计时',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '计时',
    '计时器',
    '重复次数',
    '默认计时器',
])

# ---- 转发层结束 ----
