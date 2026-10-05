# -*- coding: utf-8 -*-
"""电子邮件.消息 —— 汉语库（由 tools/汉化库.py 从 Lib/email/message.py 机械生成，**不要手改**）。

英文库 Lib/email.message.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


"""Basic message object for the email package object model."""
_英文原名表 = {'EmailMessage': '电子邮件消息', 'MIMEPart': 'MIME部分', 'Message': '邮件消息', 'walk': '遍历'}

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
__all__ = ['Message', 'EmailMessage']
import binascii
import re
import quopri
from io import BytesIO, StringIO
from 电子邮件 import 工具
from 电子邮件 import 错误
from 电子邮件._策略基类 import compat32
from 电子邮件 import 字符集 as _charset
from 电子邮件._编码词 import decode_b
Charset = _charset.Charset
SEMISPACE = '; '
tspecials = re.compile('[ \\(\\)<>@,;:\\\\"/\\[\\]\\?=]')

def _splitparam(param):
    a, sep, b = str(param).partition(';')
    if not sep:
        return (a.strip(), None)
    return (a.strip(), b.strip())

def _formatparam(param, value=None, quote=True):
    """Convenience function to format and return a key=value pair.

    This will quote the value if needed or if quote is true.  If value is a
    three tuple (charset, language, value), it will be encoded according
    to RFC2231 rules.  If it contains non-ascii characters it will likewise
    be encoded according to RFC2231 rules, using the utf-8 charset and
    a null language.
    """
    if value is not None and len(value) > 0:
        if isinstance(value, tuple):
            param += '*'
            value = 工具.encode_rfc2231(value[2], value[0], value[1])
            return '%s=%s' % (param, value)
        else:
            try:
                value.encode('ascii')
            except UnicodeEncodeError:
                param += '*'
                value = 工具.encode_rfc2231(value, 'utf-8', '')
                return '%s=%s' % (param, value)
        if quote or tspecials.search(value):
            return '%s="%s"' % (param, 工具.quote(value))
        else:
            return '%s=%s' % (param, value)
    else:
        return param

def _parseparam(s):
    s = ';' + str(s)
    plist = []
    start = 0
    while s.find(';', start) == start:
        start += 1
        end = s.find(';', start)
        ind, diff = (start, 0)
        while end > 0:
            diff += s.count('"', ind, end) - s.count('\\"', ind, end)
            if diff % 2 == 0:
                break
            end, ind = (ind, s.find(';', end + 1))
        if end < 0:
            end = len(s)
        i = s.find('=', start, end)
        if i == -1:
            f = s[start:end]
        else:
            f = s[start:i].rstrip().lower() + '=' + s[i + 1:end].lstrip()
        plist.append(f.strip())
        start = end
    return plist

def _unquotevalue(value):
    if isinstance(value, tuple):
        return (value[0], value[1], 工具.unquote(value[2]))
    else:
        return 工具.unquote(value)

def _decode_uu(encoded):
    """Decode uuencoded data."""
    decoded_lines = []
    encoded_lines_iter = iter(encoded.splitlines())
    for line in encoded_lines_iter:
        if line.startswith(b'begin '):
            mode, _, path = line.removeprefix(b'begin ').partition(b' ')
            try:
                int(mode, base=8)
            except ValueError:
                continue
            else:
                break
    else:
        raise ValueError('`begin` line not found')
    for line in encoded_lines_iter:
        if not line:
            raise ValueError('Truncated input')
        elif line.strip(b' \t\r\n\x0c') == b'end':
            break
        try:
            decoded_line = binascii.a2b_uu(line)
        except binascii.Error:
            nbytes = ((line[0] - 32 & 63) * 4 + 5) // 3
            decoded_line = binascii.a2b_uu(line[:nbytes])
        decoded_lines.append(decoded_line)
    return b''.join(decoded_lines)

class 邮件消息:
    """Basic message object.

    A message object is defined as something that has a bunch of RFC 5322
    headers and a payload.  It may optionally have an envelope header
    (a.k.a. Unix-From or From_ header).  If the message is a container (i.e. a
    multipart or a message/rfc822), then the payload is a list of Message
    objects, otherwise it is a string.

    Message objects implement part of the 'mapping' interface, which assumes
    there is exactly one occurrence of the header per message.  Some headers
    do in fact appear multiple times (e.g. Received) and for those headers,
    you must use the explicit API to set or get all the headers.  Not all of
    the mapping methods are implemented.
    """

    def __init__(self, policy=compat32):
        self.policy = policy
        self._headers = []
        self._unixfrom = None
        self._payload = None
        self._charset = None
        self.preamble = self.epilogue = None
        self.defects = []
        self._default_type = 'text/plain'

    def __str__(self):
        """Return the entire formatted message as a string.
        """
        return self.转字符串()

    def 转字符串(self, unixfrom=False, maxheaderlen=0, policy=None):
        """Return the entire formatted message as a string.

        Optional 'unixfrom', when true, means include the Unix From_ envelope
        header.  For backward compatibility reasons, if maxheaderlen is
        not specified it defaults to 0, so you must override it explicitly
        if you want a different maxheaderlen.  'policy' is passed to the
        Generator instance used to serialize the message; if it is not
        specified the policy associated with the message instance is used.

        If the message object contains binary data that is not encoded
        according to RFC standards, the non-compliant data will be replaced by
        unicode "unknown character" code points.
        """
        from 电子邮件.生成器 import Generator
        policy = self.policy if policy is None else policy
        fp = StringIO()
        g = Generator(fp, mangle_from_=False, maxheaderlen=maxheaderlen, policy=policy)
        g.flatten(self, unixfrom=unixfrom)
        return fp.getvalue()

    def __bytes__(self):
        """Return the entire formatted message as a bytes object.
        """
        return self.转字节()

    def 转字节(self, unixfrom=False, policy=None):
        """Return the entire formatted message as a bytes object.

        Optional 'unixfrom', when true, means include the Unix From_ envelope
        header.  'policy' is passed to the BytesGenerator instance used to
        serialize the message; if not specified the policy associated with
        the message instance is used.
        """
        from 电子邮件.生成器 import BytesGenerator
        policy = self.policy if policy is None else policy
        fp = BytesIO()
        g = BytesGenerator(fp, mangle_from_=False, policy=policy)
        g.flatten(self, unixfrom=unixfrom)
        return fp.getvalue()

    def 是多部分吗(self):
        """Return True if the message consists of multiple parts."""
        return isinstance(self._payload, list)

    def 设Unix信封头(self, unixfrom):
        self._unixfrom = unixfrom

    def 取Unix信封头(self):
        return self._unixfrom

    def 附加(self, payload):
        """Add the given payload to the current payload.

        The current payload will always be a list of objects after this method
        is called.  If you want to set the payload to a scalar object, use
        set_payload() instead.
        """
        if self._payload is None:
            self._payload = [payload]
        else:
            try:
                self._payload.append(payload)
            except AttributeError:
                raise TypeError('Attach is not valid on a message with a non-multipart payload')

    def 取载荷(self, i=None, decode=False):
        """Return a reference to the payload.

        The payload will either be a list object or a string.  If you mutate
        the list object, you modify the message's payload in place.  Optional
        i returns that index into the payload.

        Optional decode is a flag indicating whether the payload should be
        decoded or not, according to the Content-Transfer-Encoding header
        (default is False).

        When True and the message is not a multipart, the payload will be
        decoded if this header's value is `quoted-printable' or `base64'.  If
        some other encoding is used, or the header is missing, or if the
        payload has bogus data (i.e. bogus base64 or uuencoded data), the
        payload is returned as-is.

        If the message is a multipart and the decode flag is True, then None
        is returned.
        """
        if self.是多部分吗():
            if decode:
                return None
            if i is None:
                return self._payload
            else:
                return self._payload[i]
        if i is not None and (not isinstance(self._payload, list)):
            raise TypeError('Expected list, got %s' % type(self._payload))
        payload = self._payload
        cte = self.get('content-transfer-encoding', '')
        if hasattr(cte, 'cte'):
            cte = cte.cte
        else:
            cte = str(cte).strip().lower()
        if not decode:
            if isinstance(payload, str) and 工具._has_surrogates(payload):
                try:
                    bpayload = payload.encode('ascii', 'surrogateescape')
                    try:
                        payload = bpayload.decode(self.get_content_charset('ascii'), 'replace')
                    except LookupError:
                        payload = bpayload.decode('ascii', 'replace')
                except UnicodeEncodeError:
                    pass
            return payload
        if isinstance(payload, str):
            try:
                bpayload = payload.encode('ascii', 'surrogateescape')
            except UnicodeEncodeError:
                bpayload = payload.encode('raw-unicode-escape')
        else:
            bpayload = payload
        if cte == 'quoted-printable':
            return quopri.decodestring(bpayload)
        elif cte == 'base64':
            value, defects = decode_b(b''.join(bpayload.splitlines()))
            for defect in defects:
                self.policy.handle_defect(self, defect)
            return value
        elif cte in ('x-uuencode', 'uuencode', 'uue', 'x-uue'):
            try:
                return _decode_uu(bpayload)
            except ValueError:
                return bpayload
        if isinstance(payload, str):
            return bpayload
        return payload

    def 设载荷(self, payload, charset=None):
        """Set the payload to the given value.

        Optional charset sets the message's default character set.  See
        set_charset() for details.
        """
        if hasattr(payload, 'encode'):
            if charset is None:
                self._payload = payload
                return
            if not isinstance(charset, Charset):
                charset = Charset(charset)
            payload = payload.encode(charset.output_charset, 'surrogateescape')
        if hasattr(payload, 'decode'):
            self._payload = payload.decode('ascii', 'surrogateescape')
        else:
            self._payload = payload
        if charset is not None:
            self.设字符集(charset)

    def 设字符集(self, charset):
        """Set the charset of the payload to a given character set.

        charset can be a Charset instance, a string naming a character set, or
        None.  If it is a string it will be converted to a Charset instance.
        If charset is None, the charset parameter will be removed from the
        Content-Type field.  Anything else will generate a TypeError.

        The message will be assumed to be of type text/* encoded with
        charset.input_charset.  It will be converted to charset.output_charset
        and encoded properly, if needed, when generating the plain text
        representation of the message.  MIME headers (MIME-Version,
        Content-Type, Content-Transfer-Encoding) will be added as needed.
        """
        if charset is None:
            self.删参数('charset')
            self._charset = None
            return
        if not isinstance(charset, Charset):
            charset = Charset(charset)
        self._charset = charset
        if 'MIME-Version' not in self:
            self.加邮件头('MIME-Version', '1.0')
        if 'Content-Type' not in self:
            self.加邮件头('Content-Type', 'text/plain', charset=charset.get_output_charset())
        else:
            self.设参数('charset', charset.get_output_charset())
        if charset != charset.get_output_charset():
            self._payload = charset.body_encode(self._payload)
        if 'Content-Transfer-Encoding' not in self:
            cte = charset.get_body_encoding()
            try:
                cte(self)
            except TypeError:
                payload = self._payload
                if payload:
                    try:
                        payload = payload.encode('ascii', 'surrogateescape')
                    except UnicodeError:
                        payload = payload.encode(charset.output_charset)
                self._payload = charset.body_encode(payload)
                self.加邮件头('Content-Transfer-Encoding', cte)

    def 取字符集(self):
        """Return the Charset instance associated with the message's payload.
        """
        return self._charset

    def __len__(self):
        """Return the total number of headers, including duplicates."""
        return len(self._headers)

    def __getitem__(self, name):
        """Get a header value.

        Return None if the header is missing instead of raising an exception.

        Note that if the header appeared multiple times, exactly which
        occurrence gets returned is undefined.  Use get_all() to get all
        the values matching a header field name.
        """
        return self.get(name)

    def __setitem__(self, name, val):
        """Set the value of a header.

        Note: this does not overwrite an existing header with the same field
        name.  Use __delitem__() first to delete any existing headers.
        """
        max_count = self.policy.header_max_count(name)
        if max_count:
            lname = name.lower()
            found = 0
            for k, v in self._headers:
                if k.lower() == lname:
                    found += 1
                    if found >= max_count:
                        raise ValueError('There may be at most {} {} headers in a message'.format(max_count, name))
        self._headers.append(self.policy.header_store_parse(name, val))

    def __delitem__(self, name):
        """Delete all occurrences of a header, if present.

        Does not raise an exception if the header is missing.
        """
        name = name.lower()
        newheaders = []
        for k, v in self._headers:
            if k.lower() != name:
                newheaders.append((k, v))
        self._headers = newheaders

    def __contains__(self, name):
        name_lower = name.lower()
        for k, v in self._headers:
            if name_lower == k.lower():
                return True
        return False

    def __iter__(self):
        for field, value in self._headers:
            yield field

    def keys(self):
        """Return a list of all the message's header field names.

        These will be sorted in the order they appeared in the original
        message, or were added to the message, and may contain duplicates.
        Any fields deleted and re-inserted are always appended to the header
        list.
        """
        return [k for k, v in self._headers]

    def values(self):
        """Return a list of all the message's header values.

        These will be sorted in the order they appeared in the original
        message, or were added to the message, and may contain duplicates.
        Any fields deleted and re-inserted are always appended to the header
        list.
        """
        return [self.policy.header_fetch_parse(k, v) for k, v in self._headers]

    def items(self):
        """Get all the message's header fields and values.

        These will be sorted in the order they appeared in the original
        message, or were added to the message, and may contain duplicates.
        Any fields deleted and re-inserted are always appended to the header
        list.
        """
        return [(k, self.policy.header_fetch_parse(k, v)) for k, v in self._headers]

    def get(self, name, failobj=None):
        """Get a header value.

        Like __getitem__() but return failobj instead of None when the field
        is missing.
        """
        name = name.lower()
        for k, v in self._headers:
            if k.lower() == name:
                return self.policy.header_fetch_parse(k, v)
        return failobj

    def 设原始内容(self, name, value):
        """Store name and value in the model without modification.

        This is an "internal" API, intended only for use by a parser.
        """
        self._headers.append((name, value))

    def 原始项(self):
        """Return the (name, value) header pairs without modification.

        This is an "internal" API, intended only for use by a generator.
        """
        return iter(self._headers.copy())

    def 取全部(self, name, failobj=None):
        """Return a list of all the values for the named field.

        These will be sorted in the order they appeared in the original
        message, and may contain duplicates.  Any fields deleted and
        re-inserted are always appended to the header list.

        If no such fields exist, failobj is returned (defaults to None).
        """
        values = []
        name = name.lower()
        for k, v in self._headers:
            if k.lower() == name:
                values.append(self.policy.header_fetch_parse(k, v))
        if not values:
            return failobj
        return values

    def 加邮件头(self, _name, _value, **_params):
        """Extended header setting.

        name is the header field to add.  keyword arguments can be used to set
        additional parameters for the header field, with underscores converted
        to dashes.  Normally the parameter will be added as key="value" unless
        value is None, in which case only the key will be added.  If a
        parameter value contains non-ASCII characters it can be specified as a
        three-tuple of (charset, language, value), in which case it will be
        encoded according to RFC2231 rules.  Otherwise it will be encoded using
        the utf-8 charset and a language of ''.

        Examples:

        msg.add_header('content-disposition', 'attachment', filename='bud.gif')
        msg.add_header('content-disposition', 'attachment',
                       filename=('utf-8', '', 'Fußballer.ppt'))
        msg.add_header('content-disposition', 'attachment',
                       filename='Fußballer.ppt'))
        """
        parts = []
        for k, v in _params.items():
            if v is None:
                parts.append(k.replace('_', '-'))
            else:
                parts.append(_formatparam(k.replace('_', '-'), v))
        if _value is not None:
            parts.insert(0, _value)
        self[_name] = SEMISPACE.join(parts)

    def 换邮件头(self, _name, _value):
        """Replace a header.

        Replace the first matching header found in the message, retaining
        header order and case.  If no matching header was found, a KeyError is
        raised.
        """
        _name = _name.lower()
        for i, (k, v) in zip(range(len(self._headers)), self._headers):
            if k.lower() == _name:
                self._headers[i] = self.policy.header_store_parse(k, _value)
                break
        else:
            raise KeyError(_name)

    def 取内容类型(self):
        """Return the message's content type.

        The returned string is coerced to lower case of the form
        'maintype/subtype'.  If there was no Content-Type header in the
        message, the default type as given by get_default_type() will be
        returned.  Since according to RFC 2045, messages always have a default
        type this will always return a value.

        RFC 2045 defines a message's default type to be text/plain unless it
        appears inside a multipart/digest container, in which case it would be
        message/rfc822.
        """
        missing = object()
        value = self.get('content-type', missing)
        if value is missing:
            return self.get_default_type()
        ctype = _splitparam(value)[0].lower()
        if ctype.count('/') != 1:
            return 'text/plain'
        return ctype

    def 取内容主类型(self):
        """Return the message's main content type.

        This is the 'maintype' part of the string returned by
        get_content_type().
        """
        ctype = self.取内容类型()
        return ctype.split('/')[0]

    def 取内容子类型(self):
        """Returns the message's sub-content type.

        This is the 'subtype' part of the string returned by
        get_content_type().
        """
        ctype = self.取内容类型()
        return ctype.split('/')[1]

    def get_default_type(self):
        """Return the 'default' content type.

        Most messages have a default content type of text/plain, except for
        messages that are subparts of multipart/digest containers.  Such
        subparts have a default content type of message/rfc822.
        """
        return self._default_type

    def set_default_type(self, ctype):
        """Set the 'default' content type.

        ctype should be either "text/plain" or "message/rfc822", although this
        is not enforced.  The default content type is not stored in the
        Content-Type header.
        """
        self._default_type = ctype

    def _get_params_preserve(self, failobj, header):
        missing = object()
        value = self.get(header, missing)
        if value is missing:
            return failobj
        params = []
        for p in _parseparam(value):
            try:
                name, val = p.split('=', 1)
                name = name.strip()
                val = val.strip()
            except ValueError:
                name = p.strip()
                val = ''
            params.append((name, val))
        params = 工具.decode_params(params)
        return params

    def 取参数们(self, failobj=None, header='content-type', unquote=True):
        """Return the message's Content-Type parameters, as a list.

        The elements of the returned list are 2-tuples of key/value pairs, as
        split on the '=' sign.  The left hand side of the '=' is the key,
        while the right hand side is the value.  If there is no '=' sign in
        the parameter the value is the empty string.  The value is as
        described in the get_param() method.

        Optional failobj is the object to return if there is no Content-Type
        header.  Optional header is the header to search instead of
        Content-Type.  If unquote is True, the value is unquoted.
        """
        missing = object()
        params = self._get_params_preserve(missing, header)
        if params is missing:
            return failobj
        if unquote:
            return [(k, _unquotevalue(v)) for k, v in params]
        else:
            return params

    def 取参数(self, param, failobj=None, header='content-type', unquote=True):
        """Return the parameter value if found in the Content-Type header.

        Optional failobj is the object to return if there is no Content-Type
        header, or the Content-Type header has no such parameter.  Optional
        header is the header to search instead of Content-Type.

        Parameter keys are always compared case insensitively.  The return
        value can either be a string, or a 3-tuple if the parameter was RFC
        2231 encoded.  When it's a 3-tuple, the elements of the value are of
        the form (CHARSET, LANGUAGE, VALUE).  Note that both CHARSET and
        LANGUAGE can be None, in which case you should consider VALUE to be
        encoded in the us-ascii charset.  You can usually ignore LANGUAGE.
        The parameter value (either the returned string, or the VALUE item in
        the 3-tuple) is always unquoted, unless unquote is set to False.

        If your application doesn't care whether the parameter was RFC 2231
        encoded, it can turn the return value into a string as follows:

            rawparam = msg.get_param('foo')
            param = email.utils.collapse_rfc2231_value(rawparam)

        """
        if header not in self:
            return failobj
        for k, v in self._get_params_preserve(failobj, header):
            if k.lower() == param.lower():
                if unquote:
                    return _unquotevalue(v)
                else:
                    return v
        return failobj

    def 设参数(self, param, value, header='Content-Type', requote=True, charset=None, language='', replace=False):
        """Set a parameter in the Content-Type header.

        If the parameter already exists in the header, its value will be
        replaced with the new value.

        If header is Content-Type and has not yet been defined for this
        message, it will be set to "text/plain" and the new parameter and
        value will be appended as per RFC 2045.

        An alternate header can be specified in the header argument, and all
        parameters will be quoted as necessary unless requote is False.

        If charset is specified, the parameter will be encoded according to RFC
        2231.  Optional language specifies the RFC 2231 language, defaulting
        to the empty string.  Both charset and language should be strings.
        """
        if not isinstance(value, tuple) and charset:
            value = (charset, language, value)
        if header not in self and header.lower() == 'content-type':
            ctype = 'text/plain'
        else:
            ctype = self.get(header)
        if not self.取参数(param, header=header):
            if not ctype:
                ctype = _formatparam(param, value, requote)
            else:
                ctype = SEMISPACE.join([ctype, _formatparam(param, value, requote)])
        else:
            ctype = ''
            for old_param, old_value in self.取参数们(header=header, unquote=requote):
                append_param = ''
                if old_param.lower() == param.lower():
                    append_param = _formatparam(param, value, requote)
                else:
                    append_param = _formatparam(old_param, old_value, requote)
                if not ctype:
                    ctype = append_param
                else:
                    ctype = SEMISPACE.join([ctype, append_param])
        if ctype != self.get(header):
            if replace:
                self.换邮件头(header, ctype)
            else:
                del self[header]
                self[header] = ctype

    def 删参数(self, param, header='content-type', requote=True):
        """Remove the given parameter completely from the Content-Type header.

        The header will be re-written in place without the parameter or its
        value. All values will be quoted as necessary unless requote is
        False.  Optional header specifies an alternative to the Content-Type
        header.
        """
        if header not in self:
            return
        new_ctype = ''
        for p, v in self.取参数们(header=header, unquote=requote):
            if p.lower() != param.lower():
                if not new_ctype:
                    new_ctype = _formatparam(p, v, requote)
                else:
                    new_ctype = SEMISPACE.join([new_ctype, _formatparam(p, v, requote)])
        if new_ctype != self.get(header):
            del self[header]
            self[header] = new_ctype

    def 设类型(self, type, header='Content-Type', requote=True):
        """Set the main type and subtype for the Content-Type header.

        type must be a string in the form "maintype/subtype", otherwise a
        ValueError is raised.

        This method replaces the Content-Type header, keeping all the
        parameters in place.  If requote is False, this leaves the existing
        header's quoting as is.  Otherwise, the parameters will be quoted (the
        default).

        An alternative header can be specified in the header argument.  When
        the Content-Type header is set, we'll always also add a MIME-Version
        header.
        """
        if not type.count('/') == 1:
            raise ValueError
        if header.lower() == 'content-type':
            del self['mime-version']
            self['MIME-Version'] = '1.0'
        if header not in self:
            self[header] = type
            return
        params = self.取参数们(header=header, unquote=requote)
        del self[header]
        self[header] = type
        for p, v in params[1:]:
            self.设参数(p, v, header, requote)

    def 取文件名(self, failobj=None):
        """Return the filename associated with the payload if present.

        The filename is extracted from the Content-Disposition header's
        'filename' parameter, and it is unquoted.  If that header is missing
        the 'filename' parameter, this method falls back to looking for the
        'name' parameter.
        """
        missing = object()
        filename = self.取参数('filename', missing, 'content-disposition')
        if filename is missing:
            filename = self.取参数('name', missing, 'content-type')
        if filename is missing:
            return failobj
        return 工具.collapse_rfc2231_value(filename).strip()

    def 取边界(self, failobj=None):
        """Return the boundary associated with the payload if present.

        The boundary is extracted from the Content-Type header's 'boundary'
        parameter, and it is unquoted.
        """
        missing = object()
        boundary = self.取参数('boundary', missing)
        if boundary is missing:
            return failobj
        return 工具.collapse_rfc2231_value(boundary).rstrip()

    def 设边界(self, boundary):
        """Set the boundary parameter in Content-Type to 'boundary'.

        This is subtly different than deleting the Content-Type header and
        adding a new one with a new boundary parameter via add_header().  The
        main difference is that using the set_boundary() method preserves the
        order of the Content-Type header in the original message.

        HeaderParseError is raised if the message has no Content-Type header.
        """
        missing = object()
        params = self._get_params_preserve(missing, 'content-type')
        if params is missing:
            raise 错误.HeaderParseError('No Content-Type header found')
        newparams = []
        foundp = False
        for pk, pv in params:
            if pk.lower() == 'boundary':
                newparams.append(('boundary', '"%s"' % boundary))
                foundp = True
            else:
                newparams.append((pk, pv))
        if not foundp:
            newparams.append(('boundary', '"%s"' % boundary))
        newheaders = []
        for h, v in self._headers:
            if h.lower() == 'content-type':
                parts = []
                for k, v in newparams:
                    if v == '':
                        parts.append(k)
                    else:
                        parts.append('%s=%s' % (k, v))
                val = SEMISPACE.join(parts)
                newheaders.append(self.policy.header_store_parse(h, val))
            else:
                newheaders.append((h, v))
        self._headers = newheaders

    def get_content_charset(self, failobj=None):
        """Return the charset parameter of the Content-Type header.

        The returned string is always coerced to lower case.  If there is no
        Content-Type header, or if that header has no charset parameter,
        failobj is returned.
        """
        missing = object()
        字符集 = self.取参数('charset', missing)
        if 字符集 is missing:
            return failobj
        if isinstance(字符集, tuple):
            pcharset = 字符集[0] or 'us-ascii'
            try:
                转字节 = 字符集[2].encode('raw-unicode-escape')
                字符集 = str(转字节, pcharset)
            except (LookupError, UnicodeError):
                字符集 = 字符集[2]
        try:
            字符集.encode('us-ascii')
        except UnicodeError:
            return failobj
        return 字符集.lower()

    def get_charsets(self, failobj=None):
        """Return a list containing the charset(s) used in this message.

        The returned list of items describes the Content-Type headers'
        charset parameter for this message and all the subparts in its
        payload.

        Each item will either be a string (the value of the charset parameter
        in the Content-Type header of that part) or the value of the
        'failobj' parameter (defaults to None), if the part does not have a
        main MIME type of "text", or the charset is not defined.

        The list will contain one string for each part of the message, plus
        one for the container message (i.e. self), so that a non-multipart
        message will still return a list of length 1.
        """
        return [part.get_content_charset(failobj) for part in self.遍历()]

    def get_content_disposition(self):
        """Return the message's content-disposition if it exists, or None.

        The return values can be either 'inline', 'attachment' or None
        according to the rfc2183.
        """
        value = self.get('content-disposition')
        if value is None:
            return None
        c_d = _splitparam(value)[0].lower()
        return c_d
    from 电子邮件.迭代器 import 遍历
_装类转发(邮件消息, {'add_header': '加邮件头', 'as_bytes': '转字节', 'as_string': '转字符串', 'attach': '附加', 'del_param': '删参数', 'get_all': '取全部', 'get_boundary': '取边界', 'get_charset': '取字符集', 'get_content_maintype': '取内容主类型', 'get_content_subtype': '取内容子类型', 'get_content_type': '取内容类型', 'get_filename': '取文件名', 'get_param': '取参数', 'get_params': '取参数们', 'get_payload': '取载荷', 'get_unixfrom': '取Unix信封头', 'is_multipart': '是多部分吗', 'raw_items': '原始项', 'replace_header': '换邮件头', 'set_boundary': '设边界', 'set_charset': '设字符集', 'set_param': '设参数', 'set_payload': '设载荷', 'set_raw': '设原始内容', 'set_type': '设类型', 'set_unixfrom': '设Unix信封头'}, {'add_header': '加邮件头', 'as_bytes': '转字节', 'as_string': '转字符串', 'attach': '附加', 'del_param': '删参数', 'get_all': '取全部', 'get_boundary': '取边界', 'get_charset': '取字符集', 'get_content_maintype': '取内容主类型', 'get_content_subtype': '取内容子类型', 'get_content_type': '取内容类型', 'get_filename': '取文件名', 'get_param': '取参数', 'get_params': '取参数们', 'get_payload': '取载荷', 'get_unixfrom': '取Unix信封头', 'is_multipart': '是多部分吗', 'raw_items': '原始项', 'replace_header': '换邮件头', 'set_boundary': '设边界', 'set_charset': '设字符集', 'set_param': '设参数', 'set_payload': '设载荷', 'set_raw': '设原始内容', 'set_type': '设类型', 'set_unixfrom': '设Unix信封头', 'walk': '遍历'})

class MIME部分(邮件消息):

    def __init__(self, policy=None):
        if policy is None:
            from 电子邮件.策略 import default
            policy = default
        super().__init__(policy)

    def 转字符串(self, unixfrom=False, maxheaderlen=None, policy=None):
        """Return the entire formatted message as a string.

        Optional 'unixfrom', when true, means include the Unix From_ envelope
        header.  maxheaderlen is retained for backward compatibility with the
        base Message class, but defaults to None, meaning that the policy value
        for max_line_length controls the header maximum length.  'policy' is
        passed to the Generator instance used to serialize the message; if it
        is not specified the policy associated with the message instance is
        used.
        """
        policy = self.policy if policy is None else policy
        if maxheaderlen is None:
            maxheaderlen = policy.max_line_length
        return super().as_string(unixfrom, maxheaderlen, policy)

    def __str__(self):
        return self.转字符串(policy=self.policy.clone(utf8=True))

    def 是附件吗(self):
        c_d = self.get('content-disposition')
        return False if c_d is None else c_d.content_disposition == 'attachment'

    def _find_body(self, part, preferencelist):
        if part.is_attachment():
            return
        maintype, subtype = part.get_content_type().split('/')
        if maintype == 'text':
            if subtype in preferencelist:
                yield (preferencelist.index(subtype), part)
            return
        if maintype != 'multipart' or not self.是多部分吗():
            return
        if subtype != 'related':
            for subpart in part.iter_parts():
                yield from self._find_body(subpart, preferencelist)
            return
        if 'related' in preferencelist:
            yield (preferencelist.index('related'), part)
        candidate = None
        start = part.get_param('start')
        if start:
            for subpart in part.iter_parts():
                if subpart['content-id'] == start:
                    candidate = subpart
                    break
        if candidate is None:
            subparts = part.get_payload()
            candidate = subparts[0] if subparts else None
        if candidate is not None:
            yield from self._find_body(candidate, preferencelist)

    def 取正文(self, preferencelist=('related', 'html', 'plain')):
        """Return best candidate mime part for display as 'body' of message.

        Do a depth first search, starting with self, looking for the first part
        matching each of the items in preferencelist, and return the part
        corresponding to the first item that has a match, or None if no items
        have a match.  If 'related' is not included in preferencelist, consider
        the root part of any multipart/related encountered as a candidate
        match.  Ignore parts with 'Content-Disposition: attachment'.
        """
        best_prio = len(preferencelist)
        body = None
        for prio, part in self._find_body(self, preferencelist):
            if prio < best_prio:
                best_prio = prio
                body = part
                if prio == 0:
                    break
        return body
    _body_types = {('text', 'plain'), ('text', 'html'), ('multipart', 'related'), ('multipart', 'alternative')}

    def 迭代附件(self):
        """Return an iterator over the non-main parts of a multipart.

        Skip the first of each occurrence of text/plain, text/html,
        multipart/related, or multipart/alternative in the multipart (unless
        they have a 'Content-Disposition: attachment' header) and include all
        remaining subparts in the returned iterator.  When applied to a
        multipart/related, return all parts except the root part.  Return an
        empty iterator when applied to a multipart/alternative or a
        non-multipart.
        """
        maintype, subtype = self.取内容类型().split('/')
        if maintype != 'multipart' or subtype == 'alternative':
            return
        payload = self.取载荷()
        try:
            parts = payload.copy()
        except AttributeError:
            return
        if maintype == 'multipart' and subtype == 'related':
            start = self.取参数('start')
            if start:
                found = False
                attachments = []
                for part in parts:
                    if part.get('content-id') == start:
                        found = True
                    else:
                        attachments.append(part)
                if found:
                    yield from attachments
                    return
            parts.pop(0)
            yield from parts
            return
        seen = []
        for part in parts:
            maintype, subtype = part.get_content_type().split('/')
            if (maintype, subtype) in self._body_types and (not part.is_attachment()) and (subtype not in seen):
                seen.append(subtype)
                continue
            yield part

    def 迭代部分(self):
        """Return an iterator over all immediate subparts of a multipart.

        Return an empty iterator for a non-multipart.
        """
        if self.是多部分吗():
            yield from self.取载荷()

    def 取内容(self, *args, content_manager=None, **kw):
        if content_manager is None:
            content_manager = self.policy.content_manager
        return content_manager.get_content(self, *args, **kw)

    def 设内容(self, *args, content_manager=None, **kw):
        if content_manager is None:
            content_manager = self.policy.content_manager
        content_manager.set_content(self, *args, **kw)

    def _make_multipart(self, subtype, disallowed_subtypes, boundary):
        if self.取内容主类型() == 'multipart':
            existing_subtype = self.取内容子类型()
            disallowed_subtypes = disallowed_subtypes + (subtype,)
            if existing_subtype in disallowed_subtypes:
                raise ValueError('Cannot convert {} to {}'.format(existing_subtype, subtype))
        keep_headers = []
        part_headers = []
        for name, value in self._headers:
            if name.lower().startswith('content-'):
                part_headers.append((name, value))
            else:
                keep_headers.append((name, value))
        if part_headers:
            part = type(self)(policy=self.policy)
            part._headers = part_headers
            part._payload = self._payload
            self._payload = [part]
        else:
            self._payload = []
        self._headers = keep_headers
        self['Content-Type'] = 'multipart/' + subtype
        if boundary is not None:
            self.设参数('boundary', boundary)

    def 变为内嵌资源(self, boundary=None):
        self._make_multipart('related', ('alternative', 'mixed'), boundary)

    def 变为替代版本(self, boundary=None):
        self._make_multipart('alternative', ('mixed',), boundary)

    def 变为混合(self, boundary=None):
        self._make_multipart('mixed', (), boundary)

    def _add_multipart(self, _subtype, *args, _disp=None, **kw):
        if self.取内容主类型() != 'multipart' or self.取内容子类型() != _subtype:
            getattr(self, 'make_' + _subtype)()
        part = type(self)(policy=self.policy)
        part.set_content(*args, **kw)
        if _disp and 'content-disposition' not in part:
            part['Content-Disposition'] = _disp
        self.附加(part)

    def 加内嵌资源(self, *args, **kw):
        self._add_multipart('related', *args, _disp='inline', **kw)

    def 加替代版本(self, *args, **kw):
        self._add_multipart('alternative', *args, **kw)

    def 加附件(self, *args, **kw):
        self._add_multipart('mixed', *args, _disp='attachment', **kw)

    def clear(self):
        self._headers = []
        self._payload = None

    def clear_content(self):
        self._headers = [(n, v) for n, v in self._headers if not n.lower().startswith('content-')]
        self._payload = None
_装类转发(MIME部分, {'add_alternative': '加替代版本', 'add_attachment': '加附件', 'add_related': '加内嵌资源', 'as_string': '转字符串', 'get_body': '取正文', 'get_content': '取内容', 'is_attachment': '是附件吗', 'iter_attachments': '迭代附件', 'iter_parts': '迭代部分', 'make_alternative': '变为替代版本', 'make_mixed': '变为混合', 'make_related': '变为内嵌资源', 'set_content': '设内容'}, {'add_alternative': '加替代版本', 'add_attachment': '加附件', 'add_related': '加内嵌资源', 'as_string': '转字符串', 'attach': '附加', 'get_body': '取正文', 'get_content': '取内容', 'get_content_maintype': '取内容主类型', 'get_content_subtype': '取内容子类型', 'get_content_type': '取内容类型', 'get_param': '取参数', 'get_payload': '取载荷', 'is_attachment': '是附件吗', 'is_multipart': '是多部分吗', 'iter_attachments': '迭代附件', 'iter_parts': '迭代部分', 'make_alternative': '变为替代版本', 'make_mixed': '变为混合', 'make_related': '变为内嵌资源', 'set_content': '设内容', 'set_param': '设参数'})

class 电子邮件消息(MIME部分):

    def 设内容(self, *args, **kw):
        super().set_content(*args, **kw)
        if 'MIME-Version' not in self:
            self['MIME-Version'] = '1.0'
_装类转发(电子邮件消息, {'set_content': '设内容'}, {'set_content': '设内容'})


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'EmailMessage': '电子邮件消息',
    'MIMEPart': 'MIME部分',
    'Message': '邮件消息',
    'walk': '遍历',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'MIME部分': {
        'add_alternative': '加替代版本',
        'add_attachment': '加附件',
        'add_related': '加内嵌资源',
        'as_string': '转字符串',
        'get_body': '取正文',
        'get_content': '取内容',
        'is_attachment': '是附件吗',
        'iter_attachments': '迭代附件',
        'iter_parts': '迭代部分',
        'make_alternative': '变为替代版本',
        'make_mixed': '变为混合',
        'make_related': '变为内嵌资源',
        'set_content': '设内容',
    },
    '电子邮件消息': {
        'set_content': '设内容',
    },
    '邮件消息': {
        'add_header': '加邮件头',
        'as_bytes': '转字节',
        'as_string': '转字符串',
        'attach': '附加',
        'del_param': '删参数',
        'get_all': '取全部',
        'get_boundary': '取边界',
        'get_charset': '取字符集',
        'get_content_maintype': '取内容主类型',
        'get_content_subtype': '取内容子类型',
        'get_content_type': '取内容类型',
        'get_filename': '取文件名',
        'get_param': '取参数',
        'get_params': '取参数们',
        'get_payload': '取载荷',
        'get_unixfrom': '取Unix信封头',
        'is_multipart': '是多部分吗',
        'raw_items': '原始项',
        'replace_header': '换邮件头',
        'set_boundary': '设边界',
        'set_charset': '设字符集',
        'set_param': '设参数',
        'set_payload': '设载荷',
        'set_raw': '设原始内容',
        'set_type': '设类型',
        'set_unixfrom': '设Unix信封头',
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
    'MIME部分': {
        'add_alternative': '加替代版本',
        'add_attachment': '加附件',
        'add_related': '加内嵌资源',
        'as_string': '转字符串',
        'attach': '附加',
        'get_body': '取正文',
        'get_content': '取内容',
        'get_content_maintype': '取内容主类型',
        'get_content_subtype': '取内容子类型',
        'get_content_type': '取内容类型',
        'get_param': '取参数',
        'get_payload': '取载荷',
        'is_attachment': '是附件吗',
        'is_multipart': '是多部分吗',
        'iter_attachments': '迭代附件',
        'iter_parts': '迭代部分',
        'make_alternative': '变为替代版本',
        'make_mixed': '变为混合',
        'make_related': '变为内嵌资源',
        'set_content': '设内容',
        'set_param': '设参数',
    },
    '电子邮件消息': {
        'set_content': '设内容',
    },
    '邮件消息': {
        'add_header': '加邮件头',
        'as_bytes': '转字节',
        'as_string': '转字符串',
        'attach': '附加',
        'del_param': '删参数',
        'get_all': '取全部',
        'get_boundary': '取边界',
        'get_charset': '取字符集',
        'get_content_maintype': '取内容主类型',
        'get_content_subtype': '取内容子类型',
        'get_content_type': '取内容类型',
        'get_filename': '取文件名',
        'get_param': '取参数',
        'get_params': '取参数们',
        'get_payload': '取载荷',
        'get_unixfrom': '取Unix信封头',
        'is_multipart': '是多部分吗',
        'raw_items': '原始项',
        'replace_header': '换邮件头',
        'set_boundary': '设边界',
        'set_charset': '设字符集',
        'set_param': '设参数',
        'set_payload': '设载荷',
        'set_raw': '设原始内容',
        'set_type': '设类型',
        'set_unixfrom': '设Unix信封头',
        'walk': '遍历',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '电子邮件消息',
    '邮件消息',
]

# ---- 转发层结束 ----
