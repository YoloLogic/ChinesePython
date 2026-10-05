# -*- coding: utf-8 -*-
"""电子邮件.__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/email/__init__.py 机械生成，**不要手改**）。

英文库 Lib/email.__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


"""A package for parsing, handling, and generating email messages."""
_英文原名表 = {'message_from_binary_file': '从二进制文件读消息', 'message_from_bytes': '从字节读消息', 'message_from_file': '从文件读消息', 'message_from_string': '从字符串读消息'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['base64mime', 'charset', 'encoders', 'errors', 'feedparser', 'generator', 'header', 'iterators', 'message', 'message_from_file', 'message_from_binary_file', 'message_from_string', 'message_from_bytes', 'mime', 'parser', 'quoprimime', 'utils']

def 从字符串读消息(s, *args, **kws):
    """Parse a string into a Message object model.

    Optional _class and strict are passed to the Parser constructor.
    """
    from 电子邮件.解析 import Parser
    return Parser(*args, **kws).parsestr(s)

def 从字节读消息(s, *args, **kws):
    """Parse a bytes string into a Message object model.

    Optional _class and strict are passed to the Parser constructor.
    """
    from 电子邮件.解析 import BytesParser
    return BytesParser(*args, **kws).parsebytes(s)

def 从文件读消息(fp, *args, **kws):
    """Read a file and parse its contents into a Message object model.

    Optional _class and strict are passed to the Parser constructor.
    """
    from 电子邮件.解析 import Parser
    return Parser(*args, **kws).parse(fp)

def 从二进制文件读消息(fp, *args, **kws):
    """Read a binary file and parse its contents into a Message object model.

    Optional _class and strict are passed to the Parser constructor.
    """
    from 电子邮件.解析 import BytesParser
    return BytesParser(*args, **kws).parse(fp)


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
from . import _编码词 as _encoded_words
from . import _邮件头值解析 as _header_value_parser
from . import _地址解析 as _parseaddr
from . import _策略基类 as _policybase
from . import base64编码 as base64mime
from . import 字符集 as charset
from . import 内容管理 as contentmanager
from . import 编码器 as encoders
from . import 错误 as errors
from . import 流式解析 as feedparser
from . import 生成器 as generator
from . import 邮件头 as header
from . import 邮件头登记 as headerregistry
from . import 迭代器 as iterators
from . import 消息 as message
from . import 解析 as parser
from . import 策略 as policy
from . import 可打印编码 as quoprimime
from . import 工具 as utils
_模块别名 = {
    'message_from_binary_file': '从二进制文件读消息',
    'message_from_bytes': '从字节读消息',
    'message_from_file': '从文件读消息',
    'message_from_string': '从字符串读消息',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '从二进制文件读消息',
    '从字符串读消息',
    '从字节读消息',
    '从文件读消息',
])

# ---- 转发层结束 ----
