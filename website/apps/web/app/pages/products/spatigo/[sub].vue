<script setup lang="ts">
// P-21 子产品：质量之弈 / 运维之弈 / 安全之弈 / 具身之弈
const route = useRoute()
const sub = String(route.params.sub)
if (!['quality', 'maintenance', 'safety', 'embodied'].includes(sub)) throw createError({ statusCode: 404, statusMessage: '页面不存在', fatal: true })
const [{ data: p }, { data: siblings }, { data: cases }] = await Promise.all([
  useContentItem('product', `spatigo-${sub}`),
  useContentList('product', { category: 'sub_product' }),
  useContentList('case', { archived: false }),
])
const related = computed(() => (p.value.data.related as string[]) || [])
const relCases = computed(() => cases.value.items.filter((c) => (c.data.products || []).includes(p.value.slug)))
usePageSeo({ title: `${p.value.title} · 空间群弈™ SpatiGo™`, description: `${p.value.data.question}${p.value.data.tagline}` })
</script>

<template>
  <div>
    <PageHero :title="`${p.title}：${p.data.question}`" eyebrow="SpatiGo™ Sub-product" :code="p.data.code" :lead="p.data.tagline"
              :crumbs="[{ name: '产品与技术', to: '/products' }, { name: 'SpatiGo™', to: '/products/spatigo' }, { name: p.title }]">
      <UiButton :to="`/demo?product=${p.slug}`" variant="ondark" arrow>预约{{ p.title }}演示</UiButton>
    </PageHero>

    <section class="section bg-white">
      <div class="container-site grid gap-10 lg:grid-cols-[1.4fr_1fr]">
        <div>
          <SectionHeader eyebrow="How it works" title="监管智能体判断，执行智能体动作" />
          <ol class="space-y-4">
            <li v-for="(s, i) in ['感知：接入现场多模态数据（图像、视频、声音、时序数据）', '判断：监管智能体结合工业增强模型与知识库给出结论与依据', '执行：执行智能体或业务系统完成动作，关键动作人在环上确认', '追溯：全过程留痕审计，结果回流持续优化模型']" :key="i"
                class="card flex gap-4 p-5">
              <span class="stat-num text-2xl text-brand-orange-600">0{{ i + 1 }}</span>
              <span class="leading-7 text-ink-600">{{ s }}</span>
            </li>
          </ol>
        </div>
        <aside class="h-fit rounded-sm bg-brand-blue-50 p-6">
          <p class="font-semibold">支撑该子产品的能力</p>
          <p class="mt-2 text-sm leading-6 text-ink-600">{{ p.title }}由下列智能体应用与工业软件组合交付，可单独部署，也可接入盘古华云智能工厂平台。</p>
          <ul class="mt-4 space-y-2">
            <li v-for="s in siblings.items.filter((x) => x.slug !== p.slug)" :key="s.slug">
              <NuxtLink :to="`/products/spatigo/${s.slug.replace('spatigo-', '')}`" class="link text-sm">{{ s.title }} · {{ s.data.question }}</NuxtLink>
            </li>
          </ul>
        </aside>
      </div>
    </section>

    <RelatedProducts :slugs="related" title="组成能力与相关产品" />

    <section v-if="relCases.length" class="section bg-paper">
      <div class="container-site">
        <SectionHeader eyebrow="Evidence" title="相关案例" />
        <div class="grid gap-6 md:grid-cols-2"><CaseCard v-for="c in relCases" :key="c.slug" :item="c" /></div>
      </div>
    </section>
    <CtaBand :to="`/demo?product=${p.slug}`" />
  </div>
</template>
