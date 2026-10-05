# -*- coding: utf-8 -*-
"""显示层中文报错。

干的事只有一件：把「马上就要打到屏幕上的那行字」换成中文。

不干的事（很重要）：
  * 不改 type.__name__ / type.__qualname__
  * 不改 e.args、不改 str(e)、不改 e.msg
  也就是说异常对象本身一个字都没动，只有 traceback 在**格式化输出**时查表换词。
  于是 pickle（按名字序列化异常）、inspect、logging、except 匹配全部照旧。

三道保险：
  1. 查不到就原样返回英文——绝不猜、绝不半译。
  2. 这个模块里任何一步出错都被吞掉并退回英文：报错过程本身再抛异常是最糟的体验。
  3. 环境变量 CHINESEPYTHON_ERRORS=en 一键关掉，=both 中英并排（校对用）。

表在 zh_errmessages.py 里，由 tools/校验报错表.py 机械校验。
"""

import os
import re

# ---------------------------------------------------------------------------
# 模式
# ---------------------------------------------------------------------------

模式们 = ("zh", "en", "both")


def 取模式():
    """zh（默认）/ en / both。读环境变量，读不到或写错都当 zh。"""
    try:
        值 = os.environ.get("CHINESEPYTHON_ERRORS", "zh")
    except Exception:
        return "zh"
    if not isinstance(值, str):
        return "zh"
    值 = 值.strip().lower()
    return 值 if 值 in 模式们 else "zh"


# ---------------------------------------------------------------------------
# 格式串 → 正则
# ---------------------------------------------------------------------------
#
# 英文正文里带 %s / %d / %.200s / %zd / %U 这类占位符。做法是：
#   把「连续的一串占位符」整体算作 **一个** 捕获组（(.*)）。
# 这样最安全——两个挨着的 %s 本来就分不出边界，硬拆只会串位。
# 中文模板里用 %1 %2 %3 指第几个捕获组，可以少用、可以调换顺序
# （英文的 %s 有时候只是复数后缀，中文不需要）。

_格式 = re.compile(
    r"%(?:[-+ #0]*)(?:\d+|\*)?(?:\.(?:\d+|\*))?(?:hh|h|ll|l|L|z|j|t)?[diouxXeEfFgGcrsa]"
    r"|%(?:[-+ #0]*)(?:\d+|\*)?(?:\.(?:\d+|\*))?[URSVTApbN]"
    r"|%%"
)


def _转义(字面):
    # 格式串里的 %% 在真正的正文里就是一个 %
    return re.escape(字面).replace("%%", "%")


def 编模板(英文):
    """英文模板 → (正则, 捕获组个数)。正则整串锚定，绝不部分匹配。

    **除最后一组外都用非贪婪 `(.*?)`。** 这不是小事，是实测踩出来的：
        `Error %d %s: %.200s` 编译成 `^Error (.*) (.*): (.*)$` 时，
        贪婪的第一组会把 `-3 while decompressing` 一起抢走，
        第二组只剩 `data`，于是给第二组配的整组对译（while decompressing data
        → 解压数据时）永远对不上。
    非贪婪让每组只吃到**最近的**那个字面分隔符，这才符合格式串的本意。
    最后一组保持贪婪——它本来就该吞掉剩下的全部。
    """
    段 = []          # 交替放字面片段和 None（None 表示一个捕获组）
    i = 0
    字面起 = 0
    n = len(英文)
    while i < n:
        m = _格式.match(英文, i)
        if m is None:
            i += 1
            continue
        if m.group(0) == "%%":
            i = m.end()
            continue
        段.append(_转义(英文[字面起:i]))
        j = m.end()
        while True:
            m2 = _格式.match(英文, j)
            if m2 is None or m2.group(0) == "%%":
                break
            j = m2.end()
        段.append(None)
        i = j
        字面起 = j
    段.append(_转义(英文[字面起:]))

    组数 = sum(1 for x in 段 if x is None)
    拼 = []
    见 = 0
    for x in 段:
        if x is None:
            见 += 1
            拼.append("(.*)" if 见 == 组数 else "(.*?)")
        else:
            拼.append(x)
    return re.compile("^" + "".join(拼) + "$", re.DOTALL), 组数


def _前缀键(英文):
    """模板开头那段固定文字的前 6 个字符；查表时拿正文的前 6 个字符去对。"""
    k = 英文.find("%")
    return (英文 if k < 0 else 英文[:k])[:6]


def _字面字数(英文):
    """模板里除去占位符之后还剩多少字面字符。"""
    n = 0
    i = 0
    while i < len(英文):
        m = _格式.match(英文, i)
        if m is None:
            n += 1
            i += 1
        else:
            i = m.end()
    return n


def 模板安全(英文, 自校验=False):
    """太笼统的模板不能用，否则会误伤一大片正文。

    比如 `%s: %s` 会匹配上任何带冒号的句子，把好好的英文正文换成
    「甲：乙」——看着像中文，其实是把信息搞糊了。宁可漏，不可错。

    **开头就是占位符的模板要额外收紧。** 它会匹配「任何以后面那段文字收尾」
    的正文，而这类正文恰恰是「外壳包内层」的重灾区：
      `%s in %r`   —— 会吃掉任何含 in 的句子
      `%s: %s`     —— 会吃掉任何带冒号的句子
    真正有用的外壳（`%s at position %d`、`%s: line %d column %d (char %d)`）
    字面量都长得多，所以把起始占位符这一类的门槛抬到 8 个字符就够了。

    `自校验=True` 是给**手写**表里那些带「再翻必需」的外壳留的口子：
    它们只有在内层确实是一句已知正文时才成立，本身就带自检，不用靠字数把关。
    自动生成的一律传默认值，享受不到这个口子。
    """
    if "%" not in 英文:
        return True
    if 自校验:
        return _字面字数(英文) >= 1
    门槛 = 8 if 英文.startswith("%") else 4
    return _字面字数(英文) >= 门槛


_占位 = re.compile(r"%(\d+)")


def 填模板(中文模板, 分组):
    """把中文模板里的 %1 %2 换成捕获到的原文。%% 表示一个字面 %。"""
    占位符 = "\x00"
    文 = 中文模板.replace("%%", 占位符)

    def 换(m):
        k = int(m.group(1)) - 1
        if 0 <= k < len(分组):
            return 分组[k]
        return m.group(0)

    return _占位.sub(换, 文).replace(占位符, "%")


# ---------------------------------------------------------------------------
# 表
# ---------------------------------------------------------------------------

_未载入 = object()
_表 = _未载入
_已编桶 = {}


def _装配(数据):
    正文 = {}
    模板桶 = {}
    略去 = []
    # 三张数据表：
    #   zh_errmessages      手写：异常名 + 语法报错 + 高频运行时 + 框架行
    #   zh_errmessages_gen  C 层长尾，由 tools/合并报错译文.py 生成
    #   zh_errmessages_lib  库层（Lib/**/*.py 里 raise 的），同一个工具生成
    # 每张表里又分两段：
    #   `对照`      = 解释器自己有的正文（C 层能从源码逐条核对，库层能从 ast 挖出来核对）
    #   `对照_额外` = 源码里不是整条字面量、只能手写的（importlib 那种）
    源们 = [数据]
    for 名 in ("zh_errmessages_gen", "zh_errmessages_lib"):
        try:
            源们.append(__import__(名))
        except Exception:
            pass

    for 源 in 源们:
        for 表名 in ("对照", "对照_额外"):
            for 项 in getattr(源, 表名, ()):
                try:
                    英, 中 = 项[0], 项[1]
                    词替换 = 项[2] if len(项) > 2 else None
                except Exception:
                    continue
                if not isinstance(英, str) or not isinstance(中, str) or not 英:
                    continue
                if "%" not in 英:
                    # 没有占位符的走精确表，O(1)，也彻底杜绝误匹配
                    正文.setdefault(英, 中)
                    continue
                # 手标的「外壳」模板：`%s at position %d` 这种，它的 %1 是**另一句正文**。
                # 必须比普通模板先试，否则内层模板会把外壳追加的上下文一起吞掉
                # （实测：`组名 '1' at position 4 中有非法字符`）。
                # 只有手写表里明确标了的才进这里 —— 自动生成的一律不标，
                # 因为「开头是占位符」不等于「是外壳」，误判会让它抢走别的正文。
                是外壳 = isinstance(词替换, dict) and 词替换.get("优先")
                # 带「再翻必需」的外壳有自校验，可以绕开泛化门槛
                自校验 = 是外壳 and any(v == "再翻必需" for v in 词替换.values())
                if not 模板安全(英, 自校验):
                    略去.append(英)
                    continue
                if 是外壳:
                    模板桶.setdefault("__优先__", []).append((英, 中, 词替换))
                else:
                    模板桶.setdefault(_前缀键(英), []).append((英, 中, 词替换))
    # 每个桶内部都按**字面量从长到短**排。更长的模板更具体，必须先试。
    # 实测踩过：`Error %d %s`（7 个字面）和 `Error %d %s: %.200s`（10 个字面）
    # 同在一个桶里，短的先试就匹配上了长消息，贪婪的 `%2` 把
    # `while decompressing data: incorrect header check` 整段吞了，
    # 结果 zlib 的报错变成「错误 -3 while decompressing data: incorrect header check」。
    for 组 in 模板桶.values():
        组.sort(key=lambda 项: -_字面字数(项[0]))
    # 额外收录：数据文件里想手工分成字典的固定正文
    正文.update(dict(getattr(数据, "正文", ())))
    # 模块自带异常的中文名（`re.PatternError` -> `模式错误`）。这张表**单独一张**，
    # 由 tools/生成模块异常名表.py 生成，跟内置异常名那张分开 ——
    # 前者键是「显示名」（带模块前缀），后者键是裸类名。
    模块异常名 = {}
    try:
        import zh_excnames as _模
        模块异常名 = dict(getattr(_模, "模块异常名", ()))
    except Exception:
        pass
    return {
        "异常名": dict(getattr(数据, "异常名", ())),
        "模块异常名": 模块异常名,
        "正文": 正文,
        # 前缀 -> [(英文, 中文, 词替换), ...]，正则等真用到了再编
        "模板桶": 模板桶,
        "太笼统": 略去,
        "错误号": dict(getattr(数据, "错误号文本", ())),
        "尾巴": dict(getattr(数据, "尾巴", ())),
        "框架": dict(getattr(数据, "框架", ())),
    }


def 取表():
    """载入一次，之后走缓存。任何异常都变成「没有表」，退回英文。"""
    global _表
    if _表 is not _未载入:
        return _表
    try:
        import zh_errmessages as 数据
        _表 = _装配(数据)
    except Exception:
        _表 = None
    return _表


# ---------------------------------------------------------------------------
# 查表
# ---------------------------------------------------------------------------

# traceback.py 会在正文后面追加这三个英文尾巴（前两个互斥）
_尾巴_建议 = re.compile(r"\. Did you mean: '(.*)'\?$", re.DOTALL)
_尾巴_导入并 = re.compile(r" Or did you forget to import '(.*)'\?$", re.DOTALL)
_尾巴_导入独 = re.compile(r"\. Did you forget to import '(.*)'\?$", re.DOTALL)

_错误号行 = re.compile(r"^\[(Errno|WinError) (\d+)\](.*)$", re.DOTALL)


def _试一组(候选, 文):
    for 英, 中, 词替换 in 候选:
        编 = _已编桶.get(英)
        if 编 is None:
            try:
                编 = 编模板(英)
            except Exception:
                编 = False
            _已编桶[英] = 编
        if 编 is False:
            continue
        rx, 组数 = 编
        m = rx.match(文)
        if m is None:
            continue
        分组 = list(m.groups())
        if 词替换:
            # 按组号精确处理，绝不全局替换——用户变量正好叫 s，
            # 全局替换会把 `name 's' is not defined` 变成 `name '' ...`。
            #
            # 三种处理方式：
            #   {2: {"at most": "最多 "}}  这一组是 C 代码塞进来的英文词，整组对译
            #   {2: "再翻"}                这一组本身又是一句报错正文，递归再翻一次
            #   {2: "再翻必需"}            同上，但**内层翻不动就整条作废**，换下一个候选
            #   {2: "再翻", "优先": True}  同上，并且这张模板要抢在普通模板前面
            拒绝 = False
            for 号, 法 in 词替换.items():
                if 号 == "优先":
                    continue
                i = 号 - 1
                if not (0 <= i < len(分组)):
                    continue
                if 法 == "再翻必需":
                    新 = _再翻要成功(分组[i])
                    if 新 is None:
                        拒绝 = True
                        break
                    分组[i] = 新
                elif 法 == "再翻":
                    分组[i] = _再翻(分组[i])
                elif isinstance(法, dict) and 分组[i] in 法:
                    分组[i] = 法[分组[i]]
            if 拒绝:
                continue
        return 填模板(中, 分组)
    return None


_递归深度 = [0]


def _再翻(文):
    """外壳里那一组本身又是一句正文，递归再翻一次。带深度上限防成环。"""
    if _递归深度[0] >= 5:
        return 文
    _递归深度[0] += 1
    try:
        return 翻正文(文)
    finally:
        _递归深度[0] -= 1


def _再翻要成功(文):
    """同上，但内层**翻不动就返回 None**，让调用方把整条模板作废。

    给 `%s in %r` 这种太笼统的外壳用：只有内层确实是一句已知正文时它才成立，
    否则（比如某条正文里恰好有个 ` in `）就会出来一个半中半英的壳。
    实测这招能把「Octet 999 (> 255) not permitted in '1.2.3.999'」救回来，
    又不会误伤别的正文。"""
    新 = _再翻(文)
    return None if 新 == 文 else 新


def _查模板(桶, 文):
    # 先试手标的外壳表；再按前缀从长到短试，最后才试 ""（开头就是 % 的模板）。
    # 千万不能一遇到非空桶就 break —— "" 桶几乎永非空，那样后面全试不到。
    优先 = 桶.get("__优先__")
    if 优先:
        中 = _试一组(优先, 文)
        if 中 is not None:
            return 中
    n = 6 if len(文) >= 6 else len(文)
    for k in list(range(n, 0, -1)) + [0]:
        候选 = 桶.get(文[:k])
        if not 候选:
            continue
        中 = _试一组(候选, 文)
        if 中 is not None:
            return 中
    return None


def _翻错误号(表, 文):
    """[Errno 2] No such file or directory: 'x' —— 只译中间那句系统文本。

    Windows 上同一个位置写的是 [WinError 2]，文本也不同，但处理方式一样。
    """
    m = _错误号行.match(文)
    if m is None:
        return None
    余 = m.group(3)
    冒号 = 余.rfind(": ")
    尾 = ""
    if 冒号 > 0:
        尾 = 余[冒号:]
        余 = 余[:冒号]
    中 = 表["错误号"].get(余.lstrip())
    if 中 is None:
        return None
    return "[%s %s] %s%s" % (m.group(1), m.group(2), 中, 尾)


def 翻正文(文):
    """英文正文 → 中文正文。查不到、出任何岔子，都原样返回。"""
    模式 = 取模式()
    if 模式 == "en" or not isinstance(文, str) or not 文:
        return 文
    try:
        表 = 取表()
        if not 表:
            return 文
        中 = _翻译核心(表, 文)
    except Exception:
        return 文
    if 中 is None:
        return 文
    if 模式 == "both":
        return "%s（%s）" % (中, 文)
    return 中


def _翻译核心(表, 文):
    # 先把 traceback 追加的英文尾巴摘下来，译完正文再按中文语序接回去
    建议 = None
    忘记 = None
    只忘 = None
    m = _尾巴_导入并.search(文)
    if m is not None:
        忘记 = m.group(1)
        文 = 文[:m.start()]
    else:
        m = _尾巴_导入独.search(文)
        if m is not None:
            只忘 = m.group(1)
            文 = 文[:m.start()]
    m = _尾巴_建议.search(文)
    if m is not None:
        建议 = m.group(1)
        文 = 文[:m.start()]

    中 = 表["正文"].get(文)
    if 中 is None:
        中 = _查模板(表["模板桶"], 文)
    if 中 is None:
        中 = _翻错误号(表, 文)
    if 中 is None:
        return None

    尾 = 表["尾巴"]
    if 建议 is not None:
        中 += 尾.get("建议", "。是不是想写 '%s'？") % 建议
    if 忘记 is not None:
        中 += 尾.get("忘记导入", " 还是忘了导入 '%s'？") % 忘记
    if 只忘 is not None:
        中 += 尾.get("只忘记导入", "。是不是忘了导入 '%s'？") % 只忘
    return 中


def 翻异常名(名):
    """英文异常类名 → 中文。只认整串（含点号的限定名一律不动）。"""
    模式 = 取模式()
    if 模式 == "en" or not isinstance(名, str) or not 名:
        return 名
    try:
        表 = 取表()
        if not 表:
            return 名
        中 = 表["异常名"].get(名)
    except Exception:
        return 名
    if 中 is None:
        return 名
    if 模式 == "both":
        return "%s（%s）" % (中, 名)
    return 中


def 翻显示名(名):
    """`模块.类名`（traceback 显示的那个）→ 只把**类名那部分**换掉。

    内置异常走的是上面那张 `异常名` 表；模块自带的异常（`re.PatternError`、
    `json.decoder.JSONDecodeError`）在这张 `模块异常名` 表里，键就是**显示名**。

    **模块前缀原样留着**：中文名里有 13 组会撞车（`binascii.Error` /
    `_curses.error` / `zlib.error` 全叫「错误」），去掉就看不出是谁报的了。
    模块名是代码记号，按老规矩不动。

    只影响显示：`type.__name__` / `__qualname__` / `__module__` 一个字没动。
    """
    模式 = 取模式()
    if 模式 == "en" or not isinstance(名, str) or not 名:
        return 名
    中 = 翻异常名(名)
    if 中 is not 名:
        return 中                      # 内置名，上面那张表就管了
    try:
        表 = 取表()
        if not 表:
            return 名
        换 = 表["模块异常名"].get(名)
    except Exception:
        return 名
    if 换 is None:
        return 名
    if 模式 == "both":
        return "%s（%s）" % (换, 名)
    return 换


def 有表():
    """测试用：表是否真的载进来了。"""
    return bool(取表())


def 框架(英文模板, *参数):
    """回溯**框架行**的固定说法（Traceback 头 / File-line-in / 异常链标题 / 重复行）。

    和正文不一样：这些是版式，不是异常消息。但对用户来说都是屏幕上那几行字，
    所以一样只在显示层换词，英文模板原样留在 traceback.py 里当默认值。

    `en` 模式返回英文；表里没登记就返回英文。
    中文模板的 `{}` 允许比英文少（英文的复数后缀中文用不着）。

    `both` 模式对框架行**不并排**，直接给中文 —— 框架行都带换行，
    并排会把每一行都撑成两行，一千帧的递归直接没法看。
    要英文原文用 `en`。这条是刻意的，不是漏了。
    """
    模式 = 取模式()

    def 补英文():
        try:
            return 英文模板.format(*参数)
        except Exception:
            return 英文模板

    if 模式 == "en":
        return 补英文()
    try:
        表 = 取表()
        if not 表:
            return 补英文()
        中模板 = 表["框架"].get(英文模板)
        if 中模板 is None:
            return 补英文()
        return 中模板.format(*参数)
    except Exception:
        return 补英文()
