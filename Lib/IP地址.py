# -*- coding: utf-8 -*-
"""IP地址 —— 汉语库（由 tools/汉化库.py 从 Lib/ipaddress.py 机械生成，**不要手改**）。

英文库 Lib/ipaddress.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py IP地址
"""


"""A fast, lightweight IPv4/IPv6 manipulation library in Python.

This library is used to create/poke/manipulate IPv4 and IPv6 addresses
and networks.

"""
_英文原名表 = {'AddressValueError': '地址值错误', 'IPV4LENGTH': 'IPv4地址位数', 'IPV6LENGTH': 'IPv6地址位数', 'IPv4Address': 'IPv4地址', 'IPv4Interface': 'IPv4接口', 'IPv4Network': 'IPv4网络', 'IPv6Address': 'IPv6地址', 'IPv6Interface': 'IPv6接口', 'IPv6Network': 'IPv6网络', 'NetmaskValueError': '掩码值错误', 'collapse_addresses': '合并地址块', 'get_mixed_type_key': '混合类型排序键', 'ip_address': '取IP地址', 'ip_interface': '取IP接口', 'ip_network': '取IP网络', 'summarize_address_range': '汇总地址范围', 'v4_int_to_packed': 'IPv4整数转字节', 'v6_int_to_packed': 'IPv6整数转字节'}

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
__version__ = '1.0'
import functools
IPv4地址位数 = 32
IPv6地址位数 = 128

class 地址值错误(ValueError):
    """A Value Error related to the address."""

class 掩码值错误(ValueError):
    """A Value Error related to the netmask."""

def 取IP地址(address):
    """Take an IP string/int and return an object of the correct type.

    Args:
        address: A string or integer, the IP address.  Either IPv4 or
          IPv6 addresses may be supplied; integers less than 2**32 will
          be considered to be IPv4 by default.

    Returns:
        An IPv4Address or IPv6Address object.

    Raises:
        ValueError: if the *address* passed isn't either a v4 or a v6
          address

    """
    try:
        return IPv4地址(address)
    except (地址值错误, 掩码值错误):
        pass
    try:
        return IPv6地址(address)
    except (地址值错误, 掩码值错误):
        pass
    raise ValueError(f'{address!r} does not appear to be an IPv4 or IPv6 address')

def 取IP网络(address, strict=True):
    """Take an IP string/int and return an object of the correct type.

    Args:
        address: A string or integer, the IP network.  Either IPv4 or
          IPv6 networks may be supplied; integers less than 2**32 will
          be considered to be IPv4 by default.

    Returns:
        An IPv4Network or IPv6Network object.

    Raises:
        ValueError: if the string passed isn't either a v4 or a v6
          address. Or if the network has host bits set.

    """
    try:
        return IPv4网络(address, strict)
    except (地址值错误, 掩码值错误):
        pass
    try:
        return IPv6网络(address, strict)
    except (地址值错误, 掩码值错误):
        pass
    raise ValueError(f'{address!r} does not appear to be an IPv4 or IPv6 network')

def 取IP接口(address):
    """Take an IP string/int and return an object of the correct type.

    Args:
        address: A string or integer, the IP address.  Either IPv4 or
          IPv6 addresses may be supplied; integers less than 2**32 will
          be considered to be IPv4 by default.

    Returns:
        An IPv4Interface or IPv6Interface object.

    Raises:
        ValueError: if the string passed isn't either a v4 or a v6
          address.

    Notes:
        The IPv?Interface classes describe an Address on a particular
        Network, so they're basically a combination of both the Address
        and Network classes.

    """
    try:
        return IPv4接口(address)
    except (地址值错误, 掩码值错误):
        pass
    try:
        return IPv6接口(address)
    except (地址值错误, 掩码值错误):
        pass
    raise ValueError(f'{address!r} does not appear to be an IPv4 or IPv6 interface')

def IPv4整数转字节(address):
    """Represent an address as 4 packed bytes in network (big-endian) order.

    Args:
        address: An integer representation of an IPv4 IP address.

    Returns:
        The integer address packed as 4 bytes in network (big-endian) order.

    Raises:
        ValueError: If the integer is negative or too large to be an
          IPv4 IP address.

    """
    try:
        return address.to_bytes(4)
    except OverflowError:
        raise ValueError('Address negative or too large for IPv4')

def IPv6整数转字节(address):
    """Represent an address as 16 packed bytes in network (big-endian) order.

    Args:
        address: An integer representation of an IPv6 IP address.

    Returns:
        The integer address packed as 16 bytes in network (big-endian) order.

    """
    try:
        return address.to_bytes(16)
    except OverflowError:
        raise ValueError('Address negative or too large for IPv6')

def _split_optional_netmask(address):
    """Helper to split the netmask and raise AddressValueError if needed"""
    addr = str(address).split('/')
    if len(addr) > 2:
        raise 地址值错误(f"Only one '/' permitted in {address!r}")
    return addr

def _find_address_range(addresses):
    """Find a sequence of sorted deduplicated IPv#Address.

    Args:
        addresses: a list of IPv#Address objects.

    Yields:
        A tuple containing the first and last IP addresses in the sequence.

    """
    it = iter(addresses)
    first = last = next(it)
    for 取IP in it:
        if 取IP._ip != last._ip + 1:
            yield (first, last)
            first = 取IP
        last = 取IP
    yield (first, last)

def _count_righthand_zero_bits(number, bits):
    """Count the number of zero bits on the right hand side.

    Args:
        number: an integer.
        bits: maximum number of bits to count.

    Returns:
        The number of zero bits on the right hand side of the number.

    """
    if number == 0:
        return bits
    return min(bits, (~number & number - 1).bit_length())

def 汇总地址范围(first, last):
    """Summarize a network range given the first and last IP addresses.

    Example:
        >>> list(summarize_address_range(IPv4Address('192.0.2.0'),
        ...                              IPv4Address('192.0.2.130')))
        ...                                #doctest: +NORMALIZE_WHITESPACE
        [IPv4Network('192.0.2.0/25'), IPv4Network('192.0.2.128/31'),
         IPv4Network('192.0.2.130/32')]

    Args:
        first: the first IPv4Address or IPv6Address in the range.
        last: the last IPv4Address or IPv6Address in the range.

    Returns:
        An iterator of the summarized IPv(4|6) network objects.

    Raise:
        TypeError:
            If the first and last objects are not IP addresses.
            If the first and last objects are not the same version.
        ValueError:
            If the last object is not greater than the first.
            If the version of the first address is not 4 or 6.

    """
    if not (isinstance(first, _BaseAddress) and isinstance(last, _BaseAddress)):
        raise TypeError('first and last must be IP addresses, not networks')
    if first.version != last.version:
        raise TypeError('%s and %s are not of the same version' % (first, last))
    if first > last:
        raise ValueError('last IP address must be greater than first')
    if first.version == 4:
        取IP = IPv4网络
    elif first.version == 6:
        取IP = IPv6网络
    else:
        raise ValueError('unknown IP version')
    ip_bits = first.max_prefixlen
    first_int = first._ip
    last_int = last._ip
    while first_int <= last_int:
        nbits = min(_count_righthand_zero_bits(first_int, ip_bits), (last_int - first_int + 1).bit_length() - 1)
        net = 取IP((first_int, ip_bits - nbits))
        yield net
        first_int += 1 << nbits
        if first_int - 1 == 取IP._ALL_ONES:
            break

def _collapse_addresses_internal(addresses):
    """Loops through the addresses, collapsing concurrent netblocks.

    Example:

        ip1 = IPv4Network('192.0.2.0/26')
        ip2 = IPv4Network('192.0.2.64/26')
        ip3 = IPv4Network('192.0.2.128/26')
        ip4 = IPv4Network('192.0.2.192/26')

        _collapse_addresses_internal([ip1, ip2, ip3, ip4]) ->
          [IPv4Network('192.0.2.0/24')]

        This shouldn't be called directly; it is called via
          collapse_addresses([]).

    Args:
        addresses: A list of IPv4Network's or IPv6Network's

    Returns:
        A list of IPv4Network's or IPv6Network's depending on what we were
        passed.

    """
    to_merge = list(addresses)
    子网们 = {}
    while to_merge:
        net = to_merge.pop()
        超网 = net.supernet()
        existing = 子网们.get(超网)
        if existing is None:
            子网们[超网] = net
        elif existing != net:
            del 子网们[超网]
            to_merge.append(超网)
    last = None
    for net in sorted(子网们.values()):
        if last is not None:
            if last.broadcast_address >= net.broadcast_address:
                continue
        yield net
        last = net

def 合并地址块(addresses):
    """Collapse a list of IP objects.

    Example:
        collapse_addresses([IPv4Network('192.0.2.0/25'),
                            IPv4Network('192.0.2.128/25')]) ->
                           [IPv4Network('192.0.2.0/24')]

    Args:
        addresses: An iterable of IPv4Network or IPv6Network objects.

    Returns:
        An iterator of the collapsed IPv(4|6)Network objects.

    Raises:
        TypeError: If passed a list of mixed version objects.

    """
    addrs = []
    ips = []
    nets = []
    for 取IP in addresses:
        if isinstance(取IP, _BaseAddress):
            if ips and ips[-1].version != 取IP.version:
                raise TypeError('%s and %s are not of the same version' % (取IP, ips[-1]))
            ips.append(取IP)
        elif 取IP._prefixlen == 取IP.max_prefixlen:
            if ips and ips[-1].version != 取IP.version:
                raise TypeError('%s and %s are not of the same version' % (取IP, ips[-1]))
            try:
                ips.append(取IP.ip)
            except AttributeError:
                ips.append(取IP.network_address)
        else:
            if nets and nets[-1].version != 取IP.version:
                raise TypeError('%s and %s are not of the same version' % (取IP, nets[-1]))
            nets.append(取IP)
    ips = sorted(set(ips))
    if ips:
        for first, last in _find_address_range(ips):
            addrs.extend(汇总地址范围(first, last))
    return _collapse_addresses_internal(addrs + nets)

def 混合类型排序键(obj):
    """Return a key suitable for sorting between networks and addresses.

    Address and Network objects are not sortable by default; they're
    fundamentally different so the expression

        IPv4Address('192.0.2.0') <= IPv4Network('192.0.2.0/24')

    doesn't make any sense.  There are some times however, where you may wish
    to have ipaddress sort these for you anyway. If you need to do this, you
    can use this function as the key= argument to sorted().

    Args:
      obj: either a Network or Address object.
    Returns:
      appropriate key.

    """
    if isinstance(obj, _BaseNetwork):
        return obj._get_networks_key()
    elif isinstance(obj, _BaseAddress):
        return obj._get_address_key()
    return NotImplemented

class _IPAddressBase:
    """The mother class."""
    __slots__ = ()

    @property
    def 完整写法(self):
        """Return the longhand version of the IP address as a string."""
        return self._explode_shorthand_ip_string()

    @property
    def 压缩写法(self):
        """Return the shorthand version of the IP address as a string."""
        return str(self)

    @property
    def 反查指针(self):
        """The name of the reverse DNS pointer for the IP address, e.g.:
            >>> ipaddress.ip_address("127.0.0.1").reverse_pointer
            '1.0.0.127.in-addr.arpa'
            >>> ipaddress.ip_address("2001:db8::1").reverse_pointer
            '1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa'

        """
        return self._reverse_pointer()

    def _check_int_address(self, address):
        if address < 0:
            msg = '%d (< 0) is not permitted as an IPv%d address'
            raise 地址值错误(msg % (address, self.version))
        if address > self._ALL_ONES:
            msg = '%d (>= 2**%d) is not permitted as an IPv%d address'
            raise 地址值错误(msg % (address, self.最大前缀长度, self.version))

    def _check_packed_address(self, address, expected_len):
        address_len = len(address)
        if address_len != expected_len:
            msg = '%r (len %d != %d) is not permitted as an IPv%d address'
            raise 地址值错误(msg % (address, address_len, expected_len, self.version))

    @classmethod
    def _ip_int_from_prefix(cls, prefixlen):
        """Turn the prefix length into a bitwise netmask

        Args:
            prefixlen: An integer, the prefix length.

        Returns:
            An integer.

        """
        return cls._ALL_ONES ^ cls._ALL_ONES >> prefixlen

    @classmethod
    def _prefix_from_ip_int(cls, ip_int):
        """Return prefix length from the bitwise netmask.

        Args:
            ip_int: An integer, the netmask in expanded bitwise format

        Returns:
            An integer, the prefix length.

        Raises:
            ValueError: If the input intermingles zeroes & ones
        """
        trailing_zeroes = _count_righthand_zero_bits(ip_int, cls.最大前缀长度)
        前缀长度 = cls.最大前缀长度 - trailing_zeroes
        leading_ones = ip_int >> trailing_zeroes
        all_ones = (1 << 前缀长度) - 1
        if leading_ones != all_ones:
            byteslen = cls.最大前缀长度 // 8
            details = ip_int.to_bytes(byteslen, 'big')
            msg = 'Netmask pattern %r mixes zeroes & ones'
            raise ValueError(msg % details)
        return 前缀长度

    @classmethod
    def _report_invalid_netmask(cls, netmask_str):
        msg = '%r is not a valid netmask' % netmask_str
        raise 掩码值错误(msg) from None

    @classmethod
    def _prefix_from_prefix_string(cls, prefixlen_str):
        """Return prefix length from a numeric string

        Args:
            prefixlen_str: The string to be converted

        Returns:
            An integer, the prefix length.

        Raises:
            NetmaskValueError: If the input is not a valid netmask
        """
        if not (prefixlen_str.isascii() and prefixlen_str.isdigit()):
            cls._report_invalid_netmask(prefixlen_str)
        try:
            前缀长度 = int(prefixlen_str)
        except ValueError:
            cls._report_invalid_netmask(prefixlen_str)
        if not 0 <= 前缀长度 <= cls.最大前缀长度:
            cls._report_invalid_netmask(prefixlen_str)
        return 前缀长度

    @classmethod
    def _prefix_from_ip_string(cls, ip_str):
        """Turn a netmask/hostmask string into a prefix length

        Args:
            ip_str: The netmask/hostmask to be converted

        Returns:
            An integer, the prefix length.

        Raises:
            NetmaskValueError: If the input is not a valid netmask/hostmask
        """
        try:
            ip_int = cls._ip_int_from_string(ip_str)
        except 地址值错误:
            cls._report_invalid_netmask(ip_str)
        try:
            return cls._prefix_from_ip_int(ip_int)
        except ValueError:
            pass
        ip_int ^= cls._ALL_ONES
        try:
            return cls._prefix_from_ip_int(ip_int)
        except ValueError:
            cls._report_invalid_netmask(ip_str)

    @classmethod
    def _split_addr_prefix(cls, address):
        """Helper function to parse address of Network/Interface.

        Arg:
            address: Argument of Network/Interface.

        Returns:
            (addr, prefix) tuple.
        """
        if isinstance(address, (bytes, int)):
            return (address, cls.最大前缀长度)
        if not isinstance(address, tuple):
            address = _split_optional_netmask(address)
        if len(address) > 1:
            return address
        return (address[0], cls.最大前缀长度)

    def __reduce__(self):
        return (self.__class__, (str(self),))
_装类转发(_IPAddressBase, {'compressed': '压缩写法', 'exploded': '完整写法', 'reverse_pointer': '反查指针'}, {'compressed': '压缩写法', 'exploded': '完整写法', 'max_prefixlen': '最大前缀长度', 'reverse_pointer': '反查指针'})
_address_fmt_re = None

@functools.total_ordering
class _BaseAddress(_IPAddressBase):
    """A generic IP object.

    This IP class contains the version independent methods which are
    used by single IP addresses.
    """
    __slots__ = ()

    def __int__(self):
        return self._ip

    def __eq__(self, other):
        try:
            return self._ip == other._ip and self.version == other.version
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        if not isinstance(other, _BaseAddress):
            return NotImplemented
        if self.version != other.version:
            raise TypeError('%s and %s are not of the same version' % (self, other))
        if self._ip != other._ip:
            return self._ip < other._ip
        return False

    def __add__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return self.__class__(int(self) + other)

    def __sub__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return self.__class__(int(self) - other)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __str__(self):
        return str(self._string_from_ip_int(self._ip))

    def __hash__(self):
        return hash(hex(int(self._ip)))

    def _get_address_key(self):
        return (self.version, self)

    def __reduce__(self):
        return (self.__class__, (self._ip,))

    def __format__(self, fmt):
        """Returns an IP address as a formatted string.

        Supported presentation types are:
        's': returns the IP address as a string (default)
        'b': converts to binary and returns a zero-padded string
        'X' or 'x': converts to upper- or lower-case hex and returns a zero-padded string
        'n': the same as 'b' for IPv4 and 'x' for IPv6

        For binary and hex presentation types, the alternate form specifier
        '#' and the grouping option '_' are supported.
        """
        if not fmt or fmt[-1] == 's':
            return format(str(self), fmt)
        global _address_fmt_re
        if _address_fmt_re is None:
            import re
            _address_fmt_re = re.compile('(#?)(_?)([xbnX])')
        m = _address_fmt_re.fullmatch(fmt)
        if not m:
            return super().__format__(fmt)
        alternate, grouping, fmt_base = m.groups()
        if fmt_base == 'n':
            if self.version == 4:
                fmt_base = 'b'
            else:
                fmt_base = 'x'
        if fmt_base == 'b':
            padlen = self.最大前缀长度
        else:
            padlen = self.最大前缀长度 // 4
        if grouping:
            padlen += padlen // 4 - 1
        if alternate:
            padlen += 2
        return format(int(self), f'{alternate}0{padlen}{grouping}{fmt_base}')
_装类转发(_BaseAddress, {}, {'max_prefixlen': '最大前缀长度'})

@functools.total_ordering
class _BaseNetwork(_IPAddressBase):
    """A generic IP network object.

    This IP class contains the version independent methods which are
    used by networks.
    """

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __str__(self):
        return '%s/%d' % (self.网络地址, self.前缀长度)

    def 主机们(self):
        """Generate Iterator over usable hosts in a network.

        This is like __iter__ except it doesn't return the network
        or broadcast addresses.

        """
        network = int(self.网络地址)
        broadcast = int(self.广播地址)
        for x in range(network + 1, broadcast):
            yield self._address_class(x)

    def __iter__(self):
        network = int(self.网络地址)
        broadcast = int(self.广播地址)
        for x in range(network, broadcast + 1):
            yield self._address_class(x)

    def __getitem__(self, n):
        network = int(self.网络地址)
        broadcast = int(self.广播地址)
        if n >= 0:
            if network + n > broadcast:
                raise IndexError('address out of range')
            return self._address_class(network + n)
        else:
            n += 1
            if broadcast + n < network:
                raise IndexError('address out of range')
            return self._address_class(broadcast + n)

    def __lt__(self, other):
        if not isinstance(other, _BaseNetwork):
            return NotImplemented
        if self.version != other.version:
            raise TypeError('%s and %s are not of the same version' % (self, other))
        if self.网络地址 != other.network_address:
            return self.网络地址 < other.network_address
        if self.网络掩码 != other.netmask:
            return self.网络掩码 < other.netmask
        return False

    def __eq__(self, other):
        try:
            return self.version == other.version and self.网络地址 == other.network_address and (int(self.网络掩码) == int(other.netmask))
        except AttributeError:
            return NotImplemented

    def __hash__(self):
        return hash((int(self.网络地址), int(self.网络掩码)))

    def __contains__(self, other):
        if self.version != other.version:
            return False
        if isinstance(other, _BaseNetwork):
            return False
        else:
            return other._ip & self.网络掩码._ip == self.网络地址._ip

    def 有重叠吗(self, other):
        """Tell if self is partly contained in other."""
        return self.网络地址 in other or (self.广播地址 in other or (other.network_address in self or other.broadcast_address in self))

    @functools.cached_property
    def 广播地址(self):
        return self._address_class(int(self.网络地址) | int(self.主机掩码))

    @functools.cached_property
    def 主机掩码(self):
        return self._address_class(int(self.网络掩码) ^ self._ALL_ONES)

    @property
    def 带前缀长度(self):
        return '%s/%d' % (self.网络地址, self._prefixlen)

    @property
    def 带网络掩码(self):
        return '%s/%s' % (self.网络地址, self.网络掩码)

    @property
    def 带主机掩码(self):
        return '%s/%s' % (self.网络地址, self.主机掩码)

    @property
    def 地址总数(self):
        """Number of hosts in the current subnet."""
        return int(self.广播地址) - int(self.网络地址) + 1

    @property
    def _address_class(self):
        msg = '%200s has no associated address class' % (type(self),)
        raise NotImplementedError(msg)

    @property
    def 前缀长度(self):
        return self._prefixlen

    def 排除地址(self, other):
        """Remove an address from a larger block.

        For example:

            addr1 = ip_network('192.0.2.0/28')
            addr2 = ip_network('192.0.2.1/32')
            list(addr1.address_exclude(addr2)) =
                [IPv4Network('192.0.2.0/32'), IPv4Network('192.0.2.2/31'),
                 IPv4Network('192.0.2.4/30'), IPv4Network('192.0.2.8/29')]

        or IPv6:

            addr1 = ip_network('2001:db8::1/32')
            addr2 = ip_network('2001:db8::1/128')
            list(addr1.address_exclude(addr2)) =
                [ip_network('2001:db8::1/128'),
                 ip_network('2001:db8::2/127'),
                 ip_network('2001:db8::4/126'),
                 ip_network('2001:db8::8/125'),
                 ...
                 ip_network('2001:db8:8000::/33')]

        Args:
            other: An IPv4Network or IPv6Network object of the same type.

        Returns:
            An iterator of the IPv(4|6)Network objects which is self
            minus other.

        Raises:
            TypeError: If self and other are of differing address
              versions, or if other is not a network object.
            ValueError: If other is not completely contained by self.

        """
        if not self.version == other.version:
            raise TypeError('%s and %s are not of the same version' % (self, other))
        if not isinstance(other, _BaseNetwork):
            raise TypeError('%s is not a network object' % other)
        if not other.subnet_of(self):
            raise ValueError('%s not contained in %s' % (other, self))
        if other == self:
            return
        other = other.__class__('%s/%s' % (other.network_address, other.prefixlen))
        s1, s2 = self.子网们()
        while s1 != other and s2 != other:
            if other.subnet_of(s1):
                yield s2
                s1, s2 = s1.subnets()
            elif other.subnet_of(s2):
                yield s1
                s1, s2 = s2.subnets()
            else:
                raise AssertionError('Error performing exclusion: s1: %s s2: %s other: %s' % (s1, s2, other))
        if s1 == other:
            yield s2
        elif s2 == other:
            yield s1
        else:
            raise AssertionError('Error performing exclusion: s1: %s s2: %s other: %s' % (s1, s2, other))

    def 比较网络(self, other):
        """Compare two IP objects.

        This is only concerned about the comparison of the integer
        representation of the network addresses.  This means that the
        host bits aren't considered at all in this method.  If you want
        to compare host bits, you can easily enough do a
        'HostA._ip < HostB._ip'

        Args:
            other: An IP object.

        Returns:
            If the IP versions of self and other are the same, returns:

            -1 if self < other:
              eg: IPv4Network('192.0.2.0/25') < IPv4Network('192.0.2.128/25')
              IPv6Network('2001:db8::1000/124') <
                  IPv6Network('2001:db8::2000/124')
            0 if self == other
              eg: IPv4Network('192.0.2.0/24') == IPv4Network('192.0.2.0/24')
              IPv6Network('2001:db8::1000/124') ==
                  IPv6Network('2001:db8::1000/124')
            1 if self > other
              eg: IPv4Network('192.0.2.128/25') > IPv4Network('192.0.2.0/25')
                  IPv6Network('2001:db8::2000/124') >
                      IPv6Network('2001:db8::1000/124')

          Raises:
              TypeError if the IP versions are different.

        """
        if self.version != other.version:
            raise TypeError('%s and %s are not of the same type' % (self, other))
        if self.网络地址 < other.network_address:
            return -1
        if self.网络地址 > other.network_address:
            return 1
        if self.网络掩码 < other.netmask:
            return -1
        if self.网络掩码 > other.netmask:
            return 1
        return 0

    def _get_networks_key(self):
        """Network-only key function.

        Returns an object that identifies this address' network and
        netmask. This function is a suitable "key" argument for sorted()
        and list.sort().

        """
        return (self.version, self.网络地址, self.网络掩码)

    def 子网们(self, prefixlen_diff=1, new_prefix=None):
        """The subnets which join to make the current subnet.

        In the case that self contains only one IP
        (self._prefixlen == 32 for IPv4 or self._prefixlen == 128
        for IPv6), yield an iterator with just ourself.

        Args:
            prefixlen_diff: An integer, the amount the prefix length
              should be increased by. This should not be set if
              new_prefix is also set.
            new_prefix: The desired new prefix length. This must be a
              larger number (smaller prefix) than the existing prefix.
              This should not be set if prefixlen_diff is also set.

        Returns:
            An iterator of IPv(4|6) objects.

        Raises:
            ValueError: The prefixlen_diff is too small or too large.
                OR
            prefixlen_diff and new_prefix are both set or new_prefix
              is a smaller number than the current prefix (smaller
              number means a larger network)

        """
        if self._prefixlen == self.最大前缀长度:
            yield self
            return
        if new_prefix is not None:
            if new_prefix < self._prefixlen:
                raise ValueError('new prefix must be longer')
            if prefixlen_diff != 1:
                raise ValueError('cannot set prefixlen_diff and new_prefix')
            prefixlen_diff = new_prefix - self._prefixlen
        if prefixlen_diff < 0:
            raise ValueError('prefix length diff must be > 0')
        new_prefixlen = self._prefixlen + prefixlen_diff
        if new_prefixlen > self.最大前缀长度:
            raise ValueError('prefix length diff %d is invalid for netblock %s' % (new_prefixlen, self))
        start = int(self.网络地址)
        end = int(self.广播地址) + 1
        step = int(self.主机掩码) + 1 >> prefixlen_diff
        for new_addr in range(start, end, step):
            current = self.__class__((new_addr, new_prefixlen))
            yield current

    def 超网(self, prefixlen_diff=1, new_prefix=None):
        """The supernet containing the current network.

        Args:
            prefixlen_diff: An integer, the amount the prefix length of
              the network should be decreased by.  For example, given a
              /24 network and a prefixlen_diff of 3, a supernet with a
              /21 netmask is returned.

        Returns:
            An IPv4 network object.

        Raises:
            ValueError: If self.prefixlen - prefixlen_diff < 0. I.e., you have
              a negative prefix length.
                OR
            If prefixlen_diff and new_prefix are both set or new_prefix is a
              larger number than the current prefix (larger number means a
              smaller network)

        """
        if self._prefixlen == 0:
            return self
        if new_prefix is not None:
            if new_prefix > self._prefixlen:
                raise ValueError('new prefix must be shorter')
            if prefixlen_diff != 1:
                raise ValueError('cannot set prefixlen_diff and new_prefix')
            prefixlen_diff = self._prefixlen - new_prefix
        new_prefixlen = self.前缀长度 - prefixlen_diff
        if new_prefixlen < 0:
            raise ValueError('current prefixlen is %d, cannot have a prefixlen_diff of %d' % (self.前缀长度, prefixlen_diff))
        return self.__class__((int(self.网络地址) & int(self.网络掩码) << prefixlen_diff, new_prefixlen))

    @property
    def 是多播吗(self):
        """Test if the address is reserved for multicast use.

        Returns:
            A boolean, True if the address is a multicast address.
            See RFC 2373 2.7 for details.

        """
        return self.网络地址.is_multicast and self.广播地址.is_multicast

    @staticmethod
    def _is_subnet_of(a, b):
        try:
            if a.version != b.version:
                raise TypeError(f'{a} and {b} are not of the same version')
            return b.network_address <= a.network_address and b.broadcast_address >= a.broadcast_address
        except AttributeError:
            raise TypeError(f'Unable to test subnet containment between {a} and {b}')

    def 是其子网吗(self, other):
        """Return True if this network is a subnet of other."""
        return self._is_subnet_of(self, other)

    def 是其超网吗(self, other):
        """Return True if this network is a supernet of other."""
        return self._is_subnet_of(other, self)

    @property
    def 是保留地址吗(self):
        """Test if the address is otherwise IETF reserved.

        Returns:
            A boolean, True if the address is within one of the
            reserved IPv6 Network ranges.

        """
        return self.网络地址.is_reserved and self.广播地址.is_reserved

    @property
    def 是链路本地吗(self):
        """Test if the address is reserved for link-local.

        Returns:
            A boolean, True if the address is reserved per RFC 4291.

        """
        return self.网络地址.is_link_local and self.广播地址.is_link_local

    @property
    def 是私有地址吗(self):
        """Test if this network belongs to a private range.

        Returns:
            A boolean, True if the network is reserved per
            iana-ipv4-special-registry or iana-ipv6-special-registry.

        """
        return any((self.网络地址 in priv_network and self.广播地址 in priv_network for priv_network in self._constants._private_networks)) and all((self.网络地址 not in network and self.广播地址 not in network for network in self._constants._private_networks_exceptions))

    @property
    def 是全球地址吗(self):
        """Test if this address is allocated for public networks.

        Returns:
            A boolean, True if the address is not reserved per
            iana-ipv4-special-registry or iana-ipv6-special-registry.

        """
        return not self.是私有地址吗

    @property
    def 是未指定地址吗(self):
        """Test if the address is unspecified.

        Returns:
            A boolean, True if this is the unspecified address as defined in
            RFC 2373 2.5.2.

        """
        return self.网络地址.is_unspecified and self.广播地址.is_unspecified

    @property
    def 是回环吗(self):
        """Test if the address is a loopback address.

        Returns:
            A boolean, True if the address is a loopback address as defined in
            RFC 2373 2.5.3.

        """
        return self.网络地址.is_loopback and self.广播地址.is_loopback
_装类转发(_BaseNetwork, {'address_exclude': '排除地址', 'broadcast_address': '广播地址', 'compare_networks': '比较网络', 'hostmask': '主机掩码', 'hosts': '主机们', 'is_global': '是全球地址吗', 'is_link_local': '是链路本地吗', 'is_loopback': '是回环吗', 'is_multicast': '是多播吗', 'is_private': '是私有地址吗', 'is_reserved': '是保留地址吗', 'is_unspecified': '是未指定地址吗', 'num_addresses': '地址总数', 'overlaps': '有重叠吗', 'prefixlen': '前缀长度', 'subnet_of': '是其子网吗', 'subnets': '子网们', 'supernet': '超网', 'supernet_of': '是其超网吗', 'with_hostmask': '带主机掩码', 'with_netmask': '带网络掩码', 'with_prefixlen': '带前缀长度'}, {'address_exclude': '排除地址', 'broadcast_address': '广播地址', 'compare_networks': '比较网络', 'hostmask': '主机掩码', 'hosts': '主机们', 'is_global': '是全球地址吗', 'is_link_local': '是链路本地吗', 'is_loopback': '是回环吗', 'is_multicast': '是多播吗', 'is_private': '是私有地址吗', 'is_reserved': '是保留地址吗', 'is_unspecified': '是未指定地址吗', 'max_prefixlen': '最大前缀长度', 'netmask': '网络掩码', 'network_address': '网络地址', 'num_addresses': '地址总数', 'overlaps': '有重叠吗', 'prefixlen': '前缀长度', 'subnet_of': '是其子网吗', 'subnets': '子网们', 'supernet': '超网', 'supernet_of': '是其超网吗', 'with_hostmask': '带主机掩码', 'with_netmask': '带网络掩码', 'with_prefixlen': '带前缀长度'})

class _BaseConstants:
    _private_networks = []
_BaseNetwork._constants = _BaseConstants

class _BaseV4:
    """Base IPv4 object.

    The following methods are used by IPv4 objects in both single IP
    addresses and networks.

    """
    __slots__ = ()
    version = 4
    _ALL_ONES = 2 ** IPv4地址位数 - 1
    最大前缀长度 = IPv4地址位数
    _netmask_cache = {}

    def _explode_shorthand_ip_string(self):
        return str(self)

    @classmethod
    def _make_netmask(cls, arg):
        """Make a (netmask, prefix_len) tuple from the given argument.

        Argument can be:
        - an integer (the prefix length)
        - a string representing the prefix length (e.g. "24")
        - a string representing the prefix netmask (e.g. "255.255.255.0")
        """
        if arg not in cls._netmask_cache:
            if isinstance(arg, int):
                前缀长度 = arg
                if not 0 <= 前缀长度 <= cls.最大前缀长度:
                    cls._report_invalid_netmask(前缀长度)
            else:
                try:
                    前缀长度 = cls._prefix_from_prefix_string(arg)
                except 掩码值错误:
                    前缀长度 = cls._prefix_from_ip_string(arg)
            网络掩码 = IPv4地址(cls._ip_int_from_prefix(前缀长度))
            cls._netmask_cache[arg] = (网络掩码, 前缀长度)
        return cls._netmask_cache[arg]

    @classmethod
    def _ip_int_from_string(cls, ip_str):
        """Turn the given IP string into an integer for comparison.

        Args:
            ip_str: A string, the IP ip_str.

        Returns:
            The IP ip_str as an integer.

        Raises:
            AddressValueError: if ip_str isn't a valid IPv4 Address.

        """
        if not ip_str:
            raise 地址值错误('Address cannot be empty')
        octets = ip_str.split('.')
        if len(octets) != 4:
            raise 地址值错误('Expected 4 octets in %r' % ip_str)
        try:
            return int.from_bytes(map(cls._parse_octet, octets), 'big')
        except ValueError as exc:
            raise 地址值错误('%s in %r' % (exc, ip_str)) from None

    @classmethod
    def _parse_octet(cls, octet_str):
        """Convert a decimal octet into an integer.

        Args:
            octet_str: A string, the number to parse.

        Returns:
            The octet as an integer.

        Raises:
            ValueError: if the octet isn't strictly a decimal from [0..255].

        """
        if not octet_str:
            raise ValueError('Empty octet not permitted')
        if not (octet_str.isascii() and octet_str.isdigit()):
            msg = 'Only decimal digits permitted in %r'
            raise ValueError(msg % octet_str)
        if len(octet_str) > 3:
            msg = 'At most 3 characters permitted in %r'
            raise ValueError(msg % octet_str)
        if octet_str != '0' and octet_str[0] == '0':
            msg = 'Leading zeros are not permitted in %r'
            raise ValueError(msg % octet_str)
        octet_int = int(octet_str, 10)
        if octet_int > 255:
            raise ValueError('Octet %d (> 255) not permitted' % octet_int)
        return octet_int

    @classmethod
    def _string_from_ip_int(cls, ip_int):
        """Turns a 32-bit integer into dotted decimal notation.

        Args:
            ip_int: An integer, the IP address.

        Returns:
            The IP address as a string in dotted decimal notation.

        """
        return '.'.join(map(str, ip_int.to_bytes(4, 'big')))

    def _reverse_pointer(self):
        """Return the reverse DNS pointer name for the IPv4 address.

        This implements the method described in RFC1035 3.5.

        """
        reverse_octets = str(self).split('.')[::-1]
        return '.'.join(reverse_octets) + '.in-addr.arpa'
_装类转发(_BaseV4, {'max_prefixlen': '最大前缀长度'}, {'max_prefixlen': '最大前缀长度'})

class IPv4地址(_BaseV4, _BaseAddress):
    """Represent and manipulate single IPv4 Addresses."""
    __slots__ = ('_ip', '__weakref__')

    def __init__(self, address):
        """
        Args:
            address: A string or integer representing the IP

              Additionally, an integer can be passed, so
              IPv4Address('192.0.2.1') == IPv4Address(3221225985).
              or, more generally
              IPv4Address(int(IPv4Address('192.0.2.1'))) ==
                IPv4Address('192.0.2.1')

        Raises:
            AddressValueError: If ipaddress isn't a valid IPv4 address.

        """
        if isinstance(address, int):
            self._check_int_address(address)
            self._ip = address
            return
        if isinstance(address, bytes):
            self._check_packed_address(address, 4)
            self._ip = int.from_bytes(address)
            return
        addr_str = str(address)
        if '/' in addr_str:
            raise 地址值错误(f"Unexpected '/' in {address!r}")
        self._ip = self._ip_int_from_string(addr_str)

    @property
    def 打包字节(self):
        """The binary representation of this address."""
        return IPv4整数转字节(self._ip)

    @property
    def 是保留地址吗(self):
        """Test if the address is otherwise IETF reserved.

         Returns:
             A boolean, True if the address is within the
             reserved IPv4 Network range.

        """
        return self in self._constants._reserved_network

    @property
    @functools.lru_cache()
    def 是私有地址吗(self):
        """``True`` if the address is defined as not globally reachable by
        iana-ipv4-special-registry_ (for IPv4) or iana-ipv6-special-registry_
        (for IPv6) with the following exceptions:

        * ``is_private`` is ``False`` for ``100.64.0.0/10``
        * For IPv4-mapped IPv6-addresses the ``is_private`` value is determined by the
            semantics of the underlying IPv4 addresses and the following condition holds
            (see :attr:`IPv6Address.ipv4_mapped`)::

                address.is_private == address.ipv4_mapped.is_private

        ``is_private`` has value opposite to :attr:`is_global`, except for the ``100.64.0.0/10``
        IPv4 range where they are both ``False``.
        """
        return any((self in net for net in self._constants._private_networks)) and all((self not in net for net in self._constants._private_networks_exceptions))

    @property
    @functools.lru_cache()
    def 是全球地址吗(self):
        """``True`` if the address is defined as globally reachable by
        iana-ipv4-special-registry_ (for IPv4) or iana-ipv6-special-registry_
        (for IPv6) with the following exception:

        For IPv4-mapped IPv6-addresses the ``is_private`` value is determined by the
        semantics of the underlying IPv4 addresses and the following condition holds
        (see :attr:`IPv6Address.ipv4_mapped`)::

            address.is_global == address.ipv4_mapped.is_global

        ``is_global`` has value opposite to :attr:`is_private`, except for the ``100.64.0.0/10``
        IPv4 range where they are both ``False``.
        """
        return self not in self._constants._public_network and (not self.是私有地址吗)

    @property
    def 是多播吗(self):
        """Test if the address is reserved for multicast use.

        Returns:
            A boolean, True if the address is multicast.
            See RFC 3171 for details.

        """
        return self in self._constants._multicast_network

    @property
    def 是未指定地址吗(self):
        """Test if the address is unspecified.

        Returns:
            A boolean, True if this is the unspecified address as defined in
            RFC 5735 3.

        """
        return self == self._constants._unspecified_address

    @property
    def 是回环吗(self):
        """Test if the address is a loopback address.

        Returns:
            A boolean, True if the address is a loopback per RFC 3330.

        """
        return self in self._constants._loopback_network

    @property
    def 是链路本地吗(self):
        """Test if the address is reserved for link-local.

        Returns:
            A boolean, True if the address is link-local per RFC 3927.

        """
        return self in self._constants._linklocal_network

    @property
    def 映射到IPv6(self):
        """Return the IPv4-mapped IPv6 address.

        Returns:
            The IPv4-mapped IPv6 address per RFC 4291.

        """
        return IPv6地址(f'::ffff:{self}')
_装类转发(IPv4地址, {'ipv6_mapped': '映射到IPv6', 'is_global': '是全球地址吗', 'is_link_local': '是链路本地吗', 'is_loopback': '是回环吗', 'is_multicast': '是多播吗', 'is_private': '是私有地址吗', 'is_reserved': '是保留地址吗', 'is_unspecified': '是未指定地址吗', 'packed': '打包字节'}, {'ipv6_mapped': '映射到IPv6', 'is_global': '是全球地址吗', 'is_link_local': '是链路本地吗', 'is_loopback': '是回环吗', 'is_multicast': '是多播吗', 'is_private': '是私有地址吗', 'is_reserved': '是保留地址吗', 'is_unspecified': '是未指定地址吗', 'packed': '打包字节'})

class IPv4接口(IPv4地址):

    def __init__(self, address):
        addr, mask = self._split_addr_prefix(address)
        IPv4地址.__init__(self, addr)
        self.network = IPv4网络((addr, mask), strict=False)
        self.网络掩码 = self.network.netmask
        self._prefixlen = self.network._prefixlen

    @functools.cached_property
    def 主机掩码(self):
        return self.network.hostmask

    def __str__(self):
        return '%s/%d' % (self._string_from_ip_int(self._ip), self._prefixlen)

    def __eq__(self, other):
        address_equal = IPv4地址.__eq__(self, other)
        if address_equal is NotImplemented or not address_equal:
            return address_equal
        try:
            return self.network == other.network
        except AttributeError:
            return False

    def __lt__(self, other):
        address_less = IPv4地址.__lt__(self, other)
        if address_less is NotImplemented:
            return NotImplemented
        try:
            return self.network < other.network or (self.network == other.network and address_less)
        except AttributeError:
            return False

    def __hash__(self):
        return hash((self._ip, self._prefixlen, int(self.network.network_address)))
    __reduce__ = _IPAddressBase.__reduce__

    @property
    def 取IP(self):
        return IPv4地址(self._ip)

    @property
    def 带前缀长度(self):
        return '%s/%s' % (self._string_from_ip_int(self._ip), self._prefixlen)

    @property
    def 带网络掩码(self):
        return '%s/%s' % (self._string_from_ip_int(self._ip), self.网络掩码)

    @property
    def 带主机掩码(self):
        return '%s/%s' % (self._string_from_ip_int(self._ip), self.主机掩码)
_装类转发(IPv4接口, {'hostmask': '主机掩码', 'ip': '取IP', 'with_hostmask': '带主机掩码', 'with_netmask': '带网络掩码', 'with_prefixlen': '带前缀长度'}, {'hostmask': '主机掩码', 'ip': '取IP', 'netmask': '网络掩码', 'with_hostmask': '带主机掩码', 'with_netmask': '带网络掩码', 'with_prefixlen': '带前缀长度'})

class IPv4网络(_BaseV4, _BaseNetwork):
    """This class represents and manipulates 32-bit IPv4 network + addresses..

    Attributes: [examples for IPv4Network('192.0.2.0/27')]
        .network_address: IPv4Address('192.0.2.0')
        .hostmask: IPv4Address('0.0.0.31')
        .broadcast_address: IPv4Address('192.0.2.32')
        .netmask: IPv4Address('255.255.255.224')
        .prefixlen: 27

    """
    _address_class = IPv4地址

    def __init__(self, address, strict=True):
        """Instantiate a new IPv4 network object.

        Args:
            address: A string or integer representing the IP [& network].
              '192.0.2.0/24'
              '192.0.2.0/255.255.255.0'
              '192.0.2.0/0.0.0.255'
              are all functionally the same in IPv4. Similarly,
              '192.0.2.1'
              '192.0.2.1/255.255.255.255'
              '192.0.2.1/32'
              are also functionally equivalent. That is to say, failing to
              provide a subnetmask will create an object with a mask of /32.

              If the mask (portion after the / in the argument) is given in
              dotted quad form, it is treated as a netmask if it starts with a
              non-zero field (e.g. /255.0.0.0 == /8) and as a hostmask if it
              starts with a zero field (e.g. 0.255.255.255 == /8), with the
              single exception of an all-zero mask which is treated as a
              netmask == /0. If no mask is given, a default of /32 is used.

              Additionally, an integer can be passed, so
              IPv4Network('192.0.2.1') == IPv4Network(3221225985)
              or, more generally
              IPv4Interface(int(IPv4Interface('192.0.2.1'))) ==
                IPv4Interface('192.0.2.1')

        Raises:
            AddressValueError: If ipaddress isn't a valid IPv4 address.
            NetmaskValueError: If the netmask isn't valid for
              an IPv4 address.
            ValueError: If strict is True and a network address is not
              supplied.
        """
        addr, mask = self._split_addr_prefix(address)
        self.网络地址 = IPv4地址(addr)
        self.网络掩码, self._prefixlen = self._make_netmask(mask)
        打包字节 = int(self.网络地址)
        if 打包字节 & int(self.网络掩码) != 打包字节:
            if strict:
                raise ValueError('%s has host bits set' % self)
            else:
                self.网络地址 = IPv4地址(打包字节 & int(self.网络掩码))
        if self._prefixlen == self.最大前缀长度 - 1:
            self.主机们 = self.__iter__
        elif self._prefixlen == self.最大前缀长度:
            self.主机们 = lambda: iter((IPv4地址(addr),))

    @property
    @functools.lru_cache()
    def 是全球地址吗(self):
        """Test if this address is allocated for public networks.

        Returns:
            A boolean, True if the address is not reserved per
            iana-ipv4-special-registry.

        """
        return not (self.网络地址 in IPv4网络('100.64.0.0/10') and self.广播地址 in IPv4网络('100.64.0.0/10')) and (not self.是私有地址吗)
_装类转发(IPv4网络, {'is_global': '是全球地址吗'}, {'broadcast_address': '广播地址', 'hosts': '主机们', 'is_global': '是全球地址吗', 'is_private': '是私有地址吗', 'max_prefixlen': '最大前缀长度', 'netmask': '网络掩码', 'network_address': '网络地址'})

class _IPv4Constants:
    _linklocal_network = IPv4网络('169.254.0.0/16')
    _loopback_network = IPv4网络('127.0.0.0/8')
    _multicast_network = IPv4网络('224.0.0.0/4')
    _public_network = IPv4网络('100.64.0.0/10')
    _private_networks = [IPv4网络('0.0.0.0/8'), IPv4网络('10.0.0.0/8'), IPv4网络('127.0.0.0/8'), IPv4网络('169.254.0.0/16'), IPv4网络('172.16.0.0/12'), IPv4网络('192.0.0.0/24'), IPv4网络('192.0.0.170/31'), IPv4网络('192.0.2.0/24'), IPv4网络('192.168.0.0/16'), IPv4网络('198.18.0.0/15'), IPv4网络('198.51.100.0/24'), IPv4网络('203.0.113.0/24'), IPv4网络('240.0.0.0/4'), IPv4网络('255.255.255.255/32')]
    _private_networks_exceptions = [IPv4网络('192.0.0.9/32'), IPv4网络('192.0.0.10/32')]
    _reserved_network = IPv4网络('240.0.0.0/4')
    _unspecified_address = IPv4地址('0.0.0.0')
IPv4地址._constants = _IPv4Constants
IPv4网络._constants = _IPv4Constants

class _BaseV6:
    """Base IPv6 object.

    The following methods are used by IPv6 objects in both single IP
    addresses and networks.

    """
    __slots__ = ()
    version = 6
    _ALL_ONES = 2 ** IPv6地址位数 - 1
    _HEXTET_COUNT = 8
    _HEX_DIGITS = frozenset('0123456789ABCDEFabcdef')
    最大前缀长度 = IPv6地址位数
    _netmask_cache = {}

    @classmethod
    def _make_netmask(cls, arg):
        """Make a (netmask, prefix_len) tuple from the given argument.

        Argument can be:
        - an integer (the prefix length)
        - a string representing the prefix length (e.g. "24")
        - a string representing the prefix netmask (e.g. "255.255.255.0")
        """
        if arg not in cls._netmask_cache:
            if isinstance(arg, int):
                前缀长度 = arg
                if not 0 <= 前缀长度 <= cls.最大前缀长度:
                    cls._report_invalid_netmask(前缀长度)
            else:
                前缀长度 = cls._prefix_from_prefix_string(arg)
            网络掩码 = IPv6地址(cls._ip_int_from_prefix(前缀长度))
            cls._netmask_cache[arg] = (网络掩码, 前缀长度)
        return cls._netmask_cache[arg]

    @classmethod
    def _ip_int_from_string(cls, ip_str):
        """Turn an IPv6 ip_str into an integer.

        Args:
            ip_str: A string, the IPv6 ip_str.

        Returns:
            An int, the IPv6 address

        Raises:
            AddressValueError: if ip_str isn't a valid IPv6 Address.

        """
        if not ip_str:
            raise 地址值错误('Address cannot be empty')
        if len(ip_str) > 45:
            shorten = ip_str
            if len(shorten) > 100:
                shorten = f'{ip_str[:45]}({len(ip_str) - 90} chars elided){ip_str[-45:]}'
            raise 地址值错误(f'At most 45 characters expected in {shorten!r}')
        _max_parts = cls._HEXTET_COUNT + 1
        parts = ip_str.split(':', maxsplit=_max_parts)
        _min_parts = 3
        if len(parts) < _min_parts:
            msg = 'At least %d parts expected in %r' % (_min_parts, ip_str)
            raise 地址值错误(msg)
        if '.' in parts[-1]:
            try:
                ipv4_int = IPv4地址(parts.pop())._ip
            except 地址值错误 as exc:
                raise 地址值错误('%s in %r' % (exc, ip_str)) from None
            parts.append('%x' % (ipv4_int >> 16 & 65535))
            parts.append('%x' % (ipv4_int & 65535))
        if len(parts) > _max_parts:
            msg = 'At most %d colons permitted in %r' % (_max_parts - 1, ip_str)
            raise 地址值错误(msg)
        skip_index = None
        for i in range(1, len(parts) - 1):
            if not parts[i]:
                if skip_index is not None:
                    msg = "At most one '::' permitted in %r" % ip_str
                    raise 地址值错误(msg)
                skip_index = i
        if skip_index is not None:
            parts_hi = skip_index
            parts_lo = len(parts) - skip_index - 1
            if not parts[0]:
                parts_hi -= 1
                if parts_hi:
                    msg = "Leading ':' only permitted as part of '::' in %r"
                    raise 地址值错误(msg % ip_str)
            if not parts[-1]:
                parts_lo -= 1
                if parts_lo:
                    msg = "Trailing ':' only permitted as part of '::' in %r"
                    raise 地址值错误(msg % ip_str)
            parts_skipped = cls._HEXTET_COUNT - (parts_hi + parts_lo)
            if parts_skipped < 1:
                msg = "Expected at most %d other parts with '::' in %r"
                raise 地址值错误(msg % (cls._HEXTET_COUNT - 1, ip_str))
        else:
            if len(parts) != cls._HEXTET_COUNT:
                msg = "Exactly %d parts expected without '::' in %r"
                raise 地址值错误(msg % (cls._HEXTET_COUNT, ip_str))
            if not parts[0]:
                msg = "Leading ':' only permitted as part of '::' in %r"
                raise 地址值错误(msg % ip_str)
            if not parts[-1]:
                msg = "Trailing ':' only permitted as part of '::' in %r"
                raise 地址值错误(msg % ip_str)
            parts_hi = len(parts)
            parts_lo = 0
            parts_skipped = 0
        try:
            ip_int = 0
            for i in range(parts_hi):
                ip_int <<= 16
                ip_int |= cls._parse_hextet(parts[i])
            ip_int <<= 16 * parts_skipped
            for i in range(-parts_lo, 0):
                ip_int <<= 16
                ip_int |= cls._parse_hextet(parts[i])
            return ip_int
        except ValueError as exc:
            raise 地址值错误('%s in %r' % (exc, ip_str)) from None

    @classmethod
    def _parse_hextet(cls, hextet_str):
        """Convert an IPv6 hextet string into an integer.

        Args:
            hextet_str: A string, the number to parse.

        Returns:
            The hextet as an integer.

        Raises:
            ValueError: if the input isn't strictly a hex number from
              [0..FFFF].

        """
        if not cls._HEX_DIGITS.issuperset(hextet_str):
            raise ValueError('Only hex digits permitted in %r' % hextet_str)
        if len(hextet_str) > 4:
            msg = 'At most 4 characters permitted in %r'
            raise ValueError(msg % hextet_str)
        return int(hextet_str, 16)

    @classmethod
    def _compress_hextets(cls, hextets):
        """Compresses a list of hextets.

        Compresses a list of strings, replacing the longest continuous
        sequence of "0" in the list with "" and adding empty strings at
        the beginning or at the end of the string such that subsequently
        calling ":".join(hextets) will produce the compressed version of
        the IPv6 address.

        Args:
            hextets: A list of strings, the hextets to compress.

        Returns:
            A list of strings.

        """
        best_doublecolon_start = -1
        best_doublecolon_len = 0
        doublecolon_start = -1
        doublecolon_len = 0
        for index, hextet in enumerate(hextets):
            if hextet == '0':
                doublecolon_len += 1
                if doublecolon_start == -1:
                    doublecolon_start = index
                if doublecolon_len > best_doublecolon_len:
                    best_doublecolon_len = doublecolon_len
                    best_doublecolon_start = doublecolon_start
            else:
                doublecolon_len = 0
                doublecolon_start = -1
        if best_doublecolon_len > 1:
            best_doublecolon_end = best_doublecolon_start + best_doublecolon_len
            if best_doublecolon_end == len(hextets):
                hextets += ['']
            hextets[best_doublecolon_start:best_doublecolon_end] = ['']
            if best_doublecolon_start == 0:
                hextets = [''] + hextets
        return hextets

    @classmethod
    def _string_from_ip_int(cls, ip_int=None):
        """Turns a 128-bit integer into hexadecimal notation.

        Args:
            ip_int: An integer, the IP address.

        Returns:
            A string, the hexadecimal representation of the address.

        Raises:
            ValueError: The address is bigger than 128 bits of all ones.

        """
        if ip_int is None:
            ip_int = int(cls._ip)
        if ip_int > cls._ALL_ONES:
            raise ValueError('IPv6 address is too large')
        hex_str = '%032x' % ip_int
        hextets = ['%x' % int(hex_str[x:x + 4], 16) for x in range(0, 32, 4)]
        hextets = cls._compress_hextets(hextets)
        return ':'.join(hextets)

    def _explode_shorthand_ip_string(self):
        """Expand a shortened IPv6 address.

        Returns:
            A string, the expanded IPv6 address.

        """
        if isinstance(self, IPv6网络):
            ip_str = str(self.网络地址)
        elif isinstance(self, IPv6接口):
            ip_str = str(self.取IP)
        else:
            ip_str = str(self)
        ip_int = self._ip_int_from_string(ip_str)
        hex_str = '%032x' % ip_int
        parts = [hex_str[x:x + 4] for x in range(0, 32, 4)]
        if isinstance(self, (_BaseNetwork, IPv6接口)):
            return '%s/%d' % (':'.join(parts), self._prefixlen)
        return ':'.join(parts)

    def _reverse_pointer(self):
        """Return the reverse DNS pointer name for the IPv6 address.

        This implements the method described in RFC3596 2.5.

        """
        reverse_chars = self.完整写法[::-1].replace(':', '')
        return '.'.join(reverse_chars) + '.ip6.arpa'

    @staticmethod
    def _split_scope_id(ip_str):
        """Helper function to parse IPv6 string address with scope id.

        See RFC 4007 for details.

        Args:
            ip_str: A string, the IPv6 address.

        Returns:
            (addr, scope_id) tuple.

        """
        addr, sep, 作用域ID = ip_str.partition('%')
        if not sep:
            作用域ID = None
        elif not 作用域ID or '%' in 作用域ID:
            raise 地址值错误('Invalid IPv6 address: "%r"' % ip_str)
        return (addr, 作用域ID)
_装类转发(_BaseV6, {'max_prefixlen': '最大前缀长度'}, {'exploded': '完整写法', 'ip': '取IP', 'max_prefixlen': '最大前缀长度', 'network_address': '网络地址'})

class IPv6地址(_BaseV6, _BaseAddress):
    """Represent and manipulate single IPv6 Addresses."""
    __slots__ = ('_ip', '_scope_id', '__weakref__')

    def __init__(self, address):
        """Instantiate a new IPv6 address object.

        Args:
            address: A string or integer representing the IP

              Additionally, an integer can be passed, so
              IPv6Address('2001:db8::') ==
                IPv6Address(42540766411282592856903984951653826560)
              or, more generally
              IPv6Address(int(IPv6Address('2001:db8::'))) ==
                IPv6Address('2001:db8::')

        Raises:
            AddressValueError: If address isn't a valid IPv6 address.

        """
        if isinstance(address, int):
            self._check_int_address(address)
            self._ip = address
            self._scope_id = None
            return
        if isinstance(address, bytes):
            self._check_packed_address(address, 16)
            self._ip = int.from_bytes(address, 'big')
            self._scope_id = None
            return
        addr_str = str(address)
        if '/' in addr_str:
            raise 地址值错误(f"Unexpected '/' in {address!r}")
        addr_str, self._scope_id = self._split_scope_id(addr_str)
        self._ip = self._ip_int_from_string(addr_str)

    def _explode_shorthand_ip_string(self):
        映射到IPv4 = self.映射到IPv4
        if 映射到IPv4 is None:
            return super()._explode_shorthand_ip_string()
        prefix_len = 30
        raw_exploded_str = super()._explode_shorthand_ip_string()
        return f'{raw_exploded_str[:prefix_len]}{映射到IPv4!s}'

    def _reverse_pointer(self):
        映射到IPv4 = self.映射到IPv4
        if 映射到IPv4 is None:
            return super()._reverse_pointer()
        prefix_len = 30
        raw_exploded_str = super()._explode_shorthand_ip_string()[:prefix_len]
        ipv4_int = 映射到IPv4._ip
        reverse_chars = f'{raw_exploded_str}{ipv4_int:008x}'[::-1].replace(':', '')
        return '.'.join(reverse_chars) + '.ip6.arpa'

    def _ipv4_mapped_ipv6_to_str(self):
        """Return convenient text representation of IPv4-mapped IPv6 address

        See RFC 4291 2.5.5.2, 2.2 p.3 for details.

        Returns:
            A string, 'x:x:x:x:x:x:d.d.d.d', where the 'x's are the hexadecimal values of
            the six high-order 16-bit pieces of the address, and the 'd's are
            the decimal values of the four low-order 8-bit pieces of the
            address (standard IPv4 representation) as defined in RFC 4291 2.2 p.3.

        """
        映射到IPv4 = self.映射到IPv4
        if 映射到IPv4 is None:
            raise 地址值错误('Can not apply to non-IPv4-mapped IPv6 address %s' % str(self))
        high_order_bits = self._ip >> 32
        return '%s:%s' % (self._string_from_ip_int(high_order_bits), str(映射到IPv4))

    def __str__(self):
        映射到IPv4 = self.映射到IPv4
        if 映射到IPv4 is None:
            ip_str = super().__str__()
        else:
            ip_str = self._ipv4_mapped_ipv6_to_str()
        return ip_str + '%' + self._scope_id if self._scope_id else ip_str

    def __hash__(self):
        return hash((self._ip, self._scope_id))

    def __eq__(self, other):
        address_equal = super().__eq__(other)
        if address_equal is NotImplemented:
            return NotImplemented
        if not address_equal:
            return False
        return self._scope_id == getattr(other, '_scope_id', None)

    def __reduce__(self):
        return (self.__class__, (str(self),))

    @property
    def 作用域ID(self):
        """Identifier of a particular zone of the address's scope.

        See RFC 4007 for details.

        Returns:
            A string identifying the zone of the address if specified, else None.

        """
        return self._scope_id

    @property
    def 打包字节(self):
        """The binary representation of this address."""
        return IPv6整数转字节(self._ip)

    @property
    def 是多播吗(self):
        """Test if the address is reserved for multicast use.

        Returns:
            A boolean, True if the address is a multicast address.
            See RFC 2373 2.7 for details.

        """
        映射到IPv4 = self.映射到IPv4
        if 映射到IPv4 is not None:
            return 映射到IPv4.is_multicast
        return self in self._constants._multicast_network

    @property
    def 是保留地址吗(self):
        """Test if the address is otherwise IETF reserved.

        Returns:
            A boolean, True if the address is within one of the
            reserved IPv6 Network ranges.

        """
        映射到IPv4 = self.映射到IPv4
        if 映射到IPv4 is not None:
            return 映射到IPv4.is_reserved
        return any((self in x for x in self._constants._reserved_networks))

    @property
    def 是链路本地吗(self):
        """Test if the address is reserved for link-local.

        Returns:
            A boolean, True if the address is reserved per RFC 4291.

        """
        映射到IPv4 = self.映射到IPv4
        if 映射到IPv4 is not None:
            return 映射到IPv4.is_link_local
        return self in self._constants._linklocal_network

    @property
    def 是站点本地吗(self):
        """Test if the address is reserved for site-local.

        Note that the site-local address space has been deprecated by RFC 3879.
        Use is_private to test if this address is in the space of unique local
        addresses as defined by RFC 4193.

        Returns:
            A boolean, True if the address is reserved per RFC 3513 2.5.6.

        """
        return self in self._constants._sitelocal_network

    @property
    @functools.lru_cache()
    def 是私有地址吗(self):
        """``True`` if the address is defined as not globally reachable by
        iana-ipv4-special-registry_ (for IPv4) or iana-ipv6-special-registry_
        (for IPv6) with the following exceptions:

        * ``is_private`` is ``False`` for ``100.64.0.0/10``
        * For IPv4-mapped IPv6-addresses the ``is_private`` value is determined by the
            semantics of the underlying IPv4 addresses and the following condition holds
            (see :attr:`IPv6Address.ipv4_mapped`)::

                address.is_private == address.ipv4_mapped.is_private

        ``is_private`` has value opposite to :attr:`is_global`, except for the ``100.64.0.0/10``
        IPv4 range where they are both ``False``.
        """
        映射到IPv4 = self.映射到IPv4
        if 映射到IPv4 is not None:
            return 映射到IPv4.is_private
        return any((self in net for net in self._constants._private_networks)) and all((self not in net for net in self._constants._private_networks_exceptions))

    @property
    def 是全球地址吗(self):
        """``True`` if the address is defined as globally reachable by
        iana-ipv4-special-registry_ (for IPv4) or iana-ipv6-special-registry_
        (for IPv6) with the following exception:

        For IPv4-mapped IPv6-addresses the ``is_private`` value is determined by the
        semantics of the underlying IPv4 addresses and the following condition holds
        (see :attr:`IPv6Address.ipv4_mapped`)::

            address.is_global == address.ipv4_mapped.is_global

        ``is_global`` has value opposite to :attr:`is_private`, except for the ``100.64.0.0/10``
        IPv4 range where they are both ``False``.
        """
        映射到IPv4 = self.映射到IPv4
        if 映射到IPv4 is not None:
            return 映射到IPv4.is_global
        return not self.是私有地址吗

    @property
    def 是未指定地址吗(self):
        """Test if the address is unspecified.

        Returns:
            A boolean, True if this is the unspecified address as defined in
            RFC 2373 2.5.2.

        """
        映射到IPv4 = self.映射到IPv4
        if 映射到IPv4 is not None:
            return 映射到IPv4.is_unspecified
        return self._ip == 0

    @property
    def 是回环吗(self):
        """Test if the address is a loopback address.

        Returns:
            A boolean, True if the address is a loopback address as defined in
            RFC 2373 2.5.3.

        """
        映射到IPv4 = self.映射到IPv4
        if 映射到IPv4 is not None:
            return 映射到IPv4.is_loopback
        return self._ip == 1

    @property
    def 映射到IPv4(self):
        """Return the IPv4 mapped address.

        Returns:
            If the IPv6 address is a v4 mapped address, return the
            IPv4 mapped address. Return None otherwise.

        """
        if self._ip >> 32 != 65535:
            return None
        return IPv4地址(self._ip & 4294967295)

    @property
    def Teredo地址(self):
        """Tuple of embedded teredo IPs.

        Returns:
            Tuple of the (server, client) IPs or None if the address
            doesn't appear to be a teredo address (doesn't start with
            2001::/32)

        """
        if self._ip >> 96 != 536936448:
            return None
        return (IPv4地址(self._ip >> 64 & 4294967295), IPv4地址(~self._ip & 4294967295))

    @property
    def 六转四地址(self):
        """Return the IPv4 6to4 embedded address.

        Returns:
            The IPv4 6to4-embedded address if present or None if the
            address doesn't appear to contain a 6to4 embedded address.

        """
        if self._ip >> 112 != 8194:
            return None
        return IPv4地址(self._ip >> 80 & 4294967295)
_装类转发(IPv6地址, {'ipv4_mapped': '映射到IPv4', 'is_global': '是全球地址吗', 'is_link_local': '是链路本地吗', 'is_loopback': '是回环吗', 'is_multicast': '是多播吗', 'is_private': '是私有地址吗', 'is_reserved': '是保留地址吗', 'is_site_local': '是站点本地吗', 'is_unspecified': '是未指定地址吗', 'packed': '打包字节', 'scope_id': '作用域ID', 'sixtofour': '六转四地址', 'teredo': 'Teredo地址'}, {'ipv4_mapped': '映射到IPv4', 'is_global': '是全球地址吗', 'is_link_local': '是链路本地吗', 'is_loopback': '是回环吗', 'is_multicast': '是多播吗', 'is_private': '是私有地址吗', 'is_reserved': '是保留地址吗', 'is_site_local': '是站点本地吗', 'is_unspecified': '是未指定地址吗', 'packed': '打包字节', 'scope_id': '作用域ID', 'sixtofour': '六转四地址', 'teredo': 'Teredo地址'})

class IPv6接口(IPv6地址):

    def __init__(self, address):
        addr, mask = self._split_addr_prefix(address)
        IPv6地址.__init__(self, addr)
        self.network = IPv6网络((addr, mask), strict=False)
        self.网络掩码 = self.network.netmask
        self._prefixlen = self.network._prefixlen

    @functools.cached_property
    def 主机掩码(self):
        return self.network.hostmask

    def __str__(self):
        return '%s/%d' % (super().__str__(), self._prefixlen)

    def __eq__(self, other):
        address_equal = IPv6地址.__eq__(self, other)
        if address_equal is NotImplemented or not address_equal:
            return address_equal
        try:
            return self.network == other.network
        except AttributeError:
            return False

    def __lt__(self, other):
        address_less = IPv6地址.__lt__(self, other)
        if address_less is NotImplemented:
            return address_less
        try:
            return self.network < other.network or (self.network == other.network and address_less)
        except AttributeError:
            return False

    def __hash__(self):
        return hash((self._ip, self._prefixlen, int(self.network.network_address)))
    __reduce__ = _IPAddressBase.__reduce__

    @property
    def 取IP(self):
        return IPv6地址(self._ip)

    @property
    def 带前缀长度(self):
        return '%s/%s' % (self._string_from_ip_int(self._ip), self._prefixlen)

    @property
    def 带网络掩码(self):
        return '%s/%s' % (self._string_from_ip_int(self._ip), self.网络掩码)

    @property
    def 带主机掩码(self):
        return '%s/%s' % (self._string_from_ip_int(self._ip), self.主机掩码)

    @property
    def 是未指定地址吗(self):
        return self._ip == 0 and self.network.is_unspecified

    @property
    def 是回环吗(self):
        return super().is_loopback and self.network.is_loopback
_装类转发(IPv6接口, {'hostmask': '主机掩码', 'ip': '取IP', 'is_loopback': '是回环吗', 'is_unspecified': '是未指定地址吗', 'with_hostmask': '带主机掩码', 'with_netmask': '带网络掩码', 'with_prefixlen': '带前缀长度'}, {'hostmask': '主机掩码', 'ip': '取IP', 'is_loopback': '是回环吗', 'is_unspecified': '是未指定地址吗', 'netmask': '网络掩码', 'with_hostmask': '带主机掩码', 'with_netmask': '带网络掩码', 'with_prefixlen': '带前缀长度'})

class IPv6网络(_BaseV6, _BaseNetwork):
    """This class represents and manipulates 128-bit IPv6 networks.

    Attributes: [examples for IPv6('2001:db8::1000/124')]
        .network_address: IPv6Address('2001:db8::1000')
        .hostmask: IPv6Address('::f')
        .broadcast_address: IPv6Address('2001:db8::100f')
        .netmask: IPv6Address('ffff:ffff:ffff:ffff:ffff:ffff:ffff:fff0')
        .prefixlen: 124

    """
    _address_class = IPv6地址

    def __init__(self, address, strict=True):
        """Instantiate a new IPv6 Network object.

        Args:
            address: A string or integer representing the IPv6 network or the
              IP and prefix/netmask.
              '2001:db8::/128'
              '2001:db8:0000:0000:0000:0000:0000:0000/128'
              '2001:db8::'
              are all functionally the same in IPv6.  That is to say,
              failing to provide a subnetmask will create an object with
              a mask of /128.

              Additionally, an integer can be passed, so
              IPv6Network('2001:db8::') ==
                IPv6Network(42540766411282592856903984951653826560)
              or, more generally
              IPv6Network(int(IPv6Network('2001:db8::'))) ==
                IPv6Network('2001:db8::')

            strict: A boolean. If true, ensure that we have been passed
              A true network address, eg, 2001:db8::1000/124 and not an
              IP address on a network, eg, 2001:db8::1/124.

        Raises:
            AddressValueError: If address isn't a valid IPv6 address.
            NetmaskValueError: If the netmask isn't valid for
              an IPv6 address.
            ValueError: If strict was True and a network address was not
              supplied.
        """
        addr, mask = self._split_addr_prefix(address)
        self.网络地址 = IPv6地址(addr)
        self.网络掩码, self._prefixlen = self._make_netmask(mask)
        打包字节 = int(self.网络地址)
        if 打包字节 & int(self.网络掩码) != 打包字节:
            if strict:
                raise ValueError('%s has host bits set' % self)
            else:
                self.网络地址 = IPv6地址(打包字节 & int(self.网络掩码))
        if self._prefixlen == self.最大前缀长度 - 1:
            self.主机们 = self.__iter__
        elif self._prefixlen == self.最大前缀长度:
            self.主机们 = lambda: iter((IPv6地址(addr),))

    def 主机们(self):
        """Generate Iterator over usable hosts in a network.

          This is like __iter__ except it doesn't return the
          Subnet-Router anycast address.

        """
        network = int(self.网络地址)
        broadcast = int(self.广播地址)
        for x in range(network + 1, broadcast + 1):
            yield self._address_class(x)

    @property
    def 是站点本地吗(self):
        """Test if the address is reserved for site-local.

        Note that the site-local address space has been deprecated by RFC 3879.
        Use is_private to test if this address is in the space of unique local
        addresses as defined by RFC 4193.

        Returns:
            A boolean, True if the address is reserved per RFC 3513 2.5.6.

        """
        return self.网络地址.is_site_local and self.广播地址.is_site_local
_装类转发(IPv6网络, {'hosts': '主机们', 'is_site_local': '是站点本地吗'}, {'broadcast_address': '广播地址', 'hosts': '主机们', 'is_site_local': '是站点本地吗', 'max_prefixlen': '最大前缀长度', 'netmask': '网络掩码', 'network_address': '网络地址'})

class _IPv6Constants:
    _linklocal_network = IPv6网络('fe80::/10')
    _multicast_network = IPv6网络('ff00::/8')
    _private_networks = [IPv6网络('::1/128'), IPv6网络('::/128'), IPv6网络('::ffff:0:0/96'), IPv6网络('64:ff9b:1::/48'), IPv6网络('100::/64'), IPv6网络('2001::/23'), IPv6网络('2001:db8::/32'), IPv6网络('2002::/16'), IPv6网络('3fff::/20'), IPv6网络('fc00::/7'), IPv6网络('fe80::/10')]
    _private_networks_exceptions = [IPv6网络('2001:1::1/128'), IPv6网络('2001:1::2/128'), IPv6网络('2001:3::/32'), IPv6网络('2001:4:112::/48'), IPv6网络('2001:20::/28'), IPv6网络('2001:30::/28')]
    _reserved_networks = [IPv6网络('::/8'), IPv6网络('100::/8'), IPv6网络('200::/7'), IPv6网络('400::/6'), IPv6网络('800::/5'), IPv6网络('1000::/4'), IPv6网络('4000::/3'), IPv6网络('6000::/3'), IPv6网络('8000::/3'), IPv6网络('A000::/3'), IPv6网络('C000::/3'), IPv6网络('E000::/4'), IPv6网络('F000::/5'), IPv6网络('F800::/6'), IPv6网络('FE00::/9')]
    _sitelocal_network = IPv6网络('fec0::/10')
IPv6地址._constants = _IPv6Constants
IPv6网络._constants = _IPv6Constants


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'AddressValueError': '地址值错误',
    'IPV4LENGTH': 'IPv4地址位数',
    'IPV6LENGTH': 'IPv6地址位数',
    'IPv4Address': 'IPv4地址',
    'IPv4Interface': 'IPv4接口',
    'IPv4Network': 'IPv4网络',
    'IPv6Address': 'IPv6地址',
    'IPv6Interface': 'IPv6接口',
    'IPv6Network': 'IPv6网络',
    'NetmaskValueError': '掩码值错误',
    'collapse_addresses': '合并地址块',
    'get_mixed_type_key': '混合类型排序键',
    'ip_address': '取IP地址',
    'ip_interface': '取IP接口',
    'ip_network': '取IP网络',
    'summarize_address_range': '汇总地址范围',
    'v4_int_to_packed': 'IPv4整数转字节',
    'v6_int_to_packed': 'IPv6整数转字节',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'IPv4地址': {
        'ipv6_mapped': '映射到IPv6',
        'is_global': '是全球地址吗',
        'is_link_local': '是链路本地吗',
        'is_loopback': '是回环吗',
        'is_multicast': '是多播吗',
        'is_private': '是私有地址吗',
        'is_reserved': '是保留地址吗',
        'is_unspecified': '是未指定地址吗',
        'packed': '打包字节',
    },
    'IPv4接口': {
        'hostmask': '主机掩码',
        'ip': '取IP',
        'with_hostmask': '带主机掩码',
        'with_netmask': '带网络掩码',
        'with_prefixlen': '带前缀长度',
    },
    'IPv4网络': {
        'is_global': '是全球地址吗',
    },
    'IPv6地址': {
        'ipv4_mapped': '映射到IPv4',
        'is_global': '是全球地址吗',
        'is_link_local': '是链路本地吗',
        'is_loopback': '是回环吗',
        'is_multicast': '是多播吗',
        'is_private': '是私有地址吗',
        'is_reserved': '是保留地址吗',
        'is_site_local': '是站点本地吗',
        'is_unspecified': '是未指定地址吗',
        'packed': '打包字节',
        'scope_id': '作用域ID',
        'sixtofour': '六转四地址',
        'teredo': 'Teredo地址',
    },
    'IPv6接口': {
        'hostmask': '主机掩码',
        'ip': '取IP',
        'is_loopback': '是回环吗',
        'is_unspecified': '是未指定地址吗',
        'with_hostmask': '带主机掩码',
        'with_netmask': '带网络掩码',
        'with_prefixlen': '带前缀长度',
    },
    'IPv6网络': {
        'hosts': '主机们',
        'is_site_local': '是站点本地吗',
    },
    '_BaseNetwork': {
        'address_exclude': '排除地址',
        'broadcast_address': '广播地址',
        'compare_networks': '比较网络',
        'hostmask': '主机掩码',
        'hosts': '主机们',
        'is_global': '是全球地址吗',
        'is_link_local': '是链路本地吗',
        'is_loopback': '是回环吗',
        'is_multicast': '是多播吗',
        'is_private': '是私有地址吗',
        'is_reserved': '是保留地址吗',
        'is_unspecified': '是未指定地址吗',
        'num_addresses': '地址总数',
        'overlaps': '有重叠吗',
        'prefixlen': '前缀长度',
        'subnet_of': '是其子网吗',
        'subnets': '子网们',
        'supernet': '超网',
        'supernet_of': '是其超网吗',
        'with_hostmask': '带主机掩码',
        'with_netmask': '带网络掩码',
        'with_prefixlen': '带前缀长度',
    },
    '_BaseV4': {
        'max_prefixlen': '最大前缀长度',
    },
    '_BaseV6': {
        'max_prefixlen': '最大前缀长度',
    },
    '_IPAddressBase': {
        'compressed': '压缩写法',
        'exploded': '完整写法',
        'reverse_pointer': '反查指针',
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
    'IPv4地址': {
        'ipv6_mapped': '映射到IPv6',
        'is_global': '是全球地址吗',
        'is_link_local': '是链路本地吗',
        'is_loopback': '是回环吗',
        'is_multicast': '是多播吗',
        'is_private': '是私有地址吗',
        'is_reserved': '是保留地址吗',
        'is_unspecified': '是未指定地址吗',
        'packed': '打包字节',
    },
    'IPv4接口': {
        'hostmask': '主机掩码',
        'ip': '取IP',
        'netmask': '网络掩码',
        'with_hostmask': '带主机掩码',
        'with_netmask': '带网络掩码',
        'with_prefixlen': '带前缀长度',
    },
    'IPv4网络': {
        'broadcast_address': '广播地址',
        'hosts': '主机们',
        'is_global': '是全球地址吗',
        'is_private': '是私有地址吗',
        'max_prefixlen': '最大前缀长度',
        'netmask': '网络掩码',
        'network_address': '网络地址',
    },
    'IPv6地址': {
        'ipv4_mapped': '映射到IPv4',
        'is_global': '是全球地址吗',
        'is_link_local': '是链路本地吗',
        'is_loopback': '是回环吗',
        'is_multicast': '是多播吗',
        'is_private': '是私有地址吗',
        'is_reserved': '是保留地址吗',
        'is_site_local': '是站点本地吗',
        'is_unspecified': '是未指定地址吗',
        'packed': '打包字节',
        'scope_id': '作用域ID',
        'sixtofour': '六转四地址',
        'teredo': 'Teredo地址',
    },
    'IPv6接口': {
        'hostmask': '主机掩码',
        'ip': '取IP',
        'is_loopback': '是回环吗',
        'is_unspecified': '是未指定地址吗',
        'netmask': '网络掩码',
        'with_hostmask': '带主机掩码',
        'with_netmask': '带网络掩码',
        'with_prefixlen': '带前缀长度',
    },
    'IPv6网络': {
        'broadcast_address': '广播地址',
        'hosts': '主机们',
        'is_site_local': '是站点本地吗',
        'max_prefixlen': '最大前缀长度',
        'netmask': '网络掩码',
        'network_address': '网络地址',
    },
    '_BaseAddress': {
        'max_prefixlen': '最大前缀长度',
    },
    '_BaseNetwork': {
        'address_exclude': '排除地址',
        'broadcast_address': '广播地址',
        'compare_networks': '比较网络',
        'hostmask': '主机掩码',
        'hosts': '主机们',
        'is_global': '是全球地址吗',
        'is_link_local': '是链路本地吗',
        'is_loopback': '是回环吗',
        'is_multicast': '是多播吗',
        'is_private': '是私有地址吗',
        'is_reserved': '是保留地址吗',
        'is_unspecified': '是未指定地址吗',
        'max_prefixlen': '最大前缀长度',
        'netmask': '网络掩码',
        'network_address': '网络地址',
        'num_addresses': '地址总数',
        'overlaps': '有重叠吗',
        'prefixlen': '前缀长度',
        'subnet_of': '是其子网吗',
        'subnets': '子网们',
        'supernet': '超网',
        'supernet_of': '是其超网吗',
        'with_hostmask': '带主机掩码',
        'with_netmask': '带网络掩码',
        'with_prefixlen': '带前缀长度',
    },
    '_BaseV4': {
        'max_prefixlen': '最大前缀长度',
    },
    '_BaseV6': {
        'exploded': '完整写法',
        'ip': '取IP',
        'max_prefixlen': '最大前缀长度',
        'network_address': '网络地址',
    },
    '_IPAddressBase': {
        'compressed': '压缩写法',
        'exploded': '完整写法',
        'max_prefixlen': '最大前缀长度',
        'reverse_pointer': '反查指针',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
