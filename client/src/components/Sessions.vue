<template>
  <div>
    <section class="section">
      <div class="container">
        <h3 class="title is-3">Sessions</h3>
        <ul>
          <li v-for="session in sessions" :key="session.uuid">
            <div style="padding-bottom: 10px">
              <router-link :to="{ name: 'RedactionSession', params: { uuid: session.uuid }}"><h5 class="title is-5">{{ session.name }}</h5></router-link>
              <p class="subtitle is-6">{{ session.uuid }}</p>
            </div>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'sessions',
  data () {
    return {
      sessions: [],
      errors: []
    }
  },

  created () {
    axios.get(`http://127.0.0.1:8000/api/session`)
      .then(response => {
        this.sessions = response.data.results
      })
      .catch(e => {
        this.errors.push(e)
      })
  }
}
</script>

<style>
</style>
