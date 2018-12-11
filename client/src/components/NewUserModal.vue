<template>
  <div class="modal is-active">
    <div class="modal-background" @click="close"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Create New User</p>
        <button class="delete" aria-label="close" @click="close"></button>
      </header>
      <section class="modal-card-body">
        <!-- Form validation errors -->
        <alert :message="errorMessages" @hideMessage="hideErrorAlertMessage" v-show="errorMessages.length > 0" class="is-danger"></alert>
        <!-- Form upload success -->
        <alert :message="successMessage" @hideMessage="hideSuccessAlertMessage" v-show="showSuccess" class="is-success"></alert>
        <!-- Form -->
        <form id="new-user-form">
          <!-- Username -->
          <div class="field">
            <label class="label">Username</label>
            <div class="control input-container">
              <input class="input" type="text" name="username" v-model="username">
            </div>
          </div>
          <!-- Email -->
          <div class="field">
            <label class="label">Email</label>
            <div class="control input-container">
              <input class="input" type="email" name="email" v-model="email" placeholder="user@org.com">
            </div>
          </div>
          <!-- Password -->
          <div class="field">
            <label class="label">Password</label>
            <div class="control input-container">
              <input class="input" type="password" name="password" v-model="password">
            </div>
          </div>
          <!-- Password verification -->
          <div class="field">
            <label class="label">Password again (for verification)</label>
            <div class="control input-container">
              <input class="input" type="password" name="passwordVerification" v-model="passwordVerification">
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
import { HTTP } from '../api'
import Alert from '@/components/Alert'

export default {
  name: 'new-user-modal',
  components: { Alert },
  data () {
    return {
      formSubmit: false,
      errorMessages: [],
      username: '',
      email: '',
      password: '',
      passwordVerification: '',
      successMessage: 'Success!',
      showSuccess: false
    }
  },
  methods: {
    processForm: function () {
      // disable submit button
      this.formSubmit = true

      // form validation
      let formValidation = true
      if (!this.username) {
        this.errorMessages.push('Username is required.')
        formValidation = false
      }
      if (this.username.length > 150) {
        this.errorMessages.push('Username must be less than 150 characters.')
        formValidation = false
      }
      if (!this.email) {
        this.errorMessages.push('Email is required.')
        formValidation = false
      }
      if (this.password !== this.passwordVerification) {
        this.errorMessages.push('Passwords don\'t match.')
        formValidation = false
      }
      if (formValidation === false) {
        this.formSubmit = false
        return
      }

      // set data
      let data = new FormData()
      data.append('username', this.username)
      data.append('email', this.email)
      data.append('password', this.password)

      // POST form
      HTTP.post(`user/add/`, data)
        .then(response => {
          console.log(response)
          this.showSuccess = true
          this.$emit('newUser')
        })
        .catch(e => {
          this.errorMessages.push(e.response.data)
        })

      // re-enable submit button
      this.formSubmit = false
    },
    clearForm: function () {
      this.formSubmit = false
      this.username = ''
      this.email = ''
      this.password = ''
      this.passwordVerification = ''
      this.errorMessages = []
      this.showSuccess = false
    },
    hideErrorAlertMessage: function () {
      this.errorMessages = []
    },
    hideSuccessAlertMessage: function () {
      this.showSuccess = false
    },
    close: function () {
      this.$emit('newUserClose')
    }
  }
}
</script>

<style>
</style>
