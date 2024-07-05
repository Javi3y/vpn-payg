<script setup>
import Chart from 'primevue/chart'
</script>
<template>
  <div v-if="clientHistory">
    <Chart type="line" :data="this.dataset" :options="chartOptions" class="h-[20rem]" />
  </div>
</template>
<script>
import axios from 'axios'
export default {
  props: ['user'],
  data() {
    return {
      clientHistory: null,
      dataset: null
    }
  },
  async created() {
    try {
      const response = await axios.get(`/clients/${this.$route.params.id}/usage`)
      this.clientHistory = response.data
      this.dataset = {
        labels: this.clientHistory.map(function (ch) {
          return ch.time
        }),
        datasets: [
          {
            label: 'Usage',
            data: this.clientHistory.map(function (ch) {
              return ch.usage
            })
          },
          {
            label: 'Total usage',
            data: this.clientHistory.map(function (ch) {
              return ch.last_usage
            })
          }
        ]
      }
    } catch (error) {
      console.error(error)
    }
  },
  methods: {}
}
</script>
