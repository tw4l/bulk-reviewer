<template>
  <div class="modal is-active">
    <div class="modal-background" @click="close"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Are you sure you want to delete this session?</p>
        <button class="delete" aria-label="close" @click="close"></button>
      </header>
      <section class="modal-card-body">
        <h6 class="title is-5">{{ this.sessionName }}</h6>
        <p class="subtitle is-6">{{ this.sessionUUID }}</p>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-primary" @click="deleteSession">Yes, delete</button>
        <button class="button" @click="close">Cancel</button>
      </footer>
    </div>
  </div>
</template>

<script>
import bus from '../bus'
import { HTTP } from '../api'

export default {
  name: 'delete-session-modal',
  props: [ 'sessionUUID', 'sessionName', 'active' ],
  methods: {
    close: function () {
      this.$emit('deleteSessionClose')
    },
    updateSessions: function () {
      this.$emit('updateSessionsList')
    },
    deleteSession: function () {
      this.close()
      HTTP.delete(`session/${this.sessionUUID}/`)
        .then(response => {
          console.log(response)
          bus.$emit('deleteSession', this.sessionUUID)
        })
        .catch(e => {
          this.errors.push(e)
        })
    }
  }
}
</script>

<style>
</style>
