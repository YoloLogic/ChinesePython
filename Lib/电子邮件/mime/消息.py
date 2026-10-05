# -*- coding: utf-8 -*-
"""电子邮件.mime/消息 —— 汉语库（由 tools/汉化库.py 从 Lib/email/mime/message.py 机械生成，**不要手改**）。

英文库 Lib/email.mime/message.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


"""Class representing message/* MIME documents."""
_英文原名表 = {'MIMEMessage': 'MIME消息'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['MIMEMessage']
from 电子邮件 import 消息
from 电子邮件.mime.非多部分 import MIMENonMultipart

class MIME消息(MIMENonMultipart):
    """Class representing message/* MIME documents."""

    def __init__(self, _msg, _subtype='rfc822', *, policy=None):
        """Create a message/* type MIME document.

        _msg is a message object and must be an instance of Message, or a
        derived class of Message, otherwise a TypeError is raised.

        Optional _subtype defines the subtype of the contained message.  The
        default is "rfc822" (this is defined by the MIME standard, even though
        the term "rfc822" is technically outdated by RFC 2822).
        """
        MIMENonMultipart.__init__(self, 'message', _subtype, policy=policy)
        if not isinstance(_msg, 消息.Message):
            raise TypeError('Argument is not an instance of Message')
        消息.Message.attach(self, _msg)
        self.set_default_type('message/rfc822')


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'MIMEMessage': 'MIME消息',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'MIME消息',
]

# ---- 转发层结束 ----
