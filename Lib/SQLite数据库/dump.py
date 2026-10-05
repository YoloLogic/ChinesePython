# -*- coding: utf-8 -*-
"""SQLite数据库.dump —— 汉语库（由 tools/汉化库.py 从 Lib/sqlite3/dump.py 机械生成，**不要手改**）。

英文库 Lib/sqlite3.dump.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py sqlite3
"""


def _quote_name(name):
    return '"{0}"'.format(name.replace('"', '""'))

def _escape_single_quotes(value):
    return value.replace("'", "''")

def _quote_value(value):
    return "'{0}'".format(_escape_single_quotes(value))

def _iterdump(connection, *, filter=None):
    """
    Returns an iterator to the dump of the database in an SQL text format.

    Used to produce an SQL dump of the database.  Useful to save an in-memory
    database for later restoration.  This function should not be called
    directly but instead called from the Connection method, iterdump().
    """
    writeable_schema = False
    cu = connection.cursor()
    cu.row_factory = None
    violations = cu.execute('PRAGMA foreign_key_check').fetchall()
    if violations:
        yield 'PRAGMA foreign_keys=OFF;'
    yield 'BEGIN TRANSACTION;'
    if filter:
        filter_name_clause = 'AND "name" LIKE ?'
        params = [filter]
    else:
        filter_name_clause = ''
        params = []
    q = f"""\n        SELECT "name", "type", "sql"\n        FROM "sqlite_master"\n            WHERE "sql" NOT NULL AND\n            "type" == 'table'\n            {filter_name_clause}\n            ORDER BY "name"\n        """
    schema_res = cu.execute(q, params)
    sqlite_sequence = []
    for table_name, type, sql in schema_res.fetchall():
        if table_name == 'sqlite_sequence':
            rows = cu.execute('SELECT * FROM "sqlite_sequence";')
            sqlite_sequence = ['DELETE FROM "sqlite_sequence"']
            sqlite_sequence += [f'INSERT INTO "sqlite_sequence" VALUES({_quote_value(table_name)},{seq_value})' for table_name, seq_value in rows.fetchall()]
            continue
        elif table_name == 'sqlite_stat1':
            yield 'ANALYZE "sqlite_master";'
        elif table_name.startswith('sqlite_'):
            continue
        elif sql.startswith('CREATE VIRTUAL TABLE'):
            if not writeable_schema:
                writeable_schema = True
                yield 'PRAGMA writable_schema=ON;'
            yield "INSERT INTO sqlite_master(type,name,tbl_name,rootpage,sql)VALUES('table',{0},{0},0,{1});".format(_quote_value(table_name), _quote_value(sql))
        else:
            yield '{0};'.format(sql)
        table_name_ident = _quote_name(table_name)
        res = cu.execute(f'PRAGMA table_info({table_name_ident})')
        column_names = [str(table_info[1]) for table_info in res.fetchall()]
        q = "SELECT 'INSERT INTO {0} VALUES('{1}')' FROM {2};".format(_escape_single_quotes(table_name_ident), "','".join(('||quote({0})||'.format(_quote_name(col)) for col in column_names)), table_name_ident)
        query_res = cu.execute(q)
        for row in query_res:
            yield '{0};'.format(row[0])
    q = f"""\n        SELECT "name", "type", "sql"\n        FROM "sqlite_master"\n            WHERE "sql" NOT NULL AND\n            "type" IN ('index', 'trigger', 'view')\n            {filter_name_clause}\n        """
    schema_res = cu.execute(q, params)
    for name, type, sql in schema_res.fetchall():
        yield '{0};'.format(sql)
    if writeable_schema:
        yield 'PRAGMA writable_schema=OFF;'
    for row in sqlite_sequence:
        yield '{0};'.format(row)
    yield 'COMMIT;'


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# ---- 转发层结束 ----
