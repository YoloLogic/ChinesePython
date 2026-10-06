# -*- coding: utf-8 -*-
"""导入机制.元数据 —— 由 `tools\汉化库.py` 机械生成的**转发壳**（D-184），别手改。

英文模块：`importlib.metadata`（**不深拷贝**：中文名是**别名**，跟英文名指向同一个对象）
为什么：导入机械不能有两份（D-163）；深拷贝会造出第二套加载器/规格 ⇒ 走薄壳（D-182/D-183/D-184）
"""

import importlib.metadata as __英文模块

globals().update({_名: _值 for _名, _值 in vars(__英文模块).items() if not _名.startswith("__")})

_别名对 = (('DeprecatedNonAbstract', '废弃非抽象'), ('Distribution', '发行版'), ('DistributionFinder', '发行版查找器'), ('EntryPoint', '入口点'), ('EntryPoints', '入口点集'), ('FastPath', '快速路径'), ('FileHash', '文件哈希'), ('FoldedCase', '折叠大小写'), ('FreezableDefaultDict', '冻结默认字典'), ('Lookup', '查表'), ('MetadataPathFinder', '元数据查找器'), ('PackageMetadata', '包元数据'), ('PackageNotFoundError', '包未找到错误'), ('PackagePath', '包路径'), ('Pair', '对子'), ('PathDistribution', '路径发行版'), ('Prepared', '规范名'), ('Sectioned', '分段名'), ('SimplePath', '简单路径'), ('always_iterable', '总是可迭代'), ('distribution', '取发行版'), ('distributions', '遍历发行版'), ('entry_points', '取入口点'), ('files', '取文件'), ('metadata', '取元数据'), ('method_cache', '方法缓存'), ('packages_distributions', '包到发行版'), ('pass_none', '空值放行'), ('requires', '取依赖'), ('unique_everseen', '去重保序'), ('version', '取版本'))
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
