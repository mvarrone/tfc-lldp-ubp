<template>
  <div class="logs">
    <Header />
    <br />
    <h1>Logs</h1>
    <br />
    <div v-if="!tokenPresent">Token not present</div>
    <div v-if="!tokenAvailable">Token expired</div>
    <div id="app">
      <!-- <div class="container mt-1" id="app"> -->
      <table class="table table-striped table-hover" v-if="tokenPresent">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">date</th>
            <th scope="col">hour</th>
            <th scope="col">ip</th>
            <th scope="col">method</th>
            <th scope="col">path</th>
            <th scope="col">scheme</th>
            <th scope="col">error_type</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(value, index) in info_list"
            v-bind:key="value.id"
            v-on:click="
              clickRow(index + 1, value.error_descr, value.error_type)
            "
          >
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ value.date }}</td>
            <td>{{ value.hour }}</td>
            <td>{{ value.ip }}</td>
            <td>{{ value.method }}</td>
            <td>{{ value.path }}</td>
            <td>{{ value.scheme }}</td>
            <td>{{ value.error_type }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <br />
    <b-modal size="lg" v-model="modalShow" v-bind:title="titulo_modal" ok-only>
      {{ this.contenido_modal }}
    </b-modal>
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
      tokenPresent: false,
      tokenAvailable: false,
      info_list: [],
      modalShow: false,
      contenido_modal: "",
      titulo_modal: "",
      currentSort: "id_column",
      currentSortDir: "asc",
      url: process.env.VUE_APP_URL,
      port: process.env.VUE_APP_PORT,
      endpoint_logs: process.env.VUE_APP_LOGS,
    };
  },
  methods: {
    clickRow(index, error_descr, error_type) {
      // console.log("ID selected = ", index);
      this.modalShow = true;
      this.contenido_modal = error_descr;
      this.titulo_modal = index + " - " + error_type;
    },
  },
  mounted() {
    // let endpoint = "/logs";
    // const token =
    //   "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjQ2Njk4NjgxfQ.knHPGPnKQC8zmkOP8dZrn9_zo6IatBdy3DubBGgzcBQ"; // Token expirado para pruebas
    let token = localStorage.getItem("token");
    if (token) {
      this.tokenPresent = true;
      this.tokenAvailable = true;
    }
    const headers = {
      Authorization: "Bearer " + token,
    };
    axios
      .get(this.url + this.port + this.endpoint_logs, { headers })
      .then((response) => {
        this.info_list = response.data;
        // console.log(response.data);
      })
      .catch((error) => {
        // console.log("Logs.vue: Sección axios.catch()");
        // console.log("error = ");
        // console.log(error);
        // console.log("error.response = ");
        // console.log(error.response);
        // console.log("error.response.data = ");
        // console.log(error.response.data);
        // console.log("error.response.data.detail = ");
        // console.log(error.response.data.detail);
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
