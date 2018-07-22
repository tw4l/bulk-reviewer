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
        v-for="f in sortedFileData"
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
  props: [ 'fileData', 'features', 'featureType' ],
  methods: {
    compare: function (a, b) {
      // ensure that counts are ints before sorting
      const countA = parseInt(a.count)
      const countB = parseInt(b.count)

      let comparison = 0
      if (countA < countB) {
        comparison = 1
      } else if (countA > countB) {
        comparison = -1
      }
      return comparison
    }
  },
  computed: {
    sortedFileData: function () {
      let arrayToChange = this.fileData
      return arrayToChange.sort(this.compare)
    }
  }
}
</script>

<style>
</style>
