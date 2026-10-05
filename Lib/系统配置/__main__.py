# -*- coding: utf-8 -*-
"""系统配置.__main__ —— 汉语库（由 tools/汉化库.py 从 Lib/sysconfig/__main__.py 机械生成，**不要手改**）。

英文库 Lib/sysconfig.__main__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py sysconfig
"""


import json
import os
import sys
import types
from 系统配置 import _ALWAYS_STR, _PYTHON_BUILD, _get_sysconfigdata_name, get_config_h_filename, get_config_var, get_config_vars, get_default_scheme, get_makefile_filename, get_paths, get_platform, get_python_version, parse_config_h
_variable_rx = '([a-zA-Z][a-zA-Z0-9_]+)\\s*=\\s*(.*)'
_findvar1_rx = '\\$\\(([A-Za-z][A-Za-z0-9_]*)\\)'
_findvar2_rx = '\\${([A-Za-z][A-Za-z0-9_]*)}'

def _parse_makefile(filename, vars=None, keep_unresolved=True):
    """Parse a Makefile-style file.

    A dictionary containing name/value pairs is returned.  If an
    optional dictionary is passed in as the second argument, it is
    used instead of a new dictionary.
    """
    import re
    if vars is None:
        vars = {}
    done = {}
    notdone = {}
    with open(filename, encoding=sys.getfilesystemencoding(), errors='surrogateescape') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('#') or line.strip() == '':
            continue
        m = re.match(_variable_rx, line)
        if m:
            n, v = m.group(1, 2)
            v = v.strip()
            tmpv = v.replace('$$', '')
            if '$' in tmpv:
                notdone[n] = v
            else:
                try:
                    if n in _ALWAYS_STR:
                        raise ValueError
                    v = int(v)
                except ValueError:
                    done[n] = v.replace('$$', '$')
                else:
                    done[n] = v
    variables = list(notdone.keys())
    renamed_variables = ('CFLAGS', 'LDFLAGS', 'CPPFLAGS')
    while len(variables) > 0:
        for name in tuple(variables):
            value = notdone[name]
            m1 = re.search(_findvar1_rx, value)
            m2 = re.search(_findvar2_rx, value)
            if m1 and m2:
                m = m1 if m1.start() < m2.start() else m2
            else:
                m = m1 if m1 else m2
            if m is not None:
                n = m.group(1)
                found = True
                if n in done:
                    item = str(done[n])
                elif n in notdone:
                    found = False
                elif n in os.environ:
                    item = os.environ[n]
                elif n in renamed_variables:
                    if name.startswith('PY_') and name[3:] in renamed_variables:
                        item = ''
                    elif 'PY_' + n in notdone:
                        found = False
                    else:
                        item = str(done['PY_' + n])
                else:
                    done[n] = item = ''
                if found:
                    after = value[m.end():]
                    value = value[:m.start()] + item + after
                    if '$' in after:
                        notdone[name] = value
                    else:
                        try:
                            if name in _ALWAYS_STR:
                                raise ValueError
                            value = int(value)
                        except ValueError:
                            done[name] = value.strip()
                        else:
                            done[name] = value
                        variables.remove(name)
                        if name.startswith('PY_') and name[3:] in renamed_variables:
                            name = name[3:]
                            if name not in done:
                                done[name] = value
            else:
                if keep_unresolved:
                    done[name] = value
                variables.remove(name)
    for k, v in done.items():
        if isinstance(v, str):
            done[k] = v.strip()
    vars.update(done)
    return vars

def _print_config_dict(d, stream):
    print('{', file=stream)
    for k, v in sorted(d.items()):
        print(f'    {k!r}: {v!r},', file=stream)
    print('}', file=stream)

def _get_pybuilddir():
    pybuilddir = f'build/lib.{get_platform()}-{get_python_version()}'
    if get_config_var('Py_DEBUG') == '1':
        pybuilddir += '-pydebug'
    return pybuilddir

def _get_json_data_name():
    name = _get_sysconfigdata_name()
    assert name.startswith('_sysconfigdata')
    return name.replace('_sysconfigdata', '_sysconfig_vars') + '.json'

def _generate_posix_vars():
    """Generate the Python module containing build-time variables."""
    vars = {}
    makefile = get_makefile_filename()
    try:
        _parse_makefile(makefile, vars)
    except OSError as e:
        msg = f'invalid Python installation: unable to open {makefile}'
        if hasattr(e, 'strerror'):
            msg = f'{msg} ({e.strerror})'
        raise OSError(msg)
    config_h = get_config_h_filename()
    try:
        with open(config_h, encoding='utf-8') as f:
            parse_config_h(f, vars)
    except OSError as e:
        msg = f'invalid Python installation: unable to open {config_h}'
        if hasattr(e, 'strerror'):
            msg = f'{msg} ({e.strerror})'
        raise OSError(msg)
    if _PYTHON_BUILD:
        vars['BLDSHARED'] = vars['LDSHARED']
    name = _get_sysconfigdata_name()
    module = types.ModuleType(name)
    module.build_time_vars = vars
    sys.modules[name] = module
    pybuilddir = _get_pybuilddir()
    os.makedirs(pybuilddir, exist_ok=True)
    destfile = os.path.join(pybuilddir, name + '.py')
    with open(destfile, 'w', encoding='utf8') as f:
        f.write('# system configuration generated and used by the sysconfig module\n')
        f.write('build_time_vars = ')
        _print_config_dict(vars, stream=f)
    print(f'Written {destfile}')
    install_vars = get_config_vars()
    install_vars['projectbase'] = install_vars['BINDIR']
    install_vars['srcdir'] = install_vars['LIBPL']
    jsonfile = os.path.join(pybuilddir, _get_json_data_name())
    with open(jsonfile, 'w') as f:
        json.dump(install_vars, f, indent=2)
    print(f'Written {jsonfile}')
    with open('pybuilddir.txt', 'w', encoding='utf8') as f:
        f.write(pybuilddir)

def _print_dict(title, data):
    for index, (key, value) in enumerate(sorted(data.items())):
        if index == 0:
            print(f'{title}: ')
        print(f'\t{key} = "{value}"')

def _main():
    """Display all information sysconfig detains."""
    if '--generate-posix-vars' in sys.argv:
        _generate_posix_vars()
        return
    print(f'Platform: "{get_platform()}"')
    print(f'Python version: "{get_python_version()}"')
    print(f'Current installation scheme: "{get_default_scheme()}"')
    print()
    _print_dict('Paths', get_paths())
    print()
    _print_dict('Variables', get_config_vars())
if __name__ == '__main__':
    try:
        _main()
    except BrokenPipeError:
        pass


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# ---- 转发层结束 ----
