import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura';
import Noir from './persets/Noir.js'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import 'primeicons/primeicons.css' 

import App from './App.vue'
import router from './router/index.js'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(App)

app.component('DataTable', DataTable)
app.component('Column', Column)

app.use(pinia)
app.use(router)
app.use(PrimeVue, {
    theme: {
        preset: Noir,
        options: {
            prefix: 'p',
            darkModeSelector: '.p-dark',
            cssLayer: false,
        }
    }
});
app.mount('#app')
