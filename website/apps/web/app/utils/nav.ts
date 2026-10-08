// 全站导航结构（design_document/K-02 §2.2）
export interface NavLink { label: string; to: string; desc?: string; icon?: string }
export interface NavColumn { title: string; links: NavLink[] }
export interface NavItem { label: string; to: string; columns?: NavColumn[]; promo?: { title: string; text: string; to: string } }

export const NAV: NavItem[] = [
  {
    label: '产品与技术',
    to: '/products',
    columns: [
      {
        title: '平台',
        links: [
          { label: '平台总览 7+10+2+N', to: '/products', desc: '盘古华云智能工厂平台 iMoM 3.2' },
          { label: '工业增强大模型 iMLLM', to: '/products/imllm', desc: '多模态判别式工业大模型' },
          { label: '智能引擎群', to: '/products/engines', desc: '7 组工业智能引擎' },
          { label: '安全与集成', to: '/products/security-integration', desc: '工业协议、数据安全与接口' },
        ],
      },
      {
        title: '旗舰 · 空间群弈™ SpatiGo™',
        links: [
          { label: '质量之弈', to: '/products/spatigo/quality', desc: '质量波动找不到原因？', icon: 'quality' },
          { label: '运维之弈', to: '/products/spatigo/maintenance', desc: '设备总在计划外停机？', icon: 'maintenance' },
          { label: '安全之弈', to: '/products/spatigo/safety', desc: '高危作业还靠人盯？', icon: 'safety' },
          { label: '具身之弈', to: '/products/spatigo/embodied', desc: '巡检进不去、看不全？', icon: 'embodied' },
        ],
      },
      {
        title: '应用与软件',
        links: [
          { label: '工业智能体应用', to: '/products/agents', desc: '7 类工业智能体' },
          { label: '工业软件', to: '/products/software', desc: '标准软件与高级软件' },
        ],
      },
    ],
    promo: { title: '预约 SpatiGo™ 现场演示', text: '带一个现场问题来，我们用智能体给出答案。', to: '/demo?product=spatigo' },
  },
  {
    label: '解决方案',
    to: '/solutions',
    columns: [
      {
        title: '按行业',
        links: [
          { label: '矿山与电力', to: '/solutions/mining-power' },
          { label: '石油化工', to: '/solutions/petrochemical' },
          { label: '航空航天与装备制造', to: '/solutions/aerospace-equipment' },
          { label: '钢铁冶金', to: '/solutions/steel-metallurgy' },
          { label: '烟草与食药制造', to: '/solutions/tobacco-food' },
          { label: '水务与市政', to: '/solutions/water-municipal' },
        ],
      },
      {
        title: '按场景',
        links: [
          { label: '质量提升与工艺优化', to: '/products/spatigo/quality' },
          { label: '设备健康与预测性维护', to: '/products/spatigo/maintenance' },
          { label: '安全生产与特种作业', to: '/products/spatigo/safety' },
          { label: '无人巡检与具身作业', to: '/products/spatigo/embodied' },
          { label: '生产经营管理', to: '/products/agents/production-agent' },
          { label: '安全应急', to: '/products/agents/emergency-agent' },
        ],
      },
    ],
  },
  { label: '客户案例', to: '/cases' },
  { label: '标准与研究', to: '/research' },
  { label: '服务支持', to: '/support' },
  { label: '新闻中心', to: '/news' },
  {
    label: '关于我们',
    to: '/about',
    columns: [
      {
        title: '关于我们',
        links: [
          { label: '公司介绍', to: '/about' },
          { label: '资质荣誉', to: '/about/honors' },
          { label: '合作伙伴', to: '/about/partners' },
          { label: '联系我们', to: '/about/contact' },
          { label: '加入我们', to: '/about/careers' },
        ],
      },
    ],
  },
]

export const FOOTER_COLUMNS: NavColumn[] = [
  {
    title: '产品与技术',
    links: [
      { label: '平台总览', to: '/products' },
      { label: '空间群弈™ SpatiGo™', to: '/products/spatigo' },
      { label: '工业增强大模型 iMLLM', to: '/products/imllm' },
      { label: '工业智能体应用', to: '/products/agents' },
      { label: '智能引擎群', to: '/products/engines' },
      { label: '工业软件', to: '/products/software' },
    ],
  },
  {
    title: '解决方案与案例',
    links: [
      { label: '解决方案', to: '/solutions' },
      { label: '客户案例', to: '/cases' },
      { label: '标准与研究', to: '/research' },
      { label: '联合实验室', to: '/research/labs' },
    ],
  },
  {
    title: '服务与资讯',
    links: [
      { label: '服务支持', to: '/support' },
      { label: '新闻中心', to: '/news' },
      { label: '预约现场演示', to: '/demo' },
    ],
  },
  {
    title: '关于我们',
    links: [
      { label: '公司介绍', to: '/about' },
      { label: '资质荣誉', to: '/about/honors' },
      { label: '合作伙伴', to: '/about/partners' },
      { label: '加入我们', to: '/about/careers' },
      { label: '联系我们', to: '/about/contact' },
    ],
  },
]
