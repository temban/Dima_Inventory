<template>
  <form @submit.prevent="submitForm" class="space-y-4">
    <div>
      <label class="form-label">Type *</label>
      <select
        v-model="form.move_type"
        class="text-input"
        :class="{ 'border-danger': errors.move_type }"
        @change="handleTypeChange"
        :disabled="isEditing"
        required
      >
        <option value="">Select Move Type</option>
        <option value="INBOUND">Inbound</option>
        <option value="OUTBOUND">Outbound</option>
        <option value="TRANSFER">Transfer</option>
      </select>
      <p v-if="errors.move_type" class="text-danger text-sm mt-1">{{ errors.move_type }}</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-if="showFromLocation">
        <label class="form-label">From Location *</label>
        <select
          v-model="form.from_location"
          class="text-input"
          :class="{ 'border-danger': errors.from_location }"
          :disabled="isEditing"
          required
        >
          <option :value="null">Select From Location</option>
          <option
            v-for="location in locations"
            :key="location.id"
            :value="location.id"
          >
            {{ location.name }} ({{ location.code }})
          </option>
        </select>
        <p v-if="errors.from_location" class="text-danger text-sm mt-1">{{ errors.from_location }}</p>
      </div>

      <div v-if="showToLocation">
        <label class="form-label">To Location *</label>
        <select
          v-model="form.to_location"
          class="text-input"
          :class="{ 'border-danger': errors.to_location }"
          :disabled="isEditing"
          required
        >
          <option :value="null">Select To Location</option>
          <option
            v-for="location in locations"
            :key="location.id"
            :value="location.id"
          >
            {{ location.name }} ({{ location.code }})
          </option>
        </select>
        <p v-if="errors.to_location" class="text-danger text-sm mt-1">{{ errors.to_location }}</p>
      </div>
    </div>

    <div>
      <label class="form-label">Reference</label>
      <input
        v-model="form.reference"
        type="text"
        class="text-input"
        placeholder="Reference number"
      />
    </div>

    <div>
      <label class="form-label">Description</label>
      <textarea
        v-model="form.description"
        class="text-input"
        rows="2"
        placeholder="Move description"
      ></textarea>
    </div>

    <div class="border-t pt-4">
      <h3 class="section-title">Products</h3>
      
      <div 
        v-for="(line, index) in form.lines" 
        :key="index" 
        class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 p-4 bg-gray-50 rounded"
      >
        <div>
          <label class="form-label">Product *</label>
          <select
            v-model="line.product"
            class="text-input"
            :class="{ 'border-danger': errors[`lines.${index}.product`] }"
            :disabled="isEditing"
            required
          >
            <option :value="0">Select Product</option>
            <option
              v-for="product in products"
              :key="product.id"
              :value="product.id"
            >
              {{ product.name }} ({{ product.internal_reference }})
            </option>
          </select>
          <p v-if="errors[`lines.${index}.product`]" class="text-danger text-sm mt-1">
            {{ errors[`lines.${index}.product`] }}
          </p>
        </div>

        <div>
          <label class="form-label">Quantity *</label>
          <input
            v-model="line.quantity"
            type="number"
            min="1"
            class="text-input"
            :class="{ 'border-danger': errors[`lines.${index}.quantity`] }"
            placeholder="Quantity"
            required
          />
          <p v-if="errors[`lines.${index}.quantity`]" class="text-danger text-sm mt-1">
            {{ errors[`lines.${index}.quantity`] }}
          </p>
        </div>

        <div>
          <label class="form-label">Description</label>
          <input
            v-model="line.description"
            type="text"
            class="text-input"
            placeholder="Line description"
          />
          <button
            v-if="form.lines.length > 1 && !isEditing"
            type="button"
            @click="removeLine(index)"
            class="mt-2 text-danger hover:text-danger-600 text-sm"
          >
            Remove
          </button>
        </div>
      </div>

      <button
        v-if="!isEditing"
        type="button"
        @click="addLine"
        class="btn btn-primary mt-2"
      >
        Add Product
      </button>
    </div>

    <div class="flex space-x-4 pt-4">
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Saving...' : isEditing ? 'Update Stock Move' : 'Create Stock Move' }}
      </button>
      <button type="button" class="btn" @click="$emit('cancel')">Cancel</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useProductStore } from '@/store/productStore'
import { useLocationStore } from '@/store/locationStore'
import type { StockMove, StockMoveCreate } from '@/types'

interface Props {
  stockMove?: StockMove
}

interface Emits {
  (e: 'submit', data: StockMoveCreate): void
  (e: 'cancel'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const productStore = useProductStore()
const locationStore = useLocationStore()
const loading = ref(false)
const errors = reactive<Record<string, string>>({})

const isEditing = computed(() => !!props.stockMove)

const form = reactive({
  move_type: '' as 'INBOUND' | 'OUTBOUND' | 'TRANSFER' | '',
  from_location: null as number | null,
  to_location: null as number | null,
  reference: '',
  description: '',
  lines: [
    {
      product: 0,
      quantity: 0,
      description: ''
    }
  ] as Array<{ product: number; quantity: number; description: string }>
})

watch(() => props.stockMove, (newStockMove) => {
  if (newStockMove) {
    form.move_type = newStockMove.move_type
    form.from_location = newStockMove.from_location
    form.to_location = newStockMove.to_location
    form.reference = newStockMove.reference || ''
    form.description = newStockMove.description || ''
    
    form.lines = newStockMove.lines.map(line => ({
      product: line.product,
      quantity: line.quantity,
      description: line.description || ''
    }))
  }
}, { immediate: true })

const showFromLocation = computed(() => {
  return form.move_type === 'OUTBOUND' || form.move_type === 'TRANSFER'
})

const showToLocation = computed(() => {
  return form.move_type === 'INBOUND' || form.move_type === 'TRANSFER'
})

const handleTypeChange = () => {
  if (!isEditing.value) {
    form.from_location = null
    form.to_location = null
  }
}

const addLine = () => {
  form.lines.push({
    product: 0,
    quantity: 0,
    description: ''
  })
}

const removeLine = (index: number) => {
  form.lines.splice(index, 1)
}

onMounted(async () => {
  if (productStore.products.length === 0) {
    await productStore.fetchProducts()
  }
  if (locationStore.locations.length === 0) {
    await locationStore.fetchLocations()
  }
})

const submitForm = async () => {
  loading.value = true
  Object.keys(errors).forEach(key => delete errors[key])
  
  if (!form.move_type) errors.move_type = 'Type is required'
  
  if (showFromLocation.value && !form.from_location) {
    errors.from_location = 'From location is required'
  }
  
  if (showToLocation.value && !form.to_location) {
    errors.to_location = 'To location is required'
  }

  form.lines.forEach((line, index) => {
    if (!line.product || line.product === 0) {
      errors[`lines.${index}.product`] = 'Product is required'
    }
    if (!line.quantity || line.quantity <= 0) {
      errors[`lines.${index}.quantity`] = 'Valid quantity is required'
    }
  })

  if (Object.keys(errors).length > 0) {
    loading.value = false
    return
  }

  const stockMoveData: StockMoveCreate = {
    move_type: form.move_type as 'INBOUND' | 'OUTBOUND' | 'TRANSFER',
    from_location: showFromLocation.value ? form.from_location : null,
    to_location: showToLocation.value ? form.to_location : null,
    reference: form.reference.trim() || undefined,
    description: form.description.trim() || undefined,
    lines: form.lines.map(line => ({
      product: Number(line.product),
      quantity: Number(line.quantity),
      description: line.description.trim() || undefined
    }))
  }

  emit('submit', stockMoveData)
  loading.value = false
}

const products = productStore.products
const locations = locationStore.locations
</script>