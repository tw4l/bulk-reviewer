<template>
  <div class="notification" style="max-width: 500px;">
    <button class="delete" @click="hideNotification"></button>
    {{ message }}
  </div>
</template>

<script>
export default {
  name: 'alert',
  props: [ 'message' ],
  methods: {
    hideNotification () {
      this.$emit('hideMessage')
    }
  }
}
</script>

<style>
</style>
