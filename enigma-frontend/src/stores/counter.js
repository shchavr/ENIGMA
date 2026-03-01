import { defineStore } from 'pinia'
import axios from 'axios'

export const baseUrl = import.meta.env.VITE_FRONTEND_URL;

export const useDataStore = defineStore('data', {
  state: () => ({
    auth_key: '',
    emails: []
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
        const response = await axios.post(`${baseUrl}/api/v1/admin/login`, formData)

        this.setTokenRole(
          response.data.access_token, 
        )

        return response
      } catch (error) {
        console.error('Ошибка при входе:', error.response?.data || error.message)
        throw error
      }
    },
    async FetchEmails() {
      try {
        const response = await axios.get(`${baseUrl}/api/v1/admin/tickets/`,
          {
            headers: {
              'Authorization': `Bearer ${this.auth_key}`
            }
          }
        );
        this.emails = response.data
        console.log(response.data)
      } catch (error) {
        console.error('Ошибка при получении данных:', error.response?.data || error.message)
        throw error
      }
    },
    async PostAnswer(ticket_id, data) {
      try {
        const response = await axios.post(`${baseUrl}/api/v1/admin/tickets/${ticket_id}/reply`, data, {
            headers: {
              'Authorization': `Bearer ${this.auth_key}`
            }
          });
        return response
      } catch (error) {
        console.error('Ошибка при входе:', error.response?.data || error.message)
        throw error
      }
    },
  },
  getters: {
    getEmails: (s) => s.emails
  },
  persist: {
    key: 'data-store',
    storage: window.localStorage,
    paths: ['auth_key'],
  },
})
