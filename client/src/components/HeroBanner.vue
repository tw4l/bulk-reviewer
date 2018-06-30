<template>
	<div>
		<section class="hero is-info is-medium is-fullheight">
		  <div class="hero-body">
		    <div class="container">
		      <h1 class="title">
		        <slot name="primary"></slot>
		      </h1>
		      <h2 class="subtitle">
		        <slot name="secondary"></slot>
		      </h2>
		    </div>
		  </div>
		</section>
	</div>
</template>

<script>
	export default {

	}
</script>

<style>
</style>