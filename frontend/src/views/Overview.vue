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
                            <!--                            class="align-items-center"-->
                            <b-list-group-item
                                    v-for="(question, question_index) in annotation.questions"
                                    :key="question_index">
                                {{question.question}}
                                <b-badge v-b-modal="group_index+ '_' + question_index"
                                         v-if="question.outlier.score < 0.0"
                                         href="#"
                                         :style="'background-color: ' + get_color(question.outlier.score)">
                                    Potential Outlier
                                    <!--                                    <b-button v-b-modal.my-modal>Show Modal</b-button>-->
                                    <b-modal v-bind:id="group_index+ '_' + question_index" hide-footer>
                                        <template v-slot:modal-title>
                                            <b>Question:</b> {{question.question}}
                                        </template>
                                        <b-list-group flush>
                                            <b-list-group-item>
                                                <b>Outlier Score:</b>
                                                {{(Math.abs(question.outlier.score.toFixed(3))*100).toFixed(1)}}%
                                            </b-list-group-item>
                                            <b-list-group-item><b>Labeled Answer
                                                ({{question.outlier.initial_label}}):</b> <span v-html="answer_dict[question.outlier.initial_label].answer"></span>
                                                <!-- TODO: Something goes wrong here -->

                                            </b-list-group-item>
                                            <b-list-group-item><b>Predicted Answer
                                                ({{question.outlier.predicted_label}}):</b>
                                                <span v-html="answer_dict[question.outlier.predicted_label].answer"></span>
                                            </b-list-group-item>
                                        </b-list-group>
                                    </b-modal>
                                </b-badge>

                                <b-button @click="modify_annotation(question.qid, question.outlier.initial_label)"
                                          variant="outline-secondary"
                                          class="float-right btn-sm modifyannotation">
                                    &bull;&bull;&bull;
                                </b-button>
                            </b-list-group-item>
                        </b-list-group>
                    </b-card>
                </b-card-group>
            </b-row>
            <!-- MODIFY QUESTION MODAL -->
            <b-modal v-model="showModify" scrollable hide-footer>
                <template v-slot:modal-title>
                    Modify
                </template>
                <b-list-group flush>
                    <b-list-group-item>
                        <b>Question:</b> {{questions[modify_qid]}}
                    </b-list-group-item>
                    <b-list-group-item>
                        <b>Current Label:</b> {{modify_aid}}
                    </b-list-group-item>
<!--                    <b-list-group>-->
<!--                        <AnswerList ref="answerlist"></AnswerList>-->
<!--                    </b-list-group>-->
                    <b-list-group-item>
                        <b-button variant="danger" @click="delete_annotation(modify_qid, modify_aid)">Delete Annotation</b-button>
                        <!--                        <SaveAnnotation ref="saveannotation"></SaveAnnotation>-->
                        <!--                        <b-button variant="danger" @click="change_annotation(modify_qid, modify_aid)">Change Label-->
                        <!--                        </b-button>-->
                    </b-list-group-item>
                </b-list-group>
            </b-modal>
        </b-container>
    </div>
</template>

<script>
    import axios from "axios";
    // import AnswerList from "../components/AnswerList";
    import SaveAnnotation from "../components/SaveAnnotation";


    export default {
        components: {
            // AnswerList,
            // SaveAnnotation
        },

        data() {
            return {
                annotations: [],
                question_ids: [],
                questions: [],
                selected: "aid",
                options: [
                    {text: "Sort by Group", value: "group"},
                    {text: "Sort by Label", value: "aid"}
                ],
                boxtest: "",
                answer_dict: [],
                modify_qid: "",
                modify_aid: "",
                showModify: false,
            };
        },
        mounted() {
            this.generate_content()
        },
        methods: {
            modify_annotation(qid, aid) {
                this.modify_qid = qid;
                this.modify_aid = aid;
                this.showModify = true;
            },
            get_color(value) {
                value = Math.abs(value);
                if (value > 0.25)
                    return "hsl(0, 100%,50%)";
                if (value > 0.20)
                    return "hsl(0, 80%,50%)";
                if (value > 0.10)
                    return "hsl(0, 60%,50%)";
                if (value > 0.05)
                    return "hsl(0, 40%,50%)";
                return "hsl(0, 20%,50%)";
                // let hue = ((value) * 1000).toString(10);
                // console.log(["hsl(0,", hue,"%,50%)"].join(""));
                // return ["hsl(0,", hue,"%,50%)"].join("");
                // return "Hello";
            },
            delete_annotation(qid, aid) {
                const url = "http://127.0.0.1:5000/deleteannotation";
                const formData = new FormData();
                formData.append("aid", aid);
                formData.append("qid", qid);
                axios
                    .post(url, formData)
                    .then(response => {
                        this.showModify = false;
                        this.generate_content();
                    })
                    .catch(e => {
                        alert("Something went wrong! Please try again later.");
                    });
            },
            async change_annotation(qid) {
                let answerlabels = this.$refs.answerlist.get_active_answers();
                await this.$refs.saveannotation.change_annotation(this.questions[qid], qid, answerlabels);
                this.showModify = false;
                this.generate_content();
            },
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
                        this.answer_dict = response.data.answer_dict;
                        this.questions = response.data.questions;
                        this.question_ids = response.data.question_ids;
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
    .modifyannotation {
        /*color: rgba(0, 0, 0, 0.125);*/
        /*border-color: rgba(0, 0, 0, 0.125);*/
        /*color: black;*/
        /*border-color: black;*/
        color: grey;
        border-color: grey;
    }

    .justify-content-md-center {
        padding: 0 10px;
    }
</style>                                                                                                                                                                                                                                                                           