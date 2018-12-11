<template>
  <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <router-link class="navbar-item" to="/">
        <h4 class="title is-4" style="color: white">Bulk Reviewer</h4>
      </router-link>
      <div class="navbar-burger" @click="showNav = !showNav" :class="{ 'is-active': showNav }">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
    <div class="navbar-menu" :class="{ 'is-active': showNav }">
      <div class="navbar-end">
        <router-link class="navbar-item" to="/">
          <span>Sessions</span>
        </router-link>
        <router-link class="navbar-item" to="/settings">
          <span>Settings</span>
        </router-link>
        <router-link class="navbar-item" to="/users">
          <span>Users</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'TopNavbar',
  data () {
    return {
      showNav: false
    }
  }
}
</script>

<style>
.newSessionButton {
  color: white !important;
}
.newSessionButton:hover {
  color: #178B63 !important;
}
</style>
