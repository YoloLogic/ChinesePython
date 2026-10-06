# -*- coding: utf-8 -*-
"""平台信息 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`platform`（platform 的公开 API 整片是 mock.patch.object 的目标（D-093）⇒ 深拷贝不行；薄壳不动真模块，补丁照旧落得上）。
改名字 = 改 `tools\库词表.py` 里的 `包装层["platform"]`，然后：

    python tools\汉化包装层.py platform

可逆性：删这个文件 + 删词表那一段，英文 `platform` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import platform as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
架构 = __英文模块.architecture
freedesktop系统标识 = __英文模块.freedesktop_os_release
Java版本 = __英文模块.java_ver
libc版本 = __英文模块.libc_ver
macOS版本 = __英文模块.mac_ver
机器类型 = __英文模块.machine
主机名 = __英文模块.node
处理器 = __英文模块.processor
Python构建 = __英文模块.python_build
Python编译器 = __英文模块.python_compiler
Python实现 = __英文模块.python_implementation
Python修订 = __英文模块.python_revision
Python版本 = __英文模块.python_version
Python版本三元组 = __英文模块.python_version_tuple
内核发行版 = __英文模块.release
系统 = __英文模块.system
系统别名 = __英文模块.system_alias
取uname = __英文模块.uname
uname结果 = __英文模块.uname_result
版本 = __英文模块.version
Windows版本版 = __英文模块.win32_edition
是Windows物联网版吗 = __英文模块.win32_is_iot
Windows版本 = __英文模块.win32_ver

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
architecture = __英文模块.architecture
freedesktop_os_release = __英文模块.freedesktop_os_release
java_ver = __英文模块.java_ver
libc_ver = __英文模块.libc_ver
mac_ver = __英文模块.mac_ver
machine = __英文模块.machine
node = __英文模块.node
processor = __英文模块.processor
python_build = __英文模块.python_build
python_compiler = __英文模块.python_compiler
python_implementation = __英文模块.python_implementation
python_revision = __英文模块.python_revision
python_version = __英文模块.python_version
python_version_tuple = __英文模块.python_version_tuple
release = __英文模块.release
system = __英文模块.system
system_alias = __英文模块.system_alias
uname = __英文模块.uname
uname_result = __英文模块.uname_result
version = __英文模块.version
win32_edition = __英文模块.win32_edition
win32_is_iot = __英文模块.win32_is_iot
win32_ver = __英文模块.win32_ver

__all__ = [
    'architecture',
    'freedesktop_os_release',
    'java_ver',
    'libc_ver',
    'mac_ver',
    'machine',
    'node',
    'processor',
    'python_build',
    'python_compiler',
    'python_implementation',
    'python_revision',
    'python_version',
    'python_version_tuple',
    'release',
    'system',
    'system_alias',
    'uname',
    'uname_result',
    'version',
    'win32_edition',
    'win32_is_iot',
    'win32_ver',
    '架构',
    'freedesktop系统标识',
    'Java版本',
    'libc版本',
    'macOS版本',
    '机器类型',
    '主机名',
    '处理器',
    'Python构建',
    'Python编译器',
    'Python实现',
    'Python修订',
    'Python版本',
    'Python版本三元组',
    '内核发行版',
    '系统',
    '系统别名',
    '取uname',
    'uname结果',
    '版本',
    'Windows版本版',
    '是Windows物联网版吗',
    'Windows版本',
]


def __getattr__(名):
    """兜底转发：没在这儿显式列出来的名字（含私有名）照样到得了 C 那边。

    为什么必须有：硬约束是「英文原名一个都不能少」，而 C 模块的内部名
    我们没法一个个预料 —— 官方测试碰得到的、`dir(zlib)` 里有的一切，
    靠这一条全部兜住（PEP 562 的模块级 `__getattr__`）。
    """
    return getattr(__英文模块, 名)


def __dir__():
    # `dir()` 两边都算上：Shell 补全 / 官方那种按 `dir()` 算的判据都看得见。
    # ⚠ **壳自己的辅助函数不列**（D-147）：官方 `test_signal.test_functions_module_attr`
    #   会遍历 `dir()`，要求每个「非内置函数」的 `__module__` 是英文模块名 ——
    #   壳里的 `__getattr__`/`__dir__` 是 Python 函数、`__module__` 是汉语模块名
    #   ⇒ 列出来就挂（实测）。
    return sorted((set(globals()) | set(dir(__英文模块)))
                  - {"__getattr__", "__dir__", "__英文模块"})
