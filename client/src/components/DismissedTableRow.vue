<template>
  <tr>
    <td>{{ featureInfo.source_filepath }}</td>
    <td>{{ unescapedFeature }}</td>
    <td>{{ unescapedContext }}</td>
    <td><button class="button is-info" @click="markCleared"><font-awesome-icon icon="check"></font-awesome-icon></button></td>
  </tr>
</template>

<script>
export default {
  name: 'dismissed-table-row',
  props: [ 'featureInfo' ],
  methods: {
    markCleared: function () {
      alert('Not yet implemented!')
    }
  },
  computed: {
    unescapedFeature: function () {
      return this.featureInfo.feature.replace(/\\x[a-fA-F0-9]{2}/g, String.fromCharCode('$1'))
    },
    unescapedContext: function () {
      return this.featureInfo.context.replace(/\\x[a-fA-F0-9]{2}/g, String.fromCharCode('$1'))
    }
  }
}
</script>

<style>
</style>
