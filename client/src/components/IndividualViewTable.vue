<template>
  <div>
    <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
      <thead>
        <tr>
          <th>Text</th>
          <th>Context</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <individual-view-table-row
          v-for="f in paginatedFeatureData"
          :key="f.uuid"
          :featureInfo="f"
          :showFileBrowser="showFileBrowser">
        </individual-view-table-row>
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
import IndividualViewTableRow from '@/components/IndividualViewTableRow'

export default {
  name: 'individual-view-table',
  components: { IndividualViewTableRow },
  props: [ 'featureData', 'showFileBrowser' ],
  data () {
    return {
      startIndex: 0,
      pageCount: 5
    }
  },
  methods: {
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
    paginatedFeatureData () {
      return this.featureData.slice(this.startIndex, this.startIndex + this.pageCount)
    },
    numberOfPages () {
      return Math.ceil(this.featureData.length / this.pageCount)
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
