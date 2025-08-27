<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Sign in to DIMA WMS
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Warehouse Management System v1.20.3
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="username" class="sr-only">Username</label>
            <input
              id="username"
              v-model="username"
              name="username"
              type="text"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="Username"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              v-model="password"
              name="password"
              type="password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="Password"
            />
          </div>
        </div>

        <div v-if="error" class="text-danger text-sm text-center">
          {{ error }}
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="h-5 w-5 text-primary-500 group-hover:text-primary-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
              </svg>
            </span>
            {{ loading ? 'Signing in...' : 'Sign in' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/store/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    await authStore.login({
      username: username.value,
      password: password.value
    })
    router.push('/')
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>