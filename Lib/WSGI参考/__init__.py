# -*- coding: utf-8 -*-
"""WSGI参考.__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/wsgiref/__init__.py 机械生成，**不要手改**）。

英文库 Lib/wsgiref.__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py wsgiref
"""


"""wsgiref -- a WSGI (PEP 3333) Reference Library

Current Contents:

* util -- Miscellaneous useful functions and wrappers

* headers -- Manage response headers

* handlers -- base classes for server/gateway implementations

* simple_server -- a simple BaseHTTPServer that supports WSGI

* validate -- validation wrapper that sits between an app and a server
  to detect errors in either

* types -- collection of WSGI-related types for static type checking

To-Do:

* cgi_gateway -- Run WSGI apps under CGI (pending a deployment standard)

* cgi_wrapper -- Run CGI apps under WSGI

* router -- a simple middleware component that handles URL traversal
"""


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 子模块的英文名也留着（照「英文原名一个都不能少」）：
# `JSON解析.decoder` 跟 `JSON解析.解码模块` 是**同一个模块对象**。
from . import 处理器 as handlers
from . import 简单服务器 as simple_server
from . import WSGI类型 as types
from . import 工具 as util
from . import 校验 as validate

# ---- 转发层结束 ----
