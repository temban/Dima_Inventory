export interface ProductCategory {
  id: number
  name: string
  parent: number | null
}

export interface Product {
  id: number
  favorite: string
  name: string
  internal_reference: string
  responsible: string | null
  barcode: string | null
  sales_price: number
  cost: number
  product_category: number | null
  product_type: string
  quantity_on_hand: number
  forecasted_quantity: number
  activity_exception_decoration: string | null
  supplier: number | null
  default_location: number | null
  created_at: string
  updated_at: string
  category_name?: string
  supplier_name?: string
  location_name?: string
}

export interface InventoryLevel {
  product_id: number
  product_name: string
  product_sku: string
  locations: Record<string, {
    location_name: string
    location_code: string
    quantity: number
    last_updated: string
  }>
}

export interface ProductCreate {
  favorite: string
  name: string
  internal_reference: string
  responsible: string | null
  barcode: string | null
  sales_price: number
  cost: number
  product_category: number | null
  product_type: string
  supplier: number | null
  default_location: number | null
  activity_exception_decoration: string | null
}

export interface Location {
  id: number
  code: string
  name: string
  description: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LocationCreate {
  code: string
  name: string
  description?: string | null
  is_active?: boolean
}

export interface StockMoveLine {
  id: number
  product: number
  product_name: string
  product_internal_reference: string
  quantity: number
  description: string
  stock_move: number
}

export interface StockMove {
  id: number
  move_type: 'INBOUND' | 'OUTBOUND' | 'TRANSFER'
  reference: string
  description: string
  timestamp: string
  completed: boolean
  from_location: number | null
  to_location: number | null
  from_location_name?: string
  to_location_name?: string
  lines: StockMoveLine[]
}

export interface StockMoveLineCreate {
  product: number
  quantity: number
  description?: string
}

export interface StockMoveCreate {
  move_type: 'INBOUND' | 'OUTBOUND' | 'TRANSFER'
  from_location?: number | null
  to_location?: number | null
  reference?: string
  description?: string
  lines: StockMoveLineCreate[]
}

export interface StockMoveUpdate extends Partial<StockMoveCreate> {
  id: number
}

export interface AddressType {
  id: number
  name: string
}

export interface Supplier {
  id: number
  name: string
  is_company: boolean
  street: string | null
  zip_code: string | null
  city: string | null
  state: string | null
  country: string | null
  email: string | null
  phone: string | null
  created_at: string
  updated_at: string
  related_company: number | null
  address_type: number | null
  address_type_name?: string
  related_company_name?: string
}

export interface SupplierCreate {
  name: string
  is_company: boolean
  street?: string | null
  zip_code?: string | null
  city?: string | null
  state?: string | null
  country?: string | null
  email?: string | null
  phone?: string | null
  related_company?: number | null
  address_type?: number | null
}

export interface InventorySnapshot {
  id: number
  product: number
  product_name: string
  product_internal_reference: string
  location: number
  location_name: string
  location_code: string
  quantity: number
  timestamp: string
  cost_value?: number
  retail_value?: number
}

export interface CurrentInventoryItem {
  product_id: number
  product_name: string
  product_internal_reference: string
  location_id: number
  location_name: string
  location_code: string
  quantity: number
  last_updated: string
}

export interface SnapshotCreate {
  product: number
  location: number
  quantity: number
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface ApiError {
  message: string
  errors?: Record<string, string[]>
}

export interface LoginData {
  username: string
  password: string
}

export interface AuthResponse {
  access: string
  refresh: string
}