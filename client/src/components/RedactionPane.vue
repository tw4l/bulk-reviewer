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
    </div>
    <!-- Metadata -->
    <div style="margin-bottom: 15px;">
      <p v-if="allClear"><strong>Status:</strong> Clear (no results to review)</p>
      <p v-else><strong>Status:</strong> Under review</p>
      <p><strong>Results:</strong> {{ featureCount }}</p>
    </div>
    <!-- Sctions -->
    <div v-show="!allClear">
      <button class="button is-success" @click="markFileCleared" v-if="fileInfo.uuid && (fileInfo.cleared === false)">Mark all results reviewed</button>
      <button class="button" @click="markFileNotCleared" v-else-if="fileInfo.uuid && (fileInfo.cleared === true)">Undo reviewed</button>
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
        :viewingFile="viewingFile">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['ccn.txt'])"
        :key="'ccn.txt'"
        :featureType="'ccn.txt'"
        :featureTypeCount="featureTypeCount('ccn.txt')"
        :filteredFeatureArray="filterByFeatureType('ccn.txt')"
        :viewingFile="viewingFile">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['telephone.txt'])"
        :key="'telephone.txt'"
        :featureType="'telephone.txt'"
        :featureTypeCount="featureTypeCount('telephone.txt')"
        :filteredFeatureArray="filterByFeatureType('telephone.txt')"
        :viewingFile="viewingFile">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['email.txt'])"
        :key="'email.txt'"
        :featureType="'email.txt'"
        :featureTypeCount="featureTypeCount('email.txt')"
        :filteredFeatureArray="filterByFeatureType('email.txt')"
        :viewingFile="viewingFile">
      </feature-type-message>
    <h5 class="title is-5" v-if="featureFileInArray(['lightgrep.txt'])">User-supplied regular expressions</h5>
      <feature-type-message
        v-if="featureFileInArray(['lightgrep.txt'])"
        :key="'lightgrep.txt'"
        :featureType="'lightgrep.txt'"
        :featureTypeCount="featureTypeCount('lightgrep.txt')"
        :filteredFeatureArray="filterByFeatureType('lightgrep.txt')"
        :viewingFile="viewingFile">
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
        :viewingFile="viewingFile">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['domain.txt'])"
        :key="'domain.txt'"
        :featureType="'domain.txt'"
        :featureTypeCount="featureTypeCount('domain.txt')"
        :filteredFeatureArray="filterByFeatureType('domain.txt')"
        :viewingFile="viewingFile">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['rfc822.txt'])"
        :key="'rfc822.txt'"
        :featureType="'rfc822.txt'"
        :featureTypeCount="featureTypeCount('rfc822.txt')"
        :filteredFeatureArray="filterByFeatureType('rfc822.txt')"
        :viewingFile="viewingFile">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['httplogs.txt'])"
        :key="'httplogs.txt'"
        :featureType="'httplogs.txt'"
        :featureTypeCount="featureTypeCount('httplogs.txt')"
        :filteredFeatureArray="filterByFeatureType('httplogs.txt')"
        :viewingFile="viewingFile">
      </feature-type-message>
    <h5 class="title is-5" v-if="featureFileInArray(['gps.txt', 'exif.txt'])">Geolocation and EXIF metadata</h5>
      <feature-type-message
        v-if="featureFileInArray(['gps.txt'])"
        :key="'gps.txt'"
        :featureType="'gps.txt'"
        :featureTypeCount="featureTypeCount('gps.txt')"
        :filteredFeatureArray="filterByFeatureType('gps.txt')"
        :viewingFile="viewingFile">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['exif.txt'])"
        :key="'exif.txt'"
        :featureType="'exif.txt'"
        :featureTypeCount="featureTypeCount('exif.txt')"
        :filteredFeatureArray="filterByFeatureType('exif.txt')"
        :viewingFile="viewingFile">
      </feature-type-message>
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
      sessionFeatures: [],
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
    filterByFeatureType (featureFile) {
      return this.features.filter(feature => feature['feature_file'] === featureFile)
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
    markFileCleared () {
      let fileUUID = this.fileInfo.uuid
      axios.patch(`http://127.0.0.1:8000/api/file/${fileUUID}/`, { 'cleared': true }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
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
          this.updateRedactionPane(fileUUID)
        })
        .catch(e => {
          this.errors.push(e)
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
    },
    viewFile () {
      this.viewingFile = true
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
</style>
