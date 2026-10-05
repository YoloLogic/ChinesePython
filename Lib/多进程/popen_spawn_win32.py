# -*- coding: utf-8 -*-
"""多进程.popen_spawn_win32 —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/popen_spawn_win32.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.popen_spawn_win32.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


_英文原名表 = {'Popen': '进程启动器'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import os
import msvcrt
import signal
import sys
import _winapi
from subprocess import STARTUPINFO, STARTF_FORCEOFFFEEDBACK
from .context import reduction, get_spawning_popen, set_spawning_popen
from . import spawn
from . import util
__all__ = ['Popen']
TERMINATE = 65536
WINEXE = sys.platform == 'win32' and getattr(sys, 'frozen', False)
WINSERVICE = sys.executable.lower().endswith('pythonservice.exe')

def _path_eq(p1, p2):
    return p1 == p2 or os.path.normcase(p1) == os.path.normcase(p2)
WINENV = not _path_eq(sys.executable, sys._base_executable)

def _close_handles(*handles):
    for handle in handles:
        _winapi.CloseHandle(handle)

class 进程启动器(object):
    """
    Start a subprocess to run the code of a process object
    """
    method = 'spawn'

    def __init__(self, process_obj):
        prep_data = spawn.get_preparation_data(process_obj._name)
        rhandle, whandle = _winapi.CreatePipe(None, 0)
        wfd = msvcrt.open_osfhandle(whandle, 0)
        cmd = spawn.get_command_line(parent_pid=os.getpid(), pipe_handle=rhandle)
        python_exe = spawn.get_executable()
        if WINENV and _path_eq(python_exe, sys.executable):
            cmd[0] = python_exe = sys._base_executable
            env = os.environ.copy()
            env['__PYVENV_LAUNCHER__'] = sys.executable
        else:
            env = None
        cmd = ' '.join(('"%s"' % x for x in cmd))
        with open(wfd, 'wb', closefd=True) as to_child:
            try:
                hp, ht, pid, tid = _winapi.CreateProcess(python_exe, cmd, None, None, False, 0, env, None, STARTUPINFO(dwFlags=STARTF_FORCEOFFFEEDBACK))
                _winapi.CloseHandle(ht)
            except:
                _winapi.CloseHandle(rhandle)
                raise
            self.pid = pid
            self.returncode = None
            self._handle = hp
            self.sentinel = int(hp)
            self.finalizer = util.Finalize(self, _close_handles, (self.sentinel, int(rhandle)))
            set_spawning_popen(self)
            try:
                reduction.dump(prep_data, to_child)
                reduction.dump(process_obj, to_child)
            finally:
                set_spawning_popen(None)

    def duplicate_for_child(self, handle):
        assert self is get_spawning_popen()
        return reduction.duplicate(handle, self.sentinel)

    def wait(self, timeout=None):
        if self.returncode is not None:
            return self.returncode
        if timeout is None:
            msecs = _winapi.INFINITE
        else:
            msecs = max(0, int(timeout * 1000 + 0.5))
        res = _winapi.WaitForSingleObject(int(self._handle), msecs)
        if res == _winapi.WAIT_OBJECT_0:
            code = _winapi.GetExitCodeProcess(self._handle)
            if code == TERMINATE:
                code = -signal.SIGTERM
            self.returncode = code
        return self.returncode

    def poll(self):
        return self.wait(timeout=0)

    def terminate(self):
        if self.returncode is not None:
            return
        try:
            _winapi.TerminateProcess(int(self._handle), TERMINATE)
        except PermissionError:
            code = _winapi.GetExitCodeProcess(int(self._handle))
            if code == _winapi.STILL_ACTIVE:
                raise
    kill = terminate

    def close(self):
        self.finalizer()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Popen': '进程启动器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '进程启动器',
])

# ---- 转发层结束 ----
