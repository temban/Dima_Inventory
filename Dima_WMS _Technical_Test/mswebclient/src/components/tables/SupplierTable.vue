<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Name
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Type
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Contact Info
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Address
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Relations
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Actions
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="supplier in suppliers" :key="supplier.id">
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
            {{ supplier.name }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            <span :class="supplier.is_company ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'"
              class="px-2 py-1 text-xs font-medium rounded-full">
              {{ supplier.is_company ? 'Company' : 'Individual' }}
            </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            <div v-if="supplier.email">{{ supplier.email }}</div>
            <div v-if="supplier.phone">{{ supplier.phone }}</div>
            <div v-if="!supplier.email && !supplier.phone" class="text-gray-400">No contact info</div>
          </td>
          <td class="px-6 py-4 text-sm text-gray-500">
            <div v-if="supplier.street || supplier.city">
              <div v-if="supplier.street">{{ supplier.street }}</div>
              <div v-if="supplier.city || supplier.zip_code">
                {{ supplier.city }}{{ supplier.zip_code ? `, ${supplier.zip_code}` : '' }}
              </div>
              <div v-if="supplier.state || supplier.country">
                {{ supplier.state }}{{ supplier.country ? `, ${supplier.country}` : '' }}
              </div>
            </div>
            <div v-else class="text-gray-400">No address</div>
          </td>
          <td class="px-6 py-4 text-sm text-gray-500">
            <div v-if="supplier.address_type_name">
              <strong>Address Type:</strong> {{ supplier.address_type_name }}
            </div>
            <div v-if="supplier.related_company_name">
              <strong>Related Company:</strong> {{ supplier.related_company_name }}
            </div>
            <div v-if="!supplier.address_type_name && !supplier.related_company_name" class="text-gray-400">
              No relations
            </div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
            <router-link :to="{ name: 'SupplierDetail', params: { id: supplier.id } }"
              class="text-primary hover:text-primary-600 mr-4">
              View
            </router-link>
            <router-link :to="{ name: 'SupplierEdit', params: { id: supplier.id } }"
              class="text-primary hover:text-primary-600 mr-4">
              Edit
            </router-link>
            <button @click="deleteSupplier(supplier.id)" class="text-danger hover:text-danger-600">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { useSupplierStore } from '@/store/supplierStore'
import type { Supplier } from '@/types'

interface Props {
  suppliers: Supplier[]
}

const props = defineProps<Props>()
const supplierStore = useSupplierStore()

const deleteSupplier = async (id: number) => {
  if (confirm('Are you sure you want to delete this supplier?')) {
    try {
      await supplierStore.deleteSupplier(id)
    } catch (error) {
      alert('Failed to delete supplier')
    }
  }
}
</script>