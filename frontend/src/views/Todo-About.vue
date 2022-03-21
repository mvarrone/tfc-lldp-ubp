<template>
  <div class="about">
    <Header />
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
export default {
  components: {
    Header,
  },
  data() {
    return {
      info: [],
      url: process.env.VUE_APP_URL,
      port: process.env.VUE_APP_PORT,
      endpoint_about: process.env.VUE_APP_ABOUT,
    };
  },
  mounted() {
    // let endpoint = "/about";
    let token = localStorage.getItem("token");
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
