import Vue from "vue";
import App from "./App.vue";
import router from "./router";
// import "bootstrap";
// import "bootstrap/dist/css/bootstrap.min.css";
// import BootstrapVue from "bootstrap-vue";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
// import BootstrapVue from "bootstrap-vue/dist/bootstrap-vue.esm";
// import "bootstrap-vue/dist/bootstrap-vue.css";
// import "bootstrap-vue/dist/bootstrap-vue.esm";
// Import Bootstrap an BootstrapVue CSS files (order is important)
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
// import "bootstrap/dist/css/bootstrap.css";
// import VuePassword from "vue-password";

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
// Vue.component(VuePassword);

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
