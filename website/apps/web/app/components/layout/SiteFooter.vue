<script setup lang="ts">
import { FOOTER_COLUMNS } from '~/utils/nav'
// 页脚（K-01 §4）：深色、四列导航 + 联系方式 + 公众号 + 备案号
const { data: common } = await useCommon()
const c = computed(() => common.value?.data)
const year = new Date().getFullYear()
</script>

<template>
  <footer class="on-dark bg-navy-900 text-on-dark-muted">
    <div class="container-site grid gap-10 py-16 lg:grid-cols-[1.3fr_2.7fr]">
      <div>
        <img src="/media/brand/logo-white.webp" alt="华云智联" width="148" height="40" class="h-10 w-auto" loading="lazy">
        <p class="mt-4 text-lg font-semibold text-white">让智能释放产业效能</p>
        <ul v-if="c" class="mt-6 space-y-2 text-sm">
          <li class="flex gap-2"><UiIcon name="phone" :size="16" class="mt-1 shrink-0" /><a :href="`tel:${c.phone}`" class="font-latin hover:text-white">{{ c.phone }}（7×24）</a></li>
          <li class="flex gap-2"><UiIcon name="mail" :size="16" class="mt-1 shrink-0" /><a :href="`mailto:${c.email}`" class="font-latin hover:text-white">{{ c.email }}</a></li>
          <li class="flex gap-2"><UiIcon name="map" :size="16" class="mt-1 shrink-0" /><span>{{ c.address }}</span></li>
        </ul>
      </div>
      <div class="grid grid-cols-2 gap-8 md:grid-cols-5">
        <div v-for="col in FOOTER_COLUMNS" :key="col.title">
          <p class="mb-4 text-sm font-semibold text-white">{{ col.title }}</p>
          <ul class="space-y-2 text-sm">
            <li v-for="l in col.links" :key="l.to"><NuxtLink :to="l.to" class="hover:text-white">{{ l.label }}</NuxtLink></li>
          </ul>
        </div>
        <div v-if="c" class="col-span-2 md:col-span-1">
          <p class="mb-4 text-sm font-semibold text-white">微信公众号</p>
          <img :src="c.wechat.src" alt="华云智联微信公众号二维码" width="112" height="112" class="size-28 rounded-sm bg-white p-1" loading="lazy">
        </div>
      </div>
    </div>
    <div class="border-t border-white/10">
      <div class="container-site flex flex-col gap-2 py-6 text-xs md:flex-row md:items-center md:justify-between">
        <p>© {{ year }} {{ c?.company || '西安华云智联信息科技有限公司' }} 版权所有 · 盘古华云 / Pangoo Cloud 为注册商标</p>
        <p class="flex flex-wrap gap-x-4 gap-y-1">
          <NuxtLink to="/legal/privacy" class="hover:text-white">隐私政策与法律声明</NuxtLink>
          <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener" class="hover:text-white">{{ c?.icp }}</a>
        </p>
      </div>
    </div>
  </footer>
</template>
