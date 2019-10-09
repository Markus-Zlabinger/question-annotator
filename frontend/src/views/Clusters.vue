<template>
  <div>
    <h1>Clusters</h1>
    <b-container class="bv-example-row">
      <b-row class="justify-content-md-center">
        <b-col sm>
            <ClusterList />
        </b-col>
        <b-col sm>
            <LineChart />
        </b-col>
      </b-row>
    </b-container>
   
  </div>
</template>

<script>
import ClusterList from "../components/ClusterList";
import LineChart from "../components/LineChart";
export default {
  components: {
    ClusterList,
    LineChart
  }
};
</script>

<style scoped>
</style>