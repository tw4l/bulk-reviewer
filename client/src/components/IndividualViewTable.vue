<template>
  <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
    <thead>
      <tr>
        <th>Feature</th>
        <th>Context</th>
        <th>Ignore</th>
      </tr>
    </thead>
    <tbody>
      <individual-view-table-row
        v-for="f in featureData"
        :key="f.uuid"
        :featureInfo="f">
      </individual-view-table-row>
    </tbody>
  </table>
</template>

<script>
import IndividualViewTableRow from '@/components/IndividualViewTableRow'

export default {
  name: 'individual-view-table',
  components: { IndividualViewTableRow },
  props: [ 'featureData' ]
}
</script>

<style>
</style>
