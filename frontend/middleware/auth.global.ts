export default defineNuxtRouteMiddleware((to) => {
  const { isAuthenticated, loading } = useAuth();

  const publicRoutes = ["/login", "/auth/callback"];
  if (publicRoutes.includes(to.path)) {
    return;
  }

  if (!loading.value && !isAuthenticated.value) {
    return navigateTo("/login");
  }
});
