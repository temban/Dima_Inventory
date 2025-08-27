<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">Stock Moves</h1>
      <router-link :to="{ name: 'StockMoveCreate' }" class="btn btn-primary">
        Create Stock Move
      </router-link>
    </div>

    <div v-if="stockMoveStore.loading" class="text-center py-8">
      <p>Loading stock moves...</p>
    </div>

    <div v-else-if="stockMoveStore.error" class="text-danger text-center py-8">
      {{ stockMoveStore.error }}
    </div>

    <div v-else-if="stockMoveStore.stockMoves.length === 0" class="text-center py-8">
      <p>No stock moves found.</p>
      <router-link :to="{ name: 'StockMoveCreate' }" class="btn btn-primary mt-4">
        Create Your First Stock Move
      </router-link>
    </div>

    <StockMoveTable v-else :stockMoves="stockMoveStore.stockMoves" />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useStockMoveStore } from '@/store/stockMoveStore'
import StockMoveTable from '@/components/tables/StockMoveTable.vue'

const stockMoveStore = useStockMoveStore()

onMounted(async () => {
  if (stockMoveStore.stockMoves.length === 0) {
    await stockMoveStore.fetchStockMoves()
  }
})
</script>