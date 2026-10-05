# -*- coding: utf-8 -*-
"""包工具 —— 汉语库（由 tools/汉化库.py 从 Lib/pkgutil.py 机械生成，**不要手改**）。

英文库 Lib/pkgutil.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 包工具
"""


"""Utilities to support packages."""
_英文原名表 = {'ModuleInfo': '模块信息', 'extend_path': '扩展路径', 'get_data': '取数据', 'get_importer': '取导入器', 'iter_importer_modules': '迭代导入器模块', 'iter_importers': '迭代导入器', 'iter_modules': '迭代模块', 'iter_zipimport_modules': '迭代ZIP导入模块', 'read_code': '读代码', 'resolve_name': '解析名字', 'walk_packages': '遍历包'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
from collections import namedtuple
from functools import singledispatch as simplegeneric
import importlib
import importlib.util
import importlib.machinery
import os
import os.path
import sys
__all__ = ['get_importer', 'iter_importers', 'walk_packages', 'iter_modules', 'get_data', 'read_code', 'extend_path', 'ModuleInfo']
模块信息 = namedtuple('ModuleInfo', 'module_finder name ispkg')
模块信息.__doc__ = 'A namedtuple with minimal info about a module.'

def 读代码(stream):
    import marshal
    magic = stream.read(4)
    if magic != importlib.util.MAGIC_NUMBER:
        return None
    stream.read(12)
    return marshal.load(stream)

def 遍历包(path=None, prefix='', onerror=None):
    """Yields ModuleInfo for all modules recursively
    on path, or, if path is None, all accessible modules.

    'path' should be either None or a list of paths to look for
    modules in.

    'prefix' is a string to output on the front of every module name
    on output.

    Note that this function must import all *packages* (NOT all
    modules!) on the given path, in order to access the __path__
    attribute to find submodules.

    'onerror' is a function which gets called with one argument (the
    name of the package which was being imported) if any exception
    occurs while trying to import a package.  If no onerror function is
    supplied, ImportErrors are caught and ignored, while all other
    exceptions are propagated, terminating the search.

    Examples:

    # list all modules python can access
    walk_packages()

    # list all submodules of ctypes
    walk_packages(ctypes.__path__, ctypes.__name__+'.')
    """

    def seen(p, m={}):
        if p in m:
            return True
        m[p] = True
    for info in 迭代模块(path, prefix):
        yield info
        if info.ispkg:
            try:
                __import__(info.name)
            except ImportError:
                if onerror is not None:
                    onerror(info.name)
            except Exception:
                if onerror is not None:
                    onerror(info.name)
                else:
                    raise
            else:
                path = getattr(sys.modules[info.name], '__path__', None) or []
                path = [p for p in path if not seen(p)]
                yield from 遍历包(path, info.name + '.', onerror)

def 迭代模块(path=None, prefix=''):
    """Yields ModuleInfo for all submodules on path,
    or, if path is None, all top-level modules on sys.path.

    'path' should be either None or a list of paths to look for
    modules in.

    'prefix' is a string to output on the front of every module name
    on output.
    """
    if path is None:
        importers = 迭代导入器()
    elif isinstance(path, str):
        raise ValueError('path must be None or list of paths to look for modules in')
    else:
        importers = map(取导入器, path)
    yielded = {}
    for i in importers:
        for name, ispkg in 迭代导入器模块(i, prefix):
            if name not in yielded:
                yielded[name] = 1
                yield 模块信息(i, name, ispkg)

@simplegeneric
def 迭代导入器模块(importer, prefix=''):
    if not hasattr(importer, 'iter_modules'):
        return []
    return importer.iter_modules(prefix)

def _iter_file_finder_modules(importer, prefix=''):
    if importer.path is None or not os.path.isdir(importer.path):
        return
    yielded = {}
    import inspect
    try:
        filenames = os.listdir(importer.path)
    except OSError:
        filenames = []
    filenames.sort()
    for fn in filenames:
        modname = inspect.getmodulename(fn)
        if modname == '__init__' or modname in yielded:
            continue
        path = os.path.join(importer.path, fn)
        ispkg = False
        if not modname and os.path.isdir(path) and ('.' not in fn):
            modname = fn
            try:
                dircontents = os.listdir(path)
            except OSError:
                dircontents = []
            for fn in dircontents:
                subname = inspect.getmodulename(fn)
                if subname == '__init__':
                    ispkg = True
                    break
            else:
                continue
        if modname and '.' not in modname:
            yielded[modname] = 1
            yield (prefix + modname, ispkg)
迭代导入器模块.register(importlib.machinery.FileFinder, _iter_file_finder_modules)
try:
    import zipimport
    from zipimport import zipimporter

    def 迭代ZIP导入模块(importer, prefix=''):
        dirlist = sorted(zipimport._zip_directory_cache[importer.archive])
        _prefix = importer.prefix
        plen = len(_prefix)
        yielded = {}
        import inspect
        for fn in dirlist:
            if not fn.startswith(_prefix):
                continue
            fn = fn[plen:].split(os.sep)
            if len(fn) == 2 and fn[1].startswith('__init__.py'):
                if fn[0] not in yielded:
                    yielded[fn[0]] = 1
                    yield (prefix + fn[0], True)
            if len(fn) != 1:
                continue
            modname = inspect.getmodulename(fn[0])
            if modname == '__init__':
                continue
            if modname and '.' not in modname and (modname not in yielded):
                yielded[modname] = 1
                yield (prefix + modname, False)
    迭代导入器模块.register(zipimporter, 迭代ZIP导入模块)
except ImportError:
    pass

def 取导入器(path_item):
    """Retrieve a finder for the given path item

    The returned finder is cached in sys.path_importer_cache
    if it was newly created by a path hook.

    The cache (or part of it) can be cleared manually if a
    rescan of sys.path_hooks is necessary.
    """
    path_item = os.fsdecode(path_item)
    try:
        importer = sys.path_importer_cache[path_item]
    except KeyError:
        for path_hook in sys.path_hooks:
            try:
                importer = path_hook(path_item)
                sys.path_importer_cache.setdefault(path_item, importer)
                break
            except ImportError:
                pass
        else:
            importer = None
    return importer

def 迭代导入器(fullname=''):
    """Yield finders for the given module name

    If fullname contains a '.', the finders will be for the package
    containing fullname, otherwise they will be all registered top level
    finders (i.e. those on both sys.meta_path and sys.path_hooks).

    If the named module is in a package, that package is imported as a side
    effect of invoking this function.

    If no module name is specified, all top level finders are produced.
    """
    if fullname.startswith('.'):
        msg = 'Relative module name {!r} not supported'.format(fullname)
        raise ImportError(msg)
    if '.' in fullname:
        pkg_name = fullname.rpartition('.')[0]
        pkg = importlib.import_module(pkg_name)
        path = getattr(pkg, '__path__', None)
        if path is None:
            return
    else:
        yield from sys.meta_path
        path = sys.path
    for item in path:
        yield 取导入器(item)

def 扩展路径(path, name):
    """Extend a package's path.

    Intended use is to place the following code in a package's __init__.py:

        from pkgutil import extend_path
        __path__ = extend_path(__path__, __name__)

    For each directory on sys.path that has a subdirectory that
    matches the package name, add the subdirectory to the package's
    __path__.  This is useful if one wants to distribute different
    parts of a single logical package as multiple directories.

    It also looks for *.pkg files beginning where * matches the name
    argument.  This feature is similar to *.pth files (see site.py),
    except that it doesn't special-case lines starting with 'import'.
    A *.pkg file is trusted at face value: apart from checking for
    duplicates, all entries found in a *.pkg file are added to the
    path, regardless of whether they are exist the filesystem.  (This
    is a feature.)

    If the input path is not a list (as is the case for frozen
    packages) it is returned unchanged.  The input path is not
    modified; an extended copy is returned.  Items are only appended
    to the copy at the end.

    It is assumed that sys.path is a sequence.  Items of sys.path that
    are not (unicode or 8-bit) strings referring to existing
    directories are ignored.  Unicode items of sys.path that cause
    errors when used as filenames may cause this function to raise an
    exception (in line with os.path.isdir() behavior).
    """
    if not isinstance(path, list):
        return path
    sname_pkg = name + '.pkg'
    path = path[:]
    parent_package, _, final_name = name.rpartition('.')
    if parent_package:
        try:
            search_path = sys.modules[parent_package].__path__
        except (KeyError, AttributeError):
            return path
    else:
        search_path = sys.path
    for dir in search_path:
        if not isinstance(dir, str):
            continue
        finder = 取导入器(dir)
        if finder is not None:
            portions = []
            if hasattr(finder, 'find_spec'):
                spec = finder.find_spec(final_name)
                if spec is not None:
                    portions = spec.submodule_search_locations or []
            elif hasattr(finder, 'find_loader'):
                _, portions = finder.find_loader(final_name)
            for portion in portions:
                if portion not in path:
                    path.append(portion)
        pkgfile = os.path.join(dir, sname_pkg)
        if os.path.isfile(pkgfile):
            try:
                f = open(pkgfile)
            except OSError as msg:
                sys.stderr.write("Can't open %s: %s\n" % (pkgfile, msg))
            else:
                with f:
                    for line in f:
                        line = line.rstrip('\n')
                        if not line or line.startswith('#'):
                            continue
                        path.append(line)
    return path

def 取数据(package, resource):
    """Get a resource from a package.

    This is a wrapper round the PEP 302 loader get_data API. The package
    argument should be the name of a package, in standard module format
    (foo.bar). The resource argument should be in the form of a relative
    filename, using '/' as the path separator. The parent directory name '..'
    is not allowed, and nor is a rooted name (starting with a '/').

    The function returns a binary string, which is the contents of the
    specified resource.

    For packages located in the filesystem, which have already been imported,
    this is the rough equivalent of

        d = os.path.dirname(sys.modules[package].__file__)
        data = open(os.path.join(d, resource), 'rb').read()

    If the package cannot be located or loaded, or it uses a PEP 302 loader
    which does not support get_data(), then None is returned.
    """
    spec = importlib.util.find_spec(package)
    if spec is None:
        return None
    loader = spec.loader
    if loader is None or not hasattr(loader, 'get_data'):
        return None
    mod = sys.modules.get(package) or importlib._bootstrap._load(spec)
    if mod is None or not hasattr(mod, '__file__'):
        return None
    parts = resource.split('/')
    parts.insert(0, os.path.dirname(mod.__file__))
    resource_name = os.path.join(*parts)
    return loader.get_data(resource_name)
_NAME_PATTERN = None

def 解析名字(name):
    """
    Resolve a name to an object.

    It is expected that `name` will be a string in one of the following
    formats, where W is shorthand for a valid Python identifier and dot stands
    for a literal period in these pseudo-regexes:

    W(.W)*
    W(.W)*:(W(.W)*)?

    The first form is intended for backward compatibility only. It assumes that
    some part of the dotted name is a package, and the rest is an object
    somewhere within that package, possibly nested inside other objects.
    Because the place where the package stops and the object hierarchy starts
    can't be inferred by inspection, repeated attempts to import must be done
    with this form.

    In the second form, the caller makes the division point clear through the
    provision of a single colon: the dotted name to the left of the colon is a
    package to be imported, and the dotted name to the right is the object
    hierarchy within that package. Only one import is needed in this form. If
    it ends with the colon, then a module object is returned.

    The function will return an object (which might be a module), or raise one
    of the following exceptions:

    ValueError - if `name` isn't in a recognised format
    ImportError - if an import failed when it shouldn't have
    AttributeError - if a failure occurred when traversing the object hierarchy
                     within the imported package to get to the desired object.
    """
    global _NAME_PATTERN
    if _NAME_PATTERN is None:
        import re
        dotted_words = '(?!\\d)(\\w+)(\\.(?!\\d)(\\w+))*'
        _NAME_PATTERN = re.compile(f'^(?P<pkg>{dotted_words})(?P<cln>:(?P<obj>{dotted_words})?)?$', re.UNICODE)
    m = _NAME_PATTERN.match(name)
    if not m:
        raise ValueError(f'invalid format: {name!r}')
    gd = m.groupdict()
    if gd.get('cln'):
        mod = importlib.import_module(gd['pkg'])
        parts = gd.get('obj')
        parts = parts.split('.') if parts else []
    else:
        parts = name.split('.')
        modname = parts.pop(0)
        mod = importlib.import_module(modname)
        while parts:
            p = parts[0]
            s = f'{modname}.{p}'
            try:
                mod = importlib.import_module(s)
                parts.pop(0)
                modname = s
            except ImportError:
                break
    result = mod
    for p in parts:
        result = getattr(result, p)
    return result


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'ModuleInfo': '模块信息',
    'extend_path': '扩展路径',
    'get_data': '取数据',
    'get_importer': '取导入器',
    'iter_importer_modules': '迭代导入器模块',
    'iter_importers': '迭代导入器',
    'iter_modules': '迭代模块',
    'iter_zipimport_modules': '迭代ZIP导入模块',
    'read_code': '读代码',
    'resolve_name': '解析名字',
    'walk_packages': '遍历包',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '取导入器',
    '取数据',
    '扩展路径',
    '模块信息',
    '读代码',
    '迭代导入器',
    '迭代模块',
    '遍历包',
]

# ---- 转发层结束 ----
