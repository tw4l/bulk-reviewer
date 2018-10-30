<template>
  <div>
    <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
      <thead>
        <tr>
          <th>File</th>
          <th>Count</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <bulk-view-table-row
          v-for="f in paginatedFileData"
          :key="f.uuid"
          :fileInfo="f"
          :features="features"
          :featureType="featureType"
          :showFileBrowser="showFileBrowser">
        </bulk-view-table-row>
      </tbody>
    </table>
    <!-- Pagination -->
    <div class="buttons has-addons">
      <button class="button" @click="decrementStartIndex" :disabled="firstPage">Previous</button>
      <button class="button" disabled>{{ currentPage }} of {{ numberOfPages }}</button>
      <button class="button" @click="incrementStartIndex" :disabled="lastPage">Next</button>
    </div>
  </div>
</template>

<script>
import BulkViewTableRow from '@/components/BulkViewTableRow'

export default {
  name: 'bulk-view-table',
  components: { BulkViewTableRow },
  props: [ 'fileData', 'features', 'featureType', 'showFileBrowser' ],
  data () {
    return {
      startIndex: 0,
      pageCount: 5
    }
  },
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
    },
    resetStartIndex () {
      this.startIndex = 0
    },
    incrementStartIndex () {
      this.startIndex += this.pageCount
    },
    decrementStartIndex () {
      this.startIndex -= this.pageCount
    }
  },
  computed: {
    sortedFileData: function () {
      let arrayToChange = this.fileData
      return arrayToChange.sort(this.compare)
    },
    paginatedFileData () {
      return this.sortedFileData.slice(this.startIndex, this.startIndex + this.pageCount)
    },
    numberOfPages () {
      return Math.ceil(this.sortedFileData.length / this.pageCount)
    },
    currentPage () {
      return this.startIndex === 0 ? 1 : Math.ceil(this.startIndex / this.pageCount) + 1
    },
    moreThanOnePage () {
      return this.numberOfPages > 1
    },
    firstPage () {
      return this.currentPage === 1
    },
    lastPage () {
      return this.currentPage >= this.numberOfPages
    }
  }
}
</script>

<style>
</style>
