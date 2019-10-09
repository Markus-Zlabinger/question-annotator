<template>
  <div role="tablist">
    <b-card v-for="(cluster, index) in clusters" v-bind:key="index" no-body class="mb-1">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-button block href="#" v-b-toggle="'accordion-' + index" variant="info">{{cluster.name}}</b-button>
      </b-card-header>
      <b-collapse :id="getAccordionID(index)" accordion="my-accordion" role="tabpanel">
        <b-card-body>
          <b-card-text>
              <ul class="questionList">
                <li class="question" v-for="question in cluster.questions" :key=question.name>
                    <b>{{ question.name }}</b>: {{ question.text }}
                </li>
              </ul>
          </b-card-text>
        </b-card-body>
      </b-collapse>
    </b-card>
  </div>
</template>

<script>
export default {
  name: "ClusterList",
  data() {
    return {
      clusters: [
        {
          name: "Cluster 1",
          questions: [
            {
              name: "Q-Pi",
              text: "What the fuck?"
            },
            {
              name: "Q-Pa",
              text: "What the heck?"
            },
            {
              name: "Q-Po",
              text: "WTF?"
            }
          ]
        },
        {
          name: "Cluster 2",
          questions: [
            {
              name: "Q-Ene",
              text: "What the fuck?"
            },
            {
              name: "Q-Mene",
              text: "What the heck?"
            },
            {
              name: "Q-Mu",
              text: "WTF?"
            }
          ]
        }
      ]
    };
  },
  methods: {
    getAccordionID(index) {
      return "accordion-" + index;
    }
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