import { defineStore } from 'pinia'
import axios from 'axios'

export const baseUrl = import.meta.env.VITE_FRONTEND_URL;

export const useDataStore = defineStore('data', {
  state: () => ({
    auth_key: '',
  }),
  actions: {
    setTokenRole(auth_key) {
      this.auth_key = auth_key
    },
    clearTokenRole() {
      this.auth_key = ''
    },
    async PostLogin(formData) {
      try {
        const response = await axios.post(`${baseUrl}/admin/login`, formData)

        this.setTokenRole(
          response.data.access_token, 
        )

        return response
      } catch (error) {
        console.error('Ошибка при входе:', error.response?.data || error.message)
        throw error
      }
    },
  },
  getters: {
    
  },
  persist: {
    key: 'data-store',
    storage: window.localStorage,
    paths: ['auth_key'],
  },
})
