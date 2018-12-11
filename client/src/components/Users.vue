<template>
  <section class="section">
    <h3 class="title is-3">Users</h3>
    <!-- New User modal -->
    <new-user-modal
      v-show="showNewUserModal"
      @newUser="getAllUsers"
      @newUserClose="showNewUserModal = false">
    </new-user-modal>
    <!-- Add user button -->
    <button class="button is-primary" @click="toggleNewUserModal" style="margin-bottom: 15px;">Add user</button>
    <!-- Users table -->
    <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in paginatedUsers" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>
            <div class="buttons">
              <button class="button">Edit</button>
              <button class="button is-danger" v-tooltip="'Deactivate user'"><font-awesome-icon icon="user-slash"></font-awesome-icon></button>
            </div>
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
  </section>
</template>

<script>
import { HTTP } from '../api'
import NewUserModal from '@/components/NewUserModal'

export default {
  name: 'users',
  components: { NewUserModal },
  data () {
    return {
      users: [],
      errors: [],
      showNewUserModal: false,
      startIndex: 0,
      pageCount: 10
    }
  },
  created () {
    this.getAllUsers()
  },
  methods: {
    getAllUsers () {
      HTTP.get('user/')
        .then(response => {
          this.users = response.data
        })
        .catch(e => {
          this.errors.push(e)
        })
    },
    resetStartIndex () {
      this.startIndex = 0
    },
    incrementStartIndex () {
      this.startIndex += this.pageCount
    },
    decrementStartIndex () {
      this.startIndex -= this.pageCount
    },
    toggleNewUserModal () {
      this.showNewUserModal = !this.showNewUserModal
    }
  },
  computed: {
    paginatedUsers () {
      return this.users.slice(this.startIndex, this.startIndex + this.pageCount)
    },
    numberOfPages () {
      return Math.ceil(this.users.length / this.pageCount)
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
