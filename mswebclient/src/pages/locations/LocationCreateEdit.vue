<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">{{ isEditing ? 'Edit Location' : 'Create Location' }}</h1>
      <router-link :to="{ name: 'Locations' }" class="btn">
        Back to Locations
      </router-link>
    </div>

    <div v-if="loading" class="text-center py-8">
      <p>Loading...</p>
    </div>

    <LocationForm
      v-else
      :location="currentLocation"
      @submit="handleSubmit"
      @cancel="handleCancel"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useLocationStore } from '@/store/locationStore'
import LocationForm from '@/components/forms/LocationForm.vue'
import type { Location, LocationCreate } from '@/types'

const route = useRoute()
const router = useRouter()
const locationStore = useLocationStore()

const loading = ref(false)
const isEditing = computed(() => route.name === 'LocationEdit')
const locationId = computed(() => parseInt(route.params.id as string))

const currentLocation = ref<Location>()

onMounted(async () => {
  if (isEditing.value) {
    loading.value = true
    try {
      if (locationStore.locations.length === 0) {
        await locationStore.fetchLocations()
      }
      const location = locationStore.getLocationById(locationId.value)
      if (location) {
        currentLocation.value = location
      } else {
        router.push({ name: 'Locations' })
      }
    } catch (error) {
      console.error('Failed to load location:', error)
      router.push({ name: 'Locations' })
    } finally {
      loading.value = false
    }
  }
})

const handleSubmit = async (locationData: LocationCreate) => {
  loading.value = true
  try {
    if (isEditing.value) {
      await locationStore.updateLocation(locationId.value, locationData)
    } else {
      await locationStore.createLocation(locationData)
    }
    router.push({ name: 'Locations' })
  } catch (error) {
    console.error('Failed to save location:', error)
    alert('Failed to save location. Please try again.')
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  router.push({ name: 'Locations' })
}
</script>