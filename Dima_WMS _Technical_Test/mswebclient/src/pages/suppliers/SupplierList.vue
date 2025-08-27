<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">Suppliers</h1>
      <router-link :to="{ name: 'SupplierCreate' }" class="btn btn-primary">
        Add New Supplier
      </router-link>
    </div>

    <div v-if="supplierStore.loading" class="text-center py-8">
      <p>Loading suppliers...</p>
    </div>

    <div v-else-if="supplierStore.error" class="text-danger text-center py-8">
      {{ supplierStore.error }}
    </div>

    <div v-else-if="supplierStore.suppliers.length === 0" class="text-center py-8">
      <p>No suppliers found.</p>
      <router-link :to="{ name: 'SupplierCreate' }" class="btn btn-primary mt-4">
        Create Your First Supplier
      </router-link>
    </div>

    <SupplierTable v-else :suppliers="supplierStore.suppliers" />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useSupplierStore } from '@/store/supplierStore'
import SupplierTable from '@/components/tables/SupplierTable.vue'

const supplierStore = useSupplierStore()

onMounted(async () => {
  if (supplierStore.suppliers.length === 0) {
    await supplierStore.fetchSuppliers()
  }
})
</script>