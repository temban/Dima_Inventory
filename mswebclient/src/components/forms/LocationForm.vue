<template>
  <form @submit.prevent="submitForm" class="space-y-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="form-label">Code *</label>
        <input
          v-model="form.code"
          type="text"
          class="text-input"
          :class="{ 'border-danger': errors.code }"
          placeholder="Location Code"
          required
        />
        <p v-if="errors.code" class="text-danger text-sm mt-1">{{ errors.code }}</p>
      </div>

      <div>
        <label class="form-label">Name *</label>
        <input
          v-model="form.name"
          type="text"
          class="text-input"
          :class="{ 'border-danger': errors.name }"
          placeholder="Location Name"
          required
        />
        <p v-if="errors.name" class="text-danger text-sm mt-1">{{ errors.name }}</p>
      </div>
    </div>

    <div>
      <label class="form-label">Description</label>
      <textarea
        v-model="form.description"
        class="text-input"
        rows="3"
        placeholder="Location description"
      ></textarea>
    </div>

    <div>
      <label class="form-label">Status</label>
      <div class="mt-2">
        <label class="inline-flex items-center">
          <input
            v-model="form.is_active"
            type="checkbox"
            class="rounded border-gray-300 text-primary focus:ring-primary"
          >
          <span class="ml-2">Active</span>
        </label>
      </div>
    </div>

    <div class="flex space-x-4 pt-4">
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Saving...' : 'Save Location' }}
      </button>
      <button type="button" class="btn" @click="$emit('cancel')">Cancel</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import type { Location, LocationCreate } from '@/types'

interface Props {
  location?: Location
}

interface Emits {
  (e: 'submit', data: LocationCreate): void
  (e: 'cancel'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const loading = ref(false)
const errors = reactive<Record<string, string>>({})

const form = reactive({
  code: '',
  name: '',
  description: null as string | null,
  is_active: true
})

watch(() => props.location, (newLocation) => {
  if (newLocation) {
    form.code = newLocation.code || ''
    form.name = newLocation.name || ''
    form.description = newLocation.description 
    form.is_active = newLocation.is_active
  }
}, { immediate: true })

const submitForm = async () => {
  loading.value = true
  Object.keys(errors).forEach(key => delete errors[key])
  
  if (!form.code.trim()) errors.code = 'Code is required'
  if (!form.name.trim()) errors.name = 'Name is required'

  if (Object.keys(errors).length > 0) {
    loading.value = false
    return
  }

  const locationData: LocationCreate = {
    code: form.code.trim(),
    name: form.name.trim(),
    description: form.description ? form.description.trim() : null,
    is_active: form.is_active
  }

  emit('submit', locationData)
  loading.value = false
}
</script>