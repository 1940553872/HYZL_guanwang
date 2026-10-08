<script setup lang="ts">
// P-25 工业软件总览：标准软件 / 高级软件（Tabs）
import { TabsContent, TabsList, TabsRoot, TabsTrigger } from 'reka-ui'
const [{ data: list }, { data: std }, { data: adv }] = await Promise.all([
  useContentList('product', { category: 'software' }),
  useContentItem('product', 'software-standard'),
  useContentItem('product', 'software-advanced'),
])
const tab = ref('standard')
const groups = computed(() => [
  { key: 'standard', head: std.value, items: list.value.items.filter((s) => s.data.group === 'standard') },
  { key: 'advanced', head: adv.value, items: list.value.items.filter((s) => s.data.group !== 'standard') },
])
usePageSeo({ title: '工业软件', description: std.value.summary })
</script>

<template>
  <div>
    <PageHero title="工业软件" eyebrow="Industrial Software" lead="覆盖设计、生产、仓储、质量、能源、安全与运维的工业标准软件，以及面向控制、孪生与无人值守的工业高级软件。"
              :crumbs="[{ name: '产品与技术', to: '/products' }, { name: '工业软件' }]" />
    <section class="section bg-paper">
      <div class="container-site">
        <TabsRoot v-model="tab">
          <TabsList aria-label="软件分类" class="mb-10 inline-flex rounded-sm border border-line-200 bg-white p-1">
            <TabsTrigger v-for="g in groups" :key="g.key" :value="g.key"
                         class="h-10 rounded-xs px-5 text-[15px] font-medium text-ink-600 data-[state=active]:bg-brand-blue-700 data-[state=active]:text-white">
              {{ g.head.title }}（{{ g.items.length }}）
            </TabsTrigger>
          </TabsList>
          <TabsContent v-for="g in groups" :key="g.key" :value="g.key">
            <div class="mb-8 max-w-4xl">
              <p class="eyebrow">{{ g.head.data.en }}</p>
              <p v-for="(o, i) in g.head.data.overview" :key="i" class="mt-3 leading-8 text-ink-600">{{ o }}</p>
            </div>
            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              <ProductCard v-for="s in g.items" :key="s.slug" :item="s" />
            </div>
          </TabsContent>
        </TabsRoot>
      </div>
    </section>
    <CtaBand />
  </div>
</template>
