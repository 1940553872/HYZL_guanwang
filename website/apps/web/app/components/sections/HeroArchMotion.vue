<script setup lang="ts">
// 首页首屏动效：“人在回路”监管—执行智能体集群示意（纯 SVG + CSS，可暂停，尊重减少动态效果）
const paused = ref(false)
const sup = [
  { x: 120, y: 90, label: '质量之弈' },
  { x: 400, y: 90, label: '运维之弈' },
  { x: 120, y: 330, label: '安全之弈' },
  { x: 400, y: 330, label: '具身之弈' },
]
const exec = [
  [40, 30], [200, 20], [320, 20], [480, 30], [30, 210], [490, 210], [40, 390], [200, 400], [320, 400], [480, 390],
] as const
function nearest(p: readonly [number, number]) {
  return sup.reduce((a, b) => (Math.hypot(b.x - p[0], b.y - p[1]) < Math.hypot(a.x - p[0], a.y - p[1]) ? b : a))
}
</script>

<template>
  <div :class="['hero-motion relative', paused && 'is-paused']">
    <svg viewBox="0 0 520 420" class="h-auto w-full" role="img" aria-labelledby="hm-title">
      <title id="hm-title">空间群弈™ 监管—执行智能体集群示意：中心为工业增强大模型与世界模型，四个监管智能体调度外围执行智能体，人在回路</title>
      <defs>
        <radialGradient id="hm-core" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#ED6E37" stop-opacity=".55" />
          <stop offset="100%" stop-color="#ED6E37" stop-opacity="0" />
        </radialGradient>
      </defs>
      <!-- 执行层连线 -->
      <g stroke="#7FA3E6" stroke-opacity=".35" stroke-width="1">
        <line v-for="(p, i) in exec" :key="`e${i}`" :x1="p[0]" :y1="p[1]" :x2="nearest(p).x" :y2="nearest(p).y" />
      </g>
      <!-- 监管层到核心的数据流 -->
      <g stroke="#ED6E37" stroke-width="1.5" fill="none">
        <line v-for="(s, i) in sup" :key="`s${i}`" :x1="s.x" :y1="s.y" x2="260" y2="210" class="flow" :style="{ animationDelay: `${i * 0.4}s` }" />
      </g>
      <circle cx="260" cy="210" r="110" fill="url(#hm-core)" class="pulse" />
      <circle cx="260" cy="210" r="96" fill="none" stroke="#7FA3E6" stroke-opacity=".25" stroke-dasharray="2 6" class="spin" />
      <!-- 核心 -->
      <g>
        <rect x="190" y="172" width="140" height="76" rx="4" fill="#12285A" stroke="#ED6E37" />
        <text x="260" y="203" text-anchor="middle" fill="#F2F4F8" font-size="15" font-weight="700">LLM — WM</text>
        <text x="260" y="226" text-anchor="middle" fill="#A9B6CF" font-size="12">人在回路 · HITL</text>
      </g>
      <!-- 监管智能体 -->
      <g v-for="(s, i) in sup" :key="`n${i}`">
        <rect :x="s.x - 54" :y="s.y - 20" width="108" height="40" rx="4" fill="#0A1A3F" stroke="#7FA3E6" stroke-opacity=".8" />
        <text :x="s.x" :y="s.y + 5" text-anchor="middle" fill="#F2F4F8" font-size="13">{{ s.label }}</text>
      </g>
      <!-- 执行智能体 -->
      <g v-for="(p, i) in exec" :key="`x${i}`">
        <circle :cx="p[0]" :cy="p[1]" r="7" fill="#05348E" stroke="#7FA3E6" />
        <circle :cx="p[0]" :cy="p[1]" r="2.5" fill="#ED6E37" class="blink" :style="{ animationDelay: `${(i % 5) * 0.5}s` }" />
      </g>
    </svg>
    <button type="button" class="absolute right-0 bottom-0 inline-flex size-9 items-center justify-center rounded-full border border-white/30 text-on-dark hover:bg-white/10"
            :aria-label="paused ? '播放动画' : '暂停动画'" :aria-pressed="paused" @click="paused = !paused">
      <UiIcon :name="paused ? 'play' : 'pause'" :size="16" />
    </button>
  </div>
</template>

<style scoped>
.flow { stroke-dasharray: 6 10; animation: flow 1.6s linear infinite; }
.pulse { transform-origin: 260px 210px; animation: pulse 3.2s ease-in-out infinite; }
.spin { transform-origin: 260px 210px; animation: spin 40s linear infinite; }
.blink { animation: blink 2.5s ease-in-out infinite; }
.is-paused * { animation-play-state: paused !important; }
@keyframes flow { to { stroke-dashoffset: -32; } }
@keyframes pulse { 50% { transform: scale(1.08); opacity: .7; } }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes blink { 50% { opacity: .2; } }
</style>
