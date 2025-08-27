<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">Stock Move Details</h1>
      <div class="flex space-x-2">
        <router-link :to="{ name: 'StockMoveEdit', params: { id: stockMoveId } }" class="btn">
          Edit
        </router-link>
        <button @click="deleteStockMove" class="btn btn-danger">
          Delete
        </button>
        <router-link :to="{ name: 'StockMoves' }" class="btn">
          Back to Stock Moves
        </router-link>
      </div>
    </div>

    <div v-if="loading" class="text-center py-8">
      <p>Loading stock move details...</p>
    </div>

    <div v-else-if="!stockMove" class="text-center py-8">
      <p>Stock move not found.</p>
    </div>

    <div v-else class="card">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 class="section-title">Basic Information</h3>
          <dl class="space-y-2">
            <div>
              <dt class="font-medium text-gray-500">Reference</dt>
              <dd class="mt-1 text-gray-900">{{ stockMove.reference || 'N/A' }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Type</dt>
              <dd class="mt-1 text-gray-900">
                <span
                  :class="{
                    'bg-green-100 text-green-800': stockMove.move_type === 'INBOUND',
                    'bg-red-100 text-red-800': stockMove.move_type === 'OUTBOUND',
                    'bg-blue-100 text-blue-800': stockMove.move_type === 'TRANSFER'
                  }"
                  class="px-2 py-1 text-xs font-medium rounded-full"
                >
                  {{ formatStockMoveType(stockMove.move_type) }}
                </span>
              </dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Description</dt>
              <dd class="mt-1 text-gray-900">{{ stockMove.description || 'N/A' }}</dd>
            </div>
          </dl>
        </div>

        <div>
          <h3 class="section-title">Locations</h3>
          <dl class="space-y-2">
            <div>
              <dt class="font-medium text-gray-500">From Location</dt>
              <dd class="mt-1 text-gray-900">{{ getLocationName(stockMove.from_location) }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">To Location</dt>
              <dd class="mt-1 text-gray-900">{{ getLocationName(stockMove.to_location) }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Status</dt>
              <dd class="mt-1 text-gray-900">
                <span :class="stockMove.completed ? 'text-green-600' : 'text-yellow-600'">
                  {{ stockMove.completed ? 'Completed' : 'Pending' }}
                </span>
              </dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Timestamp</dt>
              <dd class="mt-1 text-gray-900">{{ formatDate(stockMove.timestamp) }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <div class="mt-6">
        <h3 class="section-title">Products</h3>
        <table class="min-w-full divide-y divide-gray-200 mt-2">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Product
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                SKU
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Quantity
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Description
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="line in stockMove.lines" :key="line.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ line.product_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ line.product_internal_reference }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ line.quantity }}
              </td>
              <td class="px-6 py-4 text-sm text-gray-900">
                {{ line.description || 'N/A' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStockMoveStore } from '@/store/stockMoveStore'
import { useLocationStore } from '@/store/locationStore'
import { formatDate, formatStockMoveType } from '@/utils/formatters'
import type { StockMove } from '@/types'

const route = useRoute()
const router = useRouter()
const stockMoveStore = useStockMoveStore()
const locationStore = useLocationStore()

const loading = ref(false)
const stockMove = ref<StockMove>()

const stockMoveId = parseInt(route.params.id as string)

const getLocationName = (locationId: number | null) => {
  if (!locationId) return 'N/A'
  const location = locationStore.locations.find(l => l.id === locationId)
  return location ? `${location.name} (${location.code})` : 'Unknown'
}

onMounted(async () => {
  loading.value = true
  try {
    if (locationStore.locations.length === 0) {
      await locationStore.fetchLocations()
    }
    stockMove.value = await stockMoveStore.fetchStockMove(stockMoveId)
  } catch (error) {
    console.error('Failed to load stock move:', error)
  } finally {
    loading.value = false
  }
})

const deleteStockMove = async () => {
  if (confirm('Are you sure you want to delete this stock move?')) {
    try {
      await stockMoveStore.deleteStockMove(stockMoveId)
      router.push({ name: 'StockMoves' })
    } catch (error) {
      alert('Failed to delete stock move')
    }
  }
}
</script>