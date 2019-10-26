<template>
    <div id="app">
        <Header/>
        <router-view/>
    </div>
</template>

<script>
    import Vue from 'vue'
    import Header from './components/layout/Header'
    // eslint-disable-next-line no-unused-vars
    // import { MdSwitch } from 'vue-material/dist/components'
    // import 'vue-material/dist/vue-material.min.css'
    // import 'vue-material/dist/theme/default.css'

    // Vue.use(MdSwitch)
    export default {
        name: 'app',
        components: {
            Header
        }
    }
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        /*text-align: center;*/
        color: #2c3e50;
    }

    .container {
        max-width: 1920px !important;
    }
</style>
