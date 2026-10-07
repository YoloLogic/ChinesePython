# ChinesePython for PyCharm

PyCharm 的 Python 关键字表**是编在 Python 插件里的**，没有用户可改的入口，
所以这边给的是**实时模板（Live Templates）**，不是高亮。

## 怎么装

1. `设置 → 编辑器 → 实时模板 → 右上角齿轮 → 导入`
2. 选 `ChinesePython.xml`
3. 在 Python 分组里勾上（导入后会自动进 `ChinesePython` 组）

装完输入 `如果` 再按 Tab，就会展开成

```python
如果 条件:
    ...
```

覆盖 38 个关键字（硬 35 + 软 3）。

## 高亮怎么办

老实说：**PyCharm 这边没解**。它的 Python 解析器认识的关键字是硬编码的，
`如果` / `定义` 会被当成普通标识符着色。能绕过的是「File Types 里挂一个
TextMate 包」，但那会**整份替掉** Python 高亮（注释、字符串、f-string 全乱），
得不偿失。所以这里不做，也不假装做了。

要完整的高亮，用 VS Code 那一份（`editors/vscode/`）。
