<template>
  <div id="app">
    <div id="nav">
      <router-link to="/dashboard">Home</router-link> |
      <!-- <router-link to="/add">Add</router-link> | -->
      <!-- <router-link to="/modify">Modify</router-link> | -->
      <!-- <router-link to="/delete">Delete</router-link> | -->
      <router-link to="/inventory">Inventory</router-link> |
      <router-link to="/diagram">Diagram</router-link> |
      <!-- <router-link to="/logs">Logs</router-link> | -->
      <router-link to="/history">History</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/logout">Log out</router-link>
    </div>
    <router-view />
  </div>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 1px;

  a {
    font-weight: bold;
    color: #2c3e50;
    text-decoration: none;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
