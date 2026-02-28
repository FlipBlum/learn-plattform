<template>
  <div class="app-layout">
    <nav class="app-nav">
      <div class="nav-links">
        <NuxtLink to="/news">Test123</NuxtLink>
        <NuxtLink to="/videos">Videos</NuxtLink>
        <NuxtLink to="/learn">Learn</NuxtLink>
      </div>
      <div v-if="user" class="nav-user">
        <img
          v-if="user.user_metadata?.avatar_url"
          :src="user.user_metadata.avatar_url"
          :alt="user.user_metadata?.full_name || user.email"
          class="avatar"
        />
        <span class="user-name">{{ user.user_metadata?.full_name || user.email }}</span>
        <button class="logout-btn" @click="signOut">Logout</button>
      </div>
    </nav>
    <main class="app-main">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
const { user, signOut } = useAuth();
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.5rem;
  background: #1a1a2e;
  color: white;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  color: #ccc;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: white;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
}

.user-name {
  font-size: 0.875rem;
  color: #ccc;
}

.logout-btn {
  padding: 0.35rem 0.75rem;
  border: 1px solid #555;
  border-radius: 6px;
  background: transparent;
  color: #ccc;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #333;
  color: white;
}

.app-main {
  flex: 1;
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>
