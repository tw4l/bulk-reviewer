<template>
  <tr>
    <td>{{ fileInfo.filepath }}</td>
    <td>{{ fileInfo.count }}</td>
    <td>
      <button class="button" @click="viewFile">View file</button>
      <button class="button is-success" @click="markReviewed">Clear all<font-awesome-icon icon="eye-slash"></font-awesome-icon></button>
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
  }
}
</script>

<style>
</style>
