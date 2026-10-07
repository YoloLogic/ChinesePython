# vscode-kit（一键装配用的模板）

这三个 JSON 是**模板**：`editors/attach-to-vscode.ps1` 会把它们抄进你工作区的 `.vscode/`，
并把里面的占位符 `__CHINESEPYTHON_PYTHON__` 换成 **ChinesePython 的 `python.exe`**。

| 文件 | 作用 |
|---|---|
| `settings.json` | 指定解释器（Python 扩展用）+ 诊断桥用的解释器（`chinesepython.interpreter`）+ UTF-8 编码 |
| `tasks.json` | 「ChinesePython：跑当前文件」/「自检」两条任务 |
| `launch.json` | 调试配置（需要官方 ms-python 扩展；没装也不影响高亮与诊断桥） |
| `中文示例.py` | 一个能直接跑的中文示例（含「删个右括号看波浪线」的提示） |

**故意不预置**任何「关掉 Pylance」的设置（见 `../../发布模板/常见问题.md`）。