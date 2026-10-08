# 华云智联官网 V2.0 —— 本地一键启停脚本（Windows PowerShell 5.1+ / PowerShell 7）
#   powershell -ExecutionPolicy Bypass -File hyzl.ps1 start [-Rebuild]
#   powershell -ExecutionPolicy Bypass -File hyzl.ps1 stop | status
# 环境变量与 hyzl.sh 一致：WEB_PORT、API_PORT、HYZL_HOST、HYZL_ADMIN_TOKEN、HYZL_DATA_DIR
param(
  [Parameter(Position = 0)][ValidateSet('start', 'stop', 'restart', 'status')][string]$Command = 'start',
  [switch]$Rebuild
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$RunDir = Join-Path $Root '.run'
$LogDir = Join-Path $RunDir 'logs'
$ApiDir = Join-Path $Root 'apps\api'
$WebDir = Join-Path $Root 'apps\web'
$ApiJar = Join-Path $ApiDir 'target\hyzl-api.jar'
$WebEntry = Join-Path $WebDir '.output\server\index.mjs'
$WebPort = if ($env:WEB_PORT) { $env:WEB_PORT } else { '3000' }
$ApiPort = if ($env:API_PORT) { $env:API_PORT } else { '8080' }
$HostAddr = if ($env:HYZL_HOST) { $env:HYZL_HOST } else { '127.0.0.1' }
$DataDir = if ($env:HYZL_DATA_DIR) { $env:HYZL_DATA_DIR } else { Join-Path $Root 'data' }

function Ok($m) { Write-Host "[OK] $m" -ForegroundColor Green }
function Info($m) { Write-Host "  > $m" }
function Fail($m) { Write-Host "[X] $m" -ForegroundColor Red; exit 1 }

function Get-SavedPid($name) {
  $f = Join-Path $RunDir "$name.pid"
  if (Test-Path $f) { return [int](Get-Content $f -Raw).Trim() } else { return $null }
}
function Test-Alive($name) {
  $p = Get-SavedPid $name
  return ($p -and (Get-Process -Id $p -ErrorAction SilentlyContinue))
}
function Test-Port($port) {
  return [bool](Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue)
}
function Wait-Http($url, $seconds) {
  for ($i = 0; $i -lt $seconds; $i++) {
    try { Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2 | Out-Null; return $true } catch { Start-Sleep -Seconds 1 }
  }
  return $false
}

function Test-Env {
  if (-not (Get-Command java -ErrorAction SilentlyContinue)) { Fail '未找到 Java，请安装 JDK 21 或更高版本。' }
  $props = & cmd /c "java -XshowSettings:properties -version 2>&1"
  $line = $props | Where-Object { $_ -match 'java.specification.version' } | Select-Object -First 1
  $jv = if ($line) { ($line -split '=')[1].Trim() } else { '0' }
  if ([int]($jv.Split('.')[0]) -lt 21) { Fail "Java 版本为 $jv，需要 21 或更高版本。" }
  if (-not (Get-Command node -ErrorAction SilentlyContinue)) { Fail '未找到 Node.js，请安装 20.19 或更高版本（推荐 22 LTS）。' }
  $nv = (& node -p 'process.versions.node').Trim()
  $parts = $nv.Split('.')
  if ([int]$parts[0] -lt 20 -or ([int]$parts[0] -eq 20 -and [int]$parts[1] -lt 19)) { Fail "Node.js 版本为 $nv，需要 20.19 或更高版本。" }
  Ok "环境检查通过：Java $jv，Node.js $nv"
}

function Invoke-Build {
  if ($Rebuild -or -not (Test-Path $ApiJar)) {
    Info '构建内容服务（首次需下载依赖，约 2–5 分钟）…'
    Push-Location $ApiDir; & .\mvnw.cmd -q -DskipTests package; $code = $LASTEXITCODE; Pop-Location
    if ($code -ne 0) { Fail 'API 构建失败。' }
  }
  if ($Rebuild -or -not (Test-Path (Join-Path $WebDir 'node_modules'))) {
    Info '安装前端依赖（npm ci）…'
    Push-Location $WebDir; & npm ci --no-audit --no-fund; $code = $LASTEXITCODE; Pop-Location
    if ($code -ne 0) { Fail 'npm 依赖安装失败。' }
  }
  if ($Rebuild -or -not (Test-Path $WebEntry)) {
    Info '构建网站（约 30 秒）…'
    Push-Location $WebDir; & npm run build *> (Join-Path $LogDir 'web-build.log'); $code = $LASTEXITCODE; Pop-Location
    if ($code -ne 0) { Fail "网站构建失败，日志：$LogDir\web-build.log" }
  }
}

function Start-Site {
  New-Item -ItemType Directory -Force -Path $LogDir, $DataDir | Out-Null
  if ((Test-Alive 'api') -and (Test-Alive 'web')) { Ok "服务已在运行：http://localhost:$WebPort"; return }
  Test-Env
  Invoke-Build
  if (-not (Test-Alive 'api')) {
    if (Test-Port $ApiPort) { Fail "端口 $ApiPort 已被占用，可设置环境变量 API_PORT 更换端口。" }
    Info "启动内容服务（端口 $ApiPort）…"
    $env:PORT = $ApiPort; $env:SERVER_ADDRESS = '127.0.0.1'; $env:HYZL_DATA_DIR = $DataDir
    $env:HYZL_CORS_ORIGINS = "http://localhost:$WebPort"
    $p = Start-Process -FilePath 'java' -ArgumentList '-Xms128m', '-Xmx512m', '-jar', "`"$ApiJar`"" -WindowStyle Hidden -PassThru `
      -RedirectStandardOutput (Join-Path $LogDir 'api.log') -RedirectStandardError (Join-Path $LogDir 'api.err.log')
    Set-Content -Path (Join-Path $RunDir 'api.pid') -Value $p.Id
    if (-not (Wait-Http "http://127.0.0.1:$ApiPort/actuator/health" 120)) { Stop-One 'api'; Fail "内容服务启动超时，日志：$LogDir\api.log" }
    Ok "内容服务已启动（PID $($p.Id)）"
  }
  if (-not (Test-Alive 'web')) {
    if (Test-Port $WebPort) { Fail "端口 $WebPort 已被占用，可设置环境变量 WEB_PORT 更换端口。" }
    Info "启动网站（端口 $WebPort）…"
    $env:PORT = $WebPort; $env:HOST = $HostAddr; $env:NUXT_API_BASE = "http://127.0.0.1:$ApiPort"
    if (-not $env:NUXT_PUBLIC_SITE_URL) { $env:NUXT_PUBLIC_SITE_URL = "http://localhost:$WebPort" }
    $env:NODE_ENV = 'production'
    $p = Start-Process -FilePath 'node' -ArgumentList "`"$WebEntry`"" -WindowStyle Hidden -PassThru `
      -RedirectStandardOutput (Join-Path $LogDir 'web.log') -RedirectStandardError (Join-Path $LogDir 'web.err.log')
    Set-Content -Path (Join-Path $RunDir 'web.pid') -Value $p.Id
    if (-not (Wait-Http "http://127.0.0.1:$WebPort/api/health" 60)) { Fail "网站启动超时，日志：$LogDir\web.log" }
    Ok "网站已启动（PID $($p.Id)）"
  }
  Ok "华云智联官网已运行：http://localhost:$WebPort"
  Info "接口文档：http://127.0.0.1:$ApiPort/api/v1/docs    日志目录：$LogDir"
  Info '停止服务：双击 stop.bat 或运行 hyzl.ps1 stop'
}

function Stop-One($name) {
  $p = Get-SavedPid $name
  if ($p -and (Get-Process -Id $p -ErrorAction SilentlyContinue)) {
    Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
    Ok "已停止 $name（PID $p）"
  } else { Info "$name 未在运行" }
  Remove-Item (Join-Path $RunDir "$name.pid") -ErrorAction SilentlyContinue
}

function Show-Status {
  foreach ($name in 'api', 'web') {
    if (Test-Alive $name) { Ok "$name 运行中（PID $(Get-SavedPid $name)）" } else { Info "$name 未运行" }
  }
}

switch ($Command) {
  'start' { Start-Site }
  'stop' { Stop-One 'web'; Stop-One 'api' }
  'restart' { Stop-One 'web'; Stop-One 'api'; Start-Site }
  'status' { Show-Status }
}
