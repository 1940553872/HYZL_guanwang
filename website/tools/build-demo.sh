#!/usr/bin/env bash
# 生成静态演示包：dist/hyzl-website-demo.zip（解压后双击 open-demo.bat 即可浏览，无需 Java 与构建）
# 前提：已构建内容服务 jar（./hyzl.sh start 会自动构建）
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WEB="$ROOT/apps/web"
OUT="$ROOT/dist/hyzl-website-demo"
API_PORT="${API_PORT:-8080}"

started_api=""
if ! curl -fsS -o /dev/null "http://127.0.0.1:$API_PORT/actuator/health"; then
  echo "› 启动内容服务以读取内容…"
  PORT="$API_PORT" SERVER_ADDRESS=127.0.0.1 HYZL_DATA_DIR="$ROOT/data" java -jar "$ROOT/apps/api/target/hyzl-api.jar" >/dev/null 2>&1 &
  started_api=$!
  for _ in $(seq 1 90); do curl -fsS -o /dev/null "http://127.0.0.1:$API_PORT/actuator/health" && break; sleep 1; done
fi
trap '[[ -n "$started_api" ]] && kill "$started_api" 2>/dev/null || true' EXIT

echo "› 预渲染全部页面…"
(cd "$WEB" && rm -rf .output-demo && HYZL_STATIC_DEMO=1 NUXT_API_BASE="http://127.0.0.1:$API_PORT" npx nuxt generate)

rm -rf "$OUT" "$OUT.zip" && mkdir -p "$OUT"
cp -r "$WEB/.output-demo/public" "$OUT/site"
cp "$ROOT/tools/demo/demo-server.mjs" "$ROOT/tools/demo/open-demo.bat" "$ROOT/tools/demo/open-demo.sh" "$ROOT/tools/demo/README.txt" "$OUT/"
(cd "$ROOT/dist" && python3 -c "
import os, zipfile
with zipfile.ZipFile('hyzl-website-demo.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for d, _, fs in os.walk('hyzl-website-demo'):
        for f in fs:
            p = os.path.join(d, f)
            z.write(p, p)
")
echo "✔ 演示包：$OUT.zip（$(du -h "$OUT.zip" | cut -f1)），页面数：$(find "$OUT/site" -name index.html | wc -l)"
