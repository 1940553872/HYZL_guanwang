// 状态与分类显示名（标准 / 专利 / 项目 / 合作单位）
export const STD_STATUS: Record<string, { label: string; tone: 'ok' | 'warn' | 'muted' }> = {
  published: { label: '已发布', tone: 'ok' },
  project: { label: '已立项', tone: 'warn' },
  drafting: { label: '编制中', tone: 'muted' },
  proof: { label: '编制证明', tone: 'muted' },
}
export const PATENT_KIND: Record<string, string> = { invention: '发明专利', utility: '实用新型', design: '外观设计' }
export const PATENT_STATE: Record<string, string> = { granted: '已授权', pending: '实审中' }
export const PROJECT_LEVEL: Record<string, string> = { national: '国家级', provincial: '省级' }
export const PROJECT_STATUS: Record<string, string> = { closed: '已结题', ongoing: '在研' }
export const PARTNER_CAT: Record<string, string> = {
  university: '高校',
  research: '科研院所与机构',
  industry: '行业企业',
  integrator: '技术与集成伙伴',
}
