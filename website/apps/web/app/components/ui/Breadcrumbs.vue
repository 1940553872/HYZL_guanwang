<script setup lang="ts">
const props = defineProps<{ items: { name: string; to?: string }[]; dark?: boolean }>()
useBreadcrumbLd([{ name: '首页', to: '/' }, ...props.items.filter((i) => i.to).map((i) => ({ name: i.name, to: i.to! }))])
</script>

<template>
  <nav aria-label="面包屑" :class="['text-sm', dark ? 'text-on-dark-muted' : 'text-ink-500']">
    <ol class="flex flex-wrap items-center gap-x-2 gap-y-1">
      <li><NuxtLink to="/" :class="dark ? 'hover:text-white' : 'hover:text-brand-blue-700'">首页</NuxtLink></li>
      <li v-for="(it, i) in items" :key="i" class="flex items-center gap-2">
        <span aria-hidden="true">/</span>
        <NuxtLink v-if="it.to && i < items.length - 1" :to="it.to" :class="dark ? 'hover:text-white' : 'hover:text-brand-blue-700'">{{ it.name }}</NuxtLink>
        <span v-else aria-current="page" :class="dark ? 'text-on-dark' : 'text-ink-900'">{{ it.name }}</span>
      </li>
    </ol>
  </nav>
</template>
