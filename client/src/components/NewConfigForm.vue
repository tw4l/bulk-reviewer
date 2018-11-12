<template>
  <div>
    <!-- Form validation errors -->
    <alert :message="errorMessage" @hideMessage="hideErrorAlertMessage" v-show="errorMessage" class="is-danger"></alert>
    <!-- Form upload success -->
    <alert :message="successMessage" @hideMessage="hideSuccessAlertMessage" v-show="showSuccess" class="is-success"></alert>
    <form enctype="multipart/form-data" id="new-config-form">
      <!-- Name -->
      <div class="field">
        <label class="label">Name</label>
        <div class="control input-container">
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
              <span class="file-name gray">{{ regexFileName }}</span>
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
            PII (SSNs, credit cards, phone numbers, email addresses)
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
          <button class="button is-primary" @click.prevent="processForm" :disabled="formSubmit">Save profile</button>
        </div>
        <div class="control">
          <button class="button is-text" @click.prevent="clearForm">Cancel</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import Alert from '@/components/Alert'

export default {
  name: 'new-config-form',
  components: { Alert },
  data () {
    return {
      formSubmit: false,
      name: '',
      fileToUpload: null,
      regexFileName: 'None currently selected',
      pii: true,
      web: false,
      exif: false,
      ssnMode: 1,
      errorMessage: '',
      successMessage: 'Success!',
      showSuccess: false
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

      // form validation for name input
      if (!this.name) {
        this.errorMessage = 'Name value is required.'
        this.formSubmit = false
        return
      } else if (this.name.length > 100) {
        this.errorMessage = 'Name must be less than 100 characters.'
        this.formSubmit = false
        return
      }

      // set data
      let data = new FormData()
      data.append('name', this.name)
      if (this.fileToUpload) {
        data.append('regex_file', this.fileToUpload, this.fileToUpload.name)
      }
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
          this.showSuccess = true
          this.$emit('refreshConfigList')
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
      this.errorMessage = ''
      this.showSuccess = false
    },
    hideErrorAlertMessage: function () {
      this.errorMessage = ''
    },
    hideSuccessAlertMessage: function () {
      this.showSuccess = false
    }
  }
}
</script>

<style>
.gray {
  color: #808080;
}
.input-container {
     max-width: 500px;
}
.input-container.input,textarea {
     width:100%;
     display:block
}
</style>
