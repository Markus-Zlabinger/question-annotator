<template>
  <div class="LineChart">
    <div id="chart">
      <apexchart type="line" height="350" :options="chartOptions" :series="series" />
    </div>
  </div>
</template>

<script>
export default {
  name: "LineChart",
  data() {
    return {
      series: [{
            name: "Some Metric",
            data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
        }],
        chartOptions: {
          chart: {
                height: 350,
                zoom: {
                    enabled: false
                },
                 toolbar: {
                    show: false
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'straight'
            },
            title: {
                text: 'Some Metric per CLuster',
                align: 'left'
            },
            grid: {
                row: {
                    colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                    opacity: 0.5
                },
            }
        }
    };
  }
};
</script>

<style scoped>
.apexcharts-legend-text {
  font-size: 20px !important;
}

apexcharts-datalabels {
  font-size: 20px !important;
}
</style>