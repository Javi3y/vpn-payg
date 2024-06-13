<script setup>
import { RouterLink } from 'vue-router'
</script>
<template>
  <RouterLink :to="`/inbound/${client.inbound.id}`">
    <p>inbound: {{ client.inbound.remark }}</p>
  </RouterLink>
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
