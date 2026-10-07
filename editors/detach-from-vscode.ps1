# 一键还原（D-196）：把 attach-to-vscode.ps1 做的事退回去。
#
#   pwsh -File editors/detach-from-vscode.ps1 [-工作区 <路径>] [-卸扩展]
#
# 规则：**有备份就还原备份，没备份就删掉我们写的那个文件**（绝不留下半个状态）。
param([string]$工作区 = (Get-Location).Path, [switch]$卸扩展)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $工作区)) { throw ('工作区不存在：' + $工作区) }
$工作区 = (Get-Item -LiteralPath $工作区).FullName
$点 = Join-Path $工作区 '.vscode'
$备份夹 = Join-Path $点 '.chinesepython备份'
$退了几 = 0
foreach ($名 in 'settings.json', 'tasks.json', 'launch.json') {
    $目标 = Join-Path $点 $名
    $备份 = Join-Path $备份夹 $名
    if (Test-Path -LiteralPath $备份) {
        Copy-Item -LiteralPath $备份 -Destination $目标 -Force
        Remove-Item -LiteralPath $备份 -Force
        Write-Host (' 还原了 ' + $名)
        $退了几++
    } elseif (Test-Path -LiteralPath $目标) {
        Remove-Item -LiteralPath $目标 -Force
        Write-Host (' 删掉了 ' + $名 + '（本来没有备份）')
        $退了几++
    }
}
if (Test-Path -LiteralPath $备份夹) {
    $剩 = Get-ChildItem -LiteralPath $备份夹 -Force -ErrorAction SilentlyContinue
    if (-not $剩) { Remove-Item -LiteralPath $备份夹 -Recurse -Force }
}
if ($卸扩展) {
    if (Get-Command code -ErrorAction SilentlyContinue) {
        & code --uninstall-extension yolologic.chinesepython 2>&1 | Select-Object -Last 1
        Write-Host ' 卸了扩展 yolologic.chinesepython'
    } else { Write-Host ' PATH 里没有 code —— 扩展没卸（在 VS Code 扩展面板手动卸）' }
}
Write-Host ('还原完成（动了 ' + $退了几 + ' 个文件）。示例文件 中文示例.py 留给你自己删。')
exit 0