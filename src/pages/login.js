import { createApp } from 'vue'
import App from './login.vue'
import TDesign from 'tdesign-vue-next';

import '../assets/main.css'

import 'tdesign-vue-next/es/style/index.css';

const app = createApp(App)
app.use(TDesign)
app.mount('#app')
