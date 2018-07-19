<template>
<div class="padded">
  <h4 class="title is-4">Session: {{ sessionInfo.name }}</h4>
  <p class="subtitle is-6">{{ sessionInfo.uuid }}</p>
  <hr>
  <div class="columns">
    <div class="column padded">
      <h4 class="title is-4">Files</h4>
      <node-tree
        :label="fileTree.label"
        :nodes="fileTree.nodes"
        :currentlySelectedUUID="currentlySelectedUUID"
        :depth="0"
        :uuid="fileTree.uuid"
        :nodeIndex="0"
        :allocated="fileTree.allocated"
        :class="{ active: currentlySelectedUUID === fileTree.uuid }">
      </node-tree>
    </div>
    <div class="column padded">
      <redaction-pane
      :currentlySelectedUUID="currentlySelectedUUID"
      @clearSelected="clearCurrentlySelectedUUID"></redaction-pane>
    </div>
  </div>
</div>
</template>

<script>
import NodeTree from './NodeTree'
import RedactionPane from './RedactionPane'
import axios from 'axios'
import bus from '../bus'

export default {
  name: 'session',
  components: { NodeTree, RedactionPane },
  data () {
    return {
      sessionInfo: {},
      files: [],
      fileTree: {},
      features: [],
      errors: [],
      currentlySelectedUUID: ''
    }
  },
  created () {
    this.getData()

    // setInterval(function () {
    //   this.getData()
    // }.bind(this), 10000)
  },
  mounted () {
    bus.$on('viewFileFromBulkTable', this.updateCurrentlySelectedUUID)
    bus.$on('updateSelected', this.updateCurrentlySelectedUUID)
  },
  methods: {
    clearCurrentlySelectedUUID () {
      this.currentlySelectedUUID = ''
    },
    updateCurrentlySelectedUUID (newUUID) {
      this.currentlySelectedUUID = newUUID
    },
    getData () {
      // api calls to add data
      let uuid = this.$route.params.uuid
      axios.get(`http://127.0.0.1:8000/api/session/${uuid}/`)
        .then(response => {
          this.sessionInfo = response.data
        })
        .catch(e => {
          this.errors.push(e)
        })
      axios.get(`http://127.0.0.1:8000/api/session/${uuid}/files/`)
        .then(response => {
          this.files = response.data
          this.fileTree = this.convertPathsToTree(this.files)
        })
        .catch(e => {
          this.errors.push(e)
        })
      axios.get(`http://127.0.0.1:8000/api/session/${uuid}/features/`)
        .then(response => {
          this.features = response.data
        })
        .catch(e => {
          this.errors.push(e)
        })
    },
    // create fileTree from files JSON
    convertPathsToTree: function (files) {
      // Build the node structure
      const rootNode = {label: 'Session', nodes: []}

      for (let file of files) {
        let path = file['filepath']
        let uuid = file['uuid']
        let allocated = file['allocated']

        this.buildNodeRecursive(rootNode, path.split('/'), 0, uuid, allocated)
      }
      return rootNode
    },
    buildNodeRecursive: function (node, path, index, uuid, allocated) {
      if (index < path.length) {
        let item = path[index]
        let dir = node.nodes.find(node => node.label === item)
        if (!dir) {
          dir = {
            label: item,
            isDir: true,
            nodes: []
          }
          if (index === path.length - 1) {
            dir['uuid'] = uuid
            dir['isDir'] = false
            dir['allocated'] = allocated
          }
          node.nodes.push(dir)
        }
        this.buildNodeRecursive(dir, path, index + 1, uuid, allocated)
      }
    }
  }
}
</script>

<style>
.padded {
  margin: 10px;
}
</style>
