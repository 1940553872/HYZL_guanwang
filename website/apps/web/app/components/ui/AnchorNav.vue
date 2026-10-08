<script setup lang="ts">
// 页内锚点子导航（吸顶，K-02 §2.1 / K-04 §2）
defineProps<{ items: { id: string; label: string }[] }>()
const active = ref('')
onMounted(() => {
  const obs = new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) active.value = e.target.id
  }, { rootMargin: '-40% 0px -55% 0px' })
  document.querySelectorAll('[data-anchor]').forEach((el) => obs.observe(el))
  onBeforeUnmount(() => obs.disconnect())
})
</script>

<template>
  <nav aria-label="本页导航" class="sticky top-[60px] z-30 border-b border-line-200 bg-white/95 backdrop-blur">
    <div class="container-site flex gap-6 overflow-x-auto text-sm whitespace-nowrap md:gap-8">
      <a v-for="it in items" :key="it.id" :href="`#${it.id}`"
         :class="['border-b-2 py-4 transition-colors', active === it.id ? 'border-brand-orange-500 text-ink-900' : 'border-transparent text-ink-500 hover:text-ink-900']">
        {{ it.label }}
      </a>
    </div>
  </nav>
</template>
