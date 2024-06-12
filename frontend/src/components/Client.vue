<template>
  <p>inbound: {{ client.inbound.remark }}</p>
  <p>protocol: {{ client.inbound.protocol.value }}</p>
  <p>price: {{ client.inbound.price }}</p>
  <p>usage: {{ client.usage}}</p>
</template>
<script>
export default {
  props: ['client'],
  data() {}
}
</script>
