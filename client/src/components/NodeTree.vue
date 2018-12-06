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
      <span :class="{ active: currentlySelectedUUID === uuid, nofeatures: featureCount === 0 }">
      {{ label }} <span v-if="featureCount === 0" v-tooltip="'No results found'"><font-awesome-icon icon="check"></font-awesome-icon></span> <span v-if="verified === true" v-tooltip="'This file is verified (all results reviewed)'" style="color: green;"><font-awesome-icon icon="check"></font-awesome-icon></span>
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
      :verified="node.verified"
      :featureCount="node.featureCount"
      :fileTreeReady="fileTreeReady">
    </node-tree>
  </div>
</template>

<script>
import bus from '../bus'

export default {
  props: [ 'label', 'nodes', 'depth', 'currentlySelectedUUID', 'uuid', 'isDir', 'allocated', 'verified', 'featureCount', 'fileTreeReady' ],
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
  },
  watch: {
    fileTreeReady: function (newValue, oldValue) {
      if (newValue === true && this.label === 'Session') {
        this.showChildren = true
      }
    }
  }
}
</script>

<style>
.active {
  background-color: #d3d3d3;
}
.nofeatures {
  color: #808080;
}
</style>
