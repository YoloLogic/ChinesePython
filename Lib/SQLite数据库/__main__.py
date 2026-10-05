# -*- coding: utf-8 -*-
"""SQLite数据库.__main__ —— 汉语库（由 tools/汉化库.py 从 Lib/sqlite3/__main__.py 机械生成，**不要手改**）。

英文库 Lib/sqlite3.__main__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py sqlite3
"""


"""A simple SQLite CLI for the sqlite3 module.

Apart from using 'argparse' for the command-line interface,
this module implements the REPL as a thin wrapper around
the InteractiveConsole class from the 'code' stdlib module.
"""
import SQLite数据库
import sys
from argparse import ArgumentParser
from code import InteractiveConsole
from textwrap import dedent

def execute(c, sql, suppress_errors=True):
    """Helper that wraps execution of SQL code.

    This is used both by the REPL and by direct execution from the CLI.

    'c' may be a cursor or a connection.
    'sql' is the SQL string to execute.
    """
    try:
        for row in c.execute(sql):
            print(row)
    except SQLite数据库.Error as e:
        tp = type(e).__name__
        try:
            print(f'{tp} ({e.sqlite_errorname}): {e}', file=sys.stderr)
        except AttributeError:
            print(f'{tp}: {e}', file=sys.stderr)
        if not suppress_errors:
            sys.exit(1)

class SqliteInteractiveConsole(InteractiveConsole):
    """A simple SQLite REPL."""

    def __init__(self, connection):
        super().__init__()
        self._con = connection
        self._cur = connection.cursor()

    def runsource(self, source, filename='<input>', symbol='single'):
        """Override runsource, the core of the InteractiveConsole REPL.

        Return True if more input is needed; buffering is done automatically.
        Return False if input is a complete statement ready for execution.
        """
        if not source or source.isspace():
            return False
        if source[0] == '.':
            match source[1:].strip():
                case 'version':
                    print(f'{SQLite数据库.sqlite_version}')
                case 'help':
                    print('Enter SQL code and press enter.')
                case 'quit':
                    sys.exit(0)
                case '':
                    pass
                case _ as unknown:
                    self.write(f'Error: unknown command or invalid arguments:  "{unknown}".\n')
        else:
            if not SQLite数据库.complete_statement(source):
                return True
            execute(self._cur, source)
        return False

def main(*args):
    parser = ArgumentParser(description='Python sqlite3 CLI', color=True)
    parser.add_argument('filename', type=str, default=':memory:', nargs='?', help="SQLite database to open (defaults to ':memory:'). A new database is created if the file does not previously exist.")
    parser.add_argument('sql', type=str, nargs='?', help='An SQL query to execute. Any returned rows are printed to stdout.')
    parser.add_argument('-v', '--version', action='version', version=f'SQLite version {SQLite数据库.sqlite_version}', help='Print underlying SQLite library version')
    args = parser.parse_args(*args)
    if args.filename == ':memory:':
        db_name = 'a transient in-memory database'
    else:
        db_name = repr(args.filename)
    if sys.platform == 'win32' and 'idlelib.run' not in sys.modules:
        eofkey = 'CTRL-Z'
    else:
        eofkey = 'CTRL-D'
    banner = dedent(f'\n        sqlite3 shell, running on SQLite version {SQLite数据库.sqlite_version}\n        Connected to {db_name}\n\n        Each command will be run using execute() on the cursor.\n        Type ".help" for more information; type ".quit" or {eofkey} to quit.\n    ').strip()
    sys.ps1 = 'sqlite> '
    sys.ps2 = '    ... '
    con = SQLite数据库.connect(args.filename, isolation_level=None)
    try:
        if args.sql:
            execute(con, args.sql, suppress_errors=False)
        else:
            console = SqliteInteractiveConsole(con)
            try:
                import readline
            except ImportError:
                pass
            console.interact(banner, exitmsg='')
    finally:
        con.close()
    sys.exit(0)
if __name__ == '__main__':
    main(sys.argv[1:])


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# ---- 转发层结束 ----
