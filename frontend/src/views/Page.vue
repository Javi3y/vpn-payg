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
        <span :class="item.icon" />
        <span class="ml-2">{{ item.label }}</span>
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
      const response = await axios.get('user')
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
          label: 'test',
          icon: 'pi pi-user'
        }
      ]
    }
  }
}
</script>
