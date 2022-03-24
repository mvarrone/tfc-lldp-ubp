<template>
  <div>
    <Header />
    <br />
    <h1>Delete device</h1>
    <br />
    <form v-on:submit.prevent="validate_delete_device_button">
      <div class="form-group row mx-sm-3">
        <label for="exampleFormControlSelect1" class="col-sm-4 col-form-label">
        </label>
        <div class="col-md-4 mb-2">
          <select
            v-bind:class="['form-control', states.hostname_list_selected]"
            id="exampleFormControlSelect1"
            v-model="info.hostname"
            @change="changeOnList($event)"
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
      <input
        class="btn btn-primary"
        type="submit"
        value="Delete"
        title="Delete a device from db"
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
        hostname: "",
      },
      hostname_list: [],
      url: process.env.VUE_APP_URL,
      port: process.env.VUE_APP_PORT,
      endpoint_hostname_list: process.env.VUE_APP_HOSTNAME_LIST,
      endpoint_delete_device: process.env.VUE_APP_DELETE_DEVICE,
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
        // console.log("Delete.vue: Sección axios.catch()");
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
      this.$bvToast.toast("Device deleted successfully", {
        title: "Action OK",
        autoHideDelay: 2500,
      });
    },
    changeOnList(event) {
      this.elementSelected = event.target.value;
      // console.log(this.elementSelected);
      this.states.hostname_list_selected = "";
    },
    validate_delete_device_button() {
      this.lista = [];
      this.contador = 0;
      if (!this.info.hostname) {
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
        this.delete_device_button();
      }
    },
    delete_device_button() {
      // let endpoint = "/delete_device";
      // console.log("Ejecución del botón delete_device_button()");
      let token = localStorage.getItem("token");
      if (token) {
        this.tokenPresent = true;
        this.tokenAvailable = true;
      }
      const headers = {
        Authorization: "Bearer " + token,
      };
      axios
        .delete(
          this.url +
            this.port +
            this.endpoint_delete_device +
            "/" +
            this.info.hostname,
          { headers }
        )
        .then(() => {
          this.info.hostname = "";
          this.update_info_after_button_clicked();
        })
        .catch((error) => {
          // console.log("DeleteDevice.vue: Sección axios.catch()");
          // console.log("DeleteDevice.vue: Method delete_device_button()");
          // console.log("error = ");
          // console.log(error);
          // console.log("error.response = ");
          // console.log(error.response);
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
    update_info_after_button_clicked() {
      // let endpoint = "/hostname_list";
      // console.log("Ejecución del botón update_info_after_button_clicked()");
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
          this.makeToast();
        })
        .catch((error) => {
          // console.log("Delete.vue: Sección axios.catch()");
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
