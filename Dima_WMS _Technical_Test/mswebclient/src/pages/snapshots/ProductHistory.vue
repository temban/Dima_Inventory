<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">Product Inventory History</h1>
      <router-link :to="{ name: 'Snapshots' }" class="btn">
        Back to Inventory
      </router-link>
    </div>

    <div class="card">
      <p class="text-gray-500">Product-specific inventory history page.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>