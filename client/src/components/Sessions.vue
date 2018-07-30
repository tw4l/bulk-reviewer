<template>
  <section class="section">
    <new-session-modal
      v-show="showNewSessionModal"
      @newSessionClose="showNewSessionModal = false"></new-session-modal>
    <div class="container">
      <h3 class="title is-3">Sessions</h3>
      <button class="button is-primary is-outlined is-rounded" @click="showNewSessionModal = true">+ New Session</button>
      <br><br>
      <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth" v-if="sessions.length > 0">
        <thead>
          <tr>
            <th>Name</th>
            <th>UUID</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="session in sessions" :key="session.uuid">
            <td><strong>{{ session.name }}</strong></td>
            <td>{{ session.uuid }}</td>
            <td>
              <router-link
                :to="{ name: 'RedactionSession', params: { uuid: session.uuid }}"
                v-if="session.processing_complete">
                <button class="button is-info">Go to session</button>
              </router-link>
              <button class="button is-danger" disabled v-else-if="session.processing_failure">Error!</button>
              <button class="button is-info" disabled v-else>
                <font-awesome-icon icon="spinner" class="fa-spin"></font-awesome-icon>
              </button>
              <delete-modal-button
                :sessionUUID="session.uuid"
                :sessionName="session.name">
              </delete-modal-button>
            </td>
          </tr>
        </tbody>
      </table>
      <h5 class="title is-5" v-else>Create a new session to get started!</h5>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import bus from '../bus'
import NewSessionModal from '@/components/NewSessionModal'
import DeleteModalButton from '@/components/DeleteModalButton'

export default {
  name: 'sessions',
  components: { NewSessionModal, DeleteModalButton },
  data () {
    return {
      sessions: [],
      errors: [],
      showNewSessionModal: false
    }
  },
  created () {
    this.getSessions()

    setInterval(function () {
      this.getSessions()
    }.bind(this), 10000)

    // delete session on receipt of message
    // from DeleteSessionModal
    bus.$on('deleteSession', this.removeSession)
  },
  methods: {
    getSessions () {
      axios.get(`http://127.0.0.1:8000/api/session`)
        .then(response => {
          this.sessions = response.data
        })
        .catch(e => {
          this.errors.push(e)
        })
    },
    removeSession (sessionToDeleteUUID) {
      this.sessions = this.sessions.filter(session => session.uuid !== sessionToDeleteUUID)
    }
  }
}
</script>

<style>
</style>
