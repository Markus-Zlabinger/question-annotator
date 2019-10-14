<template>
  <div role="tablist">
    <b-card v-for="cluster in clusters" v-bind:key="index" no-body class="mb-1">
      lol
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-button block href="#" v-b-toggle="'accordion-' + index" variant="info">{{cluster.cluster}}</b-button>
      </b-card-header>
      <b-collapse :id="getAccordionID(index)" accordion="my-accordion" role="tabpanel">
        <b-card-body>
          <b-card-text>
              <ul class="questionList">

                <li class="question" v-for="question in cluster.questions" :key=index>
                    <b>Q-{{index}}</b>: {{ question.text }}
                </li>
              </ul>
          </b-card-text>
        </b-card-body>
      </b-collapse>
    </b-card>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "ClusterList",
  data() {
    return {
       clusters: []
    }; 
  },
  methods: {
    getAccordionID(index) {
      return "accordion-" + index;
    }
  }, 
  mounted() {
    const url = "http://127.0.0.1:5000/getclusters";
    axios
    .get(url)
    .then(response => {
      console.log(response.data);
      this.clusters = response.data;
    })
    .catch(e => {
      console.log(e);
    })
  }
};
</script>

<style scoped>
.question {
    list-style-type: none;
    text-align: justify;
}
.questionList{
    padding: 0px;
    margin: 0px;
}
</style>