<template>
  <div class="modal is-active">
    <div class="modal-background" @click="close"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Export files</p>
        <button class="delete" aria-label="close" @click="close">X</button>
      </header>
      <section class="modal-card-body">
        <!-- Form validation errors -->
        <alert :message="errorMessages" @hideMessage="hideErrorAlertMessage" v-show="errorMessages.length > 0" class="is-danger"></alert>
        <!-- Form upload success -->
        <alert :message="successMessage" @hideMessage="hideSuccessAlertMessage" v-show="showSuccess" class="is-success"></alert>
        <!-- Form -->
        <form id="export-files-form">
          <!-- Name -->
          <div class="field">
            <label class="label">Name</label>
            <div class="control input-container">
              <input class="input" type="text" name="name" v-model="name" placeholder="Name">
            </div>
          </div>
        </form>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-success" :disabled="formSubmit" @click.prevent="processForm">Create</button>
        <button class="button" @click.prevent="clearForm">Clear</button>
      </footer>
    </div>
</div>
</template>

<script>
import axios from 'axios'
import Alert from '@/components/Alert'

export default {
  name: 'export-files-modal',
  props: ['sessionInfo'],
  components: { Alert },
  data () {
    return {
      name: '',
      formSubmit: false,
      errorMessages: [],
      successMessage: 'Success!',
      showSuccess: false
    }
  },
  methods: {
    close: function () {
      this.$emit('close')
    },
    processForm: function () {
      // disable submit button
      this.formSubmit = true

      // form validation
      let formValidation = true
      if (!this.name) {
        this.errorMessages.push('Name value is required.')
        formValidation = false
      }
      if (this.name.length > 100) {
        this.errorMessages.push('Name must be less than 100 characters.')
        formValidation = false
      }
      if (formValidation === false) {
        this.formSubmit = false
        return
      }

      // set data
      let data = new FormData()
      data.append('name', this.name)
      data.append('be_session', this.sessionInfo.uuid)

      // POST form
      axios.post(`http://127.0.0.1:8000/api/redacted_set/add/`, data)
        .then(response => {
          console.log(response)
          this.showSuccess = true
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
    },
    hideErrorAlertMessage: function () {
      this.errorMessages = []
    },
    hideSuccessAlertMessage: function () {
      this.showSuccess = false
    }
  }
}
</script>

<style>
</style>
