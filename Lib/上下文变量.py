# -*- coding: utf-8 -*-
"""上下文变量 —— 汉语库（由 tools/汉化库.py 从 Lib/contextvars.py 机械生成，**不要手改**）。

英文库 Lib/contextvars.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 上下文变量
"""


import _collections_abc
from _contextvars import Context, ContextVar, Token, copy_context
__all__ = ('Context', 'ContextVar', 'Token', 'copy_context')
_collections_abc.Mapping.register(Context)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import contextvars as _英文库
上下文 = _英文库.Context
上下文变量 = _英文库.ContextVar
令牌 = _英文库.Token
复制上下文 = _英文库.copy_context

# ---- 转发层结束 ----
