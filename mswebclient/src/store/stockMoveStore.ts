import { defineStore } from 'pinia'
import { ref } from 'vue'
import { stockMoveApi } from '@/api/stockMoveApi'
import type { StockMove, StockMoveCreate, PaginatedResponse } from '@/types'

export const useStockMoveStore = defineStore('stockMoves', () => {
  const stockMoves = ref<StockMove[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchStockMoves = async () => {
    loading.value = true
    error.value = null
    try {
      const response: PaginatedResponse<StockMove> = await stockMoveApi.getStockMoves()
      stockMoves.value = response.results
    } catch (err) {
      error.value = 'Failed to fetch stock moves'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  const fetchStockMove = async (id: number): Promise<StockMove | undefined> => {
    try {
      return await stockMoveApi.getStockMove(id)
    } catch (err) {
      error.value = 'Failed to fetch stock move'
      console.error(err)
      return undefined
    }
  }

  const createStockMove = async (stockMoveData: StockMoveCreate) => {
    loading.value = true
    error.value = null
    try {
      const stockMove = await stockMoveApi.createStockMove(stockMoveData)
      stockMoves.value.unshift(stockMove)
      return stockMove
    } catch (err) {
      error.value = 'Failed to create stock move'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateStockMove = async (id: number, stockMoveData: Partial<StockMoveCreate>) => {
    loading.value = true
    error.value = null
    try {
      const stockMove = await stockMoveApi.updateStockMove(id, stockMoveData)
      const index = stockMoves.value.findIndex(sm => sm.id === id)
      if (index !== -1) {
        stockMoves.value[index] = stockMove
      }
      return stockMove
    } catch (err) {
      error.value = 'Failed to update stock move'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteStockMove = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      await stockMoveApi.deleteStockMove(id)
      stockMoves.value = stockMoves.value.filter(sm => sm.id !== id)
    } catch (err) {
      error.value = 'Failed to delete stock move'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const getStockMoveById = (id: number) => {
    return stockMoves.value.find(sm => sm.id === id)
  }

  return {
    stockMoves,
    loading,
    error,
    fetchStockMoves,
    fetchStockMove,
    createStockMove,
    updateStockMove,
    deleteStockMove,
    getStockMoveById
  }
})