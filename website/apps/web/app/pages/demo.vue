<script setup lang="ts">
// P-72 预约现场演示（核心转化页，K-02 §3.1：≤ 4 步）
const { public: pub } = useRuntimeConfig()
usePageSeo({ title: '预约现场演示', description: '预约空间群弈™ SpatiGo™ 与工业智能体现场演示，工程师 1 个工作日内联系。' })
const steps = ['提交预约信息', '工程师 1 个工作日内联系，确认现场问题', '线上交流或到场演示', '给出方案与验证计划']
</script>

<template>
  <div>
    <PageHero title="预约现场演示" eyebrow="Book a Demo" lead="带一个现场问题来，我们用智能体给出答案。" :crumbs="[{ name: '预约现场演示' }]" />
    <section class="section bg-paper">
      <div class="container-site grid gap-10 lg:grid-cols-[1fr_1.6fr]">
        <aside class="space-y-6">
          <div>
            <h2 class="text-xl">接下来会发生什么</h2>
            <ol class="mt-4 space-y-3">
              <li v-for="(s, i) in steps" :key="s" class="flex gap-3"><span class="stat-num text-brand-orange-600">0{{ i + 1 }}</span><span class="text-ink-600">{{ s }}</span></li>
            </ol>
          </div>
          <div class="rounded-sm bg-navy-900 p-6 text-on-dark">
            <p class="text-sm text-on-dark-muted">不想填表？直接致电 7×24 热线</p>
            <a :href="`tel:${pub.hotline}`" class="font-latin mt-1 block text-2xl font-bold text-white">{{ pub.hotline }}</a>
          </div>
        </aside>
        <LeadForm type="demo" />
      </div>
    </section>
  </div>
</template>
