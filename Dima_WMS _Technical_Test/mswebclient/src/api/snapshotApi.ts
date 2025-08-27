import axiosInstance from './axiosInstance'
import type { InventorySnapshot, SnapshotCreate, PaginatedResponse } from '@/types'

export const snapshotApi = {
  async getSnapshots(params?: { product_id?: number; location_id?: number }): Promise<PaginatedResponse<InventorySnapshot>> {
    const response = await axiosInstance.get('/snapshots/', { params })
    return response.data
  },

  async getSnapshot(id: number): Promise<InventorySnapshot> {
    const response = await axiosInstance.get(`/snapshots/${id}/`)
    return response.data
  },

  async createSnapshot(snapshot: SnapshotCreate): Promise<InventorySnapshot> {
    const response = await axiosInstance.post('/snapshots/', snapshot)
    return response.data
  },

  async captureAll(): Promise<void> {
    await axiosInstance.post('/snapshots/capture_all/')
  },

  async getCurrentInventory(params?: { location_id?: number; product_id?: number }): Promise<PaginatedResponse<InventorySnapshot>> {
    const response = await axiosInstance.get('/snapshots/current_inventory/', { params })
    return response.data
  },

  async getInventoryHistory(productId: number, locationId?: number): Promise<InventorySnapshot[]> {
    const params = locationId ? { product_id: productId, location_id: locationId } : { product_id: productId }
    const response = await axiosInstance.get('/snapshots/', { params })
    return response.data.results
  },
  async deleteSnapshot(id: number): Promise<void> {
  await axiosInstance.delete(`/snapshots/${id}/`)
}
}