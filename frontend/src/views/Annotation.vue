<template>
    <div>
        <h1>Annotation</h1>
        <button @click="testpost()">Test</button>
    </div>
</template>

<script>
import axios from "axios";
export default {
    methods: {
        testpost() {
            const url = "http://127.0.0.1:5000/testpost";
            const mypost = {
                "pi": "pa",
                "po": "pi"
            }

            axios
            .post(url, mypost)
            .then(response => {
                console.log(response.data)
            })
            .catch(e => {
                console.log(e);
            })
        }
    }
}
</script>

<style scoped>

</style>