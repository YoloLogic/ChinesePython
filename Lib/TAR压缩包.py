# -*- coding: utf-8 -*-
"""TAR压缩包 —— 汉语库（由 tools/汉化库.py 从 Lib/tarfile.py 机械生成，**不要手改**）。

英文库 Lib/tarfile.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py TAR压缩包
"""


"""Read from and write to tar format archives.
"""
_英文原名表 = {'AREGTYPE': '备选普通文件类型', 'AbsoluteLinkError': '绝对链接错误', 'AbsolutePathError': '绝对路径错误', 'BLKTYPE': '块设备类型', 'BLOCKSIZE': '块大小', 'CHRTYPE': '字符设备类型', 'CONTTYPE': '连续文件类型', 'CompressionError': '压缩错误', 'DEFAULT_FORMAT': '默认格式', 'DIRTYPE': '目录类型', 'ENCODING': '编码方式', 'EOFHeaderError': '文件头提前结束错误', 'EmptyHeaderError': '空文件头错误', 'ExFileObject': '提取文件对象', 'ExtractError': '提取错误', 'FIFOTYPE': 'FIFO类型', 'FilterError': '过滤器错误', 'GNUTYPE_LONGLINK': 'GNU长链接类型', 'GNUTYPE_LONGNAME': 'GNU长名字类型', 'GNUTYPE_SPARSE': 'GNU稀疏类型', 'GNU_FORMAT': 'GNU格式', 'GNU_MAGIC': 'GNU魔数', 'GNU_TYPES': 'GNU类型', 'HeaderError': '文件头错误', 'InvalidHeaderError': '文件头无效错误', 'LENGTH_LINK': '链接名长度', 'LENGTH_NAME': '名字长度', 'LENGTH_PREFIX': '前缀长度', 'LNKTYPE': '硬链接类型', 'LinkFallbackError': '链接回退错误', 'LinkOutsideDestinationError': '链接越出目标错误', 'NUL': '空字节', 'OutsideDestinationError': '越出目标目录错误', 'PAX_FIELDS': 'PAX字段', 'PAX_FORMAT': 'PAX格式', 'PAX_NAME_FIELDS': 'PAX名字字段', 'PAX_NUMBER_FIELDS': 'PAX数字字段', 'POSIX_MAGIC': 'POSIX魔数', 'RECORDSIZE': '记录大小', 'REGTYPE': '普通文件类型', 'REGULAR_TYPES': '普通类型', 'ReadError': '读错误', 'SOLARIS_XHDTYPE': 'SOLARIS扩展头类型', 'SUPPORTED_TYPES': '支持的类型', 'SYMTYPE': '符号链接类型', 'SpecialFileError': '特殊文件错误', 'StreamError': '流错误', 'SubsequentHeaderError': '多余文件头错误', 'TarError': 'TAR错误', 'TarFile': 'TAR文件', 'TarInfo': 'TAR条目', 'TruncatedHeaderError': '截断文件头错误', 'USTAR_FORMAT': 'USTAR格式', 'XGLTYPE': '全局扩展头类型', 'XHDTYPE': '扩展头类型', 'calc_chksums': '算校验和', 'copyfileobj': '复制文件对象', 'is_tarfile': '是TAR文件吗', 'main': '主函数', 'symlink_exception': '符号链接异常', 'version': '版本'}

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
版本 = '0.9.0'
__author__ = 'Lars Gustäbel (lars@gustaebel.de)'
__credits__ = 'Gustavo Niemeyer, Niels Gustäbel, Richard Townsend.'
from builtins import open as bltn_open
import sys
import os
import io
import shutil
import stat
import time
import struct
import copy
import re
try:
    import pwd
except ImportError:
    pwd = None
try:
    import grp
except ImportError:
    grp = None
符号链接异常 = (AttributeError, NotImplementedError, OSError)
__all__ = ['TarFile', 'TarInfo', 'is_tarfile', 'TarError', 'ReadError', 'CompressionError', 'StreamError', 'ExtractError', 'HeaderError', 'ENCODING', 'USTAR_FORMAT', 'GNU_FORMAT', 'PAX_FORMAT', 'DEFAULT_FORMAT', 'open', 'fully_trusted_filter', 'data_filter', 'tar_filter', 'FilterError', 'AbsoluteLinkError', 'OutsideDestinationError', 'SpecialFileError', 'AbsolutePathError', 'LinkOutsideDestinationError', 'LinkFallbackError']
空字节 = b'\x00'
块大小 = 512
记录大小 = 块大小 * 20
GNU魔数 = b'ustar  \x00'
POSIX魔数 = b'ustar\x0000'
名字长度 = 100
链接名长度 = 100
前缀长度 = 155
普通文件类型 = b'0'
备选普通文件类型 = b'\x00'
硬链接类型 = b'1'
符号链接类型 = b'2'
字符设备类型 = b'3'
块设备类型 = b'4'
目录类型 = b'5'
FIFO类型 = b'6'
连续文件类型 = b'7'
GNU长名字类型 = b'L'
GNU长链接类型 = b'K'
GNU稀疏类型 = b'S'
扩展头类型 = b'x'
全局扩展头类型 = b'g'
SOLARIS扩展头类型 = b'X'
USTAR格式 = 0
GNU格式 = 1
PAX格式 = 2
默认格式 = PAX格式
支持的类型 = (普通文件类型, 备选普通文件类型, 硬链接类型, 符号链接类型, 目录类型, FIFO类型, 连续文件类型, 字符设备类型, 块设备类型, GNU长名字类型, GNU长链接类型, GNU稀疏类型)
普通类型 = (普通文件类型, 备选普通文件类型, 连续文件类型, GNU稀疏类型)
GNU类型 = (GNU长名字类型, GNU长链接类型, GNU稀疏类型)
PAX字段 = ('path', 'linkpath', 'size', 'mtime', 'uid', 'gid', 'uname', 'gname')
PAX名字字段 = {'path', 'linkpath', 'uname', 'gname'}
PAX数字字段 = {'atime': float, 'ctime': float, 'mtime': float, 'uid': int, 'gid': int, 'size': int}
if os.name == 'nt':
    编码方式 = 'utf-8'
else:
    编码方式 = sys.getfilesystemencoding()

def stn(s, length, encoding, errors):
    """Convert a string to a null-terminated bytes object.
    """
    if s is None:
        raise ValueError('metadata cannot contain None')
    s = s.encode(encoding, errors)
    return s[:length] + (length - len(s)) * 空字节

def nts(s, encoding, errors):
    """Convert a null-terminated bytes object to a string.
    """
    p = s.find(b'\x00')
    if p != -1:
        s = s[:p]
    return s.decode(encoding, errors)

def nti(s):
    """Convert a number field to a python number.
    """
    if s[0] in (128, 255):
        n = 0
        for i in range(len(s) - 1):
            n <<= 8
            n += s[i + 1]
        if s[0] == 255:
            n = -(256 ** (len(s) - 1) - n)
    else:
        try:
            s = nts(s, 'ascii', 'strict')
            n = int(s.strip() or '0', 8)
        except ValueError:
            raise 文件头无效错误('invalid header')
    return n

def itn(n, digits=8, format=默认格式):
    """Convert a python number to a number field.
    """
    original_n = n
    n = int(n)
    if 0 <= n < 8 ** (digits - 1):
        s = bytes('%0*o' % (digits - 1, n), 'ascii') + 空字节
    elif format == GNU格式 and -256 ** (digits - 1) <= n < 256 ** (digits - 1):
        if n >= 0:
            s = bytearray([128])
        else:
            s = bytearray([255])
            n = 256 ** digits + n
        for i in range(digits - 1):
            s.insert(1, n & 255)
            n >>= 8
    else:
        raise ValueError('overflow in number field')
    return s

def 算校验和(buf):
    """Calculate the checksum for a member's header by summing up all
       characters except for the chksum field which is treated as if
       it was filled with spaces. According to the GNU tar sources,
       some tars (Sun and NeXT) calculate chksum with signed char,
       which will be different if there are chars in the buffer with
       the high bit set. So we calculate two checksums, unsigned and
       signed.
    """
    unsigned_chksum = 256 + sum(struct.unpack_from('148B8x356B', buf))
    signed_chksum = 256 + sum(struct.unpack_from('148b8x356b', buf))
    return (unsigned_chksum, signed_chksum)

def 复制文件对象(src, dst, length=None, exception=OSError, bufsize=None):
    """Copy length bytes from fileobj src to fileobj dst.
       If length is None, copy the entire content.
    """
    bufsize = bufsize or 16 * 1024
    if length == 0:
        return
    if length is None:
        shutil.copyfileobj(src, dst, bufsize)
        return
    blocks, remainder = divmod(length, bufsize)
    for b in range(blocks):
        buf = src.read(bufsize)
        if len(buf) < bufsize:
            raise exception('unexpected end of data')
        dst.write(buf)
    if remainder != 0:
        buf = src.read(remainder)
        if len(buf) < remainder:
            raise exception('unexpected end of data')
        dst.write(buf)
    return
_EXTHEADER_READ_CHUNK = 1024 * 1024

def _safe_read(fileobj, size):
    """Read up to *size* bytes from *fileobj* in bounded chunks.

    Returns the same bytes as ``fileobj.read(size)`` would (including a short
    result at end of file), but limits pre-allocation, so an
    oversized size field in a crafted header cannot force a huge allocation.
    """
    if size <= _EXTHEADER_READ_CHUNK:
        return fileobj.read(size)
    chunks = []
    while size > 0:
        chunk = fileobj.read(min(size, _EXTHEADER_READ_CHUNK))
        if not chunk:
            break
        chunks.append(chunk)
        size -= len(chunk)
    return b''.join(chunks)

def _safe_print(s):
    编码 = getattr(sys.stdout, 'encoding', None)
    if 编码 is not None:
        s = s.encode(编码, 'backslashreplace').decode(编码)
    print(s, end=' ')

class TAR错误(Exception):
    """Base exception."""
    pass

class 提取错误(TAR错误):
    """General exception for extract errors."""
    pass

class 读错误(TAR错误):
    """Exception for unreadable tar archives."""
    pass

class 压缩错误(TAR错误):
    """Exception for unavailable compression methods."""
    pass

class 流错误(TAR错误):
    """Exception for unsupported operations on stream-like TarFiles."""
    pass

class 文件头错误(TAR错误):
    """Base exception for header errors."""
    pass

class 空文件头错误(文件头错误):
    """Exception for empty headers."""
    pass

class 截断文件头错误(文件头错误):
    """Exception for truncated headers."""
    pass

class 文件头提前结束错误(文件头错误):
    """Exception for end of file headers."""
    pass

class 文件头无效错误(文件头错误):
    """Exception for invalid headers."""
    pass

class 多余文件头错误(文件头错误):
    """Exception for missing and invalid extended headers."""
    pass

class _LowLevelFile:
    """Low-level file object. Supports reading and writing.
       It is used instead of a regular file object for streaming
       access.
    """

    def __init__(self, name, mode):
        mode = {'r': os.O_RDONLY, 'w': os.O_WRONLY | os.O_CREAT | os.O_TRUNC}[mode]
        if hasattr(os, 'O_BINARY'):
            mode |= os.O_BINARY
        self.fd = os.open(name, mode, 438)

    def close(self):
        os.close(self.fd)

    def read(self, size):
        return os.read(self.fd, size)

    def write(self, s):
        os.write(self.fd, s)

class _Stream:
    """Class that serves as an adapter between TarFile and
       a stream-like object.  The stream-like object only
       needs to have a read() or write() method that works with bytes,
       and the method is accessed blockwise.
       Use of gzip or bzip2 compression is possible.
       A stream-like object could be for example: sys.stdin.buffer,
       sys.stdout.buffer, a socket, a tape device etc.

       _Stream is intended to be used only internally.
    """

    def __init__(self, name, mode, comptype, fileobj, bufsize, compresslevel, preset):
        """Construct a _Stream object.
        """
        self._extfileobj = True
        if fileobj is None:
            fileobj = _LowLevelFile(name, mode)
            self._extfileobj = False
        if comptype == '*':
            fileobj = _StreamProxy(fileobj)
            comptype = fileobj.getcomptype()
        self.名字 = os.fspath(name) if name is not None else ''
        self.模式 = mode
        self.comptype = comptype
        self.文件对象 = fileobj
        self.bufsize = bufsize
        self.buf = b''
        self.pos = 0
        self.已关闭 = False
        try:
            if comptype == 'gz':
                try:
                    import zlib
                except ImportError:
                    raise 压缩错误('zlib module is not available') from None
                self.zlib = zlib
                self.crc = zlib.crc32(b'')
                if mode == 'r':
                    self.exception = zlib.error
                    self._init_read_gz()
                else:
                    self._init_write_gz(compresslevel)
            elif comptype == 'bz2':
                try:
                    import bz2
                except ImportError:
                    raise 压缩错误('bz2 module is not available') from None
                if mode == 'r':
                    self.dbuf = b''
                    self.cmp = bz2.BZ2Decompressor()
                    self.exception = OSError
                else:
                    self.cmp = bz2.BZ2Compressor(compresslevel)
            elif comptype == 'xz':
                try:
                    import lzma
                except ImportError:
                    raise 压缩错误('lzma module is not available') from None
                if mode == 'r':
                    self.dbuf = b''
                    self.cmp = lzma.LZMADecompressor()
                    self.exception = lzma.LZMAError
                else:
                    self.cmp = lzma.LZMACompressor(preset=preset)
            elif comptype == 'zst':
                try:
                    from compression import zstd
                except ImportError:
                    raise 压缩错误('compression.zstd module is not available') from None
                if mode == 'r':
                    self.dbuf = b''
                    self.cmp = zstd.ZstdDecompressor()
                    self.exception = zstd.ZstdError
                else:
                    self.cmp = zstd.ZstdCompressor()
            elif comptype != 'tar':
                raise 压缩错误('unknown compression type %r' % comptype)
        except:
            if not self._extfileobj:
                self.文件对象.close()
            self.已关闭 = True
            raise

    def __del__(self):
        if hasattr(self, 'closed') and (not self.已关闭):
            self.close()

    def _init_write_gz(self, compresslevel):
        """Initialize for writing with gzip compression.
        """
        self.cmp = self.zlib.compressobj(compresslevel, self.zlib.DEFLATED, -self.zlib.MAX_WBITS, self.zlib.DEF_MEM_LEVEL, 0)
        timestamp = struct.pack('<L', int(time.time()))
        self.__write(b'\x1f\x8b\x08\x08' + timestamp + b'\x02\xff')
        if self.名字.endswith('.gz'):
            self.名字 = self.名字[:-3]
        self.名字 = os.path.basename(self.名字)
        self.__write(self.名字.encode('iso-8859-1', 'replace') + 空字节)

    def write(self, s):
        """Write string s to the stream.
        """
        if self.comptype == 'gz':
            self.crc = self.zlib.crc32(s, self.crc)
        self.pos += len(s)
        if self.comptype != 'tar':
            s = self.cmp.compress(s)
        self.__write(s)

    def __write(self, s):
        """Write string s to the stream if a whole new block
           is ready to be written.
        """
        self.buf += s
        while len(self.buf) > self.bufsize:
            self.文件对象.write(self.buf[:self.bufsize])
            self.buf = self.buf[self.bufsize:]

    def close(self):
        """Close the _Stream object. No operation should be
           done on it afterwards.
        """
        if self.已关闭:
            return
        self.已关闭 = True
        try:
            if self.模式 == 'w' and self.comptype != 'tar':
                self.buf += self.cmp.flush()
            if self.模式 == 'w' and self.buf:
                self.文件对象.write(self.buf)
                self.buf = b''
                if self.comptype == 'gz':
                    self.文件对象.write(struct.pack('<L', self.crc))
                    self.文件对象.write(struct.pack('<L', self.pos & 4294967295))
        finally:
            if not self._extfileobj:
                self.文件对象.close()

    def _init_read_gz(self):
        """Initialize for reading a gzip compressed fileobj.
        """
        self.cmp = self.zlib.decompressobj(-self.zlib.MAX_WBITS)
        self.dbuf = b''
        if self.__read(2) != b'\x1f\x8b':
            raise 读错误('not a gzip file')
        if self.__read(1) != b'\x08':
            raise 压缩错误('unsupported compression method')
        flag = ord(self.__read(1))
        self.__read(6)
        if flag & 4:
            xlen = ord(self.__read(1)) + 256 * ord(self.__read(1))
            self.__read(xlen)
        if flag & 8:
            while True:
                s = self.__read(1)
                if not s or s == 空字节:
                    break
        if flag & 16:
            while True:
                s = self.__read(1)
                if not s or s == 空字节:
                    break
        if flag & 2:
            self.__read(2)

    def tell(self):
        """Return the stream's file pointer position.
        """
        return self.pos

    def seek(self, pos=0):
        """Set the stream's file pointer to pos. Negative seeking
           is forbidden.
        """
        if pos - self.pos >= 0:
            blocks, remainder = divmod(pos - self.pos, self.bufsize)
            for i in range(blocks):
                data = self.read(self.bufsize)
                if not data:
                    break
            self.read(remainder)
        else:
            raise 流错误('seeking backwards is not allowed')
        return self.pos

    def read(self, size):
        """Return the next size number of bytes from the stream."""
        assert size is not None
        buf = self._read(size)
        self.pos += len(buf)
        return buf

    def _read(self, size):
        """Return size bytes from the stream.
        """
        if self.comptype == 'tar':
            return self.__read(size)
        c = len(self.dbuf)
        t = [self.dbuf]
        while c < size:
            if self.buf:
                buf = self.buf
                self.buf = b''
            else:
                buf = self.文件对象.read(self.bufsize)
                if not buf:
                    break
            try:
                buf = self.cmp.decompress(buf)
            except self.exception as e:
                raise 读错误('invalid compressed data') from e
            t.append(buf)
            c += len(buf)
        t = b''.join(t)
        self.dbuf = t[size:]
        return t[:size]

    def __read(self, size):
        """Return size bytes from stream. If internal buffer is empty,
           read another block from the stream.
        """
        c = len(self.buf)
        t = [self.buf]
        while c < size:
            buf = self.文件对象.read(self.bufsize)
            if not buf:
                break
            t.append(buf)
            c += len(buf)
        t = b''.join(t)
        self.buf = t[size:]
        return t[:size]
_装类转发(_Stream, {}, {'closed': '已关闭', 'fileobj': '文件对象', 'mode': '模式', 'name': '名字'})

class _StreamProxy(object):
    """Small proxy class that enables transparent compression
       detection for the Stream interface (mode 'r|*').
    """

    def __init__(self, fileobj):
        self.文件对象 = fileobj
        self.buf = self.文件对象.read(块大小)

    def read(self, size):
        self.read = self.文件对象.read
        return self.buf

    def getcomptype(self):
        if self.buf.startswith(b'\x1f\x8b\x08'):
            return 'gz'
        elif self.buf[0:3] == b'BZh' and self.buf[4:10] == b'1AY&SY':
            return 'bz2'
        elif self.buf.startswith((b']\x00\x00\x80', b'\xfd7zXZ')):
            return 'xz'
        elif self.buf.startswith(b'(\xb5/\xfd'):
            return 'zst'
        else:
            return 'tar'

    def close(self):
        self.文件对象.close()
_装类转发(_StreamProxy, {}, {'fileobj': '文件对象'})

class _FileInFile(object):
    """A thin wrapper around an existing file object that
       provides a part of its data as an individual file
       object.
    """

    def __init__(self, fileobj, offset, size, name, blockinfo=None):
        self.文件对象 = fileobj
        self.偏移 = offset
        self.大小 = size
        self.position = 0
        self.名字 = name
        self.已关闭 = False
        if blockinfo is None:
            blockinfo = [(0, size)]
        self.map_index = 0
        self.map = []
        lastpos = 0
        realpos = self.偏移
        for offset, size in blockinfo:
            if offset > lastpos:
                self.map.append((False, lastpos, offset, None))
            self.map.append((True, offset, offset + size, realpos))
            realpos += size
            lastpos = offset + size
        if lastpos < self.大小:
            self.map.append((False, lastpos, self.大小, None))

    def flush(self):
        pass

    @property
    def 模式(self):
        return 'rb'

    def readable(self):
        return True

    def writable(self):
        return False

    def seekable(self):
        return self.文件对象.seekable()

    def tell(self):
        """Return the current file position.
        """
        return self.position

    def seek(self, position, whence=io.SEEK_SET):
        """Seek to a position in the file.
        """
        if whence == io.SEEK_SET:
            self.position = min(max(position, 0), self.大小)
        elif whence == io.SEEK_CUR:
            if position < 0:
                self.position = max(self.position + position, 0)
            else:
                self.position = min(self.position + position, self.大小)
        elif whence == io.SEEK_END:
            self.position = max(min(self.大小 + position, self.大小), 0)
        else:
            raise ValueError('Invalid argument')
        return self.position

    def read(self, size=None):
        """Read data from the file.
        """
        if size is None:
            size = self.大小 - self.position
        else:
            size = min(size, self.大小 - self.position)
        buf = b''
        while size > 0:
            while True:
                data, start, stop, 偏移 = self.map[self.map_index]
                if start <= self.position < stop:
                    break
                else:
                    self.map_index += 1
                    if self.map_index == len(self.map):
                        self.map_index = 0
            length = min(size, stop - self.position)
            if data:
                self.文件对象.seek(偏移 + (self.position - start))
                b = self.文件对象.read(length)
                if len(b) != length:
                    raise 读错误('unexpected end of data')
                buf += b
            else:
                buf += 空字节 * length
            size -= length
            self.position += length
        return buf

    def readinto(self, b):
        buf = self.read(len(b))
        b[:len(buf)] = buf
        return len(buf)

    def close(self):
        self.已关闭 = True
_装类转发(_FileInFile, {'mode': '模式'}, {'closed': '已关闭', 'fileobj': '文件对象', 'mode': '模式', 'name': '名字', 'offset': '偏移', 'size': '大小'})

class 提取文件对象(io.BufferedReader):

    def __init__(self, tarfile, tarinfo):
        文件对象 = _FileInFile(tarfile.fileobj, tarinfo.offset_data, tarinfo.size, tarinfo.name, tarinfo.sparse)
        super().__init__(文件对象)

class 过滤器错误(TAR错误):
    pass

class 绝对路径错误(过滤器错误):

    def __init__(self, tarinfo):
        self.tarinfo = tarinfo
        super().__init__(f'member {tarinfo.name!r} has an absolute path')

class 越出目标目录错误(过滤器错误):

    def __init__(self, tarinfo, path):
        self.tarinfo = tarinfo
        self._path = path
        super().__init__(f'{tarinfo.name!r} would be extracted to {path!r}, ' + 'which is outside the destination')

class 特殊文件错误(过滤器错误):

    def __init__(self, tarinfo):
        self.tarinfo = tarinfo
        super().__init__(f'{tarinfo.name!r} is a special file')

class 绝对链接错误(过滤器错误):

    def __init__(self, tarinfo):
        self.tarinfo = tarinfo
        super().__init__(f'{tarinfo.name!r} is a link to an absolute path')

class 链接越出目标错误(过滤器错误):

    def __init__(self, tarinfo, path):
        self.tarinfo = tarinfo
        self._path = path
        super().__init__(f'{tarinfo.name!r} would link to {path!r}, ' + 'which is outside the destination')

class 链接回退错误(过滤器错误):

    def __init__(self, tarinfo, path):
        self.tarinfo = tarinfo
        self._path = path
        super().__init__(f'link {tarinfo.name!r} would be extracted as a ' + f'copy of {path!r}, which was rejected')
_FILTER_ERRORS = (过滤器错误, OSError, 提取错误)

def _get_filtered_attrs(member, dest_path, for_data=True):
    new_attrs = {}
    名字 = member.name
    dest_path = os.path.realpath(dest_path, strict=os.path.ALLOW_MISSING)
    if 名字.startswith(('/', os.sep)):
        名字 = new_attrs['name'] = member.path.lstrip('/' + os.sep)
    if os.path.isabs(名字):
        raise 绝对路径错误(member)
    target_path = os.path.realpath(os.path.join(dest_path, 名字), strict=os.path.ALLOW_MISSING)
    if os.path.commonpath([target_path, dest_path]) != dest_path:
        raise 越出目标目录错误(member, target_path)
    模式 = member.mode
    if 模式 is not None:
        模式 = 模式 & 493
        if for_data:
            if member.isreg() or member.islnk():
                if not 模式 & 64:
                    模式 &= ~73
                模式 |= 384
            elif member.isdir() or member.issym():
                模式 = None
            else:
                raise 特殊文件错误(member)
        if 模式 != member.mode:
            new_attrs['mode'] = 模式
    if for_data:
        if member.uid is not None:
            new_attrs['uid'] = None
        if member.gid is not None:
            new_attrs['gid'] = None
        if member.uname is not None:
            new_attrs['uname'] = None
        if member.gname is not None:
            new_attrs['gname'] = None
        if member.islnk() or member.issym():
            if os.path.isabs(member.linkname):
                raise 绝对链接错误(member)
            if target_path == dest_path:
                raise 越出目标目录错误(member, target_path)
            normalized = os.path.normpath(member.linkname)
            if normalized != member.linkname:
                new_attrs['linkname'] = normalized
            if member.issym():
                link_dir = os.path.dirname(名字.rstrip('/' + os.sep))
                target_path = os.path.join(dest_path, link_dir, normalized)
            else:
                target_path = os.path.join(dest_path, normalized)
            target_path = os.path.realpath(target_path, strict=os.path.ALLOW_MISSING)
            if os.path.commonpath([target_path, dest_path]) != dest_path:
                raise 链接越出目标错误(member, target_path)
    return new_attrs

def fully_trusted_filter(member, dest_path):
    return member

def tar_filter(member, dest_path):
    new_attrs = _get_filtered_attrs(member, dest_path, False)
    if new_attrs:
        return member.replace(**new_attrs, deep=False)
    return member

def data_filter(member, dest_path):
    new_attrs = _get_filtered_attrs(member, dest_path, True)
    if new_attrs:
        return member.replace(**new_attrs, deep=False)
    return member
_NAMED_FILTERS = {'fully_trusted': fully_trusted_filter, 'tar': tar_filter, 'data': data_filter}
_KEEP = object()
_header_length_prefix_re = re.compile(b'([0-9]{1,20}) ')

class TAR条目(object):
    """Informational class which holds the details about an
       archive member given by a tar header block.
       TarInfo objects are returned by TarFile.getmember(),
       TarFile.getmembers() and TarFile.gettarinfo() and are
       usually created internally.
    """
    __slots__ = dict(name='Name of the archive member.', mode='Permission bits.', uid='User ID of the user who originally stored this member.', gid='Group ID of the user who originally stored this member.', size='Size in bytes.', mtime='Time of last modification.', chksum='Header checksum.', type='File type.  type is usually one of these constants: REGTYPE,\nAREGTYPE, LNKTYPE, SYMTYPE, DIRTYPE, FIFOTYPE, CONTTYPE, CHRTYPE,\nBLKTYPE, GNUTYPE_SPARSE.', linkname='Name of the target file name, which is only present in TarInfo\nobjects of type LNKTYPE and SYMTYPE.', uname='User name.', gname='Group name.', devmajor='Device major number.', devminor='Device minor number.', offset='The tar header starts here.', offset_data="The file's data starts here.", pax_headers='A dictionary containing key-value pairs of an associated pax\nextended header.', sparse='Sparse member information.', _tarfile=None, _sparse_structs=None, _link_target=None)

    def __init__(self, name=''):
        """Construct a TarInfo object. name is the optional name
           of the member.
        """
        self.名字 = name
        self.模式 = 420
        self.用户ID = 0
        self.组ID = 0
        self.大小 = 0
        self.修改时间 = 0
        self.校验和 = 0
        self.type = 普通文件类型
        self.链接名 = ''
        self.用户名 = ''
        self.组名 = ''
        self.主设备号 = 0
        self.次设备号 = 0
        self.偏移 = 0
        self.数据偏移 = 0
        self.稀疏信息 = None
        self.PAX头 = {}

    @property
    def tarfile(self):
        import warnings
        warnings.warn('The undocumented "tarfile" attribute of TarInfo objects ' + 'is deprecated and will be removed in Python 3.16', DeprecationWarning, stacklevel=2)
        return self._tarfile

    @tarfile.setter
    def tarfile(self, tarfile):
        import warnings
        warnings.warn('The undocumented "tarfile" attribute of TarInfo objects ' + 'is deprecated and will be removed in Python 3.16', DeprecationWarning, stacklevel=2)
        self._tarfile = tarfile

    @property
    def 路径(self):
        """In pax headers, "name" is called "path"."""
        return self.名字

    @路径.setter
    def 路径(self, name):
        self.名字 = name

    @property
    def 链接路径(self):
        """In pax headers, "linkname" is called "linkpath"."""
        return self.链接名

    @链接路径.setter
    def 链接路径(self, linkname):
        self.链接名 = linkname

    def __repr__(self):
        return '<%s %r at %#x>' % (self.__class__.__name__, self.名字, id(self))

    def replace(self, *, name=_KEEP, mtime=_KEEP, mode=_KEEP, linkname=_KEEP, uid=_KEEP, gid=_KEEP, uname=_KEEP, gname=_KEEP, deep=True, _KEEP=_KEEP):
        """Return a deep copy of self with the given attributes replaced.
        """
        if deep:
            result = copy.deepcopy(self)
        else:
            result = copy.copy(self)
        if name is not _KEEP:
            result.name = name
        if mtime is not _KEEP:
            result.mtime = mtime
        if mode is not _KEEP:
            result.mode = mode
        if linkname is not _KEEP:
            result.linkname = linkname
        if uid is not _KEEP:
            result.uid = uid
        if gid is not _KEEP:
            result.gid = gid
        if uname is not _KEEP:
            result.uname = uname
        if gname is not _KEEP:
            result.gname = gname
        return result

    def 取信息(self):
        """Return the TarInfo's attributes as a dictionary.
        """
        if self.模式 is None:
            模式 = None
        else:
            模式 = self.模式 & 4095
        info = {'name': self.名字, 'mode': 模式, 'uid': self.用户ID, 'gid': self.组ID, 'size': self.大小, 'mtime': self.修改时间, 'chksum': self.校验和, 'type': self.type, 'linkname': self.链接名, 'uname': self.用户名, 'gname': self.组名, 'devmajor': self.主设备号, 'devminor': self.次设备号}
        if info['type'] == 目录类型 and (not info['name'].endswith('/')):
            info['name'] += '/'
        return info

    def 转字节块(self, format=默认格式, encoding=编码方式, errors='surrogateescape'):
        """Return a tar header as a string of 512 byte blocks.
        """
        info = self.取信息()
        for 名字, value in info.items():
            if value is None:
                raise ValueError('%s may not be None' % 名字)
        if format == USTAR格式:
            return self.造USTAR头(info, encoding, errors)
        elif format == GNU格式:
            return self.造GNU头(info, encoding, errors)
        elif format == PAX格式:
            return self.造PAX头(info, encoding)
        else:
            raise ValueError('invalid format')

    def 造USTAR头(self, info, encoding, errors):
        """Return the object as a ustar header block.
        """
        info['magic'] = POSIX魔数
        if len(info['linkname'].encode(encoding, errors)) > 链接名长度:
            raise ValueError('linkname is too long')
        if len(info['name'].encode(encoding, errors)) > 名字长度:
            info['prefix'], info['name'] = self._posix_split_name(info['name'], encoding, errors)
        return self._create_header(info, USTAR格式, encoding, errors)

    def 造GNU头(self, info, encoding, errors):
        """Return the object as a GNU header block sequence.
        """
        info['magic'] = GNU魔数
        buf = b''
        if len(info['linkname'].encode(encoding, errors)) > 链接名长度:
            buf += self._create_gnu_long_header(info['linkname'], GNU长链接类型, encoding, errors)
        if len(info['name'].encode(encoding, errors)) > 名字长度:
            buf += self._create_gnu_long_header(info['name'], GNU长名字类型, encoding, errors)
        return buf + self._create_header(info, GNU格式, encoding, errors)

    def 造PAX头(self, info, encoding):
        """Return the object as a ustar header block. If it cannot be
           represented this way, prepend a pax extended header sequence
           with supplement information.
        """
        info['magic'] = POSIX魔数
        PAX头 = self.PAX头.copy()
        for 名字, hname, length in (('name', 'path', 名字长度), ('linkname', 'linkpath', 链接名长度), ('uname', 'uname', 32), ('gname', 'gname', 32)):
            if hname in PAX头:
                continue
            try:
                info[名字].encode('ascii', 'strict')
            except UnicodeEncodeError:
                PAX头[hname] = info[名字]
                continue
            if len(info[名字]) > length:
                PAX头[hname] = info[名字]
        for 名字, digits in (('uid', 8), ('gid', 8), ('size', 12), ('mtime', 12)):
            needs_pax = False
            val = info[名字]
            val_is_float = isinstance(val, float)
            val_int = round(val) if val_is_float else val
            if not 0 <= val_int < 8 ** (digits - 1):
                info[名字] = 0
                needs_pax = True
            elif val_is_float:
                info[名字] = val_int
                needs_pax = True
            if needs_pax and 名字 not in PAX头:
                PAX头[名字] = str(val)
        if PAX头:
            buf = self._create_pax_generic_header(PAX头, 扩展头类型, encoding)
        else:
            buf = b''
        return buf + self._create_header(info, USTAR格式, 'ascii', 'replace')

    @classmethod
    def 造PAX全局头(cls, pax_headers):
        """Return the object as a pax global header block sequence.
        """
        return cls._create_pax_generic_header(pax_headers, 全局扩展头类型, 'utf-8')

    def _posix_split_name(self, name, encoding, errors):
        """Split a name longer than 100 chars into a prefix
           and a name part.
        """
        components = name.split('/')
        for i in range(1, len(components)):
            prefix = '/'.join(components[:i])
            name = '/'.join(components[i:])
            if len(prefix.encode(encoding, errors)) <= 前缀长度 and len(name.encode(encoding, errors)) <= 名字长度:
                break
        else:
            raise ValueError('name is too long')
        return (prefix, name)

    @staticmethod
    def _create_header(info, format, encoding, errors):
        """Return a header block. info is a dictionary with file
           information, format must be one of the *_FORMAT constants.
        """
        has_device_fields = info.get('type') in (字符设备类型, 块设备类型)
        if has_device_fields:
            主设备号 = itn(info.get('devmajor', 0), 8, format)
            次设备号 = itn(info.get('devminor', 0), 8, format)
        else:
            主设备号 = stn('', 8, encoding, errors)
            次设备号 = stn('', 8, encoding, errors)
        filetype = info.get('type', 普通文件类型)
        if filetype is None:
            raise ValueError('TarInfo.type must not be None')
        parts = [stn(info.get('name', ''), 100, encoding, errors), itn(info.get('mode', 0) & 4095, 8, format), itn(info.get('uid', 0), 8, format), itn(info.get('gid', 0), 8, format), itn(info.get('size', 0), 12, format), itn(info.get('mtime', 0), 12, format), b'        ', filetype, stn(info.get('linkname', ''), 100, encoding, errors), info.get('magic', POSIX魔数), stn(info.get('uname', ''), 32, encoding, errors), stn(info.get('gname', ''), 32, encoding, errors), 主设备号, 次设备号, stn(info.get('prefix', ''), 155, encoding, errors)]
        buf = struct.pack('%ds' % 块大小, b''.join(parts))
        校验和 = 算校验和(buf[-块大小:])[0]
        buf = buf[:-364] + bytes('%06o\x00' % 校验和, 'ascii') + buf[-357:]
        return buf

    @staticmethod
    def _create_payload(payload):
        """Return the string payload filled with zero bytes
           up to the next 512 byte border.
        """
        blocks, remainder = divmod(len(payload), 块大小)
        if remainder > 0:
            payload += (块大小 - remainder) * 空字节
        return payload

    @classmethod
    def _create_gnu_long_header(cls, name, type, encoding, errors):
        """Return a GNUTYPE_LONGNAME or GNUTYPE_LONGLINK sequence
           for name.
        """
        name = name.encode(encoding, errors) + 空字节
        info = {}
        info['name'] = '././@LongLink'
        info['type'] = type
        info['size'] = len(name)
        info['magic'] = GNU魔数
        return cls._create_header(info, USTAR格式, encoding, errors) + cls._create_payload(name)

    @classmethod
    def _create_pax_generic_header(cls, pax_headers, type, encoding):
        """Return a POSIX.1-2008 extended or global header sequence
           that contains a list of keyword, value pairs. The values
           must be strings.
        """
        binary = False
        for keyword, value in pax_headers.items():
            try:
                value.encode('utf-8', 'strict')
            except UnicodeEncodeError:
                binary = True
                break
        records = b''
        if binary:
            records += b'21 hdrcharset=BINARY\n'
        for keyword, value in pax_headers.items():
            keyword = keyword.encode('utf-8')
            if binary:
                value = value.encode(encoding, 'surrogateescape')
            else:
                value = value.encode('utf-8')
            l = len(keyword) + len(value) + 3
            n = p = 0
            while True:
                n = l + len(str(p))
                if n == p:
                    break
                p = n
            records += bytes(str(p), 'ascii') + b' ' + keyword + b'=' + value + b'\n'
        info = {}
        info['name'] = '././@PaxHeader'
        info['type'] = type
        info['size'] = len(records)
        info['magic'] = POSIX魔数
        return cls._create_header(info, USTAR格式, 'ascii', 'replace') + cls._create_payload(records)

    @classmethod
    def 从块解析(cls, buf, encoding, errors):
        """Construct a TarInfo object from a 512 byte bytes object.

        To support the old v7 tar format AREGTYPE headers are
        transformed to DIRTYPE headers if their name ends in '/'.
        """
        return cls._frombuf(buf, encoding, errors)

    @classmethod
    def _frombuf(cls, buf, encoding, errors, *, dircheck=True):
        """Construct a TarInfo object from a 512 byte bytes object.

        If ``dircheck`` is set to ``True`` then ``AREGTYPE`` headers will
        be normalized to ``DIRTYPE`` if the name ends in a trailing slash.
        ``dircheck`` must be set to ``False`` if this function is called
        on a follow-up header such as ``GNUTYPE_LONGNAME``.
        """
        if len(buf) == 0:
            raise 空文件头错误('empty header')
        if len(buf) != 块大小:
            raise 截断文件头错误('truncated header')
        if buf.count(空字节) == 块大小:
            raise 文件头提前结束错误('end of file header')
        校验和 = nti(buf[148:156])
        if 校验和 not in 算校验和(buf):
            raise 文件头无效错误('bad checksum')
        obj = cls()
        obj.name = nts(buf[0:100], encoding, errors)
        obj.mode = nti(buf[100:108])
        obj.uid = nti(buf[108:116])
        obj.gid = nti(buf[116:124])
        obj.size = nti(buf[124:136])
        obj.mtime = nti(buf[136:148])
        obj.chksum = 校验和
        obj.type = buf[156:157]
        obj.linkname = nts(buf[157:257], encoding, errors)
        obj.uname = nts(buf[265:297], encoding, errors)
        obj.gname = nts(buf[297:329], encoding, errors)
        obj.devmajor = nti(buf[329:337])
        obj.devminor = nti(buf[337:345])
        prefix = nts(buf[345:500], encoding, errors)
        if dircheck and obj.type == 备选普通文件类型 and obj.name.endswith('/'):
            obj.type = 目录类型
        if obj.type == GNU稀疏类型:
            pos = 386
            structs = []
            for i in range(4):
                try:
                    偏移 = nti(buf[pos:pos + 12])
                    numbytes = nti(buf[pos + 12:pos + 24])
                except ValueError:
                    break
                structs.append((偏移, numbytes))
                pos += 24
            isextended = bool(buf[482])
            origsize = nti(buf[483:495])
            obj._sparse_structs = (structs, isextended, origsize)
        if obj.isdir():
            obj.name = obj.name.rstrip('/')
        if prefix and obj.type not in GNU类型:
            obj.name = prefix + '/' + obj.name
        return obj

    @classmethod
    def 从压缩包解析(cls, tarfile):
        """Return the next TarInfo object from TarFile object
           tarfile.
        """
        return cls._fromtarfile(tarfile)

    @classmethod
    def _fromtarfile(cls, tarfile, *, dircheck=True):
        """
        See dircheck documentation in _frombuf().
        """
        buf = tarfile.fileobj.read(块大小)
        obj = cls._frombuf(buf, tarfile.encoding, tarfile.errors, dircheck=dircheck)
        obj.offset = tarfile.fileobj.tell() - 块大小
        return obj._proc_member(tarfile)

    def _proc_member(self, tarfile):
        """Choose the right processing method depending on
           the type and call it.
        """
        if self.type in (GNU长名字类型, GNU长链接类型):
            return self._proc_gnulong(tarfile)
        elif self.type == GNU稀疏类型:
            return self._proc_sparse(tarfile)
        elif self.type in (扩展头类型, 全局扩展头类型, SOLARIS扩展头类型):
            return self._proc_pax(tarfile)
        else:
            return self._proc_builtin(tarfile)

    def _proc_builtin(self, tarfile):
        """Process a builtin type or an unknown type which
           will be treated as a regular file.
        """
        self.数据偏移 = tarfile.fileobj.tell()
        偏移 = self.数据偏移
        if self.是普通文件吗() or self.type not in 支持的类型:
            偏移 += self._block(self.大小)
        tarfile.offset = 偏移
        self._apply_pax_info(tarfile.pax_headers, tarfile.encoding, tarfile.errors)
        if self.是目录吗():
            self.名字 = self.名字.rstrip('/')
        return self

    def _proc_gnulong(self, tarfile):
        """Process the blocks that hold a GNU longname
           or longlink member.
        """
        buf = _safe_read(tarfile.fileobj, self._block(self.大小))
        try:
            next = self._fromtarfile(tarfile, dircheck=False)
        except 文件头错误 as e:
            raise 多余文件头错误(str(e)) from None
        next.offset = self.偏移
        if self.type == GNU长名字类型:
            next.name = nts(buf, tarfile.encoding, tarfile.errors)
        elif self.type == GNU长链接类型:
            next.linkname = nts(buf, tarfile.encoding, tarfile.errors)
        if next.isdir():
            next.name = next.name.removesuffix('/')
        return next

    def _proc_sparse(self, tarfile):
        """Process a GNU sparse header plus extra headers.
        """
        structs, isextended, origsize = self._sparse_structs
        del self._sparse_structs
        while isextended:
            buf = tarfile.fileobj.read(块大小)
            pos = 0
            for i in range(21):
                try:
                    偏移 = nti(buf[pos:pos + 12])
                    numbytes = nti(buf[pos + 12:pos + 24])
                except ValueError:
                    break
                if 偏移 and numbytes:
                    structs.append((偏移, numbytes))
                pos += 24
            isextended = bool(buf[504])
        self.稀疏信息 = structs
        self.数据偏移 = tarfile.fileobj.tell()
        tarfile.offset = self.数据偏移 + self._block(self.大小)
        self.大小 = origsize
        return self

    def _proc_pax(self, tarfile):
        """Process an extended or global header as described in
           POSIX.1-2008.
        """
        buf = _safe_read(tarfile.fileobj, self._block(self.大小))
        if self.type == 全局扩展头类型:
            PAX头 = tarfile.pax_headers
        else:
            PAX头 = tarfile.pax_headers.copy()
        pos = 0
        编码 = None
        raw_headers = []
        while len(buf) > pos and buf[pos] != 0:
            if not (match := _header_length_prefix_re.match(buf, pos)):
                raise 文件头无效错误('invalid header')
            try:
                length = int(match.group(1))
            except ValueError:
                raise 文件头无效错误('invalid header')
            if length < 5:
                raise 文件头无效错误('invalid header')
            if pos + length > len(buf):
                raise 文件头无效错误('invalid header')
            header_value_end_offset = match.start(1) + length - 1
            keyword_and_value = buf[match.end(1) + 1:header_value_end_offset]
            raw_keyword, equals, raw_value = keyword_and_value.partition(b'=')
            if not raw_keyword or equals != b'=' or buf[header_value_end_offset] != 10:
                raise 文件头无效错误('invalid header')
            raw_headers.append((length, raw_keyword, raw_value))
            if raw_keyword == b'hdrcharset' and 编码 is None:
                if raw_value == b'BINARY':
                    编码 = tarfile.encoding
                else:
                    编码 = 'utf-8'
            pos += length
        if 编码 is None:
            编码 = 'utf-8'
        for length, raw_keyword, raw_value in raw_headers:
            keyword = self._decode_pax_field(raw_keyword, 'utf-8', 'utf-8', tarfile.errors)
            if keyword in PAX名字字段:
                value = self._decode_pax_field(raw_value, 编码, tarfile.encoding, tarfile.errors)
            else:
                value = self._decode_pax_field(raw_value, 'utf-8', 'utf-8', tarfile.errors)
            PAX头[keyword] = value
        try:
            next = self._fromtarfile(tarfile, dircheck=False)
        except 文件头错误 as e:
            raise 多余文件头错误(str(e)) from None
        if 'GNU.sparse.map' in PAX头:
            self._proc_gnusparse_01(next, PAX头)
        elif 'GNU.sparse.size' in PAX头:
            self._proc_gnusparse_00(next, raw_headers)
        elif PAX头.get('GNU.sparse.major') == '1' and PAX头.get('GNU.sparse.minor') == '0':
            self._proc_gnusparse_10(next, PAX头, tarfile)
        if self.type in (扩展头类型, SOLARIS扩展头类型):
            next._apply_pax_info(PAX头, tarfile.encoding, tarfile.errors)
            next.offset = self.偏移
            if 'size' in PAX头:
                偏移 = next.offset_data
                if next.isreg() or next.type not in 支持的类型:
                    偏移 += next._block(next.size)
                tarfile.offset = 偏移
        return next

    def _proc_gnusparse_00(self, next, raw_headers):
        """Process a GNU tar extended sparse header, version 0.0.
        """
        offsets = []
        numbytes = []
        for _, keyword, value in raw_headers:
            if keyword == b'GNU.sparse.offset':
                try:
                    offsets.append(int(value.decode()))
                except ValueError:
                    raise 文件头无效错误('invalid header')
            elif keyword == b'GNU.sparse.numbytes':
                try:
                    numbytes.append(int(value.decode()))
                except ValueError:
                    raise 文件头无效错误('invalid header')
        next.sparse = list(zip(offsets, numbytes))

    def _proc_gnusparse_01(self, next, pax_headers):
        """Process a GNU tar extended sparse header, version 0.1.
        """
        稀疏信息 = [int(x) for x in pax_headers['GNU.sparse.map'].split(',')]
        next.sparse = list(zip(稀疏信息[::2], 稀疏信息[1::2]))

    def _proc_gnusparse_10(self, next, pax_headers, tarfile):
        """Process a GNU tar extended sparse header, version 1.0.
        """
        fields = None
        稀疏信息 = []
        buf = tarfile.fileobj.read(块大小)
        fields, buf = buf.split(b'\n', 1)
        fields = int(fields)
        while len(稀疏信息) < fields * 2:
            if b'\n' not in buf:
                buf += tarfile.fileobj.read(块大小)
            number, buf = buf.split(b'\n', 1)
            稀疏信息.append(int(number))
        next.offset_data = tarfile.fileobj.tell()
        next.sparse = list(zip(稀疏信息[::2], 稀疏信息[1::2]))

    def _apply_pax_info(self, pax_headers, encoding, errors):
        """Replace fields with supplemental information from a previous
           pax extended or global header.
        """
        for keyword, value in pax_headers.items():
            if keyword == 'GNU.sparse.name':
                setattr(self, 'path', value)
            elif keyword == 'GNU.sparse.size':
                setattr(self, 'size', int(value))
            elif keyword == 'GNU.sparse.realsize':
                setattr(self, 'size', int(value))
            elif keyword in PAX字段:
                if keyword in PAX数字字段:
                    try:
                        value = PAX数字字段[keyword](value)
                    except ValueError:
                        value = 0
                if keyword == 'path':
                    value = value.rstrip('/')
                setattr(self, keyword, value)
        self.PAX头 = pax_headers.copy()

    def _decode_pax_field(self, value, encoding, fallback_encoding, fallback_errors):
        """Decode a single field from a pax record.
        """
        try:
            return value.decode(encoding, 'strict')
        except UnicodeDecodeError:
            return value.decode(fallback_encoding, fallback_errors)

    def _block(self, count):
        """Round up a byte count by BLOCKSIZE and return it,
           e.g. _block(834) => 1024.
        """
        if count < 0:
            raise 文件头无效错误('invalid offset')
        blocks, remainder = divmod(count, 块大小)
        if remainder:
            blocks += 1
        return blocks * 块大小

    def 是普通文件吗(self):
        """Return True if the Tarinfo object is a regular file."""
        return self.type in 普通类型

    def 是文件吗(self):
        """Return True if the Tarinfo object is a regular file."""
        return self.是普通文件吗()

    def 是目录吗(self):
        """Return True if it is a directory."""
        return self.type == 目录类型

    def 是符号链接吗(self):
        """Return True if it is a symbolic link."""
        return self.type == 符号链接类型

    def 是硬链接吗(self):
        """Return True if it is a hard link."""
        return self.type == 硬链接类型

    def 是字符设备吗(self):
        """Return True if it is a character device."""
        return self.type == 字符设备类型

    def 是块设备吗(self):
        """Return True if it is a block device."""
        return self.type == 块设备类型

    def 是FIFO吗(self):
        """Return True if it is a FIFO."""
        return self.type == FIFO类型

    def 是稀疏文件吗(self):
        return self.稀疏信息 is not None

    def 是设备吗(self):
        """Return True if it is one of character device, block device or FIFO."""
        return self.type in (字符设备类型, 块设备类型, FIFO类型)
_装类转发(TAR条目, {'create_gnu_header': '造GNU头', 'create_pax_global_header': '造PAX全局头', 'create_pax_header': '造PAX头', 'create_ustar_header': '造USTAR头', 'frombuf': '从块解析', 'fromtarfile': '从压缩包解析', 'get_info': '取信息', 'isblk': '是块设备吗', 'ischr': '是字符设备吗', 'isdev': '是设备吗', 'isdir': '是目录吗', 'isfifo': '是FIFO吗', 'isfile': '是文件吗', 'islnk': '是硬链接吗', 'isreg': '是普通文件吗', 'issparse': '是稀疏文件吗', 'issym': '是符号链接吗', 'linkpath': '链接路径', 'path': '路径', 'tobuf': '转字节块'}, {'chksum': '校验和', 'create_gnu_header': '造GNU头', 'create_pax_global_header': '造PAX全局头', 'create_pax_header': '造PAX头', 'create_ustar_header': '造USTAR头', 'devmajor': '主设备号', 'devminor': '次设备号', 'frombuf': '从块解析', 'fromtarfile': '从压缩包解析', 'get_info': '取信息', 'gid': '组ID', 'gname': '组名', 'isblk': '是块设备吗', 'ischr': '是字符设备吗', 'isdev': '是设备吗', 'isdir': '是目录吗', 'isfifo': '是FIFO吗', 'isfile': '是文件吗', 'islnk': '是硬链接吗', 'isreg': '是普通文件吗', 'issparse': '是稀疏文件吗', 'issym': '是符号链接吗', 'linkname': '链接名', 'linkpath': '链接路径', 'mode': '模式', 'mtime': '修改时间', 'name': '名字', 'offset': '偏移', 'offset_data': '数据偏移', 'path': '路径', 'pax_headers': 'PAX头', 'size': '大小', 'sparse': '稀疏信息', 'tobuf': '转字节块', 'uid': '用户ID', 'uname': '用户名'})

class TAR文件(object):
    """The TarFile Class provides an interface to tar archives.
    """
    调试 = 0
    解引用 = False
    忽略零块 = False
    错误级别 = 1
    format = 默认格式
    编码 = 编码方式
    出错怎么办 = None
    tarinfo = TAR条目
    fileobject = 提取文件对象
    extraction_filter = None

    def __init__(self, name=None, mode='r', fileobj=None, format=None, tarinfo=None, dereference=None, ignore_zeros=None, encoding=None, errors='surrogateescape', pax_headers=None, debug=None, errorlevel=None, copybufsize=None, stream=False):
        """Open an (uncompressed) tar archive 'name'. 'mode' is either 'r' to
           read from an existing archive, 'a' to append data to an existing
           file or 'w' to create a new file overwriting an existing one. 'mode'
           defaults to 'r'.
           If 'fileobj' is given, it is used for reading or writing data. If it
           can be determined, 'mode' is overridden by 'fileobj's mode.
           'fileobj' is not closed, when TarFile is closed.
        """
        modes = {'r': 'rb', 'a': 'r+b', 'w': 'wb', 'x': 'xb'}
        if mode not in modes:
            raise ValueError("mode must be 'r', 'a', 'w' or 'x'")
        self.模式 = mode
        self._mode = modes[mode]
        if not fileobj:
            if self.模式 == 'a' and (not os.path.exists(name)):
                self.模式 = 'w'
                self._mode = 'wb'
            fileobj = bltn_open(name, self._mode)
            self._extfileobj = False
        else:
            if name is None and hasattr(fileobj, 'name') and isinstance(fileobj.name, (str, bytes)):
                name = fileobj.name
            if hasattr(fileobj, 'mode'):
                self._mode = fileobj.mode
            self._extfileobj = True
        self.名字 = os.path.abspath(name) if name else None
        self.文件对象 = fileobj
        self.流 = stream
        if format is not None:
            self.format = format
        if tarinfo is not None:
            self.tarinfo = tarinfo
        if dereference is not None:
            self.解引用 = dereference
        if ignore_zeros is not None:
            self.忽略零块 = ignore_zeros
        if encoding is not None:
            self.编码 = encoding
        self.出错怎么办 = errors
        if pax_headers is not None and self.format == PAX格式:
            self.PAX头 = pax_headers
        else:
            self.PAX头 = {}
        if debug is not None:
            self.调试 = debug
        if errorlevel is not None:
            self.错误级别 = errorlevel
        self.复制缓冲区大小 = copybufsize
        self.已关闭 = False
        self.成员表 = []
        self._loaded = False
        self.偏移 = self.文件对象.tell()
        self.索引节点 = {}
        self._unames = {}
        self._gnames = {}
        try:
            if self.模式 == 'r':
                self.首个成员 = None
                self.首个成员 = self.next()
            if self.模式 == 'a':
                while True:
                    self.文件对象.seek(self.偏移)
                    try:
                        tarinfo = self.tarinfo.fromtarfile(self)
                        self.成员表.append(tarinfo)
                    except 文件头提前结束错误:
                        self.文件对象.seek(self.偏移)
                        break
                    except 文件头错误 as e:
                        raise 读错误(str(e)) from None
            if self.模式 in ('a', 'w', 'x'):
                self._loaded = True
                if self.PAX头:
                    buf = self.tarinfo.create_pax_global_header(self.PAX头.copy())
                    self.文件对象.write(buf)
                    self.偏移 += len(buf)
        except:
            if not self._extfileobj:
                self.文件对象.close()
            self.已关闭 = True
            raise

    @classmethod
    def open(cls, name=None, mode='r', fileobj=None, bufsize=记录大小, **kwargs):
        """Open a tar archive for reading, writing or appending. Return
           an appropriate TarFile class.

           mode:
           'r' or 'r:*' open for reading with transparent compression
           'r:'         open for reading exclusively uncompressed
           'r:gz'       open for reading with gzip compression
           'r:bz2'      open for reading with bzip2 compression
           'r:xz'       open for reading with lzma compression
           'r:zst'      open for reading with zstd compression
           'a' or 'a:'  open for appending, creating the file if necessary
           'w' or 'w:'  open for writing without compression
           'w:gz'       open for writing with gzip compression
           'w:bz2'      open for writing with bzip2 compression
           'w:xz'       open for writing with lzma compression
           'w:zst'      open for writing with zstd compression

           'x' or 'x:'  create a tarfile exclusively without compression, raise
                        an exception if the file is already created
           'x:gz'       create a gzip compressed tarfile, raise an exception
                        if the file is already created
           'x:bz2'      create a bzip2 compressed tarfile, raise an exception
                        if the file is already created
           'x:xz'       create an lzma compressed tarfile, raise an exception
                        if the file is already created
           'x:zst'      create a zstd compressed tarfile, raise an exception
                        if the file is already created

           'r|*'        open a stream of tar blocks with transparent compression
           'r|'         open an uncompressed stream of tar blocks for reading
           'r|gz'       open a gzip compressed stream of tar blocks
           'r|bz2'      open a bzip2 compressed stream of tar blocks
           'r|xz'       open an lzma compressed stream of tar blocks
           'r|zst'      open a zstd compressed stream of tar blocks
           'w|'         open an uncompressed stream for writing
           'w|gz'       open a gzip compressed stream for writing
           'w|bz2'      open a bzip2 compressed stream for writing
           'w|xz'       open an lzma compressed stream for writing
           'w|zst'      open a zstd compressed stream for writing
        """
        if not name and (not fileobj):
            raise ValueError('nothing to open')
        if mode in ('r', 'r:*'):

            def not_compressed(comptype):
                return cls.打开方法[comptype] == 'taropen'
            error_msgs = []
            for comptype in sorted(cls.打开方法, key=not_compressed):
                func = getattr(cls, cls.打开方法[comptype])
                if fileobj is not None:
                    saved_pos = fileobj.tell()
                try:
                    return func(name, 'r', fileobj, **kwargs)
                except (读错误, 压缩错误) as e:
                    error_msgs.append(f'- method {comptype}: {e!r}')
                    if fileobj is not None:
                        fileobj.seek(saved_pos)
                    continue
            error_msgs_summary = '\n'.join(error_msgs)
            raise 读错误(f'file could not be opened successfully:\n{error_msgs_summary}')
        elif ':' in mode:
            filemode, comptype = mode.split(':', 1)
            filemode = filemode or 'r'
            comptype = comptype or 'tar'
            if comptype in cls.打开方法:
                func = getattr(cls, cls.打开方法[comptype])
            else:
                raise 压缩错误('unknown compression type %r' % comptype)
            return func(name, filemode, fileobj, **kwargs)
        elif '|' in mode:
            filemode, comptype = mode.split('|', 1)
            filemode = filemode or 'r'
            comptype = comptype or 'tar'
            if filemode not in ('r', 'w'):
                raise ValueError("mode must be 'r' or 'w'")
            if 'compresslevel' in kwargs and comptype not in ('gz', 'bz2'):
                raise ValueError('compresslevel is only valid for w|gz and w|bz2 modes')
            if 'preset' in kwargs and comptype not in ('xz',):
                raise ValueError('preset is only valid for w|xz mode')
            compresslevel = kwargs.pop('compresslevel', 9)
            preset = kwargs.pop('preset', None)
            流 = _Stream(name, filemode, comptype, fileobj, bufsize, compresslevel, preset)
            try:
                t = cls(name, filemode, 流, **kwargs)
            except:
                流.close()
                raise
            t._extfileobj = False
            return t
        elif mode in ('a', 'w', 'x'):
            return cls.打开TAR(name, mode, fileobj, **kwargs)
        raise ValueError('undiscernible mode')

    @classmethod
    def 打开TAR(cls, name, mode='r', fileobj=None, **kwargs):
        """Open uncompressed tar archive name for reading or writing.
        """
        if mode not in ('r', 'a', 'w', 'x'):
            raise ValueError("mode must be 'r', 'a', 'w' or 'x'")
        return cls(name, mode, fileobj, **kwargs)

    @classmethod
    def 打开GZ(cls, name, mode='r', fileobj=None, compresslevel=9, **kwargs):
        """Open gzip compressed tar archive name for reading or writing.
           Appending is not allowed.
        """
        if mode not in ('r', 'w', 'x'):
            raise ValueError("mode must be 'r', 'w' or 'x'")
        try:
            from gzip import GzipFile
        except ImportError:
            raise 压缩错误('gzip module is not available') from None
        try:
            fileobj = GzipFile(name, mode + 'b', compresslevel, fileobj)
        except OSError as e:
            if fileobj is not None and mode == 'r':
                raise 读错误('not a gzip file') from e
            raise
        try:
            t = cls.打开TAR(name, mode, fileobj, **kwargs)
        except OSError as e:
            fileobj.close()
            if mode == 'r':
                raise 读错误('not a gzip file') from e
            raise
        except:
            fileobj.close()
            raise
        t._extfileobj = False
        return t

    @classmethod
    def 打开BZ2(cls, name, mode='r', fileobj=None, compresslevel=9, **kwargs):
        """Open bzip2 compressed tar archive name for reading or writing.
           Appending is not allowed.
        """
        if mode not in ('r', 'w', 'x'):
            raise ValueError("mode must be 'r', 'w' or 'x'")
        try:
            from bz2 import BZ2File
        except ImportError:
            raise 压缩错误('bz2 module is not available') from None
        fileobj = BZ2File(fileobj or name, mode, compresslevel=compresslevel)
        try:
            t = cls.打开TAR(name, mode, fileobj, **kwargs)
        except (OSError, EOFError) as e:
            fileobj.close()
            if mode == 'r':
                raise 读错误('not a bzip2 file') from e
            raise
        except:
            fileobj.close()
            raise
        t._extfileobj = False
        return t

    @classmethod
    def 打开XZ(cls, name, mode='r', fileobj=None, preset=None, **kwargs):
        """Open lzma compressed tar archive name for reading or writing.
           Appending is not allowed.
        """
        if mode not in ('r', 'w', 'x'):
            raise ValueError("mode must be 'r', 'w' or 'x'")
        try:
            from lzma import LZMAFile, LZMAError
        except ImportError:
            raise 压缩错误('lzma module is not available') from None
        fileobj = LZMAFile(fileobj or name, mode, preset=preset)
        try:
            t = cls.打开TAR(name, mode, fileobj, **kwargs)
        except (LZMAError, EOFError) as e:
            fileobj.close()
            if mode == 'r':
                raise 读错误('not an lzma file') from e
            raise
        except:
            fileobj.close()
            raise
        t._extfileobj = False
        return t

    @classmethod
    def 打开ZSTD(cls, name, mode='r', fileobj=None, level=None, options=None, zstd_dict=None, **kwargs):
        """Open zstd compressed tar archive name for reading or writing.
           Appending is not allowed.
        """
        if mode not in ('r', 'w', 'x'):
            raise ValueError("mode must be 'r', 'w' or 'x'")
        try:
            from compression.zstd import ZstdFile, ZstdError
        except ImportError:
            raise 压缩错误('compression.zstd module is not available') from None
        fileobj = ZstdFile(fileobj or name, mode, level=level, options=options, zstd_dict=zstd_dict)
        try:
            t = cls.打开TAR(name, mode, fileobj, **kwargs)
        except (ZstdError, EOFError) as e:
            fileobj.close()
            if mode == 'r':
                raise 读错误('not a zstd file') from e
            raise
        except Exception:
            fileobj.close()
            raise
        t._extfileobj = False
        return t
    打开方法 = {'tar': 'taropen', 'gz': 'gzopen', 'bz2': 'bz2open', 'xz': 'xzopen', 'zst': 'zstopen'}

    def close(self):
        """Close the TarFile. In write-mode, two finishing zero blocks are
           appended to the archive.
        """
        if self.已关闭:
            return
        self.已关闭 = True
        try:
            if self.模式 in ('a', 'w', 'x'):
                self.文件对象.write(空字节 * (块大小 * 2))
                self.偏移 += 块大小 * 2
                blocks, remainder = divmod(self.偏移, 记录大小)
                if remainder > 0:
                    self.文件对象.write(空字节 * (记录大小 - remainder))
        finally:
            if not self._extfileobj:
                self.文件对象.close()

    def 取成员(self, name):
        """Return a TarInfo object for member 'name'. If 'name' can not be
           found in the archive, KeyError is raised. If a member occurs more
           than once in the archive, its last occurrence is assumed to be the
           most up-to-date version.
        """
        tarinfo = self._getmember(name.rstrip('/'))
        if tarinfo is None:
            raise KeyError('filename %r not found' % name)
        return tarinfo

    def 取成员们(self):
        """Return the members of the archive as a list of TarInfo objects. The
           list has the same order as the members in the archive.
        """
        self._check()
        if not self._loaded:
            self._load()
        return self.成员表

    def 取名字表(self):
        """Return the members of the archive as a list of their names. It has
           the same order as the list returned by getmembers().
        """
        return [tarinfo.name for tarinfo in self.取成员们()]

    def 取TAR条目(self, name=None, arcname=None, fileobj=None):
        """Create a TarInfo object from the result of os.stat or equivalent
           on an existing file. The file is either named by 'name', or
           specified as a file object 'fileobj' with a file descriptor. If
           given, 'arcname' specifies an alternative name for the file in the
           archive, otherwise, the name is taken from the 'name' attribute of
           'fileobj', or the 'name' argument. The name should be a text
           string.
        """
        self._check('awx')
        if fileobj is not None:
            name = fileobj.name
        if arcname is None:
            arcname = name
        drv, arcname = os.path.splitdrive(arcname)
        arcname = arcname.replace(os.sep, '/')
        arcname = arcname.lstrip('/')
        tarinfo = self.tarinfo()
        tarinfo._tarfile = self
        if fileobj is None:
            if not self.解引用:
                statres = os.lstat(name)
            else:
                statres = os.stat(name)
        else:
            statres = os.fstat(fileobj.fileno())
        链接名 = ''
        stmd = statres.st_mode
        if stat.S_ISREG(stmd):
            inode = (statres.st_ino, statres.st_dev)
            if not self.解引用 and statres.st_nlink > 1 and (inode in self.索引节点) and (arcname != self.索引节点[inode]):
                type = 硬链接类型
                链接名 = self.索引节点[inode]
            else:
                type = 普通文件类型
                if inode[0]:
                    self.索引节点[inode] = arcname
        elif stat.S_ISDIR(stmd):
            type = 目录类型
        elif stat.S_ISFIFO(stmd):
            type = FIFO类型
        elif stat.S_ISLNK(stmd):
            type = 符号链接类型
            链接名 = os.readlink(name)
        elif stat.S_ISCHR(stmd):
            type = 字符设备类型
        elif stat.S_ISBLK(stmd):
            type = 块设备类型
        else:
            return None
        tarinfo.name = arcname
        tarinfo.mode = stmd
        tarinfo.uid = statres.st_uid
        tarinfo.gid = statres.st_gid
        if type == 普通文件类型:
            tarinfo.size = statres.st_size
        else:
            tarinfo.size = 0
        tarinfo.mtime = statres.st_mtime
        tarinfo.type = type
        tarinfo.linkname = 链接名
        if pwd:
            if tarinfo.uid not in self._unames:
                try:
                    self._unames[tarinfo.uid] = pwd.getpwuid(tarinfo.uid)[0]
                except KeyError:
                    self._unames[tarinfo.uid] = ''
            tarinfo.uname = self._unames[tarinfo.uid]
        if grp:
            if tarinfo.gid not in self._gnames:
                try:
                    self._gnames[tarinfo.gid] = grp.getgrgid(tarinfo.gid)[0]
                except KeyError:
                    self._gnames[tarinfo.gid] = ''
            tarinfo.gname = self._gnames[tarinfo.gid]
        if type in (字符设备类型, 块设备类型):
            if hasattr(os, 'major') and hasattr(os, 'minor'):
                tarinfo.devmajor = os.major(statres.st_rdev)
                tarinfo.devminor = os.minor(statres.st_rdev)
        return tarinfo

    def list(self, verbose=True, *, members=None):
        """Print a table of contents to sys.stdout.

        If 'verbose' is False, only the names of the members are printed.
        If it is True, an 'ls -l'-like output is produced.  'members' is
        optional and must be a subset of the list returned by getmembers().
        """
        type2mode = {普通文件类型: stat.S_IFREG, 符号链接类型: stat.S_IFLNK, FIFO类型: stat.S_IFIFO, 字符设备类型: stat.S_IFCHR, 目录类型: stat.S_IFDIR, 块设备类型: stat.S_IFBLK}
        self._check()
        if members is None:
            members = self
        for tarinfo in members:
            if verbose:
                if tarinfo.mode is None:
                    _safe_print('??????????')
                else:
                    modetype = type2mode.get(tarinfo.type, 0)
                    _safe_print(stat.filemode(modetype | tarinfo.mode))
                _safe_print('%s/%s' % (tarinfo.uname or tarinfo.uid, tarinfo.gname or tarinfo.gid))
                if tarinfo.ischr() or tarinfo.isblk():
                    _safe_print('%10s' % ('%d,%d' % (tarinfo.devmajor, tarinfo.devminor)))
                else:
                    _safe_print('%10d' % tarinfo.size)
                if tarinfo.mtime is None:
                    _safe_print('????-??-?? ??:??:??')
                else:
                    _safe_print('%d-%02d-%02d %02d:%02d:%02d' % time.localtime(tarinfo.mtime)[:6])
            _safe_print(tarinfo.name + ('/' if tarinfo.isdir() else ''))
            if verbose:
                if tarinfo.issym():
                    _safe_print('-> ' + tarinfo.linkname)
                if tarinfo.islnk():
                    _safe_print('link to ' + tarinfo.linkname)
            print()

    def add(self, name, arcname=None, recursive=True, *, filter=None):
        """Add the file 'name' to the archive. 'name' may be any type of file
           (directory, fifo, symbolic link, etc.). If given, 'arcname'
           specifies an alternative name for the file in the archive.
           Directories are added recursively by default. This can be avoided by
           setting 'recursive' to False. 'filter' is a function
           that expects a TarInfo object argument and returns the changed
           TarInfo object, if it returns None the TarInfo object will be
           excluded from the archive.
        """
        self._check('awx')
        if arcname is None:
            arcname = name
        if self.名字 is not None and os.path.abspath(name) == self.名字:
            self._dbg(2, 'tarfile: Skipped %r' % name)
            return
        self._dbg(1, name)
        tarinfo = self.取TAR条目(name, arcname)
        if tarinfo is None:
            self._dbg(1, 'tarfile: Unsupported type %r' % name)
            return
        if filter is not None:
            tarinfo = filter(tarinfo)
            if tarinfo is None:
                self._dbg(2, 'tarfile: Excluded %r' % name)
                return
        if tarinfo.isreg():
            with bltn_open(name, 'rb') as f:
                self.加文件(tarinfo, f)
        elif tarinfo.isdir():
            self.加文件(tarinfo)
            if recursive:
                for f in sorted(os.listdir(name)):
                    self.add(os.path.join(name, f), os.path.join(arcname, f), recursive, filter=filter)
        else:
            self.加文件(tarinfo)

    def 加文件(self, tarinfo, fileobj=None):
        """Add the TarInfo object 'tarinfo' to the archive.

        If 'tarinfo' represents a non zero-size regular file, the 'fileobj'
        argument should be a binary file, and tarinfo.size bytes are read
        from it and added to the archive. You can create TarInfo objects
        directly, or by using gettarinfo().
        """
        self._check('awx')
        if fileobj is None and tarinfo.isreg() and (tarinfo.size != 0):
            raise ValueError('fileobj not provided for non zero-size regular file')
        tarinfo = copy.copy(tarinfo)
        buf = tarinfo.tobuf(self.format, self.编码, self.出错怎么办)
        self.文件对象.write(buf)
        self.偏移 += len(buf)
        bufsize = self.复制缓冲区大小
        if fileobj is not None:
            复制文件对象(fileobj, self.文件对象, tarinfo.size, bufsize=bufsize)
            blocks, remainder = divmod(tarinfo.size, 块大小)
            if remainder > 0:
                self.文件对象.write(空字节 * (块大小 - remainder))
                blocks += 1
            self.偏移 += blocks * 块大小
        self.成员表.append(tarinfo)

    def _get_filter_function(self, filter):
        if filter is None:
            filter = self.extraction_filter
            if filter is None:
                return data_filter
            if isinstance(filter, str):
                raise TypeError('String names are not supported for ' + 'TarFile.extraction_filter. Use a function such as ' + 'tarfile.data_filter directly.')
            return filter
        if callable(filter):
            return filter
        try:
            return _NAMED_FILTERS[filter]
        except KeyError:
            raise ValueError(f'filter {filter!r} not found') from None

    def 全部提取(self, path='.', members=None, *, numeric_owner=False, filter=None):
        """Extract all members from the archive to the current working
           directory and set owner, modification time and permissions on
           directories afterwards. 'path' specifies a different directory
           to extract to. 'members' is optional and must be a subset of the
           list returned by getmembers(). If 'numeric_owner' is True, only
           the numbers for user/group names are used and not the names.

           The 'filter' function will be called on each member just
           before extraction.
           It can return a changed TarInfo or None to skip the member.
           String names of common filters are accepted.
        """
        directories = []
        filter_function = self._get_filter_function(filter)
        if members is None:
            members = self
        for member in members:
            tarinfo, unfiltered = self._get_extract_tarinfo(member, filter_function, path)
            if tarinfo is None:
                continue
            if tarinfo.isdir():
                directories.append(unfiltered)
            self._extract_one(tarinfo, path, set_attrs=not tarinfo.isdir(), numeric_owner=numeric_owner, filter_function=filter_function)
        directories.sort(key=lambda a: a.name, reverse=True)
        for unfiltered in directories:
            try:
                try:
                    tarinfo = filter_function(unfiltered, path)
                except _FILTER_ERRORS as exc:
                    self._log_no_directory_fixup(unfiltered, repr(exc))
                    continue
                if tarinfo is None:
                    self._log_no_directory_fixup(unfiltered, 'excluded by filter')
                    continue
                dirpath = os.path.join(path, tarinfo.name)
                try:
                    lstat = os.lstat(dirpath)
                except FileNotFoundError:
                    self._log_no_directory_fixup(tarinfo, 'missing')
                    continue
                if not stat.S_ISDIR(lstat.st_mode):
                    self._log_no_directory_fixup(tarinfo, 'not a directory')
                    continue
                self.改属主(tarinfo, dirpath, numeric_owner=numeric_owner)
                self.改时间(tarinfo, dirpath)
                self.改权限(tarinfo, dirpath)
            except 提取错误 as e:
                self._handle_nonfatal_error(e)

    def _log_no_directory_fixup(self, member, reason):
        self._dbg(2, 'tarfile: Not fixing up directory %r (%s)' % (member.name, reason))

    def 提取(self, member, path='', set_attrs=True, *, numeric_owner=False, filter=None):
        """Extract a member from the archive to the current working directory,
           using its full name. Its file information is extracted as accurately
           as possible. 'member' may be a filename or a TarInfo object. You can
           specify a different directory using 'path'. File attributes (owner,
           mtime, mode) are set unless 'set_attrs' is False. If 'numeric_owner'
           is True, only the numbers for user/group names are used and not
           the names.

           The 'filter' function will be called before extraction.
           It can return a changed TarInfo or None to skip the member.
           String names of common filters are accepted.
        """
        filter_function = self._get_filter_function(filter)
        tarinfo, unfiltered = self._get_extract_tarinfo(member, filter_function, path)
        if tarinfo is not None:
            self._extract_one(tarinfo, path, set_attrs, numeric_owner, filter_function=filter_function)

    def _get_extract_tarinfo(self, member, filter_function, path):
        """Get (filtered, unfiltered) TarInfos from *member*

        *member* might be a string.

        Return (None, None) if not found.
        """
        if isinstance(member, str):
            unfiltered = self.取成员(member)
        else:
            unfiltered = member
        filtered = None
        try:
            filtered = filter_function(unfiltered, path)
        except (OSError, UnicodeEncodeError, 过滤器错误) as e:
            self._handle_fatal_error(e)
        except 提取错误 as e:
            self._handle_nonfatal_error(e)
        if filtered is None:
            self._dbg(2, 'tarfile: Excluded %r' % unfiltered.name)
            return (None, None)
        if filtered.islnk():
            filtered = copy.copy(filtered)
            filtered._link_target = os.path.join(path, filtered.linkname)
        return (filtered, unfiltered)

    def _extract_one(self, tarinfo, path, set_attrs, numeric_owner, filter_function=None):
        """Extract from filtered tarinfo to disk.

           filter_function is only used when extracting a *different*
           member (e.g. as fallback to creating a symlink)
        """
        self._check('r')
        try:
            self._extract_member(tarinfo, os.path.join(path, tarinfo.name), set_attrs=set_attrs, numeric_owner=numeric_owner, filter_function=filter_function, extraction_root=path)
        except (OSError, UnicodeEncodeError) as e:
            self._handle_fatal_error(e)
        except 提取错误 as e:
            self._handle_nonfatal_error(e)

    def _handle_nonfatal_error(self, e):
        """Handle non-fatal error (ExtractError) according to errorlevel"""
        if self.错误级别 > 1:
            raise
        else:
            self._dbg(1, 'tarfile: %s' % e)

    def _handle_fatal_error(self, e):
        """Handle "fatal" error according to self.errorlevel"""
        if self.错误级别 > 0:
            raise
        elif isinstance(e, OSError):
            if e.filename is None:
                self._dbg(1, 'tarfile: %s' % e.strerror)
            else:
                self._dbg(1, 'tarfile: %s %r' % (e.strerror, e.filename))
        else:
            self._dbg(1, 'tarfile: %s %s' % (type(e).__name__, e))

    def 提取文件(self, member):
        """Extract a member from the archive as a file object. 'member' may be
           a filename or a TarInfo object. If 'member' is a regular file or
           a link, an io.BufferedReader object is returned. For all other
           existing members, None is returned. If 'member' does not appear
           in the archive, KeyError is raised.
        """
        self._check('r')
        if isinstance(member, str):
            tarinfo = self.取成员(member)
        else:
            tarinfo = member
        if tarinfo.isreg() or tarinfo.type not in 支持的类型:
            return self.fileobject(self, tarinfo)
        elif tarinfo.islnk() or tarinfo.issym():
            if isinstance(self.文件对象, _Stream):
                raise 流错误('cannot extract (sym)link as file object')
            else:
                return self.提取文件(self._find_link_target(tarinfo))
        else:
            return None

    def _extract_member(self, tarinfo, targetpath, set_attrs=True, numeric_owner=False, *, filter_function=None, extraction_root=None):
        """Extract the filtered TarInfo object tarinfo to a physical
           file called targetpath.

           filter_function is only used when extracting a *different*
           member (e.g. as fallback to creating a symlink)
        """
        targetpath = targetpath.rstrip('/')
        targetpath = targetpath.replace('/', os.sep)
        upperdirs = os.path.dirname(targetpath)
        if upperdirs and (not os.path.exists(upperdirs)):
            os.makedirs(upperdirs, exist_ok=True)
        if tarinfo.islnk() or tarinfo.issym():
            self._dbg(1, '%s -> %s' % (tarinfo.name, tarinfo.linkname))
        else:
            self._dbg(1, tarinfo.name)
        if tarinfo.isreg():
            self.建文件(tarinfo, targetpath)
        elif tarinfo.isdir():
            self.建目录(tarinfo, targetpath)
        elif tarinfo.isfifo():
            self.建FIFO(tarinfo, targetpath)
        elif tarinfo.ischr() or tarinfo.isblk():
            self.建设备(tarinfo, targetpath)
        elif tarinfo.islnk() or tarinfo.issym():
            self.带过滤器建链接(tarinfo, targetpath, filter_function=filter_function, extraction_root=extraction_root)
        elif tarinfo.type not in 支持的类型:
            self.建未知项(tarinfo, targetpath)
        else:
            self.建文件(tarinfo, targetpath)
        if set_attrs:
            self.改属主(tarinfo, targetpath, numeric_owner)
            if not tarinfo.issym():
                self.改权限(tarinfo, targetpath)
                self.改时间(tarinfo, targetpath)

    def 建目录(self, tarinfo, targetpath):
        """Make a directory called targetpath.
        """
        try:
            if tarinfo.mode is None:
                os.mkdir(targetpath)
            else:
                os.mkdir(targetpath, 448)
        except FileExistsError:
            if not os.path.isdir(targetpath):
                raise

    def 建文件(self, tarinfo, targetpath):
        """Make a file called targetpath.
        """
        source = self.文件对象
        source.seek(tarinfo.offset_data)
        bufsize = self.复制缓冲区大小
        with bltn_open(targetpath, 'wb') as target:
            if tarinfo.sparse is not None:
                for 偏移, 大小 in tarinfo.sparse:
                    target.seek(偏移)
                    复制文件对象(source, target, 大小, 读错误, bufsize)
                target.seek(tarinfo.size)
                target.truncate()
            else:
                复制文件对象(source, target, tarinfo.size, 读错误, bufsize)

    def 建未知项(self, tarinfo, targetpath):
        """Make a file from a TarInfo object with an unknown type
           at targetpath.
        """
        self.建文件(tarinfo, targetpath)
        self._dbg(1, 'tarfile: Unknown file type %r, extracted as regular file.' % tarinfo.type)

    def 建FIFO(self, tarinfo, targetpath):
        """Make a fifo called targetpath.
        """
        if hasattr(os, 'mkfifo'):
            os.mkfifo(targetpath)
        else:
            raise 提取错误('fifo not supported by system')

    def 建设备(self, tarinfo, targetpath):
        """Make a character or block device called targetpath.
        """
        if not hasattr(os, 'mknod') or not hasattr(os, 'makedev'):
            raise 提取错误('special devices not supported by system')
        模式 = tarinfo.mode
        if 模式 is None:
            模式 = 384
        if tarinfo.isblk():
            模式 |= stat.S_IFBLK
        else:
            模式 |= stat.S_IFCHR
        os.mknod(targetpath, 模式, os.makedev(tarinfo.devmajor, tarinfo.devminor))

    def 建链接(self, tarinfo, targetpath):
        return self.带过滤器建链接(tarinfo, targetpath, None, None)

    def 带过滤器建链接(self, tarinfo, targetpath, filter_function, extraction_root):
        """Make a (symbolic) link called targetpath. If it cannot be created
          (platform limitation), we try to make a copy of the referenced file
          instead of a link.

          filter_function is only used when extracting a *different*
          member (e.g. as fallback to creating a link).
        """
        keyerror_to_extracterror = False
        try:
            if tarinfo.issym():
                if os.path.lexists(targetpath):
                    os.unlink(targetpath)
                os.symlink(tarinfo.linkname, targetpath)
                return
            elif os.path.exists(tarinfo._link_target):
                if os.path.lexists(targetpath):
                    os.unlink(targetpath)
                os.link(tarinfo._link_target, targetpath)
                return
        except 符号链接异常:
            keyerror_to_extracterror = True
        try:
            unfiltered = self._find_link_target(tarinfo)
        except KeyError:
            if keyerror_to_extracterror:
                raise 提取错误('unable to resolve link inside archive') from None
            else:
                raise
        if filter_function is None:
            filtered = unfiltered
        else:
            if extraction_root is None:
                raise 提取错误('makelink_with_filter: if filter_function is not None, ' + 'extraction_root must also not be None')
            try:
                filter_function(unfiltered.replace(name=tarinfo.name, deep=False), extraction_root)
                filtered = filter_function(unfiltered, extraction_root)
            except _FILTER_ERRORS as cause:
                raise 链接回退错误(tarinfo, unfiltered.name) from cause
        if filtered is not None:
            self._extract_member(filtered, targetpath, filter_function=filter_function, extraction_root=extraction_root)

    def 改属主(self, tarinfo, targetpath, numeric_owner):
        """Set owner of targetpath according to tarinfo. If numeric_owner
           is True, use .gid/.uid instead of .gname/.uname. If numeric_owner
           is False, fall back to .gid/.uid when the search based on name
           fails.
        """
        if hasattr(os, 'geteuid') and os.geteuid() == 0:
            g = tarinfo.gid
            u = tarinfo.uid
            if not numeric_owner:
                try:
                    if grp and tarinfo.gname:
                        g = grp.getgrnam(tarinfo.gname)[2]
                except KeyError:
                    pass
                try:
                    if pwd and tarinfo.uname:
                        u = pwd.getpwnam(tarinfo.uname)[2]
                except KeyError:
                    pass
            if g is None:
                g = -1
            if u is None:
                u = -1
            try:
                if tarinfo.issym() and hasattr(os, 'lchown'):
                    os.lchown(targetpath, u, g)
                else:
                    os.chown(targetpath, u, g)
            except (OSError, OverflowError) as e:
                raise 提取错误('could not change owner') from e

    def 改权限(self, tarinfo, targetpath):
        """Set file permissions of targetpath according to tarinfo.
        """
        if tarinfo.mode is None:
            return
        try:
            os.chmod(targetpath, tarinfo.mode)
        except OSError as e:
            raise 提取错误('could not change mode') from e

    def 改时间(self, tarinfo, targetpath):
        """Set modification time of targetpath according to tarinfo.
        """
        修改时间 = tarinfo.mtime
        if 修改时间 is None:
            return
        if not hasattr(os, 'utime'):
            return
        try:
            os.utime(targetpath, (修改时间, 修改时间))
        except OSError as e:
            raise 提取错误('could not change modification time') from e

    def next(self):
        """Return the next member of the archive as a TarInfo object, when
           TarFile is opened for reading. Return None if there is no more
           available.
        """
        self._check('ra')
        if self.首个成员 is not None:
            m = self.首个成员
            self.首个成员 = None
            return m
        if self.偏移 != self.文件对象.tell():
            if self.偏移 == 0:
                return None
            self.文件对象.seek(self.偏移 - 1)
            if not self.文件对象.read(1):
                raise 读错误('unexpected end of data')
        tarinfo = None
        while True:
            try:
                tarinfo = self.tarinfo.fromtarfile(self)
            except 文件头提前结束错误 as e:
                if self.忽略零块:
                    self._dbg(2, '0x%X: %s' % (self.偏移, e))
                    self.偏移 += 块大小
                    continue
            except 文件头无效错误 as e:
                if self.忽略零块:
                    self._dbg(2, '0x%X: %s' % (self.偏移, e))
                    self.偏移 += 块大小
                    continue
                elif self.偏移 == 0:
                    raise 读错误(str(e)) from None
            except 空文件头错误:
                if self.偏移 == 0:
                    raise 读错误('empty file') from None
            except 截断文件头错误 as e:
                if self.偏移 == 0:
                    raise 读错误(str(e)) from None
            except 多余文件头错误 as e:
                raise 读错误(str(e)) from None
            except Exception as e:
                try:
                    import zlib
                    if isinstance(e, zlib.error):
                        raise 读错误(f'zlib error: {e}') from None
                    else:
                        raise e
                except ImportError:
                    raise e
            break
        if tarinfo is not None:
            if not self.流:
                self.成员表.append(tarinfo)
        else:
            self._loaded = True
        return tarinfo

    def _getmember(self, name, tarinfo=None, normalize=False):
        """Find an archive member by name from bottom to top.
           If tarinfo is given, it is used as the starting point.
        """
        成员表 = self.取成员们()
        skipping = False
        if tarinfo is not None:
            try:
                index = 成员表.index(tarinfo)
            except ValueError:
                skipping = True
            else:
                成员表 = 成员表[:index]
        if normalize:
            name = os.path.normpath(name)
        for member in reversed(成员表):
            if skipping:
                if tarinfo.offset == member.offset:
                    skipping = False
                continue
            if normalize:
                member_name = os.path.normpath(member.name)
            else:
                member_name = member.name
            if name == member_name:
                return member
        if skipping:
            raise ValueError(tarinfo)

    def _load(self):
        """Read through the entire archive file and look for readable
           members. This should not run if the file is set to stream.
        """
        if not self.流:
            while self.next() is not None:
                pass
            self._loaded = True

    def _check(self, mode=None):
        """Check if TarFile is still open, and if the operation's mode
           corresponds to TarFile's mode.
        """
        if self.已关闭:
            raise OSError('%s is closed' % self.__class__.__name__)
        if mode is not None and self.模式 not in mode:
            raise OSError('bad operation for mode %r' % self.模式)

    def _find_link_target(self, tarinfo):
        """Find the target member of a symlink or hardlink member in the
           archive.
        """
        if tarinfo.issym():
            链接名 = '/'.join(filter(None, (os.path.dirname(tarinfo.name), tarinfo.linkname)))
            limit = None
        else:
            链接名 = tarinfo.linkname
            limit = tarinfo
        member = self._getmember(链接名, tarinfo=limit, normalize=True)
        if member is None:
            raise KeyError('linkname %r not found' % 链接名)
        return member

    def __iter__(self):
        """Provide an iterator object.
        """
        if self._loaded:
            yield from self.成员表
            return
        index = 0
        if self.首个成员 is not None:
            tarinfo = self.next()
            index += 1
            yield tarinfo
        while True:
            if index < len(self.成员表):
                tarinfo = self.成员表[index]
            elif not self._loaded:
                tarinfo = self.next()
                if not tarinfo:
                    self._loaded = True
                    return
            else:
                return
            index += 1
            yield tarinfo

    def _dbg(self, level, msg):
        """Write debugging output to sys.stderr.
        """
        if level <= self.调试:
            print(msg, file=sys.stderr)

    def __enter__(self):
        self._check()
        return self

    def __exit__(self, type, value, traceback):
        if type is None:
            self.close()
        else:
            if not self._extfileobj:
                self.文件对象.close()
            self.已关闭 = True
_装类转发(TAR文件, {'OPEN_METH': '打开方法', 'addfile': '加文件', 'bz2open': '打开BZ2', 'chmod': '改权限', 'chown': '改属主', 'debug': '调试', 'dereference': '解引用', 'encoding': '编码', 'errorlevel': '错误级别', 'errors': '出错怎么办', 'extract': '提取', 'extractall': '全部提取', 'extractfile': '提取文件', 'getmember': '取成员', 'getmembers': '取成员们', 'getnames': '取名字表', 'gettarinfo': '取TAR条目', 'gzopen': '打开GZ', 'ignore_zeros': '忽略零块', 'makedev': '建设备', 'makedir': '建目录', 'makefifo': '建FIFO', 'makefile': '建文件', 'makelink': '建链接', 'makelink_with_filter': '带过滤器建链接', 'makeunknown': '建未知项', 'taropen': '打开TAR', 'utime': '改时间', 'xzopen': '打开XZ', 'zstopen': '打开ZSTD'}, {'OPEN_METH': '打开方法', 'addfile': '加文件', 'bz2open': '打开BZ2', 'chmod': '改权限', 'chown': '改属主', 'closed': '已关闭', 'copybufsize': '复制缓冲区大小', 'debug': '调试', 'dereference': '解引用', 'encoding': '编码', 'errorlevel': '错误级别', 'errors': '出错怎么办', 'extract': '提取', 'extractall': '全部提取', 'extractfile': '提取文件', 'fileobj': '文件对象', 'firstmember': '首个成员', 'getmember': '取成员', 'getmembers': '取成员们', 'getnames': '取名字表', 'gettarinfo': '取TAR条目', 'gzopen': '打开GZ', 'ignore_zeros': '忽略零块', 'inodes': '索引节点', 'makedev': '建设备', 'makedir': '建目录', 'makefifo': '建FIFO', 'makefile': '建文件', 'makelink': '建链接', 'makelink_with_filter': '带过滤器建链接', 'makeunknown': '建未知项', 'members': '成员表', 'mode': '模式', 'name': '名字', 'offset': '偏移', 'pax_headers': 'PAX头', 'stream': '流', 'taropen': '打开TAR', 'utime': '改时间', 'xzopen': '打开XZ', 'zstopen': '打开ZSTD'})

def 是TAR文件吗(name):
    """Return True if name points to a tar archive that we
       are able to handle, else return False.

       'name' should be a string, file, or file-like object.
    """
    try:
        if hasattr(name, 'read'):
            pos = name.tell()
            t = open(fileobj=name)
            name.seek(pos)
        else:
            t = open(name)
        t.close()
        return True
    except TAR错误:
        return False
open = TAR文件.open

def 主函数():
    import argparse
    description = 'A simple command-line interface for tarfile module.'
    parser = argparse.ArgumentParser(description=description, color=True)
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output')
    parser.add_argument('--filter', metavar='<filtername>', choices=_NAMED_FILTERS, help='Filter for extraction')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--list', metavar='<tarfile>', help='Show listing of a tarfile')
    group.add_argument('-e', '--extract', nargs='+', metavar=('<tarfile>', '<output_dir>'), help='Extract tarfile into target dir')
    group.add_argument('-c', '--create', nargs='+', metavar=('<name>', '<file>'), help='Create tarfile from sources')
    group.add_argument('-t', '--test', metavar='<tarfile>', help='Test if a tarfile is valid')
    args = parser.parse_args()
    if args.filter and args.extract is None:
        parser.exit(1, '--filter is only valid for extraction\n')
    if args.test is not None:
        src = args.test
        if 是TAR文件吗(src):
            with open(src, 'r') as tar:
                tar.getmembers()
                print(tar.getmembers(), file=sys.stderr)
            if args.verbose:
                print('{!r} is a tar archive.'.format(src))
        else:
            parser.exit(1, '{!r} is not a tar archive.\n'.format(src))
    elif args.list is not None:
        src = args.list
        if 是TAR文件吗(src):
            with TAR文件.open(src, 'r:*') as tf:
                tf.list(verbose=args.verbose)
        else:
            parser.exit(1, '{!r} is not a tar archive.\n'.format(src))
    elif args.extract is not None:
        if len(args.extract) == 1:
            src = args.extract[0]
            curdir = os.curdir
        elif len(args.extract) == 2:
            src, curdir = args.extract
        else:
            parser.exit(1, parser.format_help())
        if 是TAR文件吗(src):
            with TAR文件.open(src, 'r:*') as tf:
                tf.extractall(path=curdir, filter=args.filter)
            if args.verbose:
                if curdir == '.':
                    msg = '{!r} file is extracted.'.format(src)
                else:
                    msg = '{!r} file is extracted into {!r} directory.'.format(src, curdir)
                print(msg)
        else:
            parser.exit(1, '{!r} is not a tar archive.\n'.format(src))
    elif args.create is not None:
        tar_name = args.create.pop(0)
        _, ext = os.path.splitext(tar_name)
        compressions = {'.gz': 'gz', '.tgz': 'gz', '.xz': 'xz', '.txz': 'xz', '.bz2': 'bz2', '.tbz': 'bz2', '.tbz2': 'bz2', '.tb2': 'bz2', '.zst': 'zst', '.tzst': 'zst'}
        tar_mode = 'w:' + compressions[ext] if ext in compressions else 'w'
        tar_files = args.create
        with TAR文件.open(tar_name, tar_mode) as tf:
            for file_name in tar_files:
                tf.add(file_name)
        if args.verbose:
            print('{!r} file created.'.format(tar_name))
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

# 本模块别名：词表里有、但规则不让改定义的名字（内置名最典型，比如 `open`）
_本模块别名 = {
    '打开': 'open',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'AREGTYPE': '备选普通文件类型',
    'AbsoluteLinkError': '绝对链接错误',
    'AbsolutePathError': '绝对路径错误',
    'BLKTYPE': '块设备类型',
    'BLOCKSIZE': '块大小',
    'CHRTYPE': '字符设备类型',
    'CONTTYPE': '连续文件类型',
    'CompressionError': '压缩错误',
    'DEFAULT_FORMAT': '默认格式',
    'DIRTYPE': '目录类型',
    'ENCODING': '编码方式',
    'EOFHeaderError': '文件头提前结束错误',
    'EmptyHeaderError': '空文件头错误',
    'ExFileObject': '提取文件对象',
    'ExtractError': '提取错误',
    'FIFOTYPE': 'FIFO类型',
    'FilterError': '过滤器错误',
    'GNUTYPE_LONGLINK': 'GNU长链接类型',
    'GNUTYPE_LONGNAME': 'GNU长名字类型',
    'GNUTYPE_SPARSE': 'GNU稀疏类型',
    'GNU_FORMAT': 'GNU格式',
    'GNU_MAGIC': 'GNU魔数',
    'GNU_TYPES': 'GNU类型',
    'HeaderError': '文件头错误',
    'InvalidHeaderError': '文件头无效错误',
    'LENGTH_LINK': '链接名长度',
    'LENGTH_NAME': '名字长度',
    'LENGTH_PREFIX': '前缀长度',
    'LNKTYPE': '硬链接类型',
    'LinkFallbackError': '链接回退错误',
    'LinkOutsideDestinationError': '链接越出目标错误',
    'NUL': '空字节',
    'OutsideDestinationError': '越出目标目录错误',
    'PAX_FIELDS': 'PAX字段',
    'PAX_FORMAT': 'PAX格式',
    'PAX_NAME_FIELDS': 'PAX名字字段',
    'PAX_NUMBER_FIELDS': 'PAX数字字段',
    'POSIX_MAGIC': 'POSIX魔数',
    'RECORDSIZE': '记录大小',
    'REGTYPE': '普通文件类型',
    'REGULAR_TYPES': '普通类型',
    'ReadError': '读错误',
    'SOLARIS_XHDTYPE': 'SOLARIS扩展头类型',
    'SUPPORTED_TYPES': '支持的类型',
    'SYMTYPE': '符号链接类型',
    'SpecialFileError': '特殊文件错误',
    'StreamError': '流错误',
    'SubsequentHeaderError': '多余文件头错误',
    'TarError': 'TAR错误',
    'TarFile': 'TAR文件',
    'TarInfo': 'TAR条目',
    'TruncatedHeaderError': '截断文件头错误',
    'USTAR_FORMAT': 'USTAR格式',
    'XGLTYPE': '全局扩展头类型',
    'XHDTYPE': '扩展头类型',
    'calc_chksums': '算校验和',
    'copyfileobj': '复制文件对象',
    'is_tarfile': '是TAR文件吗',
    'main': '主函数',
    'symlink_exception': '符号链接异常',
    'version': '版本',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'TAR文件': {
        'OPEN_METH': '打开方法',
        'addfile': '加文件',
        'bz2open': '打开BZ2',
        'chmod': '改权限',
        'chown': '改属主',
        'debug': '调试',
        'dereference': '解引用',
        'encoding': '编码',
        'errorlevel': '错误级别',
        'errors': '出错怎么办',
        'extract': '提取',
        'extractall': '全部提取',
        'extractfile': '提取文件',
        'getmember': '取成员',
        'getmembers': '取成员们',
        'getnames': '取名字表',
        'gettarinfo': '取TAR条目',
        'gzopen': '打开GZ',
        'ignore_zeros': '忽略零块',
        'makedev': '建设备',
        'makedir': '建目录',
        'makefifo': '建FIFO',
        'makefile': '建文件',
        'makelink': '建链接',
        'makelink_with_filter': '带过滤器建链接',
        'makeunknown': '建未知项',
        'taropen': '打开TAR',
        'utime': '改时间',
        'xzopen': '打开XZ',
        'zstopen': '打开ZSTD',
    },
    'TAR条目': {
        'create_gnu_header': '造GNU头',
        'create_pax_global_header': '造PAX全局头',
        'create_pax_header': '造PAX头',
        'create_ustar_header': '造USTAR头',
        'frombuf': '从块解析',
        'fromtarfile': '从压缩包解析',
        'get_info': '取信息',
        'isblk': '是块设备吗',
        'ischr': '是字符设备吗',
        'isdev': '是设备吗',
        'isdir': '是目录吗',
        'isfifo': '是FIFO吗',
        'isfile': '是文件吗',
        'islnk': '是硬链接吗',
        'isreg': '是普通文件吗',
        'issparse': '是稀疏文件吗',
        'issym': '是符号链接吗',
        'linkpath': '链接路径',
        'path': '路径',
        'tobuf': '转字节块',
    },
    '_FileInFile': {
        'mode': '模式',
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
    'TAR文件': {
        'OPEN_METH': '打开方法',
        'addfile': '加文件',
        'bz2open': '打开BZ2',
        'chmod': '改权限',
        'chown': '改属主',
        'closed': '已关闭',
        'copybufsize': '复制缓冲区大小',
        'debug': '调试',
        'dereference': '解引用',
        'encoding': '编码',
        'errorlevel': '错误级别',
        'errors': '出错怎么办',
        'extract': '提取',
        'extractall': '全部提取',
        'extractfile': '提取文件',
        'fileobj': '文件对象',
        'firstmember': '首个成员',
        'getmember': '取成员',
        'getmembers': '取成员们',
        'getnames': '取名字表',
        'gettarinfo': '取TAR条目',
        'gzopen': '打开GZ',
        'ignore_zeros': '忽略零块',
        'inodes': '索引节点',
        'makedev': '建设备',
        'makedir': '建目录',
        'makefifo': '建FIFO',
        'makefile': '建文件',
        'makelink': '建链接',
        'makelink_with_filter': '带过滤器建链接',
        'makeunknown': '建未知项',
        'members': '成员表',
        'mode': '模式',
        'name': '名字',
        'offset': '偏移',
        'pax_headers': 'PAX头',
        'stream': '流',
        'taropen': '打开TAR',
        'utime': '改时间',
        'xzopen': '打开XZ',
        'zstopen': '打开ZSTD',
    },
    'TAR条目': {
        'chksum': '校验和',
        'create_gnu_header': '造GNU头',
        'create_pax_global_header': '造PAX全局头',
        'create_pax_header': '造PAX头',
        'create_ustar_header': '造USTAR头',
        'devmajor': '主设备号',
        'devminor': '次设备号',
        'frombuf': '从块解析',
        'fromtarfile': '从压缩包解析',
        'get_info': '取信息',
        'gid': '组ID',
        'gname': '组名',
        'isblk': '是块设备吗',
        'ischr': '是字符设备吗',
        'isdev': '是设备吗',
        'isdir': '是目录吗',
        'isfifo': '是FIFO吗',
        'isfile': '是文件吗',
        'islnk': '是硬链接吗',
        'isreg': '是普通文件吗',
        'issparse': '是稀疏文件吗',
        'issym': '是符号链接吗',
        'linkname': '链接名',
        'linkpath': '链接路径',
        'mode': '模式',
        'mtime': '修改时间',
        'name': '名字',
        'offset': '偏移',
        'offset_data': '数据偏移',
        'path': '路径',
        'pax_headers': 'PAX头',
        'size': '大小',
        'sparse': '稀疏信息',
        'tobuf': '转字节块',
        'uid': '用户ID',
        'uname': '用户名',
    },
    '_FileInFile': {
        'closed': '已关闭',
        'fileobj': '文件对象',
        'mode': '模式',
        'name': '名字',
        'offset': '偏移',
        'size': '大小',
    },
    '_Stream': {
        'closed': '已关闭',
        'fileobj': '文件对象',
        'mode': '模式',
        'name': '名字',
    },
    '_StreamProxy': {
        'fileobj': '文件对象',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'GNU格式',
    'PAX格式',
    'TAR文件',
    'TAR条目',
    'TAR错误',
    'USTAR格式',
    '压缩错误',
    '打开',
    '提取错误',
    '文件头错误',
    '是TAR文件吗',
    '流错误',
    '特殊文件错误',
    '绝对路径错误',
    '绝对链接错误',
    '编码方式',
    '读错误',
    '越出目标目录错误',
    '过滤器错误',
    '链接回退错误',
    '链接越出目标错误',
    '默认格式',
]

# ---- 转发层结束 ----
