import { describe, expect, it } from 'vitest'
import { formatDate, productPath } from '~/utils/links'

describe('productPath', () => {
  it('maps every product category to its route (K-02 §2.1)', () => {
    expect(productPath({ slug: 'imom', category: 'platform' })).toBe('/products')
    expect(productPath({ slug: 'spatigo', category: 'flagship' })).toBe('/products/spatigo')
    expect(productPath({ slug: 'spatigo-quality', category: 'sub_product' })).toBe('/products/spatigo/quality')
    expect(productPath({ slug: 'imllm', category: 'model' })).toBe('/products/imllm')
    expect(productPath({ slug: 'quality-agent', category: 'agent' })).toBe('/products/agents/quality-agent')
    expect(productPath({ slug: 'idce', category: 'engine' })).toBe('/products/engines#idce')
    expect(productPath({ slug: 'imes', category: 'software' })).toBe('/products/software/imes')
    expect(productPath({ slug: 'security-integration', category: 'security' })).toBe('/products/security-integration')
  })
  it('falls back to the product hub for unknown categories', () => {
    expect(productPath({ slug: 'x' })).toBe('/products')
  })
})

describe('formatDate', () => {
  it('formats ISO dates in Chinese without leading zeros', () => {
    expect(formatDate('2026-07-02')).toBe('2026年7月2日')
    expect(formatDate(undefined)).toBe('')
  })
})
