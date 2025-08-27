<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Reference
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Name
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Category
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Stock
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Price
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Actions
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="product in products" :key="product.id">
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
            {{ product.internal_reference }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            {{ product.name }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {{ product.category_name || 'N/A' }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            <span :class="{
              'text-green-600': product.quantity_on_hand > 10,
              'text-yellow-600': product.quantity_on_hand > 0 && product.quantity_on_hand <= 10,
              'text-red-600': product.quantity_on_hand === 0
            }">
              {{ product.quantity_on_hand }}
            </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            ${{ product.sales_price }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
            <router-link
              :to="{ name: 'ProductEdit', params: { id: product.id } }"
              class="text-primary hover:text-primary-600 mr-4"
            >
              Edit
            </router-link>
            <router-link
              :to="{ name: 'ProductDetail', params: { id: product.id } }"
              class="text-primary hover:text-primary-600 mr-4"
            >
              View
            </router-link>
            <button
              @click="deleteProduct(product.id)"
              class="text-danger hover:text-danger-600"
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { useProductStore } from '@/store/productStore'
import type { Product } from '@/types'

interface Props {
  products: Product[]
}

const props = defineProps<Props>()
const productStore = useProductStore()

const deleteProduct = async (id: number) => {
  if (confirm('Are you sure you want to delete this product?')) {
    try {
      await productStore.deleteProduct(id)
    } catch (error) {
      alert('Failed to delete product')
    }
  }
}
</script>