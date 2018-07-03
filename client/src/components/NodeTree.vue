<template>
  <div class="node-tree">
    <div :style="indent" @click="toggleChildren">{{ label }}</div>
    <node-tree
      v-if="showChildren"
      v-for="node in nodes"
      :nodes="node.nodes"
      :label="node.label"
      :depth="depth + 1"
      :key="node.uuid"
    >
    </node-tree>
  </div>
</template>
<script>
export default {
  props: [ 'label', 'nodes', 'depth' ],
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
    toggleChildren () {
      this.showChildren = !this.showChildren
    }
  }
}
</script>
<style>
</style>
