<template>
  <section class="statistics-display">
    <h2>Overall Statistics</h2>
    <p><strong>Total Files Processed:</strong> {{ stats.total_files }}</p>
    <p><strong>Total Video Duration:</strong> {{ formatDuration(stats.total_video_duration_seconds) }}</p>
    <p><strong>Files by Type:</strong></p>
    <ul>
      <li v-for="(count, type) in stats.type_counts" :key="type">
        {{ type }}: {{ count }}
      </li>
    </ul>
    <p><em>{{ stats.changes_last_7_days }}</em></p>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

interface Stats {
  total_files: number;
  type_counts: Record<string, number>;
  total_video_duration_seconds: number;
  total_audio_duration_seconds: number; // Added for completeness
  changes_last_7_days: string;
}

const stats = ref<Stats>({
  total_files: 0,
  type_counts: { image: 0, video: 0, audio: 0, text: 0, other: 0 },
  total_video_duration_seconds: 0,
  total_audio_duration_seconds: 0,
  changes_last_7_days: 'Statistics data will be loaded from the backend.'
});

const fetchStatistics = () => {
  // Dummy data
  stats.value = {
    total_files: 160,
    type_counts: { image: 155, video: 2, audio: 1, text: 1, other: 1 },
    total_video_duration_seconds: 7260, // e.g., 2 hours, 1 minute
    total_audio_duration_seconds: 180, // e.g., 3 minutes
    changes_last_7_days: 'Dummy data: 7-day changes not yet implemented.'
  };
  console.log('Fetched dummy statistics');
};

const formatDuration = (totalSeconds: number): string => {
  if (totalSeconds === 0) return '0s';
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = Math.floor(totalSeconds % 60);
  let formatted = '';
  if (hours > 0) formatted += `${hours}h `;
  if (minutes > 0) formatted += `${minutes}m `;
  if (seconds > 0 || !formatted) formatted += `${seconds}s`;
  return formatted.trim();
};

onMounted(() => {
  fetchStatistics();
});
</script>

<style scoped>
.statistics-display {
  padding: 15px;
  border: 1px solid #ddd;
  background-color: #f0f8ff; /* Light alice blue */
}
.statistics-display ul {
  list-style-position: inside;
}
</style>
