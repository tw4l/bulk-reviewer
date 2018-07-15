<template>
  <div class="message">
    <div class="message-header" @click="toggleMessageBody" style="align: left;">
      <font-awesome-icon icon="caret-down" v-if="showMessageBody"></font-awesome-icon>
      <font-awesome-icon icon="caret-right" v-else></font-awesome-icon>
      {{ featureTypeLabel }} ({{ featureTypeCount }})
    </div>
    <div class="message-body" v-show="showMessageBody" style="word-wrap: break-word;">
      <individual-feature
        v-for="f in filteredFeatureArray"
        :key="f.uuid"
        :featureInfo="f"
        :viewingFile="viewingFile">
      </individual-feature>
    </div>
  </div>
</template>

<script>
// import axios from 'axios'
import IndividualFeature from '@/components/IndividualFeature'

export default {
  name: 'feature-result',
  props: ['featureType', 'featureTypeCount', 'filteredFeatureArray', 'viewingFile'],
  components: { IndividualFeature },
  data () {
    return {
      showMessageBody: false
    }
  },
  methods: {
    toggleMessageBody: function () {
      this.showMessageBody = !this.showMessageBody
    }
  },
  computed: {
    filteredFeatureUUIDArray () {
      return this.filteredFeatureArray.map(a => a.uuid)
    },
    featureTypeLabel () {
      switch (this.featureType) {
        case 'pii.txt':
          return 'Security Security #s'
        case 'ccn.txt':
          return 'Credit card #s'
        case 'telephone.txt':
          return 'Phone #s'
        case 'email.txt':
          return 'Email addresses'
        case 'lightgrep.txt':
          return 'User-supplied terms'
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
