import './assets/main.css'
import PrimeVue from 'primevue/config'
import Lara from '@/presets/lara' //import preset

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './axios'

const app = createApp(App)
app.use(PrimeVue, {
	unstyled: true,
	pt: Lara
})

app.use(router)

app.mount('#app')
