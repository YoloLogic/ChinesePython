# -*- coding: utf-8 -*-
"""压缩包导入 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`zipimport`（导入机制启动期就把英文那份 `zipimporter` 绑进了 `sys.path_hooks` ⇒ 深拷贝会造出第二个 `ZipImportError`，只能整模块**身份别名**（D-149））。
改名字 = 改 `tools\库词表.py` 里的 `包装层["zipimport"]`，然后：

    python tools\汉化包装层.py zipimport

可逆性：删这个文件 + 删词表那一段，英文 `zipimport` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import zipimport as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
中央目录定位器长度64 = __英文模块.END_CENTRAL_DIR_LOCATOR_SIZE_64
中央目录长度 = __英文模块.END_CENTRAL_DIR_SIZE
中央目录长度64 = __英文模块.END_CENTRAL_DIR_SIZE_64
最大注释长度 = __英文模块.MAX_COMMENT_LEN
最大无符号32位 = __英文模块.MAX_UINT32
归档结束串 = __英文模块.STRING_END_ARCHIVE
定位器结束串64 = __英文模块.STRING_END_LOCATOR_64
ZIP64结束串 = __英文模块.STRING_END_ZIP_64
ZIP64扩展标签 = __英文模块.ZIP64_EXTRA_TAG
压缩包导入错误 = __英文模块.ZipImportError
备用路径分隔符 = __英文模块.alt_path_sep
CP437表 = __英文模块.cp437_table
路径分隔符 = __英文模块.path_sep
压缩包导入器 = __英文模块.zipimporter

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
END_CENTRAL_DIR_LOCATOR_SIZE_64 = __英文模块.END_CENTRAL_DIR_LOCATOR_SIZE_64
END_CENTRAL_DIR_SIZE = __英文模块.END_CENTRAL_DIR_SIZE
END_CENTRAL_DIR_SIZE_64 = __英文模块.END_CENTRAL_DIR_SIZE_64
MAX_COMMENT_LEN = __英文模块.MAX_COMMENT_LEN
MAX_UINT32 = __英文模块.MAX_UINT32
STRING_END_ARCHIVE = __英文模块.STRING_END_ARCHIVE
STRING_END_LOCATOR_64 = __英文模块.STRING_END_LOCATOR_64
STRING_END_ZIP_64 = __英文模块.STRING_END_ZIP_64
ZIP64_EXTRA_TAG = __英文模块.ZIP64_EXTRA_TAG
ZipImportError = __英文模块.ZipImportError
alt_path_sep = __英文模块.alt_path_sep
cp437_table = __英文模块.cp437_table
path_sep = __英文模块.path_sep
zipimporter = __英文模块.zipimporter

__all__ = [
    'END_CENTRAL_DIR_LOCATOR_SIZE_64',
    'END_CENTRAL_DIR_SIZE',
    'END_CENTRAL_DIR_SIZE_64',
    'MAX_COMMENT_LEN',
    'MAX_UINT32',
    'STRING_END_ARCHIVE',
    'STRING_END_LOCATOR_64',
    'STRING_END_ZIP_64',
    'ZIP64_EXTRA_TAG',
    'ZipImportError',
    'alt_path_sep',
    'cp437_table',
    'path_sep',
    'zipimporter',
    '中央目录定位器长度64',
    '中央目录长度',
    '中央目录长度64',
    '最大注释长度',
    '最大无符号32位',
    '归档结束串',
    '定位器结束串64',
    'ZIP64结束串',
    'ZIP64扩展标签',
    '压缩包导入错误',
    '备用路径分隔符',
    'CP437表',
    '路径分隔符',
    '压缩包导入器',
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
