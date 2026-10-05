# -*- coding: utf-8 -*-
"""日历 —— 汉语库（由 tools/汉化库.py 从 Lib/calendar.py 机械生成，**不要手改**）。

英文库 Lib/calendar.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 日历
"""


"""Calendar printing functions

Note when comparing these calendars to the ones printed by cal(1): By
default, these calendars have Monday as the first day of the week, and
Sunday as the last (the European convention). Use setfirstweekday() to
set the first day of the week (0=Monday, 6=Sunday)."""
_实例属性全表 = {}
_反表 = {}

def _装类转发(_类, _对, _属性=None):
    if getattr(_类, '__module__', None) != __name__:
        return
    for _英, _中 in _对.items():
        if _中 in _类.__dict__:
            setattr(_类, _英, _类.__dict__[_中])
    if _属性:
        _实例属性全表.update(_属性)
        _反表.update({_中: _英 for _英, _中 in _属性.items()})
        for _英, _中 in _属性.items():
            if _英 not in _类.__dict__ and _中 in _类.__dict__:
                setattr(_类, _英, _类.__dict__[_中])
        if '__getattr__' not in _类.__dict__:

            def _取(self, _名, _对=_实例属性全表, _反=_反表):
                if _名 in _对:
                    try:
                        return object.__getattribute__(self, _对[_名])
                    except AttributeError:
                        pass
                    try:
                        return object.__getattribute__(self, _名)
                    except AttributeError:
                        pass
                if _名 in _反:
                    try:
                        return object.__getattribute__(self, _反[_名])
                    except AttributeError:
                        pass
                raise AttributeError(_名)
            try:
                _类.__getattr__ = _取
            except TypeError:
                return
        if not [_基 for _基 in _类.__mro__ if _基 is not object and '__setattr__' in _基.__dict__ and (not getattr(_基.__dict__['__setattr__'], '_中文转发钩子', False))]:

            def _设(self, _名, _值, _对=_实例属性全表, _反=_反表):
                _英 = _名 if _名 in _对 else _反.get(_名)
                if _英 is None:
                    object.__setattr__(self, _名, _值)
                    return
                _中 = _对[_英]
                _成 = False
                for _名2 in (_中, _英):
                    try:
                        object.__setattr__(self, _名2, _值)
                        _成 = True
                    except AttributeError:
                        pass
                if not _成:
                    raise AttributeError(_名)
            _设._中文转发钩子 = True
            try:
                _类.__setattr__ = _设
            except TypeError:
                return
import sys
import datetime
from enum import IntEnum, global_enum
import locale as _locale
from itertools import repeat
__all__ = ['IllegalMonthError', 'IllegalWeekdayError', 'setfirstweekday', 'firstweekday', 'isleap', 'leapdays', 'weekday', 'monthrange', 'monthcalendar', 'prmonth', 'month', 'prcal', 'calendar', 'timegm', 'month_name', 'month_abbr', 'day_name', 'day_abbr', 'Calendar', 'TextCalendar', 'HTMLCalendar', 'LocaleTextCalendar', 'LocaleHTMLCalendar', 'weekheader', 'Day', 'Month', 'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
错误 = ValueError

class 非法月份错误(ValueError, IndexError):

    def __init__(self, month):
        self.月份 = month

    def __str__(self):
        return 'bad month number %r; must be 1-12' % self.月份
_装类转发(非法月份错误, {}, {'month': '月份'})

class 非法星期错误(ValueError):

    def __init__(self, weekday):
        self.星期几 = weekday

    def __str__(self):
        return 'bad weekday number %r; must be 0 (Monday) to 6 (Sunday)' % self.星期几
_装类转发(非法星期错误, {}, {'weekday': '星期几'})

def __getattr__(name):
    if name in ('January', 'February'):
        import warnings
        warnings.warn(f"The '{name}' attribute is deprecated, use '{name.upper()}' instead", DeprecationWarning, stacklevel=2)
        if name == 'January':
            return 1
        else:
            return 2
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

@global_enum
class 月份枚举(IntEnum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

@global_enum
class 星期枚举(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6
月天数表 = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

class _localized_month:
    _months = [datetime.date(2001, i + 1, 1).strftime for i in range(12)]
    _months.insert(0, lambda x: '')

    def __init__(self, format):
        self.format = format

    def __getitem__(self, i):
        funcs = self._months[i]
        if isinstance(i, slice):
            return [f(self.format) for f in funcs]
        else:
            return funcs(self.format)

    def __len__(self):
        return 13

class _localized_day:
    _days = [datetime.date(2001, 1, i + 1).strftime for i in range(7)]

    def __init__(self, format):
        self.format = format

    def __getitem__(self, i):
        funcs = self._days[i]
        if isinstance(i, slice):
            return [f(self.format) for f in funcs]
        else:
            return funcs(self.format)

    def __len__(self):
        return 7
星期名 = _localized_day('%A')
星期简称 = _localized_day('%a')
月份名 = _localized_month('%B')
月份简称 = _localized_month('%b')

def 是闰年(year):
    """Return True for leap years, False for non-leap years."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def 闰年天数(y1, y2):
    """Return number of leap years in range [y1, y2).
       Assume y1 <= y2."""
    y1 -= 1
    y2 -= 1
    return y2 // 4 - y1 // 4 - (y2 // 100 - y1 // 100) + (y2 // 400 - y1 // 400)

def 星期几(year, month, day):
    """Return weekday (0-6 ~ Mon-Sun) for year, month (1-12), day (1-31)."""
    if not datetime.MINYEAR <= year <= datetime.MAXYEAR:
        year = 2000 + year % 400
    return 星期枚举(datetime.date(year, month, day).weekday())

def _validate_month(month):
    if not 1 <= month <= 12:
        raise 非法月份错误(month)

def 月范围(year, month):
    """Return weekday of first day of month (0-6 ~ Mon-Sun)
       and number of days (28-31) for year, month."""
    _validate_month(month)
    day1 = 星期几(year, month, 1)
    ndays = 月天数表[month] + (month == FEBRUARY and 是闰年(year))
    return (day1, ndays)

def _monthlen(year, month):
    return 月天数表[month] + (month == FEBRUARY and 是闰年(year))

def _prevmonth(year, month):
    if month == 1:
        return (year - 1, 12)
    else:
        return (year, month - 1)

def _nextmonth(year, month):
    if month == 12:
        return (year + 1, 1)
    else:
        return (year, month + 1)

class 日历器(object):
    """
    Base calendar class. This class doesn't do any formatting. It simply
    provides data to subclasses.
    """

    def __init__(self, firstweekday=0):
        self.firstweekday = firstweekday

    def 取每周第一天(self):
        return self._firstweekday % 7

    def 设每周第一天(self, firstweekday):
        self._firstweekday = firstweekday
    firstweekday = property(取每周第一天, 设每周第一天)

    def 迭代星期(self):
        """
        Return an iterator for one week of weekday numbers starting with the
        configured first one.
        """
        for i in range(self.firstweekday, self.firstweekday + 7):
            yield (i % 7)

    def 迭代月日期(self, year, month):
        """
        Return an iterator for one month. The iterator will yield datetime.date
        values and will always iterate through complete weeks, so it will yield
        dates outside the specified month.
        """
        for y, m, d in self.迭代月天数三(year, month):
            yield datetime.date(y, m, d)

    def 迭代月天数(self, year, month):
        """
        Like itermonthdates(), but will yield day numbers. For days outside
        the specified month the day number is 0.
        """
        day1, ndays = 月范围(year, month)
        days_before = (day1 - self.firstweekday) % 7
        yield from repeat(0, days_before)
        yield from range(1, ndays + 1)
        days_after = (self.firstweekday - day1 - ndays) % 7
        yield from repeat(0, days_after)

    def 迭代月天数对(self, year, month):
        """
        Like itermonthdates(), but will yield (day number, weekday number)
        tuples. For days outside the specified month the day number is 0.
        """
        for i, d in enumerate(self.迭代月天数(year, month), self.firstweekday):
            yield (d, i % 7)

    def 迭代月天数三(self, year, month):
        """
        Like itermonthdates(), but will yield (year, month, day) tuples.  Can be
        used for dates outside of datetime.date range.
        """
        day1, ndays = 月范围(year, month)
        days_before = (day1 - self.firstweekday) % 7
        days_after = (self.firstweekday - day1 - ndays) % 7
        y, m = _prevmonth(year, month)
        end = _monthlen(y, m) + 1
        for d in range(end - days_before, end):
            yield (y, m, d)
        for d in range(1, ndays + 1):
            yield (year, month, d)
        y, m = _nextmonth(year, month)
        for d in range(1, days_after + 1):
            yield (y, m, d)

    def 迭代月天数四(self, year, month):
        """
        Like itermonthdates(), but will yield (year, month, day, day_of_week) tuples.
        Can be used for dates outside of datetime.date range.
        """
        for i, (y, m, d) in enumerate(self.迭代月天数三(year, month)):
            yield (y, m, d, (self.firstweekday + i) % 7)

    def 月日期表(self, year, month):
        """
        Return a matrix (list of lists) representing a month's calendar.
        Each row represents a week; week entries are datetime.date values.
        """
        dates = list(self.迭代月日期(year, month))
        return [dates[i:i + 7] for i in range(0, len(dates), 7)]

    def 月天数对表(self, year, month):
        """
        Return a matrix representing a month's calendar.
        Each row represents a week; week entries are
        (day number, weekday number) tuples. Day numbers outside this month
        are zero.
        """
        days = list(self.迭代月天数对(year, month))
        return [days[i:i + 7] for i in range(0, len(days), 7)]

    def 月天数列表(self, year, month):
        """
        Return a matrix representing a month's calendar.
        Each row represents a week; days outside this month are zero.
        """
        days = list(self.迭代月天数(year, month))
        return [days[i:i + 7] for i in range(0, len(days), 7)]

    def 年日期表(self, year, width=3):
        """
        Return the data for the specified year ready for formatting. The return
        value is a list of month rows. Each month row contains up to width months.
        Each month contains between 4 and 6 weeks and each week contains 1-7
        days. Days are datetime.date objects.
        """
        months = [self.月日期表(year, m) for m in 月份枚举]
        return [months[i:i + width] for i in range(0, len(months), width)]

    def 年天数对表(self, year, width=3):
        """
        Return the data for the specified year ready for formatting (similar to
        yeardatescalendar()). Entries in the week lists are
        (day number, weekday number) tuples. Day numbers outside this month are
        zero.
        """
        months = [self.月天数对表(year, m) for m in 月份枚举]
        return [months[i:i + width] for i in range(0, len(months), width)]

    def 年天数表(self, year, width=3):
        """
        Return the data for the specified year ready for formatting (similar to
        yeardatescalendar()). Entries in the week lists are day numbers.
        Day numbers outside this month are zero.
        """
        months = [self.月天数列表(year, m) for m in 月份枚举]
        return [months[i:i + width] for i in range(0, len(months), width)]
_装类转发(日历器, {'getfirstweekday': '取每周第一天', 'itermonthdates': '迭代月日期', 'itermonthdays': '迭代月天数', 'itermonthdays2': '迭代月天数对', 'itermonthdays3': '迭代月天数三', 'itermonthdays4': '迭代月天数四', 'iterweekdays': '迭代星期', 'monthdatescalendar': '月日期表', 'monthdays2calendar': '月天数对表', 'monthdayscalendar': '月天数列表', 'setfirstweekday': '设每周第一天', 'yeardatescalendar': '年日期表', 'yeardays2calendar': '年天数对表', 'yeardayscalendar': '年天数表'}, {'getfirstweekday': '取每周第一天', 'itermonthdates': '迭代月日期', 'itermonthdays': '迭代月天数', 'itermonthdays2': '迭代月天数对', 'itermonthdays3': '迭代月天数三', 'itermonthdays4': '迭代月天数四', 'iterweekdays': '迭代星期', 'monthdatescalendar': '月日期表', 'monthdays2calendar': '月天数对表', 'monthdayscalendar': '月天数列表', 'setfirstweekday': '设每周第一天', 'yeardatescalendar': '年日期表', 'yeardays2calendar': '年天数对表', 'yeardayscalendar': '年天数表'})

class 文本日历(日历器):
    """
    Subclass of Calendar that outputs a calendar as a simple plain text
    similar to the UNIX program cal.
    """

    def 打印周(self, theweek, width):
        """
        Print a single week (no newline).
        """
        print(self.格式化周(theweek, width), end='')

    def 格式化日(self, day, weekday, width):
        """
        Returns a formatted day.
        """
        if day == 0:
            s = ''
        else:
            s = '%2i' % day
        return s.center(width)

    def 格式化周(self, theweek, width):
        """
        Returns a single week in a string (no newline).
        """
        return ' '.join((self.格式化日(d, wd, width) for d, wd in theweek))

    def 格式化星期名(self, day, width):
        """
        Returns a formatted week day name.
        """
        if width >= 9:
            names = 星期名
        else:
            names = 星期简称
        return names[day][:width].center(width)

    def 格式化星期表头(self, width):
        """
        Return a header for a week.
        """
        return ' '.join((self.格式化星期名(i, width) for i in self.迭代星期()))

    def 格式化月名(self, theyear, themonth, width, withyear=True):
        """
        Return a formatted month name.
        """
        _validate_month(themonth)
        s = 月份名[themonth]
        if withyear:
            s = '%s %r' % (s, theyear)
        return s.center(width)

    def 打印月(self, theyear, themonth, w=0, l=0):
        """
        Print a month's calendar.
        """
        print(self.格式化月(theyear, themonth, w, l), end='')

    def 格式化月(self, theyear, themonth, w=0, l=0):
        """
        Return a month's calendar string (multi-line).
        """
        w = max(2, w)
        l = max(1, l)
        s = self.格式化月名(theyear, themonth, 7 * (w + 1) - 1)
        s = s.rstrip()
        s += '\n' * l
        s += self.格式化星期表头(w).rstrip()
        s += '\n' * l
        for 周 in self.月天数对表(theyear, themonth):
            s += self.格式化周(周, w).rstrip()
            s += '\n' * l
        return s

    def 格式化年(self, theyear, w=2, l=1, c=6, m=3):
        """
        Returns a year's calendar as a multi-line string.
        """
        w = max(2, w)
        l = max(1, l)
        c = max(2, c)
        colwidth = (w + 1) * 7 - 1
        v = []
        a = v.append
        a(repr(theyear).center(colwidth * m + c * (m - 1)).rstrip())
        a('\n' * l)
        header = self.格式化星期表头(w)
        for i, row in enumerate(self.年天数对表(theyear, m)):
            months = range(m * i + 1, min(m * (i + 1) + 1, 13))
            a('\n' * l)
            names = (self.格式化月名(theyear, k, colwidth, False) for k in months)
            a(格式字符串(names, colwidth, c).rstrip())
            a('\n' * l)
            headers = (header for k in months)
            a(格式字符串(headers, colwidth, c).rstrip())
            a('\n' * l)
            height = max((len(cal) for cal in row))
            for j in range(height):
                weeks = []
                for cal in row:
                    if j >= len(cal):
                        weeks.append('')
                    else:
                        weeks.append(self.格式化周(cal[j], w))
                a(格式字符串(weeks, colwidth, c).rstrip())
                a('\n' * l)
        return ''.join(v)

    def 打印年(self, theyear, w=0, l=0, c=6, m=3):
        """Print a year's calendar."""
        print(self.格式化年(theyear, w, l, c, m), end='')
_装类转发(文本日历, {'formatday': '格式化日', 'formatmonth': '格式化月', 'formatmonthname': '格式化月名', 'formatweek': '格式化周', 'formatweekday': '格式化星期名', 'formatweekheader': '格式化星期表头', 'formatyear': '格式化年', 'prmonth': '打印月', 'prweek': '打印周', 'pryear': '打印年'}, {'formatday': '格式化日', 'formatmonth': '格式化月', 'formatmonthname': '格式化月名', 'formatweek': '格式化周', 'formatweekday': '格式化星期名', 'formatweekheader': '格式化星期表头', 'formatyear': '格式化年', 'iterweekdays': '迭代星期', 'monthdays2calendar': '月天数对表', 'prmonth': '打印月', 'prweek': '打印周', 'pryear': '打印年', 'yeardays2calendar': '年天数对表'})

class HTML日历(日历器):
    """
    This calendar returns complete HTML pages.
    """
    cssclasses = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    cssclasses_weekday_head = cssclasses
    cssclass_noday = 'noday'
    cssclass_month_head = 'month'
    cssclass_month = 'month'
    cssclass_year_head = 'year'
    cssclass_year = 'year'

    def 格式化日(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            return '<td class="%s">%d</td>' % (self.cssclasses[weekday], day)

    def 格式化周(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join((self.格式化日(d, wd) for d, wd in theweek))
        return '<tr>%s</tr>' % s

    def 格式化星期名(self, day):
        """
        Return a weekday name as a table header.
        """
        return '<th class="%s">%s</th>' % (self.cssclasses_weekday_head[day], 星期简称[day])

    def 格式化星期表头(self):
        """
        Return a header for a week as a table row.
        """
        s = ''.join((self.格式化星期名(i) for i in self.迭代星期()))
        return '<tr>%s</tr>' % s

    def 格式化月名(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        _validate_month(themonth)
        if withyear:
            s = '%s %s' % (月份名[themonth], theyear)
        else:
            s = '%s' % 月份名[themonth]
        return '<tr><th colspan="7" class="%s">%s</th></tr>' % (self.cssclass_month_head, s)

    def 格式化月(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % self.cssclass_month)
        a('\n')
        a(self.格式化月名(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.格式化星期表头())
        a('\n')
        for 周 in self.月天数对表(theyear, themonth):
            a(self.格式化周(周))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def 格式化年(self, theyear, width=3):
        """
        Return a formatted year as a table of tables.
        """
        v = []
        a = v.append
        width = max(width, 1)
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % self.cssclass_year)
        a('\n')
        a('<tr><th colspan="%d" class="%s">%s</th></tr>' % (width, self.cssclass_year_head, theyear))
        for i in range(JANUARY, JANUARY + 12, width):
            months = range(i, min(i + width, 13))
            a('<tr>')
            for m in months:
                a('<td>')
                a(self.格式化月(theyear, m, withyear=False))
                a('</td>')
            a('</tr>')
        a('</table>')
        return ''.join(v)

    def 格式化年页面(self, theyear, width=3, css='calendar.css', encoding=None):
        """
        Return a formatted year as a complete HTML page.
        """
        if encoding is None:
            encoding = sys.getdefaultencoding()
        v = []
        a = v.append
        a('<?xml version="1.0" encoding="%s"?>\n' % encoding)
        a('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n')
        a('<html>\n')
        a('<head>\n')
        a('<meta http-equiv="Content-Type" content="text/html; charset=%s" />\n' % encoding)
        if css is not None:
            a('<link rel="stylesheet" type="text/css" href="%s" />\n' % css)
        a('<title>Calendar for %d</title>\n' % theyear)
        a('</head>\n')
        a('<body>\n')
        a(self.格式化年(theyear, width))
        a('</body>\n')
        a('</html>\n')
        return ''.join(v).encode(encoding, 'xmlcharrefreplace')
_装类转发(HTML日历, {'formatday': '格式化日', 'formatmonth': '格式化月', 'formatmonthname': '格式化月名', 'formatweek': '格式化周', 'formatweekday': '格式化星期名', 'formatweekheader': '格式化星期表头', 'formatyear': '格式化年', 'formatyearpage': '格式化年页面'}, {'formatday': '格式化日', 'formatmonth': '格式化月', 'formatmonthname': '格式化月名', 'formatweek': '格式化周', 'formatweekday': '格式化星期名', 'formatweekheader': '格式化星期表头', 'formatyear': '格式化年', 'formatyearpage': '格式化年页面', 'iterweekdays': '迭代星期', 'monthdays2calendar': '月天数对表'})

class 换语言环境:

    def __init__(self, locale):
        self.locale = locale
        self.oldlocale = None

    def __enter__(self):
        self.oldlocale = _locale.setlocale(_locale.LC_TIME, None)
        _locale.setlocale(_locale.LC_TIME, self.locale)

    def __exit__(self, *args):
        _locale.setlocale(_locale.LC_TIME, self.oldlocale)

def _get_default_locale():
    locale = _locale.setlocale(_locale.LC_TIME, None)
    if locale == 'C':
        with 换语言环境(''):
            locale = _locale.setlocale(_locale.LC_TIME, None)
    return locale

class 本地文本日历(文本日历):
    """
    This class can be passed a locale name in the constructor and will return
    month and weekday names in the specified locale.
    """

    def __init__(self, firstweekday=0, locale=None):
        文本日历.__init__(self, firstweekday)
        if locale is None:
            locale = _get_default_locale()
        self.locale = locale

    def 格式化星期名(self, day, width):
        with 换语言环境(self.locale):
            return super().formatweekday(day, width)

    def 格式化月名(self, theyear, themonth, width, withyear=True):
        with 换语言环境(self.locale):
            return super().formatmonthname(theyear, themonth, width, withyear)
_装类转发(本地文本日历, {'formatmonthname': '格式化月名', 'formatweekday': '格式化星期名'}, {'formatmonthname': '格式化月名', 'formatweekday': '格式化星期名'})

class 本地HTML日历(HTML日历):
    """
    This class can be passed a locale name in the constructor and will return
    month and weekday names in the specified locale.
    """

    def __init__(self, firstweekday=0, locale=None):
        HTML日历.__init__(self, firstweekday)
        if locale is None:
            locale = _get_default_locale()
        self.locale = locale

    def 格式化星期名(self, day):
        with 换语言环境(self.locale):
            return super().formatweekday(day)

    def 格式化月名(self, theyear, themonth, withyear=True):
        with 换语言环境(self.locale):
            return super().formatmonthname(theyear, themonth, withyear)
_装类转发(本地HTML日历, {'formatmonthname': '格式化月名', 'formatweekday': '格式化星期名'}, {'formatmonthname': '格式化月名', 'formatweekday': '格式化星期名'})

class _CLIDemoCalendar(文本日历):

    def __init__(self, highlight_day=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.highlight_day = highlight_day

    def 格式化周(self, theweek, width, *, highlight_day=None):
        """
        Returns a single week in a string (no newline).
        """
        if highlight_day:
            from _colorize import get_colors
            ansi = get_colors()
            highlight = f'{ansi.BLACK}{ansi.BACKGROUND_YELLOW}'
            reset = ansi.RESET
        else:
            highlight = reset = ''
        return ' '.join((f'{highlight}{self.格式化日(d, wd, width)}{reset}' if d == highlight_day else self.格式化日(d, wd, width) for d, wd in theweek))

    def 格式化月(self, theyear, themonth, w=0, l=0):
        """
        Return a month's calendar string (multi-line).
        """
        if self.highlight_day and self.highlight_day.year == theyear and (self.highlight_day.month == themonth):
            highlight_day = self.highlight_day.day
        else:
            highlight_day = None
        w = max(2, w)
        l = max(1, l)
        s = self.格式化月名(theyear, themonth, 7 * (w + 1) - 1)
        s = s.rstrip()
        s += '\n' * l
        s += self.格式化星期表头(w).rstrip()
        s += '\n' * l
        for 周 in self.月天数对表(theyear, themonth):
            s += self.格式化周(周, w, highlight_day=highlight_day).rstrip()
            s += '\n' * l
        return s

    def 格式化年(self, theyear, w=2, l=1, c=6, m=3):
        """
        Returns a year's calendar as a multi-line string.
        """
        w = max(2, w)
        l = max(1, l)
        c = max(2, c)
        colwidth = (w + 1) * 7 - 1
        v = []
        a = v.append
        a(repr(theyear).center(colwidth * m + c * (m - 1)).rstrip())
        a('\n' * l)
        header = self.格式化星期表头(w)
        for i, row in enumerate(self.年天数对表(theyear, m)):
            months = range(m * i + 1, min(m * (i + 1) + 1, 13))
            a('\n' * l)
            names = (self.格式化月名(theyear, k, colwidth, False) for k in months)
            a(格式字符串(names, colwidth, c).rstrip())
            a('\n' * l)
            headers = (header for k in months)
            a(格式字符串(headers, colwidth, c).rstrip())
            a('\n' * l)
            if self.highlight_day and self.highlight_day.year == theyear and (self.highlight_day.month in months):
                month_pos = months.index(self.highlight_day.month)
            else:
                month_pos = None
            height = max((len(cal) for cal in row))
            for j in range(height):
                weeks = []
                for k, cal in enumerate(row):
                    if j >= len(cal):
                        weeks.append('')
                    else:
                        day = self.highlight_day.day if k == month_pos else None
                        weeks.append(self.格式化周(cal[j], w, highlight_day=day))
                a(格式字符串(weeks, colwidth, c).rstrip())
                a('\n' * l)
        return ''.join(v)
_装类转发(_CLIDemoCalendar, {'formatmonth': '格式化月', 'formatweek': '格式化周', 'formatyear': '格式化年'}, {'formatday': '格式化日', 'formatmonth': '格式化月', 'formatmonthname': '格式化月名', 'formatweek': '格式化周', 'formatweekheader': '格式化星期表头', 'formatyear': '格式化年', 'monthdays2calendar': '月天数对表', 'yeardays2calendar': '年天数对表'})

class _CLIDemoLocaleCalendar(本地文本日历, _CLIDemoCalendar):

    def __init__(self, highlight_day=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.highlight_day = highlight_day
c = 文本日历()
firstweekday = c.getfirstweekday

def 设每周第一天(firstweekday):
    if not MONDAY <= firstweekday <= SUNDAY:
        raise 非法星期错误(firstweekday)
    c.firstweekday = firstweekday
月历 = c.monthdayscalendar
打印周 = c.prweek
周 = c.formatweek
周表头 = c.formatweekheader
打印月 = c.prmonth
月份 = c.formatmonth
年历 = c.formatyear
打印年历 = c.pryear
_colwidth = 7 * 3 - 1
_spacing = 6

def format(cols, colwidth=_colwidth, spacing=_spacing):
    """Prints multi-column formatting for year calendars"""
    print(格式字符串(cols, colwidth, spacing))

def 格式字符串(cols, colwidth=_colwidth, spacing=_spacing):
    """Returns a string formatted from n strings, centered within n columns."""
    spacing *= ' '
    return spacing.join((c.center(colwidth) for c in cols))
纪元 = 1970
_EPOCH_ORD = datetime.date(纪元, 1, 1).toordinal()

def 时间戳(tuple):
    """Unrelated but handy function to calculate Unix timestamp from GMT."""
    year, 月份, day, hour, minute, second = tuple[:6]
    days = datetime.date(year, 月份, 1).toordinal() - _EPOCH_ORD + day - 1
    hours = days * 24 + hour
    minutes = hours * 60 + minute
    seconds = minutes * 60 + second
    return seconds

def 主函数(args=None):
    import argparse
    parser = argparse.ArgumentParser(color=True)
    textgroup = parser.add_argument_group('text only arguments')
    htmlgroup = parser.add_argument_group('html only arguments')
    textgroup.add_argument('-w', '--width', type=int, default=2, help='width of date column (default 2)')
    textgroup.add_argument('-l', '--lines', type=int, default=1, help='number of lines for each week (default 1)')
    textgroup.add_argument('-s', '--spacing', type=int, default=6, help='spacing between months (default 6)')
    textgroup.add_argument('-m', '--months', type=int, default=3, help='months per row (default 3)')
    htmlgroup.add_argument('-c', '--css', default='calendar.css', help='CSS to use for page')
    parser.add_argument('-L', '--locale', default=None, help='locale to use for month and weekday names')
    parser.add_argument('-e', '--encoding', default=None, help='encoding to use for output')
    parser.add_argument('-t', '--type', default='text', choices=('text', 'html'), help='output type (text or html)')
    parser.add_argument('-f', '--first-weekday', type=int, default=0, help='weekday (0 is Monday, 6 is Sunday) to start each week (default 0)')
    parser.add_argument('year', nargs='?', type=int, help='year number')
    parser.add_argument('month', nargs='?', type=int, help='month number (1-12, text only)')
    options = parser.parse_args(args)
    if options.locale and (not options.encoding):
        parser.error('if --locale is specified --encoding is required')
        sys.exit(1)
    locale = (options.locale, options.encoding)
    today = datetime.date.today()
    if options.type == 'html':
        if options.month:
            parser.error('incorrect number of arguments')
            sys.exit(1)
        if options.locale:
            cal = 本地HTML日历(locale=locale)
        else:
            cal = HTML日历()
        cal.setfirstweekday(options.first_weekday)
        encoding = options.encoding
        if encoding is None:
            encoding = sys.getdefaultencoding()
        optdict = dict(encoding=encoding, css=options.css)
        write = sys.stdout.buffer.write
        if options.year is None:
            write(cal.formatyearpage(today.year, **optdict))
        else:
            write(cal.formatyearpage(options.year, **optdict))
    else:
        if options.locale:
            cal = _CLIDemoLocaleCalendar(highlight_day=today, locale=locale)
        else:
            cal = _CLIDemoCalendar(highlight_day=today)
        cal.setfirstweekday(options.first_weekday)
        optdict = dict(w=options.width, l=options.lines)
        if options.month is None:
            optdict['c'] = options.spacing
            optdict['m'] = options.months
        else:
            _validate_month(options.month)
        if options.year is None:
            result = cal.formatyear(today.year, **optdict)
        elif options.month is None:
            result = cal.formatyear(options.year, **optdict)
        else:
            result = cal.formatmonth(options.year, options.month, **optdict)
        write = sys.stdout.write
        if options.encoding:
            result = result.encode(options.encoding)
            write = sys.stdout.buffer.write
        write(result)
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

# 本模块别名：词表里有、但规则不让改定义的名字（内置名最典型，比如 `open`）
_本模块别名 = {
    '格式': 'format',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'Calendar': '日历器',
    'Day': '星期枚举',
    'EPOCH': '纪元',
    'HTMLCalendar': 'HTML日历',
    'IllegalMonthError': '非法月份错误',
    'IllegalWeekdayError': '非法星期错误',
    'LocaleHTMLCalendar': '本地HTML日历',
    'LocaleTextCalendar': '本地文本日历',
    'Month': '月份枚举',
    'TextCalendar': '文本日历',
    'calendar': '年历',
    'day_abbr': '星期简称',
    'day_name': '星期名',
    'different_locale': '换语言环境',
    'error': '错误',
    'formatstring': '格式字符串',
    'isleap': '是闰年',
    'leapdays': '闰年天数',
    'main': '主函数',
    'mdays': '月天数表',
    'month': '月份',
    'month_abbr': '月份简称',
    'month_name': '月份名',
    'monthcalendar': '月历',
    'monthrange': '月范围',
    'prcal': '打印年历',
    'prmonth': '打印月',
    'prweek': '打印周',
    'setfirstweekday': '设每周第一天',
    'timegm': '时间戳',
    'week': '周',
    'weekday': '星期几',
    'weekheader': '周表头',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'HTML日历': {
        'formatday': '格式化日',
        'formatmonth': '格式化月',
        'formatmonthname': '格式化月名',
        'formatweek': '格式化周',
        'formatweekday': '格式化星期名',
        'formatweekheader': '格式化星期表头',
        'formatyear': '格式化年',
        'formatyearpage': '格式化年页面',
    },
    '_CLIDemoCalendar': {
        'formatmonth': '格式化月',
        'formatweek': '格式化周',
        'formatyear': '格式化年',
    },
    '文本日历': {
        'formatday': '格式化日',
        'formatmonth': '格式化月',
        'formatmonthname': '格式化月名',
        'formatweek': '格式化周',
        'formatweekday': '格式化星期名',
        'formatweekheader': '格式化星期表头',
        'formatyear': '格式化年',
        'prmonth': '打印月',
        'prweek': '打印周',
        'pryear': '打印年',
    },
    '日历器': {
        'getfirstweekday': '取每周第一天',
        'itermonthdates': '迭代月日期',
        'itermonthdays': '迭代月天数',
        'itermonthdays2': '迭代月天数对',
        'itermonthdays3': '迭代月天数三',
        'itermonthdays4': '迭代月天数四',
        'iterweekdays': '迭代星期',
        'monthdatescalendar': '月日期表',
        'monthdays2calendar': '月天数对表',
        'monthdayscalendar': '月天数列表',
        'setfirstweekday': '设每周第一天',
        'yeardatescalendar': '年日期表',
        'yeardays2calendar': '年天数对表',
        'yeardayscalendar': '年天数表',
    },
    '本地HTML日历': {
        'formatmonthname': '格式化月名',
        'formatweekday': '格式化星期名',
    },
    '本地文本日历': {
        'formatmonthname': '格式化月名',
        'formatweekday': '格式化星期名',
    },
}
_转发跳过 = []
_无 = object()    # 哨兵：类属性**值就是 None** 时 ≠ 「没找到」（D-126 修的真 bug）
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # ★必须从 __dict__ 拿**描述符本体**，不能用 getattr(类, 名)：
        #   getattr 会把 classmethod/staticmethod/property **绑到本类上**，
        #   再挂成别名之后，**子类**调用拿到的还是绑死在本类的那个 ——
        #   DummyFraction.from_number(...) 会返回基类实例
        #   （fractions 的 testFromNumber_subclass 就是这么挂的，见 D-035）。
        _原 = _类.__dict__.get(_中, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _中 in _基.__dict__:
                    _原 = _基.__dict__[_中]
                    break
        if _原 is _无:
            _转发跳过.append((_类名, _英, _中))
            continue
        setattr(_类, _英, _原)

# 中文成员名的兜底（D-125 起，D-126 推广到全部类）：上面主循环只认「中文名在类里」，
#   找不到就跳过 —— 可中文名**本来就不在类里**有两种情况：① 类名走了身份别名
#   （机制 3），指向英文那个对象；② 改名被规则挡下（那个名字是 import 进来的）。
#   实测 `注解库.前向引用('X').求值()`、`选择器.select选择器.选择` 都是 AttributeError。
#   这里反过来挂：从英文名取**描述符本体**，把中文名加上去。只加描述符别名，
#   **不装钩子**（英文类协议不改，照 D-070）；C 类型不可变、setattr 抛 TypeError 就跳过
#   （C 类型的方法名归机制 1 的方法名表管）。
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # 中文名已经在类里（改名成功）⇒ 没事，主循环已把英文名补回去了。
        if _中 in _类.__dict__ or any(_中 in _基.__dict__ for _基 in _类.__mro__):
            continue
        _原 = _类.__dict__.get(_英, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _英 in _基.__dict__:
                    _原 = _基.__dict__[_英]
                    break
        if _原 is None:
            _转发跳过.append((_类名, _英, _中))
            continue
        try:
            setattr(_类, _中, _原)
        except TypeError:
            continue    # C 类型不可变挂不上；主循环已经记过一笔，不重复记
        if (_类名, _英, _中) in _转发跳过:
            _转发跳过.remove((_类名, _英, _中))

# 实例属性：两个方向都翻（英文名 <-> 中文名）。
# **逻辑只有一份**，在 `_装类转发` 里 —— 每个类定义紧后面已经装过一次
# （照 D-040），这里是文件末尾的兜底，幂等。
_实例属性 = {
    'HTML日历': {
        'formatday': '格式化日',
        'formatmonth': '格式化月',
        'formatmonthname': '格式化月名',
        'formatweek': '格式化周',
        'formatweekday': '格式化星期名',
        'formatweekheader': '格式化星期表头',
        'formatyear': '格式化年',
        'formatyearpage': '格式化年页面',
        'iterweekdays': '迭代星期',
        'monthdays2calendar': '月天数对表',
    },
    '_CLIDemoCalendar': {
        'formatday': '格式化日',
        'formatmonth': '格式化月',
        'formatmonthname': '格式化月名',
        'formatweek': '格式化周',
        'formatweekheader': '格式化星期表头',
        'formatyear': '格式化年',
        'monthdays2calendar': '月天数对表',
        'yeardays2calendar': '年天数对表',
    },
    '文本日历': {
        'formatday': '格式化日',
        'formatmonth': '格式化月',
        'formatmonthname': '格式化月名',
        'formatweek': '格式化周',
        'formatweekday': '格式化星期名',
        'formatweekheader': '格式化星期表头',
        'formatyear': '格式化年',
        'iterweekdays': '迭代星期',
        'monthdays2calendar': '月天数对表',
        'prmonth': '打印月',
        'prweek': '打印周',
        'pryear': '打印年',
        'yeardays2calendar': '年天数对表',
    },
    '日历器': {
        'getfirstweekday': '取每周第一天',
        'itermonthdates': '迭代月日期',
        'itermonthdays': '迭代月天数',
        'itermonthdays2': '迭代月天数对',
        'itermonthdays3': '迭代月天数三',
        'itermonthdays4': '迭代月天数四',
        'iterweekdays': '迭代星期',
        'monthdatescalendar': '月日期表',
        'monthdays2calendar': '月天数对表',
        'monthdayscalendar': '月天数列表',
        'setfirstweekday': '设每周第一天',
        'yeardatescalendar': '年日期表',
        'yeardays2calendar': '年天数对表',
        'yeardayscalendar': '年天数表',
    },
    '本地HTML日历': {
        'formatmonthname': '格式化月名',
        'formatweekday': '格式化星期名',
    },
    '本地文本日历': {
        'formatmonthname': '格式化月名',
        'formatweekday': '格式化星期名',
    },
    '非法星期错误': {
        'weekday': '星期几',
    },
    '非法月份错误': {
        'month': '月份',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'HTML日历',
    '周表头',
    '年历',
    '打印年历',
    '打印月',
    '文本日历',
    '日历器',
    '时间戳',
    '星期几',
    '星期名',
    '星期枚举',
    '星期简称',
    '是闰年',
    '月份',
    '月份名',
    '月份枚举',
    '月份简称',
    '月历',
    '月范围',
    '本地HTML日历',
    '本地文本日历',
    '格式',
    '设每周第一天',
    '闰年天数',
    '非法星期错误',
    '非法月份错误',
]

# ---- 转发层结束 ----
