<template>
  <div>
    <div>
      <p><strong>Feature: </strong> {{ featureInfo.feature }}</p>
      <p><strong>Context: </strong> {{ featureInfo.context }}</p>
      <p v-if="viewingFile === false"><strong>File: </strong> {{ featureInfo.source_file }}</p>
    </div>
    <div>
      <button
        class="button"
        :class="{ 'is-danger': featureRedacted === true }"
        @click="markFeatureRedacted">
        <font-awesome-icon icon="bars"></font-awesome-icon>
      </button>
      <button
        class="button"
        :class="{ 'is-success': featureCleared === true }"
        @click="markFeatureCleared">
        <font-awesome-icon icon="check"></font-awesome-icon>
      </button>
      </div>
    <br>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'individual-feature',
  props: [ 'featureInfo', 'viewingFile' ],
  data () {
    return {
      featureRedacted: false,
      featureCleared: false
    }
  },
  created () {
    this.featureRedacted = this.featureInfo.redact_feature
    this.featureCleared = this.featureInfo.cleared

    // listen for parent signals with this uuid
    this.$parent.$on('redactFeature', this.showAsRedacted)
    this.$parent.$on('clearFeature', this.showAsCleared)
  },
  methods: {
    markFeatureRedacted: function () {
      let featureUUID = this.featureInfo.uuid
      axios.patch(`http://127.0.0.1:8000/api/feature/${featureUUID}/`, { 'redact_feature': true, 'cleared': false }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
          this.featureRedacted = true
          this.featureCleared = false
        })
        .catch(e => {
          console.log(e)
        })
    },
    showAsRedacted: function (uuid) {
      if (uuid === this.featureInfo.uuid) {
        this.featureRedacted = true
        this.featureCleared = false
        console.log(this.featureInfo.uuid, 'marked as redacted')
      }
    },
    showAsCleared: function (uuid) {
      if (uuid === this.featureInfo.uuid) {
        this.featureRedacted = false
        this.featureCleared = true
        console.log(this.featureInfo.uuid, 'marked as cleared')
      }
    },
    markFeatureCleared: function () {
      let featureUUID = this.featureInfo.uuid
      axios.patch(`http://127.0.0.1:8000/api/feature/${featureUUID}/`, { 'redact_feature': false, 'cleared': true }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
          this.featureRedacted = false
          this.featureCleared = true
        })
        .catch(e => {
          console.log(e)
        })
    }
  }
}
</script>

<style>
</style>
