import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router';

import RenderComponents from './components/index.tsx'

const routercfg = [
    { path: '/login', component: () => import('./pages/login.vue') },
    { path: '/forget-password', component: () => import('./pages/forgetpws.vue') },
    { path: '/change-password', component: () => import('./pages/changepassword.vue') },
]

const routes = [
  {
    path: '/',
    redirect: '/login',
    // component: RenderComponents,
    children: [...routercfg],
  },
  {
    path: '/CHANGELOG',
    component: () => import('./pages/CHANGELOG.vue')
  },
  {
    path: '/changelog',
    component: () => import('./pages/CHANGELOG.vue')
  },
  {
    path: '/:w+',
    redirect: '/',
  },
];

const routerConfig = {
  history: createWebHashHistory(),
  routes,
  scrollBehavior(to, from) {
    if (to.path !== from.path) {
      return { top: 0 };
    }
  },
};

const router = createRouter(routerConfig);

export default router;
