import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Todo-Home.vue";
import NetworkDiagramView from "../views/NetworkDiagramView.vue";
import AddDevice from "../views/AddDevice.vue";
import ModifyDevice from "../views/ModifyDevice.vue";
import DeleteDevice from "../views/DeleteDevice.vue";
import Inventory from "../views/Todo-Inventory.vue";
import About from "../views/Todo-About.vue";
import Logs from "../views/Todo-Logs.vue";
import Dashboard from "../views/Todo-Dashboard.vue";
import Logout from "../views/Todo-Logout.vue";

// import { Network } from "vue-visjs";

Vue.use(VueRouter);
// Vue.component("network", Network);

const routes = [
  { path: "/", name: "Home", component: Home },
  { path: "/home", redirect: "/" },
  { path: "/diagram", name: "NetworkDiagram", component: NetworkDiagramView },
  { path: "/add", name: "AddDevice", component: AddDevice },
  { path: "/modify", name: "ModifyDevice", component: ModifyDevice },
  { path: "/delete", name: "DeleteDevice", component: DeleteDevice },
  { path: "/inventory", name: "Inventory", component: Inventory },
  { path: "/about", name: "About", component: About },
  { path: "/logs", name: "Logs", component: Logs },
  { path: "/dashboard", name: "Dashboard", component: Dashboard },
  { path: "/logout", name: "Logout", component: Logout },
  // { path: "/logout", redirect: "/" },
];

const router = new VueRouter({
  routes,
});

export default router;
