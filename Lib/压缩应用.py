# -*- coding: utf-8 -*-
"""压缩应用 —— 汉语库（由 tools/汉化库.py 从 Lib/zipapp.py 机械生成，**不要手改**）。

英文库 Lib/zipapp.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 压缩应用
"""


_英文原名表 = {'MAIN_TEMPLATE': '主模板', 'ZipAppError': '压缩应用错误', 'create_archive': '创建归档', 'get_interpreter': '取解释器', 'main': '主函数', 'shebang_encoding': '井号编码'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import contextlib
import os
import pathlib
import shutil
import stat
import sys
import zipfile
__all__ = ['ZipAppError', 'create_archive', 'get_interpreter']
主模板 = '# -*- coding: utf-8 -*-\nimport {module}\n{module}.{fn}()\n'
if sys.platform.startswith('win'):
    井号编码 = 'utf-8'
else:
    井号编码 = sys.getfilesystemencoding()

class 压缩应用错误(ValueError):
    pass

@contextlib.contextmanager
def _maybe_open(archive, mode):
    if isinstance(archive, (str, os.PathLike)):
        with open(archive, mode) as f:
            yield f
    else:
        yield archive

def _write_file_prefix(f, interpreter):
    """Write a shebang line."""
    if interpreter:
        shebang = b'#!' + interpreter.encode(井号编码) + b'\n'
        f.write(shebang)

def _copy_archive(archive, new_archive, interpreter=None):
    """Copy an application archive, modifying the shebang line."""
    with _maybe_open(archive, 'rb') as src:
        first_2 = src.read(2)
        if first_2 == b'#!':
            first_2 = b''
            src.readline()
        with _maybe_open(new_archive, 'wb') as dst:
            _write_file_prefix(dst, interpreter)
            dst.write(first_2)
            shutil.copyfileobj(src, dst)
    if interpreter and isinstance(new_archive, str):
        os.chmod(new_archive, os.stat(new_archive).st_mode | stat.S_IEXEC)

def 创建归档(source, target=None, interpreter=None, main=None, filter=None, compressed=False):
    """Create an application archive from SOURCE.

    The SOURCE can be the name of a directory, or a filename or a file-like
    object referring to an existing archive.

    The content of SOURCE is packed into an application archive in TARGET,
    which can be a filename or a file-like object.  If SOURCE is a directory,
    TARGET can be omitted and will default to the name of SOURCE with .pyz
    appended.

    The created application archive will have a shebang line specifying
    that it should run with INTERPRETER (there will be no shebang line if
    INTERPRETER is None), and a __main__.py which runs MAIN (if MAIN is
    not specified, an existing __main__.py will be used).  It is an error
    to specify MAIN for anything other than a directory source with no
    __main__.py, and it is an error to omit MAIN if the directory has no
    __main__.py.
    """
    source_is_file = False
    if hasattr(source, 'read') and hasattr(source, 'readline'):
        source_is_file = True
    else:
        source = pathlib.Path(source)
        if source.is_file():
            source_is_file = True
    if source_is_file:
        _copy_archive(source, target, interpreter)
        return
    if not source.exists():
        raise 压缩应用错误('Source does not exist')
    has_main = (source / '__main__.py').is_file()
    if main and has_main:
        raise 压缩应用错误('Cannot specify entry point if the source has __main__.py')
    if not (main or has_main):
        raise 压缩应用错误('Archive has no entry point')
    main_py = None
    if main:
        mod, sep, fn = main.partition(':')
        mod_ok = all((part.isidentifier() for part in mod.split('.')))
        fn_ok = all((part.isidentifier() for part in fn.split('.')))
        if not (sep == ':' and mod_ok and fn_ok):
            raise 压缩应用错误('Invalid entry point: ' + main)
        main_py = 主模板.format(module=mod, fn=fn)
    if target is None:
        target = source.with_suffix('.pyz')
    elif not hasattr(target, 'write'):
        target = pathlib.Path(target)
    files_to_add = {}
    for path in sorted(source.rglob('*')):
        relative_path = path.relative_to(source)
        if filter is None or filter(relative_path):
            files_to_add[path] = relative_path
    if target in files_to_add:
        raise 压缩应用错误(f'The target archive {target} overwrites one of the source files.')
    with _maybe_open(target, 'wb') as fd:
        _write_file_prefix(fd, interpreter)
        compression = zipfile.ZIP_DEFLATED if compressed else zipfile.ZIP_STORED
        with zipfile.ZipFile(fd, 'w', compression=compression) as z:
            for path, relative_path in files_to_add.items():
                z.write(path, relative_path.as_posix())
            if main_py:
                z.writestr('__main__.py', main_py.encode('utf-8'))
    if interpreter and (not hasattr(target, 'write')):
        target.chmod(target.stat().st_mode | stat.S_IEXEC)

def 取解释器(archive):
    with _maybe_open(archive, 'rb') as f:
        if f.read(2) == b'#!':
            return f.readline().strip().decode(井号编码)

def 主函数(args=None):
    """Run the zipapp command line interface.

    The ARGS parameter lets you specify the argument list directly.
    Omitting ARGS (or setting it to None) works as for argparse, using
    sys.argv[1:] as the argument list.
    """
    import argparse
    parser = argparse.ArgumentParser(color=True)
    parser.add_argument('--output', '-o', default=None, help='The name of the output archive. Required if SOURCE is an archive.')
    parser.add_argument('--python', '-p', default=None, help='The name of the Python interpreter to use (default: no shebang line).')
    parser.add_argument('--main', '-m', default=None, help='The main function of the application (default: use an existing __main__.py).')
    parser.add_argument('--compress', '-c', action='store_true', help='Compress files with the deflate method. Files are stored uncompressed by default.')
    parser.add_argument('--info', default=False, action='store_true', help='Display the interpreter from the archive.')
    parser.add_argument('source', help='Source directory (or existing archive).')
    args = parser.parse_args(args)
    if args.info:
        if not os.path.isfile(args.source):
            raise SystemExit('Can only get info for an archive file')
        interpreter = 取解释器(args.source)
        print('Interpreter: {}'.format(interpreter or '<none>'))
        sys.exit(0)
    if os.path.isfile(args.source):
        if args.output is None or (os.path.exists(args.output) and os.path.samefile(args.source, args.output)):
            raise SystemExit('In-place editing of archives is not supported')
        if args.main:
            raise SystemExit('Cannot change the main function when copying')
    创建归档(args.source, args.output, interpreter=args.python, main=args.main, compressed=args.compress)
if __name__ == '__main__':
    主函数()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'MAIN_TEMPLATE': '主模板',
    'ZipAppError': '压缩应用错误',
    'create_archive': '创建归档',
    'get_interpreter': '取解释器',
    'main': '主函数',
    'shebang_encoding': '井号编码',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '创建归档',
    '压缩应用错误',
    '取解释器',
]

# ---- 转发层结束 ----
