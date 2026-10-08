#!/usr/bin/env bash
# 一键启动华云智联官网（等同 ./hyzl.sh start）；加 --rebuild 强制重新构建
exec "$(dirname "${BASH_SOURCE[0]}")/hyzl.sh" start "$@"
