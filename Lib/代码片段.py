# -*- coding: utf-8 -*-
"""代码片段 —— 汉语库（由 tools/汉化库.py 从 Lib/codeop.py 机械生成，**不要手改**）。

英文库 Lib/codeop.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 代码片段
"""


"""Utilities to compile possibly incomplete Python source code.

This module provides two interfaces, broadly similar to the builtin
function compile(), which take program text, a filename and a 'mode'
and:

- Return code object if the command is complete and valid
- Return None if the command is incomplete
- Raise SyntaxError, ValueError or OverflowError if the command is a
  syntax error (OverflowError and ValueError can be produced by
  malformed literals).

The two interfaces are:

compile_command(source, filename, symbol):

    Compiles a single command in the manner described above.

CommandCompiler():

    Instances of this class have __call__ methods identical in
    signature to compile_command; the difference is that if the
    instance compiles program text containing a __future__ statement,
    the instance 'remembers' and compiles all subsequent program texts
    with the statement in force.

The module also provides another class:

Compile():

    Instances of this class act like the built-in function compile,
    but with 'memory' in the sense described above.
"""
_英文原名表 = {'CommandCompiler': '命令编译器', 'Compile': '编译器', 'compile_command': '编译命令'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import __future__
import warnings
_features = [getattr(__future__, fname) for fname in __future__.all_feature_names]
__all__ = ['compile_command', 'Compile', 'CommandCompiler']
PyCF_DONT_IMPLY_DEDENT = 512
PyCF_ONLY_AST = 1024
PyCF_ALLOW_INCOMPLETE_INPUT = 16384

def _maybe_compile(compiler, source, filename, symbol, flags):
    for line in source.split('\n'):
        line = line.strip()
        if line and line[0] != '#':
            break
    else:
        if symbol != 'eval':
            source = 'pass'
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', (SyntaxWarning, DeprecationWarning))
        try:
            compiler(source, filename, symbol, flags=flags)
        except SyntaxError:
            try:
                compiler(source + '\n', filename, symbol, flags=flags)
                return None
            except _IncompleteInputError as e:
                return None
            except SyntaxError as e:
                pass
    return compiler(source, filename, symbol, incomplete_input=False)

def _compile(source, filename, symbol, incomplete_input=True, *, flags=0):
    if incomplete_input:
        flags |= PyCF_ALLOW_INCOMPLETE_INPUT
        flags |= PyCF_DONT_IMPLY_DEDENT
    return compile(source, filename, symbol, flags)

def 编译命令(source, filename='<input>', symbol='single', flags=0):
    """Compile a command and determine whether it is incomplete.

    Arguments:

    source -- the source string; may contain \\n characters
    filename -- optional filename from which source was read; default
                "<input>"
    symbol -- optional grammar start symbol; "single" (default), "exec"
              or "eval"

    Return value / exceptions raised:

    - Return a code object if the command is complete and valid
    - Return None if the command is incomplete
    - Raise SyntaxError, ValueError or OverflowError if the command is a
      syntax error (OverflowError and ValueError can be produced by
      malformed literals).
    """
    return _maybe_compile(_compile, source, filename, symbol, flags)

class 编译器:
    """Instances of this class behave much like the built-in compile
    function, but if one is used to compile text containing a future
    statement, it "remembers" and compiles all subsequent program texts
    with the statement in force."""

    def __init__(self):
        self.flags = PyCF_DONT_IMPLY_DEDENT | PyCF_ALLOW_INCOMPLETE_INPUT

    def __call__(self, source, filename, symbol, flags=0, **kwargs):
        flags |= self.flags
        if kwargs.get('incomplete_input', True) is False:
            flags &= ~PyCF_DONT_IMPLY_DEDENT
            flags &= ~PyCF_ALLOW_INCOMPLETE_INPUT
        codeob = compile(source, filename, symbol, flags, True)
        if flags & PyCF_ONLY_AST:
            return codeob
        for feature in _features:
            if codeob.co_flags & feature.compiler_flag:
                self.flags |= feature.compiler_flag
        return codeob

class 命令编译器:
    """Instances of this class have __call__ methods identical in
    signature to compile_command; the difference is that if the
    instance compiles program text containing a __future__ statement,
    the instance 'remembers' and compiles all subsequent program texts
    with the statement in force."""

    def __init__(self):
        self.compiler = 编译器()

    def __call__(self, source, filename='<input>', symbol='single'):
        """Compile a command and determine whether it is incomplete.

        Arguments:

        source -- the source string; may contain \\n characters
        filename -- optional filename from which source was read;
                    default "<input>"
        symbol -- optional grammar start symbol; "single" (default) or
                  "eval"

        Return value / exceptions raised:

        - Return a code object if the command is complete and valid
        - Return None if the command is incomplete
        - Raise SyntaxError, ValueError or OverflowError if the command is a
          syntax error (OverflowError and ValueError can be produced by
          malformed literals).
        """
        return _maybe_compile(self.compiler, source, filename, symbol, flags=self.compiler.flags)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'CommandCompiler': '命令编译器',
    'Compile': '编译器',
    'compile_command': '编译命令',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '命令编译器',
    '编译命令',
    '编译器',
])

# ---- 转发层结束 ----
