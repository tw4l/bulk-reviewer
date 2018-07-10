<template>
  <div class="modal is-active">
    <div class="modal-background" @click="close"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Create New Session</p>
        <button class="delete" aria-label="close" @click="close"></button>
      </header>
      <section class="modal-card-body">
        FORM HERE
      </section>
      <footer class="modal-card-foot">
        <button class="button is-success">Create</button>
        <button class="button" @click="close">Cancel</button>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'new-session-modal',
  methods: {
    close: function () {
      this.$emit('newSessionClose')
    }
  }
}
</script>

<style>
</style>
