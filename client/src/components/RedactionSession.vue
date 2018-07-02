<template>
<div>File tree here</div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'session',
  data () {
    return {
      files: [],
      features: [],
      errors: []
    }
  },

  created () {
    let uuid = this.$route.params.uuid
    axios.get(`http://127.0.0.1:8000/api/session/${uuid}/files/`)
      .then(response => {
        this.files = response.data.results
      })
      .catch(e => {
        this.errors.push(e)
      })
    axios.get(`http://127.0.0.1:8000/api/session/${uuid}/features/`)
      .then(response => {
        this.features = response.data.results
      })
      .catch(e => {
        this.errors.push(e)
      })
  }
}
</script>

<style>
</style>
