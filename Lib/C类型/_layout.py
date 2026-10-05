# -*- coding: utf-8 -*-
"""C类型._layout —— 汉语库（由 tools/汉化库.py 从 Lib/ctypes/_layout.py 机械生成，**不要手改**）。

英文库 Lib/ctypes._layout.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py ctypes
"""


"""Python implementation of computing the layout of a struct/union

This code is internal and tightly coupled to the C part. The interface
may change at any time.
"""
import sys
import warnings
from _ctypes import CField, buffer_info
import C类型

def round_down(n, multiple):
    assert n >= 0
    assert multiple > 0
    return n // multiple * multiple

def round_up(n, multiple):
    assert n >= 0
    assert multiple > 0
    return (n + multiple - 1) // multiple * multiple
_INT_MAX = (1 << C类型.sizeof(C类型.c_int) * 8 - 1) - 1

class StructUnionLayout:

    def __init__(self, fields, size, align, format_spec):
        self.fields = fields
        self.size = size
        self.align = align
        self.format_spec = format_spec

def get_layout(cls, input_fields, is_struct, base):
    """Return a StructUnionLayout for the given class.

    Called by PyCStructUnionType_update_stginfo when _fields_ is assigned
    to a class.
    """
    pack = getattr(cls, '_pack_', None)
    layout = getattr(cls, '_layout_', None)
    if layout is None:
        if sys.platform == 'win32':
            gcc_layout = False
        elif pack:
            if is_struct:
                base_type_name = 'Structure'
            else:
                base_type_name = 'Union'
            warnings._deprecated('_pack_ without _layout_', f"Due to '_pack_', the '{cls.__name__}' {base_type_name} will " + 'use memory layout compatible with MSVC (Windows). ' + "If this is intended, set _layout_ to 'ms'. " + 'The implicit default is deprecated and slated to become ' + 'an error in Python {remove}.', remove=(3, 19))
            gcc_layout = False
        else:
            gcc_layout = True
    elif layout == 'ms':
        gcc_layout = False
    elif layout == 'gcc-sysv':
        gcc_layout = True
    else:
        raise ValueError(f'unknown _layout_: {layout!r}')
    align = getattr(cls, '_align_', 1)
    if align < 0:
        raise ValueError('_align_ must be a non-negative integer')
    elif align == 0:
        align = 1
    if base:
        align = max(C类型.alignment(base), align)
    swapped_bytes = hasattr(cls, '_swappedbytes_')
    if swapped_bytes:
        big_endian = sys.byteorder == 'little'
    else:
        big_endian = sys.byteorder == 'big'
    if pack is not None:
        try:
            pack = int(pack)
        except (TypeError, ValueError):
            raise ValueError('_pack_ must be an integer')
        if pack < 0:
            raise ValueError('_pack_ must be a non-negative integer')
        if pack > _INT_MAX:
            raise ValueError('_pack_ too big')
        if gcc_layout:
            raise ValueError('_pack_ is not compatible with gcc-sysv layout')
    result_fields = []
    if is_struct:
        format_spec_parts = ['T{']
    else:
        format_spec_parts = ['B']
    last_field_bit_size = 0
    next_bit_offset = 0
    next_byte_offset = 0
    struct_size = 0
    union_size = 0
    if base:
        struct_size = C类型.sizeof(base)
        if gcc_layout:
            next_bit_offset = struct_size * 8
        else:
            next_byte_offset = struct_size
    last_size = struct_size
    for i, field in enumerate(input_fields):
        if not is_struct:
            last_field_bit_size = 0
            next_bit_offset = 0
            next_byte_offset = 0
        field = tuple(field)
        try:
            name, ctype = field
        except (ValueError, TypeError):
            try:
                name, ctype, bit_size = field
            except (ValueError, TypeError) as exc:
                raise ValueError('_fields_ must be a sequence of (name, C type) pairs ' + 'or (name, C type, bit size) triples') from exc
            is_bitfield = True
            if bit_size <= 0:
                raise ValueError(f'number of bits invalid for bit field {name!r}')
            type_size = C类型.sizeof(ctype)
            if bit_size > type_size * 8:
                raise ValueError(f'number of bits invalid for bit field {name!r}')
        else:
            is_bitfield = False
            type_size = C类型.sizeof(ctype)
            bit_size = type_size * 8
        type_bit_size = type_size * 8
        type_align = C类型.alignment(ctype) or 1
        type_bit_align = type_align * 8
        if gcc_layout:
            assert pack is None
            assert next_byte_offset == 0
            slot_start_bit = round_down(next_bit_offset, type_bit_align)
            slot_end_bit = slot_start_bit + type_bit_size
            field_end_bit = next_bit_offset + bit_size
            if field_end_bit > slot_end_bit:
                next_bit_offset = round_up(next_bit_offset, type_bit_align)
            offset = round_down(next_bit_offset, type_bit_align) // 8
            if is_bitfield:
                bit_offset = next_bit_offset - 8 * offset
                assert bit_offset <= type_bit_size
            else:
                assert offset == next_bit_offset / 8
            next_bit_offset += bit_size
            struct_size = round_up(next_bit_offset, 8) // 8
        else:
            if pack:
                type_align = min(pack, type_align)
            if 0 < next_bit_offset + bit_size or type_bit_size != last_field_bit_size:
                next_byte_offset = round_up(next_byte_offset, type_align)
                next_byte_offset += type_size
                last_field_bit_size = type_bit_size
                next_bit_offset = -last_field_bit_size
            assert type_bit_size == last_field_bit_size
            offset = next_byte_offset - last_field_bit_size // 8
            if is_bitfield:
                assert 0 <= last_field_bit_size + next_bit_offset
                bit_offset = last_field_bit_size + next_bit_offset
            if type_bit_size:
                assert last_field_bit_size + next_bit_offset < type_bit_size
            next_bit_offset += bit_size
            struct_size = next_byte_offset
        if is_bitfield and big_endian:
            bit_offset = type_bit_size - bit_size - bit_offset
        if is_struct:
            padding = offset - last_size
            format_spec_parts.append(padding_spec(padding))
            fieldfmt, bf_ndim, bf_shape = buffer_info(ctype)
            if bf_shape:
                format_spec_parts.extend(('(', ','.join((str(n) for n in bf_shape)), ')'))
            if fieldfmt is None:
                fieldfmt = 'B'
            if isinstance(name, bytes):
                raise TypeError(f'field {name!r}: name must be a string, not bytes')
            format_spec_parts.append(f'{fieldfmt}:{name}:')
        result_fields.append(CField(name=name, type=ctype, byte_size=type_size, byte_offset=offset, bit_size=bit_size if is_bitfield else None, bit_offset=bit_offset if is_bitfield else None, index=i, _internal_use=True))
        if is_bitfield and (not gcc_layout):
            assert type_bit_size > 0
        align = max(align, type_align)
        last_size = struct_size
        if not is_struct:
            union_size = max(struct_size, union_size)
    if is_struct:
        total_size = struct_size
    else:
        total_size = union_size
    aligned_size = round_up(total_size, align)
    if is_struct:
        padding = aligned_size - total_size
        format_spec_parts.append(padding_spec(padding))
        format_spec_parts.append('}')
    return StructUnionLayout(fields=result_fields, size=aligned_size, align=align, format_spec=''.join(format_spec_parts))

def padding_spec(padding):
    if padding <= 0:
        return ''
    if padding == 1:
        return 'x'
    return f'{padding}x'


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# ---- 转发层结束 ----
