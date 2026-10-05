# -*- coding: utf-8 -*-
"""压缩工具 —— 汉语库（由 tools/汉化库.py 从 Lib/gzip.py 机械生成，**不要手改**）。

英文库 Lib/gzip.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 压缩工具
"""


"""Functions that read and write gzipped files.

The user of the file doesn't have to worry about the compression,
but random access is not allowed."""
_英文原名表 = {'BadGzipFile': '坏GZIP文件', 'GzipFile': 'GZIP文件', 'READ_BUFFER_SIZE': '读缓冲大小', 'compress': '压缩', 'decompress': '解压', 'main': '主函数'}

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
import builtins
import io
import os
import struct
import sys
import time
import weakref
import zlib
from compression._common import _streams
__all__ = ['BadGzipFile', 'GzipFile', 'open', 'compress', 'decompress']
FTEXT, FHCRC, FEXTRA, FNAME, FCOMMENT = (1, 2, 4, 8, 16)
READ = 'rb'
WRITE = 'wb'
_COMPRESS_LEVEL_FAST = 1
_COMPRESS_LEVEL_TRADEOFF = 6
_COMPRESS_LEVEL_BEST = 9
读缓冲大小 = 128 * 1024
_WRITE_BUFFER_SIZE = 4 * io.DEFAULT_BUFFER_SIZE

def open(filename, mode='rb', compresslevel=_COMPRESS_LEVEL_BEST, encoding=None, errors=None, newline=None):
    """Open a gzip-compressed file in binary or text mode.

    The filename argument can be an actual filename (a str or bytes object),
    or an existing file object to read from or write to.

    The mode argument can be "r", "rb", "w", "wb", "x", "xb", "a" or "ab"
    for binary mode, or "rt", "wt", "xt" or "at" for text mode.  The default
    mode is "rb", and the default compresslevel is 9.

    For binary mode, this function is equivalent to the GzipFile
    constructor: GzipFile(filename, mode, compresslevel).  In this case,
    the encoding, errors and newline arguments must not be provided.

    For text mode, a GzipFile object is created, and wrapped in an
    io.TextIOWrapper instance with the specified encoding, error handling
    behavior, and line ending(s).

    """
    if 't' in mode:
        if 'b' in mode:
            raise ValueError('Invalid mode: %r' % (mode,))
    else:
        if encoding is not None:
            raise ValueError("Argument 'encoding' not supported in binary mode")
        if errors is not None:
            raise ValueError("Argument 'errors' not supported in binary mode")
        if newline is not None:
            raise ValueError("Argument 'newline' not supported in binary mode")
    gz_mode = mode.replace('t', '')
    if isinstance(filename, (str, bytes, os.PathLike)):
        binary_file = GZIP文件(filename, gz_mode, compresslevel)
    elif hasattr(filename, 'read') or hasattr(filename, 'write'):
        binary_file = GZIP文件(None, gz_mode, compresslevel, filename)
    else:
        raise TypeError('filename must be a str or bytes object, or a file')
    if 't' in mode:
        encoding = io.text_encoding(encoding)
        return io.TextIOWrapper(binary_file, encoding, errors, newline)
    else:
        return binary_file

def write32u(output, value):
    output.write(struct.pack('<L', value))

class _PaddedFile:
    """Minimal read-only file object that prepends a string to the contents
    of an actual file. Shouldn't be used outside of gzip.py, as it lacks
    essential functionality."""

    def __init__(self, f, prepend=b''):
        self._buffer = prepend
        self._length = len(prepend)
        self.file = f
        self._read = 0

    def read(self, size):
        if self._read is None:
            return self.file.read(size)
        if self._read + size <= self._length:
            read = self._read
            self._read += size
            return self._buffer[read:self._read]
        else:
            read = self._read
            self._read = None
            return self._buffer[read:] + self.file.read(size - self._length + read)

    def prepend(self, prepend=b''):
        if self._read is None:
            self._buffer = prepend
        else:
            self._read -= len(prepend)
            return
        self._length = len(self._buffer)
        self._read = 0

    def seek(self, off):
        self._read = None
        self._buffer = None
        return self.file.seek(off)

    def seekable(self):
        return True

class 坏GZIP文件(OSError):
    """Exception raised in some cases for invalid gzip files."""
import gzip as _英文身份源
坏GZIP文件 = _英文身份源.BadGzipFile

class _WriteBufferStream(io.RawIOBase):
    """Minimal object to pass WriteBuffer flushes into GzipFile"""

    def __init__(self, gzip_file):
        self.gzip_file = weakref.ref(gzip_file)

    def write(self, data):
        gzip_file = self.gzip_file()
        if gzip_file is None:
            raise RuntimeError('lost gzip_file')
        return gzip_file._write_raw(data)

    def seekable(self):
        return False

    def writable(self):
        return True

class GZIP文件(_streams.BaseStream):
    """The GzipFile class simulates most of the methods of a file object with
    the exception of the truncate() method.

    This class only supports opening files in binary mode.  If you need to
    open a compressed file in text mode, use the gzip.open() function.

    """
    myfileobj = None

    def __init__(self, filename=None, mode=None, compresslevel=_COMPRESS_LEVEL_BEST, fileobj=None, mtime=None):
        """Constructor for the GzipFile class.

        At least one of fileobj and filename must be given a
        non-trivial value.

        The new class instance is based on fileobj, which can be a regular
        file, an io.BytesIO object, or any other object which simulates
        a file.  It defaults to None, in which case filename is opened to
        provide a file object.

        When fileobj is not None, the filename argument is only used to be
        included in the gzip file header, which may include the original
        filename of the uncompressed file.  It defaults to the filename of
        fileobj, if discernible; otherwise, it defaults to the empty string,
        and in this case the original filename is not included in the
        header.

        The mode argument can be any of 'r', 'rb', 'a', 'ab', 'w', 'wb',
        'x', or 'xb' depending on whether the file will be read or written.
        The default is the mode of fileobj if discernible; otherwise, the
        default is 'rb'.  A mode of 'r' is equivalent to one of 'rb', and
        similarly for 'w' and 'wb', 'a' and 'ab', and 'x' and 'xb'.

        The compresslevel argument is an integer from 0 to 9 controlling
        the level of compression; 1 is fastest and produces the least
        compression, and 9 is slowest and produces the most compression.
        0 is no compression at all. The default is 9.

        The optional mtime argument is the timestamp requested by gzip.
        The time is in Unix format, i.e., seconds since 00:00:00 UTC,
        January 1, 1970.  If mtime is omitted or None, the current time
        is used.  Use mtime = 0 to generate a compressed stream that does
        not depend on creation time.

        """
        self.mode = None
        self.fileobj = None
        self._buffer = None
        if mode and ('t' in mode or 'U' in mode):
            raise ValueError('Invalid mode: {!r}'.format(mode))
        if mode and 'b' not in mode:
            mode += 'b'
        try:
            if fileobj is None:
                fileobj = self.myfileobj = builtins.open(filename, mode or 'rb')
            if filename is None:
                filename = getattr(fileobj, 'name', '')
                if not isinstance(filename, (str, bytes)):
                    filename = ''
            else:
                filename = os.fspath(filename)
            origmode = mode
            if mode is None:
                mode = getattr(fileobj, 'mode', 'rb')
            if mode.startswith('r'):
                self.mode = READ
                raw = _GzipReader(fileobj)
                self._buffer = io.BufferedReader(raw)
                self.name = filename
            elif mode.startswith(('w', 'a', 'x')):
                if origmode is None:
                    import warnings
                    warnings.warn('GzipFile was opened for writing, but this will change in future Python releases.  Specify the mode argument for opening it for writing.', FutureWarning, 2)
                self.mode = WRITE
                self._init_write(filename)
                self.压缩 = zlib.compressobj(compresslevel, zlib.DEFLATED, -zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, 0)
                self._write_mtime = mtime
                self._buffer_size = _WRITE_BUFFER_SIZE
                self._buffer = io.BufferedWriter(_WriteBufferStream(self), buffer_size=self._buffer_size)
            else:
                raise ValueError('Invalid mode: {!r}'.format(mode))
            self.fileobj = fileobj
            if self.mode == WRITE:
                self._write_gzip_header(compresslevel)
        except:
            self._close()
            raise

    @property
    def 修改时间(self):
        """Last modification time read from stream, or None"""
        return self._buffer.raw._last_mtime

    def __repr__(self):
        s = repr(self.fileobj)
        return '<gzip ' + s[1:-1] + ' ' + hex(id(self)) + '>'

    def _init_write(self, filename):
        self.name = filename
        self.crc = zlib.crc32(b'')
        self.size = 0
        self.writebuf = []
        self.bufsize = 0
        self.offset = 0

    def tell(self):
        self._check_not_closed()
        self._buffer.flush()
        return super().tell()

    def _write_gzip_header(self, compresslevel):
        self.fileobj.write(b'\x1f\x8b')
        self.fileobj.write(b'\x08')
        try:
            fname = os.path.basename(self.name)
            if not isinstance(fname, bytes):
                fname = fname.encode('latin-1')
            if fname.endswith(b'.gz'):
                fname = fname[:-3]
        except UnicodeEncodeError:
            fname = b''
        flags = 0
        if fname:
            flags = FNAME
        self.fileobj.write(chr(flags).encode('latin-1'))
        修改时间 = self._write_mtime
        if 修改时间 is None:
            修改时间 = time.time()
        write32u(self.fileobj, int(修改时间))
        if compresslevel == _COMPRESS_LEVEL_BEST:
            xfl = b'\x02'
        elif compresslevel == _COMPRESS_LEVEL_FAST:
            xfl = b'\x04'
        else:
            xfl = b'\x00'
        self.fileobj.write(xfl)
        self.fileobj.write(b'\xff')
        if fname:
            self.fileobj.write(fname + b'\x00')

    def write(self, data):
        self._check_not_closed()
        if self.mode != WRITE:
            import errno
            raise OSError(errno.EBADF, 'write() on read-only GzipFile object')
        if self.fileobj is None:
            raise ValueError('write() on closed GzipFile object')
        return self._buffer.write(data)

    def _write_raw(self, data):
        if isinstance(data, (bytes, bytearray)):
            length = len(data)
        else:
            data = memoryview(data)
            length = data.nbytes
        if length > 0:
            self.fileobj.write(self.压缩.compress(data))
            self.size += length
            self.crc = zlib.crc32(data, self.crc)
            self.offset += length
        return length

    def _check_read(self, caller):
        if self.mode != READ:
            import errno
            msg = f'{caller}() on write-only GzipFile object'
            raise OSError(errno.EBADF, msg)

    def read(self, size=-1):
        self._check_not_closed()
        self._check_read('read')
        return self._buffer.read(size)

    def read1(self, size=-1):
        """Implements BufferedIOBase.read1()

        Reads up to a buffer's worth of data if size is negative."""
        self._check_not_closed()
        self._check_read('read1')
        if size < 0:
            size = io.DEFAULT_BUFFER_SIZE
        return self._buffer.read1(size)

    def readinto(self, b):
        self._check_not_closed()
        self._check_read('readinto')
        return self._buffer.readinto(b)

    def readinto1(self, b):
        self._check_not_closed()
        self._check_read('readinto1')
        return self._buffer.readinto1(b)

    def peek(self, n):
        self._check_not_closed()
        self._check_read('peek')
        return self._buffer.peek(n)

    @property
    def closed(self):
        return self.fileobj is None

    def close(self):
        fileobj = self.fileobj
        if fileobj is None:
            return
        if self._buffer is None or self._buffer.closed:
            return
        try:
            if self.mode == WRITE:
                self._buffer.flush()
                fileobj.write(self.压缩.flush())
                write32u(fileobj, self.crc)
                write32u(fileobj, self.size & 4294967295)
            elif self.mode == READ:
                self._buffer.close()
        finally:
            self._close()

    def _close(self):
        self.fileobj = None
        myfileobj = self.myfileobj
        if myfileobj is not None:
            self.myfileobj = None
            myfileobj.close()

    def flush(self, zlib_mode=zlib.Z_SYNC_FLUSH):
        self._check_not_closed()
        if self.mode == WRITE:
            self._buffer.flush()
            self.fileobj.write(self.压缩.flush(zlib_mode))
            self.fileobj.flush()

    def fileno(self):
        """Invoke the underlying file object's fileno() method.

        This will raise AttributeError if the underlying file object
        doesn't support fileno().
        """
        return self.fileobj.fileno()

    def 回绕(self):
        """Return the uncompressed stream file position indicator to the
        beginning of the file"""
        if self.mode != READ:
            raise OSError("Can't rewind in write mode")
        self._buffer.seek(0)

    def readable(self):
        return self.mode == READ

    def writable(self):
        return self.mode == WRITE

    def seekable(self):
        return True

    def seek(self, offset, whence=io.SEEK_SET):
        if self.mode == WRITE:
            self._check_not_closed()
            self._buffer.flush()
            if whence != io.SEEK_SET:
                if whence == io.SEEK_CUR:
                    offset = self.offset + offset
                else:
                    raise ValueError('Seek from end not supported')
            if offset < self.offset:
                raise OSError('Negative seek in write mode')
            count = offset - self.offset
            chunk = b'\x00' * self._buffer_size
            for i in range(count // self._buffer_size):
                self.write(chunk)
            self.write(b'\x00' * (count % self._buffer_size))
        elif self.mode == READ:
            self._check_not_closed()
            return self._buffer.seek(offset, whence)
        return self.offset

    def readline(self, size=-1):
        self._check_not_closed()
        return self._buffer.readline(size)

    def __del__(self):
        if self.mode == WRITE and (not self.closed):
            import warnings
            warnings.warn('unclosed GzipFile', ResourceWarning, source=self, stacklevel=2)
        super().__del__()
_装类转发(GZIP文件, {'mtime': '修改时间', 'rewind': '回绕'}, {'compress': '压缩', 'mtime': '修改时间', 'rewind': '回绕'})

def _read_exact(fp, n):
    """Read exactly *n* bytes from `fp`

    This method is required because fp may be unbuffered,
    i.e. return short reads.
    """
    data = fp.read(n)
    while len(data) < n:
        b = fp.read(n - len(data))
        if not b:
            raise EOFError('Compressed file ended before the end-of-stream marker was reached')
        data += b
    return data

def _read_gzip_header(fp):
    """Read a gzip header from `fp` and progress to the end of the header.

    Returns last mtime if header was present or None otherwise.
    """
    magic = fp.read(2)
    if magic == b'':
        return None
    if magic != b'\x1f\x8b':
        raise 坏GZIP文件('Not a gzipped file (%r)' % magic)
    method, flag, last_mtime = struct.unpack('<BBIxx', _read_exact(fp, 8))
    if method != 8:
        raise 坏GZIP文件('Unknown compression method')
    if flag & FEXTRA:
        extra_len, = struct.unpack('<H', _read_exact(fp, 2))
        _read_exact(fp, extra_len)
    if flag & FNAME:
        while True:
            s = fp.read(1)
            if not s or s == b'\x00':
                break
    if flag & FCOMMENT:
        while True:
            s = fp.read(1)
            if not s or s == b'\x00':
                break
    if flag & FHCRC:
        _read_exact(fp, 2)
    return last_mtime

class _GzipReader(_streams.DecompressReader):

    def __init__(self, fp):
        super().__init__(_PaddedFile(fp), zlib._ZlibDecompressor, wbits=-zlib.MAX_WBITS)
        self._new_member = True
        self._last_mtime = None

    def _init_read(self):
        self._crc = zlib.crc32(b'')
        self._stream_size = 0

    def _read_gzip_header(self):
        last_mtime = _read_gzip_header(self._fp)
        if last_mtime is None:
            return False
        self._last_mtime = last_mtime
        return True

    def read(self, size=-1):
        if size < 0:
            return self.readall()
        if not size:
            return b''
        while True:
            if self._decompressor.eof:
                self._read_eof()
                self._new_member = True
                self._decompressor = self._decomp_factory(**self._decomp_args)
            if self._new_member:
                self._init_read()
                if not self._read_gzip_header():
                    self._size = self._pos
                    return b''
                self._new_member = False
            if self._decompressor.needs_input:
                buf = self._fp.read(读缓冲大小)
            else:
                buf = b''
            uncompress = self._decompressor.decompress(buf, size)
            if self._decompressor.unused_data != b'':
                self._fp.prepend(self._decompressor.unused_data)
            if uncompress != b'':
                break
            if buf == b'':
                raise EOFError('Compressed file ended before the end-of-stream marker was reached')
        self._crc = zlib.crc32(uncompress, self._crc)
        self._stream_size += len(uncompress)
        self._pos += len(uncompress)
        return uncompress

    def _read_eof(self):
        crc32, isize = struct.unpack('<II', _read_exact(self._fp, 8))
        if crc32 != self._crc:
            raise 坏GZIP文件('CRC check failed %s != %s' % (hex(crc32), hex(self._crc)))
        elif isize != self._stream_size & 4294967295:
            raise 坏GZIP文件('Incorrect length of data produced')
        c = b'\x00'
        while c == b'\x00':
            c = self._fp.read(1)
        if c:
            self._fp.prepend(c)

    def _rewind(self):
        super()._rewind()
        self._new_member = True

def 压缩(data, compresslevel=_COMPRESS_LEVEL_BEST, *, mtime=0):
    """Compress data in one shot and return the compressed string.

    compresslevel sets the compression level in range of 0-9.
    mtime can be used to set the modification time.
    The modification time is set to 0 by default, for reproducibility.
    """
    gzip_data = zlib.compress(data, level=compresslevel, wbits=31)
    if mtime is None:
        mtime = time.time()
    header = struct.pack('<4sLBB', gzip_data, int(mtime), gzip_data[8], 255)
    return header + gzip_data[10:]

def 解压(data):
    """Decompress a gzip compressed string in one shot.
    Return the decompressed string.
    """
    decompressed_members = []
    while True:
        fp = io.BytesIO(data)
        if _read_gzip_header(fp) is None:
            return b''.join(decompressed_members)
        do = zlib.decompressobj(wbits=-zlib.MAX_WBITS)
        decompressed = do.decompress(data[fp.tell():])
        if not do.eof or len(do.unused_data) < 8:
            raise EOFError('Compressed file ended before the end-of-stream marker was reached')
        crc, length = struct.unpack('<II', do.unused_data[:8])
        if crc != zlib.crc32(decompressed):
            raise 坏GZIP文件('CRC check failed')
        if length != len(decompressed) & 4294967295:
            raise 坏GZIP文件('Incorrect length of data produced')
        decompressed_members.append(decompressed)
        data = do.unused_data[8:].lstrip(b'\x00')

def 主函数():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='A simple command line interface for the gzip module: act like gzip, but do not delete the input file.', color=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--fast', action='store_true', help='compress faster')
    group.add_argument('--best', action='store_true', help='compress better')
    group.add_argument('-d', '--decompress', action='store_true', help='act like gunzip instead of gzip')
    parser.add_argument('args', nargs='*', default=['-'], metavar='file')
    args = parser.parse_args()
    compresslevel = _COMPRESS_LEVEL_TRADEOFF
    if args.fast:
        compresslevel = _COMPRESS_LEVEL_FAST
    elif args.best:
        compresslevel = _COMPRESS_LEVEL_BEST
    for arg in args.args:
        if args.decompress:
            if arg == '-':
                f = GZIP文件(filename='', mode='rb', fileobj=sys.stdin.buffer)
                g = sys.stdout.buffer
            else:
                if arg[-3:] != '.gz':
                    sys.exit(f"filename doesn't end in .gz: {arg!r}")
                f = open(arg, 'rb')
                g = builtins.open(arg[:-3], 'wb')
        elif arg == '-':
            f = sys.stdin.buffer
            g = GZIP文件(filename='', mode='wb', fileobj=sys.stdout.buffer, compresslevel=compresslevel)
        else:
            f = builtins.open(arg, 'rb')
            g = open(arg + '.gz', 'wb')
        while True:
            chunk = f.read(读缓冲大小)
            if not chunk:
                break
            g.write(chunk)
        if g is not sys.stdout.buffer:
            g.close()
        if f is not sys.stdin.buffer:
            f.close()
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

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import gzip as _英文库
坏GZIP文件 = _英文库.BadGzipFile
_模块别名 = {
    'BadGzipFile': '坏GZIP文件',
    'GzipFile': 'GZIP文件',
    'READ_BUFFER_SIZE': '读缓冲大小',
    'compress': '压缩',
    'decompress': '解压',
    'main': '主函数',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'GZIP文件': {
        'mtime': '修改时间',
        'rewind': '回绕',
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
    'GZIP文件': {
        'compress': '压缩',
        'mtime': '修改时间',
        'rewind': '回绕',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'GZIP文件',
    '压缩',
    '坏GZIP文件',
    '打开',
    '解压',
]

# ---- 转发层结束 ----
