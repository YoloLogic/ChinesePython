# -*- coding: utf-8 -*-
"""信箱 —— 汉语库（由 tools/汉化库.py 从 Lib/mailbox.py 机械生成，**不要手改**）。

英文库 Lib/mailbox.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 信箱
"""


"""Read/write support for Maildir, mbox, MH, Babyl, and MMDF mailboxes."""
_英文原名表 = {'Babyl': 'Babyl信箱', 'BabylMessage': 'Babyl消息', 'Error': '错误', 'ExternalClashError': '外部冲突错误', 'FormatError': '格式错误', 'MH': 'MH信箱', 'MHMessage': 'MH消息', 'MMDF': 'MMDF信箱', 'MMDFMessage': 'MMDF消息', 'Mailbox': '信箱', 'Maildir': '邮件目录', 'MaildirMessage': '邮件目录消息', 'Message': '消息', 'NoSuchMailboxError': '无此信箱错误', 'NotEmptyError': '非空错误', 'mbox': 'mbox信箱', 'mboxMessage': 'mbox消息'}

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
import time
import calendar
import socket
import errno
import copy
import warnings
import email
import email.message
import email.generator
import io
import contextlib
from types import GenericAlias
try:
    import fcntl
except ImportError:
    fcntl = None
__all__ = ['Mailbox', 'Maildir', 'mbox', 'MH', 'Babyl', 'MMDF', 'Message', 'MaildirMessage', 'mboxMessage', 'MHMessage', 'BabylMessage', 'MMDFMessage', 'Error', 'NoSuchMailboxError', 'NotEmptyError', 'ExternalClashError', 'FormatError']
linesep = os.linesep.encode('ascii')

class 信箱:
    """A group of messages in a particular place."""

    def __init__(self, path, factory=None, create=True):
        """Initialize a Mailbox instance."""
        self._path = os.path.abspath(os.path.expanduser(path))
        self._factory = factory

    def add(self, message):
        """Add message and return assigned key."""
        raise NotImplementedError('Method must be implemented by subclass')

    def remove(self, key):
        """Remove the keyed message; raise KeyError if it doesn't exist."""
        raise NotImplementedError('Method must be implemented by subclass')

    def __delitem__(self, key):
        self.remove(key)

    def discard(self, key):
        """If the keyed message exists, remove it."""
        try:
            self.remove(key)
        except KeyError:
            pass

    def __setitem__(self, key, message):
        """Replace the keyed message; raise KeyError if it doesn't exist."""
        raise NotImplementedError('Method must be implemented by subclass')

    def get(self, key, default=None):
        """Return the keyed message, or default if it doesn't exist."""
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __getitem__(self, key):
        """Return the keyed message; raise KeyError if it doesn't exist."""
        if not self._factory:
            return self.取消息(key)
        else:
            with contextlib.closing(self.get_file(key)) as file:
                return self._factory(file)

    def 取消息(self, key):
        """Return a Message representation or raise a KeyError."""
        raise NotImplementedError('Method must be implemented by subclass')

    def 取字符串(self, key):
        """Return a string representation or raise a KeyError.

        Uses email.message.Message to create a 7bit clean string
        representation of the message."""
        return email.message_from_bytes(self.取字节(key)).as_string()

    def 取字节(self, key):
        """Return a byte string representation or raise a KeyError."""
        raise NotImplementedError('Method must be implemented by subclass')

    def get_file(self, key):
        """Return a file-like representation or raise a KeyError."""
        raise NotImplementedError('Method must be implemented by subclass')

    def 迭代键(self):
        """Return an iterator over keys."""
        raise NotImplementedError('Method must be implemented by subclass')

    def keys(self):
        """Return a list of keys."""
        return list(self.迭代键())

    def 迭代值(self):
        """Return an iterator over all messages."""
        for key in self.迭代键():
            try:
                value = self[key]
            except KeyError:
                continue
            yield value

    def __iter__(self):
        return self.迭代值()

    def values(self):
        """Return a list of messages. Memory intensive."""
        return list(self.迭代值())

    def 迭代项(self):
        """Return an iterator over (key, message) tuples."""
        for key in self.迭代键():
            try:
                value = self[key]
            except KeyError:
                continue
            yield (key, value)

    def items(self):
        """Return a list of (key, message) tuples. Memory intensive."""
        return list(self.迭代项())

    def __contains__(self, key):
        """Return True if the keyed message exists, False otherwise."""
        raise NotImplementedError('Method must be implemented by subclass')

    def __len__(self):
        """Return a count of messages in the mailbox."""
        raise NotImplementedError('Method must be implemented by subclass')

    def clear(self):
        """Delete all messages."""
        for key in self.keys():
            self.discard(key)

    def pop(self, key, default=None):
        """Delete the keyed message and return it, or default."""
        try:
            result = self[key]
        except KeyError:
            return default
        self.discard(key)
        return result

    def popitem(self):
        """Delete an arbitrary (key, message) pair and return it."""
        for key in self.迭代键():
            return (key, self.pop(key))
        else:
            raise KeyError('No messages in mailbox')

    def update(self, arg=None):
        """Change the messages that correspond to certain keys."""
        if hasattr(arg, 'iteritems'):
            source = arg.iteritems()
        elif hasattr(arg, 'items'):
            source = arg.items()
        else:
            source = arg
        bad_key = False
        for key, message in source:
            try:
                self[key] = message
            except KeyError:
                bad_key = True
        if bad_key:
            raise KeyError('No message with key(s)')

    def flush(self):
        """Write any pending changes to the disk."""
        raise NotImplementedError('Method must be implemented by subclass')

    def lock(self):
        """Lock the mailbox."""
        raise NotImplementedError('Method must be implemented by subclass')

    def unlock(self):
        """Unlock the mailbox if it is locked."""
        raise NotImplementedError('Method must be implemented by subclass')

    def close(self):
        """Flush and close the mailbox."""
        raise NotImplementedError('Method must be implemented by subclass')

    def _string_to_bytes(self, message):
        try:
            return message.encode('ascii')
        except UnicodeError:
            raise ValueError('String input must be ASCII-only; use bytes or a Message instead')
    _append_newline = False

    def _dump_message(self, message, target, mangle_from_=False):
        """Dump message contents to target file."""
        if isinstance(message, email.message.Message):
            buffer = io.BytesIO()
            gen = email.generator.BytesGenerator(buffer, mangle_from_, 0)
            gen.flatten(message)
            buffer.seek(0)
            data = buffer.read()
            data = data.replace(b'\n', linesep)
            target.write(data)
            if self._append_newline and (not data.endswith(linesep)):
                target.write(linesep)
        elif isinstance(message, (str, bytes, io.StringIO)):
            if isinstance(message, io.StringIO):
                warnings.warn('Use of StringIO input is deprecated, use BytesIO instead', DeprecationWarning, 3)
                message = message.getvalue()
            if isinstance(message, str):
                message = self._string_to_bytes(message)
            if mangle_from_:
                message = message.replace(b'\nFrom ', b'\n>From ')
            message = message.replace(b'\n', linesep)
            target.write(message)
            if self._append_newline and (not message.endswith(linesep)):
                target.write(linesep)
        elif hasattr(message, 'read'):
            if hasattr(message, 'buffer'):
                warnings.warn('Use of text mode files is deprecated, use a binary mode file instead', DeprecationWarning, 3)
                message = message.buffer
            lastline = None
            while True:
                line = message.readline()
                if line.endswith(b'\r\n'):
                    line = line[:-2] + b'\n'
                elif line.endswith(b'\r'):
                    line = line[:-1] + b'\n'
                if not line:
                    break
                if mangle_from_ and line.startswith(b'From '):
                    line = b'>From ' + line[5:]
                line = line.replace(b'\n', linesep)
                target.write(line)
                lastline = line
            if self._append_newline and lastline and (not lastline.endswith(linesep)):
                target.write(linesep)
        else:
            raise TypeError('Invalid message type: %s' % type(message))
    __class_getitem__ = classmethod(GenericAlias)
_装类转发(信箱, {'get_bytes': '取字节', 'get_message': '取消息', 'get_string': '取字符串', 'iteritems': '迭代项', 'iterkeys': '迭代键', 'itervalues': '迭代值'}, {'get_bytes': '取字节', 'get_message': '取消息', 'get_string': '取字符串', 'iteritems': '迭代项', 'iterkeys': '迭代键', 'itervalues': '迭代值'})

class 邮件目录(信箱):
    """A qmail-style Maildir mailbox."""
    colon = ':'

    def __init__(self, dirname, factory=None, create=True):
        """Initialize a Maildir instance."""
        信箱.__init__(self, dirname, factory, create)
        self._paths = {'tmp': os.path.join(self._path, 'tmp'), 'new': os.path.join(self._path, 'new'), 'cur': os.path.join(self._path, 'cur')}
        if not os.path.exists(self._path):
            if create:
                os.mkdir(self._path, 448)
                for path in self._paths.values():
                    os.mkdir(path, 448)
            else:
                raise 无此信箱错误(self._path)
        self._toc = {}
        self._toc_mtimes = {'cur': 0, 'new': 0}
        self._last_read = 0
        self._skewfactor = 0.1

    def add(self, message):
        """Add message and return assigned key."""
        tmp_file = self._create_tmp()
        try:
            self._dump_message(message, tmp_file)
        except BaseException:
            tmp_file.close()
            os.remove(tmp_file.name)
            raise
        _sync_close(tmp_file)
        if isinstance(message, 邮件目录消息):
            subdir = message.get_subdir()
            suffix = self.colon + message.get_info()
            if suffix == self.colon:
                suffix = ''
        else:
            subdir = 'new'
            suffix = ''
        uniq = os.path.basename(tmp_file.name).split(self.colon)[0]
        dest = os.path.join(self._path, subdir, uniq + suffix)
        if isinstance(message, 邮件目录消息):
            os.utime(tmp_file.name, (os.path.getatime(tmp_file.name), message.get_date()))
        try:
            try:
                os.link(tmp_file.name, dest)
            except (AttributeError, PermissionError):
                os.rename(tmp_file.name, dest)
            else:
                os.remove(tmp_file.name)
        except OSError as e:
            os.remove(tmp_file.name)
            if e.errno == errno.EEXIST:
                raise 外部冲突错误('Name clash with existing message: %s' % dest)
            else:
                raise
        return uniq

    def remove(self, key):
        """Remove the keyed message; raise KeyError if it doesn't exist."""
        os.remove(os.path.join(self._path, self._lookup(key)))

    def discard(self, key):
        """If the keyed message exists, remove it."""
        try:
            self.remove(key)
        except (KeyError, FileNotFoundError):
            pass

    def __setitem__(self, key, message):
        """Replace the keyed message; raise KeyError if it doesn't exist."""
        old_subpath = self._lookup(key)
        temp_key = self.add(message)
        temp_subpath = self._lookup(temp_key)
        if isinstance(message, 邮件目录消息):
            dominant_subpath = temp_subpath
        else:
            dominant_subpath = old_subpath
        subdir = os.path.dirname(dominant_subpath)
        if self.colon in dominant_subpath:
            suffix = self.colon + dominant_subpath.split(self.colon)[-1]
        else:
            suffix = ''
        self.discard(key)
        tmp_path = os.path.join(self._path, temp_subpath)
        new_path = os.path.join(self._path, subdir, key + suffix)
        if isinstance(message, 邮件目录消息):
            os.utime(tmp_path, (os.path.getatime(tmp_path), message.get_date()))
        os.rename(tmp_path, new_path)

    def 取消息(self, key):
        """Return a Message representation or raise a KeyError."""
        subpath = self._lookup(key)
        with open(os.path.join(self._path, subpath), 'rb') as f:
            if self._factory:
                msg = self._factory(f)
            else:
                msg = 邮件目录消息(f)
        subdir, name = os.path.split(subpath)
        msg.set_subdir(subdir)
        if self.colon in name:
            msg.set_info(name.split(self.colon)[-1])
        msg.set_date(os.path.getmtime(os.path.join(self._path, subpath)))
        return msg

    def 取字节(self, key):
        """Return a bytes representation or raise a KeyError."""
        with open(os.path.join(self._path, self._lookup(key)), 'rb') as f:
            return f.read().replace(linesep, b'\n')

    def get_file(self, key):
        """Return a file-like representation or raise a KeyError."""
        f = open(os.path.join(self._path, self._lookup(key)), 'rb')
        return _ProxyFile(f)

    def 取信息(self, key):
        """Get the keyed message's "info" as a string."""
        subpath = self._lookup(key)
        if self.colon in subpath:
            return subpath.split(self.colon)[-1]
        return ''

    def 设信息(self, key, info: str):
        """Set the keyed message's "info" string."""
        if not isinstance(info, str):
            raise TypeError(f'info must be a string: {type(info)}')
        old_subpath = self._lookup(key)
        new_subpath = old_subpath.split(self.colon)[0]
        if info:
            new_subpath += self.colon + info
        if new_subpath == old_subpath:
            return
        old_path = os.path.join(self._path, old_subpath)
        new_path = os.path.join(self._path, new_subpath)
        os.rename(old_path, new_path)
        self._toc[key] = new_subpath

    def 取标志(self, key):
        """Return as a string the standard flags that are set on the keyed message."""
        info = self.取信息(key)
        if info.startswith('2,'):
            return info[2:]
        return ''

    def 设标志(self, key, flags: str):
        """Set the given flags and unset all others on the keyed message."""
        if not isinstance(flags, str):
            raise TypeError(f'flags must be a string: {type(flags)}')
        self.设信息(key, '2,' + ''.join(sorted(set(flags))))

    def 加标志(self, key, flag: str):
        """Set the given flag(s) without changing others on the keyed message."""
        if not isinstance(flag, str):
            raise TypeError(f'flag must be a string: {type(flag)}')
        self.设标志(key, ''.join(set(self.取标志(key)) | set(flag)))

    def 去标志(self, key, flag: str):
        """Unset the given string flag(s) without changing others on the keyed message."""
        if not isinstance(flag, str):
            raise TypeError(f'flag must be a string: {type(flag)}')
        if self.取标志(key):
            self.设标志(key, ''.join(set(self.取标志(key)) - set(flag)))

    def 迭代键(self):
        """Return an iterator over keys."""
        self._refresh()
        for key in self._toc:
            try:
                self._lookup(key)
            except KeyError:
                continue
            yield key

    def __contains__(self, key):
        """Return True if the keyed message exists, False otherwise."""
        self._refresh()
        return key in self._toc

    def __len__(self):
        """Return a count of messages in the mailbox."""
        self._refresh()
        return len(self._toc)

    def flush(self):
        """Write any pending changes to disk."""
        pass

    def lock(self):
        """Lock the mailbox."""
        return

    def unlock(self):
        """Unlock the mailbox if it is locked."""
        return

    def close(self):
        """Flush and close the mailbox."""
        return

    def 列出文件夹(self):
        """Return a list of folder names."""
        result = []
        for entry in os.listdir(self._path):
            if len(entry) > 1 and entry[0] == '.' and os.path.isdir(os.path.join(self._path, entry)):
                result.append(entry[1:])
        return result

    def 取文件夹(self, folder):
        """Return a Maildir instance for the named folder."""
        return 邮件目录(os.path.join(self._path, '.' + folder), factory=self._factory, create=False)

    def 加文件夹(self, folder):
        """Create a folder and return a Maildir instance representing it."""
        path = os.path.join(self._path, '.' + folder)
        result = 邮件目录(path, factory=self._factory)
        maildirfolder_path = os.path.join(path, 'maildirfolder')
        if not os.path.exists(maildirfolder_path):
            os.close(os.open(maildirfolder_path, os.O_CREAT | os.O_WRONLY, 438))
        return result

    def 去文件夹(self, folder):
        """Delete the named folder, which must be empty."""
        path = os.path.join(self._path, '.' + folder)
        for entry in os.listdir(os.path.join(path, 'new')) + os.listdir(os.path.join(path, 'cur')):
            if len(entry) < 1 or entry[0] != '.':
                raise 非空错误('Folder contains message(s): %s' % folder)
        for entry in os.listdir(path):
            if entry != 'new' and entry != 'cur' and (entry != 'tmp') and os.path.isdir(os.path.join(path, entry)):
                raise 非空错误("Folder contains subdirectory '%s': %s" % (folder, entry))
        for root, dirs, files in os.walk(path, topdown=False):
            for entry in files:
                os.remove(os.path.join(root, entry))
            for entry in dirs:
                os.rmdir(os.path.join(root, entry))
        os.rmdir(path)

    def 清理(self):
        """Delete old files in "tmp"."""
        now = time.time()
        for entry in os.listdir(os.path.join(self._path, 'tmp')):
            path = os.path.join(self._path, 'tmp', entry)
            if now - os.path.getatime(path) > 129600:
                os.remove(path)
    _count = 1

    def _create_tmp(self):
        """Create a file in the tmp subdirectory and open and return it."""
        now = time.time()
        hostname = socket.gethostname()
        if '/' in hostname:
            hostname = hostname.replace('/', '\\057')
        if ':' in hostname:
            hostname = hostname.replace(':', '\\072')
        uniq = '%s.M%sP%sQ%s.%s' % (int(now), int(now % 1 * 1000000.0), os.getpid(), 邮件目录._count, hostname)
        path = os.path.join(self._path, 'tmp', uniq)
        try:
            os.stat(path)
        except FileNotFoundError:
            邮件目录._count += 1
            try:
                return _create_carefully(path)
            except FileExistsError:
                pass
        raise 外部冲突错误('Name clash prevented file creation: %s' % path)

    def _refresh(self):
        """Update table of contents mapping."""
        if time.time() - self._last_read > 2 + self._skewfactor:
            refresh = False
            for subdir in self._toc_mtimes:
                mtime = os.path.getmtime(self._paths[subdir])
                if mtime > self._toc_mtimes[subdir]:
                    refresh = True
                self._toc_mtimes[subdir] = mtime
            if not refresh:
                return
        self._toc = {}
        for subdir in self._toc_mtimes:
            path = self._paths[subdir]
            for entry in os.listdir(path):
                if entry.startswith('.'):
                    continue
                p = os.path.join(path, entry)
                if os.path.isdir(p):
                    continue
                uniq = entry.split(self.colon)[0]
                self._toc[uniq] = os.path.join(subdir, entry)
        self._last_read = time.time()

    def _lookup(self, key):
        """Use TOC to return subpath for given key, or raise a KeyError."""
        try:
            if os.path.exists(os.path.join(self._path, self._toc[key])):
                return self._toc[key]
        except KeyError:
            pass
        self._refresh()
        try:
            return self._toc[key]
        except KeyError:
            raise KeyError('No message with key: %s' % key) from None

    def next(self):
        """Return the next message in a one-time iteration."""
        if not hasattr(self, '_onetime_keys'):
            self._onetime_keys = self.迭代键()
        while True:
            try:
                return self[next(self._onetime_keys)]
            except StopIteration:
                return None
            except KeyError:
                continue
_装类转发(邮件目录, {'add_flag': '加标志', 'add_folder': '加文件夹', 'clean': '清理', 'get_bytes': '取字节', 'get_flags': '取标志', 'get_folder': '取文件夹', 'get_info': '取信息', 'get_message': '取消息', 'iterkeys': '迭代键', 'list_folders': '列出文件夹', 'remove_flag': '去标志', 'remove_folder': '去文件夹', 'set_flags': '设标志', 'set_info': '设信息'}, {'add_flag': '加标志', 'add_folder': '加文件夹', 'clean': '清理', 'get_bytes': '取字节', 'get_flags': '取标志', 'get_folder': '取文件夹', 'get_info': '取信息', 'get_message': '取消息', 'iterkeys': '迭代键', 'list_folders': '列出文件夹', 'remove_flag': '去标志', 'remove_folder': '去文件夹', 'set_flags': '设标志', 'set_info': '设信息'})

class _singlefileMailbox(信箱):
    """A single-file mailbox."""

    def __init__(self, path, factory=None, create=True):
        """Initialize a single-file mailbox."""
        信箱.__init__(self, path, factory, create)
        try:
            f = open(self._path, 'rb+')
        except OSError as e:
            if e.errno == errno.ENOENT:
                if create:
                    f = open(self._path, 'wb+')
                else:
                    raise 无此信箱错误(self._path)
            elif e.errno in (errno.EACCES, errno.EROFS):
                f = open(self._path, 'rb')
            else:
                raise
        self._file = f
        self._toc = None
        self._next_key = 0
        self._pending = False
        self._pending_sync = False
        self._locked = False
        self._file_length = None

    def add(self, message):
        """Add message and return assigned key."""
        self._lookup()
        self._toc[self._next_key] = self._append_message(message)
        self._next_key += 1
        self._pending_sync = True
        return self._next_key - 1

    def remove(self, key):
        """Remove the keyed message; raise KeyError if it doesn't exist."""
        self._lookup(key)
        del self._toc[key]
        self._pending = True

    def __setitem__(self, key, message):
        """Replace the keyed message; raise KeyError if it doesn't exist."""
        self._lookup(key)
        self._toc[key] = self._append_message(message)
        self._pending = True

    def 迭代键(self):
        """Return an iterator over keys."""
        self._lookup()
        yield from self._toc.keys()

    def __contains__(self, key):
        """Return True if the keyed message exists, False otherwise."""
        self._lookup()
        return key in self._toc

    def __len__(self):
        """Return a count of messages in the mailbox."""
        self._lookup()
        return len(self._toc)

    def lock(self):
        """Lock the mailbox."""
        if not self._locked:
            _lock_file(self._file)
            self._locked = True

    def unlock(self):
        """Unlock the mailbox if it is locked."""
        if self._locked:
            _unlock_file(self._file)
            self._locked = False

    def flush(self):
        """Write any pending changes to disk."""
        if not self._pending:
            if self._pending_sync:
                _sync_flush(self._file)
                self._pending_sync = False
            return
        assert self._toc is not None
        self._file.seek(0, 2)
        cur_len = self._file.tell()
        if cur_len != self._file_length:
            raise 外部冲突错误('Size of mailbox file changed (expected %i, found %i)' % (self._file_length, cur_len))
        new_file = _create_temporary(self._path)
        try:
            new_toc = {}
            self._pre_mailbox_hook(new_file)
            for key in sorted(self._toc.keys()):
                start, stop = self._toc[key]
                self._file.seek(start)
                self._pre_message_hook(new_file)
                new_start = new_file.tell()
                while True:
                    buffer = self._file.read(min(4096, stop - self._file.tell()))
                    if not buffer:
                        break
                    new_file.write(buffer)
                new_toc[key] = (new_start, new_file.tell())
                self._post_message_hook(new_file)
            self._file_length = new_file.tell()
        except:
            new_file.close()
            os.remove(new_file.name)
            raise
        _sync_close(new_file)
        self._file.close()
        info = os.stat(self._path)
        os.chmod(new_file.name, info.st_mode)
        try:
            os.chown(new_file.name, info.st_uid, info.st_gid)
        except (AttributeError, OSError):
            pass
        try:
            os.rename(new_file.name, self._path)
        except FileExistsError:
            os.remove(self._path)
            os.rename(new_file.name, self._path)
        self._file = open(self._path, 'rb+')
        self._toc = new_toc
        self._pending = False
        self._pending_sync = False
        if self._locked:
            _lock_file(self._file, dotlock=False)

    def _pre_mailbox_hook(self, f):
        """Called before writing the mailbox to file f."""
        return

    def _pre_message_hook(self, f):
        """Called before writing each message to file f."""
        return

    def _post_message_hook(self, f):
        """Called after writing each message to file f."""
        return

    def close(self):
        """Flush and close the mailbox."""
        try:
            self.flush()
        finally:
            try:
                if self._locked:
                    self.unlock()
            finally:
                self._file.close()

    def _lookup(self, key=None):
        """Return (start, stop) or raise KeyError."""
        if self._toc is None:
            self._generate_toc()
        if key is not None:
            try:
                return self._toc[key]
            except KeyError:
                raise KeyError('No message with key: %s' % key) from None

    def _append_message(self, message):
        """Append message to mailbox and return (start, stop) offsets."""
        self._file.seek(0, 2)
        before = self._file.tell()
        if len(self._toc) == 0 and (not self._pending):
            self._pre_mailbox_hook(self._file)
        try:
            self._pre_message_hook(self._file)
            offsets = self._install_message(message)
            self._post_message_hook(self._file)
        except BaseException:
            self._file.truncate(before)
            raise
        self._file.flush()
        self._file_length = self._file.tell()
        return offsets
_装类转发(_singlefileMailbox, {'iterkeys': '迭代键'}, {'iterkeys': '迭代键'})

class _mboxMMDF(_singlefileMailbox):
    """An mbox or MMDF mailbox."""
    _mangle_from_ = True

    def 取消息(self, key):
        """Return a Message representation or raise a KeyError."""
        start, stop = self._lookup(key)
        self._file.seek(start)
        from_line = self._file.readline().replace(linesep, b'').decode('ascii')
        string = self._file.read(stop - self._file.tell())
        msg = self._message_factory(string.replace(linesep, b'\n'))
        msg.set_unixfrom(from_line)
        msg.set_from(from_line[5:])
        return msg

    def 取字符串(self, key, from_=False):
        """Return a string representation or raise a KeyError."""
        return email.message_from_bytes(self.取字节(key, from_)).as_string(unixfrom=from_)

    def 取字节(self, key, from_=False):
        """Return a string representation or raise a KeyError."""
        start, stop = self._lookup(key)
        self._file.seek(start)
        if not from_:
            self._file.readline()
        string = self._file.read(stop - self._file.tell())
        return string.replace(linesep, b'\n')

    def get_file(self, key, from_=False):
        """Return a file-like representation or raise a KeyError."""
        start, stop = self._lookup(key)
        self._file.seek(start)
        if not from_:
            self._file.readline()
        return _PartialFile(self._file, self._file.tell(), stop)

    def _install_message(self, message):
        """Format a message and blindly write to self._file."""
        from_line = None
        if isinstance(message, str):
            message = self._string_to_bytes(message)
        if isinstance(message, bytes) and message.startswith(b'From '):
            newline = message.find(b'\n')
            if newline != -1:
                from_line = message[:newline]
                message = message[newline + 1:]
            else:
                from_line = message
                message = b''
        elif isinstance(message, _mboxMMDFMessage):
            author = message.get_from().encode('ascii')
            from_line = b'From ' + author
        elif isinstance(message, email.message.Message):
            from_line = message.get_unixfrom()
            if from_line is not None:
                from_line = from_line.encode('ascii')
        if from_line is None:
            from_line = b'From MAILER-DAEMON ' + time.asctime(time.gmtime()).encode()
        start = self._file.tell()
        self._file.write(from_line + linesep)
        self._dump_message(message, self._file, self._mangle_from_)
        stop = self._file.tell()
        return (start, stop)
_装类转发(_mboxMMDF, {'get_bytes': '取字节', 'get_message': '取消息', 'get_string': '取字符串'}, {'get_bytes': '取字节', 'get_message': '取消息', 'get_string': '取字符串'})

class mbox信箱(_mboxMMDF):
    """A classic mbox mailbox."""
    _mangle_from_ = True
    _append_newline = True

    def __init__(self, path, factory=None, create=True):
        """Initialize an mbox mailbox."""
        self._message_factory = mbox消息
        _mboxMMDF.__init__(self, path, factory, create)

    def _post_message_hook(self, f):
        """Called after writing each message to file f."""
        f.write(linesep)

    def _generate_toc(self):
        """Generate key-to-(start, stop) table of contents."""
        starts, stops = ([], [])
        last_was_empty = False
        self._file.seek(0)
        while True:
            line_pos = self._file.tell()
            line = self._file.readline()
            if line.startswith(b'From '):
                if len(stops) < len(starts):
                    if last_was_empty:
                        stops.append(line_pos - len(linesep))
                    else:
                        stops.append(line_pos)
                starts.append(line_pos)
                last_was_empty = False
            elif not line:
                if last_was_empty:
                    stops.append(line_pos - len(linesep))
                else:
                    stops.append(line_pos)
                break
            elif line == linesep:
                last_was_empty = True
            else:
                last_was_empty = False
        self._toc = dict(enumerate(zip(starts, stops)))
        self._next_key = len(self._toc)
        self._file_length = self._file.tell()

class MMDF信箱(_mboxMMDF):
    """An MMDF mailbox."""

    def __init__(self, path, factory=None, create=True):
        """Initialize an MMDF mailbox."""
        self._message_factory = MMDF消息
        _mboxMMDF.__init__(self, path, factory, create)

    def _pre_message_hook(self, f):
        """Called before writing each message to file f."""
        f.write(b'\x01\x01\x01\x01' + linesep)

    def _post_message_hook(self, f):
        """Called after writing each message to file f."""
        f.write(linesep + b'\x01\x01\x01\x01' + linesep)

    def _generate_toc(self):
        """Generate key-to-(start, stop) table of contents."""
        starts, stops = ([], [])
        self._file.seek(0)
        next_pos = 0
        while True:
            line_pos = next_pos
            line = self._file.readline()
            next_pos = self._file.tell()
            if line.startswith(b'\x01\x01\x01\x01' + linesep):
                starts.append(next_pos)
                while True:
                    line_pos = next_pos
                    line = self._file.readline()
                    next_pos = self._file.tell()
                    if line == b'\x01\x01\x01\x01' + linesep:
                        stops.append(line_pos - len(linesep))
                        break
                    elif not line:
                        stops.append(line_pos)
                        break
            elif not line:
                break
        self._toc = dict(enumerate(zip(starts, stops)))
        self._next_key = len(self._toc)
        self._file.seek(0, 2)
        self._file_length = self._file.tell()

class MH信箱(信箱):
    """An MH mailbox."""

    def __init__(self, path, factory=None, create=True):
        """Initialize an MH instance."""
        信箱.__init__(self, path, factory, create)
        if not os.path.exists(self._path):
            if create:
                os.mkdir(self._path, 448)
                os.close(os.open(os.path.join(self._path, '.mh_sequences'), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 384))
            else:
                raise 无此信箱错误(self._path)
        self._locked = False

    def add(self, message):
        """Add message and return assigned key."""
        keys = self.keys()
        if len(keys) == 0:
            new_key = 1
        else:
            new_key = max(keys) + 1
        new_path = os.path.join(self._path, str(new_key))
        f = _create_carefully(new_path)
        closed = False
        try:
            if self._locked:
                _lock_file(f)
            try:
                try:
                    self._dump_message(message, f)
                except BaseException:
                    if self._locked:
                        _unlock_file(f)
                    _sync_close(f)
                    closed = True
                    os.remove(new_path)
                    raise
                if isinstance(message, MH消息):
                    self._dump_sequences(message, new_key)
            finally:
                if self._locked:
                    _unlock_file(f)
        finally:
            if not closed:
                _sync_close(f)
        return new_key

    def remove(self, key):
        """Remove the keyed message; raise KeyError if it doesn't exist."""
        path = os.path.join(self._path, str(key))
        try:
            f = open(path, 'rb+')
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise KeyError('No message with key: %s' % key)
            else:
                raise
        else:
            f.close()
            os.remove(path)

    def __setitem__(self, key, message):
        """Replace the keyed message; raise KeyError if it doesn't exist."""
        path = os.path.join(self._path, str(key))
        try:
            f = open(path, 'rb+')
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise KeyError('No message with key: %s' % key)
            else:
                raise
        try:
            if self._locked:
                _lock_file(f)
            try:
                os.close(os.open(path, os.O_WRONLY | os.O_TRUNC))
                self._dump_message(message, f)
                if isinstance(message, MH消息):
                    self._dump_sequences(message, key)
            finally:
                if self._locked:
                    _unlock_file(f)
        finally:
            _sync_close(f)

    def 取消息(self, key):
        """Return a Message representation or raise a KeyError."""
        try:
            if self._locked:
                f = open(os.path.join(self._path, str(key)), 'rb+')
            else:
                f = open(os.path.join(self._path, str(key)), 'rb')
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise KeyError('No message with key: %s' % key)
            else:
                raise
        with f:
            if self._locked:
                _lock_file(f)
            try:
                msg = MH消息(f)
            finally:
                if self._locked:
                    _unlock_file(f)
        for name, key_list in self.取序列().items():
            if key in key_list:
                msg.add_sequence(name)
        return msg

    def 取字节(self, key):
        """Return a bytes representation or raise a KeyError."""
        try:
            if self._locked:
                f = open(os.path.join(self._path, str(key)), 'rb+')
            else:
                f = open(os.path.join(self._path, str(key)), 'rb')
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise KeyError('No message with key: %s' % key)
            else:
                raise
        with f:
            if self._locked:
                _lock_file(f)
            try:
                return f.read().replace(linesep, b'\n')
            finally:
                if self._locked:
                    _unlock_file(f)

    def get_file(self, key):
        """Return a file-like representation or raise a KeyError."""
        try:
            f = open(os.path.join(self._path, str(key)), 'rb')
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise KeyError('No message with key: %s' % key)
            else:
                raise
        return _ProxyFile(f)

    def 迭代键(self):
        """Return an iterator over keys."""
        return iter(sorted((int(entry) for entry in os.listdir(self._path) if entry.isdigit())))

    def __contains__(self, key):
        """Return True if the keyed message exists, False otherwise."""
        return os.path.exists(os.path.join(self._path, str(key)))

    def __len__(self):
        """Return a count of messages in the mailbox."""
        return len(list(self.迭代键()))

    def _open_mh_sequences_file(self, text):
        mode = '' if text else 'b'
        kwargs = {'encoding': 'ASCII'} if text else {}
        path = os.path.join(self._path, '.mh_sequences')
        while True:
            try:
                return open(path, 'r+' + mode, **kwargs)
            except FileNotFoundError:
                pass
            try:
                return open(path, 'x+' + mode, **kwargs)
            except FileExistsError:
                pass

    def lock(self):
        """Lock the mailbox."""
        if not self._locked:
            self._file = self._open_mh_sequences_file(text=False)
            _lock_file(self._file)
            self._locked = True

    def unlock(self):
        """Unlock the mailbox if it is locked."""
        if self._locked:
            _unlock_file(self._file)
            _sync_close(self._file)
            del self._file
            self._locked = False

    def flush(self):
        """Write any pending changes to the disk."""
        return

    def close(self):
        """Flush and close the mailbox."""
        if self._locked:
            self.unlock()

    def 列出文件夹(self):
        """Return a list of folder names."""
        result = []
        for entry in os.listdir(self._path):
            if os.path.isdir(os.path.join(self._path, entry)):
                result.append(entry)
        return result

    def 取文件夹(self, folder):
        """Return an MH instance for the named folder."""
        return MH信箱(os.path.join(self._path, folder), factory=self._factory, create=False)

    def 加文件夹(self, folder):
        """Create a folder and return an MH instance representing it."""
        return MH信箱(os.path.join(self._path, folder), factory=self._factory)

    def 去文件夹(self, folder):
        """Delete the named folder, which must be empty."""
        path = os.path.join(self._path, folder)
        entries = os.listdir(path)
        if entries == ['.mh_sequences']:
            os.remove(os.path.join(path, '.mh_sequences'))
        elif entries == []:
            pass
        else:
            raise 非空错误('Folder not empty: %s' % self._path)
        os.rmdir(path)

    def 取序列(self):
        """Return a name-to-key-list dictionary to define each sequence."""
        results = {}
        try:
            f = open(os.path.join(self._path, '.mh_sequences'), 'r', encoding='ASCII')
        except FileNotFoundError:
            return results
        with f:
            all_keys = set(self.keys())
            for line in f:
                try:
                    name, contents = line.split(':')
                    keys = set()
                    for spec in contents.split():
                        if spec.isdigit():
                            keys.add(int(spec))
                        else:
                            start, stop = (int(x) for x in spec.split('-'))
                            keys.update(range(start, stop + 1))
                    results[name] = [key for key in sorted(keys) if key in all_keys]
                    if len(results[name]) == 0:
                        del results[name]
                except ValueError:
                    raise 格式错误('Invalid sequence specification: %s' % line.rstrip())
        return results

    def 设序列(self, sequences):
        """Set sequences using the given name-to-key-list dictionary."""
        f = self._open_mh_sequences_file(text=True)
        try:
            os.close(os.open(f.name, os.O_WRONLY | os.O_TRUNC))
            for name, keys in sequences.items():
                if len(keys) == 0:
                    continue
                f.write(name + ':')
                prev = None
                completing = False
                for key in sorted(set(keys)):
                    if key - 1 == prev:
                        if not completing:
                            completing = True
                            f.write('-')
                    elif completing:
                        completing = False
                        f.write('%s %s' % (prev, key))
                    else:
                        f.write(' %s' % key)
                    prev = key
                if completing:
                    f.write(str(prev) + '\n')
                else:
                    f.write('\n')
        finally:
            _sync_close(f)

    def pack(self):
        """Re-name messages to eliminate numbering gaps. Invalidates keys."""
        sequences = self.取序列()
        prev = 0
        changes = []
        for key in self.迭代键():
            if key - 1 != prev:
                changes.append((key, prev + 1))
                try:
                    os.link(os.path.join(self._path, str(key)), os.path.join(self._path, str(prev + 1)))
                except (AttributeError, PermissionError):
                    os.rename(os.path.join(self._path, str(key)), os.path.join(self._path, str(prev + 1)))
                else:
                    os.unlink(os.path.join(self._path, str(key)))
            prev += 1
        self._next_key = prev + 1
        if len(changes) == 0:
            return
        for name, key_list in sequences.items():
            for old, new in changes:
                if old in key_list:
                    key_list[key_list.index(old)] = new
        self.设序列(sequences)

    def _dump_sequences(self, message, key):
        """Inspect a new MHMessage and update sequences appropriately."""
        pending_sequences = message.get_sequences()
        all_sequences = self.取序列()
        for name, key_list in all_sequences.items():
            if name in pending_sequences:
                key_list.append(key)
            elif key in key_list:
                del key_list[key_list.index(key)]
        for sequence in pending_sequences:
            if sequence not in all_sequences:
                all_sequences[sequence] = [key]
        self.设序列(all_sequences)
_装类转发(MH信箱, {'add_folder': '加文件夹', 'get_bytes': '取字节', 'get_folder': '取文件夹', 'get_message': '取消息', 'get_sequences': '取序列', 'iterkeys': '迭代键', 'list_folders': '列出文件夹', 'remove_folder': '去文件夹', 'set_sequences': '设序列'}, {'add_folder': '加文件夹', 'get_bytes': '取字节', 'get_folder': '取文件夹', 'get_message': '取消息', 'get_sequences': '取序列', 'iterkeys': '迭代键', 'list_folders': '列出文件夹', 'remove_folder': '去文件夹', 'set_sequences': '设序列'})

class Babyl信箱(_singlefileMailbox):
    """An Rmail-style Babyl mailbox."""
    _special_labels = frozenset({'unseen', 'deleted', 'filed', 'answered', 'forwarded', 'edited', 'resent'})

    def __init__(self, path, factory=None, create=True):
        """Initialize a Babyl mailbox."""
        _singlefileMailbox.__init__(self, path, factory, create)
        self._labels = {}

    def add(self, message):
        """Add message and return assigned key."""
        key = _singlefileMailbox.add(self, message)
        if isinstance(message, Babyl消息):
            self._labels[key] = message.get_labels()
        return key

    def remove(self, key):
        """Remove the keyed message; raise KeyError if it doesn't exist."""
        _singlefileMailbox.remove(self, key)
        if key in self._labels:
            del self._labels[key]

    def __setitem__(self, key, message):
        """Replace the keyed message; raise KeyError if it doesn't exist."""
        _singlefileMailbox.__setitem__(self, key, message)
        if isinstance(message, Babyl消息):
            self._labels[key] = message.get_labels()

    def 取消息(self, key):
        """Return a Message representation or raise a KeyError."""
        start, stop = self._lookup(key)
        self._file.seek(start)
        self._file.readline()
        original_headers = io.BytesIO()
        while True:
            line = self._file.readline()
            if line == b'*** EOOH ***' + linesep or not line:
                break
            original_headers.write(line.replace(linesep, b'\n'))
        visible_headers = io.BytesIO()
        while True:
            line = self._file.readline()
            if line == linesep or not line:
                break
            visible_headers.write(line.replace(linesep, b'\n'))
        n = stop - self._file.tell()
        assert n >= 0
        body = self._file.read(n)
        body = body.replace(linesep, b'\n')
        msg = Babyl消息(original_headers.getvalue() + body)
        msg.set_visible(visible_headers.getvalue())
        if key in self._labels:
            msg.set_labels(self._labels[key])
        return msg

    def 取字节(self, key):
        """Return a string representation or raise a KeyError."""
        start, stop = self._lookup(key)
        self._file.seek(start)
        self._file.readline()
        original_headers = io.BytesIO()
        while True:
            line = self._file.readline()
            if line == b'*** EOOH ***' + linesep or not line:
                break
            original_headers.write(line.replace(linesep, b'\n'))
        while True:
            line = self._file.readline()
            if line == linesep or not line:
                break
        headers = original_headers.getvalue()
        n = stop - self._file.tell()
        assert n >= 0
        data = self._file.read(n)
        data = data.replace(linesep, b'\n')
        return headers + data

    def get_file(self, key):
        """Return a file-like representation or raise a KeyError."""
        return io.BytesIO(self.取字节(key).replace(b'\n', linesep))

    def get_labels(self):
        """Return a list of user-defined labels in the mailbox."""
        self._lookup()
        labels = set()
        for label_list in self._labels.values():
            labels.update(label_list)
        labels.difference_update(self._special_labels)
        return list(labels)

    def _generate_toc(self):
        """Generate key-to-(start, stop) table of contents."""
        starts, stops = ([], [])
        self._file.seek(0)
        next_pos = 0
        label_lists = []
        while True:
            line_pos = next_pos
            line = self._file.readline()
            next_pos = self._file.tell()
            if line == b'\x1f\x0c' + linesep:
                if len(stops) < len(starts):
                    stops.append(line_pos - len(linesep))
                starts.append(next_pos)
                labels = [label.strip() for label in self._file.readline()[1:].split(b',') if label.strip()]
                label_lists.append(labels)
            elif line == b'\x1f' or line == b'\x1f' + linesep:
                if len(stops) < len(starts):
                    stops.append(line_pos - len(linesep))
            elif not line:
                stops.append(line_pos - len(linesep))
                break
        self._toc = dict(enumerate(zip(starts, stops)))
        self._labels = dict(enumerate(label_lists))
        self._next_key = len(self._toc)
        self._file.seek(0, 2)
        self._file_length = self._file.tell()

    def _pre_mailbox_hook(self, f):
        """Called before writing the mailbox to file f."""
        babyl = b'BABYL OPTIONS:' + linesep
        babyl += b'Version: 5' + linesep
        labels = self.get_labels()
        labels = (label.encode() for label in labels)
        babyl += b'Labels:' + b','.join(labels) + linesep
        babyl += b'\x1f'
        f.write(babyl)

    def _pre_message_hook(self, f):
        """Called before writing each message to file f."""
        f.write(b'\x0c' + linesep)

    def _post_message_hook(self, f):
        """Called after writing each message to file f."""
        f.write(linesep + b'\x1f')

    def _install_message(self, message):
        """Write message contents and return (start, stop)."""
        start = self._file.tell()
        if isinstance(message, Babyl消息):
            special_labels = []
            labels = []
            for label in message.get_labels():
                if label in self._special_labels:
                    special_labels.append(label)
                else:
                    labels.append(label)
            self._file.write(b'1')
            for label in special_labels:
                self._file.write(b', ' + label.encode())
            self._file.write(b',,')
            for label in labels:
                self._file.write(b' ' + label.encode() + b',')
            self._file.write(linesep)
        else:
            self._file.write(b'1,,' + linesep)
        if isinstance(message, email.message.Message):
            orig_buffer = io.BytesIO()
            orig_generator = email.generator.BytesGenerator(orig_buffer, False, 0)
            orig_generator.flatten(message)
            orig_buffer.seek(0)
            while True:
                line = orig_buffer.readline()
                self._file.write(line.replace(b'\n', linesep))
                if line == b'\n' or not line:
                    break
            self._file.write(b'*** EOOH ***' + linesep)
            if isinstance(message, Babyl消息):
                vis_buffer = io.BytesIO()
                vis_generator = email.generator.BytesGenerator(vis_buffer, False, 0)
                vis_generator.flatten(message.get_visible())
                while True:
                    line = vis_buffer.readline()
                    self._file.write(line.replace(b'\n', linesep))
                    if line == b'\n' or not line:
                        break
            else:
                orig_buffer.seek(0)
                while True:
                    line = orig_buffer.readline()
                    self._file.write(line.replace(b'\n', linesep))
                    if line == b'\n' or not line:
                        break
            while True:
                buffer = orig_buffer.read(4096)
                if not buffer:
                    break
                self._file.write(buffer.replace(b'\n', linesep))
        elif isinstance(message, (bytes, str, io.StringIO)):
            if isinstance(message, io.StringIO):
                warnings.warn('Use of StringIO input is deprecated, use BytesIO instead', DeprecationWarning, 3)
                message = message.getvalue()
            if isinstance(message, str):
                message = self._string_to_bytes(message)
            body_start = message.find(b'\n\n') + 2
            if body_start - 2 != -1:
                self._file.write(message[:body_start].replace(b'\n', linesep))
                self._file.write(b'*** EOOH ***' + linesep)
                self._file.write(message[:body_start].replace(b'\n', linesep))
                self._file.write(message[body_start:].replace(b'\n', linesep))
            else:
                self._file.write(b'*** EOOH ***' + linesep + linesep)
                self._file.write(message.replace(b'\n', linesep))
        elif hasattr(message, 'readline'):
            if hasattr(message, 'buffer'):
                warnings.warn('Use of text mode files is deprecated, use a binary mode file instead', DeprecationWarning, 3)
                message = message.buffer
            original_pos = message.tell()
            first_pass = True
            while True:
                line = message.readline()
                if line.endswith(b'\r\n'):
                    line = line[:-2] + b'\n'
                elif line.endswith(b'\r'):
                    line = line[:-1] + b'\n'
                self._file.write(line.replace(b'\n', linesep))
                if line == b'\n' or not line:
                    if first_pass:
                        first_pass = False
                        self._file.write(b'*** EOOH ***' + linesep)
                        message.seek(original_pos)
                    else:
                        break
            while True:
                line = message.readline()
                if not line:
                    break
                if line.endswith(b'\r\n'):
                    line = line[:-2] + linesep
                elif line.endswith(b'\r'):
                    line = line[:-1] + linesep
                elif line.endswith(b'\n'):
                    line = line[:-1] + linesep
                self._file.write(line)
        else:
            raise TypeError('Invalid message type: %s' % type(message))
        stop = self._file.tell()
        return (start, stop)
_装类转发(Babyl信箱, {'get_bytes': '取字节', 'get_message': '取消息'}, {'get_bytes': '取字节', 'get_message': '取消息'})

class 消息(email.message.Message):
    """Message with mailbox-format-specific properties."""

    def __init__(self, message=None):
        """Initialize a Message instance."""
        if isinstance(message, email.message.Message):
            self._become_message(copy.deepcopy(message))
            if isinstance(message, 消息):
                message._explain_to(self)
        elif isinstance(message, bytes):
            self._become_message(email.message_from_bytes(message))
        elif isinstance(message, str):
            self._become_message(email.message_from_string(message))
        elif isinstance(message, io.TextIOWrapper):
            self._become_message(email.message_from_file(message))
        elif hasattr(message, 'read'):
            self._become_message(email.message_from_binary_file(message))
        elif message is None:
            email.message.Message.__init__(self)
        else:
            raise TypeError('Invalid message type: %s' % type(message))

    def _become_message(self, message):
        """Assume the non-format-specific state of message."""
        type_specific = getattr(message, '_type_specific_attributes', [])
        for name in message.__dict__:
            if name not in type_specific:
                self.__dict__[name] = message.__dict__[name]

    def _explain_to(self, message):
        """Copy format-specific state to message insofar as possible."""
        if isinstance(message, 消息):
            return
        else:
            raise TypeError('Cannot convert to specified type')

class 邮件目录消息(消息):
    """Message with Maildir-specific properties."""
    _type_specific_attributes = ['_subdir', '_info', '_date']

    def __init__(self, message=None):
        """Initialize a MaildirMessage instance."""
        self._subdir = 'new'
        self._info = ''
        self._date = time.time()
        消息.__init__(self, message)

    def get_subdir(self):
        """Return 'new' or 'cur'."""
        return self._subdir

    def set_subdir(self, subdir):
        """Set subdir to 'new' or 'cur'."""
        if subdir == 'new' or subdir == 'cur':
            self._subdir = subdir
        else:
            raise ValueError("subdir must be 'new' or 'cur': %s" % subdir)

    def 取标志(self):
        """Return as a string the flags that are set."""
        if self._info.startswith('2,'):
            return self._info[2:]
        else:
            return ''

    def 设标志(self, flags):
        """Set the given flags and unset all others."""
        self._info = '2,' + ''.join(sorted(flags))

    def 加标志(self, flag):
        """Set the given flag(s) without changing others."""
        self.设标志(''.join(set(self.取标志()) | set(flag)))

    def 去标志(self, flag):
        """Unset the given string flag(s) without changing others."""
        if self.取标志():
            self.设标志(''.join(set(self.取标志()) - set(flag)))

    def get_date(self):
        """Return delivery date of message, in seconds since the epoch."""
        return self._date

    def set_date(self, date):
        """Set delivery date of message, in seconds since the epoch."""
        try:
            self._date = float(date)
        except ValueError:
            raise TypeError("can't convert to float: %s" % date) from None

    def 取信息(self):
        """Get the message's "info" as a string."""
        return self._info

    def 设信息(self, info):
        """Set the message's "info" string."""
        if isinstance(info, str):
            self._info = info
        else:
            raise TypeError('info must be a string: %s' % type(info))

    def _explain_to(self, message):
        """Copy Maildir-specific state to message insofar as possible."""
        if isinstance(message, 邮件目录消息):
            message.set_flags(self.取标志())
            message.set_subdir(self.get_subdir())
            message.set_date(self.get_date())
        elif isinstance(message, _mboxMMDFMessage):
            flags = set(self.取标志())
            if 'S' in flags:
                message.add_flag('R')
            if self.get_subdir() == 'cur':
                message.add_flag('O')
            if 'T' in flags:
                message.add_flag('D')
            if 'F' in flags:
                message.add_flag('F')
            if 'R' in flags:
                message.add_flag('A')
            message.set_from('MAILER-DAEMON', time.gmtime(self.get_date()))
        elif isinstance(message, MH消息):
            flags = set(self.取标志())
            if 'S' not in flags:
                message.add_sequence('unseen')
            if 'R' in flags:
                message.add_sequence('replied')
            if 'F' in flags:
                message.add_sequence('flagged')
        elif isinstance(message, Babyl消息):
            flags = set(self.取标志())
            if 'S' not in flags:
                message.add_label('unseen')
            if 'T' in flags:
                message.add_label('deleted')
            if 'R' in flags:
                message.add_label('answered')
            if 'P' in flags:
                message.add_label('forwarded')
        elif isinstance(message, 消息):
            pass
        else:
            raise TypeError('Cannot convert to specified type: %s' % type(message))
_装类转发(邮件目录消息, {'add_flag': '加标志', 'get_flags': '取标志', 'get_info': '取信息', 'remove_flag': '去标志', 'set_flags': '设标志', 'set_info': '设信息'}, {'add_flag': '加标志', 'get_flags': '取标志', 'get_info': '取信息', 'remove_flag': '去标志', 'set_flags': '设标志', 'set_info': '设信息'})

class _mboxMMDFMessage(消息):
    """Message with mbox- or MMDF-specific properties."""
    _type_specific_attributes = ['_from']

    def __init__(self, message=None):
        """Initialize an mboxMMDFMessage instance."""
        self.set_from('MAILER-DAEMON', True)
        if isinstance(message, email.message.Message):
            unixfrom = message.get_unixfrom()
            if unixfrom is not None and unixfrom.startswith('From '):
                self.set_from(unixfrom[5:])
        消息.__init__(self, message)

    def get_from(self):
        """Return contents of "From " line."""
        return self._from

    def set_from(self, from_, time_=None):
        """Set "From " line, formatting and appending time_ if specified."""
        if time_ is not None:
            if time_ is True:
                time_ = time.gmtime()
            from_ += ' ' + time.asctime(time_)
        self._from = from_

    def 取标志(self):
        """Return as a string the flags that are set."""
        return self.get('Status', '') + self.get('X-Status', '')

    def 设标志(self, flags):
        """Set the given flags and unset all others."""
        flags = set(flags)
        status_flags, xstatus_flags = ('', '')
        for flag in ('R', 'O'):
            if flag in flags:
                status_flags += flag
                flags.remove(flag)
        for flag in ('D', 'F', 'A'):
            if flag in flags:
                xstatus_flags += flag
                flags.remove(flag)
        xstatus_flags += ''.join(sorted(flags))
        try:
            self.replace_header('Status', status_flags)
        except KeyError:
            self.add_header('Status', status_flags)
        try:
            self.replace_header('X-Status', xstatus_flags)
        except KeyError:
            self.add_header('X-Status', xstatus_flags)

    def 加标志(self, flag):
        """Set the given flag(s) without changing others."""
        self.设标志(''.join(set(self.取标志()) | set(flag)))

    def 去标志(self, flag):
        """Unset the given string flag(s) without changing others."""
        if 'Status' in self or 'X-Status' in self:
            self.设标志(''.join(set(self.取标志()) - set(flag)))

    def _explain_to(self, message):
        """Copy mbox- or MMDF-specific state to message insofar as possible."""
        if isinstance(message, 邮件目录消息):
            flags = set(self.取标志())
            if 'O' in flags:
                message.set_subdir('cur')
            if 'F' in flags:
                message.add_flag('F')
            if 'A' in flags:
                message.add_flag('R')
            if 'R' in flags:
                message.add_flag('S')
            if 'D' in flags:
                message.add_flag('T')
            del message['status']
            del message['x-status']
            maybe_date = ' '.join(self.get_from().split()[-5:])
            try:
                message.set_date(calendar.timegm(time.strptime(maybe_date, '%a %b %d %H:%M:%S %Y')))
            except (ValueError, OverflowError):
                pass
        elif isinstance(message, _mboxMMDFMessage):
            message.set_flags(self.取标志())
            message.set_from(self.get_from())
        elif isinstance(message, MH消息):
            flags = set(self.取标志())
            if 'R' not in flags:
                message.add_sequence('unseen')
            if 'A' in flags:
                message.add_sequence('replied')
            if 'F' in flags:
                message.add_sequence('flagged')
            del message['status']
            del message['x-status']
        elif isinstance(message, Babyl消息):
            flags = set(self.取标志())
            if 'R' not in flags:
                message.add_label('unseen')
            if 'D' in flags:
                message.add_label('deleted')
            if 'A' in flags:
                message.add_label('answered')
            del message['status']
            del message['x-status']
        elif isinstance(message, 消息):
            pass
        else:
            raise TypeError('Cannot convert to specified type: %s' % type(message))
_装类转发(_mboxMMDFMessage, {'add_flag': '加标志', 'get_flags': '取标志', 'remove_flag': '去标志', 'set_flags': '设标志'}, {'add_flag': '加标志', 'get_flags': '取标志', 'remove_flag': '去标志', 'set_flags': '设标志'})

class mbox消息(_mboxMMDFMessage):
    """Message with mbox-specific properties."""

class MH消息(消息):
    """Message with MH-specific properties."""
    _type_specific_attributes = ['_sequences']

    def __init__(self, message=None):
        """Initialize an MHMessage instance."""
        self._sequences = []
        消息.__init__(self, message)

    def 取序列(self):
        """Return a list of sequences that include the message."""
        return self._sequences[:]

    def 设序列(self, sequences):
        """Set the list of sequences that include the message."""
        self._sequences = list(sequences)

    def add_sequence(self, sequence):
        """Add sequence to list of sequences including the message."""
        if isinstance(sequence, str):
            if not sequence in self._sequences:
                self._sequences.append(sequence)
        else:
            raise TypeError('sequence type must be str: %s' % type(sequence))

    def remove_sequence(self, sequence):
        """Remove sequence from the list of sequences including the message."""
        try:
            self._sequences.remove(sequence)
        except ValueError:
            pass

    def _explain_to(self, message):
        """Copy MH-specific state to message insofar as possible."""
        if isinstance(message, 邮件目录消息):
            sequences = set(self.取序列())
            if 'unseen' in sequences:
                message.set_subdir('cur')
            else:
                message.set_subdir('cur')
                message.add_flag('S')
            if 'flagged' in sequences:
                message.add_flag('F')
            if 'replied' in sequences:
                message.add_flag('R')
        elif isinstance(message, _mboxMMDFMessage):
            sequences = set(self.取序列())
            if 'unseen' not in sequences:
                message.add_flag('RO')
            else:
                message.add_flag('O')
            if 'flagged' in sequences:
                message.add_flag('F')
            if 'replied' in sequences:
                message.add_flag('A')
        elif isinstance(message, MH消息):
            for sequence in self.取序列():
                message.add_sequence(sequence)
        elif isinstance(message, Babyl消息):
            sequences = set(self.取序列())
            if 'unseen' in sequences:
                message.add_label('unseen')
            if 'replied' in sequences:
                message.add_label('answered')
        elif isinstance(message, 消息):
            pass
        else:
            raise TypeError('Cannot convert to specified type: %s' % type(message))
_装类转发(MH消息, {'get_sequences': '取序列', 'set_sequences': '设序列'}, {'get_sequences': '取序列', 'set_sequences': '设序列'})

class Babyl消息(消息):
    """Message with Babyl-specific properties."""
    _type_specific_attributes = ['_labels', '_visible']

    def __init__(self, message=None):
        """Initialize a BabylMessage instance."""
        self._labels = []
        self._visible = 消息()
        消息.__init__(self, message)

    def get_labels(self):
        """Return a list of labels on the message."""
        return self._labels[:]

    def set_labels(self, labels):
        """Set the list of labels on the message."""
        self._labels = list(labels)

    def add_label(self, label):
        """Add label to list of labels on the message."""
        if isinstance(label, str):
            if label not in self._labels:
                self._labels.append(label)
        else:
            raise TypeError('label must be a string: %s' % type(label))

    def remove_label(self, label):
        """Remove label from the list of labels on the message."""
        try:
            self._labels.remove(label)
        except ValueError:
            pass

    def get_visible(self):
        """Return a Message representation of visible headers."""
        return 消息(self._visible)

    def set_visible(self, visible):
        """Set the Message representation of visible headers."""
        self._visible = 消息(visible)

    def update_visible(self):
        """Update and/or sensibly generate a set of visible headers."""
        for header in self._visible.keys():
            if header in self:
                self._visible.replace_header(header, self[header])
            else:
                del self._visible[header]
        for header in ('Date', 'From', 'Reply-To', 'To', 'CC', 'Subject'):
            if header in self and header not in self._visible:
                self._visible[header] = self[header]

    def _explain_to(self, message):
        """Copy Babyl-specific state to message insofar as possible."""
        if isinstance(message, 邮件目录消息):
            labels = set(self.get_labels())
            if 'unseen' in labels:
                message.set_subdir('cur')
            else:
                message.set_subdir('cur')
                message.add_flag('S')
            if 'forwarded' in labels or 'resent' in labels:
                message.add_flag('P')
            if 'answered' in labels:
                message.add_flag('R')
            if 'deleted' in labels:
                message.add_flag('T')
        elif isinstance(message, _mboxMMDFMessage):
            labels = set(self.get_labels())
            if 'unseen' not in labels:
                message.add_flag('RO')
            else:
                message.add_flag('O')
            if 'deleted' in labels:
                message.add_flag('D')
            if 'answered' in labels:
                message.add_flag('A')
        elif isinstance(message, MH消息):
            labels = set(self.get_labels())
            if 'unseen' in labels:
                message.add_sequence('unseen')
            if 'answered' in labels:
                message.add_sequence('replied')
        elif isinstance(message, Babyl消息):
            message.set_visible(self.get_visible())
            for label in self.get_labels():
                message.add_label(label)
        elif isinstance(message, 消息):
            pass
        else:
            raise TypeError('Cannot convert to specified type: %s' % type(message))

class MMDF消息(_mboxMMDFMessage):
    """Message with MMDF-specific properties."""

class _ProxyFile:
    """A read-only wrapper of a file."""

    def __init__(self, f, pos=None):
        """Initialize a _ProxyFile."""
        self._file = f
        if pos is None:
            self._pos = f.tell()
        else:
            self._pos = pos

    def read(self, size=None):
        """Read bytes."""
        return self._read(size, self._file.read)

    def read1(self, size=None):
        """Read bytes."""
        return self._read(size, self._file.read1)

    def readline(self, size=None):
        """Read a line."""
        return self._read(size, self._file.readline)

    def readlines(self, sizehint=None):
        """Read multiple lines."""
        result = []
        for line in self:
            result.append(line)
            if sizehint is not None:
                sizehint -= len(line)
                if sizehint <= 0:
                    break
        return result

    def __iter__(self):
        """Iterate over lines."""
        while (line := self.readline()):
            yield line

    def tell(self):
        """Return the position."""
        return self._pos

    def seek(self, offset, whence=0):
        """Change position."""
        if whence == 1:
            self._file.seek(self._pos)
        self._file.seek(offset, whence)
        self._pos = self._file.tell()

    def close(self):
        """Close the file."""
        if hasattr(self, '_file'):
            try:
                if hasattr(self._file, 'close'):
                    self._file.close()
            finally:
                del self._file

    def _read(self, size, read_method):
        """Read size bytes using read_method."""
        if size is None:
            size = -1
        self._file.seek(self._pos)
        result = read_method(size)
        self._pos = self._file.tell()
        return result

    def __enter__(self):
        """Context management protocol support."""
        return self

    def __exit__(self, *exc):
        self.close()

    def readable(self):
        return self._file.readable()

    def writable(self):
        return self._file.writable()

    def seekable(self):
        return self._file.seekable()

    def flush(self):
        return self._file.flush()

    @property
    def closed(self):
        if not hasattr(self, '_file'):
            return True
        if not hasattr(self._file, 'closed'):
            return False
        return self._file.closed
    __class_getitem__ = classmethod(GenericAlias)

class _PartialFile(_ProxyFile):
    """A read-only wrapper of part of a file."""

    def __init__(self, f, start=None, stop=None):
        """Initialize a _PartialFile."""
        _ProxyFile.__init__(self, f, start)
        self._start = start
        self._stop = stop

    def tell(self):
        """Return the position with respect to start."""
        return _ProxyFile.tell(self) - self._start

    def seek(self, offset, whence=0):
        """Change position, possibly with respect to start or stop."""
        if whence == 0:
            self._pos = self._start
            whence = 1
        elif whence == 2:
            self._pos = self._stop
            whence = 1
        _ProxyFile.seek(self, offset, whence)

    def _read(self, size, read_method):
        """Read size bytes using read_method, honoring start and stop."""
        remaining = self._stop - self._pos
        if remaining <= 0:
            return b''
        if size is None or size < 0 or size > remaining:
            size = remaining
        return _ProxyFile._read(self, size, read_method)

    def close(self):
        if hasattr(self, '_file'):
            del self._file

def _lock_file(f, dotlock=True):
    """Lock file f using lockf and dot locking."""
    dotlock_done = False
    try:
        if fcntl:
            try:
                fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as e:
                if e.errno in (errno.EAGAIN, errno.EACCES, errno.EROFS):
                    raise 外部冲突错误('lockf: lock unavailable: %s' % f.name)
                else:
                    raise
        if dotlock:
            try:
                pre_lock = _create_temporary(f.name + '.lock')
                pre_lock.close()
            except OSError as e:
                if e.errno in (errno.EACCES, errno.EROFS):
                    return
                else:
                    raise
            try:
                try:
                    os.link(pre_lock.name, f.name + '.lock')
                    dotlock_done = True
                except (AttributeError, PermissionError):
                    os.rename(pre_lock.name, f.name + '.lock')
                    dotlock_done = True
                else:
                    os.unlink(pre_lock.name)
            except FileExistsError:
                os.remove(pre_lock.name)
                raise 外部冲突错误('dot lock unavailable: %s' % f.name)
    except:
        if fcntl:
            fcntl.lockf(f, fcntl.LOCK_UN)
        if dotlock_done:
            os.remove(f.name + '.lock')
        raise

def _unlock_file(f):
    """Unlock file f using lockf and dot locking."""
    if fcntl:
        fcntl.lockf(f, fcntl.LOCK_UN)
    if os.path.exists(f.name + '.lock'):
        os.remove(f.name + '.lock')

def _create_carefully(path):
    """Create a file if it doesn't exist and open for reading and writing."""
    return open(path, 'xb+')

def _create_temporary(path):
    """Create a temp file based on path and open for reading and writing."""
    return _create_carefully('%s.%s.%s.%s' % (path, int(time.time()), socket.gethostname(), os.getpid()))

def _sync_flush(f):
    """Ensure changes to file f are physically on disk."""
    f.flush()
    if hasattr(os, 'fsync'):
        os.fsync(f.fileno())

def _sync_close(f):
    """Close file f, ensuring all changes are physically on disk."""
    _sync_flush(f)
    f.close()

class 错误(Exception):
    """Raised for module-specific errors."""

class 无此信箱错误(错误):
    """The specified mailbox does not exist and won't be created."""

class 非空错误(错误):
    """The specified mailbox is not empty and deletion was requested."""

class 外部冲突错误(错误):
    """Another process caused an action to fail."""

class 格式错误(错误):
    """A file appears to have an invalid format."""


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Babyl': 'Babyl信箱',
    'BabylMessage': 'Babyl消息',
    'Error': '错误',
    'ExternalClashError': '外部冲突错误',
    'FormatError': '格式错误',
    'MH': 'MH信箱',
    'MHMessage': 'MH消息',
    'MMDF': 'MMDF信箱',
    'MMDFMessage': 'MMDF消息',
    'Mailbox': '信箱',
    'Maildir': '邮件目录',
    'MaildirMessage': '邮件目录消息',
    'Message': '消息',
    'NoSuchMailboxError': '无此信箱错误',
    'NotEmptyError': '非空错误',
    'mbox': 'mbox信箱',
    'mboxMessage': 'mbox消息',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'Babyl信箱': {
        'get_bytes': '取字节',
        'get_message': '取消息',
    },
    'MH信箱': {
        'add_folder': '加文件夹',
        'get_bytes': '取字节',
        'get_folder': '取文件夹',
        'get_message': '取消息',
        'get_sequences': '取序列',
        'iterkeys': '迭代键',
        'list_folders': '列出文件夹',
        'remove_folder': '去文件夹',
        'set_sequences': '设序列',
    },
    'MH消息': {
        'get_sequences': '取序列',
        'set_sequences': '设序列',
    },
    '_mboxMMDF': {
        'get_bytes': '取字节',
        'get_message': '取消息',
        'get_string': '取字符串',
    },
    '_mboxMMDFMessage': {
        'add_flag': '加标志',
        'get_flags': '取标志',
        'remove_flag': '去标志',
        'set_flags': '设标志',
    },
    '_singlefileMailbox': {
        'iterkeys': '迭代键',
    },
    '信箱': {
        'get_bytes': '取字节',
        'get_message': '取消息',
        'get_string': '取字符串',
        'iteritems': '迭代项',
        'iterkeys': '迭代键',
        'itervalues': '迭代值',
    },
    '邮件目录': {
        'add_flag': '加标志',
        'add_folder': '加文件夹',
        'clean': '清理',
        'get_bytes': '取字节',
        'get_flags': '取标志',
        'get_folder': '取文件夹',
        'get_info': '取信息',
        'get_message': '取消息',
        'iterkeys': '迭代键',
        'list_folders': '列出文件夹',
        'remove_flag': '去标志',
        'remove_folder': '去文件夹',
        'set_flags': '设标志',
        'set_info': '设信息',
    },
    '邮件目录消息': {
        'add_flag': '加标志',
        'get_flags': '取标志',
        'get_info': '取信息',
        'remove_flag': '去标志',
        'set_flags': '设标志',
        'set_info': '设信息',
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
    'Babyl信箱': {
        'get_bytes': '取字节',
        'get_message': '取消息',
    },
    'MH信箱': {
        'add_folder': '加文件夹',
        'get_bytes': '取字节',
        'get_folder': '取文件夹',
        'get_message': '取消息',
        'get_sequences': '取序列',
        'iterkeys': '迭代键',
        'list_folders': '列出文件夹',
        'remove_folder': '去文件夹',
        'set_sequences': '设序列',
    },
    'MH消息': {
        'get_sequences': '取序列',
        'set_sequences': '设序列',
    },
    '_mboxMMDF': {
        'get_bytes': '取字节',
        'get_message': '取消息',
        'get_string': '取字符串',
    },
    '_mboxMMDFMessage': {
        'add_flag': '加标志',
        'get_flags': '取标志',
        'remove_flag': '去标志',
        'set_flags': '设标志',
    },
    '_singlefileMailbox': {
        'iterkeys': '迭代键',
    },
    '信箱': {
        'get_bytes': '取字节',
        'get_message': '取消息',
        'get_string': '取字符串',
        'iteritems': '迭代项',
        'iterkeys': '迭代键',
        'itervalues': '迭代值',
    },
    '邮件目录': {
        'add_flag': '加标志',
        'add_folder': '加文件夹',
        'clean': '清理',
        'get_bytes': '取字节',
        'get_flags': '取标志',
        'get_folder': '取文件夹',
        'get_info': '取信息',
        'get_message': '取消息',
        'iterkeys': '迭代键',
        'list_folders': '列出文件夹',
        'remove_flag': '去标志',
        'remove_folder': '去文件夹',
        'set_flags': '设标志',
        'set_info': '设信息',
    },
    '邮件目录消息': {
        'add_flag': '加标志',
        'get_flags': '取标志',
        'get_info': '取信息',
        'remove_flag': '去标志',
        'set_flags': '设标志',
        'set_info': '设信息',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'Babyl信箱',
    'Babyl消息',
    'MH信箱',
    'MH消息',
    'MMDF信箱',
    'MMDF消息',
    'mbox信箱',
    'mbox消息',
    '信箱',
    '外部冲突错误',
    '无此信箱错误',
    '格式错误',
    '消息',
    '邮件目录',
    '邮件目录消息',
    '错误',
    '非空错误',
]

# ---- 转发层结束 ----
