// v-reveal：元素进入视口时渐显（K-01 §2.6 motion.slow）。服务端渲染时不加类，避免无 JS 时内容不可见。
export default defineNuxtPlugin((nuxtApp) => {
  let observer: IntersectionObserver | null = null
  const getObserver = () => {
    if (observer) return observer
    observer = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible')
          observer?.unobserve(e.target)
        }
      }
    }, { rootMargin: '0px 0px -8% 0px' })
    return observer
  }
  nuxtApp.vueApp.directive('reveal', {
    getSSRProps: () => ({}),
    mounted(el: HTMLElement) {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
      const rect = el.getBoundingClientRect()
      if (rect.top < window.innerHeight) return // 首屏内元素不做动画，避免闪烁与 CLS
      el.classList.add('reveal')
      getObserver().observe(el)
    },
  })
})
