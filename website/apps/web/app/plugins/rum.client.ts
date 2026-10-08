// 真实用户性能上报（K-04 §1 监控）：LCP / INP / CLS / TTFB 批量发送到 /api/v1/rum
import { onCLS, onINP, onLCP, onTTFB, type Metric } from 'web-vitals'

export default defineNuxtPlugin(() => {
  if (useRuntimeConfig().public.staticDemo) return // 静态演示包没有后端
  const queue: Record<string, unknown>[] = []
  const device = window.matchMedia('(max-width: 767px)').matches ? 'mobile' : 'desktop'
  const push = (m: Metric) => {
    queue.push({ name: m.name, value: Math.round(m.value * 1000) / 1000, rating: m.rating, path: location.pathname, device })
  }
  const flush = () => {
    if (!queue.length) return
    const body = JSON.stringify({ items: queue.splice(0, 20) })
    navigator.sendBeacon?.('/api/v1/rum', new Blob([body], { type: 'application/json' }))
  }
  onLCP(push)
  onINP(push)
  onCLS(push)
  onTTFB(push)
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') flush()
  })
})
