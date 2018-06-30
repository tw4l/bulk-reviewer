<template>
  <div id="app">
    <hero-banner>
      <template slot="primary">Bulk Redactor</template>
      <template slot="secondary">Identify, review, and redact PII.</template>
    </hero-banner>
    <div class="container" style="padding-top: 10px;">
      <h3 class="title is-3">Sessions</h3>
      <session-list></session-list>
    </div>
  </div>
</template>

<script>
import HeroBanner from './components/HeroBanner.vue';
import SessionList from './components/SessionList.vue';

export default {
  name: 'app',

  components: { HeroBanner, SessionList },

  data () {
    return {

    }
  }
}
</script>

<style lang="scss">
</style>
