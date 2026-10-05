# -*- coding: utf-8 -*-
"""唯一标识 —— 汉语库（由 tools/汉化库.py 从 Lib/uuid.py 机械生成，**不要手改**）。

英文库 Lib/uuid.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 唯一标识
"""


"""UUID objects (universally unique identifiers) according to RFC 4122/9562.

This module provides immutable UUID objects (class UUID) and functions for
generating UUIDs corresponding to a specific UUID version as specified in
RFC 4122/9562, e.g., uuid1() for UUID version 1, uuid3() for UUID version 3,
and so on.

Note that UUID version 2 is deliberately omitted as it is outside the scope
of the RFC.

If all you want is a unique ID, you should probably call uuid1() or uuid4().
Note that uuid1() may compromise privacy since it creates a UUID containing
the computer's network address.  uuid4() creates a random UUID.

Typical usage:

    >>> import uuid

    # make a UUID based on the host ID and current time
    >>> uuid.uuid1()    # doctest: +SKIP
    UUID('a8098c1a-f86e-11da-bd1a-00112444be1e')

    # make a UUID using an MD5 hash of a namespace UUID and a name
    >>> uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')
    UUID('6fa459ea-ee8a-3ca4-894e-db77e160355e')

    # make a random UUID
    >>> uuid.uuid4()    # doctest: +SKIP
    UUID('16fd2706-8baf-433b-82eb-8c7fada847da')

    # make a UUID using a SHA-1 hash of a namespace UUID and a name
    >>> uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')
    UUID('886313e1-3b8a-5372-9b90-0c9aee199e5d')

    # make a UUID from a string of hex digits (braces and hyphens ignored)
    >>> x = uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}')

    # convert a UUID to a string of hex digits in standard form
    >>> str(x)
    '00010203-0405-0607-0809-0a0b0c0d0e0f'

    # get the raw 16 bytes of the UUID
    >>> x.bytes
    b'\\x00\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\n\\x0b\\x0c\\r\\x0e\\x0f'

    # make a UUID from a 16-byte string
    >>> uuid.UUID(bytes=x.bytes)
    UUID('00010203-0405-0607-0809-0a0b0c0d0e0f')

    # get the Nil UUID
    >>> uuid.NIL
    UUID('00000000-0000-0000-0000-000000000000')

    # get the Max UUID
    >>> uuid.MAX
    UUID('ffffffff-ffff-ffff-ffff-ffffffffffff')
"""
_英文原名表 = {'MAX': '最大标识', 'NAMESPACE_DNS': '域名命名空间', 'NAMESPACE_OID': '对象标识命名空间', 'NAMESPACE_URL': '网址命名空间', 'NAMESPACE_X500': 'X500命名空间', 'NIL': '空标识', 'SafeUUID': '安全标识', 'UUID': '唯一标识', 'getnode': '取节点号', 'main': '主函数', 'uuid1': '标识1', 'uuid3': '标识3', 'uuid4': '标识4', 'uuid5': '标识5', 'uuid6': '标识6', 'uuid7': '标识7', 'uuid8': '标识8'}

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
import sys
import time
from enum import Enum, _simple_enum
__author__ = 'Ka-Ping Yee <ping@zesty.ca>'
if sys.platform in {'win32', 'darwin', 'emscripten', 'wasi'}:
    _AIX = _LINUX = False
elif sys.platform == 'linux':
    _LINUX = True
    _AIX = False
else:
    import platform
    _platform_system = platform.system()
    _AIX = _platform_system == 'AIX'
    _LINUX = _platform_system in ('Linux', 'Android')
_MAC_DELIM = b':'
_MAC_OMITS_LEADING_ZEROES = False
if _AIX:
    _MAC_DELIM = b'.'
    _MAC_OMITS_LEADING_ZEROES = True
RESERVED_NCS, RFC_4122, RESERVED_MICROSOFT, RESERVED_FUTURE = ['reserved for NCS compatibility', 'specified in RFC 4122', 'reserved for Microsoft compatibility', 'reserved for future definition']
int_ = int
bytes_ = bytes

@_simple_enum(Enum)
class 安全标识:
    safe = 0
    unsafe = -1
    unknown = None
_UINT_128_MAX = (1 << 128) - 1
_RFC_4122_CLEARFLAGS_MASK = ~(61440 << 64 | 49152 << 48)
_RFC_4122_VERSION_1_FLAGS = 1 << 76 | 32768 << 48
_RFC_4122_VERSION_3_FLAGS = 3 << 76 | 32768 << 48
_RFC_4122_VERSION_4_FLAGS = 4 << 76 | 32768 << 48
_RFC_4122_VERSION_5_FLAGS = 5 << 76 | 32768 << 48
_RFC_4122_VERSION_6_FLAGS = 6 << 76 | 32768 << 48
_RFC_4122_VERSION_7_FLAGS = 7 << 76 | 32768 << 48
_RFC_4122_VERSION_8_FLAGS = 8 << 76 | 32768 << 48

class 唯一标识:
    """Instances of the UUID class represent UUIDs as specified in RFC 4122.
    UUID objects are immutable, hashable, and usable as dictionary keys.
    Converting a UUID to a string with str() yields something in the form
    '12345678-1234-1234-1234-123456789abc'.  The UUID constructor accepts
    five possible forms: a similar string of hexadecimal digits, or a tuple
    of six integer fields (with 32-bit, 16-bit, 16-bit, 8-bit, 8-bit, and
    48-bit values respectively) as an argument named 'fields', or a string
    of 16 bytes (with all the integer fields in big-endian order) as an
    argument named 'bytes', or a string of 16 bytes (with the first three
    fields in little-endian order) as an argument named 'bytes_le', or a
    single 128-bit integer as an argument named 'int'.

    UUIDs have these read-only attributes:

        bytes       the UUID as a 16-byte string (containing the six
                    integer fields in big-endian byte order)

        bytes_le    the UUID as a 16-byte string (with time_low, time_mid,
                    and time_hi_version in little-endian byte order)

        fields      a tuple of the six integer fields of the UUID,
                    which are also available as six individual attributes
                    and two derived attributes. Those attributes are not
                    always relevant to all UUID versions:

                        The 'time_*' attributes are only relevant to version 1.

                        The 'clock_seq*' and 'node' attributes are only relevant
                        to versions 1 and 6.

                        The 'time' attribute is only relevant to versions 1, 6
                        and 7.

            time_low                the first 32 bits of the UUID
            time_mid                the next 16 bits of the UUID
            time_hi_version         the next 16 bits of the UUID
            clock_seq_hi_variant    the next 8 bits of the UUID
            clock_seq_low           the next 8 bits of the UUID
            node                    the last 48 bits of the UUID

            time                    the 60-bit timestamp for UUIDv1/v6,
                                    or the 48-bit timestamp for UUIDv7
            clock_seq               the 14-bit sequence number

        hex         the UUID as a 32-character hexadecimal string

        int         the UUID as a 128-bit integer

        urn         the UUID as a URN as specified in RFC 4122/9562

        variant     the UUID variant (one of the constants RESERVED_NCS,
                    RFC_4122, RESERVED_MICROSOFT, or RESERVED_FUTURE)

        version     the UUID version number (1 through 8, meaningful only
                    when the variant is RFC_4122)

        is_safe     An enum indicating whether the UUID has been generated in
                    a way that is safe for multiprocessing applications, via
                    uuid_generate_time_safe(3).
    """
    __slots__ = ('int', 'is_safe', '__weakref__')

    def __init__(self, hex=None, bytes=None, bytes_le=None, fields=None, int=None, version=None, *, is_safe=安全标识.unknown):
        """Create a UUID from either a string of 32 hexadecimal digits,
        a string of 16 bytes as the 'bytes' argument, a string of 16 bytes
        in little-endian order as the 'bytes_le' argument, a tuple of six
        integers (32-bit time_low, 16-bit time_mid, 16-bit time_hi_version,
        8-bit clock_seq_hi_variant, 8-bit clock_seq_low, 48-bit node) as
        the 'fields' argument, or a single 128-bit integer as the 'int'
        argument.  When a string of hex digits is given, curly braces,
        hyphens, and a URN prefix are all optional.  For example, these
        expressions all yield the same UUID:

        UUID('{12345678-1234-5678-1234-567812345678}')
        UUID('12345678123456781234567812345678')
        UUID('urn:uuid:12345678-1234-5678-1234-567812345678')
        UUID(bytes='\\x12\\x34\\x56\\x78'*4)
        UUID(bytes_le='\\x78\\x56\\x34\\x12\\x34\\x12\\x78\\x56' +
                      '\\x12\\x34\\x56\\x78\\x12\\x34\\x56\\x78')
        UUID(fields=(0x12345678, 0x1234, 0x5678, 0x12, 0x34, 0x567812345678))
        UUID(int=0x12345678123456781234567812345678)

        Exactly one of 'hex', 'bytes', 'bytes_le', 'fields', or 'int' must
        be given.  The 'version' argument is optional; if given, the resulting
        UUID will have its variant and version set according to RFC 4122,
        overriding the given 'hex', 'bytes', 'bytes_le', 'fields', or 'int'.

        is_safe is an enum exposed as an attribute on the instance.  It
        indicates whether the UUID has been generated in a way that is safe
        for multiprocessing applications, via uuid_generate_time_safe(3).
        """
        if [hex, bytes, bytes_le, fields, int].count(None) != 4:
            raise TypeError('one of the hex, bytes, bytes_le, fields, or int arguments must be given')
        if int is not None:
            pass
        elif hex is not None:
            hex = hex.replace('urn:', '').replace('uuid:', '')
            hex = hex.strip('{}').replace('-', '')
            if len(hex) != 32:
                raise ValueError('badly formed hexadecimal UUID string')
            int = int_(hex, 16)
        elif bytes_le is not None:
            if len(bytes_le) != 16:
                raise ValueError('bytes_le is not a 16-char string')
            assert isinstance(bytes_le, bytes_), repr(bytes_le)
            bytes = bytes_le[4 - 1::-1] + bytes_le[6 - 1:4 - 1:-1] + bytes_le[8 - 1:6 - 1:-1] + bytes_le[8:]
            int = int_.from_bytes(bytes)
        elif bytes is not None:
            if len(bytes) != 16:
                raise ValueError('bytes is not a 16-char string')
            assert isinstance(bytes, bytes_), repr(bytes)
            int = int_.from_bytes(bytes)
        elif fields is not None:
            if len(fields) != 6:
                raise ValueError('fields is not a 6-tuple')
            time_low, time_mid, time_hi_version, clock_seq_hi_variant, clock_seq_low, node = fields
            if not 0 <= time_low < 1 << 32:
                raise ValueError('field 1 out of range (need a 32-bit value)')
            if not 0 <= time_mid < 1 << 16:
                raise ValueError('field 2 out of range (need a 16-bit value)')
            if not 0 <= time_hi_version < 1 << 16:
                raise ValueError('field 3 out of range (need a 16-bit value)')
            if not 0 <= clock_seq_hi_variant < 1 << 8:
                raise ValueError('field 4 out of range (need an 8-bit value)')
            if not 0 <= clock_seq_low < 1 << 8:
                raise ValueError('field 5 out of range (need an 8-bit value)')
            if not 0 <= node < 1 << 48:
                raise ValueError('field 6 out of range (need a 48-bit value)')
            时钟序列 = clock_seq_hi_variant << 8 | clock_seq_low
            int = time_low << 96 | time_mid << 80 | time_hi_version << 64 | 时钟序列 << 48 | node
        if not 0 <= int <= _UINT_128_MAX:
            raise ValueError('int is out of range (need a 128-bit value)')
        if version is not None:
            if not 1 <= version <= 8:
                raise ValueError('illegal version number')
            int &= _RFC_4122_CLEARFLAGS_MASK
            int |= 9223372036854775808
            int |= version << 76
        object.__setattr__(self, 'int', int)
        object.__setattr__(self, 'is_safe', is_safe)

    @classmethod
    def _from_int(cls, value):
        """Create a UUID from an integer *value*. Internal use only."""
        assert 0 <= value <= _UINT_128_MAX, repr(value)
        self = object.__new__(cls)
        object.__setattr__(self, 'int', value)
        object.__setattr__(self, 'is_safe', 安全标识.unknown)
        return self

    def __getstate__(self):
        d = {'int': self.int}
        if self.安全吗 != 安全标识.unknown:
            d['is_safe'] = self.安全吗.value
        return d

    def __setstate__(self, state):
        object.__setattr__(self, 'int', state['int'])
        object.__setattr__(self, 'is_safe', 安全标识(state['is_safe']) if 'is_safe' in state else 安全标识.unknown)

    def __eq__(self, other):
        if isinstance(other, 唯一标识):
            return self.int == other.int
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, 唯一标识):
            return self.int < other.int
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, 唯一标识):
            return self.int > other.int
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, 唯一标识):
            return self.int <= other.int
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, 唯一标识):
            return self.int >= other.int
        return NotImplemented

    def __hash__(self):
        return hash(self.int)

    def __int__(self):
        return self.int

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __setattr__(self, name, value):
        raise TypeError('UUID objects are immutable')

    def __str__(self):
        x = self.hex
        return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:]}'

    @property
    def bytes(self):
        return self.int.to_bytes(16)

    @property
    def bytes_le(self):
        bytes = self.bytes
        return bytes[4 - 1::-1] + bytes[6 - 1:4 - 1:-1] + bytes[8 - 1:6 - 1:-1] + bytes[8:]

    @property
    def fields(self):
        return (self.time_low, self.time_mid, self.time_hi_version, self.clock_seq_hi_variant, self.clock_seq_low, self.node)

    @property
    def time_low(self):
        return self.int >> 96

    @property
    def time_mid(self):
        return self.int >> 80 & 65535

    @property
    def time_hi_version(self):
        return self.int >> 64 & 65535

    @property
    def clock_seq_hi_variant(self):
        return self.int >> 56 & 255

    @property
    def clock_seq_low(self):
        return self.int >> 48 & 255

    @property
    def time(self):
        if self.version == 6:
            time_hi = self.int >> 96
            time_lo = self.int >> 64 & 4095
            return time_hi << 28 | self.time_mid << 12 | time_lo
        elif self.version == 7:
            return self.int >> 80
        else:
            time_hi = self.int >> 64 & 4095
            time_lo = self.int >> 96
            return time_hi << 48 | self.time_mid << 32 | time_lo

    @property
    def 时钟序列(self):
        return (self.clock_seq_hi_variant & 63) << 8 | self.clock_seq_low

    @property
    def node(self):
        return self.int & 281474976710655

    @property
    def hex(self):
        return self.bytes.hex()

    @property
    def URN(self):
        return 'urn:uuid:' + str(self)

    @property
    def 变体(self):
        if not self.int & 32768 << 48:
            return RESERVED_NCS
        elif not self.int & 16384 << 48:
            return RFC_4122
        elif not self.int & 8192 << 48:
            return RESERVED_MICROSOFT
        else:
            return RESERVED_FUTURE

    @property
    def version(self):
        if self.变体 == RFC_4122:
            return int(self.int >> 76 & 15)
_装类转发(唯一标识, {'clock_seq': '时钟序列', 'urn': 'URN', 'variant': '变体'}, {'clock_seq': '时钟序列', 'is_safe': '安全吗', 'urn': 'URN', 'variant': '变体'})

def _get_command_stdout(command, *args):
    import io, os, shutil, subprocess
    try:
        path_dirs = os.environ.get('PATH', os.defpath).split(os.pathsep)
        path_dirs.extend(['/sbin', '/usr/sbin'])
        executable = shutil.which(command, path=os.pathsep.join(path_dirs))
        if executable is None:
            return None
        env = dict(os.environ)
        env['LC_ALL'] = 'C'
        if args != ('',):
            command = (executable, *args)
        else:
            command = (executable,)
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env)
        if not proc:
            return None
        stdout, stderr = proc.communicate()
        return io.BytesIO(stdout)
    except (OSError, subprocess.SubprocessError):
        return None

def _is_universal(mac):
    return not mac & 1 << 41

def _find_mac_near_keyword(command, args, keywords, get_word_index):
    """Searches a command's output for a MAC address near a keyword.

    Each line of words in the output is case-insensitively searched for
    any of the given keywords.  Upon a match, get_word_index is invoked
    to pick a word from the line, given the index of the match.  For
    example, lambda i: 0 would get the first word on the line, while
    lambda i: i - 1 would get the word preceding the keyword.
    """
    stdout = _get_command_stdout(command, args)
    if stdout is None:
        return None
    first_local_mac = None
    for line in stdout:
        words = line.lower().rstrip().split()
        for i in range(len(words)):
            if words[i] in keywords:
                try:
                    word = words[get_word_index(i)]
                    mac = int(word.replace(_MAC_DELIM, b''), 16)
                except (ValueError, IndexError):
                    pass
                else:
                    if _is_universal(mac):
                        return mac
                    first_local_mac = first_local_mac or mac
    return first_local_mac or None

def _parse_mac(word):
    parts = word.split(_MAC_DELIM)
    if len(parts) != 6:
        return
    if _MAC_OMITS_LEADING_ZEROES:
        if not all((1 <= len(part) <= 2 for part in parts)):
            return
        hexstr = b''.join((part.rjust(2, b'0') for part in parts))
    else:
        if not all((len(part) == 2 for part in parts)):
            return
        hexstr = b''.join(parts)
    try:
        return int(hexstr, 16)
    except ValueError:
        return

def _find_mac_under_heading(command, args, heading):
    """Looks for a MAC address under a heading in a command's output.

    The first line of words in the output is searched for the given
    heading. Words at the same word index as the heading in subsequent
    lines are then examined to see if they look like MAC addresses.
    """
    stdout = _get_command_stdout(command, args)
    if stdout is None:
        return None
    keywords = stdout.readline().rstrip().split()
    try:
        column_index = keywords.index(heading)
    except ValueError:
        return None
    first_local_mac = None
    for line in stdout:
        words = line.rstrip().split()
        try:
            word = words[column_index]
        except IndexError:
            continue
        mac = _parse_mac(word)
        if mac is None:
            continue
        if _is_universal(mac):
            return mac
        if first_local_mac is None:
            first_local_mac = mac
    return first_local_mac

def _ifconfig_getnode():
    """Get the hardware address on Unix by running ifconfig."""
    keywords = (b'hwaddr', b'ether', b'address:', b'lladdr')
    for args in ('', '-a', '-av'):
        mac = _find_mac_near_keyword('ifconfig', args, keywords, lambda i: i + 1)
        if mac:
            return mac
    return None

def _ip_getnode():
    """Get the hardware address on Unix by running ip."""
    mac = _find_mac_near_keyword('ip', 'link', [b'link/ether'], lambda i: i + 1)
    if mac:
        return mac
    return None

def _arp_getnode():
    """Get the hardware address on Unix by running arp."""
    import os, socket
    if not hasattr(socket, 'gethostbyname'):
        return None
    try:
        ip_addr = socket.gethostbyname(socket.gethostname())
    except OSError:
        return None
    mac = _find_mac_near_keyword('arp', '-an', [os.fsencode(ip_addr)], lambda i: -1)
    if mac:
        return mac
    mac = _find_mac_near_keyword('arp', '-an', [os.fsencode(ip_addr)], lambda i: i + 1)
    if mac:
        return mac
    mac = _find_mac_near_keyword('arp', '-an', [os.fsencode('(%s)' % ip_addr)], lambda i: i + 2)
    if mac:
        return mac
    return None

def _lanscan_getnode():
    """Get the hardware address on Unix by running lanscan."""
    return _find_mac_near_keyword('lanscan', '-ai', [b'lan0'], lambda i: 0)

def _netstat_getnode():
    """Get the hardware address on Unix by running netstat."""
    return _find_mac_under_heading('netstat', '-ian', b'Address')
try:
    import _uuid
    _generate_time_safe = getattr(_uuid, 'generate_time_safe', None)
    _has_stable_extractable_node = _uuid.has_stable_extractable_node
    _UuidCreate = getattr(_uuid, 'UuidCreate', None)
except ImportError:
    _uuid = None
    _generate_time_safe = None
    _has_stable_extractable_node = False
    _UuidCreate = None

def _unix_getnode():
    """Get the hardware address on Unix using the _uuid extension module."""
    if _generate_time_safe and _has_stable_extractable_node:
        uuid_time, _ = _generate_time_safe()
        return 唯一标识(bytes=uuid_time).node

def _windll_getnode():
    """Get the hardware address on Windows using the _uuid extension module."""
    if _UuidCreate and _has_stable_extractable_node:
        uuid_bytes = _UuidCreate()
        return 唯一标识(bytes_le=uuid_bytes).node

def _random_getnode():
    """Get a random node ID."""
    return int.from_bytes(os.urandom(6)) | 1 << 40
if _LINUX:
    _OS_GETTERS = [_ip_getnode, _ifconfig_getnode]
elif sys.platform == 'darwin':
    _OS_GETTERS = [_ifconfig_getnode, _arp_getnode, _netstat_getnode]
elif sys.platform == 'win32':
    _OS_GETTERS = []
elif _AIX:
    _OS_GETTERS = [_netstat_getnode]
else:
    _OS_GETTERS = [_ifconfig_getnode, _ip_getnode, _arp_getnode, _netstat_getnode, _lanscan_getnode]
if os.name == 'posix':
    _GETTERS = [_unix_getnode] + _OS_GETTERS
elif os.name == 'nt':
    _GETTERS = [_windll_getnode] + _OS_GETTERS
else:
    _GETTERS = _OS_GETTERS
_node = None

def 取节点号():
    """Get the hardware address as a 48-bit positive integer.

    The first time this runs, it may launch a separate program, which could
    be quite slow.  If all attempts to obtain the hardware address fail, we
    choose a random 48-bit number with its eighth bit set to 1 as recommended
    in RFC 4122.
    """
    global _node
    if _node is not None:
        return _node
    for getter in _GETTERS + [_random_getnode]:
        try:
            _node = getter()
        except:
            continue
        if _node is not None and 0 <= _node < 1 << 48:
            return _node
    assert False, '_random_getnode() returned invalid value: {}'.format(_node)
_last_timestamp = None

def 标识1(node=None, clock_seq=None):
    """Generate a UUID from a host ID, sequence number, and the current time.
    If 'node' is not given, getnode() is used to obtain the hardware
    address.  If 'clock_seq' is given, it is used as the sequence number;
    otherwise a random 14-bit sequence number is chosen."""
    if _generate_time_safe is not None and node is clock_seq is None:
        uuid_time, safely_generated = _generate_time_safe()
        try:
            安全吗 = 安全标识(safely_generated)
        except ValueError:
            安全吗 = 安全标识.unknown
        return 唯一标识(bytes=uuid_time, is_safe=安全吗)
    global _last_timestamp
    nanoseconds = time.time_ns()
    timestamp = nanoseconds // 100 + 122192928000000000
    if _last_timestamp is not None and timestamp <= _last_timestamp:
        timestamp = _last_timestamp + 1
    _last_timestamp = timestamp
    if clock_seq is None:
        import random
        clock_seq = random.getrandbits(14)
    time_low = timestamp & 4294967295
    time_mid = timestamp >> 32 & 65535
    time_hi_version = timestamp >> 48 & 4095
    clock_seq_low = clock_seq & 255
    clock_seq_hi_variant = clock_seq >> 8 & 63
    if node is None:
        node = 取节点号()
    return 唯一标识(fields=(time_low, time_mid, time_hi_version, clock_seq_hi_variant, clock_seq_low, node), version=1)

def 标识3(namespace, name):
    """Generate a UUID from the MD5 hash of a namespace UUID and a name."""
    if isinstance(name, str):
        name = bytes(name, 'utf-8')
    import hashlib
    h = hashlib.md5(namespace.bytes + name, usedforsecurity=False)
    int_uuid_3 = int.from_bytes(h.digest())
    int_uuid_3 &= _RFC_4122_CLEARFLAGS_MASK
    int_uuid_3 |= _RFC_4122_VERSION_3_FLAGS
    return 唯一标识._from_int(int_uuid_3)

def 标识4():
    """Generate a random UUID."""
    int_uuid_4 = int.from_bytes(os.urandom(16))
    int_uuid_4 &= _RFC_4122_CLEARFLAGS_MASK
    int_uuid_4 |= _RFC_4122_VERSION_4_FLAGS
    return 唯一标识._from_int(int_uuid_4)

def 标识5(namespace, name):
    """Generate a UUID from the SHA-1 hash of a namespace UUID and a name."""
    if isinstance(name, str):
        name = bytes(name, 'utf-8')
    import hashlib
    h = hashlib.sha1(namespace.bytes + name, usedforsecurity=False)
    int_uuid_5 = int.from_bytes(h.digest()[:16])
    int_uuid_5 &= _RFC_4122_CLEARFLAGS_MASK
    int_uuid_5 |= _RFC_4122_VERSION_5_FLAGS
    return 唯一标识._from_int(int_uuid_5)
_last_timestamp_v6 = None

def 标识6(node=None, clock_seq=None):
    """Similar to :func:`uuid1` but where fields are ordered differently
    for improved DB locality.

    More precisely, given a 60-bit timestamp value as specified for UUIDv1,
    for UUIDv6 the first 48 most significant bits are stored first, followed
    by the 4-bit version (same position), followed by the remaining 12 bits
    of the original 60-bit timestamp.
    """
    global _last_timestamp_v6
    import time
    nanoseconds = time.time_ns()
    timestamp = nanoseconds // 100 + 122192928000000000
    if _last_timestamp_v6 is not None and timestamp <= _last_timestamp_v6:
        timestamp = _last_timestamp_v6 + 1
    _last_timestamp_v6 = timestamp
    if clock_seq is None:
        import random
        clock_seq = random.getrandbits(14)
    time_hi_and_mid = timestamp >> 12 & 281474976710655
    time_lo = timestamp & 4095
    clock_s = clock_seq & 16383
    if node is None:
        node = 取节点号()
    int_uuid_6 = time_hi_and_mid << 80
    int_uuid_6 |= time_lo << 64
    int_uuid_6 |= clock_s << 48
    int_uuid_6 |= node & 281474976710655
    int_uuid_6 |= _RFC_4122_VERSION_6_FLAGS
    return 唯一标识._from_int(int_uuid_6)
_last_timestamp_v7 = None
_last_counter_v7 = 0

def _uuid7_get_counter_and_tail():
    rand = int.from_bytes(os.urandom(10))
    counter = rand >> 32 & 2199023255551
    tail = rand & 4294967295
    return (counter, tail)

def 标识7():
    """Generate a UUID from a Unix timestamp in milliseconds and random bits.

    UUIDv7 objects feature monotonicity within a millisecond.
    """
    global _last_timestamp_v7
    global _last_counter_v7
    nanoseconds = time.time_ns()
    timestamp_ms = nanoseconds // 1000000
    if _last_timestamp_v7 is None or timestamp_ms > _last_timestamp_v7:
        counter, tail = _uuid7_get_counter_and_tail()
    else:
        if timestamp_ms < _last_timestamp_v7:
            timestamp_ms = _last_timestamp_v7 + 1
        counter = _last_counter_v7 + 1
        if counter > 4398046511103:
            timestamp_ms += 1
            counter, tail = _uuid7_get_counter_and_tail()
        else:
            tail = int.from_bytes(os.urandom(4))
    unix_ts_ms = timestamp_ms & 281474976710655
    counter_msbs = counter >> 30
    counter_hi = counter_msbs & 4095
    counter_lo = counter & 1073741823
    tail &= 4294967295
    int_uuid_7 = unix_ts_ms << 80
    int_uuid_7 |= counter_hi << 64
    int_uuid_7 |= counter_lo << 32
    int_uuid_7 |= tail
    int_uuid_7 |= _RFC_4122_VERSION_7_FLAGS
    res = 唯一标识._from_int(int_uuid_7)
    _last_timestamp_v7 = timestamp_ms
    _last_counter_v7 = counter
    return res

def 标识8(a=None, b=None, c=None):
    """Generate a UUID from three custom blocks.

    * 'a' is the first 48-bit chunk of the UUID (octets 0-5);
    * 'b' is the mid 12-bit chunk (octets 6-7);
    * 'c' is the last 62-bit chunk (octets 8-15).

    When a value is not specified, a pseudo-random value is generated.
    """
    if a is None:
        import random
        a = random.getrandbits(48)
    if b is None:
        import random
        b = random.getrandbits(12)
    if c is None:
        import random
        c = random.getrandbits(62)
    int_uuid_8 = (a & 281474976710655) << 80
    int_uuid_8 |= (b & 4095) << 64
    int_uuid_8 |= c & 4611686018427387903
    int_uuid_8 |= _RFC_4122_VERSION_8_FLAGS
    return 唯一标识._from_int(int_uuid_8)

def 主函数():
    """Run the uuid command line interface."""
    uuid_funcs = {'uuid1': 标识1, 'uuid3': 标识3, 'uuid4': 标识4, 'uuid5': 标识5, 'uuid6': 标识6, 'uuid7': 标识7, 'uuid8': 标识8}
    uuid_namespace_funcs = ('uuid3', 'uuid5')
    namespaces = {'@dns': 域名命名空间, '@url': 网址命名空间, '@oid': 对象标识命名空间, '@x500': X500命名空间}
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='Generate a UUID using the selected UUID function.', color=True)
    parser.add_argument('-u', '--uuid', choices=uuid_funcs.keys(), default='uuid4', help='function to generate the UUID')
    parser.add_argument('-n', '--namespace', metavar=f"{{any UUID,{','.join(namespaces)}}}", help='uuid3/uuid5 only: a UUID, or a well-known predefined UUID addressed by namespace name')
    parser.add_argument('-N', '--name', help='uuid3/uuid5 only: name used as part of generating the UUID')
    parser.add_argument('-C', '--count', metavar='NUM', type=int, default=1, help='generate NUM fresh UUIDs')
    args = parser.parse_args()
    uuid_func = uuid_funcs[args.uuid]
    namespace = args.namespace
    name = args.name
    if args.uuid in uuid_namespace_funcs:
        if not namespace or not name:
            parser.error(f"Incorrect number of arguments. {args.uuid} requires a namespace and a name. Run 'python -m uuid -h' for more information.")
        if namespace in namespaces:
            namespace = namespaces[namespace]
        else:
            try:
                namespace = 唯一标识(namespace)
            except ValueError as exc:
                parser.error(f'{exc}: {args.namespace!r}')
        for _ in range(args.count):
            print(uuid_func(namespace, name))
    else:
        for _ in range(args.count):
            print(uuid_func())
域名命名空间 = 唯一标识('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
网址命名空间 = 唯一标识('6ba7b811-9dad-11d1-80b4-00c04fd430c8')
对象标识命名空间 = 唯一标识('6ba7b812-9dad-11d1-80b4-00c04fd430c8')
X500命名空间 = 唯一标识('6ba7b814-9dad-11d1-80b4-00c04fd430c8')
空标识 = 唯一标识('00000000-0000-0000-0000-000000000000')
最大标识 = 唯一标识('ffffffff-ffff-ffff-ffff-ffffffffffff')
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
    'MAX': '最大标识',
    'NAMESPACE_DNS': '域名命名空间',
    'NAMESPACE_OID': '对象标识命名空间',
    'NAMESPACE_URL': '网址命名空间',
    'NAMESPACE_X500': 'X500命名空间',
    'NIL': '空标识',
    'SafeUUID': '安全标识',
    'UUID': '唯一标识',
    'getnode': '取节点号',
    'main': '主函数',
    'uuid1': '标识1',
    'uuid3': '标识3',
    'uuid4': '标识4',
    'uuid5': '标识5',
    'uuid6': '标识6',
    'uuid7': '标识7',
    'uuid8': '标识8',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '唯一标识': {
        'clock_seq': '时钟序列',
        'urn': 'URN',
        'variant': '变体',
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
    '唯一标识': {
        'clock_seq': '时钟序列',
        'is_safe': '安全吗',
        'urn': 'URN',
        'variant': '变体',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
