# -*- coding: utf-8 -*-
"""POP收信 —— 汉语库（由 tools/汉化库.py 从 Lib/poplib.py 机械生成，**不要手改**）。

英文库 Lib/poplib.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py POP收信
"""


"""A POP3 client class.

Based on the J. Myers POP3 draft, Jan. 96
"""
_英文原名表 = {'CR': '回车', 'CRLF': '回车换行', 'HAVE_SSL': '支持SSL', 'LF': '换行', 'POP3': 'POP3客户端', 'POP3_PORT': 'POP3端口', 'POP3_SSL': 'POP3安全客户端', 'POP3_SSL_PORT': 'POP3安全端口', 'error_proto': '协议错误'}

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
import errno
import re
import socket
import sys
try:
    import ssl
    支持SSL = True
except ImportError:
    支持SSL = False
__all__ = ['POP3', 'error_proto']

class 协议错误(Exception):
    pass
POP3端口 = 110
POP3安全端口 = 995
回车 = b'\r'
换行 = b'\n'
回车换行 = 回车 + 换行
_MAXLINE = 2048

class POP3客户端:
    """This class supports both the minimal and optional command sets.
    Arguments can be strings or integers (where appropriate)
    (e.g.: retr(1) and retr('1') both work equally well.

    Minimal Command Set:
            USER name               user(name)
            PASS string             pass_(string)
            STAT                    stat()
            LIST [msg]              list(msg = None)
            RETR msg                retr(msg)
            DELE msg                dele(msg)
            NOOP                    noop()
            RSET                    rset()
            QUIT                    quit()

    Optional Commands (some servers support these):
            RPOP name               rpop(name)
            APOP name digest        apop(name, digest)
            TOP msg n               top(msg, n)
            UIDL [msg]              uidl(msg = None)
            CAPA                    capa()
            STLS                    stls()
            UTF8                    utf8()

    Raises one exception: 'error_proto'.

    Instantiate with:
            POP3(hostname, port=110)

    NB:     the POP protocol locks the mailbox from user
            authorization until QUIT, so be sure to get in, suck
            the messages, and quit, each time you access the
            mailbox.

            POP is a line-based protocol, which means large mail
            messages consume lots of python cycles reading them
            line-by-line.

            If it's available on your mail server, use IMAP4
            instead, it doesn't suffer from the two problems
            above.
    """
    encoding = 'UTF-8'

    def __init__(self, host, port=POP3端口, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self._tls_established = False
        sys.audit('poplib.connect', self, host, port)
        self.sock = self._create_socket(timeout)
        self.file = self.sock.makefile('rb')
        self._debugging = 0
        self.welcome = self._getresp()

    def _create_socket(self, timeout):
        if timeout is not None and (not timeout):
            raise ValueError('Non-blocking socket (timeout=0) is not supported')
        return socket.create_connection((self.host, self.port), timeout)

    def _putline(self, line):
        if self._debugging > 1:
            print('*put*', repr(line))
        sys.audit('poplib.putline', self, line)
        self.sock.sendall(line + 回车换行)

    def _putcmd(self, line):
        if self._debugging:
            print('*cmd*', repr(line))
        line = bytes(line, self.encoding)
        self._putline(line)

    def _getline(self):
        line = self.file.readline(_MAXLINE + 1)
        if len(line) > _MAXLINE:
            raise 协议错误('line too long')
        if self._debugging > 1:
            print('*get*', repr(line))
        if not line:
            raise 协议错误('-ERR EOF')
        octets = len(line)
        if line[-2:] == 回车换行:
            return (line[:-2], octets)
        if line[:1] == 回车:
            return (line[1:-1], octets)
        return (line[:-1], octets)

    def _getresp(self):
        resp, o = self._getline()
        if self._debugging > 1:
            print('*resp*', repr(resp))
        if not resp.startswith(b'+'):
            raise 协议错误(resp)
        return resp

    def _getlongresp(self):
        resp = self._getresp()
        list = []
        octets = 0
        line, o = self._getline()
        while line != b'.':
            if line.startswith(b'..'):
                o = o - 1
                line = line[1:]
            octets = octets + o
            list.append(line)
            line, o = self._getline()
        return (resp, list, octets)

    def _shortcmd(self, line):
        self._putcmd(line)
        return self._getresp()

    def _longcmd(self, line):
        self._putcmd(line)
        return self._getlongresp()

    def 取欢迎语(self):
        return self.welcome

    def 设调试级别(self, level):
        self._debugging = level

    def 用户(self, user):
        """Send user name, return response

        (should indicate password required).
        """
        return self._shortcmd('USER %s' % user)

    def 口令(self, pswd):
        """Send password, return response

        (response includes message count, mailbox size).

        NB: mailbox is locked by server from here to 'quit()'
        """
        return self._shortcmd('PASS %s' % pswd)

    def 取状态(self):
        """Get mailbox status.

        Result is tuple of 2 ints (message count, mailbox size)
        """
        retval = self._shortcmd('STAT')
        rets = retval.split()
        if self._debugging:
            print('*stat*', repr(rets))
        if len(rets) < 3:
            raise 协议错误('Invalid STAT response format')
        try:
            numMessages = int(rets[1])
            sizeMessages = int(rets[2])
        except ValueError:
            raise 协议错误('Invalid STAT response data: non-numeric values')
        return (numMessages, sizeMessages)

    def list(self, which=None):
        """Request listing, return result.

        Result without a message number argument is in form
        ['response', ['mesg_num octets', ...], octets].

        Result when a message number argument is given is a
        single response: the "scan listing" for that message.
        """
        if which is not None:
            return self._shortcmd('LIST %s' % which)
        return self._longcmd('LIST')

    def 取邮件(self, which):
        """Retrieve whole message number 'which'.

        Result is in form ['response', ['line', ...], octets].
        """
        return self._longcmd('RETR %s' % which)

    def 删除邮件(self, which):
        """Delete message number 'which'.

        Result is 'response'.
        """
        return self._shortcmd('DELE %s' % which)

    def 空操作(self):
        """Does nothing.

        One supposes the response indicates the server is alive.
        """
        return self._shortcmd('NOOP')

    def 重置会话(self):
        """Unmark all messages marked for deletion."""
        return self._shortcmd('RSET')

    def quit(self):
        """Signoff: commit changes on server, unlock mailbox, close connection."""
        resp = self._shortcmd('QUIT')
        self.close()
        return resp

    def close(self):
        """Close the connection without assuming anything about it."""
        try:
            file = self.file
            self.file = None
            if file is not None:
                file.close()
        finally:
            sock = self.sock
            self.sock = None
            if sock is not None:
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                except OSError as exc:
                    if exc.errno != errno.ENOTCONN and getattr(exc, 'winerror', 0) != 10022:
                        raise
                finally:
                    sock.close()

    def 远程弹出(self, user):
        """Send RPOP command to access the mailbox with an alternate user."""
        return self._shortcmd('RPOP %s' % user)
    时间戳 = re.compile(b'\\+OK.[^<]*(<.*>)')

    def APOP认证(self, user, password):
        """Authorisation

        - only possible if server has supplied a timestamp in initial greeting.

        Args:
                user     - mailbox user;
                password - mailbox password.

        NB: mailbox is locked by server from here to 'quit()'
        """
        secret = bytes(password, self.encoding)
        m = self.时间戳.match(self.welcome)
        if not m:
            raise 协议错误('-ERR APOP not supported by server')
        import hashlib
        digest = m.group(1) + secret
        digest = hashlib.md5(digest).hexdigest()
        return self._shortcmd('APOP %s %s' % (user, digest))

    def 取头部(self, which, howmuch):
        """Retrieve message header of message number 'which'
        and first 'howmuch' lines of message body.

        Result is in form ['response', ['line', ...], octets].
        """
        return self._longcmd('TOP %s %s' % (which, howmuch))

    def 取唯一标识(self, which=None):
        """Return message digest (unique id) list.

        If 'which', result contains unique id for that message
        in the form 'response mesgnum uid', otherwise result is
        the list ['response', ['mesgnum uid', ...], octets]
        """
        if which is not None:
            return self._shortcmd('UIDL %s' % which)
        return self._longcmd('UIDL')

    def 切换到UTF8(self):
        """Try to enter UTF-8 mode (see RFC 6856). Returns server response.
        """
        return self._shortcmd('UTF8')

    def 取能力(self):
        """Return server capabilities (RFC 2449) as a dictionary
        >>> c=poplib.POP3('localhost')
        >>> c.capa()
        {'IMPLEMENTATION': ['Cyrus', 'POP3', 'server', 'v2.2.12'],
         'TOP': [], 'LOGIN-DELAY': ['0'], 'AUTH-RESP-CODE': [],
         'EXPIRE': ['NEVER'], 'USER': [], 'STLS': [], 'PIPELINING': [],
         'UIDL': [], 'RESP-CODES': []}
        >>>

        Really, according to RFC 2449, the cyrus folks should avoid
        having the implementation split into multiple arguments...
        """

        def _parsecap(line):
            lst = line.decode('ascii').split()
            return (lst[0], lst[1:])
        caps = {}
        try:
            resp = self._longcmd('CAPA')
            rawcaps = resp[1]
            for capline in rawcaps:
                capnm, capargs = _parsecap(capline)
                caps[capnm] = capargs
        except 协议错误:
            raise 协议错误('-ERR CAPA not supported by server')
        return caps

    def 启动TLS(self, context=None):
        """Start a TLS session on the active connection as specified in RFC 2595.

                context - a ssl.SSLContext
        """
        if not 支持SSL:
            raise 协议错误('-ERR TLS support missing')
        if self._tls_established:
            raise 协议错误('-ERR TLS session already established')
        caps = self.取能力()
        if not 'STLS' in caps:
            raise 协议错误('-ERR STLS not supported by server')
        if context is None:
            context = ssl._create_stdlib_context()
        resp = self._shortcmd('STLS')
        self.sock = context.wrap_socket(self.sock, server_hostname=self.host)
        self.file = self.sock.makefile('rb')
        self._tls_established = True
        return resp
_装类转发(POP3客户端, {'apop': 'APOP认证', 'capa': '取能力', 'dele': '删除邮件', 'getwelcome': '取欢迎语', 'noop': '空操作', 'pass_': '口令', 'retr': '取邮件', 'rpop': '远程弹出', 'rset': '重置会话', 'set_debuglevel': '设调试级别', 'stat': '取状态', 'stls': '启动TLS', 'timestamp': '时间戳', 'top': '取头部', 'uidl': '取唯一标识', 'user': '用户', 'utf8': '切换到UTF8'}, {'apop': 'APOP认证', 'capa': '取能力', 'dele': '删除邮件', 'getwelcome': '取欢迎语', 'noop': '空操作', 'pass_': '口令', 'retr': '取邮件', 'rpop': '远程弹出', 'rset': '重置会话', 'set_debuglevel': '设调试级别', 'stat': '取状态', 'stls': '启动TLS', 'timestamp': '时间戳', 'top': '取头部', 'uidl': '取唯一标识', 'user': '用户', 'utf8': '切换到UTF8'})
if 支持SSL:

    class POP3安全客户端(POP3客户端):
        """POP3 client class over SSL connection

        Instantiate with: POP3_SSL(hostname, port=995, context=None)

               hostname - the hostname of the pop3 over ssl server
               port - port number
               context - a ssl.SSLContext

        See the methods of the parent class POP3 for more documentation.
        """

        def __init__(self, host, port=POP3安全端口, *, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, context=None):
            if context is None:
                context = ssl._create_stdlib_context()
            self.context = context
            POP3客户端.__init__(self, host, port, timeout)

        def _create_socket(self, timeout):
            sock = POP3客户端._create_socket(self, timeout)
            sock = self.context.wrap_socket(sock, server_hostname=self.host)
            return sock

        def 启动TLS(self, context=None):
            """The method unconditionally raises an exception since the
            STLS command doesn't make any sense on an already established
            SSL/TLS session.
            """
            raise 协议错误('-ERR TLS session already established')
    _装类转发(POP3安全客户端, {'stls': '启动TLS'}, {'stls': '启动TLS'})
    __all__.append('POP3_SSL')
if __name__ == '__main__':
    a = POP3客户端(sys.argv[1])
    print(a.getwelcome())
    a.user(sys.argv[2])
    a.pass_(sys.argv[3])
    a.list()
    numMsgs, totalSize = a.stat()
    for i in range(1, numMsgs + 1):
        header, msg, octets = a.retr(i)
        print('Message %d:' % i)
        for line in msg:
            print('   ' + line)
        print('-----------------------')
    a.quit()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'CR': '回车',
    'CRLF': '回车换行',
    'HAVE_SSL': '支持SSL',
    'LF': '换行',
    'POP3': 'POP3客户端',
    'POP3_PORT': 'POP3端口',
    'POP3_SSL': 'POP3安全客户端',
    'POP3_SSL_PORT': 'POP3安全端口',
    'error_proto': '协议错误',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'POP3安全客户端': {
        'stls': '启动TLS',
    },
    'POP3客户端': {
        'apop': 'APOP认证',
        'capa': '取能力',
        'dele': '删除邮件',
        'getwelcome': '取欢迎语',
        'noop': '空操作',
        'pass_': '口令',
        'retr': '取邮件',
        'rpop': '远程弹出',
        'rset': '重置会话',
        'set_debuglevel': '设调试级别',
        'stat': '取状态',
        'stls': '启动TLS',
        'timestamp': '时间戳',
        'top': '取头部',
        'uidl': '取唯一标识',
        'user': '用户',
        'utf8': '切换到UTF8',
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
    'POP3安全客户端': {
        'stls': '启动TLS',
    },
    'POP3客户端': {
        'apop': 'APOP认证',
        'capa': '取能力',
        'dele': '删除邮件',
        'getwelcome': '取欢迎语',
        'noop': '空操作',
        'pass_': '口令',
        'retr': '取邮件',
        'rpop': '远程弹出',
        'rset': '重置会话',
        'set_debuglevel': '设调试级别',
        'stat': '取状态',
        'stls': '启动TLS',
        'timestamp': '时间戳',
        'top': '取头部',
        'uidl': '取唯一标识',
        'user': '用户',
        'utf8': '切换到UTF8',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'POP3安全客户端',
    'POP3客户端',
    '协议错误',
]

# ---- 转发层结束 ----
