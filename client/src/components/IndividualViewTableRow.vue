<template>
  <tr :class="{ cleared: featureInfo.cleared === true }">
    <!-- Feature -->
    <td v-if="showFileBrowser">{{ featureWithLineBreaks }}
      <button
        class="button is-small"
        v-clipboard:copy="featureInfo.feature">Copy</button>
    </td>
    <td v-else>{{ unescapedFeature }}
      <button
        class="button is-small"
        v-clipboard:copy="featureInfo.feature">Copy</button>
    </td>
    <!-- Context -->
    <td v-if="showFileBrowser">{{ contextWithLineBreaks }}</td>
    <td v-else>{{ unescapedContext }}</td>
    <!-- Buttons -->
    <td v-if="featureInfo.cleared === false">
      <button class="button is-info" @click="markCleared"><font-awesome-icon icon="eye-slash"></font-awesome-icon></button>
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
  props: [ 'featureInfo', 'showFileBrowser' ],
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
    },
    addNote: function () {
      // TODO: Add note
      alert('Not yet implemented!')
    }
  },
  computed: {
    unescapedFeature: function () {
      return this.featureInfo.feature.replace(/\\x[a-fA-F0-9]{2}/g, String.fromCharCode('$1'))
    },
    unescapedContext: function () {
      return this.featureInfo.context.replace(/\\x[a-fA-F0-9]{2}/g, String.fromCharCode('$1'))
    },
    featureWithLineBreaks: function () {
      // Add a space tag every 40 chars for narrow display
      return this.funescapedFeature.replace(/(.{40})/g, '$1 ')
    },
    contextWithLineBreaks: function () {
      // Add a space tag every 40 chars for narrow display
      return this.unescapedContext.replace(/(.{40})/g, '$1 ')
    }
  }
}
</script>

<style>
.cleared {
  color: #808080;
}
</style>
