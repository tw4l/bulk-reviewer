<template>
  <div id="app">
    <hero-banner>
      <template slot="primary">Bulk Redactor</template>
      <template slot="secondary">Identify, review, and redact PII.</template>
    </hero-banner>
  </div>
</template>

<script>
import HeroBanner from './components/HeroBanner.vue';

export default {
  name: 'app',

  components: { HeroBanner },

  data () {
    return {

    }
  }
}
</script>

<style lang="scss">

</style>
