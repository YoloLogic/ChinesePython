# -*- coding: utf-8 -*-
"""字节码表 —— 汉语库（由 tools/汉化库.py 从 Lib/opcode.py 机械生成，**不要手改**）。

英文库 Lib/opcode.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 字节码表
"""


"""
opcode module - potentially shared between dis and other modules which
operate on bytecodes (e.g. peephole optimizers).
"""
_英文原名表 = {'EXTENDED_ARG': '扩展参数', 'cmp_op': '比较运算符', 'hasarg': '有参数的', 'hascompare': '比较用的', 'hasconst': '有常量的', 'hasexc': '有异常处理的', 'hasfree': '有自由变量的', 'hasjabs': '绝对跳转的', 'hasjrel': '相对跳转的', 'hasjump': '有跳转的', 'haslocal': '有局部变量的', 'hasname': '有名字的', 'opname': '操作名'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['cmp_op', 'stack_effect', 'hascompare', 'opname', 'opmap', 'HAVE_ARGUMENT', 'EXTENDED_ARG', 'hasarg', 'hasconst', 'hasname', 'hasjump', 'hasjrel', 'hasjabs', 'hasfree', 'haslocal', 'hasexc']
import builtins
import _opcode
from _opcode import stack_effect
from _opcode_metadata import _specializations, _specialized_opmap, opmap, HAVE_ARGUMENT, MIN_INSTRUMENTED_OPCODE
扩展参数 = opmap['EXTENDED_ARG']
操作名 = ['<%r>' % (op,) for op in range(max(opmap.values()) + 1)]
for m in (opmap, _specialized_opmap):
    for op, i in m.items():
        操作名[i] = op
比较运算符 = ('<', '<=', '==', '!=', '>', '>=')
有参数的 = [op for op in opmap.values() if _opcode.has_arg(op)]
有常量的 = [op for op in opmap.values() if _opcode.has_const(op)]
有名字的 = [op for op in opmap.values() if _opcode.has_name(op)]
有跳转的 = [op for op in opmap.values() if _opcode.has_jump(op)]
相对跳转的 = 有跳转的
绝对跳转的 = []
有自由变量的 = [op for op in opmap.values() if _opcode.has_free(op)]
有局部变量的 = [op for op in opmap.values() if _opcode.has_local(op)]
有异常处理的 = [op for op in opmap.values() if _opcode.has_exc(op)]
_intrinsic_1_descs = _opcode.get_intrinsic1_descs()
_intrinsic_2_descs = _opcode.get_intrinsic2_descs()
_special_method_names = _opcode.get_special_method_names()
_common_constants = [builtins.AssertionError, builtins.NotImplementedError, builtins.tuple, builtins.all, builtins.any]
_nb_ops = _opcode.get_nb_ops()
比较用的 = [opmap['COMPARE_OP']]
_cache_format = {'LOAD_GLOBAL': {'counter': 1, 'index': 1, 'module_keys_version': 1, 'builtin_keys_version': 1}, 'BINARY_OP': {'counter': 1, 'descr': 4}, 'UNPACK_SEQUENCE': {'counter': 1}, 'COMPARE_OP': {'counter': 1}, 'CONTAINS_OP': {'counter': 1}, 'FOR_ITER': {'counter': 1}, 'LOAD_SUPER_ATTR': {'counter': 1}, 'LOAD_ATTR': {'counter': 1, 'version': 2, 'keys_version': 2, 'descr': 4}, 'STORE_ATTR': {'counter': 1, 'version': 2, 'index': 1}, 'CALL': {'counter': 1, 'func_version': 2}, 'CALL_KW': {'counter': 1, 'func_version': 2}, 'STORE_SUBSCR': {'counter': 1}, 'SEND': {'counter': 1}, 'JUMP_BACKWARD': {'counter': 1}, 'TO_BOOL': {'counter': 1, 'version': 2}, 'POP_JUMP_IF_TRUE': {'counter': 1}, 'POP_JUMP_IF_FALSE': {'counter': 1}, 'POP_JUMP_IF_NONE': {'counter': 1}, 'POP_JUMP_IF_NOT_NONE': {'counter': 1}}
_inline_cache_entries = {name: sum(value.values()) for name, value in _cache_format.items()}


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'EXTENDED_ARG': '扩展参数',
    'cmp_op': '比较运算符',
    'hasarg': '有参数的',
    'hascompare': '比较用的',
    'hasconst': '有常量的',
    'hasexc': '有异常处理的',
    'hasfree': '有自由变量的',
    'hasjabs': '绝对跳转的',
    'hasjrel': '相对跳转的',
    'hasjump': '有跳转的',
    'haslocal': '有局部变量的',
    'hasname': '有名字的',
    'opname': '操作名',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '扩展参数',
    '操作名',
    '有参数的',
    '有名字的',
    '有局部变量的',
    '有常量的',
    '有异常处理的',
    '有自由变量的',
    '有跳转的',
    '比较用的',
    '比较运算符',
    '相对跳转的',
    '绝对跳转的',
])

# ---- 转发层结束 ----
