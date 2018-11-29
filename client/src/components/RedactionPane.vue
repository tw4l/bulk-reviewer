<template>
  <div v-if="loading === true" class="loading">
    <font-awesome-icon icon="spinner" class="fa-spin"></font-awesome-icon>
  </div>
  <div v-else>
    <!-- Sticky context box (sticky to bottom) -->
    <div class="box sticky" v-if="viewingContext === true">
      <div v-if="fileInfo.filename">
        <p><strong>Currently viewing:</strong> {{ fileInfo.filename }}</p>
        <button class="button is-success" @click="returnToSessionFeatures" v-tooltip="'Return context to all files in Session'">Show all Session results</button>
        <button class="is-small"
          @click="toggleContextMenu"
          v-tooltip="'Hide context menu'"
          style="float: right;">
          x
        </button>
      </div>
      <div v-else>
        <p><strong>Currently viewing:</strong> All Session results</p>
       <button class="is-small"
          @click="toggleContextMenu"
          v-tooltip="'Hide context menu'"
          style="float: right;">
          x
        </button>
      </div>
    </div>
    <div class="box sticky" v-else>
      <button class="is-small"
        @click="toggleContextMenu"
        v-tooltip="'Expand context menu'">
        +
      </button>
    </div>
    <!-- View dismissed modal -->
    <view-dismissed-modal
      v-show="viewingDismissed"
      @viewDismissedClose="viewingDismissed = false"
      :featuresCleared="featuresCleared">
    </view-dismissed-modal>
    <!-- Context -->
    <div style="margin-bottom: 15px;">
      <h4 class="title is-4" v-if="fileInfo.filepath">File: {{ filePathWithLineBreaks }} <button class="button is-small" v-clipboard:copy="fullFilepath" v-tooltip="'Copy this file\'s full filepath to the clipboard'">Copy path</button></h4>
      <h4 class="title is-4" v-else>All results</h4>
    </div>
    <!-- Feature counts -->
    <div style="margin-bottom: 15px;">
      <p><strong>Total results:</strong> {{ featureCount }}</p>
      <p><strong>Confirmed sensitive:</strong> {{ featuresNotClearedCount }}</p>
      <p><strong>Dismissed:</strong> {{ featuresClearedCount }} <span v-if="featuresClearedCount !== 0"><button class="button is-small" @click="toggleShowDismissed" v-tooltip="'Review results dismissed as false positives'">View</button></span></p>
    </div>
    <!-- Action buttons -->
    <div class="buttons">
      <button class="button" @click="unclearAll" v-if="(featuresClearedCount > 0) && (viewingFile === false)" v-tooltip="'Reset session to original state'">Reset</button>
      <button class="button is-info" @click="unclearAll" v-else-if="(featuresClearedCount > 0)" v-tooltip="'Confirm all results as sensitive'">Confirm all</button>
      <button class="button" @click="clearAll" v-show="!allIgnored && (viewingFile === true)" v-tooltip="'Dismiss all results as false positive'">Dismiss all</button>
    </div>
    <hr>
    <!-- Features grouped by type -->
    <h4
      class="title is-4"
      v-if="featureFileInArray(['pii.txt', 'ccn.txt'])"
      style="margin-bottom: 15px;">
      Critical
      <font-awesome-icon icon="question-circle" v-tooltip="'Critical results are considered high risk and are set to be removed by default. Please review the results and dismiss any false positives you find.'"></font-awesome-icon>
    </h4>
      <feature-type-message-critical
        v-if="featureFileInArray(['pii.txt'])"
        :key="'pii.txt'"
        :featureType="'pii.txt'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message-critical>
      <feature-type-message-critical
        v-if="featureFileInArray(['ccn.txt'])"
        :key="'ccn.txt'"
        :featureType="'ccn.txt'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message-critical>
    <h4
      class="title is-4"
      v-if="featureFileInArray(['telephone.txt', 'email.txt', 'find.txt', 'url.txt', 'domain.txt', 'rfc822.txt', 'httplogs.txt', 'gps.txt', 'exif.txt', 'PERSON', 'NORP'])"
      style="margin-bottom: 15px;">
    To review
    <font-awesome-icon icon="question-circle" v-tooltip="'Non-critical results are not set to be removed by default. Please review the results and mark any sensitive results you find for removal with the Confirm button.'"></font-awesome-icon>
    </h4>
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
      <feature-type-message
        v-if="featureFileInArray(['find.txt'])"
        :key="'find.txt'"
        :featureType="'find.txt'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message>
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
      <feature-type-message
        v-if="featureFileInArray(['PERSON'])"
        :key="'PERSON'"
        :featureType="'PERSON'"
        :features="features"
        :featuresNotCleared="featuresNotCleared"
        :viewingFile="viewingFile"
        :showFileBrowser="showFileBrowser">
      </feature-type-message>
      <feature-type-message
        v-if="featureFileInArray(['NORP'])"
        :key="'NORP'"
        :featureType="'NORP'"
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
import FeatureTypeMessageCritical from '@/components/FeatureTypeMessageCritical'
import ViewDismissedModal from '@/components/ViewDismissedModal'

export default {
  name: 'redaction-pane',
  props: [ 'sessionInfo', 'currentlySelectedUUID', 'showFileBrowser' ],
  components: { FeatureTypeMessage, FeatureTypeMessageCritical, ViewDismissedModal },
  data () {
    return {
      fileInfo: {},
      sessionFeatures: [],
      features: [],
      errors: [],
      messagesOpen: false,
      loading: true,
      viewingFile: false,
      viewingDismissed: false,
      viewingContext: true
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
      let featuresIndex = self.features.findIndex(x => x.uuid === featureToUpdateUUID)
      if (featuresIndex !== -1) {
        try {
          self.features[featuresIndex].cleared = featureToUpdateCleared
          self.features[featuresIndex].note = featureToUpdateNote
        } catch (error) {
          console.log(error)
        }
      }
      // update sessionFeatures
      let sessionFeaturesIndex = self.sessionFeatures.findIndex(x => x.uuid === featureToUpdateUUID)
      if (sessionFeaturesIndex !== -1) {
        try {
          self.sessionFeatures[sessionFeaturesIndex].cleared = featureToUpdateCleared
          self.sessionFeatures[sessionFeaturesIndex].note = featureToUpdateNote
        } catch (error) {
          console.log(error)
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
    },
    toggleContextMenu () {
      this.viewingContext = !this.viewingContext
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
