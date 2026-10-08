<script setup lang="ts">
import type { ContentItem } from '~/utils/types'
// P-92 隐私政策与法律声明
const { data: page } = await useFetch<ContentItem>('/api/v1/content/page/privacy', { key: 'page:privacy' })
usePageSeo({ title: '隐私政策与法律声明', description: '华云智联网站个人信息收集、使用与保护说明。' })
</script>

<template>
  <div>
    <PageHero title="隐私政策与法律声明" eyebrow="Privacy" lead="版本 2026-10" :crumbs="[{ name: '隐私政策与法律声明' }]" />
    <section class="section bg-white">
      <div class="container-site max-w-3xl"><ContentBlocks :blocks="(page?.data as any)?.blocks || []" /></div>
    </section>
  </div>
</template>
