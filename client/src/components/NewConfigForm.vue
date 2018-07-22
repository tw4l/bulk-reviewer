<template>
  <form id="new-config-form" @submit.prevent="processForm">
    <!-- Name -->
    <div class="field">
      <label class="label">Name</label>
      <div class="control">
        <input class="input" type="text" name="name" v-model="name" placeholder="Name">
      </div>
    </div>
    <!-- Regex file upload -->
    <div class="field">
      <label class="label">Regular expressions file</label>
      <div class="control">
        <div class="file has-name">
          <label class="file-label">
            <input class="file-input" type="file" name="regex">
            <span class="file-cta">
              <span class="file-label">
                Choose a file
              </span>
            </span>
            <span class="file-name">
              None currently selected
            </span>
          </label>
        </div>
      </div>
    </div>
    <!-- Scanners -->
    <div class="field">
      <label class="label">Scanners</label>
      <div class="control">
        <label class="checkbox">
          <input type="checkbox" name="pii" default="true" v-model="pii">
          PII (SSN, credit cards, phone, email)
        </label>
      </div>
      <div class="control">
        <label class="checkbox">
          <input type="checkbox" name="web" v-model="web">
          Web resources (URLs, domains, email/HTTP headers, HTTP logs)
        </label>
      </div>
      <div class="control">
        <label class="checkbox">
          <input type="checkbox" name="exif" v-model="exif">
          EXIF and GPS metadata
        </label>
      </div>
    </div>
    <!-- SSN mode -->
    <div class="field">
      <div class="control">
        <label class="label">SSN matching mode</label>
        <div class="select">
          <select name="ssn" v-model="ssnMode">
            <option value="0">Strict ("SSN" label required, dashes required)</option>
            <option value="1">Default (dashes only required)</option>
            <option value="2">Permissive (no label or dashes required)</option>
          </select>
      </div>
    </div>
    </div>
    <!-- Buttons -->
    <div class="field is-grouped">
      <div class="control">
        <button class="button is-link" :disabled="formSubmit">Submit</button>
      </div>
      <div class="control">
        <button class="button is-text">Cancel</button>
      </div>
    </div>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  name: 'new-config-form',
  data () {
    return {
      formSubmit: false,
      name: '',
      regexFile: '',
      pii: true,
      web: false,
      exif: false,
      ssnMode: 1
    }
  },
  mounted () {
    // form event listener
    const newConfigForm = document.getElementById('new-config-form')
    newConfigForm.addEventListener('submit', this.processNewConfigForm)
  },
  methods: {
    processForm: function (e) {
      // disable submit button
      this.formSubmit = true
      // POST form
      axios.post(`http://127.0.0.1:8000/api/config/add/`, {
        name: this.name,
        // regex_file
        ssn_mode: parseInt(this.ssnMode),
        pii_scanners: this.pii,
        web_scanners: this.web,
        exif_gps_scanners: this.exif
      })
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
      // re-enable submit button
      this.formSubmit = false
    }
  }
}
</script>

<style>
</style>
