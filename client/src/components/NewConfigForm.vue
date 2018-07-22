<template>
  <div class="form">
    <!-- Name -->
    <div class="field">
      <label class="label">Name</label>
      <div class="control">
        <input class="input" type="text" name="name" placeholder="Name">
      </div>
    </div>
    <!-- Regex file upload -->
    <div class="field">
      <label class="label">Regular expressions file</label>
      <div class="control">
        <div class="file has-name">
          <label class="file-label">
            <input class="file-input" type="file" name="regex">
            <span class="file-cta">
              <span class="file-label">
                Choose a file
              </span>
            </span>
            <span class="file-name">
              None currently selected
            </span>
          </label>
        </div>
      </div>
    </div>
    <!-- Scanners -->
    <div class="field">
      <label class="label">Scanners</label>
      <div class="control">
        <label class="checkbox">
          <input type="checkbox" name="pii" default="true">
          PII (SSN, credit cards, phone, email)
        </label>
      </div>
      <div class="control">
        <label class="checkbox">
          <input type="checkbox" name="web">
          Web resources (URLs, domains, email/HTTP headers, HTTP logs)
        </label>
      </div>
      <div class="control">
        <label class="checkbox">
          <input type="checkbox" name="exif">
          EXIF and GPS metadata
        </label>
      </div>
    </div>
    <!-- SSN mode -->
    <div class="field">
      <div class="control">
        <label class="label">SSN matching mode</label>
        <div class="select">
          <select>
            <option>Default (no label required, dashes required)</option>
            <option>Strict (number must be prefaced with "SSN:", dashes required)</option>
            <option>Inclusive (no label required, no dashes required)</option>
          </select>
      </div>
    </div>
    </div>
    <!-- Buttons -->
    <div class="field is-grouped">
      <div class="control">
        <button class="button is-link">Submit</button>
      </div>
      <div class="control">
        <button class="button is-text">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'new-config-form'
}
</script>

<style>
</style>
