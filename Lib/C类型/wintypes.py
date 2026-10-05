# -*- coding: utf-8 -*-
"""C类型.wintypes —— 汉语库（由 tools/汉化库.py 从 Lib/ctypes/wintypes.py 机械生成，**不要手改**）。

英文库 Lib/ctypes.wintypes.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py ctypes
"""


_英文原名表 = {'BOOL': '布尔整数', 'BOOLEAN': '布尔值', 'BYTE': '字节值', 'CHAR': '窄字符', 'DOUBLE': '双精度', 'DWORD': '双字', 'FLOAT': '单精度', 'HANDLE': '句柄', 'HDC': '设备上下文句柄', 'HINSTANCE': '实例句柄', 'HKEY': '注册表键句柄', 'HMODULE': '模块句柄', 'HWND': '窗口句柄', 'INT': '整数', 'LARGE_INTEGER': '大整数', 'LONG': '长整', 'LPCSTR': '常量字符串指针', 'LPCVOID': '常量通用指针', 'LPCWSTR': '常量宽字符串指针', 'LPSTR': '字符串指针', 'LPVOID': '通用指针', 'LPWSTR': '宽字符串指针', 'MAX_PATH': '最大路径长度', 'RGB': '取RGB', 'SHORT': '短整', 'UINT': '无符号整数', 'ULARGE_INTEGER': '无符号大整数', 'ULONG': '无符号长整', 'USHORT': '无符号短整', 'WCHAR': '宽字符值', 'WORD': '字'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import C类型
字节值 = C类型.c_ubyte
字 = C类型.c_ushort
双字 = C类型.c_ulong
窄字符 = C类型.c_char
宽字符值 = C类型.c_wchar
无符号整数 = C类型.c_uint
整数 = C类型.c_int
双精度 = C类型.c_double
单精度 = C类型.c_float
布尔值 = 字节值
布尔整数 = C类型.c_long

class VARIANT_BOOL(C类型._SimpleCData):
    _type_ = 'v'

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.value)
无符号长整 = C类型.c_ulong
长整 = C类型.c_long
无符号短整 = C类型.c_ushort
短整 = C类型.c_short
_LARGE_INTEGER = 大整数 = C类型.c_longlong
_ULARGE_INTEGER = 无符号大整数 = C类型.c_ulonglong
LPCOLESTR = LPOLESTR = OLESTR = C类型.c_wchar_p
常量宽字符串指针 = 宽字符串指针 = C类型.c_wchar_p
常量字符串指针 = 字符串指针 = C类型.c_char_p
常量通用指针 = 通用指针 = C类型.c_void_p
if C类型.sizeof(C类型.c_long) == C类型.sizeof(C类型.c_void_p):
    WPARAM = C类型.c_ulong
    LPARAM = C类型.c_long
elif C类型.sizeof(C类型.c_longlong) == C类型.sizeof(C类型.c_void_p):
    WPARAM = C类型.c_ulonglong
    LPARAM = C类型.c_longlong
ATOM = 字
LANGID = 字
COLORREF = 双字
LGRPID = 双字
LCTYPE = 双字
LCID = 双字
句柄 = C类型.c_void_p
HACCEL = 句柄
HBITMAP = 句柄
HBRUSH = 句柄
HCOLORSPACE = 句柄
HCONV = 句柄
HCONVLIST = 句柄
HCURSOR = 句柄
设备上下文句柄 = 句柄
HDDEDATA = 句柄
HDESK = 句柄
HDROP = 句柄
HDWP = 句柄
HENHMETAFILE = 句柄
HFILE = 整数
HFONT = 句柄
HGDIOBJ = 句柄
HGLOBAL = 句柄
HHOOK = 句柄
HICON = 句柄
实例句柄 = 句柄
注册表键句柄 = 句柄
HKL = 句柄
HLOCAL = 句柄
HMENU = 句柄
HMETAFILE = 句柄
模块句柄 = 句柄
HMONITOR = 句柄
HPALETTE = 句柄
HPEN = 句柄
HRESULT = 长整
HRGN = 句柄
HRSRC = 句柄
HSTR = 句柄
HSZ = 句柄
HTASK = 句柄
HWINSTA = 句柄
窗口句柄 = 句柄
SC_HANDLE = 句柄
SERVICE_STATUS_HANDLE = 句柄

class RECT(C类型.Structure):
    _fields_ = [('left', 长整), ('top', 长整), ('right', 长整), ('bottom', 长整)]
tagRECT = _RECTL = RECTL = RECT

class _SMALL_RECT(C类型.Structure):
    _fields_ = [('Left', 短整), ('Top', 短整), ('Right', 短整), ('Bottom', 短整)]
SMALL_RECT = _SMALL_RECT

class _COORD(C类型.Structure):
    _fields_ = [('X', 短整), ('Y', 短整)]

class POINT(C类型.Structure):
    _fields_ = [('x', 长整), ('y', 长整)]
tagPOINT = _POINTL = POINTL = POINT

class SIZE(C类型.Structure):
    _fields_ = [('cx', 长整), ('cy', 长整)]
tagSIZE = SIZEL = SIZE

def 取RGB(red, green, blue):
    return red + (green << 8) + (blue << 16)

class FILETIME(C类型.Structure):
    _fields_ = [('dwLowDateTime', 双字), ('dwHighDateTime', 双字)]
_FILETIME = FILETIME

class MSG(C类型.Structure):
    _fields_ = [('hWnd', 窗口句柄), ('message', 无符号整数), ('wParam', WPARAM), ('lParam', LPARAM), ('time', 双字), ('pt', POINT)]
tagMSG = MSG
最大路径长度 = 260

class WIN32_FIND_DATAA(C类型.Structure):
    _fields_ = [('dwFileAttributes', 双字), ('ftCreationTime', FILETIME), ('ftLastAccessTime', FILETIME), ('ftLastWriteTime', FILETIME), ('nFileSizeHigh', 双字), ('nFileSizeLow', 双字), ('dwReserved0', 双字), ('dwReserved1', 双字), ('cFileName', 窄字符 * 最大路径长度), ('cAlternateFileName', 窄字符 * 14)]

class WIN32_FIND_DATAW(C类型.Structure):
    _fields_ = [('dwFileAttributes', 双字), ('ftCreationTime', FILETIME), ('ftLastAccessTime', FILETIME), ('ftLastWriteTime', FILETIME), ('nFileSizeHigh', 双字), ('nFileSizeLow', 双字), ('dwReserved0', 双字), ('dwReserved1', 双字), ('cFileName', 宽字符值 * 最大路径长度), ('cAlternateFileName', 宽字符值 * 14)]
LPBOOL = PBOOL = C类型.POINTER(布尔整数)
PBOOLEAN = C类型.POINTER(布尔值)
LPBYTE = PBYTE = C类型.POINTER(字节值)
PCHAR = C类型.POINTER(窄字符)
LPCOLORREF = C类型.POINTER(COLORREF)
LPDWORD = PDWORD = C类型.POINTER(双字)
LPFILETIME = PFILETIME = C类型.POINTER(FILETIME)
PFLOAT = C类型.POINTER(单精度)
LPHANDLE = PHANDLE = C类型.POINTER(句柄)
PHKEY = C类型.POINTER(注册表键句柄)
LPHKL = C类型.POINTER(HKL)
LPINT = PINT = C类型.POINTER(整数)
PLARGE_INTEGER = C类型.POINTER(大整数)
PLCID = C类型.POINTER(LCID)
LPLONG = PLONG = C类型.POINTER(长整)
LPMSG = PMSG = C类型.POINTER(MSG)
LPPOINT = PPOINT = C类型.POINTER(POINT)
PPOINTL = C类型.POINTER(POINTL)
LPRECT = PRECT = C类型.POINTER(RECT)
LPRECTL = PRECTL = C类型.POINTER(RECTL)
LPSC_HANDLE = C类型.POINTER(SC_HANDLE)
PSHORT = C类型.POINTER(短整)
LPSIZE = PSIZE = C类型.POINTER(SIZE)
LPSIZEL = PSIZEL = C类型.POINTER(SIZEL)
PSMALL_RECT = C类型.POINTER(SMALL_RECT)
LPUINT = PUINT = C类型.POINTER(无符号整数)
PULARGE_INTEGER = C类型.POINTER(无符号大整数)
PULONG = C类型.POINTER(无符号长整)
PUSHORT = C类型.POINTER(无符号短整)
PWCHAR = C类型.POINTER(宽字符值)
LPWIN32_FIND_DATAA = PWIN32_FIND_DATAA = C类型.POINTER(WIN32_FIND_DATAA)
LPWIN32_FIND_DATAW = PWIN32_FIND_DATAW = C类型.POINTER(WIN32_FIND_DATAW)
LPWORD = PWORD = C类型.POINTER(字)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 本模块别名：词表里有、但规则不让改定义的名字（内置名最典型，比如 `open`）
_本模块别名 = {
    '可变布尔': 'VARIANT_BOOL',
    '尺寸': 'SIZE',
    '文件时间': 'FILETIME',
    '查找数据A': 'WIN32_FIND_DATAA',
    '查找数据W': 'WIN32_FIND_DATAW',
    '消息': 'MSG',
    '点': 'POINT',
    '矩形': 'RECT',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'BOOL': '布尔整数',
    'BOOLEAN': '布尔值',
    'BYTE': '字节值',
    'CHAR': '窄字符',
    'DOUBLE': '双精度',
    'DWORD': '双字',
    'FLOAT': '单精度',
    'HANDLE': '句柄',
    'HDC': '设备上下文句柄',
    'HINSTANCE': '实例句柄',
    'HKEY': '注册表键句柄',
    'HMODULE': '模块句柄',
    'HWND': '窗口句柄',
    'INT': '整数',
    'LARGE_INTEGER': '大整数',
    'LONG': '长整',
    'LPCSTR': '常量字符串指针',
    'LPCVOID': '常量通用指针',
    'LPCWSTR': '常量宽字符串指针',
    'LPSTR': '字符串指针',
    'LPVOID': '通用指针',
    'LPWSTR': '宽字符串指针',
    'MAX_PATH': '最大路径长度',
    'RGB': '取RGB',
    'SHORT': '短整',
    'UINT': '无符号整数',
    'ULARGE_INTEGER': '无符号大整数',
    'ULONG': '无符号长整',
    'USHORT': '无符号短整',
    'WCHAR': '宽字符值',
    'WORD': '字',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
