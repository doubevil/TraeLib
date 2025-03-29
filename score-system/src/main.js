import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

import App from './App.vue'
import router from './router'

// 导入 store
import { useScoreStore } from './store/score'
import { useRelationStore } from './store/relation'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(Antd)

// 初始化 store
const scoreStore = useScoreStore()
const relationStore = useRelationStore()

app.mount('#app')
