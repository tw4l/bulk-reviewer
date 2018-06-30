<template>
	<div>
		<ul>
			<li v-for="session in sessions">
				<div style="padding-bottom: 10px">
					<h5 class="title is-5">{{ session.name }}</h5>
					<p class="subtitle">{{ session.uuid }}</p>
				</div>
			</li>
		</ul>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			sessions: {},
			errors: {}
		}
	},

	created() {
		axios.get(`http://127.0.0.1:8000/api/session`)
		.then(response => {
			this.sessions = response.data.results
		})
		.catch(e => {
			this.errors.push(e)
		})
	}
}
</script>

<style>
</style>