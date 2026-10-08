import tailwindcss from '@tailwindcss/vite'

// 华云智联官网 V2.0 前端配置（design_document/K-04）
export default defineNuxtConfig({
  compatibilityDate: '2026-10-01',
  devtools: { enabled: false },
  css: ['~/assets/css/main.css'],
  // 组件按文件名注册（不加目录前缀），如 components/ui/PageHero.vue → <PageHero>
  components: [{ path: '~/components', pathPrefix: false }],
  vite: { plugins: [tailwindcss()] },

  app: {
    head: {
      htmlAttrs: { lang: 'zh-CN' },
      titleTemplate: '%s｜华云智联',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1, viewport-fit=cover' },
        // 国产双核浏览器强制极速内核（K-04 §2.4）
        { name: 'renderer', content: 'webkit' },
        { 'http-equiv': 'X-UA-Compatible', content: 'IE=edge' },
        { name: 'theme-color', content: '#0A1A3F' },
        { name: 'format-detection', content: 'telephone=no' },
      ],
      link: [
        { rel: 'icon', type: 'image/png', href: '/favicon.png' },
        { rel: 'apple-touch-icon', href: '/favicon.png' },
      ],
    },
  },

  runtimeConfig: {
    // 服务端访问内容与业务服务的地址（NUXT_API_BASE 覆盖）
    apiBase: 'http://127.0.0.1:8080',
    public: {
      siteUrl: 'http://localhost:3000', // NUXT_PUBLIC_SITE_URL
      hotline: '029-88810623',
      icp: '陕ICP备2026024028号-1',
    },
  },

  routeRules: {
    // 旧站 URL 301（design_document/03 §5）
    '/index.html': { redirect: { to: '/', statusCode: 301 } },
    '/news.html': { redirect: { to: '/news', statusCode: 301 } },
    '/product.html': { redirect: { to: '/products', statusCode: 301 } },
    '/lab.html': { redirect: { to: '/research/labs', statusCode: 301 } },
    '/service.html': { redirect: { to: '/support', statusCode: 301 } },
    '/about.html': { redirect: { to: '/about', statusCode: 301 } },
    '/media/**': { headers: { 'cache-control': 'public, max-age=2592000' } },
  },

  nitro: {
    compressPublicAssets: true,
  },

  experimental: {
    // 使用 Vite Environment API 构建：客户端清单在内存中内联到服务端包，
    // 不再通过绝对路径 import .nuxt/dist/server/client.precomputed.mjs（该方式在 Windows 上会得到空清单，
    // 运行时报 “Either manifest or precomputed data must be provided”）
    viteEnvironmentApi: true,
  },

  typescript: { strict: true },
})
