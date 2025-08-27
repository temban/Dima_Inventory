<template>
  <nav class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <h1 class="text-xl font-semibold text-gray-900">DIMA WMS</h1>
        </div>
        <div class="flex items-center space-x-4">
          <router-link 
            v-for="item in navItems" 
            :key="item.route"
            :to="{ name: item.route }"
            class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            active-class="text-primary border-b-2 border-primary"
          >
            {{ item.label }}
          </router-link>
          <button
            @click="logout"
            class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/store/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const navItems = [
  { label: 'Products', route: 'Products' },
  { label: 'Suppliers', route: 'Suppliers' },
  { label: 'Stock Moves', route: 'StockMoves' },
  { label: 'Locations', route: 'Locations' },
  { label: 'Snapshots', route: 'Snapshots' }
]

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>