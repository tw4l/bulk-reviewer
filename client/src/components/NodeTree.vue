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
      {{ label }}
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
      :class="{ active: currentlySelectedUUID === node.uuid }"
      @bus="bus"
    >
    </node-tree>
  </div>
</template>
<script>
export default {
  props: [ 'label', 'nodes', 'depth', 'currentlySelectedUUID', 'uuid', 'isDir', 'allocated' ],
  data () {
    return { showChildren: false }
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
