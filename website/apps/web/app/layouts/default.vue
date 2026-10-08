<script setup lang="ts">
// 默认布局：跳转链接 + 页头 + 主体 + 页脚 + 悬浮咨询；输出 Organization 结构化数据（K-04 §5）
const { public: pub } = useRuntimeConfig()
useHead({
  script: [{
    type: 'application/ld+json',
    innerHTML: JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'Organization',
      name: '西安华云智联信息科技有限公司',
      alternateName: ['华云智联', "Xi'an H.Y Wisdom Information Technology Co., Ltd."],
      url: pub.siteUrl,
      logo: `${pub.siteUrl}/media/brand/logo.png`,
      foundingDate: '2018',
      telephone: pub.hotline,
      address: { '@type': 'PostalAddress', addressLocality: '西安市', addressRegion: '陕西省', addressCountry: 'CN', postalCode: '710075' },
    }),
  }],
})
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <a href="#main" class="sr-only z-[100] rounded-sm bg-white px-4 py-2 text-ink-900 focus:not-sr-only focus:fixed focus:top-2 focus:left-2">跳到主要内容</a>
    <SiteHeader />
    <main id="main" class="flex-1" tabindex="-1">
      <slot />
    </main>
    <SiteFooter />
    <FloatingCta />
  </div>
</template>
