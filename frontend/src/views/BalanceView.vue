<script setup>
import 'primeicons/primeicons.css'
import Fieldset from 'primevue/fieldset'
import InputNumber from 'primevue/inputnumber'
import Button from 'primevue/button'
</script>
<template>
  <div class="flex flex-col h-screen justify-center items-center">
    <Fieldset class="auto-rows-max" legend="Balance">
      <form @submit.prevent="addBalance">
        <div class="flex flex-col gap-2">
          <label for="amount">amount</label>
          <InputNumber id="amount" v-model="amount" />
        </div>
        <div class="flex flex-col gap-2 pt-2">
          <Button type="submit" label="add to balance" text raised />
        </div>
      </form>
    </Fieldset>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  props: ['user'],
  data() {
    return {
      amount: 0
    }
  },
  methods: {
    async addBalance() {
      try {
        let params = {
          params: { amount: this.amount }
        }

        const response = await axios.post('users/balance', null, params)
        this.$router.push('/')
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>
