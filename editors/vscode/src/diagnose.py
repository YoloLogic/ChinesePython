# -*- coding: utf-8 -*-
"""诊断桥的解释器侧（D-195）—— 手写文件，由 src/bridge.js 调起。

用法：<我们的解释器> diagnose.py <文件路径>
输出：stdout **一行 JSON**（UTF-8）：
      {"diagnostics":[{"line":1,"column":5,"endColumn":9,"message":"...","kind":"syntax-error"}]}

为什么非要用 JSON：bridge.js 那边只认 JSON。**解析人读文本的桥**，会在我们改一次
报错格式之后**静默失灵**（这正是本项目一路在防的病：有一路输出、没人验 = 迟早漂）。

⚠ 消息用 e.msg（英文）。铁律 #3 是 str(e) 保持英文 ⇒ 这条输出**跟显示层开关无关**，
   稳定、可测、不受 CHINESEPYTHON_ERRORS 影响。
"""
import ast
import json
import sys


def 诊断(路):
    出 = []
    try:
        with open(路, encoding="utf-8") as 文件:
            源 = 文件.read()
    except Exception as 错:          # 读不了（编码 / 权限 / 路径）也只报一条，绝不崩
        return [{"line": 1, "column": 1, "endColumn": 2,
                 "message": "读不了文件：%s" % 错, "kind": "read-error"}]
    try:
        ast.parse(源, filename=路)
    except SyntaxError as 错:
        行 = 错.lineno or 1
        列 = 错.offset or 1
        文 = (错.text or "").rstrip("\n")
        末列 = max(列 + 1, len(文) + 1) if 文 else 列 + 1
        出.append({"line": 行, "column": 列, "endColumn": 末列,
                   "message": 错.msg or "语法错误", "kind": "syntax-error"})
    except ValueError as 错:          # 源码里有 NUL 之类
        出.append({"line": 1, "column": 1, "endColumn": 2,
                   "message": str(错), "kind": "value-error"})
    return 出


def 主():
    路 = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.stdout.write(json.dumps({"diagnostics": 诊断(路)}, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(主())
