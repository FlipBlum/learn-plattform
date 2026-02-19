<template>
  <div class="lp-card">
    <div class="lp-header">
      <h3>{{ path.name }}</h3>
      <span :class="['lp-status', path.status]">{{ statusLabel }}</span>
    </div>

    <div v-if="epubs.length" class="lp-epubs">
      <div v-for="epub in epubs" :key="epub.id" class="epub-item">
        <div class="epub-info">
          <span class="epub-title">{{ epub.title }}</span>
          <span class="epub-progress">
            Kap. {{ epub.current_chapter }}/{{ epub.total_chapters }}
          </span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: `${epub.progress_percent}%` }"></div>
        </div>
        <div class="epub-actions">
          <button class="btn-small" @click="$emit('openReader', epub)">Lesen</button>
          <button class="btn-small btn-outline" @click="$emit('openQuiz', epub)">Quiz</button>
        </div>
      </div>
    </div>
    <p v-else class="no-epubs">Noch keine Buecher hochgeladen.</p>

    <div class="lp-actions">
      <label class="upload-label">
        <input type="file" accept=".epub" @change="onUpload" />
        + Epub hochladen
      </label>
      <button class="btn-delete" @click="$emit('delete', path.id)">&times;</button>
    </div>
  </div>
</template>

<script setup lang="ts">
interface LearningPath {
  id: string;
  name: string;
  status: string;
}

interface Epub {
  id: string;
  title: string;
  total_chapters: number;
  current_chapter: number;
  progress_percent: number;
}

const props = defineProps<{
  path: LearningPath;
  epubs: Epub[];
}>();

const emit = defineEmits<{
  delete: [id: string];
  upload: [pathId: string, file: File];
  openReader: [epub: Epub];
  openQuiz: [epub: Epub];
}>();

const statusLabels: Record<string, string> = {
  active: "Aktiv",
  paused: "Pausiert",
  completed: "Abgeschlossen",
};

const statusLabel = computed(() => statusLabels[props.path.status] || props.path.status);

function onUpload(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (file) emit("upload", props.path.id, file);
}
</script>

<style scoped>
.lp-card {
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 1.25rem;
  background: white;
}

.lp-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.lp-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.lp-status {
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.lp-status.active {
  background: #e8f5e9;
  color: #137333;
}

.lp-status.paused {
  background: #fff3e0;
  color: #e65100;
}

.lp-status.completed {
  background: #e8f0fe;
  color: #1967d2;
}

.lp-epubs {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.epub-item {
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.epub-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.35rem;
}

.epub-title {
  font-weight: 500;
  font-size: 0.9rem;
}

.epub-progress {
  font-size: 0.8rem;
  color: #888;
}

.progress-bar {
  height: 6px;
  background: #f0f0f0;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: #34a853;
  border-radius: 3px;
  transition: width 0.3s;
}

.epub-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-small {
  padding: 0.25rem 0.6rem;
  border: none;
  border-radius: 4px;
  font-size: 0.75rem;
  cursor: pointer;
  background: #1967d2;
  color: white;
}

.btn-small.btn-outline {
  background: white;
  border: 1px solid #1967d2;
  color: #1967d2;
}

.no-epubs {
  color: #999;
  font-size: 0.875rem;
  margin: 0.5rem 0 1rem;
}

.lp-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.upload-label {
  font-size: 0.85rem;
  color: #1967d2;
  cursor: pointer;
  font-weight: 500;
}

.upload-label input {
  display: none;
}

.btn-delete {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #999;
  cursor: pointer;
}

.btn-delete:hover {
  color: #d93025;
}
</style>
