# -*- coding: utf-8 -*-
"""JSON解析.工具 —— 汉语库（由 tools/汉化库.py 从 Lib/json/tool.py 机械生成，**不要手改**）。

英文库 Lib/json.tool.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py json
"""


"""Command-line tool to validate and pretty-print JSON

See `json.__main__` for a usage example (invocation as
`python -m json.tool` is supported for backwards compatibility).
"""
_英文原名表 = {'main': '主函数'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import argparse
import JSON解析
import re
import sys
from _colorize import get_theme, can_colorize
_color_pattern = re.compile('\n    (?P<key>"(\\\\.|[^"\\\\])*")(?=:)           |\n    (?P<string>"(\\\\.|[^"\\\\])*")             |\n    (?P<number>NaN|-?Infinity|[0-9\\-+.Ee]+) |\n    (?P<boolean>true|false)                 |\n    (?P<null>null)\n', re.VERBOSE)
_group_to_theme_color = {'key': 'definition', 'string': 'string', 'number': 'number', 'boolean': 'keyword', 'null': 'keyword'}

def _colorize_json(json_str, theme):

    def _replace_match_callback(match):
        for 分组, 颜色 in _group_to_theme_color.items():
            if (m := match.group(分组)):
                return f'{theme[颜色]}{m}{theme.reset}'
        return match.group()
    return re.sub(_color_pattern, _replace_match_callback, json_str)

def 主函数():
    说明 = 'A simple command line interface for json module to validate and pretty-print JSON objects.'
    解析器 = argparse.ArgumentParser(description=说明, color=True)
    解析器.add_argument('infile', nargs='?', help='a JSON file to be validated or pretty-printed', default='-')
    解析器.add_argument('outfile', nargs='?', help='write the output of infile to outfile', default=None)
    解析器.add_argument('--sort-keys', action='store_true', default=False, help='sort the output of dictionaries alphabetically by key')
    解析器.add_argument('--no-ensure-ascii', dest='ensure_ascii', action='store_false', help='disable escaping of non-ASCII characters')
    解析器.add_argument('--json-lines', action='store_true', default=False, help='parse input using the JSON Lines format. Use with --no-indent or --compact to produce valid JSON Lines output.')
    分组 = 解析器.add_mutually_exclusive_group()
    分组.add_argument('--indent', default=4, type=int, help='separate items with newlines and use this number of spaces for indentation')
    分组.add_argument('--tab', action='store_const', dest='indent', const='\t', help='separate items with newlines and use tabs for indentation')
    分组.add_argument('--no-indent', action='store_const', dest='indent', const=None, help='separate items with spaces rather than newlines')
    分组.add_argument('--compact', action='store_true', help='suppress all whitespace separation (most compact)')
    选项 = 解析器.parse_args()
    转储参数 = {'sort_keys': 选项.sort_keys, 'indent': 选项.indent, 'ensure_ascii': 选项.ensure_ascii}
    if 选项.compact:
        转储参数['indent'] = None
        转储参数['separators'] = (',', ':')
    try:
        if 选项.infile == '-':
            输入文件 = sys.stdin
        else:
            输入文件 = open(选项.infile, encoding='utf-8')
        try:
            if 选项.json_lines:
                行表 = 输入文件.readlines()
                对象们 = (JSON解析.loads(line) for line in 行表)
            else:
                对象们 = (JSON解析.load(输入文件),)
        finally:
            if 输入文件 is not sys.stdin:
                输入文件.close()
        if 选项.outfile is None:
            输出文件 = sys.stdout
        else:
            输出文件 = open(选项.outfile, 'w', encoding='utf-8')
        with 输出文件:
            if can_colorize(file=输出文件):
                t = get_theme(tty_file=输出文件).syntax
                for obj in 对象们:
                    json_str = JSON解析.dumps(obj, **转储参数)
                    输出文件.write(_colorize_json(json_str, t))
                    输出文件.write('\n')
            else:
                for obj in 对象们:
                    JSON解析.dump(obj, 输出文件, **转储参数)
                    输出文件.write('\n')
    except ValueError as e:
        raise SystemExit(e)
if __name__ == '__main__':
    try:
        主函数()
    except BrokenPipeError as exc:
        raise SystemExit(exc.errno)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'main': '主函数',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
