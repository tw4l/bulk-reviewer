<template>
  <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
    <thead>
      <tr>
        <th>Matching text</th>
        <th>Context</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <individual-view-table-row
        v-for="f in featureData"
        :key="f.uuid"
        :featureInfo="f"
        :showFileBrowser="showFileBrowser">
      </individual-view-table-row>
    </tbody>
  </table>
</template>

<script>
import IndividualViewTableRow from '@/components/IndividualViewTableRow'

export default {
  name: 'individual-view-table',
  components: { IndividualViewTableRow },
  props: [ 'featureData', 'showFileBrowser' ]
}
</script>

<style>
</style>
