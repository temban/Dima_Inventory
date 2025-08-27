<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">Products</h1>
      <router-link :to="{ name: 'ProductCreate' }" class="btn btn-primary">
        Add New Product
      </router-link>
    </div>

    <div v-if="productStore.loading" class="text-center py-8">
      <p>Loading products...</p>
    </div>

    <div v-else-if="productStore.error" class="text-danger text-center py-8">
      {{ productStore.error }}
    </div>

    <div v-else-if="productStore.products.length === 0" class="text-center py-8">
      <p>No products found.</p>
      <router-link :to="{ name: 'ProductCreate' }" class="btn btn-primary mt-4">
        Create Your First Product
      </router-link>
    </div>

    <ProductTable v-else :products="productStore.products" />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useProductStore } from '@/store/productStore'
import ProductTable from '@/components/tables/ProductTable.vue'

const productStore = useProductStore()

onMounted(async () => {
  if (productStore.products.length === 0) {
    await productStore.fetchProducts()
  }
})
</script>