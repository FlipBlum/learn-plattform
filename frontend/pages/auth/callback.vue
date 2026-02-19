<template>
  <div class="callback-page">
    <p v-if="error">Authentifizierung fehlgeschlagen. <NuxtLink to="/login">Erneut versuchen</NuxtLink></p>
    <p v-else>Authentifizierung laeuft...</p>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false });

const error = ref(false);
const { initialize } = useAuth();

onMounted(async () => {
  try {
    await initialize();
    await navigateTo("/");
  } catch {
    error.value = true;
  }
});
</script>

<style scoped>
.callback-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  font-size: 1.1rem;
  color: #666;
}
</style>
