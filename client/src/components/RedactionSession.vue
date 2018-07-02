<template>
  <div class="columns">
    <div class="column">
       Tree View Here
    </div>
    <div class="column">
      Redaction review and actions here
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'session',
  data () {
    return {
      files: [],
      fileTree: {},
      features: [],
      errors: []
    }
  },

  created () {
    let uuid = this.$route.params.uuid
    axios.get(`http://127.0.0.1:8000/api/session/${uuid}/files/`)
      .then(response => {
        this.files = response.data.results
        this.fileTree = this.convertPathsToTree(this.files)
      })
      .catch(e => {
        this.errors.push(e)
      })
    axios.get(`http://127.0.0.1:8000/api/session/${uuid}/features/`)
      .then(response => {
        this.features = response.data.results
      })
      .catch(e => {
        this.errors.push(e)
      })
  },

  methods: {
    convertPathsToTree: function (files) {
      // Build the node structure
      const rootNode = {name: 'root', children: []}

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
        let dir = node.children.find(child => child.name === item)
        if (!dir) {
          dir = {
            name: item,
            isDir: true,
            children: []
          }
          if (index === path.length - 1) {
            dir['uuid'] = uuid
            dir['isDir'] = false
            dir['redacted'] = redacted
            dir['cleared'] = cleared
            dir['allocated'] = allocated
          }
          node.children.push(dir)
        }
        this.buildNodeRecursive(dir, path, index + 1, uuid, redacted, cleared, allocated)
      }
    }
  }
}
</script>

<style>
</style>
