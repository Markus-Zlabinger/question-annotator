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
                            v-for="(annotation, group_index) in annotations"
                            :key="group_index"
                            :header="annotation.answer.aid"
                            align="left"
                    >
                        <b-list-group>
                            <b-list-group-item class="d-flex justify-content-between align-items-center"
                                               v-for="(question, question_index) in annotation.questions"
                                               :key="question_index">
                                {{question.question}}
                                <!-- IF OUTLIER IS DETECTED -->
                                <b-badge v-b-modal="group_index+ '_' + question_index"
                                         v-if="question.outlier.score < 0.0"
                                         href="#"
                                         variant="danger">
                                    Potential Outlier
                                    <!--                                    <b-button v-b-modal.my-modal>Show Modal</b-button>-->
                                    <b-modal v-bind:id="group_index+ '_' + question_index" hide-footer>
                                        <template v-slot:modal-title>
                                            <b>Question:</b> {{question.question}}
                                        </template>
                                        <b-list-group flush>
                                            <b-list-group-item><b>Labeled Answer
                                                ({{question.outlier.initial_label}}):</b>
                                                {{answers[question.outlier.initial_label]}}
                                            </b-list-group-item>
                                            <b-list-group-item><b>Predicted Answer
                                                ({{question.outlier.predicted_label}}):</b>
                                                {{answers[question.outlier.predicted_label]}}
                                            </b-list-group-item>
                                        </b-list-group>
                                    </b-modal>
                                </b-badge>
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
                selected: "aid",
                options: [
                    {text: "Sort by Group", value: "group"},
                    {text: "Sort by Label", value: "aid"}
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