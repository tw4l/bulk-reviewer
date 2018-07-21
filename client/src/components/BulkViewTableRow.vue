<template>
  <tr>
    <td>{{ filepathWithLineBreaks }}  <button class="button is-small" @click="viewFile">View</button></td>
    <td>{{ fileInfo.count }}</td>
    <td>
      <button class="button is-danger" @click="markCleared"><font-awesome-icon icon="eye-slash"></font-awesome-icon></button>
    </td>
  </tr>
</template>

<script>
import axios from 'axios'
import bus from '../bus'

export default {
  name: 'bulk-view-table-row',
  props: [ 'fileInfo', 'features', 'featureType' ],
  methods: {
    viewFile: function () {
      bus.$emit('viewFileFromBulkTable', this.fileInfo.file_uuid)
    },
    markCleared: function () {
      // Batch update all features in this file with correct type as cleared
      let featuresToUpdate = this.featuresToUpdateUUIDArray
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
    filepathWithLineBreaks: function () {
      // Add a space tag every 60 chars for narrow display
      return this.fileInfo.filepath.replace(/(.{60})/g, '$1 ')
    },
    featuresToUpdateUUIDArray: function () {
      let featuresInFileByType = this.features.filter(feature => feature.source_file === this.fileInfo.file_uuid && feature.feature_file === this.featureType)
      return featuresInFileByType.map(feature => feature.uuid)
    }
  }
}
</script>

<style>
</style>
