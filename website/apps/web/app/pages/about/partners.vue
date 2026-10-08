<script setup lang="ts">
import { PARTNER_CAT } from '~/utils/labels'
// P-73 合作伙伴：合作单位按类别分组（与“客户”区分）
const { data } = await useContentList('partner')
const groups = computed(() => Object.entries(PARTNER_CAT).map(([k, label]) => ({ k, label, items: data.value.items.filter((p) => p.category === k) })).filter((g) => g.items.length))
usePageSeo({ title: '合作伙伴', description: '与华云智联开展科研、标准与项目合作的高校、科研院所、行业企业与技术伙伴。' })
</script>

<template>
  <div>
    <PageHero title="合作伙伴" eyebrow="Partners" lead="与高校、科研院所、行业企业和技术伙伴在科研、标准与项目上开展合作。以下为合作单位，不代表客户关系。"
              :crumbs="[{ name: '关于我们', to: '/about' }, { name: '合作伙伴' }]">
      <UiButton to="/about/contact?type=partner" variant="ondark">成为合作伙伴</UiButton>
    </PageHero>
    <section class="section bg-white">
      <div class="container-site space-y-14">
        <div v-for="g in groups" :key="g.k">
          <h2 class="mb-6 text-xl">{{ g.label }} <span class="font-latin text-base text-ink-500">{{ g.items.length }}</span></h2>
          <ul class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
            <li v-for="p in g.items" :key="p.slug" class="card flex flex-col items-center justify-center gap-2 p-4">
              <img v-if="p.data.logo" :src="p.data.logo.src" :alt="p.title" loading="lazy" class="h-12 w-full object-contain">
              <span class="text-center text-xs text-ink-600">{{ p.title }}</span>
            </li>
          </ul>
        </div>
      </div>
    </section>
  </div>
</template>
