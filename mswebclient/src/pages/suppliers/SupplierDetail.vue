<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">Supplier Details</h1>
      <div class="flex space-x-2">
        <router-link :to="{ name: 'SupplierEdit', params: { id: supplierId } }" class="btn">
          Edit
        </router-link>
        <button @click="deleteSupplier" class="btn btn-danger">
          Delete
        </button>
        <router-link :to="{ name: 'Suppliers' }" class="btn">
          Back to Suppliers
        </router-link>
      </div>
    </div>

    <div v-if="loading" class="text-center py-8">
      <p>Loading supplier details...</p>
    </div>

    <div v-else-if="!supplier" class="text-center py-8">
      <p>Supplier not found.</p>
    </div>

    <div v-else class="card">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 class="section-title">Basic Information</h3>
          <dl class="space-y-2">
            <div>
              <dt class="font-medium text-gray-500">Name</dt>
              <dd class="mt-1 text-gray-900">{{ supplier.name }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Type</dt>
              <dd class="mt-1 text-gray-900">
                <span :class="supplier.is_company ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'" 
                      class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ supplier.is_company ? 'Company' : 'Individual' }}
                </span>
              </dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Email</dt>
              <dd class="mt-1 text-gray-900">{{ supplier.email || 'N/A' }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Phone</dt>
              <dd class="mt-1 text-gray-900">{{ supplier.phone || 'N/A' }}</dd>
            </div>
          </dl>
        </div>

        <div>
          <h3 class="section-title">Relations</h3>
          <dl class="space-y-2">
            <div>
              <dt class="font-medium text-gray-500">Address Type</dt>
              <dd class="mt-1 text-gray-900">{{ supplier.address_type_name || 'N/A' }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Related Company</dt>
              <dd class="mt-1 text-gray-900">{{ supplier.related_company_name || 'N/A' }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Created</dt>
              <dd class="mt-1 text-gray-900">{{ formatDate(supplier.created_at) }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Last Updated</dt>
              <dd class="mt-1 text-gray-900">{{ formatDate(supplier.updated_at) }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <div class="mt-6">
        <h3 class="section-title">Address Information</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-2">
          <div>
            <dl class="space-y-2">
              <div>
                <dt class="font-medium text-gray-500">Street</dt>
                <dd class="mt-1 text-gray-900">{{ supplier.street || 'N/A' }}</dd>
              </div>
              <div>
                <dt class="font-medium text-gray-500">City</dt>
                <dd class="mt-1 text-gray-900">{{ supplier.city || 'N/A' }}</dd>
              </div>
              <div>
                <dt class="font-medium text-gray-500">Zip Code</dt>
                <dd class="mt-1 text-gray-900">{{ supplier.zip_code || 'N/A' }}</dd>
              </div>
            </dl>
          </div>
          <div>
            <dl class="space-y-2">
              <div>
                <dt class="font-medium text-gray-500">State</dt>
                <dd class="mt-1 text-gray-900">{{ supplier.state || 'N/A' }}</dd>
              </div>
              <div>
                <dt class="font-medium text-gray-500">Country</dt>
                <dd class="mt-1 text-gray-900">{{ supplier.country || 'N/A' }}</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSupplierStore } from '@/store/supplierStore'
import { formatDate } from '@/utils/formatters'
import type { Supplier } from '@/types'

const route = useRoute()
const router = useRouter()
const supplierStore = useSupplierStore()

const loading = ref(false)
const supplier = ref<Supplier>()

const supplierId = parseInt(route.params.id as string)

onMounted(async () => {
  loading.value = true
  try {
    if (supplierStore.suppliers.length === 0) {
      await supplierStore.fetchSuppliers()
    }
    const foundSupplier = supplierStore.getSupplierById(supplierId)
    if (foundSupplier) {
      supplier.value = foundSupplier
    }
  } catch (error) {
    console.error('Failed to load supplier:', error)
  } finally {
    loading.value = false
  }
})

const deleteSupplier = async () => {
  if (confirm('Are you sure you want to delete this supplier?')) {
    try {
      await supplierStore.deleteSupplier(supplierId)
      router.push({ name: 'Suppliers' })
    } catch (error) {
      alert('Failed to delete supplier')
    }
  }
}
</script>