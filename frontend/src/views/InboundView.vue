<script setup>
import 'primeicons/primeicons.css'
</script>
<template>
  <div v-if="inbound">
    <p>inbound: {{ inbound.remark }}</p>
    <p>detail: {{ inbound.detail }}</p>
    <p>price: {{ inbound.price }}</p>
    <p>protocol: {{ inbound.protocol.value }}</p>
    <div v-if="client">
      <p>client: {{ client }}</p>
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
  }
}
</script>
