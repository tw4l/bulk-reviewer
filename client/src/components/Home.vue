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
    <ul>
      <a href="/sessions"><li>Sessions</li></a>
      <a href="/config"><li>Bulk Extractor configuration</li></a>
    </ul>
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
