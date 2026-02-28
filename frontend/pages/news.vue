<template>
  <div>
    <div class="news-header">
      <h1>News</h1>
      <div class="date-nav">
        <button @click="goToPrevDay">&larr;</button>
        <input type="date" :value="selectedDate" @change="onDateChange" />
        <button :disabled="isToday" @click="goToNextDay">&rarr;</button>
      </div>
    </div>

    <p v-if="loading" class="status">News werden geladen...</p>
    <p v-else-if="error" class="status error">{{ error }}</p>

    <template v-else-if="currentPage">
      <div class="news-meta">
        Generiert: {{ formattedDate }}
        <span v-if="currentPage.sources?.length"> &middot; {{ currentPage.sources.length }} Quellen</span>
      </div>
      <div class="news-content" v-html="renderedContent"></div>
      <div v-if="currentPage.sources?.length" class="news-sources">
        <h3>Quellen</h3>
        <ul>
          <li v-for="(src, idx) in currentPage.sources" :key="idx">
            <a v-if="src.url" :href="src.url" target="_blank" rel="noopener">{{ src.title || src.url }}</a>
            <span v-else>{{ src.title }}</span>
          </li>
        </ul>
      </div>
    </template>

    <p v-else class="status">Keine News fuer dieses Datum verfuegbar.</p>
  </div>
</template>

<script setup lang="ts">
import DOMPurify from "dompurify";
import { marked } from "marked";

const { currentPage, loading, error, fetchLatest, fetchByDate } = useNews();

const today = new Date().toISOString().split("T")[0];
const selectedDate = ref(today);

const isToday = computed(() => selectedDate.value === today);

const formattedDate = computed(() => {
  if (!currentPage.value) return "";
  return new Date(currentPage.value.generated_at).toLocaleString("de-DE");
});

const renderedContent = computed(() => {
  if (!currentPage.value?.content) return "";
  return DOMPurify.sanitize(marked(currentPage.value.content) as string);
});

function onDateChange(e: Event) {
  const target = e.target as HTMLInputElement;
  selectedDate.value = target.value;
}

function goToPrevDay() {
  const d = new Date(selectedDate.value);
  d.setDate(d.getDate() - 1);
  selectedDate.value = d.toISOString().split("T")[0];
}

function goToNextDay() {
  const d = new Date(selectedDate.value);
  d.setDate(d.getDate() + 1);
  selectedDate.value = d.toISOString().split("T")[0];
}

watch(
  selectedDate,
  (val) => {
    if (val === today) {
      fetchLatest();
    } else {
      fetchByDate(val);
    }
  },
  { immediate: true },
);
</script>

<style scoped>
.news-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.news-header h1 {
  margin: 0;
}

.date-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.date-nav button {
  padding: 0.4rem 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  font-size: 1rem;
}

.date-nav button:hover:not(:disabled) {
  background: #f0f0f0;
}

.date-nav button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.date-nav input {
  padding: 0.4rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.875rem;
}

.news-meta {
  font-size: 0.85rem;
  color: #888;
  margin-bottom: 1.5rem;
}

.news-content {
  line-height: 1.7;
  font-size: 1rem;
  color: #1a1a1a;
}

.news-content :deep(h1) {
  font-size: 1.5rem;
  margin-top: 2rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.news-content :deep(h2) {
  font-size: 1.25rem;
  margin-top: 1.5rem;
}

.news-content :deep(h3) {
  font-size: 1.1rem;
  margin-top: 1.25rem;
}

.news-content :deep(a) {
  color: #1967d2;
}

.news-content :deep(code) {
  background: #f5f5f5;
  padding: 0.15em 0.4em;
  border-radius: 3px;
  font-size: 0.9em;
}

.news-content :deep(pre) {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
}

.news-sources {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.news-sources h3 {
  margin: 0 0 0.75rem;
  font-size: 1rem;
}

.news-sources ul {
  padding-left: 1.25rem;
}

.news-sources li {
  margin-bottom: 0.3rem;
  font-size: 0.875rem;
}

.news-sources a {
  color: #1967d2;
}

.status {
  color: #666;
  padding: 2rem 0;
}

.status.error {
  color: #d93025;
}
</style>
