# -*- coding: utf-8 -*-
"""确保pip.__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/ensurepip/__init__.py 机械生成，**不要手改**）。

英文库 Lib/ensurepip.__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py ensurepip
"""


_英文原名表 = {'bootstrap': '引导安装', 'version': '版本'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import os
import subprocess
import sys
import sysconfig
import tempfile
from contextlib import nullcontext
from importlib import resources
from pathlib import Path
from shutil import copy2
__all__ = ['version', 'bootstrap']
_PIP_VERSION = '26.2.1'
_pkg_dir = sysconfig.get_config_var('WHEEL_PKG_DIR')
if _pkg_dir:
    _WHEEL_PKG_DIR = Path(_pkg_dir).resolve()
else:
    _WHEEL_PKG_DIR = None

def _find_wheel_pkg_dir_pip():
    if _WHEEL_PKG_DIR is None:
        return None
    dist_matching_wheels = _WHEEL_PKG_DIR.glob('pip-*.whl')
    try:
        last_matching_dist_wheel = sorted(dist_matching_wheels)[-1]
    except IndexError:
        return None
    return nullcontext(last_matching_dist_wheel)

def _get_pip_whl_path_ctx():
    if (alternative_pip_wheel_path := _find_wheel_pkg_dir_pip()) is not None:
        return alternative_pip_wheel_path
    return resources.as_file(resources.files('ensurepip') / '_bundled' / f'pip-{_PIP_VERSION}-py3-none-any.whl')

def _get_pip_version():
    with _get_pip_whl_path_ctx() as bundled_wheel_path:
        wheel_name = bundled_wheel_path.name
        return wheel_name.removeprefix('pip-').partition('-')[0]

def _run_pip(args, additional_paths=None):
    code = f'\nimport runpy\nimport sys\nsys.path = {additional_paths or []} + sys.path\nsys.argv[1:] = {args}\nrunpy.run_module("pip", run_name="__main__", alter_sys=True)\n'
    cmd = [sys.executable, '-W', 'ignore::DeprecationWarning', '-c', code]
    if sys.flags.isolated:
        cmd.insert(1, '-I')
    return subprocess.run(cmd, check=True).returncode

def 版本():
    """
    Returns a string specifying the bundled version of pip.
    """
    return _get_pip_version()

def _disable_pip_configuration_settings():
    keys_to_remove = [k for k in os.environ if k.startswith('PIP_')]
    for k in keys_to_remove:
        del os.environ[k]
    os.environ['PIP_CONFIG_FILE'] = os.devnull

def 引导安装(*, root=None, upgrade=False, user=False, altinstall=False, default_pip=False, verbosity=0):
    """
    Bootstrap pip into the current Python installation (or the given root
    directory).

    Note that calling this function will alter both sys.path and os.environ.
    """
    _bootstrap(root=root, upgrade=upgrade, user=user, altinstall=altinstall, default_pip=default_pip, verbosity=verbosity)

def _bootstrap(*, root=None, upgrade=False, user=False, altinstall=False, default_pip=False, verbosity=0):
    """
    Bootstrap pip into the current Python installation (or the given root
    directory). Returns pip command status code.

    Note that calling this function will alter both sys.path and os.environ.
    """
    if altinstall and default_pip:
        raise ValueError('Cannot use altinstall and default_pip together')
    sys.audit('ensurepip.bootstrap', root)
    _disable_pip_configuration_settings()
    if altinstall:
        os.environ['ENSUREPIP_OPTIONS'] = 'altinstall'
    elif not default_pip:
        os.environ['ENSUREPIP_OPTIONS'] = 'install'
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        with _get_pip_whl_path_ctx() as bundled_wheel_path:
            tmp_wheel_path = tmpdir_path / bundled_wheel_path.name
            copy2(bundled_wheel_path, tmp_wheel_path)
        args = ['install', '--no-cache-dir', '--no-index', '--find-links', tmpdir]
        if root:
            args += ['--root', root]
        if upgrade:
            args += ['--upgrade']
        if user:
            args += ['--user']
        if verbosity:
            args += ['-' + 'v' * verbosity]
        return _run_pip([*args, 'pip'], [os.fsdecode(tmp_wheel_path)])

def _uninstall_helper(*, verbosity=0):
    """Helper to support a clean default uninstall process on Windows

    Note that calling this function may alter os.environ.
    """
    try:
        import pip
    except ImportError:
        return
    available_version = 版本()
    if pip.__version__ != available_version:
        print(f'ensurepip will only uninstall a matching version ({pip.__version__!r} installed, {available_version!r} available)', file=sys.stderr)
        return
    _disable_pip_configuration_settings()
    args = ['uninstall', '-y', '--disable-pip-version-check']
    if verbosity:
        args += ['-' + 'v' * verbosity]
    return _run_pip([*args, 'pip'])

def _main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(color=True)
    parser.add_argument('--version', action='version', version='pip {}'.format(版本()), help='Show the version of pip that is bundled with this Python.')
    parser.add_argument('-v', '--verbose', action='count', default=0, dest='verbosity', help='Give more output. Option is additive, and can be used up to 3 times.')
    parser.add_argument('-U', '--upgrade', action='store_true', default=False, help='Upgrade pip and dependencies, even if already installed.')
    parser.add_argument('--user', action='store_true', default=False, help='Install using the user scheme.')
    parser.add_argument('--root', default=None, help='Install everything relative to this alternate root directory.')
    parser.add_argument('--altinstall', action='store_true', default=False, help='Make an alternate install, installing only the X.Y versioned scripts (Default: pipX, pipX.Y).')
    parser.add_argument('--default-pip', action='store_true', default=False, help='Make a default pip install, installing the unqualified pip in addition to the versioned scripts.')
    args = parser.parse_args(argv)
    return _bootstrap(root=args.root, upgrade=args.upgrade, user=args.user, verbosity=args.verbosity, altinstall=args.altinstall, default_pip=args.default_pip)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'bootstrap': '引导安装',
    'version': '版本',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '引导安装',
    '版本',
]

# ---- 转发层结束 ----
