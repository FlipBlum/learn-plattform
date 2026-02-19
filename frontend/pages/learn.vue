<template>
  <div>
    <h1>Lernpfade</h1>

    <div class="add-path">
      <input
        v-model="newPathName"
        placeholder="Neuen Lernpfad erstellen..."
        @keyup.enter="addPath"
      />
      <button :disabled="!newPathName.trim()" @click="addPath">Erstellen</button>
    </div>

    <p v-if="loading" class="status">Lernpfade werden geladen...</p>
    <p v-else-if="error" class="status error">{{ error }}</p>

    <div v-else class="paths-grid">
      <LearningPathCard
        v-for="path in paths"
        :key="path.id"
        :path="path"
        :epubs="pathEpubs[path.id] || []"
        @delete="handleDelete"
        @upload="handleUpload"
        @open-reader="openReader"
        @open-quiz="openQuiz"
      />
    </div>

    <CritiqueCard />

    <EpubReader
      v-if="readerEpub"
      :epub="readerEpub"
      @close="readerEpub = null"
      @progress-update="handleProgressUpdate"
    />

    <QuizModal
      v-if="quizEpub"
      :epub="quizEpub"
      @close="quizEpub = null"
    />
  </div>
</template>

<script setup lang="ts">
interface Epub {
  id: string;
  title: string;
  total_chapters: number;
  current_chapter: number;
  progress_percent: number;
  download_url?: string;
}

const {
  paths,
  loading,
  error,
  fetchPaths,
  createPath,
  deletePath,
  getEpubs,
  uploadEpub,
  updateProgress,
} = useLearningPaths();

const { apiFetch } = useApi();

const newPathName = ref("");
const pathEpubs = ref<Record<string, Epub[]>>({});
const readerEpub = ref<Epub | null>(null);
const quizEpub = ref<Epub | null>(null);

async function addPath() {
  if (!newPathName.value.trim()) return;
  await createPath(newPathName.value.trim());
  newPathName.value = "";
}

async function handleDelete(id: string) {
  await deletePath(id);
}

async function handleUpload(pathId: string, file: File) {
  await uploadEpub(pathId, file);
  await loadEpubs(pathId);
}

async function loadEpubs(pathId: string) {
  pathEpubs.value[pathId] = await getEpubs(pathId);
}

async function openReader(epub: Epub) {
  const detail = await apiFetch<Epub & { download_url: string }>(`/api/epub/${epub.id}`);
  readerEpub.value = detail;
}

function openQuiz(epub: Epub) {
  quizEpub.value = epub;
}

async function handleProgressUpdate(chapter: number, percent: number) {
  if (!readerEpub.value) return;
  await updateProgress(readerEpub.value.id, chapter, percent);
}

onMounted(async () => {
  await fetchPaths();
  for (const path of paths.value) {
    await loadEpubs(path.id);
  }
});
</script>

<style scoped>
h1 {
  margin: 0 0 1rem;
}

.add-path {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.add-path input {
  flex: 1;
  padding: 0.6rem 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.9rem;
}

.add-path button {
  padding: 0.6rem 1.25rem;
  background: #1967d2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
}

.add-path button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.paths-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.status {
  color: #666;
  padding: 1rem 0;
}

.status.error {
  color: #d93025;
}
</style>
