<template>
  <div class="logout">
    <Header />
  </div>
</template>

<script>
import axios from "axios";
import Header from "@/components/Todo-Header.vue";
export default {
  components: {
    Header,
  },
  data() {
    return {
      info: [],
      url: process.env.VUE_APP_URL,
      port: process.env.VUE_APP_PORT,
      endpoint_logout: process.env.VUE_APP_LOGOUT,
    };
  },
  mounted() {
    // let endpoint = "/logout";
    let token = localStorage.getItem("token");
    if (token) {
      this.tokenPresent = true;
      this.tokenAvailable = true;
    }
    const headers = {
      Authorization: "Bearer " + token,
    };
    axios
      .get(this.url + this.port + this.endpoint_logout, { headers })
      .then((response) => {
        this.info = response.data;
        this.$router.push("/");
      })
      .catch((error) => {
        // console.log("Logout.vue: Sección axios.catch()");
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.diagram {
  height: 600px;
}
</style>
