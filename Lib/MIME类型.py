# -*- coding: utf-8 -*-
"""MIME类型 —— 汉语库（由 tools/汉化库.py 从 Lib/mimetypes.py 机械生成，**不要手改**）。

英文库 Lib/mimetypes.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py MIME类型
"""


"""Guess the MIME type of a file.

This module defines two useful functions:

guess_type(url, strict=True) -- guess the MIME type and encoding of a URL.

guess_extension(type, strict=True) -- guess the extension for a given MIME type.

It also contains the following, for tuning the behavior:

Data:

knownfiles -- list of files to parse
inited -- flag set when init() has been called
suffix_map -- dictionary mapping suffixes to suffixes
encodings_map -- dictionary mapping suffixes to encodings
types_map -- dictionary mapping suffixes to types

Functions:

init([files]) -- parse a list of files, default knownfiles (on Windows, the
  default values are taken from the registry)
read_mime_types(file) -- parse one file, return a dictionary or None
"""
_英文原名表 = {'MimeTypes': 'MIME类型表', 'add_type': '加类型', 'guess_all_extensions': '猜所有扩展名', 'guess_extension': '猜扩展名', 'guess_file_type': '猜文件类型', 'guess_type': '猜类型', 'init': '初始化', 'read_mime_types': '读类型文件'}

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
try:
    from _winapi import _mimetypes_read_windows_registry
except ImportError:
    _mimetypes_read_windows_registry = None
try:
    import winreg as _winreg
except ImportError:
    _winreg = None
__all__ = ['knownfiles', 'inited', 'MimeTypes', 'guess_type', 'guess_file_type', 'guess_all_extensions', 'guess_extension', 'add_type', 'init', 'read_mime_types', 'suffix_map', 'encodings_map', 'types_map', 'common_types']
knownfiles = ['/etc/mime.types', '/etc/httpd/mime.types', '/etc/httpd/conf/mime.types', '/etc/apache/mime.types', '/etc/apache2/mime.types', '/usr/local/etc/httpd/conf/mime.types', '/usr/local/lib/netscape/mime.types', '/usr/local/etc/httpd/conf/mime.types', '/usr/local/etc/mime.types']
inited = False
_db = None

class MIME类型表:
    """MIME-types datastore.

    This datastore can handle information from mime.types-style files
    and supports basic determination of MIME type from a filename or
    URL, and can guess a reasonable extension given a MIME type.
    """

    def __init__(self, filenames=(), strict=True):
        if not inited:
            初始化()
        self.encodings_map = _encodings_map_default.copy()
        self.suffix_map = _suffix_map_default.copy()
        self.types_map = ({}, {})
        self.types_map_inv = ({}, {})
        for ext, type in _types_map_default.items():
            self.加类型(type, ext, True)
        for ext, type in _common_types_default.items():
            self.加类型(type, ext, False)
        for name in filenames:
            self.read(name, strict)

    def 加类型(self, type, ext, strict=True):
        """Add a mapping between a type and an extension.

        When the extension is already known, the new
        type will replace the old one. When the type
        is already known the extension will be added
        to the list of known extensions.

        If strict is true, information will be added to
        list of standard types, else to the list of non-standard
        types.

        Valid extensions are empty or start with a '.'.
        """
        if ext and (not ext.startswith('.')):
            from warnings import _deprecated
            _deprecated('Undotted extensions', 'Using undotted extensions is deprecated and will raise a ValueError in Python {remove}', remove=(3, 16))
        if not type:
            return
        self.types_map[strict][ext] = type
        exts = self.types_map_inv[strict].setdefault(type, [])
        if ext not in exts:
            exts.append(ext)

    def 猜类型(self, url, strict=True):
        """Guess the type of a file which is either a URL or a path-like object.

        Return value is a tuple (type, encoding) where type is None if
        the type can't be guessed (no or unknown suffix) or a string
        of the form type/subtype, usable for a MIME Content-type
        header; and encoding is None for no encoding or the name of
        the program used to encode (e.g. compress or gzip).  The
        mappings are table driven.  Encoding suffixes are case
        sensitive; type suffixes are first tried case sensitive, then
        case insensitive.

        The suffixes .tgz, .taz and .tz (case sensitive!) are all
        mapped to '.tar.gz'.  (This is table-driven too, using the
        dictionary suffix_map.)

        Optional 'strict' argument when False adds a bunch of commonly found,
        but non-standard types.
        """
        import os
        import urllib.parse
        url = os.fspath(url)
        p = urllib.parse.urlparse(url)
        if p.scheme and len(p.scheme) > 1:
            scheme = p.scheme
            url = p.path
        else:
            return self.猜文件类型(url, strict=strict)
        if scheme == 'data':
            comma = url.find(',')
            if comma < 0:
                return (None, None)
            semi = url.find(';', 0, comma)
            if semi >= 0:
                type = url[:semi]
            else:
                type = url[:comma]
            if '=' in type or '/' not in type:
                type = 'text/plain'
            return (type, None)
        import posixpath
        return self._guess_file_type(url, strict, posixpath.splitext)

    def 猜文件类型(self, path, *, strict=True):
        """Guess the type of a file based on its path.

        Similar to guess_type(), but takes file path instead of URL.
        """
        import os
        path = os.fsdecode(path)
        path = os.path.splitdrive(path)[1]
        return self._guess_file_type(path, strict, os.path.splitext)

    def _guess_file_type(self, path, strict, splitext):
        base, ext = splitext(path)
        while (ext_lower := ext.lower()) in self.suffix_map:
            base, ext = splitext(base + self.suffix_map[ext_lower])
        if ext in self.encodings_map:
            encoding = self.encodings_map[ext]
            base, ext = splitext(base)
        else:
            encoding = None
        ext = ext.lower()
        types_map = self.types_map[True]
        if ext in types_map:
            return (types_map[ext], encoding)
        elif strict:
            return (None, encoding)
        types_map = self.types_map[False]
        if ext in types_map:
            return (types_map[ext], encoding)
        else:
            return (None, encoding)

    def 猜所有扩展名(self, type, strict=True):
        """Guess the extensions for a file based on its MIME type.

        Return value is a list of strings giving the possible filename
        extensions, including the leading dot ('.').  The extension is not
        guaranteed to have been associated with any particular data stream,
        but would be mapped to the MIME type 'type' by guess_type().

        Optional 'strict' argument when false adds a bunch of commonly found,
        but non-standard types.
        """
        type = type.lower()
        extensions = list(self.types_map_inv[True].get(type, []))
        if not strict:
            for ext in self.types_map_inv[False].get(type, []):
                if ext not in extensions:
                    extensions.append(ext)
        return extensions

    def 猜扩展名(self, type, strict=True):
        """Guess the extension for a file based on its MIME type.

        Return value is a string giving a filename extension,
        including the leading dot ('.').  The extension is not
        guaranteed to have been associated with any particular data
        stream, but would be mapped to the MIME type 'type' by
        guess_type().  If no extension can be guessed for 'type', None
        is returned.

        Optional 'strict' argument when false adds a bunch of commonly found,
        but non-standard types.
        """
        extensions = self.猜所有扩展名(type, strict)
        if not extensions:
            return None
        return extensions[0]

    def read(self, filename, strict=True):
        """
        Read a single mime.types-format file, specified by pathname.

        If strict is true, information will be added to
        list of standard types, else to the list of non-standard
        types.
        """
        with open(filename, encoding='utf-8', errors='surrogateescape') as fp:
            self.从文件对象读(fp, strict)

    def 从文件对象读(self, fp, strict=True):
        """
        Read a single mime.types-format file.

        If strict is true, information will be added to
        list of standard types, else to the list of non-standard
        types.
        """
        while (line := fp.readline()):
            words = line.split()
            for i in range(len(words)):
                if words[i][0] == '#':
                    del words[i:]
                    break
            if not words:
                continue
            type, suffixes = (words[0], words[1:])
            for suff in suffixes:
                self.加类型(type, '.' + suff, strict)

    def 读Windows注册表(self, strict=True):
        """
        Load the MIME types database from Windows registry.

        If strict is true, information will be added to
        list of standard types, else to the list of non-standard
        types.
        """
        if not _mimetypes_read_windows_registry and (not _winreg):
            return
        加类型 = self.加类型
        if strict:
            加类型 = lambda type, ext: self.加类型(type, ext, True)
        if _mimetypes_read_windows_registry:
            _mimetypes_read_windows_registry(加类型)
        elif _winreg:
            self._read_windows_registry(加类型)

    @classmethod
    def _read_windows_registry(cls, add_type):

        def enum_types(mimedb):
            i = 0
            while True:
                try:
                    ctype = _winreg.EnumKey(mimedb, i)
                except OSError:
                    break
                else:
                    if '\x00' not in ctype:
                        yield ctype
                i += 1
        with _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, '') as hkcr:
            for subkeyname in enum_types(hkcr):
                try:
                    with _winreg.OpenKey(hkcr, subkeyname) as subkey:
                        if not subkeyname.startswith('.'):
                            continue
                        mimetype, datatype = _winreg.QueryValueEx(subkey, 'Content Type')
                        if datatype != _winreg.REG_SZ:
                            continue
                        add_type(mimetype, subkeyname)
                except OSError:
                    continue
_装类转发(MIME类型表, {'add_type': '加类型', 'guess_all_extensions': '猜所有扩展名', 'guess_extension': '猜扩展名', 'guess_file_type': '猜文件类型', 'guess_type': '猜类型', 'read_windows_registry': '读Windows注册表', 'readfp': '从文件对象读'}, {'add_type': '加类型', 'guess_all_extensions': '猜所有扩展名', 'guess_extension': '猜扩展名', 'guess_file_type': '猜文件类型', 'guess_type': '猜类型', 'read_windows_registry': '读Windows注册表', 'readfp': '从文件对象读'})

def 猜类型(url, strict=True):
    """Guess the type of a file based on its URL.

    Return value is a tuple (type, encoding) where type is None if the
    type can't be guessed (no or unknown suffix) or a string of the
    form type/subtype, usable for a MIME Content-type header; and
    encoding is None for no encoding or the name of the program used
    to encode (e.g. compress or gzip).  The mappings are table
    driven.  Encoding suffixes are case sensitive; type suffixes are
    first tried case sensitive, then case insensitive.

    The suffixes .tgz, .taz and .tz (case sensitive!) are all mapped
    to ".tar.gz".  (This is table-driven too, using the dictionary
    suffix_map).

    Optional 'strict' argument when false adds a bunch of commonly found, but
    non-standard types.
    """
    if _db is None:
        初始化()
    return _db.guess_type(url, strict)

def 猜文件类型(path, *, strict=True):
    """Guess the type of a file based on its path.

    Similar to guess_type(), but takes file path instead of URL.
    """
    if _db is None:
        初始化()
    return _db.guess_file_type(path, strict=strict)

def 猜所有扩展名(type, strict=True):
    """Guess the extensions for a file based on its MIME type.

    Return value is a list of strings giving the possible filename
    extensions, including the leading dot ('.').  The extension is not
    guaranteed to have been associated with any particular data
    stream, but would be mapped to the MIME type 'type' by
    guess_type().  If no extension can be guessed for 'type', None
    is returned.

    Optional 'strict' argument when false adds a bunch of commonly found,
    but non-standard types.
    """
    if _db is None:
        初始化()
    return _db.guess_all_extensions(type, strict)

def 猜扩展名(type, strict=True):
    """Guess the extension for a file based on its MIME type.

    Return value is a string giving a filename extension, including the
    leading dot ('.').  The extension is not guaranteed to have been
    associated with any particular data stream, but would be mapped to the
    MIME type 'type' by guess_type().  If no extension can be guessed for
    'type', None is returned.

    Optional 'strict' argument when false adds a bunch of commonly found,
    but non-standard types.
    """
    if _db is None:
        初始化()
    return _db.guess_extension(type, strict)

def 加类型(type, ext, strict=True):
    """Add a mapping between a type and an extension.

    When the extension is already known, the new
    type will replace the old one. When the type
    is already known the extension will be added
    to the list of known extensions.

    If strict is true, information will be added to
    list of standard types, else to the list of non-standard
    types.
    """
    if _db is None:
        初始化()
    return _db.add_type(type, ext, strict)

def 初始化(files=None):
    global suffix_map, types_map, encodings_map, common_types
    global inited, _db
    inited = True
    if files is None or _db is None:
        db = MIME类型表()
        db.read_windows_registry()
        if files is None:
            files = knownfiles
        else:
            files = knownfiles + list(files)
    else:
        db = _db
    import os
    for file in files:
        if os.path.isfile(file):
            db.read(file)
    encodings_map = db.encodings_map
    suffix_map = db.suffix_map
    types_map = db.types_map[True]
    common_types = db.types_map[False]
    _db = db

def 读类型文件(file):
    try:
        f = open(file, encoding='utf-8', errors='surrogateescape')
    except OSError:
        return None
    with f:
        db = MIME类型表()
        db.readfp(f, True)
        return db.types_map[True]

def _default_mime_types():
    global suffix_map, _suffix_map_default
    global encodings_map, _encodings_map_default
    global types_map, _types_map_default
    global common_types, _common_types_default
    suffix_map = _suffix_map_default = {'.svgz': '.svg.gz', '.tgz': '.tar.gz', '.taz': '.tar.gz', '.tz': '.tar.gz', '.tbz2': '.tar.bz2', '.txz': '.tar.xz'}
    encodings_map = _encodings_map_default = {'.gz': 'gzip', '.Z': 'compress', '.bz2': 'bzip2', '.xz': 'xz', '.br': 'br'}
    types_map = _types_map_default = {'.js': 'text/javascript', '.mjs': 'text/javascript', '.epub': 'application/epub+zip', '.gz': 'application/gzip', '.json': 'application/json', '.webmanifest': 'application/manifest+json', '.doc': 'application/msword', '.dot': 'application/msword', '.wiz': 'application/msword', '.nq': 'application/n-quads', '.nt': 'application/n-triples', '.bin': 'application/octet-stream', '.a': 'application/octet-stream', '.dll': 'application/octet-stream', '.exe': 'application/octet-stream', '.o': 'application/octet-stream', '.obj': 'application/octet-stream', '.so': 'application/octet-stream', '.oda': 'application/oda', '.ogx': 'application/ogg', '.pdf': 'application/pdf', '.p7c': 'application/pkcs7-mime', '.ps': 'application/postscript', '.ai': 'application/postscript', '.eps': 'application/postscript', '.trig': 'application/trig', '.m3u': 'application/vnd.apple.mpegurl', '.m3u8': 'application/vnd.apple.mpegurl', '.xls': 'application/vnd.ms-excel', '.xlb': 'application/vnd.ms-excel', '.eot': 'application/vnd.ms-fontobject', '.ppt': 'application/vnd.ms-powerpoint', '.pot': 'application/vnd.ms-powerpoint', '.ppa': 'application/vnd.ms-powerpoint', '.pps': 'application/vnd.ms-powerpoint', '.pwz': 'application/vnd.ms-powerpoint', '.odg': 'application/vnd.oasis.opendocument.graphics', '.odp': 'application/vnd.oasis.opendocument.presentation', '.ods': 'application/vnd.oasis.opendocument.spreadsheet', '.odt': 'application/vnd.oasis.opendocument.text', '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation', '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.rar': 'application/vnd.rar', '.wasm': 'application/wasm', '.7z': 'application/x-7z-compressed', '.bcpio': 'application/x-bcpio', '.cpio': 'application/x-cpio', '.csh': 'application/x-csh', '.deb': 'application/x-debian-package', '.dvi': 'application/x-dvi', '.gtar': 'application/x-gtar', '.hdf': 'application/x-hdf', '.h5': 'application/x-hdf5', '.latex': 'application/x-latex', '.mif': 'application/x-mif', '.cdf': 'application/x-netcdf', '.nc': 'application/x-netcdf', '.p12': 'application/x-pkcs12', '.php': 'application/x-httpd-php', '.pfx': 'application/x-pkcs12', '.ram': 'application/x-pn-realaudio', '.pyc': 'application/x-python-code', '.pyo': 'application/x-python-code', '.rpm': 'application/x-rpm', '.sh': 'application/x-sh', '.shar': 'application/x-shar', '.swf': 'application/x-shockwave-flash', '.sv4cpio': 'application/x-sv4cpio', '.sv4crc': 'application/x-sv4crc', '.tar': 'application/x-tar', '.tcl': 'application/x-tcl', '.tex': 'application/x-tex', '.texi': 'application/x-texinfo', '.texinfo': 'application/x-texinfo', '.roff': 'application/x-troff', '.t': 'application/x-troff', '.tr': 'application/x-troff', '.man': 'application/x-troff-man', '.me': 'application/x-troff-me', '.ms': 'application/x-troff-ms', '.ustar': 'application/x-ustar', '.src': 'application/x-wais-source', '.xsl': 'application/xml', '.rdf': 'application/xml', '.wsdl': 'application/xml', '.xpdl': 'application/xml', '.yaml': 'application/yaml', '.yml': 'application/yaml', '.zip': 'application/zip', '.3gp': 'audio/3gpp', '.3gpp': 'audio/3gpp', '.3g2': 'audio/3gpp2', '.3gpp2': 'audio/3gpp2', '.aac': 'audio/aac', '.adts': 'audio/aac', '.loas': 'audio/aac', '.ass': 'audio/aac', '.au': 'audio/basic', '.snd': 'audio/basic', '.flac': 'audio/flac', '.mka': 'audio/matroska', '.m4a': 'audio/mp4', '.mp3': 'audio/mpeg', '.mp2': 'audio/mpeg', '.ogg': 'audio/ogg', '.opus': 'audio/opus', '.aif': 'audio/x-aiff', '.aifc': 'audio/x-aiff', '.aiff': 'audio/x-aiff', '.ra': 'audio/x-pn-realaudio', '.wav': 'audio/vnd.wave', '.otf': 'font/otf', '.ttf': 'font/ttf', '.weba': 'audio/webm', '.woff': 'font/woff', '.woff2': 'font/woff2', '.avif': 'image/avif', '.bmp': 'image/bmp', '.emf': 'image/emf', '.fits': 'image/fits', '.g3': 'image/g3fax', '.gif': 'image/gif', '.ief': 'image/ief', '.jp2': 'image/jp2', '.jpg': 'image/jpeg', '.jpe': 'image/jpeg', '.jpeg': 'image/jpeg', '.jpm': 'image/jpm', '.jpx': 'image/jpx', '.heic': 'image/heic', '.heif': 'image/heif', '.png': 'image/png', '.svg': 'image/svg+xml', '.t38': 'image/t38', '.tiff': 'image/tiff', '.tif': 'image/tiff', '.tfx': 'image/tiff-fx', '.ico': 'image/vnd.microsoft.icon', '.webp': 'image/webp', '.wmf': 'image/wmf', '.ras': 'image/x-cmu-raster', '.pnm': 'image/x-portable-anymap', '.pbm': 'image/x-portable-bitmap', '.pgm': 'image/x-portable-graymap', '.ppm': 'image/x-portable-pixmap', '.rgb': 'image/x-rgb', '.xbm': 'image/x-xbitmap', '.xpm': 'image/x-xpixmap', '.xwd': 'image/x-xwindowdump', '.eml': 'message/rfc822', '.mht': 'message/rfc822', '.mhtml': 'message/rfc822', '.nws': 'message/rfc822', '.gltf': 'model/gltf+json', '.glb': 'model/gltf-binary', '.stl': 'model/stl', '.css': 'text/css', '.csv': 'text/csv', '.html': 'text/html', '.htm': 'text/html', '.md': 'text/markdown', '.markdown': 'text/markdown', '.n3': 'text/n3', '.txt': 'text/plain', '.bat': 'text/plain', '.c': 'text/plain', '.h': 'text/plain', '.ksh': 'text/plain', '.pl': 'text/plain', '.srt': 'text/plain', '.rtx': 'text/richtext', '.rtf': 'text/rtf', '.tsv': 'text/tab-separated-values', '.vtt': 'text/vtt', '.py': 'text/x-python', '.rst': 'text/x-rst', '.etx': 'text/x-setext', '.sgm': 'text/x-sgml', '.sgml': 'text/x-sgml', '.vcf': 'text/x-vcard', '.xml': 'text/xml', '.mkv': 'video/matroska', '.mk3d': 'video/matroska-3d', '.mp4': 'video/mp4', '.mpeg': 'video/mpeg', '.m1v': 'video/mpeg', '.mpa': 'video/mpeg', '.mpe': 'video/mpeg', '.mpg': 'video/mpeg', '.ogv': 'video/ogg', '.mov': 'video/quicktime', '.qt': 'video/quicktime', '.webm': 'video/webm', '.avi': 'video/vnd.avi', '.m4v': 'video/x-m4v', '.wmv': 'video/x-ms-wmv', '.movie': 'video/x-sgi-movie'}
    common_types = _common_types_default = {'.rtf': 'application/rtf', '.apk': 'application/vnd.android.package-archive', '.midi': 'audio/midi', '.mid': 'audio/midi', '.jpg': 'image/jpg', '.pict': 'image/pict', '.pct': 'image/pict', '.pic': 'image/pict', '.xul': 'text/xul'}
_default_mime_types()

def _parse_args(args):
    from argparse import ArgumentParser
    parser = ArgumentParser(description='map filename extensions to MIME types', color=True)
    parser.add_argument('-e', '--extension', action='store_true', help='guess extension instead of type')
    parser.add_argument('-l', '--lenient', action='store_true', help='additionally search for common but non-standard types')
    parser.add_argument('type', nargs='+', help='a type to search')
    args = parser.parse_args(args)
    return (args, parser.format_help())

def _main(args=None):
    """Run the mimetypes command-line interface and return a text to print."""
    args, help_text = _parse_args(args)
    results = []
    if args.extension:
        for gtype in args.type:
            guess = 猜扩展名(gtype, not args.lenient)
            if guess:
                results.append(str(guess))
            else:
                results.append(f'error: unknown type {gtype}')
        return results
    else:
        for gtype in args.type:
            guess, encoding = 猜类型(gtype, not args.lenient)
            if guess:
                results.append(f'type: {guess} encoding: {encoding}')
            else:
                results.append(f'error: media type unknown for {gtype}')
        return results
if __name__ == '__main__':
    import sys
    results = _main()
    print('\n'.join(results))
    sys.exit(any((result.startswith('error: ') for result in results)))


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'MimeTypes': 'MIME类型表',
    'add_type': '加类型',
    'guess_all_extensions': '猜所有扩展名',
    'guess_extension': '猜扩展名',
    'guess_file_type': '猜文件类型',
    'guess_type': '猜类型',
    'init': '初始化',
    'read_mime_types': '读类型文件',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'MIME类型表': {
        'add_type': '加类型',
        'guess_all_extensions': '猜所有扩展名',
        'guess_extension': '猜扩展名',
        'guess_file_type': '猜文件类型',
        'guess_type': '猜类型',
        'read_windows_registry': '读Windows注册表',
        'readfp': '从文件对象读',
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
    'MIME类型表': {
        'add_type': '加类型',
        'guess_all_extensions': '猜所有扩展名',
        'guess_extension': '猜扩展名',
        'guess_file_type': '猜文件类型',
        'guess_type': '猜类型',
        'read_windows_registry': '读Windows注册表',
        'readfp': '从文件对象读',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    'MIME类型表',
    '初始化',
    '加类型',
    '猜所有扩展名',
    '猜扩展名',
    '猜文件类型',
    '猜类型',
    '读类型文件',
])

# ---- 转发层结束 ----
