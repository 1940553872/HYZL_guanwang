<script setup lang="ts">
// 24×24 线性图标，1.5px 线宽，currentColor（K-01 §2.8）
const props = withDefaults(defineProps<{ name: string; size?: number }>(), { size: 24 })
const paths: Record<string, string> = {
  arrow: 'M5 12h14M13 6l6 6-6 6',
  'arrow-up': 'M12 19V5M6 11l6-6 6 6',
  phone: 'M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2',
  mail: 'M3 6h18v12H3zM3 7l9 6 9-6',
  map: 'M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11zM12 12a2 2 0 1 0 0-4 2 2 0 0 0 0 4',
  search: 'M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM20 20l-4-4',
  menu: 'M4 7h16M4 12h16M4 17h16',
  close: 'M6 6l12 12M18 6L6 18',
  chat: 'M4 5h16v11H9l-5 4z',
  calendar: 'M4 6h16v14H4zM4 10h16M8 3v4M16 3v4',
  check: 'M5 12l5 5 9-10',
  download: 'M12 4v11M7 10l5 5 5-5M5 20h14',
  wechat: 'M9 4C5 4 2 6.7 2 10c0 1.9 1 3.6 2.6 4.7L4 17l2.6-1.3c.8.2 1.6.3 2.4.3M15 9c-3.3 0-6 2.2-6 5s2.7 5 6 5c.7 0 1.4-.1 2-.3L19 20l-.5-2c1.5-1 2.5-2.4 2.5-4 0-2.8-2.7-5-6-5',
  chevron: 'M6 9l6 6 6-6',
  external: 'M14 4h6v6M20 4l-9 9M18 14v6H4V6h6',
  quality: 'M4 20V10M10 20V4M16 20v-7M22 20H2M16 9l3-3 3 3',
  maintenance: 'M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z',
  safety: 'M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6zM9 12l2 2 4-4',
  embodied: 'M7 15h10l2 4H5zM9 15V9h6v6M12 9V5M9 5h6M7 19a2 2 0 1 0 0 .1M17 19a2 2 0 1 0 0 .1',
  layers: 'M12 3l9 5-9 5-9-5zM3 13l9 5 9-5M3 17l9 5 9-5',
  cpu: 'M7 7h10v10H7zM10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4',
  shield: 'M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z',
  doc: 'M6 3h9l4 4v14H6zM14 3v5h5M9 12h7M9 16h7',
  award: 'M12 15a6 6 0 1 0 0-12 6 6 0 0 0 0 12zM8.5 13.5L7 22l5-3 5 3-1.5-8.5',
  factory: 'M3 21V10l6 4V10l6 4V6l6 3v12zM3 21h18',
  play: 'M8 5v14l11-7z',
  pause: 'M8 5h3v14H8zM13 5h3v14h-3z',
}
</script>

<template>
  <svg :width="props.size" :height="props.size" viewBox="0 0 24 24" fill="none" stroke="currentColor"
       stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
    <path :d="paths[props.name] ?? ''" />
  </svg>
</template>
