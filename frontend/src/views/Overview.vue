<template>
    <div>
        <!--        <h1>Overview</h1>-->
        <b-container>
            <b-row class="justify-content-md-center">
                <b-col>
                    <div class="submit_button">
                        <b-button variant="primary" size="lg" @click="reset_annotations()">Reset</b-button>
                    </div>
                </b-col>
                <b-col>
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
                </b-col>
            </b-row>
            <b-row class="justify-content-md-center">
                <b-card-group columns>
                    <b-card
                            v-for="(annotation, index) in annotations"
                            :key="index"
                            :header="annotation.answer['answer-short']"
                            align="left"
                    >
                        <b-list-group>
                            <b-list-group-item class="d-flex justify-content-between align-items-center"
                                               v-for="(question, index) in annotation.questions" :key="index">
                                {{question.question}}
                                <!-- IF OUTLIER IS DETECTED -->
                                <b-badge v-b-modal.my-modal v-if="question.outlier.score < 0.0" href="#" variant="danger">
                                    Potential Outlier
<!--                                    <b-button v-b-modal.my-modal>Show Modal</b-button>-->
                                    <b-modal id="my-modal" hide-footer>
                                        <template v-slot:modal-title>
                                            <b>Question:</b> {{question.question}}
                                        </template>
                                        <b-list-group flush>
                                            <b-list-group-item><b>Labeled Answer ({{question.outlier.initial_label}}):</b>
                                                {{answers[question.outlier.initial_label].answer}}
                                            </b-list-group-item>
                                            <b-list-group-item><b>Predicted Answer ({{question.outlier.predicted_label}}):</b>
                                                {{answers[question.outlier.predicted_label].answer}}
                                            </b-list-group-item>
                                        </b-list-group>
                                    </b-modal>
                                </b-badge>
                                <!--                                <div v-if="question.outlier.score < 0.0">-->
                                <!--                                    {{answers[question.outlier.predicted_label].answer}}-->
                                <!--                                </div>-->
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
                boxtest: "",
                answers: [],
            };
        },
        mounted() {
            this.generate_content()
        },
        methods: {
            generate_content() {
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
                        this.answers = response.data.answers;
                    })
                    .catch(e => {
                        console.log(e);
                    });
            },
            sort() {
                this.generate_content()
            },
            reset_annotations() {
                const url = "http://127.0.0.1:5000/reset";
                axios
                    .get(url)
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