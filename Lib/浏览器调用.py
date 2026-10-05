# -*- coding: utf-8 -*-
"""浏览器调用 —— 汉语库（由 tools/汉化库.py 从 Lib/webbrowser.py 机械生成，**不要手改**）。

英文库 Lib/webbrowser.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 浏览器调用
"""


"""Interfaces for launching and remotely controlling web browsers."""
_英文原名表 = {'BackgroundBrowser': '后台浏览器', 'BaseBrowser': '浏览器基类', 'Chrome': 'Chrome浏览器', 'Edge': 'Edge浏览器', 'Elinks': 'Elinks浏览器', 'Epiphany': 'Epiphany浏览器', 'Error': '错误', 'GenericBrowser': '通用浏览器', 'IOSBrowser': 'iOS浏览器', 'Konqueror': 'Konqueror浏览器', 'MacOSXOSAScript': 'macOS脚本浏览器', 'Mozilla': 'Mozilla浏览器', 'Opera': 'Opera浏览器', 'UnixBrowser': 'Unix浏览器', 'WindowsDefault': 'Windows默认浏览器', 'get': '取浏览器', 'main': '主函数', 'open_new': '新窗口打开', 'open_new_tab': '新标签页打开', 'parse_args': '解析参数', 'register': '登记浏览器', 'register_X_browsers': '登记X下的浏览器', 'register_standard_browsers': '登记标准浏览器'}

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
import os
import shlex
import shutil
import sys
import subprocess
import threading
__all__ = ['Error', 'open', 'open_new', 'open_new_tab', 'get', 'register']

class 错误(Exception):
    pass
_lock = threading.RLock()
_browsers = {}
_tryorder = None
_os_preferred_browser = None

def 登记浏览器(name, klass, instance=None, *, preferred=False):
    """Register a browser connector."""
    with _lock:
        if _tryorder is None:
            登记标准浏览器()
        _browsers[name.lower()] = [klass, instance]
        if preferred or (_os_preferred_browser and f'{name}.desktop' == _os_preferred_browser):
            _tryorder.insert(0, name)
        else:
            _tryorder.append(name)

def 取浏览器(using=None):
    """Return a browser launcher instance appropriate for the environment."""
    if _tryorder is None:
        with _lock:
            if _tryorder is None:
                登记标准浏览器()
    if using is not None:
        alternatives = [using]
    else:
        alternatives = _tryorder
    for browser in alternatives:
        if '%s' in browser:
            browser = shlex.split(browser)
            if browser[-1] == '&':
                return 后台浏览器(browser[:-1])
            else:
                return 通用浏览器(browser)
        else:
            try:
                command = _browsers[browser.lower()]
            except KeyError:
                command = _synthesize(browser)
            if command[1] is not None:
                return command[1]
            elif command[0] is not None:
                return command[0]()
    raise 错误('could not locate runnable browser')

def open(url, new=0, autoraise=True):
    """Display url using the default browser.

    If possible, open url in a location determined by new.
    - 0: the same browser window (the default).
    - 1: a new browser window.
    - 2: a new browser page ("tab").
    If possible, autoraise raises the window (the default) or not.

    If opening the browser succeeds, return True.
    If there is a problem, return False.
    """
    if _tryorder is None:
        with _lock:
            if _tryorder is None:
                登记标准浏览器()
    for name in _tryorder:
        browser = 取浏览器(name)
        if browser.open(url, new, autoraise):
            return True
    return False

def 新窗口打开(url):
    """Open url in a new window of the default browser.

    If not possible, then open url in the only browser window.
    """
    return open(url, 1)

def 新标签页打开(url):
    """Open url in a new page ("tab") of the default browser.

    If not possible, then the behavior becomes equivalent to open_new().
    """
    return open(url, 2)

def _synthesize(browser, *, preferred=False):
    """Attempt to synthesize a controller based on existing controllers.

    This is useful to create a controller when a user specifies a path to
    an entry in the BROWSER environment variable -- we can copy a general
    controller to operate using a specific installation of the desired
    browser in this way.

    If we can't create a controller in this way, or if there is no
    executable for the requested browser, return [None, None].

    """
    cmd = browser.split()[0]
    if not shutil.which(cmd):
        return [None, None]
    name = os.path.basename(cmd)
    try:
        command = _browsers[name.lower()]
    except KeyError:
        return [None, None]
    controller = command[1]
    if controller and name.lower() == controller.basename:
        import copy
        controller = copy.copy(controller)
        controller.name = browser
        controller.basename = os.path.basename(browser)
        登记浏览器(browser, None, instance=controller, preferred=preferred)
        return [None, controller]
    return [None, None]

class 浏览器基类:
    """Parent class for all browsers. Do not use directly."""
    args = ['%s']

    def __init__(self, name=''):
        self.name = name
        self.basename = name

    def open(self, url, new=0, autoraise=True):
        raise NotImplementedError

    def 新窗口打开(self, url):
        return self.open(url, 1)

    def 新标签页打开(self, url):
        return self.open(url, 2)

    @staticmethod
    def _check_url(url):
        """Ensures that the URL is safe to pass to subprocesses as a parameter"""
        if url and url.lstrip().startswith('-'):
            raise ValueError(f'Invalid URL (leading dash disallowed): {url!r}')
_装类转发(浏览器基类, {'open_new': '新窗口打开', 'open_new_tab': '新标签页打开'}, {'open_new': '新窗口打开', 'open_new_tab': '新标签页打开'})

class 通用浏览器(浏览器基类):
    """Class for all browsers started with a command
       and without remote functionality."""

    def __init__(self, name):
        if isinstance(name, str):
            self.name = name
            self.args = ['%s']
        else:
            self.name = name[0]
            self.args = name[1:]
        self.basename = os.path.basename(self.name)

    def open(self, url, new=0, autoraise=True):
        sys.audit('webbrowser.open', url)
        self._check_url(url)
        cmdline = [self.name] + [arg.replace('%s', url) for arg in self.args]
        try:
            if sys.platform[:3] == 'win':
                p = subprocess.Popen(cmdline)
            else:
                p = subprocess.Popen(cmdline, close_fds=True)
            return not p.wait()
        except OSError:
            return False

class 后台浏览器(通用浏览器):
    """Class for all browsers which are to be started in the
       background."""

    def open(self, url, new=0, autoraise=True):
        cmdline = [self.name] + [arg.replace('%s', url) for arg in self.args]
        sys.audit('webbrowser.open', url)
        self._check_url(url)
        try:
            if sys.platform[:3] == 'win':
                p = subprocess.Popen(cmdline)
            else:
                p = subprocess.Popen(cmdline, close_fds=True, start_new_session=True)
            return p.poll() is None
        except OSError:
            return False

class Unix浏览器(浏览器基类):
    """Parent class for all Unix browsers with remote functionality."""
    raise_opts = None
    background = False
    redirect_stdout = True
    remote_args = ['%action', '%s']
    remote_action = None
    remote_action_newwin = None
    remote_action_newtab = None

    def _invoke(self, args, remote, autoraise, url=None):
        raise_opt = []
        if remote and self.raise_opts:
            autoraise = int(autoraise)
            opt = self.raise_opts[autoraise]
            if opt:
                raise_opt = [opt]
        cmdline = [self.name] + raise_opt + args
        if remote or self.background:
            inout = subprocess.DEVNULL
        else:
            inout = None
        p = subprocess.Popen(cmdline, close_fds=True, stdin=inout, stdout=self.redirect_stdout and inout or None, stderr=inout, start_new_session=True)
        if remote:
            try:
                rc = p.wait(5)
                return not rc
            except subprocess.TimeoutExpired:
                return True
        elif self.background:
            if p.poll() is None:
                return True
            else:
                return False
        else:
            return not p.wait()

    def open(self, url, new=0, autoraise=True):
        sys.audit('webbrowser.open', url)
        if new == 0:
            action = self.remote_action
        elif new == 1:
            action = self.remote_action_newwin
        elif new == 2:
            if self.remote_action_newtab is None:
                action = self.remote_action_newwin
            else:
                action = self.remote_action_newtab
        else:
            raise 错误(f"Bad 'new' parameter to open(); expected 0, 1, or 2, got {new}")
        self._check_url(url.replace('%action', action))
        args = [arg.replace('%action', action).replace('%s', url) for arg in self.remote_args]
        args = [arg for arg in args if arg]
        success = self._invoke(args, True, autoraise, url)
        if not success:
            args = [arg.replace('%s', url) for arg in self.args]
            return self._invoke(args, False, False)
        else:
            return True

class Mozilla浏览器(Unix浏览器):
    """Launcher class for Mozilla browsers."""
    remote_args = ['%action', '%s']
    remote_action = ''
    remote_action_newwin = '-new-window'
    remote_action_newtab = '-new-tab'
    background = True

class Epiphany浏览器(Unix浏览器):
    """Launcher class for Epiphany browser."""
    raise_opts = ['-noraise', '']
    remote_args = ['%action', '%s']
    remote_action = '-n'
    remote_action_newwin = '-w'
    background = True

class Chrome浏览器(Unix浏览器):
    """Launcher class for Google Chrome browser."""
    remote_args = ['%action', '%s']
    remote_action = ''
    remote_action_newwin = '--new-window'
    remote_action_newtab = ''
    background = True
Chromium = Chrome浏览器

class Opera浏览器(Unix浏览器):
    """Launcher class for Opera browser."""
    remote_args = ['%action', '%s']
    remote_action = ''
    remote_action_newwin = '--new-window'
    remote_action_newtab = ''
    background = True

class Elinks浏览器(Unix浏览器):
    """Launcher class for Elinks browsers."""
    remote_args = ['-remote', 'openURL(%s%action)']
    remote_action = ''
    remote_action_newwin = ',new-window'
    remote_action_newtab = ',new-tab'
    background = False
    redirect_stdout = False

class Konqueror浏览器(浏览器基类):
    """Controller for the KDE File Manager (kfm, or Konqueror).

    See the output of ``kfmclient --commands``
    for more information on the Konqueror remote-control interface.
    """

    def open(self, url, new=0, autoraise=True):
        sys.audit('webbrowser.open', url)
        self._check_url(url)
        if new == 2:
            action = 'newTab'
        else:
            action = 'openURL'
        devnull = subprocess.DEVNULL
        try:
            p = subprocess.Popen(['kfmclient', action, url], close_fds=True, stdin=devnull, stdout=devnull, stderr=devnull)
        except OSError:
            pass
        else:
            p.wait()
            return True
        try:
            p = subprocess.Popen(['konqueror', '--silent', url], close_fds=True, stdin=devnull, stdout=devnull, stderr=devnull, start_new_session=True)
        except OSError:
            pass
        else:
            if p.poll() is None:
                return True
        try:
            p = subprocess.Popen(['kfm', '-d', url], close_fds=True, stdin=devnull, stdout=devnull, stderr=devnull, start_new_session=True)
        except OSError:
            return False
        else:
            return p.poll() is None

class Edge浏览器(Unix浏览器):
    """Launcher class for Microsoft Edge browser."""
    remote_args = ['%action', '%s']
    remote_action = ''
    remote_action_newwin = '--new-window'
    remote_action_newtab = ''
    background = True

def 登记X下的浏览器():
    if shutil.which('xdg-open'):
        登记浏览器('xdg-open', None, 后台浏览器('xdg-open'))
    if shutil.which('gio'):
        登记浏览器('gio', None, 后台浏览器(['gio', 'open', '--', '%s']))
    xdg_desktop = os.getenv('XDG_CURRENT_DESKTOP', '').split(':')
    if ('GNOME' in xdg_desktop or 'GNOME_DESKTOP_SESSION_ID' in os.environ) and shutil.which('gvfs-open'):
        登记浏览器('gvfs-open', None, 后台浏览器('gvfs-open'))
    if ('KDE' in xdg_desktop or 'KDE_FULL_SESSION' in os.environ) and shutil.which('kfmclient'):
        登记浏览器('kfmclient', Konqueror浏览器, Konqueror浏览器('kfmclient'))
    if shutil.which('x-www-browser'):
        登记浏览器('x-www-browser', None, 后台浏览器('x-www-browser'))
    for browser in ('firefox', 'iceweasel', 'seamonkey', 'mozilla-firefox', 'mozilla'):
        if shutil.which(browser):
            登记浏览器(browser, None, Mozilla浏览器(browser))
    if shutil.which('kfm'):
        登记浏览器('kfm', Konqueror浏览器, Konqueror浏览器('kfm'))
    elif shutil.which('konqueror'):
        登记浏览器('konqueror', Konqueror浏览器, Konqueror浏览器('konqueror'))
    if shutil.which('epiphany'):
        登记浏览器('epiphany', None, Epiphany浏览器('epiphany'))
    for browser in ('google-chrome', 'chrome', 'chromium', 'chromium-browser'):
        if shutil.which(browser):
            登记浏览器(browser, None, Chrome浏览器(browser))
    if shutil.which('opera'):
        登记浏览器('opera', None, Opera浏览器('opera'))
    if shutil.which('microsoft-edge'):
        登记浏览器('microsoft-edge', None, Edge浏览器('microsoft-edge'))

def 登记标准浏览器():
    global _tryorder
    _tryorder = []
    if sys.platform == 'darwin':
        登记浏览器('MacOSX', None, macOS脚本浏览器('default'))
        登记浏览器('chrome', None, macOS脚本浏览器('google chrome'))
        登记浏览器('firefox', None, macOS脚本浏览器('firefox'))
        登记浏览器('safari', None, macOS脚本浏览器('safari'))
    if sys.platform == 'ios':
        登记浏览器('iosbrowser', None, iOS浏览器(), preferred=True)
    if sys.platform == 'serenityos':
        登记浏览器('Browser', None, 后台浏览器('Browser'))
    if sys.platform[:3] == 'win':
        登记浏览器('windows-default', Windows默认浏览器)
        edge64 = os.path.join(os.environ.get('PROGRAMFILES(x86)', 'C:\\Program Files (x86)'), 'Microsoft\\Edge\\Application\\msedge.exe')
        edge32 = os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Microsoft\\Edge\\Application\\msedge.exe')
        for browser in ('firefox', 'seamonkey', 'mozilla', 'chrome', 'opera', edge64, edge32):
            if shutil.which(browser):
                登记浏览器(browser, None, 后台浏览器(browser))
        if shutil.which('MicrosoftEdge.exe'):
            登记浏览器('microsoft-edge', None, Edge浏览器('MicrosoftEdge.exe'))
    else:
        if sys.platform != 'darwin' and (os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY')):
            try:
                cmd = 'xdg-settings get default-web-browser'.split()
                raw_result = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
                result = raw_result.decode().strip()
            except (FileNotFoundError, subprocess.CalledProcessError, PermissionError, NotADirectoryError):
                pass
            else:
                global _os_preferred_browser
                _os_preferred_browser = result
            登记X下的浏览器()
        if os.environ.get('TERM'):
            if shutil.which('www-browser'):
                登记浏览器('www-browser', None, 通用浏览器('www-browser'))
            if shutil.which('links'):
                登记浏览器('links', None, 通用浏览器('links'))
            if shutil.which('elinks'):
                登记浏览器('elinks', None, Elinks浏览器('elinks'))
            if shutil.which('lynx'):
                登记浏览器('lynx', None, 通用浏览器('lynx'))
            if shutil.which('w3m'):
                登记浏览器('w3m', None, 通用浏览器('w3m'))
    if 'BROWSER' in os.environ:
        userchoices = os.environ['BROWSER'].split(os.pathsep)
        userchoices.reverse()
        for cmdline in userchoices:
            if all((x not in cmdline for x in ' \t')):
                try:
                    command = _browsers[cmdline.lower()]
                except KeyError:
                    pass
                else:
                    if not isinstance(command[1], 通用浏览器):
                        _tryorder.insert(0, cmdline.lower())
                        continue
            if cmdline != '':
                cmd = _synthesize(cmdline, preferred=True)
                if cmd[1] is None:
                    登记浏览器(cmdline, None, 通用浏览器(cmdline), preferred=True)
if sys.platform[:3] == 'win':

    class Windows默认浏览器(浏览器基类):

        def open(self, url, new=0, autoraise=True):
            sys.audit('webbrowser.open', url)
            self._check_url(url)
            try:
                os.startfile(url)
            except OSError:
                return False
            else:
                return True
if sys.platform == 'darwin':

    class macOS脚本浏览器(浏览器基类):

        def __init__(self, name='default'):
            super().__init__(name)

        def open(self, url, new=0, autoraise=True):
            sys.audit('webbrowser.open', url)
            self._check_url(url)
            url = url.replace('"', '%22')
            if self.name == 'default':
                proto, _sep, _rest = url.partition(':')
                if _sep and proto.lower() in {'http', 'https'}:
                    script = f'open location "{url}"'
                else:
                    script = f'''\n                        use framework "AppKit"\n                        use AppleScript version "2.4"\n                        use scripting additions\n\n                        property NSWorkspace : a reference to current application's NSWorkspace\n                        property NSURL : a reference to current application's NSURL\n\n                        set http_url to NSURL's URLWithString:"https://python.org"\n                        set browser_url to (NSWorkspace's sharedWorkspace)'s ¬\n                            URLForApplicationToOpenURL:http_url\n                        set app_path to browser_url's relativePath as text -- NSURL to absolute path '/Applications/Safari.app'\n\n                        tell application app_path\n                            activate\n                            open location "{url}"\n                        end tell\n                    '''
            else:
                script = f'\n                   tell application "{self.name}"\n                       activate\n                       open location "{url}"\n                   end\n                   '
            osapipe = os.popen('/usr/bin/osascript', 'w')
            if osapipe is None:
                return False
            osapipe.write(script)
            rc = osapipe.close()
            return not rc
if sys.platform == 'ios':
    from _ios_support import objc
    if objc:
        from ctypes import c_void_p, c_char_p, c_ulong

    class iOS浏览器(浏览器基类):

        def open(self, url, new=0, autoraise=True):
            sys.audit('webbrowser.open', url)
            self._check_url(url)
            if objc is None:
                return False
            objc.objc_msgSend.restype = c_void_p
            NSString = objc.objc_getClass(b'NSString')
            constructor = objc.sel_registerName(b'stringWithCString:encoding:')
            objc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_char_p, c_ulong]
            url_string = objc.objc_msgSend(NSString, constructor, url.encode('utf-8'), 4)
            NSURL = objc.objc_getClass(b'NSURL')
            urlWithString_ = objc.sel_registerName(b'URLWithString:')
            objc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_void_p]
            ns_url = objc.objc_msgSend(NSURL, urlWithString_, url_string)
            UIApplication = objc.objc_getClass(b'UIApplication')
            sharedApplication = objc.sel_registerName(b'sharedApplication')
            objc.objc_msgSend.argtypes = [c_void_p, c_void_p]
            shared_app = objc.objc_msgSend(UIApplication, sharedApplication)
            openURL_ = objc.sel_registerName(b'openURL:options:completionHandler:')
            objc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p, c_void_p]
            objc.objc_msgSend.restype = None
            objc.objc_msgSend(shared_app, openURL_, ns_url, None, None)
            return True

def 解析参数(arg_list: list[str] | None):
    import argparse
    parser = argparse.ArgumentParser(description='Open URL in a web browser.', color=True)
    parser.add_argument('url', help='URL to open')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', '--new-window', action='store_const', const=1, default=0, dest='new_win', help='open new window')
    group.add_argument('-t', '--new-tab', action='store_const', const=2, default=0, dest='new_win', help='open new tab')
    args = parser.parse_args(arg_list)
    return args

def 主函数(arg_list: list[str] | None=None):
    args = 解析参数(arg_list)
    open(args.url, args.new_win)
    print('\x07')
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
    'BackgroundBrowser': '后台浏览器',
    'BaseBrowser': '浏览器基类',
    'Chrome': 'Chrome浏览器',
    'Edge': 'Edge浏览器',
    'Elinks': 'Elinks浏览器',
    'Epiphany': 'Epiphany浏览器',
    'Error': '错误',
    'GenericBrowser': '通用浏览器',
    'IOSBrowser': 'iOS浏览器',
    'Konqueror': 'Konqueror浏览器',
    'MacOSXOSAScript': 'macOS脚本浏览器',
    'Mozilla': 'Mozilla浏览器',
    'Opera': 'Opera浏览器',
    'UnixBrowser': 'Unix浏览器',
    'WindowsDefault': 'Windows默认浏览器',
    'get': '取浏览器',
    'main': '主函数',
    'open_new': '新窗口打开',
    'open_new_tab': '新标签页打开',
    'parse_args': '解析参数',
    'register': '登记浏览器',
    'register_X_browsers': '登记X下的浏览器',
    'register_standard_browsers': '登记标准浏览器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '浏览器基类': {
        'open_new': '新窗口打开',
        'open_new_tab': '新标签页打开',
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
    '浏览器基类': {
        'open_new': '新窗口打开',
        'open_new_tab': '新标签页打开',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '取浏览器',
    '新标签页打开',
    '新窗口打开',
    '登记浏览器',
    '错误',
]

# ---- 转发层结束 ----
