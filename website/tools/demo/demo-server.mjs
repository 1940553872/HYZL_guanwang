// 华云智联官网 · 静态演示包本地服务器（无依赖，只需 Node.js 18+）
// 用法：node demo-server.mjs [端口]，默认 3000；被占用时自动换下一个端口，并自动打开浏览器
import { createReadStream, existsSync, statSync } from 'node:fs'
import { createServer } from 'node:http'
import { extname, join, normalize } from 'node:path'
import { exec } from 'node:child_process'

const root = join(import.meta.dirname, 'site')
const TYPES = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.webp': 'image/webp', '.ico': 'image/x-icon', '.woff': 'font/woff', '.woff2': 'font/woff2',
}

function resolveFile(urlPath) {
  const clean = normalize(decodeURIComponent(urlPath.split('?')[0])).replace(/^([/\\])+/, '')
  if (clean.startsWith('..')) return null
  const base = join(root, clean)
  for (const f of [base, join(base, 'index.html'), `${base}.html`]) {
    if (existsSync(f) && statSync(f).isFile()) return f
  }
  return null
}

const server = createServer((req, res) => {
  const file = resolveFile(req.url || '/')
  const target = file || join(root, '404.html')
  res.writeHead(file ? 200 : 404, { 'content-type': TYPES[extname(target)] || 'application/octet-stream' })
  createReadStream(target).pipe(res)
})

let port = Number(process.argv[2] || 3000)
server.on('error', (e) => {
  if (e.code === 'EADDRINUSE' && port < 3010) { port++; server.listen(port, '127.0.0.1') } else { console.error(e.message); process.exit(1) }
})
server.on('listening', () => {
  const url = `http://localhost:${port}`
  console.log(`\n  华云智联官网演示已启动：${url}\n  关闭本窗口即可停止。\n`)
  const open = process.platform === 'win32' ? `start "" "${url}"` : process.platform === 'darwin' ? `open ${url}` : `xdg-open ${url}`
  if (!process.env.NO_OPEN) exec(open, () => {})
})
server.listen(port, '127.0.0.1')
