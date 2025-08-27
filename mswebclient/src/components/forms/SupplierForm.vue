<template>
  <form @submit.prevent="submitForm" class="space-y-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="form-label">Name *</label>
        <input
          v-model="form.name"
          type="text"
          class="text-input"
          :class="{ 'border-danger': errors.name }"
          placeholder="Supplier Name"
          required
        />
        <p v-if="errors.name" class="text-danger text-sm mt-1">{{ errors.name }}</p>
      </div>

      <div>
        <label class="form-label">Company Type</label>
        <div class="mt-2">
          <label class="inline-flex items-center">
            <input
              v-model="form.is_company"
              type="checkbox"
              class="rounded border-gray-300 text-primary focus:ring-primary"
            >
            <span class="ml-2">Is Company</span>
          </label>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="form-label">Email</label>
        <input
          v-model="form.email"
          type="email"
          class="text-input"
          placeholder="email@example.com"
        />
      </div>

      <div>
        <label class="form-label">Phone</label>
        <input
          v-model="form.phone"
          type="tel"
          class="text-input"
          placeholder="Phone number"
        />
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="form-label">Address Type</label>
        <select
          v-model="form.address_type"
          class="text-input"
        >
          <option :value="null">Select Address Type</option>
          <option
            v-for="addressType in addressTypes"
            :key="addressType.id"
            :value="addressType.id"
          >
            {{ addressType.name }}
          </option>
        </select>
      </div>

      <div v-if="form.is_company">
        <label class="form-label">Related Company</label>
        <select
          v-model="form.related_company"
          class="text-input"
        >
          <option :value="null">Select Related Company</option>
          <option
            v-for="company in companies"
            :key="company.id"
            :value="company.id"
            :disabled="company.id === supplier?.id"
          >
            {{ company.name }}
          </option>
        </select>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="form-label">Street</label>
        <input
          v-model="form.street"
          type="text"
          class="text-input"
          placeholder="Street address"
        />
      </div>

      <div>
        <label class="form-label">Zip Code</label>
        <input
          v-model="form.zip_code"
          type="text"
          class="text-input"
          placeholder="Zip code"
        />
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div>
        <label class="form-label">City</label>
        <input
          v-model="form.city"
          type="text"
          class="text-input"
          placeholder="City"
        />
      </div>

      <div>
        <label class="form-label">State</label>
        <input
          v-model="form.state"
          type="text"
          class="text-input"
          placeholder="State"
        />
      </div>

      <div>
        <label class="form-label">Country</label>
        <input
          v-model="form.country"
          type="text"
          class="text-input"
          placeholder="Country"
        />
      </div>
    </div>

    <div class="flex space-x-4 pt-4">
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Saving...' : 'Save Supplier' }}
      </button>
      <button type="button" class="btn" @click="$emit('cancel')">Cancel</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch, computed } from 'vue'
import { useSupplierStore } from '@/store/supplierStore'
import type { Supplier, SupplierCreate } from '@/types'

interface Props {
  supplier?: Supplier
}

interface Emits {
  (e: 'submit', data: SupplierCreate): void
  (e: 'cancel'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const supplierStore = useSupplierStore()
const loading = ref(false)
const errors = reactive<Record<string, string>>({})

const form = reactive({
  name: '',
  is_company: false,
  street: null as string | null,
  zip_code: null as string | null,
  city: null as string | null,
  state: null as string | null,
  country: null as string | null,
  email: null as string | null,
  phone: null as string | null,
  related_company: null as number | null,
  address_type: null as number | null
})

watch(() => props.supplier, (newSupplier) => {
  if (newSupplier) {
    form.name = newSupplier.name || ''
    form.is_company = newSupplier.is_company || false
    form.street = newSupplier.street
    form.zip_code = newSupplier.zip_code
    form.city = newSupplier.city
    form.state = newSupplier.state
    form.country = newSupplier.country
    form.email = newSupplier.email
    form.phone = newSupplier.phone
    form.related_company = newSupplier.related_company
    form.address_type = newSupplier.address_type
  }
}, { immediate: true })

onMounted(async () => {
  if (supplierStore.suppliers.length === 0) {
    await supplierStore.fetchSuppliers()
  }
  if (supplierStore.addressTypes.length === 0) {
    await supplierStore.fetchAddressTypes()
  }
})

const submitForm = async () => {
  loading.value = true
  Object.keys(errors).forEach(key => delete errors[key])
  
  if (!form.name.trim()) errors.name = 'Name is required'

  if (Object.keys(errors).length > 0) {
    loading.value = false
    return
  }

  const supplierData: SupplierCreate = {
    name: form.name.trim(),
    is_company: form.is_company,
    street: form.street?.trim() || null,
    zip_code: form.zip_code?.trim() || null,
    city: form.city?.trim() || null,
    state: form.state?.trim() || null,
    country: form.country?.trim() || null,
    email: form.email?.trim() || null,
    phone: form.phone?.trim() || null,
    related_company: form.related_company,
    address_type: form.address_type
  }

  emit('submit', supplierData)
  loading.value = false
}

const addressTypes = computed(() => supplierStore.addressTypes)
const companies = computed(() => supplierStore.suppliers.filter(s => s.is_company && s.id !== props.supplier?.id))
</script>