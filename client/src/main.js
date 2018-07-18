// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import 'bulma/css/bulma.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faCaretDown, faCaretRight, faFolder, faFolderOpen, faFile, faTrashAlt, faSpinner, faLevelUpAlt, faBars, faCheck, faEyeSlash } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// register fontawesome icons
library.add(faCaretDown, faCaretRight, faFolder, faFolderOpen, faFile, faTrashAlt, faSpinner, faLevelUpAlt, faBars, faCheck, faEyeSlash)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
