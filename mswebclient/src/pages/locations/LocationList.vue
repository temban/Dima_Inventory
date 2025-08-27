<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">Locations</h1>
      <router-link :to="{ name: 'LocationCreate' }" class="btn btn-primary">
        Add New Location
      </router-link>
    </div>

    <div v-if="locationStore.loading" class="text-center py-8">
      <p>Loading locations...</p>
    </div>

    <div v-else-if="locationStore.error" class="text-danger text-center py-8">
      {{ locationStore.error }}
    </div>

    <div v-else-if="locationStore.locations.length === 0" class="text-center py-8">
      <p>No locations found.</p>
      <router-link :to="{ name: 'LocationCreate' }" class="btn btn-primary mt-4">
        Create Your First Location
      </router-link>
    </div>

    <LocationTable v-else :locations="locationStore.locations" />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useLocationStore } from '@/store/locationStore'
import LocationTable from '@/components/tables/LocationTable.vue'

const locationStore = useLocationStore()

onMounted(async () => {
  if (locationStore.locations.length === 0) {
    await locationStore.fetchLocations()
  }
})
</script>