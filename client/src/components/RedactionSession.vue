<template>
<div class="padded">
  <!-- Header -->
  <div class="columns">
    <div class="column padded">
      <h4 class="title is-4">Session: {{ sessionInfo.name }}</h4>
      <p><strong>Source:</strong> {{ sessionInfo.source_path }}</p>
      <p><strong>Source type:</strong> {{ sourceType }}</p>
      <div v-if="redactionView === false">
        <button class="button" @click="toggleShowFileBrowser" style="margin-top: 10px;" v-if="showFileBrowser" >Hide file browser</button>
        <button class="button" @click="toggleShowFileBrowser" style="margin-top: 10px;" v-else>Show file browser</button>
      </div>
    </div>
    <div class="column padded">
      <h5 class="title is-5" v-if="redactionView === false">Happy with current selection?</h5>
      <h5 class="title is-5" v-else>Want to make changes to current selection?</h5>
      <div v-if="redactionView === false">
         <button class="button is-primary" @click="toggleRedactionView">Move on to Reporting and Removal</button>
      </div>
      <div v-else>
        <button class="button is-primary is-outlined" @click="toggleRedactionView">Return to Review</button>
      </div>
    </div>
  </div>
  <hr>
  <!-- Redaction -->
  <div class="padded" v-if="redactionView === true">
    <h3 class="title is-3">Reporting and Removal</h3>
    <h4 class="title is-4">Reporting</h4>
    <button class="button is-primary is-outlined">Download results CSV</button>
    <br><br>
    <h4 class="title is-4">Redaction</h4>
    <ul>
      <li>- Remove files</li>
      <li>- Redact bytes from disk image</li>
      <li>- Use manual redaction workflow tracker</li>
    </ul>
  </div>
  <!-- Review -->
  <div v-else>
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
      <div class="column" :class="{ 'is-four-fifths': !showFileBrowser }">
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
      features: [],
      errors: [],
      currentlySelectedUUID: '',
      redactionView: false,
      showFileBrowser: false
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
    },
    toggleRedactionView: function () {
      this.redactionView = !this.redactionView
    },
    toggleShowFileBrowser: function () {
      this.showFileBrowser = !this.showFileBrowser
    }
  },
  computed: {
    sourceType: function () {
      return this.sessionInfo.disk_image === true ? 'Disk image' : 'Directory'
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
