<template>
  <div class="critique-card">
    <div class="critique-header">
      <h3>Lernkritik</h3>
      <button v-if="!loading" class="btn-generate" @click="generate">
        Neue Kritik generieren
      </button>
    </div>

    <p v-if="loading" class="status">Kritik wird generiert...</p>

    <template v-else-if="latestCritique">
      <div class="critique-meta">
        {{ formattedDate }} &middot; {{ latestCritique.period }}
      </div>
      <div class="critique-content" v-html="renderedContent"></div>
    </template>

    <p v-else class="status">
      Noch keine Kritik vorhanden. Generiere deine erste Lernkritik.
    </p>
  </div>
</template>

<script setup lang="ts">
import { marked } from "marked";

interface CritiqueData {
  id: string;
  period: string;
  content: string;
  created_at: string;
}

const { apiFetch } = useApi();
const critiques = ref<CritiqueData[]>([]);
const loading = ref(false);

const latestCritique = computed(() => critiques.value[0] ?? null);

const formattedDate = computed(() => {
  if (!latestCritique.value) return "";
  return new Date(latestCritique.value.created_at).toLocaleDateString("de-DE");
});

const renderedContent = computed(() => {
  if (!latestCritique.value?.content) return "";
  return marked(latestCritique.value.content);
});

async function fetchCritiques() {
  try {
    critiques.value = await apiFetch<CritiqueData[]>("/api/critique/");
  } catch {
    /* ignore */
  }
}

async function generate() {
  loading.value = true;
  try {
    const newCritique = await apiFetch<CritiqueData>("/api/critique/generate", {
      method: "POST",
    });
    critiques.value.unshift(newCritique);
  } catch {
    /* ignore */
  } finally {
    loading.value = false;
  }
}

onMounted(() => fetchCritiques());
</script>

<style scoped>
.critique-card {
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 1.25rem;
  background: white;
}

.critique-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.critique-header h3 {
  margin: 0;
}

.btn-generate {
  padding: 0.4rem 0.8rem;
  border: 1px solid #1967d2;
  border-radius: 6px;
  background: white;
  color: #1967d2;
  font-size: 0.8rem;
  cursor: pointer;
}

.btn-generate:hover {
  background: #e8f0fe;
}

.critique-meta {
  font-size: 0.8rem;
  color: #888;
  margin-bottom: 1rem;
}

.critique-content {
  line-height: 1.7;
  font-size: 0.95rem;
}

.critique-content :deep(h1),
.critique-content :deep(h2),
.critique-content :deep(h3) {
  margin-top: 1rem;
  font-size: 1.05rem;
}

.critique-content :deep(ul) {
  padding-left: 1.25rem;
}

.status {
  color: #888;
  font-size: 0.9rem;
}
</style>
