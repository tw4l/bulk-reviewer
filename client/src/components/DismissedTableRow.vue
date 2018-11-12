<template>
  <tr>
    <td>{{ featureInfo.source_filepath }}</td>
    <td>{{ featureTypeLabel }}</td>
    <td>{{ unescapedFeature }}</td>
    <td>{{ unescapedContext }}</td>
    <td><button class="button" @click="markNotCleared"><font-awesome-icon icon="times"></font-awesome-icon></button></td>
  </tr>
</template>

<script>
import { HTTP } from '../api'

export default {
  name: 'dismissed-table-row',
  props: [ 'featureInfo' ],
  methods: {
    markCleared: function () {
      alert('Not yet implemented!')
    },
    markNotCleared: function () {
      let featureUUID = this.featureInfo.uuid
      HTTP.patch(`feature/${featureUUID}/`, { 'cleared': false }, { headers: { 'Content-Type': 'application/json' } })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
    }
  },
  computed: {
    unescapedFeature: function () {
      return this.featureInfo.feature.replace(/\\x[a-fA-F0-9]{2}/g, String.fromCharCode('$1'))
    },
    unescapedContext: function () {
      return this.featureInfo.context.replace(/\\x[a-fA-F0-9]{2}/g, String.fromCharCode('$1'))
    },
    featureTypeLabel () {
      switch (this.featureInfo.feature_file) {
        case 'pii.txt':
          return 'SSN'
        case 'ccn.txt':
          return 'Credit card'
        case 'telephone.txt':
          return 'Phone'
        case 'email.txt':
          return 'Email'
        case 'lightgrep.txt':
          return 'Regex'
        case 'url.txt':
          return 'URL'
        case 'domain.txt':
          return 'Domain'
        case 'rfc822.txt':
          return 'RFC822'
        case 'httplogs.txt':
          return 'HTTP log'
        case 'gps.txt':
          return 'GPS'
        case 'exif.txt':
          return 'EXIF'
        default:
          return this.featureInfo.feature_file
      }
    }
  }
}
</script>

<style>
</style>
