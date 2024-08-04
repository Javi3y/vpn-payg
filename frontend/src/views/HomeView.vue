<script setup>
import Fieldset from 'primevue/fieldset'
import Client from '@/components/Client.vue'
</script>
<template>
  <div class="grid grid-cols-2 gap-2" v-if="user">
    <Fieldset legend="User">
      <h2>Username:</h2>
      <h3 class="pl-4">{{ user.username }}</h3>
      <h2>Balance:</h2>
      <h3 class="pl-4">
        <RouterLink class="green" to="/balance"> {{ user.balance }} T </RouterLink>
      </h3>
	  <h2 class="green"><a :href="`http://localhost:8000/sub/${user.uuid}`">sub</a></h2>
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
      clients: [],
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
