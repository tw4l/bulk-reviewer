<template>
  <div v-if="loading === true">
    <font-awesome-icon icon="spinner" class="fa-spin"></font-awesome-icon>
  </div>
  <div v-else>
    <!-- All files button -->
    <div style="margin-bottom: 15px;">
      <button v-if="fileInfo.uuid" class="button" @click="returnToSessionFeatures"><font-awesome-icon icon="level-up-alt" class="fa-fw"></font-awesome-icon>All results</button>
    </div>
    <!-- Context -->
    <div style="margin-bottom: 15px;">
      <h4 class="title is-4" v-if="fileInfo.filepath">{{ filePathWithLineBreaks }}</h4>
      <h4 class="title is-4" v-else>All results</h4>
      <label class="checkbox">
        <input type="checkbox" @click="toggleViewingCleared">
        Show results I've marked as Ignore
      </label>
    </div>
    <!-- Metadata -->
    <div style="margin-bottom: 15px;">
      <p v-if="allClear"><strong>Status:</strong> Clear (no results to review)</p>
      <p v-else><strong>Status:</strong> Under review</p>
      <p><strong>Results found:</strong> {{ featureCount }}</p>
      <p><strong>Results remaining (not Ignored):</strong> {{ featuresNotClearedCount }}</p>
    </div>
    <hr>
    <!-- Features grouped by type -->
    <h5
    class="title is-5"
    v-if="featureFileInArray(['pii.txt', 'ccn.txt', 'telephone.txt', 'email.txt'])">Personally Identifiable Information</h5>
      <feature-type-message
        v-if="featureFileInArray(['pii.txt'])"
        :key="'pii.txt'"
        :featureType="'pii.txt'"
        :featureTypeCount="featureTypeCount('pii.txt')"
        :filteredFeatureArray="filterByFeatureType('pii.txt')"
        :featureTypeCountNotCleared="featureTypeCountNotCleared('pii.txt')"
        :filteredFeatureArrayNotCleared="filterByFeatureTypeNotCleared('pii.txt')"
        :viewingFile="viewingFile"
        :viewingCleared="viewingCleared">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['ccn.txt'])"
        :key="'ccn.txt'"
        :featureType="'ccn.txt'"
        :featureTypeCount="featureTypeCount('ccn.txt')"
        :filteredFeatureArray="filterByFeatureType('ccn.txt')"
        :featureTypeCountNotCleared="featureTypeCountNotCleared('ccn.txt')"
        :filteredFeatureArrayNotCleared="filterByFeatureTypeNotCleared('ccn.txt')"
        :viewingFile="viewingFile"
        :viewingCleared="viewingCleared">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['telephone.txt'])"
        :key="'telephone.txt'"
        :featureType="'telephone.txt'"
        :featureTypeCount="featureTypeCount('telephone.txt')"
        :filteredFeatureArray="filterByFeatureType('telephone.txt')"
        :featureTypeCountNotCleared="featureTypeCountNotCleared('telephone.txt')"
        :filteredFeatureArrayNotCleared="filterByFeatureTypeNotCleared('telephone.txt')"
        :viewingFile="viewingFile"
        :viewingCleared="viewingCleared">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['email.txt'])"
        :key="'email.txt'"
        :featureType="'email.txt'"
        :featureTypeCount="featureTypeCount('email.txt')"
        :filteredFeatureArray="filterByFeatureType('email.txt')"
        :featureTypeCountNotCleared="featureTypeCountNotCleared('email.txt')"
        :filteredFeatureArrayNotCleared="filterByFeatureTypeNotCleared('email.txt')"
        :viewingFile="viewingFile"
        :viewingCleared="viewingCleared">
      </feature-type-message>
    <h5 class="title is-5" v-if="featureFileInArray(['lightgrep.txt'])">User-supplied regular expressions</h5>
      <feature-type-message
        v-if="featureFileInArray(['lightgrep.txt'])"
        :key="'lightgrep.txt'"
        :featureType="'lightgrep.txt'"
        :featureTypeCount="featureTypeCount('lightgrep.txt')"
        :filteredFeatureArray="filterByFeatureType('lightgrep.txt')"
        :featureTypeCountNotCleared="featureTypeCountNotCleared('lightgrep.txt')"
        :filteredFeatureArrayNotCleared="filterByFeatureTypeNotCleared('lightgrep.txt')"
        :viewingFile="viewingFile"
        :viewingCleared="viewingCleared">
      </feature-type-message>
    <h5
      class="title is-5"
      v-if="featureFileInArray(['url.txt', 'domain.txt', 'rfc822.txt', 'httplogs.txt'])">Web resources</h5>
      <feature-type-message
        v-if="featureFileInArray(['url.txt'])"
        :key="'url.txt'"
        :featureType="'url.txt'"
        :featureTypeCount="featureTypeCount('url.txt')"
        :filteredFeatureArray="filterByFeatureType('url.txt')"
        :featureTypeCountNotCleared="featureTypeCountNotCleared('url.txt')"
        :filteredFeatureArrayNotCleared="filterByFeatureTypeNotCleared('url.txt')"
        :viewingFile="viewingFile"
        :viewingCleared="viewingCleared">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['domain.txt'])"
        :key="'domain.txt'"
        :featureType="'domain.txt'"
        :featureTypeCount="featureTypeCount('domain.txt')"
        :filteredFeatureArray="filterByFeatureType('domain.txt')"
        :featureTypeCountNotCleared="featureTypeCountNotCleared('domain.txt')"
        :filteredFeatureArrayNotCleared="filterByFeatureTypeNotCleared('domain.txt')"
        :viewingFile="viewingFile"
        :viewingCleared="viewingCleared">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['rfc822.txt'])"
        :key="'rfc822.txt'"
        :featureType="'rfc822.txt'"
        :featureTypeCount="featureTypeCount('rfc822.txt')"
        :filteredFeatureArray="filterByFeatureType('rfc822.txt')"
        :featureTypeCountNotCleared="featureTypeCountNotCleared('rfc822.txt')"
        :filteredFeatureArrayNotCleared="filterByFeatureTypeNotCleared('rfc822.txt')"
        :viewingFile="viewingFile"
        :viewingCleared="viewingCleared">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['httplogs.txt'])"
        :key="'httplogs.txt'"
        :featureType="'httplogs.txt'"
        :featureTypeCount="featureTypeCount('httplogs.txt')"
        :filteredFeatureArray="filterByFeatureType('httplogs.txt')"
        :featureTypeCountNotCleared="featureTypeCountNotCleared('httplogs.txt')"
        :filteredFeatureArrayNotCleared="filterByFeatureTypeNotCleared('httplogs.txt')"
        :viewingFile="viewingFile"
        :viewingCleared="viewingCleared">
      </feature-type-message>
    <h5 class="title is-5" v-if="featureFileInArray(['gps.txt', 'exif.txt'])">Geolocation and EXIF metadata</h5>
      <feature-type-message
        v-if="featureFileInArray(['gps.txt'])"
        :key="'gps.txt'"
        :featureType="'gps.txt'"
        :featureTypeCount="featureTypeCount('gps.txt')"
        :filteredFeatureArray="filterByFeatureType('gps.txt')"
        :featureTypeCountNotCleared="featureTypeCountNotCleared('gps.txt')"
        :filteredFeatureArrayNotCleared="filterByFeatureTypeNotCleared('gps.txt')"
        :viewingFile="viewingFile"
        :viewingCleared="viewingCleared">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['exif.txt'])"
        :key="'exif.txt'"
        :featureType="'exif.txt'"
        :featureTypeCount="featureTypeCount('exif.txt')"
        :filteredFeatureArray="filterByFeatureType('exif.txt')"
        :featureTypeCountNotCleared="featureTypeCountNotCleared('exif.txt')"
        :filteredFeatureArrayNotCleared="filterByFeatureTypeNotCleared('exif.txt')"
        :viewingFile="viewingFile"
        :viewingCleared="viewingCleared">
      </feature-type-message>
  </div>
</template>

<script>
import axios from 'axios'
import ReconnectingWebsocket from 'reconnectingwebsocket'
import FeatureTypeMessage from '@/components/FeatureTypeMessage'
import Alert from '@/components/Alert'

export default {
  name: 'redaction-pane',
  props: [ 'currentlySelectedUUID' ],
  components: { FeatureTypeMessage, Alert },
  data () {
    return {
      fileInfo: {},
      sessionFeatures: [],
      features: [],
      errors: [],
      messagesOpen: false,
      alertMessage: '',
      showAlertMessage: false,
      loading: true,
      viewingFile: false,
      viewingCleared: false
    }
  },
  created () {
    this.getAllSessionFeatures()
  },
  mounted () {
    // Update features using websocket messages
    // sent after Feature model post_save signal
    let ws = new ReconnectingWebsocket('ws://localhost:8000/ws/features/')

    let self = this
    ws.onmessage = function (message) {
      let data = JSON.parse(message.data)
      // get data from websocket message
      let featureToUpdateUUID = data.message.uuid
      let featureToUpdateCleared = data.message.cleared
      let featureToUpdateNote = data.message.note
      // check features and update feature if UUID matches
      let success = false
      for (var i = 0; i < self.features.length; i++) {
        if (self.features[i].uuid === featureToUpdateUUID) {
          self.features[i].cleared = featureToUpdateCleared
          self.features[i].note = featureToUpdateNote
          success = true
          break
        }
      }
      // log to console if unsuccessful
      if (success === false) {
        console.log('Warning: Feature ' + featureToUpdateUUID + ' not found.')
      }
    }
  },
  watch: {
    currentlySelectedUUID: function (newUUID, oldUUID) {
      if (newUUID !== '') {
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
    }
  },
  methods: {
    featureTypeCount: function (featureFile) {
      return this.features.filter(feature => feature['feature_file'] === featureFile).length
    },
    featureTypeCountNotCleared: function (featureFile) {
      return this.featuresNotCleared.filter(feature => feature['feature_file'] === featureFile).length
    },
    filterByFeatureType (featureFile) {
      return this.features.filter(feature => feature['feature_file'] === featureFile)
    },
    filterByFeatureTypeNotCleared (featureFile) {
      return this.featuresNotCleared.filter(feature => feature['feature_file'] === featureFile)
    },
    // return true if any feature files in input array are in this.featureTypeArray
    featureFileInArray (arrayOfFeatureFiles) {
      let returnValue = false
      let self = this
      arrayOfFeatureFiles.forEach(function (featureFile) {
        if (self.featureTypeArray.includes(featureFile)) {
          returnValue = true
        }
      })
      return returnValue
    },
    featureFileInArrayNotCleared (arrayOfFeatureFiles) {
      let returnValue = false
      let self = this
      arrayOfFeatureFiles.forEach(function (featureFile) {
        if (self.featureTypeArrayNotCleared.includes(featureFile)) {
          returnValue = true
        }
      })
      return returnValue
    },
    getAllSessionFeatures () {
      // retrieve data
      this.loading = true
      let apiCall = 'http://127.0.0.1:8000/api' + this.$route.path + '/features/'
      axios.get(`${apiCall}`)
        .then(response => {
          this.sessionFeatures = response.data
          this.features = this.sessionFeatures
          this.loading = false
        })
        .catch(e => {
          this.errors.push(e)
        })
      // clear fileInfo
      this.fileInfo = {}
      // mark redaction pane as viewing session
      this.viewingFile = false
      // clear currentlySelectedUUID
      this.$emit('clearSelected')
    },
    returnToSessionFeatures () {
      // mark redaction pane as viewing session
      this.viewingFile = false
      // use session features
      this.features = this.sessionFeatures
      // clear fileInfo
      this.fileInfo = {}
      // clear currentlySelectedUUID
      this.$emit('clearSelected')
    },
    updateRedactionPane (fileUUID) {
      axios.get(`http://127.0.0.1:8000/api/file/${fileUUID}/`)
        .then(response => {
          this.fileInfo = response.data
        })
        .catch(e => {
          this.errors.push(e)
        })
    },
    viewFile () {
      this.viewingFile = true
    },
    toggleViewingCleared () {
      this.viewingCleared = !this.viewingCleared
    }
  },
  computed: {
    featuresNotCleared () {
      return this.features.filter(a => a.cleared === false)
    },
    featureCount () {
      return this.features.length
    },
    featuresNotClearedCount () {
      return this.features.filter(a => a.cleared === false).length
    },
    featureTypeArray () {
      return [...new Set(this.features.map(feature => feature['feature_file']))]
    },
    featureTypeArrayNotCleared () {
      return [...new Set(this.featuresNotCleared.map(feature => feature['feature_file']))]
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
</style>
