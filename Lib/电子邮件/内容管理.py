# -*- coding: utf-8 -*-
"""电子邮件.内容管理 —— 汉语库（由 tools/汉化库.py 从 Lib/email/contentmanager.py 机械生成，**不要手改**）。

英文库 Lib/email.contentmanager.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


_英文原名表 = {'ContentManager': '内容管理器', 'get_message_content': '取消息内容', 'get_non_text_content': '取非文本内容', 'get_text_content': '取文本内容', 'raw_data_manager': '原始数据管理器', 'set_bytes_content': '设字节内容', 'set_message_content': '设消息内容', 'set_text_content': '设文本内容'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import binascii
import 电子邮件.字符集
import 电子邮件.消息
import 电子邮件.错误
import sys
from 电子邮件 import 可打印编码

class 内容管理器:

    def __init__(self):
        self.get_handlers = {}
        self.set_handlers = {}

    def add_get_handler(self, key, handler):
        self.get_handlers[key] = handler

    def get_content(self, msg, *args, **kw):
        content_type = msg.get_content_type()
        if content_type in self.get_handlers:
            return self.get_handlers[content_type](msg, *args, **kw)
        maintype = msg.get_content_maintype()
        if maintype in self.get_handlers:
            return self.get_handlers[maintype](msg, *args, **kw)
        if '' in self.get_handlers:
            return self.get_handlers[''](msg, *args, **kw)
        raise KeyError(content_type)

    def add_set_handler(self, typekey, handler):
        self.set_handlers[typekey] = handler

    def set_content(self, msg, obj, *args, **kw):
        if msg.get_content_maintype() == 'multipart':
            raise TypeError('set_content not valid on multipart')
        handler = self._find_set_handler(msg, obj)
        msg.clear_content()
        handler(msg, obj, *args, **kw)

    def _find_set_handler(self, msg, obj):
        full_path_for_error = None
        for typ in type(obj).__mro__:
            if typ in self.set_handlers:
                return self.set_handlers[typ]
            qname = typ.__qualname__
            modname = getattr(typ, '__module__', '')
            full_path = '.'.join((modname, qname)) if modname else qname
            if full_path_for_error is None:
                full_path_for_error = full_path
            if full_path in self.set_handlers:
                return self.set_handlers[full_path]
            if qname in self.set_handlers:
                return self.set_handlers[qname]
            name = typ.__name__
            if name in self.set_handlers:
                return self.set_handlers[name]
        if None in self.set_handlers:
            return self.set_handlers[None]
        raise KeyError(full_path_for_error)
原始数据管理器 = 内容管理器()

def 取文本内容(msg, errors='replace'):
    content = msg.get_payload(decode=True)
    字符集 = msg.get_param('charset', 'ASCII')
    return content.decode(字符集, errors=errors)
原始数据管理器.add_get_handler('text', 取文本内容)

def 取非文本内容(msg):
    return msg.get_payload(decode=True)
for maintype in 'audio image video application'.split():
    原始数据管理器.add_get_handler(maintype, 取非文本内容)
del maintype

def 取消息内容(msg):
    return msg.get_payload(0)
for subtype in 'rfc822 external-body'.split():
    原始数据管理器.add_get_handler('message/' + subtype, 取消息内容)
del subtype

def get_and_fixup_unknown_message_content(msg):
    return bytes(msg.get_payload(0))
原始数据管理器.add_get_handler('message', get_and_fixup_unknown_message_content)

def _prepare_set(msg, maintype, subtype, headers):
    msg['Content-Type'] = '/'.join((maintype, subtype))
    if headers:
        if not hasattr(headers[0], 'name'):
            mp = msg.policy
            headers = [mp.header_factory(*mp.header_source_parse([邮件头])) for 邮件头 in headers]
        try:
            for 邮件头 in headers:
                if 邮件头.defects:
                    raise 邮件头.defects[0]
                msg[邮件头.name] = 邮件头
        except 电子邮件.错误.HeaderDefect as exc:
            raise ValueError('Invalid header: {}'.format(邮件头.fold(policy=msg.policy))) from exc

def _finalize_set(msg, disposition, filename, cid, params):
    if disposition is None and filename is not None:
        disposition = 'attachment'
    if disposition is not None:
        msg['Content-Disposition'] = disposition
    if filename is not None:
        msg.set_param('filename', filename, header='Content-Disposition', replace=True)
    if cid is not None:
        msg['Content-ID'] = cid
    if params is not None:
        for key, value in params.items():
            msg.set_param(key, value)

def _encode_base64(data, max_line_length):
    encoded_lines = []
    unencoded_bytes_per_line = max_line_length // 4 * 3
    for i in range(0, len(data), unencoded_bytes_per_line):
        thisline = data[i:i + unencoded_bytes_per_line]
        encoded_lines.append(binascii.b2a_base64(thisline).decode('ascii'))
    return ''.join(encoded_lines)

def _encode_text(string, charset, cte, policy):
    maxlen = policy.max_line_length or sys.maxsize
    lines = string.encode(charset).splitlines()
    linesep = policy.linesep.encode('ascii')

    def embedded_body(lines):
        return linesep.join(lines) + linesep

    def normal_body(lines):
        return b'\n'.join(lines) + b'\n'
    if cte is None:
        if max(map(len, lines), default=0) <= maxlen:
            try:
                return ('7bit', normal_body(lines).decode('ascii'))
            except UnicodeDecodeError:
                pass
            if policy.cte_type == '8bit':
                return ('8bit', normal_body(lines).decode('ascii', 'surrogateescape'))
        sniff = embedded_body(lines[:10])
        sniff_qp = 可打印编码.body_encode(sniff.decode('latin-1'), maxlen)
        sniff_base64 = binascii.b2a_base64(sniff)
        if len(sniff_qp) > len(sniff_base64):
            cte = 'base64'
        else:
            cte = 'quoted-printable'
            if len(lines) <= 10:
                return (cte, sniff_qp)
    if cte == '7bit':
        data = normal_body(lines).decode('ascii')
    elif cte == '8bit':
        data = normal_body(lines).decode('ascii', 'surrogateescape')
    elif cte == 'quoted-printable':
        data = 可打印编码.body_encode(normal_body(lines).decode('latin-1'), maxlen)
    elif cte == 'base64':
        data = _encode_base64(embedded_body(lines), maxlen)
    else:
        raise ValueError('Unknown content transfer encoding {}'.format(cte))
    return (cte, data)

def 设文本内容(msg, string, subtype='plain', charset='utf-8', cte=None, disposition=None, filename=None, cid=None, params=None, headers=None):
    _prepare_set(msg, 'text', subtype, headers)
    cte, payload = _encode_text(string, charset, cte, msg.policy)
    msg.set_payload(payload)
    msg.set_param('charset', 电子邮件.字符集.ALIASES.get(charset, charset), replace=True)
    msg['Content-Transfer-Encoding'] = cte
    _finalize_set(msg, disposition, filename, cid, params)
原始数据管理器.add_set_handler(str, 设文本内容)

def 设消息内容(msg, message, subtype='rfc822', cte=None, disposition=None, filename=None, cid=None, params=None, headers=None):
    if subtype == 'partial':
        raise ValueError('message/partial is not supported for Message objects')
    if subtype == 'rfc822':
        if cte not in (None, '7bit', '8bit', 'binary'):
            raise ValueError('message/rfc822 parts do not support cte={}'.format(cte))
        cte = '8bit' if cte is None else cte
    elif subtype == 'external-body':
        if cte not in (None, '7bit'):
            raise ValueError('message/external-body parts do not support cte={}'.format(cte))
        cte = '7bit'
    elif cte is None:
        cte = '7bit'
    _prepare_set(msg, 'message', subtype, headers)
    msg.set_payload([message])
    msg['Content-Transfer-Encoding'] = cte
    _finalize_set(msg, disposition, filename, cid, params)
原始数据管理器.add_set_handler(电子邮件.消息.Message, 设消息内容)

def 设字节内容(msg, data, maintype, subtype, cte='base64', disposition=None, filename=None, cid=None, params=None, headers=None):
    _prepare_set(msg, maintype, subtype, headers)
    if cte == 'base64':
        data = _encode_base64(data, max_line_length=msg.policy.max_line_length)
    elif cte == 'quoted-printable':
        data = binascii.b2a_qp(data, istext=False, header=False, quotetabs=True)
        data = data.decode('ascii')
    elif cte == '7bit':
        data = data.decode('ascii')
    elif cte in ('8bit', 'binary'):
        data = data.decode('ascii', 'surrogateescape')
    msg.set_payload(data)
    msg['Content-Transfer-Encoding'] = cte
    _finalize_set(msg, disposition, filename, cid, params)
for typ in (bytes, bytearray, memoryview):
    原始数据管理器.add_set_handler(typ, 设字节内容)
del typ


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'ContentManager': '内容管理器',
    'get_message_content': '取消息内容',
    'get_non_text_content': '取非文本内容',
    'get_text_content': '取文本内容',
    'raw_data_manager': '原始数据管理器',
    'set_bytes_content': '设字节内容',
    'set_message_content': '设消息内容',
    'set_text_content': '设文本内容',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
