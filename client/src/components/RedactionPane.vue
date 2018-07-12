<template>
  <div v-if="loading === true">
    <font-awesome-icon icon="spinner" class="fa-spin"></font-awesome-icon>
  </div>
  <div v-else>
    <!-- All files button -->
    <div style="margin-bottom: 15px;">
      <button v-if="fileInfo.uuid" class="button" @click="getAllSessionFeatures"><font-awesome-icon icon="level-up-alt" class="fa-fw"></font-awesome-icon>All results</button>
    </div>
    <!-- Context -->
    <div style="margin-bottom: 15px;">
      <h4 class="title is-4" v-if="fileInfo.filepath">{{ filePathWithLineBreaks }}</h4>
      <h4 class="title is-4" v-else>All results</h4>
    </div>
    <!-- Metadata -->
    <div style="margin-bottom: 15px;">
      <p v-if="allClear"><strong>Status:</strong> Clear (no features in file)</p>
      <p v-else-if="fileInfo.uuid && (fileInfo.cleared === true)"><strong>Status:</strong> <span class="cleared">Cleared</span></p>
      <p v-else-if="fileInfo.uuid && (fileInfo.redact_file === true)"><strong>Status:</strong> <span class="redacted">Redacted</span></p>
      <p v-else><strong>Status:</strong> Under review</p>
      <p><strong>Results:</strong> {{ featureCount }}</p>
    </div>
    <!-- Sctions -->
    <div v-show="!allClear">
      <button class="button is-danger" @click="markFileRedacted" v-if="fileInfo.uuid && (fileInfo.redact_file === false) && (fileInfo.cleared === false)">Mark file redacted</button>
      <button class="button is-success" @click="markFileCleared" v-if="fileInfo.uuid && (fileInfo.cleared === false)">Mark file reviewed</button>
      <button class="button" @click="markFileNotCleared" v-else-if="fileInfo.uuid && (fileInfo.cleared === true)">Undo reviewed</button>
    </div>
    <hr>
    <!-- Features grouped by type -->
    <feature-type-message
    v-for="featureType in featureTypeArray"
    :key="featureType"
    :featureType="featureType"
    :featureTypeCount="featureTypeCount(featureType)"
    :filteredFeatureArray="filterByFeatureType(featureType)"
    :viewingFile="viewingFile"
    ></feature-type-message>
  </div>
</template>

<script>
import axios from 'axios'
import FeatureTypeMessage from '@/components/FeatureTypeMessage'
import Alert from '@/components/Alert'

export default {
  name: 'redaction-pane',
  props: [ 'currentlySelectedUUID' ],
  components: { FeatureTypeMessage, Alert },
  data () {
    return {
      fileInfo: {},
      features: [],
      errors: [],
      messagesOpen: false,
      alertMessage: '',
      showAlertMessage: false,
      loading: true,
      viewingFile: false
    }
  },
  created () {
    this.getAllSessionFeatures()
  },
  watch: {
    currentlySelectedUUID: function (newUUID, oldUUID) {
      // hide alert message from last file if existing
      this.showAlertMessage = false
      // mark redaction pane as viewing single file
      this.viewingFile = true
      // update data shown to user
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
      this.loading = true
      let apiCall = 'http://127.0.0.1:8000/api' + this.$route.path + '/features/'
      axios.get(`${apiCall}`)
        .then(response => {
          this.features = response.data
          this.loading = false
        })
        .catch(e => {
          this.errors.push(e)
        })
      // clear fileInfo
      this.fileInfo = {}
      // mark redaction pane as viewing session
      this.viewingFile = false
    },
    markFileCleared () {
      let fileUUID = this.fileInfo.uuid
      axios.patch(`http://127.0.0.1:8000/api/file/${fileUUID}/`, { 'cleared': true, 'redact_file': false }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
          this.alertMessage = 'Success'
          this.showAlertMessage = true
          this.updateRedactionPane(fileUUID)
        })
        .catch(e => {
          this.errors.push(e)
          this.alertMessage = 'Failure updating database via API. ' + e
          this.showAlertMessage = true
        })
    },
    markFileNotCleared () {
      let fileUUID = this.fileInfo.uuid
      axios.patch(`http://127.0.0.1:8000/api/file/${fileUUID}/`, { 'cleared': false }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
          this.alertMessage = 'Success'
          this.showAlertMessage = true
          this.updateRedactionPane(fileUUID)
        })
        .catch(e => {
          this.errors.push(e)
          this.alertMessage = 'Failure updating database via API. ' + e
          this.showAlertMessage = true
        })
    },
    markFileRedacted () {
      let fileUUID = this.fileInfo.uuid
      axios.patch(`http://127.0.0.1:8000/api/file/${fileUUID}/`, { 'redact_file': true, 'cleared': false }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
          this.alertMessage = 'Success'
          this.showAlertMessage = true
          this.updateRedactionPane(fileUUID)
        })
        .catch(e => {
          this.alertMessage = 'Failure updating database via API. ' + e
          this.showAlertMessage = true
        })
    },
    markFileNotRedacted () {
      let fileUUID = this.fileInfo.uuid
      axios.patch(`http://127.0.0.1:8000/api/file/${fileUUID}/`, { 'redact_file': false }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
          this.alertMessage = 'Success'
          this.showAlertMessage = true
          this.updateRedactionPane(fileUUID)
        })
        .catch(e => {
          this.alertMessage = 'Failure updating database via API. ' + e
          this.showAlertMessage = true
        })
    },
    updateRedactionPane (fileUUID) {
      axios.get(`http://127.0.0.1:8000/api/file/${fileUUID}/`)
        .then(response => {
          this.fileInfo = response.data
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
    },
    allClear () {
      return this.features.length === 0
    },
    filePathWithLineBreaks () {
      // Add <br> tag every 100 chars for narrow display
      return this.fileInfo.filepath.replace(/(.{100})/g, '$1<br>')
    }
  }
}
</script>

<style>
.cleared {
  color: green;
}
.redacted {
  color: red;
}
</style>
