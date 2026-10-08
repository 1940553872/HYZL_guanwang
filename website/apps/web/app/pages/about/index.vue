<script setup lang="ts">
import type { ContentItem } from '~/utils/types'
// P-70 公司介绍：使命、简介、价值观、发展历程、企业风采
const { data: page } = await useFetch<ContentItem>('/api/v1/content/page/about', { key: 'page:about' })
const a = computed(() => page.value?.data as any)
const lightbox = ref<{ src: string; alt?: string } | null>(null)
usePageSeo({ title: '关于我们', description: '西安华云智联信息科技有限公司成立于2018年，是新一代工业人工智能科技公司，使命“让智能释放产业效能”。' })
</script>

<template>
  <div v-if="a">
    <PageHero :title="a.mission" eyebrow="About Huayun Zhilian" :lead="a.missionEn" :crumbs="[{ name: '关于我们' }]" />
    <section class="section bg-white">
      <div class="container-site grid gap-10 lg:grid-cols-[1fr_1.6fr]">
        <SectionHeader eyebrow="Company" title="新一代工业人工智能科技公司" />
        <div class="space-y-5"><p v-for="(p, i) in a.intro" :key="i" class="leading-8 text-ink-600">{{ p }}</p></div>
      </div>
    </section>
    <section class="section on-dark bg-navy-900 text-on-dark">
      <div class="container-site">
        <SectionHeader eyebrow="Values" title="我们坚持的三件事" dark />
        <div class="grid gap-4 md:grid-cols-3">
          <div v-for="v in a.values" :key="v.title" class="rounded-sm border border-white/15 p-7">
            <p class="text-3xl font-bold text-brand-orange-500">{{ v.title }}</p>
            <p class="mt-4 leading-7 text-on-dark-muted">{{ v.text }}</p>
          </div>
        </div>
      </div>
    </section>
    <section class="section bg-white">
      <div class="container-site">
        <SectionHeader eyebrow="Milestones" title="发展历程" />
        <ol class="relative border-l-2 border-line-200 pl-8 md:ml-24">
          <li v-for="m in a.milestones" :key="m.year" v-reveal class="relative pb-10 last:pb-0">
            <span class="absolute top-2 -left-[39px] size-4 rounded-full border-4 border-white bg-brand-orange-500 ring-1 ring-line-200" />
            <span class="stat-num text-2xl text-brand-blue-700 md:absolute md:top-0 md:-left-[132px]">{{ m.year }}</span>
            <p class="mt-1 max-w-3xl leading-8 text-ink-600 md:mt-0">{{ m.text }}</p>
          </li>
        </ol>
      </div>
    </section>
    <section class="section bg-paper">
      <div class="container-site">
        <SectionHeader eyebrow="Gallery" title="企业风采" />
        <div class="grid grid-cols-2 gap-4 md:grid-cols-4">
          <figure v-for="ph in a.photos" :key="ph.src" class="card overflow-hidden">
            <button type="button" class="block aspect-[16/10] w-full cursor-zoom-in overflow-hidden" :aria-label="`放大查看：${ph.alt}`" @click="lightbox = ph">
              <img :src="ph.src" :alt="ph.alt" :width="ph.w" :height="ph.h" loading="lazy" class="size-full object-cover">
            </button>
            <figcaption class="px-3 py-2 text-xs leading-5 text-ink-600">{{ ph.alt }}</figcaption>
          </figure>
        </div>
      </div>
    </section>
    <section class="bg-white py-12">
      <div class="container-site grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <NuxtLink v-for="l in [{ to: '/about/honors', t: '资质荣誉', d: '证书、奖项与知识产权' }, { to: '/about/partners', t: '合作伙伴', d: '高校、院所与行业伙伴' }, { to: '/about/careers', t: '加入我们', d: '开放职位' }, { to: '/about/contact', t: '联系我们', d: '电话、邮箱与地址' }]"
                  :key="l.to" :to="l.to" class="card card-hover group flex items-center justify-between p-6">
          <span><span class="block text-lg font-semibold">{{ l.t }}</span><span class="text-sm text-ink-500">{{ l.d }}</span></span>
          <UiIcon name="arrow" class="text-brand-blue-700 transition-transform group-hover:translate-x-1" />
        </NuxtLink>
      </div>
    </section>
    <CtaBand />
    <Lightbox v-model="lightbox" />
  </div>
</template>
