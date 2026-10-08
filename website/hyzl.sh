#!/usr/bin/env bash
# 华云智联官网 V2.0 —— 本地一键启停脚本（Linux / macOS）
#
#   ./hyzl.sh start [--rebuild]   构建（首次或 --rebuild）并后台启动 API(8080) + 网站(3000)
#   ./hyzl.sh stop                停止两个服务
#   ./hyzl.sh restart [--rebuild] 先停止再启动
#   ./hyzl.sh status              查看运行状态
#   ./hyzl.sh logs [api|web]      跟踪日志
#
# 可用环境变量：WEB_PORT（默认 3000）、API_PORT（默认 8080）、HYZL_HOST（网站监听地址，默认 127.0.0.1，
# 局域网演示可设为 0.0.0.0）、HYZL_ADMIN_TOKEN（启用线索管理接口）、HYZL_DATA_DIR（数据目录，默认 ./data）。
# 详见 docs/本地部署说明.md。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_DIR="$ROOT/.run"
LOG_DIR="$RUN_DIR/logs"
API_DIR="$ROOT/apps/api"
WEB_DIR="$ROOT/apps/web"
API_JAR="$API_DIR/target/hyzl-api.jar"
WEB_ENTRY="$WEB_DIR/.output/server/index.mjs"

WEB_PORT="${WEB_PORT:-3000}"
API_PORT="${API_PORT:-8080}"
HYZL_HOST="${HYZL_HOST:-127.0.0.1}"
HYZL_DATA_DIR="${HYZL_DATA_DIR:-$ROOT/data}"

c_ok=$'\033[32m'; c_warn=$'\033[33m'; c_err=$'\033[31m'; c_off=$'\033[0m'
info() { printf '%s\n' "› $*"; }
ok()   { printf '%s\n' "${c_ok}✔${c_off} $*"; }
warn() { printf '%s\n' "${c_warn}!${c_off} $*"; }
die()  { printf '%s\n' "${c_err}✘ $*${c_off}" >&2; exit 1; }

pid_of() { [[ -f "$RUN_DIR/$1.pid" ]] && cat "$RUN_DIR/$1.pid" || true; }
alive()  { local p; p="$(pid_of "$1")"; [[ -n "$p" ]] && kill -0 "$p" 2>/dev/null; }

port_busy() {
  if command -v lsof >/dev/null 2>&1; then lsof -iTCP:"$1" -sTCP:LISTEN -t >/dev/null 2>&1
  elif command -v ss >/dev/null 2>&1; then ss -ltn "( sport = :$1 )" 2>/dev/null | grep -q ":$1"
  else (exec 3<>"/dev/tcp/127.0.0.1/$1") 2>/dev/null
  fi
}

wait_http() { # url seconds name
  local i
  for ((i = 0; i < $2; i++)); do
    if curl -fsS -o /dev/null "$1" 2>/dev/null; then return 0; fi
    sleep 1
  done
  return 1
}

check_env() {
  command -v curl >/dev/null || die "未找到 curl，请先安装。"
  command -v java >/dev/null || die "未找到 Java。请安装 JDK 21 或更高版本（如 Eclipse Temurin 21）。"
  local jv
  jv="$(java -XshowSettings:properties -version 2>&1 | awk -F'= ' '/java.specification.version/ {print $2}' | tr -d '[:space:]')"
  [[ "${jv%%.*}" -ge 21 ]] 2>/dev/null || die "Java 版本为 ${jv:-未知}，需要 21 或更高版本。"
  command -v node >/dev/null || die "未找到 Node.js。请安装 Node.js 20.19 或更高版本（推荐 22 LTS）。"
  local nv; nv="$(node -p 'process.versions.node')"
  local major="${nv%%.*}" minor; minor="$(echo "$nv" | cut -d. -f2)"
  if (( major < 20 || (major == 20 && minor < 19) )); then die "Node.js 版本为 $nv，需要 20.19 或更高版本。"; fi
  local patch; patch="$(echo "$nv" | cut -d. -f3)"
  # Nuxt 4.6 官方支持范围：^22.22.3 || ^24.15.0 || >=26
  if ! (( (major == 22 && (minor > 22 || (minor == 22 && patch >= 3))) || (major == 24 && minor >= 15) || major >= 26 )); then
    warn "Node.js $nv 不在 Nuxt 4.6 官方支持范围内（22.22.3+ / 24.15+ / 26+），建议升级到最新 22 LTS 或 24 LTS。"
  fi
  command -v npm >/dev/null || die "未找到 npm。"
  ok "环境检查通过：Java $jv，Node.js $nv"
}

build() {
  local force="${1:-}"
  if [[ "$force" == "--rebuild" || ! -f "$API_JAR" ]]; then
    info "构建内容服务（Spring Boot，首次需下载依赖，约 2–5 分钟）…"
    (cd "$API_DIR" && ./mvnw -q -DskipTests package) || die "API 构建失败，详见上方输出。"
    ok "API 构建完成：apps/api/target/hyzl-api.jar"
  fi
  if [[ "$force" == "--rebuild" || ! -d "$WEB_DIR/node_modules" ]]; then
    info "安装前端依赖（npm ci）…"
    (cd "$WEB_DIR" && npm ci --no-audit --no-fund) || die "npm 依赖安装失败。"
  fi
  if [[ "$force" == "--rebuild" || ! -f "$WEB_ENTRY" ]]; then
    info "构建网站（Nuxt，约 30 秒）…"
    (cd "$WEB_DIR" && npm run build >"$LOG_DIR/web-build.log" 2>&1) || die "网站构建失败，日志：$LOG_DIR/web-build.log"
    ok "网站构建完成：apps/web/.output"
  fi
}

start() {
  mkdir -p "$LOG_DIR" "$HYZL_DATA_DIR"
  if alive api && alive web; then
    ok "服务已在运行：http://localhost:$WEB_PORT"; return 0
  fi
  check_env
  build "${1:-}"

  if ! alive api; then
    port_busy "$API_PORT" && die "端口 $API_PORT 已被占用。可用 API_PORT=8081 ./hyzl.sh start 更换端口。"
    info "启动内容服务（端口 $API_PORT）…"
    PORT="$API_PORT" SERVER_ADDRESS=127.0.0.1 HYZL_DATA_DIR="$HYZL_DATA_DIR" \
      HYZL_CORS_ORIGINS="http://localhost:$WEB_PORT" \
      nohup java -Xms128m -Xmx512m -jar "$API_JAR" >"$LOG_DIR/api.log" 2>&1 &
    echo $! >"$RUN_DIR/api.pid"
    if ! wait_http "http://127.0.0.1:$API_PORT/actuator/health" 120; then
      tail -n 30 "$LOG_DIR/api.log" >&2 || true
      stop_one api
      die "内容服务启动超时，完整日志：$LOG_DIR/api.log"
    fi
    ok "内容服务已启动（PID $(pid_of api)）"
  fi

  if ! alive web; then
    port_busy "$WEB_PORT" && { stop_one api; die "端口 $WEB_PORT 已被占用。可用 WEB_PORT=3001 ./hyzl.sh start 更换端口。"; }
    info "启动网站（端口 $WEB_PORT）…"
    PORT="$WEB_PORT" HOST="$HYZL_HOST" NUXT_API_BASE="http://127.0.0.1:$API_PORT" \
      NUXT_PUBLIC_SITE_URL="${NUXT_PUBLIC_SITE_URL:-http://localhost:$WEB_PORT}" NODE_ENV=production \
      nohup node "$WEB_ENTRY" >"$LOG_DIR/web.log" 2>&1 &
    echo $! >"$RUN_DIR/web.pid"
    if ! wait_http "http://127.0.0.1:$WEB_PORT/api/health" 60; then
      tail -n 30 "$LOG_DIR/web.log" >&2 || true
      die "网站启动超时，完整日志：$LOG_DIR/web.log"
    fi
    ok "网站已启动（PID $(pid_of web)）"
  fi

  echo
  ok "华云智联官网已运行：${c_ok}http://localhost:$WEB_PORT${c_off}"
  info "接口文档：http://127.0.0.1:$API_PORT/api/v1/docs    日志目录：$LOG_DIR"
  [[ -n "${HYZL_ADMIN_TOKEN:-}" ]] && info "线索管理接口已启用：GET http://127.0.0.1:$API_PORT/admin/v1/leads（Bearer Token）"
  info "停止服务：./hyzl.sh stop"
}

stop_one() {
  local name="$1" p
  p="$(pid_of "$name")"
  if [[ -n "$p" ]] && kill -0 "$p" 2>/dev/null; then
    kill "$p" 2>/dev/null || true
    for _ in $(seq 1 20); do kill -0 "$p" 2>/dev/null || break; sleep 0.5; done
    kill -0 "$p" 2>/dev/null && kill -9 "$p" 2>/dev/null || true
    ok "已停止 $name（PID $p）"
  else
    info "$name 未在运行"
  fi
  rm -f "$RUN_DIR/$name.pid"
}

stop() { stop_one web; stop_one api; }

status() {
  local name url
  for name in api web; do
    if alive "$name"; then
      [[ "$name" == api ]] && url="http://127.0.0.1:$API_PORT/actuator/health" || url="http://127.0.0.1:$WEB_PORT/api/health"
      if curl -fsS -o /dev/null "$url" 2>/dev/null; then ok "$name 运行中（PID $(pid_of "$name")），健康检查通过"
      else warn "$name 进程存在（PID $(pid_of "$name")），但健康检查未通过"; fi
    else
      info "$name 未运行"
    fi
  done
}

logs() {
  local f="$LOG_DIR/${1:-web}.log"
  [[ -f "$f" ]] || die "暂无日志：$f"
  tail -n 100 -f "$f"
}

case "${1:-}" in
  start)   start "${2:-}" ;;
  stop)    stop ;;
  restart) stop; start "${2:-}" ;;
  status)  status ;;
  logs)    logs "${2:-web}" ;;
  *) sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
