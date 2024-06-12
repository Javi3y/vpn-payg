<script setup>
import 'primeicons/primeicons.css'
import Fieldset from 'primevue/fieldset'
import Client from '@/components/Client.vue'
</script>
<template>
  <div class="grid grid-cols-2 gap-2" v-if="user">
    <Fieldset legend="Header">
      <h2>Username:</h2>
      <h3 class="pl-4">{{ user.username }}</h3>
      <h2>Balance:</h2>
      <h3 class="pl-4">{{ user.balance }} T</h3>
    </Fieldset>
    <Fieldset legend="Clients" :toggleable="true" v-if="clients.length > 0">
      <Client v-for="client in clients" :client="client"></Client>
    </Fieldset>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  props: ['user'],
  data() {
    return {
      clients: []
    }
  },
  async created() {
    try {
      const response = await axios.get('clients')
      this.clients = response.data
    } catch (error) {
      console.error(error)
    }
  }
}
</script>
