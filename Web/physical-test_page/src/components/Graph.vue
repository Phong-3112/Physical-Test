<template>
  <div class="graph">
    <Plotly
      :data="data"
      :layout="layout"
      :display-mode-bar="false"
    ></Plotly>
  </div>
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
  height: 670px;
  max-width: 800px;
  margin: 30px auto;
  overflow: auto;
  min-height: 300px;
  border: 1px solid steelblue;
  border-radius: 5px;
}
</style>