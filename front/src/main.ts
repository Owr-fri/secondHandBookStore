import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'
import './assets/main.css'
import './assets/icon/iconfont.css'
import axios from '@/common/js/axios.js'
import VueAxios from 'vue-axios'
import API from '@/common/js/API.js'
import { jsonp } from 'vue-jsonp'
import { createPinia } from 'pinia'
import lodash from 'lodash'

const pinia = createPinia()
const app = createApp(App)

app.config.globalProperties.$API = API
app.config.globalProperties.$VueJsonp = jsonp
app.config.globalProperties.$lodash = lodash

app.use(VueAxios, axios)
app.provide('axios', app.config.globalProperties.axios)
app.use(router)
app.use(pinia)
app.mount("#app")