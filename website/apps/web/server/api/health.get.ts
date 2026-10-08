// 健康检查：返回前端版本与内容服务连通性（K-04 §6.3）
export default defineEventHandler(async (event) => {
  const { apiBase } = useRuntimeConfig(event)
  let api = 'DOWN'
  try {
    const r = await $fetch<{ status: string }>(`${apiBase}/actuator/health`, { timeout: 2000 })
    api = r.status
  } catch {
    api = 'DOWN'
  }
  setResponseStatus(event, api === 'UP' ? 200 : 503)
  return { status: api === 'UP' ? 'ok' : 'degraded', web: 'UP', api, version: '2.0.0' }
})
