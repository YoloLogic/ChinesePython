# -*- coding: utf-8 -*-
"""多进程.heap —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/heap.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.heap.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


_英文原名表 = {'BufferWrapper': '缓冲包装', 'Heap': '堆'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import bisect
from collections import defaultdict
import mmap
import os
import sys
import tempfile
import threading
from .context import reduction, assert_spawning
from . import util
__all__ = ['BufferWrapper']
if sys.platform == 'win32':
    import _winapi

    class Arena(object):
        """
        A shared memory area backed by anonymous memory (Windows).
        """
        _rand = tempfile._RandomNameSequence()

        def __init__(self, size):
            self.size = size
            for i in range(100):
                name = 'pym-%d-%s' % (os.getpid(), next(self._rand))
                buf = mmap.mmap(-1, size, tagname=name)
                if _winapi.GetLastError() == 0:
                    break
                buf.close()
            else:
                raise FileExistsError('Cannot find name for new mmap')
            self.name = name
            self.buffer = buf
            self._state = (self.size, self.name)

        def __getstate__(self):
            assert_spawning(self)
            return self._state

        def __setstate__(self, state):
            self.size, self.name = self._state = state
            self.buffer = mmap.mmap(-1, self.size, tagname=self.name)
else:

    class Arena(object):
        """
        A shared memory area backed by a temporary file (POSIX).
        """
        if sys.platform == 'linux':
            _dir_candidates = ['/dev/shm']
        else:
            _dir_candidates = []

        def __init__(self, size, fd=-1):
            self.size = size
            self.fd = fd
            if fd == -1:
                self.fd, name = tempfile.mkstemp(prefix='pym-%d-' % os.getpid(), dir=self._choose_dir(size))
                os.unlink(name)
                util.Finalize(self, os.close, (self.fd,))
                os.ftruncate(self.fd, size)
            self.buffer = mmap.mmap(self.fd, self.size)

        def _choose_dir(self, size):
            for d in self._dir_candidates:
                st = os.statvfs(d)
                if st.f_bavail * st.f_frsize >= size:
                    return d
            return util.get_temp_dir()

    def reduce_arena(a):
        if a.fd == -1:
            raise ValueError('Arena is unpicklable because forking was enabled when it was created')
        return (rebuild_arena, (a.size, reduction.DupFd(a.fd)))

    def rebuild_arena(size, dupfd):
        return Arena(size, dupfd.detach())
    reduction.register(Arena, reduce_arena)

class 堆(object):
    _alignment = 8
    _DISCARD_FREE_SPACE_LARGER_THAN = 4 * 1024 ** 2
    _DOUBLE_ARENA_SIZE_UNTIL = 4 * 1024 ** 2

    def __init__(self, size=mmap.PAGESIZE):
        self._lastpid = os.getpid()
        self._lock = threading.Lock()
        self._size = size
        self._lengths = []
        self._len_to_seq = {}
        self._start_to_block = {}
        self._stop_to_block = {}
        self._allocated_blocks = defaultdict(set)
        self._arenas = []
        self._pending_free_blocks = []
        self._n_mallocs = 0
        self._n_frees = 0

    @staticmethod
    def _roundup(n, alignment):
        mask = alignment - 1
        return n + mask & ~mask

    def _new_arena(self, size):
        length = self._roundup(max(self._size, size), mmap.PAGESIZE)
        if self._size < self._DOUBLE_ARENA_SIZE_UNTIL:
            self._size *= 2
        util.info('allocating a new mmap of length %d', length)
        arena = Arena(length)
        self._arenas.append(arena)
        return (arena, 0, length)

    def _discard_arena(self, arena):
        length = arena.size
        if length < self._DISCARD_FREE_SPACE_LARGER_THAN:
            return
        blocks = self._allocated_blocks.pop(arena)
        assert not blocks
        del self._start_to_block[arena, 0]
        del self._stop_to_block[arena, length]
        self._arenas.remove(arena)
        seq = self._len_to_seq[length]
        seq.remove((arena, 0, length))
        if not seq:
            del self._len_to_seq[length]
            self._lengths.remove(length)

    def _malloc(self, size):
        i = bisect.bisect_left(self._lengths, size)
        if i == len(self._lengths):
            return self._new_arena(size)
        else:
            length = self._lengths[i]
            seq = self._len_to_seq[length]
            block = seq.pop()
            if not seq:
                del self._len_to_seq[length], self._lengths[i]
        arena, start, stop = block
        del self._start_to_block[arena, start]
        del self._stop_to_block[arena, stop]
        return block

    def _add_free_block(self, block):
        arena, start, stop = block
        try:
            prev_block = self._stop_to_block[arena, start]
        except KeyError:
            pass
        else:
            start, _ = self._absorb(prev_block)
        try:
            next_block = self._start_to_block[arena, stop]
        except KeyError:
            pass
        else:
            _, stop = self._absorb(next_block)
        block = (arena, start, stop)
        length = stop - start
        try:
            self._len_to_seq[length].append(block)
        except KeyError:
            self._len_to_seq[length] = [block]
            bisect.insort(self._lengths, length)
        self._start_to_block[arena, start] = block
        self._stop_to_block[arena, stop] = block

    def _absorb(self, block):
        arena, start, stop = block
        del self._start_to_block[arena, start]
        del self._stop_to_block[arena, stop]
        length = stop - start
        seq = self._len_to_seq[length]
        seq.remove(block)
        if not seq:
            del self._len_to_seq[length]
            self._lengths.remove(length)
        return (start, stop)

    def _remove_allocated_block(self, block):
        arena, start, stop = block
        blocks = self._allocated_blocks[arena]
        blocks.remove((start, stop))
        if not blocks:
            self._discard_arena(arena)

    def _free_pending_blocks(self):
        while True:
            try:
                block = self._pending_free_blocks.pop()
            except IndexError:
                break
            self._add_free_block(block)
            self._remove_allocated_block(block)

    def free(self, block):
        if os.getpid() != self._lastpid:
            raise ValueError('My pid ({0:n}) is not last pid {1:n}'.format(os.getpid(), self._lastpid))
        if not self._lock.acquire(False):
            self._pending_free_blocks.append(block)
        else:
            try:
                self._n_frees += 1
                self._free_pending_blocks()
                self._add_free_block(block)
                self._remove_allocated_block(block)
            finally:
                self._lock.release()

    def malloc(self, size):
        if size < 0:
            raise ValueError('Size {0:n} out of range'.format(size))
        if sys.maxsize <= size:
            raise OverflowError('Size {0:n} too large'.format(size))
        if os.getpid() != self._lastpid:
            self.__init__()
        with self._lock:
            self._n_mallocs += 1
            self._free_pending_blocks()
            size = self._roundup(max(size, 1), self._alignment)
            arena, start, stop = self._malloc(size)
            real_stop = start + size
            if real_stop < stop:
                self._add_free_block((arena, real_stop, stop))
            self._allocated_blocks[arena].add((start, real_stop))
            return (arena, start, real_stop)

class 缓冲包装(object):
    _heap = 堆()

    def __init__(self, size):
        if size < 0:
            raise ValueError('Size {0:n} out of range'.format(size))
        if sys.maxsize <= size:
            raise OverflowError('Size {0:n} too large'.format(size))
        block = 缓冲包装._heap.malloc(size)
        self._state = (block, size)
        util.Finalize(self, 缓冲包装._heap.free, args=(block,))

    def create_memoryview(self):
        (arena, start, stop), size = self._state
        return memoryview(arena.buffer)[start:start + size]


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BufferWrapper': '缓冲包装',
    'Heap': '堆',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '缓冲包装',
]

# ---- 转发层结束 ----
