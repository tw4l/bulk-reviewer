<template>
  <div v-if="loading === true" class="loading">
    <font-awesome-icon icon="spinner" class="fa-spin"></font-awesome-icon>
  </div>
  <div v-else>
    <!-- Sticky context box (sticky to bottom) -->
    <div class="box sticky">
      <p v-if="fileInfo.filename"><strong>Currently viewing:</strong> {{ fileInfo.filename }}</p>
      <p v-else><strong>Currently viewing:</strong> All Session results</p>
    </div>
    <!-- View dismissed modal -->
    <view-dismissed-modal
      v-show="viewingDismissed"
      @viewDismissedClose="viewingDismissed = false"
      :featuresCleared="featuresCleared">
    </view-dismissed-modal>
    <!-- Context -->
    <div style="margin-bottom: 15px;" v-if="currentlySelectedUUID !== ''">
      <button class="button" @click="returnToSessionFeatures" v-tooltip="'Change context to view results for all files in source'"><font-awesome-icon icon="level-up-alt" class="fa-fw"></font-awesome-icon>Show all Session results</button>
    </div>
    <div style="margin-bottom: 15px;">
      <h4 class="title is-4" v-if="fileInfo.filepath">File: {{ filePathWithLineBreaks }} <button class="button is-small" v-clipboard:copy="fullFilepath">Copy path</button></h4>
      <h4 class="title is-4" v-else>All results</h4>
    </div>
    <!-- Metadata -->
    <div style="margin-bottom: 15px;">
      <p><strong>Total:</strong> {{ featureCount }}</p>
      <p><strong>Dismissed:</strong> {{ featuresClearedCount }} <span v-if="featuresClearedCount !== 0"><button class="button is-small" @click="toggleShowDismissed">View</button></span></p>
      <p><strong>Remaining:</strong> {{ featuresNotClearedCount }}</p>
      <div class="buttons">
        <button class="button" @click="unclearAll" v-if="(featuresClearedCount > 0) && (viewingFile === false)">Reset</button>
        <button class="button is-info" @click="unclearAll" v-else-if="(featuresClearedCount > 0)" v-tooltip="'Confirm all results as sensitive'">Confirm all</button>
        <button class="button" @click="clearAll" v-show="!allIgnored && (viewingFile === true)" v-tooltip="'Dismiss all results as false positive'">Dismiss all</button>
      </div>
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
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['ccn.txt'])"
        :key="'ccn.txt'"
        :featureType="'ccn.txt'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['telephone.txt'])"
        :key="'telephone.txt'"
        :featureType="'telephone.txt'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['email.txt'])"
        :key="'email.txt'"
        :featureType="'email.txt'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message>
    <h5 class="title is-5" v-if="featureFileInArray(['find.txt'])">User-supplied regular expressions</h5>
      <feature-type-message
        v-if="featureFileInArray(['find.txt'])"
        :key="'find.txt'"
        :featureType="'find.txt'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message>
    <h5
      class="title is-5"
      v-if="featureFileInArray(['url.txt', 'domain.txt', 'rfc822.txt', 'httplogs.txt'])">Web resources</h5>
      <feature-type-message
        v-if="featureFileInArray(['url.txt'])"
        :key="'url.txt'"
        :featureType="'url.txt'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['domain.txt'])"
        :key="'domain.txt'"
        :featureType="'domain.txt'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['rfc822.txt'])"
        :key="'rfc822.txt'"
        :featureType="'rfc822.txt'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['httplogs.txt'])"
        :key="'httplogs.txt'"
        :featureType="'httplogs.txt'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message>
    <h5 class="title is-5" v-if="featureFileInArray(['gps.txt', 'exif.txt'])">Geolocation and EXIF metadata</h5>
      <feature-type-message
        v-if="featureFileInArray(['gps.txt'])"
        :key="'gps.txt'"
        :featureType="'gps.txt'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['exif.txt'])"
        :key="'exif.txt'"
        :featureType="'exif.txt'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message>
  </div>
</template>

<script>
import { HTTP } from '../api'
import bus from '../bus'
import ReconnectingWebsocket from 'reconnectingwebsocket'
import FeatureTypeMessage from '@/components/FeatureTypeMessage'
import ViewDismissedModal from '@/components/ViewDismissedModal'

export default {
  name: 'redaction-pane',
  props: [ 'sessionInfo', 'currentlySelectedUUID', 'showFileBrowser' ],
  components: { FeatureTypeMessage, ViewDismissedModal },
  data () {
    return {
      fileInfo: {},
      sessionFeatures: [],
      features: [],
      errors: [],
      messagesOpen: false,
      loading: true,
      viewingFile: false,
      viewingDismissed: false
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
      // update features
      for (let i = 0, numFeatures = self.features.length; i < numFeatures; i++) {
        if (self.features[i].uuid === featureToUpdateUUID) {
          self.features[i].cleared = featureToUpdateCleared
          self.features[i].note = featureToUpdateNote
          break
        }
      }
      // update sessionFeatures
      for (let i = 0, numFeatures = self.sessionFeatures.length; i < numFeatures; i++) {
        if (self.sessionFeatures[i].uuid === featureToUpdateUUID) {
          self.sessionFeatures[i].cleared = featureToUpdateCleared
          self.sessionFeatures[i].note = featureToUpdateNote
          break
        }
      }
    }

    // Listen for returnToSessionFeatures from RedactionSession
    bus.$on('returnToSessionFeatures', this.returnToSessionFeatures)
  },
  watch: {
    currentlySelectedUUID: function (newUUID, oldUUID) {
      if (newUUID !== '') {
        // mark redaction pane as viewing single file
        this.viewingFile = true
        // update data shown to user
        HTTP.get(`file/${newUUID}/`)
          .then(response => {
            this.fileInfo = response.data
          })
          .catch(e => {
            this.errors.push(e)
          })
        HTTP.get(`file/${newUUID}/features`)
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
    clearAll () {
      // Batch update all features in this file as cleared
      let featuresToUpdate = this.featuresNotClearedUUIDs
      HTTP.patch(`batch_feature_update/`, { 'cleared': true, 'feature_list': featuresToUpdate }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
    },
    unclearAll () {
      // Batch update all features in this file as not cleared
      let featuresToUpdate = this.featuresClearedUUIDs
      HTTP.patch(`batch_feature_update/`, { 'cleared': false, 'feature_list': featuresToUpdate }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
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
      let apiCall = this.$route.path + '/features/'
      HTTP.get(`${apiCall}`)
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
      HTTP.get(`file/${fileUUID}/`)
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
    toggleShowDismissed () {
      this.viewingDismissed = !this.viewingDismissed
    }
  },
  computed: {
    featuresNotCleared () {
      return this.features.filter(a => a.cleared === false)
    },
    featuresNotClearedUUIDs () {
      return this.featuresNotCleared.map(f => f.uuid)
    },
    featuresCleared () {
      return this.features.filter(a => a.cleared === true)
    },
    featuresClearedUUIDs () {
      return this.featuresCleared.map(f => f.uuid)
    },
    featuresClearedCount () {
      return this.featuresCleared.length
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
    allIgnored () {
      return this.featuresNotCleared.length === 0
    },
    someIgnored () {
      return this.featuresCleared > 0
    },
    filePathWithLineBreaks () {
      // Add <br> tag every 100 chars for narrow display
      return this.fileInfo.filepath.replace(/(.{100})/g, '$1<br>')
    },
    fullFilepath () {
      var path = require('path')
      return "'" + path.join(this.sessionInfo.source_path, this.fileInfo.filepath) + "'"
    }
  }
}
</script>

<style>
.sticky{
  position: fixed;
  bottom: 0;
  right: 0;
  margin-right: 10px;
  overflow: hidden;
  z-index: 100;
}
.loading {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
