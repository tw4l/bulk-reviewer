<template>
  <tr>
    <td>{{ filepathWithLineBreaks }}  <button class="button is-small" @click="viewFile">View</button></td>
    <td>{{ fileInfo.count }}</td>
    <td>
      <button class="button is-success" @click="markReviewed"><font-awesome-icon icon="eye-slash"></font-awesome-icon></button>
    </td>
  </tr>
</template>

<script>
import axios from 'axios'
import bus from '../bus'

export default {
  name: 'bulk-view-table-row',
  props: [ 'fileInfo' ],
  methods: {
    viewFile: function () {
      bus.$emit('viewFileFromBulkTable', this.fileInfo.file_uuid)
    },
    markReviewed: function () {
      let fileUUID = this.fileInfo.file_uuid
      axios.patch(`http://127.0.0.1:8000/api/file/${fileUUID}/`, { 'cleared': true }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
    }
  },
  computed: {
    filepathWithLineBreaks: function () {
      // Add a space tag every 60 chars for narrow display
      return this.fileInfo.filepath.replace(/(.{60})/g, '$1 ')
    }
  }
}
</script>

<style>
</style>
