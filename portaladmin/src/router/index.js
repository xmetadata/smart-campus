import Vue from 'vue'
import Router from 'vue-router'

// in development-env not use lazy-loading, because lazy-loading too many pages will cause webpack hot update too slow. so only in production use lazy-loading;
// detail: https://panjiachen.github.io/vue-element-admin-site/#/lazy-loading

Vue.use(Router)

/* Layout */
import Layout from '../views/layout/Layout'

/**
* hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
* alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
*                                if not set alwaysShow, only more than one route under the children
*                                it will becomes nested mode, otherwise not show the root menu
* redirect: noredirect           if `redirect:noredirect` will no redirct in the breadcrumb
* name:'router-name'             the name is used by <keep-alive> (must set!!!)
* meta : {
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
  }
**/
export const constantRouterMap = [
  { path: '/login', component: () => import('@/views/login/index'), hidden: true },
  { path: '/404', component: () => import('@/views/404'), hidden: true },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    name: 'Dashboard',
    hidden: true,
    children: [{
      path: 'dashboard',
      component: () => import('@/views/dashboard/index')
    }]
  },

  {
    path: '/node',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Node',
        component: () => import('@/views/node/index'),
        meta: { title: '资料管理', icon: 'tree' }
      }
    ]
  },

  {
    path: '/notice',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Notice',
        component: () => import('@/views/form/index'),
        meta: { title: '通知', icon: 'notice' }
      }
    ]
  },

  {
    path: '/payment',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Payment',
        component: () => import('@/views/form/index'),
        meta: { title: '缴费', icon: 'payment' }
      }
    ]
  },

  {
    path: '/card',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Card',
        component: () => import('@/views/form/index'),
        meta: { title: '一卡通', icon: 'card' }
      }
    ]
  },

  {
    path: '/attendance',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Attendance',
        component: () => import('@/views/form/index'),
        meta: { title: '考勤卡', icon: 'attendance' }
      }
    ]
  },

  {
    path: '/stats',
    component: Layout,
    redirect: '/stats/table',
    name: 'Stats',
    meta: { title: '报表统计', icon: 'example' },
    children: [
      {
        path: 'payment',
        name: 'Payment',
        component: () => import('@/views/table/index'),
        meta: { title: '缴费统计', icon: 'payment' }
      },
      {
        path: 'attendance',
        name: 'Attendance',
        component: () => import('@/views/tree/index'),
        meta: { title: '考勤统计', icon: 'tree' }
      }
    ]
  },

  { path: '*', redirect: '/404', hidden: true }
]

export default new Router({
  // mode: 'history', //后端支持可开
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})

