<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Code
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Name
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Actions
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="location in locations" :key="location.id">
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
            {{ location.code }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            {{ location.name }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
            <router-link
              :to="{ name: 'LocationEdit', params: { id: location.id } }"
              class="text-primary hover:text-primary-600 mr-4"
            >
              Edit
            </router-link>
            <button
              @click="deleteLocation(location.id)"
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
import { useLocationStore } from '@/store/locationStore'
import type { Location } from '@/types'

interface Props {
  locations: Location[]
}

const props = defineProps<Props>()
const locationStore = useLocationStore()

const deleteLocation = async (id: number) => {
  if (confirm('Are you sure you want to delete this location?')) {
    try {
      await locationStore.deleteLocation(id)
    } catch (error) {
      alert('Failed to delete location')
    }
  }
}
</script>