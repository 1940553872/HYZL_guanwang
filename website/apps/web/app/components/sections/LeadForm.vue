<script setup lang="ts">
import { validateLead } from '~/utils/lead'
// 留资表单（K-02 §3.1 / K-04 §3 / K-05 §2.2）：手机号或邮箱至少一项、隐私勾选、蜜罐、提交失败保留已填内容
const props = withDefaults(defineProps<{ type?: 'demo' | 'contact' | 'partner'; submitLabel?: string }>(), {
  type: 'demo',
  submitLabel: '提交预约',
})
const { public: pub } = useRuntimeConfig()
const route = useRoute()
const staticDemo = !!pub.staticDemo

const PRODUCTS = [
  { value: 'spatigo', label: '空间群弈™ SpatiGo™（整体）' },
  { value: 'spatigo-quality', label: '质量之弈' },
  { value: 'spatigo-maintenance', label: '运维之弈' },
  { value: 'spatigo-safety', label: '安全之弈' },
  { value: 'spatigo-embodied', label: '具身之弈' },
  { value: 'imllm', label: '工业增强大模型 iMLLM' },
  { value: 'agents', label: '工业智能体应用' },
  { value: 'software', label: '工业软件（iMES、iQMS 等）' },
  { value: 'imom', label: '盘古华云智能工厂平台' },
  { value: 'other', label: '其他 / 暂不确定' },
]
const pre = String(route.query.product || '')

const form = reactive({
  name: '',
  company: '',
  title: '',
  phone: '',
  email: '',
  productInterest: PRODUCTS.some((p) => p.value === pre) ? pre : (pre ? 'other' : ''),
  scenario: '',
  consent: false,
  website: '',
})

const errors = ref<Record<string, string>>({})
const status = ref<'idle' | 'sending' | 'done' | 'error'>('idle')
const serverMsg = ref('')
const formEl = ref<HTMLFormElement>()

function focusFirstError() {
  nextTick(() => {
    const first = Object.keys(errors.value)[0]
    if (first) formEl.value?.querySelector<HTMLElement>(`[name="${first}"]`)?.focus()
  })
}

async function submit() {
  errors.value = {}
  serverMsg.value = ''
  errors.value = validateLead(form)
  if (Object.keys(errors.value).length) {
    focusFirstError()
    return
  }
  if (staticDemo) {
    // 静态演示包没有后端：只演示校验与成功状态，不提交任何数据
    status.value = 'done'
    return
  }
  status.value = 'sending'
  try {
    await $fetch('/api/v1/leads', {
      method: 'POST',
      body: {
        type: props.type,
        name: form.name.trim(),
        company: form.company.trim(),
        title: form.title.trim() || null,
        phone: form.phone.trim() || null,
        email: form.email.trim() || null,
        productInterest: form.productInterest || null,
        scenario: form.scenario.trim() || null,
        locale: 'zh',
        sourcePage: route.fullPath,
        utmSource: route.query.utm_source || null,
        utmMedium: route.query.utm_medium || null,
        utmCampaign: route.query.utm_campaign || null,
        consent: form.consent,
        consentVersion: '2026-10',
        website: form.website,
      },
    })
    status.value = 'done'
  } catch (e: any) {
    status.value = 'error'
    const body = e?.data
    if (e?.statusCode === 429) serverMsg.value = '提交过于频繁，请稍后再试，或直接拨打热线。'
    else if (body?.details?.length) {
      for (const d of body.details) if (d.field && !errors.value[d.field]) errors.value[d.field] = d.message
      serverMsg.value = body.message || '请检查填写内容'
      focusFirstError()
    } else serverMsg.value = body?.message || '网络异常，提交未成功。已填写的内容已保留，请重试或拨打热线。'
  }
}

const field = 'mt-1.5 block h-11 w-full rounded-sm border bg-white px-3 text-base outline-none transition-colors focus:border-brand-blue-700'
const cls = (k: string) => [field, errors.value[k] ? 'border-danger' : 'border-line-300']
</script>

<template>
  <div v-if="status === 'done'" class="card p-8 text-center" role="status">
    <span class="mx-auto inline-flex size-14 items-center justify-center rounded-full bg-[#E6F4EC] text-success"><UiIcon name="check" :size="28" /></span>
    <h2 class="mt-4 text-2xl">提交成功</h2>
    <p v-if="staticDemo" class="mt-2 text-sm text-warning">（演示版：表单校验已通过，演示环境不会保存或发送任何数据）</p>
    <p class="mt-3 text-ink-600">我们的工程师将在 <strong>1 个工作日内</strong> 与您联系。紧急需求请直接拨打 7×24 热线：</p>
    <a :href="`tel:${pub.hotline}`" class="font-latin mt-2 inline-block text-2xl font-bold text-brand-blue-700">{{ pub.hotline }}</a>
    <div class="mt-6 flex flex-wrap justify-center gap-3">
      <UiButton to="/cases" variant="secondary">先看看客户案例</UiButton>
      <UiButton to="/" variant="text" arrow>返回首页</UiButton>
    </div>
  </div>

  <form v-else ref="formEl" novalidate class="card space-y-5 p-6 md:p-8" @submit.prevent="submit">
    <p class="text-sm text-ink-500"><span class="text-danger">*</span> 为必填项；手机号与邮箱至少填写一项。</p>
    <div class="grid gap-5 md:grid-cols-2">
      <div>
        <label for="lf-name" class="text-sm font-medium">姓名 <span class="text-danger">*</span></label>
        <input id="lf-name" v-model="form.name" name="name" autocomplete="name" maxlength="50" :class="cls('name')"
               :aria-invalid="!!errors.name" aria-describedby="lf-name-err">
        <p v-if="errors.name" id="lf-name-err" class="mt-1 text-sm text-danger">{{ errors.name }}</p>
      </div>
      <div>
        <label for="lf-company" class="text-sm font-medium">公司名称 <span class="text-danger">*</span></label>
        <input id="lf-company" v-model="form.company" name="company" autocomplete="organization" maxlength="100" :class="cls('company')"
               :aria-invalid="!!errors.company" aria-describedby="lf-company-err">
        <p v-if="errors.company" id="lf-company-err" class="mt-1 text-sm text-danger">{{ errors.company }}</p>
      </div>
      <div>
        <label for="lf-phone" class="text-sm font-medium">手机号</label>
        <input id="lf-phone" v-model="form.phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" maxlength="20" :class="cls('phone')"
               :aria-invalid="!!errors.phone" aria-describedby="lf-phone-err">
        <p v-if="errors.phone" id="lf-phone-err" class="mt-1 text-sm text-danger">{{ errors.phone }}</p>
      </div>
      <div>
        <label for="lf-email" class="text-sm font-medium">邮箱</label>
        <input id="lf-email" v-model="form.email" name="email" type="email" autocomplete="email" maxlength="120" :class="cls('email')"
               :aria-invalid="!!errors.email" aria-describedby="lf-email-err">
        <p v-if="errors.email" id="lf-email-err" class="mt-1 text-sm text-danger">{{ errors.email }}</p>
      </div>
      <div>
        <label for="lf-title" class="text-sm font-medium">职位</label>
        <input id="lf-title" v-model="form.title" name="title" autocomplete="organization-title" maxlength="50" :class="cls('title')">
        <p v-if="errors.title" class="mt-1 text-sm text-danger">{{ errors.title }}</p>
      </div>
      <div>
        <label for="lf-product" class="text-sm font-medium">关注产品 / 场景</label>
        <select id="lf-product" v-model="form.productInterest" name="productInterest" :class="cls('productInterest')">
          <option value="">请选择</option>
          <option v-for="p in PRODUCTS" :key="p.value" :value="p.value">{{ p.label }}</option>
        </select>
      </div>
    </div>
    <div>
      <label for="lf-scenario" class="text-sm font-medium">现场问题 / 需求描述（选填）</label>
      <textarea id="lf-scenario" v-model="form.scenario" name="scenario" rows="4" maxlength="500"
                placeholder="例如：某条产线质量波动原因难以定位，希望了解质量之弈的现场效果"
                :class="[...cls('scenario'), 'h-auto py-2']" />
      <p class="mt-1 flex justify-between text-xs text-ink-500">
        <span class="text-danger">{{ errors.scenario }}</span><span class="font-latin">{{ form.scenario.length }}/500</span>
      </p>
    </div>
    <!-- 蜜罐字段：对用户与读屏隐藏 -->
    <div class="absolute -left-[9999px]" aria-hidden="true">
      <label for="lf-website">网站</label>
      <input id="lf-website" v-model="form.website" name="website" tabindex="-1" autocomplete="off">
    </div>
    <div>
      <label class="flex items-start gap-2 text-sm text-ink-600">
        <input v-model="form.consent" name="consent" type="checkbox" class="mt-1 size-4 accent-brand-blue-700" :aria-invalid="!!errors.consent">
        <span>我已阅读并同意 <NuxtLink to="/legal/privacy" target="_blank" class="link">《隐私政策》</NuxtLink>，同意华云智联就本次咨询与我联系。</span>
      </label>
      <p v-if="errors.consent" class="mt-1 text-sm text-danger">{{ errors.consent }}</p>
    </div>
    <p v-if="serverMsg" class="rounded-sm border border-danger/30 bg-[#FDECEA] px-4 py-3 text-sm text-danger" role="alert">
      {{ serverMsg }} 热线 <a :href="`tel:${pub.hotline}`" class="font-latin font-semibold underline">{{ pub.hotline }}</a>
    </p>
    <div class="flex flex-wrap items-center gap-4">
      <UiButton type="submit" size="lg" :loading="status === 'sending'">{{ submitLabel }}</UiButton>
      <span class="text-sm text-ink-500">个人信息加密存储，仅用于本次联系。</span>
    </div>
  </form>
</template>
