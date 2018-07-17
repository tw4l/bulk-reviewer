<template>
  <tr>
    <td>{{ fileInfo.filepath }}</td>
    <td>{{ fileInfo.count }}</td>
    <td><button class="button" @click="viewFile">View file</button></td>
  </tr>
</template>

<script>
import bus from '../bus'

export default {
  name: 'bulk-view-table-row',
  props: [ 'fileInfo' ],
  methods: {
    viewFile: function (newUUID) {
      bus.$emit('viewFileFromBulkTable', this.fileInfo.file_uuid)
    }
  }
}
</script>

<style>
</style>
