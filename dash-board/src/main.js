import Vue from 'vue'
import App from './App.vue'
import JsonExcel from 'vue-json-excel'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false
Vue.component('downloadExcel', JsonExcel)

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
