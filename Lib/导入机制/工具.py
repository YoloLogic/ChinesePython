# -*- coding: utf-8 -*-
"""导入机制.工具 —— 由 `tools\汉化库.py` 机械生成的**转发壳**（D-184），别手改。

英文模块：`importlib.util`（**不深拷贝**：中文名是**别名**，跟英文名指向同一个对象）
为什么：导入机械不能有两份（D-163）；深拷贝会造出第二套加载器/规格 ⇒ 走薄壳（D-182/D-183/D-184）
"""

import importlib.util as __英文模块

globals().update({_名: _值 for _名, _值 in vars(__英文模块).items() if not _名.startswith("__")})

_别名对 = (('LazyLoader', '懒加载器'), ('MAGIC_NUMBER', '魔数'), ('cache_from_source', '缓存自源码'), ('decode_source', '解码源码'), ('find_spec', '查找规格'), ('module_from_spec', '模块自规格'), ('resolve_name', '解析名字'), ('source_from_cache', '源码自缓存'), ('source_hash', '源码哈希'), ('spec_from_file_location', '规格自路径'), ('spec_from_loader', '规格自加载器'))
for _英, _中 in _别名对:
    if hasattr(__英文模块, _英):
        globals()[_中] = getattr(__英文模块, _英)

if hasattr(__英文模块, "__all__"):
    __all__ = list(__英文模块.__all__) + [_中 for _英, _中 in _别名对 if _中 in globals()]


def __getattr__(名):
    """兜底转发：没显式起中文名的名字（含私有名）照样到得了英文那边。"""
    return getattr(__英文模块, 名)


def __dir__():
    return sorted(set(globals()) | set(dir(__英文模块)))
