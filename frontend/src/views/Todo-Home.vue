<template>
  <div class="Home">
    <!-- <HelloWorld msg="Sistema de monitoreo a través de LLDP" /> -->
    <!-- <HelloWorld msg="LLDP" /> -->
    <div class="wrapper fadeInDown">
      <div id="formContent">
        <!-- Tabs Titles -->

        <!-- Icon -->
        <div class="fadeIn first">
          <img src="@/assets/ubp_logo.png" id="icon" alt="User Icon" />
        </div>

        <!-- Login Form -->
        <form v-on:submit.prevent="validate_log_in_button">
          <input
            type="text"
            id="login"
            class="fadeIn second"
            name="login"
            placeholder="username"
            v-model="creds.username"
            v-bind:class="['form-control', states.username]"
            autocomplete="off"
            @click="removeErrorDivUsername"
          />
          <!-- <input
            type="password"
            id="password"
            class="fadeIn third"
            name="login"
            placeholder="password"
            v-model="creds.password"
            v-bind:class="['form-control', states.password]"
            autocomplete="off"
          /> -->
          <!-- <input
            type="password"
            id="password"
            class="fadeIn third"
            name="login"
            placeholder="password"
            v-model="creds.password"
            v-bind:class="['form-control', states.password]"
            autocomplete="off"
          />
          <span class="input-group-text"
            ><i class="fa fa-eye-slash" aria-hidden="true"></i
          ></span> -->
          <div class="field has-addons">
            <div class="control is-expanded">
              <input
                v-if="showPassword"
                type="text"
                id="password"
                class="fadeIn third"
                name="login"
                placeholder="password"
                v-model="creds.password"
                v-bind:class="['form-control', states.password]"
                autocomplete="off"
                @click="removeErrorDivPassword"
              />
              <input
                v-else
                type="password"
                id="password"
                class="fadeIn third"
                name="login"
                placeholder="password"
                v-model="creds.password"
                v-bind:class="['form-control', states.password]"
                autocomplete="off"
                @click="removeErrorDivPassword"
              />
              <!-- <button class="button fadeIn third" @click="toggleShow">
                <span class="icon is-small is-right">
                  <i
                    class="fa"
                    :class="{
                      'fa-eye-slash': showPassword,
                      'fa-eye': !showPassword,
                    }"
                  ></i>
                </span>
              </button> -->
            </div>
          </div>
          <!-- <i style="font-size: 20px" class="fa">&#xf070;</i></span> -->
          <!-- <i class="fa fa-eye-slash" aria-hidden="true"></i> -->
          <!-- <vue-password
            type="password"
            id="password"
            class="fadeIn third"
            name="login"
            placeholder="password"
            v-model="creds.password"
            v-bind:class="['form-control', states.password]"
            autocomplete="off"
            disableStrength="true"
          >
          </vue-password> -->
          <input type="submit" class="fadeIn fourth" value="Log In" />
        </form>
        <div class="alert alert-danger" role="alert" v-if="creds.error">
          {{ creds.error_msg }}
        </div>
        <!-- Remind Password -->
        <!-- <div id="formFooter">
          <a class="underlineHover" href="#">Forgot Password?</a>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
import axios from "axios";
// import VuePassword from "vue-password";
export default {
  name: "TodoHome",
  components: {
    // VuePassword,
    // HelloWorld,
  },
  data() {
    return {
      showPassword: false,
      password: null,
      user: {
        email: "",
        password: "",
      },
      states: {
        username: "",
        password: "",
      },
      creds: {
        username: "",
        password: "",
        error: false,
        error_msg: "",
        success_msg: "",
      },
      info: [],
      url: process.env.VUE_APP_URL,
      port: process.env.VUE_APP_PORT,
      endpoint_home: process.env.VUE_APP_HOME,
      endpoint_token: process.env.VUE_APP_TOKEN,
    };
  },
  mounted() {
    // let endpoint = "/";
    localStorage.removeItem("token");

    axios
      .get(this.url + this.port + this.endpoint_home)
      .then((response) => {
        this.info = response.data;
        // console.log(this.info);
      })
      .catch(() => {
        // console.log("Home.vue: Sección axios.catch()");
        // console.log("error = ");
        // console.log(error);
      });
  },
  methods: {
    validate_log_in_button() {
      this.lista = [];
      this.contador = 0;
      if (!this.creds.username) {
        this.contador = this.contador + 1;
        this.lista = this.lista + this.contador + ") username is required\n";
        this.states.username = "is-invalid";
      } else {
        this.states.username = "";
      }
      if (!this.creds.password) {
        this.contador = this.contador + 1;
        this.lista = this.lista + this.contador + ") password is required\n";
        this.states.password = "is-invalid";
      } else {
        this.states.password = "";
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
        this.login();
      }
    },
    login() {
      // console.log(this.creds.username);
      // console.log(this.creds.password);
      let formData = new FormData();
      formData.append("username", this.creds.username);
      formData.append("password", this.creds.password);
      axios
        .post(this.url + this.port + this.endpoint_token, formData)
        .then((response) => {
          // console.log(response);
          // console.log(response.data);
          // console.log(response.data.admin_permissions);
          // console.log(response.request.status);
          if (response.request.status == 200) {
            // console.log("OK");
            this.creds.success_msg = "OK";
            this.creds.error = false;
            localStorage.token = response.data.access_token;
            this.$router.push("dashboard");
          }
        })
        .catch((error) => {
          // console.log(error);
          // console.log(error.response);
          // console.log(error.response.data);
          // console.log(error.response.data.detail);
          // alert(error);
          // alert(error.response);
          // alert(error.response.data);
          // alert(error.response.data.detail);
          if (error.response.request.status == 401) {
            // console.log(error.response.data.detail);
            this.creds.error = true;
            this.creds.error_msg = error.response.data.detail;
          }
        });
      this.creds.username = "";
      this.creds.password = "";
    },
    toggleShow() {
      this.showPassword = !this.showPassword;
    },
    removeErrorDivUsername() {
      this.creds.error = false;
    },
    removeErrorDivPassword() {
      this.creds.error = false;
    },
  },
};
</script>

<style scoped>
/* BASIC */
html {
  background-color: #56baed;
}
body {
  font-family: "Poppins", sans-serif;
  height: 100vh;
}
a {
  color: #92badd;
  display: inline-block;
  text-decoration: none;
  font-weight: 400;
}
h2 {
  text-align: center;
  font-size: 16px;
  font-weight: 600;
  text-transform: uppercase;
  display: inline-block;
  margin: 40px 8px 10px 8px;
  color: #cccccc;
}
/* STRUCTURE */
.wrapper {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  min-height: 100%;
  padding: 20px;
}
#formContent {
  -webkit-border-radius: 10px 10px 10px 10px;
  border-radius: 10px 10px 10px 10px;
  background: #fff;
  padding: 30px;
  width: 90%;
  max-width: 450px;
  position: relative;
  padding: 0px;
  -webkit-box-shadow: 0 30px 60px 0 rgba(0, 0, 0, 0.3);
  box-shadow: 0 30px 60px 0 rgba(0, 0, 0, 0.3);
  text-align: center;
}
#formFooter {
  background-color: #f6f6f6;
  border-top: 1px solid #dce8f1;
  padding: 25px;
  text-align: center;
  -webkit-border-radius: 0 0 10px 10px;
  border-radius: 0 0 10px 10px;
}
/* TABS */
h2.inactive {
  color: #cccccc;
}
h2.active {
  color: #0d0d0d;
  border-bottom: 2px solid #5fbae9;
}
/* FORM TYPOGRAPHY*/
input[type="button"],
input[type="submit"],
input[type="reset"] {
  background-color: #56baed;
  border: none;
  color: white;
  padding: 15px 80px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  text-transform: uppercase;
  font-size: 13px;
  -webkit-box-shadow: 0 10px 30px 0 rgba(95, 186, 233, 0.4);
  box-shadow: 0 10px 30px 0 rgba(95, 186, 233, 0.4);
  -webkit-border-radius: 5px 5px 5px 5px;
  border-radius: 5px 5px 5px 5px;
  margin: 5px 20px 40px 20px;
  -webkit-transition: all 0.3s ease-in-out;
  -moz-transition: all 0.3s ease-in-out;
  -ms-transition: all 0.3s ease-in-out;
  -o-transition: all 0.3s ease-in-out;
  transition: all 0.3s ease-in-out;
}
input[type="button"]:hover,
input[type="submit"]:hover,
input[type="reset"]:hover {
  background-color: #39ace7;
}
input[type="button"]:active,
input[type="submit"]:active,
input[type="reset"]:active {
  -moz-transform: scale(0.95);
  -webkit-transform: scale(0.95);
  -o-transform: scale(0.95);
  -ms-transform: scale(0.95);
  transform: scale(0.95);
}
input[type="text"],
input[type="password"] {
  background-color: #f6f6f6;
  border: none;
  color: #0d0d0d;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 5px;
  width: 85%;
  border: 2px solid #f6f6f6;
  -webkit-transition: all 0.5s ease-in-out;
  -moz-transition: all 0.5s ease-in-out;
  -ms-transition: all 0.5s ease-in-out;
  -o-transition: all 0.5s ease-in-out;
  transition: all 0.5s ease-in-out;
  -webkit-border-radius: 5px 5px 5px 5px;
  border-radius: 5px 5px 5px 5px;
}
input[type="text"]:focus,
input[type="password"]:focus {
  background-color: #fff;
  border-bottom: 2px solid #5fbae9;
}
input[type="text"]:placeholder,
input[type="password"]:placeholder {
  color: #cccccc;
}
/* ANIMATIONS */
/* Simple CSS3 Fade-in-down Animation */
.fadeInDown {
  -webkit-animation-name: fadeInDown;
  animation-name: fadeInDown;
  -webkit-animation-duration: 1s;
  animation-duration: 1s;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
}
@-webkit-keyframes fadeInDown {
  0% {
    opacity: 0;
    -webkit-transform: translate3d(0, -100%, 0);
    transform: translate3d(0, -100%, 0);
  }
  100% {
    opacity: 1;
    -webkit-transform: none;
    transform: none;
  }
}
@keyframes fadeInDown {
  0% {
    opacity: 0;
    -webkit-transform: translate3d(0, -100%, 0);
    transform: translate3d(0, -100%, 0);
  }
  100% {
    opacity: 1;
    -webkit-transform: none;
    transform: none;
  }
}
/* Simple CSS3 Fade-in Animation */
@-webkit-keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
@-moz-keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
.fadeIn {
  opacity: 0;
  -webkit-animation: fadeIn ease-in 1;
  -moz-animation: fadeIn ease-in 1;
  animation: fadeIn ease-in 1;

  -webkit-animation-fill-mode: forwards;
  -moz-animation-fill-mode: forwards;
  animation-fill-mode: forwards;

  -webkit-animation-duration: 1s;
  -moz-animation-duration: 1s;
  animation-duration: 1s;
}
.fadeIn.first {
  -webkit-animation-delay: 0.4s;
  -moz-animation-delay: 0.4s;
  animation-delay: 0.4s;
}
.fadeIn.second {
  -webkit-animation-delay: 0.6s;
  -moz-animation-delay: 0.6s;
  animation-delay: 0.6s;
}
.fadeIn.third {
  -webkit-animation-delay: 0.8s;
  -moz-animation-delay: 0.8s;
  animation-delay: 0.8s;
}
.fadeIn.fourth {
  -webkit-animation-delay: 1s;
  -moz-animation-delay: 1s;
  animation-delay: 1s;
}
/* Simple CSS3 Fade-in Animation */
.underlineHover:after {
  display: block;
  left: 0;
  bottom: -10px;
  width: 0;
  height: 2px;
  background-color: #56baed;
  content: "";
  transition: width 0.2s;
}
.underlineHover:hover {
  color: #0d0d0d;
}
.underlineHover:hover:after {
  width: 100%;
}
/* OTHERS */
*:focus {
  outline: none;
}
#icon {
  width: 60%;
}
</style>
