# -*- coding: utf-8 -*-
"""URL工具.机器人规则 —— 汉语库（由 tools/汉化库.py 从 Lib/urllib/robotparser.py 机械生成，**不要手改**）。

英文库 Lib/urllib.robotparser.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py urllib
"""


""" robotparser.py

    Copyright (C) 2000  Bastian Kleineidam

    You can choose between two licenses when using this package:
    1) GNU GPLv2
    2) PSF license for Python 2.2

    The robots.txt Exclusion Protocol is implemented as specified in
    RFC 9309
"""
_英文原名表 = {'Entry': '条目', 'RobotFileParser': '机器人规则解析器', 'RuleLine': '规则行'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import collections
import re
import URL工具.错误
import URL工具.解析
import URL工具.请求
__all__ = ['RobotFileParser']
RequestRate = collections.namedtuple('RequestRate', 'requests seconds')

class 机器人规则解析器:
    """ This class provides a set of methods to read, parse and answer
    questions about a single robots.txt file.

    """

    def __init__(self, url=''):
        self.entries = []
        self.groups = {}
        self.sitemaps = []
        self.default_entry = None
        self.disallow_all = False
        self.allow_all = False
        self.set_url(url)
        self.last_checked = 0

    def mtime(self):
        """Returns the time the robots.txt file was last fetched.

        This is useful for long-running web spiders that need to
        check for new robots.txt files periodically.

        """
        return self.last_checked

    def modified(self):
        """Sets the time the robots.txt file was last fetched to the
        current time.

        """
        import time
        self.last_checked = time.time()

    def set_url(self, url):
        """Sets the URL referring to a robots.txt file."""
        self.url = url
        self.host, self.path = URL工具.解析.urlsplit(url)[1:3]

    def read(self):
        """Reads the robots.txt URL and feeds it to the parser."""
        try:
            f = URL工具.请求.urlopen(self.url)
        except URL工具.错误.HTTPError as err:
            if err.code in (401, 403):
                self.disallow_all = True
            elif 400 <= err.code < 500:
                self.allow_all = True
            elif 500 <= err.code < 600:
                self.disallow_all = True
            err.close()
        else:
            raw = f.read()
            self.parse(raw.decode('utf-8', 'surrogateescape').splitlines())

    def _add_entry(self, entry):
        self.entries.append(entry)
        for agent in entry.useragents:
            agent = agent.lower()
            if agent not in self.groups:
                self.groups[agent] = entry
            else:
                self.groups[agent] = merge_entries(self.groups[agent], entry)

    def parse(self, lines):
        """Parse the input lines from a robots.txt file.

        We allow that a user-agent: line is not preceded by
        one or more blank lines.
        """
        entries = []
        state = 0
        entry = 条目()
        self.modified()
        for line in lines:
            i = line.find('#')
            if i >= 0:
                line = line[:i]
            line = line.strip()
            if not line:
                continue
            line = line.split(':', 1)
            if len(line) == 2:
                line[0] = line[0].strip().lower()
                line[1] = line[1].strip()
                if line[0] == 'user-agent':
                    if state == 2:
                        self._add_entry(entry)
                        entry = 条目()
                    product_token = line[1]
                    entry.useragents.append(product_token)
                    state = 1
                elif line[0] == 'disallow':
                    if state != 0:
                        state = 2
                        try:
                            entry.rulelines.append(规则行(line[1], False))
                        except ValueError:
                            pass
                elif line[0] == 'allow':
                    if state != 0:
                        state = 2
                        try:
                            entry.rulelines.append(规则行(line[1], True))
                        except ValueError:
                            pass
                elif line[0] == 'crawl-delay':
                    if state != 0:
                        if line[1].strip().isdecimal():
                            entry.delay = int(line[1])
                        state = 2
                elif line[0] == 'request-rate':
                    if state != 0:
                        numbers = line[1].split('/')
                        if len(numbers) == 2 and numbers[0].strip().isdecimal() and numbers[1].strip().isdecimal():
                            entry.req_rate = RequestRate(int(numbers[0]), int(numbers[1]))
                        state = 2
                elif line[0] == 'sitemap':
                    self.sitemaps.append(line[1])
        if state != 0:
            self._add_entry(entry)

    def _find_entry(self, useragent):
        entry = self.groups.get(useragent.lower())
        if entry is not None:
            return entry
        for entry in self.groups.values():
            if entry.applies_to(useragent):
                return entry
        return self.groups.get('*')

    def can_fetch(self, useragent, url):
        """using the parsed robots.txt decide if useragent can fetch url"""
        if self.disallow_all:
            return False
        if self.allow_all:
            return True
        if not self.last_checked:
            return False
        parsed_url = URL工具.解析._urlsplit(url, '')
        url = URL工具.解析._urlunsplit(None, None, *parsed_url[2:])
        url = normalize_uri(url)
        if not url:
            url = '/'
        if url == '/robots.txt':
            return True
        entry = self._find_entry(useragent)
        if entry is None:
            return True
        return entry.allowance(url)

    def crawl_delay(self, useragent):
        if not self.mtime():
            return None
        entry = self._find_entry(useragent)
        if entry is None:
            return None
        return entry.delay

    def request_rate(self, useragent):
        if not self.mtime():
            return None
        entry = self._find_entry(useragent)
        if entry is None:
            return None
        return entry.req_rate

    def site_maps(self):
        if not self.sitemaps:
            return None
        return self.sitemaps

    def __str__(self):
        entries = self.entries
        if self.default_entry is not None:
            entries = entries + [self.default_entry]
        return '\n\n'.join(filter(None, map(str, entries)))

class 规则行:
    """A rule line is a single "Allow:" (allowance==True) or "Disallow:"
       (allowance==False) followed by a path."""

    def __init__(self, path, allowance):
        if path == '' and (not allowance):
            allowance = True
        path = re.sub('[*]{2,}', '*', path)
        path = re.sub('[$][$*]+', '$', path)
        path = normalize_pattern(path)
        self.fullmatch = path.endswith('$')
        path = path.rstrip('$')
        if '$' in path:
            raise ValueError('$ not at the end of path')
        self.matcher = None
        if '*' in path:
            pattern = re.compile(translate_pattern(path), re.DOTALL)
            if self.fullmatch:
                self.matcher = pattern.fullmatch
            else:
                self.matcher = pattern.match
        self.path = path
        self.allowance = allowance

    def applies_to(self, filename):
        if self.matcher is not None:
            m = self.matcher(filename)
            if m:
                return m.end() + 1
        elif self.fullmatch:
            if filename == self.path:
                return len(self.path) + 1
        elif filename.startswith(self.path):
            return len(self.path) + 1
        return 0

    def __str__(self):
        return ('Allow' if self.allowance else 'Disallow') + ': ' + self.path + ('$' if self.fullmatch else '')

class 条目:
    """An entry has one or more user-agents and zero or more rulelines"""

    def __init__(self):
        self.useragents = []
        self.rulelines = []
        self.delay = None
        self.req_rate = None

    def __str__(self):
        if not self.useragents:
            return ''
        ret = []
        for agent in self.useragents:
            ret.append(f'User-agent: {agent}')
        if self.delay is not None:
            ret.append(f'Crawl-delay: {self.delay}')
        if self.req_rate is not None:
            rate = self.req_rate
            ret.append(f'Request-rate: {rate.requests}/{rate.seconds}')
        if self.rulelines:
            ret.extend(map(str, self.rulelines))
        else:
            ret.append('Allow:')
        return '\n'.join(ret)

    def applies_to(self, useragent):
        """check if this entry applies to the specified agent"""
        if useragent is None:
            return '*' in self.useragents
        useragent = useragent.split('/')[0].lower()
        for agent in self.useragents:
            if agent != '*':
                agent = agent.lower()
                if agent in useragent:
                    return True
        return False

    def allowance(self, filename):
        """Preconditions:
        - our agent applies to this entry
        - filename is URL encoded
        """
        best_match = -1
        allowance = True
        for line in self.rulelines:
            m = line.applies_to(filename)
            if m:
                if m > best_match:
                    best_match = m
                    allowance = line.allowance
                elif m == best_match and (not allowance):
                    allowance = line.allowance
        return allowance

def normalize(path):
    unquoted = URL工具.解析.unquote(path, errors='surrogateescape')
    return URL工具.解析.quote(unquoted, errors='surrogateescape')

def normalize_uri(path):
    path, sep, query = path.partition('?')
    path = normalize(path)
    if sep:
        query = re.sub('[^=&]+', lambda m: normalize(m[0]), query)
        path += '?' + query
    return path

def normalize_pattern(path):
    path, sep, query = path.partition('?')
    path = re.sub('[^*$]+', lambda m: normalize(m[0]), path)
    if sep:
        query = re.sub('[^=&*$]+', lambda m: normalize(m[0]), query)
        path += '?' + query
    return path

def translate_pattern(path):
    parts = list(map(re.escape, path.split('*')))
    for i in range(1, len(parts) - 1):
        parts[i] = f'(?>.*?{parts[i]})'
    parts[-1] = f'.*{parts[-1]}'
    return ''.join(parts)

def merge_entries(e1, e2):
    entry = 条目()
    entry.useragents = list(filter(set(e2.useragents).__contains__, e1.useragents))
    entry.rulelines = e1.rulelines + e2.rulelines
    entry.delay = e1.delay if e2.delay is None else e2.delay
    entry.req_rate = e1.req_rate if e2.req_rate is None else e2.req_rate
    return entry


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Entry': '条目',
    'RobotFileParser': '机器人规则解析器',
    'RuleLine': '规则行',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '机器人规则解析器',
]

# ---- 转发层结束 ----
