# -*- coding: utf-8 -*-
"""单元测试.main —— 汉语库（由 tools/汉化库.py 从 Lib/unittest/main.py 机械生成，**不要手改**）。

英文库 Lib/unittest.main.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py unittest
"""


"""Unittest main program"""
_英文原名表 = {'MAIN_EXAMPLES': '主程序示例', 'MODULE_EXAMPLES': '模块示例', 'TestProgram': '测试程序', 'main': '主函数'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import sys
import argparse
import os
from . import loader, runner
from .signals import installHandler
__unittest = True
_NO_TESTS_EXITCODE = 5
主程序示例 = 'Examples:\n  %(prog)s test_module               - run tests from test_module\n  %(prog)s module.TestClass          - run tests from module.TestClass\n  %(prog)s module.Class.test_method  - run specified test method\n  %(prog)s path/to/test_file.py      - run tests from test_file.py\n'
模块示例 = "Examples:\n  %(prog)s                           - run default set of tests\n  %(prog)s MyTestSuite               - run suite 'MyTestSuite'\n  %(prog)s MyTestCase.testSomething  - run MyTestCase.testSomething\n  %(prog)s MyTestCase                - run all 'test*' test methods\n                                       in MyTestCase\n"

def _convert_name(name):
    if os.path.isfile(name) and name.lower().endswith('.py'):
        if os.path.isabs(name):
            rel_path = os.path.relpath(name, os.getcwd())
            if os.path.isabs(rel_path) or rel_path.startswith(os.pardir):
                return name
            name = rel_path
        return os.path.normpath(name)[:-3].replace('\\', '.').replace('/', '.')
    return name

def _convert_names(names):
    return [_convert_name(name) for name in names]

def _convert_select_pattern(pattern):
    if not '*' in pattern:
        pattern = '*%s*' % pattern
    return pattern

class 测试程序(object):
    """A command-line program that runs a set of tests; this is primarily
       for making test modules conveniently executable.
    """
    module = None
    verbosity = 1
    failfast = catchbreak = buffer = progName = warnings = testNamePatterns = None
    _discovery_parser = None

    def __init__(self, module='__main__', defaultTest=None, argv=None, testRunner=None, testLoader=loader.defaultTestLoader, exit=True, verbosity=1, failfast=None, catchbreak=None, buffer=None, warnings=None, *, tb_locals=False, durations=None):
        if isinstance(module, str):
            self.module = __import__(module)
            for part in module.split('.')[1:]:
                self.module = getattr(self.module, part)
        else:
            self.module = module
        if argv is None:
            argv = sys.argv
        self.exit = exit
        self.failfast = failfast
        self.catchbreak = catchbreak
        self.verbosity = verbosity
        self.buffer = buffer
        self.tb_locals = tb_locals
        self.durations = durations
        if warnings is None and (not sys.warnoptions):
            self.warnings = 'default'
        else:
            self.warnings = warnings
        self.defaultTest = defaultTest
        self.testRunner = testRunner
        self.testLoader = testLoader
        self.progName = os.path.basename(argv[0])
        self.parseArgs(argv)
        self.runTests()

    def _print_help(self, *args, **kwargs):
        if self.module is None:
            print(self._main_parser.format_help())
            print(主程序示例 % {'prog': self.progName})
            self._discovery_parser.print_help()
        else:
            print(self._main_parser.format_help())
            print(模块示例 % {'prog': self.progName})

    def parseArgs(self, argv):
        self._initArgParsers()
        if self.module is None:
            if len(argv) > 1 and argv[1].lower() == 'discover':
                self._do_discovery(argv[2:])
                return
            self._main_parser.parse_args(argv[1:], self)
            if not self.tests:
                self._do_discovery([])
                return
        else:
            self._main_parser.parse_args(argv[1:], self)
        if self.tests:
            self.testNames = _convert_names(self.tests)
            if __name__ == '__main__':
                self.module = None
        elif self.defaultTest is None:
            self.testNames = None
        elif isinstance(self.defaultTest, str):
            self.testNames = (self.defaultTest,)
        else:
            self.testNames = list(self.defaultTest)
        self.createTests()

    def createTests(self, from_discovery=False, Loader=None):
        if self.testNamePatterns:
            self.testLoader.testNamePatterns = self.testNamePatterns
        if from_discovery:
            loader = self.testLoader if Loader is None else Loader()
            self.test = loader.discover(self.start, self.pattern, self.top)
        elif self.testNames is None:
            self.test = self.testLoader.loadTestsFromModule(self.module)
        else:
            self.test = self.testLoader.loadTestsFromNames(self.testNames, self.module)

    def _initArgParsers(self):
        parent_parser = self._getParentArgParser()
        self._main_parser = self._getMainArgParser(parent_parser)
        self._discovery_parser = self._getDiscoveryArgParser(parent_parser)

    def _getParentArgParser(self):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-v', '--verbose', dest='verbosity', action='store_const', const=2, help='Verbose output')
        parser.add_argument('-q', '--quiet', dest='verbosity', action='store_const', const=0, help='Quiet output')
        parser.add_argument('--locals', dest='tb_locals', action='store_true', help='Show local variables in tracebacks')
        parser.add_argument('--durations', dest='durations', type=int, default=None, metavar='N', help='Show the N slowest test cases (N=0 for all)')
        if self.failfast is None:
            parser.add_argument('-f', '--failfast', dest='failfast', action='store_true', help='Stop on first fail or error')
            self.failfast = False
        if self.catchbreak is None:
            parser.add_argument('-c', '--catch', dest='catchbreak', action='store_true', help='Catch Ctrl-C and display results so far')
            self.catchbreak = False
        if self.buffer is None:
            parser.add_argument('-b', '--buffer', dest='buffer', action='store_true', help='Buffer stdout and stderr during tests')
            self.buffer = False
        if self.testNamePatterns is None:
            parser.add_argument('-k', dest='testNamePatterns', action='append', type=_convert_select_pattern, help='Only run tests which match the given substring')
            self.testNamePatterns = []
        return parser

    def _getMainArgParser(self, parent):
        parser = argparse.ArgumentParser(parents=[parent], color=True)
        parser.prog = self.progName
        parser.print_help = self._print_help
        parser.add_argument('tests', nargs='*', help='a list of any number of test modules, classes and test methods.')
        return parser

    def _getDiscoveryArgParser(self, parent):
        parser = argparse.ArgumentParser(parents=[parent], color=True)
        parser.prog = '%s discover' % self.progName
        parser.epilog = 'For test discovery all test modules must be importable from the top level directory of the project.'
        parser.add_argument('-s', '--start-directory', dest='start', help="Directory to start discovery ('.' default)")
        parser.add_argument('-p', '--pattern', dest='pattern', help="Pattern to match tests ('test*.py' default)")
        parser.add_argument('-t', '--top-level-directory', dest='top', help='Top level directory of project (defaults to start directory)')
        for arg in ('start', 'pattern', 'top'):
            parser.add_argument(arg, nargs='?', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        return parser

    def _do_discovery(self, argv, Loader=None):
        self.start = '.'
        self.pattern = 'test*.py'
        self.top = None
        if argv is not None:
            if self._discovery_parser is None:
                self._initArgParsers()
            self._discovery_parser.parse_args(argv, self)
        self.createTests(from_discovery=True, Loader=Loader)

    def runTests(self):
        if self.catchbreak:
            installHandler()
        if self.testRunner is None:
            self.testRunner = runner.TextTestRunner
        if isinstance(self.testRunner, type):
            try:
                try:
                    testRunner = self.testRunner(verbosity=self.verbosity, failfast=self.failfast, buffer=self.buffer, warnings=self.warnings, tb_locals=self.tb_locals, durations=self.durations)
                except TypeError:
                    testRunner = self.testRunner(verbosity=self.verbosity, failfast=self.failfast, buffer=self.buffer, warnings=self.warnings)
            except TypeError:
                testRunner = self.testRunner()
        else:
            testRunner = self.testRunner
        self.result = testRunner.run(self.test)
        if self.exit:
            if not self.result.wasSuccessful():
                sys.exit(1)
            elif self.result.testsRun == 0 and len(self.result.skipped) == 0:
                sys.exit(_NO_TESTS_EXITCODE)
            else:
                sys.exit(0)
主函数 = 测试程序


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'MAIN_EXAMPLES': '主程序示例',
    'MODULE_EXAMPLES': '模块示例',
    'TestProgram': '测试程序',
    'main': '主函数',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
