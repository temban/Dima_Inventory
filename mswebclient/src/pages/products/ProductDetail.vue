<template>
  <div>
    <div class="app-header">
      <h1 class="app-title">Product Details</h1>
      <div class="flex space-x-2">
        <router-link :to="{ name: 'ProductEdit', params: { id: productId } }" class="btn">
          Edit
        </router-link>
        <router-link :to="{ name: 'Products' }" class="btn">
          Back to Products
        </router-link>
      </div>
    </div>

    <div v-if="loading" class="text-center py-8">
      <p>Loading product details...</p>
    </div>

    <div v-else-if="!product" class="text-center py-8">
      <p>Product not found.</p>
    </div>

    <div v-else class="card">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 class="section-title">Basic Information</h3>
          <dl class="space-y-2">
            <div>
              <dt class="font-medium text-gray-500">Internal Reference</dt>
              <dd class="mt-1 text-gray-900">{{ product.internal_reference }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Name</dt>
              <dd class="mt-1 text-gray-900">{{ product.name }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Category</dt>
              <dd class="mt-1 text-gray-900">{{ product.category_name || 'N/A' }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Product Type</dt>
              <dd class="mt-1 text-gray-900">{{ product.product_type }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Barcode</dt>
              <dd class="mt-1 text-gray-900">{{ product.barcode || 'N/A' }}</dd>
            </div>
          </dl>
        </div>

        <div>
          <h3 class="section-title">Pricing & Stock</h3>
          <dl class="space-y-2">
            <div>
              <dt class="font-medium text-gray-500">Sales Price</dt>
              <dd class="mt-1 text-gray-900">${{ product.sales_price }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Cost</dt>
              <dd class="mt-1 text-gray-900">${{ product.cost }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Total Quantity on Hand</dt>
              <dd class="mt-1 text-gray-900">{{ product.quantity_on_hand }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Forecasted Quantity</dt>
              <dd class="mt-1 text-gray-900">{{ product.forecasted_quantity }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 class="section-title">Relations</h3>
          <dl class="space-y-2">
            <div>
              <dt class="font-medium text-gray-500">Supplier</dt>
              <dd class="mt-1 text-gray-900">{{ product.supplier_name || 'N/A' }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Default Location</dt>
              <dd class="mt-1 text-gray-900">{{ product.location_name || 'N/A' }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Responsible</dt>
              <dd class="mt-1 text-gray-900">{{ product.responsible || 'N/A' }}</dd>
            </div>
          </dl>
        </div>

        <div>
          <h3 class="section-title">Metadata</h3>
          <dl class="space-y-2">
            <div>
              <dt class="font-medium text-gray-500">Favorite</dt>
              <dd class="mt-1 text-gray-900">{{ product.favorite }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Activity Exception</dt>
              <dd class="mt-1 text-gray-900">{{ product.activity_exception_decoration || 'N/A' }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Created</dt>
              <dd class="mt-1 text-gray-900">{{ formatDate(product.created_at) }}</dd>
            </div>
            <div>
              <dt class="font-medium text-gray-500">Last Updated</dt>
              <dd class="mt-1 text-gray-900">{{ formatDate(product.updated_at) }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <div class="mt-6">
        <h3 class="section-title">Real-time Inventory by Location</h3>
        <div v-if="inventoryLoading" class="text-center py-4">
          <p>Loading inventory levels...</p>
        </div>
        <div v-else-if="inventoryError" class="text-danger text-center py-4">
          {{ inventoryError }}
        </div>
        <div v-else-if="inventoryLevels.length === 0" class="text-center py-4">
          <p>No inventory data available for this product.</p>
        </div>
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 mt-2">
  <thead class="bg-gray-50">
    <tr>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
        Product
      </th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
        SKU
      </th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
        Location
      </th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
        Code
      </th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
        Quantity
      </th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
        Last Updated
      </th>
    </tr>
  </thead>
  <tbody class="bg-white divide-y divide-gray-200">
    <tr v-for="level in inventoryLevels" :key="level.id">
      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
        {{ product?.name || product?.product_name }}
      </td>
      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
        {{ product?.internal_reference || product?.product_sku }}
      </td>
      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
        {{ level.location_name }}
      </td>
      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
        {{ level.location_code }}
      </td>
      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
        <span :class="{
          'text-green-600': level.quantity > 10,
          'text-yellow-600': level.quantity > 0 && level.quantity <= 10,
          'text-red-600': level.quantity === 0
        }" class="font-bold">
          {{ level.quantity }}
        </span>
      </td>
      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
        {{ formatDate(level.last_updated) }}
      </td>
    </tr>
  </tbody>
</table>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useProductStore } from '@/store/productStore'
import { formatDate } from '@/utils/formatters'
import type { Product } from '@/types'

const route = useRoute()
const productStore = useProductStore()

const loading = ref(false)
const inventoryLoading = ref(false)
const inventoryError = ref<string | null>(null)
const product = ref<Product>()
const inventoryLevels = ref<any[]>([]) 

const productId = parseInt(route.params.id as string)

onMounted(async () => {
  loading.value = true
  try {
    if (productStore.products.length === 0) {
      await productStore.fetchProducts()
    }
    product.value = productStore.getProductById(productId)
    
    await fetchInventoryLevels()
  } catch (error) {
    console.error('Failed to load product:', error)
  } finally {
    loading.value = false
  }
})

const fetchInventoryLevels = async () => {
  inventoryLoading.value = true
  inventoryError.value = null
  try {
    const raw = await productStore.fetchInventoryLevels({ product_id: productId })
    console.log("Raw inventory response:", raw)

    const productData = raw[productId]
    if (!productData || !productData.locations) {
      inventoryLevels.value = []
      return
    }
    inventoryLevels.value = Object.entries(productData.locations).map(([locId, data]: any) => ({
      id: locId,
      ...data
    }))

    console.log("Mapped Levels:", inventoryLevels.value)
  } catch (error: any) {
    inventoryError.value = error.message || 'Failed to load inventory levels'
    console.error('Failed to load inventory levels:', error)
  } finally {
    inventoryLoading.value = false
  }
}
</script>
