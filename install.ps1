# 安装/卸载（install.ps1）：把 bin\ 加进**当前用户** PATH，不改系统 PATH
param([switch]$卸载)
$ErrorActionPreference = 'Stop'
$bin = (Join-Path $PSScriptRoot 'bin').TrimEnd('\')
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
        Write-Host "已把 bin\ 加进用户 PATH：$bin"
    }
    Write-Host '请**新开**一个命令行窗口，然后敲 python 进中文 REPL。'
    Write-Host "（不改 PATH 的用法：$bin\python.exe 脚本.py）"
}