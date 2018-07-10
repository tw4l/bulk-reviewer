<template>
  <div>
    <div>
      <p><strong>Feature: </strong> {{ featureInfo.feature }}</p>
      <p><strong>Context: </strong> {{ featureInfo.context }}</p>
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
  props: [ 'featureInfo' ],
  data () {
    return {
      featureRedacted: false,
      featureCleared: false
    }
  },
  created () {
    this.featureRedacted = this.featureInfo.redact_feature
    this.featureCleared = this.featureInfo.cleared

    this.$parent.$on('getFeatureStatus', this.getFeatureStatus)
  },
  methods: {
    getFeatureStatus: function () {
      let featureUUID = this.featureInfo.uuid
      axios.get(`http://127.0.0.1:8000/api/feature/${featureUUID}/`)
        .then(response => {
          this.featureRedacted = response.data.redact_feature
          this.featureCleared = response.data.cleared
        })
        .catch(e => {
          console.log(e)
        })
    },
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
