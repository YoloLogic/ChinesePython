# -*- coding: utf-8 -*-
"""文件模式 —— 汉语库（由 tools/汉化库.py 从 Lib/stat.py 机械生成，**不要手改**）。

英文库 Lib/stat.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 文件模式
"""


"""Constants/functions for interpreting results of os.stat() and os.lstat().

Suggested usage: from stat import *
"""
_英文原名表 = {'ST_ATIME': '访问时间项', 'ST_CTIME': '状态变更时间项', 'ST_DEV': '设备号项', 'ST_GID': '属组ID项', 'ST_INO': 'inode号项', 'ST_MODE': '模式项', 'ST_MTIME': '修改时间项', 'ST_NLINK': '硬链数项', 'ST_SIZE': '大小项', 'ST_UID': '属主ID项', 'S_IFBLK': '块设备位', 'S_IFCHR': '字符设备位', 'S_IFDIR': '目录位', 'S_IFIFO': 'FIFO位', 'S_IFLNK': '软链位', 'S_IFMT': '类型掩码', 'S_IFREG': '普通文件位', 'S_IFSOCK': '套接字位', 'S_IMODE': '权限位', 'S_IRGRP': '属组读', 'S_IROTH': '其他读', 'S_IRUSR': '属主读', 'S_IRWXG': '属组全权', 'S_IRWXO': '其他全权', 'S_IRWXU': '属主全权', 'S_ISBLK': '是块设备吗', 'S_ISCHR': '是字符设备吗', 'S_ISDIR': '是目录吗', 'S_ISDOOR': '是门吗', 'S_ISFIFO': '是FIFO吗', 'S_ISGID': '设置属组ID', 'S_ISLNK': '是软链吗', 'S_ISPORT': '是端口吗', 'S_ISREG': '是普通文件吗', 'S_ISSOCK': '是套接字吗', 'S_ISUID': '设置属主ID', 'S_ISVTX': '粘滞位', 'S_ISWHT': '是白障吗', 'S_IWGRP': '属组写', 'S_IWOTH': '其他写', 'S_IWUSR': '属主写', 'S_IXGRP': '属组执行', 'S_IXOTH': '其他执行', 'S_IXUSR': '属主执行', 'filemode': '模式文本'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
模式项 = 0
inode号项 = 1
设备号项 = 2
硬链数项 = 3
属主ID项 = 4
属组ID项 = 5
大小项 = 6
访问时间项 = 7
修改时间项 = 8
状态变更时间项 = 9

def 权限位(mode):
    """Return the portion of the file's mode that can be set by
    os.chmod().
    """
    return mode & 4095

def 类型掩码(mode):
    """Return the portion of the file's mode that describes the
    file type.
    """
    return mode & 61440
目录位 = 16384
字符设备位 = 8192
块设备位 = 24576
普通文件位 = 32768
FIFO位 = 4096
软链位 = 40960
套接字位 = 49152
S_IFDOOR = 0
S_IFPORT = 0
S_IFWHT = 0

def 是目录吗(mode):
    """Return True if mode is from a directory."""
    return 类型掩码(mode) == 目录位

def 是字符设备吗(mode):
    """Return True if mode is from a character special device file."""
    return 类型掩码(mode) == 字符设备位

def 是块设备吗(mode):
    """Return True if mode is from a block special device file."""
    return 类型掩码(mode) == 块设备位

def 是普通文件吗(mode):
    """Return True if mode is from a regular file."""
    return 类型掩码(mode) == 普通文件位

def 是FIFO吗(mode):
    """Return True if mode is from a FIFO (named pipe)."""
    return 类型掩码(mode) == FIFO位

def 是软链吗(mode):
    """Return True if mode is from a symbolic link."""
    return 类型掩码(mode) == 软链位

def 是套接字吗(mode):
    """Return True if mode is from a socket."""
    return 类型掩码(mode) == 套接字位

def 是门吗(mode):
    """Return True if mode is from a door."""
    return False

def 是端口吗(mode):
    """Return True if mode is from an event port."""
    return False

def 是白障吗(mode):
    """Return True if mode is from a whiteout."""
    return False
设置属主ID = 2048
设置属组ID = 1024
S_ENFMT = 设置属组ID
粘滞位 = 512
S_IREAD = 256
S_IWRITE = 128
S_IEXEC = 64
属主全权 = 448
属主读 = 256
属主写 = 128
属主执行 = 64
属组全权 = 56
属组读 = 32
属组写 = 16
属组执行 = 8
其他全权 = 7
其他读 = 4
其他写 = 2
其他执行 = 1
UF_SETTABLE = 65535
UF_NODUMP = 1
UF_IMMUTABLE = 2
UF_APPEND = 4
UF_OPAQUE = 8
UF_NOUNLINK = 16
UF_COMPRESSED = 32
UF_TRACKED = 64
UF_DATAVAULT = 128
UF_HIDDEN = 32768
SF_SETTABLE = 4294901760
SF_ARCHIVED = 65536
SF_IMMUTABLE = 131072
SF_APPEND = 262144
SF_RESTRICTED = 524288
SF_NOUNLINK = 1048576
SF_SNAPSHOT = 2097152
SF_FIRMLINK = 8388608
SF_DATALESS = 1073741824
_filemode_table = (((软链位, 'l'), (套接字位, 's'), (普通文件位, '-'), (块设备位, 'b'), (目录位, 'd'), (字符设备位, 'c'), (FIFO位, 'p')), ((属主读, 'r'),), ((属主写, 'w'),), ((属主执行 | 设置属主ID, 's'), (设置属主ID, 'S'), (属主执行, 'x')), ((属组读, 'r'),), ((属组写, 'w'),), ((属组执行 | 设置属组ID, 's'), (设置属组ID, 'S'), (属组执行, 'x')), ((其他读, 'r'),), ((其他写, 'w'),), ((其他执行 | 粘滞位, 't'), (粘滞位, 'T'), (其他执行, 'x')))

def 模式文本(mode):
    """Convert a file's mode to a string of the form '-rwxrwxrwx'."""
    perm = []
    for index, table in enumerate(_filemode_table):
        for bit, char in table:
            if index == 0:
                if 类型掩码(mode) == bit:
                    perm.append(char)
                    break
            elif mode & bit == bit:
                perm.append(char)
                break
        else:
            if index == 0:
                perm.append('?')
            else:
                perm.append('-')
    return ''.join(perm)
FILE_ATTRIBUTE_ARCHIVE = 32
FILE_ATTRIBUTE_COMPRESSED = 2048
FILE_ATTRIBUTE_DEVICE = 64
FILE_ATTRIBUTE_DIRECTORY = 16
FILE_ATTRIBUTE_ENCRYPTED = 16384
FILE_ATTRIBUTE_HIDDEN = 2
FILE_ATTRIBUTE_INTEGRITY_STREAM = 32768
FILE_ATTRIBUTE_NORMAL = 128
FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 8192
FILE_ATTRIBUTE_NO_SCRUB_DATA = 131072
FILE_ATTRIBUTE_OFFLINE = 4096
FILE_ATTRIBUTE_READONLY = 1
FILE_ATTRIBUTE_REPARSE_POINT = 1024
FILE_ATTRIBUTE_SPARSE_FILE = 512
FILE_ATTRIBUTE_SYSTEM = 4
FILE_ATTRIBUTE_TEMPORARY = 256
FILE_ATTRIBUTE_VIRTUAL = 65536
try:
    from _stat import *
except ImportError:
    pass


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'ST_ATIME': '访问时间项',
    'ST_CTIME': '状态变更时间项',
    'ST_DEV': '设备号项',
    'ST_GID': '属组ID项',
    'ST_INO': 'inode号项',
    'ST_MODE': '模式项',
    'ST_MTIME': '修改时间项',
    'ST_NLINK': '硬链数项',
    'ST_SIZE': '大小项',
    'ST_UID': '属主ID项',
    'S_IFBLK': '块设备位',
    'S_IFCHR': '字符设备位',
    'S_IFDIR': '目录位',
    'S_IFIFO': 'FIFO位',
    'S_IFLNK': '软链位',
    'S_IFMT': '类型掩码',
    'S_IFREG': '普通文件位',
    'S_IFSOCK': '套接字位',
    'S_IMODE': '权限位',
    'S_IRGRP': '属组读',
    'S_IROTH': '其他读',
    'S_IRUSR': '属主读',
    'S_IRWXG': '属组全权',
    'S_IRWXO': '其他全权',
    'S_IRWXU': '属主全权',
    'S_ISBLK': '是块设备吗',
    'S_ISCHR': '是字符设备吗',
    'S_ISDIR': '是目录吗',
    'S_ISDOOR': '是门吗',
    'S_ISFIFO': '是FIFO吗',
    'S_ISGID': '设置属组ID',
    'S_ISLNK': '是软链吗',
    'S_ISPORT': '是端口吗',
    'S_ISREG': '是普通文件吗',
    'S_ISSOCK': '是套接字吗',
    'S_ISUID': '设置属主ID',
    'S_ISVTX': '粘滞位',
    'S_ISWHT': '是白障吗',
    'S_IWGRP': '属组写',
    'S_IWOTH': '其他写',
    'S_IWUSR': '属主写',
    'S_IXGRP': '属组执行',
    'S_IXOTH': '其他执行',
    'S_IXUSR': '属主执行',
    'filemode': '模式文本',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
