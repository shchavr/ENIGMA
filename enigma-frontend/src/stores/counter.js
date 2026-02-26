import { defineStore } from 'pinia'
import axios from 'axios'
import router from '../router';

export const baseUrl = import.meta.env.VITE_FRONTEND_URL;

export const useDataStore = defineStore('data', {
  state: () => ({

  }),
  actions: {

  },
  getters: {
    getProfileData: (state) => state.profileData,
  },
  persist: {
    key: 'data-store',
    storage: window.localStorage,
    paths: ['auth_key', 'excursionsStats'],
  },
})
