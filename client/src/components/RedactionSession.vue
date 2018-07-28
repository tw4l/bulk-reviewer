<template>
<div class="padded">
  <!-- Header -->
  <div class="columns">
    <div class="column padded">
      <h4 class="title is-4">Session: {{ sessionInfo.name }}</h4>
      <p class="subtitle is-6" style="margin-bottom: 0px;">
        {{ sessionInfo.source_path }}
        <font-awesome-icon icon="hdd" v-if="sessionInfo.disk_image === true"></font-awesome-icon>
        <font-awesome-icon icon="folder" v-else></font-awesome-icon>
      </p>
      <button class="button is-primary is-outlined" @click="toggleShowFileBrowser" style="margin-top: 10px;" v-if="showFileBrowser" >Hide file browser</button>
      <button class="button is-primary is-outlined" @click="toggleShowFileBrowser" style="margin-top: 10px;" v-else>Show file browser</button>
    </div>
    <div class="column padded">
      <h5 class="title is-5">Happy with current selection?</h5>
      <button class="button is-primary is-outlined" @click="downloadReports">Download CSV reports</button>
      <button class="button is-primary" @click="exportFiles">Export files</button>
    </div>
  </div>
  <hr>
  <!-- Review -->
  <div>
    <div class="columns is-centered">
      <div class="column" v-if="showFileBrowser">
        <h3 class="title is-3">Review</h3>
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
      <div class="column">
        <redaction-pane
        :currentlySelectedUUID="currentlySelectedUUID"
        @clearSelected="clearCurrentlySelectedUUID"
        :showFileBrowser="showFileBrowser"></redaction-pane>
      </div>
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
      errors: [],
      currentlySelectedUUID: '',
      showFileBrowser: true
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
    },
    toggleShowFileBrowser: function () {
      this.showFileBrowser = !this.showFileBrowser
    },
    downloadReports: function () {
      alert('Not yet implemented!')
    },
    exportFiles: function () {
      alert('Not yet implemented!')
    }
  }
}
</script>

<style>
.padded {
  margin-top: 10px;
  margin-left: 10px;
  margin-right: 10px;
}
</style>
