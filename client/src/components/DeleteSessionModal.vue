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
        <button class="button is-danger" @click="deleteSession">Yes, delete</button>
        <button class="button" @click="close">Cancel</button>
      </footer>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

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
      axios.delete(`http://127.0.0.1:8000/api/session/${this.sessionUUID}/`)
        .then(response => {
          console.log(response)
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
