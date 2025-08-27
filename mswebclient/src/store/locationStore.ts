import { defineStore } from 'pinia'
import { ref } from 'vue'
import { locationApi } from '@/api/locationApi'
import type { Location, LocationCreate } from '@/types'

export const useLocationStore = defineStore('locations', () => {
  const locations = ref<Location[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

const fetchLocations = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await locationApi.getLocations()
    locations.value = response.results
  } catch (err) {
    error.value = 'Failed to fetch locations'
    console.error(err)
  } finally {
    loading.value = false
  }
}

  const createLocation = async (locationData: LocationCreate) => {
    loading.value = true
    error.value = null
    try {
      const location = await locationApi.createLocation(locationData)
      locations.value.push(location)
      return location
    } catch (err) {
      error.value = 'Failed to create location'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateLocation = async (id: number, locationData: Partial<LocationCreate>) => {
    loading.value = true
    error.value = null
    try {
      const location = await locationApi.updateLocation(id, locationData)
      const index = locations.value.findIndex(l => l.id === id)
      if (index !== -1) {
        locations.value[index] = location
      }
      return location
    } catch (err) {
      error.value = 'Failed to update location'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteLocation = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      await locationApi.deleteLocation(id)
      locations.value = locations.value.filter(l => l.id !== id)
    } catch (err) {
      error.value = 'Failed to delete location'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const getLocationById = (id: number) => {
    return locations.value.find(l => l.id === id)
  }

  return {
    locations,
    loading,
    error,
    fetchLocations,
    createLocation,
    updateLocation,
    deleteLocation,
    getLocationById
  }
})