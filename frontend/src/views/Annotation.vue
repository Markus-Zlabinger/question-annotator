<template>
  <div>
    <h1>Annotation</h1>
    <b-container>
      <b-row class="justify-content-md-center">
        <b-col sm>
          <span>
            <b>Candidate Question:</b>
            {{candidate.question}}
          </span>
        </b-col>
      </b-row>
      <b-row class="justify-content-md-center">
        <b-card-group deck>
          <b-card header="Select similar question(s)">
            <b-list-group>
              <b-list-group-item v-for="(question, index) in ranked_questions" :key="index" @click="question_clicked(index)" :class="{'active': selected_questions[index]}" button>
                <div class="question">{{question.question}}</div>
                <div class="similarity">{{question.similarity}}</div>
              </b-list-group-item>
            </b-list-group>
          </b-card>
          <b-card header="Select answer(s)">
            <b-list-group>
            <b-list-group-item>
                <label for="search_answers"><b>Search: </b></label>
                <input id="search_answers" type="text"  v-model="search_answers">
            </b-list-group-item>
              <b-list-group-item v-for="(answer, index) in filtered_answers" :key="index" @click="answer_clicked(index)" :class="{'active': selected_answers[index]}" button>
                <div class="answer">
                  <b>{{answer.aid}}</b>
                  {{answer.answer}}
                </div>
              </b-list-group-item>
              <b-list-group-item>
                  <div class="add_news_answer">
                    <p>Add new answer </p>
                    <label for="add_answer_title"><b>title: </b></label>
                    <b-form-input id="add_answer_title" type="text"  v-model="add_answer_title"></b-form-input>
                    <label for="add_answer_text"><b>text: </b></label>
                    <b-form-input id="add_answer_text" type="text"  v-model="add_answer_text"></b-form-input>
                    <b-button class="add_answer_button" block variant="primary" @click="add_new_answer">Add new answer</b-button>
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
      selected_questions: [],
      answers: [],
      search_answers: '',
      selected_answers: [], 
      add_answer_title: '',
      add_answer_text: ''
    };
  },
  methods: {
    question_clicked(index) {
        this.$set(this.selected_questions, index, !this.selected_questions[index])
    },
    answer_clicked(index) {
        this.$set(this.selected_answers, index, !this.selected_answers[index])
    }, 
    add_new_answer() {
        if(add_answer_title=="" | add_answer_text=="") {
            alert("New answer title or text missing!");
        }
        this.answers.push({aid: uuidv4(), answer: add_answer_title + ": " + add_answer_text});
        this.selected_answers.puhs(true);
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
  }, 
  computed: {
      filtered_answers() {
      return this.answers.filter(answer => {
        return answer.answer.toLowerCase().includes(this.search_answers.toLowerCase())
      })
    }
  }
};
</script>
<style scoped>
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
</style>