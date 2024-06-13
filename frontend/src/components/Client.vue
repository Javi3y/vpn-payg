<script setup>
import { RouterLink } from 'vue-router'
</script>
<template>
  <p>
    <RouterLink class="green" :to="`/inbound/${client.inbound.id}`">
      inbound: {{ client.inbound.remark }}
    </RouterLink>
  </p>
  <p>protocol: {{ client.inbound.protocol.value }}</p>
  <p>price: {{ client.inbound.price }}</p>
  <p>usage: {{ client.usage }}</p>
</template>
<script>
export default {
  props: ['client'],
  data() {}
}
</script>
