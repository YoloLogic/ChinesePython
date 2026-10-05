# -*- coding: utf-8 -*-
"""C类型.util —— 汉语库（由 tools/汉化库.py 从 Lib/ctypes/util.py 机械生成，**不要手改**）。

英文库 Lib/ctypes.util.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py ctypes
"""


import os
import shutil
import subprocess
import sys
if os.name == 'nt':

    def _get_build_version():
        """Return the version of MSVC that was used to build Python.

        For Python 2.3 and up, the version number is included in
        sys.version.  For earlier versions, assume the compiler is MSVC 6.
        """
        prefix = 'MSC v.'
        i = sys.version.find(prefix)
        if i == -1:
            return 6
        i = i + len(prefix)
        s, rest = sys.version[i:].split(' ', 1)
        majorVersion = int(s[:-2]) - 6
        if majorVersion >= 13:
            majorVersion += 1
        minorVersion = int(s[2:3]) / 10.0
        if majorVersion == 6:
            minorVersion = 0
        if majorVersion >= 6:
            return majorVersion + minorVersion
        return None

    def find_msvcrt():
        """Return the name of the VC runtime dll"""
        version = _get_build_version()
        if version is None:
            return None
        if version <= 6:
            clibname = 'msvcrt'
        elif version <= 13:
            clibname = 'msvcr%d' % (version * 10)
        else:
            return None
        import importlib.machinery
        if '_d.pyd' in importlib.machinery.EXTENSION_SUFFIXES:
            clibname += 'd'
        return clibname + '.dll'

    def find_library(name):
        if name in ('c', 'm'):
            return find_msvcrt()
        for directory in os.environ['PATH'].split(os.pathsep):
            fname = os.path.join(directory, name)
            if os.path.isfile(fname):
                return fname
            if fname.lower().endswith('.dll'):
                continue
            fname = fname + '.dll'
            if os.path.isfile(fname):
                return fname
        return None
    import C类型
    from C类型 import wintypes
    _kernel32 = C类型.WinDLL('kernel32', use_last_error=True)
    _get_current_process = _kernel32['GetCurrentProcess']
    _get_current_process.restype = wintypes.HANDLE
    _k32_get_module_file_name = _kernel32['GetModuleFileNameW']
    _k32_get_module_file_name.restype = wintypes.DWORD
    _k32_get_module_file_name.argtypes = (wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD)
    _enum_process_modules = None

    def _get_module_filename(module: wintypes.HMODULE):
        name = (wintypes.WCHAR * 32767)()
        if _k32_get_module_file_name(module, name, len(name)):
            return name.value
        return None

    def _get_module_handles():
        global _enum_process_modules
        if _enum_process_modules is None:
            _psapi = C类型.WinDLL('psapi', use_last_error=True)
            _enum_process_modules = _psapi['EnumProcessModules']
            _enum_process_modules.restype = wintypes.BOOL
            _enum_process_modules.argtypes = (wintypes.HANDLE, C类型.POINTER(wintypes.HMODULE), wintypes.DWORD, wintypes.LPDWORD)
        process = _get_current_process()
        space_needed = wintypes.DWORD()
        n = 1024
        while True:
            modules = (wintypes.HMODULE * n)()
            if not _enum_process_modules(process, modules, C类型.sizeof(modules), C类型.byref(space_needed)):
                err = C类型.get_last_error()
                msg = C类型.FormatError(err).strip()
                raise C类型.WinError(err, f'EnumProcessModules failed: {msg}')
            n = space_needed.value // C类型.sizeof(wintypes.HMODULE)
            if n <= len(modules):
                return modules[:n]

    def dllist():
        """Return a list of loaded shared libraries in the current process."""
        modules = _get_module_handles()
        libraries = [name for h in modules if (name := _get_module_filename(h)) is not None]
        return libraries
elif os.name == 'posix' and sys.platform in {'darwin', 'ios', 'tvos', 'watchos'}:
    from C类型.macholib.dyld import dyld_find as _dyld_find

    def find_library(name):
        possible = ['lib%s.dylib' % name, '%s.dylib' % name, '%s.framework/%s' % (name, name)]
        for name in possible:
            try:
                return _dyld_find(name)
            except ValueError:
                continue
        return None
    import C类型
    _libc = C类型.CDLL(find_library('c'))
    _dyld_get_image_name = _libc['_dyld_get_image_name']
    _dyld_get_image_name.restype = C类型.c_char_p

    def dllist():
        """Return a list of loaded shared libraries in the current process."""
        num_images = _libc._dyld_image_count()
        libraries = [os.fsdecode(name) for i in range(num_images) if (name := _dyld_get_image_name(i)) is not None]
        return libraries
elif sys.platform.startswith('aix'):
    from C类型._aix import find_library
elif sys.platform == 'android':

    def find_library(name):
        directory = '/system/lib'
        if '64' in os.uname().machine:
            directory += '64'
        fname = f'{directory}/lib{name}.so'
        return fname if os.path.isfile(fname) else None
elif sys.platform == 'emscripten':

    def _is_wasm(filename):
        wasm_header = b'\x00asm'
        with open(filename, 'br') as thefile:
            return thefile.read(4) == wasm_header

    def find_library(name):
        candidates = [f'lib{name}.so', f'lib{name}.wasm']
        paths = os.environ.get('LD_LIBRARY_PATH', '')
        for libdir in paths.split(':'):
            for name in candidates:
                libfile = os.path.join(libdir, name)
                if os.path.isfile(libfile) and _is_wasm(libfile):
                    return libfile
        return None
elif os.name == 'posix':
    import re, tempfile

    def _is_elf(filename):
        """Return True if the given file is an ELF file"""
        elf_header = b'\x7fELF'
        try:
            with open(filename, 'br') as thefile:
                return thefile.read(4) == elf_header
        except FileNotFoundError:
            return False

    def _findLib_gcc(name):
        expr = os.fsencode('[^\\(\\)\\s]*lib%s\\.[^\\(\\)\\s]*' % re.escape(name))
        c_compiler = shutil.which('gcc')
        if not c_compiler:
            c_compiler = shutil.which('cc')
        if not c_compiler:
            return None
        temp = tempfile.NamedTemporaryFile()
        try:
            args = [c_compiler, '-Wl,-t', '-o', temp.name, '-l' + name]
            env = dict(os.environ)
            env['LC_ALL'] = 'C'
            env['LANG'] = 'C'
            try:
                proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
            except OSError:
                return None
            with proc:
                trace = proc.stdout.read()
        finally:
            try:
                temp.close()
            except FileNotFoundError:
                pass
        res = re.findall(expr, trace)
        if not res:
            return None
        for file in res:
            if not _is_elf(file):
                continue
            return os.fsdecode(file)
    if sys.platform == 'sunos5':

        def _get_soname(f):
            if not f:
                return None
            try:
                proc = subprocess.Popen(('/usr/ccs/bin/dump', '-Lpv', f), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            except OSError:
                return None
            with proc:
                data = proc.stdout.read()
            res = re.search(b'\\[.*\\]\\sSONAME\\s+([^\\s]+)', data)
            if not res:
                return None
            return os.fsdecode(res.group(1))
    else:

        def _get_soname(f):
            if not f:
                return None
            objdump = shutil.which('objdump')
            if not objdump:
                return None
            try:
                proc = subprocess.Popen((objdump, '-p', '-j', '.dynamic', f), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            except OSError:
                return None
            with proc:
                dump = proc.stdout.read()
            res = re.search(b'\\sSONAME\\s+([^\\s]+)', dump)
            if not res:
                return None
            return os.fsdecode(res.group(1))
    if sys.platform.startswith(('freebsd', 'openbsd', 'dragonfly')):

        def _num_version(libname):
            parts = libname.split(b'.')
            nums = []
            try:
                while parts:
                    nums.insert(0, int(parts.pop()))
            except ValueError:
                pass
            return nums or [sys.maxsize]

        def find_library(name):
            ename = re.escape(name)
            expr = ':-l%s\\.\\S+ => \\S*/(lib%s\\.\\S+)' % (ename, ename)
            expr = os.fsencode(expr)
            try:
                proc = subprocess.Popen(('/sbin/ldconfig', '-r'), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            except OSError:
                data = b''
            else:
                with proc:
                    data = proc.stdout.read()
            res = re.findall(expr, data)
            if not res:
                return _get_soname(_findLib_gcc(name))
            res.sort(key=_num_version)
            return os.fsdecode(res[-1])
    elif sys.platform == 'sunos5':

        def _findLib_crle(name, is64):
            if not os.path.exists('/usr/bin/crle'):
                return None
            env = dict(os.environ)
            env['LC_ALL'] = 'C'
            if is64:
                args = ('/usr/bin/crle', '-64')
            else:
                args = ('/usr/bin/crle',)
            paths = None
            try:
                proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env)
            except OSError:
                return None
            with proc:
                for line in proc.stdout:
                    line = line.strip()
                    if line.startswith(b'Default Library Path (ELF):'):
                        paths = os.fsdecode(line).split()[4]
            if not paths:
                return None
            for dir in paths.split(':'):
                libfile = os.path.join(dir, 'lib%s.so' % name)
                if os.path.exists(libfile):
                    return libfile
            return None

        def find_library(name, is64=False):
            return _get_soname(_findLib_crle(name, is64) or _findLib_gcc(name))
    else:

        def _findSoname_ldconfig(name):
            import struct
            if struct.calcsize('l') == 4:
                machine = os.uname().machine + '-32'
            else:
                machine = os.uname().machine + '-64'
            mach_map = {'x86_64-64': 'libc6,x86-64', 'ppc64-64': 'libc6,64bit', 'sparc64-64': 'libc6,64bit', 's390x-64': 'libc6,64bit', 'ia64-64': 'libc6,IA-64'}
            abi_type = mach_map.get(machine, 'libc6')
            regex = '\\s+(lib%s\\.[^\\s]+)\\s+\\(%s'
            regex = os.fsencode(regex % (re.escape(name), abi_type))
            try:
                with subprocess.Popen(['/sbin/ldconfig', '-p'], stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE, env={'LC_ALL': 'C', 'LANG': 'C'}) as p:
                    res = re.search(regex, p.stdout.read())
                    if res:
                        return os.fsdecode(res.group(1))
            except OSError:
                pass

        def _findLib_ld(name):
            expr = '[^\\(\\)\\s]*lib%s\\.[^\\(\\)\\s]*' % re.escape(name)
            cmd = ['ld', '-t']
            libpath = os.environ.get('LD_LIBRARY_PATH')
            if libpath:
                for d in libpath.split(':'):
                    cmd.extend(['-L', d])
            cmd.extend(['-o', os.devnull, '-l%s' % name])
            result = None
            try:
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, _ = p.communicate()
                res = re.findall(expr, os.fsdecode(out))
                for file in res:
                    if not _is_elf(file):
                        continue
                    return os.fsdecode(file)
            except Exception:
                pass
            return result

        def find_library(name):
            return _findSoname_ldconfig(name) or _get_soname(_findLib_gcc(name)) or _get_soname(_findLib_ld(name))
try:
    from _ctypes import dllist
except ImportError:
    pass

def test():
    from C类型 import cdll
    if os.name == 'nt':
        print(cdll.msvcrt)
        print(cdll.load('msvcrt'))
        print(find_library('msvcrt'))
    if os.name == 'posix':
        print(find_library('m'))
        print(find_library('c'))
        print(find_library('bz2'))
        if sys.platform == 'darwin':
            print(cdll.LoadLibrary('libm.dylib'))
            print(cdll.LoadLibrary('libcrypto.dylib'))
            print(cdll.LoadLibrary('libSystem.dylib'))
            print(cdll.LoadLibrary('System.framework/System'))
        elif sys.platform.startswith('aix'):
            from C类型 import CDLL
            if sys.maxsize < 2 ** 32:
                print(f"Using CDLL(name, os.RTLD_MEMBER): {CDLL('libc.a(shr.o)', os.RTLD_MEMBER)}")
                print(f"Using cdll.LoadLibrary(): {cdll.LoadLibrary('libc.a(shr.o)')}")
                print(find_library('rpm'))
                print(cdll.LoadLibrary('librpm.so'))
            else:
                print(f"Using CDLL(name, os.RTLD_MEMBER): {CDLL('libc.a(shr_64.o)', os.RTLD_MEMBER)}")
                print(f"Using cdll.LoadLibrary(): {cdll.LoadLibrary('libc.a(shr_64.o)')}")
            print(f"crypt\t:: {find_library('crypt')}")
            print(f"crypt\t:: {cdll.LoadLibrary(find_library('crypt'))}")
            print(f"crypto\t:: {find_library('crypto')}")
            print(f"crypto\t:: {cdll.LoadLibrary(find_library('crypto'))}")
        else:
            print(cdll.LoadLibrary('libm.so'))
            print(cdll.LoadLibrary('libcrypt.so'))
            print(find_library('crypt'))
    try:
        dllist
    except NameError:
        print('dllist() not available')
    else:
        print(dllist())
if __name__ == '__main__':
    test()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# ---- 转发层结束 ----
