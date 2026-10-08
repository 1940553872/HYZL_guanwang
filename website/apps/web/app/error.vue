<script setup lang="ts">
import type { NuxtError } from '#app'
// P-91 错误页（404 / 500）
const props = defineProps<{ error: NuxtError }>()
const is404 = computed(() => props.error.statusCode === 404)
useHead({ title: is404.value ? '页面不存在' : '服务暂时不可用', meta: [{ name: 'robots', content: 'noindex' }] })
const { public: pub } = useRuntimeConfig()
</script>

<template>
  <NuxtLayout>
    <section class="on-dark relative flex min-h-[70vh] items-center overflow-hidden bg-navy-900 pt-32 pb-20 text-on-dark">
      <HeroGrid class="pointer-events-none absolute inset-0" />
      <div class="container-site relative">
        <p class="stat-num text-7xl text-brand-orange-500 md:text-8xl">{{ error.statusCode }}</p>
        <h1 class="mt-4 text-3xl text-white md:text-4xl">{{ is404 ? '页面不存在或已调整' : '服务暂时不可用' }}</h1>
        <p class="mt-4 max-w-xl text-on-dark-muted">{{ is404 ? '页面可能已在网站改版中迁移。可以返回首页、搜索站内内容，或直接联系我们。' : `请稍后刷新重试；紧急需求请拨打 7×24 热线 ${pub.hotline}。` }}</p>
        <div class="mt-8 flex flex-wrap gap-3">
          <UiButton variant="ondark" @click="clearError({ redirect: '/' })">返回首页</UiButton>
          <UiButton variant="ghost" @click="clearError({ redirect: '/products' })">浏览产品</UiButton>
          <UiButton variant="ghost" @click="clearError({ redirect: '/demo' })">预约现场演示</UiButton>
        </div>
      </div>
    </section>
  </NuxtLayout>
</template>
