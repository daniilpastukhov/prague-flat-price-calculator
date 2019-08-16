import Vue from 'vue'
import Router from 'vue-router'
import Calculator from './views/Calculator.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'calculator',
      component: Calculator
    },
    {
      path: '/statistics',
      name: 'statistics',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: function () { 
        return import(/* webpackChunkName: "about" */ './views/Statistics.vue')
      }
    }
  ]
})
