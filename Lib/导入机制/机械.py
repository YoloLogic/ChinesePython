# -*- coding: utf-8 -*-
"""导入机制.机械 —— 由 `tools\汉化库.py` 机械生成的**转发壳**（D-184），别手改。

英文模块：`importlib.machinery`（**不深拷贝**：中文名是**别名**，跟英文名指向同一个对象）
为什么：导入机械不能有两份（D-163）；深拷贝会造出第二套加载器/规格 ⇒ 走薄壳（D-182/D-183/D-184）
"""

import importlib.machinery as __英文模块

globals().update({_名: _值 for _名, _值 in vars(__英文模块).items() if not _名.startswith("__")})

_别名对 = (('BYTECODE_SUFFIXES', '字节码后缀'), ('BuiltinImporter', '内建导入器'), ('EXTENSION_SUFFIXES', '扩展后缀'), ('ExtensionFileLoader', '扩展加载器'), ('FileFinder', '文件查找器'), ('FrozenImporter', '冻结导入器'), ('ModuleSpec', '模块规格'), ('NamespaceLoader', '空间包加载器'), ('PathFinder', '路径查找器'), ('SOURCE_SUFFIXES', '源码后缀'), ('SourceFileLoader', '源文件加载器'), ('SourcelessFileLoader', '无源码加载器'), ('WindowsRegistryFinder', '注册表查找器'), ('all_suffixes', '全部后缀'))
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
