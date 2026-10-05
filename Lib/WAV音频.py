# -*- coding: utf-8 -*-
"""WAV音频 —— 汉语库（由 tools/汉化库.py 从 Lib/wave.py 机械生成，**不要手改**）。

英文库 Lib/wave.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py WAV音频
"""


"""Stuff to parse WAVE files.

Usage.

Reading WAVE files:
      f = wave.open(file, 'r')
where file is either the name of a file or an open file pointer.
The open file pointer must have methods read(), seek(), and close().
When the setpos() and rewind() methods are not used, the seek()
method is not  necessary.

This returns an instance of a class with the following public methods:
      getnchannels()  -- returns number of audio channels (1 for
                         mono, 2 for stereo)
      getsampwidth()  -- returns sample width in bytes
      getframerate()  -- returns sampling frequency
      getnframes()    -- returns number of audio frames
      getcomptype()   -- returns compression type ('NONE' for linear samples)
      getcompname()   -- returns human-readable version of
                         compression type ('not compressed' linear samples)
      getparams()     -- returns a namedtuple consisting of all of the
                         above in the above order
      getmarkers()    -- returns None (for compatibility with the
                         old aifc module)
      getmark(id)     -- raises an error since the mark does not
                         exist (for compatibility with the old aifc module)
      readframes(n)   -- returns at most n frames of audio
      rewind()        -- rewind to the beginning of the audio stream
      setpos(pos)     -- seek to the specified position
      tell()          -- return the current position
      close()         -- close the instance (make it unusable)
The position returned by tell() and the position given to setpos()
are compatible and have nothing to do with the actual position in the
file.
The close() method is called automatically when the class instance
is destroyed.

Writing WAVE files:
      f = wave.open(file, 'w')
where file is either the name of a file or an open file pointer.
The open file pointer must have methods write(), tell(), seek(), and
close().

This returns an instance of a class with the following public methods:
      setnchannels(n) -- set the number of channels
      setsampwidth(n) -- set the sample width
      setframerate(n) -- set the frame rate
      setnframes(n)   -- set the number of frames
      setcomptype(type, name)
                      -- set the compression type and the
                         human-readable compression type
      setparams(tuple)
                      -- set all parameters at once
      tell()          -- return current position in output file
      writeframesraw(data)
                      -- write audio frames without patching up the
                         file header
      writeframes(data)
                      -- write audio frames and patch up the file header
      close()         -- patch up the file header and close the
                         output file
You should set the parameters before the first writeframesraw or
writeframes.  The total number of frames does not need to be set,
but when it is set to the correct value, the header does not have to
be patched up.
It is best to first set all parameters, perhaps possibly the
compression type, and then write audio frames using writeframesraw.
When all frames have been written, either call writeframes(b'') or
close() to patch up the sizes in the header.
The close() method is called automatically when the class instance
is destroyed.
"""
_英文原名表 = {'Error': '波形错误', 'Wave_read': '波形读取器', 'Wave_write': '波形写入器'}

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
from collections import namedtuple
import builtins
import struct
import sys
__all__ = ['open', 'Error', 'Wave_read', 'Wave_write']

class 波形错误(Exception):
    pass
WAVE_FORMAT_PCM = 1
WAVE_FORMAT_EXTENSIBLE = 65534
KSDATAFORMAT_SUBTYPE_PCM = b'\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x008\x9bq'
_array_fmts = (None, 'b', 'h', None, 'i')
_wave_params = namedtuple('_wave_params', 'nchannels sampwidth framerate nframes comptype compname')

def _byteswap(data, width):
    swapped_data = bytearray(len(data))
    for i in range(0, len(data), width):
        for j in range(width):
            swapped_data[i + width - 1 - j] = data[i + j]
    return bytes(swapped_data)

class _Chunk:

    def __init__(self, file, align=True, bigendian=True, inclheader=False):
        self.closed = False
        self.align = align
        if bigendian:
            strflag = '>'
        else:
            strflag = '<'
        self.file = file
        self.chunkname = file.read(4)
        if len(self.chunkname) < 4:
            raise EOFError
        try:
            self.chunksize = struct.unpack_from(strflag + 'L', file.read(4))[0]
        except struct.error:
            raise EOFError from None
        if inclheader:
            self.chunksize = self.chunksize - 8
        self.size_read = 0
        try:
            self.offset = self.file.tell()
        except (AttributeError, OSError):
            self.seekable = False
        else:
            self.seekable = True

    def getname(self):
        """Return the name (ID) of the current chunk."""
        return self.chunkname

    def close(self):
        if not self.closed:
            try:
                self.skip()
            finally:
                self.closed = True

    def seek(self, pos, whence=0):
        """Seek to specified position into the chunk.
        Default position is 0 (start of chunk).
        If the file is not seekable, this will result in an error.
        """
        if self.closed:
            raise ValueError('I/O operation on closed file')
        if not self.seekable:
            raise OSError('cannot seek')
        if whence == 1:
            pos = pos + self.size_read
        elif whence == 2:
            pos = pos + self.chunksize
        if pos < 0 or pos > self.chunksize:
            raise RuntimeError
        self.file.seek(self.offset + pos, 0)
        self.size_read = pos

    def tell(self):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        return self.size_read

    def read(self, size=-1):
        """Read at most size bytes from the chunk.
        If size is omitted or negative, read until the end
        of the chunk.
        """
        if self.closed:
            raise ValueError('I/O operation on closed file')
        if self.size_read >= self.chunksize:
            return b''
        if size < 0:
            size = self.chunksize - self.size_read
        if size > self.chunksize - self.size_read:
            size = self.chunksize - self.size_read
        data = self.file.read(size)
        self.size_read = self.size_read + len(data)
        if self.size_read == self.chunksize and self.align and self.chunksize & 1:
            dummy = self.file.read(1)
            self.size_read = self.size_read + len(dummy)
        return data

    def skip(self):
        """Skip the rest of the chunk.
        If you are not interested in the contents of the chunk,
        this method should be called so that the file points to
        the start of the next chunk.
        """
        if self.closed:
            raise ValueError('I/O operation on closed file')
        if self.seekable:
            try:
                n = self.chunksize - self.size_read
                if self.align and self.chunksize & 1:
                    n = n + 1
                self.file.seek(n, 1)
                self.size_read = self.size_read + n
                return
            except OSError:
                pass
        while self.size_read < self.chunksize:
            n = min(8192, self.chunksize - self.size_read)
            dummy = self.read(n)
            if not dummy:
                raise EOFError

class 波形读取器:
    """Variables used in this class:

    These variables are available to the user though appropriate
    methods of this class:
    _file -- the open file with methods read(), close(), and seek()
              set through the __init__() method
    _nchannels -- the number of audio channels
              available through the getnchannels() method
    _nframes -- the number of audio frames
              available through the getnframes() method
    _sampwidth -- the number of bytes per audio sample
              available through the getsampwidth() method
    _framerate -- the sampling frequency
              available through the getframerate() method
    _comptype -- the AIFF-C compression type ('NONE' if AIFF)
              available through the getcomptype() method
    _compname -- the human-readable AIFF-C compression type
              available through the getcomptype() method
    _soundpos -- the position in the audio stream
              available through the tell() method, set through the
              setpos() method

    These variables are used internally only:
    _fmt_chunk_read -- 1 iff the FMT chunk has been read
    _data_seek_needed -- 1 iff positioned correctly in audio
              file for readframes()
    _data_chunk -- instantiation of a chunk class for the DATA chunk
    _framesize -- size of one frame in the file
    """

    def 从文件初始化(self, file):
        self._convert = None
        self._soundpos = 0
        self._file = _Chunk(file, bigendian=0)
        if self._file.getname() != b'RIFF':
            raise 波形错误('file does not start with RIFF id')
        if self._file.read(4) != b'WAVE':
            raise 波形错误('not a WAVE file')
        self._fmt_chunk_read = 0
        self._data_chunk = None
        while 1:
            self._data_seek_needed = 1
            try:
                chunk = _Chunk(self._file, bigendian=0)
            except EOFError:
                break
            chunkname = chunk.getname()
            if chunkname == b'fmt ':
                self._read_fmt_chunk(chunk)
                self._fmt_chunk_read = 1
            elif chunkname == b'data':
                if not self._fmt_chunk_read:
                    raise 波形错误('data chunk before fmt chunk')
                self._data_chunk = chunk
                self._nframes = chunk.chunksize // self._framesize
                self._data_seek_needed = 0
                break
            chunk.skip()
        if not self._fmt_chunk_read or not self._data_chunk:
            raise 波形错误('fmt chunk and/or data chunk missing')

    def __init__(self, f):
        self._i_opened_the_file = None
        if isinstance(f, str):
            f = builtins.open(f, 'rb')
            self._i_opened_the_file = f
        try:
            self.从文件初始化(f)
        except:
            if self._i_opened_the_file:
                f.close()
            raise

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def 取文件对象(self):
        return self._file

    def 倒回(self):
        self._data_seek_needed = 1
        self._soundpos = 0

    def close(self):
        self._file = None
        file = self._i_opened_the_file
        if file:
            self._i_opened_the_file = None
            file.close()

    def tell(self):
        return self._soundpos

    def 取声道数(self):
        return self._nchannels

    def 取帧数(self):
        return self._nframes

    def 取采样宽度(self):
        return self._sampwidth

    def 取采样率(self):
        return self._framerate

    def 取压缩类型(self):
        return self._comptype

    def 取压缩名(self):
        return self._compname

    def 取参数组(self):
        return _wave_params(self.取声道数(), self.取采样宽度(), self.取采样率(), self.取帧数(), self.取压缩类型(), self.取压缩名())

    def 取标记表(self):
        import warnings
        warnings._deprecated('Wave_read.getmarkers', remove=(3, 15))
        return None

    def 取标记(self, id):
        import warnings
        warnings._deprecated('Wave_read.getmark', remove=(3, 15))
        raise 波形错误('no marks')

    def 设位置(self, pos):
        if pos < 0 or pos > self._nframes:
            raise 波形错误('position not in range')
        self._soundpos = pos
        self._data_seek_needed = 1

    def 读帧(self, nframes):
        if self._data_seek_needed:
            self._data_chunk.seek(0, 0)
            pos = self._soundpos * self._framesize
            if pos:
                self._data_chunk.seek(pos, 0)
            self._data_seek_needed = 0
        if nframes == 0:
            return b''
        data = self._data_chunk.read(nframes * self._framesize)
        if self._sampwidth != 1 and sys.byteorder == 'big':
            data = _byteswap(data, self._sampwidth)
        if self._convert and data:
            data = self._convert(data)
        self._soundpos = self._soundpos + len(data) // (self._nchannels * self._sampwidth)
        return data

    def _read_fmt_chunk(self, chunk):
        try:
            wFormatTag, self._nchannels, self._framerate, dwAvgBytesPerSec, wBlockAlign = struct.unpack_from('<HHLLH', chunk.read(14))
        except struct.error:
            raise EOFError from None
        if wFormatTag != WAVE_FORMAT_PCM and wFormatTag != WAVE_FORMAT_EXTENSIBLE:
            raise 波形错误('unknown format: %r' % (wFormatTag,))
        try:
            sampwidth = struct.unpack_from('<H', chunk.read(2))[0]
        except struct.error:
            raise EOFError from None
        if wFormatTag == WAVE_FORMAT_EXTENSIBLE:
            try:
                cbSize, wValidBitsPerSample, dwChannelMask = struct.unpack_from('<HHL', chunk.read(8))
                SubFormat = chunk.read(16)
                if len(SubFormat) < 16:
                    raise EOFError
            except struct.error:
                raise EOFError from None
            if SubFormat != KSDATAFORMAT_SUBTYPE_PCM:
                try:
                    import uuid
                    subformat_msg = f'unknown extended format: {uuid.UUID(bytes_le=SubFormat)}'
                except Exception:
                    subformat_msg = 'unknown extended format'
                raise 波形错误(subformat_msg)
        self._sampwidth = (sampwidth + 7) // 8
        if not self._sampwidth:
            raise 波形错误('bad sample width')
        if not self._nchannels:
            raise 波形错误('bad # of channels')
        self._framesize = self._nchannels * self._sampwidth
        self._comptype = 'NONE'
        self._compname = 'not compressed'
_装类转发(波形读取器, {'getcompname': '取压缩名', 'getcomptype': '取压缩类型', 'getfp': '取文件对象', 'getframerate': '取采样率', 'getmark': '取标记', 'getmarkers': '取标记表', 'getnchannels': '取声道数', 'getnframes': '取帧数', 'getparams': '取参数组', 'getsampwidth': '取采样宽度', 'initfp': '从文件初始化', 'readframes': '读帧', 'rewind': '倒回', 'setpos': '设位置'}, {'getcompname': '取压缩名', 'getcomptype': '取压缩类型', 'getfp': '取文件对象', 'getframerate': '取采样率', 'getmark': '取标记', 'getmarkers': '取标记表', 'getnchannels': '取声道数', 'getnframes': '取帧数', 'getparams': '取参数组', 'getsampwidth': '取采样宽度', 'initfp': '从文件初始化', 'readframes': '读帧', 'rewind': '倒回', 'setpos': '设位置'})

class 波形写入器:
    """Variables used in this class:

    These variables are user settable through appropriate methods
    of this class:
    _file -- the open file with methods write(), close(), tell(), seek()
              set through the __init__() method
    _comptype -- the AIFF-C compression type ('NONE' in AIFF)
              set through the setcomptype() or setparams() method
    _compname -- the human-readable AIFF-C compression type
              set through the setcomptype() or setparams() method
    _nchannels -- the number of audio channels
              set through the setnchannels() or setparams() method
    _sampwidth -- the number of bytes per audio sample
              set through the setsampwidth() or setparams() method
    _framerate -- the sampling frequency
              set through the setframerate() or setparams() method
    _nframes -- the number of audio frames written to the header
              set through the setnframes() or setparams() method

    These variables are used internally only:
    _datalength -- the size of the audio samples written to the header
    _nframeswritten -- the number of frames actually written
    _datawritten -- the size of the audio samples actually written
    """
    _file = None

    def __init__(self, f):
        self._i_opened_the_file = None
        if isinstance(f, str):
            f = builtins.open(f, 'wb')
            self._i_opened_the_file = f
        try:
            self.从文件初始化(f)
        except:
            if self._i_opened_the_file:
                f.close()
            raise

    def 从文件初始化(self, file):
        self._file = file
        self._convert = None
        self._nchannels = 0
        self._sampwidth = 0
        self._framerate = 0
        self._nframes = 0
        self._nframeswritten = 0
        self._datawritten = 0
        self._datalength = 0
        self._headerwritten = False

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def 设声道数(self, nchannels):
        if self._datawritten:
            raise 波形错误('cannot change parameters after starting to write')
        if nchannels < 1:
            raise 波形错误('bad # of channels')
        self._nchannels = nchannels

    def 取声道数(self):
        if not self._nchannels:
            raise 波形错误('number of channels not set')
        return self._nchannels

    def 设采样宽度(self, sampwidth):
        if self._datawritten:
            raise 波形错误('cannot change parameters after starting to write')
        if sampwidth < 1 or sampwidth > 4:
            raise 波形错误('bad sample width')
        self._sampwidth = sampwidth

    def 取采样宽度(self):
        if not self._sampwidth:
            raise 波形错误('sample width not set')
        return self._sampwidth

    def 设采样率(self, framerate):
        if self._datawritten:
            raise 波形错误('cannot change parameters after starting to write')
        if framerate <= 0:
            raise 波形错误('bad frame rate')
        self._framerate = int(round(framerate))

    def 取采样率(self):
        if not self._framerate:
            raise 波形错误('frame rate not set')
        return self._framerate

    def 设帧数(self, nframes):
        if self._datawritten:
            raise 波形错误('cannot change parameters after starting to write')
        self._nframes = nframes

    def 取帧数(self):
        return self._nframeswritten

    def 设压缩类型(self, comptype, compname):
        if self._datawritten:
            raise 波形错误('cannot change parameters after starting to write')
        if comptype not in ('NONE',):
            raise 波形错误('unsupported compression type')
        self._comptype = comptype
        self._compname = compname

    def 取压缩类型(self):
        return self._comptype

    def 取压缩名(self):
        return self._compname

    def 设参数组(self, params):
        nchannels, sampwidth, framerate, nframes, comptype, compname = params
        if self._datawritten:
            raise 波形错误('cannot change parameters after starting to write')
        self.设声道数(nchannels)
        self.设采样宽度(sampwidth)
        self.设采样率(framerate)
        self.设帧数(nframes)
        self.设压缩类型(comptype, compname)

    def 取参数组(self):
        if not self._nchannels or not self._sampwidth or (not self._framerate):
            raise 波形错误('not all parameters set')
        return _wave_params(self._nchannels, self._sampwidth, self._framerate, self._nframes, self._comptype, self._compname)

    def 设标记(self, id, pos, name):
        import warnings
        warnings._deprecated('Wave_write.setmark', remove=(3, 15))
        raise 波形错误('setmark() not supported')

    def 取标记(self, id):
        import warnings
        warnings._deprecated('Wave_write.getmark', remove=(3, 15))
        raise 波形错误('no marks')

    def 取标记表(self):
        import warnings
        warnings._deprecated('Wave_write.getmarkers', remove=(3, 15))
        return None

    def tell(self):
        return self._nframeswritten

    def 写原始帧(self, data):
        if not isinstance(data, (bytes, bytearray)):
            data = memoryview(data).cast('B')
        self._ensure_header_written(len(data))
        nframes = len(data) // (self._sampwidth * self._nchannels)
        if self._convert:
            data = self._convert(data)
        if self._sampwidth != 1 and sys.byteorder == 'big':
            data = _byteswap(data, self._sampwidth)
        self._file.write(data)
        self._datawritten += len(data)
        self._nframeswritten = self._nframeswritten + nframes

    def 写帧(self, data):
        self.写原始帧(data)
        if self._datalength != self._datawritten:
            self._patchheader()

    def close(self):
        try:
            if self._file:
                self._ensure_header_written(0)
                if self._datalength != self._datawritten:
                    self._patchheader()
                self._file.flush()
        finally:
            self._file = None
            file = self._i_opened_the_file
            if file:
                self._i_opened_the_file = None
                file.close()

    def _ensure_header_written(self, datasize):
        if not self._headerwritten:
            if not self._nchannels:
                raise 波形错误('# channels not specified')
            if not self._sampwidth:
                raise 波形错误('sample width not specified')
            if not self._framerate:
                raise 波形错误('sampling rate not specified')
            self._write_header(datasize)

    def _write_header(self, initlength):
        assert not self._headerwritten
        self._file.write(b'RIFF')
        if not self._nframes:
            self._nframes = initlength // (self._nchannels * self._sampwidth)
        self._datalength = self._nframes * self._nchannels * self._sampwidth
        try:
            self._form_length_pos = self._file.tell()
        except (AttributeError, OSError):
            self._form_length_pos = None
        self._file.write(struct.pack('<L4s4sLHHLLHH4s', 36 + self._datalength, b'WAVE', b'fmt ', 16, WAVE_FORMAT_PCM, self._nchannels, self._framerate, self._nchannels * self._framerate * self._sampwidth, self._nchannels * self._sampwidth, self._sampwidth * 8, b'data'))
        if self._form_length_pos is not None:
            self._data_length_pos = self._file.tell()
        self._file.write(struct.pack('<L', self._datalength))
        self._headerwritten = True

    def _patchheader(self):
        assert self._headerwritten
        if self._datawritten == self._datalength:
            return
        curpos = self._file.tell()
        self._file.seek(self._form_length_pos, 0)
        self._file.write(struct.pack('<L', 36 + self._datawritten))
        self._file.seek(self._data_length_pos, 0)
        self._file.write(struct.pack('<L', self._datawritten))
        self._file.seek(curpos, 0)
        self._datalength = self._datawritten
_装类转发(波形写入器, {'getcompname': '取压缩名', 'getcomptype': '取压缩类型', 'getframerate': '取采样率', 'getmark': '取标记', 'getmarkers': '取标记表', 'getnchannels': '取声道数', 'getnframes': '取帧数', 'getparams': '取参数组', 'getsampwidth': '取采样宽度', 'initfp': '从文件初始化', 'setcomptype': '设压缩类型', 'setframerate': '设采样率', 'setmark': '设标记', 'setnchannels': '设声道数', 'setnframes': '设帧数', 'setparams': '设参数组', 'setsampwidth': '设采样宽度', 'writeframes': '写帧', 'writeframesraw': '写原始帧'}, {'getcompname': '取压缩名', 'getcomptype': '取压缩类型', 'getframerate': '取采样率', 'getmark': '取标记', 'getmarkers': '取标记表', 'getnchannels': '取声道数', 'getnframes': '取帧数', 'getparams': '取参数组', 'getsampwidth': '取采样宽度', 'initfp': '从文件初始化', 'setcomptype': '设压缩类型', 'setframerate': '设采样率', 'setmark': '设标记', 'setnchannels': '设声道数', 'setnframes': '设帧数', 'setparams': '设参数组', 'setsampwidth': '设采样宽度', 'writeframes': '写帧', 'writeframesraw': '写原始帧'})

def open(f, mode=None):
    if mode is None:
        if hasattr(f, 'mode'):
            mode = f.mode
        else:
            mode = 'rb'
    if mode in ('r', 'rb'):
        return 波形读取器(f)
    elif mode in ('w', 'wb'):
        return 波形写入器(f)
    else:
        raise 波形错误("mode must be 'r', 'rb', 'w', or 'wb'")


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
    'PCM子类型': 'KSDATAFORMAT_SUBTYPE_PCM',
    'PCM波形格式': 'WAVE_FORMAT_PCM',
    '可扩展波形格式': 'WAVE_FORMAT_EXTENSIBLE',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'Error': '波形错误',
    'Wave_read': '波形读取器',
    'Wave_write': '波形写入器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '波形写入器': {
        'getcompname': '取压缩名',
        'getcomptype': '取压缩类型',
        'getframerate': '取采样率',
        'getmark': '取标记',
        'getmarkers': '取标记表',
        'getnchannels': '取声道数',
        'getnframes': '取帧数',
        'getparams': '取参数组',
        'getsampwidth': '取采样宽度',
        'initfp': '从文件初始化',
        'setcomptype': '设压缩类型',
        'setframerate': '设采样率',
        'setmark': '设标记',
        'setnchannels': '设声道数',
        'setnframes': '设帧数',
        'setparams': '设参数组',
        'setsampwidth': '设采样宽度',
        'writeframes': '写帧',
        'writeframesraw': '写原始帧',
    },
    '波形读取器': {
        'getcompname': '取压缩名',
        'getcomptype': '取压缩类型',
        'getfp': '取文件对象',
        'getframerate': '取采样率',
        'getmark': '取标记',
        'getmarkers': '取标记表',
        'getnchannels': '取声道数',
        'getnframes': '取帧数',
        'getparams': '取参数组',
        'getsampwidth': '取采样宽度',
        'initfp': '从文件初始化',
        'readframes': '读帧',
        'rewind': '倒回',
        'setpos': '设位置',
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
    '波形写入器': {
        'getcompname': '取压缩名',
        'getcomptype': '取压缩类型',
        'getframerate': '取采样率',
        'getmark': '取标记',
        'getmarkers': '取标记表',
        'getnchannels': '取声道数',
        'getnframes': '取帧数',
        'getparams': '取参数组',
        'getsampwidth': '取采样宽度',
        'initfp': '从文件初始化',
        'setcomptype': '设压缩类型',
        'setframerate': '设采样率',
        'setmark': '设标记',
        'setnchannels': '设声道数',
        'setnframes': '设帧数',
        'setparams': '设参数组',
        'setsampwidth': '设采样宽度',
        'writeframes': '写帧',
        'writeframesraw': '写原始帧',
    },
    '波形读取器': {
        'getcompname': '取压缩名',
        'getcomptype': '取压缩类型',
        'getfp': '取文件对象',
        'getframerate': '取采样率',
        'getmark': '取标记',
        'getmarkers': '取标记表',
        'getnchannels': '取声道数',
        'getnframes': '取帧数',
        'getparams': '取参数组',
        'getsampwidth': '取采样宽度',
        'initfp': '从文件初始化',
        'readframes': '读帧',
        'rewind': '倒回',
        'setpos': '设位置',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'PCM子类型',
    'PCM波形格式',
    '可扩展波形格式',
    '波形写入器',
    '波形读取器',
    '波形错误',
]

# ---- 转发层结束 ----
