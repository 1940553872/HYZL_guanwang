import { z } from 'zod'

// 留资表单校验（与后端 LeadRequest / LeadService.normalizePhone 规则一致，K-05 §2.2）
export const PHONE_RE = /^(1[3-9]\d{9}|0\d{2,3}-?\d{7,8})$/

/** 去掉空格、括号与 +86 / 0086 前缀，全角数字转半角。 */
export function normalizePhone(v: string): string {
  return v
    .replace(/[０-９]/g, (d) => String.fromCharCode(d.charCodeAt(0) - 0xfee0))
    .replace(/[\s()（）]/g, '')
    .replace(/^(\+86|0086)/, '')
}

export const leadSchema = z.object({
  name: z.string().trim().min(1, '请填写姓名').max(50, '姓名不超过50个字'),
  company: z.string().trim().min(1, '请填写公司名称').max(100, '公司名称不超过100个字'),
  title: z.string().trim().max(50, '职位不超过50个字'),
  phone: z.string().trim().refine((v) => !v || PHONE_RE.test(normalizePhone(v)), '手机号格式不正确'),
  email: z.string().trim().refine((v) => !v || z.email().safeParse(v).success, '邮箱格式不正确'),
  scenario: z.string().max(500, '需求描述不超过500个字'),
  consent: z.literal(true, { error: '请阅读并同意隐私政策' }),
})

/** 校验并返回 { 字段: 首条错误 }；通过时返回空对象。 */
export function validateLead(form: Record<string, unknown>): Record<string, string> {
  const r = leadSchema.safeParse(form)
  const errors: Record<string, string> = {}
  if (!r.success) {
    for (const i of r.error.issues) {
      const k = String(i.path[0])
      if (!errors[k]) errors[k] = i.message
    }
  }
  // “至少一项”放在对象校验之外，保证与其他字段错误同时提示
  const phone = String(form.phone ?? '').trim()
  const email = String(form.email ?? '').trim()
  if (!phone && !email && !errors.phone) errors.phone = '手机号或邮箱至少填写一项'
  return errors
}
