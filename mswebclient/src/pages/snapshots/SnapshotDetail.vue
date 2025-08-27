<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">Snapshot Details</h1>
      <router-link :to="{ name: 'Snapshots' }" class="btn">
        Back to Snapshots
      </router-link>
    </div>

    <div v-if="loading" class="text-center py-8">
      <p>Loading snapshot details...</p>
    </div>

    <div v-else-if="!snapshot" class="text-center py-8">
      <p>Snapshot not found.</p>
    </div>

    <div v-else class="card">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 class="section-title">Snapshot Information</h3>
          <dl class="space-y-2">
            <div>
              <dt class="font-medium text-gray-500">Snapshot ID</dt>
              <dd class="mt-1 text-gray-900">{{ snapshot.id }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Timestamp</dt>
              <dd class="mt-1 text-gray-900">{{ formatDateTime(snapshot.timestamp) }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Quantity Recorded</dt>
              <dd class="mt-1 text-gray-900 text-2xl font-bold">
                <span :class="{
                  'text-green-600': snapshot.quantity > 0,
                  'text-red-600': snapshot.quantity === 0
                }">
                  {{ snapshot.quantity }}
                </span>
              </dd>
            </div>
          </dl>
        </div>

        <div>
          <h3 class="section-title">Product & Location</h3>
          <dl class="space-y-2">
            <div>
              <dt class="font-medium text-gray-500">Product</dt>
              <dd class="mt-1 text-gray-900">{{ snapshot.product_name }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Product SKU</dt>
              <dd class="mt-1 text-gray-900">{{ snapshot.product_internal_reference }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Location</dt>
              <dd class="mt-1 text-gray-900">{{ snapshot.location_name }} ({{ snapshot.location_code }})</dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useSnapshotStore } from '@/store/snapshotStore'
import { formatDateTime } from '@/utils/formatters'

const route = useRoute()
const snapshotStore = useSnapshotStore()

const loading = ref(false)
const snapshot = ref<any>(null)

const snapshotId = parseInt(route.params.id as string)

onMounted(async () => {
  loading.value = true
  try {
    if (snapshotStore.snapshots.length === 0) {
      await snapshotStore.fetchSnapshots()
    }
    snapshot.value = snapshotStore.getSnapshotById(snapshotId)
  } catch (error) {
    console.error('Failed to load snapshot:', error)
  } finally {
    loading.value = false
  }
})
</script>