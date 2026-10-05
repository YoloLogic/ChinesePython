# ChinesePython（发行仓）

**说中文的 Python**：中文关键字（`如果`/`类型`/`对于`/`使用`…）+ 中文标准库 API（`操作系统`、`并行.futures`、`多进程`…）+ 中文报错；与英文**可混写**，**英文原名一直可用**。基于 **CPython 3.14.7**（fork），自带 pip。

本仓只放**可以直接用的东西**：`bin\` 解释器与运行时、`Lib\` 中文标准库、一份用户手册。开发过程与决策记录不在本仓。

## 安装（一次性）
1. 把本仓放到一个**不打算再移动**的目录（例如 `D:\ChinesePython`）；
2. 双击 **`一键安装.cmd`**（把 `bin\` 加进当前用户的 PATH）；
3. **新开**一个命令行窗口，敲 `python` 即进中文 REPL。

不想改 PATH 也行：直接双击根目录 **`启动.cmd`**，或用 `bin\python.exe 你的脚本.py`。

## 快速开始
```python
导入 操作系统 作为 操
定义 平方(甲):
    返回 甲 * 甲
使用 并行.futures.线程池执行器(2) 作为 池:
    打印([任务.result() for 任务 in [池.submit(平方, 数字) for 数字 in range(4)]])
```
装第三方包：`python -m pip install 包名`（第三方库本身仍是英文 API）。

## 自检 / 卸载
```powershell
powershell -ExecutionPolicy Bypass -File verify.ps1
powershell -ExecutionPolicy Bypass -File install.ps1 -卸载
```

## 已知限制
* 报错**显示**是中文，但 `str(e)`、异常类名仍是英文（有意设计）；设环境变量 `CHINESEPYTHON_ERRORS=en` 可**完全还原**英文；
* 少数库**只翻了一部分**，另有一批库未汉化（`asyncio` / `unittest` / `importlib` / `tkinter` …）—— 这些名字的英文版照旧可用；
* **pickle 协议 <4** 写不了中文模块名，用协议 4/5（`pickle.HIGHEST_PROTOCOL`，即默认）；
* 详细清单见 `用户手册.md`，安装/使用问题见 `常见问题.md`。

## 目录
```
bin\        解释器、运行时 DLL/.pyd、pip
Lib\        中文标准库
用户手册.md  关键字全表 / 已汉化库 / 未汉化库 / 切换英文报错 / 许可
中文对照表.md 英文名 ⇄ 中文名总表
常见问题.md  FAQ
verify.ps1  自检 · install.ps1 安装/卸载 · 启动.cmd 一键进 REPL
```

## 许可与来源
基于 **CPython 3.14.7** fork（完整保留上游 PSF 许可，见 `LICENSE.txt`；上游 https://github.com/python/cpython ）。本项目自身代码/文档以 **MIT** 发布（见 `LICENSE-MIT`）。