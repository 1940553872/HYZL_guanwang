<script setup lang="ts">
// P-51 联合实验室
const { data } = await useContentList('lab')
usePageSeo({ title: '联合实验室', description: '华云智联与高校、科研院所和行业企业共建的工业互联网与智能制造联合实验室。' })
</script>

<template>
  <div>
    <PageHero title="联合实验室" eyebrow="Joint Labs" lead="与高校、科研院所和行业企业共建研发验证环境，把研究成果带到工业现场。"
              :crumbs="[{ name: '标准与研究', to: '/research' }, { name: '联合实验室' }]" />
    <section class="section bg-white">
      <div class="container-site space-y-16">
        <article v-for="(l, i) in data.items" :key="l.slug" class="grid gap-8 lg:grid-cols-2 lg:items-center">
          <img v-if="l.data.image" :src="l.data.image.src" :alt="l.title" :width="l.data.image.w" :height="l.data.image.h" loading="lazy"
               :class="['w-full rounded-sm border border-line-200', i % 2 && 'lg:order-2']">
          <div>
            <p class="eyebrow">{{ l.data.en }}</p>
            <h2 class="mt-3 text-2xl">{{ l.title }}</h2>
            <p class="mt-4 leading-8 text-ink-600">{{ l.data.body }}</p>
          </div>
        </article>
      </div>
    </section>
    <CtaBand />
  </div>
</template>
