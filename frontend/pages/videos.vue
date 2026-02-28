<template>
  <div>
    <h1>Lernvideos</h1>

    <div class="source-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.value"
        :class="['tab', { active: activeSource === tab.value }]"
        @click="activeSource = tab.value"
      >
        {{ tab.label }}
      </button>
    </div>

    <p v-if="loading" class="status">Videos werden geladen...</p>
    <p v-else-if="error" class="status error">Fehler: {{ error }}</p>
    <p v-else-if="videos.length === 0" class="status">Keine Videos gefunden.</p>

    <div v-else class="video-grid">
      <VideoCard v-for="video in videos" :key="video.id" :video="video" />
    </div>
  </div>
</template>

<script setup lang="ts">
const { apiFetch } = useApi();

interface Video {
  id: string;
  source: string;
  title: string;
  url: string;
  description?: string;
  discovered_at: string;
}

const tabs = [
  { label: "Alle", value: "" },
  { label: "deeplearning.ai", value: "deeplearning.ai" },
  { label: "Coursera", value: "coursera" },
  { label: "Google AI", value: "google_ai" },
];

const activeSource = ref("");
const videos = ref<Video[]>([]);
const loading = ref(true);
const error = ref("");

async function fetchVideos() {
  loading.value = true;
  error.value = "";
  try {
    const params = activeSource.value ? `?source=${activeSource.value}` : "";
    const data = await apiFetch<{ videos: Video[] }>(`/api/videos${params}`);
    videos.value = data.videos;
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Unbekannter Fehler";
  } finally {
    loading.value = false;
  }
}

watch(activeSource, () => fetchVideos());
onMounted(() => fetchVideos());
</script>

<style scoped>
h1 {
  margin: 0 0 1rem;
}

.source-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.tab {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.tab:hover {
  border-color: #4285f4;
}

.tab.active {
  background: #4285f4;
  color: white;
  border-color: #4285f4;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.status {
  color: #666;
  padding: 2rem 0;
}

.status.error {
  color: #d93025;
}
</style>
