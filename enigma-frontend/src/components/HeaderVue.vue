<template>
  <header class="header">
    <nav class="nav">
      <router-link
        v-for="link in links"
        :key="link.path"
        :to="link.path"
        :class="{ active: isActive(link.path) }"
      >
        {{ link.name }}
      </router-link>
    </nav>
  </header>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const links = [
  { name: 'История обращений', path: '/' },
  { name: 'Аналитика', path: '/analyze' },
]

const isActive = (path) => route.path === path
</script>

<style scoped>
.header {
  background-color: #fff;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: absolute;
  top: 20px;
  width: calc(100% - 80px);
}

.nav {
  display: flex;
  gap: 20px; /* расстояние между ссылками */
}

.nav a {
  text-decoration: none;
  color: #333;
  font-weight: normal;
}

.nav a.active {
  font-weight: bold;
}
</style>