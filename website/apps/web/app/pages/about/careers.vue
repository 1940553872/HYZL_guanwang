<script setup lang="ts">
// P-75 加入我们
const [{ data }, { data: common }] = await Promise.all([useContentList('job'), useCommon()])
const open = ref<string | null>(null)
usePageSeo({ title: '加入我们', description: '华云智联开放职位：工程项目经理、Web 前端工程师、Java 后端工程师。' })
</script>

<template>
  <div>
    <PageHero title="加入我们" eyebrow="Careers" lead="和我们一起，把人工智能带到工业现场。" :crumbs="[{ name: '关于我们', to: '/about' }, { name: '加入我们' }]" />
    <section class="section bg-white">
      <div class="container-site max-w-4xl">
        <p class="mb-8 text-ink-600">简历请发送至 <a :href="`mailto:${common?.data.email}`" class="link font-latin">{{ common?.data.email }}</a>，邮件标题注明“应聘岗位 + 姓名”。</p>
        <ul class="divide-y divide-line-200 border-y border-line-200">
          <li v-for="j in data.items" :key="j.slug">
            <h2>
              <button type="button" class="flex w-full items-center justify-between py-5 text-left text-xl font-bold" :aria-expanded="open === j.slug"
                      :aria-controls="`job-${j.slug}`" @click="open = open === j.slug ? null : j.slug">
                {{ j.title }}<UiIcon name="chevron" :class="['transition-transform', open === j.slug && 'rotate-180']" />
              </button>
            </h2>
            <div v-show="open === j.slug" :id="`job-${j.slug}`" class="grid gap-8 pb-8 md:grid-cols-2">
              <div><h3 class="mb-3 text-base">岗位职责</h3><ol class="list-decimal space-y-2 pl-5 text-[15px] leading-7 text-ink-600"><li v-for="(d, i) in j.data.duties" :key="i">{{ d }}</li></ol></div>
              <div><h3 class="mb-3 text-base">任职要求</h3><ul class="space-y-2 text-[15px] leading-7 text-ink-600"><li v-for="(r, i) in j.data.reqs" :key="i">{{ r }}</li></ul></div>
            </div>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>
