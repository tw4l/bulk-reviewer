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
import { HTTP } from '../api'

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
      HTTP.delete(`config/${this.config.uuid}/`)
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
