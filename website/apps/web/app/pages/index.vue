<script setup lang="ts">
import type { ContentItem } from '~/utils/types'
// P-01 首页（design_document/02 §3、K-01 §3）：深浅交替，证据先行
const [{ data: home }, { data: subs }, { data: cases }, { data: solutions }, { data: drafting }, { data: certs }, { data: news }, { data: stdAll }] = await Promise.all([
  useFetch<ContentItem>('/api/v1/content/page/home', { key: 'page:home' }),
  useContentList('product', { category: 'sub_product' }),
  useContentList('case', { featured: true, archived: false }),
  useContentList('solution'),
  useContentList('standard', { category: 'drafting' }),
  useContentList('certificate'),
  useContentList('news', { within: 365, limit: 3 }),
  useContentList('standard', { limit: 1 }),
])
const h = computed(() => home.value?.data as any)
const lightbox = ref<{ src: string; alt?: string } | null>(null)

usePageSeo({
  title: '工业人工智能 · 空间群弈™ SpatiGo™ 监管—执行智能体集群',
  description: '华云智联是新一代工业人工智能科技公司。空间群弈™ SpatiGo™ 工业监管—执行智能体集群、盘古华云智能工厂平台“7+10+2+N”，服务矿山、石化、航空航天等行业。',
})
useHead({ titleTemplate: '华云智联｜%s' })
</script>

<template>
  <div v-if="h">
    <!-- 首屏 -->
    <section class="on-dark relative overflow-hidden bg-navy-900 text-on-dark">
      <HeroGrid class="pointer-events-none absolute inset-0" />
      <div class="container-site relative grid grid-cols-1 gap-10 pt-32 pb-16 md:pt-40 lg:grid-cols-[1.05fr_1fr] [&>*]:min-w-0 lg:items-center lg:pb-24">
        <div>
          <NuxtLink v-if="h.announcement" :to="h.announcement.href"
                    class="inline-flex max-w-full items-center gap-2 rounded-full border border-white/20 bg-white/5 py-1 pr-3 pl-1 text-[13px] text-on-dark hover:border-brand-orange-500">
            <span class="shrink-0 rounded-full bg-brand-orange-500 px-2 py-0.5 text-xs font-semibold text-navy-900">最新</span>
            <span class="truncate">{{ h.announcement.text }}</span>
            <UiIcon name="arrow" :size="14" class="shrink-0" />
          </NuxtLink>
          <p class="eyebrow mt-8">{{ h.hero.eyebrow }}</p>
          <h1 class="mt-4 text-[36px] leading-[46px] text-white md:text-[56px] md:leading-[68px] xl:text-[64px] xl:leading-[76px]">{{ h.hero.title }}</h1>
          <p class="mt-6 max-w-xl text-base leading-8 text-on-dark-muted md:text-lg">{{ h.hero.subtitle }}</p>
          <div class="mt-10 flex flex-wrap gap-3">
            <UiButton :to="h.hero.primary.href" variant="ondark" size="lg" arrow>{{ h.hero.primary.label }}</UiButton>
            <UiButton :to="h.hero.secondary.href" variant="ghost" size="lg">{{ h.hero.secondary.label }}</UiButton>
          </div>
        </div>
        <HeroArchMotion class="mx-auto w-full max-w-[560px]" />
      </div>
    </section>

    <!-- 关键数字 -->
    <section class="bg-white py-14 md:py-20">
      <div class="container-site">
        <StatGroup :stats="h.stats" />
        <ol class="mt-10 space-y-1 border-t border-line-200 pt-4 text-xs leading-5 text-ink-500">
          <li v-for="(f, i) in h.footnotes" :id="`fn-${i + 1}`" :key="i"><sup>{{ i + 1 }}</sup> {{ f }}</li>
        </ol>
      </div>
    </section>

    <!-- 信任带 -->
    <section class="border-y border-line-200 bg-paper py-12 md:py-16">
      <div class="container-site"><TrustBand :customers="h.customers" :committees="h.committees" /></div>
    </section>

    <!-- 痛点 → 子产品 -->
    <section class="section bg-white">
      <div class="container-site">
        <SectionHeader eyebrow="SpatiGo™" title="从一个现场问题开始" lead="空间群弈™ 四个子产品分别回答质量、运维、安全与具身作业四类现场问题，监管智能体负责判断，执行智能体负责动作，关键环节人在回路。" />
        <PainCards v-reveal :items="subs.items" />
        <div class="mt-8"><UiButton to="/products/spatigo" variant="secondary" arrow>了解空间群弈™ SpatiGo™</UiButton></div>
      </div>
    </section>

    <!-- 平台架构 -->
    <section class="section on-dark bg-navy-900 text-on-dark">
      <div class="container-site">
        <SectionHeader eyebrow="Platform" title="盘古华云智能工厂平台 7+10+2+N" dark
                       lead="“乐高”式组合算法引擎、工业软件、约束模型与智能体集群，按智能工厂成熟度逐步建设。" />
        <ArchDiagram :layers="h.arch" />
      </div>
    </section>

    <!-- 证据：案例 -->
    <section v-if="cases.items.length" class="section bg-white">
      <div class="container-site">
        <div class="flex flex-wrap items-end justify-between gap-4">
          <SectionHeader eyebrow="Evidence" title="在现场跑起来的项目" class="!mb-0" />
          <UiButton to="/cases" variant="text" arrow>全部案例</UiButton>
        </div>
        <div class="mt-10 grid gap-6 md:grid-cols-2">
          <CaseCard v-for="c in cases.items" :key="c.slug" v-reveal :item="c" />
        </div>
      </div>
    </section>

    <!-- 部署与安全 -->
    <section class="section bg-paper">
      <div class="container-site">
        <SectionHeader eyebrow="Deploy & Security" title="数据不出厂网，模型可大可小" />
        <div class="grid gap-4 md:grid-cols-3">
          <div v-for="(d, i) in h.deploy" :key="d.title" v-reveal class="card p-7">
            <UiIcon :name="['shield', 'cpu', 'layers'][i] || 'shield'" :size="28" class="text-brand-blue-700" />
            <h3 class="mt-5 text-lg">{{ d.title }}</h3>
            <p class="mt-2 text-[15px] leading-7 text-ink-600">{{ d.text }}</p>
          </div>
        </div>
        <div class="mt-8"><UiButton to="/products/security-integration" variant="text" arrow>安全与集成能力</UiButton></div>
      </div>
    </section>

    <!-- 行业 -->
    <section class="section bg-white">
      <div class="container-site">
        <div class="flex flex-wrap items-end justify-between gap-4">
          <SectionHeader eyebrow="Industries" title="面向六大行业的解决方案" class="!mb-0" />
          <UiButton to="/solutions" variant="text" arrow>解决方案总览</UiButton>
        </div>
        <div class="mt-10 grid gap-px overflow-hidden rounded-sm border border-line-200 bg-line-200 sm:grid-cols-2 lg:grid-cols-3">
          <NuxtLink v-for="s in solutions.items" :key="s.slug" :to="`/solutions/${s.slug}`" class="group flex flex-col bg-white p-6 hover:bg-brand-blue-50">
            <span class="flex items-center justify-between text-lg font-semibold">{{ s.title }}<UiIcon name="arrow" :size="18" class="text-brand-blue-700 transition-transform group-hover:translate-x-1" /></span>
            <span class="mt-2 text-[15px] leading-7 text-ink-600">{{ s.summary }}</span>
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- 标准与研究 -->
    <section class="section on-dark bg-navy-900 text-on-dark">
      <div class="container-site grid gap-10 lg:grid-cols-[1fr_1.2fr]">
        <div>
          <p class="eyebrow">Standards & Research</p>
          <h2 class="mt-3 text-2xl text-white md:text-[34px] md:leading-[44px]">以标准沉淀工程方法</h2>
          <p class="mt-4 leading-8 text-on-dark-muted">参与数字孪生、工业软件、人工智能、工业通信、智能工厂、预测性维护等国家与国际标准工作，标准目录共 {{ stdAll.total }} 个条目，另有专利、软件著作权与国家 / 省级科研项目。</p>
          <div class="mt-8 flex flex-wrap gap-3">
            <UiButton to="/research" variant="ondark" arrow>标准与研究</UiButton>
            <UiButton to="/research/labs" variant="ghost">联合实验室</UiButton>
          </div>
        </div>
        <div>
          <p class="text-sm font-semibold text-on-dark">2026 年参与编写</p>
          <ul class="mt-4 divide-y divide-white/10 border-y border-white/10">
            <li v-for="s in drafting.items" :key="s.slug" class="flex flex-col gap-1 py-4 sm:flex-row sm:items-baseline sm:gap-6">
              <span class="code w-36 shrink-0 text-brand-orange-500">{{ s.data.code }}</span>
              <span class="text-on-dark">{{ s.title }}</span>
            </li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 资质证书 -->
    <section v-if="certs.items.length" class="section bg-paper">
      <div class="container-site">
        <div class="flex flex-wrap items-end justify-between gap-4">
          <SectionHeader eyebrow="Certificates" title="资质与体系认证" class="!mb-0" />
          <UiButton to="/about/honors" variant="text" arrow>全部资质荣誉</UiButton>
        </div>
        <div class="mt-10 grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
          <DocCard v-for="c in certs.items" :key="c.slug" :title="c.title" :image="c.data.image" :meta="c.data.number"
                   :badge="c.status === 'expiring' ? '即将到期' : '有效'" :badge-tone="c.status === 'expiring' ? 'warn' : 'ok'"
                   @open="lightbox = $event" />
        </div>
      </div>
    </section>

    <!-- 新闻：近 12 个月不少于 3 条才展示（02 §3） -->
    <section v-if="news.items.length >= 3" class="section bg-white">
      <div class="container-site">
        <div class="flex flex-wrap items-end justify-between gap-4">
          <SectionHeader eyebrow="News" title="最新动态" class="!mb-0" />
          <UiButton to="/news" variant="text" arrow>新闻中心</UiButton>
        </div>
        <div class="mt-10 grid gap-6 md:grid-cols-3"><NewsCard v-for="n in news.items" :key="n.slug" :item="n" /></div>
      </div>
    </section>

    <CtaBand :title="h.cta.title" :to="h.cta.primary.href" :label="h.cta.primary.label" />
    <Lightbox v-model="lightbox" />
  </div>
</template>
