// ChinesePython 诊断桥（D-195）—— 手写文件（src/ 下只有它和 diagnose.py 不是生成的）。
//
// 干什么：把「我们解释器看得懂的语法错」变成 VS Code 的**诊断**（红波浪线）。
//   为什么要它：VS Code 的官方 Python 支持（Pylance/pyright）是 TypeScript 重实现，
//   **永远不认识中文关键字** ⇒ 中文行会被误标红；而没装官方扩展时又什么诊断都没有。
// 怎么做的：调**我们自己的解释器**跑 src/diagnose.py（它用 ast.parse），
//   拿到的必须是**机器可读的 JSON**（行/列/消息）—— 绝不解析人读的 traceback
//   （解析人读文本的桥，会在我们改一次报错格式后**静默失灵**）。
const vscode = require('vscode');
const cp = require('child_process');
const path = require('path');

let 集合 = null;
const 定时 = new Map();

function 读设置() {
    const 配 = vscode.workspace.getConfiguration('chinesepython');
    return { 解释器: 配.get('interpreter') || 'python', 开着: 配.get('diagnostics') !== false };
}

function 诊断文档(文档) {
    if (!集合 || !文档 || 文档.languageId !== 'python') {
        return;
    }
    const 设 = 读设置();
    if (!设.开着) {
        集合.delete(文档.uri);
        return;
    }
    const 桥 = path.join(__dirname, 'diagnose.py');
    const 选项 = { encoding: 'utf8', timeout: 10000, windowsHide: true };
    cp.execFile(设.解释器, [桥, 文档.uri.fsPath], 选项, function (错, 出) {
        let 数据 = null;
        try { 数据 = JSON.parse(出 || '{}'); } catch (e) { 数据 = null; }
        if (!数据 || !Array.isArray(数据.diagnostics)) {
            if (错) {
                const 范 = new vscode.Range(new vscode.Position(0, 0), new vscode.Position(0, 1));
                const 一条 = new vscode.Diagnostic(范, 'ChinesePython 诊断桥跑不起来：' + String(错.message || 错), vscode.DiagnosticSeverity.Warning);
                一条.source = 'ChinesePython';
                集合.set(文档.uri, [一条]);
            }
            return;
        }
        const 诊断们 = 数据.diagnostics.map(function (项) {
            const 行 = Math.max(0, (项.line || 1) - 1);
            const 列 = Math.max(0, (项.column || 1) - 1);
            const 末列 = Math.max(列 + 1, (项.endColumn || 列 + 2));
            const 范围 = new vscode.Range(new vscode.Position(行, 列), new vscode.Position(行, 末列));
            const 一条 = new vscode.Diagnostic(范围, 项.message || '语法错误', vscode.DiagnosticSeverity.Error);
            一条.source = 'ChinesePython';
            if (项.kind) { 一条.code = 项.kind; }
            return 一条;
        });
        集合.set(文档.uri, 诊断们);
    });
}

function 稍后(文档) {
    const 键 = 文档.uri.toString();
    if (定时.has(键)) { clearTimeout(定时.get(键)); }
    定时.set(键, setTimeout(function () { 定时.delete(键); 诊断文档(文档); }, 400));
}

function activate(上下文) {
    集合 = vscode.languages.createDiagnosticCollection('chinesepython');
    上下文.subscriptions.push(集合);
    上下文.subscriptions.push(vscode.workspace.onDidOpenTextDocument(诊断文档));
    上下文.subscriptions.push(vscode.workspace.onDidSaveTextDocument(诊断文档));
    上下文.subscriptions.push(vscode.workspace.onDidChangeTextDocument(function (事) { 稍后(事.document); }));
    上下文.subscriptions.push(vscode.workspace.onDidCloseTextDocument(function (文档) { if (集合) { 集合.delete(文档.uri); } }));
    vscode.workspace.textDocuments.forEach(诊断文档);
}

module.exports = { activate: activate };
