<script setup>
import Menubar from 'primevue/menubar'
import logo from '../assets/vpn.svg'
import 'primeicons/primeicons.css'
//import { RouterLink, RouterView } from 'vue-router'
import { useRoute } from 'vue-router'
</script>
<template>
  <Menubar :model="items" class="w-svw fixed h-16">
    <template #start>
      <object class="mr-2" :data="logo" width="35" height="35"></object>
    </template>
    <template #item="{ item }">
      <router-link v-slot="routerProps" activeClass="test" :to="item.url" custom>
        <a
          :href="routerProps.href"
          @click="($event) => routerProps.navigate($event)"
          @keydown.enter.space="($event) => routerProps.navigate($event)"
          class="flex items-center cursor-pointer px-4 py-2 overflow-hidden relative font-semibold text-lg uppercase"
        >
          <span :class="item.icon" />
          <span class="ml-2">{{ item.label }}</span>
        </a>
      </router-link>
    </template>
    <template #end>
      <router-link v-slot="routerProps" to="/logout" custom>
        <a
          :href="routerProps.href"
          @click="($event) => routerProps.navigate($event)"
          @keydown.enter.space="($event) => routerProps.navigate($event)"
          class="flex items-center cursor-pointer px-4 py-2 overflow-hidden relative font-semibold text-lg uppercase"
        >
          <span class="pi pi-sign-out" />
          <span class="ml-2">logout</span>
        </a>
      </router-link>
    </template>
  </Menubar>
  <div class="m-4 p-4">
    <router-view :key="$router.fullPath"></router-view>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  async created() {
    try {
      const response = await axios.get('users/profile')
      this.user = response.data
      const adminResponse = await axios.get('users/is_admin')
      if (!adminResponse.data) {
      this.$router.push('/')
      }
    } catch (error) {
      //this.$router.push('/login')
      console.error(error)
    }
  },
  data() {
    return {
      user: null,
      items: [
        {
          label: 'home',
          icon: 'pi pi-home',
          url: '/'
        },
        {
          label: 'users',
          icon: 'pi pi-users',
          url: '/admin/users'
        }
      ]
    }
  }
}
</script>
