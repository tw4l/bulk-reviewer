<template>
  <div class="message">
    <div class="message-header">
      <span @click="toggleMessageBody">{{ featureType }} ({{ featureTypeCount }})</span>
      <span style="align: right;">
        <button class="button is-danger"><font-awesome-icon icon="bars" class="fa-fw"></font-awesome-icon>Redact all</button>
        <button class="button is-success"><font-awesome-icon icon="check" class="fa-fw"></font-awesome-icon>Clear all</button>
        <button class="button" @click="toggleMessageBody">(+/-)</button>
      </span>
    </div>
    <div class="message-body" v-show="showMessageBody" style="word-wrap: break-word;">
      <individual-feature
        v-for="f in filteredFeatureArray"
        :key="f.uuid"
        :featureInfo="f"></individual-feature>
    </div>
  </div>
</template>

<script>
import IndividualFeature from '@/components/IndividualFeature'

export default {
  name: 'feature-result',
  props: ['featureType', 'featureTypeCount', 'filteredFeatureArray'],
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
  }
}
</script>

<style>
</style>
