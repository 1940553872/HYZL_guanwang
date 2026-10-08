<script setup lang="ts">
import { TabsContent, TabsList, TabsRoot, TabsTrigger } from 'reka-ui'
import { PATENT_KIND, PATENT_STATE, PROJECT_LEVEL, PROJECT_STATUS, STD_STATUS } from '~/utils/labels'
// P-50 标准与研究：标准目录（筛选范围 / 状态）、专利、软件著作权、科研项目
const route = useRoute()
const router = useRouter()
const [{ data: std }, { data: patents }, { data: copyrights }, { data: projects }] = await Promise.all([
  useContentList('standard'),
  useContentList('patent'),
  useContentList('copyright'),
  useContentList('project'),
])
const tabs = ['standards', 'patents', 'copyrights', 'projects']
const tab = ref(tabs.includes(String(route.query.tab)) ? String(route.query.tab) : 'standards')
watch(tab, (t) => router.replace({ query: { ...route.query, tab: t } }))

const scope = ref<'all' | 'international' | 'national' | 'drafting'>('all')
const status = ref('')
const stdRows = computed(() => std.value.items.filter((s) =>
  (scope.value === 'all' || s.category === scope.value) && (!status.value || s.data.status === status.value)))
const count = (c: string) => std.value.items.filter((s) => s.category === c).length
const lightbox = ref<{ src: string; alt?: string } | null>(null)
const projAmount = computed(() => projects.value.items.reduce((a, p) => a + (Number(p.data.amountWan) || 0), 0))
usePageSeo({ title: '标准与研究', description: '华云智联参与的国家与国际标准、发明专利、软件著作权与国家 / 省级科研项目目录。' })
</script>

<template>
  <div>
    <PageHero title="标准与研究" eyebrow="Standards & Research" lead="SAC/TC124、SAC/TC28（SC41、SC42）、SAC/TC88 与 IEC/TC65 委员单位，参与数字孪生、工业软件、人工智能、预测性维护等标准工作。"
              :crumbs="[{ name: '标准与研究' }]">
      <UiButton to="/research/labs" variant="ghost">联合实验室</UiButton>
    </PageHero>
    <section class="border-b border-line-200 bg-white py-10">
      <div class="container-site">
        <StatGroup :stats="[
          { value: String(count('international')), label: '国际标准目录条目' },
          { value: String(count('national')), label: '国家标准目录条目' },
          { value: String(patents.total), label: '专利（含申请）' },
          { value: String(copyrights.total), label: '软件著作权' },
        ]" />
      </div>
    </section>
    <section class="section bg-paper">
      <div class="container-site">
        <TabsRoot v-model="tab">
          <TabsList aria-label="研究成果分类" class="mb-8 flex gap-6 overflow-x-auto border-b border-line-200">
            <TabsTrigger v-for="[k, l] in [['standards', '标准'], ['patents', '专利'], ['copyrights', '软件著作权'], ['projects', '科研项目']]" :key="k" :value="k"
                         class="-mb-px border-b-2 border-transparent py-3 text-base whitespace-nowrap text-ink-500 data-[state=active]:border-brand-orange-500 data-[state=active]:font-semibold data-[state=active]:text-ink-900">
              {{ l }}
            </TabsTrigger>
          </TabsList>

          <TabsContent value="standards">
            <div class="mb-6 flex flex-wrap items-center gap-3">
              <div role="group" aria-label="标准范围" class="inline-flex rounded-sm border border-line-200 bg-white p-1">
                <button v-for="[k, l] in [['all', '全部'], ['international', '国际'], ['national', '国家'], ['drafting', '2026 在编']]" :key="k" type="button"
                        :aria-pressed="scope === k" :class="['h-8 rounded-xs px-3 text-sm', scope === k ? 'bg-brand-blue-700 text-white' : 'text-ink-600']"
                        @click="scope = k as any">{{ l }}</button>
              </div>
              <label class="text-sm text-ink-600">状态
                <select v-model="status" class="ml-2 h-10 rounded-sm border border-line-300 bg-white px-2">
                  <option value="">全部</option>
                  <option v-for="(v, k) in STD_STATUS" :key="k" :value="k">{{ v.label }}</option>
                </select>
              </label>
              <span class="text-sm text-ink-500" aria-live="polite">共 {{ stdRows.length }} 条</span>
            </div>
            <div class="relative overflow-x-auto rounded-sm border border-line-200 bg-white">
              <table class="w-full min-w-[760px] text-left text-sm">
                <thead class="bg-paper"><tr>
                  <th scope="col" class="px-4 py-3 font-semibold">标准编号</th>
                  <th scope="col" class="px-4 py-3 font-semibold">名称</th>
                  <th scope="col" class="px-4 py-3 font-semibold">状态</th>
                  <th scope="col" class="px-4 py-3 font-semibold">角色</th>
                  <th scope="col" class="px-4 py-3 font-semibold">证明材料</th>
                </tr></thead>
                <tbody>
                  <tr v-for="s in stdRows" :key="s.slug" class="border-t border-line-200 align-top">
                    <td class="code px-4 py-3 whitespace-nowrap text-brand-blue-700">
                      <span v-if="!s.data.code || s.data.code === '制定中'" class="text-ink-500">—</span>
                      <template v-else>{{ s.data.code }}<sup v-if="s.data.codeSource === 'ocr'" title="编号据证明材料识别，待核实">†</sup></template>
                    </td>
                    <td class="px-4 py-3">{{ s.title }}</td>
                    <td class="px-4 py-3 whitespace-nowrap"><span :class="['rounded-xs px-2 py-0.5 text-xs', STD_STATUS[s.data.status]?.tone === 'ok' ? 'bg-[#E6F4EC] text-success' : STD_STATUS[s.data.status]?.tone === 'warn' ? 'bg-[#FFF4E0] text-warning' : 'bg-paper text-ink-500']">{{ STD_STATUS[s.data.status]?.label || s.data.status }}</span></td>
                    <td class="px-4 py-3 whitespace-nowrap text-ink-600">{{ s.data.role }}</td>
                    <td class="px-4 py-3">
                      <span class="flex gap-2">
                        <button v-for="(im, i) in s.data.images" :key="i" type="button" class="link text-xs" :aria-label="`查看《${s.title}》证明材料 ${i + 1}`"
                                @click="lightbox = { src: im.src, alt: s.title }">查看{{ s.data.images.length > 1 ? i + 1 : '' }}</button>
                        <span v-if="!s.data.images?.length" class="text-ink-500">—</span>
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p class="mt-3 text-xs text-ink-500">† 标准编号据证明材料识别整理，以标准发布机构公告为准。</p>
          </TabsContent>

          <TabsContent value="patents">
            <div class="grid grid-cols-2 gap-4 md:grid-cols-4 xl:grid-cols-6">
              <DocCard v-for="p in patents.items" :key="p.slug" :title="p.title" :image="p.data.image" :meta="p.data.number"
                       :badge="`${PATENT_KIND[p.data.kind] || ''} · ${PATENT_STATE[p.data.state] || ''}`" :badge-tone="p.data.state === 'granted' ? 'ok' : 'muted'"
                       @open="lightbox = $event" />
            </div>
          </TabsContent>

          <TabsContent value="copyrights">
            <div class="grid grid-cols-2 gap-4 md:grid-cols-4 xl:grid-cols-6">
              <DocCard v-for="p in copyrights.items" :key="p.slug" :title="p.title" :image="p.data.image" :meta="`${p.data.regNo}`" @open="lightbox = $event" />
            </div>
          </TabsContent>

          <TabsContent value="projects">
            <p class="mb-4 text-sm text-ink-600">共 {{ projects.total }} 项国家级与省级科研项目，合同经费合计约 <span class="font-latin font-semibold">{{ projAmount.toFixed(0) }}</span> 万元。</p>
            <div class="relative overflow-x-auto rounded-sm border border-line-200 bg-white">
              <table class="w-full min-w-[760px] text-left text-sm">
                <thead class="bg-paper"><tr>
                  <th scope="col" class="px-4 py-3 font-semibold">年份</th>
                  <th scope="col" class="px-4 py-3 font-semibold">项目名称</th>
                  <th scope="col" class="px-4 py-3 font-semibold">级别 / 来源</th>
                  <th scope="col" class="px-4 py-3 font-semibold">角色</th>
                  <th scope="col" class="px-4 py-3 font-semibold">状态</th>
                </tr></thead>
                <tbody>
                  <tr v-for="p in projects.items" :key="p.slug" class="border-t border-line-200 align-top">
                    <td class="font-latin px-4 py-3">{{ p.data.year }}</td>
                    <td class="px-4 py-3">{{ p.title }}</td>
                    <td class="px-4 py-3 text-ink-600">{{ PROJECT_LEVEL[p.data.level] }} · {{ p.data.source }}</td>
                    <td class="px-4 py-3 whitespace-nowrap text-ink-600">{{ p.data.role }}</td>
                    <td class="px-4 py-3 whitespace-nowrap">{{ PROJECT_STATUS[p.data.status] || p.data.status }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </TabsContent>
        </TabsRoot>
      </div>
    </section>
    <CtaBand />
    <Lightbox v-model="lightbox" />
  </div>
</template>
