# -*- coding: utf-8 -*-
"""电子邮件.mime/非多部分 —— 汉语库（由 tools/汉化库.py 从 Lib/email/mime/nonmultipart.py 机械生成，**不要手改**）。

英文库 Lib/email.mime/nonmultipart.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


"""Base class for MIME type messages that are not multipart."""
_英文原名表 = {'MIMENonMultipart': 'MIME非多部分'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['MIMENonMultipart']
from 电子邮件 import 错误
from 电子邮件.mime.基类 import MIMEBase

class MIME非多部分(MIMEBase):
    """Base class for MIME non-multipart type messages."""

    def attach(self, payload):
        raise 错误.MultipartConversionError('Cannot attach additional subparts to non-multipart/*')


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'MIMENonMultipart': 'MIME非多部分',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    'MIME非多部分',
])

# ---- 转发层结束 ----
