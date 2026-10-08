<script setup lang="ts">
// 大数字：首次进入视口时计数一次（motion.count 1200ms），带脚注编号
const props = defineProps<{ stats: { value: string; label: string; note?: number }[]; dark?: boolean }>()
const root = ref<HTMLElement>()
const shown = ref(props.stats.map((s) => s.value))

function parts(v: string) {
  const m = v.match(/^([^\d]*)([\d.]+)(.*)$/)
  return m ? { pre: m[1], num: Number(m[2]), dec: (m[2].split('.')[1] || '').length, post: m[3] } : null
}

onMounted(() => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !root.value) return
  const obs = new IntersectionObserver((entries) => {
    if (!entries[0]?.isIntersecting) return
    obs.disconnect()
    const start = performance.now()
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / 1200)
      const k = 1 - Math.pow(1 - t, 3)
      shown.value = props.stats.map((s) => {
        const p = parts(s.value)
        return p ? `${p.pre}${(p.num * k).toFixed(p.dec)}${p.post}` : s.value
      })
      if (t < 1) requestAnimationFrame(tick)
    }
    requestAnimationFrame(tick)
  }, { threshold: 0.4 })
  obs.observe(root.value)
})
</script>

<template>
  <dl ref="root" class="grid grid-cols-2 gap-x-6 gap-y-8 md:grid-cols-4">
    <div v-for="(s, i) in stats" :key="s.label" :class="['border-l-2 pl-4', dark ? 'border-brand-orange-500' : 'border-brand-blue-700']">
      <dt class="sr-only">{{ s.label }}</dt>
      <dd :class="['stat-num text-[40px] leading-[48px] md:text-[56px] md:leading-[64px]', dark ? 'text-brand-orange-500' : 'text-brand-blue-700']"
          :aria-label="s.value">
        <span aria-hidden="true">{{ shown[i] }}</span>
      </dd>
      <dd :class="['mt-1 text-sm', dark ? 'text-on-dark-muted' : 'text-ink-600']">
        {{ s.label }}<sup v-if="s.note" class="ml-0.5"><a :href="`#fn-${s.note}`" class="link">{{ s.note }}</a></sup>
      </dd>
    </div>
  </dl>
</template>
