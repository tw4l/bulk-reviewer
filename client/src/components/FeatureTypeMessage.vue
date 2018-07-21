<template>
  <div class="message">
    <div class="message-header" @click="toggleMessageBody" style="align: left;">
        {{ featureTypeLabel }} ({{ count }})
      <font-awesome-icon icon="caret-down" v-if="showMessageBody"></font-awesome-icon>
      <font-awesome-icon icon="caret-right" v-else></font-awesome-icon>
    </div>
    <div class="message-body" v-show="showMessageBody" style="word-wrap: break-word;">
      <div v-if="viewingFile === true">
          <button class="button is-danger" @click="ignoreAllIndividualResults" style="margin-bottom: 15px; float: right;" v-show="count > 0">Ignore all</button>
          <individual-view-table
            :featureData="individualViewFilteredFeatureArray"
            v-show="count > 0">
          </individual-view-table>
      </div>
      <div v-else>
        <button class="button is-danger" @click="ignoreAllBulkResults" style="margin-bottom: 15px; float: right;" v-show="count > 0">Ignore all</button>
        <bulk-view-table
          :fileData="bulkViewFilteredFeatureArray"
          :features="features"
          :featureType="featureType"
          v-show="count > 0">
        </bulk-view-table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import IndividualViewTable from '@/components/IndividualViewTable'
import BulkViewTable from '@/components/BulkViewTable'

export default {
  name: 'feature-type-message',
  props: ['featureType', 'features', 'featuresNotCleared', 'viewingFile', 'viewingCleared'],
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
      axios.patch(`http://127.0.0.1:8000/api/batch_feature_update/`, { 'cleared': true, 'feature_list': featuresToUpdate }, { headers: { 'Content-Type': 'application/json' } })
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
      axios.patch(`http://127.0.0.1:8000/api/batch_feature_update/`, { 'cleared': true, 'feature_list': featuresToUpdate }, { headers: { 'Content-Type': 'application/json' } })
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
    filterByFeatureTypeNotCleared () {
      return this.featuresNotCleared.filter(feature => feature['feature_file'] === this.featureType)
    },
    individualViewFilteredFeatureArray () {
      let arr = this.filterByFeatureTypeNotCleared
      if (this.viewingCleared === true) {
        arr = this.filterByFeatureType
      }
      return arr
    },
    individualViewFilteredFeatureUUIDArray () {
      return this.individualViewFilteredFeatureArray.map(f => f.uuid)
    },
    bulkViewFilteredFeatureArray () {
      let arr = this.filterByFeatureTypeNotCleared
      if (this.viewingCleared === true) {
        arr = this.filterByFeatureType
      }
      let checkedUUIDs = []
      let returnArr = []
      // create array of unique files with counts
      arr.forEach(function (e) {
        if (!checkedUUIDs.includes(e.source_file)) {
          let filepath = e.source_filepath
          let fileUUID = e.source_file
          let count = arr.filter(function (obj) { return obj.source_file === fileUUID }).length
          checkedUUIDs.push(fileUUID)
          returnArr.push({'filepath': filepath, 'file_uuid': fileUUID, 'count': count})
        }
      })
      return returnArr
    },
    bulkViewFilteredFeatureUUIDArray () {
      return this.filterByFeatureTypeNotCleared.map(f => f.uuid)
    },
    count () {
      let count = this.featureTypeCountNotCleared
      if (this.viewingCleared === true) {
        count = this.featureTypeCount
      }
      return count
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
        case 'lightgrep.txt':
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
        default:
          return this.featureType
      }
    }
  }
}
</script>

<style>
</style>
