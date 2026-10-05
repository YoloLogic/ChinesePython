# -*- coding: utf-8 -*-
"""选择器 —— 汉语库（由 tools/汉化库.py 从 Lib/selectors.py 机械生成，**不要手改**）。

英文库 Lib/selectors.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 选择器
"""


"""Selectors module.

This module allows high-level and efficient I/O multiplexing, built upon the
`select` module primitives.
"""
_英文原名表 = {'BaseSelector': '选择器基类', 'DefaultSelector': '默认选择器', 'DevpollSelector': 'devpoll选择器', 'EVENT_READ': '可读事件', 'EVENT_WRITE': '可写事件', 'EpollSelector': 'epoll选择器', 'KqueueSelector': 'kqueue选择器', 'PollSelector': 'poll选择器', 'SelectSelector': 'select选择器', 'SelectorKey': '选择器键'}

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
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from collections.abc import Mapping
import math
import select
import sys
可读事件 = 1 << 0
可写事件 = 1 << 1

def _fileobj_to_fd(fileobj):
    """Return a file descriptor from a file object.

    Parameters:
    fileobj -- file object or file descriptor

    Returns:
    corresponding file descriptor

    Raises:
    ValueError if the object is invalid
    """
    if isinstance(fileobj, int):
        fd = fileobj
    else:
        try:
            fd = int(fileobj.fileno())
        except (AttributeError, TypeError, ValueError):
            raise ValueError('Invalid file object: {!r}'.format(fileobj)) from None
    if fd < 0:
        raise ValueError('Invalid file descriptor: {}'.format(fd))
    return fd
选择器键 = namedtuple('SelectorKey', ['fileobj', 'fd', 'events', 'data'])
选择器键.__doc__ = 'SelectorKey(fileobj, fd, events, data)\n\n    Object used to associate a file object to its backing\n    file descriptor, selected event mask, and attached data.\n'
选择器键.fileobj.__doc__ = 'File object registered.'
选择器键.fd.__doc__ = 'Underlying file descriptor.'
选择器键.events.__doc__ = 'Events that must be waited for on this file object.'
选择器键.data.__doc__ = 'Optional opaque data associated to this file object.\nFor example, this could be used to store a per-client session ID.'

class _SelectorMapping(Mapping):
    """Mapping of file objects to selector keys."""

    def __init__(self, selector):
        self._selector = selector

    def __len__(self):
        return len(self._selector._fd_to_key)

    def get(self, fileobj, default=None):
        fd = self._selector._fileobj_lookup(fileobj)
        return self._selector._fd_to_key.get(fd, default)

    def __getitem__(self, fileobj):
        fd = self._selector._fileobj_lookup(fileobj)
        key = self._selector._fd_to_key.get(fd)
        if key is None:
            raise KeyError('{!r} is not registered'.format(fileobj))
        return key

    def __iter__(self):
        return iter(self._selector._fd_to_key)

class 选择器基类(metaclass=ABCMeta):
    """Selector abstract base class.

    A selector supports registering file objects to be monitored for specific
    I/O events.

    A file object is a file descriptor or any object with a `fileno()` method.
    An arbitrary object can be attached to the file object, which can be used
    for example to store context information, a callback, etc.

    A selector can use various implementations (select(), poll(), epoll()...)
    depending on the platform. The default `Selector` class uses the most
    efficient implementation on the current platform.
    """

    @abstractmethod
    def 登记(self, fileobj, events, data=None):
        """Register a file object.

        Parameters:
        fileobj -- file object or file descriptor
        events  -- events to monitor (bitwise mask of EVENT_READ|EVENT_WRITE)
        data    -- attached data

        Returns:
        SelectorKey instance

        Raises:
        ValueError if events is invalid
        KeyError if fileobj is already registered
        OSError if fileobj is closed or otherwise is unacceptable to
                the underlying system call (if a system call is made)

        Note:
        OSError may or may not be raised
        """
        raise NotImplementedError

    @abstractmethod
    def 注销(self, fileobj):
        """Unregister a file object.

        Parameters:
        fileobj -- file object or file descriptor

        Returns:
        SelectorKey instance

        Raises:
        KeyError if fileobj is not registered

        Note:
        If fileobj is registered but has since been closed this does
        *not* raise OSError (even if the wrapped syscall does)
        """
        raise NotImplementedError

    def 修改(self, fileobj, events, data=None):
        """Change a registered file object monitored events or attached data.

        Parameters:
        fileobj -- file object or file descriptor
        events  -- events to monitor (bitwise mask of EVENT_READ|EVENT_WRITE)
        data    -- attached data

        Returns:
        SelectorKey instance

        Raises:
        Anything that unregister() or register() raises
        """
        self.注销(fileobj)
        return self.登记(fileobj, events, data)

    @abstractmethod
    def select(self, timeout=None):
        """Perform the actual selection, until some monitored file objects are
        ready or a timeout expires.

        Parameters:
        timeout -- if timeout > 0, this specifies the maximum wait time, in
                   seconds
                   if timeout <= 0, the select() call won't block, and will
                   report the currently ready file objects
                   if timeout is None, select() will block until a monitored
                   file object becomes ready

        Returns:
        list of (key, events) for ready file objects
        `events` is a bitwise mask of EVENT_READ|EVENT_WRITE
        """
        raise NotImplementedError

    def close(self):
        """Close the selector.

        This must be called to make sure that any underlying resource is freed.
        """
        pass

    def 取键(self, fileobj):
        """Return the key associated to a registered file object.

        Returns:
        SelectorKey for this file object
        """
        mapping = self.取映射表()
        if mapping is None:
            raise RuntimeError('Selector is closed')
        try:
            return mapping[fileobj]
        except KeyError:
            raise KeyError('{!r} is not registered'.format(fileobj)) from None

    @abstractmethod
    def 取映射表(self):
        """Return a mapping of file objects to selector keys."""
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
_装类转发(选择器基类, {'get_key': '取键', 'get_map': '取映射表', 'modify': '修改', 'register': '登记', 'select': '选择', 'unregister': '注销'}, {'get_key': '取键', 'get_map': '取映射表', 'modify': '修改', 'register': '登记', 'select': '选择', 'unregister': '注销'})

class _BaseSelectorImpl(选择器基类):
    """Base selector implementation."""

    def __init__(self):
        self._fd_to_key = {}
        self._map = _SelectorMapping(self)

    def _fileobj_lookup(self, fileobj):
        """Return a file descriptor from a file object.

        This wraps _fileobj_to_fd() to do an exhaustive search in case
        the object is invalid but we still have it in our map.  This
        is used by unregister() so we can unregister an object that
        was previously registered even if it is closed.  It is also
        used by _SelectorMapping.
        """
        try:
            return _fileobj_to_fd(fileobj)
        except ValueError:
            for key in self._fd_to_key.values():
                if key.fileobj is fileobj:
                    return key.fd
            raise

    def 登记(self, fileobj, events, data=None):
        if not events or events & ~(可读事件 | 可写事件):
            raise ValueError('Invalid events: {!r}'.format(events))
        key = 选择器键(fileobj, self._fileobj_lookup(fileobj), events, data)
        if key.fd in self._fd_to_key:
            raise KeyError('{!r} (FD {}) is already registered'.format(fileobj, key.fd))
        self._fd_to_key[key.fd] = key
        return key

    def 注销(self, fileobj):
        try:
            key = self._fd_to_key.pop(self._fileobj_lookup(fileobj))
        except KeyError:
            raise KeyError('{!r} is not registered'.format(fileobj)) from None
        return key

    def 修改(self, fileobj, events, data=None):
        try:
            key = self._fd_to_key[self._fileobj_lookup(fileobj)]
        except KeyError:
            raise KeyError('{!r} is not registered'.format(fileobj)) from None
        if events != key.events:
            self.注销(fileobj)
            key = self.登记(fileobj, events, data)
        elif data != key.data:
            key = key._replace(data=data)
            self._fd_to_key[key.fd] = key
        return key

    def close(self):
        self._fd_to_key.clear()
        self._map = None

    def 取映射表(self):
        return self._map
_装类转发(_BaseSelectorImpl, {'get_map': '取映射表', 'modify': '修改', 'register': '登记', 'unregister': '注销'}, {'get_map': '取映射表', 'modify': '修改', 'register': '登记', 'unregister': '注销'})

class select选择器(_BaseSelectorImpl):
    """Select-based selector."""

    def __init__(self):
        super().__init__()
        self._readers = set()
        self._writers = set()

    def 登记(self, fileobj, events, data=None):
        key = super().register(fileobj, events, data)
        if events & 可读事件:
            self._readers.add(key.fd)
        if events & 可写事件:
            self._writers.add(key.fd)
        return key

    def 注销(self, fileobj):
        key = super().unregister(fileobj)
        self._readers.discard(key.fd)
        self._writers.discard(key.fd)
        return key
    if sys.platform == 'win32':

        def _select(self, r, w, _, timeout=None):
            r, w, x = select.select(r, w, w, timeout)
            return (r, w + x, [])
    else:
        _select = select.select

    def select(self, timeout=None):
        timeout = None if timeout is None else max(timeout, 0)
        ready = []
        try:
            r, w, _ = self._select(self._readers, self._writers, [], timeout)
        except InterruptedError:
            return ready
        r = frozenset(r)
        w = frozenset(w)
        rw = r | w
        fd_to_key_get = self._fd_to_key.get
        for fd in rw:
            key = fd_to_key_get(fd)
            if key:
                events = (fd in r and 可读事件) | (fd in w and 可写事件)
                ready.append((key, events & key.events))
        return ready
_装类转发(select选择器, {'register': '登记', 'select': '选择', 'unregister': '注销'}, {'register': '登记', 'select': '选择', 'unregister': '注销'})

class _PollLikeSelector(_BaseSelectorImpl):
    """Base class shared between poll, epoll and devpoll selectors."""
    _selector_cls = None
    _EVENT_READ = None
    _EVENT_WRITE = None

    def __init__(self):
        super().__init__()
        self._selector = self._selector_cls()

    def 登记(self, fileobj, events, data=None):
        key = super().register(fileobj, events, data)
        poller_events = (events & 可读事件 and self._EVENT_READ) | (events & 可写事件 and self._EVENT_WRITE)
        try:
            self._selector.register(key.fd, poller_events)
        except:
            super().unregister(fileobj)
            raise
        return key

    def 注销(self, fileobj):
        key = super().unregister(fileobj)
        try:
            self._selector.unregister(key.fd)
        except OSError:
            pass
        return key

    def 修改(self, fileobj, events, data=None):
        try:
            key = self._fd_to_key[self._fileobj_lookup(fileobj)]
        except KeyError:
            raise KeyError(f'{fileobj!r} is not registered') from None
        changed = False
        if events != key.events:
            selector_events = (events & 可读事件 and self._EVENT_READ) | (events & 可写事件 and self._EVENT_WRITE)
            try:
                self._selector.modify(key.fd, selector_events)
            except:
                super().unregister(fileobj)
                raise
            changed = True
        if data != key.data:
            changed = True
        if changed:
            key = key._replace(events=events, data=data)
            self._fd_to_key[key.fd] = key
        return key

    def select(self, timeout=None):
        if timeout is None:
            timeout = None
        elif timeout <= 0:
            timeout = 0
        else:
            timeout = math.ceil(timeout * 1000.0)
        ready = []
        try:
            fd_event_list = self._selector.poll(timeout)
        except InterruptedError:
            return ready
        fd_to_key_get = self._fd_to_key.get
        for fd, event in fd_event_list:
            key = fd_to_key_get(fd)
            if key:
                events = (event & ~self._EVENT_READ and 可写事件) | (event & ~self._EVENT_WRITE and 可读事件)
                ready.append((key, events & key.events))
        return ready
_装类转发(_PollLikeSelector, {'modify': '修改', 'register': '登记', 'select': '选择', 'unregister': '注销'}, {'modify': '修改', 'register': '登记', 'select': '选择', 'unregister': '注销'})
if hasattr(select, 'poll'):

    class poll选择器(_PollLikeSelector):
        """Poll-based selector."""
        _selector_cls = select.poll
        _EVENT_READ = select.POLLIN
        _EVENT_WRITE = select.POLLOUT
if hasattr(select, 'epoll'):
    _NOT_EPOLLIN = ~select.EPOLLIN
    _NOT_EPOLLOUT = ~select.EPOLLOUT

    class epoll选择器(_PollLikeSelector):
        """Epoll-based selector."""
        _selector_cls = select.epoll
        _EVENT_READ = select.EPOLLIN
        _EVENT_WRITE = select.EPOLLOUT

        def fileno(self):
            return self._selector.fileno()

        def select(self, timeout=None):
            if timeout is None:
                timeout = -1
            elif timeout <= 0:
                timeout = 0
            else:
                timeout = math.ceil(timeout * 1000.0) * 0.001
            max_ev = len(self._fd_to_key) or 1
            ready = []
            try:
                fd_event_list = self._selector.poll(timeout, max_ev)
            except InterruptedError:
                return ready
            fd_to_key = self._fd_to_key
            for fd, event in fd_event_list:
                key = fd_to_key.get(fd)
                if key:
                    events = (event & _NOT_EPOLLIN and 可写事件) | (event & _NOT_EPOLLOUT and 可读事件)
                    ready.append((key, events & key.events))
            return ready

        def close(self):
            self._selector.close()
            super().close()
    _装类转发(epoll选择器, {'select': '选择'}, {'select': '选择'})
if hasattr(select, 'devpoll'):

    class devpoll选择器(_PollLikeSelector):
        """Solaris /dev/poll selector."""
        _selector_cls = select.devpoll
        _EVENT_READ = select.POLLIN
        _EVENT_WRITE = select.POLLOUT

        def fileno(self):
            return self._selector.fileno()

        def close(self):
            self._selector.close()
            super().close()
if hasattr(select, 'kqueue'):

    class kqueue选择器(_BaseSelectorImpl):
        """Kqueue-based selector."""

        def __init__(self):
            super().__init__()
            self._selector = select.kqueue()
            self._max_events = 0

        def fileno(self):
            return self._selector.fileno()

        def 登记(self, fileobj, events, data=None):
            key = super().register(fileobj, events, data)
            try:
                if events & 可读事件:
                    kev = select.kevent(key.fd, select.KQ_FILTER_READ, select.KQ_EV_ADD)
                    self._selector.control([kev], 0, 0)
                    self._max_events += 1
                if events & 可写事件:
                    kev = select.kevent(key.fd, select.KQ_FILTER_WRITE, select.KQ_EV_ADD)
                    self._selector.control([kev], 0, 0)
                    self._max_events += 1
            except:
                super().unregister(fileobj)
                raise
            return key

        def 注销(self, fileobj):
            key = super().unregister(fileobj)
            if key.events & 可读事件:
                kev = select.kevent(key.fd, select.KQ_FILTER_READ, select.KQ_EV_DELETE)
                self._max_events -= 1
                try:
                    self._selector.control([kev], 0, 0)
                except OSError:
                    pass
            if key.events & 可写事件:
                kev = select.kevent(key.fd, select.KQ_FILTER_WRITE, select.KQ_EV_DELETE)
                self._max_events -= 1
                try:
                    self._selector.control([kev], 0, 0)
                except OSError:
                    pass
            return key

        def select(self, timeout=None):
            timeout = None if timeout is None else max(timeout, 0)
            max_ev = self._max_events or 1
            ready = []
            try:
                kev_list = self._selector.control(None, max_ev, timeout)
            except InterruptedError:
                return ready
            fd_to_key_get = self._fd_to_key.get
            for kev in kev_list:
                fd = kev.ident
                flag = kev.filter
                key = fd_to_key_get(fd)
                if key:
                    events = (flag == select.KQ_FILTER_READ and 可读事件) | (flag == select.KQ_FILTER_WRITE and 可写事件)
                    ready.append((key, events & key.events))
            return ready

        def close(self):
            self._selector.close()
            super().close()
    _装类转发(kqueue选择器, {'register': '登记', 'select': '选择', 'unregister': '注销'}, {'register': '登记', 'select': '选择', 'unregister': '注销'})

def _can_use(method):
    """Check if we can use the selector depending upon the
    operating system. """
    selector = getattr(select, method, None)
    if selector is None:
        return False
    try:
        selector_obj = selector()
        if method == 'poll':
            selector_obj.poll(0)
        else:
            selector_obj.close()
        return True
    except OSError:
        return False
if _can_use('kqueue'):
    默认选择器 = kqueue选择器
elif _can_use('epoll'):
    默认选择器 = epoll选择器
elif _can_use('devpoll'):
    默认选择器 = devpoll选择器
elif _can_use('poll'):
    默认选择器 = poll选择器
else:
    默认选择器 = select选择器


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BaseSelector': '选择器基类',
    'DefaultSelector': '默认选择器',
    'DevpollSelector': 'devpoll选择器',
    'EVENT_READ': '可读事件',
    'EVENT_WRITE': '可写事件',
    'EpollSelector': 'epoll选择器',
    'KqueueSelector': 'kqueue选择器',
    'PollSelector': 'poll选择器',
    'SelectSelector': 'select选择器',
    'SelectorKey': '选择器键',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '_BaseSelectorImpl': {
        'get_map': '取映射表',
        'modify': '修改',
        'register': '登记',
        'unregister': '注销',
    },
    '_PollLikeSelector': {
        'modify': '修改',
        'register': '登记',
        'select': '选择',
        'unregister': '注销',
    },
    'epoll选择器': {
        'select': '选择',
    },
    'kqueue选择器': {
        'register': '登记',
        'select': '选择',
        'unregister': '注销',
    },
    'select选择器': {
        'register': '登记',
        'select': '选择',
        'unregister': '注销',
    },
    '选择器基类': {
        'get_key': '取键',
        'get_map': '取映射表',
        'modify': '修改',
        'register': '登记',
        'select': '选择',
        'unregister': '注销',
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
    '_BaseSelectorImpl': {
        'get_map': '取映射表',
        'modify': '修改',
        'register': '登记',
        'unregister': '注销',
    },
    '_PollLikeSelector': {
        'modify': '修改',
        'register': '登记',
        'select': '选择',
        'unregister': '注销',
    },
    'epoll选择器': {
        'select': '选择',
    },
    'kqueue选择器': {
        'register': '登记',
        'select': '选择',
        'unregister': '注销',
    },
    'select选择器': {
        'register': '登记',
        'select': '选择',
        'unregister': '注销',
    },
    '选择器基类': {
        'get_key': '取键',
        'get_map': '取映射表',
        'modify': '修改',
        'register': '登记',
        'select': '选择',
        'unregister': '注销',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
