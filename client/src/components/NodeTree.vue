<template>
  <div class="node-tree" :style="indent">
    <!-- expanding carat for sessions and directories -->
    <span>
      <span class="icon is-small" @click="toggleChildren" v-if="openable">
        <font-awesome-icon icon="caret-down" v-if="showChildren"></font-awesome-icon>
        <font-awesome-icon icon="caret-right" v-else></font-awesome-icon>
      </span>
      <span class="icon is-small" v-else></span>
    </span>
    <!-- icons and labels -->
    <span @click="updateSelected">
      <span class="icon is-small" v-if="openable">
        <font-awesome-icon icon="folder-open" v-if="showChildren"></font-awesome-icon>
        <font-awesome-icon icon="folder" v-else></font-awesome-icon>
      </span>
      <span class="icon is-small" v-else>
        <font-awesome-icon icon="file" v-if="allocated"></font-awesome-icon>
        <font-awesome-icon icon="trash-alt" v-else></font-awesome-icon>
      </span>
      <span :class="{ active: currentlySelectedUUID === uuid }">
      {{ label }}
      </span>
    </span>
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
      :allocated="node.allocated"
      :cleared="node.cleared">
    </node-tree>
  </div>
</template>

<script>
import bus from '../bus'

export default {
  props: [ 'label', 'nodes', 'depth', 'currentlySelectedUUID', 'uuid', 'isDir', 'allocated', 'cleared' ],
  data () {
    return {
      showChildren: false,
      errors: []
    }
  },
  name: 'node-tree',
  computed: {
    indent () {
      return { transform: `translate(${this.depth + 25}px)` }
    },
    zeroDepth () {
      return this.depth === 0
    },
    openable () {
      return this.isDir || this.label === 'Session'
    }
  },
  methods: {
    toggleChildren: function () {
      this.showChildren = !this.showChildren
    },
    updateSelected: function () {
      bus.$emit('updateSelected', this.uuid)
    }
  }
}
</script>

<style>
.active {
  background-color: #d3d3d3;
}
</style>
