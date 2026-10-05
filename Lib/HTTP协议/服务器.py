# -*- coding: utf-8 -*-
"""HTTP协议.服务器 —— 汉语库（由 tools/汉化库.py 从 Lib/http/server.py 机械生成，**不要手改**）。

英文库 Lib/http.server.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py http
"""


"""HTTP server classes.

Note: BaseHTTPRequestHandler doesn't implement any HTTP request; see
SimpleHTTPRequestHandler for simple implementations of GET, HEAD and POST,
and (deprecated) CGIHTTPRequestHandler for CGI scripts.

It does, however, optionally implement HTTP/1.1 persistent connections.

Notes on CGIHTTPRequestHandler
------------------------------

This class is deprecated. It implements GET and POST requests to cgi-bin scripts.

If the os.fork() function is not present (Windows), subprocess.Popen() is used,
with slightly altered but never documented semantics.  Use from a threaded
process is likely to trigger a warning at os.fork() time.

In all cases, the implementation is intentionally naive -- all
requests are executed synchronously.

SECURITY WARNING: DON'T USE THIS CODE UNLESS YOU ARE INSIDE A FIREWALL
-- it may execute arbitrary Python code or external programs.

Note that status code 200 is sent prior to execution of a CGI script, so
scripts cannot send other status codes such as 302 (redirect).

XXX To do:

- log requests even later (to capture byte count)
- log user-agent header and other interesting goodies
- send error log to separate file
"""
_英文原名表 = {'BaseHTTPRequestHandler': 'HTTP请求处理基类', 'CGIHTTPRequestHandler': 'CGI请求处理器', 'DEFAULT_ERROR_CONTENT_TYPE': '默认错误内容类型', 'DEFAULT_ERROR_MESSAGE': '默认错误消息', 'DualStackServerMixin': '双栈服务器混入', 'HTTPDualStackServer': 'HTTP双栈服务器', 'HTTPSDualStackServer': 'HTTPS双栈服务器', 'HTTPSServer': 'HTTPS服务器', 'HTTPServer': 'HTTP服务器', 'SimpleHTTPRequestHandler': '简单HTTP请求处理器', 'ThreadingHTTPSServer': '多线程HTTPS服务器', 'ThreadingHTTPServer': '多线程HTTP服务器', 'test': '演示服务器'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__version__ = '0.6'
__all__ = ['HTTPServer', 'ThreadingHTTPServer', 'HTTPSServer', 'ThreadingHTTPSServer', 'BaseHTTPRequestHandler', 'SimpleHTTPRequestHandler', 'CGIHTTPRequestHandler']
import copy
import datetime
import email.utils
import html
import HTTP协议.客户端
import io
import itertools
import mimetypes
import os
import posixpath
import select
import shutil
import socket
import socketserver
import sys
import time
import urllib.parse
from HTTP协议 import HTTPStatus
默认错误消息 = '<!DOCTYPE HTML>\n<html lang="en">\n    <head>\n        <meta charset="utf-8">\n        <style type="text/css">\n            :root {\n                color-scheme: light dark;\n            }\n        </style>\n        <title>Error response</title>\n    </head>\n    <body>\n        <h1>Error response</h1>\n        <p>Error code: %(code)d</p>\n        <p>Message: %(message)s.</p>\n        <p>Error code explanation: %(code)s - %(explain)s.</p>\n    </body>\n</html>\n'
默认错误内容类型 = 'text/html;charset=utf-8'
_MIN_READ_BUF_SIZE = 1 << 20

class HTTP服务器(socketserver.TCPServer):
    allow_reuse_address = True
    allow_reuse_port = False

    def server_bind(self):
        """Override server_bind to store the server name."""
        socketserver.TCPServer.server_bind(self)
        host, port = self.server_address[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

class 多线程HTTP服务器(socketserver.ThreadingMixIn, HTTP服务器):
    daemon_threads = True

class HTTPS服务器(HTTP服务器):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, *, certfile, keyfile=None, password=None, alpn_protocols=None):
        try:
            import ssl
        except ImportError:
            raise RuntimeError('SSL module is missing; HTTPS support is unavailable')
        self.ssl = ssl
        self.certfile = certfile
        self.keyfile = keyfile
        self.password = password
        self.alpn_protocols = ['http/1.1'] if alpn_protocols is None else alpn_protocols
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    def server_activate(self):
        """Wrap the socket in SSLSocket."""
        super().server_activate()
        context = self._create_context()
        self.socket = context.wrap_socket(self.socket, server_side=True)

    def _create_context(self):
        """Create a secure SSL context."""
        context = self.ssl.create_default_context(self.ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(self.certfile, self.keyfile, self.password)
        context.set_alpn_protocols(self.alpn_protocols)
        return context

class 多线程HTTPS服务器(socketserver.ThreadingMixIn, HTTPS服务器):
    daemon_threads = True

class HTTP请求处理基类(socketserver.StreamRequestHandler):
    """HTTP request handler base class.

    The following explanation of HTTP serves to guide you through the
    code as well as to expose any misunderstandings I may have about
    HTTP (so you don't need to read the code to figure out I'm wrong
    :-).

    HTTP (HyperText Transfer Protocol) is an extensible protocol on
    top of a reliable stream transport (e.g. TCP/IP).  The protocol
    recognizes three parts to a request:

    1. One line identifying the request type and path
    2. An optional set of RFC-822-style headers
    3. An optional data part

    The headers and data are separated by a blank line.

    The first line of the request has the form

    <command> <path> <version>

    where <command> is a (case-sensitive) keyword such as GET or POST,
    <path> is a string containing path information for the request,
    and <version> should be the string "HTTP/1.0" or "HTTP/1.1".
    <path> is encoded using the URL encoding scheme (using %xx to signify
    the ASCII character with hex code xx).

    The specification specifies that lines are separated by CRLF but
    for compatibility with the widest range of clients recommends
    servers also handle LF.  Similarly, whitespace in the request line
    is treated sensibly (allowing multiple spaces between components
    and allowing trailing whitespace).

    Similarly, for output, lines ought to be separated by CRLF pairs
    but most clients grok LF characters just fine.

    If the first line of the request has the form

    <command> <path>

    (i.e. <version> is left out) then this is assumed to be an HTTP
    0.9 request; this form has no optional headers and data part and
    the reply consists of just the data.

    The reply form of the HTTP 1.x protocol again has three parts:

    1. One line giving the response code
    2. An optional set of RFC-822-style headers
    3. The data

    Again, the headers and data are separated by a blank line.

    The response code line has the form

    <version> <responsecode> <responsestring>

    where <version> is the protocol version ("HTTP/1.0" or "HTTP/1.1"),
    <responsecode> is a 3-digit response code indicating success or
    failure of the request, and <responsestring> is an optional
    human-readable string explaining what the response code means.

    This server parses the request and the headers, and then calls a
    function specific to the request type (<command>).  Specifically,
    a request SPAM will be handled by a method do_SPAM().  If no
    such method exists the server sends an error response to the
    client.  If it exists, it is called with no arguments:

    do_SPAM()

    Note that the request name is case sensitive (i.e. SPAM and spam
    are different requests).

    The various request details are stored in instance variables:

    - client_address is the client IP address in the form (host,
    port);

    - command, path and version are the broken-down request line;

    - headers is an instance of email.message.Message (or a derived
    class) containing the header information;

    - rfile is a file object open for reading positioned at the
    start of the optional input data part;

    - wfile is a file object open for writing.

    IT IS IMPORTANT TO ADHERE TO THE PROTOCOL FOR WRITING!

    The first thing to be written must be the response line.  Then
    follow 0 or more header lines, then a blank line, and then the
    actual data (if any).  The meaning of the header lines depends on
    the command executed by the server; in most cases, when data is
    returned, there should be at least one header line of the form

    Content-type: <type>/<subtype>

    where <type> and <subtype> should be registered MIME types,
    e.g. "text/html" or "text/plain".

    """
    sys_version = 'Python/' + sys.version.split()[0]
    server_version = 'BaseHTTP/' + __version__
    error_message_format = 默认错误消息
    error_content_type = 默认错误内容类型
    default_request_version = 'HTTP/0.9'

    def parse_request(self):
        """Parse a request (internal).

        The request should be stored in self.raw_requestline; the results
        are in self.command, self.path, self.request_version and
        self.headers.

        Return True for success, False for failure; on failure, any relevant
        error response has already been sent back.

        """
        is_http_0_9 = False
        self.command = None
        self.request_version = version = self.default_request_version
        self.close_connection = True
        requestline = str(self.raw_requestline, 'iso-8859-1')
        requestline = requestline.rstrip('\r\n')
        self.requestline = requestline
        words = requestline.split()
        if len(words) == 0:
            return False
        if len(words) >= 3:
            version = words[-1]
            try:
                if not version.startswith('HTTP/'):
                    raise ValueError
                base_version_number = version.split('/', 1)[1]
                version_number = base_version_number.split('.')
                if len(version_number) != 2:
                    raise ValueError
                if any((not component.isdigit() for component in version_number)):
                    raise ValueError('non digit in http version')
                if any((len(component) > 10 for component in version_number)):
                    raise ValueError('unreasonable length http version')
                version_number = (int(version_number[0]), int(version_number[1]))
            except (ValueError, IndexError):
                self.request_version = ''
                self.send_error(HTTPStatus.BAD_REQUEST, 'Bad request version (%r)' % version)
                return False
            self.request_version = version
            if version_number >= (1, 1) and self.protocol_version >= 'HTTP/1.1':
                self.close_connection = False
            if version_number >= (2, 0):
                self.send_error(HTTPStatus.HTTP_VERSION_NOT_SUPPORTED, 'Invalid HTTP version (%s)' % base_version_number)
                return False
        if not 2 <= len(words) <= 3:
            self.request_version = ''
            self.send_error(HTTPStatus.BAD_REQUEST, 'Bad request syntax (%r)' % requestline)
            return False
        command, path = words[:2]
        if len(words) == 2:
            self.close_connection = True
            if command != 'GET':
                self.request_version = ''
                self.send_error(HTTPStatus.BAD_REQUEST, 'Bad HTTP/0.9 request type (%r)' % command)
                return False
            is_http_0_9 = True
        self.command, self.path = (command, path)
        if self.path.startswith('//'):
            self.path = '/' + self.path.lstrip('/')
        if is_http_0_9:
            self.headers = {}
            return True
        try:
            self.headers = HTTP协议.客户端.parse_headers(self.rfile, _class=self.MessageClass)
        except HTTP协议.客户端.LineTooLong as err:
            self.send_error(HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE, 'Line too long', str(err))
            return False
        except HTTP协议.客户端.HTTPException as err:
            self.send_error(HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE, 'Too many headers', str(err))
            return False
        conntype = self.headers.get('Connection', '')
        if conntype.lower() == 'close':
            self.close_connection = True
        elif conntype.lower() == 'keep-alive' and self.protocol_version >= 'HTTP/1.1':
            self.close_connection = False
        expect = self.headers.get('Expect', '')
        if expect.lower() == '100-continue' and self.protocol_version >= 'HTTP/1.1' and (self.request_version >= 'HTTP/1.1'):
            if not self.handle_expect_100():
                return False
        return True

    def handle_expect_100(self):
        """Decide what to do with an "Expect: 100-continue" header.

        If the client is expecting a 100 Continue response, we must
        respond with either a 100 Continue or a final response before
        waiting for the request body. The default is to always respond
        with a 100 Continue. You can behave differently (for example,
        reject unauthorized requests) by overriding this method.

        This method should either return True (possibly after sending
        a 100 Continue response) or send an error response and return
        False.

        """
        self.send_response_only(HTTPStatus.CONTINUE)
        self.end_headers()
        return True

    def handle_one_request(self):
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                return
            mname = 'do_' + self.command
            if not hasattr(self, mname):
                self.send_error(HTTPStatus.NOT_IMPLEMENTED, 'Unsupported method (%r)' % self.command)
                return
            method = getattr(self, mname)
            method()
            self.wfile.flush()
        except TimeoutError as e:
            self.log_error('Request timed out: %r', e)
            self.close_connection = True
            return

    def handle(self):
        """Handle multiple requests if necessary."""
        self.close_connection = True
        self.handle_one_request()
        while not self.close_connection:
            self.handle_one_request()

    def send_error(self, code, message=None, explain=None):
        """Send and log an error reply.

        Arguments are
        * code:    an HTTP error code
                   3 digits
        * message: a simple optional 1 line reason phrase.
                   *( HTAB / SP / VCHAR / %x80-FF )
                   defaults to short entry matching the response code
        * explain: a detailed message defaults to the long entry
                   matching the response code.

        This sends an error response (so it must be called before any
        output has been generated), logs the error, and finally sends
        a piece of HTML explaining the error to the user.

        """
        try:
            shortmsg, longmsg = self.responses[code]
        except KeyError:
            shortmsg, longmsg = ('???', '???')
        if message is None:
            message = shortmsg
        if explain is None:
            explain = longmsg
        self.log_error('code %d, message %s', code, message)
        self.send_response(code, message)
        self.send_header('Connection', 'close')
        body = None
        if code >= 200 and code not in (HTTPStatus.NO_CONTENT, HTTPStatus.RESET_CONTENT, HTTPStatus.NOT_MODIFIED):
            content = self.error_message_format % {'code': code, 'message': html.escape(message, quote=False), 'explain': html.escape(explain, quote=False)}
            body = content.encode('UTF-8', 'replace')
            self.send_header('Content-Type', self.error_content_type)
            self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if self.command != 'HEAD' and body:
            self.wfile.write(body)

    def send_response(self, code, message=None):
        """Add the response header to the headers buffer and log the
        response code.

        Also send two standard headers with the server software
        version and the current date.

        """
        self.log_request(code)
        self.send_response_only(code, message)
        self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())

    def send_response_only(self, code, message=None):
        """Send the response header only."""
        if self.request_version != 'HTTP/0.9':
            if message is None:
                if code in self.responses:
                    message = self.responses[code][0]
                else:
                    message = ''
            if not hasattr(self, '_headers_buffer'):
                self._headers_buffer = []
            self._headers_buffer.append(('%s %d %s\r\n' % (self.protocol_version, code, message)).encode('latin-1', 'strict'))

    def send_header(self, keyword, value):
        """Send a MIME header to the headers buffer."""
        if self.request_version != 'HTTP/0.9':
            if not hasattr(self, '_headers_buffer'):
                self._headers_buffer = []
            self._headers_buffer.append(('%s: %s\r\n' % (keyword, value)).encode('latin-1', 'strict'))
        if keyword.lower() == 'connection':
            if value.lower() == 'close':
                self.close_connection = True
            elif value.lower() == 'keep-alive':
                self.close_connection = False

    def end_headers(self):
        """Send the blank line ending the MIME headers."""
        if self.request_version != 'HTTP/0.9':
            self._headers_buffer.append(b'\r\n')
            self.flush_headers()

    def flush_headers(self):
        if hasattr(self, '_headers_buffer'):
            self.wfile.write(b''.join(self._headers_buffer))
            self._headers_buffer = []

    def log_request(self, code='-', size='-'):
        """Log an accepted request.

        This is called by send_response().

        """
        if isinstance(code, HTTPStatus):
            code = code.value
        self.log_message('"%s" %s %s', self.requestline, str(code), str(size))

    def log_error(self, format, *args):
        """Log an error.

        This is called when a request cannot be fulfilled.  By
        default it passes the message on to log_message().

        Arguments are the same as for log_message().

        XXX This should go to the separate error log.

        """
        self.log_message(format, *args)
    _control_char_table = str.maketrans({c: f'\\x{c:02x}' for c in itertools.chain(range(32), range(127, 160))})
    _control_char_table[ord('\\')] = '\\\\'

    def log_message(self, format, *args):
        """Log an arbitrary message.

        This is used by all other logging functions.  Override
        it if you have specific logging wishes.

        The first argument, FORMAT, is a format string for the
        message to be logged.  If the format string contains
        any % escapes requiring parameters, they should be
        specified as subsequent arguments (it's just like
        printf!).

        The client ip and current date/time are prefixed to
        every message.

        Unicode control characters are replaced with escaped hex
        before writing the output to stderr.

        """
        message = format % args
        sys.stderr.write('%s - - [%s] %s\n' % (self.address_string(), self.log_date_time_string(), message.translate(self._control_char_table)))

    def version_string(self):
        """Return the server software version string."""
        return self.server_version + ' ' + self.sys_version

    def date_time_string(self, timestamp=None):
        """Return the current date and time formatted for a message header."""
        if timestamp is None:
            timestamp = time.time()
        return email.utils.formatdate(timestamp, usegmt=True)

    def log_date_time_string(self):
        """Return the current time formatted for logging."""
        now = time.time()
        year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
        s = '%02d/%3s/%04d %02d:%02d:%02d' % (day, self.monthname[month], year, hh, mm, ss)
        return s
    weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    monthname = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def address_string(self):
        """Return the client address."""
        return self.client_address[0]
    protocol_version = 'HTTP/1.0'
    MessageClass = HTTP协议.客户端.HTTPMessage
    responses = {v: (v.phrase, v.description) for v in HTTPStatus.__members__.values()}

class 简单HTTP请求处理器(HTTP请求处理基类):
    """Simple HTTP request handler with GET and HEAD commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method.

    The GET and HEAD requests are identical except that the HEAD
    request omits the actual contents of the file.

    """
    server_version = 'SimpleHTTP/' + __version__
    index_pages = ('index.html', 'index.htm')
    extensions_map = _encodings_map_default = {'.gz': 'application/gzip', '.Z': 'application/octet-stream', '.bz2': 'application/x-bzip2', '.xz': 'application/x-xz'}

    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = os.fspath(directory)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            parts = urllib.parse.urlsplit(self.path)
            if not parts.path.endswith(('/', '%2f', '%2F')):
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                new_parts = (parts[0], parts[1], parts[2] + '/', parts[3], parts[4])
                new_url = urllib.parse.urlunsplit(new_parts)
                self.send_header('Location', new_url)
                self.send_header('Content-Length', '0')
                self.end_headers()
                return None
            for index in self.index_pages:
                index = os.path.join(path, index)
                if os.path.isfile(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        if path.endswith('/'):
            self.send_error(HTTPStatus.NOT_FOUND, 'File not found')
            return None
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, 'File not found')
            return None
        try:
            fs = os.fstat(f.fileno())
            if 'If-Modified-Since' in self.headers and 'If-None-Match' not in self.headers:
                try:
                    ims = email.utils.parsedate_to_datetime(self.headers['If-Modified-Since'])
                except (TypeError, IndexError, OverflowError, ValueError):
                    pass
                else:
                    if ims.tzinfo is None:
                        ims = ims.replace(tzinfo=datetime.timezone.utc)
                    if ims.tzinfo is datetime.timezone.utc:
                        last_modif = datetime.datetime.fromtimestamp(fs.st_mtime, datetime.timezone.utc)
                        last_modif = last_modif.replace(microsecond=0)
                        if last_modif <= ims:
                            self.send_response(HTTPStatus.NOT_MODIFIED)
                            self.end_headers()
                            f.close()
                            return None
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', ctype)
            self.send_header('Content-Length', str(fs[6]))
            self.send_header('Last-Modified', self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, 'No permission to list directory')
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        displaypath = self.path
        displaypath = displaypath.split('#', 1)[0]
        displaypath = displaypath.split('?', 1)[0]
        try:
            displaypath = urllib.parse.unquote(displaypath, errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(displaypath)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
        title = f'Directory listing for {displaypath}'
        r.append('<!DOCTYPE HTML>')
        r.append('<html lang="en">')
        r.append('<head>')
        r.append(f'<meta charset="{enc}">')
        r.append('<style type="text/css">\n:root {\ncolor-scheme: light dark;\n}\n</style>')
        r.append(f'<title>{title}</title>\n</head>')
        r.append(f'<body>\n<h1>{title}</h1>')
        r.append('<hr>\n<ul>')
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            if os.path.isdir(fullname):
                displayname = name + '/'
                linkname = name + '/'
            if os.path.islink(fullname):
                displayname = name + '@'
            r.append('<li><a href="%s">%s</a></li>' % (urllib.parse.quote(linkname, errors='surrogatepass'), html.escape(displayname, quote=False)))
        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/html; charset=%s' % enc)
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        path = path.split('#', 1)[0]
        path = path.split('?', 1)[0]
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        trailing_slash = path.endswith('/')
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = self.directory
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        guess, _ = mimetypes.guess_file_type(path)
        if guess:
            return guess
        return 'application/octet-stream'

def _url_collapse_path(path):
    """
    Given a URL path, remove extra '/'s and '.' path elements and collapse
    any '..' references and returns a collapsed path.

    Implements something akin to RFC-2396 5.2 step 6 to parse relative paths.
    The utility of this function is limited to is_cgi method and helps
    preventing some security attacks.

    Returns: The reconstituted URL, which will always start with a '/'.

    Raises: IndexError if too many '..' occur within the path.

    """
    path, _, query = path.partition('?')
    path = urllib.parse.unquote(path)
    path_parts = path.split('/')
    head_parts = []
    for part in path_parts[:-1]:
        if part == '..':
            head_parts.pop()
        elif part and part != '.':
            head_parts.append(part)
    if path_parts:
        tail_part = path_parts.pop()
        if tail_part:
            if tail_part == '..':
                head_parts.pop()
                tail_part = ''
            elif tail_part == '.':
                tail_part = ''
    else:
        tail_part = ''
    if query:
        tail_part = '?'.join((tail_part, query))
    splitpath = ('/' + '/'.join(head_parts), tail_part)
    collapsed_path = '/'.join(splitpath)
    return collapsed_path
nobody = None

def nobody_uid():
    """Internal routine to get nobody's uid"""
    global nobody
    if nobody:
        return nobody
    try:
        import pwd
    except ImportError:
        return -1
    try:
        nobody = pwd.getpwnam('nobody')[2]
    except KeyError:
        nobody = 1 + max((x[2] for x in pwd.getpwall()))
    return nobody

def executable(path):
    """Test for executable file."""
    return os.access(path, os.X_OK)

class CGI请求处理器(简单HTTP请求处理器):
    """Complete HTTP server with GET, HEAD and POST commands.

    GET and HEAD also support running CGI scripts.

    The POST command is *only* implemented for CGI scripts.

    """

    def __init__(self, *args, **kwargs):
        import warnings
        warnings._deprecated('http.server.CGIHTTPRequestHandler', remove=(3, 15))
        super().__init__(*args, **kwargs)
    have_fork = hasattr(os, 'fork')
    rbufsize = 0

    def do_POST(self):
        """Serve a POST request.

        This is only implemented for CGI scripts.

        """
        if self.is_cgi():
            self.run_cgi()
        else:
            self.send_error(HTTPStatus.NOT_IMPLEMENTED, 'Can only POST to CGI scripts')

    def send_head(self):
        """Version of send_head that support CGI scripts"""
        if self.is_cgi():
            return self.run_cgi()
        else:
            return 简单HTTP请求处理器.send_head(self)

    def is_cgi(self):
        """Test whether self.path corresponds to a CGI script.

        Returns True and updates the cgi_info attribute to the tuple
        (dir, rest) if self.path requires running a CGI script.
        Returns False otherwise.

        If any exception is raised, the caller should assume that
        self.path was rejected as invalid and act accordingly.

        The default implementation tests whether the normalized url
        path begins with one of the strings in self.cgi_directories
        (and the next character is a '/' or the end of the string).

        """
        collapsed_path = _url_collapse_path(self.path)
        dir_sep = collapsed_path.find('/', 1)
        while dir_sep > 0 and (not collapsed_path[:dir_sep] in self.cgi_directories):
            dir_sep = collapsed_path.find('/', dir_sep + 1)
        if dir_sep > 0:
            head, tail = (collapsed_path[:dir_sep], collapsed_path[dir_sep + 1:])
            self.cgi_info = (head, tail)
            return True
        return False
    cgi_directories = ['/cgi-bin', '/htbin']

    def is_executable(self, path):
        """Test whether argument path is an executable file."""
        return executable(path)

    def is_python(self, path):
        """Test whether argument path is a Python script."""
        head, tail = os.path.splitext(path)
        return tail.lower() in ('.py', '.pyw')

    def run_cgi(self):
        """Execute a CGI script."""
        dir, rest = self.cgi_info
        path = dir + '/' + rest
        i = path.find('/', len(dir) + 1)
        while i >= 0:
            nextdir = path[:i]
            nextrest = path[i + 1:]
            scriptdir = self.translate_path(nextdir)
            if os.path.isdir(scriptdir):
                dir, rest = (nextdir, nextrest)
                i = path.find('/', len(dir) + 1)
            else:
                break
        rest, _, query = rest.partition('?')
        i = rest.find('/')
        if i >= 0:
            script, rest = (rest[:i], rest[i:])
        else:
            script, rest = (rest, '')
        scriptname = dir + '/' + script
        scriptfile = self.translate_path(scriptname)
        if not os.path.exists(scriptfile):
            self.send_error(HTTPStatus.NOT_FOUND, 'No such CGI script (%r)' % scriptname)
            return
        if not os.path.isfile(scriptfile):
            self.send_error(HTTPStatus.FORBIDDEN, 'CGI script is not a plain file (%r)' % scriptname)
            return
        ispy = self.is_python(scriptname)
        if self.have_fork or not ispy:
            if not self.is_executable(scriptfile):
                self.send_error(HTTPStatus.FORBIDDEN, 'CGI script is not executable (%r)' % scriptname)
                return
        env = copy.deepcopy(os.environ)
        env['SERVER_SOFTWARE'] = self.version_string()
        env['SERVER_NAME'] = self.server.server_name
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['SERVER_PROTOCOL'] = self.protocol_version
        env['SERVER_PORT'] = str(self.server.server_port)
        env['REQUEST_METHOD'] = self.command
        uqrest = urllib.parse.unquote(rest)
        env['PATH_INFO'] = uqrest
        env['PATH_TRANSLATED'] = self.translate_path(uqrest)
        env['SCRIPT_NAME'] = scriptname
        env['QUERY_STRING'] = query
        env['REMOTE_ADDR'] = self.client_address[0]
        authorization = self.headers.get('authorization')
        if authorization:
            authorization = authorization.split()
            if len(authorization) == 2:
                import base64, binascii
                env['AUTH_TYPE'] = authorization[0]
                if authorization[0].lower() == 'basic':
                    try:
                        authorization = authorization[1].encode('ascii')
                        authorization = base64.decodebytes(authorization).decode('ascii')
                    except (binascii.Error, UnicodeError):
                        pass
                    else:
                        authorization = authorization.split(':')
                        if len(authorization) == 2:
                            env['REMOTE_USER'] = authorization[0]
        if self.headers.get('content-type') is None:
            env['CONTENT_TYPE'] = self.headers.get_content_type()
        else:
            env['CONTENT_TYPE'] = self.headers['content-type']
        length = self.headers.get('content-length')
        if length:
            env['CONTENT_LENGTH'] = length
        referer = self.headers.get('referer')
        if referer:
            env['HTTP_REFERER'] = referer
        accept = self.headers.get_all('accept', ())
        env['HTTP_ACCEPT'] = ','.join(accept)
        ua = self.headers.get('user-agent')
        if ua:
            env['HTTP_USER_AGENT'] = ua
        co = filter(None, self.headers.get_all('cookie', []))
        cookie_str = ', '.join(co)
        if cookie_str:
            env['HTTP_COOKIE'] = cookie_str
        for k in ('QUERY_STRING', 'REMOTE_HOST', 'CONTENT_LENGTH', 'HTTP_USER_AGENT', 'HTTP_COOKIE', 'HTTP_REFERER'):
            env.setdefault(k, '')
        self.send_response(HTTPStatus.OK, 'Script output follows')
        self.flush_headers()
        decoded_query = query.replace('+', ' ')
        if self.have_fork:
            args = [script]
            if '=' not in decoded_query:
                args.append(decoded_query)
            nobody = nobody_uid()
            self.wfile.flush()
            pid = os.fork()
            if pid != 0:
                pid, sts = os.waitpid(pid, 0)
                while select.select([self.rfile], [], [], 0)[0]:
                    if not self.rfile.read(1):
                        break
                exitcode = os.waitstatus_to_exitcode(sts)
                if exitcode:
                    self.log_error(f'CGI script exit code {exitcode}')
                return
            try:
                try:
                    os.setuid(nobody)
                except OSError:
                    pass
                os.dup2(self.rfile.fileno(), 0)
                os.dup2(self.wfile.fileno(), 1)
                os.execve(scriptfile, args, env)
            except:
                self.server.handle_error(self.request, self.client_address)
                os._exit(127)
        else:
            import subprocess
            cmdline = [scriptfile]
            if self.is_python(scriptfile):
                interp = sys.executable
                if interp.lower().endswith('w.exe'):
                    interp = interp[:-5] + interp[-4:]
                cmdline = [interp, '-u'] + cmdline
            if '=' not in query:
                cmdline.append(query)
            self.log_message('command: %s', subprocess.list2cmdline(cmdline))
            try:
                nbytes = int(length)
            except (TypeError, ValueError):
                nbytes = 0
            p = subprocess.Popen(cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            if self.command.lower() == 'post' and nbytes > 0:
                cursize = 0
                data = self.rfile.read(min(nbytes, _MIN_READ_BUF_SIZE))
                while len(data) < nbytes and len(data) != cursize:
                    cursize = len(data)
                    delta = min(cursize, nbytes - cursize)
                    try:
                        data += self.rfile.read(delta)
                    except TimeoutError:
                        break
            else:
                data = None
            while select.select([self.rfile._sock], [], [], 0)[0]:
                if not self.rfile._sock.recv(1):
                    break
            stdout, stderr = p.communicate(data)
            self.wfile.write(stdout)
            if stderr:
                self.log_error('%s', stderr)
            p.stderr.close()
            p.stdout.close()
            status = p.returncode
            if status:
                self.log_error('CGI script exit status %#x', status)
            else:
                self.log_message('CGI script exited OK')

def _get_best_family(*address):
    infos = socket.getaddrinfo(*address, type=socket.SOCK_STREAM, flags=socket.AI_PASSIVE)
    family, type, proto, canonname, sockaddr = next(iter(infos))
    return (family, sockaddr)

def 演示服务器(HandlerClass=HTTP请求处理基类, ServerClass=多线程HTTP服务器, protocol='HTTP/1.0', port=8000, bind=None, tls_cert=None, tls_key=None, tls_password=None):
    """Test the HTTP request handler class.

    This runs an HTTP server on port 8000 (or the port argument).

    """
    ServerClass.address_family, addr = _get_best_family(bind, port)
    HandlerClass.protocol_version = protocol
    if tls_cert:
        服务器 = ServerClass(addr, HandlerClass, certfile=tls_cert, keyfile=tls_key, password=tls_password)
    else:
        服务器 = ServerClass(addr, HandlerClass)
    with 服务器 as httpd:
        host, port = httpd.socket.getsockname()[:2]
        url_host = f'[{host}]' if ':' in host else host
        protocol = 'HTTPS' if tls_cert else 'HTTP'
        print(f'Serving {protocol} on {host} port {port} ({protocol.lower()}://{url_host}:{port}/) ...')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nKeyboard interrupt received, exiting.')
            sys.exit(0)
if __name__ == '__main__':
    import argparse
    import contextlib
    parser = argparse.ArgumentParser(color=True)
    parser.add_argument('--cgi', action='store_true', help='run as CGI server')
    parser.add_argument('-b', '--bind', metavar='ADDRESS', help='bind to this address (default: all interfaces)')
    parser.add_argument('-d', '--directory', default=os.getcwd(), help='serve this directory (default: current directory)')
    parser.add_argument('-p', '--protocol', metavar='VERSION', default='HTTP/1.0', help='conform to this HTTP version (default: %(default)s)')
    parser.add_argument('--tls-cert', metavar='PATH', help='path to the TLS certificate chain file')
    parser.add_argument('--tls-key', metavar='PATH', help='path to the TLS key file')
    parser.add_argument('--tls-password-file', metavar='PATH', help='path to the password file for the TLS key')
    parser.add_argument('port', default=8000, type=int, nargs='?', help='bind to this port (default: %(default)s)')
    args = parser.parse_args()
    if not args.tls_cert and args.tls_key:
        parser.error('--tls-key requires --tls-cert to be set')
    tls_key_password = None
    if args.tls_password_file:
        if not args.tls_cert:
            parser.error('--tls-password-file requires --tls-cert to be set')
        try:
            with open(args.tls_password_file, 'r', encoding='utf-8') as f:
                tls_key_password = f.read().strip()
        except OSError as e:
            parser.error(f'Failed to read TLS password file: {e}')
    if args.cgi:
        handler_class = CGI请求处理器
    else:
        handler_class = 简单HTTP请求处理器

    class 双栈服务器混入:

        def server_bind(self):
            with contextlib.suppress(Exception):
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

        def finish_request(self, request, client_address):
            self.RequestHandlerClass(request, client_address, self, directory=args.directory)

    class HTTP双栈服务器(双栈服务器混入, 多线程HTTP服务器):
        pass

    class HTTPS双栈服务器(双栈服务器混入, 多线程HTTPS服务器):
        pass
    ServerClass = HTTPS双栈服务器 if args.tls_cert else HTTP双栈服务器
    演示服务器(HandlerClass=handler_class, ServerClass=ServerClass, port=args.port, bind=args.bind, protocol=args.protocol, tls_cert=args.tls_cert, tls_key=args.tls_key, tls_password=tls_key_password)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BaseHTTPRequestHandler': 'HTTP请求处理基类',
    'CGIHTTPRequestHandler': 'CGI请求处理器',
    'DEFAULT_ERROR_CONTENT_TYPE': '默认错误内容类型',
    'DEFAULT_ERROR_MESSAGE': '默认错误消息',
    'DualStackServerMixin': '双栈服务器混入',
    'HTTPDualStackServer': 'HTTP双栈服务器',
    'HTTPSDualStackServer': 'HTTPS双栈服务器',
    'HTTPSServer': 'HTTPS服务器',
    'HTTPServer': 'HTTP服务器',
    'SimpleHTTPRequestHandler': '简单HTTP请求处理器',
    'ThreadingHTTPSServer': '多线程HTTPS服务器',
    'ThreadingHTTPServer': '多线程HTTP服务器',
    'test': '演示服务器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'CGI请求处理器',
    'HTTPS服务器',
    'HTTP服务器',
    'HTTP请求处理基类',
    '多线程HTTPS服务器',
    '多线程HTTP服务器',
    '简单HTTP请求处理器',
]

# ---- 转发层结束 ----
