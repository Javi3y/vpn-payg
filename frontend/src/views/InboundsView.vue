<script setup>
import InboundCard from '@/components/InboundCard.vue'
</script>
<template>
  <inbound-card v-for="inbound in inbounds" :inbound="inbound"></inbound-card>
</template>
<script>
import axios from 'axios'
export default {
  props: ['user'],
  data() {
    return {
      inbounds: []
    }
  },
  async created() {
    try {
      const response = await axios.get('inbounds')
      this.inbounds = response.data
    } catch (error) {
      console.error(error)
    }
  }
}
</script>
