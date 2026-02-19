<template>
  <a :href="video.url" target="_blank" rel="noopener noreferrer" class="video-card">
    <div class="video-source">{{ sourceLabel }}</div>
    <h3 class="video-title">{{ video.title }}</h3>
    <p v-if="video.description" class="video-desc">{{ video.description }}</p>
    <time class="video-date">{{ formattedDate }}</time>
  </a>
</template>

<script setup lang="ts">
interface Video {
  id: string;
  source: string;
  title: string;
  url: string;
  description?: string;
  discovered_at: string;
}

const props = defineProps<{ video: Video }>();

const sourceLabels: Record<string, string> = {
  "deeplearning.ai": "deeplearning.ai",
  coursera: "Coursera",
  google_ai: "Google AI",
};

const sourceLabel = computed(() => sourceLabels[props.video.source] || props.video.source);

const formattedDate = computed(() => {
  return new Date(props.video.discovered_at).toLocaleDateString("de-DE", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
});
</script>

<style scoped>
.video-card {
  display: block;
  padding: 1.25rem;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s;
  background: white;
}

.video-card:hover {
  border-color: #4285f4;
  box-shadow: 0 2px 8px rgb(66 133 244 / 15%);
  transform: translateY(-1px);
}

.video-source {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  background: #e8f0fe;
  color: #1967d2;
  margin-bottom: 0.5rem;
}

.video-title {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  line-height: 1.4;
  color: #1a1a1a;
}

.video-desc {
  margin: 0 0 0.5rem;
  font-size: 0.875rem;
  color: #666;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-date {
  font-size: 0.75rem;
  color: #999;
}
</style>
