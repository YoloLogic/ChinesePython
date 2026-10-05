# -*- coding: utf-8 -*-
"""ChinesePython 报错正文中英对照表。

这份文件是**数据**，逻辑在 zh_traceback.py 里。分工的原因：
数据会越来越长（英文模板全集 3900+ 条），逻辑很短，分开才改得动。

对照表怎么写
------------
`对照` 里每条都是 (英文, 中文)。规则：

1. **占位符不许自己写**。英文里每一段连续的 %s/%.200s/%d/%zd/%U 会被算成
   **一个**捕获组，中文里用 %1 %2 %3 指第几组。可以少用、可以换顺序——
   英文的 %s 有时候只是复数后缀，中文不需要，那就别写。
   `%%` 表示一个字面百分号。
2. **英文代码一个都不能少**。报错里出现的引号包起来的东西是**代码**不是散文：
   'if'、'else'、':'、'*' 一律照留。用户按英文写也照样能跑，所以这是可执行的提示。
   ⚠ **D-144 起顺序反过来**（中文关键字第一位）：有中文词形的关键字写成
   「中文名（英文原名）」，比如 '如果'（if）——用户多半写的是中文关键字，
   先让他对上号；英文原名仍**原样保留**在括号里，一个都不少。
   符号（':'、'*'、'+='）没有词形，照旧只写符号。
3. 不含 % 的条目会被自动放进精确表（O(1) 且绝不可能误匹配）；含 % 的进模板表。
4. 查不到就原样吐英文，所以**宁可缺，不可错**。

`异常名` 是显示用的异常类名，取 `Objects/exceptions.c` 里 zh_exc_aliases[] 的
**主名**（表里靠前那个；同义词只进 except 子句，不进显示）。
绝不能改用 type.__name__ 本身——那会断 pickle 和 inspect。
"""

# ---------------------------------------------------------------------------
# 一、异常类名（显示层换名，异常对象本身不动）
# ---------------------------------------------------------------------------

异常名 = {
    "BaseException": "基异常",
    "Exception": "异常",
    "BaseExceptionGroup": "基异常组",
    "ExceptionGroup": "异常组",
    "Warning": "警告",
    "BytesWarning": "字节警告",
    "DeprecationWarning": "弃用警告",
    "EncodingWarning": "编码警告",
    "FutureWarning": "未来警告",
    "ImportWarning": "导入警告",
    "PendingDeprecationWarning": "待弃用警告",
    "ResourceWarning": "资源警告",
    "RuntimeWarning": "运行时警告",
    "SyntaxWarning": "语法警告",
    "UnicodeWarning": "统一码警告",
    "UserWarning": "用户警告",
    "ArithmeticError": "算术错误",
    "FloatingPointError": "浮点错误",
    "OverflowError": "溢出错误",
    "ZeroDivisionError": "除零错误",
    "TypeError": "类型错误",
    "ValueError": "值错误",
    "LookupError": "查找错误",
    "IndexError": "索引错误",
    "KeyError": "键错误",
    "NameError": "名字错误",
    "UnboundLocalError": "未绑定局部错误",
    "ReferenceError": "引用错误",
    "AssertionError": "断言错误",
    "AttributeError": "属性错误",
    "MemoryError": "内存错误",
    "RecursionError": "递归错误",
    "BufferError": "缓冲区错误",
    "SystemError": "系统错误",
    "RuntimeError": "运行时错误",
    "SystemExit": "系统退出",
    "KeyboardInterrupt": "键盘中断",
    "GeneratorExit": "生成器退出",
    "PythonFinalizationError": "Python收尾错误",
    "OSError": "操作系统错误",
    "IOError": "输入输出错误",
    "EnvironmentError": "环境错误",
    "WindowsError": "Windows错误",
    "BlockingIOError": "阻塞错误",
    "BrokenPipeError": "管道破裂错误",
    "ChildProcessError": "子进程错误",
    "ConnectionError": "连接错误",
    "ConnectionAbortedError": "连接中止错误",
    "ConnectionRefusedError": "连接拒绝错误",
    "ConnectionResetError": "连接重置错误",
    "FileExistsError": "文件已存在错误",
    "FileNotFoundError": "文件未找到错误",
    "InterruptedError": "被中断错误",
    "IsADirectoryError": "是目录错误",
    "NotADirectoryError": "不是目录错误",
    "PermissionError": "权限错误",
    "ProcessLookupError": "进程不存在错误",
    "TimeoutError": "超时错误",
    "ImportError": "导入错误",
    "ModuleNotFoundError": "模块未找到错误",
    "EOFError": "文件结束错误",
    "_IncompleteInputError": "_不完整输入错误",
    "SyntaxError": "语法错误",
    "IndentationError": "缩进错误",
    "TabError": "制表符错误",
    "UnicodeError": "统一码错误",
    "UnicodeDecodeError": "统一码解码错误",
    "UnicodeEncodeError": "统一码编码错误",
    "UnicodeTranslateError": "统一码转换错误",
    "StopIteration": "停止迭代",
    "StopAsyncIteration": "停止异步迭代",
    "NotImplementedError": "未实现错误",
}

# ---------------------------------------------------------------------------
# 二、traceback 追加的两个英文尾巴（traceback.py 自己加的，不是 C 层给的）
# ---------------------------------------------------------------------------

尾巴 = {
    "建议": "。是不是想写 '%s'？",
    "忘记导入": " 还是忘了导入 '%s'？",
    "只忘记导入": "。是不是忘了导入 '%s'？",
}

# ---------------------------------------------------------------------------
# 三、报错正文对照
# ---------------------------------------------------------------------------

对照 = [
    # ===== 三·1 语法/缩进：内核那一句「语法无效」 =====================
    ("invalid syntax", "语法无效"),
    ("invalid syntax. Perhaps you forgot a comma?", "语法无效。是不是漏了逗号？"),
    ("invalid syntax. Maybe you meant '==' or ':=' instead of '='?",
     "语法无效。是不是想写 '==' 或 ':='，而不是 '='？"),
    ("invalid syntax. Is this intended to be part of the string?",
     "语法无效。这段是想写在字符串里面的吗？"),
    ("invalid token", "词法单元非法"),
    ("unknown parsing error", "未知的解析错误"),
    ("unexpected EOF while parsing", "还没解析完就碰到了输入结尾"),
    ("incomplete input", "输入不完整"),
    ("error at start before reading any input", "还没读进任何输入就出错了"),
    ("multiple statements found while compiling a single statement",
     "按单条语句编译时发现了多条语句"),
    ("(%s) unknown error", "(%1) 未知错误"),
    ("expected '%s'", "应为 '%1'"),
    ("expected (%s)", "应为 (%1)"),
    ("expected ':'", "应为 ':'"),
    ("expected an indented block", "应为缩进块"),
    ("expected an indented block after function definition on line %d",
     "函数定义后应为缩进块（第 %1 行）"),
    ("expected an indented block after class definition on line %d",
     "类型定义后应为缩进块（第 %1 行）"),
    ("expected an indented block after 'if' statement on line %d",
     "'如果'（if）语句后应为缩进块（第 %1 行）"),
    ("expected an indented block after 'elif' statement on line %d",
     "'否则如果'（elif）语句后应为缩进块（第 %1 行）"),
    ("expected an indented block after 'else' statement on line %d",
     "'否则'（else）语句后应为缩进块（第 %1 行）"),
    ("expected an indented block after 'while' statement on line %d",
     "'每当'（while）语句后应为缩进块（第 %1 行）"),
    ("expected an indented block after 'for' statement on line %d",
     "'对于'（for）语句后应为缩进块（第 %1 行）"),
    ("expected an indented block after 'with' statement on line %d",
     "'使用'（with）语句后应为缩进块（第 %1 行）"),
    ("expected an indented block after 'try' statement on line %d",
     "'尝试'（try）语句后应为缩进块（第 %1 行）"),
    ("expected an indented block after 'except' statement on line %d",
     "'捕获'（except）语句后应为缩进块（第 %1 行）"),
    ("expected an indented block after 'except*' statement on line %d",
     "'except*' 语句后应为缩进块（第 %1 行）"),
    ("expected an indented block after 'finally' statement on line %d",
     "'最终必须'（finally）语句后应为缩进块（第 %1 行）"),
    ("expected an indented block after 'match' statement on line %d",
     "'匹配'（match）语句后应为缩进块（第 %1 行）"),
    ("expected an indented block after 'case' statement on line %d",
     "'情形'（case）语句后应为缩进块（第 %1 行）"),
    ("unexpected indent", "缩进多余"),
    ("unexpected unindent", "退回缩进多余"),
    ("unindent does not match any outer indentation level",
     "退回的缩进量和任何一个外层缩进层级都对不上"),
    ("inconsistent use of tabs and spaces in indentation",
     "缩进里混用了制表符和空格"),
    ("too many levels of indentation", "缩进层级过多"),
    ("unexpected character after line continuation character",
     "续行符后面还有多余字符"),

    # ===== 三·2 括号、字符串、数字字面量：词法器 =======================
    ("'%c' was never closed", "'%1' 一直没有收尾"),
    ("unmatched '%c'", "'%1' 没有配对"),
    ("closing parenthesis '%c' does not match opening parenthesis '%c'",
     "收尾括号 '%1' 和开头括号 '%2' 对不上"),
    ("closing parenthesis '%c' does not match opening parenthesis '%c' on line %d",
     "收尾括号 '%1' 和第 %3 行的开头括号 '%2' 对不上"),
    ("too many nested parentheses", "圆括号嵌套层数过多"),
    ("unterminated string literal (detected at line %d)",
     "字符串字面量没有收尾（在第 %1 行发现）"),
    ("unterminated string literal (detected at line %d); perhaps you escaped the end quote?",
     "字符串字面量没有收尾（在第 %1 行发现）；是不是把收尾的引号转义了？"),
    ("unterminated triple-quoted string literal (detected at line %d)",
     "三引号字符串字面量没有收尾（在第 %1 行发现）"),
    ("source code cannot contain null bytes", "源代码里不能有空字节"),
    ("invalid character '%c' (U+%04X)", "字符 '%1' 非法（U+%2）"),
    ("invalid non-printable character U+%04X", "不可打印字符 U+%1"),
    ("invalid decimal literal", "十进制字面量非法"),
    ("invalid hexadecimal literal", "十六进制字面量非法"),
    ("invalid octal literal", "八进制字面量非法"),
    ("invalid binary literal", "二进制字面量非法"),
    ("invalid digit '%c' in octal literal", "八进制字面量里有非法数字 '%1'"),
    ("invalid digit '%c' in binary literal", "二进制字面量里有非法数字 '%1'"),
    ("invalid %s literal", "%1 字面量非法"),
    ("too many nested f-strings or t-strings", "f-string 或 t-string 嵌套层数过多"),
    ("bytes can only contain ASCII literal characters",
     "bytes 字面量里只能有 ASCII 字符"),
    ("string to parse is too long", "要解析的字符串太长"),
    ("cannot mix bytes and nonbytes literals", "不能把 bytes 字面量和非 bytes 字面量混在一起"),

    # ===== 三·3 f-string / t-string ==================================
    ("%c-string: expecting '}'", "%1-string：应为 '}'"),
    ("%c-string: single '}' is not allowed", "%1-string：不允许单个 '}'"),
    ("%c-string: unmatched '%c'", "%1-string：'%2' 没有配对"),
    ("%c-string: expressions nested too deeply", "%1-string：表达式嵌套太深"),
    ("%c-string: conversion type must come right after the exclamation mark",
     "%1-string：转换类型必须紧跟在感叹号后面"),
    ("%c-string: invalid conversion character %R: expected 's', 'r', or 'a'",
     "%1-string：转换字符 %2 非法，只能是 's'、'r' 或 'a'"),
    ("%c-string: newlines are not allowed in format specifiers for single quoted %c-strings",
     "%1-string：单引号 %2-string 的格式说明里不允许换行"),
    ("unterminated %c-string literal (detected at line %d)",
     "%1-string 字面量没有收尾（在第 %2 行发现）"),
    ("unterminated triple-quoted %c-string literal (detected at line %d)",
     "三引号 %1-string 字面量没有收尾（在第 %2 行发现）"),
    ("f-string: expecting '}'", "f-string：应为 '}'"),
    ("f-string: expecting ':' or '}'", "f-string：应为 ':' 或 '}'"),
    ("f-string: expecting '}', or format specs", "f-string：应为 '}' 或格式说明"),
    ("f-string: expecting '!', or ':', or '}'", "f-string：应为 '!'、':' 或 '}'"),
    ("f-string: expecting '=', or '!', or ':', or '}'",
     "f-string：应为 '='、'!'、':' 或 '}'"),
    ("f-string: expecting a valid expression after '{'",
     "f-string：'{' 后面应为合法表达式"),
    ("f-string: valid expression required before '='",
     "f-string：'=' 前面要有合法表达式"),
    ("f-string: valid expression required before '!'",
     "f-string：'!' 前面要有合法表达式"),
    ("f-string: valid expression required before ':'",
     "f-string：':' 前面要有合法表达式"),
    ("f-string: valid expression required before '}'",
     "f-string：'}' 前面要有合法表达式"),
    ("f-string: missing conversion character", "f-string：缺少转换字符"),
    ("f-string: invalid conversion character", "f-string：转换字符非法"),
    ("f-string: lambda expressions are not allowed without parentheses",
     "f-string：lambda 表达式不加圆括号是不允许的"),
    ("t-string: expecting '}'", "t-string：应为 '}'"),
    ("t-string: expecting ':' or '}'", "t-string：应为 ':' 或 '}'"),
    ("t-string: expecting '}', or format specs", "t-string：应为 '}' 或格式说明"),
    ("t-string: expecting '!', or ':', or '}'", "t-string：应为 '!'、':' 或 '}'"),
    ("t-string: expecting '=', or '!', or ':', or '}'",
     "t-string：应为 '='、'!'、':' 或 '}'"),
    ("t-string: expecting a valid expression after '{'",
     "t-string：'{' 后面应为合法表达式"),
    ("t-string: valid expression required before '='",
     "t-string：'=' 前面要有合法表达式"),
    ("t-string: valid expression required before '!'",
     "t-string：'!' 前面要有合法表达式"),
    ("t-string: valid expression required before ':'",
     "t-string：':' 前面要有合法表达式"),
    ("t-string: valid expression required before '}'",
     "t-string：'}' 前面要有合法表达式"),
    ("t-string: missing conversion character", "t-string：缺少转换字符"),
    ("t-string: invalid conversion character", "t-string：转换字符非法"),
    ("t-string: lambda expressions are not allowed without parentheses",
     "t-string：lambda 表达式不加圆括号是不允许的"),
    ("cannot mix t-string literals with string or bytes literals",
     "t-string 字面量不能和字符串或 bytes 字面量混用"),

    # ===== 三·4 赋值、注解、参数表 ====================================
    ("cannot assign to %s", "不能赋值给 %1"),
    ("cannot assign to %s here. Maybe you meant '==' instead of '='?",
     "这里不能赋值给 %1。是不是想写 '==' 而不是 '='？"),
    ("cannot assign to keyword argument unpacking", "不能赋值给关键字实参解包"),
    ("cannot assign to iterable argument unpacking", "不能赋值给可迭代实参解包"),
    ("cannot use assignment expressions with %s", "不能在 %1 里用赋值表达式"),
    ("expression cannot contain assignment, perhaps you meant \"==\"?",
     "表达式里不能有赋值，是不是想写 \"==\"？"),
    ("assignment to yield expression not possible", "不能给 yield（产出）表达式赋值"),
    ("'%s' is an illegal expression for augmented assignment",
     "'%1' 不能作为增量赋值的目标"),
    ("only single target (not %s) can be annotated", "只有单个目标能加注解（不能是 %1）"),
    ("only single target (not tuple) can be annotated", "只有单个目标能加注解（不能是元组）"),
    ("illegal target for annotation", "注解的目标非法"),
    ("cannot use starred expression here", "这里不能用星号表达式"),
    ("cannot use double starred expression here", "这里不能用双星号表达式"),
    ("Invalid star expression", "星号表达式非法"),
    ("cannot use %s as import target", "不能用 %1 作为 import 的目标"),
    ("cannot use %s as pattern target", "不能用 %1 作为模式目标"),
    ("cannot use '_' as a target", "不能用 '_' 作为目标"),
    ("cannot use except statement with %s", "不能对 %1 用 except 语句"),
    ("cannot use except* statement with %s", "不能对 %1 用 except* 语句"),
    ("expected one or more exception types", "应为一个或多个异常类型"),
    ("cannot have both 'except' and 'except*' on the same 'try'",
     "同一个 'try' 里不能既有 'except' 又有 'except*'"),
    ("expected 'except' or 'finally' block", "应为 '捕获'（except）或 '最终必须'（finally）块"),
    ("'elif' block follows an 'else' block",
     "'否则如果'（elif）块跑到了 '否则'（else）块的后面"),
    ("expected 'else' after 'if' expression",
     "'如果'（if）表达式后应为 '否则'（else）"),
    ("expected expression before 'if', but statement is given",
     "'如果'（if）前面应为表达式，给过来的却是语句"),
    ("expected expression after 'else', but statement is given",
     "'否则'（else）后面应为表达式，给过来的却是语句"),
    ("'not' after an operator must be parenthesized",
     "运算符后面的 '并非'（not）必须加圆括号"),
    ("'in' expected after for-loop variables", "for 循环变量后面应为 '属于'（in）"),
    ("Generator expression must be parenthesized", "生成器表达式必须加圆括号"),
    ("did you forget parentheses around the comprehension target?",
     "是不是漏了推导式目标的圆括号？"),
    ("iterable unpacking cannot be used in comprehension", "推导式里不能用可迭代解包"),
    ("dict unpacking cannot be used in dict comprehension", "字典推导式里不能用字典解包"),
    ("expected argument value expression", "应为实参值表达式"),
    ("expected default value expression", "应为默认值表达式"),
    ("Missing parentheses in call to '%U'. Did you mean %U(...)?",
     "调用 '%1' 时忘了圆括号。是不是想写 %2(...)？"),

    # ===== 三·5 形参表（/ 与 * 那一堆） ===============================
    ("at least one argument must precede /", "/ 前面至少要有一个参数"),
    ("/ may appear only once", "/ 只能出现一次"),
    ("/ must be ahead of *", "/ 必须在 * 前面"),
    ("expected comma between / and *", "/ 和 * 之间应为逗号"),
    ("* argument may appear only once", "* 参数只能出现一次"),
    ("named arguments must follow bare *", "具名参数必须跟在单独的 * 后面"),
    ("bare * has associated type comment", "单独的 * 上挂了类型注释"),
    ("var-positional argument cannot have default value", "可变位置参数不能有默认值"),
    ("var-keyword argument cannot have default value", "可变关键字参数不能有默认值"),
    ("arguments cannot follow var-keyword argument", "实参不能排在可变关键字参数后面"),
    ("parameter without a default follows parameter with a default",
     "没有默认值的形参排到了有默认值的形参后面"),
    ("Function parameters cannot be parenthesized", "函数形参不能加圆括号"),
    ("Lambda expression parameters cannot be parenthesized",
     "lambda（匿名函数）的形参不能加圆括号"),
    ("Cannot have two type comments on def", "def（定义）上不能有两个类型注释"),

    # ===== 三·6 字典、模式匹配 ========================================
    ("expression expected after dictionary key and ':'", "字典键和 ':' 后面应为表达式"),
    ("':' expected after dictionary key", "字典键后面应为 ':'"),
    ("positional patterns follow keyword patterns", "位置模式排到了关键字模式后面"),
    ("trailing comma not allowed without surrounding parentheses",
     "外面没有圆括号时不允许尾随逗号"),

    # ===== 三·7 解析器自身的故障（一般见不到） ========================
    ("Parser column offset overflow - source line is too big",
     "语法器列偏移溢出 —— 源代码行太长"),
    ("Parser stack overflowed - Python source too complex to parse",
     "语法器栈溢出 —— Python 源代码太复杂，解析不了"),
    ("unexpected expression in assignment %d (line %d)",
     "赋值里出现了意料之外的表达式 %1（第 %2 行）"),
    ("unexpected TemplateStr node without debug data in t-string at line %d",
     "t-string 里第 %1 行出现了没有调试数据的意外 TemplateStr 节点"),
    ("unexpected JoinedStr node without debug data in f-string at line %d",
     "f-string 里第 %1 行出现了没有调试数据的意外 JoinedStr 节点"),

    # ===== 三·8 转义序列 ==============================================
    (r'"\%.3s" is an invalid octal escape sequence. Did you mean "\\%.3s"? A raw string is also an option.',
     r'"%1" 是非法八进制转义序列。是不是想写 "\\%2"？写成原始字符串也行。'),
    (r'"\%c" is an invalid escape sequence. Did you mean "\\%c"? A raw string is also an option.',
     r'"%1" 是非法转义序列。是不是想写 "\\%2"？写成原始字符串也行。'),
    # 3.14 起这两条带「以后就不管用了」的措辞
    (r'"\%.3s" is an invalid octal escape sequence. Such sequences will not work in the future. Did you mean "\\%.3s"? A raw string is also an option.',
     r'"%1" 是非法八进制转义序列，以后这种写法就不管用了。是不是想写 "\\%2"？写成原始字符串也行。'),
    (r'"\%c" is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\%c"? A raw string is also an option.',
     r'"%1" 是非法转义序列，以后这种写法就不管用了。是不是想写 "\\%2"？写成原始字符串也行。'),

    # ===== 三·9 只用 future 才碰得到的梗 ==============================
    ("with Barry as BDFL, use '<>' instead of '!='",
     "既然 Barry 是 BDFL，那就用 '<>' 而不要用 '!='"),
    ("imaginary number required in complex literal", "复数字面量需要虚部"),
    ("real number required in complex literal", "复数字面量需要实部"),
    ("Underscores in numeric literals are only supported in Python 3.6 and greater",
     "数字字面量里的下划线要到 Python 3.6 及以上才支持"),
    ("%S - Consider hexadecimal for huge integer literals to avoid decimal conversion limits.",
     "%1 —— 这么大的整数字面量建议写成十六进制，免得撞上十进制转换上限。"),
    ("unicodedata.normalize() must return a string, not %.200s",
     "unicodedata.normalize() 必须返回字符串，不能是 %1"),
    ("identifier field can't represent '%s' constant",
     "标识符字段表示不了 %1 常量"),

    # ===== 三·10 名字、属性、下标：新手最常撞的一批 ====================
    ("index out of range", "索引超出范围"),
    ("list index out of range", "列表索引超出范围"),
    ("string index out of range", "字符串索引超出范围"),
    ("tuple index out of range", "元组索引超出范围"),
    ("bytearray index out of range", "bytearray 索引超出范围"),
    ("list assignment index out of range", "列表赋值索引超出范围"),
    ("pop index out of range", "pop 的索引超出范围"),
    ("cannot delete attribute", "不能删除属性"),
    ("Cannot delete attribute", "不能删除属性"),
    ("cannot delete __annotate__ attribute", "不能删除 __annotate__ 属性"),
    ("attribute name must be string, not '%.200s'", "属性名必须是字符串，不能是 '%1'"),
    ("'%.100s' object has no attribute '%U'", "'%1' 对象没有属性 '%2'"),
    ("'%.100s' object has no attributes (%s .%U)", "'%1' 对象没有任何属性（%2 .%3）"),
    ("module '%U' has no attribute '%U'", "模块 '%1' 没有属性 '%2'"),
    ("This object has no __dict__", "这个对象没有 __dict__"),
    ("__annotations__", "__annotations__"),
    ("attribute value type must be bool", "属性值的类型必须是 bool"),
    ("assign to", "赋值给"),
    ("type name must not contain null characters", "类型名里不能有空字符"),
    ("cannot create '%s' instances", "不能创建 '%1' 的实例"),
    ("abstract class", "抽象类型"),

    # ===== 三·11 可迭代、可调用、可下标：类型错误 ======================
    ("'%.200s' object is not iterable", "'%1' 对象不可迭代"),
    ("argument of type '%.200s' is not iterable", "类型为 '%1' 的参数不可迭代"),
    ("'%.200s' object is not callable", "'%1' 对象不可调用"),
    ("'%.200s' object is not callable. Did you mean: '%U.%U(...)'?",
     "'%1' 对象不可调用。是不是想写 '%2.%3(...)'？"),
    ("attribute of type '%.200s' is not callable", "类型为 '%1' 的属性不可调用"),
    ("'%.200s' object is not subscriptable", "'%1' 对象不支持下标访问"),
    ("type '%.200s' is not subscriptable", "类型 '%1' 不支持下标访问"),
    ("'%.200s' object is not a mapping", "'%1' 对象不是映射"),
    ("'%.200s' object is not reversible", "'%1' 对象不能反向遍历"),
    ("'%.100s' object is not an iterator", "'%1' 对象不是迭代器"),
    ("'%.200s' object does not support vectorcall", "'%1' 对象不支持 vectorcall"),
    ("object of type '%.200s' has no len()", "类型为 '%1' 的对象没有 len()"),
    ("first argument must be callable", "第一个参数必须是可调用的"),
    ("argument list must be a tuple", "参数列表必须是元组"),
    ("keywords must be strings", "关键字必须是字符串"),
    ("Value after * must be an iterable, not %.200s", "* 后面必须跟可迭代对象，不能是 %1"),
    ("cannot pickle '%.200s' object", "不能 pickle '%1' 对象"),
    ("cannot unpack non-iterable %.200s object", "不能解包不可迭代的 %1 对象"),
    ("cannot create new view on restricted memoryview", "不能在被限制的 memoryview 上再建视图"),
    ("expected PickleBuffer, %.200s found", "应为 PickleBuffer，拿到的是 %1"),
    ("expected bytes, %.200s found", "应为 bytes，拿到的是 %1"),
    ("expected bytes, got %R", "应为 bytes，拿到的是 %1"),
    ("expected int, got %T", "应为 int，拿到的是 %1"),
    ("expect int, got %T", "应为 int，拿到的是 %1"),
    ("expect str, got %T", "应为 str，拿到的是 %1"),
    ("Expected a type param, got %R", "应为类型参数，拿到的是 %1"),
    ("must be str or None, not %.100s", "必须是 str 或 None，不能是 %1"),
    ("byteorder must be either 'little' or 'big'", "byteorder 只能是 'little' 或 'big'"),
    ("can't concat %.100s to %.100s", "不能把 %2 拼到 %1 上"),
    ("unsupported operand type(s) for %.100s: '%.100s' and '%.100s'",
     "%1 的操作数类型不支持：'%2' 和 '%3'"),
    ("unsupported operand type(s) for %.100s: '%.100s', '%.100s', '%.100s'",
     "%1 的操作数类型不支持：'%2'、'%3' 和 '%4'"),
    ("'%s' not supported between instances of '%.100s' and '%.100s'",
     "'%2' 和 '%3' 之间不支持 '%1'"),
    ("an integer is required", "需要一个整数"),
    ("dict expected", "应为字典"),
    ("state is not a dictionary", "state 不是字典"),
    ("<module>.__dict__ is not a dictionary", "<module>.__dict__ 不是字典"),
    ("memoryview: invalid slice key", "memoryview：切片键非法"),
    ("memoryview: format %s not supported", "memoryview：不支持格式 %1"),
    ("memoryview: underlying buffer is not C-contiguous",
     "memoryview：底层缓冲区不是 C 连续的"),
    ("memoryview: number of dimensions must not exceed ", "memoryview：维度数超出上限"),
    ("multi-dimensional sub-views are not implemented", "还没实现多维子视图"),
    ("sub-views are not implemented", "还没实现子视图"),
    ("underlying buffer is not writable", "底层缓冲区不可写"),
    ("slice indices must be integers or None or have an __index__ method",
     "切片索引必须是整数、None，或者有 __index__ 方法"),
    ("slice step cannot be zero", "切片步长不能为零"),
    ("list indices must be integers or slices, not %.200s",
     "列表索引必须是整数或切片，不能是 %1"),
    ("tuple indices must be integers or slices, not %.200s",
     "元组索引必须是整数或切片，不能是 %1"),
    ("bytearray indices must be integers or slices, not %.200s",
     "bytearray 索引必须是整数或切片，不能是 %1"),
    ("string indices must be integers, not '%.200s'", "字符串索引必须是整数，不能是 %1"),
    ("invalid indexing of 0-dim memory", "0 维内存不能这样索引"),

    # ===== 三·12 数值与算术 ===========================================
    # 注：3.14 把 float/complex/integer 三种除零统一成了 "division by zero"
    ("division by zero", "除以零"),
    ("math domain error", "数学定义域错误"),
    ("math range error", "数学结果超出范围"),
    ("negative shift count", "移位位数是负数"),
    ("int too big to convert", "整数太大，转换不了"),
    ("Cannot convert negative int", "不能转换负整数"),
    ("too many digits in integer", "整数位数太多"),
    ("invalid literal for int() with base %d: %.200R",
     "int() 收到非法字面量（进制 %1）：%2"),
    ("could not convert string to float: %R", "字符串转不成浮点数：%1"),
    ("complex() argument must be a string or a number, not %T",
     "complex() 的参数必须是字符串或数，不能是 %1"),
    ("complex() argument 'real' must be a real number, not %T",
     "complex() 的 'real' 参数必须是实数，不能是 %1"),
    ("complex() argument 'imag' must be a real number, not %T",
     "complex() 的 'imag' 参数必须是实数，不能是 %1"),
    ("cannot convert Infinity to integer ratio", "不能把无穷大转成整数比"),
    ("cannot convert NaN to integer ratio", "不能把 NaN 转成整数比"),
    ("required argument is not a float", "要求的参数不是浮点数"),
    ("required argument is not a complex", "要求的参数不是复数"),
    ("Invalid value NaN (not a number)", "值非法：NaN（不是数）"),
    ("precision too big", "精度太大"),
    ("width too big", "宽度太大"),
    ("frexp() result out of range", "frexp() 的结果超出范围"),
    ("byte must be in range(0, 256)", "字节必须在 range(0, 256) 内"),
    ("bytes must be in range(0, 256)", "bytes 必须在 range(0, 256) 内"),
    ("character mapping must be in range(0x%lx)", "字符映射必须在 range(0x%1) 内"),
    ("character mapping must return integer, None or str",
     "字符映射必须返回整数、None 或 str"),
    ("%c arg not in range(0x110000)", "字符 %1 超出 range(0x110000)"),
    ("size must be positive", "大小必须为正"),
    ("negative count", "计数为负"),
    ("invalid start argument", "start 参数非法"),

    # ===== 三·13 整数溢出（getargs / 类型转换） ========================
    ("signed short integer is less than minimum", "有符号短整数小于下限"),
    ("signed short integer is greater than maximum", "有符号短整数大于上限"),
    ("unsigned byte integer is less than minimum", "无符号字节整数小于下限"),
    ("unsigned byte integer is greater than maximum", "无符号字节整数大于上限"),
    ("timeout value is too large", "超时值太大"),
    ("events set too many times", "事件设置次数过多"),
    ("string is too long", "字符串太长"),
    ("replace string is too long", "替换用的字符串太长"),
    ("replace bytes is too long", "替换用的 bytes 太长"),
    ("repeated bytes are too long", "重复出来的 bytes 太长"),
    ("encoded result is too long for a Python string", "编码结果对 Python 字符串来说太长"),
    ("strings are too large to concat", "字符串太大，拼不起来"),
    ("buffer too large", "缓冲区太大"),
    ("cannot add more objects to bytearray", "没法再往 bytearray 里加东西了"),
    ("translation table must be 256 characters long", "转换表必须正好 256 个字符长"),
    ("not enough arguments for format string", "格式字符串的参数给少了"),    ("not all arguments converted during string formatting",
     "字符串格式化时参数没用完"),
    ("not all arguments converted during bytes formatting",
     "bytes 格式化时参数没用完"),
    ("format requires a mapping", "该格式需要一个映射"),
    ("incomplete format key", "格式键不完整"),
    ("incomplete format", "格式不完整"),
    ("unsupported format character '%c' (0x%x) at index %zd",
     "不支持的格式字符 '%1'（0x%2），位置在第 %3"),

    # ===== 三·14 字符串、bytes =======================================
    ("embedded null character", "里面嵌了空字符"),
    ("embedded null byte", "里面嵌了空字节"),
    ("empty separator", "分隔符是空的"),
    ("substring not found", "找不到这个子串"),
    ("subsection not found", "找不到这个子段"),
    ("unsupported error handler", "不支持的错误处理方式"),
    ("invalid code page number", "代码页编号非法"),
    ("'%.400s' decoder returned '%.400s' instead of 'str'; use codecs.decode() to decode to arbitrary types",
     "'%1' 解码器返回的是 '%2' 而不是 'str'；要解成任意类型请用 codecs.decode()"),
    ("encoding without a string argument", "给了编码方式，却没给字符串参数"),
    ("errors without a string argument", "给了错误处理方式，却没给字符串参数"),
    ("string argument without an encoding", "给了字符串参数，却没给编码方式"),
    ("__bytes__ returned non-bytes (type %.200s)", "__bytes__ 返回的不是 bytes（类型是 %1）"),
    ("Invalid UTF-8 sequence", "UTF-8 序列非法"),

    # ===== 三·15 容器在迭代中被改 =====================================
    ("dictionary changed size during iteration", "迭代过程中字典大小变了"),
    ("dictionary keys changed during iteration", "迭代过程中字典的键变了"),
    ("list changed size during iteration", "迭代过程中列表大小变了"),
    ("deque mutated during iteration", "迭代过程中 deque 被改了"),
    ("OrderedDict mutated during iteration", "迭代过程中 OrderedDict 被改了"),
    ("deque index out of range", "deque 索引超出范围"),
    ("pop from an empty deque", "从空 deque 里 pop"),
    ("pop from empty list", "从空列表里 pop"),
    ("pop from an empty set", "从空集合里 pop"),
    ("list.remove(x): x not in list", "list.remove(x)：x 不在列表里"),
    ("list.index(x): x not in list", "list.index(x)：x 不在列表里"),
    ("%s() iterable argument is empty", "%1() 的可迭代参数是空的"),
    ("reduce() of empty iterable with no initial value",
     "对空可迭代对象做 reduce()，又没有给初始值"),
    ("range() arg 3 must not be zero", "range() 的第 3 个参数不能为零"),

    # ===== 三·16 参数打包（最经典的「参数对不上」） ====================
    ("%.200s%s takes no arguments", "%1 不接受参数"),
    ("%.200s%s takes no positional arguments", "%1 不接受位置参数"),
    ("%.200s%s takes %s %d positional argument%s (%zd given)",
     "%1 需要%2%3 个位置参数，但给了 %5 个",
     {2: {"at most": "最多 ", "exactly": "正好 "}}),
    ("%.200s%s takes at most %d %sargument%s (%zd given)",
     "%1 最多接受 %2 个%3参数，但给了 %5 个",
     {3: {"keyword ": "关键字"}}),
    ("%U takes no arguments (%zd given)", "%1 不接受参数（给了 %2 个）"),
    ("%U takes exactly one argument (%zd given)", "%1 只接受一个参数（给了 %2 个）"),
    ("%U takes no keyword arguments", "%1 不接受关键字参数"),
    ("%.200s() takes no keyword arguments", "%1() 不接受关键字参数"),
    ("copy() takes no arguments", "copy() 不接受参数"),
    ("%s() method: bad call flags", "%1() 方法：调用标志不对"),
    ("attempt to assign sequence of size %zd to extended slice of size %zd",
     "想把长度为 %1 的序列赋给长度为 %2 的扩展切片"),
    ("memoryview has %zd exported buffer%s", "memoryview 导出了 %1 个缓冲区"),
    ("Existing exports of data: object cannot be re-sized",
     "数据还有导出在外：这个对象不能改大小"),
    ("operation forbidden on released memoryview object",
     "memoryview 已释放，不能再操作"),
    ("operation forbidden on released PickleBuffer object",
     "PickleBuffer 已释放，不能再操作"),
    ("I/O operation on uninitialized object", "对象还没初始化，不能做 I/O"),

    # ===== 三·17 描述符、类型 =========================================
    ("descriptor '%V' for '%.100s' objects doesn't apply to a '%.100s' object",
     "'%2' 对象的描述符 '%1' 不适用于 '%3' 对象"),
    ("descriptor '%V' of '%.100s' object needs an argument",
     "'%2' 对象的描述符 '%1' 需要一个参数"),
    ("__init__() should return None, not '%.200s'", "__init__() 应该返回 None，不能是 '%1'"),
    ("__name__ must be set to a string object", "__name__ 必须设成字符串对象"),
    ("__qualname__ must be set to a string object", "__qualname__ 必须设成字符串对象"),
    ("__annotate__ returned non-dict of type '%.100s'",
     "__annotate__ 返回的不是字典，类型是 '%1'"),
    ("__annotate__ must be callable or None", "__annotate__ 必须可调用或者是 None"),
    ("Bivariant types are not supported.", "不支持双变类型。"),
    ("Variance cannot be specified with infer_variance.",
     "指定了 infer_variance 就不能再指定 Variance。"),
    ("Cannot watch non-dictionary", "只能监视字典"),
    ("Cannot watch non-type", "只能监视类型"),

    # ===== 三·18 生成器、协程、异步 ===================================
    ("coroutine ignored GeneratorExit", "协程忽略了 GeneratorExit"),
    ("cannot reuse already awaited __anext__()/asend()",
     "已经 await 过的 __anext__()/asend() 不能重复用"),
    ("cannot reuse already awaited aclose()/athrow()",
     "已经 await 过的 aclose()/athrow() 不能重复用"),
    ("anext(): asynchronous generator is already running",
     "anext()：异步生成器已经在跑了"),
    ("aclose(): asynchronous generator is already running",
     "aclose()：异步生成器已经在跑了"),
    ("athrow(): asynchronous generator is already running",
     "athrow()：异步生成器已经在跑了"),
    ("cannot 'yield from' a coroutine object in a non-coroutine generator",
     "在非协程生成器里不能对协程对象用 'yield from'"),
    ("'async for' requires an object with __aiter__ method, got %.100s",
     "'async for' 需要一个带 __aiter__ 方法的对象，拿到的是 %1"),
    ("'async for' received an object from __aiter__ that does not implement __anext__: %.100s",
     "'async for' 从 __aiter__ 拿到的对象没实现 __anext__：%1"),
    ("instance exception may not have a separate value",
     "异常实例不能再单独带一个值"),
    ("super(): arg[0] deleted", "super()：第 0 个参数被删掉了"),

    # ===== 三·19 导入与模块 ===========================================
    ("__build_class__ not found", "找不到 __build_class__"),
    ("no sys module", "没有 sys 模块"),
    ("lost sys.stdout", "sys.stdout 丢了"),
    ("Exception ignored while removing modules", "移除模块时忽略了异常"),
    ("Exception ignored while clearing module dict", "清空模块字典时忽略了异常"),
    ("Exception ignored in %s watcher callback for %R",
     "在 %1 监视器回调里处理 %2 时忽略了异常"),
    ("Exception ignored while closing generator %R",
     "关闭生成器 %1 时忽略了异常"),
    ("Exception ignored while calling deallocator %R",
     "调用 %1 的析构函数时忽略了异常"),
    ("Exception ignored while calling weakref callback %R",
     "调用弱引用回调 %1 时忽略了异常"),
    ("Exception ignored in bf_releasebuffer of %s",
     "%1 的 bf_releasebuffer 里忽略了异常"),

    # ===== 三·20 解释器自身（基本撞不见，但乱码地报错更难受） ==========
    ("no locals found", "找不到局部变量"),
    ("no locals found when storing %R", "往 %1 里存的时候找不到局部变量"),
    ("no locals when deleting %R", "删 %1 的时候找不到局部变量"),
    ("no locals found when setting up annotations", "设置注解时找不到局部变量"),
    ("null argument to internal routine", "内部函数收到了空参数"),
    ("PyArg_UnpackTuple() argument list is not a tuple",
     "PyArg_UnpackTuple() 的参数列表不是元组"),
    ("Missing frame when calling trace function.", "调用跟踪函数时缺了栈帧"),
    ("position %zd from error handler out of bounds",
     "错误处理器返回的位置 %1 越界了"),
    ("cannot release un-acquired lock", "没拿到锁就想释放"),
    ("Unable to allocate lock", "分配不到锁"),
    ("sub-interpreter creation failed", "创建子解释器失败"),
    ("failed to get LC_CTYPE locale", "取不到 LC_CTYPE 区域设置"),
    ("signal number out of range", "信号编号超出范围"),
    ("GDBM object has already been closed", "GDBM 对象已经关掉了"),
    ("cannot remove local variables from FrameLocalsProxy",
     "不能从 FrameLocalsProxy 里删局部变量"),

    # ===== 三·21 名字未定义、局部变量未绑定（新手第一个错） ============
    ("name '%.200s' is not defined", "名字 '%1' 没有定义"),
    ("cannot access local variable '%s' where it is not associated with a value",
     "局部变量 '%1' 在这里还没有值"),
    ("cannot access free variable '%s' where it is not associated with a value in enclosing scope",
     "外层作用域里的自由变量 '%1' 在这里还没有值"),
    ("local variable '%R' is not defined", "局部变量 %1 没有定义"),
    ("unhashable type: '%.200s'", "不可哈希的类型：'%1'"),
    # 括号里那句是**另一个异常的消息**，得递归再翻一次，
    # 否则会变成「不能把 'list' 用作字典的键（unhashable type: 'list'）」
    ("cannot use '%T' as a dict key (%S)",
     "不能把 '%1' 用作字典的键（%2）", {2: "再翻"}),
    ("union contains %zd unhashable elements", "并集里有 %1 个不可哈希的元素"),

    # ===== 三·22 解包、递归 ===========================================
    ("not enough values to unpack (expected %d, got %d)",
     "要解包的值不够（应为 %1 个，只有 %2 个）"),
    ("not enough values to unpack (expected at least %d, got %d)",
     "要解包的值不够（应至少 %1 个，只有 %2 个）"),
    ("not enough values to unpack (expected at least %d, got %zd)",
     "要解包的值不够（应至少 %1 个，只有 %2 个）"),
    ("too many values to unpack (expected %d, got %zd)",
     "要解包的值太多（应为 %1 个，却有 %2 个）"),
    ("too many values to unpack (expected %d)", "要解包的值太多（应为 %1 个）"),
    ("too many values to unpack (expected 2)", "要解包的值太多（应为 2 个）"),
    ("need more than 0 values to unpack", "要解包的值不止 0 个"),
    ("maximum recursion depth exceeded", "递归深度超出上限"),
    ("maximum recursion depth exceeded while normalizing an exception",
     "整理异常时递归深度超出上限"),
    ("cannot set the recursion limit to %i at the recursion depth %i: the limit is too low",
     "在递归深度 %2 的时候不能把递归上限设成 %1：这个上限太低了"),

    # ===== 三·23 拼接：类型不匹配 =====================================
    ("can only concatenate str (not \"%.200s\") to str",
     "str 只能和 str 拼接（不能拼 \"%1\"）"),
    ("can only concatenate list (not \"%.200s\") to list",
     "list 只能和 list 拼接（不能拼 \"%1\"）"),
    ("can only concatenate tuple (not \"%.200s\") to tuple",
     "tuple 只能和 tuple 拼接（不能拼 \"%1\"）"),
    ("can only concatenate deque (not \"%.200s\") to deque",
     "deque 只能和 deque 拼接（不能拼 \"%1\"）"),
    ("can only concatenate string.templatelib.Template (not \"%T\") to string.templatelib.Template",
     "string.templatelib.Template 只能和同类拼接（不能拼 \"%1\"）"),
    ("int() argument must be a string, a bytes-like object or a real number, not '%.200s'",
     "int() 的参数必须是字符串、bytes 类对象或实数，不能是 '%1'"),
    ("a bytes-like object is required, not '%.100s'",
     "需要 bytes 类对象，不能是 '%1'"),
    ("memoryview: a bytes-like object is required, not '%.200s'",
     "memoryview：需要 bytes 类对象，不能是 '%1'"),
    ("decoding to str: need a bytes-like object, %.80s found",
     "解码成 str：需要 bytes 类对象，拿到的是 %1"),
    ("sequence item %zd: expected a bytes-like object, %.80s found",
     "序列第 %1 项：应为 bytes 类对象，拿到的是 %2"),
    ("sequence item %zd: expected str instance, %.80s found",
     "序列第 %1 项：应为 str 实例，拿到的是 %2"),
    ("__format__ must return a str, not %.200s", "__format__ 必须返回 str，不能是 %1"),
    ("Type %.100s doesn't define __format__", "类型 %1 没有定义 __format__"),
    ("unsupported format string passed to %.200s.__format__",
     "传给 %1.__format__ 的格式字符串不支持"),
    ("int() missing string argument", "int() 少了字符串参数"),
    # ceval.c 的 format_missing：%s 那一组是 C 塞进来的英文词
    # "positional" / "keyword-only"，不处理就会出来「缺少 1 个必需的 positional 参数」
    ("%U() missing %zd required %s argument%s: %U",
     "%1() 缺少 %2 个必需的%3参数：%5",
     {3: {"positional": "位置", "keyword-only": "关键字"}}),

    # ===== 三·24 参数对不上：关键字、多余的值 ==========================
    ("%.200s%s got an unexpected keyword argument '%S'",
     "%1 收到一个意料之外的关键字参数 '%2'"),    ("%.200s%s got an unexpected keyword argument '%S'. Did you mean '%S'?",
     "%1 收到一个意料之外的关键字参数 '%2'。是不是想写 '%3'？"),
    ("%U() got an unexpected keyword argument '%S'",
     "%1() 收到一个意料之外的关键字参数 '%2'"),
    ("%U() got an unexpected keyword argument '%S'. Did you mean '%S'?",
     "%1() 收到一个意料之外的关键字参数 '%2'。是不是想写 '%3'？"),
    ("%U() got multiple values for argument '%S'", "%1() 的参数 '%2' 拿到了多个值"),
    ("%U got multiple values for keyword argument '%S'",
     "%1 的关键字参数 '%2' 拿到了多个值"),
    ("%.400s got multiple values for argument %R", "%1 的参数 %2 拿到了多个值"),
    ("%s() takes no keyword arguments", "%1() 不接受关键字参数"),
    ("wrapper %s() takes no keyword arguments", "包装器 %1() 不接受关键字参数"),
    ("%.400s constructor takes at most %zd positional argument%s",
     "%1 的构造函数最多接受 %2 个位置参数"),
    ("__set_name__() takes 2 positional arguments but %zd were given",
     "__set_name__() 只接受 2 个位置参数，却给了 %1 个"),
    ("missing positional arguments in 'partial' call; expected at least %zd, got %zd",
     "'partial' 调用少了位置参数：应至少 %1 个，只给了 %2 个"),
    ("Cannot specify a default for %s() with multiple positional arguments",
     "%1() 有多个位置参数时不能指定默认值"),
    ("bad argument type for built-in operation", "内置操作的参数类型不对"),

    # ===== 三·25 弃用与警告类正文 =====================================
    ("cannot use a string pattern on a bytes-like object",
     "不能拿字符串模式去匹配 bytes 类对象"),
    ("cannot use a bytes pattern on a string-like object",
     "不能拿 bytes 模式去匹配字符串类对象"),

    # ===== 三·27 `is` 拿字面量比较（最常见的 SyntaxWarning） ===========
    # 出现在 codegen.c：先赋给 const char *msg 再 _PyCompile_Warn，
    # 所以正文提取器要专门扫一遍三元表达式才挖得到
    ('"is" with \'%.200s\' literal. Did you mean "=="?',
     '"is"（等同）拿 \'%1\' 字面量来比。是不是想写 "=="？'),
    ('"is not" with \'%.200s\' literal. Did you mean "!="?',
     '"is not"（并非等同）拿 \'%1\' 字面量来比。是不是想写 "!="？'),

    # ===== 三·26 导入：新手第二天就会撞上的一批 ========================
    ("cannot import name %R from %R (unknown location)",
     "不能从 %2 导入名字 %1（位置未知）"),
    ("cannot import name %R from %R (%S)", "不能从 %2 导入名字 %1（%3）"),
    ("cannot import name %R from partially initialized module %R (most likely due to a circular import)",
     "不能从「初始化到一半的模块」%2 导入名字 %1（多半是循环导入）"),
    ("cannot import name %R from partially initialized module %R (most likely due to a circular import) (%S)",
     "不能从「初始化到一半的模块」%2 导入名字 %1（多半是循环导入）（%3）"),
    ("cannot import name %R from %R (consider renaming %R if it has the same name as a library you intended to import)",
     "不能从 %2 导入名字 %1（如果 %3 和你打算导入的库同名，建议改名）"),
    ("cannot import name %R from %R (consider renaming %R since it has the same name as the standard library module named %R and prevents importing that standard library module)",
     "不能从 %2 导入名字 %1（建议给 %3 改名：它和标准库模块 %4 同名，挡住了那个标准库模块的导入）"),

    # ===== 三·28 「外壳包内层」的拼装正文 =============================
    # 这几个的 %1 **本身又是一句正文**（异常类在自己的 __init__ 里把内层消息包了一层）。
    # 必须同时打两个标记：
    #   「优先」  —— 抢在普通模板前面试。不然内层模板会先把外壳追加的上下文吞掉。
    #   「再翻」  —— 把内层正文递归再译一遍，否则内层还是英文。
    # 实测没这两个标记时：
    #   python -c "import re; re.compile('(?P<1>a)')"
    #   -> re.PatternError: 组名 '1' at position 4 中有非法字符     （at position 4 漏了）
    # 加上之后：
    #   -> re.PatternError: 组名 '1' 中有非法字符，位置 4
    ("%s at position %d", "%1，位置 %2", {1: "再翻", "优先": True}),
    ("%s (line %d, column %d)", "%1（第 %2 行，第 %3 列）",
     {1: "再翻", "优先": True}),
    ("%s: line %d column %d (char %d)", "%1：第 %2 行第 %3 列（第 %4 个字符）",
     {1: "再翻", "优先": True}),
    ("%s: line %zd, column %zd", "%1：第 %2 行，第 %3 列", {1: "再翻", "优先": True}),
    # ipaddress 的通用外壳：`'01' in '01.2.3.4'`、`Octet 999 (> 255) not permitted in '1.2.3.999'`。
    # 它只 4 个字面字符，本该被「太笼统」挡掉；靠「再翻必需」放行 ——
    # 只有内层确实是一句已知正文时才成立，所以不会把别的正文套壳套歪。
    ("%s in %r", "%1，出现在 %2 里", {1: "再翻必需", "优先": True}),

    # ===== 三·30 英文复数后缀那一组不许用 ==============================
    # `argument%s` 里的 `%s` 在英文只是个复数后缀（`s` / 空串），中文不需要它。
    # 可它偏偏是个正常捕获组，机器翻译很容易顺手用上 —— 实测出了
    # `类型错误: isinstance 需要2s 个参数，却有 1 个` 这种「多一个 s」的译文。
    # tools/校验报错表.py 现在有机械检查（「中文用了英文复数后缀那一组」），
    # 下面 5 条就是它抓出来的，全部手写改正（手写的优先，会自动顶掉生成的）。
    ("%.150s%s takes %s %d argument%s (%zd given)",
     "%1 需要%2%3 个参数（给了 %5 个）",
     {2: {"at most": "最多 ", "exactly": "正好 "}}),
    # `%s` 那一格在 C 里被填成 "" / "at least " / "at most "（注意**带尾空格**），
    # 中文若把它丢掉，屏幕上就会冒出 `需要 at most 3 个参数` 这种中英夹杂。
    ("%.200s expected %s%zd argument%s, got %zd",
     "%1 需要 %2 个参数，却给了 %4 个"),
    ("%.400s.__replace__ missing %ld keyword argument%s: %U.",
     "%1.__replace__ 缺少 %2 个关键字参数：%4。"),
    ("unpacked tuple should have %s%zd element%s, but has %zd",
     "要解包的元组应有 %1 个元素，却有 %3 个"),
    ("don't know how to document object%s of type %s",
     "不知道如何为 %2 类型的对象生成文档"),

    # ===== 三·31 整数串转换上限 / math 的非负输入 ======================
    # 这两个是提取器盲区修好之后才挖出来的：一个是 #define *_ERROR_FMT_*，
    # 一个是 mathmodule.c 的 FUNC1D/FUNC1AD 宏（正文排在**最后**一个参数）。
    ("Exceeds the limit (%d digits) for integer string conversion: value has %zd digits; use sys.set_int_max_str_digits() to increase the limit",
     "超出整数串转换上限（%1 位）：值有 %2 位；用 sys.set_int_max_str_digits() 调高上限"),
    ("Exceeds the limit (%d digits) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit",
     "超出整数串转换上限（%1 位）；用 sys.set_int_max_str_digits() 调高上限"),
    ("expected a nonnegative input, got %s", "需要非负输入，却拿到了 %1"),
    # mathmodule.c 那一族（FUNC1D/FUNC1AD 宏的最后一个参数）
    ("expected a finite input, got %s", "需要有限输入，却拿到了 %1"),
    ("expected a number in range from -1 up to 1, got %s",
     "需要 -1 到 1 之间的数，却拿到了 %1"),
    ("expected a number between -1 and 1, got %s",
     "需要 -1 和 1 之间的数，却拿到了 %1"),
    ("expected a noninteger or positive integer, got %s",
     "需要非整数或者正整数，却拿到了 %1"),
    ("expected argument value not less than 1, got %s",
     "需要参数值不小于 1，却拿到了 %1"),
    ("expected argument value > -1, got %s", "需要参数值大于 -1，却拿到了 %1"),

    # 跟 `cannot use '%T' as a dict key (%S)` 同一个形状：括号里那句本身又是正文
    ("cannot use '%T' as a set element (%S)",
     "不能把 '%1' 用作集合元素（%2）", {2: "再翻"}),

    # ===== 三·29 库层新挖出来的叶子正文 ===============================
    ("%s is not a tar archive.\n", "%1 不是 tar 包。\n"),
    ("%s: error: %s\n", "%1：错误：%2\n", {2: "再翻"}),
    ("No section: %r", "没有这一节：%1"),
    ("No option %r in section: %r", "%2 这一节里没有选项 %1"),
    ("Bad value substitution: option %s in section %s contains an interpolation key %s which is not a valid option name. Raw value: %s",
     "%2 这一节的选项 %1 里有个插值键 %3，不是合法的选项名。原始值：%4"),
    ("Recursion limit exceeded in value substitution: option %s in section %s contains an interpolation key which cannot be substituted in %s steps. Raw value: %s",
     "值替换的递归层数超了：%2 这一节的选项 %1 里有个插值键，替换 %3 步都替换不完。原始值：%4"),
    ("Source contains parsing errors: %s", "源里有解析错误：%1"),
    ("File contains no section headers.\nfile: %r, line: %d\n%r",
     "文件里没有节标题。\n文件：%1，第 %2 行\n%3"),
    ("Key without value continued with an indented line.\nfile: %r, line: %d\n%r",
     "键后面没有值，却跟了一行缩进行。\n文件：%1，第 %2 行\n%3"),
    ("Support for UNNAMED_SECTION is disabled.",
     "未命名节（UNNAMED_SECTION）的支持没打开。"),
    ("member %s has an absolute path", "成员 %1 用的是绝对路径"),
    ("%s is a special file", "%1 是特殊文件"),
    ("%s is a link to an absolute path", "%1 是指向绝对路径的链接"),
    ("%s bytes read on a total of %s expected bytes",
     "读到了 %1 字节，总共期望 %2 字节"),
    ("got more than %d bytes when reading %s", "读 %2 时超过了 %1 字节"),
]


# ---------------------------------------------------------------------------
# 五、Python 层自己拼出来的正文
# ---------------------------------------------------------------------------
# 这些不在 C 源码里（是 importlib 之类用 f-string 拼的），所以
# tools/校验报错表.py 对它们不做「源码里存不存在」的核对。
# `%s` 在这里表示「把格式化好的那段原样接上」，不是 C 的转换说明。

对照_额外 = [
    ("No module named '%s'", "没有名为 '%1' 的模块"),
    ("No module named '%s'; '%s' is not a package", "没有名为 '%1' 的模块；'%2' 不是包"),
    ("attempted relative import beyond top-level package",
     "相对导入跑到顶层包外面去了"),
    ("attempted relative import with no known parent package",
     "相对导入找不到已知的父包"),
    ("import of %s halted; None in sys.modules",
     "导入 %1 中断了：sys.modules 里是 None"),

    # --- 打包进来的 C 库自己给的文本 -----------------------------------
    # 这些字符串**不在 CPython 源码里**，是那些库自己吐的（expat 的 XML_ErrorString()、
    # zlib 的 z_errmsg[]、sqlite3 的 sqlite3_errmsg()），所以静态提取器挖不到，
    # 只能列在这儿。好在都是**整串/固定形状**，精确匹配就行，不会误伤。
    # 挖不到也不会错——查不到照样吐英文，只是那一条不翻。

    # zlib 的两个外壳：%2 是 C 塞进来的英文短语，%3 是 zlib 的文本（要再翻一层）
    # 中文别照着英文语序写成「错误 -3 解压数据时」——那是翻译腔。
    ("Error %d %s", "%2出错（%1）",
     {2: {"while compressing data": "压缩数据时",
          "while finishing compression": "结束压缩时",
          "while preparing to decompress data": "准备解压数据时",
          "while decompressing data": "解压数据时",
          "while finishing decompression": "结束解压时",
          "while creating compression object": "创建压缩对象时",
          "while creating decompression object": "创建解压对象时",
          "while setting zdict": "设置 zdict 时"}}),
    ("Error %d %s: %.200s", "%2出错（%1）：%3",
     {2: {"while compressing data": "压缩数据时",
          "while finishing compression": "结束压缩时",
          "while preparing to decompress data": "准备解压数据时",
          "while decompressing data": "解压数据时",
          "while finishing decompression": "结束解压时",
          "while creating compression object": "创建压缩对象时",
          "while creating decompression object": "创建解压对象时",
          "while setting zdict": "设置 zdict 时"},
      3: "再翻"}),

    # zlib 的错误文本（z_errmsg 表，稳定不变）
    ("need dictionary", "需要字典"),
    ("stream end", "数据流结束"),
    ("file error", "文件错误"),
    ("stream error", "数据流出错"),
    ("data error", "数据出错"),
    ("insufficient memory", "内存不够"),
    ("buffer error", "缓冲区出错"),
    ("incompatible version", "版本不兼容"),
    ("incorrect header check", "头部校验不对"),
    ("unknown compression method", "认不出压缩方法"),
    ("invalid window size", "窗口大小非法"),
    ("unknown header flags set", "设了认不出的头标志"),
    ("header crc mismatch", "头部 CRC 对不上"),
    ("invalid block type", "块类型非法"),
    ("invalid stored block lengths", "存储块长度非法"),
    ("too many length or distance symbols", "长度或距离符号太多"),
    ("invalid code lengths set", "码长集合非法"),
    ("invalid bit length repeat", "比特长度重复段非法"),
    ("invalid code -- missing end-of-block", "代码非法 —— 缺少块结束标记"),
    ("invalid literal/lengths set", "字面量/长度集合非法"),
    ("invalid distances set", "距离集合非法"),
    ("invalid literal/length code", "字面量/长度代码非法"),
    ("invalid distance code", "距离代码非法"),
    ("invalid distance too far back", "距离回退得太远"),
    ("incorrect data check", "数据校验不对"),
    ("incorrect length check", "长度校验不对"),
    ("invalid input data", "输入数据非法"),
    ("incomplete or truncated stream", "数据流不完整或被截断"),

    # sqlite3 的错误文本（sqlite3_errmsg，常见的那批）
    ("no such table: %s", "没有这个表：%1"),
    ("no such column: %s", "没有这一列：%1"),
    ("no such index: %s", "没有这个索引：%1"),
    ("no such function: %s", "没有这个函数：%1"),
    ('near "%s": syntax error', '"%1" 附近有语法错误'),
    ('unrecognized token: "%s"', '认不出的记号："%1"'),
    ("UNIQUE constraint failed: %s", "UNIQUE 约束不满足：%1"),
    ("NOT NULL constraint failed: %s", "NOT NULL 约束不满足：%1"),
    ("CHECK constraint failed: %s", "CHECK 约束不满足：%1"),
    ("FOREIGN KEY constraint failed", "外键约束不满足"),
    ("database is locked", "数据库被锁住了"),
    ("database table is locked", "数据库表被锁住了"),
    ("attempt to write a readonly database", "想写只读数据库"),
    ("table %s already exists", "表 %1 已经存在"),
    ("unable to open database file", "打不开数据库文件"),
    ("datatype mismatch", "数据类型对不上"),
    ("PRIMARY KEY must be unique", "主键必须唯一"),
    ("too many SQL variables", "SQL 变量太多"),

    # expat 的错误文本（Modules/expat/xmlparse.c 的 XML_ErrorString()，44 条）
    ("out of memory", "内存不够"),
    ("syntax error", "语法错误"),
    ("no element found", "没找到元素"),
    ("not well-formed (invalid token)", "格式不合格（记号非法）"),
    ("unclosed token", "记号没有收尾"),
    ("partial character", "字符不完整"),
    ("mismatched tag", "标签不匹配"),
    ("duplicate attribute", "属性重复"),
    ("junk after document element", "文档元素后面有多余内容"),
    ("illegal parameter entity reference", "参数实体引用非法"),
    ("undefined entity", "实体没有定义"),
    ("recursive entity reference", "实体引用成环"),
    ("asynchronous entity", "异步实体"),
    ("reference to invalid character number", "引用了非法的字符编号"),
    ("reference to binary entity", "引用了二进制实体"),
    ("reference to external entity in attribute", "属性里引用了外部实体"),
    ("XML or text declaration not at start of entity", "XML 或文本声明不在实体开头"),
    ("unknown encoding", "认不出这个编码"),
    ("encoding specified in XML declaration is incorrect", "XML 声明里指定的编码不对"),
    ("unclosed CDATA section", "CDATA 段没有收尾"),
    ("error in processing external entity reference", "处理外部实体引用时出错"),
    ("document is not standalone", "文档不是独立的"),
    ("unexpected parser state - please send a bug report",
     "解析器状态出乎意料 —— 请提交 bug 报告"),
    ("entity declared in parameter entity", "实体是在参数实体里声明的"),
    ("requested feature requires XML_DTD support in Expat",
     "请求的功能需要 Expat 的 XML_DTD 支持"),
    ("cannot change setting once parsing has begun", "解析开始后就不能改设置了"),
    ("unbound prefix", "前缀没有绑定"),
    ("must not undeclare prefix", "不能取消声明前缀"),
    ("incomplete markup in parameter entity", "参数实体里的标记不完整"),
    ("XML declaration not well-formed", "XML 声明格式不合格"),
    ("text declaration not well-formed", "文本声明格式不合格"),
    ("illegal character(s) in public id", "public id 里有非法字符"),
    ("parser suspended", "解析器已挂起"),
    ("parser not suspended", "解析器没有挂起"),
    ("parsing aborted", "解析已中止"),
    ("parsing finished", "解析已结束"),
    ("cannot suspend in external parameter entity", "在外部参数实体里不能挂起"),
    ("reserved prefix (xml) must not be undeclared or bound to another namespace name",
     "保留前缀 (xml) 不能取消声明，也不能绑到别的命名空间名"),
    ("reserved prefix (xmlns) must not be declared or undeclared",
     "保留前缀 (xmlns) 不能声明，也不能取消声明"),
    ("prefix must not be bound to one of the reserved namespace names",
     "前缀不能绑到保留命名空间名上"),
    ("invalid argument", "参数非法"),
    ("a successful prior call to function XML_GetBuffer is required",
     "必须先成功调用一次 XML_GetBuffer"),
    ("limit on input amplification factor (from DTD and entities) breached",
     "输入放大倍数超过了上限（来自 DTD 和实体）"),
    ("parser not started", "解析器还没启动"),
    # —— 参数解析器（argparse）那层 ——
    # argparse 的报错不走异常，`error()` 直接 stderr + exit(2)；
    # 正文靠 Lib/argparse.py 里的钩子过一遍这张表。
    # `argument -f/--foo: invalid choice: 'x' (...)`
    #   -> 前面那截是 ArgumentError.__str__ 拼的（`argument %s: %s`），
    #      后半截才是具体的错，所以第 2 组要「再翻」一次。
    ("argument %s: %s", "参数 %1：%2", {2: "再翻"}),
    # optparse 的 `--foo option requires 1 argument`
    ("%s option requires %d argument", "%1 选项需要 %2 个参数"),
    ("%s option does not take a value", "%1 选项不接受值"),

    # ===== 三·32 编辑器扩展那一轮「人工过基准线」揪出来的漏译 =============
    #
    # 都是同一类：英文的词是从 `%s` / `%U` 里塞进去的，母版存着 `%s`，
    # 渲染完屏幕上只剩词 —— 表里没这个词，就原样漏出来了。
    # 这几条是新增的「整条正文」，另一些（`at most` / reason / 类型清单）
    # 是给已有的母版补上「词替换」或「再翻」。
    ("'%U' codec can't encode character '%s' in position %zd: %U",
     "'%1' 编解码器无法编码位置 %3 处的字符 '%2'：%4",
     {4: "再翻"}),
    # 编解码器报的 reason，本身就是几个固定说法
    ("invalid start byte", "起始字节非法"),
    ("invalid continuation byte", "后续字节非法"),
    # `unexpected end of data` 这里不写 —— 表里本来就有译文（`意料之外的数据结尾`），
    # 再写一条只会把它顶掉，CSV 那边就变味了。
    ("truncated data", "数据被截断"),
    ("surrogates not allowed", "不允许代理项"),
    ("character maps to <undefined>", "字符没有对应的映射"),
    # 上游把正文先赋给变量再 PyErr_SetString，C 提取器只认字面量，看不见这两条
    ("compile() mode must be 'exec', 'eval' or 'single'",
     "compile() 的 mode 必须是 'exec'、'eval' 或 'single'"),
    ("compile() mode must be 'exec', 'eval', 'single' or 'func_type'",
     "compile() 的 mode 必须是 'exec'、'eval'、'single' 或 'func_type'"),
    # 时区那条：原文读着顺一点
    # --- 渲染后的样子：`%s` 那一格在 C 里就是个**英文词** -------------
    # PyArg_UnpackTuple 的母版是 `"%.200s expected %s%zd argument%s, got %zd"`，
    # 中间那个 `%s` 被填成 "" / "at least " / "at most "。
    # 母版上没法改：`%s%zd` 是**两个连续占位符 = 一个捕获组**（`编模板` 故意合并的，
    # 不然 `at most 3` 切不准），那一组拿到的是整个 `at most 3`，词替换按整组比，
    # 永远对不上。所以按渲染后的三种样子各写一条 —— 这也正是
    # `%.200s%s takes at most %d %sargument%s (%zd given)` 那条一直在用的办法。
    ("%.200s expected at most %zd argument%s, got %zd",
     "%1 最多接受 %2 个参数，却给了 %4 个"),
    ("%.200s expected at least %zd argument%s, got %zd",
     "%1 至少需要 %2 个参数，却只给了 %4 个"),
    ("%.200s expected %zd argument%s, got %zd",
     "%1 需要 %2 个参数，却给了 %4 个"),
    ("unpacked tuple should have at most %zd element%s, but has %zd",
     "要解包的元组最多应有 %1 个元素，却有 %3 个"),
    ("unpacked tuple should have at least %zd element%s, but has %zd",
     "要解包的元组至少应有 %1 个元素，却只有 %3 个"),
    ("unpacked tuple should have %zd element%s, but has %zd",
     "要解包的元组应有 %1 个元素，却有 %3 个"),
    # `%.200s() %.200s must be %.50s, not %.50s` 的第二个 `%.200s` 拿到的是
    # `argument 2` 这种**带序号的参数名**，母版翻不动它，按渲染后的样子补一条。
    ("%.200s() argument %d must be %.50s, not %.50s",
     "%1() 的第 %2 个参数必须是 %3，而不是 %4"),
    # `"%s() arg 1 must be a %s object"` 的第二个 `%s` 是类型清单
    # （bltinmodule 里写死的 `"string, bytes or code"`）。
    ("%s() arg 1 must be a string, bytes or code object",
     "%1() 的第 1 个参数必须是字符串、bytes 或代码对象"),
    # ===== 三·33 `tools/查C层盲区.py` 揪出来的：正文先存进变量再递出去 ====
    #
    # 提取器是正则扫字面量的，跟着变量走不了：
    #     msg = "generator already executing";
    #     PyErr_SetString(PyExc_ValueError, msg);
    # 这种形态它一条都看不见。`tools/查C层盲区.py` 专门扫这个形态 ——
    # 52 处命中里，去掉测试件、类名这类不该译的，剩下这些是真给用户看的。
    ("generator already executing", "生成器已经在执行"),
    ("coroutine already executing", "协程已经在执行"),
    ("async generator already executing", "异步生成器已经在执行"),
    ("async generator ignored GeneratorExit",
     "异步生成器忽略了 GeneratorExit"),
    # 上游这两条是相邻字面量拼起来的，得按**拼完整**的样子写
    ("can't send non-None value to a just-started generator",
     "刚启动的生成器不能发送非 None 值"),
    ("can't send non-None value to a just-started coroutine",
     "刚启动的协程不能发送非 None 值"),
    ("__class__ not set defining %.200R as %.200R. "
     "Was __classcell__ propagated to type.__new__?",
     "定义 %1 为 %2 时 __class__ 没有设置。"
     "__classcell__ 传给 type.__new__ 了吗？"),
    ("__class__ set to %.200R defining %.200R as %.200R",
     "定义 %2 为 %3 时 __class__ 却是 %1"),
    ("setupterm: could not find terminal", "setupterm：找不到终端"),
    ("setupterm: could not find terminfo database",
     "setupterm：找不到 terminfo 数据库"),
    ("setupterm: unknown error", "setupterm：未知错误"),
    ("gdbm mappings have bytes or string indices only",
     "gdbm 映射只能用 bytes 或字符串作索引"),
    ("bad operand type", "操作数类型不对"),
    ("cannot find bytecode for specified line",
     "找不到指定行对应的字节码"),
    ("can't jump from unreachable code", "不能从不可达代码处跳转"),
    ("stack to deep to analyze", "栈太深，无法分析"),
    ("object does not support cross-interpreter data",
     "对象不支持跨解释器数据"),
    ("%R does not support cross-interpreter data",
     "%1 不支持跨解释器数据"),
    # ===== 三·34 `Lib/configparser.py` 那种「拼出来的」正文 ================
    # 它是这么写的：
    #     message = ["While reading from ", repr(source)]
    #     message.append(" [line {0:2d}]".format(lineno))
    #     message.append(": section "); message.extend(msg)
    #     Error.__init__(self, "".join(msg))
    # ast 提取器找的是「传给异常构造器的那个表达式」，这儿传的是个 join 结果，
    # **整条看不见**。所以按渲染后的样子手写。
    # 端到端那个探针（tools/查漏.py）里加了场景盯着，别再漏回去。
    ("While reading from %s [line %d]: section %s already exists",
     "读取 %1 时（第 %2 行）：节 %3 已经存在"),
    ("While reading from %s: section %s already exists",
     "读取 %1 时：节 %2 已经存在"),
    ("Section %s already exists", "节 %1 已经存在"),
    ("While reading from %s [line %d]: option %s in section %s already exists",
     "读取 %1 时（第 %2 行）：节 %4 里的选项 %3 已经存在"),
    ("While reading from %s: option %s in section %s already exists",
     "读取 %1 时：节 %3 里的选项 %2 已经存在"),
    ("Option %s in section %s already exists", "节 %2 里的选项 %1 已经存在"),
]

# ---------------------------------------------------------------------------
# 六、操作系统的 strerror 文本
# ---------------------------------------------------------------------------
# [Errno 2] No such file or directory: 'x' 里那句系统文本是 C 库给的，
# 不在 C 源码里，所以单独一张表。译不到就保留英文（绝不影响 Errno 那部分）。

错误号文本 = {
    "No such file or directory": "没有那个文件或目录",
    "Permission denied": "权限不够",
    "File exists": "文件已存在",
    "Is a directory": "是个目录",
    "Not a directory": "不是目录",
    "Directory not empty": "目录非空",
    "No space left on device": "设备上没有剩余空间",
    "Read-only file system": "只读文件系统",
    "Invalid argument": "参数无效",
    "Invalid cross-device link": "跨设备链接无效",
    "Bad file descriptor": "文件描述符无效",
    "Resource temporarily unavailable": "资源暂时不可用",
    "Resource deadlock avoided": "已避免资源死锁",
    "Operation not permitted": "操作不被允许",
    "Operation not supported": "操作不支持",
    "Operation now in progress": "操作正在进行中",
    "Operation already in progress": "操作已经在进行中",
    "No such process": "没有那个进程",
    "No such device": "没有那个设备",
    "No such device or address": "没有那个设备或地址",
    "Interrupted system call": "系统调用被中断",
    "Too many open files": "打开的文件过多",
    "Too many open files in system": "系统里打开的文件过多",
    "Argument list too long": "参数列表太长",
    "Cannot allocate memory": "内存分配不出来",
    "Out of memory": "内存耗尽",
    "Address already in use": "地址已被占用",
    "Cannot assign requested address": "分配不到请求的地址",
    "Network is unreachable": "网络不可达",
    "Network is down": "网络已断开",
    "No route to host": "没有通往该主机的路由",
    "Connection refused": "连接被拒绝",
    "Connection reset by peer": "连接被对端重置",
    "Connection aborted": "连接已中止",
    "Connection timed out": "连接超时",
    "Broken pipe": "管道已破裂",
    "Transport endpoint is not connected": "传输端点尚未连接",
    "Software caused connection abort": "软件导致了连接中止",
    "File name too long": "文件名太长",
    "Value too large for defined data type": "值超出了已定义数据类型的范围",
    "Numerical result out of range": "数值结果超出范围",
    "Result too large": "结果太大",
    "Exec format error": "可执行文件格式错误",
    "Device or resource busy": "设备或资源正忙",
    "Text file busy": "文本文件正忙",
    "No lock": "没有锁",
    "No buffer space available": "没有可用的缓冲区空间",
    "Message too long": "消息太长",
    "Protocol not available": "协议不可用",
    "Protocol wrong type for socket": "套接字协议类型不对",
    "Socket operation on non-socket": "在一个非套接字上做套接字操作",
    "Destination address required": "需要目标地址",
    "Not a tty": "不是终端设备",
    "Inappropriate ioctl for device": "对该设备来说 ioctl 不适用",
    "Illegal seek": "非法的定位操作",
    "Input/output error": "输入输出错误",
    "Invalid or incomplete multibyte or wide character": "多字节或宽字符非法或不完整",
    "Symbolic link loop": "符号链接成环",
    "Too many levels of symbolic links": "符号链接层级过深",
    "Stale file handle": "文件句柄已失效",
    "Host is down": "主机已关机",
    # Windows CRT 常见说法
    "The system cannot find the file specified": "系统找不到指定的文件",
    "The process cannot access the file because it is being used by another process":
        "进程无法访问该文件，因为另一个进程正在使用它",
    "The filename or extension is too long": "文件名或扩展名太长",
    "The directory name is invalid": "目录名无效",
    "The system cannot find the path specified": "系统找不到指定的路径",
    "Access is denied": "访问被拒绝",
}

# ---------------------------------------------------------------------------
# 七、回溯框架行
# ---------------------------------------------------------------------------
# 这些是**版式**不是正文：`Traceback (most recent call last):`、`File "x", line 3, in f` 之类。
# key 是 traceback.py 里的英文格式串（原样抄，一个字不能差），
# value 是中文格式串，`{}` 按位置填，**允许比英文少**
# （英文的复数后缀 `time{""/"s"}` 中文不需要）。
#
# 注意：`  File "x", line 3, in f` 这一行是**编辑器用来做「点击跳转」的锚点**：
# VS Code / PyCharm 的终端链接识别靠的就是 `File "..."` 这个模式。
# 译了之后英文模式下的点击跳转就用不了了 —— 要跳转就把
# CHINESEPYTHON_ERRORS 设成 en（或者以后做编辑器扩展时认中文模式）。

框架 = {
    "Traceback (most recent call last):\n":
        "回溯（最近一次调用最后）:\n",
    "Exception Group Traceback (most recent call last):\n":
        "异常组回溯（最近一次调用最后）:\n",
    "\nThe above exception was the direct cause of the following exception:\n\n":
        "\n上面的异常是下面这个异常的直接原因:\n\n",
    "\nDuring handling of the above exception, another exception occurred:\n\n":
        "\n处理上面的异常时，又发生了另一个异常:\n\n",
    '  File {}"{}"{}, line {}{}{}, in {}{}{}\n':
        '  文件 {}"{}"{}, 第 {}{}{} 行, 在 {}{}{} 中\n',
    '  File {}"{}"{}, line {}{}{}\n':
        '  文件 {}"{}"{}, 第 {}{}{} 行\n',
    '  [Previous line repeated {} more time{}]\n':
        '  [上一行又重复了 {} 次]\n',
    '... (max_group_depth is {})\n':
        '……（max_group_depth 是 {}）\n',
    'and {} more exception{}\n':
        '还有 {} 个异常\n',
}
