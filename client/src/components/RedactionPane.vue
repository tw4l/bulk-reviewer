<template>
  <div>
    <p><strong>Path:</strong> {{ fileInfo.filepath }}</p>
    <p><strong>Features:</strong> {{ featureCount }}</p>
    <hr>
    <div class="message" v-for="featureType in featureTypeArray" :key="featureType">
      <div class="message-header">{{ featureType }} ({{ featureTypeCount(featureType) }})</div>
      <div class="message-body">
        <ul>
          <li v-for="f in filterByFeatureType(featureType)" :key="f.uuid">
            <p><strong>Feature: </strong> {{ f.feature }}</p>
            <p><strong>Context: </strong> {{ f.context }}</p>
            <br>
          </li>
        </ul>
      </div>
      <hr>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'redaction-pane',
  props: [ 'currentlySelectedUUID' ],
  data () {
    return {
      fileInfo: {},
      features: [],
      errors: []
    }
  },
  watch: {
    currentlySelectedUUID: function (newUUID, oldUUID) {
      axios.get(`http://127.0.0.1:8000/api/file/${newUUID}/`)
        .then(response => {
          this.fileInfo = response.data
        })
        .catch(e => {
          this.errors.push(e)
        })
      axios.get(`http://127.0.0.1:8000/api/file/${newUUID}/features`)
        .then(response => {
          this.features = response.data
        })
        .catch(e => {
          this.errors.push(e)
        })
    }
  },
  methods: {
    featureTypeCount: function (featureFile) {
      return this.features.filter(feature => feature['feature_file'] === featureFile).length
    },
    filterByFeatureType (featureFile) {
      return this.features.filter(feature => feature['feature_file'] === featureFile)
    }
  },
  computed: {
    featureCount () {
      return this.features.length
    },
    featureTypeArray () {
      return [...new Set(this.features.map(feature => feature['feature_file']))]
    }
  }
}
</script>

<style>
</style>
