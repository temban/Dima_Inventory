<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">{{ isEditing ? 'Edit Product' : 'Create Product' }}</h1>
      <router-link :to="{ name: 'Products' }" class="btn">
        Back to Products
      </router-link>
    </div>

    <div v-if="loading" class="text-center py-8">
      <p>Loading...</p>
    </div>

    <ProductForm
      v-else
      :product="currentProduct"
      @submit="handleSubmit"
      @cancel="handleCancel"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '@/store/productStore'
import ProductForm from '@/components/forms/ProductForm.vue'
import type { Product, ProductCreate } from '@/types'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()

const loading = ref(false)
const isEditing = computed(() => route.name === 'ProductEdit')
const productId = computed(() => parseInt(route.params.id as string))

const currentProduct = ref<Product>()

onMounted(async () => {
  if (isEditing.value) {
    loading.value = true
    try {
      const product = await productStore.fetchProductById(productId.value)
      if (product) {
        currentProduct.value = product
      } else {
        router.push({ name: 'Products' })
      }
    } catch (error) {
      console.error('Failed to load product:', error)
      router.push({ name: 'Products' })
    } finally {
      loading.value = false
    }
  }
})

const handleSubmit = async (productData: ProductCreate) => {
  loading.value = true
  try {
    if (isEditing.value) {
      await productStore.updateProduct(productId.value, productData)
    } else {
      await productStore.createProduct(productData)
    }
    router.push({ name: 'Products' })
  } catch (error) {
    console.error('Failed to save product:', error)
    alert('Failed to save product. Please try again.')
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  router.push({ name: 'Products' })
}
</script>