<template>
  <div>
    <div v-if="this.admin_value == 1">
      <Header />
    </div>
    <div v-else>
      <HeaderNoAdmin />
    </div>
    <br />
    <h1>Inventory</h1>
    <br />
    <div id="app">
      <!-- <div class="container mt-1" id="app"> -->
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">device_type</th>
            <th scope="col">hostname</th>
            <th scope="col">port</th>
            <th scope="col">username</th>
            <!-- <th scope="col">password</th>
            <th scope="col">secret</th> -->
            <th scope="col">conn_timeout</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(value, index) in inventory_list" :key="value.id">
            <th scope="row">{{ index }}</th>
            <td>{{ value.device_type }}</td>
            <td>{{ value.host }}</td>
            <td>{{ value.port }}</td>
            <td>{{ value.username }}</td>
            <!-- <td>{{ value.password }}</td>
            <td>{{ value.secret }}</td> -->
            <td>{{ value.conn_timeout }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <br /><br />
  </div>
</template>

<script>
import axios from "axios";
import Header from "@/components/Todo-Header.vue";
import HeaderNoAdmin from "@/components/Todo-HeaderNoAdmin.vue";
export default {
  components: {
    Header,
    HeaderNoAdmin,
  },
  data() {
    return {
      admin_value: 0,
      inventory_list: [],
      url: process.env.VUE_APP_URL,
      port: process.env.VUE_APP_PORT,
      endpoint_inventory_list: process.env.VUE_APP_INVENTORY_LIST,
      endpoint_permission_value: process.env.VUE_APP_PERMISSIONS,
    };
  },
  mounted() {
    // let endpoint = "/inventory_list";
    let token = localStorage.getItem("token");

    this.check_value(token);

    if (token) {
      this.tokenPresent = true;
      this.tokenAvailable = true;
    }

    const headers = {
      Authorization: "Bearer " + token,
    };

    axios
      .get(this.url + this.port + this.endpoint_inventory_list, { headers })
      .then((response) => {
        this.inventory_list = response.data;
        // console.log(response.data);
      })
      .catch((error) => {
        // console.log("Inventory.vue: Sección axios.catch()");
        // console.log("error = ");
        // console.log(error);
        if (error.response.data.detail == "Signature has expired.") {
          this.tokenAvailable = false;
          this.$router.push("/");
        }
        if (error.response.data.detail == "Not enough segments") {
          this.tokenPresent = false;
          this.tokenAvailable = true;
          this.$router.push("/");
        }
      });
  },
  methods: {
    check_value(token) {
      const headers = {
        Authorization: "Bearer " + token,
      };
      axios
        .get(this.url + this.port + this.endpoint_permission_value, { headers })
        .then((response) => {
          this.admin_value = response.data;
        })
        .catch((error) => {
          if (error.response.data.detail == "Signature has expired.") {
            this.tokenAvailable = false;
            this.$router.push("/");
          }
          if (error.response.data.detail == "Not enough segments") {
            this.tokenPresent = false;
            this.tokenAvailable = true;
            this.$router.push("/");
          }
          if (error.response.status == 403) {
            this.$router.push("/dashboard");
          }
        });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.diagram {
  height: 600px;
}
</style>
