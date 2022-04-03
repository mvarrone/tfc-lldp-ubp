<template>
  <div class="history">
    <Header />
    <div v-if="!tokenPresent">Token not present</div>
    <div v-if="!tokenAvailable">Token expired</div>
    <div id="app">
      <div v-if="empty_response">Nothing to show</div>
      <splitpanes vertical style="height: 575px" v-if="!empty_response">
        <pane :size="20">
          <div class="table-wrapper-scroll-y my-custom-scrollbar">
            <table class="table table-striped table-hover" v-if="tokenPresent">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">date</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(value, index) in response_list"
                  v-bind:key="value.id"
                  v-on:click="clickRow(index + 1)"
                >
                  <th scope="row">{{ index + 1 }}</th>
                  <td>{{ value.date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </pane>
        <pane :size="80">
          <div>
            <network
              class="diagram"
              ref="network"
              :nodes="nodes"
              :edges="edges"
              :options="options"
            />
          </div>
        </pane>
      </splitpanes>
    </div>
    <br />
  </div>
</template>

<script>
import axios from "axios";
import Header from "@/components/Todo-Header.vue";
import { Splitpanes, Pane } from "splitpanes";
import "splitpanes/dist/splitpanes.css";
import { Network } from "vue-visjs";
export default {
  components: {
    Header,
    Splitpanes,
    Pane,
    Network,
  },
  data() {
    return {
      empty_response: false,
      id: 0,
      nodes: [],
      edges: [],
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
      tokenPresent: false,
      tokenAvailable: false,
      response_list: [],
      url: process.env.VUE_APP_URL,
      port: process.env.VUE_APP_PORT,
      endpoint_name_list: process.env.VUE_APP_NAMELIST,
      endpoint_get_diagram_info_by_id: process.env.VUE_APP_DIAGRAMINFO,
    };
  },
  methods: {
    clickRow(index) {
      // console.log("ID selected = ", index);
      this.id = index;
      // let endpoint = "/get_diagram_info_by_id/{id}";
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
            this.endpoint_get_diagram_info_by_id +
            "/" +
            this.id,
          {
            headers,
          },
          {
            id: this.id,
          }
        )
        .then((response) => {
          // console.log(response.data);
          // console.log(response.data.nodes);
          // console.log(response.data.edges);
          this.nodes = response.data.nodes;
          this.edges = response.data.edges;
        })
        .catch((error) => {
          // console.log("Todo-History.vue: Section axios.catch()");
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
  },
  mounted() {
    // let endpoint = "/get_diagram_name_list";
    let token = localStorage.getItem("token");
    if (token) {
      this.tokenPresent = true;
      this.tokenAvailable = true;
    }
    const headers = {
      Authorization: "Bearer " + token,
    };
    axios
      .get(this.url + this.port + this.endpoint_name_list, { headers })
      .then((response) => {
        if (response.data.length == 0) {
          this.empty_response = true;
        } else {
          this.response_list = response.data;
          this.empty_response = false;
        }
      })
      .catch((error) => {
        // console.log("Todo-History.vue: Sección axios.catch()");
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

<style scoped lang="scss">
.multipane.foo.layout-v .multipane-resizer {
  margin: 0;
  left: 0; /* reset default styling */
  width: 15px;
  background: rgb(255, 255, 255);
}

.multipane.foo.layout-h .multipane-resizer {
  margin: 0;
  top: 0; /* reset default styling */
  height: 15px;
  background: rgb(255, 255, 255);
}

.diagram {
  height: 575px;
  width: auto;
}

.my-custom-scrollbar {
  position: relative;
  height: 575px;
  overflow: auto;
}

.table-wrapper-scroll-y {
  display: block;
}
</style>



