<template>
  <tr>
    <td>{{ config.name }}</td>
    <td>
      <button class="button is-small" @click="deleteConfig">
        <font-awesome-icon icon="trash-alt"></font-awesome-icon>
      </button>
    </td>
  </tr>
</template>

<script>
import axios from 'axios'

export default {
  name: 'existing-config',
  props: [ 'config' ],
  data () {
    return {
      errors: []
    }
  },
  methods: {
    deleteConfig: function () {
      axios.delete(`http://127.0.0.1:8000/api/config/${this.config.uuid}/`)
        .then(response => {
          console.log(response)
          this.$emit('removeSession', this.config.uuid)
        })
        .catch(e => {
          this.errors.push(e)
        })
    }
  }
}
</script>

<style>
</style>
