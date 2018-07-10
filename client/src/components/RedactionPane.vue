<template>
  <div>
    <p><strong>Path:</strong> {{ fileInfo.filepath || "Entire Session" }}</p>
    <p v-if="fileInfo.uuid"><strong>Cleared:</strong> {{ fileInfo.cleared }}</p>
    <p v-if="fileInfo.uuid"><strong>Marked for redaction:</strong> {{ fileInfo.redact_file }}</p>
    <p><strong>Features:</strong> {{ featureCount }}</p>
    <button class="button" @click="getAllSessionFeatures">See all Session features</button>
    <div>
      <button class="button is-success" @click="markFileCleared" v-if="fileInfo.uuid && (fileInfo.cleared === false)">Mark file cleared</button>
      <button class="button" @click="markFileNotCleared" v-else-if="fileInfo.uuid && (fileInfo.cleared === true)">Mark file not cleared</button>
    </div>
    <div>
      <button class="button is-danger" @click="markFileRedacted" v-if="fileInfo.uuid && (fileInfo.redact_file === false) && (fileInfo.cleared === false)">Mark file redacted</button>
    </div>
    <hr>
    <feature-type-message
    v-for="featureType in featureTypeArray"
    :key="featureType"
    :featureType="featureType"
    :featureTypeCount="featureTypeCount(featureType)"
    :filteredFeatureArray="filterByFeatureType(featureType)"
    ></feature-type-message>
  </div>
</template>

<script>
import axios from 'axios'
import FeatureTypeMessage from '@/components/FeatureTypeMessage'

export default {
  name: 'redaction-pane',
  props: [ 'currentlySelectedUUID' ],
  components: { FeatureTypeMessage },
  data () {
    return {
      fileInfo: {},
      features: [],
      errors: [],
      messagesOpen: false
    }
  },
  created () {
    this.getAllSessionFeatures()
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
    },
    getAllSessionFeatures () {
      // retrieve data
      let apiCall = 'http://127.0.0.1:8000/api' + this.$route.path + '/features/'
      axios.get(`${apiCall}`)
        .then(response => {
          this.features = response.data
        })
        .catch(e => {
          this.errors.push(e)
        })
      // clear fileInfo
      this.fileInfo = {}
    },
    markFileCleared () {
      let fileUUID = this.fileInfo.uuid
      axios.patch(`http://127.0.0.1:8000/api/file/${fileUUID}/`, { 'cleared': true, 'redact_file': false }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
          alert('success!')
        })
        .catch(e => {
          this.errors.push(e)
        })
    },
    markFileNotCleared () {
      let fileUUID = this.fileInfo.uuid
      axios.patch(`http://127.0.0.1:8000/api/file/${fileUUID}/`, { 'cleared': false }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          this.errors.push(e)
        })
    },
    markFileRedacted () {
      let fileUUID = this.fileInfo.uuid
      axios.patch(`http://127.0.0.1:8000/api/file/${fileUUID}/`, { 'redact_file': true, 'cleared': false }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
          alert('success!')
        })
        .catch(e => {
          this.errors.push(e)
        })
    },
    markFileNotRedacted () {
      let fileUUID = this.fileInfo.uuid
      axios.patch(`http://127.0.0.1:8000/api/file/${fileUUID}/`, { 'redact_file': false }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          this.errors.push(e)
        })
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
