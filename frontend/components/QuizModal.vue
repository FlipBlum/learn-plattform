<template>
  <div class="quiz-overlay">
    <div class="quiz-modal">
      <div class="quiz-header">
        <h3>Quiz: {{ epub.title }} - Kapitel {{ chapter }}</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>

      <div v-if="loading" class="quiz-status">Quiz wird generiert...</div>
      <div v-else-if="error" class="quiz-status error">{{ error }}</div>

      <div v-else-if="result" class="quiz-result">
        <h4>Ergebnis: {{ result.correct }}/{{ result.total }} ({{ result.score.toFixed(0) }}%)</h4>
        <button class="btn-primary" @click="$emit('close')">Schliessen</button>
      </div>

      <div v-else-if="quiz" class="quiz-body">
        <div v-for="(q, qi) in quiz.questions" :key="qi" class="question">
          <p class="question-text">{{ qi + 1 }}. {{ q.question }}</p>
          <div class="options">
            <label
              v-for="(opt, oi) in q.options"
              :key="oi"
              :class="['option', { selected: answers[qi] === oi }]"
            >
              <input v-model="answers[qi]" type="radio" :name="`q-${qi}`" :value="oi" />
              {{ opt }}
            </label>
          </div>
        </div>
        <button
          class="btn-primary"
          :disabled="answers.some((a) => a === -1)"
          @click="submitQuiz"
        >
          Abgeben
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Epub {
  id: string;
  title: string;
  current_chapter: number;
}

interface QuizQuestion {
  question: string;
  options: string[];
  correct_index: number;
}

interface QuizData {
  id: string;
  questions: QuizQuestion[];
}

interface QuizResult {
  score: number;
  correct: number;
  total: number;
}

const props = defineProps<{ epub: Epub }>();
defineEmits<{ close: [] }>();

const { apiFetch } = useApi();
const chapter = computed(() => props.epub.current_chapter || 1);
const quiz = ref<QuizData | null>(null);
const answers = ref<number[]>([]);
const result = ref<QuizResult | null>(null);
const loading = ref(true);
const error = ref("");

onMounted(async () => {
  try {
    quiz.value = await apiFetch<QuizData>(
      `/api/epub/${props.epub.id}/quiz?chapter=${chapter.value}`,
    );
    answers.value = new Array(quiz.value.questions.length).fill(-1);
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Fehler beim Laden";
  } finally {
    loading.value = false;
  }
});

async function submitQuiz() {
  if (!quiz.value) return;
  try {
    result.value = await apiFetch<QuizResult>(
      `/api/epub/${props.epub.id}/quiz/${quiz.value.id}`,
      {
        method: "POST",
        body: JSON.stringify({ answers: answers.value }),
      },
    );
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Fehler beim Absenden";
  }
}
</script>

<style scoped>
.quiz-overlay {
  position: fixed;
  inset: 0;
  background: rgb(0 0 0 / 60%);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
}

.quiz-modal {
  background: white;
  width: 90vw;
  max-width: 600px;
  max-height: 85vh;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.quiz-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #eee;
}

.quiz-header h3 {
  margin: 0;
  font-size: 1rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.quiz-body {
  padding: 1.25rem;
  overflow-y: auto;
  flex: 1;
}

.question {
  margin-bottom: 1.5rem;
}

.question-text {
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.15s;
}

.option:hover {
  background: #f5f5f5;
}

.option.selected {
  border-color: #1967d2;
  background: #e8f0fe;
}

.option input {
  accent-color: #1967d2;
}

.btn-primary {
  margin-top: 1rem;
  padding: 0.6rem 1.5rem;
  background: #1967d2;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quiz-status {
  padding: 2rem;
  text-align: center;
  color: #666;
}

.quiz-status.error {
  color: #d93025;
}

.quiz-result {
  padding: 2rem;
  text-align: center;
}

.quiz-result h4 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}
</style>
