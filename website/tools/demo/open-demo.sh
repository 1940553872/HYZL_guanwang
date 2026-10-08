#!/usr/bin/env bash
# 打开华云智联官网静态演示（需要 Node.js 18+）
cd "$(dirname "$0")" && exec node demo-server.mjs "$@"
