<script setup>
</script>
<template>
  <div class="flex flex-row w-full text-wrap h-full">
	  <div class="basis-1/3 w-1/3" style="background-color: red;">
      <div>
      </div>
    </div>
    <div class="basis-2/3"></div>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  data() {
    return {}
  },
  async created() {
    try {
      const response = await axios.get('users')
      this.user = response.data
      const adminResponse = await axios.get('users/is_admin')
      if (adminResponse.data) {
        this.items.push({
          label: 'admin',
          icon: 'pi pi-user-plus',
          url: '/admin'
        })
      }

    } catch (error) {
      console.error(error)
    }
  }
}
</script>
