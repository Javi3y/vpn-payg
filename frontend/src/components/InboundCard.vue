<script setup>
import 'primeicons/primeicons.css'
import { RouterLink } from 'vue-router';
</script>
<template>
	<div>
		<RouterLink :to="`/inbound/${inbound.id}`">
		<p>inbound: {{ inbound.remark }}</p>
		<p>inbound: {{ inbound.detail }}</p>
		<p>inbound: {{ inbound.price }}</p>
		<p>inbound: {{ inbound.protocol.value }}</p>
		</RouterLink>
	</div>
</template>
<script>
export default {
  props: ['inbound'],
  data() {}
}
</script>
