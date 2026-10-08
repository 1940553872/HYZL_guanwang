<script setup lang="ts">
// 按钮（K-01 §4）：primary 行动橙 / secondary 华云蓝描边 / ondark 深底橙 / ghost 深底白描边 / text 文字链接
const props = withDefaults(defineProps<{
  to?: string
  href?: string
  variant?: 'primary' | 'secondary' | 'ondark' | 'ghost' | 'text'
  size?: 'sm' | 'md' | 'lg'
  type?: 'button' | 'submit'
  disabled?: boolean
  loading?: boolean
  arrow?: boolean
}>(), { variant: 'primary', size: 'md', type: 'button', arrow: false })

const cls = computed(() => {
  const base = 'inline-flex items-center justify-center gap-2 rounded-sm font-semibold whitespace-nowrap transition-colors duration-150 ease-out disabled:cursor-not-allowed'
  const size = { sm: 'h-8 px-4 text-sm', md: 'h-10 px-5 text-base', lg: 'h-12 px-6 text-base' }[props.size]
  const variant = {
    primary: 'bg-brand-orange-600 text-white hover:bg-brand-orange-700 active:bg-brand-orange-700 disabled:bg-line-200 disabled:text-ink-500',
    secondary: 'border border-brand-blue-700 text-brand-blue-700 bg-transparent hover:bg-brand-blue-50',
    ondark: 'bg-brand-orange-500 text-navy-900 hover:bg-[#F28C5B]',
    ghost: 'border border-white/70 text-white hover:bg-white/10',
    text: 'h-auto px-0 text-brand-blue-700 hover:underline underline-offset-4',
  }[props.variant]
  return [base, props.variant === 'text' ? '' : size, variant].join(' ')
})
</script>

<template>
  <NuxtLink v-if="to" :to="to" :class="cls">
    <slot /><UiIcon v-if="arrow" name="arrow" :size="18" />
  </NuxtLink>
  <a v-else-if="href" :href="href" :class="cls">
    <slot /><UiIcon v-if="arrow" name="arrow" :size="18" />
  </a>
  <button v-else :type="type" :class="cls" :disabled="disabled || loading" :aria-busy="loading || undefined">
    <svg v-if="loading" class="size-4 animate-spin" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" opacity=".3" />
      <path d="M21 12a9 9 0 0 0-9-9" stroke="currentColor" stroke-width="2" />
    </svg>
    <slot /><UiIcon v-if="arrow && !loading" name="arrow" :size="18" />
  </button>
</template>
