<template>
  <div>
    <Header />
    <br />
    <h1>Add device</h1>
    <br />
    <form v-on:submit.prevent="validate_add_device_button">
      <div class="form-group row mx-sm-3">
        <label for="exampleFormControlSelect1" class="col-sm-4 col-form-label">
          device_type
        </label>
        <div class="col-md-4 mb-2">
          <select
            v-bind:class="['form-control', states.device_type]"
            id="exampleFormControlSelect1"
            v-model="info.device_type"
            @change="changeOnList($event)"
          >
            <option disabled value="">Select a device type</option>
            <option v-for="value in device_type_list" v-bind:key="value.id">
              {{ value.device_type }}
            </option>
          </select>
          <!-- <div class="invalid-feedback">device_type required</div> -->
        </div>
      </div>
      <div class="form-group row mx-sm-3">
        <label for="hostname" class="col-sm-4 col-form-label"> hostname </label>
        <div class="col-md-4 mb-2">
          <input
            type="text"
            class="form-control"
            v-bind:class="['form-control', states.hostname]"
            id="hostname"
            placeholder="hostname"
            v-model="info.hostname"
          />
          <!-- <div class="invalid-feedback">hostname required</div> -->
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
            v-bind:class="['form-control', states.port]"
            id="port"
            placeholder="port"
            v-model="info.port"
          />
          <!-- <div class="invalid-feedback">port required</div> -->
        </div>
      </div>
      <div class="form-group row mx-sm-3">
        <label for="username" class="col-sm-4 col-form-label"> username </label>
        <div class="col-md-4 mb-2">
          <input
            type="text"
            v-bind:class="['form-control', states.username]"
            id="username"
            placeholder="username"
            v-model="info.username"
          />
          <!-- <div class="invalid-feedback">username required</div> -->
        </div>
      </div>
      <div class="form-group row mx-sm-3">
        <label for="password" class="col-sm-4 col-form-label"> password </label>
        <div class="col-md-4 mb-2">
          <input
            type="password"
            v-bind:class="['form-control', states.password]"
            id="password"
            placeholder="password"
            v-model="info.password"
            autocomplete="off"
          />
          <!-- <div class="invalid-feedback">password required</div> -->
        </div>
      </div>
      <div class="form-group row mx-sm-3">
        <label for="secret" class="col-sm-4 col-form-label">
          secret (used by Cisco devices)
        </label>
        <div class="col-md-4 mb-2">
          <input
            type="password"
            v-bind:class="['form-control', states.secret]"
            id="secret"
            placeholder="secret"
            v-model="info.secret"
            autocomplete="off"
          />
          <!-- <div class="invalid-feedback">secret required</div> -->
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
            v-bind:class="['form-control', states.conn_timeout]"
            id="conn_timeout"
            placeholder="conn_timeout"
            v-model="info.conn_timeout"
          />
          <!-- <div class="invalid-feedback">conn_timeout required</div> -->
        </div>
      </div>
      <br />
      <input
        class="btn btn-primary"
        type="submit"
        value="Add"
        title="Add a device to db"
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
        device_type: "",
        hostname: "",
        port: "",
        username: "",
        password: "",
        secret: "",
        conn_timeout: "",
      },
      lista: [],
      contador: 0,
      error_msg: "",
      info: {
        device_type: "",
        hostname: "",
        port: "22",
        username: "",
        password: "",
        secret: "",
        conn_timeout: "5",
      },
      device_type_list: [],
      url: process.env.VUE_APP_URL,
      port: process.env.VUE_APP_PORT,
      endpoint_device_type_list: process.env.VUE_APP_DEVICE_TYPE_LIST,
      endpoint_add_device: process.env.VUE_APP_ADD_DEVICE,
    };
  },
  mounted() {
    // let endpoint = "/device_type_list";
    let token = localStorage.getItem("token");
    if (token) {
      this.tokenPresent = true;
      this.tokenAvailable = true;
    }
    const headers = {
      Authorization: "Bearer " + token,
    };
    axios
      .get(this.url + this.port + this.endpoint_device_type_list, { headers })
      .then((response) => {
        this.device_type_list = response.data;
      })
      .catch((error) => {
        // console.log("AddDevice.vue: Sección axios.catch()");
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
      this.$bvToast.toast("Device added successfully", {
        title: "Action OK",
        autoHideDelay: 2500,
      });
    },
    changeOnList(event) {
      this.elementSelected = event.target.value;
      // console.log(this.elementSelected);
      this.states.device_type = "";
    },
    validate_add_device_button() {
      this.lista = [];
      this.contador = 0;
      if (!this.info.device_type) {
        this.contador = this.contador + 1;
        this.lista = this.lista + this.contador + ") device_type is required\n";
        this.states.device_type = "is-invalid";
      } else {
        this.states.device_type = "";
      }
      if (!this.info.hostname) {
        this.contador = this.contador + 1;
        this.lista = this.lista + this.contador + ") hostname is required\n";
        this.states.hostname = "is-invalid";
      } else {
        this.states.hostname = "";
      }
      if (!this.info.port) {
        this.contador = this.contador + 1;
        this.lista = this.lista + this.contador + ") port is required\n";
        this.states.port = "is-invalid";
      } else {
        this.states.port = "";
      }
      if (!this.info.username) {
        this.contador = this.contador + 1;
        this.lista = this.lista + this.contador + ") username is required\n";
        this.states.username = "is-invalid";
      } else {
        this.states.username = "";
      }
      if (!this.info.password) {
        this.contador = this.contador + 1;
        this.lista = this.lista + this.contador + ") password is required\n";
        this.states.password = "is-invalid";
      } else {
        this.states.password = "";
      }
      if (
        this.info.device_type == "cisco_ios" ||
        this.info.device_type == "cisco_nxos" ||
        this.info.device_type == "cisco_s300" ||
        this.info.device_type == "cisco_xr"
      ) {
        if (!this.info.secret) {
          this.contador = this.contador + 1;
          this.lista = this.lista + this.contador + ") secret is required\n";
          this.states.secret = "is-invalid";
        } else {
          this.states.secret = "";
        }
      } else {
        this.states.secret = "";
      }
      if (!this.info.conn_timeout) {
        this.contador = this.contador + 1;
        this.lista = this.lista + this.contador + ") conn_timeout is required";
        this.states.conn_timeout = "is-invalid";
      } else {
        this.states.conn_timeout = "";
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
        this.add_device_button();
      }
    },
    add_device_button() {
      // let endpoint = "/add_device";
      // console.log("Ejecución del botón add_device_button()");
      // alert("Ejecución desde add_device_button()");
      let token = localStorage.getItem("token");
      if (token) {
        this.tokenPresent = true;
        this.tokenAvailable = true;
      }
      const headers = {
        Authorization: "Bearer " + token,
      };
      axios
        .post(
          this.url +
            this.port +
            this.endpoint_add_device +
            "/" +
            this.info.hostname,
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
          this.info.device_type = "";
          this.info.hostname = "";
          this.info.port = "22";
          this.info.username = "";
          this.info.password = "";
          this.info.secret = "";
          this.info.conn_timeout = "5";
          // alert("Device added successfully");
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
  },
};
</script>
