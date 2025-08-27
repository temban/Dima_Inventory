import axiosInstance from './axiosInstance'
import type { Product, ProductCreate, ProductCategory, PaginatedResponse } from '@/types'

export const productApi = {
  async getProducts(params?: { category?: number; low_stock?: boolean }): Promise<PaginatedResponse<Product>> {
    const response = await axiosInstance.get('/products/', { params })
    return response.data
  },

  async getProduct(id: number): Promise<Product> {
    const response = await axiosInstance.get(`/products/${id}/`)
    return response.data
  },

  async createProduct(product: ProductCreate): Promise<Product> {
    const response = await axiosInstance.post('/products/', product)
    return response.data
  },

  async updateProduct(id: number, product: Partial<ProductCreate>): Promise<Product> {
    const response = await axiosInstance.put(`/products/${id}/`, product)
    return response.data
  },

  async deleteProduct(id: number): Promise<void> {
    await axiosInstance.delete(`/products/${id}/`)
  },

  async adjustStock(id: number, quantity: number): Promise<void> {
    await axiosInstance.post(`/products/${id}/adjust_stock/`, { quantity })
  },

  async getLowStock(threshold?: number): Promise<Product[]> {
    const params = threshold ? { threshold } : {}
    const response = await axiosInstance.get('/products/low_stock/', { params })
    return response.data
  },

async getCategories(): Promise<PaginatedResponse<ProductCategory>> {
  const response = await axiosInstance.get('/products/categories/')
  return response.data
},

  async createCategory(category: { name: string; parent?: number }): Promise<ProductCategory> {
    const response = await axiosInstance.post('/products/categories/', category)
    return response.data
  },
  async getInventoryLevels(params?: { product_id?: number; location_id?: number }): Promise<any> {
    const response = await axiosInstance.get('/products/inventory_levels/', { params })
    return response.data
  }
}