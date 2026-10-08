<script setup lang="ts">
// 相关产品互链（每个详情页底部至少 2 个相关推荐，K-02 §2.1）
const props = withDefaults(defineProps<{ slugs: string[]; title?: string }>(), { title: '相关产品' })
const { pick } = await useProducts()
const items = computed(() => pick(props.slugs))
</script>

<template>
  <section v-if="items.length" class="section bg-white">
    <div class="container-site">
      <SectionHeader eyebrow="Related" :title="title" />
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <ProductCard v-for="p in items" :key="p.slug" :item="p" />
      </div>
    </div>
  </section>
</template>
