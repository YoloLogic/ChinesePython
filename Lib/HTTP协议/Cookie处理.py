# -*- coding: utf-8 -*-
"""HTTP协议.Cookie处理 —— 汉语库（由 tools/汉化库.py 从 Lib/http/cookies.py 机械生成，**不要手改**）。

英文库 Lib/http.cookies.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py http
"""


"""
Here's a sample session to show how to use this module.
At the moment, this is the only documentation.

The Basics
----------

Importing is easy...

   >>> from http import cookies

Most of the time you start by creating a cookie.

   >>> C = cookies.SimpleCookie()

Once you've created your Cookie, you can add values just as if it were
a dictionary.

   >>> C = cookies.SimpleCookie()
   >>> C["fig"] = "newton"
   >>> C["sugar"] = "wafer"
   >>> C.output()
   'Set-Cookie: fig=newton\\r\\nSet-Cookie: sugar=wafer'

Notice that the printable representation of a Cookie is the
appropriate format for a Set-Cookie: header.  This is the
default behavior.  You can change the header and printed
attributes by using the .output() function

   >>> C = cookies.SimpleCookie()
   >>> C["rocky"] = "road"
   >>> C["rocky"]["path"] = "/cookie"
   >>> print(C.output(header="Cookie:"))
   Cookie: rocky=road; Path=/cookie
   >>> print(C.output(attrs=[], header="Cookie:"))
   Cookie: rocky=road

The load() method of a Cookie extracts cookies from a string.  In a
CGI script, you would use this method to extract the cookies from the
HTTP_COOKIE environment variable.

   >>> C = cookies.SimpleCookie()
   >>> C.load("chips=ahoy; vienna=finger")
   >>> C.output()
   'Set-Cookie: chips=ahoy\\r\\nSet-Cookie: vienna=finger'

The load() method is darn-tootin smart about identifying cookies
within a string.  Escaped quotation marks, nested semicolons, and other
such trickeries do not confuse it.

   >>> C = cookies.SimpleCookie()
   >>> C.load('keebler="E=everybody; L=\\\\"Loves\\\\"; fudge=;";')
   >>> print(C)
   Set-Cookie: keebler="E=everybody; L=\\"Loves\\"; fudge=;"

Each element of the Cookie also supports all of the RFC 2109
Cookie attributes.  Here's an example which sets the Path
attribute.

   >>> C = cookies.SimpleCookie()
   >>> C["oreo"] = "doublestuff"
   >>> C["oreo"]["path"] = "/"
   >>> print(C)
   Set-Cookie: oreo=doublestuff; Path=/

Each dictionary element has a 'value' attribute, which gives you
back the value associated with the key.

   >>> C = cookies.SimpleCookie()
   >>> C["twix"] = "none for you"
   >>> C["twix"].value
   'none for you'

The SimpleCookie expects that all values should be standard strings.
Just to be sure, SimpleCookie invokes the str() builtin to convert
the value to a string, when the values are set dictionary-style.

   >>> C = cookies.SimpleCookie()
   >>> C["number"] = 7
   >>> C["string"] = "seven"
   >>> C["number"].value
   '7'
   >>> C["string"].value
   'seven'
   >>> C.output()
   'Set-Cookie: number=7\\r\\nSet-Cookie: string=seven'

Finis.
"""
_英文原名表 = {'BaseCookie': '基础Cookie', 'CookieError': 'Cookie错误', 'Morsel': 'Cookie项', 'SimpleCookie': '简单Cookie'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import re
import string
import types
__all__ = ['CookieError', 'BaseCookie', 'SimpleCookie']
_nulljoin = ''.join
_semispacejoin = '; '.join
_spacejoin = ' '.join

class Cookie错误(Exception):
    pass
_LegalChars = string.ascii_letters + string.digits + "!#$%&'*+-.^_`|~:"
_UnescapedChars = _LegalChars + ' ()/<=>?@[]{}'
_Translator = {n: '\\%03o' % n for n in set(range(256)) - set(map(ord, _UnescapedChars))}
_Translator.update({ord('"'): '\\"', ord('\\'): '\\\\'})
_is_legal_key = re.compile('[%s]+' % re.escape(_LegalChars)).fullmatch
_control_character_re = re.compile('[\\x00-\\x1F\\x7F]')

def _has_control_character(*val):
    """Detects control characters within a value.
    Supports any type, as header values can be any type.
    """
    return any((_control_character_re.search(str(v)) for v in val))

def _quote(str):
    """Quote a string for use in a cookie header.

    If the string does not need to be double-quoted, then just return the
    string.  Otherwise, surround the string in doublequotes and quote
    (with a \\) special characters.
    """
    if str is None or _is_legal_key(str):
        return str
    else:
        return '"' + str.translate(_Translator) + '"'
_unquote_sub = re.compile('\\\\(?:([0-3][0-7][0-7])|(.))').sub

def _unquote_replace(m):
    if m[1]:
        return chr(int(m[1], 8))
    else:
        return m[2]

def _unquote(str):
    if str is None or len(str) < 2:
        return str
    if str[0] != '"' or str[-1] != '"':
        return str
    str = str[1:-1]
    return _unquote_sub(_unquote_replace, str)
_weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
_monthname = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def _getdate(future=0, weekdayname=_weekdayname, monthname=_monthname):
    from time import gmtime, time
    now = time()
    year, month, day, hh, mm, ss, wd, y, z = gmtime(now + future)
    return '%s, %02d %3s %4d %02d:%02d:%02d GMT' % (weekdayname[wd], day, monthname[month], year, hh, mm, ss)

class Cookie项(dict):
    """A class to hold ONE (key, value) pair.

    In a cookie, each such pair may have several attributes, so this class is
    used to keep the attributes associated with the appropriate key,value pair.
    This class also includes a coded_value attribute, which is used to hold
    the network representation of the value.
    """
    _reserved = {'expires': 'expires', 'path': 'Path', 'comment': 'Comment', 'domain': 'Domain', 'max-age': 'Max-Age', 'secure': 'Secure', 'httponly': 'HttpOnly', 'version': 'Version', 'samesite': 'SameSite', 'partitioned': 'Partitioned'}
    _reserved_defaults = dict.fromkeys(_reserved, '')
    _flags = {'secure', 'httponly', 'partitioned'}

    def __init__(self):
        self._key = self._value = self._coded_value = None
        dict.update(self, self._reserved_defaults)

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @property
    def coded_value(self):
        return self._coded_value

    def __setitem__(self, K, V):
        K = K.lower()
        if not K in self._reserved:
            raise Cookie错误('Invalid attribute %r' % (K,))
        if _has_control_character(K, V):
            raise Cookie错误(f'Control characters are not allowed in cookies {K!r} {V!r}')
        dict.__setitem__(self, K, V)

    def setdefault(self, key, val=None):
        key = key.lower()
        if key not in self._reserved:
            raise Cookie错误('Invalid attribute %r' % (key,))
        if _has_control_character(key, val):
            raise Cookie错误('Control characters are not allowed in cookies %r %r' % (key, val))
        return dict.setdefault(self, key, val)

    def __eq__(self, morsel):
        if not isinstance(morsel, Cookie项):
            return NotImplemented
        return dict.__eq__(self, morsel) and self._value == morsel._value and (self._key == morsel._key) and (self._coded_value == morsel._coded_value)
    __ne__ = object.__ne__

    def copy(self):
        morsel = Cookie项()
        dict.update(morsel, self)
        morsel.__dict__.update(self.__dict__)
        return morsel

    def update(self, values):
        data = {}
        for key, val in dict(values).items():
            key = key.lower()
            if key not in self._reserved:
                raise Cookie错误('Invalid attribute %r' % (key,))
            if _has_control_character(key, val):
                raise Cookie错误(f'Control characters are not allowed in cookies {key!r} {val!r}')
            data[key] = val
        dict.update(self, data)

    def __ior__(self, values):
        self.update(values)
        return self

    def isReservedKey(self, K):
        return K.lower() in self._reserved

    def set(self, key, val, coded_val):
        if key.lower() in self._reserved:
            raise Cookie错误('Attempt to set a reserved key %r' % (key,))
        if not _is_legal_key(key):
            raise Cookie错误('Illegal key %r' % (key,))
        if _has_control_character(key, val, coded_val):
            raise Cookie错误('Control characters are not allowed in cookies %r %r %r' % (key, val, coded_val))
        self._key = key
        self._value = val
        self._coded_value = coded_val

    def __getstate__(self):
        return {'key': self._key, 'value': self._value, 'coded_value': self._coded_value}

    def __setstate__(self, state):
        key = state['key']
        value = state['value']
        coded_value = state['coded_value']
        if _has_control_character(key, value, coded_value):
            raise Cookie错误(f'Control characters are not allowed in cookies {key!r} {value!r} {coded_value!r}')
        self._key = key
        self._value = value
        self._coded_value = coded_value

    def output(self, attrs=None, header='Set-Cookie:'):
        return '%s %s' % (header, self.OutputString(attrs))
    __str__ = output

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.OutputString())

    def js_output(self, attrs=None):
        import urllib.parse
        output_string = self.OutputString(attrs)
        if _has_control_character(output_string):
            raise Cookie错误('Control characters are not allowed in cookies')
        output_encoded = urllib.parse.quote(output_string, safe='', encoding='utf-8')
        return '\n        <script type="text/javascript">\n        <!-- begin hiding\n        document.cookie = decodeURIComponent("%s");\n        // end hiding -->\n        </script>\n        ' % (output_encoded,)

    def OutputString(self, attrs=None):
        result = []
        append = result.append
        append('%s=%s' % (self.key, self.coded_value))
        if attrs is None:
            attrs = self._reserved
        items = sorted(self.items())
        for key, value in items:
            if value == '':
                continue
            if key not in attrs:
                continue
            if key == 'expires' and isinstance(value, int):
                append('%s=%s' % (self._reserved[key], _getdate(value)))
            elif key == 'max-age' and isinstance(value, int):
                append('%s=%d' % (self._reserved[key], value))
            elif key == 'comment' and isinstance(value, str):
                append('%s=%s' % (self._reserved[key], _quote(value)))
            elif key in self._flags:
                if value:
                    append(str(self._reserved[key]))
            else:
                append('%s=%s' % (self._reserved[key], value))
        return _semispacejoin(result)
    __class_getitem__ = classmethod(types.GenericAlias)
_LegalKeyChars = "\\w\\d!#%&'~_`><@,:/\\$\\*\\+\\-\\.\\^\\|\\)\\(\\?\\}\\{\\="
_LegalValueChars = _LegalKeyChars + '\\[\\]'
_CookiePattern = re.compile("\n    \\s*                            # Optional whitespace at start of cookie\n    (?P<key>                       # Start of group 'key'\n    [" + _LegalKeyChars + ']+?   # Any word of at least one letter\n    )                              # End of group \'key\'\n    (                              # Optional group: there may not be a value.\n    \\s*=\\s*                          # Equal Sign\n    (?P<val>                         # Start of group \'val\'\n    "(?:[^\\\\"]|\\\\.)*"                  # Any double-quoted string\n    |                                  # or\n    # Special case for "expires" attr\n    (\\w{3,6}day|\\w{3}),\\s              # Day of the week or abbreviated day\n    [\\w\\d\\s-]{9,11}\\s[\\d:]{8}\\sGMT     # Date and time in specific format\n    |                                  # or\n    [' + _LegalValueChars + "]*      # Any word or empty string\n    )                                # End of group 'val'\n    )?                             # End of optional value group\n    \\s*                            # Any number of spaces.\n    (\\s+|;|$)                      # Ending either at space, semicolon, or EOS.\n    ", re.ASCII | re.VERBOSE)

class 基础Cookie(dict):
    """A container class for a set of Morsels."""

    def value_decode(self, val):
        """real_value, coded_value = value_decode(STRING)
        Called prior to setting a cookie's value from the network
        representation.  The VALUE is the value read from HTTP
        header.
        Override this function to modify the behavior of cookies.
        """
        return (val, val)

    def value_encode(self, val):
        """real_value, coded_value = value_encode(VALUE)
        Called prior to setting a cookie's value from the dictionary
        representation.  The VALUE is the value being assigned.
        Override this function to modify the behavior of cookies.
        """
        strval = str(val)
        return (strval, strval)

    def __init__(self, input=None):
        if input:
            self.load(input)

    def __set(self, key, real_value, coded_value):
        """Private method for setting a cookie's value"""
        M = self.get(key, Cookie项())
        M.set(key, real_value, coded_value)
        dict.__setitem__(self, key, M)

    def __setitem__(self, key, value):
        """Dictionary style assignment."""
        if isinstance(value, Cookie项):
            dict.__setitem__(self, key, value)
        else:
            rval, cval = self.value_encode(value)
            self.__set(key, rval, cval)

    def output(self, attrs=None, header='Set-Cookie:', sep='\r\n'):
        """Return a string suitable for HTTP."""
        result = []
        items = sorted(self.items())
        for key, value in items:
            value_output = value.output(attrs, header)
            if _has_control_character(value_output):
                raise Cookie错误('Control characters are not allowed in cookies')
            result.append(value_output)
        return sep.join(result)
    __str__ = output

    def __repr__(self):
        l = []
        items = sorted(self.items())
        for key, value in items:
            l.append('%s=%s' % (key, repr(value.value)))
        return '<%s: %s>' % (self.__class__.__name__, _spacejoin(l))

    def js_output(self, attrs=None):
        """Return a string suitable for JavaScript."""
        result = []
        items = sorted(self.items())
        for key, value in items:
            result.append(value.js_output(attrs))
        return _nulljoin(result)

    def load(self, rawdata):
        """Load cookies from a string (presumably HTTP_COOKIE) or
        from a dictionary.  Loading cookies from a dictionary 'd'
        is equivalent to calling:
            map(Cookie.__setitem__, d.keys(), d.values())
        """
        if isinstance(rawdata, str):
            self.__parse_string(rawdata)
        else:
            for key, value in rawdata.items():
                self[key] = value
        return

    def __parse_string(self, str, patt=_CookiePattern):
        i = 0
        n = len(str)
        parsed_items = []
        morsel_seen = False
        TYPE_ATTRIBUTE = 1
        TYPE_KEYVALUE = 2
        while 0 <= i < n:
            match = patt.match(str, i)
            if not match:
                break
            key, value = (match.group('key'), match.group('val'))
            i = match.end(0)
            if key[0] == '$':
                if not morsel_seen:
                    continue
                parsed_items.append((TYPE_ATTRIBUTE, key[1:], value))
            elif key.lower() in Cookie项._reserved:
                if not morsel_seen:
                    return
                if value is None:
                    if key.lower() in Cookie项._flags:
                        parsed_items.append((TYPE_ATTRIBUTE, key, True))
                    else:
                        return
                else:
                    parsed_items.append((TYPE_ATTRIBUTE, key, _unquote(value)))
            elif value is not None:
                parsed_items.append((TYPE_KEYVALUE, key, self.value_decode(value)))
                morsel_seen = True
            else:
                return
        M = None
        for tp, key, value in parsed_items:
            if tp == TYPE_ATTRIBUTE:
                assert M is not None
                M[key] = value
            else:
                assert tp == TYPE_KEYVALUE
                rval, cval = value
                self.__set(key, rval, cval)
                M = self[key]

class 简单Cookie(基础Cookie):
    """
    SimpleCookie supports strings as cookie values.  When setting
    the value using the dictionary assignment notation, SimpleCookie
    calls the builtin str() to convert the value to a string.  Values
    received from HTTP are kept as strings.
    """

    def value_decode(self, val):
        return (_unquote(val), val)

    def value_encode(self, val):
        strval = str(val)
        return (strval, _quote(strval))


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BaseCookie': '基础Cookie',
    'CookieError': 'Cookie错误',
    'Morsel': 'Cookie项',
    'SimpleCookie': '简单Cookie',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    'Cookie错误',
    '基础Cookie',
    '简单Cookie',
])

# ---- 转发层结束 ----
