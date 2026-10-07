# 一键装配到我的 VS Code（D-196）—— 语义 = **从当前源重打 + 装 + 可一键还原**。
#
#   pwsh -File editors/attach-to-vscode.ps1                       # 装到当前目录（默认）
#   pwsh -File editors/attach-to-vscode.ps1 -工作区 D:/我的项目     # 装到别处
#   pwsh -File editors/attach-to-vscode.ps1 -解释器 <python.exe>    # 明说用哪个解释器
#   pwsh -File editors/attach-to-vscode.ps1 -不装扩展               # 只写 .vscode/ 配置
#
# 为什么是「重打 + 装」而不是「装附件里那个 VSIX」：有版本号、没构建身份的东西一定会漂
#   （D-193 的教训：源改过、包还是旧的，光看版本号看不出来）。
param(
    [string]$工作区 = (Get-Location).Path,
    [string]$解释器 = '',
    [switch]$不装扩展
)
$ErrorActionPreference = 'Stop'
$套件夹 = $PSScriptRoot
$根 = Split-Path $套件夹 -Parent
$模板夹 = Join-Path $套件夹 'vscode-kit'

function 找解释器 {
    if ($解释器) {
        if (-not (Test-Path -LiteralPath $解释器)) { throw ('指定的解释器不存在：' + $解释器) }
        return (Get-Item -LiteralPath $解释器).FullName
    }
    foreach ($名 in 'CHINESEPYTHON_PYTHON', 'CHINESEPYTHON_HOME') {
        $值 = [Environment]::GetEnvironmentVariable($名)
        if ($值) {
            $路 = if ($值 -like '*.exe') { $值 } else { Join-Path $值 'python.exe' }
            if (Test-Path -LiteralPath $路) { return (Get-Item -LiteralPath $路).FullName }
        }
    }
    $候选 = @((Join-Path $env:LOCALAPPDATA 'Programs/ChinesePython/python.exe'))
    Get-ChildItem (Join-Path $env:LOCALAPPDATA 'ChinesePython') -Directory -Filter 'runtime-*' -ErrorAction SilentlyContinue |
        Sort-Object Name -Descending | ForEach-Object { $候选 += (Join-Path $_.FullName 'python.exe') }
    foreach ($路 in $候选) { if (Test-Path -LiteralPath $路) { return (Get-Item -LiteralPath $路).FullName } }
    $在路 = Get-Command python -ErrorAction SilentlyContinue
    if ($在路) { return $在路.Source }
    throw '找不到 ChinesePython 的 python.exe —— 用 -解释器 <路径> 明说一个。'
}

$py = 找解释器
if (-not (Test-Path -LiteralPath $工作区)) { throw ('工作区不存在：' + $工作区) }
$工作区 = (Get-Item -LiteralPath $工作区).FullName
$点 = Join-Path $工作区 '.vscode'
$备份夹 = Join-Path $点 '.chinesepython备份'
New-Item -ItemType Directory -Force $点 | Out-Null
Write-Host ('解释器：' + $py)
Write-Host ('工作区：' + $工作区)

if (-not $不装扩展) {
    Write-Host '1) 从当前源重打 VSIX'
    pwsh -NoProfile -File (Join-Path $根 'tools/打包编辑器扩展.ps1') | Select-Object -Last 2
    if ($LASTEXITCODE -ne 0) { throw '打包编辑器扩展 失败' }
    if (-not (Get-Command code -ErrorAction SilentlyContinue)) {
        throw 'PATH 里没有 code —— 在 VS Code 里按 Ctrl+Shift+P 跑「Shell Command: Install code command in PATH」'
    }
    Write-Host '2) 装扩展（--force 覆盖旧那份）'
    $vsix = Get-ChildItem (Join-Path $根 'editors/dist') -Filter *.vsix | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if (-not $vsix) { throw '没找到 editors/dist/*.vsix —— 打包那步没成功？' }
    & code --install-extension $vsix.FullName --force | Select-Object -Last 1
    if ($LASTEXITCODE -ne 0) { throw '装扩展失败' }
}

Write-Host '3) 抄 .vscode/ 三个配置（同名先备份到 .vscode/.chinesepython备份/）'
$斜 = [string][char]92
foreach ($名 in 'settings.json', 'tasks.json', 'launch.json') {
    $目标 = Join-Path $点 $名
    if (Test-Path -LiteralPath $目标) {
        New-Item -ItemType Directory -Force $备份夹 | Out-Null
        Copy-Item -LiteralPath $目标 -Destination (Join-Path $备份夹 $名) -Force
    }
    $文 = Get-Content -LiteralPath (Join-Path $模板夹 $名) -Raw -Encoding UTF8
    $文 = $文.Replace('__CHINESEPYTHON_PYTHON__', $py.Replace($斜, ($斜 + $斜)))
    [IO.File]::WriteAllText($目标, $文, (New-Object Text.UTF8Encoding $false))
    Write-Host ('   ' + $名)
}
$示例 = Join-Path $工作区 '中文示例.py'
if (-not (Test-Path -LiteralPath $示例)) { Copy-Item -LiteralPath (Join-Path $模板夹 '中文示例.py') $示例; Write-Host '   中文示例.py' }
Write-Host ''
Write-Host '装配完成。接下来：'
Write-Host '  * 打开 中文示例.py —— F5 调试，或 Ctrl+Shift+P → Run Task → ChinesePython：跑当前文件'
Write-Host '  * 把某行的右括号删掉：红波浪线应当落在**我们报的那一行**（诊断桥），中文行**不再**被误红'
Write-Host ('还原：pwsh -NoProfile -File "' + (Join-Path $套件夹 'detach-from-vscode.ps1') + '" -工作区 "' + $工作区 + '"')
exit 0