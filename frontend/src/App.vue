<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Calculator</router-link>
      <router-link to="/statistics">Statistics</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;
    text-decoration: none;
    margin: 0 10px;
    &.router-link-exact-active {
      color: #c90000;
    }
  }
}
</style>
