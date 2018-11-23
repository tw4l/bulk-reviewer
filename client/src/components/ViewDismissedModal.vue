<template>
  <div class="modal is-active">
    <div class="modal-background" @click="close"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Dismissed results</p>
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
            <dismissed-table-row v-for="f in featuresCleared" :featureInfo="f" :key="f.uuid"></dismissed-table-row>
          </tbody>
        </table>
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
  methods: {
    close: function () {
      this.$emit('viewDismissedClose')
    }
  }
}
</script>
