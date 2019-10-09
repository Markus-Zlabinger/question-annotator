<template>
  <header class="header">
    <span class="title">
        <b>GWAT</b>
         - A
        <b>G</b>roup
        <b>W</b>ise
        <b>A</b>nnotation
        <b>T</b>ool
    </span>
    <div id="nav">
       <router-link to="/">About</router-link> |
       <router-link to="/clusters">Clusters</router-link> |
       <router-link to="/annotation">Annotation</router-link> |
       <router-link to="/overview">Overview</router-link>
     </div>
  </header>
</template>

<script>
export default {
  name: "Header"
}
</script>

<style scoped>
  .header {
    background: #333;
    color: #fff;
    text-align: center;
    padding: 10px;
  }
  .header a {
    color: #fff;
    padding-right: 5px;
    text-decoration: none;
  }
  .title {
      font-size: 24px;
  }
</style>