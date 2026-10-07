# 编辑器扩展

让编辑器认识 ChinesePython 的中文关键字。**这里的东西都是生成的** ——
改请改 `tools/生成编辑器扩展.py`，然后跑 `tools/校验编辑器扩展.py` 确认没跟解释器脱节。

> 例外：`vscode/src/` 下两个文件（`bridge.js` 诊断桥 + `diagnose.py` 解释器侧）是**手写**的，
> 不由生成器产出；它们由「源 ↔ VSIX 包 ↔ 已安装」三份一致守卫（`tools/打包编辑器扩展.ps1 -检查`）
> 与 `tests/诊断桥冒烟.py` 看住。

| 目录 | 给谁 | 给什么 |
|---|---|---|
| [`vscode/`](vscode/) | VS Code | **高亮**（注入式语法，不替换内置 Python 语法）+ 代码片段 + **诊断桥**（用我们自己的解释器做语法诊断，D-195） |
| [`pycharm/`](pycharm/) | PyCharm | **代码片段**（实时模板，可直接导入）。高亮那边没解，原因见它的 README |
| [`vscode-kit/`](vscode-kit/) | VS Code | 一键装配用的**配置模板**（settings / tasks / launch + 中文示例） |

## 一键装配到我的 VS Code

```powershell
pwsh -File editors/attach-to-vscode.ps1 -工作区 D:/我的项目    # 从当前源重打 VSIX + 装 + 写 .vscode/ 配置
pwsh -File editors/detach-from-vscode.ps1 -工作区 D:/我的项目  # 一键还原（有备份还原备份，没备份删掉我们写的）
```

（Windows 上也可以双击 `一键装配到我的VSCode.cmd` / `一键还原.cmd`。）

**语义是「重打 + 装」**，不是「装附件里那个现成 VSIX」—— 有版本号、没有构建身份的东西一定会漂（D-193）。
**故意不预置**任何「关掉 Pylance」的设置（目标机上通常没装官方 Python 扩展，预先关一个不存在的扩展，用户看不懂为什么）。

覆盖 **202** 个名字（中文关键字 35 + 软关键字 3 + 内置名 74 + 异常类名 85 + 模块孪生属性 5），
分成 14 个作用域。名字全部来自解释器自己那几张表，不是手抄的：

```
Tools/peg_generator/pegen/zh_keywords.py   硬关键字 / 软关键字（D-144）
Python/bltinmodule.c     zh_aliases[]
Python/pylifecycle.c     late[]          ← 装晚了的那几个（比如「打开」）
Objects/exceptions.c     zh_exc_aliases[]
Objects/moduleobject.c   zh_module_twins[]
```

## 为什么要生成，不手写

编辑器的关键字表是最容易**悄悄过期**的东西：加一个关键字、改一个译名，
编辑器那边没人会想起来同步，高亮就慢慢跟解释器对不上 —— 而且一声不吭。
第一版这个生成器只读了 `bltinmodule.c`，就漏掉了 `Python/pylifecycle.c` 里
「装晚了」的 `打开`；是 `tools/校验编辑器扩展.py` 拿 `dir(builtins)` 一比才现形的。

所以校验器查的不是「文件写得对不对」，是**「跟解释器还是不是一回事」**：

```powershell
python tools\校验编辑器扩展.py
```

它做五件事：名字对得上（拿 `keyword.kwlist` / `dir(builtins)` 比）、
整词匹配（`类型别名` 不能被切成 `类型`+`别名`，这就是不能用 `\b` 的原因）、
最长匹配、注释与字符串里的汉字不许高亮、纯英文 Python 文件零命中，
最后再确认生成物没跟生成器脱节。

## 打包与校验（D-193）

```powershell
pwsh -File tools/打包编辑器扩展.ps1        # 重生成源 -> 打 VSIX 到 dist/
pwsh -File tools/打包编辑器扩展.ps1 -检查   # 源 <-> 包内 逐字节 + 包内嵌源哈希 +（装了的话）已安装那份
```

**为什么加这一环**：曾出现「源在 10-04 改过、VSIX 还是 10-01 打的」——
**有版本号、没有构建身份**的东西一定会漂。所以 VSIX 里现在带 `extension/源哈希.txt`
（四份源的联合 SHA-256），包能自证出处；打包与校验都已挂闸门。
