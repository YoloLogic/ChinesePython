# -*- coding: utf-8 -*-
"""导入机制 —— 由 `tools\汉化库.py` 机械生成的**薄壳**（D-182），别手改。

英文模块：`importlib`（**不深拷贝**：中文名是**别名**，跟英文名指向同一个对象）
为什么：导入机械不能有两份（D-163）；包级可翻名字只有 3 个，薄壳是唯一无损路线（D-183）

⚠ 薄壳 = **包级名字 + 子模块名都指向英文那份同一个对象**（D-183）：
  * `globals().update(英文公开名)` + `__path__ = 英文.__path__`
  * 子模块**先真导入一遍再挂到 `sys.modules[汉语名.子模块]`** —— 少了这一句，
    `import 导入机制.子模块` 会**再加载一份**：两个类对象（`isinstance` 挂），
    导入机械出现两套状态（官方 `test_importlib` 实测 138 条失败）。
"""

import importlib as __导入工具
import sys as __系统
import importlib as __英文

for _子 in ('_abc', '_bootstrap', '_bootstrap_external', 'abc', 'machinery', 'metadata', 'metadata._adapters', 'metadata._collections', 'metadata._functools', 'metadata._itertools', 'metadata._meta', 'metadata._text', 'metadata.diagnose', 'readers', 'resources', 'resources._adapters', 'resources._common', 'resources._functional', 'resources._itertools', 'resources.abc', 'resources.readers', 'resources.simple', 'simple', 'util'):
    try:
        __系统.modules["导入机制." + _子] = __导入工具.import_module("importlib." + _子)
    except ImportError:
        pass      # 平台相关子模块（如 Windows 上的 asyncio.unix_events）

globals().update({_名: _值 for _名, _值 in vars(__英文).items() if not _名.startswith("__")})
__path__ = __英文.__path__

_别名对 = (('import_module', '导入模块'), ('invalidate_caches', '失效缓存'), ('reload', '重载'))
for _英, _中 in _别名对:
    if hasattr(__英文, _英):
        globals()[_中] = getattr(__英文, _英)

__all__ = tuple(list(getattr(__英文, "__all__", [])) +
               [_中 for _英, _中 in _别名对 if _中 in globals()])


def __getattr__(名):
    """兜底转发：没显式起中文名的（含私有名）照样到得了英文那边。"""
    return getattr(__英文, 名)


def __dir__():
    return sorted(set(globals()) | set(dir(__英文)))
