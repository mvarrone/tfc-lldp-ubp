<template>
  <div>
    <Header />
    <br />
    <h1>Modify device</h1>
    <br />
    <form v-on:submit.prevent="validate_modify_device_button">
      <div class="form-group row mx-sm-3">
        <label for="exampleFormControlSelect1" class="col-sm-4 col-form-label">
        </label>
        <div class="col-md-4 mb-2">
          <select
            v-bind:class="['form-control', states.hostname_list_selected]"
            id="exampleFormControlSelect1"
            v-model="info.hostname_selected"
            @change="switchSelect($event)"
          >
            <option disabled value="">Select a hostname</option>
            <option v-for="value in hostname_list" v-bind:key="value.id">
              {{ value.host }}
            </option>
          </select>
          <div class="invalid-feedback">
            Please, select a hostname from the list
          </div>
        </div>
      </div>
      <br />
      <div class="form-group row mx-sm-3">
        <label for="hostname" class="col-sm-4 col-form-label"> hostname </label>
        <div class="col-md-4 mb-2">
          <input
            type="text"
            class="form-control"
            id="hostname"
            placeholder="hostname"
            v-model="info.hostname"
          />
        </div>
      </div>
      <div class="form-group row mx-sm-3">
        <label for="device_type" class="col-sm-4 col-form-label">
          device_type
        </label>
        <div class="col-md-4 mb-2">
          <input
            type="text"
            class="form-control"
            id="device_type"
            placeholder="device_type"
            v-model="info.device_type"
          />
        </div>
      </div>
      <div class="form-group row mx-sm-3">
        <label for="port" class="col-sm-4 col-form-label">
          port (default: 22)
        </label>
        <div class="col-md-4 mb-2">
          <input
            type="number"
            min="1"
            oninput="validity.valid||(value='')"
            class="form-control"
            id="port"
            placeholder="port"
            v-model="info.port"
          />
        </div>
      </div>
      <div class="form-group row mx-sm-3">
        <label for="username" class="col-sm-4 col-form-label"> username </label>
        <div class="col-md-4 mb-2">
          <input
            type="text"
            class="form-control"
            id="username"
            placeholder="username"
            v-model="info.username"
          />
        </div>
      </div>
      <div class="form-group row mx-sm-3">
        <label for="password" class="col-sm-4 col-form-label"> password </label>
        <div class="col-md-4 mb-2">
          <input
            type="password"
            class="form-control"
            id="password"
            placeholder="password"
            v-model="info.password"
            autocomplete="off"
          />
        </div>
      </div>
      <div class="form-group row mx-sm-3">
        <label for="secret" class="col-sm-4 col-form-label">
          secret (used by Cisco devices)
        </label>
        <div class="col-md-4 mb-2">
          <input
            type="password"
            class="form-control"
            id="secret"
            placeholder="secret"
            v-model="info.secret"
            autocomplete="off"
          />
        </div>
      </div>
      <div class="form-group row mx-sm-3">
        <label for="conn_timeout" class="col-sm-4 col-form-label">
          conn_timeout (default: 5 s)
        </label>
        <div class="col-md-4 mb-2">
          <input
            type="number"
            min="1"
            oninput="validity.valid||(value='')"
            class="form-control"
            id="conn_timeout"
            placeholder="conn_timeout"
            v-model="info.conn_timeout"
          />
        </div>
      </div>
      <br />
      <input
        class="btn btn-primary"
        type="submit"
        value="Modify"
        title="Modify device parameters from db"
      />
      <br /><br />
    </form>
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
      elementSelected: [],
      states: {
        hostname_list_selected: "",
      },
      lista: [],
      contador: 0,
      error_msg: "",
      info: {
        device_type: "",
        hostname: "",
        hostname_selected: "",
        port: "22",
        username: "",
        password: "",
        secret: "",
        conn_timeout: "5",
      },
      hostname_list: [],
      url: process.env.VUE_APP_URL,
      port: process.env.VUE_APP_PORT,
      endpoint_hostname_list: process.env.VUE_APP_HOSTNAME_LIST,
      endpoint_modify_device: process.env.VUE_APP_MODIFY_DEVICE,
      endpoint_device_values_to_modify:
        process.env.VUE_APP_DEVICE_VALUES_TO_MODIFY,
    };
  },
  mounted() {
    // let endpoint = "/hostname_list";
    // console.log("Ejecución desde mounted()");
    let token = localStorage.getItem("token");
    if (token) {
      this.tokenPresent = true;
      this.tokenAvailable = true;
    }
    const headers = {
      Authorization: "Bearer " + token,
    };
    axios
      .get(this.url + this.port + this.endpoint_hostname_list, { headers })
      .then((response) => {
        this.hostname_list = response.data;
        // console.log(response.data);
      })
      .catch((error) => {
        // console.log("ModifyDevice.vue: Sección axios.catch()");
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
  methods: {
    makeToast() {
      this.$bvToast.toast("Device modified successfully", {
        title: "Action OK",
        autoHideDelay: 2500,
      });
    },
    validate_modify_device_button() {
      // alert("aaaaaaaaaaaaa");
      this.lista = [];
      this.contador = 0;
      if (!this.info.hostname_selected) {
        this.contador = this.contador + 1;
        this.lista =
          this.lista + this.contador + ") selecting a hostname is required";
        this.states.hostname_list_selected = "is-invalid";
      } else {
        this.states.hostname_list_selected = "";
      }
      if (this.contador > 0) {
        if (this.contador == 1) {
          this.error_msg = this.contador + " error\n\n" + this.lista;
        }
        if (this.contador > 1) {
          this.error_msg = this.contador + " errors\n\n" + this.lista;
        }
        // alert(this.error_msg);
      }
      if (this.contador == 0) {
        this.modify_device_button();
      }
    },
    modify_device_button() {
      // let endpoint = "/modify_device";
      // console.log("Ejecución del botón modify_device_button()");
      let token = localStorage.getItem("token");
      if (token) {
        this.tokenPresent = true;
        this.tokenAvailable = true;
      }
      const headers = {
        Authorization: "Bearer " + token,
      };
      axios
        .put(
          this.url +
            this.port +
            this.endpoint_modify_device +
            "/" +
            // this.info.hostname,
            this.info.hostname_selected,
          {
            device_type: this.info.device_type,
            hostname: this.info.hostname,
            port: this.info.port,
            username: this.info.username,
            password: this.info.password,
            secret: this.info.secret,
            conn_timeout: this.info.conn_timeout,
          },
          { headers }
        )
        .then(() => {
          // console.log("Sección axios.then()");
          // console.log("result = ");
          // console.log(result);
          this.info.hostname = "";
          this.info.device_type = "";
          this.info.port = "22";
          this.info.username = "";
          this.info.password = "";
          this.info.secret = "";
          this.info.conn_timeout = "5";
          this.update_info_after_modify_button_clicked();
        })
        .catch((error) => {
          // console.log("Sección axios.catch()");
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
    update_info_after_modify_button_clicked() {
      // console.log("que");
      // let endpoint = "/hostname_list";
      // console.log("Ejecución desde update_info_after_modify_button_clicked()");
      let token = localStorage.getItem("token");
      if (token) {
        this.tokenPresent = true;
        this.tokenAvailable = true;
      }
      const headers = {
        Authorization: "Bearer " + token,
      };
      axios
        .get(
          this.url +
            this.port +
            this.endpoint_device_values_to_modify +
            "/" +
            this.info.hostname_selected,
          { headers },
          {
            hostname: this.info.hostname_selected,
          }
        )
        .then((result) => {
          // console.log("Sección axios.then()");
          // console.log("result = ");
          // console.log(result);
          // console.log("result.data = ");
          // console.log(result.data);
          this.info.device_type = result.data.device_type;
          this.info.hostname = result.data.host;
          this.info.port = result.data.port;
          this.info.username = result.data.username;
          this.info.conn_timeout = result.data.conn_timeout;
          this.makeToast();
        })
        .catch((error) => {
          // console.log("Sección axios.catch()");
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
    switchSelect(event) {
      this.selected = event.target.value;
      this.states.hostname_list_selected = "";
      // console.log(this.selected);
      // let endpoint = "/device_values_to_modify";
      // console.log("Ejecución de switchSelect(event)");
      let token = localStorage.getItem("token");
      if (token) {
        this.tokenPresent = true;
        this.tokenAvailable = true;
      }
      const headers = {
        Authorization: "Bearer " + token,
      };
      axios
        .get(
          this.url +
            this.port +
            this.endpoint_device_values_to_modify +
            "/" +
            this.info.hostname_selected,
          { headers },
          {
            hostname: this.info.hostname_selected,
          }
        )
        .then((result) => {
          // console.log("Sección axios.then()");
          // console.log("result = ");
          // console.log(result);
          // console.log("result.data = ");
          // console.log(result.data);
          this.info.device_type = result.data.device_type;
          this.info.hostname = result.data.host;
          this.info.port = result.data.port;
          this.info.username = result.data.username;
          this.info.conn_timeout = result.data.conn_timeout;
        })
        .catch((error) => {
          // console.log("Sección axios.catch()");
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
  },
};
</script>
