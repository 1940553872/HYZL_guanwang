<script setup lang="ts">
import { NAV } from '~/utils/nav'
// 页头（K-01 §4 / K-02 §2.2）：顶部工具条 + 主导航；页面顶部在深色首屏上透明，滚动后变白并收起工具条
const { public: pub } = useRuntimeConfig()
const route = useRoute()
const scrolled = ref(false)
const openIdx = ref<number | null>(null)
const drawer = ref(false)
const searchOpen = ref(false)
let closeTimer: ReturnType<typeof setTimeout> | undefined

function onScroll() { scrolled.value = window.scrollY > 8 }
onMounted(() => { onScroll(); window.addEventListener('scroll', onScroll, { passive: true }) })
onBeforeUnmount(() => window.removeEventListener('scroll', onScroll))
watch(() => route.fullPath, () => { openIdx.value = null; drawer.value = false })

const solid = computed(() => scrolled.value || openIdx.value !== null)
function enter(i: number) { clearTimeout(closeTimer); openIdx.value = i }
function leave() { closeTimer = setTimeout(() => { openIdx.value = null }, 120) }
function toggle(i: number) { openIdx.value = openIdx.value === i ? null : i }
function isActive(to: string) { return route.path === to || route.path.startsWith(`${to}/`) }
function onKey(e: KeyboardEvent) { if (e.key === 'Escape') openIdx.value = null }
</script>

<template>
  <header class="fixed inset-x-0 top-0 z-50" @keydown="onKey">
    <!-- 工具条：热线 / 搜索（桌面端） -->
    <div :class="['hidden overflow-hidden transition-[height] duration-200 lg:block', solid ? 'h-0' : 'h-9']">
      <div class="container-site flex h-9 items-center justify-end gap-6 border-b border-white/10 text-[13px] text-on-dark-muted">
        <a :href="`tel:${pub.hotline}`" class="inline-flex items-center gap-1.5 hover:text-white">
          <UiIcon name="phone" :size="14" />7×24 服务热线 <span class="font-latin text-on-dark">{{ pub.hotline }}</span>
        </a>
        <NuxtLink to="/about/contact" class="hover:text-white">联系我们</NuxtLink>
        <NuxtLink to="/about/careers" class="hover:text-white">加入我们</NuxtLink>
      </div>
    </div>

    <div :class="['transition-colors duration-200', solid ? 'bg-white text-ink-900 shadow-1' : 'bg-transparent text-white']">
      <div class="container-site flex h-[60px] items-center gap-6 lg:h-16">
        <NuxtLink to="/" class="flex shrink-0 items-center" aria-label="华云智联 首页">
          <img :src="solid ? '/media/brand/logo.webp' : '/media/brand/logo-white.webp'" alt="华云智联" width="148" height="40"
               class="h-8 w-auto lg:h-9">
        </NuxtLink>

        <nav aria-label="主导航" class="hidden flex-1 lg:block">
          <ul class="flex items-center justify-center gap-1 xl:gap-2">
            <li v-for="(item, i) in NAV" :key="item.to" class="relative" @mouseenter="item.columns && enter(i)" @mouseleave="item.columns && leave()">
              <NuxtLink v-if="!item.columns" :to="item.to"
                        :class="['flex h-16 items-center border-b-2 px-3 text-[15px] font-medium', isActive(item.to) ? 'border-brand-orange-500' : 'border-transparent hover:border-current/30']">
                {{ item.label }}
              </NuxtLink>
              <button v-else type="button" :aria-expanded="openIdx === i" :aria-controls="`mega-${i}`"
                      :class="['flex h-16 items-center gap-1 border-b-2 px-3 text-[15px] font-medium', isActive(item.to) ? 'border-brand-orange-500' : 'border-transparent']"
                      @click="toggle(i)">
                {{ item.label }}<UiIcon name="chevron" :size="14" :class="['transition-transform', openIdx === i && 'rotate-180']" />
              </button>
            </li>
          </ul>
        </nav>

        <div class="ml-auto flex items-center gap-2 lg:ml-0">
          <button type="button" class="inline-flex size-10 items-center justify-center rounded-sm hover:bg-current/10" aria-label="站内搜索"
                  @click="searchOpen = true">
            <UiIcon name="search" :size="20" />
          </button>
          <UiButton to="/demo" :variant="solid ? 'primary' : 'ondark'" size="sm" class="hidden sm:inline-flex">预约现场演示</UiButton>
          <button type="button" class="inline-flex size-10 items-center justify-center lg:hidden" aria-label="打开菜单" @click="drawer = true">
            <UiIcon name="menu" />
          </button>
        </div>
      </div>

      <!-- 下拉面板 -->
      <template v-for="(item, i) in NAV" :key="`m-${item.to}`">
        <div v-if="item.columns" v-show="openIdx === i" :id="`mega-${i}`"
             class="absolute inset-x-0 top-full hidden border-t border-line-200 bg-white text-ink-900 shadow-2 lg:block"
             @mouseenter="enter(i)" @mouseleave="leave()">
          <div class="container-site grid gap-10 py-8" :style="{ gridTemplateColumns: `repeat(${item.columns.length + (item.promo ? 1 : 0)}, minmax(0, 1fr))` }">
            <div v-for="col in item.columns" :key="col.title">
              <p class="mb-3 text-xs font-semibold tracking-wider text-ink-500">{{ col.title }}</p>
              <ul class="space-y-1">
                <li v-for="l in col.links" :key="l.to + l.label">
                  <NuxtLink :to="l.to" class="group flex items-start gap-3 rounded-sm px-2 py-2 hover:bg-paper">
                    <span v-if="l.icon" class="mt-0.5 inline-flex size-8 shrink-0 items-center justify-center rounded-sm bg-brand-blue-50 text-brand-blue-700">
                      <UiIcon :name="l.icon" :size="18" />
                    </span>
                    <span>
                      <span class="block text-[15px] font-medium group-hover:text-brand-blue-700">{{ l.label }}</span>
                      <span v-if="l.desc" class="block text-[13px] leading-5 text-ink-500">{{ l.desc }}</span>
                    </span>
                  </NuxtLink>
                </li>
              </ul>
            </div>
            <NuxtLink v-if="item.promo" :to="item.promo.to" class="on-dark flex flex-col justify-between rounded-sm bg-navy-900 p-6 text-on-dark">
              <span>
                <span class="eyebrow">Live Demo</span>
                <span class="mt-2 block text-lg font-bold text-white">{{ item.promo.title }}</span>
                <span class="mt-2 block text-sm text-on-dark-muted">{{ item.promo.text }}</span>
              </span>
              <span class="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-brand-orange-500">立即预约<UiIcon name="arrow" :size="16" /></span>
            </NuxtLink>
          </div>
        </div>
      </template>
    </div>

    <MobileDrawer v-model:open="drawer" />
    <SearchDialog v-model:open="searchOpen" />
  </header>
</template>
