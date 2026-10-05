# -*- coding: utf-8 -*-
"""词法单元 —— 汉语库（由 tools/汉化库.py 从 Lib/token.py 机械生成，**不要手改**）。

英文库 Lib/token.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 词法单元
"""


"""Token constants."""
_英文原名表 = {'COMMENT': '注释', 'DEDENT': '反缩进', 'ENCODING': '编码声明', 'ENDMARKER': '结束标记', 'ERRORTOKEN': '错误词法单元', 'EXACT_TOKEN_TYPES': '精确词法单元类型', 'FSTRING_END': 'f字符串结束', 'FSTRING_MIDDLE': 'f字符串中段', 'FSTRING_START': 'f字符串开始', 'INDENT': '缩进', 'ISEOF': '是文件尾吗', 'ISNONTERMINAL': '是非终结符吗', 'ISTERMINAL': '是终结符吗', 'NAME': '名字', 'NEWLINE': '换行', 'NL': '空行', 'NT_OFFSET': '非终结符偏移', 'NUMBER': '数字', 'N_TOKENS': '词法单元种数', 'OP': '运算符', 'STRING': '字符串', 'TYPE_COMMENT': '类型注释', 'TYPE_IGNORE': '类型忽略', 'tok_name': '词法单元名'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['tok_name', 'ISTERMINAL', 'ISNONTERMINAL', 'ISEOF', 'EXACT_TOKEN_TYPES']
结束标记 = 0
名字 = 1
数字 = 2
字符串 = 3
换行 = 4
缩进 = 5
反缩进 = 6
LPAR = 7
RPAR = 8
LSQB = 9
RSQB = 10
COLON = 11
COMMA = 12
SEMI = 13
PLUS = 14
MINUS = 15
STAR = 16
SLASH = 17
VBAR = 18
AMPER = 19
LESS = 20
GREATER = 21
EQUAL = 22
DOT = 23
PERCENT = 24
LBRACE = 25
RBRACE = 26
EQEQUAL = 27
NOTEQUAL = 28
LESSEQUAL = 29
GREATEREQUAL = 30
TILDE = 31
CIRCUMFLEX = 32
LEFTSHIFT = 33
RIGHTSHIFT = 34
DOUBLESTAR = 35
PLUSEQUAL = 36
MINEQUAL = 37
STAREQUAL = 38
SLASHEQUAL = 39
PERCENTEQUAL = 40
AMPEREQUAL = 41
VBAREQUAL = 42
CIRCUMFLEXEQUAL = 43
LEFTSHIFTEQUAL = 44
RIGHTSHIFTEQUAL = 45
DOUBLESTAREQUAL = 46
DOUBLESLASH = 47
DOUBLESLASHEQUAL = 48
AT = 49
ATEQUAL = 50
RARROW = 51
ELLIPSIS = 52
COLONEQUAL = 53
EXCLAMATION = 54
运算符 = 55
类型忽略 = 56
类型注释 = 57
SOFT_KEYWORD = 58
f字符串开始 = 59
f字符串中段 = 60
f字符串结束 = 61
TSTRING_START = 62
TSTRING_MIDDLE = 63
TSTRING_END = 64
注释 = 65
空行 = 66
错误词法单元 = 67
编码声明 = 68
词法单元种数 = 69
非终结符偏移 = 256
词法单元名 = {value: name for name, value in globals().items() if isinstance(value, int) and (not name.startswith('_'))}
__all__.extend(词法单元名.values())
精确词法单元类型 = {'!': EXCLAMATION, '!=': NOTEQUAL, '%': PERCENT, '%=': PERCENTEQUAL, '&': AMPER, '&=': AMPEREQUAL, '(': LPAR, ')': RPAR, '*': STAR, '**': DOUBLESTAR, '**=': DOUBLESTAREQUAL, '*=': STAREQUAL, '+': PLUS, '+=': PLUSEQUAL, ',': COMMA, '-': MINUS, '-=': MINEQUAL, '->': RARROW, '.': DOT, '...': ELLIPSIS, '/': SLASH, '//': DOUBLESLASH, '//=': DOUBLESLASHEQUAL, '/=': SLASHEQUAL, ':': COLON, ':=': COLONEQUAL, ';': SEMI, '<': LESS, '<<': LEFTSHIFT, '<<=': LEFTSHIFTEQUAL, '<=': LESSEQUAL, '=': EQUAL, '==': EQEQUAL, '>': GREATER, '>=': GREATEREQUAL, '>>': RIGHTSHIFT, '>>=': RIGHTSHIFTEQUAL, '@': AT, '@=': ATEQUAL, '[': LSQB, ']': RSQB, '^': CIRCUMFLEX, '^=': CIRCUMFLEXEQUAL, '{': LBRACE, '|': VBAR, '|=': VBAREQUAL, '}': RBRACE, '~': TILDE}

def 是终结符吗(x: int) -> bool:
    return x < 非终结符偏移

def 是非终结符吗(x: int) -> bool:
    return x >= 非终结符偏移

def 是文件尾吗(x: int) -> bool:
    return x == 结束标记


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'COMMENT': '注释',
    'DEDENT': '反缩进',
    'ENCODING': '编码声明',
    'ENDMARKER': '结束标记',
    'ERRORTOKEN': '错误词法单元',
    'EXACT_TOKEN_TYPES': '精确词法单元类型',
    'FSTRING_END': 'f字符串结束',
    'FSTRING_MIDDLE': 'f字符串中段',
    'FSTRING_START': 'f字符串开始',
    'INDENT': '缩进',
    'ISEOF': '是文件尾吗',
    'ISNONTERMINAL': '是非终结符吗',
    'ISTERMINAL': '是终结符吗',
    'NAME': '名字',
    'NEWLINE': '换行',
    'NL': '空行',
    'NT_OFFSET': '非终结符偏移',
    'NUMBER': '数字',
    'N_TOKENS': '词法单元种数',
    'OP': '运算符',
    'STRING': '字符串',
    'TYPE_COMMENT': '类型注释',
    'TYPE_IGNORE': '类型忽略',
    'tok_name': '词法单元名',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '是文件尾吗',
    '是终结符吗',
    '是非终结符吗',
    '精确词法单元类型',
    '词法单元名',
]

# ---- 转发层结束 ----
