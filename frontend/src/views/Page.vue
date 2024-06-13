<script setup>
import Menubar from 'primevue/menubar'
import logo from '../assets/vpn.svg'
import 'primeicons/primeicons.css'
import { RouterLink, RouterView } from 'vue-router'
</script>
<template>
  <Menubar :model="items" class="w-svw">
    <template #start>
      <object class="mr-2" :data="logo" width="35" height="35"></object>
    </template>
    <template #item="{ item }">
      <a v-ripple class="flex align-items-center">
        <RouterLink to="/">
          <span :class="item.icon" />
          <span class="ml-2">{{ item.label }}</span>
        </RouterLink>
      </a>
    </template>
	<template #end>

      <a v-ripple class="flex align-items-center">
        <RouterLink to="/logout/">
          <span class="pi pi-sign-out" />
          <span class="ml-2">logout</span>
        </RouterLink>
      </a>
	</template>
  </Menubar>
  <div class="m-3 p-3">
    <Router-view :user="user" :key="$route.path"></Router-view>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  async created() {
    try {
      const response = await axios.get('users/profile')
      this.user = response.data
    } catch (error) {
      console.error(error)
    }
  },
  data() {
    return {
      user: null,
      items: [
        {
          label: 'home',
          icon: 'pi pi-home'
        }
      ]
    }
  }
}
</script>
