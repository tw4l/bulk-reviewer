<template>
  <div class="node-tree" :style="indent">
    <span @click="toggleChildren" v-if="zeroDepth">SESSION: </span>
    <span @click="toggleChildren" v-else-if="isDir">FOLDER: </span>
    <span @click="toggleChildren" v-else>FILE: </span>
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
      :isDir="node.isDir"
      :class="{ active: currentlySelectedUUID === node.uuid }"
      @bus="bus"
    >
    </node-tree>
  </div>
</template>
<script>
export default {
  props: [ 'label', 'nodes', 'depth', 'currentlySelectedUUID', 'uuid', 'isDir' ],
  data () {
    return { showChildren: false }
  },
  name: 'node-tree',
  computed: {
    indent () {
      return { transform: `translate(${this.depth * 25}px)` }
    },
    zeroDepth () {
      return this.depth === 0
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
