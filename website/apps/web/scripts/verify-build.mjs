// 构建后自检：确认服务端包里含有客户端资源清单（precomputed）。
// 清单为空时站点能启动，但每个页面都会返回 500（"Either manifest or precomputed data must be provided"），
// 因此在构建阶段就失败并给出明确提示。
import { existsSync, readdirSync, readFileSync } from 'node:fs'
import { join } from 'node:path'

const dir = join(import.meta.dirname, '..', '.output', 'server', 'chunks', 'virtual')
const file = existsSync(dir) ? readdirSync(dir).find((f) => f.startsWith('precomputed') && f.endsWith('.mjs')) : undefined
const code = file ? readFileSync(join(dir, file), 'utf8') : ''

if (!code.includes('dependencies')) {
  console.error('\n[verify-build] 构建产物缺少客户端资源清单（.output/server/chunks/virtual/precomputed.mjs），网站将无法渲染页面。')
  console.error('[verify-build] 请删除 apps/web/.nuxt 与 apps/web/.output 后重新构建；若仍失败，请升级 Node.js 到 22.22.3+ / 24.15+。\n')
  process.exit(1)
}
console.log('[verify-build] 构建产物自检通过')
