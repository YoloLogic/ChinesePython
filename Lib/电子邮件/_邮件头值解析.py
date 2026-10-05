# -*- coding: utf-8 -*-
"""电子邮件._邮件头值解析 —— 汉语库（由 tools/汉化库.py 从 Lib/email/_header_value_parser.py 机械生成，**不要手改**）。

英文库 Lib/email._header_value_parser.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


"""Header value parser implementing various email-related RFC parsing rules.

The parsing methods defined in this module implement various email related
parsing rules.  Principal among them is RFC 5322, which is the followon
to RFC 2822 and primarily a clarification of the former.  It also implements
RFC 2047 encoded word decoding.

RFC 5322 goes to considerable trouble to maintain backward compatibility with
RFC 822 in the parse phase, while cleaning up the structure on the generation
phase.  This parser supports correct RFC 5322 generation by tagging white space
as folding white space only when folding is allowed in the non-obsolete rule
sets.  Actually, the parser is even more generous when accepting input than RFC
5322 mandates, following the spirit of Postel's Law, which RFC 5322 encourages.
Where possible deviations from the standard are annotated on the 'defects'
attribute of tokens that deviate.

The general structure of the parser follows RFC 5322, and uses its terminology
where there is a direct correspondence.  Where the implementation requires a
somewhat different structure than that used by the formal grammar, new terms
that mimic the closest existing terms are used.  Thus, it really helps to have
a copy of RFC 5322 handy when studying this code.

Input to the parser is a string that has already been unfolded according to
RFC 5322 rules.  According to the RFC this unfolding is the very first step, and
this parser leaves the unfolding step to a higher level message parser, which
will have already detected the line breaks that need unfolding while
determining the beginning and end of each header.

The output of the parser is a TokenList object, which is a list subclass.  A
TokenList is a recursive data structure.  The terminal nodes of the structure
are Terminal objects, which are subclasses of str.  These do not correspond
directly to terminal objects in the formal grammar, but are instead more
practical higher level combinations of true terminals.

All TokenList and Terminal objects have a 'value' attribute, which produces the
semantically meaningful value of that part of the parse subtree.  The value of
all whitespace tokens (no matter how many sub-tokens they may contain) is a
single space, as per the RFC rules.  This includes 'CFWS', which is herein
included in the general class of whitespace tokens.  There is one exception to
the rule that whitespace tokens are collapsed into single spaces in values: in
the value of a 'bare-quoted-string' (a quoted-string with no leading or
trailing whitespace), any whitespace that appeared between the quotation marks
is preserved in the returned value.  Note that in all Terminal strings quoted
pairs are turned into their unquoted values.

All TokenList and Terminal objects also have a string value, which attempts to
be a "canonical" representation of the RFC-compliant form of the substring that
produced the parsed subtree, including minimal use of quoted pair quoting.
Whitespace runs are not collapsed.

Comment tokens also have a 'content' attribute providing the string found
between the parens (including any nested comments) with whitespace preserved.

All TokenList and Terminal objects have a 'defects' attribute which is a
possibly empty list all of the defects found while creating the token.  Defects
may appear on any token in the tree, and a composite list of all defects in the
subtree is available through the 'all_defects' attribute of any node.  (For
Terminal notes x.defects == x.all_defects.)

Each object in a parse tree is called a 'token', and each has a 'token_type'
attribute that gives the name from the RFC 5322 grammar that it represents.
Not all RFC 5322 nodes are produced, and there is one non-RFC 5322 node that
may be produced: 'ptext'.  A 'ptext' is a string of printable ascii characters.
It is returned in place of lists of (ctext/quoted-pair) and
(qtext/quoted-pair).

XXX: provide complete list of token types.
"""
_英文原名表 = {'Address': '地址', 'AddressList': '地址表', 'AngleAddr': '尖括号地址', 'Atom': '原子', 'Attribute': '属性', 'Comment': '注释', 'ContentDisposition': '内容处置', 'ContentTransferEncoding': '内容传输编码', 'ContentType': '内容类型', 'Domain': '域名', 'DomainLiteral': '域名字面量', 'DotAtom': '点原子', 'EncodedWord': '编码词', 'Group': '地址组', 'GroupList': '地址组表', 'Header': '邮件头', 'HeaderLabel': '邮件头标签', 'LocalPart': '本地部分', 'MIMEVersion': 'MIME版本', 'Mailbox': '信箱', 'MailboxList': '信箱表', 'MessageID': '消息ID', 'MimeParameters': 'MIME参数表', 'NameAddr': '具名地址', 'Parameter': '参数', 'ParameterizedHeaderValue': '带参数邮件头值', 'Phrase': '短语', 'QuotedString': '引号串', 'Token': '词法单元', 'TokenList': '词法单元表', 'UnstructuredTokenList': '非结构化词法单元表', 'Value': '值', 'WhiteSpaceTokenList': '空白词法单元表', 'Word': '词', 'get_addr_spec': '取地址规格', 'get_address': '取地址', 'get_address_list': '取地址表', 'get_angle_addr': '取尖括号地址', 'get_atext': '取原子文本', 'get_atom': '取原子', 'get_bare_quoted_string': '取裸引号串', 'get_cfws': '取注释与前导空白', 'get_comment': '取注释', 'get_display_name': '取显示名', 'get_domain': '取域名', 'get_domain_literal': '取域名字面量', 'get_dot_atom': '取点原子', 'get_dot_atom_text': '取点原子文本', 'get_encoded_word': '取编码词', 'get_fws': '取前导空白', 'get_group': '取地址组', 'get_group_list': '取地址组表', 'get_local_part': '取本地部分', 'get_mailbox': '取信箱', 'get_mailbox_list': '取信箱表', 'get_msg_id': '取消息ID', 'get_name_addr': '取具名地址', 'get_phrase': '取短语', 'get_qcontent': '取Q内容', 'get_qp_ctext': '取QP文本', 'get_quoted_string': '取引号串', 'get_unstructured': '取非结构化值', 'get_word': '取词', 'make_quoted_pairs': '造引号对', 'parse_content_disposition_header': '解析内容处置邮件头', 'parse_content_transfer_encoding_header': '解析传输编码邮件头', 'parse_content_type_header': '解析内容类型邮件头', 'parse_message_id': '解析消息ID', 'parse_message_ids': '解析消息ID表', 'parse_mime_parameters': '解析MIME参数', 'parse_mime_version': '解析MIME版本', 'quote_string': '加引号'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import re
import sys
import urllib
from string import hexdigits
from operator import itemgetter
from 电子邮件 import _编码词 as _ew
from 电子邮件 import 错误
from 电子邮件 import 工具
_WSP = ' \t'
WSP = set(_WSP)
CFWS_LEADER = WSP | set('(')
SPECIALS = set('()<>@,:;.\\"[]')
ATOM_ENDS = SPECIALS | WSP
DOT_ATOM_ENDS = ATOM_ENDS - set('.')
PHRASE_ENDS = SPECIALS - set('."(')
TSPECIALS = (SPECIALS | set('/?=')) - set('.')
TOKEN_ENDS = TSPECIALS | WSP
ASPECIALS = TSPECIALS | set("*'%")
ATTRIBUTE_ENDS = ASPECIALS | WSP
EXTENDED_ATTRIBUTE_ENDS = ATTRIBUTE_ENDS - set('%')
NLSET = {'\n', '\r'}
SPECIALSNL = SPECIALS | NLSET

def 造引号对(value):
    """Escape dquote and backslash for use within a quoted-string."""
    return str(value).replace('\\', '\\\\').replace('"', '\\"')

def make_parenthesis_pairs(value):
    """Escape parenthesis and backslash for use within a comment."""
    return str(value).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

def 加引号(value):
    escaped = 造引号对(value)
    return f'"{escaped}"'
rfc2047_matcher = re.compile("\n   =\\?            # literal =?\n   [^?]*          # charset\n   \\?             # literal ?\n   [qQbB]         # literal 'q' or 'b', case insensitive\n   \\?             # literal ?\n  .*?             # encoded word\n  \\?=             # literal ?=\n", re.VERBOSE | re.MULTILINE)

class 词法单元表(list):
    token_type = None
    syntactic_break = True
    ew_combine_allowed = True

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.defects = []

    def __str__(self):
        return ''.join((str(x) for x in self))

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())

    @property
    def value(self):
        return ''.join((x.value for x in self if x.value))

    @property
    def all_defects(self):
        return sum((x.all_defects for x in self), self.defects)

    def startswith_fws(self):
        return self[0].startswith_fws()

    @property
    def as_ew_allowed(self):
        """True if all top level tokens of this part may be RFC2047 encoded."""
        return all((part.as_ew_allowed for part in self))

    @property
    def comments(self):
        comments = []
        for token in self:
            comments.extend(token.comments)
        return comments

    def fold(self, *, policy):
        return _refold_parse_tree(self, policy=policy)

    def pprint(self, indent=''):
        print(self.ppstr(indent=indent))

    def ppstr(self, indent=''):
        return '\n'.join(self._pp(indent=indent))

    def _pp(self, indent=''):
        yield '{}{}/{}('.format(indent, self.__class__.__name__, self.token_type)
        for token in self:
            if not hasattr(token, '_pp'):
                yield (indent + '    !! invalid element in token list: {!r}'.format(token))
            else:
                yield from token._pp(indent + '    ')
        if self.defects:
            extra = ' Defects: {}'.format(self.defects)
        else:
            extra = ''
        yield '{}){}'.format(indent, extra)

class 空白词法单元表(词法单元表):

    @property
    def value(self):
        return ' '

    @property
    def comments(self):
        return [x.content for x in self if x.token_type == 'comment']

class 非结构化词法单元表(词法单元表):
    token_type = 'unstructured'

class 短语(词法单元表):
    token_type = 'phrase'

class 词(词法单元表):
    token_type = 'word'

class CFWSList(空白词法单元表):
    token_type = 'cfws'

class 原子(词法单元表):
    token_type = 'atom'

class 词法单元(词法单元表):
    token_type = 'token'
    encode_as_ew = False

class 编码词(词法单元表):
    token_type = 'encoded-word'
    cte = None
    charset = None
    lang = None

class 引号串(词法单元表):
    token_type = 'quoted-string'

    @property
    def content(self):
        for x in self:
            if x.token_type == 'bare-quoted-string':
                return x.value

    @property
    def quoted_value(self):
        res = []
        for x in self:
            if x.token_type == 'bare-quoted-string':
                res.append(str(x))
            else:
                res.append(x.value)
        return ''.join(res)

    @property
    def stripped_value(self):
        for token in self:
            if token.token_type == 'bare-quoted-string':
                return token.value

class BareQuotedString(引号串):
    token_type = 'bare-quoted-string'

    def __str__(self):
        return 加引号(''.join((str(x) for x in self)))

    @property
    def value(self):
        return ''.join((str(x) for x in self))

class 注释(空白词法单元表):
    token_type = 'comment'

    def __str__(self):
        return ''.join(sum([['('], [self.quote(x) for x in self], [')']], []))

    def quote(self, value):
        if value.token_type == 'comment':
            return str(value)
        return str(value).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

    @property
    def content(self):
        return ''.join((str(x) for x in self))

    @property
    def comments(self):
        return [self.content]

class 地址表(词法单元表):
    token_type = 'address-list'

    @property
    def addresses(self):
        return [x for x in self if x.token_type == 'address']

    @property
    def mailboxes(self):
        return sum((x.mailboxes for x in self if x.token_type == 'address'), [])

    @property
    def all_mailboxes(self):
        return sum((x.all_mailboxes for x in self if x.token_type == 'address'), [])

class 地址(词法单元表):
    token_type = 'address'

    @property
    def display_name(self):
        if self[0].token_type == 'group':
            return self[0].display_name

    @property
    def mailboxes(self):
        if self[0].token_type == 'mailbox':
            return [self[0]]
        elif self[0].token_type == 'invalid-mailbox':
            return []
        return self[0].mailboxes

    @property
    def all_mailboxes(self):
        if self[0].token_type == 'mailbox':
            return [self[0]]
        elif self[0].token_type == 'invalid-mailbox':
            return [self[0]]
        return self[0].all_mailboxes

class 信箱表(词法单元表):
    token_type = 'mailbox-list'

    @property
    def mailboxes(self):
        return [x for x in self if x.token_type == 'mailbox']

    @property
    def all_mailboxes(self):
        return [x for x in self if x.token_type in ('mailbox', 'invalid-mailbox')]

class 地址组表(词法单元表):
    token_type = 'group-list'

    @property
    def mailboxes(self):
        if not self or self[0].token_type != 'mailbox-list':
            return []
        return self[0].mailboxes

    @property
    def all_mailboxes(self):
        if not self or self[0].token_type != 'mailbox-list':
            return []
        return self[0].all_mailboxes

class 地址组(词法单元表):
    token_type = 'group'

    @property
    def mailboxes(self):
        if self[2].token_type != 'group-list':
            return []
        return self[2].mailboxes

    @property
    def all_mailboxes(self):
        if self[2].token_type != 'group-list':
            return []
        return self[2].all_mailboxes

    @property
    def display_name(self):
        return self[0].display_name

class 具名地址(词法单元表):
    token_type = 'name-addr'

    @property
    def display_name(self):
        if len(self) == 1:
            return None
        return self[0].display_name

    @property
    def local_part(self):
        return self[-1].local_part

    @property
    def domain(self):
        return self[-1].domain

    @property
    def route(self):
        return self[-1].route

    @property
    def addr_spec(self):
        return self[-1].addr_spec

class 尖括号地址(词法单元表):
    token_type = 'angle-addr'

    @property
    def local_part(self):
        for x in self:
            if x.token_type == 'addr-spec':
                return x.local_part

    @property
    def domain(self):
        for x in self:
            if x.token_type == 'addr-spec':
                return x.domain

    @property
    def route(self):
        for x in self:
            if x.token_type == 'obs-route':
                return x.domains

    @property
    def addr_spec(self):
        for x in self:
            if x.token_type == 'addr-spec':
                if x.local_part:
                    return x.addr_spec
                else:
                    return 加引号(x.local_part) + x.addr_spec
        else:
            return '<>'

class ObsRoute(词法单元表):
    token_type = 'obs-route'

    @property
    def domains(self):
        return [x.domain for x in self if x.token_type == 'domain']

class 信箱(词法单元表):
    token_type = 'mailbox'

    @property
    def display_name(self):
        if self[0].token_type == 'name-addr':
            return self[0].display_name

    @property
    def local_part(self):
        return self[0].local_part

    @property
    def domain(self):
        return self[0].domain

    @property
    def route(self):
        if self[0].token_type == 'name-addr':
            return self[0].route

    @property
    def addr_spec(self):
        return self[0].addr_spec

class InvalidMailbox(词法单元表):
    token_type = 'invalid-mailbox'

    @property
    def display_name(self):
        return None
    local_part = domain = route = addr_spec = display_name

class 域名(词法单元表):
    token_type = 'domain'
    as_ew_allowed = False

    @property
    def domain(self):
        return ''.join(super().value.split())

class 点原子(词法单元表):
    token_type = 'dot-atom'

class DotAtomText(词法单元表):
    token_type = 'dot-atom-text'
    as_ew_allowed = True

class NoFoldLiteral(词法单元表):
    token_type = 'no-fold-literal'
    as_ew_allowed = False

class AddrSpec(词法单元表):
    token_type = 'addr-spec'
    as_ew_allowed = False

    @property
    def local_part(self):
        return self[0].local_part

    @property
    def domain(self):
        if len(self) < 3:
            return None
        return self[-1].domain

    @property
    def value(self):
        if len(self) < 3:
            return self[0].value
        return self[0].value.rstrip() + self[1].value + self[2].value.lstrip()

    @property
    def addr_spec(self):
        nameset = set(self.local_part)
        if len(nameset) > len(nameset - DOT_ATOM_ENDS):
            lp = 加引号(self.local_part)
        else:
            lp = self.local_part
        if self.domain is not None:
            return lp + '@' + self.domain
        return lp

class ObsLocalPart(词法单元表):
    token_type = 'obs-local-part'
    as_ew_allowed = False

class DisplayName(短语):
    token_type = 'display-name'
    ew_combine_allowed = False

    @property
    def display_name(self):
        res = 词法单元表(self)
        if len(res) == 0:
            return res.value
        if res[0].token_type == 'cfws':
            res.pop(0)
        elif isinstance(res[0], 词法单元表) and res[0][0].token_type == 'cfws':
            res[0] = 词法单元表(res[0][1:])
        if res[-1].token_type == 'cfws':
            res.pop()
        elif isinstance(res[-1], 词法单元表) and res[-1][-1].token_type == 'cfws':
            res[-1] = 词法单元表(res[-1][:-1])
        return res.value

    @property
    def value(self):
        quote = False
        if self.defects:
            quote = True
        else:
            for x in self:
                if x.token_type == 'quoted-string':
                    quote = True
        if len(self) != 0 and quote:
            pre = post = ''
            if self[0].token_type == 'cfws' or (isinstance(self[0], 词法单元表) and self[0][0].token_type == 'cfws'):
                pre = ' '
            if self[-1].token_type == 'cfws' or (isinstance(self[-1], 词法单元表) and self[-1][-1].token_type == 'cfws'):
                post = ' '
            return pre + 加引号(self.display_name) + post
        else:
            return super().value

class 本地部分(词法单元表):
    token_type = 'local-part'
    as_ew_allowed = False

    @property
    def value(self):
        if self[0].token_type == 'quoted-string':
            return self[0].quoted_value
        else:
            return self[0].value

    @property
    def local_part(self):
        res = [DOT]
        last = DOT
        last_is_tl = False
        for tok in self[0] + [DOT]:
            if tok.token_type == 'cfws':
                continue
            if last_is_tl and tok.token_type == 'dot' and last and (last[-1].token_type == 'cfws'):
                res[-1] = 词法单元表(last[:-1])
            is_tl = isinstance(tok, 词法单元表)
            if is_tl and last.token_type == 'dot' and tok and (tok[0].token_type == 'cfws'):
                res.append(词法单元表(tok[1:]))
            else:
                res.append(tok)
            last = res[-1]
            last_is_tl = is_tl
        res = 词法单元表(res[1:-1])
        return res.value

class 域名字面量(词法单元表):
    token_type = 'domain-literal'
    as_ew_allowed = False

    @property
    def domain(self):
        return ''.join(super().value.split())

    @property
    def ip(self):
        for x in self:
            if x.token_type == 'ptext':
                return x.value

class MIME版本(词法单元表):
    token_type = 'mime-version'
    major = None
    minor = None

class 参数(词法单元表):
    token_type = 'parameter'
    sectioned = False
    extended = False
    charset = 'us-ascii'

    @property
    def section_number(self):
        return self[1].number if self.sectioned else 0

    @property
    def param_value(self):
        for token in self:
            if token.token_type == 'value':
                return token.stripped_value
            if token.token_type == 'quoted-string':
                for token in token:
                    if token.token_type == 'bare-quoted-string':
                        for token in token:
                            if token.token_type == 'value':
                                return token.stripped_value
        return ''

class InvalidParameter(参数):
    token_type = 'invalid-parameter'

class 属性(词法单元表):
    token_type = 'attribute'

    @property
    def stripped_value(self):
        for token in self:
            if token.token_type.endswith('attrtext'):
                return token.value

class Section(词法单元表):
    token_type = 'section'
    number = None

class 值(词法单元表):
    token_type = 'value'

    @property
    def stripped_value(self):
        token = self[0]
        if token.token_type == 'cfws':
            token = self[1]
        if token.token_type.endswith(('quoted-string', 'attribute', 'extended-attribute')):
            return token.stripped_value
        return self.value

class MIME参数表(词法单元表):
    token_type = 'mime-parameters'
    syntactic_break = False

    @property
    def params(self):
        params = {}
        for token in self:
            if not token.token_type.endswith('parameter'):
                continue
            if token[0].token_type != 'attribute':
                continue
            name = token[0].value.strip()
            if name not in params:
                params[name] = []
            params[name].append((token.section_number, token))
        for name, parts in params.items():
            parts = sorted(parts, key=itemgetter(0))
            first_param = parts[0][1]
            charset = first_param.charset
            if not first_param.extended and len(parts) > 1:
                if parts[1][0] == 0:
                    parts[1][1].defects.append(错误.InvalidHeaderDefect('duplicate parameter name; duplicate(s) ignored'))
                    parts = parts[:1]
            value_parts = []
            i = 0
            for section_number, param in parts:
                if section_number != i:
                    if not param.extended:
                        param.defects.append(错误.InvalidHeaderDefect('duplicate parameter name; duplicate ignored'))
                        continue
                    else:
                        param.defects.append(错误.InvalidHeaderDefect('inconsistent RFC2231 parameter numbering'))
                i += 1
                value = param.param_value
                if param.extended:
                    try:
                        value = urllib.parse.unquote_to_bytes(value)
                    except UnicodeEncodeError:
                        value = urllib.parse.unquote(value, encoding='latin-1')
                    else:
                        try:
                            value = value.decode(charset, 'surrogateescape')
                        except (LookupError, UnicodeEncodeError):
                            value = value.decode('us-ascii', 'surrogateescape')
                        if 工具._has_surrogates(value):
                            param.defects.append(错误.UndecodableBytesDefect())
                value_parts.append(value)
            value = ''.join(value_parts)
            yield (name, value)

    def __str__(self):
        params = []
        for name, value in self.params:
            if value:
                params.append('{}={}'.format(name, 加引号(value)))
            else:
                params.append(name)
        params = '; '.join(params)
        return ' ' + params if params else ''

class 带参数邮件头值(词法单元表):
    syntactic_break = False

    @property
    def params(self):
        for token in reversed(self):
            if token.token_type == 'mime-parameters':
                return token.params
        return {}

class 内容类型(带参数邮件头值):
    token_type = 'content-type'
    as_ew_allowed = False
    maintype = 'text'
    subtype = 'plain'

class 内容处置(带参数邮件头值):
    token_type = 'content-disposition'
    as_ew_allowed = False
    content_disposition = None

class 内容传输编码(词法单元表):
    token_type = 'content-transfer-encoding'
    as_ew_allowed = False
    cte = '7bit'

class 邮件头标签(词法单元表):
    token_type = 'header-label'
    as_ew_allowed = False

class MsgID(词法单元表):
    token_type = 'msg-id'
    as_ew_allowed = False

    def fold(self, policy):
        return str(self) + policy.linesep

class 消息ID(MsgID):
    token_type = 'message-id'

class InvalidMessageID(消息ID):
    token_type = 'invalid-message-id'

class MessageIDList(词法单元表):
    token_type = 'message-id-list'

    @property
    def message_ids(self):
        return [x for x in self if x.token_type == 'msg-id']

class 邮件头(词法单元表):
    token_type = 'header'

class Terminal(str):
    as_ew_allowed = True
    ew_combine_allowed = True
    syntactic_break = True

    def __new__(cls, value, token_type):
        self = super().__new__(cls, value)
        self.token_type = token_type
        self.defects = []
        return self

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())

    def pprint(self):
        print(self.__class__.__name__ + '/' + self.token_type)

    @property
    def all_defects(self):
        return list(self.defects)

    def _pp(self, indent=''):
        return ['{}{}/{}({}){}'.format(indent, self.__class__.__name__, self.token_type, super().__repr__(), '' if not self.defects else ' {}'.format(self.defects))]

    def pop_trailing_ws(self):
        return None

    @property
    def comments(self):
        return []

    def __getnewargs__(self):
        return (str(self), self.token_type)

class WhiteSpaceTerminal(Terminal):

    @property
    def value(self):
        return ' '

    def startswith_fws(self):
        return self and self[0] in WSP

class ValueTerminal(Terminal):

    @property
    def value(self):
        return self

    def startswith_fws(self):
        return False

class EWWhiteSpaceTerminal(WhiteSpaceTerminal):

    @property
    def value(self):
        return ''

    def __str__(self):
        return ''

class _InvalidEwError(错误.HeaderParseError):
    """Invalid encoded word found while parsing headers."""
DOT = ValueTerminal('.', 'dot')
ListSeparator = ValueTerminal(',', 'list-separator')
ListSeparator.as_ew_allowed = False
ListSeparator.syntactic_break = False
RouteComponentMarker = ValueTerminal('@', 'route-component-marker')
_wsp_splitter = re.compile('([{}]+)'.format(''.join(WSP))).split
_non_atom_end_matcher = re.compile('[^{}]+'.format(re.escape(''.join(ATOM_ENDS)))).match
_non_printable_finder = re.compile('[\\x00-\\x20\\x7F]').findall
_non_token_end_matcher = re.compile('[^{}]+'.format(re.escape(''.join(TOKEN_ENDS)))).match
_non_attribute_end_matcher = re.compile('[^{}]+'.format(re.escape(''.join(ATTRIBUTE_ENDS)))).match
_non_extended_attribute_end_matcher = re.compile('[^{}]+'.format(re.escape(''.join(EXTENDED_ATTRIBUTE_ENDS)))).match

def _validate_xtext(xtext):
    """If input token contains ASCII non-printables, register a defect."""
    non_printables = _non_printable_finder(xtext)
    if non_printables:
        xtext.defects.append(错误.NonPrintableDefect(non_printables))
    if 工具._has_surrogates(xtext):
        xtext.defects.append(错误.UndecodableBytesDefect('Non-ASCII characters found in header token'))

def _get_ptext_to_endchars(value, endchars):
    """Scan printables/quoted-pairs until endchars and return unquoted ptext.

    This function turns a run of qcontent, ccontent-without-comments, or
    dtext-with-quoted-printables into a single string by unquoting any
    quoted printables.  It returns the string, the remaining value, and
    a flag that is True iff there were any quoted printables decoded.

    """
    if not value:
        return ('', '', False)
    fragment, *remainder = _wsp_splitter(value, 1)
    vchars = []
    escape = False
    had_qp = False
    for pos in range(len(fragment)):
        if fragment[pos] == '\\':
            if escape:
                escape = False
                had_qp = True
            else:
                escape = True
                continue
        if escape:
            escape = False
        elif fragment[pos] in endchars:
            break
        vchars.append(fragment[pos])
    else:
        pos = pos + 1
    return (''.join(vchars), ''.join([fragment[pos:]] + remainder), had_qp)

def 取前导空白(value):
    """FWS = 1*WSP

    This isn't the RFC definition.  We're using fws to represent tokens where
    folding can be done, but when we are parsing the *un*folding has already
    been done so we don't need to watch out for CRLF.

    """
    newvalue = value.lstrip()
    fws = WhiteSpaceTerminal(value[:len(value) - len(newvalue)], 'fws')
    return (fws, newvalue)

def 取编码词(value, terminal_type='vtext'):
    """ encoded-word = "=?" charset "?" encoding "?" encoded-text "?="

    """
    ew = 编码词()
    if not value.startswith('=?'):
        raise 错误.HeaderParseError('expected encoded word but found {}'.format(value))
    tok, *remainder = value[2:].split('?=', 1)
    if tok == value[2:]:
        raise 错误.HeaderParseError('expected encoded word but found {}'.format(value))
    remstr = ''.join(remainder)
    if len(remstr) > 1 and remstr[0] in hexdigits and (remstr[1] in hexdigits) and (tok.count('?') < 2):
        rest, *remainder = remstr.split('?=', 1)
        tok = tok + '?=' + rest
    if len(tok.split()) > 1:
        ew.defects.append(错误.InvalidHeaderDefect('whitespace inside encoded word'))
    ew.cte = value
    value = ''.join(remainder)
    try:
        text, charset, lang, defects = _ew.decode('=?' + tok + '?=')
    except (ValueError, KeyError):
        raise _InvalidEwError("encoded word format invalid: '{}'".format(ew.cte))
    ew.charset = charset
    ew.lang = lang
    ew.defects.extend(defects)
    while text:
        if text[0] in WSP:
            token, text = 取前导空白(text)
            ew.append(token)
            continue
        chars, *remainder = _wsp_splitter(text, 1)
        vtext = ValueTerminal(chars, terminal_type)
        _validate_xtext(vtext)
        ew.append(vtext)
        text = ''.join(remainder)
    if value and value[0] not in WSP:
        ew.defects.append(错误.InvalidHeaderDefect('missing trailing whitespace after encoded-word'))
    return (ew, value)

def 取非结构化值(value):
    """unstructured = (*([FWS] vchar) *WSP) / obs-unstruct
       obs-unstruct = *((*LF *CR *(obs-utext) *LF *CR)) / FWS)
       obs-utext = %d0 / obs-NO-WS-CTL / LF / CR

       obs-NO-WS-CTL is control characters except WSP/CR/LF.

    So, basically, we have printable runs, plus control characters or nulls in
    the obsolete syntax, separated by whitespace.  Since RFC 2047 uses the
    obsolete syntax in its specification, but requires whitespace on either
    side of the encoded words, I can see no reason to need to separate the
    non-printable-non-whitespace from the printable runs if they occur, so we
    parse this into xtext tokens separated by WSP tokens.

    Because an 'unstructured' value must by definition constitute the entire
    value, this 'get' routine does not return a remaining value, only the
    parsed TokenList.

    """
    unstructured = 非结构化词法单元表()
    while value:
        if value[0] in WSP:
            token, value = 取前导空白(value)
            unstructured.append(token)
            continue
        valid_ew = True
        if value.startswith('=?'):
            try:
                token, value = 取编码词(value, 'utext')
            except _InvalidEwError:
                valid_ew = False
            except 错误.HeaderParseError:
                pass
            else:
                have_ws = True
                if len(unstructured) > 0:
                    if unstructured[-1].token_type != 'fws':
                        unstructured.defects.append(错误.InvalidHeaderDefect('missing whitespace before encoded word'))
                        have_ws = False
                if have_ws and len(unstructured) > 1:
                    if unstructured[-2].token_type == 'encoded-word':
                        unstructured[-1] = EWWhiteSpaceTerminal(unstructured[-1], 'fws')
                unstructured.append(token)
                continue
        tok, *remainder = _wsp_splitter(value, 1)
        if valid_ew and rfc2047_matcher.search(tok):
            tok, *remainder = value.partition('=?')
        vtext = ValueTerminal(tok, 'utext')
        _validate_xtext(vtext)
        unstructured.append(vtext)
        value = ''.join(remainder)
    return unstructured

def 取QP文本(value):
    """ctext = <printable ascii except \\ ( )>

    This is not the RFC ctext, since we are handling nested comments in comment
    and unquoting quoted-pairs here.  We allow anything except the '()'
    characters, but if we find any ASCII other than the RFC defined printable
    ASCII, a NonPrintableDefect is added to the token's defects list.  Since
    quoted pairs are converted to their unquoted values, what is returned is
    a 'ptext' token.  In this case it is a WhiteSpaceTerminal, so it's value
    is ' '.

    """
    ptext, value, _ = _get_ptext_to_endchars(value, '()')
    ptext = WhiteSpaceTerminal(ptext, 'ptext')
    _validate_xtext(ptext)
    return (ptext, value)

def 取Q内容(value):
    """qcontent = qtext / quoted-pair

    We allow anything except the DQUOTE character, but if we find any ASCII
    other than the RFC defined printable ASCII, a NonPrintableDefect is
    added to the token's defects list.  Any quoted pairs are converted to their
    unquoted values, so what is returned is a 'ptext' token.  In this case it
    is a ValueTerminal.

    """
    ptext, value, _ = _get_ptext_to_endchars(value, '"')
    ptext = ValueTerminal(ptext, 'ptext')
    _validate_xtext(ptext)
    return (ptext, value)

def 取原子文本(value):
    """atext = <matches _atext_matcher>

    We allow any non-ATOM_ENDS in atext, but add an InvalidATextDefect to
    the token's defects list if we find non-atext characters.
    """
    m = _non_atom_end_matcher(value)
    if not m:
        raise 错误.HeaderParseError("expected atext but found '{}'".format(value))
    atext = m.group()
    value = value[len(atext):]
    atext = ValueTerminal(atext, 'atext')
    _validate_xtext(atext)
    return (atext, value)

def 取裸引号串(value):
    """bare-quoted-string = DQUOTE *([FWS] qcontent) [FWS] DQUOTE

    A quoted-string without the leading or trailing white space.  Its
    value is the text between the quote marks, with whitespace
    preserved and quoted pairs decoded.
    """
    if not value or value[0] != '"':
        raise 错误.HeaderParseError('expected \'"\' but found \'{}\''.format(value))
    bare_quoted_string = BareQuotedString()
    value = value[1:]
    if value and value[0] == '"':
        return (bare_quoted_string, value[1:])
    while value and value[0] != '"':
        if value[0] in WSP:
            token, value = 取前导空白(value)
        elif value[:2] == '=?':
            valid_ew = False
            try:
                token, value = 取编码词(value)
                bare_quoted_string.defects.append(错误.InvalidHeaderDefect('encoded word inside quoted string'))
                valid_ew = True
            except 错误.HeaderParseError:
                token, value = 取Q内容(value)
            if valid_ew and len(bare_quoted_string) > 1:
                if bare_quoted_string[-1].token_type == 'fws' and bare_quoted_string[-2].token_type == 'encoded-word':
                    bare_quoted_string[-1] = EWWhiteSpaceTerminal(bare_quoted_string[-1], 'fws')
        else:
            token, value = 取Q内容(value)
        bare_quoted_string.append(token)
    if not value:
        bare_quoted_string.defects.append(错误.InvalidHeaderDefect('end of header inside quoted string'))
        return (bare_quoted_string, value)
    return (bare_quoted_string, value[1:])

def 取注释(value):
    """comment = "(" *([FWS] ccontent) [FWS] ")"
       ccontent = ctext / quoted-pair / comment

    We handle nested comments here, and quoted-pair in our qp-ctext routine.
    """
    if value and value[0] != '(':
        raise 错误.HeaderParseError("expected '(' but found '{}'".format(value))
    comment = 注释()
    value = value[1:]
    while value and value[0] != ')':
        if value[0] in WSP:
            token, value = 取前导空白(value)
        elif value[0] == '(':
            token, value = 取注释(value)
        else:
            token, value = 取QP文本(value)
        comment.append(token)
    if not value:
        comment.defects.append(错误.InvalidHeaderDefect('end of header inside comment'))
        return (comment, value)
    return (comment, value[1:])

def 取注释与前导空白(value):
    """CFWS = (1*([FWS] comment) [FWS]) / FWS

    """
    cfws = CFWSList()
    while value and value[0] in CFWS_LEADER:
        if value[0] in WSP:
            token, value = 取前导空白(value)
        else:
            token, value = 取注释(value)
        cfws.append(token)
    return (cfws, value)

def 取引号串(value):
    """quoted-string = [CFWS] <bare-quoted-string> [CFWS]

    'bare-quoted-string' is an intermediate class defined by this
    parser and not by the RFC grammar.  It is the quoted string
    without any attached CFWS.
    """
    quoted_string = 引号串()
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        quoted_string.append(token)
    token, value = 取裸引号串(value)
    quoted_string.append(token)
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        quoted_string.append(token)
    return (quoted_string, value)

def 取原子(value):
    """atom = [CFWS] 1*atext [CFWS]

    An atom could be an rfc2047 encoded word.
    """
    atom = 原子()
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        atom.append(token)
    if value and value[0] in ATOM_ENDS:
        raise 错误.HeaderParseError("expected atom but found '{}'".format(value))
    if value.startswith('=?'):
        try:
            token, value = 取编码词(value)
        except 错误.HeaderParseError:
            token, value = 取原子文本(value)
    else:
        token, value = 取原子文本(value)
    atom.append(token)
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        atom.append(token)
    return (atom, value)

def 取点原子文本(value):
    """ dot-text = 1*atext *("." 1*atext)

    """
    dot_atom_text = DotAtomText()
    if not value or value[0] in ATOM_ENDS:
        raise 错误.HeaderParseError("expected atom at a start of dot-atom-text but found '{}'".format(value))
    while value and value[0] not in ATOM_ENDS:
        token, value = 取原子文本(value)
        dot_atom_text.append(token)
        if value and value[0] == '.':
            dot_atom_text.append(DOT)
            value = value[1:]
    if dot_atom_text[-1] is DOT:
        raise 错误.HeaderParseError("expected atom at end of dot-atom-text but found '{}'".format('.' + value))
    return (dot_atom_text, value)

def 取点原子(value):
    """ dot-atom = [CFWS] dot-atom-text [CFWS]

    Any place we can have a dot atom, we could instead have an rfc2047 encoded
    word.
    """
    dot_atom = 点原子()
    if value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        dot_atom.append(token)
    if value.startswith('=?'):
        try:
            token, value = 取编码词(value)
        except 错误.HeaderParseError:
            token, value = 取点原子文本(value)
    else:
        token, value = 取点原子文本(value)
    dot_atom.append(token)
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        dot_atom.append(token)
    return (dot_atom, value)

def 取词(value):
    """word = atom / quoted-string

    Either atom or quoted-string may start with CFWS.  We have to peel off this
    CFWS first to determine which type of word to parse.  Afterward we splice
    the leading CFWS, if any, into the parsed sub-token.

    If neither an atom or a quoted-string is found before the next special, a
    HeaderParseError is raised.

    The token returned is either an Atom or a QuotedString, as appropriate.
    This means the 'word' level of the formal grammar is not represented in the
    parse tree; this is because having that extra layer when manipulating the
    parse tree is more confusing than it is helpful.

    """
    if value[0] in CFWS_LEADER:
        leader, value = 取注释与前导空白(value)
    else:
        leader = None
    if not value:
        raise 错误.HeaderParseError("Expected 'atom' or 'quoted-string' but found nothing.")
    if value[0] == '"':
        token, value = 取引号串(value)
    elif value[0] in SPECIALS:
        raise 错误.HeaderParseError("Expected 'atom' or 'quoted-string' but found '{}'".format(value))
    else:
        token, value = 取原子(value)
    if leader is not None:
        token[:0] = [leader]
    return (token, value)

def 取短语(value):
    """ phrase = 1*word / obs-phrase
        obs-phrase = word *(word / "." / CFWS)

    This means a phrase can be a sequence of words, periods, and CFWS in any
    order as long as it starts with at least one word.  If anything other than
    words is detected, an ObsoleteHeaderDefect is added to the token's defect
    list.  We also accept a phrase that starts with CFWS followed by a dot;
    this is registered as an InvalidHeaderDefect, since it is not supported by
    even the obsolete grammar.

    """
    phrase = 短语()
    try:
        token, value = 取词(value)
        phrase.append(token)
    except 错误.HeaderParseError:
        phrase.defects.append(错误.InvalidHeaderDefect('phrase does not start with word'))
    while value and value[0] not in PHRASE_ENDS:
        if value[0] == '.':
            phrase.append(DOT)
            phrase.defects.append(错误.ObsoleteHeaderDefect("period in 'phrase'"))
            value = value[1:]
        else:
            try:
                token, value = 取词(value)
                if token[0].token_type == 'encoded-word' and phrase and (phrase[-1].token_type == 'atom') and (len(phrase[-1]) > 1) and (phrase[-1][-2].token_type == 'encoded-word') and (phrase[-1][-1].token_type == 'cfws') and (not phrase[-1][-1].comments):
                    phrase[-1][-1] = EWWhiteSpaceTerminal(phrase[-1], 'fws')
            except 错误.HeaderParseError:
                if value[0] in CFWS_LEADER:
                    token, value = 取注释与前导空白(value)
                    phrase.defects.append(错误.ObsoleteHeaderDefect('comment found without atom'))
                else:
                    raise
            phrase.append(token)
    return (phrase, value)

def 取本地部分(value):
    """ local-part = dot-atom / quoted-string / obs-local-part

    """
    local_part = 本地部分()
    leader = None
    if value and value[0] in CFWS_LEADER:
        leader, value = 取注释与前导空白(value)
    if not value:
        raise 错误.HeaderParseError("expected local-part but found '{}'".format(value))
    try:
        token, value = 取点原子(value)
    except 错误.HeaderParseError:
        try:
            token, value = 取词(value)
        except 错误.HeaderParseError:
            if value[0] != '\\' and value[0] in PHRASE_ENDS:
                raise
            token = 词法单元表()
    if leader is not None:
        token[:0] = [leader]
    local_part.append(token)
    if value and (value[0] == '\\' or value[0] not in PHRASE_ENDS):
        obs_local_part, value = get_obs_local_part(str(local_part) + value)
        if obs_local_part.token_type == 'invalid-obs-local-part':
            local_part.defects.append(错误.InvalidHeaderDefect('local-part is not dot-atom, quoted-string, or obs-local-part'))
        else:
            local_part.defects.append(错误.ObsoleteHeaderDefect('local-part is not a dot-atom (contains CFWS)'))
        local_part[0] = obs_local_part
    try:
        local_part.value.encode('ascii')
    except UnicodeEncodeError:
        local_part.defects.append(错误.NonASCIILocalPartDefect('local-part contains non-ASCII characters)'))
    return (local_part, value)

def get_obs_local_part(value):
    """ obs-local-part = word *("." word)
    """
    obs_local_part = ObsLocalPart()
    last_non_ws_was_dot = False
    while value and (value[0] == '\\' or value[0] not in PHRASE_ENDS):
        if value[0] == '.':
            if last_non_ws_was_dot:
                obs_local_part.defects.append(错误.InvalidHeaderDefect("invalid repeated '.'"))
            obs_local_part.append(DOT)
            last_non_ws_was_dot = True
            value = value[1:]
            continue
        elif value[0] == '\\':
            obs_local_part.append(ValueTerminal(value[0], 'misplaced-special'))
            value = value[1:]
            obs_local_part.defects.append(错误.InvalidHeaderDefect("'\\' character outside of quoted-string/ccontent"))
            last_non_ws_was_dot = False
            continue
        if obs_local_part and obs_local_part[-1].token_type != 'dot':
            obs_local_part.defects.append(错误.InvalidHeaderDefect("missing '.' between words"))
        try:
            token, value = 取词(value)
            last_non_ws_was_dot = False
        except 错误.HeaderParseError:
            if value[0] not in CFWS_LEADER:
                raise
            token, value = 取注释与前导空白(value)
        obs_local_part.append(token)
    if not obs_local_part:
        raise 错误.HeaderParseError("expected obs-local-part but found '{}'".format(value))
    if obs_local_part[0].token_type == 'dot' or (obs_local_part[0].token_type == 'cfws' and len(obs_local_part) > 1 and (obs_local_part[1].token_type == 'dot')):
        obs_local_part.defects.append(错误.InvalidHeaderDefect("Invalid leading '.' in local part"))
    if obs_local_part[-1].token_type == 'dot' or (obs_local_part[-1].token_type == 'cfws' and len(obs_local_part) > 1 and (obs_local_part[-2].token_type == 'dot')):
        obs_local_part.defects.append(错误.InvalidHeaderDefect("Invalid trailing '.' in local part"))
    if obs_local_part.defects:
        obs_local_part.token_type = 'invalid-obs-local-part'
    return (obs_local_part, value)

def get_dtext(value):
    """ dtext = <printable ascii except \\ [ ]> / obs-dtext
        obs-dtext = obs-NO-WS-CTL / quoted-pair

    We allow anything except the excluded characters, but if we find any
    ASCII other than the RFC defined printable ASCII, a NonPrintableDefect is
    added to the token's defects list.  Quoted pairs are converted to their
    unquoted values, so what is returned is a ptext token, in this case a
    ValueTerminal.  If there were quoted-printables, an ObsoleteHeaderDefect is
    added to the returned token's defect list.

    """
    ptext, value, had_qp = _get_ptext_to_endchars(value, '[]')
    ptext = ValueTerminal(ptext, 'ptext')
    if had_qp:
        ptext.defects.append(错误.ObsoleteHeaderDefect('quoted printable found in domain-literal'))
    _validate_xtext(ptext)
    return (ptext, value)

def _check_for_early_dl_end(value, domain_literal):
    if value:
        return False
    domain_literal.defects.append(错误.InvalidHeaderDefect('end of input inside domain-literal'))
    domain_literal.append(ValueTerminal(']', 'domain-literal-end'))
    return True

def 取域名字面量(value):
    """ domain-literal = [CFWS] "[" *([FWS] dtext) [FWS] "]" [CFWS]

    """
    domain_literal = 域名字面量()
    if value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        domain_literal.append(token)
    if not value:
        raise 错误.HeaderParseError('expected domain-literal')
    if value[0] != '[':
        raise 错误.HeaderParseError("expected '[' at start of domain-literal but found '{}'".format(value))
    value = value[1:]
    domain_literal.append(ValueTerminal('[', 'domain-literal-start'))
    if _check_for_early_dl_end(value, domain_literal):
        return (domain_literal, value)
    if value[0] in WSP:
        token, value = 取前导空白(value)
        domain_literal.append(token)
    token, value = get_dtext(value)
    domain_literal.append(token)
    if _check_for_early_dl_end(value, domain_literal):
        return (domain_literal, value)
    if value[0] in WSP:
        token, value = 取前导空白(value)
        domain_literal.append(token)
    if _check_for_early_dl_end(value, domain_literal):
        return (domain_literal, value)
    if value[0] != ']':
        raise 错误.HeaderParseError("expected ']' at end of domain-literal but found '{}'".format(value))
    domain_literal.append(ValueTerminal(']', 'domain-literal-end'))
    value = value[1:]
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        domain_literal.append(token)
    return (domain_literal, value)

def 取域名(value):
    """ domain = dot-atom / domain-literal / obs-domain
        obs-domain = atom *("." atom))

    """
    domain = 域名()
    leader = None
    if value and value[0] in CFWS_LEADER:
        leader, value = 取注释与前导空白(value)
    if not value:
        raise 错误.HeaderParseError("expected domain but found '{}'".format(value))
    if value[0] == '[':
        token, value = 取域名字面量(value)
        if leader is not None:
            token[:0] = [leader]
        domain.append(token)
        return (domain, value)
    try:
        token, value = 取点原子(value)
    except 错误.HeaderParseError:
        token, value = 取原子(value)
    if value and value[0] == '@':
        raise 错误.HeaderParseError('Invalid Domain')
    if leader is not None:
        token[:0] = [leader]
    domain.append(token)
    if value and value[0] == '.':
        domain.defects.append(错误.ObsoleteHeaderDefect('domain is not a dot-atom (contains CFWS)'))
        if domain[0].token_type == 'dot-atom':
            domain[:] = domain[0]
        while value and value[0] == '.':
            domain.append(DOT)
            token, value = 取原子(value[1:])
            domain.append(token)
    return (domain, value)

def 取地址规格(value):
    """ addr-spec = local-part "@" domain

    """
    addr_spec = AddrSpec()
    token, value = 取本地部分(value)
    addr_spec.append(token)
    if not value or value[0] != '@':
        addr_spec.defects.append(错误.InvalidHeaderDefect('addr-spec local part with no domain'))
        return (addr_spec, value)
    addr_spec.append(ValueTerminal('@', 'address-at-symbol'))
    token, value = 取域名(value[1:])
    addr_spec.append(token)
    return (addr_spec, value)

def get_obs_route(value):
    """ obs-route = obs-domain-list ":"
        obs-domain-list = *(CFWS / ",") "@" domain *("," [CFWS] ["@" domain])

        Returns an obs-route token with the appropriate sub-tokens (that is,
        there is no obs-domain-list in the parse tree).
    """
    obs_route = ObsRoute()
    while value and (value[0] == ',' or value[0] in CFWS_LEADER):
        if value[0] in CFWS_LEADER:
            token, value = 取注释与前导空白(value)
            obs_route.append(token)
        elif value[0] == ',':
            obs_route.append(ListSeparator)
            value = value[1:]
    if not value or value[0] != '@':
        raise 错误.HeaderParseError("expected obs-route domain but found '{}'".format(value))
    obs_route.append(RouteComponentMarker)
    token, value = 取域名(value[1:])
    obs_route.append(token)
    while value and value[0] == ',':
        obs_route.append(ListSeparator)
        value = value[1:]
        if not value:
            break
        if value[0] in CFWS_LEADER:
            token, value = 取注释与前导空白(value)
            obs_route.append(token)
        if not value:
            break
        if value[0] == '@':
            obs_route.append(RouteComponentMarker)
            token, value = 取域名(value[1:])
            obs_route.append(token)
    if not value:
        raise 错误.HeaderParseError('end of header while parsing obs-route')
    if value[0] != ':':
        raise 错误.HeaderParseError("expected ':' marking end of obs-route but found '{}'".format(value))
    obs_route.append(ValueTerminal(':', 'end-of-obs-route-marker'))
    return (obs_route, value[1:])

def 取尖括号地址(value):
    """ angle-addr = [CFWS] "<" addr-spec ">" [CFWS] / obs-angle-addr
        obs-angle-addr = [CFWS] "<" obs-route addr-spec ">" [CFWS]

    """
    angle_addr = 尖括号地址()
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        angle_addr.append(token)
    if not value or value[0] != '<':
        raise 错误.HeaderParseError("expected angle-addr but found '{}'".format(value))
    angle_addr.append(ValueTerminal('<', 'angle-addr-start'))
    value = value[1:]
    if value and value[0] == '>':
        angle_addr.append(ValueTerminal('>', 'angle-addr-end'))
        angle_addr.defects.append(错误.InvalidHeaderDefect('null addr-spec in angle-addr'))
        value = value[1:]
        return (angle_addr, value)
    try:
        token, value = 取地址规格(value)
    except 错误.HeaderParseError:
        try:
            token, value = get_obs_route(value)
            angle_addr.defects.append(错误.ObsoleteHeaderDefect('obsolete route specification in angle-addr'))
        except 错误.HeaderParseError:
            raise 错误.HeaderParseError("expected addr-spec or obs-route but found '{}'".format(value))
        angle_addr.append(token)
        token, value = 取地址规格(value)
    angle_addr.append(token)
    if value and value[0] == '>':
        value = value[1:]
    else:
        angle_addr.defects.append(错误.InvalidHeaderDefect("missing trailing '>' on angle-addr"))
    angle_addr.append(ValueTerminal('>', 'angle-addr-end'))
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        angle_addr.append(token)
    return (angle_addr, value)

def 取显示名(value):
    """ display-name = phrase

    Because this is simply a name-rule, we don't return a display-name
    token containing a phrase, but rather a display-name token with
    the content of the phrase.

    """
    display_name = DisplayName()
    token, value = 取短语(value)
    display_name.extend(token[:])
    display_name.defects = token.defects[:]
    return (display_name, value)

def 取具名地址(value):
    """ name-addr = [display-name] angle-addr

    """
    name_addr = 具名地址()
    leader = None
    if not value:
        raise 错误.HeaderParseError("expected name-addr but found '{}'".format(value))
    if value[0] in CFWS_LEADER:
        leader, value = 取注释与前导空白(value)
        if not value:
            raise 错误.HeaderParseError("expected name-addr but found '{}'".format(leader))
    if value[0] != '<':
        if value[0] in PHRASE_ENDS:
            raise 错误.HeaderParseError("expected name-addr but found '{}'".format(value))
        token, value = 取显示名(value)
        if not value:
            raise 错误.HeaderParseError("expected name-addr but found '{}'".format(token))
        if leader is not None:
            if isinstance(token[0], 词法单元表):
                token[0][:0] = [leader]
            else:
                token[:0] = [leader]
            leader = None
        name_addr.append(token)
    token, value = 取尖括号地址(value)
    if leader is not None:
        token[:0] = [leader]
    name_addr.append(token)
    return (name_addr, value)

def 取信箱(value):
    """ mailbox = name-addr / addr-spec

    """
    mailbox = 信箱()
    try:
        token, value = 取具名地址(value)
    except 错误.HeaderParseError:
        try:
            token, value = 取地址规格(value)
        except 错误.HeaderParseError:
            raise 错误.HeaderParseError("expected mailbox but found '{}'".format(value))
    if any((isinstance(x, 错误.InvalidHeaderDefect) for x in token.all_defects)):
        mailbox.token_type = 'invalid-mailbox'
    mailbox.append(token)
    return (mailbox, value)

def get_invalid_mailbox(value, endchars):
    """ Read everything up to one of the chars in endchars.

    This is outside the formal grammar.  The InvalidMailbox TokenList that is
    returned acts like a Mailbox, but the data attributes are None.

    """
    invalid_mailbox = InvalidMailbox()
    while value and value[0] not in endchars:
        if value[0] in PHRASE_ENDS:
            invalid_mailbox.append(ValueTerminal(value[0], 'misplaced-special'))
            value = value[1:]
        else:
            token, value = 取短语(value)
            invalid_mailbox.append(token)
    return (invalid_mailbox, value)

def 取信箱表(value):
    """ mailbox-list = (mailbox *("," mailbox)) / obs-mbox-list
        obs-mbox-list = *([CFWS] ",") mailbox *("," [mailbox / CFWS])

    For this routine we go outside the formal grammar in order to improve error
    handling.  We recognize the end of the mailbox list only at the end of the
    value or at a ';' (the group terminator).  This is so that we can turn
    invalid mailboxes into InvalidMailbox tokens and continue parsing any
    remaining valid mailboxes.  We also allow all mailbox entries to be null,
    and this condition is handled appropriately at a higher level.

    """
    mailbox_list = 信箱表()
    while value and value[0] != ';':
        try:
            token, value = 取信箱(value)
            mailbox_list.append(token)
        except 错误.HeaderParseError:
            leader = None
            if value[0] in CFWS_LEADER:
                leader, value = 取注释与前导空白(value)
                if not value or value[0] in ',;':
                    mailbox_list.append(leader)
                    mailbox_list.defects.append(错误.ObsoleteHeaderDefect('empty element in mailbox-list'))
                else:
                    token, value = get_invalid_mailbox(value, ',;')
                    if leader is not None:
                        token[:0] = [leader]
                    mailbox_list.append(token)
                    mailbox_list.defects.append(错误.InvalidHeaderDefect('invalid mailbox in mailbox-list'))
            elif value[0] == ',':
                mailbox_list.defects.append(错误.ObsoleteHeaderDefect('empty element in mailbox-list'))
            else:
                token, value = get_invalid_mailbox(value, ',;')
                if leader is not None:
                    token[:0] = [leader]
                mailbox_list.append(token)
                mailbox_list.defects.append(错误.InvalidHeaderDefect('invalid mailbox in mailbox-list'))
        if value and value[0] not in ',;':
            mailbox = mailbox_list[-1]
            mailbox.token_type = 'invalid-mailbox'
            token, value = get_invalid_mailbox(value, ',;')
            mailbox.extend(token)
            mailbox_list.defects.append(错误.InvalidHeaderDefect('invalid mailbox in mailbox-list'))
        if value and value[0] == ',':
            mailbox_list.append(ListSeparator)
            value = value[1:]
    return (mailbox_list, value)

def 取地址组表(value):
    """ group-list = mailbox-list / CFWS / obs-group-list
        obs-group-list = 1*([CFWS] ",") [CFWS]

    """
    group_list = 地址组表()
    if not value:
        group_list.defects.append(错误.InvalidHeaderDefect('end of header before group-list'))
        return (group_list, value)
    leader = None
    if value and value[0] in CFWS_LEADER:
        leader, value = 取注释与前导空白(value)
        if not value:
            group_list.defects.append(错误.InvalidHeaderDefect('end of header in group-list'))
            group_list.append(leader)
            return (group_list, value)
        if value[0] == ';':
            group_list.append(leader)
            return (group_list, value)
    token, value = 取信箱表(value)
    if len(token.all_mailboxes) == 0:
        if leader is not None:
            group_list.append(leader)
        group_list.extend(token)
        group_list.defects.append(错误.ObsoleteHeaderDefect('group-list with empty entries'))
        return (group_list, value)
    if leader is not None:
        token[:0] = [leader]
    group_list.append(token)
    return (group_list, value)

def 取地址组(value):
    """ group = display-name ":" [group-list] ";" [CFWS]

    """
    group = 地址组()
    token, value = 取显示名(value)
    if not value or value[0] != ':':
        raise 错误.HeaderParseError("expected ':' at end of group display name but found '{}'".format(value))
    group.append(token)
    group.append(ValueTerminal(':', 'group-display-name-terminator'))
    value = value[1:]
    if value and value[0] == ';':
        group.append(ValueTerminal(';', 'group-terminator'))
        return (group, value[1:])
    token, value = 取地址组表(value)
    group.append(token)
    if not value:
        group.defects.append(错误.InvalidHeaderDefect('end of header in group'))
    elif value[0] != ';':
        raise 错误.HeaderParseError("expected ';' at end of group but found {}".format(value))
    group.append(ValueTerminal(';', 'group-terminator'))
    value = value[1:]
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        group.append(token)
    return (group, value)

def 取地址(value):
    """ address = mailbox / group

    Note that counter-intuitively, an address can be either a single address or
    a list of addresses (a group).  This is why the returned Address object has
    a 'mailboxes' attribute which treats a single address as a list of length
    one.  When you need to differentiate between to two cases, extract the single
    element, which is either a mailbox or a group token.

    """
    address = 地址()
    try:
        token, value = 取地址组(value)
    except 错误.HeaderParseError:
        try:
            token, value = 取信箱(value)
        except 错误.HeaderParseError:
            raise 错误.HeaderParseError("expected address but found '{}'".format(value))
    address.append(token)
    return (address, value)

def 取地址表(value):
    """ address_list = (address *("," address)) / obs-addr-list
        obs-addr-list = *([CFWS] ",") address *("," [address / CFWS])

    We depart from the formal grammar here by continuing to parse until the end
    of the input, assuming the input to be entirely composed of an
    address-list.  This is always true in email parsing, and allows us
    to skip invalid addresses to parse additional valid ones.

    """
    address_list = 地址表()
    while value:
        try:
            token, value = 取地址(value)
            address_list.append(token)
        except 错误.HeaderParseError:
            leader = None
            if value[0] in CFWS_LEADER:
                leader, value = 取注释与前导空白(value)
                if not value or value[0] == ',':
                    address_list.append(leader)
                    address_list.defects.append(错误.ObsoleteHeaderDefect('address-list entry with no content'))
                else:
                    token, value = get_invalid_mailbox(value, ',')
                    if leader is not None:
                        token[:0] = [leader]
                    address_list.append(地址([token]))
                    address_list.defects.append(错误.InvalidHeaderDefect('invalid address in address-list'))
            elif value[0] == ',':
                address_list.defects.append(错误.ObsoleteHeaderDefect('empty element in address-list'))
            else:
                token, value = get_invalid_mailbox(value, ',')
                if leader is not None:
                    token[:0] = [leader]
                address_list.append(地址([token]))
                address_list.defects.append(错误.InvalidHeaderDefect('invalid address in address-list'))
        if value and value[0] != ',':
            token, value = get_invalid_mailbox(value, ',')
            address_list.append(地址([token]))
            address_list.defects.append(错误.InvalidHeaderDefect('invalid address in address-list'))
        if value:
            address_list.append(ListSeparator)
            value = value[1:]
    return (address_list, value)

def get_no_fold_literal(value):
    """ no-fold-literal = "[" *dtext "]"
    """
    no_fold_literal = NoFoldLiteral()
    if not value:
        raise 错误.HeaderParseError("expected no-fold-literal but found '{}'".format(value))
    if value[0] != '[':
        raise 错误.HeaderParseError("expected '[' at the start of no-fold-literal but found '{}'".format(value))
    no_fold_literal.append(ValueTerminal('[', 'no-fold-literal-start'))
    value = value[1:]
    token, value = get_dtext(value)
    no_fold_literal.append(token)
    if not value or value[0] != ']':
        raise 错误.HeaderParseError("expected ']' at the end of no-fold-literal but found '{}'".format(value))
    no_fold_literal.append(ValueTerminal(']', 'no-fold-literal-end'))
    return (no_fold_literal, value[1:])

def 取消息ID(value):
    """msg-id = [CFWS] "<" id-left '@' id-right  ">" [CFWS]
       id-left = dot-atom-text / obs-id-left
       id-right = dot-atom-text / no-fold-literal / obs-id-right
       no-fold-literal = "[" *dtext "]"
    """
    msg_id = MsgID()
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        msg_id.append(token)
    if not value or value[0] != '<':
        raise 错误.HeaderParseError("expected msg-id but found '{}'".format(value))
    msg_id.append(ValueTerminal('<', 'msg-id-start'))
    value = value[1:]
    try:
        token, value = 取点原子文本(value)
    except 错误.HeaderParseError:
        try:
            token, value = get_obs_local_part(value)
            msg_id.defects.append(错误.ObsoleteHeaderDefect('obsolete id-left in msg-id'))
        except 错误.HeaderParseError:
            raise 错误.HeaderParseError("expected dot-atom-text or obs-id-left but found '{}'".format(value))
    msg_id.append(token)
    if not value or value[0] != '@':
        msg_id.defects.append(错误.InvalidHeaderDefect('msg-id with no id-right'))
        if value and value[0] == '>':
            msg_id.append(ValueTerminal('>', 'msg-id-end'))
            value = value[1:]
        return (msg_id, value)
    msg_id.append(ValueTerminal('@', 'address-at-symbol'))
    value = value[1:]
    try:
        token, value = 取点原子文本(value)
    except 错误.HeaderParseError:
        try:
            token, value = get_no_fold_literal(value)
        except 错误.HeaderParseError:
            try:
                token, value = 取域名(value)
                msg_id.defects.append(错误.ObsoleteHeaderDefect('obsolete id-right in msg-id'))
            except 错误.HeaderParseError:
                raise 错误.HeaderParseError("expected dot-atom-text, no-fold-literal or obs-id-right but found '{}'".format(value))
    msg_id.append(token)
    if value and value[0] == '>':
        value = value[1:]
    else:
        msg_id.defects.append(错误.InvalidHeaderDefect("missing trailing '>' on msg-id"))
    msg_id.append(ValueTerminal('>', 'msg-id-end'))
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        msg_id.append(token)
    return (msg_id, value)

def 解析消息ID(value):
    """message-id      =   "Message-ID:" msg-id CRLF
    """
    message_id = 消息ID()
    try:
        token, value = 取消息ID(value)
        message_id.append(token)
    except 错误.HeaderParseError as ex:
        token = 取非结构化值(value)
        message_id = InvalidMessageID(token)
        message_id.defects.append(错误.InvalidHeaderDefect('Invalid msg-id: {!r}'.format(ex)))
    else:
        if value:
            message_id.defects.append(错误.InvalidHeaderDefect('Unexpected {!r}'.format(value)))
    return message_id

def 解析消息ID表(value):
    """in-reply-to     =   "In-Reply-To:" 1*msg-id CRLF
       references      =   "References:" 1*msg-id CRLF
    """
    message_id_list = MessageIDList()
    while value:
        if value[0] == ',':
            message_id_list.defects.append(错误.InvalidHeaderDefect('comma in msg-id list'))
            message_id_list.append(WhiteSpaceTerminal(' ', 'invalid-comma-replacement'))
            value = value[1:]
            continue
        try:
            token, value = 取消息ID(value)
            message_id_list.append(token)
        except 错误.HeaderParseError as ex:
            token = 取非结构化值(value)
            message_id_list.append(InvalidMessageID(token))
            message_id_list.defects.append(错误.InvalidHeaderDefect('Invalid msg-id: {!r}'.format(ex)))
            break
    return message_id_list

def 解析MIME版本(value):
    """ mime-version = [CFWS] 1*digit [CFWS] "." [CFWS] 1*digit [CFWS]

    """
    mime_version = MIME版本()
    if not value:
        mime_version.defects.append(错误.HeaderMissingRequiredValue('Missing MIME version number (eg: 1.0)'))
        return mime_version
    if value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        mime_version.append(token)
        if not value:
            mime_version.defects.append(错误.HeaderMissingRequiredValue('Expected MIME version number but found only CFWS'))
    digits = ''
    while value and value[0] != '.' and (value[0] not in CFWS_LEADER):
        digits += value[0]
        value = value[1:]
    if not digits.isdigit():
        mime_version.defects.append(错误.InvalidHeaderDefect('Expected MIME major version number but found {!r}'.format(digits)))
        mime_version.append(ValueTerminal(digits, 'xtext'))
    else:
        mime_version.major = int(digits)
        mime_version.append(ValueTerminal(digits, 'digits'))
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        mime_version.append(token)
    if not value or value[0] != '.':
        if mime_version.major is not None:
            mime_version.defects.append(错误.InvalidHeaderDefect('Incomplete MIME version; found only major number'))
        if value:
            mime_version.append(ValueTerminal(value, 'xtext'))
        return mime_version
    mime_version.append(ValueTerminal('.', 'version-separator'))
    value = value[1:]
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        mime_version.append(token)
    if not value:
        if mime_version.major is not None:
            mime_version.defects.append(错误.InvalidHeaderDefect('Incomplete MIME version; found only major number'))
        return mime_version
    digits = ''
    while value and value[0] not in CFWS_LEADER:
        digits += value[0]
        value = value[1:]
    if not digits.isdigit():
        mime_version.defects.append(错误.InvalidHeaderDefect('Expected MIME minor version number but found {!r}'.format(digits)))
        mime_version.append(ValueTerminal(digits, 'xtext'))
    else:
        mime_version.minor = int(digits)
        mime_version.append(ValueTerminal(digits, 'digits'))
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        mime_version.append(token)
    if value:
        mime_version.defects.append(错误.InvalidHeaderDefect('Excess non-CFWS text after MIME version'))
        mime_version.append(ValueTerminal(value, 'xtext'))
    return mime_version

def get_invalid_parameter(value):
    """ Read everything up to the next ';'.

    This is outside the formal grammar.  The InvalidParameter TokenList that is
    returned acts like a Parameter, but the data attributes are None.

    """
    invalid_parameter = InvalidParameter()
    while value and value[0] != ';':
        if value[0] in PHRASE_ENDS:
            invalid_parameter.append(ValueTerminal(value[0], 'misplaced-special'))
            value = value[1:]
        else:
            token, value = 取短语(value)
            invalid_parameter.append(token)
    return (invalid_parameter, value)

def get_ttext(value):
    """ttext = <matches _ttext_matcher>

    We allow any non-TOKEN_ENDS in ttext, but add defects to the token's
    defects list if we find non-ttext characters.  We also register defects for
    *any* non-printables even though the RFC doesn't exclude all of them,
    because we follow the spirit of RFC 5322.

    """
    m = _non_token_end_matcher(value)
    if not m:
        raise 错误.HeaderParseError("expected ttext but found '{}'".format(value))
    ttext = m.group()
    value = value[len(ttext):]
    ttext = ValueTerminal(ttext, 'ttext')
    _validate_xtext(ttext)
    return (ttext, value)

def get_token(value):
    """token = [CFWS] 1*ttext [CFWS]

    The RFC equivalent of ttext is any US-ASCII chars except space, ctls, or
    tspecials.  We also exclude tabs even though the RFC doesn't.

    The RFC implies the CFWS but is not explicit about it in the BNF.

    """
    mtoken = 词法单元()
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        mtoken.append(token)
    if value and value[0] in TOKEN_ENDS:
        raise 错误.HeaderParseError("expected token but found '{}'".format(value))
    token, value = get_ttext(value)
    mtoken.append(token)
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        mtoken.append(token)
    return (mtoken, value)

def get_attrtext(value):
    """attrtext = 1*(any non-ATTRIBUTE_ENDS character)

    We allow any non-ATTRIBUTE_ENDS in attrtext, but add defects to the
    token's defects list if we find non-attrtext characters.  We also register
    defects for *any* non-printables even though the RFC doesn't exclude all of
    them, because we follow the spirit of RFC 5322.

    """
    m = _non_attribute_end_matcher(value)
    if not m:
        raise 错误.HeaderParseError('expected attrtext but found {!r}'.format(value))
    attrtext = m.group()
    value = value[len(attrtext):]
    attrtext = ValueTerminal(attrtext, 'attrtext')
    _validate_xtext(attrtext)
    return (attrtext, value)

def get_attribute(value):
    """ [CFWS] 1*attrtext [CFWS]

    This version of the BNF makes the CFWS explicit, and as usual we use a
    value terminal for the actual run of characters.  The RFC equivalent of
    attrtext is the token characters, with the subtraction of '*', "'", and '%'.
    We include tab in the excluded set just as we do for token.

    """
    attribute = 属性()
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        attribute.append(token)
    if value and value[0] in ATTRIBUTE_ENDS:
        raise 错误.HeaderParseError("expected token but found '{}'".format(value))
    token, value = get_attrtext(value)
    attribute.append(token)
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        attribute.append(token)
    return (attribute, value)

def get_extended_attrtext(value):
    """attrtext = 1*(any non-ATTRIBUTE_ENDS character plus '%')

    This is a special parsing routine so that we get a value that
    includes % escapes as a single string (which we decode as a single
    string later).

    """
    m = _non_extended_attribute_end_matcher(value)
    if not m:
        raise 错误.HeaderParseError('expected extended attrtext but found {!r}'.format(value))
    attrtext = m.group()
    value = value[len(attrtext):]
    attrtext = ValueTerminal(attrtext, 'extended-attrtext')
    _validate_xtext(attrtext)
    return (attrtext, value)

def get_extended_attribute(value):
    """ [CFWS] 1*extended_attrtext [CFWS]

    This is like the non-extended version except we allow % characters, so that
    we can pick up an encoded value as a single string.

    """
    attribute = 属性()
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        attribute.append(token)
    if value and value[0] in EXTENDED_ATTRIBUTE_ENDS:
        raise 错误.HeaderParseError("expected token but found '{}'".format(value))
    token, value = get_extended_attrtext(value)
    attribute.append(token)
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        attribute.append(token)
    return (attribute, value)

def get_section(value):
    """ '*' digits

    The formal BNF is more complicated because leading 0s are not allowed.  We
    check for that and add a defect.  We also assume no CFWS is allowed between
    the '*' and the digits, though the RFC is not crystal clear on that.
    The caller should already have dealt with leading CFWS.

    """
    section = Section()
    if not value or value[0] != '*':
        raise 错误.HeaderParseError('Expected section but found {}'.format(value))
    section.append(ValueTerminal('*', 'section-marker'))
    value = value[1:]
    if not value or not value[0].isdigit():
        raise 错误.HeaderParseError('Expected section number but found {}'.format(value))
    digits = ''
    while value and value[0].isdigit():
        digits += value[0]
        value = value[1:]
    if digits[0] == '0' and digits != '0':
        section.defects.append(错误.InvalidHeaderDefect('section number has an invalid leading 0'))
    section.number = int(digits)
    section.append(ValueTerminal(digits, 'digits'))
    return (section, value)

def get_value(value):
    """ quoted-string / attribute

    """
    v = 值()
    if not value:
        raise 错误.HeaderParseError('Expected value but found end of string')
    leader = None
    if value[0] in CFWS_LEADER:
        leader, value = 取注释与前导空白(value)
    if not value:
        raise 错误.HeaderParseError('Expected value but found only {}'.format(leader))
    if value[0] == '"':
        token, value = 取引号串(value)
    else:
        token, value = get_extended_attribute(value)
    if leader is not None:
        token[:0] = [leader]
    v.append(token)
    return (v, value)

def get_parameter(value):
    """ attribute [section] ["*"] [CFWS] "=" value

    The CFWS is implied by the RFC but not made explicit in the BNF.  This
    simplified form of the BNF from the RFC is made to conform with the RFC BNF
    through some extra checks.  We do it this way because it makes both error
    recovery and working with the resulting parse tree easier.
    """
    param = 参数()
    token, value = get_attribute(value)
    param.append(token)
    if not value or value[0] == ';':
        param.defects.append(错误.InvalidHeaderDefect('Parameter contains name ({}) but no value'.format(token)))
        return (param, value)
    if value[0] == '*':
        try:
            token, value = get_section(value)
            param.sectioned = True
            param.append(token)
        except 错误.HeaderParseError:
            pass
        if not value:
            raise 错误.HeaderParseError('Incomplete parameter')
        if value[0] == '*':
            param.append(ValueTerminal('*', 'extended-parameter-marker'))
            value = value[1:]
            param.extended = True
    if value[0] != '=':
        raise 错误.HeaderParseError("Parameter not followed by '='")
    param.append(ValueTerminal('=', 'parameter-separator'))
    value = value[1:]
    if value and value[0] in CFWS_LEADER:
        token, value = 取注释与前导空白(value)
        param.append(token)
    remainder = None
    appendto = param
    if param.extended and value and (value[0] == '"'):
        qstring, remainder = 取引号串(value)
        inner_value = qstring.stripped_value
        semi_valid = False
        if param.section_number == 0:
            if inner_value and inner_value[0] == "'":
                semi_valid = True
            else:
                token, rest = get_attrtext(inner_value)
                if rest and rest[0] == "'":
                    semi_valid = True
        else:
            try:
                token, rest = get_extended_attrtext(inner_value)
            except:
                pass
            else:
                if not rest:
                    semi_valid = True
        if semi_valid:
            param.defects.append(错误.InvalidHeaderDefect('Quoted string value for extended parameter is invalid'))
            param.append(qstring)
            for t in qstring:
                if t.token_type == 'bare-quoted-string':
                    t[:] = []
                    appendto = t
                    break
            value = inner_value
        else:
            remainder = None
            param.defects.append(错误.InvalidHeaderDefect('Parameter marked as extended but appears to have a quoted string value that is non-encoded'))
    if value and value[0] == "'":
        token = None
    else:
        token, value = get_value(value)
    if not param.extended or param.section_number > 0:
        if not value or value[0] != "'":
            appendto.append(token)
            if remainder is not None:
                assert not value, value
                value = remainder
            return (param, value)
        param.defects.append(错误.InvalidHeaderDefect('Apparent initial-extended-value but attribute was not marked as extended or was not initial section'))
    if not value:
        param.defects.append(错误.InvalidHeaderDefect('Missing required charset/lang delimiters'))
        appendto.append(token)
        if remainder is None:
            return (param, value)
    else:
        if token is not None:
            for t in token:
                if t.token_type == 'extended-attrtext':
                    break
            t.token_type == 'attrtext'
            appendto.append(t)
            param.charset = t.value
        if value[0] != "'":
            raise 错误.HeaderParseError('Expected RFC2231 char/lang encoding delimiter, but found {!r}'.format(value))
        appendto.append(ValueTerminal("'", 'RFC2231-delimiter'))
        value = value[1:]
        if value and value[0] != "'":
            token, value = get_attrtext(value)
            appendto.append(token)
            param.lang = token.value
            if not value or value[0] != "'":
                raise 错误.HeaderParseError('Expected RFC2231 char/lang encoding delimiter, but found {}'.format(value))
        appendto.append(ValueTerminal("'", 'RFC2231-delimiter'))
        value = value[1:]
    if remainder is not None:
        v = 值()
        while value:
            if value[0] in WSP:
                token, value = 取前导空白(value)
            elif value[0] == '"':
                token = ValueTerminal('"', 'DQUOTE')
                value = value[1:]
            else:
                token, value = 取Q内容(value)
            v.append(token)
        token = v
    else:
        token, value = get_value(value)
    appendto.append(token)
    if remainder is not None:
        assert not value, value
        value = remainder
    return (param, value)

def 解析MIME参数(value):
    """ parameter *( ";" parameter )

    That BNF is meant to indicate this routine should only be called after
    finding and handling the leading ';'.  There is no corresponding rule in
    the formal RFC grammar, but it is more convenient for us for the set of
    parameters to be treated as its own TokenList.

    This is 'parse' routine because it consumes the remaining value, but it
    would never be called to parse a full header.  Instead it is called to
    parse everything after the non-parameter value of a specific MIME header.

    """
    mime_parameters = MIME参数表()
    while value:
        try:
            token, value = get_parameter(value)
            mime_parameters.append(token)
        except 错误.HeaderParseError:
            leader = None
            if value[0] in CFWS_LEADER:
                leader, value = 取注释与前导空白(value)
            if not value:
                mime_parameters.append(leader)
                return mime_parameters
            if value[0] == ';':
                if leader is not None:
                    mime_parameters.append(leader)
                mime_parameters.defects.append(错误.InvalidHeaderDefect('parameter entry with no content'))
            else:
                token, value = get_invalid_parameter(value)
                if leader:
                    token[:0] = [leader]
                mime_parameters.append(token)
                mime_parameters.defects.append(错误.InvalidHeaderDefect('invalid parameter {!r}'.format(token)))
        if value and value[0] != ';':
            param = mime_parameters[-1]
            param.token_type = 'invalid-parameter'
            token, value = get_invalid_parameter(value)
            param.extend(token)
            mime_parameters.defects.append(错误.InvalidHeaderDefect('parameter with invalid trailing text {!r}'.format(token)))
        if value:
            mime_parameters.append(ValueTerminal(';', 'parameter-separator'))
            value = value[1:]
    return mime_parameters

def _find_mime_parameters(tokenlist, value):
    """Do our best to find the parameters in an invalid MIME header

    """
    while value and value[0] != ';':
        if value[0] in PHRASE_ENDS:
            tokenlist.append(ValueTerminal(value[0], 'misplaced-special'))
            value = value[1:]
        else:
            token, value = 取短语(value)
            tokenlist.append(token)
    if not value:
        return
    tokenlist.append(ValueTerminal(';', 'parameter-separator'))
    tokenlist.append(解析MIME参数(value[1:]))

def 解析内容类型邮件头(value):
    """ maintype "/" subtype *( ";" parameter )

    The maintype and substype are tokens.  Theoretically they could
    be checked against the official IANA list + x-token, but we
    don't do that.
    """
    ctype = 内容类型()
    if not value:
        ctype.defects.append(错误.HeaderMissingRequiredValue('Missing content type specification'))
        return ctype
    try:
        token, value = get_token(value)
    except 错误.HeaderParseError:
        ctype.defects.append(错误.InvalidHeaderDefect('Expected content maintype but found {!r}'.format(value)))
        _find_mime_parameters(ctype, value)
        return ctype
    ctype.append(token)
    if not value or value[0] != '/':
        ctype.defects.append(错误.InvalidHeaderDefect('Invalid content type'))
        if value:
            _find_mime_parameters(ctype, value)
        return ctype
    ctype.maintype = token.value.strip().lower()
    ctype.append(ValueTerminal('/', 'content-type-separator'))
    value = value[1:]
    try:
        token, value = get_token(value)
    except 错误.HeaderParseError:
        ctype.defects.append(错误.InvalidHeaderDefect('Expected content subtype but found {!r}'.format(value)))
        _find_mime_parameters(ctype, value)
        return ctype
    ctype.append(token)
    ctype.subtype = token.value.strip().lower()
    if not value:
        return ctype
    if value[0] != ';':
        ctype.defects.append(错误.InvalidHeaderDefect('Only parameters are valid after content type, but found {!r}'.format(value)))
        del ctype.maintype, ctype.subtype
        _find_mime_parameters(ctype, value)
        return ctype
    ctype.append(ValueTerminal(';', 'parameter-separator'))
    ctype.append(解析MIME参数(value[1:]))
    return ctype

def 解析内容处置邮件头(value):
    """ disposition-type *( ";" parameter )

    """
    disp_header = 内容处置()
    if not value:
        disp_header.defects.append(错误.HeaderMissingRequiredValue('Missing content disposition'))
        return disp_header
    try:
        token, value = get_token(value)
    except 错误.HeaderParseError:
        disp_header.defects.append(错误.InvalidHeaderDefect('Expected content disposition but found {!r}'.format(value)))
        _find_mime_parameters(disp_header, value)
        return disp_header
    disp_header.append(token)
    disp_header.content_disposition = token.value.strip().lower()
    if not value:
        return disp_header
    if value[0] != ';':
        disp_header.defects.append(错误.InvalidHeaderDefect('Only parameters are valid after content disposition, but found {!r}'.format(value)))
        _find_mime_parameters(disp_header, value)
        return disp_header
    disp_header.append(ValueTerminal(';', 'parameter-separator'))
    disp_header.append(解析MIME参数(value[1:]))
    return disp_header

def 解析传输编码邮件头(value):
    """ mechanism

    """
    cte_header = 内容传输编码()
    if not value:
        cte_header.defects.append(错误.HeaderMissingRequiredValue('Missing content transfer encoding'))
        return cte_header
    try:
        token, value = get_token(value)
    except 错误.HeaderParseError:
        cte_header.defects.append(错误.InvalidHeaderDefect('Expected content transfer encoding but found {!r}'.format(value)))
    else:
        cte_header.append(token)
        cte_header.cte = token.value.strip().lower()
    if not value:
        return cte_header
    while value:
        cte_header.defects.append(错误.InvalidHeaderDefect('Extra text after content transfer encoding'))
        if value[0] in PHRASE_ENDS:
            cte_header.append(ValueTerminal(value[0], 'misplaced-special'))
            value = value[1:]
        else:
            token, value = 取短语(value)
            cte_header.append(token)
    return cte_header

def _steal_trailing_WSP_if_exists(lines):
    wsp = ''
    if lines and lines[-1] and (lines[-1][-1] in WSP):
        wsp = lines[-1][-1]
        lines[-1] = lines[-1][:-1]
        if not lines[-1]:
            lines.pop()
    return wsp

def _refold_parse_tree(parse_tree, *, policy):
    """Return string of contents of parse_tree folded according to RFC rules.

    """
    maxlen = policy.max_line_length or sys.maxsize
    encoding = 'utf-8' if policy.utf8 else 'us-ascii'
    lines = ['']
    last_word_is_ew = False
    last_ew = None
    last_charset = None
    wrap_as_ew_blocked = 0
    want_encoding = False
    end_ew_not_allowed = Terminal('', 'wrap_as_ew_blocked')
    parts = list(parse_tree)
    while parts:
        part = parts.pop(0)
        if part is end_ew_not_allowed:
            wrap_as_ew_blocked -= 1
            continue
        tstr = str(part)
        if not want_encoding:
            if part.token_type in ('ptext', 'vtext'):
                want_encoding = not SPECIALSNL.isdisjoint(tstr)
            else:
                want_encoding = not NLSET.isdisjoint(tstr)
        try:
            tstr.encode(encoding)
            charset = encoding
        except UnicodeEncodeError:
            if any((isinstance(x, 错误.UndecodableBytesDefect) for x in part.all_defects)):
                charset = 'unknown-8bit'
            else:
                charset = 'utf-8'
            want_encoding = True
        if part.token_type == 'mime-parameters':
            _fold_mime_parameters(part, lines, maxlen, encoding)
            last_word_is_ew = False
            continue
        if want_encoding and (not wrap_as_ew_blocked):
            if not part.as_ew_allowed:
                want_encoding = False
                last_ew = None
                if part.syntactic_break:
                    encoded_part = part.fold(policy=policy)[:-len(policy.linesep)]
                    if policy.linesep not in encoded_part:
                        if len(encoded_part) > maxlen - len(lines[-1]):
                            newline = _steal_trailing_WSP_if_exists(lines)
                            lines.append(newline)
                        lines[-1] += encoded_part
                        last_word_is_ew = False
                        continue
            if not hasattr(part, 'encode'):
                parts = list(part) + parts
                want_encoding = False
                continue
            elif part.as_ew_allowed:
                if last_ew is not None and charset != last_charset and (last_charset == 'unknown-8bit' or (last_charset == 'utf-8' and charset != 'us-ascii')):
                    last_ew = None
                last_ew = _fold_as_ew(tstr, lines, maxlen, last_ew, part.ew_combine_allowed, charset, last_word_is_ew)
                last_word_is_ew = True
                last_charset = charset
                want_encoding = False
                continue
            else:
                last_ew = None
                want_encoding = False
        if len(tstr) <= maxlen - len(lines[-1]):
            lines[-1] += tstr
            last_word_is_ew = last_word_is_ew and (not bool(tstr.strip(_WSP)))
            continue
        if part.syntactic_break and len(tstr) + 1 <= maxlen:
            newline = _steal_trailing_WSP_if_exists(lines)
            if newline or part.startswith_fws():
                lines.append(newline + tstr)
                last_word_is_ew = last_word_is_ew and (not bool(lines[-1].strip(_WSP)))
                last_ew = None
                continue
        if not hasattr(part, 'encode'):
            newparts = list(part)
            if part.token_type == 'bare-quoted-string':
                newparts = [ValueTerminal('"', 'ptext')] + [ValueTerminal(造引号对(p), 'ptext') for p in newparts] + [ValueTerminal('"', 'ptext')]
            if part.token_type == 'comment':
                newparts = [ValueTerminal('(', 'ptext')] + [ValueTerminal(make_parenthesis_pairs(p), 'ptext') if p.token_type == 'ptext' else p for p in newparts] + [ValueTerminal(')', 'ptext')]
            if not part.as_ew_allowed:
                wrap_as_ew_blocked += 1
                newparts.append(end_ew_not_allowed)
            parts = newparts + parts
            continue
        if part.as_ew_allowed and (not wrap_as_ew_blocked):
            parts.insert(0, part)
            want_encoding = True
            continue
        newline = _steal_trailing_WSP_if_exists(lines)
        if newline or part.startswith_fws():
            lines.append(newline + tstr)
        else:
            lines[-1] += tstr
        last_word_is_ew = last_word_is_ew and (not bool(tstr.strip(_WSP)))
    return policy.linesep.join(lines) + policy.linesep

def _fold_as_ew(to_encode, lines, maxlen, last_ew, ew_combine_allowed, charset, last_word_is_ew):
    """Fold string to_encode into lines as encoded word, combining if allowed.
    Return the new value for last_ew, or None if ew_combine_allowed is False.

    If there is already an encoded word in the last line of lines (indicated by
    a non-None value for last_ew) and ew_combine_allowed is true, decode the
    existing ew, combine it with to_encode, and re-encode.  Otherwise, encode
    to_encode.  In either case, split to_encode as necessary so that the
    encoded segments fit within maxlen.

    """
    if last_ew is not None and ew_combine_allowed:
        to_encode = str(取非结构化值(lines[-1][last_ew:] + to_encode))
        lines[-1] = lines[-1][:last_ew]
    elif last_word_is_ew:
        len_without_wsp = len(lines[-1].rstrip(_WSP))
        leading_whitespace = lines[-1][len_without_wsp:]
        lines[-1] = lines[-1][:len_without_wsp] + (' ' if leading_whitespace else '')
        to_encode = leading_whitespace + to_encode
    elif to_encode[0] in WSP:
        leading_wsp = to_encode[0]
        to_encode = to_encode[1:]
        if len(lines[-1]) == maxlen:
            lines.append(_steal_trailing_WSP_if_exists(lines))
        lines[-1] += leading_wsp
    trailing_wsp = ''
    if to_encode[-1] in WSP:
        trailing_wsp = to_encode[-1]
        to_encode = to_encode[:-1]
    new_last_ew = len(lines[-1]) if last_ew is None else last_ew
    encode_as = 'utf-8' if charset == 'us-ascii' else charset
    chrome_len = len(encode_as) + 7
    if chrome_len + 1 >= maxlen:
        raise 错误.HeaderParseError('max_line_length is too small to fit an encoded word')
    while to_encode:
        remaining_space = maxlen - len(lines[-1])
        text_space = remaining_space - chrome_len
        if text_space <= 0:
            newline = _steal_trailing_WSP_if_exists(lines)
            lines.append(newline or ' ')
            new_last_ew = len(lines[-1])
            continue
        to_encode_word = to_encode[:text_space]
        encoded_word = _ew.encode(to_encode_word, charset=encode_as)
        excess = len(encoded_word) - remaining_space
        while excess > 0:
            to_encode_word = to_encode_word[:-1]
            encoded_word = _ew.encode(to_encode_word, charset=encode_as)
            excess = len(encoded_word) - remaining_space
        lines[-1] += encoded_word
        to_encode = to_encode[len(to_encode_word):]
        if to_encode:
            lines.append(' ')
            new_last_ew = len(lines[-1])
    lines[-1] += trailing_wsp
    return new_last_ew if ew_combine_allowed else None

def _fold_mime_parameters(part, lines, maxlen, encoding):
    """Fold TokenList 'part' into the 'lines' list as mime parameters.

    Using the decoded list of parameters and values, format them according to
    the RFC rules, including using RFC2231 encoding if the value cannot be
    expressed in 'encoding' and/or the parameter+value is too long to fit
    within 'maxlen'.

    """
    for name, value in part.params:
        if not lines[-1].rstrip().endswith(';'):
            lines[-1] += ';'
        charset = encoding
        error_handler = 'strict'
        try:
            value.encode(encoding)
            encoding_required = False
        except UnicodeEncodeError:
            encoding_required = True
            if 工具._has_surrogates(value):
                charset = 'unknown-8bit'
                error_handler = 'surrogateescape'
            else:
                charset = 'utf-8'
        if encoding_required:
            encoded_value = urllib.parse.quote(value, safe='', errors=error_handler)
            tstr = "{}*={}''{}".format(name, charset, encoded_value)
        else:
            tstr = '{}={}'.format(name, 加引号(value))
        if len(lines[-1]) + len(tstr) + 1 < maxlen:
            lines[-1] = lines[-1] + ' ' + tstr
            continue
        elif len(tstr) + 2 <= maxlen:
            lines.append(' ' + tstr)
            continue
        section = 0
        extra_chrome = charset + "''"
        while value:
            chrome_len = len(name) + len(str(section)) + 3 + len(extra_chrome)
            if maxlen <= chrome_len + 3:
                maxlen = 78
            splitpoint = maxchars = maxlen - chrome_len - 2
            while True:
                partial = value[:splitpoint]
                encoded_value = urllib.parse.quote(partial, safe='', errors=error_handler)
                if len(encoded_value) <= maxchars:
                    break
                splitpoint -= 1
            lines.append(' {}*{}*={}{}'.format(name, section, extra_chrome, encoded_value))
            extra_chrome = ''
            section += 1
            value = value[splitpoint:]
            if value:
                lines[-1] += ';'


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Address': '地址',
    'AddressList': '地址表',
    'AngleAddr': '尖括号地址',
    'Atom': '原子',
    'Attribute': '属性',
    'Comment': '注释',
    'ContentDisposition': '内容处置',
    'ContentTransferEncoding': '内容传输编码',
    'ContentType': '内容类型',
    'Domain': '域名',
    'DomainLiteral': '域名字面量',
    'DotAtom': '点原子',
    'EncodedWord': '编码词',
    'Group': '地址组',
    'GroupList': '地址组表',
    'Header': '邮件头',
    'HeaderLabel': '邮件头标签',
    'LocalPart': '本地部分',
    'MIMEVersion': 'MIME版本',
    'Mailbox': '信箱',
    'MailboxList': '信箱表',
    'MessageID': '消息ID',
    'MimeParameters': 'MIME参数表',
    'NameAddr': '具名地址',
    'Parameter': '参数',
    'ParameterizedHeaderValue': '带参数邮件头值',
    'Phrase': '短语',
    'QuotedString': '引号串',
    'Token': '词法单元',
    'TokenList': '词法单元表',
    'UnstructuredTokenList': '非结构化词法单元表',
    'Value': '值',
    'WhiteSpaceTokenList': '空白词法单元表',
    'Word': '词',
    'get_addr_spec': '取地址规格',
    'get_address': '取地址',
    'get_address_list': '取地址表',
    'get_angle_addr': '取尖括号地址',
    'get_atext': '取原子文本',
    'get_atom': '取原子',
    'get_bare_quoted_string': '取裸引号串',
    'get_cfws': '取注释与前导空白',
    'get_comment': '取注释',
    'get_display_name': '取显示名',
    'get_domain': '取域名',
    'get_domain_literal': '取域名字面量',
    'get_dot_atom': '取点原子',
    'get_dot_atom_text': '取点原子文本',
    'get_encoded_word': '取编码词',
    'get_fws': '取前导空白',
    'get_group': '取地址组',
    'get_group_list': '取地址组表',
    'get_local_part': '取本地部分',
    'get_mailbox': '取信箱',
    'get_mailbox_list': '取信箱表',
    'get_msg_id': '取消息ID',
    'get_name_addr': '取具名地址',
    'get_phrase': '取短语',
    'get_qcontent': '取Q内容',
    'get_qp_ctext': '取QP文本',
    'get_quoted_string': '取引号串',
    'get_unstructured': '取非结构化值',
    'get_word': '取词',
    'make_quoted_pairs': '造引号对',
    'parse_content_disposition_header': '解析内容处置邮件头',
    'parse_content_transfer_encoding_header': '解析传输编码邮件头',
    'parse_content_type_header': '解析内容类型邮件头',
    'parse_message_id': '解析消息ID',
    'parse_message_ids': '解析消息ID表',
    'parse_mime_parameters': '解析MIME参数',
    'parse_mime_version': '解析MIME版本',
    'quote_string': '加引号',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
