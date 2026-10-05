# -*- coding: utf-8 -*-
"""区域设置 —— 汉语库（由 tools/汉化库.py 从 Lib/locale.py 机械生成，**不要手改**）。

英文库 Lib/locale.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 区域设置
"""


"""Locale support module.

The module provides low-level access to the C lib's locale APIs and adds high
level number formatting APIs as well as a locale aliasing engine to complement
these.

The aliasing engine includes support for many commonly used locale names and
maps them to values suitable for passing to the C lib's setlocale() function. It
also includes default encodings for all supported locale names.

"""
_英文原名表 = {'atof': '转浮点', 'atoi': '转整数', 'currency': '货币', 'delocalize': '去本地化', 'format_string': '格式化字符串', 'getdefaultlocale': '取默认区域', 'getlocale': '取区域', 'getpreferredencoding': '取首选编码', 'locale_alias': '区域别名', 'locale_encoding_alias': '区域编码别名', 'localize': '本地化', 'normalize': '规范化', 'windows_locale': 'Windows区域'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import sys
import encodings
import encodings.aliases
import _collections_abc
from builtins import str as _builtin_str
import functools
__all__ = ['getlocale', 'getdefaultlocale', 'getpreferredencoding', 'Error', 'setlocale', 'localeconv', 'strcoll', 'strxfrm', 'str', 'atof', 'atoi', 'format_string', 'currency', 'normalize', 'LC_CTYPE', 'LC_COLLATE', 'LC_TIME', 'LC_MONETARY', 'LC_NUMERIC', 'LC_ALL', 'CHAR_MAX', 'getencoding']

def _strcoll(a, b):
    """ strcoll(string,string) -> int.
        Compares two strings according to the locale.
    """
    return (a > b) - (a < b)

def _strxfrm(s):
    """ strxfrm(string) -> string.
        Returns a string that behaves for cmp locale-aware.
    """
    return s
try:
    from _locale import *
except ImportError:
    CHAR_MAX = 127
    LC_ALL = 6
    LC_COLLATE = 3
    LC_CTYPE = 0
    LC_MESSAGES = 5
    LC_MONETARY = 4
    LC_NUMERIC = 1
    LC_TIME = 2
    Error = ValueError

    def localeconv():
        """ localeconv() -> dict.
            Returns numeric and monetary locale-specific parameters.
        """
        return {'grouping': [127], 'currency_symbol': '', 'n_sign_posn': 127, 'p_cs_precedes': 127, 'n_cs_precedes': 127, 'mon_grouping': [], 'n_sep_by_space': 127, 'decimal_point': '.', 'negative_sign': '', 'positive_sign': '', 'p_sep_by_space': 127, 'int_curr_symbol': '', 'p_sign_posn': 127, 'thousands_sep': '', 'mon_thousands_sep': '', 'frac_digits': 127, 'mon_decimal_point': '', 'int_frac_digits': 127}

    def setlocale(category, value=None):
        """ setlocale(integer,string=None) -> string.
            Activates/queries locale processing.
        """
        if value not in (None, '', 'C'):
            raise Error('_locale emulation only supports "C" locale')
        return 'C'
if 'strxfrm' not in globals():
    strxfrm = _strxfrm
if 'strcoll' not in globals():
    strcoll = _strcoll
_localeconv = localeconv
_override_localeconv = {}

@functools.wraps(_localeconv)
def localeconv():
    d = _localeconv()
    if _override_localeconv:
        d.update(_override_localeconv)
    return d

def _grouping_intervals(grouping):
    last_interval = None
    for interval in grouping:
        if interval == CHAR_MAX:
            return
        if interval == 0:
            if last_interval is None:
                raise ValueError('invalid grouping')
            while True:
                yield last_interval
        yield interval
        last_interval = interval

def _group(s, monetary=False):
    conv = localeconv()
    thousands_sep = conv[monetary and 'mon_thousands_sep' or 'thousands_sep']
    grouping = conv[monetary and 'mon_grouping' or 'grouping']
    if not grouping:
        return (s, 0)
    if s[-1] == ' ':
        stripped = s.rstrip()
        right_spaces = s[len(stripped):]
        s = stripped
    else:
        right_spaces = ''
    left_spaces = ''
    groups = []
    for interval in _grouping_intervals(grouping):
        if not s or s[-1] not in '0123456789':
            left_spaces = s
            s = ''
            break
        groups.append(s[-interval:])
        s = s[:-interval]
    if s:
        groups.append(s)
    groups.reverse()
    return (left_spaces + thousands_sep.join(groups) + right_spaces, len(thousands_sep) * (len(groups) - 1))

def _strip_padding(s, amount):
    lpos = 0
    while amount and s[lpos] == ' ':
        lpos += 1
        amount -= 1
    rpos = len(s) - 1
    while amount and s[rpos] == ' ':
        rpos -= 1
        amount -= 1
    return s[lpos:rpos + 1]
_percent_re = None

def _format(percent, value, grouping=False, monetary=False, *additional):
    if additional:
        formatted = percent % ((value,) + additional)
    else:
        formatted = percent % value
    if percent[-1] in 'eEfFgGdiu':
        formatted = _localize(formatted, grouping, monetary)
    return formatted

def _localize(formatted, grouping=False, monetary=False):
    if '.' in formatted:
        seps = 0
        parts = formatted.split('.')
        if grouping:
            parts[0], seps = _group(parts[0], monetary=monetary)
        decimal_point = localeconv()[monetary and 'mon_decimal_point' or 'decimal_point']
        formatted = decimal_point.join(parts)
        if seps:
            formatted = _strip_padding(formatted, seps)
    else:
        seps = 0
        if grouping:
            formatted, seps = _group(formatted, monetary=monetary)
        if seps:
            formatted = _strip_padding(formatted, seps)
    return formatted

def 格式化字符串(f, val, grouping=False, monetary=False):
    """Formats a string in the same way that the % formatting would use,
    but takes the current locale into account.

    Grouping is applied if the third parameter is true.
    Conversion uses monetary thousands separator and grouping strings if
    forth parameter monetary is true."""
    global _percent_re
    if _percent_re is None:
        import re
        _percent_re = re.compile('%(?:\\((?P<key>.*?)\\))?(?P<modifiers>[-#0-9 +*.hlL]*?)[eEfFgGdiouxXcrs%]')
    percents = list(_percent_re.finditer(f))
    new_f = _percent_re.sub('%s', f)
    if isinstance(val, _collections_abc.Mapping):
        new_val = []
        for perc in percents:
            if perc.group()[-1] == '%':
                new_val.append('%')
            else:
                new_val.append(_format(perc.group(), val, grouping, monetary))
    else:
        if not isinstance(val, tuple):
            val = (val,)
        new_val = []
        i = 0
        for perc in percents:
            if perc.group()[-1] == '%':
                new_val.append('%')
            else:
                starcount = perc.group('modifiers').count('*')
                new_val.append(_format(perc.group(), val[i], grouping, monetary, *val[i + 1:i + 1 + starcount]))
                i += 1 + starcount
    val = tuple(new_val)
    return new_f % val

def 货币(val, symbol=True, grouping=False, international=False):
    """Formats val according to the currency settings
    in the current locale."""
    conv = localeconv()
    digits = conv[international and 'int_frac_digits' or 'frac_digits']
    if digits == 127:
        raise ValueError("Currency formatting is not possible using the 'C' locale.")
    s = _localize(f'{abs(val):.{digits}f}', grouping, monetary=True)
    s = '<' + s + '>'
    if symbol:
        smb = conv[international and 'int_curr_symbol' or 'currency_symbol']
        precedes = conv[val < 0 and 'n_cs_precedes' or 'p_cs_precedes']
        separated = conv[val < 0 and 'n_sep_by_space' or 'p_sep_by_space']
        if precedes:
            s = smb + (separated and ' ' or '') + s
        else:
            if international and smb[-1] == ' ':
                smb = smb[:-1]
            s = s + (separated and ' ' or '') + smb
    sign_pos = conv[val < 0 and 'n_sign_posn' or 'p_sign_posn']
    sign = conv[val < 0 and 'negative_sign' or 'positive_sign']
    if sign_pos == 0:
        s = '(' + s + ')'
    elif sign_pos == 1:
        s = sign + s
    elif sign_pos == 2:
        s = s + sign
    elif sign_pos == 3:
        s = s.replace('<', sign)
    elif sign_pos == 4:
        s = s.replace('>', sign)
    else:
        s = sign + s
    return s.replace('<', '').replace('>', '')

def str(val):
    """Convert float to string, taking the locale into account."""
    return _format('%.12g', val)

def 去本地化(string):
    """Parses a string as a normalized number according to the locale settings."""
    conv = localeconv()
    ts = conv['thousands_sep']
    if ts:
        string = string.replace(ts, '')
    dd = conv['decimal_point']
    if dd:
        string = string.replace(dd, '.')
    return string

def 本地化(string, grouping=False, monetary=False):
    """Parses a string as locale number according to the locale settings."""
    return _localize(string, grouping, monetary)

def 转浮点(string, func=float):
    """Parses a string as a float according to the locale settings."""
    return func(去本地化(string))

def 转整数(string):
    """Converts a string to an integer according to the locale settings."""
    return int(去本地化(string))

def _test():
    setlocale(LC_ALL, '')
    s1 = 格式化字符串('%d', 123456789, 1)
    print(s1, 'is', 转整数(s1))
    s1 = str(3.14)
    print(s1, 'is', 转浮点(s1))
_setlocale = setlocale

def _replace_encoding(code, encoding):
    if '.' in code:
        langname = code[:code.index('.')]
    else:
        langname = code
    norm_encoding = encodings.normalize_encoding(encoding)
    norm_encoding = encodings.aliases.aliases.get(norm_encoding.lower(), norm_encoding)
    encoding = norm_encoding
    norm_encoding = norm_encoding.lower()
    if norm_encoding in 区域编码别名:
        encoding = 区域编码别名[norm_encoding]
    else:
        norm_encoding = norm_encoding.replace('_', '')
        norm_encoding = norm_encoding.replace('-', '')
        if norm_encoding in 区域编码别名:
            encoding = 区域编码别名[norm_encoding]
    return langname + '.' + encoding

def _append_modifier(code, modifier):
    if modifier == 'euro':
        if '.' not in code:
            return code + '.ISO8859-15'
        _, _, encoding = code.partition('.')
        if encoding in ('ISO8859-15', 'UTF-8'):
            return code
        if encoding == 'ISO8859-1':
            return _replace_encoding(code, 'ISO8859-15')
    return code + '@' + modifier

def 规范化(localename):
    """ Returns a normalized locale code for the given locale
        name.

        The returned locale code is formatted for use with
        setlocale().

        If normalization fails, the original name is returned
        unchanged.

        If the given encoding is not known, the function defaults to
        the default encoding for the locale code just like setlocale()
        does.

    """
    code = localename.lower()
    if ':' in code:
        code = code.replace(':', '.')
    if '@' in code:
        code, modifier = code.split('@', 1)
    else:
        modifier = ''
    if '.' in code:
        langname, encoding = code.split('.')[:2]
    else:
        langname = code
        encoding = ''
    lang_enc = langname
    if encoding:
        norm_encoding = encoding.replace('-', '')
        norm_encoding = norm_encoding.replace('_', '')
        lang_enc += '.' + norm_encoding
    lookup_name = lang_enc
    if modifier:
        lookup_name += '@' + modifier
    code = 区域别名.get(lookup_name, None)
    if code is not None:
        return code
    if modifier:
        code = 区域别名.get(lang_enc, None)
        if code is not None:
            if '@' not in code:
                return _append_modifier(code, modifier)
            if code.split('@', 1)[1].lower() == modifier:
                return code
    if encoding:
        lookup_name = langname
        if modifier:
            lookup_name += '@' + modifier
        code = 区域别名.get(lookup_name, None)
        if code is not None:
            if '@' not in code:
                return _replace_encoding(code, encoding)
            code, modifier = code.split('@', 1)
            return _replace_encoding(code, encoding) + '@' + modifier
        if modifier:
            code = 区域别名.get(langname, None)
            if code is not None:
                if '@' not in code:
                    code = _replace_encoding(code, encoding)
                    return _append_modifier(code, modifier)
                code, defmod = code.split('@', 1)
                if defmod.lower() == modifier:
                    return _replace_encoding(code, encoding) + '@' + defmod
    return localename

def _parse_localename(localename):
    """ Parses the locale code for localename and returns the
        result as tuple (language code, encoding).

        The localename is normalized and passed through the locale
        alias engine. A ValueError is raised in case the locale name
        cannot be parsed.

        The language code corresponds to RFC 1766.  code and encoding
        can be None in case the values cannot be determined or are
        unknown to this implementation.

    """
    code = 规范化(localename)
    if '@' in code:
        code, modifier = code.split('@', 1)
        if modifier == 'euro' and '.' not in code:
            return (code, 'iso-8859-15')
    if '.' in code:
        return tuple(code.split('.')[:2])
    elif code == 'C':
        return (None, None)
    elif code == 'UTF-8':
        return (None, 'UTF-8')
    raise ValueError('unknown locale: %s' % localename)

def _build_localename(localetuple):
    """ Builds a locale code from the given tuple (language code,
        encoding).

        No aliasing or normalizing takes place.

    """
    try:
        language, encoding = localetuple
        if language is None:
            language = 'C'
        if encoding is None:
            return language
        else:
            return language + '.' + encoding
    except (TypeError, ValueError):
        raise TypeError('Locale must be None, a string, or an iterable of two strings -- language code, encoding.') from None

def 取默认区域(envvars=('LC_ALL', 'LC_CTYPE', 'LANG', 'LANGUAGE')):
    """ Tries to determine the default locale settings and returns
        them as tuple (language code, encoding).

        According to POSIX, a program which has not called
        setlocale(LC_ALL, "") runs using the portable 'C' locale.
        Calling setlocale(LC_ALL, "") lets it use the default locale as
        defined by the LANG variable. Since we don't want to interfere
        with the current locale setting we thus emulate the behavior
        in the way described above.

        To maintain compatibility with other platforms, not only the
        LANG variable is tested, but a list of variables given as
        envvars parameter. The first found to be defined will be
        used. envvars defaults to the search path used in GNU gettext;
        it must always contain the variable name 'LANG'.

        Except for the code 'C', the language code corresponds to RFC
        1766.  code and encoding can be None in case the values cannot
        be determined.

    """
    return _getdefaultlocale(envvars)

def _getdefaultlocale(envvars=('LC_ALL', 'LC_CTYPE', 'LANG', 'LANGUAGE')):
    try:
        import _locale
        code, encoding = _locale._getdefaultlocale()
    except (ImportError, AttributeError):
        pass
    else:
        if sys.platform == 'win32' and code and (code[:2] == '0x'):
            code = Windows区域.get(int(code, 0))
        return (code, encoding)
    import os
    lookup = os.environ.get
    for variable in envvars:
        localename = lookup(variable, None)
        if localename:
            if variable == 'LANGUAGE':
                localename = localename.split(':')[0]
            break
    else:
        localename = 'C'
    return _parse_localename(localename)

def 取区域(category=LC_CTYPE):
    """ Returns the current setting for the given locale category as
        tuple (language code, encoding).

        category may be one of the LC_* value except LC_ALL. It
        defaults to LC_CTYPE.

        Except for the code 'C', the language code corresponds to RFC
        1766.  code and encoding can be None in case the values cannot
        be determined.

    """
    localename = _setlocale(category)
    if category == LC_ALL and ';' in localename:
        raise TypeError('category LC_ALL is not supported')
    return _parse_localename(localename)

def setlocale(category, locale=None):
    """ Set the locale for the given category.  The locale can be
        a string, an iterable of two strings (language code and encoding),
        or None.

        Iterables are converted to strings using the locale aliasing
        engine.  Locale strings are passed directly to the C lib.

        category may be given as one of the LC_* values.

    """
    if locale and (not isinstance(locale, _builtin_str)):
        locale = 规范化(_build_localename(locale))
    return _setlocale(category, locale)
try:
    from _locale import getencoding
except ImportError:

    def getencoding():
        return sys.getfilesystemencoding()
try:
    CODESET
except NameError:

    def 取首选编码(do_setlocale=True):
        """Return the charset that the user is likely using."""
        if sys.flags.warn_default_encoding:
            import warnings
            warnings.warn('UTF-8 Mode affects locale.getpreferredencoding(). Consider locale.getencoding() instead.', EncodingWarning, 2)
        if sys.flags.utf8_mode:
            return 'utf-8'
        return getencoding()
else:

    def 取首选编码(do_setlocale=True):
        """Return the charset that the user is likely using,
        according to the system configuration."""
        if sys.flags.warn_default_encoding:
            import warnings
            warnings.warn('UTF-8 Mode affects locale.getpreferredencoding(). Consider locale.getencoding() instead.', EncodingWarning, 2)
        if sys.flags.utf8_mode:
            return 'utf-8'
        if not do_setlocale:
            return getencoding()
        old_loc = setlocale(LC_CTYPE)
        try:
            try:
                setlocale(LC_CTYPE, '')
            except Error:
                pass
            return getencoding()
        finally:
            setlocale(LC_CTYPE, old_loc)
区域编码别名 = {'437': 'C', 'c': 'C', 'en': 'ISO8859-1', 'jis': 'JIS7', 'jis7': 'JIS7', 'ajec': 'eucJP', 'koi8c': 'KOI8-C', 'microsoftcp1251': 'CP1251', 'microsoftcp1255': 'CP1255', 'microsoftcp1256': 'CP1256', '88591': 'ISO8859-1', '88592': 'ISO8859-2', '88595': 'ISO8859-5', '885915': 'ISO8859-15', 'ascii': 'ISO8859-1', 'latin_1': 'ISO8859-1', 'iso8859_1': 'ISO8859-1', 'iso8859_10': 'ISO8859-10', 'iso8859_11': 'ISO8859-11', 'iso8859_13': 'ISO8859-13', 'iso8859_14': 'ISO8859-14', 'iso8859_15': 'ISO8859-15', 'iso8859_16': 'ISO8859-16', 'iso8859_2': 'ISO8859-2', 'iso8859_3': 'ISO8859-3', 'iso8859_4': 'ISO8859-4', 'iso8859_5': 'ISO8859-5', 'iso8859_6': 'ISO8859-6', 'iso8859_7': 'ISO8859-7', 'iso8859_8': 'ISO8859-8', 'iso8859_9': 'ISO8859-9', 'iso2022_jp': 'JIS7', 'shift_jis': 'SJIS', 'tactis': 'TACTIS', 'euc_jp': 'eucJP', 'euc_kr': 'eucKR', 'utf_8': 'UTF-8', 'koi8_r': 'KOI8-R', 'koi8_t': 'KOI8-T', 'koi8_u': 'KOI8-U', 'kz1048': 'RK1048', 'cp1251': 'CP1251', 'cp1255': 'CP1255', 'cp1256': 'CP1256'}
for k, v in sorted(区域编码别名.items()):
    k = k.replace('_', '')
    区域编码别名.setdefault(k, v)
del k, v
区域别名 = {'a3': 'az_AZ.KOI8-C', 'a3_az': 'az_AZ.KOI8-C', 'a3_az.koic': 'az_AZ.KOI8-C', 'aa_dj': 'aa_DJ.ISO8859-1', 'aa_er': 'aa_ER.UTF-8', 'aa_et': 'aa_ET.UTF-8', 'af': 'af_ZA.ISO8859-1', 'af_za': 'af_ZA.ISO8859-1', 'agr_pe': 'agr_PE.UTF-8', 'ak_gh': 'ak_GH.UTF-8', 'am': 'am_ET.UTF-8', 'am_et': 'am_ET.UTF-8', 'american': 'en_US.ISO8859-1', 'an_es': 'an_ES.ISO8859-15', 'anp_in': 'anp_IN.UTF-8', 'ar': 'ar_AA.ISO8859-6', 'ar_aa': 'ar_AA.ISO8859-6', 'ar_ae': 'ar_AE.ISO8859-6', 'ar_bh': 'ar_BH.ISO8859-6', 'ar_dz': 'ar_DZ.ISO8859-6', 'ar_eg': 'ar_EG.ISO8859-6', 'ar_in': 'ar_IN.UTF-8', 'ar_iq': 'ar_IQ.ISO8859-6', 'ar_jo': 'ar_JO.ISO8859-6', 'ar_kw': 'ar_KW.ISO8859-6', 'ar_lb': 'ar_LB.ISO8859-6', 'ar_ly': 'ar_LY.ISO8859-6', 'ar_ma': 'ar_MA.ISO8859-6', 'ar_om': 'ar_OM.ISO8859-6', 'ar_qa': 'ar_QA.ISO8859-6', 'ar_sa': 'ar_SA.ISO8859-6', 'ar_sd': 'ar_SD.ISO8859-6', 'ar_ss': 'ar_SS.UTF-8', 'ar_sy': 'ar_SY.ISO8859-6', 'ar_tn': 'ar_TN.ISO8859-6', 'ar_ye': 'ar_YE.ISO8859-6', 'arabic': 'ar_AA.ISO8859-6', 'as': 'as_IN.UTF-8', 'as_in': 'as_IN.UTF-8', 'ast_es': 'ast_ES.ISO8859-15', 'ayc_pe': 'ayc_PE.UTF-8', 'az': 'az_AZ.ISO8859-9E', 'az_az': 'az_AZ.ISO8859-9E', 'az_az.iso88599e': 'az_AZ.ISO8859-9E', 'az_ir': 'az_IR.UTF-8', 'be': 'be_BY.CP1251', 'be@latin': 'be_BY.UTF-8@latin', 'be_bg.utf8': 'bg_BG.UTF-8', 'be_by': 'be_BY.CP1251', 'be_by@latin': 'be_BY.UTF-8@latin', 'bem_zm': 'bem_ZM.UTF-8', 'ber_dz': 'ber_DZ.UTF-8', 'ber_ma': 'ber_MA.UTF-8', 'bg': 'bg_BG.CP1251', 'bg_bg': 'bg_BG.CP1251', 'bhb_in.utf8': 'bhb_IN.UTF-8', 'bho_in': 'bho_IN.UTF-8', 'bho_np': 'bho_NP.UTF-8', 'bi_vu': 'bi_VU.UTF-8', 'bn_bd': 'bn_BD.UTF-8', 'bn_in': 'bn_IN.UTF-8', 'bo_cn': 'bo_CN.UTF-8', 'bo_in': 'bo_IN.UTF-8', 'bokmal': 'nb_NO.ISO8859-1', 'bokmål': 'nb_NO.ISO8859-1', 'br': 'br_FR.ISO8859-1', 'br_fr': 'br_FR.ISO8859-1', 'brx_in': 'brx_IN.UTF-8', 'bs': 'bs_BA.ISO8859-2', 'bs_ba': 'bs_BA.ISO8859-2', 'bulgarian': 'bg_BG.CP1251', 'byn_er': 'byn_ER.UTF-8', 'c': 'C', 'c-french': 'fr_CA.ISO8859-1', 'c.ascii': 'C', 'c.en': 'C', 'c.iso88591': 'en_US.ISO8859-1', 'c_c': 'C', 'c_c.c': 'C', 'ca': 'ca_ES.ISO8859-1', 'ca_ad': 'ca_AD.ISO8859-1', 'ca_es': 'ca_ES.ISO8859-1', 'ca_es@valencia': 'ca_ES.UTF-8@valencia', 'ca_fr': 'ca_FR.ISO8859-1', 'ca_it': 'ca_IT.ISO8859-1', 'catalan': 'ca_ES.ISO8859-1', 'ce_ru': 'ce_RU.UTF-8', 'cextend': 'en_US.ISO8859-1', 'chinese-s': 'zh_CN.eucCN', 'chinese-t': 'zh_TW.eucTW', 'chr_us': 'chr_US.UTF-8', 'ckb_iq': 'ckb_IQ.UTF-8', 'cmn_tw': 'cmn_TW.UTF-8', 'crh_ru': 'crh_RU.UTF-8', 'crh_ua': 'crh_UA.UTF-8', 'croatian': 'hr_HR.ISO8859-2', 'cs': 'cs_CZ.ISO8859-2', 'cs_cs': 'cs_CZ.ISO8859-2', 'cs_cz': 'cs_CZ.ISO8859-2', 'csb_pl': 'csb_PL.UTF-8', 'cv_ru': 'cv_RU.UTF-8', 'cy': 'cy_GB.ISO8859-1', 'cy_gb': 'cy_GB.ISO8859-1', 'cz': 'cs_CZ.ISO8859-2', 'cz_cz': 'cs_CZ.ISO8859-2', 'czech': 'cs_CZ.ISO8859-2', 'da': 'da_DK.ISO8859-1', 'da_dk': 'da_DK.ISO8859-1', 'danish': 'da_DK.ISO8859-1', 'dansk': 'da_DK.ISO8859-1', 'de': 'de_DE.ISO8859-1', 'de_at': 'de_AT.ISO8859-1', 'de_be': 'de_BE.ISO8859-1', 'de_ch': 'de_CH.ISO8859-1', 'de_de': 'de_DE.ISO8859-1', 'de_it': 'de_IT.UTF-8', 'de_li': 'de_LI.ISO8859-1', 'de_lu': 'de_LU.ISO8859-1', 'deutsch': 'de_DE.ISO8859-1', 'doi_in': 'doi_IN.UTF-8', 'dsb_de': 'dsb_DE.UTF-8', 'dutch': 'nl_NL.ISO8859-1', 'dutch.iso88591': 'nl_BE.ISO8859-1', 'dv_mv': 'dv_MV.UTF-8', 'dz_bt': 'dz_BT.UTF-8', 'ee': 'ee_EE.ISO8859-4', 'ee_ee': 'ee_EE.ISO8859-4', 'eesti': 'et_EE.ISO8859-1', 'el': 'el_GR.ISO8859-7', 'el_cy': 'el_CY.ISO8859-7', 'el_gr': 'el_GR.ISO8859-7', 'el_gr@euro': 'el_GR.ISO8859-15', 'en': 'en_US.ISO8859-1', 'en_ag': 'en_AG.UTF-8', 'en_au': 'en_AU.ISO8859-1', 'en_be': 'en_BE.ISO8859-1', 'en_bw': 'en_BW.ISO8859-1', 'en_ca': 'en_CA.ISO8859-1', 'en_dk': 'en_DK.ISO8859-1', 'en_dl.utf8': 'en_DL.UTF-8', 'en_gb': 'en_GB.ISO8859-1', 'en_hk': 'en_HK.ISO8859-1', 'en_ie': 'en_IE.ISO8859-1', 'en_il': 'en_IL.ISO8859-1', 'en_in': 'en_IN.ISO8859-1', 'en_ng': 'en_NG.UTF-8', 'en_nz': 'en_NZ.ISO8859-1', 'en_ph': 'en_PH.ISO8859-1', 'en_sc.utf8': 'en_SC.UTF-8', 'en_sg': 'en_SG.ISO8859-1', 'en_uk': 'en_GB.ISO8859-1', 'en_us': 'en_US.ISO8859-1', 'en_us@euro@euro': 'en_US.ISO8859-15', 'en_za': 'en_ZA.ISO8859-1', 'en_zm': 'en_ZM.UTF-8', 'en_zw': 'en_ZW.ISO8859-1', 'en_zw.utf8': 'en_ZS.UTF-8', 'eng_gb': 'en_GB.ISO8859-1', 'english': 'en_EN.ISO8859-1', 'english_uk': 'en_GB.ISO8859-1', 'english_united-states': 'en_US.ISO8859-1', 'english_united-states.437': 'C', 'english_us': 'en_US.ISO8859-1', 'eo': 'eo_XX.ISO8859-3', 'eo.utf8': 'eo.UTF-8', 'eo_eo': 'eo_EO.ISO8859-3', 'eo_us.utf8': 'eo_US.UTF-8', 'eo_xx': 'eo_XX.ISO8859-3', 'es': 'es_ES.ISO8859-1', 'es_ar': 'es_AR.ISO8859-1', 'es_bo': 'es_BO.ISO8859-1', 'es_cl': 'es_CL.ISO8859-1', 'es_co': 'es_CO.ISO8859-1', 'es_cr': 'es_CR.ISO8859-1', 'es_cu': 'es_CU.ISO8859-1', 'es_do': 'es_DO.ISO8859-1', 'es_ec': 'es_EC.ISO8859-1', 'es_es': 'es_ES.ISO8859-1', 'es_gt': 'es_GT.ISO8859-1', 'es_hn': 'es_HN.ISO8859-1', 'es_mx': 'es_MX.ISO8859-1', 'es_ni': 'es_NI.ISO8859-1', 'es_pa': 'es_PA.ISO8859-1', 'es_pe': 'es_PE.ISO8859-1', 'es_pr': 'es_PR.ISO8859-1', 'es_py': 'es_PY.ISO8859-1', 'es_sv': 'es_SV.ISO8859-1', 'es_us': 'es_US.ISO8859-1', 'es_uy': 'es_UY.ISO8859-1', 'es_ve': 'es_VE.ISO8859-1', 'estonian': 'et_EE.ISO8859-1', 'et': 'et_EE.ISO8859-15', 'et_ee': 'et_EE.ISO8859-15', 'eu': 'eu_ES.ISO8859-1', 'eu_es': 'eu_ES.ISO8859-1', 'eu_fr': 'eu_FR.ISO8859-1', 'fa': 'fa_IR.UTF-8', 'fa_ir': 'fa_IR.UTF-8', 'fa_ir.isiri3342': 'fa_IR.ISIRI-3342', 'ff_sn': 'ff_SN.UTF-8', 'fi': 'fi_FI.ISO8859-15', 'fi_fi': 'fi_FI.ISO8859-15', 'fil_ph': 'fil_PH.UTF-8', 'finnish': 'fi_FI.ISO8859-1', 'fo': 'fo_FO.ISO8859-1', 'fo_fo': 'fo_FO.ISO8859-1', 'fr': 'fr_FR.ISO8859-1', 'fr_be': 'fr_BE.ISO8859-1', 'fr_ca': 'fr_CA.ISO8859-1', 'fr_ch': 'fr_CH.ISO8859-1', 'fr_fr': 'fr_FR.ISO8859-1', 'fr_lu': 'fr_LU.ISO8859-1', 'français': 'fr_FR.ISO8859-1', 'fre_fr': 'fr_FR.ISO8859-1', 'french': 'fr_FR.ISO8859-1', 'french.iso88591': 'fr_CH.ISO8859-1', 'french_france': 'fr_FR.ISO8859-1', 'fur_it': 'fur_IT.UTF-8', 'fy_de': 'fy_DE.UTF-8', 'fy_nl': 'fy_NL.UTF-8', 'ga': 'ga_IE.ISO8859-1', 'ga_ie': 'ga_IE.ISO8859-1', 'galego': 'gl_ES.ISO8859-1', 'galician': 'gl_ES.ISO8859-1', 'gbm_in': 'gbm_IN.UTF-8', 'gd': 'gd_GB.ISO8859-1', 'gd_gb': 'gd_GB.ISO8859-1', 'ger_de': 'de_DE.ISO8859-1', 'german': 'de_DE.ISO8859-1', 'german.iso88591': 'de_CH.ISO8859-1', 'german_germany': 'de_DE.ISO8859-1', 'gez_er': 'gez_ER.UTF-8', 'gez_et': 'gez_ET.UTF-8', 'gl': 'gl_ES.ISO8859-1', 'gl_es': 'gl_ES.ISO8859-1', 'greek': 'el_GR.ISO8859-7', 'gu_in': 'gu_IN.UTF-8', 'gv': 'gv_GB.ISO8859-1', 'gv_gb': 'gv_GB.ISO8859-1', 'ha_ng': 'ha_NG.UTF-8', 'hak_tw': 'hak_TW.UTF-8', 'he': 'he_IL.ISO8859-8', 'he_il': 'he_IL.ISO8859-8', 'hebrew': 'he_IL.ISO8859-8', 'hi': 'hi_IN.ISCII-DEV', 'hi_in': 'hi_IN.ISCII-DEV', 'hi_in.isciidev': 'hi_IN.ISCII-DEV', 'hif_fj': 'hif_FJ.UTF-8', 'hne': 'hne_IN.UTF-8', 'hne_in': 'hne_IN.UTF-8', 'hr': 'hr_HR.ISO8859-2', 'hr_hr': 'hr_HR.ISO8859-2', 'hrvatski': 'hr_HR.ISO8859-2', 'hsb_de': 'hsb_DE.ISO8859-2', 'ht_ht': 'ht_HT.UTF-8', 'hu': 'hu_HU.ISO8859-2', 'hu_hu': 'hu_HU.ISO8859-2', 'hungarian': 'hu_HU.ISO8859-2', 'hy_am': 'hy_AM.UTF-8', 'hy_am.armscii8': 'hy_AM.ARMSCII_8', 'ia': 'ia.UTF-8', 'ia_fr': 'ia_FR.UTF-8', 'icelandic': 'is_IS.ISO8859-1', 'id': 'id_ID.ISO8859-1', 'id_id': 'id_ID.ISO8859-1', 'ie': 'ie.UTF-8', 'ig_ng': 'ig_NG.UTF-8', 'ik_ca': 'ik_CA.UTF-8', 'in': 'id_ID.ISO8859-1', 'in_id': 'id_ID.ISO8859-1', 'is': 'is_IS.ISO8859-1', 'is_is': 'is_IS.ISO8859-1', 'iso-8859-1': 'en_US.ISO8859-1', 'iso-8859-15': 'en_US.ISO8859-15', 'iso8859-1': 'en_US.ISO8859-1', 'iso8859-15': 'en_US.ISO8859-15', 'iso_8859_1': 'en_US.ISO8859-1', 'iso_8859_15': 'en_US.ISO8859-15', 'it': 'it_IT.ISO8859-1', 'it_ch': 'it_CH.ISO8859-1', 'it_it': 'it_IT.ISO8859-1', 'italian': 'it_IT.ISO8859-1', 'iu': 'iu_CA.NUNACOM-8', 'iu_ca': 'iu_CA.NUNACOM-8', 'iu_ca.nunacom8': 'iu_CA.NUNACOM-8', 'iw': 'he_IL.ISO8859-8', 'iw_il': 'he_IL.ISO8859-8', 'iw_il.utf8': 'iw_IL.UTF-8', 'ja': 'ja_JP.eucJP', 'ja_jp': 'ja_JP.eucJP', 'ja_jp.euc': 'ja_JP.eucJP', 'ja_jp.mscode': 'ja_JP.SJIS', 'ja_jp.pck': 'ja_JP.SJIS', 'japan': 'ja_JP.eucJP', 'japanese': 'ja_JP.eucJP', 'japanese-euc': 'ja_JP.eucJP', 'japanese.euc': 'ja_JP.eucJP', 'jp_jp': 'ja_JP.eucJP', 'ka': 'ka_GE.GEORGIAN-ACADEMY', 'ka_ge': 'ka_GE.GEORGIAN-ACADEMY', 'ka_ge.georgianacademy': 'ka_GE.GEORGIAN-ACADEMY', 'ka_ge.georgianps': 'ka_GE.GEORGIAN-PS', 'ka_ge.georgianrs': 'ka_GE.GEORGIAN-ACADEMY', 'kab_dz': 'kab_DZ.UTF-8', 'kk_kz': 'kk_KZ.ptcp154', 'kl': 'kl_GL.ISO8859-1', 'kl_gl': 'kl_GL.ISO8859-1', 'km_kh': 'km_KH.UTF-8', 'kn': 'kn_IN.UTF-8', 'kn_in': 'kn_IN.UTF-8', 'ko': 'ko_KR.eucKR', 'ko_kr': 'ko_KR.eucKR', 'ko_kr.euc': 'ko_KR.eucKR', 'kok_in': 'kok_IN.UTF-8', 'korean': 'ko_KR.eucKR', 'korean.euc': 'ko_KR.eucKR', 'ks': 'ks_IN.UTF-8', 'ks_in': 'ks_IN.UTF-8', 'ks_in@devanagari.utf8': 'ks_IN.UTF-8@devanagari', 'ku_tr': 'ku_TR.ISO8859-9', 'kv_ru': 'kv_RU.UTF-8', 'kw': 'kw_GB.ISO8859-1', 'kw_gb': 'kw_GB.ISO8859-1', 'ky': 'ky_KG.UTF-8', 'ky_kg': 'ky_KG.UTF-8', 'lb_lu': 'lb_LU.UTF-8', 'lg_ug': 'lg_UG.ISO8859-10', 'li_be': 'li_BE.UTF-8', 'li_nl': 'li_NL.UTF-8', 'lij_it': 'lij_IT.UTF-8', 'lithuanian': 'lt_LT.ISO8859-13', 'ln_cd': 'ln_CD.UTF-8', 'lo': 'lo_LA.MULELAO-1', 'lo_la': 'lo_LA.MULELAO-1', 'lo_la.cp1133': 'lo_LA.IBM-CP1133', 'lo_la.ibmcp1133': 'lo_LA.IBM-CP1133', 'lo_la.mulelao1': 'lo_LA.MULELAO-1', 'lt': 'lt_LT.ISO8859-13', 'lt_lt': 'lt_LT.ISO8859-13', 'ltg_lv.utf8': 'ltg_LV.UTF-8', 'lv': 'lv_LV.ISO8859-13', 'lv_lv': 'lv_LV.ISO8859-13', 'lzh_tw': 'lzh_TW.UTF-8', 'mag_in': 'mag_IN.UTF-8', 'mai': 'mai_IN.UTF-8', 'mai_in': 'mai_IN.UTF-8', 'mai_np': 'mai_NP.UTF-8', 'mdf_ru': 'mdf_RU.UTF-8', 'mfe_mu': 'mfe_MU.UTF-8', 'mg_mg': 'mg_MG.ISO8859-15', 'mhr_ru': 'mhr_RU.UTF-8', 'mi': 'mi_NZ.ISO8859-1', 'mi_nz': 'mi_NZ.ISO8859-1', 'miq_ni': 'miq_NI.UTF-8', 'mjw_in': 'mjw_IN.UTF-8', 'mk': 'mk_MK.ISO8859-5', 'mk_mk': 'mk_MK.ISO8859-5', 'ml': 'ml_IN.UTF-8', 'ml_in': 'ml_IN.UTF-8', 'mn_mn': 'mn_MN.UTF-8', 'mni_in': 'mni_IN.UTF-8', 'mnw_mm': 'mnw_MM.UTF-8', 'mr': 'mr_IN.UTF-8', 'mr_in': 'mr_IN.UTF-8', 'ms': 'ms_MY.ISO8859-1', 'ms_my': 'ms_MY.ISO8859-1', 'mt': 'mt_MT.ISO8859-3', 'mt_mt': 'mt_MT.ISO8859-3', 'my_mm': 'my_MM.UTF-8', 'nan_tw': 'nan_TW.UTF-8', 'nb': 'nb_NO.ISO8859-1', 'nb_no': 'nb_NO.ISO8859-1', 'nds_de': 'nds_DE.UTF-8', 'nds_nl': 'nds_NL.UTF-8', 'ne_np': 'ne_NP.UTF-8', 'nhn_mx': 'nhn_MX.UTF-8', 'niu_nu': 'niu_NU.UTF-8', 'niu_nz': 'niu_NZ.UTF-8', 'nl': 'nl_NL.ISO8859-1', 'nl_aw': 'nl_AW.UTF-8', 'nl_be': 'nl_BE.ISO8859-1', 'nl_nl': 'nl_NL.ISO8859-1', 'nn': 'nn_NO.ISO8859-1', 'nn_no': 'nn_NO.ISO8859-1', 'no': 'no_NO.ISO8859-1', 'no@nynorsk': 'ny_NO.ISO8859-1', 'no_no': 'no_NO.ISO8859-1', 'no_no.iso88591@bokmal': 'no_NO.ISO8859-1', 'no_no.iso88591@nynorsk': 'no_NO.ISO8859-1', 'norwegian': 'no_NO.ISO8859-1', 'nr': 'nr_ZA.ISO8859-1', 'nr_za': 'nr_ZA.ISO8859-1', 'nso': 'nso_ZA.ISO8859-15', 'nso_za': 'nso_ZA.ISO8859-15', 'ny': 'ny_NO.ISO8859-1', 'ny_no': 'ny_NO.ISO8859-1', 'nynorsk': 'nn_NO.ISO8859-1', 'oc': 'oc_FR.ISO8859-1', 'oc_fr': 'oc_FR.ISO8859-1', 'om_et': 'om_ET.UTF-8', 'om_ke': 'om_KE.ISO8859-1', 'or': 'or_IN.UTF-8', 'or_in': 'or_IN.UTF-8', 'os_ru': 'os_RU.UTF-8', 'pa': 'pa_IN.UTF-8', 'pa_in': 'pa_IN.UTF-8', 'pa_pk': 'pa_PK.UTF-8', 'pap_an': 'pap_AN.UTF-8', 'pap_aw': 'pap_AW.UTF-8', 'pap_cw': 'pap_CW.UTF-8', 'pd': 'pd_US.ISO8859-1', 'pd_de': 'pd_DE.ISO8859-1', 'pd_us': 'pd_US.ISO8859-1', 'ph': 'ph_PH.ISO8859-1', 'ph_ph': 'ph_PH.ISO8859-1', 'pl': 'pl_PL.ISO8859-2', 'pl_pl': 'pl_PL.ISO8859-2', 'polish': 'pl_PL.ISO8859-2', 'portuguese': 'pt_PT.ISO8859-1', 'portuguese_brazil': 'pt_BR.ISO8859-1', 'posix': 'C', 'posix-utf2': 'C', 'pp': 'pp_AN.ISO8859-1', 'pp_an': 'pp_AN.ISO8859-1', 'ps_af': 'ps_AF.UTF-8', 'pt': 'pt_PT.ISO8859-1', 'pt_br': 'pt_BR.ISO8859-1', 'pt_pt': 'pt_PT.ISO8859-1', 'quz_pe': 'quz_PE.UTF-8', 'raj_in': 'raj_IN.UTF-8', 'rif_ma': 'rif_MA.UTF-8', 'ro': 'ro_RO.ISO8859-2', 'ro_ro': 'ro_RO.ISO8859-2', 'romanian': 'ro_RO.ISO8859-2', 'ru': 'ru_RU.UTF-8', 'ru_ru': 'ru_RU.UTF-8', 'ru_ua': 'ru_UA.KOI8-U', 'rumanian': 'ro_RO.ISO8859-2', 'russian': 'ru_RU.ISO8859-5', 'rw': 'rw_RW.ISO8859-1', 'rw_rw': 'rw_RW.ISO8859-1', 'sa_in': 'sa_IN.UTF-8', 'sah_ru': 'sah_RU.UTF-8', 'sat_in': 'sat_IN.UTF-8', 'sc_it': 'sc_IT.UTF-8', 'scn_it': 'scn_IT.UTF-8', 'sd': 'sd_IN.UTF-8', 'sd_in': 'sd_IN.UTF-8', 'sd_in@devanagari.utf8': 'sd_IN.UTF-8@devanagari', 'sd_pk': 'sd_PK.UTF-8', 'se_no': 'se_NO.UTF-8', 'serbocroatian': 'sr_RS.UTF-8@latin', 'sgs_lt': 'sgs_LT.UTF-8', 'sh': 'sr_RS.UTF-8@latin', 'sh_ba.iso88592@bosnia': 'sr_CS.ISO8859-2', 'sh_hr': 'sh_HR.ISO8859-2', 'sh_hr.iso88592': 'hr_HR.ISO8859-2', 'sh_sp': 'sr_CS.ISO8859-2', 'sh_yu': 'sr_RS.UTF-8@latin', 'shn_mm': 'shn_MM.UTF-8', 'shs_ca': 'shs_CA.UTF-8', 'si': 'si_LK.UTF-8', 'si_lk': 'si_LK.UTF-8', 'sid_et': 'sid_ET.UTF-8', 'sinhala': 'si_LK.UTF-8', 'sk': 'sk_SK.ISO8859-2', 'sk_sk': 'sk_SK.ISO8859-2', 'sl': 'sl_SI.ISO8859-2', 'sl_cs': 'sl_CS.ISO8859-2', 'sl_si': 'sl_SI.ISO8859-2', 'slovak': 'sk_SK.ISO8859-2', 'slovene': 'sl_SI.ISO8859-2', 'slovenian': 'sl_SI.ISO8859-2', 'sm_ws': 'sm_WS.UTF-8', 'so_dj': 'so_DJ.ISO8859-1', 'so_et': 'so_ET.UTF-8', 'so_ke': 'so_KE.ISO8859-1', 'so_so': 'so_SO.ISO8859-1', 'sp': 'sr_CS.ISO8859-5', 'sp_yu': 'sr_CS.ISO8859-5', 'spanish': 'es_ES.ISO8859-1', 'spanish_spain': 'es_ES.ISO8859-1', 'sq': 'sq_AL.ISO8859-2', 'sq_al': 'sq_AL.ISO8859-2', 'sq_mk': 'sq_MK.UTF-8', 'sr': 'sr_RS.UTF-8', 'sr@cyrillic': 'sr_RS.UTF-8', 'sr@latn': 'sr_RS.UTF-8@latin', 'sr_cs': 'sr_CS.UTF-8', 'sr_cs.iso88592@latn': 'sr_CS.ISO8859-2', 'sr_cs@latn': 'sr_CS.UTF-8@latin', 'sr_me': 'sr_ME.UTF-8', 'sr_rs': 'sr_RS.UTF-8', 'sr_rs@latn': 'sr_RS.UTF-8@latin', 'sr_sp': 'sr_CS.ISO8859-2', 'sr_yu': 'sr_RS.UTF-8@latin', 'sr_yu.cp1251@cyrillic': 'sr_CS.CP1251', 'sr_yu.iso88592': 'sr_CS.ISO8859-2', 'sr_yu.iso88595': 'sr_CS.ISO8859-5', 'sr_yu.iso88595@cyrillic': 'sr_CS.ISO8859-5', 'sr_yu.microsoftcp1251@cyrillic': 'sr_CS.CP1251', 'sr_yu.utf8': 'sr_RS.UTF-8', 'sr_yu.utf8@cyrillic': 'sr_RS.UTF-8', 'sr_yu@cyrillic': 'sr_RS.UTF-8', 'ss': 'ss_ZA.ISO8859-1', 'ss_za': 'ss_ZA.ISO8859-1', 'ssy_er': 'ssy_ER.UTF-8', 'st': 'st_ZA.ISO8859-1', 'st_za': 'st_ZA.ISO8859-1', 'su_id': 'su_ID.UTF-8', 'sv': 'sv_SE.ISO8859-1', 'sv_fi': 'sv_FI.ISO8859-1', 'sv_se': 'sv_SE.ISO8859-1', 'sw_ke': 'sw_KE.UTF-8', 'sw_tz': 'sw_TZ.UTF-8', 'swedish': 'sv_SE.ISO8859-1', 'syr': 'syr.UTF-8', 'szl_pl': 'szl_PL.UTF-8', 'ta': 'ta_IN.TSCII-0', 'ta_in': 'ta_IN.TSCII-0', 'ta_in.tscii': 'ta_IN.TSCII-0', 'ta_in.tscii0': 'ta_IN.TSCII-0', 'ta_lk': 'ta_LK.UTF-8', 'tcy_in.utf8': 'tcy_IN.UTF-8', 'te': 'te_IN.UTF-8', 'te_in': 'te_IN.UTF-8', 'tg': 'tg_TJ.KOI8-C', 'tg_tj': 'tg_TJ.KOI8-C', 'th': 'th_TH.ISO8859-11', 'th_th': 'th_TH.ISO8859-11', 'th_th.tactis': 'th_TH.TIS620', 'th_th.tis620': 'th_TH.TIS620', 'thai': 'th_TH.ISO8859-11', 'the_np': 'the_NP.UTF-8', 'ti_er': 'ti_ER.UTF-8', 'ti_et': 'ti_ET.UTF-8', 'tig_er': 'tig_ER.UTF-8', 'tk_tm': 'tk_TM.UTF-8', 'tl': 'tl_PH.ISO8859-1', 'tl_ph': 'tl_PH.ISO8859-1', 'tn': 'tn_ZA.ISO8859-15', 'tn_za': 'tn_ZA.ISO8859-15', 'to_to': 'to_TO.UTF-8', 'tok': 'tok.UTF-8', 'tpi_pg': 'tpi_PG.UTF-8', 'tr': 'tr_TR.ISO8859-9', 'tr_cy': 'tr_CY.ISO8859-9', 'tr_tr': 'tr_TR.ISO8859-9', 'ts': 'ts_ZA.ISO8859-1', 'ts_za': 'ts_ZA.ISO8859-1', 'tt': 'tt_RU.TATAR-CYR', 'tt_ru': 'tt_RU.TATAR-CYR', 'tt_ru.tatarcyr': 'tt_RU.TATAR-CYR', 'tt_ru@iqtelif': 'tt_RU.UTF-8@iqtelif', 'turkish': 'tr_TR.ISO8859-9', 'ug_cn': 'ug_CN.UTF-8', 'uk': 'uk_UA.KOI8-U', 'uk_ua': 'uk_UA.KOI8-U', 'univ.utf8': 'en_US.UTF-8', 'universal.utf8@ucs4': 'en_US.UTF-8', 'unm_us': 'unm_US.UTF-8', 'ur': 'ur_PK.CP1256', 'ur_in': 'ur_IN.UTF-8', 'ur_pk': 'ur_PK.CP1256', 'uz': 'uz_UZ.UTF-8', 'uz_uz': 'uz_UZ.UTF-8', 'uz_uz@cyrillic': 'uz_UZ.UTF-8', 've': 've_ZA.UTF-8', 've_za': 've_ZA.UTF-8', 'vi': 'vi_VN.TCVN', 'vi_vn': 'vi_VN.TCVN', 'vi_vn.tcvn': 'vi_VN.TCVN', 'vi_vn.tcvn5712': 'vi_VN.TCVN', 'vi_vn.viscii': 'vi_VN.VISCII', 'vi_vn.viscii111': 'vi_VN.VISCII', 'wa': 'wa_BE.ISO8859-1', 'wa_be': 'wa_BE.ISO8859-1', 'wae_ch': 'wae_CH.UTF-8', 'wal_et': 'wal_ET.UTF-8', 'wo_sn': 'wo_SN.UTF-8', 'xh': 'xh_ZA.ISO8859-1', 'xh_za': 'xh_ZA.ISO8859-1', 'yi': 'yi_US.CP1255', 'yi_us': 'yi_US.CP1255', 'yo_ng': 'yo_NG.UTF-8', 'yue_hk': 'yue_HK.UTF-8', 'yuw_pg': 'yuw_PG.UTF-8', 'zgh_ma': 'zgh_MA.UTF-8', 'zh': 'zh_CN.eucCN', 'zh_cn': 'zh_CN.gb2312', 'zh_cn.big5': 'zh_TW.big5', 'zh_cn.euc': 'zh_CN.eucCN', 'zh_hk': 'zh_HK.big5hkscs', 'zh_hk.big5hk': 'zh_HK.big5hkscs', 'zh_sg': 'zh_SG.GB2312', 'zh_sg.gbk': 'zh_SG.GBK', 'zh_tw': 'zh_TW.big5', 'zh_tw.euc': 'zh_TW.eucTW', 'zh_tw.euctw': 'zh_TW.eucTW', 'zu': 'zu_ZA.ISO8859-1', 'zu_za': 'zu_ZA.ISO8859-1'}
Windows区域 = {54: 'af', 1078: 'af_ZA', 28: 'sq', 1052: 'sq_AL', 132: 'gsw', 1156: 'gsw_FR', 94: 'am', 1118: 'am_ET', 1: 'ar', 1025: 'ar_SA', 2049: 'ar_IQ', 3073: 'ar_EG', 4097: 'ar_LY', 5121: 'ar_DZ', 6145: 'ar_MA', 7169: 'ar_TN', 8193: 'ar_OM', 9217: 'ar_YE', 10241: 'ar_SY', 11265: 'ar_JO', 12289: 'ar_LB', 13313: 'ar_KW', 14337: 'ar_AE', 15361: 'ar_BH', 16385: 'ar_QA', 43: 'hy', 1067: 'hy_AM', 77: 'as', 1101: 'as_IN', 44: 'az', 29740: 'az', 30764: 'az', 1068: 'az_AZ', 69: 'bn', 1093: 'bn_IN', 2117: 'bn_BD', 109: 'ba', 1133: 'ba_RU', 45: 'eu', 1069: 'eu_ES', 35: 'be', 1059: 'be_BY', 25626: 'bs', 26650: 'bs', 5146: 'bs_BA', 8218: 'bs_BA', 30746: 'bs', 126: 'br', 1150: 'br_FR', 2: 'bg', 1026: 'bg_BG', 85: 'my', 1109: 'my_MM', 3: 'ca', 1027: 'ca_ES', 2051: 'ca_ES', 146: 'ku', 31890: 'ku', 1170: 'ku_IQ', 92: 'chr', 31836: 'chr', 1116: 'chr_US', 4: 'zh', 30724: 'zh', 31748: 'zh', 1028: 'zh_TW', 2052: 'zh_CN', 3076: 'zh_HK', 4100: 'zh_SG', 5124: 'zh_MO', 131: 'co', 1155: 'co_FR', 26: 'hr', 1050: 'hr_HR', 4122: 'hr_BA', 5: 'cs', 1029: 'cs_CZ', 6: 'da', 1030: 'da_DK', 140: 'prs', 1164: 'prs_AF', 101: 'dv', 1125: 'dv_MV', 19: 'nl', 1043: 'nl_NL', 2067: 'nl_BE', 3153: 'dz_BT', 9: 'en', 1033: 'en_US', 2057: 'en_GB', 3081: 'en_AU', 4105: 'en_CA', 5129: 'en_NZ', 6153: 'en_IE', 7177: 'en_ZA', 8201: 'en_JM', 10249: 'en_BZ', 11273: 'en_TT', 12297: 'en_ZW', 13321: 'en_PH', 15369: 'en_HK', 16393: 'en_IN', 17417: 'en_MY', 18441: 'en_SG', 19465: 'en_AE', 37: 'et', 1061: 'et_EE', 56: 'fo', 1080: 'fo_FO', 100: 'fil', 1124: 'fil_PH', 11: 'fi', 1035: 'fi_FI', 12: 'fr', 1036: 'fr_FR', 2060: 'fr_BE', 3084: 'fr_CA', 4108: 'fr_CH', 5132: 'fr_LU', 6156: 'fr_MC', 7180: 'fr_029', 8204: 'fr_RE', 9228: 'fr_CD', 10252: 'fr_SN', 11276: 'fr_CM', 12300: 'fr_CI', 13324: 'fr_ML', 14348: 'fr_MA', 15372: 'fr_HT', 98: 'fy', 1122: 'fy_NL', 103: 'ff', 31847: 'ff', 1127: 'ff_NG', 2151: 'ff_SN', 86: 'gl', 1110: 'gl_ES', 55: 'ka', 1079: 'ka_GE', 7: 'de', 1031: 'de_DE', 2055: 'de_CH', 3079: 'de_AT', 4103: 'de_LU', 5127: 'de_LI', 8: 'el', 1032: 'el_GR', 111: 'kl', 1135: 'kl_GL', 116: 'gn', 1140: 'gn_PY', 71: 'gu', 1095: 'gu_IN', 104: 'ha', 31848: 'ha', 1128: 'ha_NG', 117: 'haw', 1141: 'haw_US', 13: 'he', 1037: 'he_IL', 57: 'hi', 1081: 'hi_IN', 14: 'hu', 1038: 'hu_HU', 15: 'is', 1039: 'is_IS', 112: 'ig', 1136: 'ig_NG', 33: 'id', 1057: 'id_ID', 93: 'iu', 30813: 'iu', 31837: 'iu', 1117: 'iu_CA', 2141: 'iu_CA', 60: 'ga', 2108: 'ga_IE', 16: 'it', 1040: 'it_IT', 2064: 'it_CH', 17: 'ja', 1041: 'ja_JP', 75: 'kn', 1099: 'kn_IN', 1137: 'kr_NG', 96: 'ks', 1120: 'ks', 2144: 'ks_IN', 63: 'kk', 1087: 'kk_KZ', 83: 'km', 1107: 'km_KH', 135: 'rw', 1159: 'rw_RW', 65: 'sw', 1089: 'sw_KE', 87: 'kok', 1111: 'kok_IN', 18: 'ko', 1042: 'ko_KR', 64: 'ky', 1088: 'ky_KG', 84: 'lo', 1108: 'lo_LA', 1142: 'la_VA', 38: 'lv', 1062: 'lv_LV', 39: 'lt', 1063: 'lt_LT', 31790: 'dsb', 2094: 'dsb_DE', 110: 'lb', 1134: 'lb_LU', 47: 'mk', 1071: 'mk_MK', 62: 'ms', 1086: 'ms_MY', 2110: 'ms_BN', 76: 'ml', 1100: 'ml_IN', 58: 'mt', 1082: 'mt_MT', 129: 'mi', 1153: 'mi_NZ', 122: 'arn', 1146: 'arn_CL', 78: 'mr', 1102: 'mr_IN', 124: 'moh', 1148: 'moh_CA', 80: 'mn', 30800: 'mn', 31824: 'mn', 1104: 'mn_MN', 3152: 'mn_MN', 97: 'ne', 1121: 'ne_NP', 2145: 'ne_IN', 20: 'no', 1044: 'nb_NO', 2068: 'nn_NO', 30740: 'nn', 31764: 'nb', 130: 'oc', 1154: 'oc_FR', 72: 'or', 1096: 'or_IN', 114: 'om', 1138: 'om_ET', 99: 'ps', 1123: 'ps_AF', 41: 'fa', 1065: 'fa_IR', 21: 'pl', 1045: 'pl_PL', 22: 'pt', 1046: 'pt_BR', 2070: 'pt_PT', 70: 'pa', 31814: 'pa', 1094: 'pa_IN', 2118: 'pa_PK', 107: 'quz', 1131: 'quz_BO', 2155: 'quz_EC', 3179: 'quz_PE', 24: 'ro', 1048: 'ro_RO', 2072: 'ro_MD', 23: 'rm', 1047: 'rm_CH', 25: 'ru', 1049: 'ru_RU', 2073: 'ru_MD', 133: 'sah', 1157: 'sah_RU', 59: 'se', 1083: 'se_NO', 2107: 'se_SE', 3131: 'se_FI', 31803: 'smj', 4155: 'smj_NO', 5179: 'smj_SE', 30779: 'sma', 6203: 'sma_NO', 7227: 'sma_SE', 29755: 'sms', 8251: 'sms_FI', 28731: 'smn', 9275: 'smn_FI', 79: 'sa', 1103: 'sa_IN', 145: 'gd', 1169: 'gd_GB', 27674: 'sr', 28698: 'sr', 31770: 'sr', 2074: 'sr_CS', 3098: 'sr_CS', 6170: 'sr_BA', 7194: 'sr_BA', 9242: 'sr_RS', 10266: 'sr_RS', 11290: 'sr_ME', 12314: 'sr_ME', 108: 'nso', 1132: 'nso_ZA', 50: 'tn', 1074: 'tn_ZA', 2098: 'tn_BW', 89: 'sd', 31833: 'sd', 2137: 'sd_PK', 91: 'si', 1115: 'si_LK', 27: 'sk', 1051: 'sk_SK', 36: 'sl', 1060: 'sl_SI', 1143: 'so_SO', 48: 'st', 1072: 'st_ZA', 10: 'es', 1034: 'es_ES', 2058: 'es_MX', 3082: 'es_ES', 4106: 'es_GT', 5130: 'es_CR', 6154: 'es_PA', 7178: 'es_DO', 8202: 'es_VE', 9226: 'es_CO', 10250: 'es_PE', 11274: 'es_AR', 12298: 'es_EC', 13322: 'es_CL', 14346: 'es_UY', 15370: 'es_PY', 16394: 'es_BO', 17418: 'es_SV', 18442: 'es_HN', 19466: 'es_NI', 20490: 'es_PR', 21514: 'es_US', 23562: 'es_CU', 29: 'sv', 1053: 'sv_SE', 2077: 'sv_FI', 90: 'syr', 1114: 'syr_SY', 40: 'tg', 31784: 'tg', 1064: 'tg_TJ', 95: 'tzm', 30815: 'tzm', 31839: 'tzm', 2143: 'tzm_DZ', 1119: 'tzm_MA', 4191: 'tzm_MA', 73: 'ta', 1097: 'ta_IN', 2121: 'ta_LK', 68: 'tt', 1092: 'tt_RU', 74: 'te', 1098: 'te_IN', 30: 'th', 1054: 'th_TH', 81: 'bo', 1105: 'bo_CN', 115: 'ti', 1139: 'ti_ET', 2163: 'ti_ER', 49: 'ts', 1073: 'ts_ZA', 31: 'tr', 1055: 'tr_TR', 66: 'tk', 1090: 'tk_TM', 34: 'uk', 1058: 'uk_UA', 46: 'hsb', 1070: 'hsb_DE', 32: 'ur', 1056: 'ur_PK', 2080: 'ur_IN', 128: 'ug', 1152: 'ug_CN', 67: 'uz', 30787: 'uz', 31811: 'uz', 1091: 'uz_UZ', 51: 've', 1075: 've_ZA', 42: 'vi', 1066: 'vi_VN', 82: 'cy', 1106: 'cy_GB', 136: 'wo', 1160: 'wo_SN', 52: 'xh', 1076: 'xh_ZA', 120: 'ii', 1144: 'ii_CN', 1085: 'yi_001', 106: 'yo', 1130: 'yo_NG', 53: 'zu', 1077: 'zu_ZA', 134: 'qut', 66567: 'de_DE', 66574: 'hu_HU', 66615: 'ka_GE', 133124: 'zh_CN', 135172: 'zh_SG', 136196: 'zh_MO', 197636: 'zh_TW', 263172: 'zh_TW', 263185: 'ja_JP', 265220: 'zh_HK', 267268: 'zh_MO', 329732: 'zh_CN', 331780: 'zh_SG'}

def _print_locale():
    """ Test function.
    """
    categories = {}

    def _init_categories(categories=categories):
        for k, v in globals().items():
            if k[:3] == 'LC_':
                categories[k] = v
    _init_categories()
    del categories['LC_ALL']
    print('Locale defaults as determined by getdefaultlocale():')
    print('-' * 72)
    lang, enc = 取默认区域()
    print('Language: ', lang or '(undefined)')
    print('Encoding: ', enc or '(undefined)')
    print()
    print('Locale settings on startup:')
    print('-' * 72)
    for name, category in categories.items():
        print(name, '...')
        lang, enc = 取区域(category)
        print('   Language: ', lang or '(undefined)')
        print('   Encoding: ', enc or '(undefined)')
        print()
    try:
        setlocale(LC_ALL, '')
    except:
        print('NOTE:')
        print('setlocale(LC_ALL, "") does not support the default locale')
        print('given in the OS environment variables.')
    else:
        print()
        print('Locale settings after calling setlocale(LC_ALL, ""):')
        print('-' * 72)
        for name, category in categories.items():
            print(name, '...')
            lang, enc = 取区域(category)
            print('   Language: ', lang or '(undefined)')
            print('   Encoding: ', enc or '(undefined)')
            print()
try:
    LC_MESSAGES
except NameError:
    pass
else:
    __all__.append('LC_MESSAGES')
if __name__ == '__main__':
    print('Locale aliasing:')
    print()
    _print_locale()
    print()
    print('Number formatting:')
    print()
    _test()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'atof': '转浮点',
    'atoi': '转整数',
    'currency': '货币',
    'delocalize': '去本地化',
    'format_string': '格式化字符串',
    'getdefaultlocale': '取默认区域',
    'getlocale': '取区域',
    'getpreferredencoding': '取首选编码',
    'locale_alias': '区域别名',
    'locale_encoding_alias': '区域编码别名',
    'localize': '本地化',
    'normalize': '规范化',
    'windows_locale': 'Windows区域',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '取区域',
    '取首选编码',
    '取默认区域',
    '格式化字符串',
    '规范化',
    '货币',
    '转整数',
    '转浮点',
]

# ---- 转发层结束 ----
