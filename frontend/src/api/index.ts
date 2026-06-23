import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 5000
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.reload()
    }
    return Promise.reject(error)
  }
)

export interface Supplier {
  id: number
  name: string
  contact_person: string
  phone: string
  email: string
  address: string
  product_type: string
  credit_rating: number
  created_at: string
  updated_at: string
}

export interface PriceHistory {
  id: number
  supplier_id: number
  product_name: string
  price: number
  currency: string
  date: string
}

export interface PurchaseRecord {
  id: number
  supplier_id: number
  product_name: string
  quantity: number
  unit_price: number
  total_amount: number
  purchase_date: string
  status: string
}

export interface WeatherData {
  id: number
  date: string
  temperature: number
  humidity: number
  precipitation: number
  wind_speed: number
  weather_condition: string
  city: string
}

export interface PricePrediction {
  supplier_id: number
  product_name: string
  predictions: { date: string; predicted_price: number; confidence: number }[]
  model_metrics: { mse: number; r2: number }
}

export interface User {
  id: number
  username: string
  email: string
  role: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: User
}

export const supplierApi = {
  getAll: () => api.get<Supplier[]>('/suppliers'),
  getById: (id: number) => api.get<Supplier>(`/suppliers/${id}`),
  create: (data: Omit<Supplier, 'id' | 'created_at' | 'updated_at'>) => api.post<Supplier>('/suppliers', data),
  update: (id: number, data: Partial<Supplier>) => api.put<Supplier>(`/suppliers/${id}`, data),
  delete: (id: number) => api.delete(`/suppliers/${id}`),
  getPriceHistory: (id: number) => api.get<PriceHistory[]>(`/suppliers/${id}/price-history`),
  createPriceHistory: (data: Omit<PriceHistory, 'id'>) => api.post<PriceHistory>('/suppliers/price-history', data),
  getPurchaseRecords: (id: number) => api.get<PurchaseRecord[]>(`/suppliers/${id}/purchase-records`),
  createPurchaseRecord: (data: Omit<PurchaseRecord, 'id'>) => api.post<PurchaseRecord>('/suppliers/purchase-records', data)
}

export const predictionApi = {
  predictPrice: (supplierId: number, productName: string, daysAhead: number = 7) =>
    api.post<PricePrediction>('/prediction/price', { supplier_id: supplierId, product_name: productName, days_ahead: daysAhead })
}

export const weatherApi = {
  getCurrent: () => api.get('/weather/current'),
  getHistorical: (startDate: string, endDate: string) =>
    api.get<WeatherData[]>(`/weather/historical?start_date=${startDate}&end_date=${endDate}`)
}

export const authApi = {
  login: (username: string, password: string) =>
    api.post<TokenResponse>('/auth/login', { username, password }),
  register: (data: { username: string; email: string; password: string }) =>
    api.post<User>('/auth/register', data)
}