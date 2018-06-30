import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import BulkextConfig from '@/components/BulkextConfig'
import Sessions from '@/components/Sessions'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/config',
      name: 'BulkextConfig',
      component: BulkextConfig
    },
    {
      path: '/sessions',
      name: 'Sessions',
      component: Sessions
    }
  ]
})
