<script setup lang="ts">
defineProps<{ title: string; text?: string }>()
</script>

<template>
  <div class="card flex flex-col items-center px-6 py-14 text-center">
    <UiIcon name="doc" :size="32" class="text-line-300" />
    <p class="mt-4 text-lg font-semibold">{{ title }}</p>
    <p v-if="text" class="mt-2 max-w-md text-ink-500">{{ text }}</p>
    <div v-if="$slots.default" class="mt-6 flex flex-wrap justify-center gap-3"><slot /></div>
  </div>
</template>
