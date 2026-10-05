# -*- coding: utf-8 -*-
"""电子邮件.mime/音频 —— 汉语库（由 tools/汉化库.py 从 Lib/email/mime/audio.py 机械生成，**不要手改**）。

英文库 Lib/email.mime/audio.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


"""Class representing audio/* type MIME documents."""
_英文原名表 = {'MIMEAudio': 'MIME音频'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['MIMEAudio']
from 电子邮件 import 编码器
from 电子邮件.mime.非多部分 import MIMENonMultipart

class MIME音频(MIMENonMultipart):
    """Class for generating audio/* MIME documents."""

    def __init__(self, _audiodata, _subtype=None, _encoder=编码器.encode_base64, *, policy=None, **_params):
        """Create an audio/* type MIME document.

        _audiodata contains the bytes for the raw audio data.  If this data
        can be decoded as au, wav, aiff, or aifc, then the
        subtype will be automatically included in the Content-Type header.
        Otherwise, you can specify  the specific audio subtype via the
        _subtype parameter.  If _subtype is not given, and no subtype can be
        guessed, a TypeError is raised.

        _encoder is a function which will perform the actual encoding for
        transport of the image data.  It takes one argument, which is this
        Image instance.  It should use get_payload() and set_payload() to
        change the payload to the encoded form.  It should also add any
        Content-Transfer-Encoding or other headers to the message as
        necessary.  The default encoding is Base64.

        Any additional keyword arguments are passed to the base class
        constructor, which turns them into parameters on the Content-Type
        header.
        """
        if _subtype is None:
            _subtype = _what(_audiodata)
        if _subtype is None:
            raise TypeError('Could not find audio MIME subtype')
        MIMENonMultipart.__init__(self, 'audio', _subtype, policy=policy, **_params)
        self.set_payload(_audiodata)
        _encoder(self)
_rules = []

def _what(data):
    for testfn in _rules:
        if (res := testfn(data)):
            return res
    else:
        return None

def rule(rulefunc):
    _rules.append(rulefunc)
    return rulefunc

@rule
def _aiff(h):
    if not h.startswith(b'FORM'):
        return None
    if h[8:12] in {b'AIFC', b'AIFF'}:
        return 'x-aiff'
    else:
        return None

@rule
def _au(h):
    if h.startswith(b'.snd'):
        return 'basic'
    else:
        return None

@rule
def _wav(h):
    if not h.startswith(b'RIFF') or h[8:12] != b'WAVE' or h[12:16] != b'fmt ':
        return None
    else:
        return 'x-wav'


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'MIMEAudio': 'MIME音频',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'MIME音频',
]

# ---- 转发层结束 ----
