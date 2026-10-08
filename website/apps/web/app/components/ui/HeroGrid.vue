<script setup lang="ts">
// 深色段背景纹理：点阵 + 等高线网格（替代现网蓝紫渐变光效，K-01 §2.2）
</script>

<template>
  <svg aria-hidden="true" preserveAspectRatio="xMidYMid slice" viewBox="0 0 1440 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <pattern id="hyzl-dots" width="24" height="24" patternUnits="userSpaceOnUse">
        <circle cx="1" cy="1" r="1" fill="#7FA3E6" opacity=".18" />
      </pattern>
      <linearGradient id="hyzl-fade" x1="0" x2="1" y1="0" y2="0">
        <stop offset="0" stop-color="#0A1A3F" />
        <stop offset=".55" stop-color="#0A1A3F" stop-opacity="0" />
      </linearGradient>
    </defs>
    <rect width="1440" height="600" fill="url(#hyzl-dots)" />
    <g fill="none" stroke="#3060AC" stroke-opacity=".28">
      <path d="M760 520c120-60 260-40 360-110s180-150 320-160" />
      <path d="M720 560c140-70 280-50 390-120s190-150 330-170" />
      <path d="M800 470c110-50 230-40 320-100s170-130 320-150" />
      <path d="M860 420c100-40 200-40 280-90s160-110 300-130" />
    </g>
    <rect width="1440" height="600" fill="url(#hyzl-fade)" />
  </svg>
</template>
