<template>
  <div>
    <h1>Overview</h1>
    <b-container>
      <b-row class="justify-content-md-center">
        <b-col sm>
          <div class="tablist" role="tablist">
            <b-card v-for="(annotation, index) in annotations" :key="index" no-body class="mb-1">
              <b-card-header header-tag="header" class="p-1" role="tab">
                <b-button
                  block
                  href="#"
                  v-b-toggle="'accordion-' + index"
                  variant="info"
                >Label: {{annotation.answer['answer-short']}}</b-button>
              </b-card-header>
              <b-collapse :id="getAccordionID(index)" accordion="my-accordion" role="tabpanel">
                <b-card-body>
                  <b-card-text>
                    <ul class="questionList">
                      <li
                        class="question"
                        v-for="(question, index) in annotation.questions"
                        :key="index"
                      >
                        <b>Q-{{question.qid}}</b>
                        : {{ question.question }}
                      </li>
                    </ul>
                  </b-card-text>
                </b-card-body>
              </b-collapse>
            </b-card>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      annotations: []
    };
  },
  methods: {
    getAccordionID(index) {
      return "accordion-" + index;
    }
  },
  mounted() {
    const url = "http://127.0.0.1:5000/get_overview";
    axios
      .get(url)
      .then(response => {
        console.log(response.data);
        this.annotations = response.data.annotations;
      })
      .catch(e => {
        console.log(e);
      });
  }
};
</script>

<style scoped>
</style>