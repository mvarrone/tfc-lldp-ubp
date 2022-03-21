<template>
  <div>
    <Header />
    <!-- Este es el dashboard -->
    <HelloWorld msg="Monitoring system through LLDP" />
    <!-- <HelloWorld msg="LLDP" /> -->
  </div>
</template>

<script>
import axios from "axios";
import Header from "@/components/Todo-Header.vue";
import HelloWorld from "@/components/HelloWorld.vue";
export default {
  name: "TodoDashboard",
  components: {
    Header,
    HelloWorld,
  },
  data() {
    return {
      info: [],
      url: process.env.VUE_APP_URL,
      port: process.env.VUE_APP_PORT,
      endpoint_dashboard: process.env.VUE_APP_DASHBOARD,
    };
  },
  mounted() {
    // let endpoint = "/dashboard";
    let token = localStorage.getItem("token");
    if (token) {
      this.tokenPresent = true;
      this.tokenAvailable = true;
    }
    const headers = {
      Authorization: "Bearer " + token,
    };
    axios
      .get(this.url + this.port + this.endpoint_dashboard, { headers })
      .then(response => {
        this.info = response.data;
      })
      .catch(error => {
        // console.log("Dashboard.vue: Sección axios.catch()");
        // console.log("error = ");
        // console.log(error);
        if (error.response.data.detail == "Signature has expired.") {
          // console.log("Token expirado");
          // alert("Token has expired");
          this.tokenAvailable = false;
          this.$router.push("/");
        }
        if (error.response.data.detail == "Not enough segments") {
          // console.log("Not enough segments");
          // alert("Not enough segments");
          this.tokenPresent = false;
          this.tokenAvailable = true;
          this.$router.push("/");
        }
      });
  },
};
</script>
<style lang="stylus" scoped></style>
