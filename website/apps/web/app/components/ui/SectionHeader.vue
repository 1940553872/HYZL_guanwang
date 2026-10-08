<script setup lang="ts">
withDefaults(defineProps<{ eyebrow?: string; title: string; lead?: string; center?: boolean; as?: 'h1' | 'h2'; dark?: boolean }>(), { as: 'h2' })
</script>

<template>
  <div :class="['mb-10 md:mb-14', center ? 'mx-auto max-w-3xl text-center' : 'max-w-3xl']">
    <p v-if="eyebrow" class="eyebrow mb-3">{{ eyebrow }}</p>
    <component :is="as" :class="['text-2xl md:text-[34px] md:leading-[44px]', dark && 'text-white']">{{ title }}</component>
    <p v-if="lead" :class="['mt-4 text-base leading-7 md:text-lg md:leading-8', dark ? 'text-on-dark-muted' : 'text-ink-600']">{{ lead }}</p>
    <slot />
  </div>
</template>
