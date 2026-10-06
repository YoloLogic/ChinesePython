# -*- coding: utf-8 -*-
"""导入机制 —— 由 `tools\汉化库.py` 机械生成的**薄壳包**（D-182/D-184），别手改。

英文包：`importlib`（**不深拷贝**：中文名是**别名**，跟英文名指向同一个对象）
为什么：导入机械不能有两份（D-163）；深拷贝会造出第二套加载器/规格 ⇒ 走薄壳（D-182/D-183/D-184）

三层保命（D-182 / D-183 / D-184）：
  ① **英文子模块名**挂进 sys.modules（键 = 汉语名 + 点 + 英文子模块名），指向**同一份**真模块 ——
     少了它，`from importlib import X` 会走 module.__name__（= 汉语名）**再加载一份**
     （D-183 实测 138 条失败：两个类对象、两套导入机械状态）；
  ② **中文子模块**（汉语名 + 点 + 中文名）是各文件的**转发壳**：同对象别名 + 中文名；
  ③ 包级名字 = `globals().update` + 词表别名。
"""

import importlib as __导入工具
import sys as __系统
import importlib as __英文

# ⓪ 子模块解析路径 = 我们自己的目录 + 英文那份（见文件头 ①）
__path__ = list(__path__) + [p for p in list(__英文.__path__) if p not in __path__]

# ① 英文子模块名 -> 同一对象（import 英文名.X 与 汉语名.X 是同一个模块）
for _英子 in ('_abc', '_bootstrap', '_bootstrap_external', 'abc', 'machinery', 'metadata', 'metadata._adapters', 'metadata._collections', 'metadata._functools', 'metadata._itertools', 'metadata._meta', 'metadata._text', 'metadata.diagnose', 'readers', 'resources', 'resources._adapters', 'resources._common', 'resources._functional', 'resources._itertools', 'resources.abc', 'resources.readers', 'resources.simple', 'simple', 'util'):
    try:
        __系统.modules["导入机制." + _英子] = __导入工具.import_module("importlib." + _英子)
    except ImportError:
        pass      # 平台相关子模块（如 Windows 上的 asyncio.unix_events）

# ② 中文子模块壳（先导入 ⇒ 包属性也挂上）
for _中壳 in ('元数据', '元数据.诊断', '工具', '抽象基类', '机械', '资源', '资源.抽象基类', '资源.简易', '资源.读取器'):
    __导入工具.import_module("导入机制." + _中壳)

globals().update({_名: _值 for _名, _值 in vars(__英文).items() if not _名.startswith("__")})

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
