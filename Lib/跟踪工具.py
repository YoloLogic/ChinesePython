# -*- coding: utf-8 -*-
"""跟踪工具 —— 汉语库（由 tools/汉化库.py 从 Lib/trace.py 机械生成，**不要手改**）。

英文库 Lib/trace.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 跟踪工具
"""


"""program/module to trace Python program or function execution

Sample use, command line:
  trace.py -c -f counts --ignore-dir '$prefix' spam.py eggs
  trace.py -t --ignore-dir '$prefix' spam.py eggs
  trace.py --trackcalls spam.py eggs

Sample use, programmatically
  import sys

  # create a Trace object, telling it what to ignore, and whether to
  # do tracing or line-counting or both.
  tracer = trace.Trace(ignoredirs=[sys.base_prefix, sys.base_exec_prefix,],
                       trace=0, count=1)
  # run the new command using the given tracer
  tracer.run('main()')
  # make a report, placing output in /tmp
  r = tracer.results()
  r.write_results(show_missing=True, coverdir="/tmp")
"""
_英文原名表 = {'CoverageResults': '覆盖率结果', 'PRAGMA_NOCOVER': '不覆盖标记', 'Trace': '跟踪器', 'main': '主函数'}

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
__all__ = ['Trace', 'CoverageResults']
import io
import linecache
import os
import sys
import sysconfig
import token
import tokenize
import inspect
import gc
import dis
import pickle
from time import monotonic as _time
import threading
不覆盖标记 = '#pragma NO COVER'

class _Ignore:

    def __init__(self, modules=None, dirs=None):
        self._mods = set() if not modules else set(modules)
        self._dirs = [] if not dirs else [os.path.normpath(d) for d in dirs]
        self._ignore = {'<string>': 1}

    def 取名字(self, filename, modulename):
        if modulename in self._ignore:
            return self._ignore[modulename]
        if modulename in self._mods:
            self._ignore[modulename] = 1
            return 1
        for mod in self._mods:
            if modulename.startswith(mod + '.'):
                self._ignore[modulename] = 1
                return 1
        if filename is None:
            self._ignore[modulename] = 1
            return 1
        for d in self._dirs:
            if filename.startswith(d + os.sep):
                self._ignore[modulename] = 1
                return 1
        self._ignore[modulename] = 0
        return 0
_装类转发(_Ignore, {'names': '取名字'}, {'names': '取名字'})

def _modname(path):
    """Return a plausible module name for the path."""
    base = os.path.basename(path)
    filename, ext = os.path.splitext(base)
    return filename

def _fullmodname(path):
    """Return a plausible module name for the path."""
    comparepath = os.path.normcase(path)
    longest = ''
    for dir in sys.path:
        dir = os.path.normcase(dir)
        if comparepath.startswith(dir) and comparepath[len(dir)] == os.sep:
            if len(dir) > len(longest):
                longest = dir
    if longest:
        base = path[len(longest) + 1:]
    else:
        base = path
    drive, base = os.path.splitdrive(base)
    base = base.replace(os.sep, '.')
    if os.altsep:
        base = base.replace(os.altsep, '.')
    filename, ext = os.path.splitext(base)
    return filename.lstrip('.')

class 覆盖率结果:

    def __init__(self, counts=None, calledfuncs=None, infile=None, callers=None, outfile=None):
        self.counts = counts
        if self.counts is None:
            self.counts = {}
        self.counter = self.counts.copy()
        self.calledfuncs = calledfuncs
        if self.calledfuncs is None:
            self.calledfuncs = {}
        self.calledfuncs = self.calledfuncs.copy()
        self.callers = callers
        if self.callers is None:
            self.callers = {}
        self.callers = self.callers.copy()
        self.infile = infile
        self.outfile = outfile
        if self.infile:
            try:
                with open(self.infile, 'rb') as f:
                    counts, calledfuncs, callers = pickle.load(f)
                self.update(self.__class__(counts, calledfuncs, callers=callers))
            except (OSError, EOFError, ValueError) as err:
                print('Skipping counts file %r: %s' % (self.infile, err), file=sys.stderr)

    def 是忽略的文件吗(self, filename):
        """Return True if the filename does not refer to a file
        we want to have reported.
        """
        return filename.startswith('<') and filename.endswith('>')

    def update(self, other):
        """Merge in the data from another CoverageResults"""
        counts = self.counts
        calledfuncs = self.calledfuncs
        callers = self.callers
        other_counts = other.counts
        other_calledfuncs = other.calledfuncs
        other_callers = other.callers
        for key in other_counts:
            counts[key] = counts.get(key, 0) + other_counts[key]
        for key in other_calledfuncs:
            calledfuncs[key] = 1
        for key in other_callers:
            callers[key] = 1

    def 写出结果(self, show_missing=True, summary=False, coverdir=None, *, ignore_missing_files=False):
        """
        Write the coverage results.

        :param show_missing: Show lines that had no hits.
        :param summary: Include coverage summary per module.
        :param coverdir: If None, the results of each module are placed in its
                         directory, otherwise it is included in the directory
                         specified.
        :param ignore_missing_files: If True, counts for files that no longer
                         exist are silently ignored. Otherwise, a missing file
                         will raise a FileNotFoundError.
        """
        if self.calledfuncs:
            print()
            print('functions called:')
            calls = self.calledfuncs
            for filename, modulename, funcname in sorted(calls):
                print('filename: %s, modulename: %s, funcname: %s' % (filename, modulename, funcname))
        if self.callers:
            print()
            print('calling relationships:')
            lastfile = lastcfile = ''
            for (pfile, pmod, pfunc), (cfile, cmod, cfunc) in sorted(self.callers):
                if pfile != lastfile:
                    print()
                    print('***', pfile, '***')
                    lastfile = pfile
                    lastcfile = ''
                if cfile != pfile and lastcfile != cfile:
                    print('  -->', cfile)
                    lastcfile = cfile
                print('    %s.%s -> %s.%s' % (pmod, pfunc, cmod, cfunc))
        per_file = {}
        for filename, lineno in self.counts:
            lines_hit = per_file[filename] = per_file.get(filename, {})
            lines_hit[lineno] = self.counts[filename, lineno]
        sums = {}
        for filename, count in per_file.items():
            if self.是忽略的文件吗(filename):
                continue
            if filename.endswith('.pyc'):
                filename = filename[:-1]
            if ignore_missing_files and (not os.path.isfile(filename)):
                continue
            if coverdir is None:
                dir = os.path.dirname(os.path.abspath(filename))
                modulename = _modname(filename)
            else:
                dir = coverdir
                os.makedirs(dir, exist_ok=True)
                modulename = _fullmodname(filename)
            if show_missing:
                lnotab = _find_executable_linenos(filename)
            else:
                lnotab = {}
            source = linecache.getlines(filename)
            coverpath = os.path.join(dir, modulename + '.cover')
            with open(filename, 'rb') as fp:
                encoding, _ = tokenize.detect_encoding(fp.readline)
            n_hits, n_lines = self.写出结果文件(coverpath, source, lnotab, count, encoding)
            if summary and n_lines:
                sums[modulename] = (n_lines, n_hits, modulename, filename)
        if summary and sums:
            print('lines   cov%   module   (path)')
            for m in sorted(sums):
                n_lines, n_hits, modulename, filename = sums[m]
                print(f'{n_lines:5d}   {n_hits / n_lines:.1%}   {modulename}   ({filename})')
        if self.outfile:
            try:
                with open(self.outfile, 'wb') as f:
                    pickle.dump((self.counts, self.calledfuncs, self.callers), f, 1)
            except OSError as err:
                print("Can't save counts files because %s" % err, file=sys.stderr)

    def 写出结果文件(self, path, lines, lnotab, lines_hit, encoding=None):
        """Return a coverage results file in path."""
        try:
            outfile = open(path, 'w', encoding=encoding)
        except OSError as err:
            print('trace: Could not open %r for writing: %s - skipping' % (path, err), file=sys.stderr)
            return (0, 0)
        n_lines = 0
        n_hits = 0
        with outfile:
            for lineno, line in enumerate(lines, 1):
                if lineno in lines_hit:
                    outfile.write('%5d: ' % lines_hit[lineno])
                    n_hits += 1
                    n_lines += 1
                elif lineno in lnotab and (not 不覆盖标记 in line):
                    outfile.write('>>>>>> ')
                    n_lines += 1
                else:
                    outfile.write('       ')
                outfile.write(line.expandtabs(8))
        return (n_hits, n_lines)
_装类转发(覆盖率结果, {'is_ignored_filename': '是忽略的文件吗', 'write_results': '写出结果', 'write_results_file': '写出结果文件'}, {'is_ignored_filename': '是忽略的文件吗', 'write_results': '写出结果', 'write_results_file': '写出结果文件'})

def _find_lines_from_code(code, strs):
    """Return dict where keys are lines in the line number table."""
    linenos = {}
    for _, lineno in dis.findlinestarts(code):
        if lineno not in strs:
            linenos[lineno] = 1
    return linenos

def _find_lines(code, strs):
    """Return lineno dict for all code objects reachable from code."""
    linenos = _find_lines_from_code(code, strs)
    for c in code.co_consts:
        if inspect.iscode(c):
            linenos.update(_find_lines(c, strs))
    return linenos

def _find_strings(filename, encoding=None):
    """Return a dict of possible docstring positions.

    The dict maps line numbers to strings.  There is an entry for
    line that contains only a string or a part of a triple-quoted
    string.
    """
    d = {}
    prev_ttype = token.INDENT
    with open(filename, encoding=encoding) as f:
        tok = tokenize.generate_tokens(f.readline)
        for ttype, tstr, start, end, line in tok:
            if ttype == token.STRING:
                if prev_ttype == token.INDENT:
                    sline, scol = start
                    eline, ecol = end
                    for i in range(sline, eline + 1):
                        d[i] = 1
            prev_ttype = ttype
    return d

def _find_executable_linenos(filename):
    """Return dict where keys are line numbers in the line number table."""
    try:
        with tokenize.open(filename) as f:
            prog = f.read()
            encoding = f.encoding
    except OSError as err:
        print('Not printing coverage data for %r: %s' % (filename, err), file=sys.stderr)
        return {}
    code = compile(prog, filename, 'exec')
    strs = _find_strings(filename, encoding)
    return _find_lines(code, strs)

class 跟踪器:

    def __init__(self, count=1, trace=1, countfuncs=0, countcallers=0, ignoremods=(), ignoredirs=(), infile=None, outfile=None, timing=False):
        """
        @param count true iff it should count number of times each
                     line is executed
        @param trace true iff it should print out each line that is
                     being counted
        @param countfuncs true iff it should just output a list of
                     (filename, modulename, funcname,) for functions
                     that were called at least once;  This overrides
                     'count' and 'trace'
        @param ignoremods a list of the names of modules to ignore
        @param ignoredirs a list of the names of directories to ignore
                     all of the (recursive) contents of
        @param infile file from which to read stored counts to be
                     added into the results
        @param outfile file in which to write the results
        @param timing true iff timing information be displayed
        """
        self.infile = infile
        self.outfile = outfile
        self.ignore = _Ignore(ignoremods, ignoredirs)
        self.counts = {}
        self.pathtobasename = {}
        self.donothing = 0
        self.trace = trace
        self._calledfuncs = {}
        self._callers = {}
        self._caller_cache = {}
        self.start_time = None
        if timing:
            self.start_time = _time()
        if countcallers:
            self.globaltrace = self.globaltrace_trackcallers
        elif countfuncs:
            self.globaltrace = self.globaltrace_countfuncs
        elif trace and count:
            self.globaltrace = self.globaltrace_lt
            self.localtrace = self.localtrace_trace_and_count
        elif trace:
            self.globaltrace = self.globaltrace_lt
            self.localtrace = self.localtrace_trace
        elif count:
            self.globaltrace = self.globaltrace_lt
            self.localtrace = self.localtrace_count
        else:
            self.donothing = 1

    def 运行(self, cmd):
        import __main__
        dict = __main__.__dict__
        self.带上下文运行(cmd, dict, dict)

    def 带上下文运行(self, cmd, globals=None, locals=None):
        if globals is None:
            globals = {}
        if locals is None:
            locals = {}
        if not self.donothing:
            threading.settrace(self.globaltrace)
            sys.settrace(self.globaltrace)
        try:
            exec(cmd, globals, locals)
        finally:
            if not self.donothing:
                sys.settrace(None)
                threading.settrace(None)

    def 运行函数(self, func, /, *args, **kw):
        result = None
        if not self.donothing:
            sys.settrace(self.globaltrace)
        try:
            result = func(*args, **kw)
        finally:
            if not self.donothing:
                sys.settrace(None)
        return result

    def 取所在文件模块函数(self, frame):
        code = frame.f_code
        filename = code.co_filename
        if filename:
            modulename = _modname(filename)
        else:
            modulename = None
        funcname = code.co_name
        clsname = None
        if code in self._caller_cache:
            if self._caller_cache[code] is not None:
                clsname = self._caller_cache[code]
        else:
            self._caller_cache[code] = None
            funcs = [f for f in gc.get_referrers(code) if inspect.isfunction(f)]
            if len(funcs) == 1:
                dicts = [d for d in gc.get_referrers(funcs[0]) if isinstance(d, dict)]
                if len(dicts) == 1:
                    classes = [c for c in gc.get_referrers(dicts[0]) if hasattr(c, '__bases__')]
                    if len(classes) == 1:
                        clsname = classes[0].__name__
                        self._caller_cache[code] = clsname
        if clsname is not None:
            funcname = '%s.%s' % (clsname, funcname)
        return (filename, modulename, funcname)

    def globaltrace_trackcallers(self, frame, why, arg):
        """Handler for call events.

        Adds information about who called who to the self._callers dict.
        """
        if why == 'call':
            this_func = self.取所在文件模块函数(frame)
            parent_func = self.取所在文件模块函数(frame.f_back)
            self._callers[parent_func, this_func] = 1

    def globaltrace_countfuncs(self, frame, why, arg):
        """Handler for call events.

        Adds (filename, modulename, funcname) to the self._calledfuncs dict.
        """
        if why == 'call':
            this_func = self.取所在文件模块函数(frame)
            self._calledfuncs[this_func] = 1

    def globaltrace_lt(self, frame, why, arg):
        """Handler for call events.

        If the code block being entered is to be ignored, returns 'None',
        else returns self.localtrace.
        """
        if why == 'call':
            code = frame.f_code
            filename = frame.f_globals.get('__file__', None)
            if filename:
                modulename = _modname(filename)
                if modulename is not None:
                    ignore_it = self.ignore.names(filename, modulename)
                    if not ignore_it:
                        if self.trace:
                            print(' --- modulename: %s, funcname: %s' % (modulename, code.co_name))
                        return self.localtrace
            else:
                return None

    def localtrace_trace_and_count(self, frame, why, arg):
        if why == 'line':
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            key = (filename, lineno)
            self.counts[key] = self.counts.get(key, 0) + 1
            if self.start_time:
                print('%.2f' % (_time() - self.start_time), end=' ')
            bname = os.path.basename(filename)
            line = linecache.getline(filename, lineno)
            print('%s(%d)' % (bname, lineno), end='')
            if line:
                print(': ', line, end='')
            else:
                print()
        return self.localtrace

    def localtrace_trace(self, frame, why, arg):
        if why == 'line':
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            if self.start_time:
                print('%.2f' % (_time() - self.start_time), end=' ')
            bname = os.path.basename(filename)
            line = linecache.getline(filename, lineno)
            print('%s(%d)' % (bname, lineno), end='')
            if line:
                print(': ', line, end='')
            else:
                print()
        return self.localtrace

    def localtrace_count(self, frame, why, arg):
        if why == 'line':
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            key = (filename, lineno)
            self.counts[key] = self.counts.get(key, 0) + 1
        return self.localtrace

    def 取结果(self):
        return 覆盖率结果(self.counts, infile=self.infile, outfile=self.outfile, calledfuncs=self._calledfuncs, callers=self._callers)
_装类转发(跟踪器, {'file_module_function_of': '取所在文件模块函数', 'results': '取结果', 'run': '运行', 'runctx': '带上下文运行', 'runfunc': '运行函数'}, {'file_module_function_of': '取所在文件模块函数', 'results': '取结果', 'run': '运行', 'runctx': '带上下文运行', 'runfunc': '运行函数'})

def 主函数():
    import argparse
    parser = argparse.ArgumentParser(color=True)
    parser.add_argument('--version', action='version', version='trace 2.0')
    grp = parser.add_argument_group('Main options', 'One of these (or --report) must be given')
    grp.add_argument('-c', '--count', action='store_true', help="Count the number of times each line is executed and write the counts to <module>.cover for each module executed, in the module's directory. See also --coverdir, --file, --no-report below.")
    grp.add_argument('-t', '--trace', action='store_true', help='Print each line to sys.stdout before it is executed')
    grp.add_argument('-l', '--listfuncs', action='store_true', help='Keep track of which functions are executed at least once and write the results to sys.stdout after the program exits. Cannot be specified alongside --trace or --count.')
    grp.add_argument('-T', '--trackcalls', action='store_true', help='Keep track of caller/called pairs and write the results to sys.stdout after the program exits.')
    grp = parser.add_argument_group('Modifiers')
    _grp = grp.add_mutually_exclusive_group()
    _grp.add_argument('-r', '--report', action='store_true', help='Generate a report from a counts file; does not execute any code. --file must specify the results file to read, which must have been created in a previous run with --count --file=FILE')
    _grp.add_argument('-R', '--no-report', action='store_true', help='Do not generate the coverage report files. Useful if you want to accumulate over several runs.')
    grp.add_argument('-f', '--file', help='File to accumulate counts over several runs')
    grp.add_argument('-C', '--coverdir', help='Directory where the report files go. The coverage report for <package>.<module> will be written to file <dir>/<package>/<module>.cover')
    grp.add_argument('-m', '--missing', action='store_true', help='Annotate executable lines that were not executed with ">>>>>> "')
    grp.add_argument('-s', '--summary', action='store_true', help='Write a brief summary for each file to sys.stdout. Can only be used with --count or --report')
    grp.add_argument('-g', '--timing', action='store_true', help='Prefix each line with the time since the program started. Only used while tracing')
    grp = parser.add_argument_group('Filters', 'Can be specified multiple times')
    grp.add_argument('--ignore-module', action='append', default=[], help='Ignore the given module(s) and its submodules (if it is a package). Accepts comma separated list of module names.')
    grp.add_argument('--ignore-dir', action='append', default=[], help='Ignore files in the given directory (multiple directories can be joined by os.pathsep).')
    parser.add_argument('--module', action='store_true', default=False, help='Trace a module. ')
    parser.add_argument('progname', nargs='?', help='file to run as main program')
    parser.add_argument('arguments', nargs=argparse.REMAINDER, help='arguments to the program')
    opts = parser.parse_args()
    if opts.ignore_dir:
        _prefix = sysconfig.get_path('stdlib')
        _exec_prefix = sysconfig.get_path('platstdlib')

    def parse_ignore_dir(s):
        s = os.path.expanduser(os.path.expandvars(s))
        s = s.replace('$prefix', _prefix).replace('$exec_prefix', _exec_prefix)
        return os.path.normpath(s)
    opts.ignore_module = [mod.strip() for i in opts.ignore_module for mod in i.split(',')]
    opts.ignore_dir = [parse_ignore_dir(s) for i in opts.ignore_dir for s in i.split(os.pathsep)]
    if opts.report:
        if not opts.file:
            parser.error('-r/--report requires -f/--file')
        取结果 = 覆盖率结果(infile=opts.file, outfile=opts.file)
        return 取结果.write_results(opts.missing, opts.summary, opts.coverdir)
    if not any([opts.trace, opts.count, opts.listfuncs, opts.trackcalls]):
        parser.error('must specify one of --trace, --count, --report, --listfuncs, or --trackcalls')
    if opts.listfuncs and (opts.count or opts.trace):
        parser.error('cannot specify both --listfuncs and (--trace or --count)')
    if opts.summary and (not opts.count):
        parser.error('--summary can only be used with --count or --report')
    if opts.progname is None:
        parser.error('progname is missing: required with the main options')
    t = 跟踪器(opts.count, opts.trace, countfuncs=opts.listfuncs, countcallers=opts.trackcalls, ignoremods=opts.ignore_module, ignoredirs=opts.ignore_dir, infile=opts.file, outfile=opts.file, timing=opts.timing)
    try:
        if opts.module:
            import runpy
            module_name = opts.progname
            mod_name, mod_spec, code = runpy._get_module_details(module_name)
            sys.argv = [code.co_filename, *opts.arguments]
            globs = {'__name__': '__main__', '__file__': code.co_filename, '__package__': mod_spec.parent, '__loader__': mod_spec.loader, '__spec__': mod_spec, '__cached__': None}
        else:
            sys.argv = [opts.progname, *opts.arguments]
            sys.path[0] = os.path.dirname(opts.progname)
            with io.open_code(opts.progname) as fp:
                code = compile(fp.read(), opts.progname, 'exec')
            globs = {'__file__': opts.progname, '__name__': '__main__', '__package__': None, '__cached__': None}
        t.runctx(code, globs, globs)
    except OSError as err:
        sys.exit('Cannot run file %r because: %s' % (sys.argv[0], err))
    except SystemExit:
        pass
    取结果 = t.results()
    if not opts.no_report:
        取结果.write_results(opts.missing, opts.summary, opts.coverdir)
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
    'CoverageResults': '覆盖率结果',
    'PRAGMA_NOCOVER': '不覆盖标记',
    'Trace': '跟踪器',
    'main': '主函数',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '_Ignore': {
        'names': '取名字',
    },
    '覆盖率结果': {
        'is_ignored_filename': '是忽略的文件吗',
        'write_results': '写出结果',
        'write_results_file': '写出结果文件',
    },
    '跟踪器': {
        'file_module_function_of': '取所在文件模块函数',
        'results': '取结果',
        'run': '运行',
        'runctx': '带上下文运行',
        'runfunc': '运行函数',
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
    '_Ignore': {
        'names': '取名字',
    },
    '覆盖率结果': {
        'is_ignored_filename': '是忽略的文件吗',
        'write_results': '写出结果',
        'write_results_file': '写出结果文件',
    },
    '跟踪器': {
        'file_module_function_of': '取所在文件模块函数',
        'results': '取结果',
        'run': '运行',
        'runctx': '带上下文运行',
        'runfunc': '运行函数',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '覆盖率结果',
    '跟踪器',
]

# ---- 转发层结束 ----
