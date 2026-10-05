# -*- coding: utf-8 -*-
"""正则._compiler —— 由 `tools\汉化库.py` 机械生成的**薄转发**（D-146），别手改。

英文模块：`re._compiler`（**不深拷贝**，名字全部指过去）
为什么：`_sre` 把 `re._compile_template` 缓存在**进程级**（D-145），深拷贝一份会自相矛盾

中文名一个都不改、一个都不加 —— 这个壳只做一件事：让 `正则._compiler` 这个**包内名字**
指向**同一批对象**（`is` 判据成立）。跟机制 4 给纯 C 模块造的壳同一个路子。
"""

import re._compiler as __英文模块

# 名字全部指向**同一个对象**（不是复制一份）：跳过 `__` 开头的（那是导入机制自己生的）。
globals().update({_名: _值 for _名, _值 in vars(__英文模块).items() if not _名.startswith("__")})
if hasattr(__英文模块, "__all__"):
    __all__ = list(__英文模块.__all__)


def __getattr__(名):
    """兜底转发：没显式列出来的名字（含私有名）照样到得了英文那边。"""
    return getattr(__英文模块, 名)


def __dir__():
    return sorted(set(globals()) | set(dir(__英文模块)))
