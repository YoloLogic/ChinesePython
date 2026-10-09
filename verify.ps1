# 发行包自检（verify.ps1）：用**包内**解释器验 **17 项** —— 中文标准库 / 中文关键字 / 中文报错显示层 /
# 英文还原开关 / pip / 图形界面运行时（Tcl/Tk 9）/ 官方英文文档副本 / 一键安装脚本布局 / VS Code 一键装配 kit /
# **七份许可与披露文件**（LICENSE / LICENSE.txt / NOTICE.txt / LICENSE-SCOPE.md / TRADEMARK.md /
# LICENSE-第三方.txt / LICENSE-TCL-TK.txt）。D-212、D-220、D-223
# 自检项数：17   ← 这个数字必须与下面真正的检查点个数、以及 发布说明-v0.1.md 里写的数字一致
#             （由 tests\许可条款冒烟.py 的「数字对拍」守住；改这里就要改那里）
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
function 查文件($名, $相对) {
    if (Test-Path (Join-Path $PSScriptRoot $相对)) { Write-Host ("  [OK] " + $名) }
    else { Write-Host ("  [!!] " + $名 + " 缺失：" + $相对); $script:坏++ }
}
function 查有文件($名, $目录, $通配) {
    $有 = Get-ChildItem (Join-Path $PSScriptRoot $目录) -Filter $通配 -ErrorAction SilentlyContinue
    if ($有) { Write-Host ("  [OK] " + $名) }
    else { Write-Host ("  [!!] " + $名 + " 缺失：" + $目录 + "\" + $通配); $script:坏++ }
}
function 查脚本($名, $相对) {
    $p = Join-Path $PSScriptRoot $相对
    if (-not (Test-Path $p)) { Write-Host ("  [!!] 缺少 " + $相对); $script:坏++; return }
    $壳 = if (Get-Command pwsh -ErrorAction SilentlyContinue) { 'pwsh' } else { 'powershell' }
    $o = & $壳 -NoProfile -ExecutionPolicy Bypass -File $p -检查 2>&1 | Out-String
    if ($LASTEXITCODE -eq 0) { Write-Host ("  [OK] " + $名) }
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

# Tcl/Tk 9（D-220）：包里必须带着 tcl90.dll + tcl9tk90.dll；Tcl 9 把脚本库编进 DLL，
# 所以**不需要 tcl\ 目录、也不需要 TCL_LIBRARY**（实测 TCL_LIBRARY=None 照样跑）。
查 '图形界面运行时（Tcl/Tk 9：tkinter 能建解释器）' '导入 tkinter; 打印(tkinter.Tcl().eval("info patchlevel"))'
查文件 '官方英文文档副本（Doc\html，含中文入口页）' 'Doc\html\中文入口.html'
查脚本 '一键安装脚本（目录与解释器对得上）' 'install.ps1'
查文件 'VS Code 一键装配 kit（editors\vscode-kit\settings.json）' 'editors\vscode-kit\settings.json'
查有文件 'VS Code 扩展 VSIX（editors\dist\*.vsix）' 'editors\dist' '*.vsix'

# 许可与披露（D-223）：**逐份点名**，少一份就红 —— 这些是发行包里必须随附的文件
查文件 '许可：LICENSE（本项目自定义条款，禁止再发布）' 'LICENSE'
查文件 '上游许可：LICENSE.txt（PSF，逐字节未改）' 'LICENSE.txt'
查文件 '第三方披露：NOTICE.txt' 'NOTICE.txt'
查文件 '许可范围说明：LICENSE-SCOPE.md' 'LICENSE-SCOPE.md'
查文件 '名称与图标条款：TRADEMARK.md' 'TRADEMARK.md'
查文件 '第三方许可正文：LICENSE-第三方.txt（含 OpenSSL / libffi / zlib …）' 'LICENSE-第三方.txt'
查文件 'Tcl/Tk 许可正文：LICENSE-TCL-TK.txt' 'LICENSE-TCL-TK.txt'

if ($坏 -eq 0) { Write-Host '全部通过 OK' } else { Write-Host ($坏.ToString() + ' 项未通过') }
exit $坏
