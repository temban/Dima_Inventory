<template>
  <div id="app">
    <Navbar />
    <div class="app-container">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/layout/Navbar.vue'
</script>