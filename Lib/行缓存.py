# -*- coding: utf-8 -*-
"""行缓存 —— 汉语库（由 tools/汉化库.py 从 Lib/linecache.py 机械生成，**不要手改**）。

英文库 Lib/linecache.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 行缓存
"""


"""Cache lines from Python source files.

This is intended to read lines from modules imported -- hence if a filename
is not found, it will look down the module search path for a file by
that name.
"""
_英文原名表 = {'cache': '缓存', 'checkcache': '检查缓存', 'clearcache': '清缓存', 'getline': '取行', 'getlines': '取多行', 'lazycache': '懒缓存'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['getline', 'clearcache', 'checkcache', 'lazycache']
缓存 = {}
_interactive_cache = {}

def 清缓存():
    """Clear the cache entirely."""
    缓存.clear()

def 取行(filename, lineno, module_globals=None):
    """Get a line for a Python source file from the cache.
    Update the cache if it doesn't contain an entry for this file already."""
    lines = 取多行(filename, module_globals)
    if 1 <= lineno <= len(lines):
        return lines[lineno - 1]
    return ''

def 取多行(filename, module_globals=None):
    """Get the lines for a Python source file from the cache.
    Update the cache if it doesn't contain an entry for this file already."""
    entry = 缓存.get(filename, None)
    if entry is not None and len(entry) != 1:
        return entry[2]
    try:
        return updatecache(filename, module_globals)
    except MemoryError:
        清缓存()
        return []

def _getline_from_code(filename, lineno):
    lines = _getlines_from_code(filename)
    if 1 <= lineno <= len(lines):
        return lines[lineno - 1]
    return ''

def _make_key(code):
    return (code.co_filename, code.co_qualname, code.co_firstlineno)

def _getlines_from_code(code):
    code_id = _make_key(code)
    entry = _interactive_cache.get(code_id, None)
    if entry is not None and len(entry) != 1:
        return entry[2]
    return []

def _source_unavailable(filename):
    """Return True if the source code is unavailable for such file name."""
    return not filename or (filename.startswith('<') and filename.endswith('>') and (not filename.startswith('<frozen ')))

def 检查缓存(filename=None):
    """Discard cache entries that are out of date.
    (This is not checked upon each call!)"""
    if filename is None:
        filenames = 缓存.copy().keys()
    else:
        filenames = [filename]
    for filename in filenames:
        entry = 缓存.get(filename, None)
        if entry is None or len(entry) == 1:
            continue
        size, mtime, lines, fullname = entry
        if mtime is None:
            continue
        try:
            import os
        except ImportError:
            return
        try:
            stat = os.stat(fullname)
        except (OSError, ValueError):
            缓存.pop(filename, None)
            continue
        if size != stat.st_size or mtime != stat.st_mtime:
            缓存.pop(filename, None)

def updatecache(filename, module_globals=None):
    """Update a cache entry and return its list of lines.
    If something's wrong, print a message, discard the cache entry,
    and return an empty list."""
    try:
        import os
        import sys
        import tokenize
    except ImportError:
        return []
    entry = 缓存.pop(filename, None)
    if _source_unavailable(filename):
        return []
    if filename.startswith('<frozen '):
        if module_globals is None:
            return []
        fullname = module_globals.get('__file__')
        if fullname is None:
            return []
    else:
        fullname = filename
    try:
        stat = os.stat(fullname)
    except OSError:
        basename = filename
        lazy_entry = entry if entry is not None and len(entry) == 1 else None
        if lazy_entry is None:
            lazy_entry = _make_lazycache_entry(filename, module_globals)
        if lazy_entry is not None:
            try:
                data = lazy_entry[0]()
            except (ImportError, OSError):
                pass
            else:
                if data is None:
                    return []
                entry = (len(data), None, [line + '\n' for line in data.splitlines()], fullname)
                缓存[filename] = entry
                return entry[2]
        if os.path.isabs(filename):
            return []
        for dirname in sys.path:
            try:
                fullname = os.path.join(dirname, basename)
            except (TypeError, AttributeError):
                continue
            try:
                stat = os.stat(fullname)
                break
            except (OSError, ValueError):
                pass
        else:
            return []
    except ValueError:
        return []
    try:
        with tokenize.open(fullname) as fp:
            lines = fp.readlines()
    except (OSError, UnicodeDecodeError, SyntaxError):
        return []
    if not lines:
        lines = ['\n']
    elif not lines[-1].endswith('\n'):
        lines[-1] += '\n'
    size, mtime = (stat.st_size, stat.st_mtime)
    缓存[filename] = (size, mtime, lines, fullname)
    return lines

def 懒缓存(filename, module_globals):
    """Seed the cache for filename with module_globals.

    The module loader will be asked for the source only when getlines is
    called, not immediately.

    If there is an entry in the cache already, it is not altered.

    :return: True if a lazy load is registered in the cache,
        otherwise False. To register such a load a module loader with a
        get_source method must be found, the filename must be a cacheable
        filename, and the filename must not be already cached.
    """
    entry = 缓存.get(filename, None)
    if entry is not None:
        return len(entry) == 1
    lazy_entry = _make_lazycache_entry(filename, module_globals)
    if lazy_entry is not None:
        缓存[filename] = lazy_entry
        return True
    return False

def _make_lazycache_entry(filename, module_globals):
    if not filename or (filename.startswith('<') and filename.endswith('>')):
        return None
    if module_globals and '__name__' in module_globals:
        spec = module_globals.get('__spec__')
        name = getattr(spec, 'name', None) or module_globals['__name__']
        loader = getattr(spec, 'loader', None)
        if loader is None:
            loader = module_globals.get('__loader__')
        get_source = getattr(loader, 'get_source', None)
        if name and get_source:

            def get_lines(name=name, *args, **kwargs):
                return get_source(name, *args, **kwargs)
            return (get_lines,)
    return None

def _register_code(code, string, name):
    entry = (len(string), None, [line + '\n' for line in string.splitlines()], name)
    stack = [code]
    while stack:
        code = stack.pop()
        for const in code.co_consts:
            if isinstance(const, type(code)):
                stack.append(const)
        key = _make_key(code)
        _interactive_cache[key] = entry


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 本模块别名：词表里有、但规则不让改定义的名字（内置名最典型，比如 `open`）
_本模块别名 = {
    '更新缓存': 'updatecache',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'cache': '缓存',
    'checkcache': '检查缓存',
    'clearcache': '清缓存',
    'getline': '取行',
    'getlines': '取多行',
    'lazycache': '懒缓存',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '取行',
    '懒缓存',
    '更新缓存',
    '检查缓存',
    '清缓存',
]

# ---- 转发层结束 ----
