<template>
  <div>
    <section class="hero is-info is-medium">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            {{ title }}
          </h1>
          <h2 class="subtitle">
            {{ subtitle }}
          </h2>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container is-fluid">
        <ul>
          <li><a href="/sessions">Sessions</a></li>
          <li><a href="/config">Bulk Extractor configuration</a></li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      title: 'Bulk Redactor',
      subtitle: 'Identify, review, and redact PII.'
    }
  }
}
</script>

<style>
</style>
