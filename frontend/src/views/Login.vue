<script setup>
import Fieldset from 'primevue/fieldset'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
</script>
<template>
  <div class="flex flex-col h-screen justify-center items-center">
    <Fieldset class="auto-rows-max" legend="Login">
      <form @submit.prevent="login">
        <div class="flex flex-col gap-2">
          <label for="username">Username</label>
          <InputText id="username" v-model="username" />
        </div>
        <div class="flex flex-col gap-2">
          <label for="password">Password</label>
          <Password id="password" toggleMask :feedback="false" v-model="password" />
        </div>
        <div class="flex flex-col gap-2 pt-2">
          <Button type="submit" label="Primary" text raised />
        </div>
        <div class="flex flex-col gap-2 pt-3">
          <p>don't have an account? <a href="">register here</a></p>
        </div>
      </form>
    </Fieldset>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'UserLogin',
  created() {
    localStorage.removeItem('token')
  },
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async login() {
      try {
        const params = new URLSearchParams()
        params.append('username', this.username)
        params.append('password', this.password)

        const response = await axios.post('login', params)
		console.log("yes")
        localStorage.setItem('token', response.data.access_token)
        this.$router.push('/')
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>
