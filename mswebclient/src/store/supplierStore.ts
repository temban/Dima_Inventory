import { defineStore } from 'pinia'
import { ref } from 'vue'
import { supplierApi } from '@/api/supplierApi'
import type { Supplier, SupplierCreate, AddressType, PaginatedResponse } from '@/types'

export const useSupplierStore = defineStore('suppliers', () => {
  const suppliers = ref<Supplier[]>([])
  const addressTypes = ref<AddressType[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchSuppliers = async () => {
    loading.value = true
    error.value = null
    try {
      const response: PaginatedResponse<Supplier> = await supplierApi.getSuppliers()
      suppliers.value = response.results
    } catch (err) {
      error.value = 'Failed to fetch suppliers'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  const fetchAddressTypes = async () => {
    loading.value = true
    error.value = null
    try {
      const response: PaginatedResponse<AddressType> = await supplierApi.getAddressTypes()
      addressTypes.value = response.results
    } catch (err) {
      error.value = 'Failed to fetch address types'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  const createSupplier = async (supplierData: SupplierCreate) => {
    loading.value = true
    error.value = null
    try {
      const supplier = await supplierApi.createSupplier(supplierData)
      suppliers.value.push(supplier)
      return supplier
    } catch (err) {
      error.value = 'Failed to create supplier'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateSupplier = async (id: number, supplierData: Partial<SupplierCreate>) => {
    loading.value = true
    error.value = null
    try {
      const supplier = await supplierApi.updateSupplier(id, supplierData)
      const index = suppliers.value.findIndex(s => s.id === id)
      if (index !== -1) {
        suppliers.value[index] = supplier
      }
      return supplier
    } catch (err) {
      error.value = 'Failed to update supplier'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteSupplier = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      await supplierApi.deleteSupplier(id)
      suppliers.value = suppliers.value.filter(s => s.id !== id)
    } catch (err) {
      error.value = 'Failed to delete supplier'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const getSupplierById = (id: number) => {
    return suppliers.value.find(s => s.id === id)
  }

  return {
    suppliers,
    addressTypes,
    loading,
    error,
    fetchSuppliers,
    fetchAddressTypes,
    createSupplier,
    updateSupplier,
    deleteSupplier,
    getSupplierById
  }
})