# ChinesePython（发行仓）

**说中文的 Python**：中文关键字（`如果`/`类型`/`对于`/`使用`…）+ 中文标准库 API（`操作系统`、`并行.futures`、`多进程`…）+ 中文报错；与英文**可混写**，**英文原名一直可用**。基于 **CPython 3.14.7**（fork），自带 pip。

本仓只放**可以直接用的东西**：`bin\` 解释器与运行时、`Lib\` 中文标准库、一份用户手册。开发过程与决策记录不在本仓。

## 安装（一次性）
1. 把本仓放到一个**不打算再移动**的目录（例如 `D:\ChinesePython`）；
2. 双击 **`一键安装.cmd`**（把 `bin\` 加进当前用户的 PATH）；
3. **新开**一个命令行窗口，敲 `python` 即进中文 REPL。

不想改 PATH 也行：直接双击根目录 **`启动.cmd`**，或用 `bin\python.exe 你的脚本.py`。

## 两个单文件 exe（在 Release 附件里另给，不在本仓内）
* **`ChinesePython.exe`（便携解释器）**：`ChinesePython.exe 你的脚本.py` 直接用（`-c` / `-m` 也可以）；首次运行解包到 `%LOCALAPPDATA%\ChinesePython\`，之后走缓存；换了版本会**自动清掉旧缓存**。
* **`ChinesePython-install.exe`（自解压）**：双击即解包到 `%LOCALAPPDATA%\Programs\ChinesePython`，并跑一遍包内自检；**不擅自改 PATH、不写注册表**（想加 PATH 再双击包里的 `一键安装.cmd`）。

## 快速开始
```python
导入 操作系统 作为 操
来自 并行.futures 导入 线程池执行器
定义 平方(甲):
    返回 甲 * 甲
使用 线程池执行器(2) 作为 池:
    打印([任务.result() 对于 任务 属于 [池.submit(平方, 数字) 对于 数字 属于 range(4)]])
```
装第三方包：`python -m pip install 包名`（第三方库本身仍是英文 API）。

想知道「手里这份到底是哪一份」：`python --build-info` —— 会打出**全量改动文件的联合哈希**（唯一身份）、`python314.dll` 的 SHA-256（**当场实测**）、两仓 HEAD 与预装 pip 版本；**dll 被换过会当场显示不一致**。

## 自检 / 卸载
```powershell
powershell -ExecutionPolicy Bypass -File verify.ps1
powershell -ExecutionPolicy Bypass -File install.ps1 -卸载
```

## 许可与再分发
* ✅ **能用它写程序卖钱**：用它开发、运行、发布、销售**你自己的程序** —— 个人或公司、开源或闭源都行；**产出完全归使用者**，许可不附加任何条件；
* ❌ **不许重新打包发布**：不得把本发行包（或修改版）重新打包、改名换标、上架、随产品/硬件捆绑，或当付费服务提供（除事先取得作者书面许可）；
* ✅ **非营利、原封不动地整体转发可以**（教学 / 社团 / 非营利镜像；四个条件：一个字节不改 / 不收费不带广告 / 不暗示是自己的 / 保留官方来源链接）；
* ❌ **名字不能用**：不得用 `ChinesePython` 的名称与图标发布衍生版本（即使尚未注册商标，这条作为许可条款同样有效）。

正文见本仓 `LICENSE`，范围判定见 `LICENSE-SCOPE.md`，名称条款见 `TRADEMARK.md`，第三方披露见 `NOTICE.txt`。
本仓派生自 **CPython 3.14.7** 的部分按 **PSF 许可**（`LICENSE-PSF.txt`，逐字节未改）。

> ⚠ GitHub 的 **Assets 区块默认可能是折叠的** —— 看不到附件时点一下「Assets」。

## VS Code 扩展（在 Release 附件里另给）
* `chinesepython-0.1.1.vsix`：中文关键字**高亮**（注入式，不动内置 Python 语法）+ 38 条中文片段，覆盖 202 个名字。
* 装：`code --install-extension chinesepython-0.1.1.vsix`（或扩展面板 → `...` → 从 VSIX 安装）。
* ⚠ 若以后另装了官方 Python 扩展：Pylance 是 TypeScript 重实现、**永远不认识中文关键字**，中文行会被误标红（**不影响运行**）。届时见 `常见问题.md`。

## 签名与校验和
* 两个单文件 exe 与包内 exe 都带**自签**数字签名（发布者 **YoloLogic**，带时间戳）——验「来源 + 没被改过」够用；
* 但**自签**证书 Windows 默认不信任 ⇒ 首次运行仍会提示「未知发布者」（点「更多信息 → 仍要运行」）。想让本机显示为受信任，可把 `ChinesePython-signing.cer` 装进「受信任的根证书颁发机构 / 受信任的发布者」，**随你**；
* Release 说明里每个附件都有 **SHA-256**，下载后 `Get-FileHash <文件> -Algorithm SHA256` 对照一下再装；
* 要真正去掉提示只能买受信任 CA 的证书（OV/EV）或走云签名 —— 我们没买。

## 已知限制
* 报错**显示**是中文，但 `str(e)`、异常类名仍是英文（有意设计）；设环境变量 `CHINESEPYTHON_ERRORS=en` 可**完全还原**英文；
* 少数库**只翻了一部分**，另有一批库未汉化（`tkinter` …）—— 这些名字的英文版照旧可用；
* **pickle 协议 <4** 写不了中文模块名，用协议 4/5（`pickle.HIGHEST_PROTOCOL`，即默认）；
* 详细清单见 `用户手册.md`，安装/使用问题见 `常见问题.md`。

## 目录
```
bin\        解释器、运行时 DLL/.pyd、pip
Lib\        中文标准库（含 Lib\test 官方测试套）
Doc\html\   官方英文 HTML 文档（每页顶部加了中文横幅，另有 中文入口.html）
include\    C 头文件（编译 C 扩展用）
libs\       导入库（同上）
用户手册.md  关键字全表 / 已汉化库 / 未汉化库 / 切换英文报错 / 许可
中文对照表.md 英文名 ⇄ 中文名总表
常见问题.md  FAQ
verify.ps1  自检 · install.ps1 安装/卸载 · 启动.cmd 一键进 REPL
```

## 许可与来源
基于 **CPython 3.14.7** fork（完整保留上游 PSF 许可，见 `LICENSE-PSF.txt`；上游 https://github.com/python/cpython ）。本项目自身代码/文档以 **MIT** 发布（见 `LICENSE-MIT`）。