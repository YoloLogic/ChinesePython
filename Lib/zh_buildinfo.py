# -*- coding: utf-8 -*-
"""ChinesePython 的构建身份（``python --build-info``）。

数据来自生成物 ``zh_buildinfo_data``（由 ``tools/生成构建信息.py`` 生成，见 D-197）。
本文件是**手写**的：报告怎么摆、哪些值运行时实测，都在这里。

两条硬规矩：
1. **不许猜**。``sys.version``、``python314.dll`` 的 SHA-256、pip 版本都**当场实测**再打印；
   生成时的值同时打印作对照 —— 不一致就是不一致（P1 那种「同版本号的第二份 dll」当场露馅）。
2. **不许按清单挑**。身份只有一个：``base-3.14.7`` → 工作树全量改动文件的联合哈希。
"""
import hashlib
import os
import pathlib
import sys
import time

try:
    from zh_buildinfo_data import 数据
except Exception as 错:  # 生成物缺失/坏了也不能崩
    数据 = None
    _读不出 = str(错)

__all__ = ["数据", "报告", "report", "python_dll", "实装pip", "生成时间"]


def _文件哈希(路):
    try:
        return hashlib.sha256(pathlib.Path(路).read_bytes()).hexdigest()
    except OSError:
        return None


def python_dll():
    """返回 (路径, 实测哈希)；实测不到就是 None。"""
    夹 = pathlib.Path(sys.executable).parent
    名 = "python%d%d.dll" % sys.version_info[:2]
    for 候选 in (名, "_" + 名):
        路 = 夹 / 候选
        if 路.is_file():
            return str(路), _文件哈希(路)
    return str(夹 / 名), None


def 实装pip():
    try:
        import importlib.metadata as 元数据
        return 元数据.version("pip")
    except Exception:
        return "未知"


def 生成时间():
    try:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(__file__)))
    except OSError:
        return "未知"


def 报告():
    """--build-info 打印的就是这一串。第一行是人类可读的一句话。"""
    if 数据 is None:
        return ("ChinesePython 构建身份：读不出生成物 zh_buildinfo_data（" + _读不出 + "）" + chr(10)
                + "版本    : " + sys.version + chr(10)
                + "提示    : 跑一次 tools/生成构建信息.py，或确认 Lib 里带着 zh_buildinfo_data.py")
    行 = []
    行.append("ChinesePython 0.1.0 = CPython " + sys.version.split()[0] + " 的 fork；改动 "
             + str(数据["改动数"]) + " 个文件（Lib/ " + str(数据["改动_Lib"]) + "）；身份 "
             + 数据["身份"][:16] + "…")
    行.append("版本    : " + sys.version)
    路, 实测 = python_dll()
    if 实测 and 实测 == 数据["python_dll"]:
        判 = "一致"
    elif 实测:
        判 = "不一致（这个 dll 不是生成时那个！）"
    else:
        判 = "读不到（只有生成时的值）"
    行.append("dll     : " + 路 + "  " + ("实测 " + 实测[:16] if 实测 else "实测 读不到")
             + " / 生成时 " + 数据["python_dll"][:16] + "  [" + 判 + "]")
    行.append("身份    : " + 数据["身份"])
    行.append("          （" + 数据["基线"] + " → 工作树 全量改动文件的联合哈希；唯一排除物：Lib/zh_buildinfo_data.py 自身）")
    行.append("仓 HEAD : ChinesePython " + 数据["仓_HEAD"]["ChinesePython"][:12] + " / Python "
             + 数据["仓_HEAD"]["Python"][:12] + "   （生成时快照）")
    行.append("生成器  : " + "  ".join(名 + "=" + 值[:12] for 名, 值 in sorted(数据["生成器"].items())))
    实 = 实装pip()
    # 生成时那个值可能带来源注记（比如「26.2.1（ensurepip 轮子）」），比版本号时先剥掉
    # —— 否则**装好的包里**会永远显示「← 不一致」，那是假警报。
    pip记 = 数据["pip"].split("（")[0].strip()
    行.append("pip     : 生成时 " + 数据["pip"] + " / 实装 " + 实 + ("" if 实 == pip记 else "   ← 不一致"))
    行.append("生成时间: " + 生成时间() + "（本文件的 mtime）")
    return chr(10).join(行)


# C 侧 --build-info 调的是 ASCII 名（宽字符串里不塞中文，免得栽在编码上）
report = 报告


if __name__ == "__main__":
    print(报告())
