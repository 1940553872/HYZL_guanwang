export default defineEventHandler((event) => {
  const { public: pub } = useRuntimeConfig(event)
  setHeader(event, 'content-type', 'text/plain; charset=utf-8')
  return `User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /search\nSitemap: ${pub.siteUrl}/sitemap.xml\n`
})
