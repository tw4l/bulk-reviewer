<template>
  <div class="notification" style="max-width: 500px;">
    <button class="delete" @click="hideNotification"></button>
    <div v-if="checkIfArray === true">
      <ul>
        <li v-for="m in message" :key="m">- {{ m }}</li>
      </ul>
    </div>
    <div v-else>
      {{ message }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'alert',
  props: [ 'message' ],
  methods: {
    hideNotification: function () {
      this.$emit('hideMessage')
    }
  },
  computed: {
    checkIfArray: function () {
      return Array.isArray(this.message)
    }
  }
}
</script>

<style>
</style>
