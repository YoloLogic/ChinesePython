# ChinesePython 的许可范围（哪些受「禁止再发布」约束、哪些不受）

> 这一份说明**为什么**包里同时存在多种许可，以及**怎么判定**某个文件属于哪一种。
> 判定规则是**机器可查**的（看文件自己的声明或与上游的比对结果），不靠人记。
> 条款正文见同目录 [LICENSE](LICENSE)；逐条披露见 [NOTICE.txt](NOTICE.txt)。

著作权归 ChinesePython 项目作者所有。**本项目原创部分采用自定义许可**：
源码公开、允许阅读 / 修改（自用）/ 用它开发并发布你自己的程序（含商用），
但**禁止重新打包再发布**；唯一的例外是**非营利、原封不动地整体转发**（四个条件见 LICENSE 第四节）。

## 一、本项目原创部分 —— 受 `LICENSE` 约束（禁止再发布）

* 中文关键字拼写表、中文软关键字、中文报错显示层正文表，以及它们的生成器与守卫
  （`Python/Tools/peg_generator/pegen/zh_*.py`、`Python/Python/zh_*.c`、`Python/Python/zh_*.h`）
* 汉语标准库与库词表：`Python/Lib/zh_*.py`、`tools/库词表.py`、`tools/汉化包装层.py`、
  `tools/zh库/`（**词表驱动的中文副本**；官方 `Python/Lib/**` 的原文件我们一个字节没改）
* `tools/`、`tests/`、`docs/`、`发布模板/`、`editors/` 下的脚本、数据与文档
* 发行包里的 `install.ps1`、`verify.ps1`、`启动.cmd`、`一键安装.cmd` 与全部中文说明文档
* 编辑器扩展与 kit（`editors/`：语法高亮、中文补全、VSIX 与配置模板）

**用本项目运行 / 打包出来的程序，版权与许可完全由作者自己决定。**
本许可**不**对这些产出附加任何条件（不「传染」到你的软件）——这是明确的授权，不需要再问。

## 二、从 CPython 派生的部分 —— **PSF License Agreement**（不受本许可约束）

* 解释器本体：`Python/Python/`、`Python/Objects/`、`Python/Parser/`、`Python/Modules/`、
  `Python/Include/` 等目录中**被我们改动过的源文件**（改动清单见 `docs/构建基线.md`
  与 `python --build-info` 打出的联合哈希）
* 二进制：`python.exe`、`python314.dll`、`python3.dll`、`*.pyd`（内置扩展）
* 官方标准库原文件：`Python/Lib/**` 中**与上游同名同内容**的文件（我们不改它们，
  中文 API 走的是并列的中文副本）

这些**不是**本项目的版权：它们派生自 CPython，按 **PSF License Agreement** 分发
（正文见同目录 `LICENSE.txt`，**与上游 `Python/LICENSE` 逐字节相同**）。

⇒ **你从本发行包拿到的这些部分，仍然享有 PSF 许可给你的全部权利**（可再分发、可商用）。
`LICENSE` 里那条「禁止再发布」**只约束本项目原创部分，不改变、也无权改变**这一部分的权利。

## 三、随包的第三方组件（各按各的许可，不受本许可约束）

| 在包里 | 是什么 | 许可 / 来源 |
|---|---|---|
| `tcl90.dll`、`tcl9tk90.dll` | Tcl/Tk **9.0.4** | BSD 式（正文：`LICENSE-第三方.txt` 与 Tcl/Tk 的 `license.terms`）|
| `libcrypto-3.dll`、`libssl-3.dll` | OpenSSL **3.x** | Apache-2.0 |
| `libffi-8.dll` | libffi | MIT 式 |
| `libtommath.dll` | LibTomMath | 公有领域（Public Domain）|
| `sqlite3.dll` | SQLite | 公有领域（Public Domain）|
| `zlib1.dll` | zlib | zlib 许可 |
| `Lib/site-packages/pip` | pip **26.2.1** | MIT（见其 `METADATA` 的 `License-Expression: MIT`）|
| `vcruntime140.dll`、`vcruntime140_1.dll` | Visual C++ 运行时库（app-local）| 微软**可再分发**运行库，按其再分发条款随包附带 |

各第三方许可**正文**：`LICENSE-第三方.txt`（= 上游 `Doc/license.rst` 的逐字节副本，含 OpenSSL /
expat / libffi / zlib / LibTomMath / SQLite 等）+ `LICENSE.txt`（PSF）+ 包内
`Doc/html/license.html`（同一份许可汇编的官方 HTML 版）。逐文件来源与 SHA-256 见包内 `MANIFEST.txt`。

## 四、怎么判定（机器可查的规则）

按顺序套用，命中即停：

1. 文件头带 `SPDX-License-Identifier: <标识>` 的 ⇒ **按其声明的许可**，不受本许可约束。
2. 文件头带 `Copyright (c) ... Python Software Foundation`、`Copyright (c) ... Microsoft`
   或其他**上游署名**的 ⇒ 按其原有许可（PSF / Apache-2.0 / BSD 式 …）。
3. 位于 `Python/Lib/**`、`Python/Modules/**`、`Python/Objects/**`、`Python/Parser/**`、
   `Python/Python/**` 等上游目录，且**与上游同名文件逐字节相同**的 ⇒ 上游许可（PSF）。
4. 位于 `Python/Lib/` 但文件名以 `zh_` 开头（词表驱动的中文副本）、或位于
   `tools/` `tests/` `docs/` `发布模板/` `editors/` 的 ⇒ **本项目原创**，受 `LICENSE` 约束。
5. 二进制：按第三节表格判定；表格里没有的，视为本项目原创构建产物（受 `LICENSE` 约束），
   但其中**派生自上游的字节**仍按上游许可。

> 实现这条规则的守卫：`tests/许可条款冒烟.py` —— 它会核对许可正文是否正确、披露是否齐全，
> 并自带「这些检查必须真的会失败」的自测。

## 五、名称与图标

见同目录 [TRADEMARK.md](TRADEMARK.md)：不得用 `ChinesePython` 的名称与图标发布衍生版本
（**即使尚未注册商标，这一条作为许可条款的一部分同样有效**）。

## 六、一句话概括

> * 我们写的东西：**源码公开，但禁止重新打包再发布**；非营利原样转发可以（见 `LICENSE` 第四节）。
> * 自己用、公司内部用、拿它写程序卖钱：**随便**；你用本项目写出来的程序**完全归你**。
> * CPython / Tcl-Tk / OpenSSL 等上游与第三方：各按各的许可 —— 我们没有、也不会给它们加限制。
