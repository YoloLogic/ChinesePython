# 发行包自检（verify.ps1）：用**包内**解释器验六项 —— 中文标准库 / 中文关键字 / 中文报错显示层 / 英文还原开关 / pip / 官方英文文档副本
$ErrorActionPreference = 'Continue'
$py = Join-Path $PSScriptRoot 'python.exe'
if (-not (Test-Path $py)) { $py = Join-Path $PSScriptRoot 'bin\python.exe' }
$坏 = 0
function 跑($码) {
    $t = Join-Path $env:TEMP ('cp自检-' + [guid]::NewGuid().ToString('N') + '.py')
    Set-Content -Path $t -Value $码 -Encoding UTF8
    $o = & $py $t 2>&1 | Out-String
    $script:末 = $LASTEXITCODE
    Remove-Item $t -Force -ErrorAction SilentlyContinue
    return $o
}
function 查($名, $码) {
    $o = 跑 $码
    if ($script:末 -eq 0 -and $o -notmatch 'Traceback') { Write-Host ("  [OK] " + $名) }
    else { Write-Host ("  [!!] " + $名 + "  ==> " + $o.Trim()); $script:坏++ }
}
function 查报错($名, $码, $应含, $应不含) {
    $o = 跑 $码
    if ($script:末 -ne 0 -and $o -match $应含 -and $o -notmatch $应不含) { Write-Host ("  [OK] " + $名) }
    else { Write-Host ("  [!!] " + $名 + "  ==> " + $o.Trim()); $script:坏++ }
}

Write-Host 'ChinesePython 自检'
查 '中文标准库' '导入 操作系统, 并行.futures; 打印(操作系统.取当前目录())'
查 '中文关键字' '定义 加(甲, 乙): 返回 甲 + 乙' + [char]10 + '打印(加(1, 2))'
查报错 '中文报错（显示层）' '1/0' '除零错误' 'ZeroDivisionError|Traceback'
$env:CHINESEPYTHON_ERRORS = 'en'
查报错 '英文还原（CHINESEPYTHON_ERRORS=en）' '1/0' 'ZeroDivisionError' '除零错误'
Remove-Item Env:CHINESEPYTHON_ERRORS -ErrorAction SilentlyContinue
查 'pip 开箱可用' 'import pip; print(pip.__version__)'

# 官方英文 HTML 文档副本（D-185）：有中文入口页就算在（正文是官方英文原文）
$文档入口 = Join-Path $PSScriptRoot 'Doc\html\中文入口.html'
if (Test-Path $文档入口) { Write-Host '  [OK] 官方英文文档副本（Doc\html，含中文入口页）' }
else { Write-Host '  [!!] 官方英文文档副本缺失（Doc\html\中文入口.html）'; $坏++ }

if ($坏 -eq 0) { Write-Host '全部通过 OK' } else { Write-Host ($坏.ToString() + ' 项未通过') }
exit $坏