<template>
  <aside class="w-64 bg-white shadow-md">
    <div class="p-4">
      <h2 class="text-lg font-semibold text-gray-900">DIMA WMS</h2>
    </div>
    <nav class="mt-4">
      <router-link
        v-for="item in navItems"
        :key="item.route"
        :to="{ name: item.route }"
        class="block px-4 py-2 text-gray-600 hover:bg-gray-100 hover:text-gray-900"
        active-class="bg-primary-100 text-primary border-r-4 border-primary"
      >
        {{ item.label }}
      </router-link>
    </nav>
  </aside>
</template>

<script setup lang="ts">
const navItems = [
  { label: 'Products', route: 'Products' },
  { label: 'Locations', route: 'Locations' },
  { label: 'Stock Moves', route: 'StockMoves' },
  { label: 'Suppliers', route: 'Suppliers' },
  { label: 'Inventory', route: 'Snapshots' }
]
</script>