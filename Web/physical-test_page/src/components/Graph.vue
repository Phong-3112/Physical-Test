<template>
        <Plotly class="graph"
            :data="data"
            :layout="layout"
            :display-mode-bar="false"
        >Graph</Plotly>
</template>

<script>
import Plotly from './Plotly.vue'
//import Form from './Form.vue'

export default {
  components: {
    Plotly,
//    Form
  },
  props:{
    data: Array,
    layout: Object,
  },
}
</script>

<style>
.graph {
  height: 800px;
  max-width: 500px;
  margin: 30px auto;
  overflow: auto;
  min-height: 300px;
  border: 1px solid steelblue;
  padding: 30px;
  border-radius: 5px;
}
</style>