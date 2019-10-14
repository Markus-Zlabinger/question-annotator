<template>
  <div>
    <h1>Annotation</h1>
    <b-container class="bv-example-row">
      <b-row class="justify-content-md-center">
        <b-col sm>
            <span>
                <b>Candidate Question: </b>
                {{candidate.question}}
            </span>
        </b-col>
      </b-row>
      <b-row class="justify-content-md-center">
        <b-col sm>
            <label class="typo__label">Select similar question(s):</label>
            <multiselect v-model="selected_questions" :options="ranked_questions" :multiple="true" :close-on-select="false" :clear-on-select="false" :preserve-search="true" placeholder="Pick some" label="question" track-by="question" :preselect-first="false" selectLabel="" selectedLabel="" /> 
        </b-col>
      </b-row>
      <b-row class="justify-content-md-center">
        <b-col sm>
            <label class="typo__label">Select/Add answer(s):</label>
            <multiselect v-model="selected_answers" tag-placeholder="Add this as new answer" placeholder="Search or add an answer" label="answer" track-by="answer" :options="answers" :multiple="true" :taggable="true" @tag="addAnswer" :preselect-first="false" :close-on-select="false" :clear-on-select="false" selectLabel="" selectedLabel="" />
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";
import Multiselect from "vue-multiselect";
import uuidv4 from 'uuid/v4';

export default {
  components: {
    Multiselect
  },
  data() {
    return {
      candidate: {},
      ranked_questions: [],
      selected_questions: [],
      answers: [],
      selected_answers: [],
    };
  },
  methods: {
   addAnswer (newAnswer) {
      const answer = {
        aid: uuidv4(),
        answer: newAnswer
      }
      this.answers.push(answer)
      this.selected_answers.push(answer)
    }
  },
  mounted() {
    const url = "http://127.0.0.1:5000/candidate";
    axios
      .get(url)
      .then(response => {
        console.log(response.data);
        this.candidate = response.data.candidate;
        this.ranked_questions = response.data.ranked_questions;
        this.answers = response.data.answers;
      })
      .catch(e => {
        console.log(e);
      });
  }
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style>
.multiselect__option {
    white-space: normal !important;
}
</style>