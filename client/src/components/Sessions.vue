<template>
  <section class="section">
    <new-session-modal
      v-show="showNewSessionModal"
      @newSessionClose="showNewSessionModal = false"></new-session-modal>
    <div class="container">
      <h3 class="title is-3">Sessions</h3>
      <button class="button is-primary is-outlined is-rounded" @click="showNewSessionModal = true">+ New Session</button>
      <br><br>
      <div v-if="sessions.length > 0">
        <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
          <thead>
            <tr>
              <th>Name</th>
              <th>Details</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="session in paginatedSessions" :key="session.uuid">
              <td>
                <strong>{{ session.name }}</strong>
              </td>
              <td>
                <p>
                  <em>Source:</em> {{ session.source_path }}
                  <span v-if="session.disk_image">
                     <font-awesome-icon icon="hdd" v-tooltip="'Source type: Disk image'"></font-awesome-icon>
                  </span>
                  <span v-else>
                    <font-awesome-icon icon="folder" v-tooltip="'Source type: Directory'"></font-awesome-icon>
                  </span>
                </p>
                <p><em>Profile:</em> {{ session.be_config }}</p>
                <p v-if="session.named_entity_extraction"><em>NLP Enabled:</em> True</p>
                <p v-else><em>NLP Enabled:</em> False</p>
                <p><em>UUID:</em> {{ session.uuid }}</p>
              </td>
              <td>
                <span v-if="session.processing_complete">Complete</span>
                <span v-else-if="session.processing_failure">Failed. See logs for details.</span>
                <span v-else>Currently processing. This may take some time.</span>
              </td>
              <td>
                <span v-if="session.processing_complete">
                  <router-link
                    :to="{ name: 'RedactionSession', params: { uuid: session.uuid }}">
                    <button
                      class="button is-info"
                      v-tooltip="'Go to session'">
                      <font-awesome-icon icon="sign-in-alt" class="fa"></font-awesome-icon>
                    </button>
                  </router-link>
                </span>
                <span v-else-if="session.processing_failure">
                  <button class="button is-danger"
                          v-tooltip="'Error'"
                          disabled>
                    <font-awesome-icon icon="times"></font-awesome-icon>
                  </button>
                </span>
                <span v-else>
                  <button class="button is-info"
                          disabled>
                    <font-awesome-icon icon="spinner" class="fa-spin"></font-awesome-icon>
                  </button>
                </span>
                <delete-modal-button
                  :sessionUUID="session.uuid"
                  :sessionName="session.name"
                  v-tooltip="'Delete'">
                </delete-modal-button>
              </td>
            </tr>
          </tbody>
        </table>
        <!-- Pagination -->
        <div class="buttons has-addons">
          <button class="button" @click="decrementStartIndex" :disabled="firstPage">Previous</button>
          <button class="button" disabled>{{ currentPage }} of {{ numberOfPages }}</button>
          <button class="button" @click="incrementStartIndex" :disabled="lastPage">Next</button>
        </div>
      </div>
      <div v-else>
        <h5 class="title is-5">Create a new session to get started!</h5>
      </div>
    </div>
  </section>
</template>

<script>
import { HTTP, WebSocketURLBase } from '../api'
import bus from '../bus'
import ReconnectingWebsocket from 'reconnectingwebsocket'
import NewSessionModal from '@/components/NewSessionModal'
import DeleteModalButton from '@/components/DeleteModalButton'

export default {
  name: 'sessions',
  components: { NewSessionModal, DeleteModalButton },
  data () {
    return {
      sessions: [],
      errors: [],
      showNewSessionModal: false,
      startIndex: 0,
      pageCount: 10
    }
  },
  created () {
    // get session array on initialization
    this.getSessions()
  },
  mounted () {
    // Update sessions whenever Session model post_save signal sends ws
    let wsSessionsURL = WebSocketURLBase + 'sessions/'
    let ws = new ReconnectingWebsocket(wsSessionsURL)
    let self = this
    ws.onmessage = function (message) {
      self.getSessions()
    }
    // Remove session from list on receipt of event from bus
    bus.$on('deleteSession', this.removeSession)
  },
  methods: {
    getSessions: function () {
      HTTP.get(`session/`)
        .then(response => {
          this.sessions = response.data
        })
        .catch(e => {
          this.errors.push(e)
        })
    },
    removeSession: function (sessionToDeleteUUID) {
      this.sessions = this.sessions.filter(session => session.uuid !== sessionToDeleteUUID)
    },
    resetStartIndex () {
      this.startIndex = 0
    },
    incrementStartIndex () {
      this.startIndex += this.pageCount
    },
    decrementStartIndex () {
      this.startIndex -= this.pageCount
    }
  },
  computed: {
    sessionsUUIDs: function () {
      return this.sessions.map(session => session.uuid)
    },
    paginatedSessions () {
      return this.sessions.slice(this.startIndex, this.startIndex + this.pageCount)
    },
    numberOfPages () {
      return Math.ceil(this.sessions.length / this.pageCount)
    },
    currentPage () {
      return this.startIndex === 0 ? 1 : Math.ceil(this.startIndex / this.pageCount) + 1
    },
    moreThanOnePage () {
      return this.numberOfPages > 1
    },
    firstPage () {
      return this.currentPage === 1
    },
    lastPage () {
      return this.currentPage >= this.numberOfPages
    }
  }
}
</script>

<style>
</style>
