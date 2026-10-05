# -*- coding: utf-8 -*-
"""单元测试.result —— 汉语库（由 tools/汉化库.py 从 Lib/unittest/result.py 机械生成，**不要手改**）。

英文库 Lib/unittest.result.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py unittest
"""


"""Test result object"""
_英文原名表 = {'STDERR_LINE': '标准错误行', 'STDOUT_LINE': '标准输出行', 'TestResult': '测试结果', 'failfast': '快速失败'}

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
import sys
import traceback
from . import util
from functools import wraps
__unittest = True

def 快速失败(method):

    @wraps(method)
    def inner(self, *args, **kw):
        if getattr(self, 'failfast', False):
            self.stop()
        return method(self, *args, **kw)
    return inner
标准输出行 = '\nStdout:\n%s'
标准错误行 = '\nStderr:\n%s'

class 测试结果(object):
    """Holder for test result information.

    Test results are automatically managed by the TestCase and TestSuite
    classes, and do not need to be explicitly manipulated by writers of tests.

    Each instance holds the total number of tests run, and collections of
    failures and errors that occurred among those test runs. The collections
    contain tuples of (testcase, exceptioninfo), where exceptioninfo is the
    formatted traceback of the error that occurred.
    """
    _previousTestClass = None
    _testRunEntered = False
    _moduleSetUpFailed = False

    def __init__(self, stream=None, descriptions=None, verbosity=None):
        self.快速失败 = False
        self.failures = []
        self.errors = []
        self.testsRun = 0
        self.skipped = []
        self.expectedFailures = []
        self.unexpectedSuccesses = []
        self.collectedDurations = []
        self.shouldStop = False
        self.buffer = False
        self.tb_locals = False
        self._stdout_buffer = None
        self._stderr_buffer = None
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._mirrorOutput = False

    def printErrors(self):
        """Called by TestRunner after test run"""

    def startTest(self, test):
        """Called when the given test is about to be run"""
        self.testsRun += 1
        self._mirrorOutput = False
        self._setupStdout()

    def _setupStdout(self):
        if self.buffer:
            if self._stderr_buffer is None:
                self._stderr_buffer = io.StringIO()
                self._stdout_buffer = io.StringIO()
            sys.stdout = self._stdout_buffer
            sys.stderr = self._stderr_buffer

    def startTestRun(self):
        """Called once before any tests are executed.

        See startTest for a method called before each test.
        """

    def stopTest(self, test):
        """Called when the given test has been run"""
        self._restoreStdout()
        self._mirrorOutput = False

    def _restoreStdout(self):
        if self.buffer:
            if self._mirrorOutput:
                output = sys.stdout.getvalue()
                error = sys.stderr.getvalue()
                if output:
                    if not output.endswith('\n'):
                        output += '\n'
                    self._original_stdout.write(标准输出行 % output)
                if error:
                    if not error.endswith('\n'):
                        error += '\n'
                    self._original_stderr.write(标准错误行 % error)
            sys.stdout = self._original_stdout
            sys.stderr = self._original_stderr
            self._stdout_buffer.seek(0)
            self._stdout_buffer.truncate()
            self._stderr_buffer.seek(0)
            self._stderr_buffer.truncate()

    def stopTestRun(self):
        """Called once after all tests are executed.

        See stopTest for a method called after each test.
        """

    @快速失败
    def addError(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info().
        """
        self.errors.append((test, self._exc_info_to_string(err, test)))
        self._mirrorOutput = True

    @快速失败
    def addFailure(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info()."""
        self.failures.append((test, self._exc_info_to_string(err, test)))
        self._mirrorOutput = True

    def addSubTest(self, test, subtest, err):
        """Called at the end of a subtest.
        'err' is None if the subtest ended successfully, otherwise it's a
        tuple of values as returned by sys.exc_info().
        """
        if err is not None:
            if getattr(self, 'failfast', False):
                self.stop()
            if issubclass(err[0], test.failureException):
                errors = self.failures
            else:
                errors = self.errors
            errors.append((subtest, self._exc_info_to_string(err, test)))
            self._mirrorOutput = True

    def addSuccess(self, test):
        """Called when a test has completed successfully"""
        pass

    def addSkip(self, test, reason):
        """Called when a test is skipped."""
        self.skipped.append((test, reason))

    def addExpectedFailure(self, test, err):
        """Called when an expected failure/error occurred."""
        self.expectedFailures.append((test, self._exc_info_to_string(err, test)))

    @快速失败
    def addUnexpectedSuccess(self, test):
        """Called when a test was expected to fail, but succeed."""
        self.unexpectedSuccesses.append(test)

    def addDuration(self, test, elapsed):
        """Called when a test finished to run, regardless of its outcome.
        *test* is the test case corresponding to the test method.
        *elapsed* is the time represented in seconds, and it includes the
        execution of cleanup functions.
        """
        if hasattr(self, 'collectedDurations'):
            self.collectedDurations.append((str(test), elapsed))

    def wasSuccessful(self):
        """Tells whether or not this result was a success."""
        return len(self.failures) == len(self.errors) == 0 and (not hasattr(self, 'unexpectedSuccesses') or len(self.unexpectedSuccesses) == 0)

    def stop(self):
        """Indicates that the tests should be aborted."""
        self.shouldStop = True

    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        exctype, value, tb = err
        tb = self._clean_tracebacks(exctype, value, tb, test)
        tb_e = traceback.TracebackException(exctype, value, tb, capture_locals=self.tb_locals, compact=True)
        from _colorize import can_colorize
        colorize = hasattr(self, 'stream') and can_colorize(file=self.stream)
        msgLines = list(tb_e.format(colorize=colorize))
        if self.buffer:
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()
            if output:
                if not output.endswith('\n'):
                    output += '\n'
                msgLines.append(标准输出行 % output)
            if error:
                if not error.endswith('\n'):
                    error += '\n'
                msgLines.append(标准错误行 % error)
        return ''.join(msgLines)

    def _clean_tracebacks(self, exctype, value, tb, test):
        ret = None
        first = True
        excs = [(exctype, value, tb)]
        seen = {id(value)}
        while excs:
            exctype, value, tb = excs.pop()
            while tb and self._is_relevant_tb_level(tb):
                tb = tb.tb_next
            if exctype is test.failureException:
                self._remove_unittest_tb_frames(tb)
            if first:
                ret = tb
                first = False
            else:
                value.__traceback__ = tb
            if value is not None:
                for c in (value.__cause__, value.__context__):
                    if c is not None and id(c) not in seen:
                        excs.append((type(c), c, c.__traceback__))
                        seen.add(id(c))
        return ret

    def _is_relevant_tb_level(self, tb):
        return '__unittest' in tb.tb_frame.f_globals

    def _remove_unittest_tb_frames(self, tb):
        """Truncates usercode tb at the first unittest frame.

        If the first frame of the traceback is in user code,
        the prefix up to the first unittest frame is returned.
        If the first frame is already in the unittest module,
        the traceback is not modified.
        """
        prev = None
        while tb and (not self._is_relevant_tb_level(tb)):
            prev = tb
            tb = tb.tb_next
        if prev is not None:
            prev.tb_next = None

    def __repr__(self):
        return '<%s run=%i errors=%i failures=%i>' % (util.strclass(self.__class__), self.testsRun, len(self.errors), len(self.failures))
_装类转发(测试结果, {}, {'failfast': '快速失败'})


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'STDERR_LINE': '标准错误行',
    'STDOUT_LINE': '标准输出行',
    'TestResult': '测试结果',
    'failfast': '快速失败',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# 实例属性：两个方向都翻（英文名 <-> 中文名）。
# **逻辑只有一份**，在 `_装类转发` 里 —— 每个类定义紧后面已经装过一次
# （照 D-040），这里是文件末尾的兜底，幂等。
_实例属性 = {
    '测试结果': {
        'failfast': '快速失败',
    },
}
_成员别名 = {}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
