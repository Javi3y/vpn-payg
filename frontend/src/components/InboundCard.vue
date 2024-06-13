<script setup>
import { RouterLink } from 'vue-router'
</script>
<template>
  <div>
    <RouterLink :to="`/inbound/${inbound.id}`">
      <p>inbound: {{ inbound.remark }}</p>
      <p>detail: {{ inbound.detail }}</p>
      <p>price: {{ inbound.price }}</p>
      <p>protocol: {{ inbound.protocol.value }}</p>
    </RouterLink>
  </div>
</template>
<script>
export default {
  props: ['inbound'],
  data() {}
}
</script>
