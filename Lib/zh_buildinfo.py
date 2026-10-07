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
    """返回 (路径, 实测哈希)；实测不到就是 None。

    Windows：挨着 python.exe 的 python314.dll；
    Linux/macOS：libpython3.14.so / .dylib —— **优先问 sysconfig**（别硬猜），
    再退回构建树里常见的名字（构建树里它就跟 ./python 同级）。"""
    夹 = pathlib.Path(sys.executable).parent
    候 = []
    if sys.platform == "win32":
        名 = "python%d%d.dll" % sys.version_info[:2]
        候 = [夹 / 名, 夹 / ("_" + 名)]
    else:
        核 = "libpython%d.%d" % sys.version_info[:2]
        # ⚠ 先找**构建树里**我们自己编出来的那份，再退 sysconfig：
        #   Ubuntu 默认不编共享库 ⇒ 产物是 libpython3.14.a（静态库）；
        #   而 sysconfig 可能指向系统里**另一份**安装的库（实测踩过，D-209）。
        候 += [夹 / (核 + 扩) for 扩 in (".so", ".so.1.0", ".dylib", ".a")]
        try:
            import sysconfig
            名 = sysconfig.get_config_var("INSTSONAME") or sysconfig.get_config_var("LDLIBRARY")
            库夹 = sysconfig.get_config_var("LIBDIR")
            if 名:
                候.append((pathlib.Path(库夹) if 库夹 else 夹) / 名)
        except Exception:
            pass
    路 = next((p for p in 候 if p.is_file()), None)
    if 路 is None:
        return str(候[0] if 候 else 夹), None
    return str(路), _文件哈希(路)


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
    行.append("ChinesePython " + str(数据.get("版本", "0.1.1")) + " = CPython " + sys.version.split()[0] + " 的 fork；改动 "
             + str(数据["改动数"]) + " 个文件（Lib/ " + str(数据["改动_Lib"]) + "）；身份 "
             + 数据["身份"][:16] + "…")
    行.append("版本    : " + sys.version)
    路, 实测 = python_dll()
    同名 = (pathlib.Path(路).name == str(数据.get("python_dll_名", "")))
    if 实测 and 实测 == 数据["python_dll"]:
        判 = "一致"
    elif 实测 and not 同名:
        # 跨平台/跨构建（生成时那份是 Windows 的 python314.dll，本机是 libpython3.14.a 之类）
        # ⇒ 根本不是同一个文件，**不该喊「不一致」**（D-212 修：以前在 Linux 上一直误报）。
        判 = "跨平台/跨构建（生成时那份是 " + str(数据.get("python_dll_名", "?")) + "）⇒ 跳过比对"
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
