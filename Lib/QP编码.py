# -*- coding: utf-8 -*-
"""QP编码 —— 汉语库（由 tools/汉化库.py 从 Lib/quopri.py 机械生成，**不要手改**）。

英文库 Lib/quopri.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py QP编码
"""


"""Conversions to/from quoted-printable transport encoding as per RFC 1521."""
_英文原名表 = {'EMPTYSTRING': '空字符串', 'ESCAPE': '转义符', 'HEX': '十六进制表', 'MAXLINESIZE': '最大行宽', 'decode': '解码', 'decodestring': '解码字符串', 'encode': '编码', 'encodestring': '编码字符串', 'ishex': '是十六进制吗', 'main': '主函数', 'needsquoting': '需要引号吗', 'quote': '加引号', 'unhex': '解十六进制'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['encode', 'decode', 'encodestring', 'decodestring']
转义符 = b'='
最大行宽 = 76
十六进制表 = b'0123456789ABCDEF'
空字符串 = b''
try:
    from binascii import a2b_qp, b2a_qp
except ImportError:
    a2b_qp = None
    b2a_qp = None

def 需要引号吗(c, quotetabs, header):
    """Decide whether a particular byte ordinal needs to be quoted.

    The 'quotetabs' flag indicates whether embedded tabs and spaces should be
    quoted.  Note that line-ending tabs and spaces are always encoded, as per
    RFC 1521.
    """
    assert isinstance(c, bytes)
    if c in b' \t':
        return quotetabs
    if c == b'_':
        return header
    return c == 转义符 or not b' ' <= c <= b'~'

def 加引号(c):
    """Quote a single character."""
    assert isinstance(c, bytes) and len(c) == 1
    c = ord(c)
    return 转义符 + bytes((十六进制表[c // 16], 十六进制表[c % 16]))

def 编码(input, output, quotetabs, header=False):
    """Read 'input', apply quoted-printable encoding, and write to 'output'.

    'input' and 'output' are binary file objects. The 'quotetabs' flag
    indicates whether embedded tabs and spaces should be quoted. Note that
    line-ending tabs and spaces are always encoded, as per RFC 1521.
    The 'header' flag indicates whether we are encoding spaces as _ as per RFC
    1522."""
    if b2a_qp is not None:
        data = input.read()
        odata = b2a_qp(data, quotetabs=quotetabs, header=header)
        output.write(odata)
        return

    def write(s, output=output, lineEnd=b'\n'):
        if s and s[-1:] in b' \t':
            output.write(s[:-1] + 加引号(s[-1:]) + lineEnd)
        elif s == b'.':
            output.write(加引号(s) + lineEnd)
        else:
            output.write(s + lineEnd)
    prevline = None
    while (line := input.readline()):
        outline = []
        stripped = b''
        if line[-1:] == b'\n':
            line = line[:-1]
            stripped = b'\n'
        for c in line:
            c = bytes((c,))
            if 需要引号吗(c, quotetabs, header):
                c = 加引号(c)
            if header and c == b' ':
                outline.append(b'_')
            else:
                outline.append(c)
        if prevline is not None:
            write(prevline)
        thisline = 空字符串.join(outline)
        while len(thisline) > 最大行宽:
            write(thisline[:最大行宽 - 1], lineEnd=b'=\n')
            thisline = thisline[最大行宽 - 1:]
        prevline = thisline
    if prevline is not None:
        write(prevline, lineEnd=stripped)

def 编码字符串(s, quotetabs=False, header=False):
    if b2a_qp is not None:
        return b2a_qp(s, quotetabs=quotetabs, header=header)
    from io import BytesIO
    infp = BytesIO(s)
    outfp = BytesIO()
    编码(infp, outfp, quotetabs, header)
    return outfp.getvalue()

def 解码(input, output, header=False):
    """Read 'input', apply quoted-printable decoding, and write to 'output'.
    'input' and 'output' are binary file objects.
    If 'header' is true, decode underscore as space (per RFC 1522)."""
    if a2b_qp is not None:
        data = input.read()
        odata = a2b_qp(data, header=header)
        output.write(odata)
        return
    new = b''
    while (line := input.readline()):
        i, n = (0, len(line))
        if n > 0 and line[n - 1:n] == b'\n':
            partial = 0
            n = n - 1
            while n > 0 and line[n - 1:n] in b' \t\r':
                n = n - 1
        else:
            partial = 1
        while i < n:
            c = line[i:i + 1]
            if c == b'_' and header:
                new = new + b' '
                i = i + 1
            elif c != 转义符:
                new = new + c
                i = i + 1
            elif i + 1 == n and (not partial):
                partial = 1
                break
            elif i + 1 < n and line[i + 1:i + 2] == 转义符:
                new = new + 转义符
                i = i + 2
            elif i + 2 < n and 是十六进制吗(line[i + 1:i + 2]) and 是十六进制吗(line[i + 2:i + 3]):
                new = new + bytes((解十六进制(line[i + 1:i + 3]),))
                i = i + 3
            else:
                new = new + c
                i = i + 1
        if not partial:
            output.write(new + b'\n')
            new = b''
    if new:
        output.write(new)

def 解码字符串(s, header=False):
    if a2b_qp is not None:
        return a2b_qp(s, header=header)
    from io import BytesIO
    infp = BytesIO(s)
    outfp = BytesIO()
    解码(infp, outfp, header=header)
    return outfp.getvalue()

def 是十六进制吗(c):
    """Return true if the byte ordinal 'c' is a hexadecimal digit in ASCII."""
    assert isinstance(c, bytes)
    return b'0' <= c <= b'9' or b'a' <= c <= b'f' or b'A' <= c <= b'F'

def 解十六进制(s):
    """Get the integer value of a hexadecimal number."""
    bits = 0
    for c in s:
        c = bytes((c,))
        if b'0' <= c <= b'9':
            i = ord('0')
        elif b'a' <= c <= b'f':
            i = ord('a') - 10
        elif b'A' <= c <= b'F':
            i = ord(b'A') - 10
        else:
            assert False, 'non-hex digit ' + repr(c)
        bits = bits * 16 + (ord(c) - i)
    return bits

def 主函数():
    import sys
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'td')
    except getopt.error as msg:
        sys.stdout = sys.stderr
        print(msg)
        print('usage: quopri [-t | -d] [file] ...')
        print('-t: quote tabs')
        print('-d: decode; default encode')
        sys.exit(2)
    deco = False
    tabs = False
    for o, a in opts:
        if o == '-t':
            tabs = True
        if o == '-d':
            deco = True
    if tabs and deco:
        sys.stdout = sys.stderr
        print('-t and -d are mutually exclusive')
        sys.exit(2)
    if not args:
        args = ['-']
    sts = 0
    for file in args:
        if file == '-':
            fp = sys.stdin.buffer
        else:
            try:
                fp = open(file, 'rb')
            except OSError as msg:
                sys.stderr.write("%s: can't open (%s)\n" % (file, msg))
                sts = 1
                continue
        try:
            if deco:
                解码(fp, sys.stdout.buffer)
            else:
                编码(fp, sys.stdout.buffer, tabs)
        finally:
            if file != '-':
                fp.close()
    if sts:
        sys.exit(sts)
if __name__ == '__main__':
    主函数()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'EMPTYSTRING': '空字符串',
    'ESCAPE': '转义符',
    'HEX': '十六进制表',
    'MAXLINESIZE': '最大行宽',
    'decode': '解码',
    'decodestring': '解码字符串',
    'encode': '编码',
    'encodestring': '编码字符串',
    'ishex': '是十六进制吗',
    'main': '主函数',
    'needsquoting': '需要引号吗',
    'quote': '加引号',
    'unhex': '解十六进制',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '编码',
    '编码字符串',
    '解码',
    '解码字符串',
])

# ---- 转发层结束 ----
