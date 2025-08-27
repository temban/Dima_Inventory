<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">{{ isEditing ? 'Edit Supplier' : 'Create Supplier' }}</h1>
      <router-link :to="{ name: 'Suppliers' }" class="btn">
        Back to Suppliers
      </router-link>
    </div>

    <div v-if="loading" class="text-center py-8">
      <p>Loading...</p>
    </div>

    <SupplierForm
      v-else
      :supplier="currentSupplier"
      @submit="handleSubmit"
      @cancel="handleCancel"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSupplierStore } from '@/store/supplierStore'
import SupplierForm from '@/components/forms/SupplierForm.vue'
import type { Supplier, SupplierCreate } from '@/types'

const route = useRoute()
const router = useRouter()
const supplierStore = useSupplierStore()

const loading = ref(false)
const isEditing = computed(() => route.name === 'SupplierEdit')
const supplierId = computed(() => parseInt(route.params.id as string))

const currentSupplier = ref<Supplier>()

onMounted(async () => {
  if (isEditing.value) {
    loading.value = true
    try {
      await Promise.all([
        supplierStore.suppliers.length === 0 ? supplierStore.fetchSuppliers() : Promise.resolve(),
        supplierStore.addressTypes.length === 0 ? supplierStore.fetchAddressTypes() : Promise.resolve()
      ])
      
      const supplier = supplierStore.getSupplierById(supplierId.value)
      if (supplier) {
        currentSupplier.value = supplier
      } else {
        router.push({ name: 'Suppliers' })
      }
    } catch (error) {
      console.error('Failed to load supplier:', error)
      router.push({ name: 'Suppliers' })
    } finally {
      loading.value = false
    }
  }
})

const handleSubmit = async (supplierData: SupplierCreate) => {
  loading.value = true
  try {
    if (isEditing.value) {
      await supplierStore.updateSupplier(supplierId.value, supplierData)
    } else {
      await supplierStore.createSupplier(supplierData)
    }
    router.push({ name: 'Suppliers' })
  } catch (error) {
    console.error('Failed to save supplier:', error)
    alert('Failed to save supplier. Please try again.')
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  router.push({ name: 'Suppliers' })
}
</script>