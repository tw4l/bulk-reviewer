import Vue from 'vue'
import Router from 'vue-router'
import Settings from '@/components/Settings'
import Sessions from '@/components/Sessions'
import RedactionSession from '@/components/RedactionSession'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/settings',
      name: 'Settings',
      component: Settings
    },
    {
      path: '/',
      name: 'Sessions',
      component: Sessions
    },
    {
      path: '/session/:uuid',
      name: 'RedactionSession',
      component: RedactionSession
    }
  ]
})
