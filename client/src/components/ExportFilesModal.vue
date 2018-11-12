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
        <alert :message="processingMessage" @hideMessage="hideProcessingAlertMessage" v-show="showProcessing"></alert>
        <!-- Form -->
        <form id="export-files-form">
          <p>Create an export containing: a directory of clean files; a directory of files containing confirmed sensitive information to redact, restrict, or remove; and a directory of CSV reports.</p>
        </form>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-info" disabled v-if="formSubmit == true">
          <font-awesome-icon icon="spinner" class="fa-spin"></font-awesome-icon>
        </button>
        <button class="button is-success" :disabled="formSubmit" @click.prevent="processForm" v-else>Create</button>
        <button class="button" @click.prevent="clearForm">Clear</button>
      </footer>
    </div>
</div>
</template>

<script>
import Alert from '@/components/Alert'
import { HTTP } from '../api'

export default {
  name: 'export-files-modal',
  props: ['sessionInfo'],
  components: { Alert },
  data () {
    return {
      formSubmit: false,
      processingComplete: false,
      processingFailure: false,
      errorMessages: [],
      showProcessing: false,
      processingMessage: 'Request successfully submitted. Bulk Reviewer will alert you when export is ready.'
    }
  },
  methods: {
    close: function () {
      this.clearForm()
      this.$emit('close')
    },
    processForm: function () {
      // disable submit button
      this.formSubmit = true

      // set data
      let data = new FormData()
      data.append('be_session', this.sessionInfo.uuid)

      // POST form
      HTTP.post(`redacted_set/add/`, data)
        .then(response => {
          this.requestUUID = response.data.uuid
          this.showProcessing = true
          this.formSubmit = false
        })
        .catch(e => {
          console.log(e)
        })
    },
    clearForm: function () {
      this.formSubmit = false
      this.showProcessing = false
      this.processingComplete = false
      this.processingFailure = false
      this.errorMessages = []
    },
    hideErrorAlertMessage: function () {
      this.errorMessages = []
    },
    hideProcessingAlertMessage: function () {
      this.showProcessing = false
    }
  }
}
</script>

<style>
</style>
