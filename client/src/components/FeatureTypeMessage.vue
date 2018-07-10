<template>
  <div class="message">
    <div class="message-header">
      <span @click="toggleMessageBody">{{ featureType }} ({{ featureTypeCount }})</span>
      <span style="align: right;">
        <button
          class="button is-danger"
          @click="markAllFeaturesRedacted">
          <font-awesome-icon icon="bars" class="fa-fw"></font-awesome-icon>
          Redact all
        </button>
        <button
          class="button is-success"
          @click="markAllFeaturesCleared">
          <font-awesome-icon icon="check" class="fa-fw"></font-awesome-icon>
          Clear all
        </button>
        <button class="button" @click="toggleMessageBody">(+/-)</button>
      </span>
    </div>
    <div class="message-body" v-show="showMessageBody" style="word-wrap: break-word;">
      <individual-feature
        v-for="f in filteredFeatureArray"
        :key="f.uuid"
        :featureInfo="f"></individual-feature>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import IndividualFeature from '@/components/IndividualFeature'

export default {
  name: 'feature-result',
  props: ['featureType', 'featureTypeCount', 'filteredFeatureArray'],
  components: { IndividualFeature },
  data () {
    return {
      showMessageBody: false
    }
  },
  methods: {
    toggleMessageBody: function () {
      this.showMessageBody = !this.showMessageBody
      this.$emit('getFeatureStatus')
    },
    markAllFeaturesRedacted: function () {
      let featuresToRedact = this.filteredFeatureArray
      let self = this
      featuresToRedact.forEach(function (f) {
        let featureUUID = f.uuid
        self.markFeatureRedacted(featureUUID)
      })
    },
    markAllFeaturesCleared: function () {
      let featuresToClear = this.filteredFeatureArray
      let self = this
      featuresToClear.forEach(function (f) {
        let featureUUID = f.uuid
        self.markFeatureCleared(featureUUID)
      })
    },
    markFeatureRedacted: function (featureUUID) {
      axios.patch(`http://127.0.0.1:8000/api/feature/${featureUUID}/`, { 'redact_feature': true, 'cleared': false }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
          this.$emit('getFeatureStatus')
        })
        .catch(e => {
          console.log(e)
        })
    },
    markFeatureCleared: function (featureUUID) {
      axios.patch(`http://127.0.0.1:8000/api/feature/${featureUUID}/`, { 'redact_feature': false, 'cleared': true }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
          this.$emit('getFeatureStatus')
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
