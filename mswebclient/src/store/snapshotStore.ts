import { defineStore } from 'pinia'
import { ref } from 'vue'
import { snapshotApi } from '@/api/snapshotApi'
import type { InventorySnapshot, SnapshotCreate, PaginatedResponse } from '@/types'

export const useSnapshotStore = defineStore('snapshots', () => {
  const snapshots = ref<InventorySnapshot[]>([])
  const currentInventory = ref<InventorySnapshot[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchSnapshots = async (params?: { product_id?: number; location_id?: number }) => {
    loading.value = true
    error.value = null
    try {
      const response: PaginatedResponse<InventorySnapshot> = await snapshotApi.getSnapshots(params)
      snapshots.value = response.results
    } catch (err) {
      error.value = 'Failed to fetch snapshots'
      console.error('Snapshot fetch error:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchCurrentInventory = async (params?: { location_id?: number; product_id?: number }) => {
    loading.value = true
    error.value = null
    try {
      console.log('Fetching current inventory...')
      const response: PaginatedResponse<InventorySnapshot> = await snapshotApi.getCurrentInventory(params)
      console.log('Current inventory response:', response)
      currentInventory.value = response.results
    } catch (err) {
      error.value = 'Failed to fetch current inventory'
      console.error('Current inventory fetch error:', err)
    } finally {
      loading.value = false
    }
  }

  const createSnapshot = async (snapshotData: SnapshotCreate) => {
    loading.value = true
    error.value = null
    try {
      const snapshot = await snapshotApi.createSnapshot(snapshotData)
      snapshots.value.push(snapshot)
      return snapshot
    } catch (err) {
      error.value = 'Failed to create snapshot'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }
const deleteSnapshot = async (id: number) => {
  loading.value = true
  error.value = null
  try {
    await snapshotApi.deleteSnapshot(id)
    snapshots.value = snapshots.value.filter(s => s.id !== id)
  } catch (err) {
    error.value = 'Failed to delete snapshot'
    console.error(err)
    throw err
  } finally {
    loading.value = false
  }
}
  const captureAll = async () => {
    loading.value = true
    error.value = null
    try {
      await snapshotApi.captureAll()
      await fetchCurrentInventory()
    } catch (err) {
      error.value = 'Failed to capture all snapshots'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const getSnapshotById = (id: number) => {
    return snapshots.value.find(s => s.id === id)
  }

  const getProductHistory = async (productId: number, locationId?: number) => {
    try {
      return await snapshotApi.getInventoryHistory(productId, locationId)
    } catch (err) {
      error.value = 'Failed to fetch product history'
      console.error(err)
      return []
    }
  }

  return {
    snapshots,
    currentInventory,
    loading,
    error,
    fetchSnapshots,
    fetchCurrentInventory,
    createSnapshot,
    captureAll,
    getSnapshotById,
    getProductHistory,
    deleteSnapshot
  }
})