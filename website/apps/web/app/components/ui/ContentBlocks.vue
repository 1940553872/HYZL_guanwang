<script setup lang="ts">
import type { Block } from '~/utils/types'
// 渲染结构化正文：段落 / 小标题 / 能力条目（标签：说明）/ 图片（点击放大）
const props = defineProps<{ blocks: Block[]; capLayout?: 'grid' | 'list' }>()
const lightbox = ref<{ src: string; alt?: string } | null>(null)

// 连续的 cap 条目合并为一组，便于按网格展示
const groups = computed(() => {
  const out: { kind: 'caps' | 'single'; items: Block[] }[] = []
  for (const b of props.blocks) {
    if (b.t === 'cap') {
      const last = out[out.length - 1]
      if (last && last.kind === 'caps') last.items.push(b)
      else out.push({ kind: 'caps', items: [b] })
    } else {
      out.push({ kind: 'single', items: [b] })
    }
  }
  return out
})
</script>

<template>
  <div class="space-y-6">
    <template v-for="(g, gi) in groups" :key="gi">
      <div v-if="g.kind === 'caps'" :class="capLayout === 'list' ? 'space-y-4' : 'grid grid-cols-1 gap-4 md:grid-cols-2'">
        <div v-for="(c, ci) in g.items" :key="ci" class="card p-6">
          <h4 class="mb-2 flex items-start gap-2 text-lg">
            <span class="mt-2.5 inline-block size-1.5 shrink-0 bg-brand-orange-500" aria-hidden="true" />
            {{ (c as any).label }}
          </h4>
          <p class="text-[15px] leading-7 text-ink-600">{{ (c as any).text }}</p>
        </div>
      </div>
      <template v-else>
        <template v-for="(b, bi) in g.items" :key="bi">
          <h3 v-if="b.t === 'h'" class="pt-4 text-xl md:text-[22px]">{{ b.text }}</h3>
          <p v-else-if="b.t === 'p'" class="text-[15px] leading-7 text-ink-600 md:text-base md:leading-8">{{ b.text }}</p>
          <figure v-else-if="b.t === 'img'" class="card overflow-hidden">
            <button type="button" class="block w-full cursor-zoom-in" :aria-label="`放大查看：${b.alt || '图片'}`"
                    @click="lightbox = { src: b.src, alt: b.alt }">
              <img :src="b.src" :alt="b.alt || ''" :width="b.w" :height="b.h" loading="lazy" decoding="async" class="w-full">
            </button>
            <figcaption v-if="b.alt" class="border-t border-line-200 px-4 py-2 text-sm text-ink-500">{{ b.alt }}</figcaption>
          </figure>
        </template>
      </template>
    </template>
    <Lightbox v-model="lightbox" />
  </div>
</template>
