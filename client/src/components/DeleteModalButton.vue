<template>
  <span>
    <delete-session-modal
      :sessionUUID="sessionUUID"
      :sessionName="sessionName"
      v-show="showDeleteSessionModal === true"
      @deleteSessionClose="showDeleteSessionModal = false">
    </delete-session-modal>
    <button
      class="button"
      @click="showDeleteSessionModal = true"
      ><font-awesome-icon icon="trash-alt"></font-awesome-icon></button>
  </span>
</template>

<script>
import DeleteSessionModal from '@/components/DeleteSessionModal'

export default {
  name: 'delete-modal-button',
  components: { DeleteSessionModal },
  props: [ 'sessionUUID', 'sessionName' ],
  data () {
    return {
      showDeleteSessionModal: false
    }
  }
}
</script>

<style>
</style>
