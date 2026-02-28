<template>
  <div class="epub-reader-overlay">
    <div class="epub-reader">
      <div class="reader-header">
        <h3>{{ epub.title }}</h3>
        <div class="reader-nav">
          <button :disabled="currentChapter <= 1" @click="prevChapter">&larr; Vorheriges</button>
          <span>Kapitel {{ currentChapter }} / {{ epub.total_chapters }}</span>
          <button :disabled="currentChapter >= epub.total_chapters" @click="nextChapter">
            Naechstes &rarr;
          </button>
        </div>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      <div ref="readerContainer" class="reader-body"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import ePub from "epubjs";

interface EpubData {
  id: string;
  title: string;
  total_chapters: number;
  current_chapter: number;
  download_url?: string;
}

const props = defineProps<{ epub: EpubData }>();
const emit = defineEmits<{
  close: [];
  progressUpdate: [chapter: number, percent: number];
}>();

const readerContainer = ref<HTMLElement | null>(null);
const currentChapter = ref(props.epub.current_chapter || 1);
let book: any = null;
let rendition: any = null;

onMounted(async () => {
  if (!props.epub.download_url || !readerContainer.value) return;

  book = ePub(props.epub.download_url);
  rendition = book.renderTo(readerContainer.value, {
    width: "100%",
    height: "100%",
    spread: "none",
  });
  await rendition.display();
});

function prevChapter() {
  if (currentChapter.value > 1) {
    currentChapter.value--;
    rendition?.prev();
    emitProgress();
  }
}

function nextChapter() {
  if (currentChapter.value < props.epub.total_chapters) {
    currentChapter.value++;
    rendition?.next();
    emitProgress();
  }
}

function emitProgress() {
  if (props.epub.total_chapters <= 0) return;
  const percent = (currentChapter.value / props.epub.total_chapters) * 100;
  emit("progressUpdate", currentChapter.value, Math.round(percent));
}

onUnmounted(() => {
  book?.destroy();
});
</script>

<style scoped>
.epub-reader-overlay {
  position: fixed;
  inset: 0;
  background: rgb(0 0 0 / 60%);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
}

.epub-reader {
  background: white;
  width: 90vw;
  height: 90vh;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.reader-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #eee;
  gap: 1rem;
}

.reader-header h3 {
  margin: 0;
  font-size: 1rem;
  flex-shrink: 0;
}

.reader-nav {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.85rem;
}

.reader-nav button {
  padding: 0.3rem 0.6rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 0.8rem;
}

.reader-nav button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  flex-shrink: 0;
}

.reader-body {
  flex: 1;
  overflow: auto;
}
</style>
