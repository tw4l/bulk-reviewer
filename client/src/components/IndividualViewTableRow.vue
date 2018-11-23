<template>
  <tr :class="{ dismissed: featureInfo.cleared === true }">
    <!-- Feature -->
    <td v-if="showFileBrowser">{{ featureWithLineBreaks }}
      <button
        class="button is-small"
        v-clipboard:copy="featureInfo.feature"
        v-tooltip="'Copy the matching text to the clipboard'">Copy</button>
    </td>
    <td v-else>{{ unescapedFeature }}
      <button
        class="button is-small"
        v-clipboard:copy="featureInfo.feature"
        v-tooltip="'Copy the matching text to the clipboard'">Copy</button>
    </td>
    <!-- Context -->
    <td v-if="showFileBrowser">{{ contextWithLineBreaks }}</td>
    <td v-else>{{ unescapedContext }}</td>
    <!-- Buttons -->
    <td v-if="featureInfo.cleared === false">
      <button class="button is-info" @click="markCleared" v-tooltip="'Dismiss result as false positive'"><font-awesome-icon icon="check"></font-awesome-icon></button>
    </td>
    <td v-else>
      <button class="button" @click="markNotCleared" v-tooltip="'Confirm result as sensitive'"><font-awesome-icon icon="times"></font-awesome-icon></button>
    </td>
  </tr>
</template>

<script>
import { HTTP } from '../api'

export default {
  name: 'individual-view-table-row',
  props: [ 'featureInfo', 'showFileBrowser', 'critical' ],
  methods: {
    markCleared: function () {
      let featureUUID = this.featureInfo.uuid
      HTTP.patch(`feature/${featureUUID}/`, { 'cleared': true }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
    },
    markNotCleared: function () {
      let featureUUID = this.featureInfo.uuid
      HTTP.patch(`feature/${featureUUID}/`, { 'cleared': false }, { headers: { 'Content-Type': 'application/json' } })
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
      // Add a space every 40 chars for narrow display
      return this.unescapedFeature.replace(/(.{40})/g, '$1 ')
    },
    contextWithLineBreaks: function () {
      // Add a space every 40 chars for narrow display
      return this.unescapedContext.replace(/(.{40})/g, '$1 ')
    }
  }
}
</script>

<style>
.dismissed {
  color: #8c8c8c;
}
</style>
