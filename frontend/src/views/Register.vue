<script setup>
import Fieldset from 'primevue/fieldset'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Divider from 'primevue/divider'
</script>
<template>
  <div class="flex flex-col h-screen justify-center items-center">
    <Fieldset class="auto-rows-max" legend="Login">
      <form @submit.prevent="register">
        <div class="flex flex-col gap-2">
          <label for="email">Email</label>
          <InputText :invalid="!validateEmail" id="email" v-model="email" />
        </div>
        <div class="flex flex-col gap-2">
          <label for="username">Username</label>
          <InputText id="username" v-model="username" />
        </div>
        <div class="flex flex-col gap-2">
          <label for="tgid">Telegram Id(number id)</label>
          <InputText id="tgid" v-model="tgid" />
        </div>
        <div class="flex flex-col gap-2">
          <label for="password">Password</label>
          <Password :invalid="!passwordCheck" id="password" toggleMask v-model="password">
            <template #header>
              <h6>Pick a password</h6>
            </template>
            <template #footer>
              <Divider />
              <p class="mt-2 p-0 mb-2">Suggestions</p>
              <ul class="p-0 pl-2 m-0 ml-2 list-disc leading-6" style="line-height: 1.5">
                <li :class="passwordLower ? '' : 'text-red-600'">At least one lowercase</li>
                <li :class="passwordUpper ? '' : 'text-red-600'">At least one uppercase</li>
                <li :class="passwordNumeric ? '' : 'text-red-600'">At least one numeric</li>
                <li :class="password8 ? '' : 'text-red-600'">Minimum 8 characters</li>
              </ul>
            </template>
          </Password>

          <Password :invalid="!passwordVerify" id="passwordV" :feedback="false" v-model="passwordV">
          </Password>
        </div>
        <div class="flex flex-col gap-2 pt-2">
          <Button type="submit" label="Primary" text raised :disabled="!disabled" />
        </div>
        <div class="flex flex-col gap-2 pt-3">
          <p>have an account? <RouterLink class="green" to="/login">login here</RouterLink></p>
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
  computed: {
    passwordCheck() {
      return (
        (this.password.length >= 8) &
        /[A-Z]/.test(this.password) &
        /[a-z]/.test(this.password) &
        /[0-9]/.test(this.password)
      )
    },
    validateEmail() {
      return String(this.email)
        .toLowerCase()
        .match(
          /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        )
    },
    passwordVerify() {
      return this.password == this.passwordV && this.passwordV
    },
    password8() {
      return this.password.length >= 8
    },
    passwordUpper() {
      return /[A-Z]/.test(this.password)
    },
    passwordLower() {
      return /[a-z]/.test(this.password)
    },
    passwordNumeric() {
      return /[0-9]/.test(this.password)
    },
    disabled() {
      return this.username && this.email && this.tgid && this.passwordCheck && this.passwordVerify
    }
  },
  data() {
    return {
      username: '',
      email: '',
      password: '',
      tgid: '',
      passwordV: ''
    }
  },
  methods: {
    async register() {
      try {
        const params = {
          username: this.username,
          email: this.email,
          password: this.password,
          tgid: this.tgid
        }

        let response = await axios.post('users', params, params)

		const loginParams = new URLSearchParams()
		loginParams.append('username', this.username)
		loginParams.append('password', this.password)

		const loginResponse = await axios.post('login', loginParams)
		localStorage.setItem('token', loginResponse.data.access_token)
		this.$router.push('/')
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>
