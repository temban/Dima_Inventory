import axiosInstance from './axiosInstance'
import type { StockMove, StockMoveCreate, StockMoveUpdate, PaginatedResponse } from '@/types'

export const stockMoveApi = {
  async getStockMoves(params?: { product_id?: number; move_type?: string }): Promise<PaginatedResponse<StockMove>> {
    const response = await axiosInstance.get('/stockmoves/', { params })
    return response.data
  },

  async getStockMove(id: number): Promise<StockMove> {
    const response = await axiosInstance.get(`/stockmoves/${id}/`)
    return response.data
  },

  async createStockMove(stockMove: StockMoveCreate): Promise<StockMove> {
    const response = await axiosInstance.post('/stockmoves/', stockMove)
    return response.data
  },

  async updateStockMove(id: number, stockMove: Partial<StockMoveCreate>): Promise<StockMove> {
    const response = await axiosInstance.put(`/stockmoves/${id}/`, stockMove)
    return response.data
  },

  async deleteStockMove(id: number): Promise<void> {
    await axiosInstance.delete(`/stockmoves/${id}/`)
  },

  async completeStockMove(id: number): Promise<void> {
    await axiosInstance.post(`/stockmoves/${id}/complete/`)
  }
}