// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faCaretDown, faCaretRight, faFolder, faFolderOpen, faFile, faTrashAlt, faSpinner, faLevelUpAlt, faEyeSlash, faPen, faHdd } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import VueClipboard from 'vue-clipboard2'

// sass/css
require('./assets/sass/main.scss')

// use VueClipboard
Vue.use(VueClipboard)

// register fontawesome icons
library.add(faCaretDown, faCaretRight, faFolder, faFolderOpen, faFile, faTrashAlt, faSpinner, faLevelUpAlt, faEyeSlash, faPen, faHdd)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
