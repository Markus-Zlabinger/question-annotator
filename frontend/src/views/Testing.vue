<template>
    <div>
        <input
                type="checkbox"
                v-model="toggle"
                true-value="true"
                false-value="false"
        >
    </div>
</template>

<script>
    export default {
        data() {
            return {
                toggle: "no"
            };
        }
    }
</script>

<style scoped>
    /*.custom-control-label::before ,.custom-control-label::after{width:120px; height:50px}*/
</style>