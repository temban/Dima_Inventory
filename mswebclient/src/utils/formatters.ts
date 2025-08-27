export const formatDate = (dateString: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

export const formatDateTime = (dateString: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString()
}

export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

export const formatStockMoveType = (type: string): string => {
  const types: Record<string, string> = {
    'INBOUND': 'Inbound',
    'OUTBOUND': 'Outbound',
    'TRANSFER': 'Transfer'
  }
  return types[type] || type
}