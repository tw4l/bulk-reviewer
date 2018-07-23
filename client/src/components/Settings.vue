<template>
  <section class="section">
    <h3 class="title is-3">Settings</h3>
    <div class="columns">
      <div class="column is-two-thirds padded">
        <h4 class="title is-4">Create new Bulk Extractor profile</h4>
        <new-config-form @refreshConfigList="getAllConfigs"></new-config-form>
      </div>
      <div class="column is-one-third padded">
        <h4 class="title is-4">Existing profiles</h4>
        <ul>
          <li v-for="config in configs" :key="config.uuid" style="margin-bottom: 15px;">
            - {{ config.name }} (edit) (delete)
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import NewConfigForm from '@/components/NewConfigForm'

export default {
  name: 'settings',
  components: { NewConfigForm },
  data () {
    return {
      configs: [],
      errors: []
    }
  },
  created () {
    this.getAllConfigs()
  },
  methods: {
    getAllConfigs () {
      axios.get(`http://127.0.0.1:8000/api/config`)
        .then(response => {
          this.configs = response.data
        })
        .catch(e => {
          this.errors.push(e)
        })
    }
  }
}
</script>

<style>
.padded {
  margin: 15px;
}
</style>
