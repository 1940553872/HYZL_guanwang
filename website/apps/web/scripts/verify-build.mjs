// 构建后自检：实际启动构建产物并请求首页，确认 Vue 渲染器可用。
// 渲染器缺少客户端资源清单时，所有页面都会返回 Nuxt 自带的 "500 undefined" 页
// （日志 "Either manifest or precomputed data must be provided"），这里在构建阶段就发现它。
// 不依赖产物文件名：不同平台上 Nitro 的分块方式不同（Windows 会把清单合并进 nitro.mjs）。
import { spawn } from 'node:child_process'
import { existsSync } from 'node:fs'
import { join } from 'node:path'

const entry = join(import.meta.dirname, '..', '.output', 'server', 'index.mjs')
const fail = (msg) => {
  console.error(`\n[verify-build] ${msg}`)
  console.error('[verify-build] 请删除 apps/web/.nuxt 与 apps/web/.output 后重新构建；仍失败请把 .run/logs/web-build.log 发给开发者。\n')
  process.exit(1)
}
if (!existsSync(entry)) fail('未找到构建产物 .output/server/index.mjs。')

const port = String(39000 + Math.floor(Math.random() * 900))
// 内容服务地址指向不存在的端口：页面会因取不到内容走到站点自己的错误页，但这仍然证明 Vue 渲染器可用
const child = spawn(process.execPath, [entry], {
  env: { ...process.env, PORT: port, HOST: '127.0.0.1', NITRO_HOST: '127.0.0.1', NUXT_API_BASE: 'http://127.0.0.1:9' },
  stdio: ['ignore', 'ignore', 'pipe'],
})
let stderr = ''
child.stderr.on('data', (d) => { stderr += d })

let html = ''
const deadline = Date.now() + 30_000
while (Date.now() < deadline) {
  try {
    const res = await fetch(`http://127.0.0.1:${port}/`)
    html = await res.text()
    break
  } catch {
    await new Promise((r) => setTimeout(r, 300))
  }
}
child.kill()

if (!html) fail('构建产物无法启动或 30 秒内无响应。')
// 只有 Vue 应用真正渲染时才会输出 id="__nuxt" 根节点；渲染器损坏时只有 Nuxt 内置的错误模板
if (!html.includes('id="__nuxt"') || stderr.includes('Either manifest or precomputed data')) {
  fail('构建产物无法渲染页面（缺少客户端资源清单）。')
}
console.log('[verify-build] 构建产物自检通过')
