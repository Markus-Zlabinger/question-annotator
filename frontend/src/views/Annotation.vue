<template>
    <div>
<!--        <h1>Annotation</h1>-->
        <b-container>
            <b-row class="justify-content-md-center">
                <b-col>
                  <span class="candidate">
                    <b>Candidate Question:</b>
                    {{candidate.question}}
                  </span>
                </b-col>
                <b-col>
                    <b-row>
                        <b-col>
                            <div class="submit_button">
                                <b-button variant="primary" size="lg" @click="save_annotation">Save Annotation</b-button>
                            </div>

                        </b-col>
                        <b-col>
                            <div class="custom-control custom-switch">
                                <input type="checkbox" class="custom-control-input" id="togglePreselect"
                                       @click="toggle_preselect_clicked()"
                                       v-model="toggle_preselect">
                                <label class="custom-control-label" for="togglePreselect">Preselect Clusters</label>
                            </div>
                        </b-col>
                        <b-col>
                            <b-alert v-model="annotation_success" variant="success" dismissible>
                                The candidate <b>'{{success_candidate}}'</b> and <b>{{success_num_annotations}}</b> other questions were annotated.
                            </b-alert>
                        </b-col>
                    </b-row>
                </b-col>
            </b-row>
            <b-row class="justify-content-md-center">
                <b-card-group deck header-tag="header">
                    <b-card align="center">
                        <template v-slot:header>
                            <b>Select questions</b>
                        </template>
                        <b-list-group>
                            <b-list-group-item
                                    v-for="(question, index) in ranked_questions"
                                    :key="index"
                                    @click="question_clicked(question, index)"
                                    :class="{'active': active_questions[index]}"
                                    button
                            >
                                <div class="question">{{question.question}}</div>
                                <div class="similarity">similarity: {{question.similarity.toFixed(2)}}</div>
                            </b-list-group-item>
                        </b-list-group>
                    </b-card>
                    <b-card align="center">
                        <template v-slot:header>
                            <b>Select answer(s)</b>
                        </template>
                        <b-list-group>
                            <b-list-group-item>
                                <label for="search_answers">
                                    <b>Search:</b>
                                </label>
                                <input id="search_answers" type="text" v-model="search_answers"/>
                            </b-list-group-item>
                            <b-list-group-item
                                    v-for="(answer, index) in filtered_answers"
                                    :key="index"
                                    @click="answer_clicked(index)"
                                    :class="{'active': selected_answer == index}"
                                    button
                            >
                                <div class="answer">
                                    <b>{{answer.aid}}</b>
                                    {{answer["answer-short"]}}: {{answer.answer}}
                                </div>
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
    import Multiselect from "vue-multiselect";
    import uuidv4 from "uuid/v4";

    export default {
        components: {
            Multiselect
        },
        data() {
            return {
                candidate: {},
                ranked_questions: [],
                active_questions: [],
                selected_questions: [],
                answers: [],
                search_answers: "",
                //selected_answers: [],
                selected_answer: -999,
                add_answer_short: "",
                add_answer_long: "",
                toggle_preselect: this.$store.state.preselect,
                annotation_success: false,
                success_num_annotations: 0,
                success_candidate: ""
            };
        },
        methods: {
            question_clicked(question, index) {
                this.$set(this.active_questions, index, !this.active_questions[index]);
            },
            answer_clicked(index) {
                this.selected_answer = index;
            },
            toggle_preselect_clicked() {
                this.$store.state.preselect = !this.$store.state.preselect
                this.render_active_questions()
                // this.active_questions = this.ranked_questions.map(question => {
                //     return event.target.checked && (question.preselect);
                // });
                // if (this.$store.state.preselect) {
                //     this.active_questions = this.ranked_questions.map(question => {
                //         return (this.$store.state.preselect) && (question.preselect);;
                //     });
                // } else {
                //     this.active_questions = this.ranked_questions.map(question => {
                //         return false;
                //     });
                // }
            },
            save_annotation() {
                if (this.selected_answer == -999 || isNaN(this.selected_answer)) {
                    alert("Please select an Answer");
                    window.scrollTo(0, 0);
                    return;
                }
                const url = "http://127.0.0.1:5000/saveannotation";
                const formData = new FormData();
                formData.append("labels", this.selected_answer);
                this.selected_questions = this.ranked_questions
                    .filter((question, i) => this.active_questions[i])
                    .map(question => question.qid);
                this.selected_questions.forEach(question => {
                    formData.append("questionlist[]", question);
                });
                formData.append("candidate", this.candidate.qid);
                this.success_num_annotations = this.selected_questions.length
                this.success_candidate = this.candidate.question
                axios
                    .post(url, formData)
                    .then(response => {
                        this.generate_content(response)
                        this.search_answers = "";
                        this.selected_answer = -999;
                        this.annotation_success = true
                        window.scrollTo(0, 0);
                    })
                    .catch(e => {
                        alert("Something went wrong! Please try again later.");
                    });
            },
            render_active_questions() {
                this.active_questions = this.ranked_questions.map(question => {
                    return this.$store.state.preselect && question.preselect;
                });
            },
            generate_content(response) {
                console.log(response.data);
                this.candidate = response.data.candidate;
                this.ranked_questions = response.data.ranked_questions;
                this.answers = response.data.answers;
                this.selected_answers = Array.apply(
                    null,
                    Array(this.answers.length)
                ).map(function () {
                });
                this.render_active_questions()
            },
        },
        mounted() {
            const url = "http://127.0.0.1:5000/candidate";
            axios
                .get(url)
                .then(response => {
                    this.generate_content(response)
                })
                .catch(e => {
                    console.log(e);
                });
        },
        computed: {
            filtered_answers() {
                return this.answers.filter(answer => {
                    return (
                        answer.answer
                            .toLowerCase()
                            .includes(this.search_answers.toLowerCase()) ||
                        answer["answer-short"]
                            .toLowerCase()
                            .includes(this.search_answers.toLowerCase())
                    );
                });
            }
        }
    };
</script>
<style scoped>
    .candidate {
        font-size: 20px;
    }

    .similarity {
        float: right;
    }

    .question {
        float: left;
    }

    .answer {
        text-align: left;
    }

    .add_news_answer {
        text-align: left;
    }

    .add_answer_button {
        margin-top: 10px;
    }

    .submit_button {
        /*   float: right !important;
        margin-top: 16px; */
        vertical-align: center;
    }

    .justify-content-md-center {
        padding: 10px;
    }
</style>

<!--           add_new_answer() {-->
<!--                if ((this.add_answer_short == "") | (this.add_answer_long == "")) {-->
<!--                    alert("Answer-short and/or answer missing!");-->
<!--                } else {-->
<!--                    const url = "http://127.0.0.1:5000/create_new_answer";-->
<!--                    const formData = new FormData();-->
<!--                    formData.append("answer", this.add_answer_long);-->
<!--                    formData.append("answer-short", this.add_answer_short);-->
<!--                    axios-->
<!--                        .post(url, formData)-->
<!--                        .then(response => {-->
<!--                            console.log(response.data);-->
<!--                            this.answers.push({-->
<!--                                aid: response.data.aid,-->
<!--                                "answer-short": this.add_answer_short,-->
<!--                                answer: this.add_answer_long-->
<!--                            });-->
<!--                            //this.selected_answers.push(true);-->
<!--                            this.selected_answer = this.answers.length - 1;-->
<!--                            this.add_answer_short = "";-->
<!--                            this.add_answer_long = "";-->
<!--                        })-->
<!--                        .catch(e => {-->
<!--                            alert("Something went wrong! Please try again later.");-->
<!--                        });-->
<!--                }-->
<!--            },-->

<!--     <b-list-group-item>-->
<!--                                <div class="add_news_answer">-->
<!--                                    <p>Add new answer</p>-->
<!--                                    <label for="add_answer_title">-->
<!--                                        <b>Answer-Short:</b>-->
<!--                                    </label>-->
<!--                                    <b-form-input id="add_answer_title" type="text" v-model="add_answer_short"></b-form-input>-->
<!--                                    <label for="add_answer_text">-->
<!--                                        <b>Answer:</b>-->
<!--                                    </label>-->
<!--                                    <b-form-input id="add_answer_text" type="text" v-model="add_answer_long"></b-form-input>-->
<!--                                    <b-button-->
<!--                                            class="add_answer_button"-->
<!--                                            block-->
<!--                                            variant="primary"-->
<!--                                            @click="add_new_answer"-->
<!--                                    >Add new answer-->
<!--                                    </b-button>-->
<!--                                </div>-->
<!--                            </b-list-group-item>-->