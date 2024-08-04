<script setup>
import Button from 'primevue/button'
</script>
<template>
  <div v-if="inbound">
    <p>inbound: {{ inbound.remark }}</p>
    <p>detail: {{ inbound.detail }}</p>
    <p>price: {{ inbound.price }}</p>
    <p>protocol: {{ inbound.protocol.value }}</p>
    <div v-if="client">
    <RouterLink class="green" :to="`/clientHistory/${client.id}`">
      client: {{ client }}
    </RouterLink>
      <form @submit.prevent="deleteClient">
        <Button type="submit" label="Delete Client" text />
      </form>
    </div>
    <div v-else>
      <form @submit.prevent="createClient">
        <Button type="submit" label="Create new Client" text />
      </form>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  props: ['user'],
  data() {
    return {
      inbound: null,
      client: null
    }
  },
  async created() {
    try {
      const response = await axios.get(`inbounds/${this.$route.params.id}`)
      this.inbound = response.data
      if (this.inbound) {
        const clientResponse = await axios.get('clients')
        this.client = clientResponse.data.find((client) => client.inbound.id == this.inbound.id)
      }
    } catch (error) {
      console.error(error)
    }
  },
  methods: {
    async createClient() {
      try {
        let params = { inbound: this.inbound.id }
        const response = await axios.post('clients', params)
        this.client = response.data
      } catch (error) {
        console.error(error)
      }
    },
    async deleteClient() {
      try {
        await axios.delete(`clients/${this.client.id}`)
        this.client = null
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>
