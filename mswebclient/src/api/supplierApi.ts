import axiosInstance from './axiosInstance'
import type { Supplier, SupplierCreate, AddressType, PaginatedResponse } from '@/types'

export const supplierApi = {
  async getSuppliers(params?: { is_company?: boolean }): Promise<PaginatedResponse<Supplier>> {
    const response = await axiosInstance.get('/suppliers/', { params })
    return response.data
  },

  async getSupplier(id: number): Promise<Supplier> {
    const response = await axiosInstance.get(`/suppliers/${id}/`)
    return response.data
  },

  async createSupplier(supplier: SupplierCreate): Promise<Supplier> {
    const response = await axiosInstance.post('/suppliers/', supplier)
    return response.data
  },

  async updateSupplier(id: number, supplier: Partial<SupplierCreate>): Promise<Supplier> {
    const response = await axiosInstance.put(`/suppliers/${id}/`, supplier)
    return response.data
  },

  async deleteSupplier(id: number): Promise<void> {
    await axiosInstance.delete(`/suppliers/${id}/`)
  },

  async getAddressTypes(): Promise<PaginatedResponse<AddressType>> {
    const response = await axiosInstance.get('/suppliers/address-types/')
    return response.data
  }
}