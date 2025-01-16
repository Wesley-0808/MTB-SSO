import { createApp } from 'vue'
import App from './index.vue'
import route from './router.ts'

import TDesign from 'tdesign-vue-next'


// 引入组件库全局样式资源
import 'tdesign-vue-next/es/style/index.css';

import './style.scss'
import './assets/main.css'

const app = createApp(App)

app.use(TDesign).use(route).mount('#sso')