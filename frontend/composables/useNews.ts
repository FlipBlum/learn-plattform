interface NewsSource {
  title?: string;
  url?: string;
}

interface NewsPage {
  id: string;
  date: string;
  content: string;
  sources: NewsSource[];
  generated_at: string;
}

export function useNews() {
  const { apiFetch } = useApi();
  const currentPage = ref<NewsPage | null>(null);
  const loading = ref(false);
  const error = ref("");

  async function fetchLatest() {
    loading.value = true;
    error.value = "";
    try {
      currentPage.value = await apiFetch<NewsPage>("/api/news/latest");
    } catch (e) {
      error.value = e instanceof Error ? e.message : "Unbekannter Fehler";
      currentPage.value = null;
    } finally {
      loading.value = false;
    }
  }

  async function fetchByDate(date: string) {
    loading.value = true;
    error.value = "";
    try {
      currentPage.value = await apiFetch<NewsPage>(`/api/news/${date}`);
    } catch (e) {
      error.value = e instanceof Error ? e.message : "Unbekannter Fehler";
      currentPage.value = null;
    } finally {
      loading.value = false;
    }
  }

  return {
    currentPage: computed(() => currentPage.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    fetchLatest,
    fetchByDate,
  };
}
