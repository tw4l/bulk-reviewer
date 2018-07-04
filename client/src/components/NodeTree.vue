<template>
  <div class="node-tree" :style="indent">
    <span @click="toggleChildren">ICON: </span>
    <span @click="updateSelected">{{ label }}</span>
    <node-tree
      v-if="showChildren"
      v-for="node in nodes"
      :nodes="node.nodes"
      :label="node.label"
      :depth="depth + 1"
      :key="node.uuid"
      :currentlySelectedUUID="currentlySelectedUUID"
      :uuid="node.uuid"
      :class="{ active: currentlySelectedUUID === node.uuid }"
      @bus="bus"
    >
    </node-tree>
  </div>
</template>
<script>
export default {
  props: [ 'label', 'nodes', 'depth', 'currentlySelectedUUID', 'uuid' ],
  data () {
    return { showChildren: false }
  },
  name: 'node-tree',
  computed: {
    indent () {
      return { transform: `translate(${this.depth * 25}px)` }
    }
  },
  methods: {
    toggleChildren: function () {
      this.showChildren = !this.showChildren
    },
    bus: function (data) {
      this.$emit('bus', data)
    },
    updateSelected: function () {
      this.$emit('bus', this.uuid)
    }
  }
}
</script>
<style>
.active {
  background-color: #d3d3d3;
}
</style>
