import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/authStore'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/auth/Login.vue')
  },
  {
    path: '/',
    redirect: '/products'
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('@/pages/products/ProductList.vue')
  },
  {
    path: '/products/create',
    name: 'ProductCreate',
    component: () => import('@/pages/products/ProductCreateEdit.vue')
  },
  {
    path: '/products/edit/:id',
    name: 'ProductEdit',
    component: () => import('@/pages/products/ProductCreateEdit.vue'),
    props: true
  },
  {
    path: '/products/:id',
    name: 'ProductDetail',
    component: () => import('@/pages/products/ProductDetail.vue'),
    props: true
  },
  {
    path: '/locations',
    name: 'Locations',
    component: () => import('@/pages/locations/LocationList.vue')
  },
  {
    path: '/locations/create',
    name: 'LocationCreate',
    component: () => import('@/pages/locations/LocationCreateEdit.vue')
  },
  {
    path: '/locations/edit/:id',
    name: 'LocationEdit',
    component: () => import('@/pages/locations/LocationCreateEdit.vue'),
    props: true
  },
  {
    path: '/stockmoves',
    name: 'StockMoves',
    component: () => import('@/pages/stockmoves/StockMoveList.vue')
  },
  {
  path: '/stockmoves/create',
  name: 'StockMoveCreate',
  component: () => import('@/pages/stockmoves/StockMoveCreate.vue')
},
{
  path: '/stockmoves/:id',
  name: 'StockMoveDetail',
  component: () => import('@/pages/stockmoves/StockMoveDetail.vue')
},
{
  path: '/stockmoves/:id/edit',
  name: 'StockMoveEdit',
  component: () => import('@/pages/stockmoves/StockMoveEdit.vue')
},
  {
    path: '/suppliers',
    name: 'Suppliers',
    component: () => import('@/pages/suppliers/SupplierList.vue')
  },
  {
    path: '/suppliers/create',
    name: 'SupplierCreate',
    component: () => import('@/pages/suppliers/SupplierCreateEdit.vue')
  },
  {
  path: '/suppliers/:id',
  name: 'SupplierDetail',
  component: () => import('@/pages/suppliers/SupplierDetail.vue')
},
  {
    path: '/suppliers/edit/:id',
    name: 'SupplierEdit',
    component: () => import('@/pages/suppliers/SupplierCreateEdit.vue'),
    props: true
  },
{
  path: '/inventory',
  name: 'Snapshots',
  component: () => import('@/pages/snapshots/SnapshotList.vue')
},
{
  path: '/inventory/snapshot/:id',
  name: 'SnapshotDetail',
  component: () => import('@/pages/snapshots/SnapshotDetail.vue')
},
{
  path: '/inventory/history',
  name: 'InventoryHistory',
  component: () => import('@/pages/snapshots/InventoryHistory.vue')
},
{
  path: '/products/:id/history',
  name: 'ProductHistory',
  component: () => import('@/pages/snapshots/ProductHistory.vue')
}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.name !== 'Login' && !authStore.isAuthenticated) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router