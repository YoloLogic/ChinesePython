# -*- coding: utf-8 -*-
"""运行库 —— 汉语库（由 tools/汉化库.py 从 Lib/runpy.py 机械生成，**不要手改**）。

英文库 Lib/runpy.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 运行库
"""


"""runpy.py - locating and running Python code using the module namespace

Provides support for locating and running Python scripts using the Python
module namespace instead of the native filesystem.

This allows Python code to play nicely with non-filesystem based PEP 302
importers when locating support scripts as well as when importing modules.
"""
_英文原名表 = {'run_module': '运行模块', 'run_path': '运行路径'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import sys
import importlib.machinery
import importlib.util
import io
import os
__all__ = ['run_module', 'run_path']
ModuleType = type(sys)

class _TempModule(object):
    """Temporarily replace a module in sys.modules with an empty namespace"""

    def __init__(self, mod_name):
        self.mod_name = mod_name
        self.module = ModuleType(mod_name)
        self._saved_module = []

    def __enter__(self):
        mod_name = self.mod_name
        try:
            self._saved_module.append(sys.modules[mod_name])
        except KeyError:
            pass
        sys.modules[mod_name] = self.module
        return self

    def __exit__(self, *args):
        if self._saved_module:
            sys.modules[self.mod_name] = self._saved_module[0]
        else:
            del sys.modules[self.mod_name]
        self._saved_module = []

class _ModifiedArgv0(object):

    def __init__(self, value):
        self.value = value
        self._saved_value = self._sentinel = object()

    def __enter__(self):
        if self._saved_value is not self._sentinel:
            raise RuntimeError('Already preserving saved value')
        self._saved_value = sys.argv[0]
        sys.argv[0] = self.value

    def __exit__(self, *args):
        self.value = self._sentinel
        sys.argv[0] = self._saved_value

def _run_code(code, run_globals, init_globals=None, mod_name=None, mod_spec=None, pkg_name=None, script_name=None):
    """Helper to run code in nominated namespace"""
    if init_globals is not None:
        run_globals.update(init_globals)
    if mod_spec is None:
        loader = None
        fname = script_name
        cached = None
    else:
        loader = mod_spec.loader
        fname = mod_spec.origin
        cached = mod_spec.cached
        if pkg_name is None:
            pkg_name = mod_spec.parent
    run_globals.update(__name__=mod_name, __file__=fname, __cached__=cached, __doc__=None, __loader__=loader, __package__=pkg_name, __spec__=mod_spec)
    exec(code, run_globals)
    return run_globals

def _run_module_code(code, init_globals=None, mod_name=None, mod_spec=None, pkg_name=None, script_name=None):
    """Helper to run code in new namespace with sys modified"""
    fname = script_name if mod_spec is None else mod_spec.origin
    with _TempModule(mod_name) as temp_module, _ModifiedArgv0(fname):
        mod_globals = temp_module.module.__dict__
        _run_code(code, mod_globals, init_globals, mod_name, mod_spec, pkg_name, script_name)
    return mod_globals.copy()

def _get_module_details(mod_name, error=ImportError):
    kwargs = {'name': mod_name} if issubclass(error, ImportError) else {}
    if mod_name.startswith('.'):
        raise error('Relative module names not supported', **kwargs)
    pkg_name, _, _ = mod_name.rpartition('.')
    if pkg_name:
        try:
            __import__(pkg_name)
        except ImportError as e:
            if e.name is None or (e.name != pkg_name and (not pkg_name.startswith(e.name + '.'))):
                raise
        existing = sys.modules.get(mod_name)
        if existing is not None and (not hasattr(existing, '__path__')):
            from warnings import warn
            msg = '{mod_name!r} found in sys.modules after import of package {pkg_name!r}, but prior to execution of {mod_name!r}; this may result in unpredictable behaviour'.format(mod_name=mod_name, pkg_name=pkg_name)
            warn(RuntimeWarning(msg))
    try:
        spec = importlib.util.find_spec(mod_name)
    except (ImportError, AttributeError, TypeError, ValueError) as ex:
        msg = 'Error while finding module specification for {!r} ({}: {})'
        if mod_name.endswith('.py'):
            msg += f". Try using '{mod_name[:-3]}' instead of '{mod_name}' as the module name."
        raise error(msg.format(mod_name, type(ex).__name__, ex), **kwargs) from ex
    if spec is None:
        raise error('No module named %s' % mod_name, **kwargs)
    if spec.submodule_search_locations is not None:
        if mod_name == '__main__' or mod_name.endswith('.__main__'):
            raise error('Cannot use package as __main__ module', **kwargs)
        try:
            pkg_main_name = mod_name + '.__main__'
            return _get_module_details(pkg_main_name, error)
        except error as e:
            if mod_name not in sys.modules:
                raise
            raise error(('%s; %r is a package and cannot ' + 'be directly executed') % (e, mod_name), **kwargs)
    loader = spec.loader
    if loader is None:
        raise error('%r is a namespace package and cannot be executed' % mod_name, **kwargs)
    try:
        code = loader.get_code(mod_name)
    except ImportError as e:
        raise error(format(e), **kwargs) from e
    if code is None:
        raise error('No code object available for %s' % mod_name, **kwargs)
    return (mod_name, spec, code)

class _Error(Exception):
    """Error that _run_module_as_main() should report without a traceback"""

def _run_module_as_main(mod_name, alter_argv=True):
    """Runs the designated module in the __main__ namespace

       Note that the executed module will have full access to the
       __main__ namespace. If this is not desirable, the run_module()
       function should be used to run the module code in a fresh namespace.

       At the very least, these variables in __main__ will be overwritten:
           __name__
           __file__
           __cached__
           __loader__
           __package__
    """
    try:
        if alter_argv or mod_name != '__main__':
            mod_name, mod_spec, code = _get_module_details(mod_name, _Error)
        else:
            mod_name, mod_spec, code = _get_main_module_details(_Error)
    except _Error as exc:
        msg = '%s: %s' % (sys.executable, exc)
        sys.exit(msg)
    main_globals = sys.modules['__main__'].__dict__
    if alter_argv:
        sys.argv[0] = mod_spec.origin
    return _run_code(code, main_globals, None, '__main__', mod_spec)

def 运行模块(mod_name, init_globals=None, run_name=None, alter_sys=False):
    """Execute a module's code without importing it.

       mod_name -- an absolute module name or package name.

       Optional arguments:
       init_globals -- dictionary used to pre-populate the module’s
       globals dictionary before the code is executed.

       run_name -- if not None, this will be used for setting __name__;
       otherwise, __name__ will be set to mod_name + '__main__' if the
       named module is a package and to just mod_name otherwise.

       alter_sys -- if True, sys.argv[0] is updated with the value of
       __file__ and sys.modules[__name__] is updated with a temporary
       module object for the module being executed. Both are
       restored to their original values before the function returns.

       Returns the resulting module globals dictionary.
    """
    mod_name, mod_spec, code = _get_module_details(mod_name)
    if run_name is None:
        run_name = mod_name
    if alter_sys:
        return _run_module_code(code, init_globals, run_name, mod_spec)
    else:
        return _run_code(code, {}, init_globals, run_name, mod_spec)

def _get_main_module_details(error=ImportError):
    main_name = '__main__'
    kwargs = {'name': main_name} if issubclass(error, ImportError) else {}
    saved_main = sys.modules[main_name]
    del sys.modules[main_name]
    try:
        return _get_module_details(main_name)
    except ImportError as exc:
        if main_name in str(exc):
            raise error("can't find %r module in %r" % (main_name, sys.path[0]), **kwargs) from exc
        raise
    finally:
        sys.modules[main_name] = saved_main

def _get_code_from_file(fname):
    from pkgutil import read_code
    code_path = os.path.abspath(fname)
    with io.open_code(code_path) as f:
        code = read_code(f)
    if code is None:
        with io.open_code(code_path) as f:
            code = compile(f.read(), fname, 'exec')
    return code

def 运行路径(path_name, init_globals=None, run_name=None):
    """Execute code located at the specified filesystem location.

       path_name -- filesystem location of a Python script, zipfile,
       or directory containing a top level __main__.py script.

       Optional arguments:
       init_globals -- dictionary used to pre-populate the module’s
       globals dictionary before the code is executed.

       run_name -- if not None, this will be used to set __name__;
       otherwise, '<run_path>' will be used for __name__.

       Returns the resulting module globals dictionary.
    """
    if run_name is None:
        run_name = '<run_path>'
    pkg_name = run_name.rpartition('.')[0]
    from pkgutil import get_importer
    importer = get_importer(path_name)
    path_name = os.fsdecode(path_name)
    if isinstance(importer, type(None)):
        code = _get_code_from_file(path_name)
        return _run_module_code(code, init_globals, run_name, pkg_name=pkg_name, script_name=path_name)
    else:
        sys.path.insert(0, path_name)
        try:
            mod_name, mod_spec, code = _get_main_module_details()
            with _TempModule(run_name) as temp_module, _ModifiedArgv0(path_name):
                mod_globals = temp_module.module.__dict__
                return _run_code(code, mod_globals, init_globals, run_name, mod_spec, pkg_name).copy()
        finally:
            try:
                sys.path.remove(path_name)
            except ValueError:
                pass
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('No module specified for execution', file=sys.stderr)
    else:
        del sys.argv[0]
        _run_module_as_main(sys.argv[0])


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'run_module': '运行模块',
    'run_path': '运行路径',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '运行模块',
    '运行路径',
])

# ---- 转发层结束 ----
