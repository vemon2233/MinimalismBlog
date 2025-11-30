import routes from '~pages'
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  // 不用pages的写法
  // routes: [{
  //   name: "Home",
  //   path: "/",
  //   'component': () => import('../pages/Home.vue')
  // }],

  // 用了pages就不用一个一个去写了
  routes: [
    // 默认使用Layout的路由
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: "/home",
      component: () => import('../Layout.vue'),
      children: routes.filter(route => !route.meta?.noLayout)
    },
    // 不使用Layout的独立路由，在vue页面上写入如下代码
    // <route>
    // {
    //   meta: {
    //     noLayout: true
    //   }
    // }
    // </route>
    ...routes.filter(route => route.meta?.noLayout).map(route => ({
      ...route,
      path: route.path
    }))
  ],
  history: createWebHistory()
})

// 全局前置守卫，在路由切换前执行
router.beforeEach((to, from, next) => {
  // 检查目标路由是否有 meta.title
  // <route>
  // {
  //   meta: {
  //     title: "Tailllll",
  //   }
  // }
  // </route>
  if (to.meta.title) {
      document.title = to.meta.title;
  }
  next();
})

export default router
