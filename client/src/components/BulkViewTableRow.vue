<template>
  <tr>
    <td v-if="showFileBrowser">{{ filepathWithLineBreaks }}  <button class="button is-small" @click="viewFile">View</button></td>
    <td v-else>{{ fileInfo.filepath }}  <button class="button is-small" @click="viewFile">View</button></td>
    <td v-if="containsClearedFeatures">{{ featuresNotClearedCount }} <span style="color: #808080;">(of {{ fileInfo.count }})</span></td>
    <td v-else>{{ fileInfo.count }}</td>
    <td>
      <div class="buttons">
        <button class="button is-info" @click="markCleared" v-tooltip="'Confirm all results in this file as sensitive'"><font-awesome-icon icon="check"></font-awesome-icon></button>
        <button class="button" @click="markNotCleared" v-tooltip="'Dismiss all results in this file as false positives'"><font-awesome-icon icon="times"></font-awesome-icon></button>
      </div>
    </td>
  </tr>
</template>

<script>
import { HTTP } from '../api'
import bus from '../bus'

export default {
  name: 'bulk-view-table-row',
  props: [ 'fileInfo', 'features', 'featureType', 'showFileBrowser' ],
  methods: {
    viewFile: function () {
      bus.$emit('viewFileFromBulkTable', this.fileInfo.file_uuid)
    },
    markNotCleared: function () {
      // Batch update all features in this file with correct type as cleared
      let featuresToUpdate = this.featuresToUpdateUUIDArray
      HTTP.patch(`batch_feature_update/`, { 'cleared': true, 'feature_list': featuresToUpdate }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
    },
    markCleared: function () {
      // Batch update all features in this file with correct type as cleared
      let featuresToUpdate = this.featuresToUpdateUUIDArray
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
    filepathWithLineBreaks: function () {
      // Add a space tag every 60 chars for narrow display
      return this.fileInfo.filepath.replace(/(.{60})/g, '$1 ')
    },
    featuresInFileByType: function () {
      // filter features by source type and feature type
      return this.features.filter(feature => feature.source_file === this.fileInfo.file_uuid && feature.feature_file === this.featureType)
    },
    featuresToUpdateUUIDArray: function () {
      // return mapped array of UUIDs
      return this.featuresInFileByType.map(feature => feature.uuid)
    },
    containsClearedFeatures: function () {
      // return true if there are cleared features of this type in file
      let clearedFeaturesArray = this.featuresInFileByType.filter(feature => feature.cleared === true)
      return clearedFeaturesArray.length > 0
    },
    featuresNotClearedCount: function () {
      // return count of objects in featuresInFileByType where cleared === false
      return this.featuresInFileByType.filter(feature => feature.cleared === false).length
    }
  }
}
</script>

<style>
</style>
