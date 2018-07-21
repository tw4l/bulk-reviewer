<template>
  <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
    <thead>
      <tr>
        <th>File</th>
        <th>Count</th>
        <th>Ignore</th>
      </tr>
    </thead>
    <tbody>
      <bulk-view-table-row
        v-for="f in fileData"
        :key="f.uuid"
        :fileInfo="f"
        :features="features"
        :featureType="featureType">
      </bulk-view-table-row>
    </tbody>
  </table>
</template>

<script>
import BulkViewTableRow from '@/components/BulkViewTableRow'

export default {
  name: 'bulk-view-table',
  components: { BulkViewTableRow },
  props: [ 'fileData', 'features', 'featureType' ]
}
</script>

<style>
</style>
