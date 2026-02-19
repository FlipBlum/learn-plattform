<template>
  <div>
    <h1>Willkommen, {{ userName }}</h1>
    <p class="subtitle">Deine personalisierte Lernplattform</p>

    <div class="dashboard-grid">
      <NuxtLink to="/news" class="dash-card">
        <h2>News</h2>
        <p>Taegliche personalisierte News aus deinen Lernpfaden</p>
      </NuxtLink>

      <NuxtLink to="/videos" class="dash-card">
        <h2>Videos</h2>
        <p>Kuratierte Lernvideos von deeplearning.ai, Coursera & Google AI</p>
      </NuxtLink>

      <NuxtLink to="/learn" class="dash-card">
        <h2>Lernpfade</h2>
        <p>Fortschritt tracken, Buecher lesen, Quizzes & Kritik</p>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
const { user } = useAuth();
const userName = computed(() => user.value?.user_metadata?.full_name || "Lerner");
</script>

<style scoped>
h1 {
  margin: 0 0 0.25rem;
}

.subtitle {
  color: #666;
  margin: 0 0 2rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
}

.dash-card {
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  background: white;
  transition: all 0.2s;
}

.dash-card:hover {
  border-color: #4285f4;
  box-shadow: 0 2px 12px rgb(66 133 244 / 12%);
  transform: translateY(-2px);
}

.dash-card h2 {
  margin: 0 0 0.5rem;
  font-size: 1.2rem;
  color: #1a1a2e;
}

.dash-card p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
}
</style>
