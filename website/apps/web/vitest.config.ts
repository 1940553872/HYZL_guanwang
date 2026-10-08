import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vitest/config'

// 纯函数单元测试（utils），不启动 Nuxt
export default defineConfig({
  resolve: { alias: { '~': fileURLToPath(new URL('./app', import.meta.url)) } },
  test: { include: ['tests/unit/**/*.test.ts'], environment: 'node' },
})
