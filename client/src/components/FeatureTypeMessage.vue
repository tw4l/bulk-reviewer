<template>
  <div class="message">
    <div class="message-header" @click="toggleMessageBody" style="align: left;">
      <font-awesome-icon icon="caret-down" v-if="showMessageBody"></font-awesome-icon>
      <font-awesome-icon icon="caret-right" v-else></font-awesome-icon>
      {{ featureType }} ({{ featureTypeCount }})
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
    }
  }
}
</script>

<style>
</style>
