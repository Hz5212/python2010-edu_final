// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import axios from "axios";
Vue.prototype.$axios = axios;

import Element from "element-ui"
import "element-ui/lib/theme-chalk/index.css"

// 设置项目的全局样式
import "../static/css/global.css"

Vue.use(Element)

Vue.config.productionTip = false

// 让自定义配置生效
import settings from "./settings";
Vue.prototype.$settings = settings;

// 导入极验验证码
import "../static/js/gt"


// vue-video-player依赖
require('video.js/dist/video-js.css')
require('vue-video-player/src/custom-theme.css')
import VideoPlayer from 'vue-video-player'

Vue.use(VideoPlayer);

import store from "./store/index.js"

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
