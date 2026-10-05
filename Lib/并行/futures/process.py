# -*- coding: utf-8 -*-
"""并行.futures/process —— 汉语库（由 tools/汉化库.py 从 Lib/concurrent/futures/process.py 机械生成，**不要手改**）。

英文库 Lib/concurrent.futures/process.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py concurrent
"""


"""Implements ProcessPoolExecutor.

The following diagram and text describe the data-flow through the system:

|======================= In-process =====================|== Out-of-process ==|

+----------+     +----------+       +--------+     +-----------+    +---------+
|          |  => | Work Ids |       |        |     | Call Q    |    | Process |
|          |     +----------+       |        |     +-----------+    |  Pool   |
|          |     | ...      |       |        |     | ...       |    +---------+
|          |     | 6        |    => |        |  => | 5, call() | => |         |
|          |     | 7        |       |        |     | ...       |    |         |
| Process  |     | ...      |       | Local  |     +-----------+    | Process |
|  Pool    |     +----------+       | Worker |                      |  #1..n  |
| Executor |                        | Thread |                      |         |
|          |     +----------- +     |        |     +-----------+    |         |
|          | <=> | Work Items | <=> |        | <=  | Result Q  | <= |         |
|          |     +------------+     |        |     +-----------+    |         |
|          |     | 6: call()  |     |        |     | ...       |    |         |
|          |     |    future  |     |        |     | 4, result |    |         |
|          |     | ...        |     |        |     | 3, except |    |         |
+----------+     +------------+     +--------+     +-----------+    +---------+

Executor.submit() called:
- creates a uniquely numbered _WorkItem and adds it to the "Work Items" dict
- adds the id of the _WorkItem to the "Work Ids" queue

Local worker thread:
- reads work ids from the "Work Ids" queue and looks up the corresponding
  WorkItem from the "Work Items" dict: if the work item has been cancelled then
  it is simply removed from the dict, otherwise it is repackaged as a
  _CallItem and put in the "Call Q". New _CallItems are put in the "Call Q"
  until "Call Q" is full. NOTE: the size of the "Call Q" is kept small because
  calls placed in the "Call Q" can no longer be cancelled with Future.cancel().
- reads _ResultItems from "Result Q", updates the future stored in the
  "Work Items" dict and deletes the dict entry

Process #1..n:
- reads _CallItems from "Call Q", executes the calls, and puts the resulting
  _ResultItems in "Result Q"
"""
_英文原名表 = {'BrokenProcessPool': '进程池损坏错误', 'EXTRA_QUEUED_CALLS': '额外排队数'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__author__ = 'Brian Quinlan (brian@sweetapp.com)'
import os
from 并行.futures import _base
import queue
import multiprocessing as mp
import multiprocessing.connection
from multiprocessing.queues import Queue
import threading
import weakref
from functools import partial
import itertools
import sys
from traceback import format_exception
_threads_wakeups = weakref.WeakKeyDictionary()
_global_shutdown = False

class _ThreadWakeup:

    def __init__(self):
        self._closed = False
        self._lock = threading.Lock()
        self._reader, self._writer = mp.Pipe(duplex=False)

    def close(self):
        with self._lock:
            if not self._closed:
                self._closed = True
                self._writer.close()
                self._reader.close()

    def wakeup(self):
        with self._lock:
            if not self._closed:
                self._writer.send_bytes(b'')

    def clear(self):
        if self._closed:
            raise RuntimeError('operation on closed _ThreadWakeup')
        while self._reader.poll():
            self._reader.recv_bytes()

def _python_exit():
    global _global_shutdown
    _global_shutdown = True
    items = list(_threads_wakeups.items())
    for _, thread_wakeup in items:
        thread_wakeup.wakeup()
    for t, _ in items:
        t.join()
threading._register_atexit(_python_exit)
额外排队数 = 1
_MAX_WINDOWS_WORKERS = 63 - 2

class _RemoteTraceback(Exception):

    def __init__(self, tb):
        self.tb = tb

    def __str__(self):
        return self.tb

class _ExceptionWithTraceback:

    def __init__(self, exc, tb):
        tb = ''.join(format_exception(type(exc), exc, tb))
        self.exc = exc
        self.exc.__traceback__ = None
        self.tb = '\n"""\n%s"""' % tb

    def __reduce__(self):
        return (_rebuild_exc, (self.exc, self.tb))

def _rebuild_exc(exc, tb):
    exc.__cause__ = _RemoteTraceback(tb)
    return exc

class _WorkItem(object):

    def __init__(self, future, fn, args, kwargs):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

class _ResultItem(object):

    def __init__(self, work_id, exception=None, result=None, exit_pid=None):
        self.work_id = work_id
        self.exception = exception
        self.result = result
        self.exit_pid = exit_pid

class _CallItem(object):

    def __init__(self, work_id, fn, args, kwargs):
        self.work_id = work_id
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

class _SafeQueue(Queue):
    """Safe Queue set exception to the future object linked to a job"""

    def __init__(self, max_size=0, *, ctx, pending_work_items, thread_wakeup):
        self.pending_work_items = pending_work_items
        self.thread_wakeup = thread_wakeup
        super().__init__(max_size, ctx=ctx)

    def _on_queue_feeder_error(self, e, obj):
        if isinstance(obj, _CallItem):
            tb = format_exception(type(e), e, e.__traceback__)
            e.__cause__ = _RemoteTraceback('\n"""\n{}"""'.format(''.join(tb)))
            work_item = self.pending_work_items.pop(obj.work_id, None)
            self.thread_wakeup.wakeup()
            if work_item is not None:
                work_item.future.set_exception(e)
        else:
            super()._on_queue_feeder_error(e, obj)

def _process_chunk(fn, chunk):
    """ Processes a chunk of an iterable passed to map.

    Runs the function passed to map() on a chunk of the
    iterable passed to map.

    This function is run in a separate process.

    """
    return [fn(*args) for args in chunk]

def _sendback_result(result_queue, work_id, result=None, exception=None, exit_pid=None):
    """Safely send back the given result or exception"""
    try:
        result_queue.put(_ResultItem(work_id, result=result, exception=exception, exit_pid=exit_pid))
    except BaseException as e:
        exc = _ExceptionWithTraceback(e, e.__traceback__)
        result_queue.put(_ResultItem(work_id, exception=exc, exit_pid=exit_pid))

def _process_worker(call_queue, result_queue, initializer, initargs, max_tasks=None):
    """Evaluates calls from call_queue and places the results in result_queue.

    This worker is run in a separate process.

    Args:
        call_queue: A ctx.Queue of _CallItems that will be read and
            evaluated by the worker.
        result_queue: A ctx.Queue of _ResultItems that will written
            to by the worker.
        initializer: A callable initializer, or None
        initargs: A tuple of args for the initializer
    """
    if initializer is not None:
        try:
            initializer(*initargs)
        except BaseException:
            _base.LOGGER.critical('Exception in initializer:', exc_info=True)
            return
    num_tasks = 0
    exit_pid = None
    while True:
        call_item = call_queue.get(block=True)
        if call_item is None:
            result_queue.put(os.getpid())
            return
        if max_tasks is not None:
            num_tasks += 1
            if num_tasks >= max_tasks:
                exit_pid = os.getpid()
        try:
            r = call_item.fn(*call_item.args, **call_item.kwargs)
        except BaseException as e:
            exc = _ExceptionWithTraceback(e, e.__traceback__)
            _sendback_result(result_queue, call_item.work_id, exception=exc, exit_pid=exit_pid)
        else:
            _sendback_result(result_queue, call_item.work_id, result=r, exit_pid=exit_pid)
            del r
        del call_item
        if exit_pid is not None:
            return

def _spawn_worker(mp_context, call_queue, result_queue, initializer, initargs, max_tasks_per_child, processes):
    """Start one worker process and record it in *processes* by pid."""
    p = mp_context.Process(target=_process_worker, args=(call_queue, result_queue, initializer, initargs, max_tasks_per_child))
    p.start()
    processes[p.pid] = p

class _ExecutorManagerThread(threading.Thread):
    """Manages the communication between this process and the worker processes.

    The manager is run in a local thread.

    Args:
        executor: A reference to the ProcessPoolExecutor that owns
            this thread. A weakref will be own by the manager as well as
            references to internal objects used to introspect the state of
            the executor.
    """

    def __init__(self, executor):
        self.thread_wakeup = executor._executor_manager_thread_wakeup
        self.shutdown_lock = executor._shutdown_lock

        def weakref_cb(_, thread_wakeup=self.thread_wakeup, mp_util_debug=mp.util.debug):
            mp_util_debug('Executor collected: triggering callback for QueueManager wakeup')
            thread_wakeup.wakeup()
        self.executor_reference = weakref.ref(executor, weakref_cb)
        self.processes = executor._processes
        self.call_queue = executor._call_queue
        self.result_queue = executor._result_queue
        self.work_ids_queue = executor._work_ids
        self.max_tasks_per_child = executor._max_tasks_per_child
        self.max_workers = executor._max_workers
        self.pending_work_items = executor._pending_work_items
        super().__init__()

    def run(self):
        while True:
            try:
                self.add_call_item_to_queue()
            except BaseException as exc:
                cause = format_exception(exc)
                self.terminate_broken(cause)
                return
            result_item, is_broken, cause = self.wait_result_broken_or_wakeup()
            if is_broken:
                self.terminate_broken(cause)
                return
            if result_item is not None:
                self.process_result_item(result_item)
                process_exited = result_item.exit_pid is not None
                if process_exited:
                    p = self.processes.pop(result_item.exit_pid)
                    p.join()
                del result_item
                if process_exited:
                    with self.shutdown_lock:
                        broken = self._replace_dead_worker()
                    if broken is not None:
                        self.terminate_broken(*broken)
                        return
                elif (executor := self.executor_reference()):
                    executor._idle_worker_semaphore.release()
                    del executor
            if self.is_shutting_down():
                self.flag_executor_shutting_down()
                self.add_call_item_to_queue()
                if not self.pending_work_items:
                    self.join_executor_internals()
                    return

    def _replace_dead_worker(self):
        """Spawn a replacement for a worker that exited at its
        max_tasks_per_child limit.  Called under self.shutdown_lock.

        Returns None while the pool can still make progress, otherwise a
        (cause, message) tuple describing why the remaining work items can
        never run, so that run() can fail their futures.
        """
        assert self.shutdown_lock.locked()
        cause = None
        message = None
        executor = self.executor_reference()
        if executor is None:
            message = 'The ProcessPoolExecutor was garbage collected with work pending after its last worker process exited upon reaching max_tasks_per_child; the pending work can never be run.'
        elif executor._force_shutting_down:
            message = 'A worker process exited while the pool was being forcefully shut down; work that was still enqueued will not be run.'
        elif self.pending_work_items or not self.is_shutting_down():
            if len(self.processes) < self.max_workers:
                try:
                    _spawn_worker(executor._mp_context, self.call_queue, self.result_queue, executor._initializer, executor._initargs, self.max_tasks_per_child, self.processes)
                except Exception as exc:
                    cause = format_exception(exc)
                    message = 'A replacement worker process could not be started, leaving the pool without workers to run the remaining work.'
        del executor
        if not self.processes and (self.pending_work_items or cause is not None):
            return (cause, message)
        return None

    def add_call_item_to_queue(self):
        while True:
            if self.call_queue.full():
                return
            try:
                work_id = self.work_ids_queue.get(block=False)
            except queue.Empty:
                return
            else:
                work_item = self.pending_work_items[work_id]
                if work_item.future.set_running_or_notify_cancel():
                    self.call_queue.put(_CallItem(work_id, work_item.fn, work_item.args, work_item.kwargs), block=True)
                else:
                    del self.pending_work_items[work_id]
                    continue

    def wait_result_broken_or_wakeup(self):
        result_reader = self.result_queue._reader
        assert not self.thread_wakeup._closed
        wakeup_reader = self.thread_wakeup._reader
        readers = [result_reader, wakeup_reader]
        worker_sentinels = [p.sentinel for p in list(self.processes.values())]
        ready = mp.connection.wait(readers + worker_sentinels)
        cause = None
        is_broken = True
        result_item = None
        if result_reader in ready:
            try:
                result_item = result_reader.recv()
                is_broken = False
            except BaseException as exc:
                cause = format_exception(exc)
        elif wakeup_reader in ready:
            is_broken = False
        self.thread_wakeup.clear()
        return (result_item, is_broken, cause)

    def process_result_item(self, result_item):
        work_item = self.pending_work_items.pop(result_item.work_id, None)
        if work_item is not None:
            if result_item.exception is not None:
                work_item.future.set_exception(result_item.exception)
            else:
                work_item.future.set_result(result_item.result)

    def is_shutting_down(self):
        executor = self.executor_reference()
        return _global_shutdown or executor is None or executor._shutdown_thread

    def _terminate_broken(self, cause, bpe_message=None):
        executor = self.executor_reference()
        if executor is not None:
            executor._broken = 'A child process terminated abruptly, the process pool is not usable anymore'
            executor._shutdown_thread = True
            executor = None
        cause_tb = None
        if cause is not None:
            cause_tb = f"\n'''\n{''.join(cause)}'''"
        if bpe_message is None:
            bpe_message = 'A process in the process pool was terminated abruptly while the future was running or pending.'
        for work_id, work_item in self.pending_work_items.items():
            bpe = 进程池损坏错误(bpe_message)
            if cause_tb is not None:
                bpe.__cause__ = _RemoteTraceback(cause_tb)
            try:
                work_item.future.set_exception(bpe)
            except _base.InvalidStateError:
                pass
            del work_item
        self.pending_work_items.clear()
        for p in self.processes.values():
            p.terminate()
        self.call_queue._terminate_broken()
        self._join_executor_internals(broken=True)

    def terminate_broken(self, cause, bpe_message=None):
        with self.shutdown_lock:
            self._terminate_broken(cause, bpe_message)

    def flag_executor_shutting_down(self):
        executor = self.executor_reference()
        if executor is not None:
            executor._shutdown_thread = True
            if executor._cancel_pending_futures:
                new_pending_work_items = {}
                for work_id, work_item in self.pending_work_items.items():
                    if not work_item.future.cancel():
                        new_pending_work_items[work_id] = work_item
                self.pending_work_items = new_pending_work_items
                while True:
                    try:
                        self.work_ids_queue.get_nowait()
                    except queue.Empty:
                        break
                executor._cancel_pending_futures = False

    def shutdown_workers(self):
        n_children_to_stop = self.get_n_children_alive()
        n_sentinels_sent = 0
        while n_sentinels_sent < n_children_to_stop and self.get_n_children_alive() > 0:
            for i in range(n_children_to_stop - n_sentinels_sent):
                try:
                    self.call_queue.put_nowait(None)
                    n_sentinels_sent += 1
                except queue.Full:
                    break

    def join_executor_internals(self):
        with self.shutdown_lock:
            self._join_executor_internals()

    def _join_executor_internals(self, broken=False):
        if not broken:
            self.shutdown_workers()
        self.call_queue.close()
        self.call_queue.join_thread()
        self.thread_wakeup.close()
        for p in self.processes.values():
            if broken:
                p.terminate()
            p.join()

    def get_n_children_alive(self):
        return sum((p.is_alive() for p in self.processes.values()))
_system_limits_checked = False
_system_limited = None

def _check_system_limits():
    global _system_limits_checked, _system_limited
    if _system_limits_checked:
        if _system_limited:
            raise NotImplementedError(_system_limited)
    _system_limits_checked = True
    try:
        import multiprocessing.synchronize
    except ImportError:
        _system_limited = 'This Python build lacks multiprocessing.synchronize, usually due to named semaphores being unavailable on this platform.'
        raise NotImplementedError(_system_limited)
    try:
        nsems_max = os.sysconf('SC_SEM_NSEMS_MAX')
    except (AttributeError, ValueError):
        return
    if nsems_max == -1:
        return
    if nsems_max >= 256:
        return
    _system_limited = 'system provides too few semaphores (%d available, 256 necessary)' % nsems_max
    raise NotImplementedError(_system_limited)

def _chain_from_iterable_of_lists(iterable):
    """
    Specialized implementation of itertools.chain.from_iterable.
    Each item in *iterable* should be a list.  This function is
    careful not to keep references to yielded objects.
    """
    for element in iterable:
        element.reverse()
        while element:
            yield element.pop()

class 进程池损坏错误(_base.BrokenExecutor):
    """
    Raised when a process in a ProcessPoolExecutor terminated abruptly
    while a future was in the running state.
    """
_TERMINATE = 'terminate'
_KILL = 'kill'
_SHUTDOWN_CALLBACK_OPERATION = {_TERMINATE, _KILL}

class ProcessPoolExecutor(_base.Executor):

    def __init__(self, max_workers=None, mp_context=None, initializer=None, initargs=(), *, max_tasks_per_child=None):
        """Initializes a new ProcessPoolExecutor instance.

        Args:
            max_workers: The maximum number of processes that can be used to
                execute the given calls.  If None or not given then as many
                worker processes will be created as the machine has
                processors.
            mp_context: A multiprocessing context to launch the workers
                created using the multiprocessing.get_context('start method')
                API.  This object should provide SimpleQueue, Queue and
                Process.
            initializer: A callable used to initialize worker processes.
            initargs: A tuple of arguments to pass to the initializer.
            max_tasks_per_child: The maximum number of tasks a worker
                process can complete before it will exit and be replaced
                with a fresh worker process.  The default of None means
                worker process will live as long as the executor.  Requires
                a non-'fork' mp_context start method.  When given, we
                default to using 'spawn' if no mp_context is supplied.
        """
        _check_system_limits()
        if max_workers is None:
            self._max_workers = os.process_cpu_count() or 1
            if sys.platform == 'win32':
                self._max_workers = min(_MAX_WINDOWS_WORKERS, self._max_workers)
        else:
            if max_workers <= 0:
                raise ValueError('max_workers must be greater than 0')
            elif sys.platform == 'win32' and max_workers > _MAX_WINDOWS_WORKERS:
                raise ValueError(f'max_workers must be <= {_MAX_WINDOWS_WORKERS}')
            self._max_workers = max_workers
        if mp_context is None:
            if max_tasks_per_child is not None:
                mp_context = mp.get_context('spawn')
            else:
                mp_context = mp.get_context()
        self._mp_context = mp_context
        self._safe_to_dynamically_spawn_children = self._mp_context.get_start_method(allow_none=False) != 'fork'
        if initializer is not None and (not callable(initializer)):
            raise TypeError('initializer must be a callable')
        self._initializer = initializer
        self._initargs = initargs
        if max_tasks_per_child is not None:
            if not isinstance(max_tasks_per_child, int):
                raise TypeError('max_tasks_per_child must be an integer')
            elif max_tasks_per_child <= 0:
                raise ValueError('max_tasks_per_child must be >= 1')
            if self._mp_context.get_start_method(allow_none=False) == 'fork':
                raise ValueError("max_tasks_per_child is incompatible with the 'fork' multiprocessing start method; supply a different mp_context.")
        self._max_tasks_per_child = max_tasks_per_child
        self._executor_manager_thread = None
        self._processes = {}
        self._shutdown_thread = False
        self._shutdown_lock = threading.Lock()
        self._idle_worker_semaphore = threading.Semaphore(0)
        self._broken = False
        self._queue_count = 0
        self._pending_work_items = {}
        self._cancel_pending_futures = False
        self._force_shutting_down = False
        self._executor_manager_thread_wakeup = _ThreadWakeup()
        queue_size = self._max_workers + 额外排队数
        self._call_queue = _SafeQueue(max_size=queue_size, ctx=self._mp_context, pending_work_items=self._pending_work_items, thread_wakeup=self._executor_manager_thread_wakeup)
        self._call_queue._ignore_epipe = True
        self._result_queue = mp_context.SimpleQueue()
        self._work_ids = queue.Queue()

    def _start_executor_manager_thread(self):
        if self._executor_manager_thread is None:
            if not self._safe_to_dynamically_spawn_children:
                self._launch_processes()
            self._executor_manager_thread = _ExecutorManagerThread(self)
            self._executor_manager_thread.start()
            _threads_wakeups[self._executor_manager_thread] = self._executor_manager_thread_wakeup

    def _adjust_process_count(self):
        if self._processes is None:
            return
        if self._force_shutting_down:
            return
        if self._idle_worker_semaphore.acquire(blocking=False):
            return
        process_count = len(self._processes)
        if process_count < self._max_workers:
            assert self._safe_to_dynamically_spawn_children or not self._executor_manager_thread, 'https://github.com/python/cpython/issues/90622'
            self._spawn_process()

    def _launch_processes(self):
        assert not self._executor_manager_thread, 'Processes cannot be fork()ed after the thread has started, deadlock in the child processes could result.'
        for _ in range(len(self._processes), self._max_workers):
            self._spawn_process()

    def _spawn_process(self):
        _spawn_worker(self._mp_context, self._call_queue, self._result_queue, self._initializer, self._initargs, self._max_tasks_per_child, self._processes)

    def submit(self, fn, /, *args, **kwargs):
        with self._shutdown_lock:
            if self._broken:
                raise 进程池损坏错误(self._broken)
            if self._shutdown_thread:
                raise RuntimeError('cannot schedule new futures after shutdown')
            if _global_shutdown:
                raise RuntimeError('cannot schedule new futures after interpreter shutdown')
            f = _base.Future()
            w = _WorkItem(f, fn, args, kwargs)
            self._pending_work_items[self._queue_count] = w
            self._work_ids.put(self._queue_count)
            self._queue_count += 1
            self._executor_manager_thread_wakeup.wakeup()
            if self._safe_to_dynamically_spawn_children:
                self._adjust_process_count()
            self._start_executor_manager_thread()
            return f
    submit.__doc__ = _base.Executor.submit.__doc__

    def map(self, fn, *iterables, timeout=None, chunksize=1, buffersize=None):
        """Returns an iterator equivalent to map(fn, iter).

        Args:
            fn: A callable that will take as many arguments as there are
                passed iterables.
            timeout: The maximum number of seconds to wait.  If None, then
                there is no limit on the wait time.
            chunksize: If greater than one, the iterables will be chopped
                into chunks of size chunksize and submitted to the process
                pool.  If set to one, the items in the list will be sent
                one at a time.
            buffersize: The number of submitted tasks whose results have not
                yet been yielded.  If the buffer is full, iteration over the
                iterables pauses until a result is yielded from the buffer.
                If None, all input elements are eagerly collected, and
                a task is submitted for each.

        Returns:
            An iterator equivalent to: map(func, *iterables) but the calls
            may be evaluated out-of-order.

        Raises:
            TimeoutError: If the entire result iterator could not be
                generated before the given timeout.
            Exception: If fn(*args) raises for any values.
        """
        if chunksize < 1:
            raise ValueError('chunksize must be >= 1.')
        results = super().map(partial(_process_chunk, fn), itertools.batched(zip(*iterables), chunksize), timeout=timeout, buffersize=buffersize)
        return _chain_from_iterable_of_lists(results)

    def shutdown(self, wait=True, *, cancel_futures=False):
        with self._shutdown_lock:
            self._cancel_pending_futures = cancel_futures
            self._shutdown_thread = True
            if self._executor_manager_thread_wakeup is not None:
                self._executor_manager_thread_wakeup.wakeup()
        if self._executor_manager_thread is not None and wait:
            self._executor_manager_thread.join()
        self._executor_manager_thread = None
        self._call_queue = None
        if self._result_queue is not None and wait:
            self._result_queue.close()
        self._result_queue = None
        self._processes = None
        self._executor_manager_thread_wakeup = None
    shutdown.__doc__ = _base.Executor.shutdown.__doc__

    def _force_shutdown(self, operation):
        """Attempts to terminate or kill the executor's workers based off the
        given operation. Iterates through all of the current processes and
        performs the relevant task if the process is still alive.

        After terminating workers, the pool will be in a broken state
        and no longer usable (for instance, new tasks should not be
        submitted).
        """
        if operation not in _SHUTDOWN_CALLBACK_OPERATION:
            raise ValueError(f'Unsupported operation: {operation!r}')
        with self._shutdown_lock:
            self._force_shutting_down = True
        processes = {}
        if self._processes:
            processes = self._processes.copy()
        self.shutdown(wait=False, cancel_futures=True)
        if not processes:
            return
        for proc in processes.values():
            try:
                if not proc.is_alive():
                    continue
            except ValueError:
                continue
            try:
                if operation == _TERMINATE:
                    proc.terminate()
                elif operation == _KILL:
                    proc.kill()
            except ProcessLookupError:
                continue

    def terminate_workers(self):
        """Attempts to terminate the executor's workers.
        Iterates through all of the current worker processes and terminates
        each one that is still alive.

        After terminating workers, the pool will be in a broken state
        and no longer usable (for instance, new tasks should not be
        submitted).
        """
        return self._force_shutdown(operation=_TERMINATE)

    def kill_workers(self):
        """Attempts to kill the executor's workers.
        Iterates through all of the current worker processes and kills
        each one that is still alive.

        After killing workers, the pool will be in a broken state
        and no longer usable (for instance, new tasks should not be
        submitted).
        """
        return self._force_shutdown(operation=_KILL)


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
    '进程池执行器': 'ProcessPoolExecutor',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'BrokenProcessPool': '进程池损坏错误',
    'EXTRA_QUEUED_CALLS': '额外排队数',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
