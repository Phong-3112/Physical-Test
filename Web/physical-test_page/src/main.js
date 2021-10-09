import { createApp,h } from 'vue'
import App from './App.vue'

//import { Plotly } from "@/index.js";
//Vue.component("plotly", Plotly);
const app  = createApp({
    render: ()=>h(App)
});
//app.component("plotly",Plotly)

app.mount("#app")