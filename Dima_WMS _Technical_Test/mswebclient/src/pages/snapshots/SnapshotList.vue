<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">Inventory Snapshots</h1>
      <div class="flex space-x-2">
        <button @click="showCreateForm = true" class="btn btn-primary">
          Create Manual Snapshot
        </button>
        <button @click="captureAllSnapshots" class="btn btn-secondary" :disabled="loading">
          {{ loading ? 'Capturing All...' : 'Capture All Products' }}
        </button>
        <button @click="refreshInventory" class="btn" :disabled="loading">
          Refresh
        </button>
      </div>
    </div>

    <div v-if="showCreateForm" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-medium mb-4">Create Manual Snapshot</h3>
        
        <div class="space-y-4">
          <div>
            <label class="form-label">Product *</label>
            <select v-model="newSnapshot.product" class="text-input" required>
              <option :value="null">Select Product</option>
              <option v-for="product in productStore.products" :key="product.id" :value="product.id">
                {{ product.name }} ({{ product.internal_reference }})
              </option>
            </select>
          </div>

          <div>
            <label class="form-label">Location *</label>
            <select v-model="newSnapshot.location" class="text-input" required>
              <option :value="null">Select Location</option>
              <option v-for="location in locationStore.locations" :key="location.id" :value="location.id">
                {{ location.name }} ({{ location.code }})
              </option>
            </select>
          </div>

          <div>
            <label class="form-label">Quantity *</label>
            <input v-model="newSnapshot.quantity" type="number" class="text-input" required>
          </div>

          <div class="flex space-x-2 pt-4">
            <button @click="createManualSnapshot" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Creating...' : 'Create Snapshot' }}
            </button>
            <button @click="showCreateForm = false" class="btn">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center py-8">
      <p>Loading inventory data...</p>
    </div>

    <div v-else-if="error" class="text-danger text-center py-8">
      <p>Error: {{ error }}</p>
      <button @click="refreshInventory" class="btn btn-primary mt-2">Retry</button>
    </div>

    <div v-else-if="snapshots.length === 0" class="text-center py-8">
      <p>No snapshots available yet.</p>
      <p class="text-gray-500 text-sm mt-2">Create your first snapshot to track inventory levels.</p>
    </div>

    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Timestamp
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Product
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Location
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Quantity
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="snapshot in snapshots" :key="snapshot.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatDateTime(snapshot.timestamp) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              {{ snapshot.product_name }} ({{ snapshot.product_internal_reference }})
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ snapshot.location_name }} ({{ snapshot.location_code }})
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              <span :class="{
                'text-green-600': snapshot.quantity > 0,
                'text-red-600': snapshot.quantity === 0
              }" class="font-bold">
                {{ snapshot.quantity }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
            <router-link
              :to="{ name: 'SnapshotDetail', params: { id: snapshot.id } }"
              class="text-primary hover:text-primary-600 mr-4"
            >
              View Details
            </router-link>
            <button
              @click="deleteSnapshot(snapshot.id)"
              class="text-danger hover:text-danger-600"
            >
              Delete
            </button>
          </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useSnapshotStore } from '@/store/snapshotStore'
import { useProductStore } from '@/store/productStore'
import { useLocationStore } from '@/store/locationStore'
import { formatDateTime } from '@/utils/formatters'
import type { SnapshotCreate } from '@/types'

const snapshotStore = useSnapshotStore()
const productStore = useProductStore()
const locationStore = useLocationStore()

const loading = ref(false)
const error = ref<string | null>(null)
const showCreateForm = ref(false)

const newSnapshot = ref<SnapshotCreate>({
  product: null as unknown as number,
  location: null as unknown as number,
  quantity: 0
})

const snapshots = computed(() => snapshotStore.snapshots)

onMounted(async () => {
  await loadData()
})

const loadData = async () => {
  loading.value = true
  error.value = null
  
  try {
    await Promise.all([
      productStore.fetchProducts(),
      locationStore.fetchLocations(),
      snapshotStore.fetchSnapshots()
    ])
    
    console.log('Products loaded:', productStore.products.length)
    console.log('Locations loaded:', locationStore.locations.length)
    console.log('Snapshots loaded:', snapshotStore.snapshots.length)
    
  } catch (err: any) {
    error.value = err.message || 'Failed to load data'
    console.error('Load error:', err)
  } finally {
    loading.value = false
  }
}

const createManualSnapshot = async () => {
  if (!newSnapshot.value.product || !newSnapshot.value.location) {
    error.value = 'Please select both product and location'
    return
  }

  loading.value = true
  try {
    await snapshotStore.createSnapshot(newSnapshot.value)
    showCreateForm.value = false
    newSnapshot.value = {
      product: null as unknown as number,
      location: null as unknown as number,
      quantity: 0
    }
    await snapshotStore.fetchSnapshots() 
  } catch (err: any) {
    error.value = err.message || 'Failed to create snapshot'
  } finally {
    loading.value = false
  }
}

const captureAllSnapshots = async () => {
  loading.value = true
  try {
    await snapshotStore.captureAll()
    await snapshotStore.fetchSnapshots() 
  } catch (err: any) {
    error.value = err.message || 'Failed to capture all snapshots'
  } finally {
    loading.value = false
  }
}
const deleteSnapshot = async (id: number) => {
  if (!confirm('Are you sure you want to delete this snapshot?')) return
  
  try {
    await snapshotStore.deleteSnapshot(id)
    await snapshotStore.fetchSnapshots() 
  } catch (err: any) {
    error.value = err.message || 'Failed to delete snapshot'
  }
}
const refreshInventory = async () => {
  await loadData()
}
</script>