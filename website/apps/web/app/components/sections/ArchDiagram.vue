<script setup lang="ts">
// “7+10+2+N”分层架构（K-01 §3 架构图重绘）：自上而下 N 智能体 → 2 约束 → 10 软件 → 7 引擎 → 数据底座，可聚焦查看
const props = defineProps<{ layers: { key: string; title: string; desc: string; href: string }[]; dark?: boolean }>()
const active = ref(0)
</script>

<template>
  <div class="grid gap-8 lg:grid-cols-[1.2fr_1fr] lg:items-center">
    <ol class="space-y-2" aria-label="平台分层">
      <li v-for="(l, i) in props.layers" :key="l.key">
        <NuxtLink :to="l.href"
                  :class="['group flex items-center gap-4 rounded-sm border px-5 py-4 transition-all duration-150',
                           active === i ? 'border-brand-orange-500 bg-white/10' : 'border-white/15 hover:border-white/40']"
                  :style="{ marginInline: `${Math.abs(i - 2) * 12}px` }"
                  @mouseenter="active = i" @focus="active = i">
          <span class="stat-num w-16 shrink-0 text-center text-3xl text-brand-orange-500">{{ l.key === 'base' ? '∞' : l.key.toUpperCase() }}</span>
          <span class="flex-1">
            <span class="block font-semibold text-white">{{ l.title }}</span>
            <span class="mt-0.5 block text-sm text-on-dark-muted lg:hidden">{{ l.desc }}</span>
          </span>
          <UiIcon name="arrow" :size="18" class="text-on-dark-muted transition-transform group-hover:translate-x-1" />
        </NuxtLink>
      </li>
    </ol>
    <div class="hidden rounded-sm border border-white/15 bg-navy-800 p-8 lg:block" aria-live="polite">
      <p class="eyebrow">Layer {{ active + 1 }} / {{ layers.length }}</p>
      <p class="mt-3 text-2xl font-bold text-white">{{ layers[active]?.title }}</p>
      <p class="mt-4 leading-8 text-on-dark-muted">{{ layers[active]?.desc }}</p>
      <NuxtLink :to="layers[active]?.href || '/products'" class="mt-6 inline-flex items-center gap-2 font-semibold text-brand-orange-500">
        查看详情<UiIcon name="arrow" :size="16" />
      </NuxtLink>
    </div>
  </div>
</template>
