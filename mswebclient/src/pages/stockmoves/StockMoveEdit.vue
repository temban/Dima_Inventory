<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">Edit Stock Move</h1>
      <router-link :to="{ name: 'StockMoves' }" class="btn">
        Back to Stock Moves
      </router-link>
    </div>

    <!-- Error alert banner -->
    <div v-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <div class="flex justify-between items-start">
        <div>
          <strong class="font-bold">Error: </strong>
          <span class="block sm:inline">{{ errorMessage }}</span>
        </div>
        <button @click="errorMessage = ''" class="text-red-700 hover:text-red-900">
          <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
          </svg>
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-8">
      <p>Loading...</p>
    </div>

    <StockMoveForm
      v-else
      :stockMove="currentStockMove"
      @submit="handleSubmit"
      @cancel="handleCancel"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStockMoveStore } from '@/store/stockMoveStore'
import StockMoveForm from '@/components/forms/StockMoveForm.vue'
import type { StockMove, StockMoveCreate } from '@/types'

const route = useRoute()
const router = useRouter()
const stockMoveStore = useStockMoveStore()

const loading = ref(false)
const errorMessage = ref('')
const stockMoveId = computed(() => parseInt(route.params.id as string))

const currentStockMove = ref<StockMove>()

onMounted(async () => {
  loading.value = true
  errorMessage.value = ''
  try {
    currentStockMove.value = await stockMoveStore.fetchStockMove(stockMoveId.value)
    if (!currentStockMove.value) {
      router.push({ name: 'StockMoves' })
    }
  } catch (error: any) {
    console.error('Failed to load stock move:', error)
    errorMessage.value = error.response?.data?.error || error.response?.data?.detail || 'Failed to load stock move'
  } finally {
    loading.value = false
  }
})

const handleSubmit = async (stockMoveData: StockMoveCreate) => {
  loading.value = true
  errorMessage.value = ''
  try {
    await stockMoveStore.updateStockMove(stockMoveId.value, stockMoveData)
    router.push({ name: 'StockMoves' })
  } catch (error: any) {
    console.error('Failed to update stock move:', error)
    
    const backendError = error.response?.data?.error || 
                        error.response?.data?.detail || 
                        error.response?.data?.message ||
                        error.message ||
                        'Failed to update stock move. Please try again.'
    
    errorMessage.value = backendError
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  router.push({ name: 'StockMoves' })
}
</script>