<template>
  <div class="news-card">
    <div class="news-card-header">
      <span class="source-badge" :class="source.source_type">{{ source.source_type }}</span>
      <span v-if="source.title" class="source-title">{{ source.title }}</span>
    </div>
    <p v-if="source.content" class="source-content">{{ source.content }}</p>
    <a
      v-if="source.url"
      :href="source.url"
      target="_blank"
      rel="noopener noreferrer"
      class="source-link"
    >
      Quelle ansehen &rarr;
    </a>
  </div>
</template>

<script setup lang="ts">
interface Source {
  source_type: string;
  title?: string;
  content?: string;
  url?: string;
}

defineProps<{ source: Source }>();
</script>

<style scoped>
.news-card {
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
}

.news-card-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.source-badge {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
}

.source-badge.gmail {
  background: #fce8e6;
  color: #c5221f;
}

.source-badge.rss {
  background: #e8f5e9;
  color: #137333;
}

.source-title {
  font-weight: 500;
  font-size: 0.9rem;
}

.source-content {
  font-size: 0.85rem;
  color: #555;
  margin: 0.5rem 0;
  line-height: 1.4;
}

.source-link {
  font-size: 0.8rem;
  color: #1967d2;
  text-decoration: none;
}

.source-link:hover {
  text-decoration: underline;
}
</style>
