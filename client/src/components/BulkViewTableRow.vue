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
// import axios from 'axios'
import bus from '../bus'

export default {
  name: 'bulk-view-table-row',
  props: [ 'fileInfo' ],
  methods: {
    viewFile: function () {
      bus.$emit('viewFileFromBulkTable', this.fileInfo.file_uuid)
    },
    markReviewed: function () {
      // TODO: Batch update all features in this file as cleared
      alert('Not yet implemented!')
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
