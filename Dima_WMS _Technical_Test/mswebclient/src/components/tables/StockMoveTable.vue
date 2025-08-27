<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Reference
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Type
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Timestamp
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Status
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Actions
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="move in stockMoves" :key="move.id">
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
            {{ move.reference || 'N/A' }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <span
              :class="{
                'bg-green-100 text-green-800': move.move_type === 'INBOUND',
                'bg-red-100 text-red-800': move.move_type === 'OUTBOUND',
                'bg-blue-100 text-blue-800': move.move_type === 'TRANSFER'
              }"
              class="px-2 py-1 text-xs font-medium rounded-full"
            >
              {{ formatStockMoveType(move.move_type) }}
            </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {{ formatDate(move.timestamp) }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm">
            <span :class="move.completed ? 'text-green-600' : 'text-yellow-600'">
              {{ move.completed ? 'Completed' : 'Pending' }}
            </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
            <router-link
              :to="{ name: 'StockMoveDetail', params: { id: move.id } }"
              class="text-primary hover:text-primary-600 mr-4"
            >
              View
            </router-link>
            <router-link
              :to="{ name: 'StockMoveEdit', params: { id: move.id } }"
              class="text-primary hover:text-primary-600 mr-4"
            >
              Edit
            </router-link>
            <button
              @click="deleteStockMove(move.id)"
              class="text-danger hover:text-danger-600"
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useLocationStore } from '@/store/locationStore'
import { useStockMoveStore } from '@/store/stockMoveStore'
import { formatDate, formatStockMoveType } from '@/utils/formatters'
import type { StockMove } from '@/types'

interface Props {
  stockMoves: StockMove[]
}

const props = defineProps<Props>()
const locationStore = useLocationStore()
const stockMoveStore = useStockMoveStore()

const getLocationName = (locationId: number | null) => {
  if (!locationId) return '-'
  const location = locationStore.locations.find(l => l.id === locationId)
  return location ? `${location.name} (${location.code})` : 'Unknown'
}

const deleteStockMove = async (id: number) => {
  if (confirm('Are you sure you want to delete this stock move?')) {
    try {
      await stockMoveStore.deleteStockMove(id)
    } catch (error) {
      alert('Failed to delete stock move')
    }
  }
}
</script>