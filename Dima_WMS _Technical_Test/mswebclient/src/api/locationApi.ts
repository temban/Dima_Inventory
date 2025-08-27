import axiosInstance from './axiosInstance'
import type { Location, LocationCreate, PaginatedResponse } from '@/types'

export const locationApi = {
  async getLocations(params?: { is_active?: boolean }): Promise<PaginatedResponse<Location>> {
  const response = await axiosInstance.get('/locations/', { params })
  return response.data
},

  async getLocation(id: number): Promise<Location> {
    const response = await axiosInstance.get(`/locations/${id}/`)
    return response.data
  },

  async createLocation(location: LocationCreate): Promise<Location> {
    const response = await axiosInstance.post('/locations/', location)
    return response.data
  },

  async updateLocation(id: number, location: Partial<LocationCreate>): Promise<Location> {
    const response = await axiosInstance.put(`/locations/${id}/`, location)
    return response.data
  },

  async deleteLocation(id: number): Promise<void> {
    await axiosInstance.delete(`/locations/${id}/`)
  }
}