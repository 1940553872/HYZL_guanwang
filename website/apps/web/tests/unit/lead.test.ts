import { describe, expect, it } from 'vitest'
import { normalizePhone, validateLead } from '~/utils/lead'

const base = { name: '张工', company: '某能源集团', title: '', phone: '13800138000', email: '', scenario: '', consent: true }

describe('validateLead', () => {
  it('accepts a complete form', () => {
    expect(validateLead(base)).toEqual({})
  })
  it('requires phone or email', () => {
    expect(validateLead({ ...base, phone: '' }).phone).toBe('手机号或邮箱至少填写一项')
    expect(validateLead({ ...base, phone: '', email: 'a@b.cn' })).toEqual({})
  })
  it('rejects malformed phone and email', () => {
    expect(validateLead({ ...base, phone: '12345' }).phone).toBe('手机号格式不正确')
    expect(validateLead({ ...base, email: 'not-an-email' }).email).toBe('邮箱格式不正确')
  })
  it('accepts landlines and +86 prefixes', () => {
    expect(validateLead({ ...base, phone: '029-88810623' })).toEqual({})
    expect(validateLead({ ...base, phone: '+86 138 0013 8000' })).toEqual({})
  })
  it('requires consent and required fields', () => {
    const e = validateLead({ ...base, name: ' ', company: '', consent: false })
    expect(e.name).toBe('请填写姓名')
    expect(e.company).toBe('请填写公司名称')
    expect(e.consent).toBe('请阅读并同意隐私政策')
  })
  it('limits scenario length to 500', () => {
    expect(validateLead({ ...base, scenario: 'x'.repeat(501) }).scenario).toBe('需求描述不超过500个字')
  })
})

describe('normalizePhone', () => {
  it('handles full-width digits and prefixes', () => {
    expect(normalizePhone('＋86 １３８００１３８０００'.replace('＋', '+'))).toBe('13800138000')
    expect(normalizePhone('0086(138)0013 8000')).toBe('13800138000')
  })
})
