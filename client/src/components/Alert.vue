<template>
  <div class="notification">
    <button class="delete" show="showNotification" @click="hideNotification"></button>
    {{ message }}
  </div>
</template>

<script>
export default {
  name: 'alert',
  props: [ 'message', 'showMessage' ],
  methods: {
    hideNotification () {
      this.$emit('hideMessage')
    }
  }
}
</script>

<style>
</style>
