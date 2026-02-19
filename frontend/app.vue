<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
const { initialize } = useAuth();
onMounted(() => initialize());
</script>
