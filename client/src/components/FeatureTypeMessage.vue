<template>
  <div class="message">
    <div class="message-header" @click="toggleMessageBody" style="align: left;" v-if="showMessageBody">
        (-) {{ featureTypeLabel }} (total: {{ featureTypeCount }}, confirmed sensitive: {{ featureTypeCountNotCleared }})
        <span></span>
      <font-awesome-icon icon="caret-down"></font-awesome-icon>
    </div>
    <div class="message-header" @click="toggleMessageBody" style="align: left;" v-else>
        (+) {{ featureTypeLabel }} (total: {{ featureTypeCount }}, confirmed sensitive: {{ featureTypeCountNotCleared }})
      <font-awesome-icon icon="caret-right"></font-awesome-icon>
    </div>
    <div class="message-body" v-show="showMessageBody" style="word-wrap: break-word; padding-bottom: 50px;">
      <div v-if="viewingFile === true">
        <div class="buttons" style="float: right; padding-bottom: 15px;">
          <button class="button is-info" @click="resetAllResults" v-tooltip="'Confirm all results as sensitive'">Confirm all</button>
          <button class="button" @click="ignoreAllIndividualResults" v-tooltip="'Dismiss all results as false positives'">Dismiss all</button>
        </div>
        <individual-view-table
          :featureData="filterByFeatureType"
          :showFileBrowser="showFileBrowser">
        </individual-view-table>
      </div>
      <div v-else>
         <div class="buttons" style="float: right; padding-bottom: 15px;">
          <button class="button is-info" @click="resetAllResults" v-tooltip="'Confirm all results as sensitive'">Confirm all</button>
          <button class="button" @click="ignoreAllBulkResults" v-tooltip="'Dismiss all results as false positives'">Dismiss all</button>
        </div>
        <bulk-view-table
          :fileData="bulkViewFilteredFeatureArray"
          :features="features"
          :featureType="featureType"
          :showFileBrowser="showFileBrowser"
          :critical="false">
        </bulk-view-table>
      </div>
    </div>
  </div>
</template>

<script>
import IndividualViewTable from '@/components/IndividualViewTable'
import BulkViewTable from '@/components/BulkViewTable'
import { HTTP } from '../api'

export default {
  name: 'feature-type-message',
  props: ['featureType', 'features', 'featuresNotCleared', 'viewingFile', 'showFileBrowser'],
  components: { IndividualViewTable, BulkViewTable },
  data () {
    return {
      showMessageBody: false
    }
  },
  methods: {
    toggleMessageBody: function () {
      this.showMessageBody = !this.showMessageBody
    },
    ignoreAllIndividualResults: function () {
      // Batch update all features in this file with correct type as cleared
      let featuresToUpdate = this.individualViewFilteredFeatureUUIDArray
      HTTP.patch(`batch_feature_update/`, { 'cleared': true, 'feature_list': featuresToUpdate }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
    },
    ignoreAllBulkResults: function () {
      // Batch update all features in this file with correct type as cleared
      let featuresToUpdate = this.bulkViewFilteredFeatureUUIDArray
      HTTP.patch(`batch_feature_update/`, { 'cleared': true, 'feature_list': featuresToUpdate }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
    },
    resetAllResults: function () {
      let featuresToUpdate = this.filterByFeatureTypeCleared
      HTTP.patch(`batch_feature_update/`, { 'cleared': false, 'feature_list': featuresToUpdate }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
    }
  },
  computed: {
    featureTypeCount: function () {
      return this.features.filter(feature => feature['feature_file'] === this.featureType).length
    },
    featureTypeCountNotCleared: function () {
      return this.featuresNotCleared.filter(feature => feature['feature_file'] === this.featureType).length
    },
    filterByFeatureType () {
      return this.features.filter(feature => feature['feature_file'] === this.featureType)
    },
    filterByFeatureTypeCleared () {
      return this.filterByFeatureType.filter(f => f['cleared'] === true).map(f => f.uuid)
    },
    filterByFeatureTypeNotCleared () {
      return this.featuresNotCleared.filter(feature => feature['feature_file'] === this.featureType)
    },
    individualViewFilteredFeatureUUIDArray () {
      return this.filterByFeatureType.map(f => f.uuid)
    },
    bulkViewFilteredFeatureArray () {
      let arr = this.filterByFeatureType
      let checkedUUIDs = []
      let returnArr = []
      // create array of unique files with counts
      arr.forEach(function (e) {
        if (!checkedUUIDs.includes(e.source_file)) {
          let filepath = e.source_filepath
          let fileUUID = e.source_file
          let count = arr.filter(function (obj) { return obj.source_file === fileUUID }).length
          let verified = e.source_file_verified
          checkedUUIDs.push(fileUUID)
          returnArr.push({ 'filepath': filepath, 'file_uuid': fileUUID, 'count': count, 'verified': verified })
        }
      })
      return returnArr
    },
    bulkViewFilteredFeatureUUIDArray () {
      return this.filterByFeatureTypeNotCleared.map(f => f.uuid)
    },
    featureTypeLabel () {
      switch (this.featureType) {
        case 'pii.txt':
          return 'Social Security Numbers'
        case 'ccn.txt':
          return 'Credit card numbers'
        case 'telephone.txt':
          return 'Phone numbers'
        case 'email.txt':
          return 'Email addresses'
        case 'find.txt':
          return 'Regular expressions'
        case 'url.txt':
          return 'URLs'
        case 'domain.txt':
          return 'Domains'
        case 'rfc822.txt':
          return 'Email/HTTP headers (RFC822)'
        case 'httplogs.txt':
          return 'HTTP logs'
        case 'gps.txt':
          return 'GPS data'
        case 'exif.txt':
          return 'EXIF metadata'
        case 'PERSON':
          return 'Person'
        case 'NORP':
          return 'Nationalities or religious or political groups'
        default:
          return this.featureType
      }
    }
  }
}
</script>

<style>
</style>
