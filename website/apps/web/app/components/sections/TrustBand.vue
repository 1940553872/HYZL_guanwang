<script setup lang="ts">
// 信任带：服务客户（文字形式，Logo 授权前不使用图形标识）+ 标委会委员单位
defineProps<{ customers: string[]; committees: { code: string; name: string }[] }>()
</script>

<template>
  <div class="grid gap-10 lg:grid-cols-[1fr_1fr]">
    <div>
      <p class="text-sm font-semibold text-ink-500">服务的行业客户（部分）</p>
      <ul class="mt-4 flex flex-wrap gap-x-6 gap-y-3">
        <li v-for="c in customers" :key="c" class="text-lg font-semibold text-ink-600">{{ c }}</li>
      </ul>
    </div>
    <div>
      <p class="text-sm font-semibold text-ink-500">国际 / 国家标委会委员单位</p>
      <ul class="mt-4 grid gap-3 sm:grid-cols-2">
        <li v-for="c in committees" :key="c.code" class="flex items-start gap-3">
          <span class="code shrink-0 rounded-xs bg-brand-blue-50 px-2 py-0.5 text-sm text-brand-blue-700">{{ c.code }}</span>
          <span class="text-sm leading-6 text-ink-600">{{ c.name }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>
