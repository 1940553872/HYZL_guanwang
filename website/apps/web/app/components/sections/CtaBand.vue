<script setup lang="ts">
// 页面底部转化条（全站统一：预约现场演示 + 热线）
withDefaults(defineProps<{ title?: string; text?: string; to?: string; label?: string }>(), {
  title: '带一个现场问题来，我们用智能体给出答案。',
  text: '工程师 1 个工作日内与您联系，可安排线上交流或现场演示。',
  to: '/demo',
  label: '预约现场演示',
})
const { public: pub } = useRuntimeConfig()
</script>

<template>
  <section class="on-dark relative overflow-hidden bg-navy-900 text-on-dark">
    <HeroGrid class="pointer-events-none absolute inset-0 opacity-40" />
    <div class="container-site relative flex flex-col gap-8 py-16 md:flex-row md:items-center md:justify-between md:py-20">
      <div class="max-w-2xl">
        <h2 class="text-2xl text-white md:text-[32px] md:leading-[44px]">{{ title }}</h2>
        <p class="mt-3 text-on-dark-muted">{{ text }}</p>
      </div>
      <div class="flex flex-wrap items-center gap-4">
        <UiButton :to="to" variant="ondark" size="lg" arrow>{{ label }}</UiButton>
        <a :href="`tel:${pub.hotline}`" class="inline-flex items-center gap-2 text-on-dark hover:text-white">
          <UiIcon name="phone" :size="18" /><span class="font-latin text-lg font-semibold">{{ pub.hotline }}</span>
        </a>
      </div>
    </div>
  </section>
</template>
