<template>
  <table class="table">
    <thead>
      <tr>
        <th>File</th>
        <th>Count</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <bulk-view-table-row
        v-for="f in fileData"
        :key="f.uuid"
        :fileInfo="f">
      </bulk-view-table-row>
    </tbody>
  </table>
</template>

<script>
import BulkViewTableRow from '@/components/BulkViewTableRow'

export default {
  name: 'bulk-view-table',
  components: { BulkViewTableRow },
  props: [ 'fileData' ]
}
</script>

<style>
</style>
