<template>
  <div>
    <header class="app-header">
      <top-navbar/>
    </header>
    <main>
      <router-view/>
    </main>
  </div>
</template>

<script>
import TopNavbar from './components/TopNavbar'
export default {
  name: 'App',
  components: { TopNavbar }
}
</script>

<style>
</style>
