import { defineStore } from 'pinia'
import { ref } from 'vue'
import { productApi } from '@/api/productApi'
import type { Product, ProductCreate, ProductCategory, PaginatedResponse } from '@/types'

export const useProductStore = defineStore('products', () => {
  const products = ref<Product[]>([])
  const categories = ref<ProductCategory[]>([])
  const pagination = ref({
    count: 0,
    next: null as string | null,
    previous: null as string | null
  })
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchProducts = async (params?: { category?: number; low_stock?: boolean }) => {
    loading.value = true
    error.value = null
    try {
      const response: PaginatedResponse<Product> = await productApi.getProducts(params)
      products.value = response.results
      pagination.value = {
        count: response.count,
        next: response.next,
        previous: response.previous
      }
    } catch (err) {
      error.value = 'Failed to fetch products'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  const fetchInventoryLevels = async (params?: { product_id?: number; location_id?: number }) => {
    loading.value = true
    error.value = null
    try {
      const response = await productApi.getInventoryLevels(params)
      return response
    } catch (err) {
      error.value = 'Failed to fetch inventory levels'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }


  const fetchProductById = async (id: number): Promise<Product | undefined> => {
    try {
      const existingProduct = products.value.find(p => p.id === id)
      if (existingProduct) {
        return existingProduct
      }
      
      return await productApi.getProduct(id)
    } catch (err) {
      console.error('Failed to fetch product:', err)
      return undefined
    }
  }

 const fetchCategories = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await productApi.getCategories() 
    categories.value = response.results 
  } catch (err) {
    error.value = 'Failed to fetch categories'
    console.error(err)
  } finally {
    loading.value = false
  }
}

  const createProduct = async (productData: ProductCreate) => {
    loading.value = true
    error.value = null
    try {
      const product = await productApi.createProduct(productData)
      products.value.push(product)
      return product
    } catch (err) {
      error.value = 'Failed to create product'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const updateProduct = async (id: number, productData: Partial<ProductCreate>) => {
    loading.value = true
    error.value = null
    try {
      const product = await productApi.updateProduct(id, productData)
      const index = products.value.findIndex(p => p.id === id)
      if (index !== -1) {
        products.value[index] = product
      }
      return product
    } catch (err) {
      error.value = 'Failed to update product'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteProduct = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      await productApi.deleteProduct(id)
      products.value = products.value.filter(p => p.id !== id)
    } catch (err) {
      error.value = 'Failed to delete product'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const getProductById = (id: number) => {
    return products.value.find(p => p.id === id)
  }

  return {
    products,
    categories,
    pagination,
    loading,
    error,
    fetchProducts,
    fetchProductById,
    fetchCategories,
    createProduct,
    updateProduct,
    deleteProduct,
    getProductById,
    fetchInventoryLevels
  }
})