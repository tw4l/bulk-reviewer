<template>
<div class="padded">
  <h4 class="title is-4">Session: {{ sessionInfo.name }}</h4>
  <p class="subtitle is-6">{{ sessionInfo.uuid }}</p>
  <hr>
  <div class="columns">
    <div class="column is-one-third">
      <node-tree
        :label="fileTree.label"
        :nodes="fileTree.nodes"
        :currentlySelectedUUID="currentlySelectedUUID"
        :depth="0"
        :uuid="fileTree.uuid"
        :allocated="fileTree.allocated"
        :class="{ active: currentlySelectedUUID === fileTree.uuid }"
        @bus="bus"></node-tree>
      </div>
    <div class="column is-two-thirds">
      <div>
        Redaction review and actions here
      </div>
    </div>
  </div>
</div>
</template>

<script>
import NodeTree from './NodeTree'
import axios from 'axios'

export default {
  name: 'session',
  components: { NodeTree },
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
  mounted () {

  },
  created () {
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

  methods: {
    // update currentlySelectedUUID from recursive node-tree components
    bus (newUUID) {
      this.currentlySelectedUUID = newUUID
    },
    // create fileTree from files JSON
    convertPathsToTree: function (files) {
      // Build the node structure
      const rootNode = {label: 'Session', nodes: []}

      for (let file of files) {
        let path = file['filepath']
        let uuid = file['uuid']
        let redacted = file['redact_file']
        let cleared = file['cleared']
        let allocated = file['allocated']

        this.buildNodeRecursive(rootNode, path.split('/'), 0, uuid, redacted, cleared, allocated)
      }
      return rootNode
    },

    buildNodeRecursive: function (node, path, index, uuid, redacted, cleared, allocated) {
      if (index < path.length) {
        let item = path[index]
        let dir = node.nodes.find(node => node.label === item)
        if (!dir) {
          const uuidv4 = require('uuid/v4')
          let uuidString = uuidv4().toString()
          dir = {
            label: item,
            isDir: true,
            nodes: [],
            uuid: uuidString
          }
          if (index === path.length - 1) {
            dir['uuid'] = uuid
            dir['isDir'] = false
            dir['redacted'] = redacted
            dir['cleared'] = cleared
            dir['allocated'] = allocated
          }
          node.nodes.push(dir)
        }
        this.buildNodeRecursive(dir, path, index + 1, uuid, redacted, cleared, allocated)
      }
    }
  }
}
</script>

<style>
.padded {
  margin: 20px;
}
</style>
