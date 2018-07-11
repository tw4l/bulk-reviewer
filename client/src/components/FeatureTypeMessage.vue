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
        :featureInfo="f"
        :viewingFile="viewingFile"></individual-feature>
    </div>
  </div>
</template>

<script>
// import axios from 'axios'
import IndividualFeature from '@/components/IndividualFeature'

export default {
  name: 'feature-result',
  props: ['featureType', 'featureTypeCount', 'filteredFeatureArray', 'viewingFile'],
  components: { IndividualFeature },
  data () {
    return {
      showMessageBody: false
    }
  },
  methods: {
    toggleMessageBody: function () {
      this.showMessageBody = !this.showMessageBody
    },
    markAllFeaturesRedacted: function () {
      // in place for testing - replace with API call and front end refresh
      let uuids = this.filteredFeatureUUIDArray
      console.log(uuids)
      // emit signal for each uuid
      let self = this
      uuids.forEach(function (uuid) {
        self.$emit('redactFeature', uuid)
      })
    },
    markAllFeaturesCleared: function () {
      // in place for testing - replace with API call and front end refresh
      let uuids = this.filteredFeatureUUIDArray
      console.log(uuids)
      // emit signal for each uuid
      let self = this
      uuids.forEach(function (uuid) {
        self.$emit('clearFeature', uuid)
      })
    }
  },
  computed: {
    filteredFeatureUUIDArray () {
      return this.filteredFeatureArray.map(a => a.uuid)
    }
  }
}
</script>

<style>
</style>
