# -*- coding: utf-8 -*-
"""导入机制.资源 —— 由 `tools\汉化库.py` 机械生成的**转发壳**（D-184），别手改。

英文模块：`importlib.resources`（**不深拷贝**：中文名是**别名**，跟英文名指向同一个对象）
为什么：导入机械不能有两份（D-163）；深拷贝会造出第二套加载器/规格 ⇒ 走薄壳（D-182/D-183/D-184）
"""

import importlib.resources as __英文模块

globals().update({_名: _值 for _名, _值 in vars(__英文模块).items() if not _名.startswith("__")})

_别名对 = (('Anchor', '锚点'), ('Package', '包名'), ('ResourceReader', '资源读取器'), ('as_file', '转成文件'), ('contents', '列内容'), ('files', '资源文件'), ('is_resource', '是资源吗'), ('open_binary', '开二进制'), ('open_text', '开文本'), ('path', '资源路径'), ('read_binary', '读二进制'), ('read_text', '读文本'))
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
