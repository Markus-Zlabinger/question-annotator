<template>
    <div>
        <AnswerList ref="answerlist"></AnswerList>
        <b-button @click="updateComponentData">click me</b-button>
    </div>

</template>


<script>
    import AnswerList from "../components/AnswerList";

    export default {
        components: {
            AnswerList,

        },
        data() {
            return {
                answer: "123",
            }
        },
        methods:
            {
                updateComponentData: function () {
                    //this.$refs.component.answer = "heeeeyho";
                }
            },
        mounted() {
           // this.$refs.component.answer = "super";
        }
    }
</script>

<style scoped>
    /*.custom-control-label::before ,.custom-control-label::after{width:120px; height:50px}*/
</style>