<template>
  <div>
    <p><strong>Feature: </strong> {{ featureInfo.feature }}</p>
    <p><strong>Context: </strong> {{ contextWithLineBreaks }}</p>
    <br>
  </div>
</template>

<script>
export default {
  name: 'individual-feature',
  props: [ 'featureInfo' ],
  computed: {
    contextWithLineBreaks: function () {
      // Add <br> tag every 100 chars for narrow display
      return this.featureInfo.context.replace(/(.{100})/g, '$1<br>')
    }
  }
}
</script>

<style>
</style>
