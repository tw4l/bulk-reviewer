// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faCaretDown, faCaretRight, faFolder, faFolderOpen, faFile, faTrashAlt, faSpinner, faLevelUpAlt, faTimes, faPen, faHdd, faCheck, faQuestionCircle, faUserSlash } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import VueClipboard from 'vue-clipboard2'
import VTooltip from 'v-tooltip'

// sass/css
require('./assets/sass/main.scss')

// use VueClipboard and VTooltip
Vue.use(VueClipboard)
Vue.use(VTooltip)

// register fontawesome icons
library.add(faCaretDown, faCaretRight, faFolder, faFolderOpen, faFile, faTrashAlt, faSpinner, faLevelUpAlt, faTimes, faPen, faHdd, faCheck, faQuestionCircle, faUserSlash)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
