<script setup>
import 'primeicons/primeicons.css'
import Fieldset from 'primevue/fieldset'
</script>
<template>
  <div class="grid grid-cols-2" v-if="user">
    <Fieldset legend="Header">
		<h2 >Username:</h2>
		<h3 class="pl-4">{{ user.username }}</h3>
		<h2 >Balance:</h2>
		<h3 class="pl-4">{{ user.balance }} T</h3>
    </Fieldset>
    <div>
      <h1>Clients:</h1>
    </div>
  </div>
</template>
<script>
export default {
  props: ['user'],
  data() {
    return {}
  }
}
</script>
