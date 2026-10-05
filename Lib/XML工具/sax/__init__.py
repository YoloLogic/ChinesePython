# -*- coding: utf-8 -*-
"""XML工具.sax/__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/xml/sax/__init__.py 机械生成，**不要手改**）。

英文库 Lib/xml.sax/__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py xml
"""


"""Simple API for XML (SAX) implementation for Python.

This module provides an implementation of the SAX 2 interface;
information about the Java version of the interface can be found at
http://www.megginson.com/SAX/.  The Python version of the interface is
documented at <...>.

This package contains the following modules:

handler -- Base classes and constants which define the SAX 2 API for
           the 'client-side' of SAX for Python.

saxutils -- Implementation of the convenience classes commonly used to
            work with SAX.

xmlreader -- Base classes and constants which define the SAX 2 API for
             the parsers used with SAX for Python.

expatreader -- Driver that allows use of the Expat parser with SAX.
"""
_英文原名表 = {'default_parser_list': '默认解析器清单', 'make_parser': '造解析器', 'parse': '解析', 'parseString': '解析字符串'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
from .xmlreader import InputSource
from .handler import ContentHandler, ErrorHandler
from ._exceptions import SAXException, SAXNotRecognizedException, SAXParseException, SAXNotSupportedException, SAXReaderNotAvailable

def 解析(source, handler, errorHandler=ErrorHandler()):
    parser = 造解析器()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)
    parser.parse(source)

def 解析字符串(string, handler, errorHandler=ErrorHandler()):
    import io
    if errorHandler is None:
        errorHandler = ErrorHandler()
    parser = 造解析器()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)
    inpsrc = InputSource()
    if isinstance(string, str):
        inpsrc.setCharacterStream(io.StringIO(string))
    else:
        inpsrc.setByteStream(io.BytesIO(string))
    parser.parse(inpsrc)
默认解析器清单 = ['xml.sax.expatreader']
_false = 0
if _false:
    import XML工具.sax.expatreader
import os, sys
if not sys.flags.ignore_environment and 'PY_SAX_PARSER' in os.environ:
    默认解析器清单 = os.environ['PY_SAX_PARSER'].split(',')
del os, sys

def 造解析器(parser_list=()):
    """Creates and returns a SAX parser.

    Creates the first parser it is able to instantiate of the ones
    given in the iterable created by chaining parser_list and
    default_parser_list.  The iterables must contain the names of Python
    modules containing both a SAX parser and a create_parser function."""
    for parser_name in list(parser_list) + 默认解析器清单:
        try:
            return _create_parser(parser_name)
        except ImportError:
            import sys
            if parser_name in sys.modules:
                raise
        except SAXReaderNotAvailable:
            pass
    raise SAXReaderNotAvailable('No parsers found', None)

def _create_parser(parser_name):
    drv_module = __import__(parser_name, {}, {}, ['create_parser'])
    return drv_module.create_parser()
__all__ = ['ContentHandler', 'ErrorHandler', 'InputSource', 'SAXException', 'SAXNotRecognizedException', 'SAXNotSupportedException', 'SAXParseException', 'SAXReaderNotAvailable', 'default_parser_list', 'make_parser', 'parse', 'parseString']


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'default_parser_list': '默认解析器清单',
    'make_parser': '造解析器',
    'parse': '解析',
    'parseString': '解析字符串',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '解析',
    '解析字符串',
    '造解析器',
    '默认解析器清单',
])

# ---- 转发层结束 ----
