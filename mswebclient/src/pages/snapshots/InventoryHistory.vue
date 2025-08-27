<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">Inventory History</h1>
      <router-link :to="{ name: 'Snapshots' }" class="btn">
        Back to Current Inventory
      </router-link>
    </div>

    <div class="card">
      <p class="text-gray-500">Inventory history page showing all historical snapshots.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>