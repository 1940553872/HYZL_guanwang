#!/usr/bin/env bash
# 一键停止华云智联官网（等同 ./hyzl.sh stop）
exec "$(dirname "${BASH_SOURCE[0]}")/hyzl.sh" stop
