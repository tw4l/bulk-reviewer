<template>
  <div class="message">
    <div class="message-header">{{ featureType }} ({{ featureTypeCount }})    <button class="button" @click="toggleMessageBody">(show/hide)</button></div>
    <div class="message-body" v-show="showMessageBody" style="word-wrap: break-word;">
      <ul>
        <li v-for="f in filteredFeatureArray" :key="f.uuid">
          <p><strong>Feature: </strong> {{ f.feature }}</p>
          <p><strong>Context: </strong> {{ f.context }}</p>
          <br>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'feature-result',
  props: ['featureType', 'featureTypeCount', 'filteredFeatureArray'],
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
