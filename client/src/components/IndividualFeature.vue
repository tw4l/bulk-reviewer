<template>
  <div>
    <p><strong>Feature: </strong> {{ featureInfo.feature }}</p>
    <p><strong>Context: </strong> {{ featureInfo.context }}</p>
    <p v-if="viewingFile === false"><strong>File: </strong> {{ featureInfo.source_filepath }}</p>
    <br>
  </div>
</template>

<script>
export default {
  name: 'individual-feature',
  props: [ 'featureInfo', 'viewingFile' ]
}
</script>

<style>
</style>
