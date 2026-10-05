# -*- coding: utf-8 -*-
"""电子邮件.mime/图像 —— 汉语库（由 tools/汉化库.py 从 Lib/email/mime/image.py 机械生成，**不要手改**）。

英文库 Lib/email.mime/image.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


"""Class representing image/* type MIME documents."""
_英文原名表 = {'MIMEImage': 'MIME图像'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['MIMEImage']
from 电子邮件 import 编码器
from 电子邮件.mime.非多部分 import MIMENonMultipart

class MIME图像(MIMENonMultipart):
    """Class for generating image/* type MIME documents."""

    def __init__(self, _imagedata, _subtype=None, _encoder=编码器.encode_base64, *, policy=None, **_params):
        """Create an image/* type MIME document.

        _imagedata contains the bytes for the raw image data.  If the data
        type can be detected (jpeg, png, gif, tiff, rgb, pbm, pgm, ppm,
        rast, xbm, bmp, webp, and exr attempted), then the subtype will be
        automatically included in the Content-Type header. Otherwise, you can
        specify the specific image subtype via the _subtype parameter.

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
        _subtype = _what(_imagedata) if _subtype is None else _subtype
        if _subtype is None:
            raise TypeError('Could not guess image MIME subtype')
        MIMENonMultipart.__init__(self, 'image', _subtype, policy=policy, **_params)
        self.set_payload(_imagedata)
        _encoder(self)
_rules = []

def _what(data):
    for rule in _rules:
        if (res := rule(data)):
            return res
    else:
        return None

def rule(rulefunc):
    _rules.append(rulefunc)
    return rulefunc

@rule
def _jpeg(h):
    """JPEG data with JFIF or Exif markers; and raw JPEG"""
    if h[6:10] in (b'JFIF', b'Exif'):
        return 'jpeg'
    elif h[:4] == b'\xff\xd8\xff\xdb':
        return 'jpeg'

@rule
def _png(h):
    if h.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'

@rule
def _gif(h):
    """GIF ('87 and '89 variants)"""
    if h[:6] in (b'GIF87a', b'GIF89a'):
        return 'gif'

@rule
def _tiff(h):
    """TIFF (can be in Motorola or Intel byte order)"""
    if h[:2] in (b'MM', b'II'):
        return 'tiff'

@rule
def _rgb(h):
    """SGI image library"""
    if h.startswith(b'\x01\xda'):
        return 'rgb'

@rule
def _pbm(h):
    """PBM (portable bitmap)"""
    if len(h) >= 3 and h[0] == ord(b'P') and (h[1] in b'14') and (h[2] in b' \t\n\r'):
        return 'pbm'

@rule
def _pgm(h):
    """PGM (portable graymap)"""
    if len(h) >= 3 and h[0] == ord(b'P') and (h[1] in b'25') and (h[2] in b' \t\n\r'):
        return 'pgm'

@rule
def _ppm(h):
    """PPM (portable pixmap)"""
    if len(h) >= 3 and h[0] == ord(b'P') and (h[1] in b'36') and (h[2] in b' \t\n\r'):
        return 'ppm'

@rule
def _rast(h):
    """Sun raster file"""
    if h.startswith(b'Y\xa6j\x95'):
        return 'rast'

@rule
def _xbm(h):
    """X bitmap (X10 or X11)"""
    if h.startswith(b'#define '):
        return 'xbm'

@rule
def _bmp(h):
    if h.startswith(b'BM'):
        return 'bmp'

@rule
def _webp(h):
    if h.startswith(b'RIFF') and h[8:12] == b'WEBP':
        return 'webp'

@rule
def _exr(h):
    if h.startswith(b'v/1\x01'):
        return 'exr'


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'MIMEImage': 'MIME图像',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'MIME图像',
]

# ---- 转发层结束 ----
