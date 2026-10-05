# -*- coding: utf-8 -*-
"""虚拟环境.__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/venv/__init__.py 机械生成，**不要手改**）。

英文库 Lib/venv.__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py venv
"""


"""
Virtual environment (venv) package for Python. Based on PEP 405.

Copyright (C) 2011-2014 Vinay Sajip.
Licensed to the PSF under a contributor agreement.
"""
_英文原名表 = {'CORE_VENV_DEPS': '核心依赖', 'EnvBuilder': '环境构建器', 'create': '创建', 'main': '主函数'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
_实例属性全表 = {}
_反表 = {}

def _装类转发(_类, _对, _属性=None):
    if getattr(_类, '__module__', None) != __name__:
        return
    for _英, _中 in _对.items():
        if _中 in _类.__dict__:
            setattr(_类, _英, _类.__dict__[_中])
    if _属性:
        _实例属性全表.update(_属性)
        _反表.update({_中: _英 for _英, _中 in _属性.items()})
        for _英, _中 in _属性.items():
            if _英 not in _类.__dict__ and _中 in _类.__dict__:
                setattr(_类, _英, _类.__dict__[_中])
        if '__getattr__' not in _类.__dict__:

            def _取(self, _名, _对=_实例属性全表, _反=_反表):
                if _名 in _对:
                    try:
                        return object.__getattribute__(self, _对[_名])
                    except AttributeError:
                        pass
                    try:
                        return object.__getattribute__(self, _名)
                    except AttributeError:
                        pass
                if _名 in _反:
                    try:
                        return object.__getattribute__(self, _反[_名])
                    except AttributeError:
                        pass
                raise AttributeError(_名)
            try:
                _类.__getattr__ = _取
            except TypeError:
                return
        if not [_基 for _基 in _类.__mro__ if _基 is not object and '__setattr__' in _基.__dict__ and (not getattr(_基.__dict__['__setattr__'], '_中文转发钩子', False))]:

            def _设(self, _名, _值, _对=_实例属性全表, _反=_反表):
                _英 = _名 if _名 in _对 else _反.get(_名)
                if _英 is None:
                    object.__setattr__(self, _名, _值)
                    return
                _中 = _对[_英]
                _成 = False
                for _名2 in (_中, _英):
                    try:
                        object.__setattr__(self, _名2, _值)
                        _成 = True
                    except AttributeError:
                        pass
                if not _成:
                    raise AttributeError(_名)
            _设._中文转发钩子 = True
            try:
                _类.__setattr__ = _设
            except TypeError:
                return
import logging
import os
import shutil
import subprocess
import sys
import sysconfig
import types
import shlex
核心依赖 = ('pip',)
logger = logging.getLogger(__name__)

class 环境构建器:
    """
    This class exists to allow virtual environment creation to be
    customized. The constructor parameters determine the builder's
    behaviour when called upon to create a virtual environment.

    By default, the builder makes the system (global) site-packages dir
    *un*available to the created environment.

    If invoked using the Python -m option, the default is to use copying
    on Windows platforms but symlinks elsewhere. If instantiated some
    other way, the default is to *not* use symlinks.

    :param system_site_packages: If True, the system (global) site-packages
                                 dir is available to created environments.
    :param clear: If True, delete the contents of the environment directory if
                  it already exists, before environment creation.
    :param symlinks: If True, attempt to symlink rather than copy files into
                     virtual environment.
    :param upgrade: If True, upgrade an existing virtual environment.
    :param with_pip: If True, ensure pip is installed in the virtual
                     environment
    :param prompt: Alternative terminal prefix for the environment.
    :param upgrade_deps: Update the base venv modules to the latest on PyPI
    :param scm_ignore_files: Create ignore files for the SCMs specified by the
                             iterable.
    """

    def __init__(self, system_site_packages=False, clear=False, symlinks=False, upgrade=False, with_pip=False, prompt=None, upgrade_deps=False, *, scm_ignore_files=frozenset()):
        self.system_site_packages = system_site_packages
        self.clear = clear
        self.symlinks = symlinks
        self.upgrade = upgrade
        self.with_pip = with_pip
        self.orig_prompt = prompt
        if prompt == '.':
            prompt = os.path.basename(os.getcwd())
        self.prompt = prompt
        self.upgrade_deps = upgrade_deps
        self.scm_ignore_files = frozenset(map(str.lower, scm_ignore_files))

    def 创建(self, env_dir):
        """
        Create a virtual environment in a directory.

        :param env_dir: The target directory to create an environment in.

        """
        env_dir = os.path.abspath(env_dir)
        context = self.确保目录(env_dir)
        for scm in self.scm_ignore_files:
            getattr(self, f'create_{scm}_ignore_file')(context)
        true_system_site_packages = self.system_site_packages
        self.system_site_packages = False
        self.创建配置(context)
        self.setup_python(context)
        if self.with_pip:
            self._setup_pip(context)
        if not self.upgrade:
            self.布置脚本(context)
            self.后置设置(context)
        if true_system_site_packages:
            self.system_site_packages = True
            self.创建配置(context)
        if self.upgrade_deps:
            self.升级依赖(context)

    def 清空目录(self, path):
        for fn in os.listdir(path):
            fn = os.path.join(path, fn)
            if os.path.islink(fn) or os.path.isfile(fn):
                os.remove(fn)
            elif os.path.isdir(fn):
                shutil.rmtree(fn)

    def _venv_path(self, env_dir, name):
        vars = {'base': env_dir, 'platbase': env_dir}
        return sysconfig.get_path(name, scheme='venv', vars=vars)

    @classmethod
    def _same_path(cls, path1, path2):
        """Check whether two paths appear the same.

        Whether they refer to the same file is irrelevant; we're testing for
        whether a human reader would look at the path string and easily tell
        that they're the same file.
        """
        if sys.platform == 'win32':
            if os.path.normcase(path1) == os.path.normcase(path2):
                return True
            import _winapi
            try:
                path1 = _winapi.GetLongPathName(os.fsdecode(path1))
            except OSError:
                pass
            try:
                path2 = _winapi.GetLongPathName(os.fsdecode(path2))
            except OSError:
                pass
            if os.path.normcase(path1) == os.path.normcase(path2):
                return True
            return False
        else:
            return path1 == path2

    def 确保目录(self, env_dir):
        """
        Create the directories for the environment.

        Returns a context object which holds paths in the environment,
        for use by subsequent logic.
        """

        def create_if_needed(d):
            if not os.path.exists(d):
                os.makedirs(d)
            elif os.path.islink(d) or os.path.isfile(d):
                raise ValueError('Unable to create directory %r' % d)
        if os.pathsep in os.fspath(env_dir):
            raise ValueError(f'Refusing to create a venv in {env_dir} because it contains the PATH separator {os.pathsep}.')
        if os.path.exists(env_dir) and self.clear:
            self.清空目录(env_dir)
        context = types.SimpleNamespace()
        context.env_dir = env_dir
        context.env_name = os.path.split(env_dir)[1]
        context.prompt = self.prompt if self.prompt is not None else context.env_name
        create_if_needed(env_dir)
        executable = sys._base_executable
        if not executable:
            raise ValueError('Unable to determine path to the running Python interpreter. Provide an explicit path or check that your PATH environment variable is correctly set.')
        dirname, exename = os.path.split(os.path.abspath(executable))
        if sys.platform == 'win32':
            _d = '_d' if os.path.splitext(exename)[0].endswith('_d') else ''
            exename = f'python{_d}.exe'
        context.executable = executable
        context.python_dir = dirname
        context.python_exe = exename
        binpath = self._venv_path(env_dir, 'scripts')
        libpath = self._venv_path(env_dir, 'purelib')
        incpath = os.path.join(env_dir, 'Include' if os.name == 'nt' else 'include')
        context.inc_path = incpath
        create_if_needed(incpath)
        context.lib_path = libpath
        create_if_needed(libpath)
        if sys.maxsize > 2 ** 32 and os.name == 'posix' and (sys.platform != 'darwin'):
            link_path = os.path.join(env_dir, 'lib64')
            if not os.path.exists(link_path):
                os.symlink('lib', link_path)
        context.bin_path = binpath
        context.bin_name = os.path.relpath(binpath, env_dir)
        context.env_exe = os.path.join(binpath, exename)
        create_if_needed(binpath)
        context.env_exec_cmd = context.env_exe
        if sys.platform == 'win32':
            real_env_exe = os.path.realpath(context.env_exe)
            if not self._same_path(real_env_exe, context.env_exe):
                logger.warning('Actual environment location may have moved due to redirects, links or junctions.\n  Requested location: "%s"\n  Actual location:    "%s"', context.env_exe, real_env_exe)
                context.env_exec_cmd = real_env_exe
        return context

    def 创建配置(self, context):
        """
        Create a configuration file indicating where the environment's Python
        was copied from, and whether the system site-packages should be made
        available in the environment.

        :param context: The information for the environment creation request
                        being processed.
        """
        context.cfg_path = path = os.path.join(context.env_dir, 'pyvenv.cfg')
        with open(path, 'w', encoding='utf-8') as f:
            f.write('home = %s\n' % context.python_dir)
            if self.system_site_packages:
                incl = 'true'
            else:
                incl = 'false'
            f.write('include-system-site-packages = %s\n' % incl)
            f.write('version = %d.%d.%d\n' % sys.version_info[:3])
            if self.prompt is not None:
                f.write(f'prompt = {self.prompt!r}\n')
            f.write('executable = %s\n' % os.path.realpath(sys.executable))
            args = []
            nt = os.name == 'nt'
            if nt and self.symlinks:
                args.append('--symlinks')
            if not nt and (not self.symlinks):
                args.append('--copies')
            if not self.with_pip:
                args.append('--without-pip')
            if self.system_site_packages:
                args.append('--system-site-packages')
            if self.clear:
                args.append('--clear')
            if self.upgrade:
                args.append('--upgrade')
            if self.upgrade_deps:
                args.append('--upgrade-deps')
            if self.orig_prompt is not None:
                args.append(f'--prompt="{self.orig_prompt}"')
            if not self.scm_ignore_files:
                args.append('--without-scm-ignore-files')
            args.append(context.env_dir)
            args = ' '.join(args)
            f.write(f'command = {sys.executable} -m venv {args}\n')

    def 符号链接或复制(self, src, dst, relative_symlinks_ok=False):
        """
        Try symlinking a file, and if that fails, fall back to copying.
        (Unused on Windows, because we can't just copy a failed symlink file: we
        switch to a different set of files instead.)
        """
        assert os.name != 'nt'
        force_copy = not self.symlinks
        if not force_copy:
            try:
                if not os.path.islink(dst):
                    if relative_symlinks_ok:
                        assert os.path.dirname(src) == os.path.dirname(dst)
                        os.symlink(os.path.basename(src), dst)
                    else:
                        os.symlink(src, dst)
            except Exception:
                logger.warning('Unable to symlink %r to %r', src, dst)
                force_copy = True
        if force_copy:
            shutil.copyfile(src, dst)

    def 创建git忽略文件(self, context):
        """
        Create a .gitignore file in the environment directory.

        The contents of the file cause the entire environment directory to be
        ignored by git.
        """
        gitignore_path = os.path.join(context.env_dir, '.gitignore')
        with open(gitignore_path, 'w', encoding='utf-8') as file:
            file.write('# Created by venv; see https://docs.python.org/3/library/venv.html\n')
            file.write('*\n')
    if os.name != 'nt':

        def setup_python(self, context):
            """
            Set up a Python executable in the environment.

            :param context: The information for the environment creation request
                            being processed.
            """
            binpath = context.bin_path
            path = context.env_exe
            copier = self.符号链接或复制
            dirname = context.python_dir
            copier(context.executable, path)
            if not os.path.islink(path):
                os.chmod(path, 493)
            suffixes = ['python', 'python3', f'python3.{sys.version_info[1]}']
            if sys.version_info[:2] == (3, 14) and sys.getfilesystemencoding() == 'utf-8':
                suffixes.append('𝜋thon')
            for suffix in suffixes:
                path = os.path.join(binpath, suffix)
                if not os.path.exists(path):
                    copier(context.env_exe, path, relative_symlinks_ok=True)
                    if not os.path.islink(path):
                        os.chmod(path, 493)
    else:

        def setup_python(self, context):
            """
            Set up a Python executable in the environment.

            :param context: The information for the environment creation request
                            being processed.
            """
            binpath = context.bin_path
            dirname = context.python_dir
            exename = os.path.basename(context.env_exe)
            exe_stem = os.path.splitext(exename)[0]
            exe_d = '_d' if os.path.normcase(exe_stem).endswith('_d') else ''
            if sysconfig.is_python_build():
                scripts = dirname
            else:
                scripts = os.path.join(os.path.dirname(__file__), 'scripts', 'nt')
            if not sysconfig.get_config_var('Py_GIL_DISABLED'):
                python_exe = os.path.join(dirname, f'python{exe_d}.exe')
                pythonw_exe = os.path.join(dirname, f'pythonw{exe_d}.exe')
                link_sources = {'python.exe': python_exe, f'python{exe_d}.exe': python_exe, 'pythonw.exe': pythonw_exe, f'pythonw{exe_d}.exe': pythonw_exe}
                python_exe = os.path.join(scripts, f'venvlauncher{exe_d}.exe')
                pythonw_exe = os.path.join(scripts, f'venvwlauncher{exe_d}.exe')
                copy_sources = {'python.exe': python_exe, f'python{exe_d}.exe': python_exe, 'pythonw.exe': pythonw_exe, f'pythonw{exe_d}.exe': pythonw_exe}
            else:
                exe_t = f'3.{sys.version_info[1]}t'
                python_exe = os.path.join(dirname, f'python{exe_t}{exe_d}.exe')
                pythonw_exe = os.path.join(dirname, f'pythonw{exe_t}{exe_d}.exe')
                link_sources = {'python.exe': python_exe, f'python{exe_d}.exe': python_exe, f'python{exe_t}.exe': python_exe, f'python{exe_t}{exe_d}.exe': python_exe, 'pythonw.exe': pythonw_exe, f'pythonw{exe_d}.exe': pythonw_exe, f'pythonw{exe_t}.exe': pythonw_exe, f'pythonw{exe_t}{exe_d}.exe': pythonw_exe}
                python_exe = os.path.join(scripts, f'venvlaunchert{exe_d}.exe')
                pythonw_exe = os.path.join(scripts, f'venvwlaunchert{exe_d}.exe')
                copy_sources = {'python.exe': python_exe, f'python{exe_d}.exe': python_exe, f'python{exe_t}.exe': python_exe, f'python{exe_t}{exe_d}.exe': python_exe, 'pythonw.exe': pythonw_exe, f'pythonw{exe_d}.exe': pythonw_exe, f'pythonw{exe_t}.exe': pythonw_exe, f'pythonw{exe_t}{exe_d}.exe': pythonw_exe}
            do_copies = True
            if self.symlinks:
                do_copies = False
                link_sources.update({f: os.path.join(dirname, f) for f in os.listdir(dirname) if os.path.normcase(f).startswith(('python', 'vcruntime')) and os.path.normcase(os.path.splitext(f)[1]) == '.dll'})
                to_unlink = []
                for dest, src in link_sources.items():
                    dest = os.path.join(binpath, dest)
                    try:
                        os.symlink(src, dest)
                        to_unlink.append(dest)
                    except OSError:
                        logger.warning('Unable to symlink %r to %r', src, dest)
                        do_copies = True
                        for f in to_unlink:
                            try:
                                os.unlink(f)
                            except OSError:
                                logger.warning('Failed to clean up symlink %r', f)
                        logger.warning('Retrying with copies')
                        break
            if do_copies:
                for dest, src in copy_sources.items():
                    dest = os.path.join(binpath, dest)
                    try:
                        shutil.copy2(src, dest)
                    except OSError:
                        logger.warning('Unable to copy %r to %r', src, dest)
            if sysconfig.is_python_build():
                for root, dirs, files in os.walk(context.python_dir):
                    if 'init.tcl' in files:
                        tcldir = os.path.basename(root)
                        tcldir = os.path.join(context.env_dir, 'Lib', tcldir)
                        if not os.path.exists(tcldir):
                            os.makedirs(tcldir)
                        src = os.path.join(root, 'init.tcl')
                        dst = os.path.join(tcldir, 'init.tcl')
                        shutil.copyfile(src, dst)
                        break

    def _call_new_python(self, context, *py_args, **kwargs):
        """Executes the newly created Python using safe-ish options"""
        args = [context.env_exec_cmd, *py_args]
        kwargs['env'] = env = os.environ.copy()
        env['VIRTUAL_ENV'] = context.env_dir
        env.pop('PYTHONHOME', None)
        env.pop('PYTHONPATH', None)
        kwargs['cwd'] = context.env_dir
        kwargs['executable'] = context.env_exec_cmd
        subprocess.check_output(args, **kwargs)

    def _setup_pip(self, context):
        """Installs or upgrades pip in a virtual environment"""
        self._call_new_python(context, '-m', 'ensurepip', '--upgrade', '--default-pip', stderr=subprocess.STDOUT)

    def 布置脚本(self, context):
        """
        Set up scripts into the created environment from a directory.

        This method installs the default scripts into the environment
        being created. You can prevent the default installation by overriding
        this method if you really need to, or if you need to specify
        a different location for the scripts to install. By default, the
        'scripts' directory in the venv package is used as the source of
        scripts to install.
        """
        path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(path, 'scripts')
        self.安装脚本(context, path)

    def 后置设置(self, context):
        """
        Hook for post-setup modification of the venv. Subclasses may install
        additional packages or scripts here, add activation shell scripts, etc.

        :param context: The information for the environment creation request
                        being processed.
        """
        pass

    def 替换变量(self, text, context):
        """
        Replace variable placeholders in script text with context-specific
        variables.

        Return the text passed in , but with variables replaced.

        :param text: The text in which to replace placeholder variables.
        :param context: The information for the environment creation request
                        being processed.
        """
        replacements = {'__VENV_DIR__': context.env_dir, '__VENV_NAME__': context.env_name, '__VENV_PROMPT__': context.prompt, '__VENV_BIN_NAME__': context.bin_name, '__VENV_PYTHON__': context.env_exe}

        def quote_ps1(s):
            """
            This should satisfy PowerShell quoting rules [1], unless the quoted
            string is passed directly to Windows native commands [2].
            [1]: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules
            [2]: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing#passing-arguments-that-contain-quote-characters
            """
            s = s.replace("'", "''")
            return f"'{s}'"

        def quote_bat(s):
            return s
        quote = shlex.quote
        script_path = context.script_path
        if script_path.endswith('.ps1'):
            quote = quote_ps1
        elif script_path.endswith('.bat'):
            quote = quote_bat
        else:
            quote = shlex.quote
        replacements = {key: quote(s) for key, s in replacements.items()}
        for key, quoted in replacements.items():
            text = text.replace(key, quoted)
        return text

    def 安装脚本(self, context, path):
        """
        Install scripts into the created environment from a directory.

        :param context: The information for the environment creation request
                        being processed.
        :param path:    Absolute pathname of a directory containing script.
                        Scripts in the 'common' subdirectory of this directory,
                        and those in the directory named for the platform
                        being run on, are installed in the created environment.
                        Placeholder variables are replaced with environment-
                        specific values.
        """
        binpath = context.bin_path
        plen = len(path)
        if os.name == 'nt':

            def skip_file(f):
                f = os.path.normcase(f)
                return f.startswith(('python', 'venv')) and f.endswith(('.exe', '.pdb'))
        else:

            def skip_file(f):
                return False
        for root, dirs, files in os.walk(path):
            if root == path:
                for d in dirs[:]:
                    if d not in ('common', os.name):
                        dirs.remove(d)
                continue
            for f in files:
                if skip_file(f):
                    continue
                srcfile = os.path.join(root, f)
                suffix = root[plen:].split(os.sep)[2:]
                if not suffix:
                    dstdir = binpath
                else:
                    dstdir = os.path.join(binpath, *suffix)
                if not os.path.exists(dstdir):
                    os.makedirs(dstdir)
                dstfile = os.path.join(dstdir, f)
                if os.name == 'nt' and srcfile.endswith(('.exe', '.pdb')):
                    shutil.copy2(srcfile, dstfile)
                    continue
                with open(srcfile, 'rb') as f:
                    data = f.read()
                try:
                    context.script_path = srcfile
                    new_data = self.替换变量(data.decode('utf-8'), context).encode('utf-8')
                except UnicodeError as e:
                    logger.warning('unable to copy script %r, may be binary: %s', srcfile, e)
                    continue
                if new_data == data:
                    shutil.copy(srcfile, dstfile)
                else:
                    with open(dstfile, 'wb') as f:
                        f.write(new_data)
                    shutil.copymode(srcfile, dstfile)

    def 升级依赖(self, context):
        logger.debug(f'Upgrading {核心依赖} packages in {context.bin_path}')
        self._call_new_python(context, '-m', 'pip', 'install', '--upgrade', *核心依赖)
_装类转发(环境构建器, {'clear_directory': '清空目录', 'create': '创建', 'create_configuration': '创建配置', 'create_git_ignore_file': '创建git忽略文件', 'ensure_directories': '确保目录', 'install_scripts': '安装脚本', 'post_setup': '后置设置', 'replace_variables': '替换变量', 'setup_scripts': '布置脚本', 'symlink_or_copy': '符号链接或复制', 'upgrade_dependencies': '升级依赖'}, {'clear_directory': '清空目录', 'create': '创建', 'create_configuration': '创建配置', 'create_git_ignore_file': '创建git忽略文件', 'ensure_directories': '确保目录', 'install_scripts': '安装脚本', 'post_setup': '后置设置', 'replace_variables': '替换变量', 'setup_scripts': '布置脚本', 'symlink_or_copy': '符号链接或复制', 'upgrade_dependencies': '升级依赖'})

def 创建(env_dir, system_site_packages=False, clear=False, symlinks=False, with_pip=False, prompt=None, upgrade_deps=False, *, scm_ignore_files=frozenset()):
    """Create a virtual environment in a directory."""
    builder = 环境构建器(system_site_packages=system_site_packages, clear=clear, symlinks=symlinks, with_pip=with_pip, prompt=prompt, upgrade_deps=upgrade_deps, scm_ignore_files=scm_ignore_files)
    builder.create(env_dir)

def 主函数(args=None):
    import argparse
    parser = argparse.ArgumentParser(description='Creates virtual Python environments in one or more target directories.', epilog='Once an environment has been created, you may wish to activate it, e.g. by sourcing an activate script in its bin directory.', color=True)
    parser.add_argument('dirs', metavar='ENV_DIR', nargs='+', help='A directory to create the environment in.')
    parser.add_argument('--system-site-packages', default=False, action='store_true', dest='system_site', help='Give the virtual environment access to the system site-packages dir.')
    if os.name == 'nt':
        use_symlinks = False
    else:
        use_symlinks = True
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--symlinks', default=use_symlinks, action='store_true', dest='symlinks', help='Try to use symlinks rather than copies, when symlinks are not the default for the platform.')
    group.add_argument('--copies', default=not use_symlinks, action='store_false', dest='symlinks', help='Try to use copies rather than symlinks, even when symlinks are the default for the platform.')
    parser.add_argument('--clear', default=False, action='store_true', dest='clear', help='Delete the contents of the environment directory if it already exists, before environment creation.')
    parser.add_argument('--upgrade', default=False, action='store_true', dest='upgrade', help='Upgrade the environment directory to use this version of Python, assuming Python has been upgraded in-place.')
    parser.add_argument('--without-pip', dest='with_pip', default=True, action='store_false', help='Skips installing or upgrading pip in the virtual environment (pip is bootstrapped by default)')
    parser.add_argument('--prompt', help='Provides an alternative prompt prefix for this environment.')
    parser.add_argument('--upgrade-deps', default=False, action='store_true', dest='upgrade_deps', help=f"Upgrade core dependencies ({', '.join(核心依赖)}) to the latest version in PyPI")
    parser.add_argument('--without-scm-ignore-files', dest='scm_ignore_files', action='store_const', const=frozenset(), default=frozenset(['git']), help='Skips adding SCM ignore files to the environment directory (Git is supported by default).')
    options = parser.parse_args(args)
    if options.upgrade and options.clear:
        raise ValueError('you cannot supply --upgrade and --clear together.')
    builder = 环境构建器(system_site_packages=options.system_site, clear=options.clear, symlinks=options.symlinks, upgrade=options.upgrade, with_pip=options.with_pip, prompt=options.prompt, upgrade_deps=options.upgrade_deps, scm_ignore_files=options.scm_ignore_files)
    for d in options.dirs:
        builder.create(d)
if __name__ == '__main__':
    rc = 1
    try:
        主函数()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'CORE_VENV_DEPS': '核心依赖',
    'EnvBuilder': '环境构建器',
    'create': '创建',
    'main': '主函数',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '环境构建器': {
        'clear_directory': '清空目录',
        'create': '创建',
        'create_configuration': '创建配置',
        'create_git_ignore_file': '创建git忽略文件',
        'ensure_directories': '确保目录',
        'install_scripts': '安装脚本',
        'post_setup': '后置设置',
        'replace_variables': '替换变量',
        'setup_scripts': '布置脚本',
        'symlink_or_copy': '符号链接或复制',
        'upgrade_dependencies': '升级依赖',
    },
}
_转发跳过 = []
_无 = object()    # 哨兵：类属性**值就是 None** 时 ≠ 「没找到」（D-126 修的真 bug）
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # ★必须从 __dict__ 拿**描述符本体**，不能用 getattr(类, 名)：
        #   getattr 会把 classmethod/staticmethod/property **绑到本类上**，
        #   再挂成别名之后，**子类**调用拿到的还是绑死在本类的那个 ——
        #   DummyFraction.from_number(...) 会返回基类实例
        #   （fractions 的 testFromNumber_subclass 就是这么挂的，见 D-035）。
        _原 = _类.__dict__.get(_中, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _中 in _基.__dict__:
                    _原 = _基.__dict__[_中]
                    break
        if _原 is _无:
            _转发跳过.append((_类名, _英, _中))
            continue
        setattr(_类, _英, _原)

# 中文成员名的兜底（D-125 起，D-126 推广到全部类）：上面主循环只认「中文名在类里」，
#   找不到就跳过 —— 可中文名**本来就不在类里**有两种情况：① 类名走了身份别名
#   （机制 3），指向英文那个对象；② 改名被规则挡下（那个名字是 import 进来的）。
#   实测 `注解库.前向引用('X').求值()`、`选择器.select选择器.选择` 都是 AttributeError。
#   这里反过来挂：从英文名取**描述符本体**，把中文名加上去。只加描述符别名，
#   **不装钩子**（英文类协议不改，照 D-070）；C 类型不可变、setattr 抛 TypeError 就跳过
#   （C 类型的方法名归机制 1 的方法名表管）。
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # 中文名已经在类里（改名成功）⇒ 没事，主循环已把英文名补回去了。
        if _中 in _类.__dict__ or any(_中 in _基.__dict__ for _基 in _类.__mro__):
            continue
        _原 = _类.__dict__.get(_英, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _英 in _基.__dict__:
                    _原 = _基.__dict__[_英]
                    break
        if _原 is None:
            _转发跳过.append((_类名, _英, _中))
            continue
        try:
            setattr(_类, _中, _原)
        except TypeError:
            continue    # C 类型不可变挂不上；主循环已经记过一笔，不重复记
        if (_类名, _英, _中) in _转发跳过:
            _转发跳过.remove((_类名, _英, _中))

# 实例属性：两个方向都翻（英文名 <-> 中文名）。
# **逻辑只有一份**，在 `_装类转发` 里 —— 每个类定义紧后面已经装过一次
# （照 D-040），这里是文件末尾的兜底，幂等。
_实例属性 = {
    '环境构建器': {
        'clear_directory': '清空目录',
        'create': '创建',
        'create_configuration': '创建配置',
        'create_git_ignore_file': '创建git忽略文件',
        'ensure_directories': '确保目录',
        'install_scripts': '安装脚本',
        'post_setup': '后置设置',
        'replace_variables': '替换变量',
        'setup_scripts': '布置脚本',
        'symlink_or_copy': '符号链接或复制',
        'upgrade_dependencies': '升级依赖',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
