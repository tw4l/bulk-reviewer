<template>
  <div>
    <section class="section">
      <new-session-modal
        v-show="showNewSessionModal"
        @newSessionClose="showNewSessionModal = false"></new-session-modal>
      <div class="container">
        <h3 class="title is-3">Sessions</h3>
        <button class="button is-link" @click="showNewSessionModal = true">+ New Session</button>
        <br><br>
        <ul>
          <li v-for="session in sessions" :key="session.uuid">
            <div style="padding-bottom: 10px">
              <div class="columns">
                <div class="column">
                  <h5 class="title is-5">{{ session.name }}</h5>
                  <p class="subtitle is-6">{{ session.uuid }}</p>
                </div>
                <div class="column">
                  <router-link
                    :to="{ name: 'RedactionSession', params: { uuid: session.uuid }}"
                    v-if="session.processing_complete">
                    <button class="button is-info">Go to session</button>
                  </router-link>
                  <button class="button is-info" disabled v-else>
                    <font-awesome-icon icon="spinner" class="fa-spin"></font-awesome-icon>
                  </button>
                  <delete-modal-button
                    :sessionUUID="session.uuid"
                    :sessionName="session.name">
                  </delete-modal-button>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'
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
    }.bind(this), 3000)
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
    }
  }
}
</script>

<style>
</style>
