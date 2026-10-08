<script setup lang="ts">
// P-71 资质荣誉：证书（有效期 / 状态）、奖项；知识产权链接至 P-50
const [{ data: certs }, { data: awards }] = await Promise.all([useContentList('certificate'), useContentList('award')])
const lightbox = ref<{ src: string; alt?: string } | null>(null)
usePageSeo({ title: '资质荣誉', description: '华云智联资质证书、体系认证与所获奖项。' })
</script>

<template>
  <div>
    <PageHero title="资质荣誉" eyebrow="Certificates & Awards" lead="展示仍在有效期内的资质证书与历年所获奖项；专利、软件著作权与标准见“标准与研究”。"
              :crumbs="[{ name: '关于我们', to: '/about' }, { name: '资质荣誉' }]">
      <UiButton to="/research?tab=patents" variant="ghost">专利与软著</UiButton>
    </PageHero>
    <section class="section bg-white">
      <div class="container-site">
        <SectionHeader eyebrow="Certificates" title="资质与体系认证" />
        <div class="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
          <DocCard v-for="c in certs.items" :key="c.slug" :title="c.title" :image="c.data.image"
                   :meta="[c.data.number, c.expiresAt ? `有效期至 ${c.expiresAt}` : ''].filter(Boolean).join(' · ')"
                   :badge="c.status === 'expiring' ? '即将到期' : '有效'" :badge-tone="c.status === 'expiring' ? 'warn' : 'ok'" @open="lightbox = $event" />
        </div>
      </div>
    </section>
    <section class="section bg-paper">
      <div class="container-site">
        <SectionHeader eyebrow="Awards" title="所获奖项" />
        <div class="grid grid-cols-2 gap-4 md:grid-cols-4 xl:grid-cols-7">
          <DocCard v-for="a in awards.items" :key="a.slug" :title="a.title" :image="a.data.image" :meta="`${a.data.year} · ${a.data.grade}`" @open="lightbox = $event" />
        </div>
      </div>
    </section>
    <Lightbox v-model="lightbox" />
  </div>
</template>
