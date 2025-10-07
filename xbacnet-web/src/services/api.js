/**
 * API Service
 * Handles all HTTP requests to the XBACnet API backend
 */

import axios from 'axios'
import { ElMessage } from 'element-plus'

// Create axios instance
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      localStorage.removeItem('token')
      window.location.href = '/login'
    } else if (error.response?.status >= 500) {
      ElMessage.error('Server error. Please try again later.')
    } else if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    } else {
      ElMessage.error('Network error. Please check your connection.')
    }
    
    return Promise.reject(error)
  }
)

// API Service class
class ApiService {
  // Health and Statistics
  async getHealth() {
    const response = await api.get('/health')
    return response.data
  }
  
  async getStats() {
    const response = await api.get('/stats')
    return response.data
  }
  
  // User Management
  async getUsers(params = {}) {
    const response = await api.get('/users', { params })
    return response.data
  }
  
  async getUser(id) {
    const response = await api.get(`/users/${id}`)
    return response.data
  }
  
  async createUser(userData) {
    const response = await api.post('/users', userData)
    return response.data
  }
  
  async updateUser(id, userData) {
    const response = await api.put(`/users/${id}`, userData)
    return response.data
  }
  
  async deleteUser(id) {
    const response = await api.delete(`/users/${id}`)
    return response.data
  }
  
  async login(credentials) {
    const response = await api.post('/login', credentials)
    return response.data
  }
  
  async logout(logoutData) {
    const response = await api.post('/logout', logoutData)
    return response.data
  }
  
  // Analog Input Objects
  async getAnalogInputs(params = {}) {
    const response = await api.get('/analog-inputs', { params })
    return response.data
  }
  
  async getAnalogInput(id) {
    const response = await api.get(`/analog-inputs/${id}`)
    return response.data
  }
  
  async createAnalogInput(data) {
    const response = await api.post('/analog-inputs', data)
    return response.data
  }
  
  async updateAnalogInput(id, data) {
    const response = await api.put(`/analog-inputs/${id}`, data)
    return response.data
  }
  
  async deleteAnalogInput(id) {
    const response = await api.delete(`/analog-inputs/${id}`)
    return response.data
  }
  
  // Analog Output Objects
  async getAnalogOutputs(params = {}) {
    const response = await api.get('/analog-outputs', { params })
    return response.data
  }
  
  async getAnalogOutput(id) {
    const response = await api.get(`/analog-outputs/${id}`)
    return response.data
  }
  
  async createAnalogOutput(data) {
    const response = await api.post('/analog-outputs', data)
    return response.data
  }
  
  async updateAnalogOutput(id, data) {
    const response = await api.put(`/analog-outputs/${id}`, data)
    return response.data
  }
  
  async deleteAnalogOutput(id) {
    const response = await api.delete(`/analog-outputs/${id}`)
    return response.data
  }
  
  // Binary Input Objects
  async getBinaryInputs(params = {}) {
    const response = await api.get('/binary-inputs', { params })
    return response.data
  }
  
  async getBinaryInput(id) {
    const response = await api.get(`/binary-inputs/${id}`)
    return response.data
  }
  
  async createBinaryInput(data) {
    const response = await api.post('/binary-inputs', data)
    return response.data
  }
  
  async updateBinaryInput(id, data) {
    const response = await api.put(`/binary-inputs/${id}`, data)
    return response.data
  }
  
  async deleteBinaryInput(id) {
    const response = await api.delete(`/binary-inputs/${id}`)
    return response.data
  }
  
  // Binary Output Objects
  async getBinaryOutputs(params = {}) {
    const response = await api.get('/binary-outputs', { params })
    return response.data
  }
  
  async getBinaryOutput(id) {
    const response = await api.get(`/binary-outputs/${id}`)
    return response.data
  }
  
  async createBinaryOutput(data) {
    const response = await api.post('/binary-outputs', data)
    return response.data
  }
  
  async updateBinaryOutput(id, data) {
    const response = await api.put(`/binary-outputs/${id}`, data)
    return response.data
  }
  
  async deleteBinaryOutput(id) {
    const response = await api.delete(`/binary-outputs/${id}`)
    return response.data
  }
  
  // Multi-state Input Objects
  async getMultiStateInputs(params = {}) {
    const response = await api.get('/multi-state-inputs', { params })
    return response.data
  }
  
  async getMultiStateInput(id) {
    const response = await api.get(`/multi-state-inputs/${id}`)
    return response.data
  }
  
  async createMultiStateInput(data) {
    const response = await api.post('/multi-state-inputs', data)
    return response.data
  }
  
  async updateMultiStateInput(id, data) {
    const response = await api.put(`/multi-state-inputs/${id}`, data)
    return response.data
  }
  
  async deleteMultiStateInput(id) {
    const response = await api.delete(`/multi-state-inputs/${id}`)
    return response.data
  }
  
  // Multi-state Output Objects
  async getMultiStateOutputs(params = {}) {
    const response = await api.get('/multi-state-outputs', { params })
    return response.data
  }
  
  async getMultiStateOutput(id) {
    const response = await api.get(`/multi-state-outputs/${id}`)
    return response.data
  }
  
  async createMultiStateOutput(data) {
    const response = await api.post('/multi-state-outputs', data)
    return response.data
  }
  
  async updateMultiStateOutput(id, data) {
    const response = await api.put(`/multi-state-outputs/${id}`, data)
    return response.data
  }
  
  async deleteMultiStateOutput(id) {
    const response = await api.delete(`/multi-state-outputs/${id}`)
    return response.data
  }
  
  // Analog Value Objects
  async getAnalogValues(params = {}) {
    const response = await api.get('/analog-values', { params })
    return response.data
  }
  
  async getAnalogValue(id) {
    const response = await api.get(`/analog-values/${id}`)
    return response.data
  }
  
  async createAnalogValue(data) {
    const response = await api.post('/analog-values', data)
    return response.data
  }
  
  async updateAnalogValue(id, data) {
    const response = await api.put(`/analog-values/${id}`, data)
    return response.data
  }
  
  async deleteAnalogValue(id) {
    const response = await api.delete(`/analog-values/${id}`)
    return response.data
  }
  
  // Binary Value Objects
  async getBinaryValues(params = {}) {
    const response = await api.get('/binary-values', { params })
    return response.data
  }
  
  async getBinaryValue(id) {
    const response = await api.get(`/binary-values/${id}`)
    return response.data
  }
  
  async createBinaryValue(data) {
    const response = await api.post('/binary-values', data)
    return response.data
  }
  
  async updateBinaryValue(id, data) {
    const response = await api.put(`/binary-values/${id}`, data)
    return response.data
  }
  
  async deleteBinaryValue(id) {
    const response = await api.delete(`/binary-values/${id}`)
    return response.data
  }
  
  // Multi-state Value Objects
  async getMultiStateValues(params = {}) {
    const response = await api.get('/multi-state-values', { params })
    return response.data
  }
  
  async getMultiStateValue(id) {
    const response = await api.get(`/multi-state-values/${id}`)
    return response.data
  }
  
  async createMultiStateValue(data) {
    const response = await api.post('/multi-state-values', data)
    return response.data
  }
  
  async updateMultiStateValue(id, data) {
    const response = await api.put(`/multi-state-values/${id}`, data)
    return response.data
  }
  
  async deleteMultiStateValue(id) {
    const response = await api.delete(`/multi-state-values/${id}`)
    return response.data
  }
}

// Export singleton instance
export const apiService = new ApiService()
export default apiService
