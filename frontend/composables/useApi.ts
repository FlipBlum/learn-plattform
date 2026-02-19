export function useApi() {
  const config = useRuntimeConfig();
  const { getAccessToken } = useAuth();

  async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
    const token = getAccessToken();
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${config.public.apiBaseUrl}${path}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      throw new Error(body.detail || `API error ${response.status}`);
    }

    return response.json();
  }

  return { apiFetch };
}
