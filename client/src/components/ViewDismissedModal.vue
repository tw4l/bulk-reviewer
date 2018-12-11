<template>
  <div class="modal is-active">
    <div class="modal-background" @click="close"></div>
    <div class="modal-card" style="width: 90% !important;">
      <header class="modal-card-head">
        <p class="modal-card-title">Unconfirmed and dismissed results</p>
        <button class="delete" aria-label="close" @click="close">X</button>
      </header>
      <section class="modal-card-body">
        <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
          <thead>
            <tr>
              <th>File</th>
              <th>Type</th>
              <th>Text</th>
              <th>Context</th>
              <th>Undo</th>
            </tr>
          </thead>
          <tbody>
            <dismissed-table-row v-for="f in paginatedFeaturesCleared" :featureInfo="f" :key="f.uuid"></dismissed-table-row>
          </tbody>
        </table>
        <!-- Pagination -->
        <div class="buttons has-addons">
          <button class="button" @click="decrementStartIndex" :disabled="firstPage">Previous</button>
          <button class="button" disabled>{{ currentPage }} of {{ numberOfPages }}</button>
          <button class="button" @click="incrementStartIndex" :disabled="lastPage">Next</button>
        </div>
      </section>
    </div>
</div>
</template>

<script>
import DismissedTableRow from '@/components/DismissedTableRow'

export default {
  name: 'view-dismissed-modal',
  components: { DismissedTableRow },
  props: [ 'featuresCleared' ],
  data () {
    return {
      startIndex: 0,
      pageCount: 25
    }
  },
  methods: {
    close: function () {
      this.$emit('viewDismissedClose')
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
    paginatedFeaturesCleared () {
      return this.featuresCleared.slice(this.startIndex, this.startIndex + this.pageCount)
    },
    numberOfPages () {
      return Math.ceil(this.featuresCleared.length / this.pageCount)
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
