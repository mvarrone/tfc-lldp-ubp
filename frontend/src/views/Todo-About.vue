<template>
  <div class="about">
    <div v-if="this.admin_value == 1">
      <Header />
    </div>
    <div v-else>
      <HeaderNoAdmin />
    </div>
    <br /><br /><br /><br />
    <br /><br />
    <h2>
      <a
        href="https://www.ubp.edu.ar/"
        target="_blank"
        rel="noopener noreferrer"
      >
        <img src="../assets/ubp_logo.png" alt="UBP Logo" />
      </a>
    </h2>
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
      info: [],
      url: process.env.VUE_APP_URL,
      port: process.env.VUE_APP_PORT,
      endpoint_about: process.env.VUE_APP_ABOUT,
      endpoint_permission_value: process.env.VUE_APP_PERMISSIONS,
    };
  },
  mounted() {
    // let endpoint = "/about";
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
      .get(this.url + this.port + this.endpoint_about, { headers })
      .then((response) => {
        this.info = response.data;
      })
      .catch((error) => {
        // console.log("About.vue: Sección axios.catch()");
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
