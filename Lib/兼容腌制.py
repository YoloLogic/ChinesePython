# -*- coding: utf-8 -*-
"""兼容腌制 —— 汉语库（由 tools/汉化库.py 从 Lib/_compat_pickle.py 机械生成，**不要手改**）。

英文库 Lib/_compat_pickle.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 兼容腌制
"""


_英文原名表 = {'IMPORT_MAPPING': '导入映射', 'MULTIPROCESSING_EXCEPTIONS': '多进程异常', 'NAME_MAPPING': '名字映射', 'PYTHON2_EXCEPTIONS': 'Python2异常', 'PYTHON3_IMPORTERROR_EXCEPTIONS': 'Python3导入错误异常', 'PYTHON3_OSERROR_EXCEPTIONS': 'Python3操作系统错误异常', 'REVERSE_IMPORT_MAPPING': '反向导入映射', 'REVERSE_NAME_MAPPING': '反向名字映射'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
导入映射 = {'__builtin__': 'builtins', 'copy_reg': 'copyreg', 'Queue': 'queue', 'SocketServer': 'socketserver', 'ConfigParser': 'configparser', 'repr': 'reprlib', 'tkFileDialog': 'tkinter.filedialog', 'tkSimpleDialog': 'tkinter.simpledialog', 'tkColorChooser': 'tkinter.colorchooser', 'tkCommonDialog': 'tkinter.commondialog', 'Dialog': 'tkinter.dialog', 'Tkdnd': 'tkinter.dnd', 'tkFont': 'tkinter.font', 'tkMessageBox': 'tkinter.messagebox', 'ScrolledText': 'tkinter.scrolledtext', 'Tkconstants': 'tkinter.constants', 'ttk': 'tkinter.ttk', 'Tkinter': 'tkinter', 'markupbase': '_markupbase', '_winreg': 'winreg', 'thread': '_thread', 'dummy_thread': '_dummy_thread', 'dbhash': 'dbm.bsd', 'dumbdbm': 'dbm.dumb', 'dbm': 'dbm.ndbm', 'gdbm': 'dbm.gnu', 'xmlrpclib': 'xmlrpc.client', 'SimpleXMLRPCServer': 'xmlrpc.server', 'httplib': 'http.client', 'htmlentitydefs': 'html.entities', 'HTMLParser': 'html.parser', 'Cookie': 'http.cookies', 'cookielib': 'http.cookiejar', 'BaseHTTPServer': 'http.server', 'test.test_support': 'test.support', 'commands': 'subprocess', 'urlparse': 'urllib.parse', 'robotparser': 'urllib.robotparser', 'urllib2': 'urllib.request', 'anydbm': 'dbm', '_abcoll': 'collections.abc'}
名字映射 = {('__builtin__', 'xrange'): ('builtins', 'range'), ('__builtin__', 'reduce'): ('functools', 'reduce'), ('__builtin__', 'intern'): ('sys', 'intern'), ('__builtin__', 'unichr'): ('builtins', 'chr'), ('__builtin__', 'unicode'): ('builtins', 'str'), ('__builtin__', 'long'): ('builtins', 'int'), ('itertools', 'izip'): ('builtins', 'zip'), ('itertools', 'imap'): ('builtins', 'map'), ('itertools', 'ifilter'): ('builtins', 'filter'), ('itertools', 'ifilterfalse'): ('itertools', 'filterfalse'), ('itertools', 'izip_longest'): ('itertools', 'zip_longest'), ('UserDict', 'IterableUserDict'): ('collections', 'UserDict'), ('UserList', 'UserList'): ('collections', 'UserList'), ('UserString', 'UserString'): ('collections', 'UserString'), ('whichdb', 'whichdb'): ('dbm', 'whichdb'), ('_socket', 'fromfd'): ('socket', 'fromfd'), ('_multiprocessing', 'Connection'): ('multiprocessing.connection', 'Connection'), ('multiprocessing.process', 'Process'): ('multiprocessing.context', 'Process'), ('multiprocessing.forking', 'Popen'): ('multiprocessing.popen_fork', 'Popen'), ('urllib', 'ContentTooShortError'): ('urllib.error', 'ContentTooShortError'), ('urllib', 'getproxies'): ('urllib.request', 'getproxies'), ('urllib', 'pathname2url'): ('urllib.request', 'pathname2url'), ('urllib', 'quote_plus'): ('urllib.parse', 'quote_plus'), ('urllib', 'quote'): ('urllib.parse', 'quote'), ('urllib', 'unquote_plus'): ('urllib.parse', 'unquote_plus'), ('urllib', 'unquote'): ('urllib.parse', 'unquote'), ('urllib', 'url2pathname'): ('urllib.request', 'url2pathname'), ('urllib', 'urlcleanup'): ('urllib.request', 'urlcleanup'), ('urllib', 'urlencode'): ('urllib.parse', 'urlencode'), ('urllib', 'urlopen'): ('urllib.request', 'urlopen'), ('urllib', 'urlretrieve'): ('urllib.request', 'urlretrieve'), ('urllib2', 'HTTPError'): ('urllib.error', 'HTTPError'), ('urllib2', 'URLError'): ('urllib.error', 'URLError')}
Python2异常 = ('ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BufferError', 'BytesWarning', 'DeprecationWarning', 'EOFError', 'EnvironmentError', 'Exception', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError', 'RuntimeWarning', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError')
try:
    WindowsError
except NameError:
    pass
else:
    Python2异常 += ('WindowsError',)
for excname in Python2异常:
    名字映射['exceptions', excname] = ('builtins', excname)
多进程异常 = ('AuthenticationError', 'BufferTooShort', 'ProcessError', 'TimeoutError')
for excname in 多进程异常:
    名字映射['multiprocessing', excname] = ('multiprocessing.context', excname)
反向导入映射 = dict(((v, k) for k, v in 导入映射.items()))
assert len(反向导入映射) == len(导入映射)
反向名字映射 = dict(((v, k) for k, v in 名字映射.items()))
assert len(反向名字映射) == len(名字映射)
导入映射.update({'cPickle': 'pickle', '_elementtree': 'xml.etree.ElementTree', 'FileDialog': 'tkinter.filedialog', 'SimpleDialog': 'tkinter.simpledialog', 'DocXMLRPCServer': 'xmlrpc.server', 'SimpleHTTPServer': 'http.server', 'CGIHTTPServer': 'http.server', 'UserDict': 'collections', 'UserList': 'collections', 'UserString': 'collections', 'whichdb': 'dbm', 'StringIO': 'io', 'cStringIO': 'io'})
反向导入映射.update({'_bz2': 'bz2', '_dbm': 'dbm', '_functools': 'functools', '_gdbm': 'gdbm', '_pickle': 'pickle'})
名字映射.update({('__builtin__', 'basestring'): ('builtins', 'str'), ('exceptions', 'StandardError'): ('builtins', 'Exception'), ('UserDict', 'UserDict'): ('collections', 'UserDict'), ('socket', '_socketobject'): ('socket', 'SocketType')})
反向名字映射.update({('_functools', 'reduce'): ('__builtin__', 'reduce'), ('tkinter.filedialog', 'FileDialog'): ('FileDialog', 'FileDialog'), ('tkinter.filedialog', 'LoadFileDialog'): ('FileDialog', 'LoadFileDialog'), ('tkinter.filedialog', 'SaveFileDialog'): ('FileDialog', 'SaveFileDialog'), ('tkinter.simpledialog', 'SimpleDialog'): ('SimpleDialog', 'SimpleDialog'), ('xmlrpc.server', 'ServerHTMLDoc'): ('DocXMLRPCServer', 'ServerHTMLDoc'), ('xmlrpc.server', 'XMLRPCDocGenerator'): ('DocXMLRPCServer', 'XMLRPCDocGenerator'), ('xmlrpc.server', 'DocXMLRPCRequestHandler'): ('DocXMLRPCServer', 'DocXMLRPCRequestHandler'), ('xmlrpc.server', 'DocXMLRPCServer'): ('DocXMLRPCServer', 'DocXMLRPCServer'), ('xmlrpc.server', 'DocCGIXMLRPCRequestHandler'): ('DocXMLRPCServer', 'DocCGIXMLRPCRequestHandler'), ('http.server', 'SimpleHTTPRequestHandler'): ('SimpleHTTPServer', 'SimpleHTTPRequestHandler'), ('http.server', 'CGIHTTPRequestHandler'): ('CGIHTTPServer', 'CGIHTTPRequestHandler'), ('_socket', 'socket'): ('socket', '_socketobject')})
Python3操作系统错误异常 = ('BrokenPipeError', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'FileExistsError', 'FileNotFoundError', 'InterruptedError', 'IsADirectoryError', 'NotADirectoryError', 'PermissionError', 'ProcessLookupError', 'TimeoutError')
for excname in Python3操作系统错误异常:
    反向名字映射['builtins', excname] = ('exceptions', 'OSError')
Python3导入错误异常 = ('ModuleNotFoundError',)
for excname in Python3导入错误异常:
    反向名字映射['builtins', excname] = ('exceptions', 'ImportError')
del excname


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'IMPORT_MAPPING': '导入映射',
    'MULTIPROCESSING_EXCEPTIONS': '多进程异常',
    'NAME_MAPPING': '名字映射',
    'PYTHON2_EXCEPTIONS': 'Python2异常',
    'PYTHON3_IMPORTERROR_EXCEPTIONS': 'Python3导入错误异常',
    'PYTHON3_OSERROR_EXCEPTIONS': 'Python3操作系统错误异常',
    'REVERSE_IMPORT_MAPPING': '反向导入映射',
    'REVERSE_NAME_MAPPING': '反向名字映射',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
