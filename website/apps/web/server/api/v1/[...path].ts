// 将浏览器与 SSR 对 /api/v1/** 的请求代理到内容与业务服务（K-04 §2.2、K-05 §2）
export default defineEventHandler(async (event) => {
  const { apiBase } = useRuntimeConfig(event)
  const path = getRouterParam(event, 'path') || ''
  const query = getRequestURL(event).search
  return proxyRequest(event, `${apiBase}/api/v1/${path}${query}`, {
    headers: { 'x-forwarded-for': getRequestIP(event, { xForwardedFor: true }) || '' },
  })
})
