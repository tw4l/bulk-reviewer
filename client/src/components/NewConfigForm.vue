<template>
  <form enctype="multipart/form-data" id="new-config-form">
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
            <input class="file-input" type="file" name="regex" v-on:change="onFileChange">
            <span class="file-cta">
              <span class="file-label">
                Choose a file
              </span>
            </span>
            <span class="file-name">{{ regexFileName }}</span>
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
        <button class="button is-link" @click.prevent="processForm" :disabled="formSubmit">Submit</button>
      </div>
      <div class="control">
        <button class="button is-text" @click.prevent="clearForm">Cancel</button>
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
      fileToUpload: null,
      regexFileName: 'None currently selected',
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
    onFileChange: function (e) {
      let files = e.target.files || e.dataTransfer.files
      if (!files.length) {
        console.log('No files uploaded')
      } else {
        this.fileToUpload = files[0]
        this.regexFileName = files[0].name
      }
    },
    processForm: function () {
      // disable submit button
      this.formSubmit = true

      // set data
      let data = new FormData()
      data.append('name', this.name)
      data.append('regex_file', this.fileToUpload, this.fileToUpload.name)
      data.append('ssn_mode', parseInt(this.ssnMode))
      data.append('pii_scanners', this.pii)
      data.append('web_scanners', this.web)
      data.append('exif_gps_scanners', this.exif)

      // set config
      const config = {
        headers: { 'content-type': 'multipart/form-data' }
      }

      // POST form
      axios.post(`http://127.0.0.1:8000/api/config/add/`, data, config)
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
      // re-enable submit button
      this.formSubmit = false
    },
    clearForm: function () {
      this.formSubmit = false
      this.name = ''
      this.fileToUpload = null
      this.regexFileName = 'None currently selected'
      this.pii = true
      this.web = false
      this.exif = false
      this.ssnMode = 1
    }
  }
}
</script>

<style>
</style>
