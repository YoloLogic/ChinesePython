# -*- coding: utf-8 -*-
"""单元测试.runner —— 汉语库（由 tools/汉化库.py 从 Lib/unittest/runner.py 机械生成，**不要手改**）。

英文库 Lib/unittest.runner.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py unittest
"""


"""Running tests"""
import sys
import time
import warnings
from _colorize import get_theme
from . import result
from .case import _SubTest
from .signals import registerResult
__unittest = True

class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""

    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream, attr)

    def writeln(self, arg=None):
        if arg:
            self.write(arg)
        self.write('\n')

class 文本测试结果(result.TestResult):
    """A test result class that can print formatted text results to a stream.

    Used by TextTestRunner.
    """
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, stream, descriptions, verbosity, *, durations=None):
        """Construct a TextTestResult. Subclasses should accept **kwargs
        to ensure compatibility as the interface changes."""
        super(文本测试结果, self).__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions
        self._theme = get_theme(tty_file=stream).unittest
        self._newline = True
        self.durations = durations

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        else:
            return str(test)

    def startTest(self, test):
        super(文本测试结果, self).startTest(test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(' ... ')
            self.stream.flush()
            self._newline = False

    def _write_status(self, test, status):
        is_subtest = isinstance(test, _SubTest)
        if is_subtest or self._newline:
            if not self._newline:
                self.stream.writeln()
            if is_subtest:
                self.stream.write('  ')
            self.stream.write(self.getDescription(test))
            self.stream.write(' ... ')
        self.stream.writeln(status)
        self.stream.flush()
        self._newline = True

    def addSubTest(self, test, subtest, err):
        if err is not None:
            t = self._theme
            if self.showAll:
                if issubclass(err[0], subtest.failureException):
                    self._write_status(subtest, f'{t.fail}FAIL{t.reset}')
                else:
                    self._write_status(subtest, f'{t.fail}ERROR{t.reset}')
            elif self.dots:
                if issubclass(err[0], subtest.failureException):
                    self.stream.write(f'{t.fail}F{t.reset}')
                else:
                    self.stream.write(f'{t.fail}E{t.reset}')
                self.stream.flush()
        super(文本测试结果, self).addSubTest(test, subtest, err)

    def addSuccess(self, test):
        super(文本测试结果, self).addSuccess(test)
        t = self._theme
        if self.showAll:
            self._write_status(test, f'{t.passed}ok{t.reset}')
        elif self.dots:
            self.stream.write(f'{t.passed}.{t.reset}')
            self.stream.flush()

    def addError(self, test, err):
        super(文本测试结果, self).addError(test, err)
        t = self._theme
        if self.showAll:
            self._write_status(test, f'{t.fail}ERROR{t.reset}')
        elif self.dots:
            self.stream.write(f'{t.fail}E{t.reset}')
            self.stream.flush()

    def addFailure(self, test, err):
        super(文本测试结果, self).addFailure(test, err)
        t = self._theme
        if self.showAll:
            self._write_status(test, f'{t.fail}FAIL{t.reset}')
        elif self.dots:
            self.stream.write(f'{t.fail}F{t.reset}')
            self.stream.flush()

    def addSkip(self, test, reason):
        super(文本测试结果, self).addSkip(test, reason)
        t = self._theme
        if self.showAll:
            self._write_status(test, f'{t.warn}skipped{t.reset} {reason!r}')
        elif self.dots:
            self.stream.write(f'{t.warn}s{t.reset}')
            self.stream.flush()

    def addExpectedFailure(self, test, err):
        super(文本测试结果, self).addExpectedFailure(test, err)
        t = self._theme
        if self.showAll:
            self.stream.writeln(f'{t.warn}expected failure{t.reset}')
            self.stream.flush()
        elif self.dots:
            self.stream.write(f'{t.warn}x{t.reset}')
            self.stream.flush()

    def addUnexpectedSuccess(self, test):
        super(文本测试结果, self).addUnexpectedSuccess(test)
        t = self._theme
        if self.showAll:
            self.stream.writeln(f'{t.fail}unexpected success{t.reset}')
            self.stream.flush()
        elif self.dots:
            self.stream.write(f'{t.fail}u{t.reset}')
            self.stream.flush()

    def printErrors(self):
        t = self._theme
        if self.dots or self.showAll:
            self.stream.writeln()
            self.stream.flush()
        self.printErrorList(f'{t.fail}ERROR{t.reset}', self.errors)
        self.printErrorList(f'{t.fail}FAIL{t.reset}', self.failures)
        unexpectedSuccesses = getattr(self, 'unexpectedSuccesses', ())
        if unexpectedSuccesses:
            self.stream.writeln(self.separator1)
            for test in unexpectedSuccesses:
                self.stream.writeln(f'{t.fail}UNEXPECTED SUCCESS{t.fail_info}: {self.getDescription(test)}{t.reset}')
            self.stream.flush()

    def printErrorList(self, flavour, errors):
        t = self._theme
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln(f'{flavour}{t.fail_info}: {self.getDescription(test)}{t.reset}')
            self.stream.writeln(self.separator2)
            self.stream.writeln('%s' % err)
            self.stream.flush()

class 文本测试运行器(object):
    """A test runner class that displays results in textual form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    """
    resultclass = 文本测试结果

    def __init__(self, stream=None, descriptions=True, verbosity=1, failfast=False, buffer=False, resultclass=None, warnings=None, *, tb_locals=False, durations=None):
        """Construct a TextTestRunner.

        Subclasses should accept **kwargs to ensure compatibility as the
        interface changes.
        """
        if stream is None:
            stream = sys.stderr
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        self.tb_locals = tb_locals
        self.durations = durations
        self.warnings = warnings
        if resultclass is not None:
            self.resultclass = resultclass

    def _makeResult(self):
        try:
            return self.resultclass(self.stream, self.descriptions, self.verbosity, durations=self.durations)
        except TypeError:
            return self.resultclass(self.stream, self.descriptions, self.verbosity)

    def _printDurations(self, result):
        if not result.collectedDurations:
            return
        ls = sorted(result.collectedDurations, key=lambda x: x[1], reverse=True)
        if self.durations > 0:
            ls = ls[:self.durations]
        self.stream.writeln('Slowest test durations')
        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)
        hidden = False
        for test, elapsed in ls:
            if self.verbosity < 2 and elapsed < 0.001:
                hidden = True
                continue
            self.stream.writeln('%-10s %s' % ('%.3fs' % elapsed, test))
        if hidden:
            self.stream.writeln('\n(durations < 0.001s were hidden; use -v to show these durations)')
        else:
            self.stream.writeln('')

    def run(self, test):
        """Run the given test case or test suite."""
        result = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        result.tb_locals = self.tb_locals
        with warnings.catch_warnings():
            if self.warnings:
                warnings.simplefilter(self.warnings)
            start_time = time.perf_counter()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()
            try:
                test(result)
            finally:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()
            stop_time = time.perf_counter()
        time_taken = stop_time - start_time
        result.printErrors()
        if self.durations is not None:
            self._printDurations(result)
        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)
        run = result.testsRun
        self.stream.writeln('Ran %d test%s in %.3fs' % (run, run != 1 and 's' or '', time_taken))
        self.stream.writeln()
        expected_fails = unexpected_successes = skipped = 0
        try:
            results = map(len, (result.expectedFailures, result.unexpectedSuccesses, result.skipped))
        except AttributeError:
            pass
        else:
            expected_fails, unexpected_successes, skipped = results
        infos = []
        t = get_theme(tty_file=self.stream).unittest
        if not result.wasSuccessful():
            self.stream.write(f'{t.fail_info}FAILED{t.reset}')
            failed, errored = (len(result.failures), len(result.errors))
            if failed:
                infos.append(f'{t.fail_info}failures={failed}{t.reset}')
            if errored:
                infos.append(f'{t.fail_info}errors={errored}{t.reset}')
        elif run == 0 and (not skipped):
            self.stream.write(f'{t.warn}NO TESTS RAN{t.reset}')
        else:
            self.stream.write(f'{t.passed}OK{t.reset}')
        if skipped:
            infos.append(f'{t.warn}skipped={skipped}{t.reset}')
        if expected_fails:
            infos.append(f'{t.warn}expected failures={expected_fails}{t.reset}')
        if unexpected_successes:
            infos.append(f'{t.fail}unexpected successes={unexpected_successes}{t.reset}')
        if infos:
            self.stream.writeln(' (%s)' % (', '.join(infos),))
        else:
            self.stream.write('\n')
        self.stream.flush()
        return result


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'TextTestResult': '文本测试结果',
    'TextTestRunner': '文本测试运行器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
