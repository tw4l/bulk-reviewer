<template>
  <section class="section">
    <h3 class="title is-3">Settings</h3>
    <div class="columns">
      <div class="column is-two-thirds">
        <h4 class="title is-4">Create new Bulk Extractor profile</h4>
        <new-config-form @refreshConfigList="getAllConfigs"></new-config-form>
      </div>
      <div class="column is-one-third">
        <h4 class="title is-4">Existing profiles</h4>
        <table class="table is-hoverable">
          <thead>
            <th>Name</th>
            <th>Remove</th>
          </thead>
          <tbody>
            <existing-config v-for="config in configs" :config="config" :key="config.uuid" @removeSession="removeSessionFromList"></existing-config>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import NewConfigForm from '@/components/NewConfigForm'
import ExistingConfig from '@/components/ExistingConfig'

export default {
  name: 'settings',
  components: { NewConfigForm, ExistingConfig },
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
    },
    removeSessionFromList (sessionUUID) {
      this.configs = this.configs.filter(function (obj) {
        return obj.uuid !== sessionUUID
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
