# -*- coding: utf-8 -*-
"""内存追踪 —— 汉语库（由 tools/汉化库.py 从 Lib/tracemalloc.py 机械生成，**不要手改**）。

英文库 Lib/tracemalloc.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 内存追踪
"""


_英文原名表 = {'BaseFilter': '过滤器基类', 'DomainFilter': '域过滤器', 'Filter': '过滤器', 'Frame': '帧', 'Snapshot': '快照', 'Statistic': '统计项', 'StatisticDiff': '统计差异项', 'Trace': '追踪记录', 'Traceback': '回溯', 'get_object_traceback': '取对象回溯', 'take_snapshot': '取快照'}

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
from collections.abc import Sequence, Iterable
from functools import total_ordering
import fnmatch
import linecache
import os.path
import pickle
from _tracemalloc import *
from _tracemalloc import _get_object_traceback, _get_traces

def _format_size(size, sign):
    for unit in ('B', 'KiB', 'MiB', 'GiB', 'TiB'):
        if abs(size) < 100 and unit != 'B':
            if sign:
                return '%+.1f %s' % (size, unit)
            else:
                return '%.1f %s' % (size, unit)
        if abs(size) < 10 * 1024 or unit == 'TiB':
            if sign:
                return '%+.0f %s' % (size, unit)
            else:
                return '%.0f %s' % (size, unit)
        size /= 1024

class 统计项:
    """
    Statistic difference on memory allocations between two Snapshot instance.
    """
    __slots__ = ('traceback', 'size', 'count')

    def __init__(self, traceback, size, count):
        self.回溯信息 = traceback
        self.大小 = size
        self.count = count

    def __hash__(self):
        return hash((self.回溯信息, self.大小, self.count))

    def __eq__(self, other):
        if not isinstance(other, 统计项):
            return NotImplemented
        return self.回溯信息 == other.traceback and self.大小 == other.size and (self.count == other.count)

    def __str__(self):
        text = '%s: size=%s, count=%i' % (self.回溯信息, _format_size(self.大小, False), self.count)
        if self.count:
            average = self.大小 / self.count
            text += ', average=%s' % _format_size(average, False)
        return text

    def __repr__(self):
        return '<Statistic traceback=%r size=%i count=%i>' % (self.回溯信息, self.大小, self.count)

    def _sort_key(self):
        return (self.大小, self.count, self.回溯信息)
_装类转发(统计项, {}, {'count': '个数', 'size': '大小', 'traceback': '回溯信息'})

class 统计差异项:
    """
    Statistic difference on memory allocations between an old and a new
    Snapshot instance.
    """
    __slots__ = ('traceback', 'size', 'size_diff', 'count', 'count_diff')

    def __init__(self, traceback, size, size_diff, count, count_diff):
        self.回溯信息 = traceback
        self.大小 = size
        self.大小差 = size_diff
        self.count = count
        self.个数差 = count_diff

    def __hash__(self):
        return hash((self.回溯信息, self.大小, self.大小差, self.count, self.个数差))

    def __eq__(self, other):
        if not isinstance(other, 统计差异项):
            return NotImplemented
        return self.回溯信息 == other.traceback and self.大小 == other.size and (self.大小差 == other.size_diff) and (self.count == other.count) and (self.个数差 == other.count_diff)

    def __str__(self):
        text = '%s: size=%s (%s), count=%i (%+i)' % (self.回溯信息, _format_size(self.大小, False), _format_size(self.大小差, True), self.count, self.个数差)
        if self.count:
            average = self.大小 / self.count
            text += ', average=%s' % _format_size(average, False)
        return text

    def __repr__(self):
        return '<StatisticDiff traceback=%r size=%i (%+i) count=%i (%+i)>' % (self.回溯信息, self.大小, self.大小差, self.count, self.个数差)

    def _sort_key(self):
        return (abs(self.大小差), self.大小, abs(self.个数差), self.count, self.回溯信息)
_装类转发(统计差异项, {}, {'count': '个数', 'count_diff': '个数差', 'size': '大小', 'size_diff': '大小差', 'traceback': '回溯信息'})

def _compare_grouped_stats(old_group, new_group):
    统计 = []
    for 回溯信息, stat in new_group.items():
        previous = old_group.pop(回溯信息, None)
        if previous is not None:
            stat = 统计差异项(回溯信息, stat.size, stat.size - previous.size, stat.count, stat.count - previous.count)
        else:
            stat = 统计差异项(回溯信息, stat.size, stat.size, stat.count, stat.count)
        统计.append(stat)
    for 回溯信息, stat in old_group.items():
        stat = 统计差异项(回溯信息, 0, -stat.size, 0, -stat.count)
        统计.append(stat)
    return 统计

@total_ordering
class 帧:
    """
    Frame of a traceback.
    """
    __slots__ = ('_frame',)

    def __init__(self, frame):
        self._frame = frame

    @property
    def 文件名(self):
        return self._frame[0]

    @property
    def 行号(self):
        return self._frame[1]

    def __eq__(self, other):
        if not isinstance(other, 帧):
            return NotImplemented
        return self._frame == other._frame

    def __lt__(self, other):
        if not isinstance(other, 帧):
            return NotImplemented
        return self._frame < other._frame

    def __hash__(self):
        return hash(self._frame)

    def __str__(self):
        return '%s:%s' % (self.文件名, self.行号)

    def __repr__(self):
        return '<Frame filename=%r lineno=%r>' % (self.文件名, self.行号)
_装类转发(帧, {'filename': '文件名', 'lineno': '行号'}, {'filename': '文件名', 'lineno': '行号'})

@total_ordering
class 回溯(Sequence):
    """
    Sequence of Frame instances sorted from the oldest frame
    to the most recent frame.
    """
    __slots__ = ('_frames', '_total_nframe')

    def __init__(self, frames, total_nframe=None):
        Sequence.__init__(self)
        self._frames = tuple(reversed(frames))
        self._total_nframe = total_nframe

    @property
    def 总帧数(self):
        return self._total_nframe

    def __len__(self):
        return len(self._frames)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return tuple((帧(trace) for trace in self._frames[index]))
        else:
            return 帧(self._frames[index])

    def __contains__(self, frame):
        return frame._frame in self._frames

    def __hash__(self):
        return hash(self._frames)

    def __eq__(self, other):
        if not isinstance(other, 回溯):
            return NotImplemented
        return self._frames == other._frames

    def __lt__(self, other):
        if not isinstance(other, 回溯):
            return NotImplemented
        return self._frames < other._frames

    def __str__(self):
        return str(self[0])

    def __repr__(self):
        s = f'<Traceback {tuple(self)}'
        if self._total_nframe is None:
            s += '>'
        else:
            s += f' total_nframe={self.总帧数}>'
        return s

    def format(self, limit=None, most_recent_first=False):
        lines = []
        if limit is not None:
            if limit > 0:
                frame_slice = self[-limit:]
            else:
                frame_slice = self[:limit]
        else:
            frame_slice = self
        if most_recent_first:
            frame_slice = reversed(frame_slice)
        for frame in frame_slice:
            lines.append('  File "%s", line %s' % (frame.filename, frame.lineno))
            line = linecache.getline(frame.filename, frame.lineno).strip()
            if line:
                lines.append('    %s' % line)
        return lines
_装类转发(回溯, {'total_nframe': '总帧数'}, {'total_nframe': '总帧数'})

def 取对象回溯(obj):
    """
    Get the traceback where the Python object *obj* was allocated.
    Return a Traceback instance.

    Return None if the tracemalloc module is not tracing memory allocations or
    did not trace the allocation of the object.
    """
    frames = _get_object_traceback(obj)
    if frames is not None:
        return 回溯(frames)
    else:
        return None

class 追踪记录:
    """
    Trace of a memory block.
    """
    __slots__ = ('_trace',)

    def __init__(self, trace):
        self._trace = trace

    @property
    def 域(self):
        return self._trace[0]

    @property
    def 大小(self):
        return self._trace[1]

    @property
    def 回溯信息(self):
        return 回溯(*self._trace[2:])

    def __eq__(self, other):
        if not isinstance(other, 追踪记录):
            return NotImplemented
        return self._trace == other._trace

    def __hash__(self):
        return hash(self._trace)

    def __str__(self):
        return '%s: %s' % (self.回溯信息, _format_size(self.大小, False))

    def __repr__(self):
        return '<Trace domain=%s size=%s, traceback=%r>' % (self.域, _format_size(self.大小, False), self.回溯信息)
_装类转发(追踪记录, {'domain': '域', 'size': '大小', 'traceback': '回溯信息'}, {'domain': '域', 'size': '大小', 'traceback': '回溯信息'})

class _Traces(Sequence):

    def __init__(self, traces):
        Sequence.__init__(self)
        self._traces = traces

    def __len__(self):
        return len(self._traces)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return tuple((追踪记录(trace) for trace in self._traces[index]))
        else:
            return 追踪记录(self._traces[index])

    def __contains__(self, trace):
        return trace._trace in self._traces

    def __eq__(self, other):
        if not isinstance(other, _Traces):
            return NotImplemented
        return self._traces == other._traces

    def __repr__(self):
        return '<Traces len=%s>' % len(self)

def _normalize_filename(filename):
    filename = os.path.normcase(filename)
    if filename.endswith('.pyc'):
        filename = filename[:-1]
    return filename

class 过滤器基类:

    def __init__(self, inclusive):
        self.包含式 = inclusive

    def _match(self, trace):
        raise NotImplementedError
_装类转发(过滤器基类, {}, {'inclusive': '包含式'})

class 过滤器(过滤器基类):

    def __init__(self, inclusive, filename_pattern, lineno=None, all_frames=False, domain=None):
        super().__init__(inclusive)
        self.包含式 = inclusive
        self._filename_pattern = _normalize_filename(filename_pattern)
        self.行号 = lineno
        self.all_frames = all_frames
        self.域 = domain

    @property
    def 文件名模式(self):
        return self._filename_pattern

    def _match_frame_impl(self, filename, lineno):
        filename = _normalize_filename(filename)
        if not fnmatch.fnmatch(filename, self._filename_pattern):
            return False
        if self.行号 is None:
            return True
        else:
            return lineno == self.行号

    def _match_frame(self, filename, lineno):
        return self._match_frame_impl(filename, lineno) ^ (not self.包含式)

    def _match_traceback(self, traceback):
        if self.all_frames:
            if any((self._match_frame_impl(文件名, 行号) for 文件名, 行号 in traceback)):
                return self.包含式
            else:
                return not self.包含式
        else:
            文件名, 行号 = traceback[0]
            return self._match_frame(文件名, 行号)

    def _match(self, trace):
        域, 大小, 回溯信息, 总帧数 = trace
        res = self._match_traceback(回溯信息)
        if self.域 is not None:
            if self.包含式:
                return res and 域 == self.域
            else:
                return res or 域 != self.域
        return res
_装类转发(过滤器, {'filename_pattern': '文件名模式'}, {'domain': '域', 'filename_pattern': '文件名模式', 'inclusive': '包含式', 'lineno': '行号'})

class 域过滤器(过滤器基类):

    def __init__(self, inclusive, domain):
        super().__init__(inclusive)
        self._domain = domain

    @property
    def 域(self):
        return self._domain

    def _match(self, trace):
        域, 大小, 回溯信息, 总帧数 = trace
        return (域 == self.域) ^ (not self.包含式)
_装类转发(域过滤器, {'domain': '域'}, {'domain': '域', 'inclusive': '包含式'})

class 快照:
    """
    Snapshot of traces of memory blocks allocated by Python.
    """

    def __init__(self, traces, traceback_limit):
        self.追踪记录表 = _Traces(traces)
        self.回溯上限 = traceback_limit

    def 转储(self, filename):
        """
        Write the snapshot into a file.
        """
        with open(filename, 'wb') as fp:
            pickle.dump(self, fp, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def 载入(filename):
        """
        Load a snapshot from a file.
        """
        with open(filename, 'rb') as fp:
            return pickle.load(fp)

    def _filter_trace(self, include_filters, exclude_filters, trace):
        if include_filters:
            if not any((trace_filter._match(trace) for trace_filter in include_filters)):
                return False
        if exclude_filters:
            if any((not trace_filter._match(trace) for trace_filter in exclude_filters)):
                return False
        return True

    def 过滤追踪(self, filters):
        """
        Create a new Snapshot instance with a filtered traces sequence, filters
        is a list of Filter or DomainFilter instances.  If filters is an empty
        list, return a new Snapshot instance with a copy of the traces.
        """
        if not isinstance(filters, Iterable):
            raise TypeError('filters must be a list of filters, not %s' % type(filters).__name__)
        if filters:
            include_filters = []
            exclude_filters = []
            for trace_filter in filters:
                if trace_filter.inclusive:
                    include_filters.append(trace_filter)
                else:
                    exclude_filters.append(trace_filter)
            new_traces = [trace for trace in self.追踪记录表._traces if self._filter_trace(include_filters, exclude_filters, trace)]
        else:
            new_traces = self.追踪记录表._traces.copy()
        return 快照(new_traces, self.回溯上限)

    def _group_by(self, key_type, cumulative):
        if key_type not in ('traceback', 'filename', 'lineno'):
            raise ValueError('unknown key_type: %r' % (key_type,))
        if cumulative and key_type not in ('lineno', 'filename'):
            raise ValueError('cumulative mode cannot by used with key type %r' % key_type)
        stats = {}
        tracebacks = {}
        if not cumulative:
            for trace in self.追踪记录表._traces:
                域, 大小, trace_traceback, 总帧数 = trace
                try:
                    回溯信息 = tracebacks[trace_traceback]
                except KeyError:
                    if key_type == 'traceback':
                        frames = trace_traceback
                    elif key_type == 'lineno':
                        frames = trace_traceback[:1]
                    else:
                        frames = ((trace_traceback[0][0], 0),)
                    回溯信息 = 回溯(frames)
                    tracebacks[trace_traceback] = 回溯信息
                try:
                    stat = stats[回溯信息]
                    stat.size += 大小
                    stat.count += 1
                except KeyError:
                    stats[回溯信息] = 统计项(回溯信息, 大小, 1)
        else:
            for trace in self.追踪记录表._traces:
                域, 大小, trace_traceback, 总帧数 = trace
                for frame in trace_traceback:
                    try:
                        回溯信息 = tracebacks[frame]
                    except KeyError:
                        if key_type == 'lineno':
                            frames = (frame,)
                        else:
                            frames = ((frame[0], 0),)
                        回溯信息 = 回溯(frames)
                        tracebacks[frame] = 回溯信息
                    try:
                        stat = stats[回溯信息]
                        stat.size += 大小
                        stat.count += 1
                    except KeyError:
                        stats[回溯信息] = 统计项(回溯信息, 大小, 1)
        return stats

    def 统计(self, key_type, cumulative=False):
        """
        Group statistics by key_type. Return a sorted list of Statistic
        instances.
        """
        grouped = self._group_by(key_type, cumulative)
        统计 = list(grouped.values())
        统计.sort(reverse=True, key=统计项._sort_key)
        return 统计

    def 比较(self, old_snapshot, key_type, cumulative=False):
        """
        Compute the differences with an old snapshot old_snapshot. Get
        statistics as a sorted list of StatisticDiff instances, grouped by
        group_by.
        """
        new_group = self._group_by(key_type, cumulative)
        old_group = old_snapshot._group_by(key_type, cumulative)
        统计 = _compare_grouped_stats(old_group, new_group)
        统计.sort(reverse=True, key=统计差异项._sort_key)
        return 统计
_装类转发(快照, {'compare_to': '比较', 'dump': '转储', 'filter_traces': '过滤追踪', 'load': '载入', 'statistics': '统计'}, {'compare_to': '比较', 'dump': '转储', 'filter_traces': '过滤追踪', 'load': '载入', 'statistics': '统计', 'traceback_limit': '回溯上限', 'traces': '追踪记录表'})

def 取快照():
    """
    Take a snapshot of traces of memory blocks allocated by Python.
    """
    if not is_tracing():
        raise RuntimeError('the tracemalloc module must be tracing memory allocations to take a snapshot')
    追踪记录表 = _get_traces()
    回溯上限 = get_traceback_limit()
    return 快照(追踪记录表, 回溯上限)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import tracemalloc as _英文库
清追踪 = _英文库.clear_traces
取回溯上限 = _英文库.get_traceback_limit
取追踪内存 = _英文库.get_traced_memory
追踪中吗 = _英文库.is_tracing
重置峰值 = _英文库.reset_peak
启动追踪 = _英文库.start
停止追踪 = _英文库.stop
_模块别名 = {
    'BaseFilter': '过滤器基类',
    'DomainFilter': '域过滤器',
    'Filter': '过滤器',
    'Frame': '帧',
    'Snapshot': '快照',
    'Statistic': '统计项',
    'StatisticDiff': '统计差异项',
    'Trace': '追踪记录',
    'Traceback': '回溯',
    'get_object_traceback': '取对象回溯',
    'take_snapshot': '取快照',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '回溯': {
        'total_nframe': '总帧数',
    },
    '域过滤器': {
        'domain': '域',
    },
    '帧': {
        'filename': '文件名',
        'lineno': '行号',
    },
    '快照': {
        'compare_to': '比较',
        'dump': '转储',
        'filter_traces': '过滤追踪',
        'load': '载入',
        'statistics': '统计',
    },
    '过滤器': {
        'filename_pattern': '文件名模式',
    },
    '追踪记录': {
        'domain': '域',
        'size': '大小',
        'traceback': '回溯信息',
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
    '回溯': {
        'total_nframe': '总帧数',
    },
    '域过滤器': {
        'domain': '域',
        'inclusive': '包含式',
    },
    '帧': {
        'filename': '文件名',
        'lineno': '行号',
    },
    '快照': {
        'compare_to': '比较',
        'dump': '转储',
        'filter_traces': '过滤追踪',
        'load': '载入',
        'statistics': '统计',
        'traceback_limit': '回溯上限',
        'traces': '追踪记录表',
    },
    '统计差异项': {
        'count': '个数',
        'count_diff': '个数差',
        'size': '大小',
        'size_diff': '大小差',
        'traceback': '回溯信息',
    },
    '统计项': {
        'count': '个数',
        'size': '大小',
        'traceback': '回溯信息',
    },
    '过滤器': {
        'domain': '域',
        'filename_pattern': '文件名模式',
        'inclusive': '包含式',
        'lineno': '行号',
    },
    '过滤器基类': {
        'inclusive': '包含式',
    },
    '追踪记录': {
        'domain': '域',
        'size': '大小',
        'traceback': '回溯信息',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
