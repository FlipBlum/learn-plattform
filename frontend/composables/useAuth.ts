import type { User, Session } from "@supabase/supabase-js";

interface AuthState {
  user: User | null;
  session: Session | null;
  loading: boolean;
}

const authState = reactive<AuthState>({
  user: null,
  session: null,
  loading: true,
});

export function useAuth() {
  const { $supabase } = useNuxtApp();

  async function initialize() {
    authState.loading = true;
    try {
      const {
        data: { session },
      } = await $supabase.auth.getSession();
      authState.session = session;
      authState.user = session?.user ?? null;
    } finally {
      authState.loading = false;
    }

    $supabase.auth.onAuthStateChange((_event: string, session: Session | null) => {
      authState.session = session;
      authState.user = session?.user ?? null;
    });
  }

  async function signInWithGoogle() {
    const { error } = await $supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });
    if (error) throw error;
  }

  async function signOut() {
    const { error } = await $supabase.auth.signOut();
    if (error) throw error;
    authState.user = null;
    authState.session = null;
    await navigateTo("/login");
  }

  function getAccessToken(): string | null {
    return authState.session?.access_token ?? null;
  }

  return {
    user: computed(() => authState.user),
    session: computed(() => authState.session),
    loading: computed(() => authState.loading),
    isAuthenticated: computed(() => !!authState.user),
    initialize,
    signInWithGoogle,
    signOut,
    getAccessToken,
  };
}
