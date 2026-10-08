<script setup lang="ts">
// P-24 智能引擎群：7 个引擎页内锚点
const [{ data: g }, { data: list }] = await Promise.all([
  useContentItem('product', 'engines'),
  useContentList('product', { category: 'engine' }),
])
usePageSeo({ title: '智能引擎群', description: g.value.summary })
</script>

<template>
  <div>
    <PageHero title="智能引擎群" :eyebrow="g.data.en" :lead="g.summary" :crumbs="[{ name: '产品与技术', to: '/products' }, { name: '智能引擎群' }]" />
    <AnchorNav :items="list.items.map((e) => ({ id: e.slug, label: e.data.code }))" />
    <section class="bg-white pt-14">
      <div class="container-site max-w-4xl"><p v-for="(o, i) in g.data.overview" :key="i" class="leading-8 text-ink-600">{{ o }}</p></div>
    </section>
    <section class="section bg-white">
      <div class="container-site space-y-6">
        <article v-for="e in list.items" :id="e.slug" :key="e.slug" data-anchor class="card grid scroll-mt-32 gap-6 p-7 md:grid-cols-[240px_1fr] md:p-9">
          <div>
            <p class="code text-2xl text-brand-blue-700">{{ e.data.code }}</p>
            <h2 class="mt-2 text-xl">{{ e.data.name }}</h2>
            <p class="mt-2 text-xs leading-5 text-ink-500">{{ e.data.fullName }}</p>
          </div>
          <p class="text-[15px] leading-8 text-ink-600">{{ e.data.text }}</p>
        </article>
      </div>
    </section>
    <RelatedProducts :slugs="['imllm', 'software-standard', 'software-advanced', 'security-integration']" />
    <CtaBand />
  </div>
</template>
