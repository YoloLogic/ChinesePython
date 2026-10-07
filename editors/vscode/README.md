# ChinesePython for VS Code

给 [ChinesePython](https://github.com/YoloLogic/ChinesePython) 加中文关键字高亮和代码片段。

**这个文件夹里的东西是生成的**，改请改 `tools/生成编辑器扩展.py`，
然后跑一次 `tools/校验编辑器扩展.py` 确认没跟解释器脱节。

- `syntaxes/chinesepython.tmLanguage.json` —— 注入式语法（`injectTo: source.python`），
  **不替换**内置 Python 语法，只往里加：英文关键字、注释、字符串、缩进照旧。
- `snippets/chinesepython.json` —— 202 个中文关键字/名字的代码片段。

## 装

仓库里已经打好一个可以直接装的包：`editors/dist/chinesepython-0.1.1.vsix`

```powershell
code --install-extension editors\dist\chinesepython-0.1.1.vsix
```

或者在 VS Code 里 `扩展` 面板右上角 `...` → `从 VSIX 安装`。

## 自己打包

```powershell
cd editors\vscode
npx --yes @vscode/vsce package --out ..\dist\chinesepython-0.1.1.vsix
```

（会警告一句「没有 LICENSE」—— 仓库许可证还没定稿，属正常。）

覆盖 202 个名字（中文关键字 35 + 软关键字 3 + 内置名 74 + 异常类名 85 + 模块孪生属性 5）。

## 许可证

跟仓库一致，**还没定稿**（见仓库根 `README.md`），所以 `package.json` 里
故意没写 `license` —— `vsce package` 会因此警告一句，属正常。
