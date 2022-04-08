<template>
  <div>
    <div v-if="this.admin_value == 1">
      <Header />
    </div>
    <div v-else>
      <HeaderNoAdmin />
    </div>
    <section v-if="errored">
      <!-- <p>Error</p> -->
      <p>Error: {{ this.msg_error }}</p>
    </section>
    <section v-else>
      <div v-if="loading">
        Loading...
        <div
          class="spinner-border spinner-border-sm"
          style="width: 0.9rem; height: 0.9rem; border-width: 0.15em"
          role="status"
        ></div>
      </div>
      <div v-else>
        <div>
          <section v-if="errored_2">
            <p>{{ time }} {{ unit }} - Error: {{ this.msg_error_2 }}</p>
            <network
              class="diagram"
              ref="network"
              :nodes="nodes"
              :edges="edges"
              :options="options"
            />
          </section>
          <section v-else>
            <p>{{ time }} {{ unit }}</p>
            <network
              class="diagram"
              ref="network"
              :nodes="nodes"
              :edges="edges"
              :options="options"
            />
          </section>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";
import { Network } from "vue-visjs";
import Header from "@/components/Todo-Header.vue";
import HeaderNoAdmin from "@/components/Todo-HeaderNoAdmin.vue";
// import my_nodes from "@/json/nodes.json"; // Cargar datos desde archivo local
// import my_edges from "@/json/edges.json"; // Cargar datos desde archivo local
export default {
  name: "NetworkDiagram",
  components: {
    Network,
    Header,
    HeaderNoAdmin,
  },
  data: function () {
    return {
      admin_value: 0,
      // count: 200,
      loading: true,
      errored: false,
      errored_2: false,
      msg_error: "",
      msg_error_2: "",
      nodes: [],
      edges: [],
      time: [],
      unit: [],
      // nodes: my_nodes,
      // edges: my_edges,
      options: {
        // autoResize: true,
        // height: "100%",
        // width: "100%",
        // clickToUse: false,
        layout: {
          randomSeed: 10,
        },
        physics: {
          enabled: true,
          stabilization: false,
          // barnesHut: {
          //   springConstant: 0.9, // 0.9, 2
          //   // avoidOverlap: 1,
          // },
          // maxVelocity: 1,
          // minVelocity: 10,
          // solver: "barnesHut",
          // stabilization: {
          //   enabled: true,
          //   iterations: 1,
          //   onlyDynamicEdges: true,
          //   fit: true
          // },
          // timestep: 0.5,
          // adaptiveTimestep: true
        },
        nodes: {
          font: {
            size: 15,
            color: "#000000",
          },
          borderWidth: 1,
          shadow: true,
          // shape: "dot",
        },
        interaction: {
          dragNodes: true,
          tooltipDelay: 10,
        },
        // hierarchical: {
        //   enabled: true,
        //   // levelSeparation: 300, // does not seem to work, 150 default
        //   nodeSpacing: 250, // 100 default
        //   direction: "UD", // UD, DU, LR, RL
        //   sortMethod: "directed", // hubsize, directed
        // },
      },
      url: process.env.VUE_APP_URL,
      port: process.env.VUE_APP_PORT,
      endpoint_diagram: process.env.VUE_APP_DIAGRAM,
      endpoint_permission_value: process.env.VUE_APP_PERMISSIONS,
    };
  },
  mounted() {
    // let endpoint = "/diagram";
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
      .get(this.url + this.port + this.endpoint_diagram, { headers })
      .then((response) => {
        // console.log("Estamos en axios.then()");
        // console.log("response.data = ");
        // console.log(response.data);
        // console.log("axios.then(): response.data.error");
        // console.log(response.data.error);
        // console.log("axios.then(): response.data.cant_errores");
        // console.log(response.data.cant_errores);
        if (response.data.error == "at_least_one_down") {
          this.errored_2 = true;
          if (response.data.cant_errores == 1) {
            this.msg_error_2 = "No se pudo conectar a 1 equipo. Revisar Logs";
          } else {
            this.msg_error_2 =
              "No se pudo conectar a " +
              response.data.cant_errores +
              " equipos. Revisar Logs";
          }
        }
        this.nodes = response.data.nodes;
        this.edges = response.data.edges;
        this.time = response.data.time;
        this.unit = response.data.unit;
      })
      .catch((error) => {
        // console.log("NetworkDiagram.vue: Sección axios.catch()");
        // console.log("error = ");
        // console.log(error);
        // console.log("error.response = ");
        // console.log(error.response);
        // console.log("error.response.data = ");
        // console.log(error.response.data);
        // console.log("error.response.data.detail = ");
        // console.log(error.response.data.detail);
        this.msg_error = error.response.data.detail;
        this.errored = true;
        if (error.response.data.detail == "Signature has expired.") {
          this.tokenAvailable = false;
          this.$router.push("/");
        }
        if (error.response.data.detail == "Not enough segments") {
          this.tokenPresent = false;
          this.tokenAvailable = true;
          this.$router.push("/");
        }
      })
      .finally(() => {
        this.loading = false;
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
  height: 570px;
}
section {
  margin: 1px 0 0;
}
</style>
