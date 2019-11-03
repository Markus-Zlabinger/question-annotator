<template>
    <b-card>
        <template v-slot:header>
            <b-row class="text-center">
                <b-col>
                    <b>Select answer(s)</b>
                </b-col>
                <b-col>
                    <div class="custom-control custom-switch">
                        <input type="checkbox" class="custom-control-input" id="toggleMultipleanswers"
                               @click="toggle_multipleanswers_clicked()"
                               v-model="$store.state.multipleanswers">
                        <label class="custom-control-label" for="toggleMultipleanswers">Multiple Answers</label>
                    </div>
                </b-col>
            </b-row>
        </template>

        <b-list-group>
            <b-list-group-item class="text-center">
                <b-form-input type="text" placeholder="Prefix Search" v-model="search_answers"
                              label-cols-sm="3"></b-form-input>
            </b-list-group-item>
            <b-list-group-item
                    v-for="(answer, index) in filtered_answers"
                    :key="index"
                    @click="answer_clicked(index)"
                    :class="{'active': active_answers[index]}"
                    button
            >
                <div class="answer">
                    <b>{{answer.aid}}: </b>
                    <span v-html="answer.answer"></span>
                    <b-badge variant="light" :style="'background-color: ' + getColor(answer.similarity)"
                             class="float-right">
                        {{answer.similarity.toFixed(2)}}
                    </b-badge>
                </div>
            </b-list-group-item>
        </b-list-group>
    </b-card>
</template>


<script>
    import axios from "axios";

    export default {
        name: 'AnswerList',
        data() {
            return {
                search_answers: "",
                answers: [],
                active_answers: [],
                qids: [],
            };
        },
        mounted() {
            const url = "http://127.0.0.1:5000/getanswers";
            const formData = new FormData();
            this.qids.forEach(qid => {
                formData.append("qids[]", qid);
            });
            console.log(this.qids)
            // console.log("LOOOL")
            // formData.append("qids[]", "47");
            // formData.append("qids[]", "48");
            // formData.append("qids[]", "49");
            axios
                .post(url, formData)
                .then(response => {
                    console.log(response.data);
                    this.answers = response.data.answers;
                    this.reset_active_answers();
                })
                .catch(e => {
                    console.log(e);
                })
        },
        methods: {
            reset_active_answers() {
                this.active_answers = new Array(this.answers.length).fill(false);
            },
            answer_clicked(index) {
                if (this.$store.state.multipleanswers === false) {
                    this.reset_active_answers()
                }
                this.$set(this.active_answers, index, !this.active_answers[index]);
            },
            get_active_answers() {
                let active_answers = [];
                this.answers.forEach((answer, index) => {
                    if (this.active_answers[index]) {
                        active_answers.push(answer.aid)
                    }
                });
                if (active_answers.length > 0) {
                    this.search_answers = "";
                }
                return active_answers
            },
            toggle_multipleanswers_clicked() {
                this.reset_active_answers();
            },
            getColor(value) {
                //value from 0 to 1
                let hue = ((value) * 120).toString(10);
                return ["hsl(", hue, ",100%,50%)"].join("");
            },
        },
        computed: {
            filtered_answers() {
                return this.answers.filter(answer => {
                    return (
                        answer.answer
                            .toLowerCase()
                            .includes(this.search_answers.toLowerCase()) ||
                        answer.aid
                            .toLowerCase()
                            .includes(this.search_answers.toLowerCase())
                    );
                });
            }
        }
    }


</script>

<style scoped>
</style>