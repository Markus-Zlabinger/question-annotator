<template>
    <div>


        <h1 v-if="!candidate">All questions are annotated.</h1>
        <b-container v-if="candidate">
            <!-- CANDIDATE QUESTION -->
            <b-row class="justify-content-md-center">
                <b-col class="text-center">
                  <span v-if="candidate" class="candidate">
                    <b>Candidate Question:</b>
                    {{candidate.question}}
                  </span>
                </b-col>
                <b-col>
                    <b-row>
                        <!-- OPTION MENU -->
                        <b-col>
                            <div class="submit_button">
                                <b-button variant="primary" size="lg" @click="save_annotation">Save Annotation
                                </b-button>
                            </div>
                            <SaveAnnotation ref="saveannotation"></SaveAnnotation>
                        </b-col>
                    </b-row>
                </b-col>
            </b-row>
            <b-row class="justify-content-md-center">
                <b-card-group deck header-tag="header">
                    <!-- QUESTION LIST  -->
                    <b-card>
                        <template v-slot:header>
                            <b-row>
                                <b-col>
                                    <b>Select question(s)</b>
                                </b-col>
                                <b-col>
                                    <div class="custom-control custom-switch">
                                        <input type="checkbox" class="custom-control-input" id="togglePreselect"
                                               @click="toggle_preselect_clicked()"
                                               v-model="toggle_preselect">
                                        <label class="custom-control-label" for="togglePreselect">Preselect Clusters</label>
                                    </div>
                                </b-col>
                            </b-row>
                        </template>
                        <b-list-group>
                            <b-list-group-item
                                    v-for="(question, index) in ranked_questions"
                                    :key="index"
                                    @click="question_clicked(question, index)"
                                    :class="{'active': active_questions[index]}"
                                    button
                            >
                                <!--                                <div class="question">-->
                                {{question.qid}}: {{question.question}}
                                <b-badge variant="light" :style="'background-color: ' + ranked_questions_colorcodes[index]" class="float-right">
                                    {{question.similarity.toFixed(2)}}
                                </b-badge>
                            </b-list-group-item>
                        </b-list-group>
                    </b-card>

                    <!-- ANSWER LIST  -->
                    <AnswerList ref="answerlist"></AnswerList>
                </b-card-group>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    import axios from "axios";
    import AnswerList from "../components/AnswerList";
    import SaveAnnotation from "../components/SaveAnnotation";


    export default {
        components: {
            AnswerList,
            SaveAnnotation,
        },
        data() {
            return {
                candidate: {},
                ranked_questions: [],
                ranked_questions_colorcodes: [],
                active_questions: [],
                selected_questions: [],
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
            toggle_preselect_clicked() {
                this.$store.state.preselect = !this.$store.state.preselect;
                this.render_active_questions();
            },

            async save_annotation() {
                let questionlabels = this.ranked_questions
                    .filter((question, i) => this.active_questions[i])
                    .map(question => question.qid);
                questionlabels.push(this.candidate.qid)
                let answerlabels = this.$refs.answerlist.get_active_answers();
                let retval = await this.$refs.saveannotation.save_annotation(this.candidate.question, answerlabels, questionlabels);
                if (retval !== false) {
                    this.generate_content();
                }

            },
            getColor(value) {
                //value from 0 to 1
                let hue = ((value) * 120).toString(10);
                return ["hsl(", hue, ",100%,50%)"].join("");
            },
            render_active_questions() {
                this.active_questions = this.ranked_questions.map(question => {
                    return this.$store.state.preselect && question.preselect;
                });
            },

            generate_content() {
                const url = "http://127.0.0.1:5000/candidate";
                axios
                    .get(url)
                    .then(response => {
                        this.candidate = response.data.candidate;
                        this.ranked_questions = response.data.ranked_questions;
                        this.answers = response.data.answers;
                        this.ranked_questions_colorcodes = this.ranked_questions.map(question => {
                            return this.getColor(question.similarity);
                        });
                        // Change THis TODO
                        this.$refs.answerlist.qids = [];
                        this.$refs.answerlist.qids.push("47");
                        console.log(this.$refs.answerlist.qids)


                            // new Array(this.ranked_questions.length).fill("yellow");
                        // this.render_active_answers();
                        this.render_active_questions();
                    })
                    .catch(e => {
                        console.log(e);
                    });

            },
        },
        mounted() {
            this.generate_content();
        }
    }
</script>
<style scoped>
    .candidate {
        font-size: 20px;
    }

    .similarity {
        float: right;
    }

    /*.question {*/
    /*    float: left;*/
    /*}*/

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
