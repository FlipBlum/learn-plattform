interface LearningPath {
  id: string;
  user_id: string;
  name: string;
  status: "active" | "paused" | "completed";
  created_at: string;
}

interface Epub {
  id: string;
  user_id: string;
  learning_path_id: string;
  title: string;
  file_path: string;
  total_chapters: number;
  current_chapter: number;
  progress_percent: number;
  uploaded_at: string;
}

export function useLearningPaths() {
  const { apiFetch } = useApi();

  const paths = ref<LearningPath[]>([]);
  const loading = ref(false);
  const error = ref("");

  async function fetchPaths() {
    loading.value = true;
    error.value = "";
    try {
      paths.value = await apiFetch<LearningPath[]>("/api/learning-paths/");
    } catch (e) {
      error.value = e instanceof Error ? e.message : "Fehler";
    } finally {
      loading.value = false;
    }
  }

  async function createPath(name: string) {
    const created = await apiFetch<LearningPath>("/api/learning-paths/", {
      method: "POST",
      body: JSON.stringify({ name }),
    });
    paths.value.push(created);
    return created;
  }

  async function deletePath(id: string) {
    await apiFetch(`/api/learning-paths/${id}`, { method: "DELETE" });
    paths.value = paths.value.filter((p) => p.id !== id);
  }

  async function getEpubs(pathId: string): Promise<Epub[]> {
    return apiFetch<Epub[]>(`/api/epub/path/${pathId}`);
  }

  async function uploadEpub(pathId: string, file: File): Promise<Epub> {
    const { getAccessToken } = useAuth();
    const config = useRuntimeConfig();
    const token = getAccessToken();

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
      `${config.public.apiBaseUrl}/api/epub/upload?learning_path_id=${pathId}`,
      {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        body: formData,
      },
    );

    if (!response.ok) throw new Error("Upload fehlgeschlagen");
    return response.json();
  }

  async function updateProgress(epubId: string, currentChapter: number, progressPercent: number) {
    return apiFetch(`/api/epub/${epubId}/progress`, {
      method: "PUT",
      body: JSON.stringify({
        current_chapter: currentChapter,
        progress_percent: progressPercent,
      }),
    });
  }

  return {
    paths: computed(() => paths.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    fetchPaths,
    createPath,
    deletePath,
    getEpubs,
    uploadEpub,
    updateProgress,
  };
}
