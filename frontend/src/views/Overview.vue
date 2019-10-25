<template>
    <div>
        <h1>Overview</h1>
        <b-container>
            <b-row class="justify-content-md-center">
                <b-form-group label="Select a sorting method">
                    <b-form-radio-group
                            id="btn-radios-2"
                            v-model="selected"
                            :options="options"
                            buttons
                            button-variant="outline-primary"
                            size="lg"
                            name="radio-btn-outline"
                            @input="sort()"
                    ></b-form-radio-group>
                </b-form-group>
            </b-row>
            <b-row class="justify-content-md-center">
                <b-card-group columns>
                    <b-card
                            v-for="(annotation, index) in annotations"
                            :key="index"
                            :header="annotation.answer['answer-short']"
                            border-variant="info"
                            header-bg-variant="info"
                            header-text-variant="white"
                            align="center"
                    >
                        <b-list-group>
                            <b-list-group-item v-for="(question, index) in annotation.questions" :key="index">
                                <div class="question">{{question.question}}</div>
                            </b-list-group-item>
                        </b-list-group>
                    </b-card>
                </b-card-group>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        data() {
            return {
                annotations: [],
                selected: "group",
                options: [
                    {text: "Sort by Group", value: "group"},
                    {text: "Sort by Label", value: "label"}
                ],
                boxtest: ""
            };
        },
        mounted() {
            const url = "http://127.0.0.1:5000/get_overview";
            axios
                .get(url, {
                    params: {
                        sort_by: this.selected
                    }
                })
                .then(response => {
                    console.log(response.data);
                    this.annotations = response.data.annotations;
                })
                .catch(e => {
                    console.log(e);
                });
        },
        methods: {
            sort() {
                const url = "http://127.0.0.1:5000/get_overview";
                axios
                    .get(url, {
                        params: {
                            sort_by: this.selected
                        }
                    })
                    .then(response => {
                        console.log(response.data);
                        this.annotations = response.data.annotations;
                    })
                    .catch(e => {
                        console.log(e);
                    });
            }
        }
    };
</script>

<style scoped>
    .justify-content-md-center {
        padding: 0 10px;
    }
</style>