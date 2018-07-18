<template>
  <tr :class="{ cleared: featureInfo.cleared === true }">
    <td>{{ featureInfo.feature }}</td>
    <td>{{ contextWithLineBreaks }}</td>
    <td v-if="featureInfo.cleared === false">
      <button class="button is-success" @click="markCleared"><font-awesome-icon icon="eye-slash"></font-awesome-icon></button>
    </td>
    <td v-else>
      <button class="button" @click="markNotCleared">Undo</button>
    </td>
  </tr>
</template>

<script>
import axios from 'axios'

export default {
  name: 'individual-view-table-row',
  props: [ 'featureInfo' ],
  methods: {
    markCleared: function () {
      let featureUUID = this.featureInfo.uuid
      axios.patch(`http://127.0.0.1:8000/api/feature/${featureUUID}/`, { 'cleared': true }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
    },
    markNotCleared: function () {
      let featureUUID = this.featureInfo.uuid
      axios.patch(`http://127.0.0.1:8000/api/feature/${featureUUID}/`, { 'cleared': false }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
    }
  },
  computed: {
    contextWithLineBreaks: function () {
      // Add <br> tag every 100 chars for narrow display
      return this.featureInfo.context.replace(/(.{100})/g, '$1<br>')
    }
  }
}
</script>

<style>
.cleared {
  color: #808080;
}
</style>
