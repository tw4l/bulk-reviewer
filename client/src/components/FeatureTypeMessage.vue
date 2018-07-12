<template>
  <div class="message">
    <div class="message-header" @click="toggleMessageBody" style="align: left;">
      <font-awesome-icon icon="caret-down" v-if="showMessageBody"></font-awesome-icon>
      <font-awesome-icon icon="caret-right" v-else></font-awesome-icon>
      {{ featureType }} ({{ featureTypeCount }})
    </div>
    <div class="message-body" v-show="showMessageBody" style="word-wrap: break-word;">
      <button
        class="button is-danger"
        @click="markAllFeaturesRedacted">
        <font-awesome-icon icon="bars" class="fa-fw"></font-awesome-icon>
        Mark all redacted
      </button>
      <button
        class="button is-success"
        @click="markAllFeaturesCleared"
        style="margin-bottom:15px;">
        <font-awesome-icon icon="check" class="fa-fw"></font-awesome-icon>
        Mark all reviewed
      </button>
      <individual-feature
        v-for="f in filteredFeatureArray"
        :key="f.uuid"
        :featureInfo="f"
        :viewingFile="viewingFile">
      </individual-feature>
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
