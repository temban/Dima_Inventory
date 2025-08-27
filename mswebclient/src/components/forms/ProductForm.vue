<template>
  <form @submit.prevent="submitForm" class="space-y-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="form-label">Favorite</label>
        <select v-model="form.favorite" class="text-input">
          <option value="Normal">Normal</option>
          <option value="Favorite">Favorite</option>
        </select>
      </div>

      <div>
        <label class="form-label">Name *</label>
        <input
          v-model="form.name"
          type="text"
          class="text-input"
          :class="{ 'border-danger': errors.name }"
          placeholder="Product Name"
          required
        />
        <p v-if="errors.name" class="text-danger text-sm mt-1">{{ errors.name }}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="form-label">Internal Reference *</label>
        <input
          v-model="form.internal_reference"
          type="text"
          class="text-input"
          :class="{ 'border-danger': errors.internal_reference }"
          placeholder="Internal Reference"
          required
        />
        <p v-if="errors.internal_reference" class="text-danger text-sm mt-1">{{ errors.internal_reference }}</p>
      </div>

      <div>
        <label class="form-label">Barcode</label>
        <input
          v-model="form.barcode"
          type="text"
          class="text-input"
          placeholder="Barcode"
        />
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div>
        <label class="form-label">Quantity *</label>
        <input
          v-model="form.quantity_on_hand"
          type="number"
          step="0.01"
          class="text-input"
          :class="{ 'border-danger': errors.quantity_on_hand }"
          placeholder="0.00"
          required
        />
        <p v-if="errors.quantity_on_hand" class="text-danger text-sm mt-1">{{ errors.quantity_on_hand }}</p>
      </div>
      <div>
        <label class="form-label">Sales Price *</label>
        <input
          v-model="form.sales_price"
          type="number"
          step="0.01"
          class="text-input"
          :class="{ 'border-danger': errors.sales_price }"
          placeholder="0.00"
          required
        />
        <p v-if="errors.sales_price" class="text-danger text-sm mt-1">{{ errors.sales_price }}</p>
      </div>

      <div>
        <label class="form-label">Cost *</label>
        <input
          v-model="form.cost"
          type="number"
          step="0.01"
          class="text-input"
          :class="{ 'border-danger': errors.cost }"
          placeholder="0.00"
          required
        />
        <p v-if="errors.cost" class="text-danger text-sm mt-1">{{ errors.cost }}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div>
        <label class="form-label">Product Type *</label>
        <select
          v-model="form.product_type"
          class="text-input"
          required
        >
          <option value="storable">Storable</option>
          <option value="consumable">Consumable</option>
          <option value="service">Service</option>
        </select>
      </div>

      <div>
        <label class="form-label">Category</label>
        <select
          v-model="form.product_category"
          class="text-input"
        >
          <option :value="null">No Category</option>
          <option
            v-for="category in productStore.categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </option>
        </select>
      </div>

      <div>
        <label class="form-label">Responsible</label>
        <input
          v-model="form.responsible"
          type="text"
          class="text-input"
          placeholder="Responsible person"
        />
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="form-label">Supplier</label>
        <select
          v-model="form.supplier"
          class="text-input"
        >
          <option :value="null">No Supplier</option>
          <option
            v-for="supplier in supplierStore.suppliers"
            :key="supplier.id"
            :value="supplier.id"
          >
            {{ supplier.name }}
          </option>
        </select>
      </div>

      <div>
        <label class="form-label">Default Location</label>
        <select
          v-model="form.default_location"
          class="text-input"
        >
          <option :value="null">No Location</option>
          <option
            v-for="location in locationStore.locations"
            :key="location.id"
            :value="location.id"
          >
            {{ location.name }} ({{ location.code }})
          </option>
        </select>
      </div>
    </div>


    <div>
      <label class="form-label">Activity Exception Decoration</label>
      <textarea
        v-model="form.activity_exception_decoration"
        class="text-input"
        rows="2"
        placeholder="Activity exception notes"
      ></textarea>
    </div>

    <div class="flex space-x-4 pt-4">
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Saving...' : 'Save Product' }}
      </button>
      <button type="button" class="btn" @click="$emit('cancel')">Cancel</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { useProductStore } from '@/store/productStore'
import { useSupplierStore } from '@/store/supplierStore'
import { useLocationStore } from '@/store/locationStore'
import type { Product, ProductCreate } from '@/types'

interface Props {
  product?: Product
}

interface Emits {
  (e: 'submit', data: ProductCreate): void
  (e: 'cancel'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const productStore = useProductStore()
const supplierStore = useSupplierStore()
const locationStore = useLocationStore()

const loading = ref(false)
const errors = reactive<Record<string, string>>({})

const form = reactive({
  favorite: 'Normal',
  name: '',
  internal_reference: '',
  responsible: null as string | null,
  barcode: null as string | null,
  quantity_on_hand: 0,
  sales_price: 0,
  cost: 0,
  product_category: null as number | null,
  product_type: 'storable',
  supplier: null as number | null,
  default_location: null as number | null,
  activity_exception_decoration: null as string | null
})

watch(() => props.product, (newProduct) => {
  if (newProduct) {
    form.favorite = newProduct.favorite || 'Normal'
    form.name = newProduct.name || ''
    form.internal_reference = newProduct.internal_reference || ''
    form.responsible = newProduct.responsible
    form.barcode = newProduct.barcode
    form.quantity_on_hand = newProduct.quantity_on_hand
    form.sales_price = newProduct.sales_price
    form.cost = newProduct.cost
    form.product_category = newProduct.product_category
    form.product_type = newProduct.product_type || 'storable'
    form.supplier = newProduct.supplier
    form.default_location = newProduct.default_location
    form.activity_exception_decoration = newProduct.activity_exception_decoration
  }
}, { immediate: true })

onMounted(async () => {
  try {
    if (productStore.categories.length === 0) {
      await productStore.fetchCategories()
    }
    if (supplierStore.suppliers.length === 0) {
      await supplierStore.fetchSuppliers()
    }
    if (locationStore.locations.length === 0) {
      await locationStore.fetchLocations()
    }
  } catch (error) {
    console.error('Failed to load dropdown data:', error)
  }
})

const submitForm = async () => {
  loading.value = true
  Object.keys(errors).forEach(key => delete errors[key])
  
  if (!form.name.trim()) errors.name = 'Name is required'
  if (!form.internal_reference.trim()) errors.internal_reference = 'Internal Reference is required'
  if (Number(form.sales_price) <= 0) errors.sales_price = 'Sales Price must be positive'
  if (Number(form.cost) <= 0) errors.cost = 'Cost must be positive'

  if (Object.keys(errors).length > 0) {
    loading.value = false
    return
  }

  const productData: ProductCreate = {
    favorite: form.favorite,
    name: form.name.trim(),
    internal_reference: form.internal_reference.trim(),
    responsible: form.responsible ? String(form.responsible).trim() : null,
    barcode: form.barcode ? String(form.barcode).trim() : null,
    quantity_on_hand: Number(form.quantity_on_hand),
    sales_price: Number(form.sales_price),
    cost: Number(form.cost),
    product_category: form.product_category,
    product_type: form.product_type,
    supplier: form.supplier,
    default_location: form.default_location,
    activity_exception_decoration: form.activity_exception_decoration ? String(form.activity_exception_decoration).trim() : null
  }

  emit('submit', productData)
  loading.value = false
}
</script>