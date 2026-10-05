# -*- coding: utf-8 -*-
"""电子邮件.迭代器 —— 汉语库（由 tools/汉化库.py 从 Lib/email/iterators.py 机械生成，**不要手改**）。

英文库 Lib/email.iterators.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


"""Various types of useful iterators and generators."""
_英文原名表 = {'body_line_iterator': '正文行迭代器', 'typed_subpart_iterator': '按类型迭代子部分', 'walk': '遍历'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['body_line_iterator', 'typed_subpart_iterator', 'walk']
import sys
from io import StringIO

def 遍历(self):
    """Walk over the message tree, yielding each subpart.

    The walk is performed in depth-first order.  This method is a
    generator.
    """
    yield self
    if self.is_multipart():
        for subpart in self.get_payload():
            yield from subpart.walk()

def 正文行迭代器(msg, decode=False):
    """Iterate over the parts, returning string payloads line-by-line.

    Optional decode (default False) is passed through to .get_payload().
    """
    for subpart in msg.walk():
        payload = subpart.get_payload(decode=decode)
        if isinstance(payload, str):
            yield from StringIO(payload)

def 按类型迭代子部分(msg, maintype='text', subtype=None):
    """Iterate over the subparts with a given MIME type.

    Use 'maintype' as the main MIME type to match against; this defaults to
    "text".  Optional 'subtype' is the MIME subtype to match against; if
    omitted, only the main type is matched.
    """
    for subpart in msg.walk():
        if subpart.get_content_maintype() == maintype:
            if subtype is None or subpart.get_content_subtype() == subtype:
                yield subpart

def _structure(msg, fp=None, level=0, include_default=False):
    """A handy debugging aid"""
    if fp is None:
        fp = sys.stdout
    tab = ' ' * (level * 4)
    print(tab + msg.get_content_type(), end='', file=fp)
    if include_default:
        print(' [%s]' % msg.get_default_type(), file=fp)
    else:
        print(file=fp)
    if msg.is_multipart():
        for subpart in msg.get_payload():
            _structure(subpart, fp, level + 1, include_default)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'body_line_iterator': '正文行迭代器',
    'typed_subpart_iterator': '按类型迭代子部分',
    'walk': '遍历',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '按类型迭代子部分',
    '正文行迭代器',
    '遍历',
])

# ---- 转发层结束 ----
