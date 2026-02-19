<template>
  <div>
    <nav>
      <NuxtLink to="/news">News</NuxtLink>
      <NuxtLink to="/videos">Videos</NuxtLink>
      <NuxtLink to="/learn">Learn</NuxtLink>
    </nav>
    <main>
      <slot />
    </main>
  </div>
</template>
