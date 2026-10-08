<script setup lang="ts">
// P-74 联系我们：联系方式 + 联系 / 合作表单
const route = useRoute()
const { data: common } = await useCommon()
const c = computed(() => common.value?.data)
const type = computed(() => (route.query.type === 'partner' ? 'partner' : 'contact'))
usePageSeo({ title: '联系我们', description: '华云智联联系电话 029-88810623、邮箱与办公地址。' })
</script>

<template>
  <div>
    <PageHero title="联系我们" eyebrow="Contact" lead="7×24 小时服务热线随时响应；商务合作与媒体联络请留言，我们将在 1 个工作日内回复。"
              :crumbs="[{ name: '关于我们', to: '/about' }, { name: '联系我们' }]" />
    <section class="section bg-paper">
      <div class="container-site grid gap-10 lg:grid-cols-[1fr_1.4fr]">
        <div v-if="c" class="space-y-4">
          <a :href="`tel:${c.phone}`" class="card card-hover flex gap-4 p-6"><UiIcon name="phone" class="text-brand-blue-700" /><span><span class="block text-sm text-ink-500">7×24 服务热线</span><span class="font-latin text-2xl font-bold">{{ c.phone }}</span></span></a>
          <a :href="`mailto:${c.email}`" class="card card-hover flex gap-4 p-6"><UiIcon name="mail" class="text-brand-blue-700" /><span><span class="block text-sm text-ink-500">商务邮箱</span><span class="font-latin text-lg font-semibold">{{ c.email }}</span></span></a>
          <div class="card flex gap-4 p-6"><UiIcon name="map" class="shrink-0 text-brand-blue-700" /><span><span class="block text-sm text-ink-500">公司地址（邮编 {{ c.postcode }}）</span><span class="font-medium">{{ c.address }}</span></span></div>
          <div class="card flex items-center gap-4 p-6">
            <img :src="c.wechat.src" alt="华云智联微信公众号二维码" width="96" height="96" class="size-24">
            <span class="text-sm text-ink-600">扫码关注“华云智联”微信公众号，获取产品与活动动态。</span>
          </div>
        </div>
        <div>
          <h2 class="mb-4 text-2xl">{{ type === 'partner' ? '合作申请' : '在线留言' }}</h2>
          <LeadForm :type="type" submit-label="提交留言" />
        </div>
      </div>
    </section>
  </div>
</template>
