<script setup lang="ts">
// 二级页面首屏：深海军蓝 + 面包屑 + 眉标 + H1 + 导语（K-01 §3）
defineProps<{
  title: string
  eyebrow?: string
  lead?: string
  crumbs: { name: string; to?: string }[]
  code?: string
}>()
</script>

<template>
  <section class="on-dark relative overflow-hidden bg-navy-900 pt-36 pb-16 text-on-dark md:pt-44 md:pb-20">
    <HeroGrid class="pointer-events-none absolute inset-0 opacity-60" />
    <div class="container-site relative">
      <Breadcrumbs :items="crumbs" dark />
      <p v-if="eyebrow" class="eyebrow mt-8">{{ eyebrow }}</p>
      <p v-if="code" class="code mt-6 text-sm text-brand-orange-500">{{ code }}</p>
      <h1 class="mt-3 max-w-4xl text-[30px] leading-[38px] text-white md:text-[44px] md:leading-[56px]">{{ title }}</h1>
      <p v-if="lead" class="mt-5 max-w-3xl text-base leading-7 text-on-dark-muted md:text-lg md:leading-8">{{ lead }}</p>
      <div v-if="$slots.default" class="mt-8 flex flex-wrap gap-3"><slot /></div>
    </div>
  </section>
</template>
