# 安装/卸载（install.ps1）：把**解释器所在目录**加进当前用户 PATH，不改系统 PATH。
#
# ⚠ 两种布局都要认（D-188）：
#   * 发布仓布局：本脚本在根、`python.exe` 在 `bin\`  ⇒ 加 `<根>\bin`；
#   * 绿色目录 / zip 布局：`python.exe` 就在本脚本旁边 ⇒ 加 `<根>` 本身。
#   （D-186 把本脚本也放进了 zip，但它当时写死 `bin\` ⇒ 绿色目录会加一个**不存在**的目录。）
param([switch]$卸载, [switch]$检查)
$ErrorActionPreference = 'Stop'
$bin = (Join-Path $PSScriptRoot 'bin')
if (-not (Test-Path (Join-Path $bin 'python.exe'))) { $bin = $PSScriptRoot }
$bin = $bin.TrimEnd('\')
if ($检查) {
    $有解释器 = Test-Path (Join-Path $bin 'python.exe')
    Write-Host ('install.ps1 会加的目录：' + $bin)
    if ($有解释器) { Write-Host '布局对得上 OK' } else { Write-Host '[!!] 那儿没有 python.exe —— 布局不对' }
    exit $(if ($有解释器) { 0 } else { 1 })
}
$项 = @([Environment]::GetEnvironmentVariable('Path', 'User') -split ';' | Where-Object { $_.Trim() -ne '' })
$有 = $项 | Where-Object { $_.TrimEnd('\') -ieq $bin }
if ($卸载) {
    if ($有) {
        [Environment]::SetEnvironmentVariable('Path', (($项 | Where-Object { $_.TrimEnd('\') -ine $bin }) -join ';'), 'User')
        Write-Host "已从用户 PATH 移除：$bin"
    } else { Write-Host "用户 PATH 里本来就没有：$bin" }
} else {
    if ($有) { Write-Host "用户 PATH 里已有：$bin" }
    else {
        [Environment]::SetEnvironmentVariable('Path', (($项 + $bin) -join ';'), 'User')
        Write-Host "已把解释器目录加进用户 PATH：$bin"
    }
    Write-Host '请**新开**一个命令行窗口，然后敲 python 进中文 REPL。'
    Write-Host "（不改 PATH 的用法：$bin\python.exe 脚本.py）"
}