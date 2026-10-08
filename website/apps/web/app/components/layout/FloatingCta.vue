<script setup lang="ts">
// 右下角可折叠悬浮咨询（K-02 §2.1）：预约演示 / 电话 / 微信二维码 / 返回顶部
const { public: pub } = useRuntimeConfig()
const open = ref(false)
const showTop = ref(false)
const qr = ref(false)
function onScroll() { showTop.value = window.scrollY > 800 }
onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onBeforeUnmount(() => window.removeEventListener('scroll', onScroll))
function toTop() { window.scrollTo({ top: 0, behavior: 'smooth' }) }
const route = useRoute()
const hidden = computed(() => route.path === '/demo')
</script>

<template>
  <div v-if="!hidden" class="fixed right-4 bottom-4 z-40 flex flex-col items-end gap-2 md:right-6 md:bottom-6">
    <div v-show="open" id="float-panel" class="w-56 overflow-hidden rounded-md border border-line-200 bg-white text-sm shadow-2">
      <NuxtLink to="/demo" class="flex items-center gap-3 px-4 py-3 hover:bg-paper"><UiIcon name="calendar" :size="18" class="text-brand-orange-600" />预约现场演示</NuxtLink>
      <a :href="`tel:${pub.hotline}`" class="flex items-center gap-3 border-t border-line-200 px-4 py-3 hover:bg-paper">
        <UiIcon name="phone" :size="18" class="text-brand-blue-700" /><span>7×24 热线<br><span class="font-latin font-semibold">{{ pub.hotline }}</span></span>
      </a>
      <button type="button" class="flex w-full items-center gap-3 border-t border-line-200 px-4 py-3 text-left hover:bg-paper" :aria-expanded="qr" @click="qr = !qr">
        <UiIcon name="wechat" :size="18" class="text-success" />微信公众号
      </button>
      <img v-if="qr" src="/media/about/wechat_qrcode.webp" alt="华云智联微信公众号二维码" width="160" height="160" class="mx-auto mb-3 size-40">
    </div>
    <div class="flex gap-2">
      <button v-show="showTop" type="button" class="inline-flex size-12 items-center justify-center rounded-full border border-line-200 bg-white text-ink-900 shadow-1"
              aria-label="返回顶部" @click="toTop"><UiIcon name="arrow-up" /></button>
      <button type="button" class="inline-flex h-12 items-center gap-2 rounded-full bg-brand-orange-600 px-5 font-semibold text-white shadow-2 hover:bg-brand-orange-700"
              :aria-expanded="open" aria-controls="float-panel" @click="open = !open">
        <UiIcon :name="open ? 'close' : 'chat'" :size="20" /><span class="hidden sm:inline">{{ open ? '收起' : '咨询' }}</span><span class="sr-only sm:hidden">{{ open ? '收起咨询' : '打开咨询' }}</span>
      </button>
    </div>
  </div>
</template>
